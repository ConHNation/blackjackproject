# This module contains all the functions, data and classes related to cards and the dealing of the deck.

# requirements
from random import shuffle
import logging
import threading
# all possible cards
all_card_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
all_card_types = ["♠", "♣", "♦", "♥"]

# card class - this allows me to make the cards python objects, which makes them easier to compare and reduces errors
class card:
	'''
  This is a Python class I made
	to simplify the evaluation, printing, and 
 	calculation of cards during games.

 	The __str__ function returns what should
	be printed when a deck.card object is printed.

 	The __init__ function defines the different parameters
	of a card class.

 	The __eq__ function allows multiple card objects to be 
	evaluated against each other or added up. 
 	'''
	def __init__(self, card_type, card_num):
		self.type = card_type
		if card_num in ["J", "Q", "K"]:
			self.number = 10
		elif card_num == "A":
			self.number = 11
		else:
			self.number = card_num

	def __str__(self):
		return f"{self.type} {self.number}"

	def __eq__(self, other):
		if self.__class__ != other.__class__:
			return NotImplementedError
		return (self.number == other.number)

# custom error for if there are too many decks
class TooManyDecksError(Exception):
  "Too many decks were requested."
  pass

# generates the deck
def new_deck(num):
	logging.info("Generating new deck...")
	if type(num) != int:
		logging.error("TypeError: new_deck function was given a non-integer, but requires an integer to prevent errors.")
		raise TypeError("new_deck function was given a non-integer, but requires an integer to prevent errors.")
		return None
	if int(num) > 8 or int(num) <= 0:
		return TooManyDecksError
	else:
		num = int(num)
		global all_card_types, all_card_nums
		deck = []
		for _ in range(num):
			for x in all_card_types:
				for y in all_card_nums:
					deck.append(card(x, y))
		shuffle(deck)
		return deck

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
	elif dealertotal > 21:
		return f"win.{playertotal}"
	elif dealertotal == 21:
		return f"loss.{playertotal}"
	elif dealertotal == 21:
		return f"loss.{playertotal}"
	else:
		return f"active.{playertotal}"