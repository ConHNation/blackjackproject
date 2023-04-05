# file to manage game logic

# dependencies
import deck
import logging

def result(playercards, dealercards, finish = False):
	# exception manager
	if type(playercards) != list:
		logging.error(f"cards should be a list, not {type(playercards)}.")
		return TypeError(f"cards should be a list, not {type(playercards)}.")
	if type(dealercards) != list:
		logging.error(f"dealer total should be a int, not {type(dealercards)}.")
		return TypeError(f"dealer total should be a int, not {type(dealercards)}.")
	if type(finish) != bool:
		logging.error(f"finish should be a boolean string, not {type(finish)}.")
		return TypeError(f"finish should be a boolean string, not {type(finish)}.")
		
	# deck total calculator
	playertotal = deck.gettotal(playercards)
	dealertotal = deck.gettotal(dealercards)
	logging.debug(f"Result | Player: {playertotal} Dealer: {dealertotal}")
		
	# win calculator
	# if dealer bust and user under 21
	if playertotal > 21:
		if not finish:
			logging.debug("User over 21. Bust, dealer's turn.")
			return "bust"
		else:
			if dealertotal <= 21:
				logging.debug("User over 21 and dealer finished, bust. Dealer won.")
				return "loss"
			else:
				logging.debug("Both dealer and user over 21. User tied, push.")
				return "push"
	elif finish:
		if dealertotal > 21 or playertotal > dealertotal:
			logging.debug("Player is higher than user, win.")
			return "win"
		elif dealertotal > playertotal:
			logging.debug("Dealer is higher than user, lost.")
			return "loss"
		else:
			logging.debug("Dealer is same as user, tied. Push.")
			return "push"
	else:
		logging.debug("No result, game active.")
		return "active"