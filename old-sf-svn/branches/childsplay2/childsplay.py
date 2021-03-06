#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Stas Zykiewicz <stas.zytkiewicz@gmail.com>
#
#           seniorplay
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation.  A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys
sys.path.insert(0, "..")

import subprocess
#import gc
#gc.set_debug(gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)
# first parse commandline options
from SPOptionParser import OParser
# if this doesn't bail out the options are correct and we continue with schoolsplay

op = OParser()
# this will return a class object with the options as attributes  
CMD_Options = op.get_options()
# Add special attribute which will be checked by the core to look if local activities
# should be loaded. This is only done for developing new activities.
CMD_Options.run_local = True

######## Here we add options for debugging #####
### Must be removed or at least discussed before release #####
#CMD_Options.loglevel = 'debug'
# TODO: remove this when the login is using SPWidgets iso ocempgui
#CMD_Options.no_login = True
CMD_Options.user = 'BT_user'
CMD_Options.nocountdown = True

import SPLogging
SPLogging.set_level(CMD_Options.loglevel)
SPLogging.start()

#create logger, configuration of logger was done above
import logging
CPmodule_logger = logging.getLogger("schoolsplay.seniorplay")
CPmodule_logger.debug("Created schoolsplay loggers")

CPmodule_logger.info("IMPORTANT READ THE FOLLOWING LINES")
CPmodule_logger.info("For debugging purposes we run with some cmdline options hardcoded.")
CPmodule_logger.info("These must be removed before releasing this to the real world")
CPmodule_logger.info("Look at the top of this module for these options")

if CMD_Options.loglevel == 'debug':
    from SPConstants import *
    CPmodule_logger.debug("Paths defined in SPConstants:")
    for v in ['ACTIVITYDATADIR', 'ALPHABETDIR', 'BASEDIR',\
               'DBASEPATH', 'HOMEDIR', 'HOMEIMAGES', 'HOME_DIR_NAME',\
               'LOCALEDIR', 'LOCKFILE', 'OCWBASEDIR','PYTHONCPDIR']:
        CPmodule_logger.debug("%s > %s" % (v, eval(v)))

import utils
# this will return the tuple (lang,rtl=bool)
LANG = utils.set_locale(lang=CMD_Options.lang, theme=CMD_Options.theme)

if CMD_Options.checklog:
    try:
        import SPlogCheck
    except (ImportError, utils.SPError):
        sys.exit(1)
    except utils.MyError:
        sys.exit(1)
    sys.exit(0)

if CMD_Options.admingui:
    # This will not return
    try:
        import gui.AdminGui as AdminGui
        AdminGui.main()
    except Exception,info:
        print "GUI raised an exception"
        print info
        sys.exit(1)
    else:
        sys.exit(0)
        
if not utils._set_lock():
    sys.exit(1)
    
import SPMainCore

from SPgdm import GDMEscapeKeyException

# start the maincore, we only return here on an exit
CPmodule_logger.debug("Start logging")
CPmodule_logger.debug("commandline options: %s" % CMD_Options)
CPmodule_logger.debug("SPMainCore running from: %s" % SPMainCore)

abort = 0 
while not abort:
    try:
        # there's no support for other resolutions then 800x600
        mcgui = SPMainCore.MainCoreGui(resolution=(800,600),\
                                        options=CMD_Options,\
                                        language=LANG)
        mcgui.start()
    except SPMainCore.MainEscapeKeyException:
        if CMD_Options.no_login or CMD_Options.user:
            # we have no login screen or the user was passed as a cmdline option so we exit
            #sys.exit(0)
            abort = True
            CPmodule_logger.info("nologin screen, clean exit")
    except GDMEscapeKeyException:
        CPmodule_logger.info("login screen, clean exit")
        break
    except SystemExit,status:
        if str(status) == '0':
            CPmodule_logger.info("systemexit, clean exit")
            abort = True
        else:
            CPmodule_logger.info("systemexit, not a clean exit")
            abort = True
    except utils.SPError, info:
        CPmodule_logger.error("Unrecoverable error, not a clean exit")
        abort = True
    except Exception,status:        
        CPmodule_logger.exception("unhandled exception in toplevel, traceback follows:")
        abort = True
        
try:
    mcgui.activity.stop_timer()
except:
    CPmodule_logger.warning("Failed to stop activity timers, you may have to kill me")
    
CPmodule_logger.info("Seniorplay stopped.")

from SPWidgets import Dialog

try:
    import SPlogCheck
except (ImportError, utils.SPError),  info:
    text = _("Failed to parse the logfile, please contact the developers.\nMessage was: %s" % info)
    dlg = Dialog(text, buttons=[_('OK')], title=_('Warning !'))
    dlg.run()
except utils.MyError, info:
    text = "%s" % info
    #dlg = Dialog(text, buttons=[_('OK')], title=_('Warning !'))
    #dlg.run()
    
#if sys.platform == "linux2":
#    CPmodule_logger.info("Removing pyc files")
#    subprocess.Popen('find . -name "*.pyc" -exec rm {} \;',shell=True )

# BT+ specific stuff
if CMD_Options.theme == 'braintrainer' and CMD_Options.fullscreen:
    import os
    # TODO: Rene, make sure these hardcoded paths are correct
    pid=os.spawnl(os.P_NOWAIT,'/usr/local/bin/control_panel','/usr/local/bin/control_panel')
    CPmodule_logger.debug("launched Control Panel with pid %s" % pid)


