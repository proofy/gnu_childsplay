# Copyright (c) 2007 Chris Van Bael <chris.van.bael@gmail.com>
#
#           setup.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.



# Bootstrap setuptools, will install if isn't installed yet
#from ez_setup import use_setuptools
#use_setuptools()

from setuptools import setup
from schoolsplay import SPVersion
import sys, os, shutil, string
import pygame
import wx

# Minimum requirements
PYTHON_MINIMUM = (2, 4)
PYGAME_MINIMUM = (1, 7, 1)
OCEMPG_MINIMUM = '0.2.6'


# Stuff that can change regurarly
PATCH_VERSION = ""
# nothing when you release a main version, eg '' gives 0.85.1
# '_x' when you release a patch version, eg 0.85.1_1 needs '_1'
DATA_DIRS = ['locale', 'share']
SP_MODULES = []

ocemp_orig = ''
ocemp_copy = ''

def run_checks ():
    # Python version check.
    if sys.version_info < PYTHON_MINIMUM: # major, minor check
        raise Exception ("You should have at least Python >= %d.%d.x installed." % PYTHON_MINIMUM)

    # Pygame versioning checks.
    pygame_version = None
    try:
        import pygame
        if pygame.version.vernum < PYGAME_MINIMUM:
            raise Exception ("You should have at least Pygame >= %d.%d.%d installed" % PYGAME_MINIMUM)
        pygame_version = pygame.version.ver
    except ImportError:
        pass
        
    # OcempGui versioning checks.
    ocempg_version = None
    try:
        import ocempgui
        if ocempgui.__version__ < OCEMPG_MINIMUM:
            raise Exception ("You should have at least OcempGui >= " + OCEMPG_MINIMUM + " installed")
        ocempg_version = ocempgui.__version__
    except ImportError:
        pass    

def get_data_files():
    global ocemp_orig
    global ocemp_copy

    # 1st get PyGame font and icon files
    pygamedir = os.path.split(pygame.base.__file__)[0]
    pygamefiles = [os.path.join(pygamedir, pygame.font.get_default_font()), os.path.join(pygamedir, 'pygame_icon.bmp')]
    datafiles = [('./pygame', pygamefiles)]

    # 2nd add files in Schoolsplay dir made & needed by Schoolsplay
    datafiles.append(('.', SP_MODULES))
    
    # 3rd add OCempGui data files (themes) and now change temporarily the path
    import ocempgui.widgets.Constants
    old_DEFAULTDATADIR = ocempgui.widgets.Constants.DEFAULTDATADIR
    for dirpath, dirnames, filenames in os.walk(old_DEFAULTDATADIR):
        for name in filenames:
            datafiles.append((os.path.join('./themes', dirpath.lstrip(old_DEFAULTDATADIR)), [os.path.join(dirpath, name)]))

    # Here I presume you have set you PYTHONPATH variable
    ocemp_orig =  os.path.join(os.environ['PYTHONPATH'], 'Lib', 'site-packages', 'ocempgui', 'widgets', 'Constants.py')
    ocemp_copy =  os.path.join(os.environ['PYTHONPATH'], 'Lib', 'site-packages', 'ocempgui', 'widgets', 'Constants.old')    
     
    shutil.copyfile(ocemp_orig, ocemp_copy)
    fpin = open(ocemp_orig, 'r').read()
    fpin = fpin.replace(old_DEFAULTDATADIR, '.')
    fpout = open(ocemp_orig, 'w')
    fpout.write(fpin)        
    fpout.close()    
    
    
    # 4th add all files in all subdirectories for DATA_DIRS
    for directory in DATA_DIRS:
        for dirpath, dirnames, filenames in os.walk(directory):
            for name in filenames:
                datafiles.append((dirpath, [os.path.join(dirpath, name)]))
                
    # 5th add necessary WxWindows DLLs (msvcp71.dll)
    wxdir = wx.__path__[0]
    wxdll = [os.path.join(wxdir, 'msvcp71.dll'), ]
    datafiles.append(('.', wxdll ))
                
    return datafiles
    
    
