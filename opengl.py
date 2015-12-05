import pygame
from pygame.locals import *

import OpenGL.GL as gl
import OpenGL.GLU as glu

def main():
    """ Main entry point to the visualisation """
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    mainloop()

def mainloop():
    """ Visualization main loop """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

main()
