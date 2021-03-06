#! /usr/bin/env python3
# -----------------------------------------------------------------------------
#                      xrst: Extract Sphinx RST Files
#          Copyright (C) 2020-22 Bradley M. Bell (bradbell@seanet.com)
#              This program is distributed under the terms of the
#              GNU General Public License version 3.0 or later see
#                    https://www.gnu.org/licenses/gpl-3.0.txt
# ----------------------------------------------------------------------------
"""
{xrst_begin run_xrst}
{xrst_spell
    cd
    dir
}

Run Extract Sphinx RST And Sphinx
#################################



Syntax
******
-   ``xrst`` *target* *root_file* *sphinx_dir* [ *line_increment* ]


target
******
The command line argument *target* must be ``html`` or ``pdf``.
It specifies the type of type output you plan to generate using sphinx.

html
====
If *target* is ``html`` you can generate the sphinx output using
the following command:

|space|   ``sphinx-build -b html`` *sphinx_dir* *html_dir*

where *html_dir* is the directory where the html files are written,
see below for the meaning of *sphinx_dir*.

pdf
===
If *target* is ``pdf``, you can use the following commands:
{xrst_code sh}
cd sphinx_dir
sphinx-build -b latex . latex
cd latex
make root_section_name.pdf
{xrst_code}
where root_section_name is the name of the root section for you documentation.

root_file
*********
The command line argument *root_file* is the name of a file.
This can be an absolute path or
relative to the directory where :ref:`xrst<run_xrst>` is executed.

sphinx_dir
**********
The command line argument *sphinx_dir* is a directory relative to
of the directory where *root_file* is located.

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

Example
-------
:ref:`preamble.rst`

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

Example
-------
:ref:`spelling`

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

Example
-------
:ref:`keyword`


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

Other Automatically Generated Files
===================================
{xrst_children
    xrst/auto_file.py
    sphinx/configure.xrst
}
See :ref:`auto_file` for the other automatically generated files in the
*sphinx_dir* directory.


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

{xrst_end run_xrst}
"""
# ---------------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------------
import sys
import re
import os
import pdb
import string
import spellchecker
import shutil
import filecmp
#
# sys.path
# used so that we can test before installing
if( os.getcwd().endswith('/xrst.git') ) :
    if( os.path.isdir('xrst') ) :
        sys.path.insert(0, os.getcwd() )
