'''
File: ReadBinFile.py
Author: uig05389
Description: 
    Python script for decoding EVS binary output.
'''

import struct

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

class rxData_returns:
    ''' 
    Format EVS binary output for each attribute based on their bit sizes
    '''
    ## .bin output has 12 byte offset with following structure
    fmt_u_intensity = 'i'  # 32-bit integer (4 bytes)
    fmt_u_distance = 'i'   # 32-bit integer (4 bytes)
    fmt_u_elevation = 'h'  # 16-bit integer (2 bytes)
    fmt_u_azimuth = 'h'    # 16-bit integer (2 bytes)
    fmt_u_pixelRowIdWFoV = 'B'  # 8-bit unsigned integer (1 byte)
    fmt_u_pixelColIdWFoV = 'B'  # 8-bit unsigned integer (1 byte)
    fmt_u_pixelRowIdNFoV = 'B'  # 8-bit unsigned integer (1 byte)
    fmt_u_pixelColIdNFoV = 'B'  # 8-bit unsigned integer (1 byte)

    def __init__(self, buffer):
        self.unpack(buffer)

    def __str__(self):
        return f"u_intensity: {self.u_intensity}, " \
            f"u_distance: {self.u_distance}, " \
            f"u_elevation: {self.u_elevation}, " \
            f"u_azimuth: {self.u_azimuth}, " \
            f"u_pixelRowIdWFoV: {self.u_pixelRowIdWFoV}, " \
            f"u_pixelColIdWFoV: {self.u_pixelColIdWFoV}, " \
            f"u_pixelRowIdNFoV: {self.u_pixelRowIdNFoV}, " \
            f"u_pixelColIdNFoV: {self.u_pixelColIdNFoV}"

    def unpack(self, buffer):
        '''Unpack the binary data using the defined format strings'''
        (self.u_intensity,) = struct.unpack(self.fmt_u_intensity, buffer[:4])
        (self.u_distance,) = struct.unpack(self.fmt_u_distance, buffer[4:8])
        (self.u_elevation,) = struct.unpack(self.fmt_u_elevation, buffer[8:10])
        (self.u_azimuth,) = struct.unpack(self.fmt_u_azimuth, buffer[10:12])
        (self.u_pixelRowIdWFoV,) = struct.unpack(self.fmt_u_pixelRowIdWFoV, buffer[12:13])
        (self.u_pixelColIdWFoV,) = struct.unpack(self.fmt_u_pixelColIdWFoV, buffer[13:14])
        (self.u_pixelRowIdNFoV,) = struct.unpack(self.fmt_u_pixelRowIdNFoV, buffer[14:15])
        (self.u_pixelColIdNFoV,) = struct.unpack(self.fmt_u_pixelColIdNFoV, buffer[15:16])

def create_rxData_array(input_buffer):
    '''
    Create python-formatted data structure for EVS getFrame binary output

    Returns:
        rx_data_list: all rx data
        data2d_intensity: 2d numpy array, [idx, idy] -> intensity data int4
        data2d_distance: 2d numpy array, [idx, idy] -> distance data int4
    '''
    rx_data_list = []
    data2d_intensity = np.zeros((86, 166))
    data2d_distance = np.zeros((86, 166))

    werid_counter = 0

    BYTE_OFFSET = 12  # Start reading from the 12th byte
    RX_STRUCT_BYTE_SIZE = 16  # Size of each rxData_returns object in bytes

    # Low Speed = 25840 Shoots, High Speed = 14742
    # num_shots = 14742

    num_shots = ((len(input_buffer)-BYTE_OFFSET))//RX_STRUCT_BYTE_SIZE
    

    print(f'num_shots: {num_shots}')

    for i in range(num_shots):
        idx = i * RX_STRUCT_BYTE_SIZE + BYTE_OFFSET

        data_buffer = input_buffer[ idx : idx+RX_STRUCT_BYTE_SIZE ]
        rx_data = rxData_returns(data_buffer)

        rx_data_list.append(rx_data)
        try:
            data2d_intensity[rx_data.u_pixelRowIdNFoV, rx_data.u_pixelColIdNFoV] = rx_data.u_intensity
            data2d_distance[rx_data.u_pixelRowIdNFoV, rx_data.u_pixelColIdNFoV] = rx_data.u_distance
        except Exception:
            werid_counter += 1

    print(f"Weird value counter: {werid_counter}")
    return rx_data_list, data2d_intensity, data2d_distance

