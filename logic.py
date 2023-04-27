# Module that manages game logic.
# Only function is designed to calculate whether a round
# is finished, a turn is finished, or who won the round.

# dependencies
from deck import gettotal, getacetotal
import logging
from hint import fiveCardRule

# Calculates whether a round is finished, a turn
# is finished, or who won the round.
def result(playercards, dealercards, finish = False):
	# Confirms types of variables and raises error if wrong type.
	if type(playercards) != list:
		logging.error(f"cards should be a list, not {type(playercards)}.")
		return TypeError(f"cards should be a list, not {type(playercards)}.")
	if type(dealercards) != list:
		logging.error(f"dealer total should be a int, not {type(dealercards)}.")
		return TypeError(f"dealer total should be a int, not {type(dealercards)}.")
	if type(finish) != bool:
		logging.error(f"finish should be a boolean string, not {type(finish)}.")
		return TypeError(f"finish should be a boolean string, not {type(finish)}.")
		
	# Gets the total of the hands
	playertemptotal = gettotal(playercards)
	dealertemptotal = gettotal(dealercards)

	# Gets the correct total to use if an ace appears for the player.
	playertotal = getacetotal(playertemptotal)

	# Gets the correct total to use if an ace appears for the dealer.
	dealertotal = getacetotal(dealertemptotal)
		
	# Logs the resulting totals.
	logging.debug(f"Result | Player: {playertotal} Dealer: {dealertotal}")
		
	# Calculates the result.
	# If the user is over 21 (bust).
	if playertotal > 21:
		# If the turn isn't already finished, end the turn.
		if not finish:
			logging.debug("User over 21. Bust, dealer's turn.")
			return "bust"
		else:
			# If the dealer is under 21, player wins.
			if dealertotal <= 21:
				logging.debug("User over 21 and dealer finished, bust. Dealer won.")
				return "loss"
			# If both the dealer and player is under 21, tie game.
			else:
				logging.debug("Both dealer and user over 21. User tied, push.")
				return "push"
	# If the player has drawn 5 or more cards, player wins.
	elif len(playercards) >= 5 and playertotal < 22:
		logging.debug("Player has drawn 5 cards or more, win.")
		fiveCardRule(True)
		return "win"
	# If the dealer has drawn 5 or more cards, dealer wins.
	elif len(dealercards) >= 5 and dealertotal < 22:
		logging.debug("Dealer has drawn 5 cards or more, loss.")
		fiveCardRule(True)
		return "loss"
	# If the game is finished
	elif finish:
		# If the dealer busts or player is higher than 
		# the dealer, player wins.
		if (dealertotal > 21 or playertotal > dealertotal) and playertotal <= 21:
			logging.debug("Player is higher than dealer, win.")
			return "win"
		# If the dealer is higher than the playe, player loses.
		elif dealertotal > playertotal and dealertotal <= 21:
			logging.debug("Dealer is higher than player, lost.")
			return "loss"
		# If the dealer is the same as player or both players
		# went over 21, game is tied.
		else:
			logging.debug("Dealer is same as user, tied. Push.")
			return "push"
		# If the player is at 21 and is higher than
		# the dealer, turn over.
	elif playertotal == 21 and playertotal > dealertotal:
		logging.debug("User has blackjack, turn over.")
		return "bj"
	else:
		logging.debug("No result, game active.")
		return "active"