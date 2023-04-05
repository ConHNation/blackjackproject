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
		self.number = card_num

	def __str__(self):
		return f"{self.type} {self.number}"

	def __eq__(self, other):
		if self.__class__ != other.__class__:
			return NotImplementedError
		return (self.number == other.number)

def gettotal(deck):
	total = 0
	for x in deck:
		if type(x) != card:
			return TypeError(f"expected card object, not {type(x)}")
		elif x.number == "A":
			total += 11
		elif x.number in ["J", "K", "Q"]:
			total += 10
		elif type(x.number) != int:
			return TypeError(f"card number should be integer or face card, not {type(x.number)}.")
		elif x.number > 11:
			return Exception("stop cheating")
		else:
			total += x.number
	return total	
		
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
		logging.info("New deck has been generated successfully.")
		return deck

