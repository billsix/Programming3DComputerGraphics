# Copyright (c) 2025-2026 William Emerison Six
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

# Stencil lens -- the "lens of truth" effect, drawn with the stencil buffer.
#
# A room with a floor and three pillars is always visible.  A creature
# stands in the middle of it, but it is only drawn where a circular
# "lens" has marked the stencil buffer.  Every frame has three steps:
#
#   1. Draw the room normally.
#   2. Draw a flat circle into the STENCIL buffer only (colour and depth
#      writes off), setting each stencil value it covers to 1.
#   3. Draw the creature with the stencil test set to pass only where the
#      stencil value is 1.
#
# Controls:  LEFT/RIGHT/UP/DOWN move the lens, PAGE_UP/PAGE_DOWN resize
# it, and S switches the stencil test off, so the creature is drawn
# everywhere and you can see what the mask was hiding.

import math
import sys
import typing

import glfw
import OpenGL.GL as GL
import OpenGL.GLU as GLU

from intro3dgraphics.util.windowing import on_key

# This file is a program, not a module: from here on it acquires resources (a
# window, a GL context) and then runs its own loop.  A tool that imports it to
# inspect it stops here instead of opening a window.
if __name__ != "__main__":
    sys.exit("this is a demo, run it directly rather than importing it")


if not glfw.init():
    sys.exit()

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 1)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
# the stencil buffer only exists if we ask for one before the window is made
glfw.window_hint(glfw.STENCIL_BITS, 8)

window: typing.Any = glfw.create_window(600, 600, "Stencil lens", None, None)
if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)
glfw.set_key_callback(window, on_key)

GL.glClearColor(0.0289, 0.071875, 0.0972, 1.0)
GL.glClearStencil(0)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glDepthFunc(GL.GL_LEQUAL)

# lens position and radius, in normalized device coordinates
lens_x: float = 0.0
lens_y: float = 0.25
lens_radius: float = 0.3

use_stencil: bool = True
s_was_down: bool = False

quadric: typing.Any = GLU.gluNewQuadric()


def draw_room() -> None:
    """The scene that is always visible: a floor and three pillars."""

    def draw_box(
        half_width: float, half_height: float, half_depth: float
    ) -> None:
        """Draw an axis-aligned box centered on the origin."""
        GL.glBegin(GL.GL_QUADS)
        for normal_axis in range(3):
            for sign in (-1.0, 1.0):
                for corner_u, corner_v in (
                    (-1, -1),
                    (1, -1),
                    (1, 1),
                    (-1, 1),
                ):
                    coordinates: list[float] = [0.0, 0.0, 0.0]
                    extent: tuple[float, float, float] = (
                        half_width,
                        half_height,
                        half_depth,
                    )
                    u_axis: int = (normal_axis + 1) % 3
                    v_axis: int = (normal_axis + 2) % 3
                    coordinates[normal_axis] = sign * extent[normal_axis]
                    coordinates[u_axis] = corner_u * extent[u_axis]
                    coordinates[v_axis] = corner_v * extent[v_axis]
                    GL.glVertex3f(*coordinates)
        GL.glEnd()

    GL.glColor3f(0.12, 0.35, 0.18)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex3f(-6.0, -1.0, 4.0)
    GL.glVertex3f(6.0, -1.0, 4.0)
    GL.glVertex3f(6.0, -1.0, -10.0)
    GL.glVertex3f(-6.0, -1.0, -10.0)
    GL.glEnd()

    GL.glColor3f(0.25, 0.4, 0.75)
    for pillar_x in (-3.0, 0.0, 3.0):
        GL.glPushMatrix()
        GL.glTranslatef(pillar_x, 1.0, -7.0)
        draw_box(0.5, 2.0, 0.5)
        GL.glPopMatrix()


def draw_creature() -> None:
    """The hidden creature: a body and head made of spheres."""
    GL.glColor3f(0.9, 0.25, 0.2)
    for center_y, radius in ((0.0, 1.0), (1.4, 0.6)):
        GL.glPushMatrix()
        GL.glTranslatef(0.0, center_y, -4.0)
        GLU.gluSphere(quadric, radius, 32, 32)
        GL.glPopMatrix()
    GL.glColor3f(1.0, 0.9, 0.3)
    for eye_x in (-0.25, 0.25):
        GL.glPushMatrix()
        GL.glTranslatef(eye_x, 1.55, -3.45)
        GLU.gluSphere(quadric, 0.12, 16, 16)
        GL.glPopMatrix()


def draw_lens_circle() -> None:
    """A flat circle in normalized device coordinates."""
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPushMatrix()
    GL.glLoadIdentity()
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glPushMatrix()
    GL.glLoadIdentity()

    GL.glBegin(GL.GL_TRIANGLE_FAN)
    GL.glVertex2f(lens_x, lens_y)
    for step in range(65):
        angle: float = 2.0 * math.pi * step / 64
        GL.glVertex2f(
            lens_x + lens_radius * math.cos(angle),
            lens_y + lens_radius * math.sin(angle),
        )
    GL.glEnd()

    GL.glPopMatrix()
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glPopMatrix()
    GL.glMatrixMode(GL.GL_MODELVIEW)


def handle_inputs() -> None:
    global lens_x, lens_y, lens_radius, use_stencil, s_was_down
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        lens_x -= 0.02
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        lens_x += 0.02
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        lens_y += 0.02
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        lens_y -= 0.02
    if glfw.get_key(window, glfw.KEY_PAGE_UP) == glfw.PRESS:
        lens_radius += 0.01
    if glfw.get_key(window, glfw.KEY_PAGE_DOWN) == glfw.PRESS:
        lens_radius = max(0.05, lens_radius - 0.01)
    s_is_down: bool = glfw.get_key(window, glfw.KEY_S) == glfw.PRESS
    if s_is_down and not s_was_down:
        use_stencil = not use_stencil
    s_was_down = s_is_down


# doc-region-begin stencil lens frame
while not glfw.window_should_close(window):
    glfw.poll_events()
    handle_inputs()

    width, height = glfw.get_framebuffer_size(window)
    side: int = min(width, height)
    GL.glViewport((width - side) // 2, (height - side) // 2, side, side)
    GL.glClear(
        GL.GL_COLOR_BUFFER_BIT  # ty: ignore
        | GL.GL_DEPTH_BUFFER_BIT
        | GL.GL_STENCIL_BUFFER_BIT
    )

    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(45.0, 1.0, 0.1, 100.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GL.glTranslatef(0.0, -0.5, -2.0)

    # 1. the room, with the stencil test off
    draw_room()

    if use_stencil:
        # 2. write 1 into the stencil buffer wherever the lens circle is,
        #    without changing a single colour or depth value
        GL.glEnable(GL.GL_STENCIL_TEST)
        GL.glStencilFunc(GL.GL_ALWAYS, 1, 0xFF)
        GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_REPLACE)
        GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
        GL.glDepthMask(GL.GL_FALSE)
        draw_lens_circle()
        GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)
        GL.glDepthMask(GL.GL_TRUE)

        # 3. draw only where the stencil value is 1, and leave it alone
        GL.glStencilFunc(GL.GL_EQUAL, 1, 0xFF)
        GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_KEEP)

    draw_creature()
    GL.glDisable(GL.GL_STENCIL_TEST)

    glfw.swap_buffers(window)
# doc-region-end stencil lens frame

glfw.terminate()
