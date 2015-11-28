""" Will Luckin <will@luckin.co.uk> """

import numpy as np
import pygame
from numpy.linalg import norm
from numpy.random import rand

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
g = 10
# Speed of light
c = 3e8

# Screen parameters
WIDTH = 1280
HEIGHT = 720

# Initialise the game library, change rendering parameters
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("will.luckin.co.uk")
clock = pygame.time.Clock()

class orbiter(object):
    """ Represent a gravitational object """
    def __init__(self, **kwargs):
        self.mass = kwargs.get("mass") or 1.
        self.pos = kwargs.pop("pos", np.array([0., 0.]))
        self.vel = kwargs.pop("vel", np.array([0., 0.]))
        self.acc = kwargs.pop("acc", np.array([0., 0.]))
        self.color = kwargs.pop("color", (100, 100, 100))
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
                if norm(r) < 10: # If two things collide
                        # orbiters.remove(self)  # Remove the things
                        # orbiters.remove(orb)
                        # # Create a new combined thing via conserving momentum
                        # orbiter(pos=(self.pos + orb.pos)/2,
                        #         mass=(self.mass + orb.mass),
                        #         vel=((self.mass/(self.mass + orb.mass))*self.vel +
                        #              (orb.mass/(self.mass + orb.mass))*orb.vel),
                        #         acc=np.array([0., 0.]))
                    if orb.mass > self.mass:
                        orbiters.remove(self)
                        dead_paths.append(self.path)
                        orb.pos = (self.pos + orb.pos)/2
                        orb.mass = (self.mass + orb.mass)
                        orb.vel = ((self.mass/(self.mass + orb.mass))*self.vel +
                                   (orb.mass/(self.mass + orb.mass))*orb.vel)
                        orb.acc = np.array([0., 0.])
                    else:
                        pass
                else:
                    # Calculate the acceleration based upon all other objects
                    self.acc_ -= (g*orb.mass/(norm(r)**3))*r

    def update(self, dt_):
        """ Commits the acceleration changes made after all calculations are complete """
        self.acc = self.acc_
        self.vel += (self.acc * dt_)
        self.path.append(list(self.pos + np.array([WIDTH/2, HEIGHT/2])))
        self.pos += (self.vel * dt_)

    def draw(self):
        """ Renders the object to the pygame canvas """
        pygame.draw.circle(screen, self.color,
                           (self.pos+[WIDTH/2, HEIGHT/2]).astype(int), int(0.2*self.mass**(1/3.)))
        if len(self.path) > 2:
            pygame.draw.aalines(screen, self.color, False, self.path, 50)

# danwoods = orbiter(vel=np.array([0., 50.]), pos=np.array([-200., 0.]))
# danwoods2 = orbiter(pos=np.array([0., 0.]), mass=100000., color=(200, 0, 0))
# danwoods3 = orbiter(pos=np.array([100., 100.]), mass=20000.,
#                     vel=np.array([0., -50.]), color=(0, 200, 0))
# danwoods4 = orbiter(pos=np.array([80., 0.]), mass=1000.,
#                     vel=np.array([-20., -50.]), color=(0, 100, 0))

# danwoods = orbiter(vel=np.array([0., 50.]))
# danwoods2 = orbiter(vel=np.array([0., -20.]), pos=np.array([0., 100.]), mass=2.)

# Generate some random particles
for i in range(1, 20):
    orbiter(pos=(rand(2)*800)-400,
            vel=(rand(2)*100)-50,
            mass=np.random.ranf()*100000,
            color=(np.random.randint(1, 255),
                   np.random.randint(1, 255),
                   np.random.randint(1, 255)))

done = False

while not done:
    screen.fill((0, 0, 0))
    dt = clock.tick(60)/1000.
    for i in orbiters:
        i.calcInteractions()
    for i in orbiters:
        i.update(dt)
        i.draw()
    for i in dead_paths:
        pygame.draw.aalines(screen, (100, 100, 100), False, i, 50)
    pygame.display.flip()

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

pygame.quit()
