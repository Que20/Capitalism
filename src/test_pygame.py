import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Test pygame")

from interface_rect import *
from interface_button import *
from interface_window import *

background = pygame.image.load("background.jpeg").convert()
quit = False
window.blit(background, (0,0))

event_mouse = []
event_key   = []

to_display  = []

# Création bouton
b = vz_Button(vz_Rect(20, 20, 300, 300), pygame.image.load("b1.png").convert_alpha(), pygame.image.load("b2.png").convert_alpha(), pygame.image.load("b3.png").convert_alpha())
b.init(event_mouse, to_display)

# Tests
test = vz_Window(vz_Rect(150, 150, 800, 600), None, "Fenêtre de test")
test.init(event_mouse, to_display)

test2 = vz_Window(vz_Rect(600, 10, 400, 350), None)
test2.init(event_mouse, to_display)

while not quit :
	window.blit(background, (0,0))

	# Affichage des choses à afficher
	for clbk in to_display :
		clbk(window)

	# Refresh
	pygame.display.flip()

	# Events de la fenêtre
	for event in pygame.event.get():

		# Fenêtre modale affichée
		if dialog.visible :
			

		# Le jeu
		else :
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