#  bg_test.py
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
#  Created by: Shaif Salehin

import cv2
import numpy as np 


while True:
    #This is to check whether to break the first loop
    isclosed=0
    cap = cv2.VideoCapture('Assets/misc/bg.mp4')
    while (True):

        ret, frame = cap.read()
        # It should only show the frame when the ret is true
        if ret == True:

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) == 27:
                # When esc is pressed isclosed is 1
                isclosed=1
                break
        else:
            break
    # To break the loop if it is closed manually
    if isclosed:
        break



cap.release()
cv2.destroyAllWindows()
