# import clr
import time

# Add references to the necessary DLL files
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")

# Import required modules and classes
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal


class ThorlabMotor:

    def __init__(self, serial) -> None:
        self.isConnected = False
        self.serial = serial  
        self.channel = None
        self.device = None

        self.initChannel()
        self.setChannelSettings()

        if not self.isHomed():
            self.home()

    def initChannel(self):
        # Create and connect to the stepper motor device
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial)
        self.device.Connect(self.serial_no)
        time.sleep(0.25)

        # Get the motor channel
        self.channel = self.device.GetChannel(1)

        self.setChannelSettings()

        # Wait for the channel settings to be initialized
        if not self.channel.IsSettingsInitialized():
            self.channel.WaitForSettingsInitialized(10000)
            print("Channel settings not initialized")
            assert self.channel.IsSettingsInitialized() is True
 
        # Start polling and enable the device
        self.channel.StartPolling(250)
        time.sleep(0.25)
        self.channel.EnableDevice()
        time.sleep(0.25)

        self.isConnected = True

    def setChannelSettings(self):
        # Load motor configuration and update device settings
        channel_config = self.channel.LoadMotorConfiguration(self.serial)
        chan_settings = self.channel.MotorDeviceSettings
        self.channel.GetSettings(chan_settings)

        # Set the device settings name and update the configuration
        channel_config.DeviceSettingsName = 'HDR50'
        channel_config.UpdateCurrentConfiguration()

        # Apply the settings to the channel
        self.channel.SetSettings(chan_settings, True, False)
    
    def closeChannel(self):
        print("Disconnecting Stepper Motor")
        self.channel.StopPolling()
        self.device.Disconnect()

        self.isConnected = False

    def isHomed(self) -> bool:
        return self.channel.Status.IsHomed()

    def getPosition(self) -> float:
        return self.channel.Position

    def home(self):
        print(f"Homing Motor from position ~{self.get_position()}")
        self.channel.Home(60000)
        print(f"Done - Current position: {self.get_position()}")
 
    def movRelative(self, stepsize: float):
        print(f"Moving relative {stepsize} units")
        self.channel.MoveRelative(MotorDirection.Forward, Decimal(stepsize), 10000)
        print(f"Done - Current position: {self.getPosition()}")
 
    def moveTo(self, location: float):
        print(f"Moving to {location}")
        self.channel.MoveTo(Decimal(float(location)), 60000)
        print(f"Done - Current position: {self.getPosition()}")