#created by: Shaif Salehin

import RPi.GPIO as GPIO


#setup
cost_to_play = 0.00 # how much $ in coins to charge for playing, increment in 0.25 (only quarters are currently accepted)
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

