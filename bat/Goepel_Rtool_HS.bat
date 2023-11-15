@echo off
@echo off
set LOGFILE=Rtool.log

echo Logging session started on %date% at %time% > %LOGFILE%

set "extension=.bin"
set "baseName=bat\output\testRtool_"

echo Logging
FOR /L %%K IN (1,1,10) DO (	
	
    echo Running iteration %%K >> %LOGFILE% 2>>&1

	set "n=%%K"	
	exe\HrlControlCLI.exe generateExtendedShotlistRToolHs 192.168.1.12 0 0 165 85 0 0 165 85 >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1
	Timeout 10
	exe\HrlControlCLI.exe switchShotlist 192.168.1.12 1 >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1
	Timeout 3
	@echo Set mirror static >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setYMirrorAmplitude 192.168.1.12 0 >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe enableMirrors 192.168.1.12 00 >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1

	@echo PPAR camera specific >> %LOGFILE% 2>>&1 >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 LG_FF  >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 LG_NF  >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 HG_FF  >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setThreshold 192.168.1.12 6000 HG_NF  >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setLaserPowerScanningMode 192.168.1.12 28 >> %LOGFILE% 2>>&1
	Timeout 3
	@ECHO Write WDI to 1 to turn on the laser >> %LOGFILE% 2>>&1
	exe\HrlControlCLI.exe setGpio 192.168.1.12 0x3e 0x1 0x1 >> %LOGFILE% 2>>&1
	FOR /L %%J IN (1,1,4) DO (
		set "m=%%J"	
		@echo setting the Rx channel >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe setGainChannel 192.168.1.12 m >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0004104 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa000013c >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0000138 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0000104 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe getFrames 192.168.1.12 1 %baseName%!n:~-2!_!m:~-2!_1%extension% >> %LOGFILE% 2>>&1
		Timeout 1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0004104 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa000013c >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0000138 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe readAxiRegister 192.168.1.12 0xa0000104 >> %LOGFILE% 2>>&1
		exe\HrlControlCLI.exe getFrames 192.168.1.12 1 %baseName%!n:~-2!_!m:~-2!_2%extension% >> %LOGFILE% 2>>&1
		Timeout 1
	)
)

