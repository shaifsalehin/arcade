#  coin_acceptor.py
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
#  Created by: Shaif Salehin

import RPi.GPIO as GPIO


#setup
cost_to_play = 0.00# how much $ in coins to charge for playing, increment in 0.25 (only quarters are currently accepted)
credit = 0.00 # don't change unless different types of coins are being added other than quarters

    
def coin_received(object):
	global credit

	credit += 0.25

    
def coin_accepted():
	global credit, cost_to_play
	
	if credit >= cost_to_play:
		credit = 0 # correct amount of coins inserted, entered game select, reset credits
		return True
	else:
		return False

