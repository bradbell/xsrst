.. include:: xrst_preamble.rst

!!!!!!!!
run_xrst
!!!!!!!!

xrst input file: ``xrst/run_xrst.py``

.. meta::
   :keywords: run_xrst, run, extract, sphinx, rst, sphinx

.. index:: run_xrst, run, extract, sphinx, rst, sphinx

.. _run_xrst:

Run Extract Sphinx RST And Sphinx
#################################
.. contents::
   :local:

.. meta::
   :keywords: syntax

.. index:: syntax

.. _run_xrst@syntax:

Syntax
******
-   ``xrst`` *target* *root_file* *sphinx_dir* [ *line_increment* ]

.. meta::
   :keywords: target

.. index:: target

.. _run_xrst@target:

target
******
The command line argument *target* must be ``html`` or ``pdf``.
It specifies the type of type output you plan to generate using sphinx.

.. meta::
   :keywords: html

.. index:: html

.. _run_xrst@target@html:

html
====
If *target* is ``html`` you can generate the sphinx output using
the following command:

|space|   ``sphinx-build -b html`` *sphinx_dir* *html_dir*

where *html_dir* is the directory where the html files are written,
see below for the meaning of *sphinx_dir*.

.. meta::
   :keywords: pdf

.. index:: pdf

.. _run_xrst@target@pdf:

pdf
===
If *target* is ``pdf``, you can use the following commands:

.. code-block:: sh

    cd sphinx_dir
    sphinx-build -b latex . latex
    cd latex
    make root_section_name.pdf

where root_section_name is the name of the root section for you documentation.

.. meta::
   :keywords: root_file

.. index:: root_file

.. _run_xrst@root_file:

root_file
*********
The command line argument *root_file* is the name of a file.
This can be an absolute path or
relative to the directory where :ref:`xrst<run_xrst>` is executed.

.. meta::
   :keywords: sphinx_dir

.. index:: sphinx_dir

.. _run_xrst@sphinx_dir:

sphinx_dir
**********
The command line argument *sphinx_dir* is a directory relative to
of the directory where *root_file* is located.

.. meta::
   :keywords: preamble.rst

.. index:: preamble.rst

.. _run_xrst@sphinx_dir@preamble.rst:

preamble.rst
============
The file *sphinx_dir* ``/preamble.rst`` can be create by the user.
If it exists, it is included at the beginning of every section.
It should only define things, it should not generate any output.
For example, :ref:`preamble.rst`.
The Latex macros in this file can be used by any section.
There must be one macro definition per line and each such line must match the
following python regular expression:

    ``\n[ \t]*:math:`\\newcommand\{[^`]*\}`[ \t]*``

.. meta::
   :keywords: example

.. index:: example

.. _run_xrst@sphinx_dir@preamble.rst@example:

Example
-------
:ref:`preamble.rst`

.. meta::
   :keywords: spelling

.. index:: spelling

.. _run_xrst@sphinx_dir@spelling:

spelling
========
The file *sphinx_dir* ``/spelling`` can be create by the user.
If it exists, it contains a list of words
that the spell checker will consider correct for all sections.
A line that begins with :code:`#` is a comment (not included in the list).
The words are one per line and
leading and trailing white space in a word are ignored.
For example; see :ref:`spelling`.
Special words, for a particular section, are specified using the
:ref:`spell command<spell_cmd>`.

.. meta::
   :keywords: example

.. index:: example

.. _run_xrst@sphinx_dir@spelling@example:

Example
-------
:ref:`spelling`

.. meta::
   :keywords: keyword

.. index:: keyword

.. _run_xrst@sphinx_dir@keyword:

keyword
=======
The file *sphinx_dir* ``/keyword`` can be create by the user.
If it exists, it contains a list of
python regular expressions for heading tokens
that are not included in the index.
A heading token is any sequence of non space or new line characters
with upper case letters converted to lower case.
For example, a heading might contain the token ``The`` but you
might not want to include ``the`` as a entry in the :ref:`genindex`.
In this case you could have a line containing just ``the`` in *keyword*.
For another example, you might want to exclude all tokens that are numbers.
In this case you could have a line containing just ``[0-9]*`` in *keyword*.
The regular expressions are one per line and
leading and trailing spaces are ignored.
A line that begins with :code:`#` is a comment
(not included in the list of python regular expressions).
For example; see :ref:`keyword`.

.. meta::
   :keywords: example

.. index:: example

.. _run_xrst@sphinx_dir@keyword@example:

Example
-------
:ref:`keyword`

.. meta::
   :keywords: section, rst, files

.. index:: section, rst, files

.. _run_xrst@sphinx_dir@section_rst_files:

Section RST Files
=================
The directory *sphinx_dir* :code:`/rst` is managed by ``xrst`` .
It contains all the rst files that were extracted from the source code,
and correspond to last time that ``xrst`` was executed.
For each :ref:`begin_cmd@section_name`, the file

|space| *sphinx_dir* ``/xrst/`` *section_name* ``.rst``

Is the RST file for the corresponding section. There is one exception
to this rule. If *section_name* ends with ``.rst``, the extra ``.rst``
is not added at the end.

.. meta::
   :keywords: other, automatically, generated, files

.. index:: other, automatically, generated, files

.. _run_xrst@sphinx_dir@other_automatically_generated_files:

Other Automatically Generated Files
===================================

See :ref:`auto_file` for the other automatically generated files in the
*sphinx_dir* directory.

.. meta::
   :keywords: line_increment

.. index:: line_increment

.. _run_xrst@line_increment:

line_increment
**************
This optional argument helps find the source of errors reported by sphinx.
If the argument *line_increment* is present,
a table is generated at the end of each output file.
This table maps line numbers in the output file to
line numbers in the corresponding xrst input file.
The argument *line_increment* is a positive integer specifying the minimum
difference between xrst input line numbers for entries in the table.
The value ``1`` will give the maximum resolution.
For example, the sphinx warning

| |tab| ... ``/xrst/children_exam.rst:30: WARNING:`` ...

corresponds to line number 30 in the file ``children_exam.rst``.
The table at the bottom of that file maps line numbers in
``children_exam.rst`` to line numbers in the corresponding xrst input file.

.. toctree::
   :maxdepth: 1
   :hidden:

   auto_file
   configure

