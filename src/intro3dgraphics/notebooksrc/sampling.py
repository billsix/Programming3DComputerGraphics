# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# (samplinglabel)=
# # Sampling: virtual pixels and virtual texels

# %% [markdown]
# An image is a grid of **texels** (texture elements), and the screen is a
# grid of **pixels**.  To draw the image, every pixel has to answer one
# question: *which texel am I looking at?*  That is the whole problem of
# sampling, and it is hard because the two grids rarely line up.
#
# We will answer the question with the idea from the rest of this book.  A
# function takes a point from texel space to pixel space.  Its **inverse**
# takes a pixel back to texel space, and the texel that contains the answer
# supplies the color.  We build four functions, one per stage:
#
# 1. a scale of exactly 1, where the grids line up,
# 2. a scale that is not 1,
# 3. a rotation,
# 4. a rotation and a scale together.
#
# The *virtual* part: a pixel is a point (its center), and a texel is a
# square cell of texel space.  Nothing here touches OpenGL; it is numpy and
# matplotlib, so you can run it in spyder or in jupyter.

# %%
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

import math
import typing

import matplotlib.pyplot as plt
import numpy as np
from gacalc.g2 import Vector
from gacalc.transforms import (
    InvertibleFunction,
    compose,
    inverse,
    scale_non_uniform,
    translate,
)

from intro3dgraphics.mathutils import rotate

# %% [markdown]
# ## The texture
#
# An 8 by 8 grid of texels.  Red grows with the texel's column, green with
# its row, and every other texel is darkened, so you can tell neighbors
# apart and see which way is up.  Texel (0, 0), the corner of the grid, is
# the darkest red.

# %%
TEXELS_ACROSS: int = 8

# indexed [row, column, rgb]
texture: np.ndarray = np.zeros((TEXELS_ACROSS, TEXELS_ACROSS, 3))
for row in range(TEXELS_ACROSS):
    for column in range(TEXELS_ACROSS):
        darken: float = 0.6 if (row + column) % 2 == 0 else 1.0
        texture[row, column] = (
            darken * (0.15 + 0.85 * column / (TEXELS_ACROSS - 1)),
            darken * (0.15 + 0.85 * row / (TEXELS_ACROSS - 1)),
            darken * 0.5,
        )

# %% [markdown]
# ## Answering "which texel am I looking at?"
#
# `sample` visits every pixel of a `pixels_across` by `pixels_across`
# picture.  For each one it:
#
# 1. takes the pixel's center, `(column + 0.5, row + 0.5)`,
# 2. sends it through the **inverse** of `texel_to_pixel`, landing in texel
#    space,
# 3. takes the texel whose cell contains that point (`floor`), and
# 4. copies that texel's color.
#
# It also counts how many pixels chose each texel.  A texel chosen zero
# times was skipped; a texel chosen many times was stretched.  A point that
# lands outside the texture gets gray.

# %%
OUTSIDE: tuple[float, float, float] = (0.85, 0.85, 0.85)


def sample(
    texel_to_pixel: InvertibleFunction[Vector], pixels_across: int
) -> tuple[np.ndarray, np.ndarray]:
    """Draw ``texture`` through ``texel_to_pixel`` with nearest sampling.

    Args:
        texel_to_pixel: Takes a point in texel space to pixel space.
        pixels_across: Width and height of the picture, in pixels.

    Returns:
        The picture, indexed ``[row, column, rgb]``, and how many pixels
        sampled each texel, indexed ``[row, column]``.
    """
    picture: np.ndarray = np.zeros((pixels_across, pixels_across, 3))
    hits: np.ndarray = np.zeros((TEXELS_ACROSS, TEXELS_ACROSS), dtype=int)
    for pixel_row in range(pixels_across):
        for pixel_column in range(pixels_across):
            # a pixel is the point at its center
            pixel_center: Vector = Vector(
                coeff_e_1=pixel_column + 0.5, coeff_e_2=pixel_row + 0.5
            )
            u, v = inverse(texel_to_pixel)(pixel_center)
            # the texel whose cell contains the point
            texel_column: int = math.floor(float(u))
            texel_row: int = math.floor(float(v))
            if (
                0 <= texel_column < TEXELS_ACROSS
                and 0 <= texel_row < TEXELS_ACROSS
            ):
                picture[pixel_row, pixel_column] = texture[
                    texel_row, texel_column
                ]
                hits[texel_row, texel_column] += 1
            else:
                picture[pixel_row, pixel_column] = OUTSIDE
    return picture, hits


# %% [markdown]
# `show` draws three panels: the texture, the picture a viewer would see,
# and the number of pixels that sampled each texel.  Zeros in the right-hand
# panel are texels that never made it to the screen.


