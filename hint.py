# Module to manage hints for new players.
# Will only show hints once per session.

# Local Variables
fiveCardRuleHint = False

# Functions
def fiveCardRule(player):
	global fiveCardRuleHint
	if not fiveCardRuleHint:
		print("-"*28)
		if player:
			print("Hint: You have just drawn more than 5 cards.\nIn blackjack, this automatically results in a win.")
			fiveCardRuleHint = True
		else:
			print("Hint: The dealer has just drawn more than 5 cards.\nIn blackjack, this automatically results in a win.")
			fiveCardRuleHint = True

def hasDone5Card():
	if fiveCardRuleHint:
		return True
	else:
		return False