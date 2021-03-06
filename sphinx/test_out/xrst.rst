.. include:: xrst_preamble.rst

!!!!
xrst
!!!!

xrst input file: ``doc.xrst``

.. meta::
   :keywords: xrst, extract, sphinx, rst, files

.. index:: xrst, extract, sphinx, rst, files

.. _xrst:

Extract Sphinx RST Files
########################
.. contents::
   :local:

.. meta::
   :keywords: version, 2022.7.30

.. index:: version, 2022.7.30

.. _xrst@version_2022.7.30:

Version 2022.7.30
******************

.. meta::
   :keywords: git, repository

.. index:: git, repository

.. _xrst@git_repository:

Git Repository
**************
https://github.com/bradbell/xrst

.. meta::
   :keywords: pip, install

.. index:: pip, install

.. _xrst@pip_install:

Pip Install
***********
-   ``pip install --index-url https://test.pypi.org/simple/ xrst``

.. meta::
   :keywords: run, program

.. index:: run, program

.. _xrst@run_program:

Run Program
***********
:ref:`run_xrst`

.. meta::
   :keywords: purpose

.. index:: purpose

.. _xrst@purpose:

Purpose
*******
This is a pseudo sphinx extension that provides the following features:

#.  The rst file name for each section is also an abbreviated title used
    in the navigation bar and for linking to the section. This makes the
    navigation bar more useful while also having long descriptive titles.
    It also makes cross reference linking from other sections easier.
#.  Each section has its own table of contents (for its headings) that is
    separate from the table of contents for the sections. This makes it
    easy to move sections to different places in the over all structure.
#.  Enables documentation in the comments for source code
    when multiple computer languages are used for one package.
    Allows the documentation for one section to span multiple locations
    in the source code; see :ref:`suspend command<suspend_cmd>`.
#.  Allows for multiple sections (rst output files) to be specified by one
    input file. In addition, one section can be the parent for the
    other sections in a file.
#.  Generates the table of contents from the specification
    of which files are included; see :ref:`child commands<child_cmd>`.
    Generates a jump table to the headings for each section
    so that the navigation bar need not include this information.
#.  Includes a configurable :ref:`spell checker<spell_cmd>` and
    :ref:`index<genindex>`. The spell checker catches double word errors.
    Words in each heading are automatically included in the index.
#.  Makes it easy to include source code that also executes, from
    directly below the :ref:`code command<code_cmd>` or from
    a different location in a :ref:`file<file_cmd>`.
    This uses tokens in the source, not line numbers,
    to signify start and stop of inclusion from a file.

.. meta::
   :keywords: contents

.. index:: contents

.. _xrst@contents:

Contents
********

-  :ref:`run_xrst`
-  :ref:`commands`
-  :ref:`other_processing`
-  :ref:`wish_list`
-  :ref:`release_notes`

.. toctree::
   :maxdepth: 1
   :hidden:

   run_xrst
   commands
   other_processing
   wish_list
   release_notes

