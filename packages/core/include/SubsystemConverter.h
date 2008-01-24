/*
 * Copyright (C) 2008 Robotics at Maryland
 * Copyright (C) 2008 Joseph Lisee <jlisee@umd.edu>
 * All rights reserved.
 *
 * Author: Joseph Lisee jlisee@umd.edu>
 * File:  packages/core/include/SubsystemConverter.h
 */

#ifndef RAM_CORE_SUBSYSTEMCONVERTER_H_01_13_2008
#define RAM_CORE_SUBSYSTEMCONVERTER_H_01_13_2008

// STD Includes
#include <string>
#include <set>

// Library Includes
#include <boost/python.hpp>

// Project Includes
#include "core/include/Subsystem.h"
#include "core/include/ToPythonConverter.h"

// Must Be Included last
#include "core/include/Export.h"

namespace ram {
namespace core {

typedef ToPythonConverter<Subsystem> SubsystemConverter;
    
template<class T>
class SpecificSubsystemConverter :
        public SpecificToPythonConverter<T, Subsystem>
{
};

} // namespace core
} // namespace ram
    
#endif // RAM_CORE_SUBSYSTEMCONVERTER_H_01_13_2008
