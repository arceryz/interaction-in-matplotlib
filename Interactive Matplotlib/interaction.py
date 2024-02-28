# Python matplotlib library for animated and interactive plots!
# Unleash the power of the interactive world.
# by Arceryz.

#
# We import the necessary matplotlib modules.
# Next to the pyplot namespace, we import the necessary parts
# for interactivity. Add more if needed!
#
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider, Button
import numpy as np

#
# The first thing we need to do is create the window.
# In matplotlib this is called a 'figure'.
# A figure does not contain the plot information, this is what Axes are for.
#
# The main axes object 'root_axes' , is created with the window and spans
# the largest part of the screen.
# We declare them here with type to get nice syntax completion and documentation.
#
fig: Figure
root_axes: Axes

# With the subplots call we can create tiled patterns of axes for
# side-by-side plots or whatever. It is a convenience to avoid having
# to write fig.add_axes([left, bottom, width, height]) for each plot (as we do later for UI).
fig, root_axes = plt.subplots()

# By default the subplots use the whole window, but we want some
# space for adding UI elements, 
# here we can override the box left, bottom, top, right with values from 0 to 1.
fig.subplots_adjust(right=0.7)

#
# Without calling axes directly we set xlim and ylim by calling plt.xlim(...) etc.
# When using the Axes class, we use set* functions to do this. 
# i.e root_axes.set_title(...).
# Using root_axes.set(...) we can set them all at once aswell.
# 
root_axes.set_title("Interactive Graph")
root_axes.set_xlim(0, 10)
root_axes.set_ylim(0, 10)
root_axes.set_xlabel("X Axis")
root_axes.set_ylabel("Y Axis")
root_axes.grid()
# root_axes.set(title="Interactive Graph", xlim=[0, 100], ylim=[0,100], xlabel="X Axis", ylabel="Y Axis")

#
# Here we create the graph objects which we will update over time.
# So rather than plotting one, we create graph objects now and modify their Y-data.
# We create an empty ylist since we will set it every frame later.
#
xlist = np.linspace(0, 10, 100)
ylist = np.zeros(100)

# We link the xlist and ylist to the plot here.
# It returns a list of Line2D's, we have only one so take the first.
graph1: Line2D = root_axes.plot(xlist, ylist)[0]

#
# The axes are the actual UI elements in matplotlib.
# When creating a plot, you always need one Axes object to put the plot in.
# Dont confuse an 'Axes' object with the X and Y axes of a graph!
#
# The axes can be arranged inside a figure by specifying their rectangle
# The coordinate system is [ left, bottom, width, height ] describes a rectangle
# from the lower left corner of the window.
#
# You can create plots in them by calling axes1.plot(...) or you can attach objects
# such as sliders and buttons by referring to them.
#
ax_spacing = 0.04
ax_width = 0.15
axes1: Axes = fig.add_axes([0.8, 1-ax_spacing, ax_width, ax_spacing/2])
axes2: Axes = fig.add_axes([0.8, 1-2*ax_spacing, ax_width, ax_spacing/2])
#axes3: Axes = fig.add_axes([0.8, 1-3*ax_spacing, ax_width, ax_spacing/2])
#axes4: Axes = fig.add_axes([0.8, 1-4*ax_spacing, ax_width, ax_spacing/2])
axes_button: Axes = fig.add_axes([0.8, ax_spacing, ax_width, 0.05])

#
# We can connect special UI elements like buttons and sliders to Axes.,
# You can use them in your equations as (var1.val + var2.val) etc.
# These sliders/buttons have many arguments for customization!
#
speed_slider = Slider(ax=axes1, label="Speed", valmin=0, valmax=10, valinit=3)
amplitude_slider = Slider(ax=axes2, label="Amplitude", valmin=0, valmax=5, valinit=5)

# For the reset button we define a function what to do when
# the button is clicked. We reset all the slider values!
def on_reset_clicked(event):
    # Add variables to reset to this list!
    resetlist = [ speed_slider, amplitude_slider ]
    for var in resetlist:
        var.reset()
    pass

# We link the callback to the button with .on_clicked(...)
reset_button = Button(ax=axes_button, label="Reset")
reset_button.on_clicked(on_reset_clicked)

#
# This is the core of this animation program.
# In here, rather than using the plt.plot(...) function, we update the
# data in an existing graph object we created earlier.
def update(time):
    # Do update logic here!
    ylist = [ 5+amplitude_slider.val*np.sin(x+speed_slider.val*time) for x in xlist ]
    graph1.set_ydata(ylist)

    # Can dynamically set anything!
    root_axes.set_title("Interactive graph at time={:3.2f}".format(time))

#
# Here create a list of time values that will be passed to the update.
# We compute time_per_frame to have the animation run in seconds.
#
num_frames = 1000
t_end = 10
time_per_frame = 1000 * t_end / num_frames
time_list = np.linspace(0, t_end, num_frames)

# Interval represents the time in ms between two frames.
ani = FuncAnimation(fig=fig, func=update, frames=time_list, interval=time_per_frame)
plt.show()