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
	playertemptotal = deck.gettotal(playercards)
	dealertemptotal = deck.gettotal(dealercards)

	# ace handler - player
	if type(playertemptotal) == int:
		playertotal = playertemptotal
	elif type(playertemptotal) == list:
		if (playertemptotal[0] > 21) and (playertemptotal[1] < 21):
			logging.debug("1st total over 21, using 2nd total.")
			playertotal = playertemptotal[1]
		elif (playertemptotal[0] > 21) and (playertemptotal[1] > 21):
			logging.debug("Both totals over 21, using 2nd total.")
			playertotal = playertemptotal[1]
		else:
			playertotal = playertemptotal[0]
	else:
		logging.error(f"The correct total to use could not be calculated with total {playertemptotal}.")

	# ace handler - dealer
	if type(dealertemptotal) == int:
		dealertotal = dealertemptotal
	elif type(dealertemptotal) == list:
		if (dealertemptotal[0] > 21) and (dealertemptotal[1] < 21):
			logging.debug("1st total over 21, using 2nd total.")
			playertotal = dealertemptotal[1]
		elif (dealertemptotal[0] > 21) and (dealertemptotal[1] > 21):
			logging.debug("Both totals over 21, using 2nd total.")
			dealertotal = dealertemptotal[1]
		else:
			dealertotal = dealertemptotal[0]
	else:
		logging.error(f"The correct total to use could not be calculated with total {dealertemptotal}.")
		
	# logs result for debugging purpouses
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