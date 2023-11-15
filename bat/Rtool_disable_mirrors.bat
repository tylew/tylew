@echo off

@REM Disable eye safe
exe\HrlControlCLI.exe writeAxiRegister 192.168.1.12 0xA00022B0 0

Rem disable mirrors
@echo Disable X mirror
exe\HrlControlCLI.exe enableMirrors 192.168.1.12 00
Timeout 3
@echo Disable Y mirror
exe\HrlControlCLI.exe setYMirrorAmplitude 192.168.1.12 0
Timeout 1

echo Mirrors disabled.


