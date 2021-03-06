# -*- coding: utf-8 -*-

# Copyright (c) 2006 Stas Zykiewicz <stas.zytkiewicz@gmail.com>
#
#           SPOptionParser.py
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

# will becomes the thing to parse the options given at startup.
# returns a dict
import sys

from SPConstants import SUPPORTEDTHEMES
from SPVersion import optversion
from optparse import OptionParser

class OParser(OptionParser):
    def __init__(self):
        usage = "usage: %prog [options]"
        OptionParser.__init__(self, usage=usage, version=optversion)
        # set some reasonable defaults
        self.set_defaults(loglevel="error", \
            theme="default", \
            no_login=False, \
            remotemysqlserver='localhost', \
            kioskmode=False, \
            adminmode=False, \
            no_sound=False, \
            no_text=False,\
            admingui=False, \
            lang='system', \
            fullscreen=False, \
            bigcursor=False, \
            no_exit_question=False)
        # add possible options to the parser
        self.add_option("--no-login", action="store_true",
            help="Don't show login window. This will run schoolsplay in 'anonymous' mode which means that there will be no data collecting",
        dest="no_login")
        self.add_option("--kioskmode", action="store_true",
            help="Enable kioskmode. This will run schoolsplay in kioskmode which means that there will be no keyboard support.",
        dest="kioskmode")
        self.add_option("--remote-mysqlserver", action="store_true",
            help="(NOT USED YET)The ip nummer of the remote mySQL server.",
            dest="remotemysqlserver")
        self.add_option("-t", "--theme",
            help="Set the theme schoolsplay will use.",
            dest="theme")
        self.add_option("-l", "--loglevel",
            help="Set logging level. Possible values are: debug,info,warning,error,critical",
            dest="loglevel")
        self.add_option("--adminmode", action="store_true",
            help="Enable adminmode. This will run schoolsplay in adminmode which means that certain extra possibilities are enabled",
        dest="adminmode")
        self.add_option("--no-sound", action="store_true",
            help="Disable any sound. Be aware that certain activities that rely on sound won't start.",
        dest="no_sound")
        self.add_option("--no-text",action="store_true",
            help="Disable text before every level's activities.",
            dest="no_text")
        self.add_option("--admin-gui", action="store_true",
            help="Start the SQL administrator GUI. This is a simple GUI to set the mu and sigma values for the activities.",
        dest="admingui")
        self.add_option("--language",
            help="Set the language schoolsplay should use. Be aware that not all languages are supported yet. If your language isn't supported and you want to provide language support,please contact the schoolsplay team.",
            dest="lang")
        self.add_option("--fullscreen", action="store_true",
            help="Run schoolsplay in fullscreen mode.",
        dest="fullscreen")
        self.add_option("--bigcursor", action="store_true",
            help="Use a bigger (48x48) cursor.",
        dest="bigcursor")
        self.add_option("--no-exit-question", action="store_true",
            help="No 'are you sure?' questions will be asked",
            dest="noexitquestion")
        (self.options, self.args) = self.parse_args()
        # in case the user starts us with a unkown theme
        if self.options.theme not in SUPPORTEDTHEMES:
            self.options.theme = 'default'
    
    def exit(self,  * args):
        """This overrides the OptionParser exit method"""
        if args:
            print args[1]
            self.print_help()
        sys.exit(0)
        
    def get_options(self):
        return self.options

if __name__ == '__main__':
    op = OParser()
    print op.get_options()
    
    
    
    
