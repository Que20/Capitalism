import card as card
import xmlCards as cardLoader

# Partie en cours
class Game:
	"""Représente la partie en cours"""

	# Constructeur
	def __init__(self, deck, player1, player2):
		self.deck = deck
		self.player1 = player1
		self.player2 = player2
	
	