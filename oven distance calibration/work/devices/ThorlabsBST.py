'''
Thorlabs Benchstop Stepper Motor implementation
@uig05389 Lewis, T

November 2023
'''

from devices.ThorlabsKinesisMotor import *

class ThorlabsBST(ThorlabsKinesisMotor):
    '''
    Implementation of abstract class ThorlabsKinesisMotor

    inherits the following variables: 
        is_connected -> bool, 
        serial -> str[int], 
        channel -> clr(BenchtopStepperMotorChannel)

    and following functions:
        isHomed()
        getPosition()
        home()
        moveRelative()
        closeChannel()

    need to implement:
        initChannel(self)
    '''
    def __init__(self) -> None:
        super().__init__()

    def initChannel(self):
        # Create and connect to the stepper motor device
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial)
        self.device.Connect(self.serial)
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

    

    
