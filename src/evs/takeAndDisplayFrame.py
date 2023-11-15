from ReadBinFile import *
import os
import subprocess
import time

# Get the directory of the Python script (current directory)
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the batch file relative to the Python script
rtool_getFrame_bat = os.path.join(script_directory, '..', '..', 'bat', 'Rtool_getFrame.bat')
# rtool_setup_bat = os.path.join(script_directory, '..', '..', 'bat', 'Rtool_setup.bat')

# Define EVS data save location
data_dir = 'data\simtest_good1.bin'


# And EVS getFrame...
while True:
    try:
        subprocess.run([rtool_getFrame_bat, data_dir, 'high'], timeout=10)
        break  # Break the loop if successful
    except subprocess.TimeoutExpired:
        print("Timed out. Retrying in 2s...")
        time.sleep(2)  # sleep before retrying

# Convert .bin to 2d data using import ReadBinFile.py
rx_data_objects, data2d_intensity, data2d_distance = get_data2d(data_dir)

d_max_index_2d, d_max_value, i_max_index_2d, i_max_value = get_illuminated_pixel(data2d_distance,data2d_intensity)

# Generate figure
fig, im, surf = create_fig_data2d(data2d_intensity, data2d_distance)

plt.show(block=True)


