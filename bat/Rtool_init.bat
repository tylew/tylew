@echo off

@REM Perform setup process
@REM gain set elsewhere prior to getting frame

REM Check if required parameters are provided

set speed=%~1
set fov=%~2

IF "%speed%"=="" (
    echo Error: Parameter [speed] is missing.
    echo Usage: %0 [speed] [fov] 
    exit /b 1
)

IF "%fov%"=="" (
    echo Error: Parameter [fov] is missing.
    echo Usage: %0 [speed] [fov]
    exit /b 1
)



REM Check valid values for [speed] [fov] 

SET "shotlist_value="
IF /i "%speed%"=="low" (
    SET "shotlist_value=02"
) ELSE IF /i "%speed%"=="high" (
    SET "shotlist_value=01"
) ELSE (
    echo Error: Invalid value for [speed]. Allowed values: low or high. 
    pause
    exit /b 1
)

REM Set val based on the value of [fov]
@REM 2-- B0.5, 3-- B1
SET "fov_value="
IF /i "%fov%"=="narrow" (
    SET "fov_value=0x00000317"
) ELSE IF /i "%fov%"=="wide" (
    SET "fov_value=0x00000311"
) ELSE (
    echo Error: Invalid value for [fov]. Allowed values: narrow or wide. 
    pause
    exit /b 1
)


REM Actual script logic using parameters
echo: Initializing device with following parameters:
echo       [speed]: %1
echo         [fov]: %2
echo    [shotlist]: %shotlist_value%


Rem turn off eye safety
@REM exe\HrlControlCLI.exe writeAxiRegister 192.168.1.12 A00022B0 00000000 

rem set limit byte ? idk
SET LimitByte=3.274.800
Rem generate both shotlists, might as well do both
exe\HrlControlCLI.exe generateExtendedShotlistRToolHs 192.168.1.12 0 0 165 85 0 0 165 85
exe\HrlControlCLI.exe generateExtendedShotlistRToolLs 192.168.1.12 0 0 165 85 0 0 165 85

Timeout 3

Rem modify shotlist setting (based on speed)
exe\HrlControlCLI.exe switchShotlist 192.168.1.12 %shotlist_value%
Timeout 3


Rem set gain thresholds, might as well do all
@echo PPAR camera specific
exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 LG_FF
exe\HrlControlCLI.exe setThreshold 192.168.1.12 5750 LG_NF 
exe\HrlControlCLI.exe setThreshold 192.168.1.12 5700 HG_FF 
exe\HrlControlCLI.exe setThreshold 192.168.1.12 5850 HG_NF 
Timeout 1

Rem activate correct FOV: WFOV 311; NFOV 317 (controlled by parameter)
@echo setting the FOV Mux control
exe\HrlControlCLI.exe writeAxiRegister 192.168.1.12 0xA0004100 %fov_value%
Timeout 3

Rem set fiber delay ? idk
exe\HrlControlCLI.exe writeAxiRegister 192.168.1.12 A0004048 06C11E03
Timeout 1

@ECHO EVS initialization complete.
