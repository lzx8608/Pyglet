#!/usr/bin/env python

'''Press R,G,B,S keys to alter target color and saturation.
'''

print __doc__

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

from ctypes import *

from pyglet.GL.VERSION_1_1 import *
from pyglet.clock import *
from pyglet.image import *
from pyglet.window import *
from pyglet.window.event import *
from pyglet.window.key import *


def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def on_key_press(symbol, modifiers):
    global target
    if symbol == K_R:
        target[0] = 1 - target[0]
    if symbol == K_G:
        target[1] = 1 - target[1]
    if symbol == K_B:
        target[2] = 1 - target[2]
    if symbol == K_S:
        target[3] = 1 - target[3]

    print_target()

def print_target():
    print 'Target color  %r saturation %f' % (target[:3], target[3])

# s is saturation, 0 = original image, 1 = solid color
def blend_to_color(r, g, b, s):
    # C = Cf(1 - Cs) + CcCs, A = AfAs
    # C = out color
    # Cf = vertex color, Cs = texture color, Cc = texture env color
    # A = out alpha
    # Af = vertex alpha, As = texture alpha
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)
    glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, 
        (c_float * 4)(r + (1-s)*(1-r), g + (1-s)*(1-g), b + (1-s)*(1-b), 1))
    glColor3f(s*r, s*g, s*b)

exit_handler = ExitHandler()
clock = Clock()
w = Window()
w.push_handlers(on_resize)
w.push_handlers(on_key_press)
w.push_handlers(exit_handler)
on_resize(w.width, w.height)

tex = Texture.load('tests/image/rgba.png')
# ordinary blend func
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glClearColor(0, 1, 1, 1)

current = [0, 0, 0, 0]
target = [0, 0, 0, 1]

print_target()

while not exit_handler.exit:
    dt = clock.tick() / 2
    if current != target:
        # hacky linear vector interpolation
        current = [c + dt * ((t-c) and abs(t-c)/(t-c)) \
                   for t,c in zip(target, current)]

    w.dispatch_events()
    glClear(GL_COLOR_BUFFER_BIT)
    blend_to_color(*current)
    tex.draw()
    w.flip()