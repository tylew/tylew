'''
Thorlabs Kinesis implementation
@uig05389 Lewis, T

November 2023
'''

import time
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

from abc import ABC, abstractmethod

class ThorlabsKinesisMotor(ABC):
    def __init__(self):
        self.is_connected = False
        self.serial = self.findSerial()[0]
        self.channel = None
        self.device = None

    @abstractmethod
    def initChannel(self):
        raise NotImplementedError("Subclasses must implement the 'initChannel' method.")

    def findSerial(self) -> list[str]:
        device_list = []

        DeviceManagerCLI.BuildDeviceList()
        device_list = list(DeviceManagerCLI.GetDeviceList())

        if len(device_list) == 0:
            raise Exception("No ThorLab devices found!")

        print(device_list)
        return device_list

    def isHomed(self) -> bool:
        return self.channel.Status.IsHomed()

    def getPosition(self) -> float:
        return self.channel.Position
    
    def home(self):
        print(f"Homing Motor from position ~{self.getPosition()}")
        self.channel.Home(60000)
        print(f"Done - Current position: {self.getPosition()}")

    def moveRelative(self, stepsize: float):
        print(f"Moving relative {stepsize} units")
        self.channel.MoveRelative(MotorDirection.Forward, Decimal(stepsize), 10000)
        print(f"Done - Current position: {self.getPosition()}")

    def moveTo(self, location: float):
        print(f"Moving to {location}")
        self.channel.MoveTo(Decimal(float(location)), 60000)
        print(f"Done - Current position: {self.getPosition()}")
    
    def closeChannel(self):
        print("Disconnecting Stepper Motor")
        self.channel.StopPolling()
        self.device.Disconnect()

        self.isConnected = False