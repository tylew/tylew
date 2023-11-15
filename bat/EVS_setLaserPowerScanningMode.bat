@echo off

@REM Define power variable
set power=%~1
@REM Ensure parameter not empty
IF "%power%"=="" (
    echo Error: Parameter [laser power] is missing.
    echo Usage: %0 [laser power]
    exit /b 1
)
@REM Check valid power value
SET /a "laser_power=%power%"
IF %laser_power% LSS 0 (
    echo Error: [laser power] must be greater than or equal to 0.
    exit /b 1
)
IF %laser_power% GTR 25 (
    echo Error: [laser power] must be less than or equal to 25.
    exit /b 1
)

@REM Laser latch watchdog mechanism
exe\HrlControlCLI.exe setGpio 192.168.1.12 0x3e 0x1 0x1
Timeout 1
@REM Laser enable
exe\HrlControlCLI.exe setGpio 192.168.1.12 0x3f 0x1 0x1
Timeout 1

@REM set laser power
exe\HrlControlCLI.exe setLaserPowerScanningMode 192.168.1.12 %laser_power%
Timeout 2

exe\HrlControlCLI.exe readLaserModuleRegister 192.168.1.12 0x39
@REM 0xc3 -> laser is in ok state (pup enabled, laser anabled, gpio set)

echo Laser set.