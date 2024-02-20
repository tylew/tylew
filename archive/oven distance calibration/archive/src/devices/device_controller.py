import time
import clr
import queue
import threading

# Add references to the necessary DLL files
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll")

# Import required modules and classes
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import *
from System import Decimal

from devices.HDR50Controller import *


class device_controller:

    def __init__(self,) -> None:
        self.motor_controller = self.init_motor_controller()

    def init_motor_controller(self):
        device_list = []

        DeviceManagerCLI.BuildDeviceList()
        device_list = DeviceManagerCLI.GetDeviceList()

        if len(list(device_list)) == 0:
            raise Exception("No ThorLab devices found!")
        
        print(list(device_list))
        return HDR50Controller(device_list[0])
    

# def process_queue(q, controller):
#     while True:
#         try:
#             command_tuple = q.get(timeout=0.1)

#             if command_tuple[0] == "move_motor_relative":
#                 controller.motor_controller.move_relative(float(command_tuple[1]))
#             else:
#                 print('Invalid queue command issued.')
#         except queue.Empty:
#             continue
#         except Exception as e:
#             print('Encountered exception in queue processing thread:', e)
#             time.sleep(0.1)

# def device_controller_target(queue):
    
#     controller = device_controller()

#     # Start queue montoring
#     queue_thread = threading.Thread(target=process_queue, args=(queue, controller))
#     queue_thread.daemon = True  # Daemonize thread
#     queue_thread.start()

'''


def gui_target(queue, terminate, lock):
    app = SimpleApp(terminate, lock)
    
    # Start the queue processing thread
    queue_thread = threading.Thread(target=process_queue, args=(queue, app))
    queue_thread.daemon = True  # Daemonize thread
    queue_thread.start()

    app.mainloop()

'''


# device_controller_target()
