#  bar.py
#  
#  Copyright 2022  <Shaif Salehin, Arianna Martinez, I'munique Hill>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# Source: https://github.com/cameronball/pygame-timer

import pygame as pg


class Bar():

    # Preferences:
    color = (139, 225, 148)
    smoothness_of_bar = 20

    # define bar y size by 1/n of the screen
    define_bar_y_size_by = 20

    def __init__(self, window):
        self.window = window
        self.bar_y_size = (window.get_height() /
                           self.define_bar_y_size_by)
        self.pointer_pos = self.pointer_x, self.pointer_y = (
            -(window.get_width()),
            ((window.get_height())-self.bar_y_size)
        )
        size = (
            (self.window.get_width()),
            (self.window.get_height())
        )
        self.size = self.width, self.height = size

    def draw(self, add_value):
        pg.draw.rect(
            self.window,
            self.color,
            (
                self.pointer_x,
                self.pointer_y,
                self.width,
                self.height
            )
        )
        if self.pointer_x < 0:
            self.pointer_x += add_value
