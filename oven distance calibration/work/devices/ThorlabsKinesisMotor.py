'''
Thorlabs Kinesis implementation
@uig05389 Lewis, T

November 2023

Download .NET packages @ 
https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
'''

import time
from devices.ThorlabsManager import *

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