#created by: Shaif Salehin

import RPi.GPIO as GPIO


#setup
cost_to_play = 0.00
credit = 0.00

    
def coin_received(object):
	global credit

	credit += 0.25

    
def coin_accepted():
	global credit, cost_to_play
	
	if credit >= cost_to_play:
		credit = 0
		return True
	else:
		return False

