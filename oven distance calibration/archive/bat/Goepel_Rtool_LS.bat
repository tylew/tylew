@echo off
SET LimitByte=3.274.800

setlocal enabledelayedexpansion enableextensions
set "extension=.bin"
set "baseName=testRtool_"

set "n=%%K"	
exe\HrlControlCLI.exe generateExtendedShotlistRToolLs 192.168.1.12 0 0 165 85 0 0 165 85
Timeout 3
exe\HrlControlCLI.exe switchShotlist 192.168.1.12 2
Timeout 3
@echo Set mirror static
exe\HrlControlCLI.exe setYMirrorAmplitude 192.168.1.12 0
exe\HrlControlCLI.exe enableMirrors 192.168.1.12 00

@echo PPAR camera specific
exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 LG_FF 
exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 LG_NF 
exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 HG_FF 
exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 HG_NF 
exe\HrlControlCLI.exe setLaserPowerScanningMode 192.168.1.12 20
exe\HrlControlCLI.exe writeAxiRegister 192.168.1.12 A0004048 063C1E01
Timeout 3
@ECHO Write WDI to 1 to turn on the laser 
exe\HrlControlCLI.exe setGpio 192.168.1.12 0x3e 0x1 0x1

FOR /L %%K IN (1,1,50) DO (	
	

	FOR /L %%J IN (1,1,4) DO (
		set "m=%%J"	
		@echo setting the Rx channel
		exe\HrlControlCLI.exe setGainChannel 192.168.1.12 m
		exe\HrlControlCLI.exe getFrames 192.168.1.12 1 %baseName%!n:~-2!_!m:~-2!_1%extension%
		Timeout 1
		exe\HrlControlCLI.exe getFrames 192.168.1.12 1 %baseName%!n:~-2!_!m:~-2!_2%extension%
		Timeout 1

	)
)

