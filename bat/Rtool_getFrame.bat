@echo off

@REM pushd "%~dp0.." REM set executing directory to master dir

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
    exe\HrlControlCLI.exe enableGainMode 192.168.1.12 1 0
) ELSE IF /i "%gain%"=="high" (
    echo Collecting HIGH gain channel
    exe\HrlControlCLI.exe enableGainMode 192.168.1.12 0 1
) ELSE (
    echo Error: Invalid value for [gain]. Allowed values: low or high. 
    pause
    exit /b 1
)
Timeout 2

exe\HrlControlCLI.exe getFrames 192.168.1.12 1 %directory_path% 0