# file to manage game logic

# dependencies
import deck
import threading

def result(playercards, dealercards, finish = False):
	# exception manager
	if type(playercards) != list:
		return TypeError(f"cards should be a list, not {type(playercards)}.")
	if type(dealercards) != list:
		return TypeError(f"dealer total should be a int, not {type(dealercards)}.")
	if type(finish) != bool:
		return TypeError(f"finish should be a boolean string, not {type(finish)}.")
		
	# deck total calculator
	playertotal = deck.gettotal(playercards)
	dealertotal = deck.gettotal(dealercards)
		
	# win calculator
	# if dealer bust and user under 21
	if playertotal > 21:
		if not finish:
			return "bust"
		else:
			if dealertotal <= 21:
				return "loss"
			else:
				return "push"
	elif finish:
		if dealertotal > 21 or playertotal > dealertotal:
			return "win"
		elif dealertotal > playertotal:
			return "loss"
		else:
			return "push"
	else:
		return "active"