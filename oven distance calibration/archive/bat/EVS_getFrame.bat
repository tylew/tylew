@echo off
set "HRLControlExe=exe\HrlControlCLI_1_0_9.exe"

@REM Define variables
set directory_path=%~1
set gain=%~2

IF "%directory_path%"=="" (
    echo Error: Parameter [directory path] is missing.
    echo Usage: %0 [directory path] [gain] 
    exit /b 1
)

IF "%gain%"=="" (
    echo Warn: Parameter [gain] is missing, using HIGH gain.
    echo Usage: %0 [directory path] [gain] 
    set gain=high
)

REM Check valid values and perform EVS set for [gain] parameter
SET "shotlist_value="
IF /i "%gain%"=="low" (
    echo Collecting LOW gain channel
    %HRLControlExe% enableGainMode 192.168.1.12 1 0
) ELSE IF /i "%gain%"=="high" (
    echo Collecting HIGH gain channel
    %HRLControlExe% enableGainMode 192.168.1.12 0 1
) ELSE (
    echo Error: Invalid value for [gain]. Allowed values: low or high. 
    pause
    exit /b 1
)
Timeout 2

%HRLControlExe% getFrames 192.168.1.12 1 %directory_path% 0