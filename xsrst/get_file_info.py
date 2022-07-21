# -----------------------------------------------------------------------------
#                      xsrst: Extract Sphinx RST Files
#          Copyright (C) 2020-22 Bradley M. Bell (bradbell@seanet.com)
#              This program is distributed under the terms of the
#              GNU General Public License version 3.0 or later see
#                    https://www.gnu.org/licenses/gpl-3.0.txt
# ----------------------------------------------------------------------------
# Get all the information for a file.
#
# section_info:
# a list of the information for sections that came before this file.
# We use infor below for one eleemnt of this list:
#
#   info['section_name']
#   is an str containing the name of a seciton that came before this file.
#
# file_in:
# is the name of the file we are getting all the information for.
#
# file_info:
# The value file_info is a list is a dictionary contianing the information
# for one section in this file. We use info below for one element of this list:
#
#   info['section_name']:
#   is an str containing the name of a seciton in this file.
#
#   info['section_data']:
#   is an str containing the data for this seciton.
#   1. Line numbers have been added using add_line_numbers.
#   2. If present in this file, the comment character and possilbe space
#      after have been removed.
#   3. The begin and end commands are not include in this data.
#   4. The suspend / resume comands and data between such pairs
#      have been removed.
#   5. If there is a common indentation for the entire section,
#      it is removed.
#
#   info['is_parent']:
#   is true (false) if this is (is not) the parent section for the other
#   sections in this file. The parent section must be the first, and hence
#   have index zero in file_info. In addition, if there is a parent section,
#   there must be at least one other section; i.e., len(file_info) >= 2.
import xsrst
def get_file_info(
        section_info,
        file_in
) :
    assert type(section_info) == list
    assert type(file_in) == str
    #
    # file_data
    file_ptr   = open(file_in, 'r')
    file_data  = file_ptr.read()
    file_ptr.close()
    #
    # file_data
    file_data = xsrst.add_line_numbers(file_data)
    file_data = xsrst.remove_comment_ch(file_data, file_in)
    #
    # file_info
    file_info = list()
    #
    # parent_section_name
    parent_section_name = None
    #
    # index to start search for next pattern in file_data
    data_index  = 0
    #
    # for each section in this file
    while data_index < len(file_data) :
        #
        # m_obj
        data_rest   = file_data[data_index : ]
        m_obj = xsrst.pattern['begin'].search(data_rest)
        if m_obj == None :
            if data_index == 0 :
                msg  = 'can not find followng at start of a line:\n'
                msg += '    {xsrst_begin section_name}\n'
                xsrst.system_exit(msg, file_name=file_in)
            #
            # data_index
            # set so that the section loop for this file terminates
            data_index = len(file_data)
        else :
            # section_name, is_parent
            section_name = m_obj.group(3)
            is_parent    = m_obj.group(2) == 'begin_parent'
            #
            # check_section_name
            xsrst.check_section_name(
                section_name,
                file_name     = file_in,
                m_obj         = m_obj,
                data          = data_rest
            )
            #
            # check if section_name appears multiple times in this file
            for info in file_info :
                if section_name == info['section_name'] :
                    msg  = 'xsrst_begin: section appears multiple times'
                    xsrst.system_exit(msg,
                        file_name=file_in,
                        section_name=section_name,
                        m_obj=m_obj,
                        data=data_rest
                    )
            #
            # check if section_name appears in another file
            for info in section_info :
                if section_name == info['section_name'] :
                    msg  = 'xsrst_begin ' + section_name
                    msg += ' appears twice\n'
                    msg += 'Once  in file ' + file_in + '\n'
                    msg += 'Again in file ' + info['file_in'] + '\n'
                    xsrst.system_exit(msg)
            #
            # check if parent sections is the first seciton in this file
            if is_parent :
                if len(file_info) != 0 :
                    msg  = 'xsrst_begin_parent'
                    msg += ' is not the first begin command in this file'
                    xsrst.system_exit(msg,
                        file_name=file_in,
                        section_name=section_name,
                        m_obj=m_obj,
                        data=data_rest
                    )
                #
                # parent_section_name
                parent_section_name = section_name
            #
            # data_index
            data_index += m_obj.end()
            #
            # m_obj
            data_rest = file_data[data_index : ]
            m_obj     = xsrst.pattern['end'].search(data_rest)
            #
            if m_obj == None :
                msg  = 'Expected the followig text at start of a line:\n'
                msg += '    {xsrst_end section_name}'
                xsrst.system_exit(
                    msg, file_name=file_in, section_name=section_name
                )
            if m_obj.group(1) != section_name :
                msg = 'begin and end section names do not match\n'
                msg += 'begin name = ' + section_name + '\n'
                msg += 'end name   = ' + m_obj.group(1)
                xsrst.system_exit(msg,
                    file_name=file_in,
                    m_obj=m_obj,
                    data=data_rest
                )
            #
            # section_data
            section_start = data_index
            section_end   = data_index + m_obj.start() + 1
            section_data  = file_data[ section_start : section_end ]
            #
            # section_data
            section_data  = xsrst.suspend_command(
                section_data, file_in, section_name
            )
            section_data = xsrst.remove_indent(
                section_data, file_in, section_name
            )
            #
            # file_info
            file_info.append( {
                'section_name' : section_name,
                'section_data' : section_data,
                'is_parent'    : is_parent,
            } )
            #
            # place to start search for next section
            data_index += m_obj.end()
    #
    if parent_section_name != None and len(file_info) < 2 :
        msg  = 'begin_parent command appreas in a file '
        msg += 'that only has one section; i.e., no children.'
        xsrst.system_exit(
            msg, file_name=file_in, section_name=parent_section_name
        )

    return file_info