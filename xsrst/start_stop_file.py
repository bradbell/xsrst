# -----------------------------------------------------------------------------
#                      xsrst: Extract Sphinx RST Files
#          Copyright (C) 2020-22 Bradley M. Bell (bradbell@seanet.com)
#              This program is distributed under the terms of the
#              GNU General Public License version 3.0 or later see
#                    https://www.gnu.org/licenses/gpl-3.0.txt
# ----------------------------------------------------------------------------
# Convert start,  stop text for a file command to start, stop line numbers.
#
# section_name:
# is the name of the section where the xsrst_file command appears.
#
# file_cmd:
# is the name of the file where the xsrst_file command appears.
#
# file_search:
# is the name of the file that we are searching. If it is not the same as
# file_cmd, then it must have appeared in the xsrst_file command.
#
# cmd_line:
# If file_cmd is equal to file_search, the section of the file between
# between line numbers cmd_line[0] and cmd_line[1] inclusive
# are in the xsrst_file command and are excluded from the search.
#
# start_text:
# is the starting text. There must be one and only one copy of this text in the
# file (not counting the excluded text). This text has no newlines and cannot
# be empty.  If not, an the error is reported and the program stops.
#
# stop_text:
# is the stopping text. There must be one and only one copy of this text in the
# file (not counting the excluded text). This text has no newlines and cannot
# be empty.  Furthermore, the stopping text must come after the end of the
# starting text. If not, an the error is reported and the program stops.
#
# start_line:
# The first element of the return start_line is the line number where
# start_text appears.
#
# stop_line:
# The second element of the return stop_line is the line number where
# stop_text appears.
#
import xsrst
def start_stop_file(
    section_name = None,
    file_cmd     = None,
    file_search  = None,
    cmd_line     = None,
    start_text   = None,
    stop_text    = None
) :
    assert type(section_name) == str
    assert type(file_cmd) == str
    assert type(file_search) == str
    assert type(cmd_line[0]) == int
    assert type(cmd_line[1]) == int
    assert type(start_text) == str
    assert type(stop_text) == str
    #
    assert cmd_line[0] <= cmd_line[1]
    #
    # exclude_line
    if file_cmd == file_search :
        exclude_line = cmd_line
    else :
        exclude_line = (0, 0)
    #
    # msg
    msg  = f'in file command:'
    #
    if start_text == '' :
        msg += ' start is empty'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    if stop_text == '' :
        msg += ' stop is empty'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    if 0 <= start_text.find('\n') :
        msg += ' a newline appears in start'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    if 0 <= stop_text.find('\n') :
        msg += ' a newline appears in stop'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    #
    # data
    file_ptr  = open(file_search, 'r')
    data      = file_ptr.read()
    file_ptr.close()
    #
    # start_line
    start_index = data.find(start_text)
    count = 0
    while 0 <= start_index :
        line = data[: start_index].count('\n') + 1
        if  line < exclude_line[0] or exclude_line[1] < line :
            start_line = line
            count      = count + 1
        start_index = data.find(start_text, start_index + len(start_text) )
    if count != 1 :
        msg += f'\nstart = "{start_text}"'
        msg += f'\nfile  =  {file_search}'
        msg += f'\nfound {count} matches expected 1'
        if file_cmd == file_search :
            msg += ' not counting the file command'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    #
    # stop_line
    stop_index = data.find(stop_text)
    count = 0
    while 0 <= stop_index :
        line = data[: stop_index].count('\n') + 1
        if  line < exclude_line[0] or exclude_line[1] < line :
            stop_line = line
            count     = count + 1
        stop_index = data.find(stop_text, stop_index + len(stop_text) )
    if count != 1 :
        msg += f'\nstop = "{stop_text}"'
        msg += f'\nfile =  {file_search}'
        msg += f'\nfound {count} matches expected 1'
        if file_cmd == file_search :
            msg += ' not counting the file command'
        xsrst.system_exit(msg,
            fname = file_cmd, sname = section_name, line = cmd_line[0]
        )
    #
    return start_line, stop_line
