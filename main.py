#""" Will Luckin <will@luckin.co.uk> """

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
from mpl_toolkits.mplot3d import Axes3D
import Tkinter as tk
from gui import mainWindow
from orbiter import orbiter

# import sympy as s
# from sympy.parsing.sympy_parser import parse_expr

# def eval_expr(expr, x_):
#     """ Evaluate the expression with a given x value. If the expression
#     isn't numerical at this point, return false. Else, return the value.
#     """
#     try:
#         x = s.symbols("x")
#         return float(expr.subs(x, x_))
#     except TypeError:
#         return False

# # Accept input from the user as a sympy expression; handle all possible errors
# print "Please input an expression."
# expr = raw_input()
# test = parse_expr(expr)
# print eval_expr(test, 1)
dt = 16./1000.

PARTICLES = 5

# Generate figure and axis object
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-600, 600)
ax.set_ylim(-600, 600)
ax.set_zlim(-600, 600)

# Initialise the GUI
root = tk.Tk()
window = mainWindow(root, [], True, ax)


# danwoods = orbiter(vel=np.array([0., 50.]), pos=np.array([-200., 0.]))
# danwoods2 = orbiter(pos=np.array([0., 0.]), mass=100000., color=(200, 0, 0))
# danwoods3 = orbiter(pos=np.array([100., 100.]), mass=20000.,
#                     vel=np.array([0., -50.]), color=(0, 200, 0))
# danwoods4 = orbiter(pos=np.array([80., 0.]), mass=1000.,
#                     vel=np.array([-20., -50.]), color=(0, 100, 0))

# danwoods = orbiter(vel=np.array([0., 50.]))
# danwoods2 = orbiter(vel=np.array([0., -20.]), pos=np.array([0., 100.]), mass=2.)

# Generate some random particles
for i in range(0, PARTICLES):
    pos_ = (rand(3)*1000)-400
    line = ax.plot(np.array([pos_[0]]), np.array([pos_[1]]), np.array([pos_[2]]))
    orbiter(pos=pos_,
            line=line,
            vel=np.array([pos_[1]/2, -pos_[0]/2, (np.random.ranf() - 0.5)*pos_[2]/2]),
            mass=np.random.ranf()*10000,
            axis=ax,
            orbiters=window.orbiters)

# danwoods1 = orbiter(mass=10000,
#                     pos=np.array([400., 400., 400.]),
#                     vel=np.array([200., 0., 0.]))

# danwoods2 = orbiter(mass=10000,
#                     pos=np.array([-400., 400., 400.]),
#                     vel=np.array([0., -200., 0.]))

danwoods = orbiter(mass=7500000.,
                   pos=np.array([0., 0., 0.]),
                   vel=np.array([0., 0., 0.]),
                   axis=ax,
                   orbiters=window.orbiters)

window.updateList()

# Keep track of time
systime = time.clock()

def animate(N):
    """ Step the animation forward """
    # If the variable dt_ is used as the i.update(dt_) timestep, the
    # simulation will prefer keeping the same simualtion speed to the
    # same accuracy. This might lead to a terrible simulation
    if window.running == True:
        global systime
        dt_ = time.clock() - systime
        systime = time.clock()
        for i in window.orbiters:
            i.calcInteractions(dt_)
        for i in window.orbiters:
            i.update(dt_)
            i.draw()
    else:
        global systime
        systime = time.clock()

    # while len(orbiters) < PARTICLES:
    #     pos_ = (rand(2)*800)-400
    #     orbiter(pos=pos_,
    #             vel=np.array([pos_[1]/2, -pos_[0]/2]),
    #             mass=np.random.ranf()*100000,
    #             color=(np.random.randint(1, 255),
    #                    np.random.randint(1, 255),
    #                    np.random.randint(1, 255)))

line_ani = anim.FuncAnimation(fig, animate, None,
                              interval=10)

fig.show()


