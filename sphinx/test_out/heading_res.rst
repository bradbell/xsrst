.. include:: xrst_preamble.rst

!!!!!!!!!!!
heading_res
!!!!!!!!!!!

xrst input file: ``sphinx/test_in/heading.py``

.. meta::
   :keywords: heading_res, heading, result

.. index:: heading_res, heading, result

.. _heading_res:

Heading Result
##############
.. contents::
   :local:

The label for this heading is the section name ``heading_res``.

.. meta::
   :keywords: second, level

.. index:: second, level

.. _heading_res@second_level:

Second Level
************
The label for this heading is ``heading_res.second_level``.

.. meta::
   :keywords: third, level

.. index:: third, level

.. _heading_res@second_level@third_level:

Third Level
===========
The label for this heading is ``heading_res.second_level.third_level``.

.. meta::
   :keywords: another, second, level

.. index:: another, second, level

.. _heading_res@another_second_level:

Another Second Level
********************
The label for this heading is ``heading_res.another_second_level``.

.. meta::
   :keywords: third, level

.. index:: third, level

.. _heading_res@another_second_level@third_level:

Third Level
===========
The label for this heading is
``heading_res.another_second_level.third_level``.

.. meta::
   :keywords: links

.. index:: links

.. _heading_res@links:

Links
*****
These links would also work from any other section because the
:ref:`section_name<begin_cmd@section_name>`
(which is ``heading_res`` in this case)
is included at the beginning of the target for the link:

1. :ref:`heading_res`
2. :ref:`heading_res@second_level`
3. :ref:`heading_res@second_level@third_level`
4. :ref:`heading_res@another_second_level`
5. :ref:`heading_res@another_second_level@third_level`

:ref:`heading_exam`

