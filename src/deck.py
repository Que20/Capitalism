#Deck
from xmlCards import*
import random

class deck:
	def __init__(self, fileName):
		try:
			self.deck = makeDeck(parseXML(fileName))
			self.shuffleDeck()
		except Exception as e:
			print(e)
			self.deck = []
	
	def pickUpCardFromDeck(self):
		return deck.pop()
		
	def shuffleDeck(self):
		random.shuffle(self.deck)
		