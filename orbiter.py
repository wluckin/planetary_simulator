import numpy as np
import matplotlib.cm as cm
from numpy.linalg import norm

# Use colourmap
colourmap = cm.get_cmap("winter")

# G
g = 6.67408e-11
# Speed of light
c = 299792458

def mass_to_color(mass, max_mass):
    """ Takes a mass and returns a matplotlib color value """
    return colourmap(int((255./np.log(max_mass))*np.log(mass)))

class orbiter(object):
    """ Represent a gravitational object """
    def __init__(self, **kwargs):
        self.mass = kwargs.get("mass") or 1.
        self.pos = np.array(kwargs.pop("pos", [0., 0., 0.]))
        self.vel = np.array(kwargs.pop("vel", [0., 0., 0.]))
        self.acc = np.array(kwargs.pop("acc", [0., 0., 0.]))
        self.ax = kwargs.pop("axis")
        self.radius = 600000.0
        self.line = kwargs.pop("line", self.ax.plot(np.array([self.pos[0]]),
                                                    np.array([self.pos[1]]),
                                                    np.array([self.pos[2]])))[0]
        
        self.path = []
        self.name = kwargs.pop("name", None)
        self.acc_ = self.acc
        self.orbiters = kwargs.pop("orbiters")

        self.line.set_color(mass_to_color(self.mass, 2e30))
        
        self.orbiters.append(self)

    def __str__(self):
        try:
            pos_ = list(np.around(self.path[0]))
        except IndexError:
            pos_ = list(np.around(self.pos))
        return self.name or "Orbiter with initial pos: {}".format(pos_)

    def reset_color(self):
        """ Reset the color (for selection purposes) """
        self.line.set_color(mass_to_color(self.mass, 7500000))

    def calcInteractions(self, dt):
        """ Calculate the acceleration of this object based on all objects
        in the orbiters list. Save this to a temporary local variable to
        update after all calculations have been completed. """
        self.acc_ = np.array([0., 0., 0.])  # Bind temporary variable to zero
        for orb in self.orbiters:
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
                            self.orbiters.remove(self)
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
                        return ((6.67e-11*orb.mass/(norm(r)**3))*r +
                                (((g**2)*(orb.mass**2))/(c**2*norm(r)**3)))
                    r_1 = r_(r)
                    r_2= r_(r+((1/2.)*r_1))
                    r_3 = r_(r+((1/2.)*r_2))
                    r_4 = r_(r+r_3)
                    r_total = (1/6.0)*(r_1 + r_4 + 2*(r_2 + r_3))
                    self.acc_ -= r_total

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
