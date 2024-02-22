'''
Yu-Suan 2023 Conti Intern
'''

import subprocess
import time
from subprocess import TimeoutExpired
# import matlab.engine
# import scipy.io
# import numpy as np
# EVS version: 2.1.5

# Specify the path to the executable file
EXECUTABLE_PATH = r"../../exe/HrlControlCLI.exe"
INTERFACE_NAME = '192.168.1.12'  # Provide the interface name


def execute_hrl_interface(timeout, command, args=[]):

    print("=======================================================================")
    print(f'==[command]====>> {command} ')

    if len(args) > 0:
        print(f'==[arguments]==>> {args} ')

    try:
        if not EXECUTABLE_PATH or not args:
            raise ValueError("Missing executable path or command arguments.")

        process = subprocess.Popen(
            [EXECUTABLE_PATH] + [command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = process.communicate(timeout=timeout)

        process.kill()

        print(outs.decode())

        time.sleep(3)
        

    except TimeoutExpired:
        print("    Time Out. Failed to execute command.")

        process.terminate()
        time.sleep(3)

    except ValueError as ve:
        print("    Error:", str(ve))


def readEvsR5Version():
    # Function Description:
    #   Read the EVS version installed in the sensor
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer
    # Outputs:
    #   EVS R5 Version: []
    #   Major version : []
    #   Minor version : []
    #   Patch level   : []
    #   Current week  : []
    #   Current year  : []

    command = 'readEvsR5Version'
    command_args = [INTERFACE_NAME]

    execute_hrl_interface(10, command, command_args)


def generateExtendedShotlistRTool(startIndexCol, startIndexRow, windowStepCol, windowStepRow):
    # Function Description :
    #   Generate an extended shotlist and loads it in another memory area for firmware in both highspeed & lowspeed mode
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer
    # Outputs:
    #   print "Extended shotlist for RTOOL High Speed mode generated successfully"
    # Notes:
    #   Command has been simplified to set same window for both narrow and wide simultanously

    command_args = [INTERFACE_NAME, startIndexCol, startIndexRow, windowStepCol,
                    windowStepRow, startIndexCol, startIndexRow, windowStepCol, windowStepRow]

    command = 'generateExtendedShotlistRToolLs'
    execute_hrl_interface(10, command, command_args)

    command = 'generateExtendedShotlistRToolHs'
    execute_hrl_interface(10, command, command_args)


def switchShotlist(shotlist):
    # Function Description:
    #   Switch shotlist type between dummy, narrow, wide and Conti Aeye logo. Shotlist type: 00 =dummy, 01 = narrow, 02 = wide, 03 = conti aeye logo
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, shotlist: string
    # Outputs:
    #   print "Shotlist changed successfully"

    command = 'switchShotlist'
    command_args = [INTERFACE_NAME, shotlist]

    execute_hrl_interface(10, command, command_args)


def checkOperationMode():
    # Function Description:
    #   Check operation mode
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer
    # Outputs:
    #   print "Operation mode: Shotlist: Operation mode checked successfully"
    # Notes:
    #   Operation mode:
    #       1 = static
    #       2 = scanning
    #   Shotlist used:
    #       00 = dummy
    #       01 = narrow
    #       02 = wide
    #       03 = conti aeye logo
    #       04 = e_pixelSwitchingNoise(fastLUT246)
    #       05 = e_rxNoiseThreshold(uniform)
    #       06 = e_advancedRxWfov(ARx48)
    #       07 = e_advancedRxNfov(ARx49)

    command = 'checkOperationMode'
    command_args = [INTERFACE_NAME]

    execute_hrl_interface(10, command, command_args)


def disable_mirrors():
    # Function Description:
    #   Disable the mirrors
    # Inputs:
    #   INTERFACE_NAME: string, timeoutMirrorValue: integer
    # Outputs:
    #   print "Command in progress. Please wait... Mirror state set to 0x0"

    command = 'enableMirrors'
    state = '00'
    command_args = [INTERFACE_NAME, state]

    execute_hrl_interface(20, command, command_args)


def enable_mirrors():
    # Function Description:
    #   Enable the mirrors
    # Inputs:
    #   INTERFACE_NAME: string, timeoutMirrorValue: integer
    # Outputs:
    #   print "Command in progress. Please wait... Mirror state set to 0x1"

    command = 'enableMirrors'
    state = '01'
    command_args = [INTERFACE_NAME, state]

    execute_hrl_interface(20, command, command_args)


def setYMirrorAmplitude(amplitudeYmirror):
    # Function Description:
    #   Set the amplitude of the Y mirror. Max value: 255
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, amplitudeYmirror: string
    # Outputs:
    #   print "Y mirror amplitude set to value 0x"

    command = 'setYMirrorAmplitude'
    command_args = [INTERFACE_NAME, amplitudeYmirror]

    execute_hrl_interface(10, command, command_args)


def getYMirrorAmplitude():
    # Function Description:
    #   Read the amplitude of the Y mirror
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer
    # Outputs:
    #   print "Y mirror amplitude "

    command = 'getYMirrorAmplitude'
    command_args = [INTERFACE_NAME]

    execute_hrl_interface(10, command, command_args)


def setThreshold(threshold, gainChannel):
    # Function Description:
    #   Set the threshold
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, threshold: string, gainChannel: string
    # Outputs:
    #   print "Threshold set successfully"
    # Notes:
    #   threshold - Threshold value
    #   gainChannel - LG_NF, HG_NF, LG_FF, HG_FF

    command = 'setThreshold'
    command_args = [INTERFACE_NAME, threshold, gainChannel]

    execute_hrl_interface(10, command, command_args)


def setLaserPowerScanningMode(desiredLaserPower):
    # Function Description:
    #   Set the power of the laser  if  this is in scanning mode using command 0x50, not 0x59 like setLaserPower().
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, desiredLaserPower: string
    # Outputs:
    #   print "DAC value:  [] Laser pump enabled with []% power"

    command = 'setLaserPowerScanningMode'
    command_args = [INTERFACE_NAME, desiredLaserPower]

    execute_hrl_interface(10, command, command_args)


def enableGainMode(gainSelect):
    # Function Description:
    #   Enable peak detect control(address 0xA0)
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, lowGain: string, highGain: string
    # Outputs:
    #   print "Gain mode enabled successfully"
    # Notes:
    #   Input parameters:
    #       lowGain - Writing a '1' here will turn off peak detection in the high gain channel for the 1st 50 meters
    #       highGain - Writing a '1' here will turn off peak detection in the low gain channel for the 1st 50 meters

    command = 'enableGainMode'

    if (gainSelect == '0'):
        lowGain = '1'
        highGain = '0'
    else:
        lowGain = '0'
        highGain = '1'

    command_args = [INTERFACE_NAME, lowGain, highGain]

    execute_hrl_interface(10, command, command_args)


def writeAxiRegister(axiRegisterAddress, axiRegisterValue):
    # Function Description:
    #   Write an AXI register
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, axiRegisterAddress: string, axiRegisterValue: string
    # Outputs:
    #   print "Value of register 0x[] was written successfully. Value of register 0x[] at memory location 0x[] was written successfully"
    # Note:
    #   axiRegisterValue: WFOV: 211; NFOV: 217

    command = 'writeAxiRegister'
    command_args = [INTERFACE_NAME,
                    axiRegisterAddress, axiRegisterValue]

    # axiRegisterAddress = int(axiRegisterAddress, 16)
    # axiRegisterValue = int(axiRegisterValue, 16)

    execute_hrl_interface(10, command, command_args)


def readAxiRegister(axiRegisterAddress):

    # Function Description:
    #   Read an AXI register
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, axiRegisterAddress: string
    # Outputs:
    #   print "Value of register 0x[] is: 0x[]"

    command = 'readAxiRegister'
    command_args = [INTERFACE_NAME, axiRegisterAddress]

    execute_hrl_interface(10, command, command_args)


def setGpio(gpioPort, outEnSelect, expectedGpioValue):

    # Function Description:
    #   Write a GPIO value
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, gpioPort: string, outEnSelect: string, expectedGpioValue: string
    # Outputs:
    #   print "GPIO port 0x[] was successfully written to 0x[]"

    command = 'setGpio'
    command_args = [INTERFACE_NAME,
                    gpioPort, outEnSelect, expectedGpioValue]

    execute_hrl_interface(10, command, command_args)


def getGpio(gpioPort, expectedGpioValue):

    # Function Description:
    #   Read a GPIO value
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, gpioPort: string, expectedGpioValue: string
    # Outputs:
    #   print "GPIO port 0x[] value: 0x[]"

    command = 'getGpio'
    command_args = [INTERFACE_NAME, gpioPort]

    execute_hrl_interface(10, command, command_args)


def getFrames(fileName, noOfFrames='1'):

    # Function Description:
    #   Retrieves data from LUT and save them in a *.bin file.
    # Inputs:
    #   INTERFACE_NAME: string, timeoutValue: integer, noOfFrames: string, fileName: string
    # Outputs:
    #   print "Capturing data started. LUT Data received successfully"
    # Notes:
    #   The function is sending a request with the number of requested frames and reads
    #   the packets( data is send in packets of 1450 bytes) and writes them is a bin file data.

    command = 'getFrames'
    command_args = [INTERFACE_NAME, noOfFrames, fileName]

    execute_hrl_interface(10, command, command_args)


def setUpDevice(
        fov, # 'narrow'/'wide'
        gain, # 'low'/'high'
        speed, # 'low'/'high'
        laserPower = '10'
):
    
    valid_fovs = ['narrow', 'wide']
    valid_gains = ['low', 'high']
    valid_speeds = ['low', 'high']
    
    if fov not in valid_fovs:
        raise ValueError(f"Invalid fov value. Allowed values: {', '.join(valid_fovs)}")
    
    if gain not in valid_gains:
        raise ValueError(f"Invalid gain value. Allowed values: {', '.join(valid_gains)}")
    
    if speed not in valid_speeds:
        raise ValueError(f"Invalid speed value. Allowed values: {', '.join(valid_speeds)}")

    
    axiRegisterAddressEyeSafety = '0xA00022B0'
    axiRegisterAddressFOV = '0xA0004100'
    gpioPort = "0x3e"

    axiRegisterValueEyeSafety = '0x00000000'
    axiRegisterValueFOV = lambda fov: (
        '0x00000211' if fov == 'wide'
        else '0x00000217' if fov == 'narrow'
        else None
    ) 

    
    outEnSelect = '0x01'
    expectedGpioValue = '0x01'

    
    
    windowStartIndexCol = '0'
    windowStartIndexRow = '0'
    windowStepCol = '165'
    windowStepRow = '85'

    amplitudeYmirror = '0'

    channel_thresholds = [
        ('LG_FF', '5650'),
        ('LG_NF', '5750'), 
        ('HG_FF', '5700'), 
        ('HG_NF', '5850')
    ]

    # Set shotlist based on speed setting
    # 00 = dummy
    # 01 = narrow
    # 02 = wide
    # 03 = conti aeye logo
    shotlist = (
        lambda speed: 
        '01' if speed == 'high' 
        else '02' if speed == 'low'
        else None
    ) (speed)


    gainSelect = lambda gain: (
        '0' if gain == 'low'
        else '1' if gain == 'high'
        else None
    ) (gain)

    # gainChannel = lambda fov, gain: (
    #     'LG_NF' if fov == 'narrow' and gain == 'low'
    #     else 'LG_FF' if fov == 'wide' and gain == 'low'
    #     else 'HG_NF' if fov == 'narrow' and gain == 'high'
    #     else 'HG_FF' if fov == 'wide' and gain == 'high'
    #     else None
    # ) (fov, gain)


    # readEvsR5Version()

    # Step 1: Create LUT with the start index and specific windows

    generateExtendedShotlistRTool(
        windowStartIndexCol, windowStartIndexRow, windowStepCol, windowStepRow)
    
    switchShotlist(shotlist)
    # checkOperationMode()


    # Step 2: Mirror settings

    setYMirrorAmplitude(amplitudeYmirror)
    # getYMirrorAmplitude()

    setLaserPowerScanningMode(laserPower)

    disable_mirrors()
    # enable_mirrors()

    setLaserPowerScanningMode(laserPower)

    disable_mirrors()


    # Step 3: PPAR camera specific

    for channel, threshold in channel_thresholds:
        setThreshold(threshold, channel)


    # Step 4: Set the Mux Register and turn off Eye Safety

    writeAxiRegister(axiRegisterAddressFOV, axiRegisterValueFOV(fov))
    readAxiRegister(axiRegisterAddressFOV)

    writeAxiRegister(axiRegisterAddressEyeSafety, axiRegisterValueEyeSafety)
    # readAxiRegister(axiRegisterAddressEyeSafety)

    # Step 5: Set the Shot Processing Low Gain/High Gain Channel

    enableGainMode(gainSelect)

    # Step 6: Write WDI Latch to 1 (turn on laser)

    setGpio(gpioPort, outEnSelect, expectedGpioValue)
    # getGpio(gpioPort, expectedGpioValue)

import ReadBinFile 
import threading

def display_live_frames(filename = 'lutTest.bin'):
    while True:
        getFrames(filename)
        # time.sleep(1)

        ReadBinFile.displayBin(filename, live = True)

def main():

    fileName = f'../test/lutTest2.bin'

    fov = 'narrow' # 'narrow'/'wide'
    gain = 'low' # 'low'/'high'
    speed = 'low' # 'low'/'high'
    laser_power = '10'

    # setUpDevice(fov, gain, speed, laser_power)
    display_live_frames()
    # plot_thread = threading.Thread(target = display_live_frames)
    # # while True:
    # plot_thread.start()
    #     getFrames(fileName)
    #     # time.sleep(1)

    #     ReadBinFile.displayBin(fileName, live = True)

if __name__ == "__main__":
    main()
