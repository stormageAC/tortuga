/*
 *  BinDetector.h
 *  
 *
 *  Created by Daniel Hakim on 6/22/07.
 *  Copyright 2007 Daniel Hakim. All rights reserved.
 *
 */

#ifndef RAM_BIN_DETECTOR_H_06_23_2007
#define RAM_BIN_DETECTOR_H_06_23_2007

#include <iostream>
#include <sstream>
#include <math.h>
#include <cstdlib>
#include <unistd.h>
#include <stdio.h>
#include "cv.h"
#include "highgui.h"
#include <string>
#include "vision/include/main.h"
#include "vision/include/ProcessList.h"
#include "vision/include/VisionCommunication.h"
#include "vision/include/OpenCVCamera.h"
#include "vision/include/OpenCVImage.h"
#include "vision/include/Image.h"
#include "vision/include/Camera.h"

namespace ram { namespace vision {
	class BinDetector
	{
		int found;
		int binX;
		int binY;
		int binCount;
		BinDetector(ram::vision::OpenCVCamera*);
		~BinDetector();
		void update();
	
		ram::vision::Image* frame;
		ram::vision::Camera* cam;
	}
	
}}//ram::vision

#endif // RAM_BIN_DETECTOR_H_06_23_2007
