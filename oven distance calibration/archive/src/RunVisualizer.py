import subprocess
import os
import multiprocessing
from gui.gui_visualizer import *
from devices.device_controller import *

# Get the directory of the Python script (current directory)
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the batch file relative to the Python script
rtool_getFrame_bat = os.path.join(script_directory, '..', 'bat', 'Rtool_getFrame.bat')
rtool_setup_bat = os.path.join(script_directory, '..', 'bat', 'Rtool_setup.bat')



'''
SERIES OF EVENTS

    GUI
        
        Should show:
            visualizer for photo array
            current set oven temp
            current attenuation
            desired illuminated pixel

    Seek pixel
        Create LUT for each fov for pixel and corresponding motor locations 

    Simulation
        Init sensor/devices
        loop:
            Set temp
            Locate pixels, take readings
            store data
'''

# Execute the batch file
# subprocess.call([rtool_setup_bat, 'low', 'wide', '22'])


from multiprocessing import Value, Lock
from evs.ReadBinFile import *


if __name__ == "__main__":
    # Create a global queue for communication between processes
    gui_queue = multiprocessing.Queue()
    device_queue = multiprocessing.Queue()
    # device_queue = multiprocessing.Queue()

    # Use a multiprocessing Value to safely share terminate flag
    terminate = Value('b', False)  # boolean 'b', set to False
    lock = Lock()

    # Start the device controller process
    devices_process = multiprocessing.Process(target=device_controller_target, args=(device_queue,))
    devices_process.start()

    # Start the Tkinter app process
    gui_process = multiprocessing.Process(target=gui_target, args=(gui_queue, device_queue, terminate, lock))
    gui_process.start()

    # Input loop in the parent process
    while not terminate.value:
        data_dir = 'data\simtest.bin'
        # subprocess.call([rtool_getFrame_bat, data_dir])

        time.sleep(.1)

        # fig = get_fig_from_file(data_dir)
        rx_data_objects, data2d_intensity, data2d_distance = get_data2d(data_dir)

        gui_queue.put(('update_graphs', data2d_intensity, data2d_distance))

    # devices_process.terminate()
    # devices_process.join()
    
    # Clean up the Tkinter app process
    gui_process.terminate()
    gui_process.join()
