import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Test pygame")

from cap_graph import *
from deck import *
from player import *

# Chargement des cartes
deck = deck("card/cards.xml")
events = [ None ]

# Initialisation pygame
background = pygame.image.load("background.jpg").convert()
quit = False
window.blit(background, (0,0))

event_mouse = []
event_key   = []

display_list  = []

class cap_clickDetector:

	def __init__(self):
		# Moitié haute
		self.up = cap_Rect(0, 0, 1280, 400)

		# Zone de carte haute
		self.up_hand = cap_Rect(60, 0, 1160, 86)

		# Gameboard haute
		self.up_gameboard = cap_Rect(350, 120, 580, 240)

		# Deck
		self.up_deck = cap_Rect(50, 188, 200, 143)

		# Event
		self.up_event = cap_Rect(50, 107, 145, 60)

		# Zone de carte basse
		self.low_hand = cap_Rect(60, 712, 1160, 88)

		# Gameboard basse
		self.low_gameboard = cap_Rect(350, 449, 580, 240)

		# Deck
		self.low_deck = cap_Rect(1037, 552, 200, 143)

	def get_zone(self, x, y):
		# Haut
		if self.up.isIn(x,y) :
			if self.up_hand.isIn(x, y) :				
				return ("up", "hand", int((x - self.up_hand.x) / 145))
			elif self.up_gameboard.isIn(x, y) :
				return ("up", "gameboard", int((x - self.up_gameboard.x) / 145), int((y - self.up_gameboard.y) / 60))
			elif self.up_deck.isIn(x, y) :
				return ("up", "deck")
			elif self.up_event.isIn(x, y) :
				return ("up", "event")
			else:
				return ("up")
		# Bas
		else :
			if self.low_hand.isIn(x, y) :				
				return ("low", "hand", int((x - self.low_hand.x) / 145))
			elif self.low_gameboard.isIn(x, y) :
				x = int((x - self.low_gameboard.x) / 145)
				y = int((y - self.low_gameboard.y) / 60)
				if x > 3 : x = 3
				if y > 3 : y = 3
				return ("low", "gameboard", x, y)
			elif self.low_deck.isIn(x, y) :
				return ("low", "deck")
			else :
				return ("low")

clicker_detector = cap_clickDetector()

# Chargement graphique du deck
deck.init(event_mouse, event_key, display_list)

deck_defausse = cap_Graph_discard([])
deck_defausse.init(event_mouse, event_key, display_list)
deck_defausse.visibility(True)

deck_deck = cap_Graph_deck(deck)
deck_deck.init(event_mouse, event_key, display_list)
deck_deck.visibility(True)

log = cap_Graph_msg()
log.init(event_mouse, event_key, display_list)
log.visibility(True)

player1 = Player("Player 1", log)
player1.graph_player.init(event_mouse, event_key, display_list)
player1.graph_player.visibility(True)

# Boucle d'affichage / évenements
while not quit :
	window.blit(background, (0,0))

	# Affichage des choses à afficher
	for clbk in display_list :
		clbk(window)

	# Refresh
	pygame.display.flip()

	# Events de la fenêtre
	for event in pygame.event.get():

		# Boutons fenêtre
		if event.type == QUIT:
			quit = True

		# Clavier
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				quit = True
			else :
				player1.addCardDeck(deck.pickUpCardFromDeck())

		# Souris
		if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION :

			if event.type == MOUSEBUTTONDOWN :
				print(clicker_detector.get_zone(event.pos[0], event.pos[1]))
				player1.playerAction(clicker_detector.get_zone(event.pos[0], event.pos[1]), events, None)

			for clbk in event_mouse :
				# Si l'event se passe dans notre range
				if clbk[0] == event.type and ( not hasattr(event, 'button') or clbk[1] == event.button ) :
					if hasattr(event, 'button') :
						button = event.button
					else :
						button = 0
					if clbk[2](event.type, button, event.pos[0], event.pos[1]):
						break

	pass