/*
 * Copyright (C) 2007 Robotics at Maryland
 * Copyright (C) 2007 Daniel Hakim
 * All rights reserved.
 *
 * Author: Daniel Hakim <dhakim@umd.edu>
 * File:  packages/vision/src/BlobDetector.cpp
 */

#define _CRT_SECURE_NO_WARNINGS

// STD Includes
#include <math.h>
#include <cstdlib>
#include <cassert>
#include <algorithm>
#include <iostream>

// Library Includes
#include "cv.h"
#include "highgui.h"
#include <boost/foreach.hpp>

// Project Includes
#include "vision/include/Image.h"
#include "vision/include/BlobDetector.h"

namespace ram {
namespace vision {

BlobDetector::BlobDetector(core::ConfigNode config,
                           core::EventHubPtr eventHub) :
    Detector(eventHub),
    data(0),
    m_dataSize(0)
{
    init(config);
}

BlobDetector::~BlobDetector()
{
    free(data);
}
    
void BlobDetector::processImage(Image* input, Image* output)
{
    m_blobs.clear();
    histogram(input->asIplImage());

    // Do debug stuff soon
    if (0 != output)
    {
        output->copyFrom(input);
        
        CvPoint boundUR;
        CvPoint boundLL;
        
        BOOST_FOREACH(Blob blob, m_blobs)
        {
            // Draw bounds around blob
            boundUR.x = blob.getMaxX();
            boundUR.y = blob.getMaxY();
            boundLL.x = blob.getMinX();
            boundLL.y = blob.getMinY();

            cvRectangle(output->asIplImage(), boundUR, boundLL,
                        CV_RGB(0,255,0), 2, CV_AA, 0);
        }
    }
}
    
bool BlobDetector::found()
{
    return m_blobs.size() > 0;
}

std::vector<BlobDetector::Blob> BlobDetector::getBlobs()
{
    return m_blobs;
}
    
void BlobDetector::init(core::ConfigNode)
{
    // Pre-allocate memory
    joins.reserve(1024);
    pixelCounts.reserve(1024);
    totalX.reserve(1024);
    totalY.reserve(1024);
    totalMinX.reserve(1024);
    totalMaxX.reserve(1024);
    totalMinY.reserve(1024);
    totalMaxY.reserve(1024);

    ensureDataSize(640 * 480);
}
    
int BlobDetector::histogram(IplImage* img)
{
    int width=img->width;
    int height=img->height;
    unsigned char* imgData=(unsigned char*)img->imageData;
    // Make sure the data array is large enough
    ensureDataSize(width * height);
    
    joins.resize(1, UINT_MAX);
    pixelCounts.resize(1, 0);
    totalX.resize(1, 0);
    totalY.resize(1, 0);
    totalMinX.resize(1, 0);
    totalMaxX.resize(1, 0);
    totalMinY.resize(1, 0);
    totalMaxY.resize(1, 0);
        
    unsigned int index=1;
    // Black out the top row, front edge so the above and left algos
    // work properly
    int imgCount=0;
    int count = 0;
    memset(imgData, 0, width * 3);
    memset(data, 0, sizeof(*data) * width);
/*    for (int x=0;x<width;x++)
    {
        imgData[imgCount]=imgData[imgCount+1]=imgData[imgCount+2]=0;
        data[count] = 0;
        imgCount+=3;
        count++;
    }
    imgCount=0;
    count = 0;*/
    for (int y=0;y<height;y++)
    {
        imgData[imgCount]=imgData[imgCount+1]=imgData[imgCount+2]=0;
        data[count]=0;
        imgCount+=3*width;
        count += width;
    }
    imgCount=0;
    count = 0;


    // Loop over every pixel
    for (int y=0; y<height;y++)
    {
        for (int x=0; x<width;x++)
        {
            // Check for a marked (ie. white) pixel
            if (imgData[imgCount]>0)
            {
                // Found a valid pixel, check the value above and below it
                unsigned int above=data[count-width];
                unsigned int left=data[count-1];
                if (above==0 && left==0)
                {
                    // Start of a new blob
                    
                    //int neededSize = index + 1;
                    //int presentSize = pixelCounts.size();
                    //assert((presentSize + 1) == neededSize);
                
                    pixelCounts.push_back(1);
                    totalX.push_back(x);
                    totalY.push_back(y);
                    totalMinX.push_back(x);
                    totalMaxX.push_back(x);
                    totalMinY.push_back(y);
                    totalMaxY.push_back(y);
                    joins.push_back(index);
                    //assert((index + 1) == (totalX.size()));
                    
                    data[count]= (index++);
                }
                else 
                {
                    // Continuation of an existing blob
                    unsigned int above2=above;
                    unsigned int left2=left;
                    if (above2==0)
                        above2=UINT_MAX;
                    else
                    {
                        //assert(above2 <= index);
                        //assert((int)joins.size() >= (above2 + 1));
                            
                        while (above2!=joins[above2])
                            above2=joins[above2];
                    }
                    if (left2==0)
                        left2=UINT_MAX;
                    else
                    {
                        //assert(left2 <= index);
                        //assert((int)joins.size() >= (left2 + 1));
                            
                        while (left2!=joins[left2])
                            left2=joins[left2];
                    }

                    //if ((left2 == above2) && (left2 == UINT_MAX))
                    //{
                    //    assert(false && "error");
                    //}
                    
                    // More sanity checks
                    //assert(left <= index);
                    //assert((int)joins.size() >= (left + 1));
                        
                    //assert(above <= index);
                    //assert((int)joins.size() >= (above + 1));

                    unsigned int idx = std::min(left2,above2);
                    joins[above]= idx;
                    joins[left]= idx;
                    data[count]= idx;

                    // Small sanity checks for refactoring
                    //assert(data[count] <= index);
                    //assert((int)totalX.size() >= (data[count] + 1));
                        
                    totalX[idx]+=x;
                    totalY[idx]+=y;
                    ++pixelCounts[idx];
                                        
                    // Min/Max
                    if (x < totalMinX[idx])
                        totalMinX[idx] = x;
                    else if (x > totalMaxX[idx])
                        totalMaxX[idx] = x;
                    if (y < totalMinY[idx])
                        totalMinY[idx] = y;
                    else if (y > totalMaxY[idx])
                        totalMaxY[idx] = y;
                }
            }
            count++;
            imgCount += 3;
        }
    }

    int maxCount=0;

    // Work from the top to bottom, collapsing the pixel clusters together
    for (unsigned int i=index-1;i>0;i--)
    {
        unsigned int join = joins[i];

        // Catch sentinal to make the first join, point to the last
        if (join == UINT_MAX)
            join = joins.size() - 1;
        
        //assert(join <= index);
        if (join!=i)
        {
            // "Unfinished" cluster of pixels, ie part of bigger cluster
            // So add all of its information to the parents information
            totalX[join]+=totalX[i];
            totalY[join]+=totalY[i];

            // Mins
            if (totalMinX[i] < totalMinX[join])
                totalMinX[join] = totalMinX[i];
            if (totalMinY[i] < totalMinY[join])
                totalMinY[join] = totalMinY[i];

            // Maxs
            if (totalMaxX[i] > totalMaxX[join])
                totalMaxX[join] = totalMaxX[i];
            if (totalMaxY[i] > totalMaxY[join])
                totalMaxY[join] = totalMaxY[i];

            pixelCounts[join]+=pixelCounts[i];
            pixelCounts[i]=0;
        }
        else
        {
            maxCount=pixelCounts[i];
            // Found a final cluster
            m_blobs.push_back(
                   BlobDetector::Blob(pixelCounts[i], totalX[i]/maxCount,
                             totalY[i]/maxCount, totalMaxX[i], totalMinX[i],
                             totalMaxY[i], totalMinY[i])
                                    );
        }
    }

    //Deallocate arrays
    //    cout<<"Happily reaching the end of histogram"<<endl;
    return maxCount;
}

void BlobDetector::ensureDataSize(int pixels)
{
    size_t bytes = (size_t)pixels * sizeof(*data);
    if (m_dataSize < (size_t)pixels)
    {
        m_dataSize = (int)pixels;
        if (data)
            data = (unsigned int*)realloc(data, bytes);
        else
            data = (unsigned int*)malloc(bytes);
    }
}
    
} // namespace vision
} // namespace ram