#""" Will Luckin <will@luckin.co.uk> """

import numpy as np
from numpy.linalg import norm
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.cm as cm
import time
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
# G
g = 5.
# Speed of light
c = 3e8

dt = 16./1000.

PARTICLES = 5

# Generate figure and axis object
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-600, 600)
ax.set_ylim(-600, 600)
ax.set_zlim(-600, 600)

# Use colourmap
colourmap = cm.get_cmap("winter")

def mass_to_color(mass, max_mass):
    """ Takes a mass and returns a matplotlib color value """
    return colourmap(int((255./np.log(max_mass))*np.log(mass)))

class orbiter(object):
    """ Represent a gravitational object """
    def __init__(self, **kwargs):
        self.mass = kwargs.get("mass") or 1.
        self.pos = kwargs.pop("pos", np.array([0., 0., 0.]))
        self.vel = kwargs.pop("vel", np.array([0., 0., 0.]))
        self.acc = kwargs.pop("acc", np.array([0., 0., 0.]))
        self.radius = 0.2*self.mass**(1/3.)
        self.line = kwargs.pop("line", ax.plot(np.array([self.pos[0]]),
                                               np.array([self.pos[1]]),
                                               np.array([self.pos[2]])))[0]
        
        self.path = []
        self.acc_ = self.acc

        self.line.set_color(mass_to_color(self.mass, 7500000))
        
        orbiters.append(self)

    def calcInteractions(self, dt):
        """ Calculate the acceleration of this object based on all objects
        in the orbiters list. Save this to a temporary local variable to
        update after all calculations have been completed. """
        self.acc_ = np.array([0., 0., 0.])  # Bind temporary variable to zero
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
                            # Stop calculating for this particle
                            orbiters.remove(self)
                            # Make the path grey
                            self.line.set_color((0.5, 0.5, 0.5))
                            orb.mass = (self.mass + orb.mass)
                            orb.vel = ((self.mass/(self.mass + orb.mass))*self.vel +
                                       (orb.mass/(self.mass + orb.mass))*orb.vel)
                            orb.radius = 0.2*orb.mass**(1/3.)
                            orb.acc = np.array([0., 0., 0.])
                        except ValueError:
                            # object already removed
                            pass
                    else:
                        pass
                else:
                    # Calculate the acceleration based upon all other objects
                    def r_(r):
                        """ Convenience function """
                        return 0.5*dt**2*(g*orb.mass/(norm(r)**3))*r
                    r_1 = r_(r)
                    r_2= r_(r+((1/2.)*r_1))
                    r_3 = r_(r+((1/2.)*r_2))
                    r_4 = r_(r+r_3)
                    r_total = (1/6.0)*(r_1 + r_4 + 2*(r_2 + r_3))
                    self.acc_ -= (r_total/(0.5*dt**2))

    def update(self, dt):
        """ Commits the acceleration changes made after all calculations are complete """
        self.acc = self.acc_
        self.vel += (self.acc * dt)
        self.path.append(list(self.pos))
        self.pos += (self.vel * dt)

    def draw(self):
        """ Mutates the line to change the path that was plotted """
        self.line.set_data(np.array(self.path)[:, 0], np.array(self.path)[:, 1])
        self.line.set_3d_properties(np.array(self.path)[:, 2])

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
            mass=np.random.ranf()*10000)

# danwoods1 = orbiter(mass=10000,
#                     pos=np.array([400., 400., 400.]),
#                     vel=np.array([200., 0., 0.]))

# danwoods2 = orbiter(mass=10000,
#                     pos=np.array([-400., 400., 400.]),
#                     vel=np.array([0., -200., 0.]))

danwoods = orbiter(mass=7500000.,
                   pos=np.array([0., 0., 0.]),
                   vel=np.array([0., 0., 0.]))

# Keep track of time
systime = time.clock()

def animate(N):
    """ Step the animation forward """
    # If the variable dt_ is used as the i.update(dt_) timestep, the
    # simulation will prefer keeping the same simualtion speed to the
    # same accuracy. This might lead to a terrible simulation
    global systime
    dt_ = time.clock() - systime
    systime = time.clock()
    for i in orbiters:
        i.calcInteractions(dt_)
    for i in orbiters:
        i.update(dt_)
        i.draw()

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
