.. include:: xrst_preamble.rst

!!!!!!!!!!!!!!
no_parent_exam
!!!!!!!!!!!!!!

xrst input file: ``sphinx/test_in/no_parent.xrst``

.. meta::
   :keywords: no_parent_exam, no, parent, example

.. index:: no_parent_exam, no, parent, example

.. _no_parent_exam:

No Parent Example
#################
.. contents::
   :local:

All the sections in the file ``children.py``
are children of the section below
because ``children.py`` does not have a
:ref:`parent section<begin_cmd@parent_section>`:

.. literalinclude:: ../../sphinx/test_in/no_parent.xrst
    :lines: 24-48
    :language: rst

.. csv-table::
    :header: "Child", "Title"
    :widths: 20, 80

    "no_parent_res", :ref:`no_parent_res`

.. toctree::
   :maxdepth: 1
   :hidden:

   no_parent_res

