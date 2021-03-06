.. include:: xrst_preamble.rst

!!!!!!!!!
auto_file
!!!!!!!!!

xrst input file: ``xrst/auto_file.py``

.. meta::
   :keywords: auto_file, automatically, generated, files

.. index:: auto_file, automatically, generated, files

.. _auto_file:

Automatically Generated Files
#############################
.. contents::
   :local:

These files are located in the
:ref:`run_xrst@sphinx_dir` directory.
A new version of these files is created each time ``xrst`` is run.
The files in the ``rst`` subdirectory that do not change are not replaced.

.. meta::
   :keywords: index.rst

.. index:: index.rst

.. _auto_file@index.rst:

index.rst
*********
The sphinx index.rst file. This is root level in the documentation tree
built by sphinx. It is one level above the first section in
:ref:`run_xrst@root_file`.

.. meta::
   :keywords: conf.py

.. index:: conf.py

.. _auto_file@conf.py:

conf.py
*******
This is the sphinx configuration_ file.

.. _configuration:  http://www.sphinx-doc.org/en/master/config

.. meta::
   :keywords: rst/xrst_table_contents.rst

.. index:: rst/xrst_table_contents.rst

.. _auto_file@rst/xrst_table_contents.rst:

rst/xrst_table_contents.rst
***************************
This file contains the table of contents for the last run of ``xrst``.
You can link to the corresponding section with the following command:

```
:ref:`xrst_table_of_contents`
```

The result of this command in this documentation is
:ref:`xrst_table_of_contents` .

.. meta::
   :keywords: rst/xrst_preamble.rst

.. index:: rst/xrst_preamble.rst

.. _auto_file@rst/xrst_preamble.rst:

rst/xrst_preamble.rst
*********************
If :ref:`run_xrst@sphinx_dir@preamble.rst` does not exist,
this file is empty.
Otherwise this file is a copy of the
:ref:`run_xrst@sphinx_dir@preamble.rst` file.
If the
:ref:`run_xrst@target` argument is
``pdf``, the latex macros have been removed.

