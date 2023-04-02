# file to manage game logic

def result(playercards, dealercards, finish = False):
	# exception manager
	if type(playercards) != list:
		return TypeError(f"cards should be a list, not {type(playercards)}.")
	if type(dealercards) != list:
		return TypeError(f"dealer total should be a int, not {type(dealercards)}.")
	if type(finish) != bool:
		return TypeError(f"finish should be a boolean string, not {type(finish)}.")
	# function
	playertotal = 0
	for card in playercards:
		playertotal += int(card.number)
	dealertotal = 0
	for card in dealercards:
		dealertotal += int(card.number)
	# win calculator
	# if dealer bust and user under 21
	if finish:
		if (playertotal == dealertotal) and (dealertotal <= 21):
			return f"push.{playertotal}"
		if (playertotal > 21) and (dealertotal <= 21):
			return f"loss.{playertotal}"
		elif (playertotal <= 21) and (dealertotal > 21):
			return f"win.{playertotal}"
		elif playertotal > dealertotal:
			return f"win.{playertotal}"
		elif playertotal < dealertotal:
			return f"loss.{playertotal}"
		else:
			return Exception(f"No winner was determined. Dealer: {dealertotal} Player: {playertotal}")
	elif playertotal > 21:
		return f"bust.{playertotal}"
	elif dealertotal == 21 and playertotal < 21:
		return f"loss.{playertotal}"
	else:
		return f"active.{playertotal}"