# %%
def show(
    title: str, texel_to_pixel: InvertibleFunction[Vector], pixels_across: int
) -> None:
    """Sample the texture and plot the texture, picture and hit counts.

    Args:
        title: The figure's heading.
        texel_to_pixel: Takes a point in texel space to pixel space.
        pixels_across: Width and height of the picture, in pixels.
    """
    picture, hits = sample(texel_to_pixel, pixels_across)
    figure, (texture_axes, picture_axes, hits_axes) = plt.subplots(
        1, 3, figsize=(11, 3.8)
    )
    figure.suptitle(title)
    texture_axes.imshow(texture, interpolation="nearest")
    texture_axes.set_title(f"{TEXELS_ACROSS}x{TEXELS_ACROSS} texels")
    picture_axes.imshow(picture, interpolation="nearest")
    picture_axes.set_title(f"{pixels_across}x{pixels_across} pixels")
    hits_image: typing.Any = hits_axes.imshow(hits, cmap="viridis", vmin=0)
    hits_axes.set_title("pixels that chose each texel")
    for row in range(TEXELS_ACROSS):
        for column in range(TEXELS_ACROSS):
            hits_axes.text(
                column,
                row,
                str(hits[row, column]),
                ha="center",
                va="center",
                color="white",
                fontsize=7,
            )
    figure.colorbar(hits_image, ax=hits_axes, fraction=0.046)
    plt.show()
    unused: int = int((hits == 0).sum())
    print(
        f"texels never chosen: {unused}; most pixels on one texel: {hits.max()}"
    )


# %% [markdown]
# ## Stage 1: scale by 1, one to one
#
# Eight pixels across for eight texels across.  The inverse maps pixel
# center `(c + 0.5, r + 0.5)` to texel-space `(c + 0.5, r + 0.5)`: every
# pixel center sits at the middle of exactly one texel.  Nothing is skipped
# and nothing is repeated, so each texel is chosen exactly once, and the
# picture is the texture.

# %%
one_to_one: InvertibleFunction[Vector] = scale_non_uniform(1.0, 1.0)
show("Stage 1: scale 1, one to one", one_to_one, pixels_across=8)

# %% [markdown]
# ## Stage 2: scale by something other than 1
#
# **Magnify** by 2.5: the picture is 20 pixels across, so each texel covers
# 2.5 pixels in each direction.  Some texels are chosen by two pixels across
# and some by three, because 2.5 is not a whole number, so in the
# right-hand panel a texel is chosen by anywhere from 4 to 9 pixels.  The
# edges between texels come out uneven.
#
# **Minify** by 0.4: the picture is 3 pixels across, so each pixel spans
# 2.5 texels, and it can only choose one.  The other texels are skipped, and
# which ones survive depends on where the pixel centers happen to fall.
# That is **aliasing**: a different scale or a small shift would show a
# different set of texels.

# %%
magnify: InvertibleFunction[Vector] = scale_non_uniform(2.5, 2.5)
show("Stage 2a: scale 2.5, magnification", magnify, pixels_across=20)

# %%
minify: InvertibleFunction[Vector] = scale_non_uniform(0.4, 0.4)
show("Stage 2b: scale 0.4, minification", minify, pixels_across=3)

# %% [markdown]
# ## Stage 3: rotation
#
# `rotate` turns about the origin, which would swing the texture out of the
# picture.  To turn the texture about its own center, move that center to
# the origin, rotate, and move it to the center of the picture:
#
# `translate(picture center) . rotate(angle) . translate(-texture center)`
#
# read right to left, the same as every composition in this book.  Even at
# scale 1, a rotated texel grid no longer lines up with the pixel grid, so a
# pixel center usually lands near an edge or a corner of a texel, and
# neighboring pixels in the picture can come from texels that are not
# neighbors.  The picture shows jagged steps along edges that are straight
# in the texture.

# %%
TEXTURE_CENTER: Vector = Vector(
    coeff_e_1=TEXELS_ACROSS / 2, coeff_e_2=TEXELS_ACROSS / 2
)
PICTURE_CENTER: Vector = Vector(coeff_e_1=6.0, coeff_e_2=6.0)

rotation_only: InvertibleFunction[Vector] = compose(
    [
        translate(b=PICTURE_CENTER),
        rotate(math.radians(30)),
        translate(b=-TEXTURE_CENTER),
    ]
)
show("Stage 3: rotate 30 degrees, scale 1", rotation_only, pixels_across=12)

# %% [markdown]
# ## Stage 4: rotation and scale together
#
# Scale first (right to left), then rotate.  Now both problems appear at
# once: the grids are misaligned by the rotation, *and* the pixel spacing
# disagrees with the texel spacing.  Here the texture is magnified by 1.7
# and turned 30 degrees, in a picture 16 pixels across.

# %%
PICTURE_CENTER_4: Vector = Vector(coeff_e_1=8.0, coeff_e_2=8.0)

rotation_and_scale: InvertibleFunction[Vector] = compose(
    [
        translate(b=PICTURE_CENTER_4),
        rotate(math.radians(30)),
        scale_non_uniform(1.7, 1.7),
        translate(b=-TEXTURE_CENTER),
    ]
)
show(
    "Stage 4: rotate 30 degrees and scale 1.7",
    rotation_and_scale,
    pixels_across=16,
)

# %% [markdown]
# ## What the picture is telling us
#
# Choosing the single texel under the pixel center ("nearest" sampling) is
# cheap, and it is exact only in stage 1.  Everywhere else the counts in the
# right-hand panel are uneven: some texels are shown too often, and some not
# at all.  Real texture units soften this by blending the four texels around
# the point (bilinear filtering) and, for minification, by averaging over a
# prefiltered set of smaller copies of the texture (mipmaps).  Both start
# from the same inverse map you built here.
