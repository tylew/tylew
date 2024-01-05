@echo off
setlocal enabledelayedexpansion enableextensions
set "extension=.bin"
set "baseName=testRtool_"
set "HRLControlExe=exe\HrlControlCLI_1_0_9.exe"
@ECHO generating ls shotlist
%HRLControlExe% generateExtendedShotlistRToolLs 192.168.1.12 0 0 165 85 0 0 165 85
Timeout 3
@ECHO setting low-speed shotlist // change this value to 1 for hs
%HRLControlExe% switchShotlist 192.168.1.12 2
Timeout 3
@echo Set mirror static
%HRLControlExe% setYMirrorAmplitude 192.168.1.12 0
%HRLControlExe% enableMirrors 192.168.1.12 00

@echo PPAR camera specific
%HRLControlExe% setThreshold 192.168.1.12 6000 LG_FF
%HRLControlExe% setThreshold 192.168.1.12 6000 LG_NF
%HRLControlExe% setThreshold 192.168.1.12 6000 HG_FF
%HRLControlExe% setThreshold 192.168.1.12 6000 HG_NF
%HRLControlExe% setLaserPowerScanningMode 192.168.1.12 20
%HRLControlExe% writeAxiRegister 192.168.1.12 A0004048 063C1E01
Timeout 3
@ECHO Write WDI to 1 to turn on the laser
%HRLControlExe% setGpio 192.168.1.12 0x3e 0x1 0x1

FOR /L %%K IN (1,1,50) DO (
    FOR /L %%J IN (1,1,4) DO (
        @echo setting the Rx channel
        %HRLControlExe% setGainChannel 192.168.1.12 %%J
        %HRLControlExe% getFrames 192.168.1.12 1 %baseName%%%K_%%J_1%extension%
        Timeout 1
        %HRLControlExe% getFrames 192.168.1.12 1 %baseName%%%K_%%J_2%extension%
        Timeout 1
    )
)
