# Written by Jeff Hickson (rvbcaboose@gmail.com).
# This file is part of burble, a plugin for Flinx. 

# Burble is free software, and comes with no warranty.
# It is licenced under the GNU GLP v3.
# The full terms of this are available in the LICENCE file,
# in the root of the project, at <http://www.gnu.org/licenses/>,
# or at <https://github.com/Tillwoofie/burble/blob/master/LICENSE>

import os
#import os.path


def dirwalk_gen(directory):
    '''
    Implements a recursive directory walker that is a generator.
    '''
    op = os.path
    dirnames = []
    if not op.exists(directory):
        # I believe this is the way to exit a generator properly?
        raise StopIteration
    # collect the list of dirs under directory.
    op.walk(directory, grab_dirs, dirnames)
    for d in dirnames:
        for f in get_files(d):
            yield (d,f)
    return


def get_files(directory):
    op = os.path
    dir_list = os.listdir(directory)
    files = []
    for f in dir_list:
        if not op.isdir(f):
            files.append(f)
    return files


def grab_dirs(arg, dirn, fnames):
    arg.append(dirn)

