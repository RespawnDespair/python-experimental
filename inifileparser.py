#!/usr/bin/python

import configparser
import subprocess
import sys, getopt
import os
import sys
import re
import importlib

def main(argv):
     mode = ''
     try:
          opts, args = getopt.getopt(argv,"hm:",["mode="])
     except getopt.GetoptError:
          print 'test.py -m <mode> (AIR or GND)'
          sys.exit(2)

     for opt, arg in opts:
          if opt == '-h':
               print 'test.py -m <mode> (AIR or GND)'
               sys.exit()
          elif opt in ("-m", "--mode"):
               mode = arg

     print 'Mode is:', mode

     print 'Loading card modules'

     card_modules=load_card_modules()

     for mod in card_modules:
          print mod

     print 'Loading camera modules'
     camera_modules=load_camera_modules()
     
     for cam in camera_modules:
          print cam

     config = configparser.ConfigParser()

     cameras = []
     cards = []
     wifi = []

     config.read('cameras.ini')
     camera_sections = config.sections()
     
     for camkey in camera_sections:  
          for cameramod in camera_modules:
               if cameramod.fitForType(config[camkey]['type']):
                    print 'Loading camera module for', camkey, config[camkey]['type']
                    loaded_class = getattr(cameramod, 'Camera')
                    camera=loaded_class(camkey)
                    cameras.append(camera)
               else:
                    print 'No suitable camera plugin found for', config[camkey]['type']

     print('Detecting available WiFi cards')

     # Get the list of network devices
     networkdevices = subprocess.Popen(['ls', '/sys/class/net'], stdout = subprocess.PIPE).communicate()[0].split('\n')

     for device in networkdevices: 
          print(device)

          if (device.startswith('wlan')):
               print('This is a WLAN device')

               cmd="cat /sys/class/net/{0}/device/uevent|nice grep DRIVER|sed 's/DRIVER=//'".format(device)
               driver=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].rstrip()
               print('   Driver type: {0}'.format(driver))

               card = None
               for cardmod in card_modules:
                    if cardmod.fitForDriver(driver):
                         loaded_class = getattr(cardmod, 'Card')
                         card=loaded_class(device, mode)
                         card.extendedSetup()
                         wifi.append(card)

          else:
               print('Not a known WLAN device, leaving it alone')
     
     print("Loaded wifi cards")
     for wificard in wifi:
          print(wificard)

def load_card_modules():
     """
     Load all the different Card modules. 
     Every module should have a class named 'Card'
     """
     pysearchre = re.compile('.py$', re.IGNORECASE)
     pluginfiles = filter(pysearchre.search,
                           os.listdir(os.path.join(os.path.dirname(__file__),
                                                 'cards')))
     form_module = lambda fp: '.' + os.path.splitext(fp)[0]
     plugins = map(form_module, pluginfiles)
     # import parent module / namespace
     importlib.import_module('cards')
     modules = []
     for plugin in plugins:
               if '__' not in plugin:
                    modules.append(importlib.import_module(plugin, package="cards"))

     return modules

def load_camera_modules():
     """
     Load all the different Camera modules. 
     Every module should have a class named 'Camera'
     """
     pysearchre = re.compile('.py$', re.IGNORECASE)
     pluginfiles = filter(pysearchre.search,
                           os.listdir(os.path.join(os.path.dirname(__file__),
                                                 'cameras')))
     form_module = lambda fp: '.' + os.path.splitext(fp)[0]
     plugins = map(form_module, pluginfiles)
     # import parent module / namespace
     importlib.import_module('cameras')
     modules = []
     for plugin in plugins:
               if '__' not in plugin:
                    modules.append(importlib.import_module(plugin, package="cameras"))

     return modules

if __name__ == "__main__":
   main(sys.argv[1:])




