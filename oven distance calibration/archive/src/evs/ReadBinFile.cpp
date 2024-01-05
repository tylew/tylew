/*
 *
 * This is a C++ MEX-file for MATLAB.
 * Copyright 2017 The MathWorks, Inc.
 *
 */

#include "mex.hpp"
#include "mexAdapter.hpp"
#include "MatlabDataArray.hpp"

#include "evsfp_types.h"
#include <iostream>
#include <fstream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <numeric>
#include <stdlib.h>
#include <cstdint>
#include <iomanip>

using namespace matlab::data;
using matlab::mex::ArgumentList;

class MexFunction : public matlab::mex::Function {
private:
    matlab::data::ArrayFactory factory;
    std::shared_ptr<matlab::engine::MATLABEngine> matlabPtr;
    
public:
    //Create Output interface
    void operator()(matlab::mex::ArgumentList outputs, matlab::mex::ArgumentList inputs) {
        //matlab::data::TypedArray<double> inArray = inputs[0];
        const int iNrOfFrames = inputs[1][0];
        const int iNrOfShots = inputs[2][0];
        matlab::data::CharArray FileName= inputs[0];
        std::string szFileName = FileName.toAscii();
        TypedArray<uint32_t> result = factory.createArray<uint32_t>({iNrOfFrames,iNrOfShots,8});
        
        rxData_returns FramesData[iNrOfFrames][iNrOfShots];
        unsigned long size_of_buffer = 0;
        unsigned long size_of_frame = iNrOfShots * sizeof(rxData_returns) * 8;
        int errorCode = -1;
        int start = 0;
        int i = 0;
        int iNrOfShotsRead = -1;
        std::ifstream binfile(szFileName, std::ios::binary);
        //check if the binary file exist, otherwise throw error
        if (binfile.good())
        {
            std::vector<unsigned char> buffer(std::istreambuf_iterator<char>(binfile), {});
            auto src = (char*) new char[buffer.size()];
            std::copy(buffer.begin(), buffer.end(), src);
            size_of_buffer = buffer.size();
            binfile.close();
            if (0 == size_of_buffer)
            {
                errorCode = -3;
            }
            else
            {
                if((size_of_buffer-4)<((20*iNrOfShots+8)*iNrOfFrames))
                {
                    errorCode = -2;
                    iNrOfShotsRead = (((size_of_buffer-4)/iNrOfFrames)-8)/20;
                }
                else
                {
                    errorCode = 0;
                    iNrOfShotsRead = iNrOfShots;
                }
                
                for (int i = 0; i < iNrOfFrames; i++)
                {
                    start = 4 + 8 * (i + 1) + size_of_frame * i;
                    std::memcpy(FramesData[i], src + start, iNrOfShotsRead * sizeof(rxData_returns));
                    for (int j = 0; j < iNrOfShots; j++)
                    {
                        result[i][j][0] = FramesData[i][j].u_intensity;
                        result[i][j][1] = FramesData[i][j].u_distance;
                        result[i][j][2] = FramesData[i][j].u_elevation;
                        result[i][j][3] = FramesData[i][j].u_azimuth;
                        result[i][j][4] = FramesData[i][j].u_pixelRowIdWFoV;
                        result[i][j][5] = FramesData[i][j].u_pixelColIdWFoV;
                        result[i][j][6] = FramesData[i][j].u_pixelRowIdNFoV;
                        result[i][j][7] = FramesData[i][j].u_pixelColIdNFoV;
                    }
                }
            }
        }
        else
        {
            errorCode = -1;
        }
        
        outputs[0] =std::move(result);
        outputs[1] =factory.createScalar(errorCode);
    }
};