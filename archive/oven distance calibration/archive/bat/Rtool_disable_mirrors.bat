@echo off
set HRLControlExe=exe\HrlControlCLI_1_0_9.exe

@REM Disable eye safe
%HRLControlExe% writeAxiRegister 192.168.1.12 0xA00022B0 0

Rem disable mirrors
@echo Disable X mirror
%HRLControlExe% enableMirrors 192.168.1.12 00
Timeout 3
@echo Disable Y mirror
%HRLControlExe% setYMirrorAmplitude 192.168.1.12 0
Timeout 1

echo Mirrors disabled.
