

**Bugfix maintenance only**

.. image:: https://raw.githubusercontent.com/pyQode/pyQode/master/media/pyqode-banner.png


About
-----

This is a fork of PyQode, which is now developed as the editor component for Rapunzel and OpenSesame. The original PyQode repository (<= v2) is no longer maintained.

*pyqode.python* adds **python** support to `pyQode`_ (code completion,
calltips, ...).


Features:
---------

* calltips mode (using `Jedi`_)
* code completion provider (using `Jedi`_)
* code folding mode
* auto indent mode
* on the fly code checkers (frosted (fork of PyFlakes), PEP8)
* a customisable python specific syntax highlighter
* a pre-configured QPythonCodeEdit (with the corresponding Qt Designer plugin)

License
-------

pyQode is licensed under the **MIT license**.

Requirements
------------

pyqode.python depends on the following libraries:

- python 2.7 or python 3 (>= 3.2)
- pyqode.core
- jedi
- pep8
- frosted
- docutils
