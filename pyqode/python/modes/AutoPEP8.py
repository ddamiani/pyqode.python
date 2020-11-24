# -*- coding: utf-8 -*-
"""
Contains the AutoPEP8 mode
"""
import re
import ast
import textwrap
import autopep8
from pyqode.core.api.mode import Mode
from pyqode.qt import QtGui
from pyqode.qt import QtCore


RETURN_KEYS = (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter)
_whitespace_only_re = re.compile('^[ \t]+$', re.MULTILINE)
_leading_whitespace_re = re.compile('(^[ \t]*)(?:[^ \t\n])', re.MULTILINE)


class AutoPEP8(Mode):

    """Automatically formats the code according to PEP8 when going from one
    line to another.
    """

    def __init__(self, lookbehind=1, **options):

        self._lookbehind = lookbehind
        self._options = options
        super(AutoPEP8, self).__init__()

    def on_state_changed(self, state):

        if state:
            self.editor.key_pressed.connect(self._on_key_pressed)
        else:
            self.editor.key_pressed.disconnect(self._on_key_pressed)

    def _on_key_pressed(self, event):

        tc = self.editor.textCursor()
        if (
            event.key() not in RETURN_KEYS or
            not self.editor.use_spaces_instead_of_tabs or
            tc.hasSelection()
        ):
            return
        # We first get the previous line, dedent it, check if either ends with 
        # colon or is valid Python code. If so, the code is cleaned. If not, 
        # we get the previous two lines, dedent them, check if it's valid 
        # Python and if so, clean it. And so on, until the maximum number of 
        # lines is reached (lookbehind). Empty lines are not cleaned.
        tc.movePosition(tc.StartOfBlock, tc.KeepAnchor)
        for lookbehind in range(self._lookbehind):
            tc.movePosition(tc.PreviousBlock, tc.KeepAnchor)
            indentation, code = self._dedent(
                tc.selectedText().replace(u'\u2029', u'\n')
            )
            if code.isspace():  # Ignore empty lines
                return
            # If the first line ends with a colon, then it's not valid Python 
            # but we still fix it.
            if not lookbehind and code.rstrip().endswith(':'):
                break
            try:
                ast.parse(code)
            except SyntaxError:
                continue
            else:
                break
        else:
            return
        clean_code = textwrap.indent(
            autopep8.fix_code(code, options=self._options),
            prefix=indentation
        )
        # Make sure that no extraneous line ending is appended
        if (not code.endswith('\n') and clean_code.endswith('\n')):
            clean_code = clean_code[:-1]
        if clean_code == code:  # Do nothing if nothing changed
            return
        tc.insertText(clean_code.replace(u'\n', u'\u2029'))
        self.editor.setTextCursor(tc)

    def _dedent(self, text):
        
        """Modified to return margin (i.e. the indentation). Original:
        https://github.com/python/cpython/blob/3.9/Lib/textwrap.py
        """
    
        # Look for the longest leading string of spaces and tabs common to
        # all lines.
        margin = None
        text = _whitespace_only_re.sub('', text)
        indents = _leading_whitespace_re.findall(text)
        for indent in indents:
            if margin is None:
                margin = indent
            # Current line more deeply indented than previous winner:
            # no change (previous winner is still on top).
            elif indent.startswith(margin):
                pass
            # Current line consistent with and no deeper than previous winner:
            # it's the new winner.
            elif margin.startswith(indent):
                margin = indent
            # Find the largest common whitespace between current line and previous
            # winner.
            else:
                for i, (x, y) in enumerate(zip(margin, indent)):
                    if x != y:
                        margin = margin[:i]
                        break
        if margin:
            text = re.sub(r'(?m)^' + margin, '', text)
        return margin, text
