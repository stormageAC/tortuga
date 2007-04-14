# Copyright (C) 2007 Maryland Robotics Club
# Copyright (C) 2007 Joseph Lisee <jlisee@umd.edu>
# All rights reserved.
#
# Author: Joseph Lisee <jlisee@umd.edu>
# File:   /sim/scene.py


# Python imports
import imp
import sys
import os.path

# Library Ipmorts
import ogre.renderer.OGRE as Ogre
import ogre.physics.OgreNewt as OgreNewt

# Project Imports
import core
import sim.defaults as defaults
from sim.util import SimulationError
from sim.serialization import ModuleLoader
from sim.physics import World
from core import fixed_update, log_init

class SceneError(SimulationError):
	pass


class ISceneLoader(core.Interface):
    """
    Provides an abstract interface to loading a scene.
    """
    
    def can_load(name):
        """
        This is a static method of the class it looks at the name to determine
        if the scene is of a type it can load.
        
        @type name: string
        @param name: The absolute path to the scene file
        
        @rtype: bool
        @return: True if loader can load the scene, false if not
        """
        pass
    
    def load(scene_file, scene):
        """
        Loads the scene from the file into the given scene object.
        
        @type scene_file: string
        @param scene_file: The absolute path to the scene file
        
        @type scene: Scene
        @param scene: The scene into which the objects should be placed
        """
        pass



class Scene(object):
    """
    This provides access to all objects in the scene, be they cameras, robots,
    or just obstacles.
    """
    
    scene_loaders = core.ExtensionPoint(ISceneLoader)    
    
    #@log_init(defaults.sim_log_config)
    def __init__(self, name, scene_data):
        """
        @type name: string
        @param name: The name of scene
        
        @type  scene_data: Anything
        @param scene_data: The object that will be passed to the scene loader
        """
        self.name = name
        self._objects = {}
        self._bodies = []
        self._robots = {}
        self._physics_update_interval = 1.0 / 60
        
        # Create Ogre SceneManager and OgreNewt World
        self._scene_manager = \
            Ogre.Root.getSingleton().createSceneManager(Ogre.ST_GENERIC,
                                                        self.name)
        self._world = World()
        
        # Search for a scene loader compatible with file format then load it
        loaders = [loader for loader in self.scene_loaders \
                   if loader.can_load(scene_data) ]
        
        if len(loaders) == 0:
            raise SceneError('No Loader found for "%s".' % scene_file)
        
        loader = loaders[0]()
        loader.load(scene_data, self)

    class scene_mgr(core.cls_property):
        """
        The Ogre scene manager for the scene
        """
        def fget(self):
            return self._scene_manager
		
    class world(core.cls_property):
        """
        The Physical world in the simulation
        """
        def fget(self):
            return self._world

    def update(self, time_since_last_update):
        self._update_physics(time_since_last_update)
        
        # Update all of our objects
        for obj in self._objects.itervalues():
           obj.update(time_since_last_update)
        pass
    
    @fixed_update('_physics_update_interval')
    def _update_physics(self, time_since_last_update):
        """
        Updates the physics of the sim at a rate near the 
        _physics_update_interval attribute of the object.
        """
        self._world.update(time_since_last_update)
        
    def save(self, location):
    	raise SceneError("Save not yet implemented")
        # TODO: Finish me
	
    def reload(self):
        raise SceneError("Reload not yet implemented")
        # TODO: Finish me
        
    def add_resource_locations(self, location_map):
        """
        Adds resouce location to the scene internal resource group.  This 
        resources will only be after the scene is loaded initialized.
		
        @type location_map: dict: string to string
        @param location_map: maps resource type, to its location.  Valid types
        					 are 'Zip' and 'FileSystem'.
		"""
        #self.logger.info('Adding resources locations')
        
#        print 'Adding resource locations'
#        print location_map
        rsrc_mrg = Ogre.ResourceGroupManager.getSingleton()
        for resource_type in location_map:
#        	self.logger.info('/tAdding resources of type: %s' % resource_type)
#        	print '\tAdding resources of type: %s' % resource_type
        	for location in location_map[resource_type]:
#        		print '\t',location_map[resource_type]
#        		print '\t\t-',location
          		location = os.path.abspath(location)
#          		self.logger.info('/t/tAdding location: %s' % location)
#          		print '\t\tAdding location: %s' % location
          		rsrc_mrg.addResourceLocation(location, resource_type,
											 self.name, False)
        rsrc_mrg.initialiseResourceGroup(self.name)
	
    def create_object(self, obj_type, *args, **kwargs):
        """
        Creates an object

        @type type: Interface
        @param type: The interface
        """
        kwargs['scene'] = self
        core.Component.create(obj_type, *args, **kwargs)
	
class ModuleSceneLoader(core.Component, ModuleLoader):
	"""
	Loads a scene by loading a python module from file and executing the
	create_scene method.
	
	B{Implements:}
	 - ISceneLoader
	"""
	
	core.implements(ISceneLoader)
	
	# ISceneLoader Methods
	def load(self, scene_file, scene):
		"""
		Uses the python imp module to load the module given the path to it.
		"""
		scene_mod = ModuleLoader.load(self, scene_file)
		scene._bodies.extend(scene_mod.create_scene(self, scene))
	
	# End ISceneLoader Methods