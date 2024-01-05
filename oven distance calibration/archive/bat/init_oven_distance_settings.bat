@echo off

call bat\Rtool_init.bat low wide
Timeout 3
call bat\Rtool_disable_mirrors.bat 
Timeout 3
call bat\EVS_setLaserPowerScanningMode.bat 20
