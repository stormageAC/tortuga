# Copyright (C) 2007 Maryland Robotics Club
# Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:   sandbox/gui_example/src/oci/app.py

# Python Imports
import time
import sys
import os
import optparse

# Library Imports
import yaml

# Project Imports
import ext.core

# To register the makers
import ram
import ext.vision
import ext.vehicle
import ext.core
import ext.math
import ext.control

import ram.logloader as logloader
import ram.ai.gate
#import ram.ai.sonarCourse
#import ram.ai.buoySonarCourse
#import ram.ai.buoyPipeSonarCourse
import ram.ai.sonar

try:
    import ctypes
    import platform
    end = 'so'
    if 'Darwin' == platform.system():
        end = 'dylib'
    ctypes.CDLL("libram_network." + end, mode = ctypes.RTLD_GLOBAL)
except OSError, e:
    print e

def main(argv = None):
    if argv is None:
        argv = sys.argv

    defaultConfigPath = os.path.abspath(
        os.path.join(os.environ['RAM_SVN_DIR'], 'tools', 'oci', 'data', 
                     'transdec.yml'))
    
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest = "configPath", 
                      default = defaultConfigPath,
                      help = "The path to the config file")
    parser.add_option("-s", "--state", dest = "startState",
                      default = "ram.ai.course.Gate",
                      help = "The state we are starting with")
    (options, args) = parser.parse_args(argv)

    # Create our C++ app
    app = ext.core.Application(options.configPath)

    # Hackish way to grab state machine then start the vehicle
    stateMachine = app.getSubsystem("StateMachine")
    stateMachine.start(logloader.resolve(options.startState))
    #stateMachine.start(ram.ai.buoySonarCourse.Gate)
    #stateMachine.start(ram.ai.buoyPipeSonarCourse.Gate)
    #stateMachine.start(ram.ai.sonar.Searching)

    # Run the main loop such that only the QueuedEventHub is being updated,
    # and its waits for events, basically leave all the CPU to other stuff
    #queuedEventHub = app.getSubsystem("QueuedEventHub")
    #queuedEventHub.setWaitUpdate(True)
    app.mainLoop(singleSubsystem = True)
    
    # Built a list of subsystems
    #subsystems = []
    #names = app.getSubsystemNames()
    #for i in xrange(0, len(names)):
    #    subsystems.append(app.getSubsystem(names[i]))

    # Filter that list based on what is backgrounded or not
    #runningSubsystems = [s for s in subsystems if not s.backgrounded()]

    #print "Running subsystems",runningSubsystems
    #print "Subsystems",type(subsystems)
    #for subsystem in subsystems:
    #    print subsystem.unbackground(True)
    #del subsystems
    #del runningSubsystems
    #del app

if __name__ == "__main__":
    try:
        sys.exit(main())
    except yaml.scanner.ScannerError, e:
        print str(e)
