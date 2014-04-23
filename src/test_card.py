import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Test pygame")

from cap_graph import *
from deck import *

# Chargement des cartes
deck = deck("card/cards.xml")

# Initialisation pygame
background = pygame.image.load("background.jpg").convert()
quit = False
window.blit(background, (0,0))

event_mouse = []
event_key   = []

display_list  = []

# Chargement graphique du deck
deck.init(event_mouse, event_key, display_list)

deck.deck[0].grap_mincard.visibility(True)
deck.deck[0].grap_mincard.rect.x = 700
deck.deck[0].grap_mincard.rect.y = 120
deck.deck[1].grap_mincard.visibility(True)
deck.deck[1].grap_mincard.rect.x = 500
deck.deck[1].grap_mincard.rect.y = 50

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

		# Souris
		if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION :
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