# -----------------------------------------------------------------------------
#                      xsrst: Extract Sphinx RST Files
#          Copyright (C) 2020-22 Bradley M. Bell (bradbell@seanet.com)
#              This program is distributed under the terms of the
#              GNU General Public License version 3.0 or later see
#                    https://www.gnu.org/licenses/gpl-3.0.txt
# ----------------------------------------------------------------------------
# process child commands
#
# data_in:
# is the data for the section before the child commands have been processed.
# Line numbers have been added to this data: see add_line_numbers.
#
# file_name:
# is the name of the file that this data comes from. This is only used
# for error reporting.
#
# section_name:
# is the name of the section that this data is in. This is only used
# for error reporting.
#
# data_out:
# The first retrun data_out is a copy of data_in with the
# child commands replaced by  {xsrst_command} where comamnd is children,
# child_list, or child_table depending on which command was in data_in.
#
# file_list:
# The second return file_list is the list of files in the child command
# (and in same order as in the child command).
#
# section_list:
# Is the list of children of the section_name section are in the the files in
# file_list. If a file in file_list has a begin_parent command, it only has
# one section in section_list for that file. Otherwise all of the secitons
# in the file are in section_list.
#
import os
import xsrst
def child_commands(data_in, file_name, section_name) :
    assert type(data_in) == str
    assert type(file_name) == str
    assert type(section_name) == str
    #
    # data_out
    data_out = data_in
    #
    # file_list, file_line, section_list
    file_list    = list()
    file_line    = list()
    section_list = list()
    #
    # m_obj
    m_obj        = xsrst.pattern['child'].search(data_out)
    if m_obj is None :
        return data_out, file_list, section_list
    #
    # m_tmp
    m_tmp = xsrst.pattern['child'].search(data_out[m_obj.end() :] )
    if m_tmp is not None :
        msg = 'More than one children or child_list command in a section.'
        xsrst.system_exit(msg,
            file_name=file_name,
            section_name=section_name,
            m_obj=m_tmp,
            data=data_out[m_obj.end():]
        )
    #
    # command
    command = m_obj.group(1)
    assert command in [ 'children', 'child_list', 'child_table']
    #
    # data_out
    replace = '\n{xsrst_' + command + '}\n'
    data_out = xsrst.pattern['child'].sub(replace, data_out)
    #
    # file_list, file_line
    for child_line in m_obj.group(2).split('\n') :
        if child_line != '' :
            m_child = xsrst.pattern['line'].search(child_line)
            assert m_child != None
            line_number = m_child.group(1)
            child_file  = xsrst.pattern['line'].sub('', child_line).strip()
            if child_file != '' :
                file_list.append(child_file)
                file_line.append(line_number)
    #
    # section_list
    assert len(section_list) == 0
    for i in range( len(file_list) ) :
        #
        # child_file, child_line
        child_file = file_list[i]
        child_line = file_line[i]
        if not os.path.isfile(child_file) :
            msg  = 'The file ' + child_file + '\n'
            msg += 'in the ' + command + ' command does not exist'
            xsrst.system_exit(msg,
                file_name=file_name, section_name=section_name, line=child_line
            )
        #
        # file_data
        # errors in the begin and end commands will be detected later
        # when this file is processed.
        file_ptr    = open(child_file, 'r')
        file_data   = file_ptr.read()
        file_ptr.close()
        file_index  = 0
        file_data   = xsrst.remove_comment_ch(file_data, child_file)
        #
        # m_obj
        m_obj  = xsrst.pattern['begin'].search(file_data)
        if m_obj is None :
            msg  = 'The file ' + child_file + '\n'
            msg += 'in the ' + command + ' command does not contain any '
            msg += 'begin commands.\n'
            xsrst.system_exit(msg,
                file_name=file_name, section_name=section_name, line=child_line
            )
        #
        # list_children
        found_parent  = m_obj.group(2) == 'begin_parent'
        child_name    = m_obj.group(3)
        list_children = [ child_name ]
        #
        # m_obj
        m_obj = xsrst.pattern['begin'].search(file_data, m_obj.end() )
        #
        while not found_parent and m_obj != None :
            is_parent = m_obj.group(2) == 'begin_parent'
            if is_parent :
                msg  = 'Found a begin_parent command that is'
                msg += ' not the first begin command in this file'
                xsrst.system_exit(msg,
                    file_name=child_file,
                    section_name=section_name,
                    m_obj=m_obj,
                    data=file_data
                )
            child_name = m_obj.group(3)
            #
            # list_children
            list_children.append( child_name )
            #
            # m_obj
            m_obj   = xsrst.pattern['begin'].search(file_data, m_obj.end() )
        #
        # section_list
        section_list += list_children
    #
    return data_out, file_list, section_list
