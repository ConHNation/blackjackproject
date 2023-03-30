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
		if card_type in ["J", "Q", "K"]:
			self.number = 10
		elif card_type == "A":
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
def new_deck(num: int):
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

def result(cards, dealertotal, finish):
	# exception manager
	if type(cards) != table:
		return Exception(f"cards should be a table, not {type(cards)}.")
	if type(dealertotal) != int:
		return TypeError(f"dealer total should be a int, not {type(dealertotal)}.")
	if type(finish != bool):
		return TypeError(f"finish should be a boolean string, not {type(finish)}.")
	# function
	playertotal = 0
	for card in cards:
		playertotal += card.number
	if finish:
		# win calculator
		# if dealer bust and user under 21