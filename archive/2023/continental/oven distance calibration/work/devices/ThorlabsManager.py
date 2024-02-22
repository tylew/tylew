'''
Thorlabs Device Management implementation
@uig05389 Lewis, T

November 2023

Download .NET packages @ 
https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
'''

import clr
from decimal import Decimal  # Import Decimal for precise floating-point calculations
# from System import Decimal

# Add references to the necessary DLL files
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")

# Import required modules and classes
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *

class ThorlabsManager:

    def __init__(self) -> None:
        self.device_list = self.findSerials()
        self.device_controllers = []

    def getDeviceList(self) -> list[str]:
        device_list = []

        DeviceManagerCLI.BuildDeviceList()
        device_list = list(DeviceManagerCLI.GetDeviceList())

        if len(device_list) == 0:
            raise Exception("No ThorLab devices found!")

        print(device_list)
        return device_list
    
    # def connectToAll(self):
    #     for serial in self.device_list:
    #         self.device_controllers.append[ThorlabsBST(serial)]