if __name__ == "__main__":
    run_checks ()
    
    # Delete output directories
    try:
        shutil.rmtree('build')
        shutil.rmtree('dist')
    except:
        print('ERROR: Could not delete output directories')
    
    # Standard distutils.core arguments
    generic_data = {
        "name": "Schoolsplay",
        "version": SPVersion.version,
        "description": "Collection of educational activities",
        "author": "Stas Zykiewicz",
        "author_email": "stas.zytkiewicz@gmail.com",
        "maintainer": "Chris Van Bael - Windows/Mac versions",
        "maintainer_email": "chris.van.bael@gmail.com",
        "license": "GPL v2",
        "url": "http://Schoolsplay.sourceforge.net",
        "packages": [],
        "data_files": get_data_files(),
        }
       # "cmdclass": { "install_data" : InstallData },
       # }
    
    
    if sys.argv[1] == 'py2exe':
        # Making Windows executable and installer
        import py2exe
        
        # Extra keywords related to py2exe
        extra_data = {
            "windows": [{ "script": "./bin/Schoolsplay",
                          "icon_resources": [(1, "Schoolsplay.ico")]
                       }],
            "options": {"py2exe": { 
                            "optimize": 0,
                            "bundle_files": 3,
                            "excludes": ['dotblas', 'email'],
                            "includes": ['pygame.*', 'shlex', 'encodings', 'encodings.*', 
                                         'pysqlite2.dbapi2', 
                                         'schoolsplay.lib.*', 'schoolsplay.Timer', 
                                         'sqlalchemy', 'sqlalchemy.*', 'sqlalchemy.mods.*',
                                         'sqlalchemy.databases.*', 'sqlalchemy.engine.*', 
                                         'sqlalchemy.ext.*', 'sqlalchemy.orm.'],}
            },
        }        
        
        setup_data = {}
        setup_data.update(generic_data)
        setup_data.update(extra_data)
        
        # Now make the executable
        sys.argv += ["--skip-archive"]
        setup(**setup_data)
        
        # Change back the OCempGui data dir reference
        shutil.copyfile(ocemp_copy, ocemp_orig)
        
        # Make InnoSetup script setup.iss from generic.iss
        print "Adapting the InnoSetup script: generic.iss..."
        setupfile =  os.path.join(os.path.dirname(os.path.abspath (sys.argv[0])), 'dist', 'setup.iss')
        
        fpin = open('generic.iss', 'r').read()
        fpin = fpin.replace('$AppVerName$', 'Schoolsplay ' + SPVersion.version + PATCH_VERSION)
        fpin = fpin.replace('$AppVersion$', SPVersion.version)
        fpin = fpin.replace('$VersionInfoVersion$', SPVersion.version)
        fpin = fpin.replace('$OutputBaseFilename$', 'Schoolsplay-' + SPVersion.version + PATCH_VERSION + '_win32')
        fpin = fpin.replace('$BaseDir$', os.path.join(os.path.dirname(os.path.abspath (sys.argv[0]))))
        fpout = open(setupfile, 'w')
        fpout.write(fpin)        
        fpout.close()
        
        # Launch InnoSetup
        print "Running Innosetup with setup.iss, please wait..."
        cmd = "C:\Programs\Innose~1\Compil32.exe /cc " + setupfile
        print cmd
        os.system(cmd)
        
        print "Finished!"
        
        
#***************************************************************************
# current problems:
# **************************************************************************        
        
        
    
    elif sys.argv[1] == 'py2app':
        # Making Mac OSX executable and disk image
        from setuptools import setup

        # Extra keywords related to py2app
        extra_data = {
            "app": ['/bin/schoolsplay'],
            "setup_requires": ['py2app'],
            "options": {"argv_emulation": True,
                        "iconfile": os.path.join(os.path.dirname(os.path.abspath (sys.argv[0])), "data","Schoolsplay.icns")},
        }
        
        setup_data = {}
        setup_data.update(generic_data)
        setup_data.update(extra_data)
        
        # Now make the application
        setup(**setup_data)        
        
        # Adapt the Disc iMaGe and let ??? make it

#***************************************************************************
# current problems:
# Timer.py not included -> maybe solved by data_files???
# others?
# **************************************************************************          
        
   
    elif sys.argv[1] == 'install':
        # Install in existing Python environment
        print get_data_files()
        shutil.copyfile(ocemp_copy, ocemp_orig)        
        pass
    
    else: 
        print "What do you want to do?"
        print "python setup.py py2exe  -> makes Windows exe"
        print "python setup.py py2app  -> makes Mac OSX exe"
        print "python setup.py install -> installs in Python"