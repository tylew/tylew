'''
File: TestbedVisualizer.py
Author: uig05389
Description: 
    Provide foundation for testbed automation in regard to the oven distance calibration project.
    This program assumes a pre-initialization of the LiDAR sensor: `bat/Rtool_init.bat` 

    Running this file will loop the taking and displaying of HRL 'frames'
'''
import subprocess
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import csv

from evs import ReadBinFile
from devices.device_controller import *


desired_col = 88
csv_filename = "seek_pix_calibration.csv"
field_names = ["d_idx", "d_idy", "i_idx", "i_idy", "dist_value", "intensity_value"]
# Default EVS data save location
data_dir = 'data\simtest.bin'
# Get the directory of the Python script (current directory)
script_directory = os.path.dirname(os.path.abspath(__file__))
# Define the path to the batch file relative to the Python script
rtool_getFrame_bat = os.path.join(script_directory, '..', 'bat', 'Rtool_getFrame.bat')
rtool_setup_bat = os.path.join(script_directory, '..', 'bat', 'Rtool_setup.bat')

def seekPixelF(x: int) -> float:
    '''
    Linear formula to locate motor position from desired pixel
    Derived from the equation visualized in `\docs\function.jpg`
    (formula may need to be calibrated if test bed is modified in any way by assembling the same function)
    '''
    F = lambda x: (float(x) - 154.3) / -1.64
    r = F(x)
    return r

def prettyPrint(string: str) -> None:
    '''
    Helper function to pretty-print for console
    '''
    print('='*3, string, '='*3)

def writeCsv(csv_filename: str, data: dict) -> None:
    '''
    Helper function to write csv file
    '''
    # Check if the CSV file exists
    file_exists = os.path.exists(csv_filename)

    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # If the file doesn't exist, write the headers
        if not file_exists:
            writer.writeheader()

        # Write data for the current iteration
        writer.writerow(data)


# controller = device_controller()
# controller.motor_controller.home_motor()
# controller.motor_controller.move_to(50)


# Call EVS setup subprocess
# subprocess.call([rtool_setup_bat, 'low', 'wide', '22'])


# Create blank Rx data arrays
blank_data2d = np.zeros((86, 166))
fig, im, surf = ReadBinFile.create_fig_data2d(blank_data2d, blank_data2d)
# Show plot
plt.show(block=False)


prettyPrint("Starting pixel-seeking loop")
stay_looping = True

while stay_looping:

    # And EVS getFrame...
    while True:
        try:
            subprocess.run([rtool_getFrame_bat, data_dir], timeout=10)
            break  # Break the loop if successful
        except subprocess.TimeoutExpired:
            prettyPrint("EVS timed out (getFrame) Retrying...")
            time.sleep(1)  # sleep before retrying

    # Convert .bin to 2d data
    rx_data_objects, data2d_intensity, data2d_distance = ReadBinFile.get_data2d(data_dir)
    # Update figure
    ReadBinFile.update_plot(im, surf, data2d_intensity, data2d_distance)
    # Store highest intensity & distance containing pixels
    d_max_index_2d, d_max_value, i_max_index_2d, i_max_value = ReadBinFile.get_illuminated_pixel(data2d_distance,data2d_intensity)

    # Uncomment to end loop
    # if (d_max_index_2d[1] == desired_col):
    #     print("Located Pixel")
    #     stay_looping = False
    #     break
    

    prettyPrint(f'Difference between desired pix [{desired_col}]: {desired_col - d_max_index_2d[1]}')

    # writeCsv('calibration.txt', 
    #     {
    #     'd_idx': d_max_index_2d[0], 
    #     'd_idy': d_max_index_2d[1], 
    #     'i_idx': i_max_index_2d[0], 
    #     'i_idy': i_max_index_2d[1], 
    #     'dist_value': d_max_value, 
    #     'intensity_value': i_max_value
    #     }
    # )
    
    
    while True:
        user_input = input("Input pixel location(int): ")
        try:
            _pixel = int(user_input)
            motor_location = seekPixelF(_pixel)


            print(f'seeking pixel {_pixel} at motor location {motor_location}')
            # controller.motor_controller.move_to(motor_location)
            break
        except ValueError:
            print("That's not a float. Try again.")


