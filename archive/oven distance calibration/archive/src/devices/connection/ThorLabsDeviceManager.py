import clr
 
# Add references to the necessary DLL files
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *

class DeviceManager:
    def __init__(self):
        self.device_list = None
 
    def build_device_list(self):
        DeviceManagerCLI.BuildDeviceList()
        self.device_list = DeviceManagerCLI.GetDeviceList()
        if not self.device_list or self.device_list:
            raise Exception("No devices found.")
         
    def build_device_list_using_prefix(self, devicePrefix):
        DeviceManagerCLI.BuildDeviceList()
        self.device_list = DeviceManagerCLI.GetDeviceList(devicePrefix)
        if not self.device_list:
            raise Exception(f"No devices found with prefix {devicePrefix}.")
   
    def get_device_list(self):
        if not self.device_list:
            self.build_device_list()
        return list(self.device_list)