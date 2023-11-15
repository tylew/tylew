import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from queue import Queue

import tkinter as tk
from tkinter import ttk
import time

from evs.ReadBinFile import *


class GraphFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.fig = plt.figure(figsize=(9, 4))

        data2d_intensity = np.zeros((86, 166))
        data2d_distance = np.zeros((86, 166))

        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.im1 = self.ax1.imshow(data2d_intensity, cmap='viridis', origin='lower', aspect='auto')
        plt.colorbar(self.im1, ax=self.ax1, label='Data Values')
        self.ax1.set_xlabel('RxColAct')
        self.ax1.set_ylabel('RxRowAct')
        self.ax1.set_title('Intensity')

        self.ax2 = self.fig.add_subplot(1, 2, 2, projection='3d')
        x, y = np.meshgrid(np.arange(data2d_distance.shape[1]), np.arange(data2d_distance.shape[0]))
        self.ax2.plot_surface(x, y, data2d_distance, cmap='viridis')
        self.ax2.set_xlabel('RxColAct')
        self.ax2.set_ylabel('RxRowAct')
        self.ax2.set_zlabel('Data Values')
        self.ax2.set_title('Distance')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_graph(self, new_data_intensity, new_data_distance):
        self.im1.set_data(new_data_intensity)
        self.im1.autoscale()

        self.ax2.clear()
        x, y = np.meshgrid(np.arange(new_data_distance.shape[1]), np.arange(new_data_distance.shape[0]))
        self.ax2.plot_surface(x, y, new_data_distance, cmap='viridis')
        self.ax2.set_xlabel('RxColAct')
        self.ax2.set_ylabel('RxRowAct')
        self.ax2.set_zlabel('Data Values')
        self.ax2.set_title('Distance')

        self.canvas.draw_idle()

class MotorControlFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.move_left_button = ttk.Button(self, text="Move counter-clockwise", command=self.move_left)
        self.move_left_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.move_right_button = ttk.Button(self, text="Move clockwise", command=self.move_right)
        self.move_right_button.grid(row=0, column=1, padx=5, pady=5)

    def move_left(self):
        print("Moving motor left.")
        # Add your logic here to move the motor left
        self.master.device_queue.put(('move_motor_relative', -2,))

    def move_right(self):
        print("Moving motor right.")
        # Add your logic here to move the motor right
        self.master.device_queue.put(('move_motor_relative', 2,))


class SimpleApp(tk.Tk):
    def __init__(self, device_queue, terminate, lock):
        super().__init__()
        self.device_queue = device_queue
        self.terminate = terminate
        self.lock = lock
        self.is_resizing = False
        self.title("Simple Tkinter App")
        self.create_widgets()
        self.bind('<Configure>', self.on_configure)

    def on_configure(self, event):
        self.is_resizing = True
        self.after(200, self.reset_resize_flag)

    def reset_resize_flag(self):
        self.is_resizing = False

    def create_widgets(self):
        self.graph_frame = GraphFrame(self)
        self.graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_rowconfigure(0, weight=1)

        self.motor_control_frame = MotorControlFrame(self)
        self.motor_control_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.quit_button = ttk.Button(self, text="Quit", command=self.terminate_program)
        self.quit_button.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

    def terminate_program(self):
        with self.lock:
            self.terminate.value = True

    # def update_graph(self, file_name):
    #     self.graph_frame.update_graph(file_name)

import threading
import queue

def process_queue(q, app):
    queued_data = None
    while True:
        try:
            if not app.is_resizing:
                if queued_data:
                    command_tuple = queued_data
                    queued_data = None  # Clear the queued data
                else:
                    command_tuple = q.get(timeout=0.1)

                if command_tuple[0] == "update_graphs":
                    app.after(0, app.graph_frame.update_graph, command_tuple[1], command_tuple[2])
                else:
                    print('Invalid queue command issued.')
            else:
                try:
                    queued_data = q.get_nowait()  # Get the latest data if available
                except queue.Empty:
                    pass  # No new data
        except queue.Empty:
            continue
        except Exception as e:
            print('Encountered exception in queue processing thread:', e)
            time.sleep(0.1)

def gui_target(queue, device_queue, terminate, lock):
    # global lock
    app = SimpleApp(device_queue, terminate, lock)
    
    # Start the queue processing thread
    queue_thread = threading.Thread(target=process_queue, args=(queue, app))
    queue_thread.daemon = True  # Daemonize thread
    queue_thread.start()

    app.mainloop()
