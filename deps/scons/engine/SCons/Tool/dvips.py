"""SCons.Tool.dvips

Tool-specific initialization for dvips.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "/home/scons/scons/branch.0/branch.96/baseline/src/engine/SCons/Tool/dvips.py 0.96.96.D001 2007/04/12 14:12:18 knight"

import SCons.Action
import SCons.Builder
import SCons.Util

PSAction = None
PSBuilder = None

def generate(env):
    """Add Builders and construction variables for dvips to an Environment."""
    global PSAction
    if PSAction is None:
        PSAction = SCons.Action.Action('$PSCOM', '$PSCOMSTR')

    global PSBuilder
    if PSBuilder is None:
        PSBuilder = SCons.Builder.Builder(action = PSAction,
                                          prefix = '$PSPREFIX',
                                          suffix = '$PSSUFFIX',
                                          src_suffix = '.dvi',
                                          src_builder = 'DVI')

    env['BUILDERS']['PostScript'] = PSBuilder
    
    env['DVIPS']      = 'dvips'
    env['DVIPSFLAGS'] = SCons.Util.CLVar('')
    # I'm not quite sure I got the directories and filenames right for build_dir
    # We need to be in the correct directory for the sake of latex \includegraphics eps included files.
    env['PSCOM']      = 'cd ${TARGET.dir} && $DVIPS $DVIPSFLAGS -o ${TARGET.file} ${SOURCE.file}'
    env['PSPREFIX'] = ''
    env['PSSUFFIX'] = '.ps'

def exists(env):
    return env.Detect('dvips')