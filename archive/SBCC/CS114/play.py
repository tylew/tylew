import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random

# MatplotlibGraph class for creating a Matplotlib graph
class MatplotlibGraph(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master)
        self.master = master
        self.title = title
        self.create_widgets()

    def create_widgets(self):
        self.figure, self.ax = plt.subplots()
        self.ax.set_title(self.title)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.plot_random_data()

    def plot_random_data(self):
        # Generate random data for the graph
        x = np.linspace(0, 2 * np.pi, 100)
        y = [random.uniform(-1, 1) * np.sin(xi) for xi in x]  # Randomized data
        self.ax.plot(x, y)
        self.canvas.draw()

# GraphContainer class for containing the Matplotlib graphs side by side
class GraphContainer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="white")
        self.create_widgets()

    def create_widgets(self):
        self.graph1 = MatplotlibGraph(self, "Graph 1")
        self.graph2 = MatplotlibGraph(self, "Graph 2")

        self.graph1.grid(row=0, column=0, padx=10, pady=10)
        self.graph2.grid(row=0, column=1, padx=10, pady=10)

# SimpleApp class for the main application
class SimpleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App with Random Matplotlib Graphs")
        self.configure(bg="#D3D3D3")
        self.create_widgets()

    def create_widgets(self):
        # Create a container for Matplotlib graphs
        self.graph_container = GraphContainer(self)
        self.graph_container.pack()

        # Button section
        self.update_button = ttk.Button(self, text="Update Graphs", command=self.update_graphs)
        self.update_button.pack(pady=10)

    def update_graphs(self):
        # Update the graphs with random data
        self.graph_container.graph1.plot_random_data()
        self.graph_container.graph2.plot_random_data()

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()

    app.geometry(f"{app.winfo_width()}x400")  # Set the window width based on content
    app.mainloop()

# ( function(x) ) for (x) in (itterator) if (conditional)


# y = [1,2,3,4,5,6]
# list = []

# list = [(x) for x in y if x != 5]

