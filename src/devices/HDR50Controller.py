import time
import clr

# from connection.ThorLabsDeviceManager import DeviceManager
 
# Add references to the necessary DLL files
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")

# Import required modules and classes
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal

class HDR50Controller:
    def __init__(self, serial_no: str):
        self.serial_no = serial_no
        self.device = None
        self.channel = None
 
        self.connect()
        device_info = self.channel.GetDeviceInfo()
        print(f"Connected to motor channel via {device_info.Description}")
        print(f"Device serial: {device_info.SerialNumber}")
        print(f"Device name: {device_info.Name}")
        self.initialize_channel_settings()
 
    def connect(self):
        # Create and connect to the stepper motor device
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_no)
        self.device.Connect(self.serial_no)
        time.sleep(0.25)
 
        # Get the motor channel
        self.channel = self.device.GetChannel(1)
 
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
 
    def initialize_channel_settings(self):
        print('Initializing settings...')
        
        # Load motor configuration and update device settings
        channel_config = self.channel.LoadMotorConfiguration(self.serial_no)
        chan_settings = self.channel.MotorDeviceSettings
        self.channel.GetSettings(chan_settings)

        # Set the device settings name and update the configuration
        channel_config.DeviceSettingsName = 'HDR50'
        channel_config.UpdateCurrentConfiguration()

        # Apply the settings to the channel
        self.channel.SetSettings(chan_settings, True, False)
        print('Done initializing')
 
    def disconnect(self):
        print("Disconnecting Stepper Motor")
        self.channel.StopPolling()
        self.device.Disconnect()

    def is_homed(self) -> bool:
        homed = self.channel.Status.IsHomed()
        if homed:
            print("Motor is homed.")
        else:
            print("Motor is not homed.")
        return homed
    
    def get_position(self) -> float:
        curr_position = self.channel.Position
        return curr_position
 
    def home_motor(self):
        print(f"Homing Motor from position {self.get_position()}")
        self.channel.Home(60000)
        print(f"Done - Current position: {self.get_position()}")
 
    def move_relative(self, stepsize: float):
        print(f"Moving relative {stepsize} units")
        self.channel.MoveRelative(MotorDirection.Forward, Decimal(stepsize), 10000)
        print(f"Done - Current position: {self.get_position()}")
 
    def move_to(self, location: float):
        print(f"Moving to {location}")
        self.channel.MoveTo(Decimal(float(location)), 60000)
        print(f"Done - Current position: {self.get_position()}")
 
    
    

if __name__ == "__main__":
    # ThorLabDeviceManager = DeviceManager()
    # device_list = ThorLabDeviceManager.get_device_list()
    DeviceManagerCLI.BuildDeviceList()
    device_list = DeviceManagerCLI.GetDeviceList()
    print(list(device_list))
    motorcontroller = HDR50Controller(serial_no=device_list[0])

    print(motorcontroller.get_position())
    motorcontroller.move_relative(20)
    motorcontroller.move_relative(20)
    # for i in range(200):
    #     motorcontroller.move_relative(.1)
    # motorcontroller.move_relative(10)
    # motorcontroller.move_relative(-20)
    homed = motorcontroller.is_homed()
    if not homed:
        motorcontroller.home_motor()
    
    # motorcontroller.move_relative(-10)

    