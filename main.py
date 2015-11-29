""" Will Luckin <will@luckin.co.uk> """

import numpy as np
from numpy.linalg import norm
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from mpl_toolkits.mplot3d import Axes3D

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

# Initialise global variables
# Holds all orbiting objects
orbiters = []
# Holds all dead paths
dead_paths = []
# G
g = 5.
# Speed of light
c = 3e8

dt = 16./1000.

PARTICLES = 50

# Generate figure and axis object
fig = plt.figure()
ax = fig.add_subplot(111)  # new method to create 3d plots
ax.set_xlim(-1000, 1000)
ax.set_ylim(-1000, 1000)

class orbiter(object):
    """ Represent a gravitational object """
    def __init__(self, **kwargs):
        self.mass = kwargs.get("mass") or 1.
        self.pos = kwargs.pop("pos", np.array([0., 0.]))
        self.vel = kwargs.pop("vel", np.array([0., 0.]))
        self.acc = kwargs.pop("acc", np.array([0., 0.]))
        self.radius = 0.2*self.mass**(1/3.)
        self.line = kwargs.pop("line", ax.plot(np.array([self.pos[0]]), np.array([self.pos[1]])))[0]
        self.path = []
        self.acc_ = self.acc
        orbiters.append(self)

    def calcInteractions(self):
        """ Calculate the acceleration of this object based on all objects
        in the orbiters list. Save this to a temporary local variable to
        update after all calculations have been completed. """
        self.acc_ = np.array([0., 0.])  # Bind temporary variable to zero
        for orb in orbiters:
            if orb == self:  # Don't calculate the gravitational force exerted on itself
                pass
            else:
                r = self.pos - orb.pos  # Calculate the radius
                if norm(r) < (abs(self.radius) + abs(orb.radius)): # If two things collide
                        # orbiters.remove(self)  # Remove the things
                        # orbiters.remove(orb)
                        # # Create a new combined thing via conserving momentum
                        # orbiter(pos=(self.pos + orb.pos)/2,
                        #         mass=(self.mass + orb.mass),
                        #         vel=((self.mass/(self.mass + orb.mass))*self.vel +
                        #              (orb.mass/(self.mass + orb.mass))*orb.vel),
                        #         acc=np.array([0., 0.]))
                    if orb.mass > self.mass:
                        try:
                            orbiters.remove(self)
                            self.line.set_data([0], [0])
                            dead_paths.append(self.path)
                            orb.mass = (self.mass + orb.mass)
                            orb.vel = ((self.mass/(self.mass + orb.mass))*self.vel +
                                       (orb.mass/(self.mass + orb.mass))*orb.vel)
                            orb.radius = 0.2*orb.mass**(1/3.)
                            orb.acc = np.array([0., 0.])
                        except ValueError:
                            # object already removed
                            pass
                    else:
                        pass
                else:
                    # Calculate the acceleration based upon all other objects
                    self.acc_ -= (g*orb.mass/(norm(r)**3))*r

    def update(self, dt):
        """ Commits the acceleration changes made after all calculations are complete """
        self.acc = self.acc_
        self.vel += (self.acc * dt)
        self.path.append(list(self.pos))
        self.pos += (self.vel * dt)

    def draw(self):
        """ Mutates the line to change the path that was plotted """
        self.line.set_data(np.array(self.path)[:, 0], np.array(self.path)[:, 1])

# danwoods = orbiter(vel=np.array([0., 50.]), pos=np.array([-200., 0.]))
# danwoods2 = orbiter(pos=np.array([0., 0.]), mass=100000., color=(200, 0, 0))
# danwoods3 = orbiter(pos=np.array([100., 100.]), mass=20000.,
#                     vel=np.array([0., -50.]), color=(0, 200, 0))
# danwoods4 = orbiter(pos=np.array([80., 0.]), mass=1000.,
#                     vel=np.array([-20., -50.]), color=(0, 100, 0))

# danwoods = orbiter(vel=np.array([0., 50.]))
# danwoods2 = orbiter(vel=np.array([0., -20.]), pos=np.array([0., 100.]), mass=2.)

# Generate some random particles
for i in range(1, PARTICLES):
    pos_ = (rand(2)*800)-400
    line = ax.plot(np.array([pos_[0]]), np.array([pos_[1]]))
    orbiter(pos=pos_,
            line=line,
            vel=np.array([pos_[1]/2, -pos_[0]/2]),
            mass=np.random.ranf()*100000)

danwoods = orbiter(mass=7500000.,
                   pos=np.array([0., 0.]))

def animate(N):
    for i in orbiters:
        i.calcInteractions()
    for i in orbiters:
        i.update(dt)
        i.draw()
    for i in dead_paths:
        try:
            #pygame.draw.aalines(screen, (100, 100, 100), False, i, 50)
            pass
        except ValueError:
            dead_paths.remove(i)

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
