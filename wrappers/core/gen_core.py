# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

# STD Imports
import pprint

# Library Imports
from pyplusplus import module_builder

# Project Imports
import buildfiles.wrap as wrap

def export_typedef(ns, typedef):
    cls = ns.typedef(typedef).type.declaration
    cls.rename(typedef)
    cls.include()
    return cls

def expose_publisher(local_ns, cls_name):
    ePublisher = local_ns.class_(cls_name)
    ePublisher.include()

    # Replace 'subscribe' method
    ePublisher.member_function('subscribe').exclude()
    ePublisher.add_declaration_code("""
    ram::core::EventConnectionPtr pysubscribe(ram::core::%s & epub,
                                              std::string type,
                                              boost::python::object pyFunction)
    {
        return epub.subscribe(type, EventFunctor(pyFunction));
    }
    """ % (cls_name))
    ePublisher.add_registration_code(
        'def("subscribe", &::pysubscribe)', works_on_instance = True )
    ePublisher.include_files.append('wrappers/core/include/EventFunctor.h')
    ePublisher.include_files.append('core/include/EventConnection.h')
    return ePublisher

def generate(module_builder, local_ns, global_ns):
    """
    local_ns: is the namespace that coresponds to the given namespace
    global_ns: is the module builder for the entire library
    """

    local_ns.exclude()
    classes = []

    # ConfigNode
    ConfigNode = local_ns.class_('ConfigNode')
    ConfigNode.include()
    ConfigNode.constructors().exclude()
    classes.append(ConfigNode)

    # Event Subsystem
    EventPublisher = expose_publisher(local_ns, 'EventPublisher')
    EventPublisher.include_files.append('core/include/EventHub.h')
    classes.append(EventPublisher)

    QueuedEventPublisher = expose_publisher(local_ns, 'QueuedEventPublisher')
    classes.append(QueuedEventPublisher)

    # EventConnection
    EventConnection = local_ns.class_('EventConnection')
    EventConnection.include()
    EventConnection.include_files.append('core/include/EventConnection.h')
    
    Event = local_ns.class_('Event')
    Event.include()
    classes.append(Event)

    # IUpdatable
    IUpdatable = local_ns.class_('IUpdatable')
    IUpdatable.include()
    classes.append(IUpdatable)

    # Application
    Application = local_ns.class_('Application')
    Application.include()

    # Replace getSubsystem with one which uses our converter
    Application.member_function('getSubsystem').exclude()
    Application.add_declaration_code("""
    boost::python::object pyGetSubsystem(ram::core::Application& app,
                                         std::string subsystemName)
    {
        ram::core::SubsystemPtr subsystem = app.getSubsystem(subsystemName);
        return ram::core::SubsystemConverter::convertObject(subsystem);
    }
    """)
    Application.add_registration_code(
        'def("getSubsystem", &::pyGetSubsystem)', works_on_instance = True )
    Application.include_files.append('core/include/SubsystemConverter.h')
    
    classes.append(Application)

    # Add registrations functions for hand wrapped classes
    module_builder.add_registration_code("registerSubsystemList();")
    module_builder.add_registration_code("registerSubsystemClass();")
    module_builder.add_registration_code("registerSubsystemMakerClass();")
    module_builder.add_registration_code("registerEventHubClass();")
    module_builder.add_registration_code("registerQueuedEventHubClass();")


    # Do class wide items
    wrap.set_implicit_conversions([Application, QueuedEventPublisher,
                                   EventPublisher], False)
    wrap.add_needed_includes(classes)
    return ['wrappers/core/include/RegisterFunctions.h']

    #local_ns.class_('Updatable').include()
    #local_ns.class_('IUpdatable').include()
    
#    local_ns.class_('ConfigNode').include()
#    local_ns.class_('ConfigNodeImp').include()
#    local_ns.class_('PythonConfigNodeImp').include()
