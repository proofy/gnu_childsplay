TemplateString = \
'''
# -*- coding: utf-8 -*-

# Copyright (c) %(year)s %(dev_name)s %(dev_email)s
#
#           %(name)s.py
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

#create logger, logger was setup in SPLogging
import logging
# In your Activity class -> 
# self.logger =  logging.getLogger("schoolsplay.%(name)s.Activity")
# self.logger.error("I don't understand logger")
# See SP manual for more info 

module_logger = logging.getLogger("schoolsplay.%(name)s")

# standard modules you probably need
import os,sys

import pygame
from pygame.constants import *

import childsplay_sp.utils as utils
from childsplay_sp.SPConstants import *
import childsplay_sp.SPSpriteUtils as SPSpriteUtils

# containers that can be used globally to store stuff
class Img:
    pass
class Snd:
    pass

class Activity:
    """  Base class mandatory for any SP activty.
    The activity is started by instancing this class by the core.
    This class must at least provide the following methods.
    start (self) called by the core before calling 'next_level'.
    post_next_level (self) called once by the core after 'next_level' *and* after the 321 count. 
    next_level (self,level) called by the core when the user changes levels.
    loop (self,events) called 40 times a second by the core and should be your 
                      main eventloop.
    get_helptitle (self) must return the title of the game can be localized.
    get_help (self) must return a list of strings describing the activty.
    get_helptip (self) must return a list of strings or an empty list
    get_name (self) must provide the activty name in english, not localized in lowercase.
    stop_timer (self) must stop any timers if any.
  """

    def __init__(self,SPGoodies):
        """SPGoodies is a class object that SP sets up and will contain references
        to objects, callback methods and observers
        TODO: add more explaination"""
        self.logger =  logging.getLogger("schoolsplay.%(name)s.Activity")
        self.logger.info("Activity started")
        self.SPG = SPGoodies
        self.screen = self.SPG.get_screen()
        self.orgscreen = self.screen.convert()# we use this to restore the screen
        self.backgr = self.SPG.get_background()
        # The location of the activities Data dir
        self.my_datadir = os.path.join(self.SPG.get_libdir_path(),'CPData','%(datadirname)s')
        # Location of the CPData dir which holds some stuff used by multiple activities
        self.CPdatadir = os.path.join(self.SPG.get_libdir_path(),'CPData')
        # Location of the alphabet sounds dir
        self.absdir = self.SPG.get_absdir_path()# alphabet sounds dir
        # You MUST call SPInit BEFORE using any of the SpriteUtils stuff
        # it returns a reference to the special CPGroup
        self.actives = SPSpriteUtils.SPInit(self.screen,self.backgr)
        
        # Remove these four lines
        text = "Template activity, hit the stop button"
        surf = utils.char2surf(text,48,RED)
        self.screen.blit(surf,(100,200))
        pygame.display.flip()
    
    def clear_screen(self):
        self.screen.blit(self.orgscreen,(0,0))
        self.backgr.blit(self.orgscreen,(0,0))
        pygame.display.update()

    def get_helptitle(self):
        """Mandatory method"""
        return _("%(Name)s")
    
    def get_name(self):
        """Mandatory method, returnt string must be in lowercase."""
        return "%(name)s"
    
    def get_help(self):
        """Mandatory methods"""
        text = [_("The aim of this activity:"),
        _(""),
        " ",
        _("Difficulty :  years"),
        " "]
        return text 
    
    def get_helptip(self):
        """Mandatory method, when no tips available returns an empty list"""
        return []
        
    def get_helptype(self):
        """Mandatory method, you must set an type"""
        # Possible types are: Memory, Math, Puzzle, Keyboardtraining, Mousetraining
        #                     Language, Alphabet, Fun, Miscellaneous
        return _("Miscellaneous")
    
    @splitpoint@
    
    def start(self):
        """Mandatory method."""
        pass
        
    def next_level(self,level,dbmapper):
        """Mandatory method.
        Return True if there levels left.
        False when no more levels left."""
        pass
        return True
    
    def post_next_level(self):
        """Mandatory method.
        This is called once by the core after 'next_level' *and* after the 321 count.
        You should place stuff in here that run in a seperate thread like sound play."""
        pass 
        
    def get_score(self,timespend):
        """Mandatory method.
        @timespend is the time spend inside the level as it's calculated
        by the core.
        returns the score value for the past level.
        return None if no score value is used"""
        m,s = timespend.split(':')
        seconds = int(m)*60 + int(s)
    
    def stop_timer(self):
        """You *must* provide a method to stop timers if you use them.
        The SPC will call this just in case and catch the exception in case 
        there's no 'stop_timer' method""" 
        try:
            self.timer.stop()
        except:
            pass

    def loop(self,events):
        """Mandatory method.
        This is the main eventloop called by the core 30 times a minute."""
        for event in events:
            if event.type is MOUSEBUTTONDOWN:
                pass
                # call your objects
        return 
        
'''

KludgeString =\
'''
    def get_helplevels(self):
        """Mandatory method, must return a string with the number of levels
        in the follwing format:
        _("This level has %s levels") % number-of-levels"""
        return _("This activity has %s levels") % 6
'''