def create_fig_data2d(data2d_intensity, data2d_distance):
    '''
    Generate MatPlotLib figure specifically for EVS Rx data
    '''
    fig = plt.figure(figsize=(9, 4))

    ax1 = fig.add_subplot(1, 2, 1)
    im = ax1.imshow(data2d_intensity, cmap='viridis', origin='lower', aspect='auto')
    plt.colorbar(im, ax=ax1, label='Data Values')
    ax1.set_xlabel('RxColAct')
    ax1.set_ylabel('RxRowAct')
    ax1.set_title('Intensity')

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    x, y = np.meshgrid(np.arange(data2d_distance.shape[1]), np.arange(data2d_distance.shape[0]))
    surf = ax2.plot_surface(x, y, data2d_distance, cmap='viridis')
    ax2.set_xlabel('RxColAct')
    ax2.set_ylabel('RxRowAct')
    ax2.set_zlabel('Data Values')
    ax2.set_title('Distance')

    return fig, im, surf

def update_plot(im, surf, data2d_intensity, data2d_distance):
    '''Update the Intensity Plot'''
    im.set_data(data2d_intensity)
    im.autoscale()

    # Update the 3D Distance Plot
    ax = surf.axes
    ax.clear()
    x, y = np.meshgrid(np.arange(data2d_distance.shape[1]), np.arange(data2d_distance.shape[0]))
    surf = ax.plot_surface(x, y, data2d_distance, cmap='viridis')
    ax.set_xlabel('RxColAct')
    ax.set_ylabel('RxRowAct')
    ax.set_zlabel('Data Values')
    ax.set_title('Distance')

    plt.draw()
    plt.pause(0.1)

def get_data2d(file_name):
    '''
    Decode a Rx binary file given its file path
    '''
    # Read the binary file
    with open(file_name, 'rb') as file:
        buffer = file.read()

    # Create the array of rxData_returns objects
    return create_rxData_array(buffer)
    
def get_fig_from_file(file_name):
    '''
    Generate figure given file path
    '''
    rx_data_objects, data2d_intensity, data2d_distance = get_data2d(file_name)
    
    # Print first 5 values to terminal
    # for obj in rx_data_objects[:5]:
    #         print(obj)

    # generate figure
    fig = create_fig_data2d(data2d_intensity, data2d_distance)
    # return figure for gui
    return fig

def get_illuminated_pixel(data2d_distance, data2d_intensity, display = True):
    # Find the index of the maximum value in the flattened array
    d_max_index_flat = np.argmax(data2d_distance)
    i_max_index_flat = np.argmax(data2d_intensity)

    # Convert the flattened index to 2D index
    d_max_index_2d = np.unravel_index(d_max_index_flat, data2d_distance.shape)
    i_max_index_2d = np.unravel_index(i_max_index_flat, data2d_intensity.shape)

    # Get the maximum value
    d_max_value = data2d_distance[d_max_index_2d]
    i_max_value = data2d_distance[i_max_index_2d]

    if display:
        # Display results in console
        print("Max distance pixel:")
        print("Index:", d_max_index_2d)
        print("Value:", d_max_value)

        print("Max intensity pixel:")
        print("Index:", i_max_index_2d)
        print("Value:", i_max_value)

    return d_max_index_2d, d_max_value, i_max_index_2d, i_max_value