#
import xrst
def run_xrst() :
    #
    # execution_directory
    execution_directory = os.getcwd()
    #
    # check number of command line arguments
    if len(sys.argv) != 4 and len(sys.argv) != 5 :
        usage  = 'xrst target root_file sphinx_dir [ line_increment ]'
        xrst.system_exit(usage)
    #
    # target
    target = sys.argv[1]
    if target != 'html' and target != 'pdf' :
        msg  = 'target = ' + target + '\n'
        msg += 'is not "html" or "pdf"'
        xrst.system_exit(msg)
    #
    # root_file
    # can not use system_exit until os.getcwd() returns root_directory
    root_file = sys.argv[2]
    if not os.path.isfile(root_file) :
        msg  = 'xsrst: Error\n'
        msg += f'root_file = {root_file}\n'
        if root_file[0] == '/' :
            msg += 'is not a file\n'
        else :
            msg += f'is not a file relative to the execution directory\n'
            msg += execution_directory
        sys.exit(msg)
    #
    # root_directory
    index = root_file.rfind('/')
    if index < 0 :
        root_directory = '.'
    elif index == 0 :
        root_directory = '/'
    elif 0 < index :
        root_directory = root_file[: index]
    os.chdir(root_directory)
    #
    # sphinx_dir
    sphinx_dir      = sys.argv[3]
    if not os.path.isdir(sphinx_dir) :
        msg  = 'sphinx_dir = ' + sphinx_dir + '\n'
        msg += 'is a valid directory path'
        xrst.system_exit(msg)
    if sphinx_dir[0] == '/' :
        msg  = 'sphinx_dir = ' + sphinx_dir + '\n'
        msg += 'must be a path relative to current workding directory'
        xrst.system_exit(msg)
    if 0 <= sphinx_dir.find('../') :
        msg  = 'sphinx_dir = ' + sphinx_dir + '\n'
        msg += 'cannot contain ../'
        xrst.system_exit(msg)
    #
    # line_increment
    if len(sys.argv) == 4 :
        line_increment = 0
    else :
        line_increment = int(sys.argv[4])
        if line_increment < 1 :
            msg += 'line_increment is not a positive integer'
            xrst.system_exit(msg)
    #
    # xsrist_dir
    rst_dir = sphinx_dir + '/rst'
    if not os.path.isdir(rst_dir) :
        os.mkdir(rst_dir)
    #
    # tmp_dir
    tmp_dir = rst_dir + '/tmp'
    if os.path.isdir(tmp_dir) :
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    #
    # spell_checker
    spell_list  = list()
    spell_file  = sphinx_dir + '/spelling'
    if os.path.isfile( spell_file ) :
        spell_list  = xrst.file2_list_str(spell_file)
    spell_checker = xrst.create_spell_checker(spell_list)
    #
    # keyword_list
    keyword_list = list()
    keyword_file = sphinx_dir + '/keyword'
    if os.path.isfile( keyword_file ) :
        str_list = xrst.file2_list_str(keyword_file)
        for regexp in str_list :
            keyword_list.append( re.compile( regexp ) )
    # -------------------------------------------------------------------------
    #
    # root_local
    index = root_file.rfind('/')
    if index < 0 :
        root_local = root_file
    else :
        root_local = root_file[index + 1 :]
    #
    # sinfo_list, finfo_stack, finfo_done
    sinfo_list       = list()
    finfo_stack      = list()
    finfo_done       = list()
    finfo = {
        'file_in'        : root_local,
        'parent_file'    : None,
        'parent_section' : None,
    }
    finfo_stack.append(finfo)
    #
    while 0 < len(finfo_stack) :
        # pop first element is stack so that order in pdf file and
        # table of contents is correct
        finfo  = finfo_stack.pop(0)
        #
        for finfo_tmp in finfo_done :
            if finfo_tmp['file_in'] == finfo['file_in'] :
                msg  = 'The file ' + finfo['file_in'] + ' is included twice\n'
                msg += 'Once in ' + finfo_tmp['parent_file'] + '\n'
                msg += 'and again in ' + finfo['parent_file'] + '\n'
                xrst.system_exit(msg)
        finfo_done.append(finfo)
        #
        file_in              = finfo['file_in']
        parent_file          = finfo['parent_file']
        parent_file_section  = finfo['parent_section']
        assert os.path.isfile(file_in)
        #
        # get xrst docuemntation in this file
        sinfo_file_in = xrst.get_file_info(
            sinfo_list,
            file_in,
        )
        #
        # parent_section_file_in
        # index in sinfo_list of parent section for this file
        parent_section_file_in = None
        if sinfo_file_in[0]['is_parent'] :
            parent_section_file_in = len(sinfo_list)
        #
        # add this files sections to sinfo_list
        for i_section in range( len(sinfo_file_in) ) :
            # ----------------------------------------------------------------
            # section_name, section_data, is_parent
            section_name = sinfo_file_in[i_section]['section_name']
            section_data = sinfo_file_in[i_section]['section_data']
            is_parent    = sinfo_file_in[i_section]['is_parent']
            is_child     = sinfo_file_in[i_section]['is_child']
            #
            # parent_section
            if is_parent or parent_section_file_in is None :
                parent_section = parent_file_section
            else :
                parent_section = parent_section_file_in
            #
            # sinfo_list
            sinfo_list.append( {
                'section_name'   : section_name,
                'file_in'        : file_in,
                'parent_section' : parent_section,
                'in_parent_file' : is_child,
            } )
            # ----------------------------------------------------------------
            # spell_command
            # do after suspend and before other commands to help ignore
            # sections of text that do not need spell checking
            section_data = xrst.spell_command(
                section_data,
                file_in,
                section_name,
                spell_checker,
            )
            # ----------------------------------------------------------------
            # child commands
            section_data, child_file, child_section_list = xrst.child_commands(
                section_data,
                file_in,
                section_name,
            )
            #
            # section_index, finfo_stack
            section_index = len(sinfo_list) - 1
            for file_tmp in child_file :
                finfo_stack.append( {
                    'file_in'        : file_tmp,
                    'parent_file'    : file_in,
                    'parent_section' : section_index,
                } )
            # ----------------------------------------------------------------
            # code commands
            section_data = xrst.code_command(
                section_data,
                file_in,
                section_name,
            )
            # ---------------------------------------------------------------
            # file command
            section_data = xrst.file_command(
                section_data,
                file_in,
                section_name,
                rst_dir,
            )
            # ---------------------------------------------------------------
            # process headings
            # add labels and indices corresponding to headings
            section_data, section_title, pseudo_heading = \
            xrst.process_headings(
                section_data,
                file_in,
                section_name,
                keyword_list,
            )
            # section title is used by table_of_contents
            sinfo_list[section_index]['section_title'] = section_title
            # ----------------------------------------------------------------
            # list_children
            # section_name for each of the children of the current section
            list_children = child_section_list
            if is_parent :
                for i in range( len(sinfo_file_in) ) :
                    if i != i_section :
                        list_children.append(sinfo_file_in[i]['section_name'])
            # ---------------------------------------------------------------
            # process children
            # want this as late as possible to toctree at end of input
            section_data = xrst.process_children(
                section_name,
                section_data,
                list_children,
            )
            # ---------------------------------------------------------------
            # write temporary file
            xrst.temporary_file(
                line_increment,
                pseudo_heading,
                file_in,
                tmp_dir,
                section_name,
                section_data,
            )
    #
    # auto_file
    xrst.auto_file(sphinx_dir, tmp_dir, target, sinfo_list)
    #
    # -------------------------------------------------------------------------
    # overwrite rst files that have changed and then remove temporary files
    tmp_list = os.listdir(tmp_dir)
    rst_list = os.listdir(rst_dir)
    for name in tmp_list :
        src = tmp_dir + '/' + name
        des = rst_dir + '/' + name
        if name.endswith('.rst') :
            if name not in rst_list :
               shutil.copyfile(src, des)
            else :
                if not filecmp.cmp(src, des, shallow=False) :
                    os.replace(src, des)
    for name in rst_list :
        if name.endswith('.rst') :
            if name not in tmp_list :
                os.remove( rst_dir + '/' + name )
    # reset tmp_dir because rmtree is such a dangerous command
    tmp_dir = rst_dir + '/tmp'
    shutil.rmtree(tmp_dir)
    # -------------------------------------------------------------------------
    print('xrst: OK')
