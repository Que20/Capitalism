import pygame
import os
from pygame.locals import *

pygame.init()
wh = (300, 400)
screen = pygame.display.set_mode(wh)
background_colour = (255,255,255)
pygame.display.set_caption('Capitalism Launcher')

from cap_rect import *
from cap_graph import *


def start():
	print("start")
	pygame.display.quit()
	os.system("py test_card.py")

def quit():
	print("quit")
	global running
	running = False

def about():
	print("about")

event_mouse = []
event_key = []
display_list = []

# Graphique
menu_logo = pygame.image.load("card/menu_logo.png").convert_alpha()
menu_start = pygame.image.load("card/menu_start.png").convert_alpha()
menu_quit = pygame.image.load("card/menu_quit.png").convert_alpha()
menu_about = pygame.image.load("card/menu_about.png").convert_alpha()

b1 = cap_graph_Button(cap_Rect(26,200,247,59), cap_Rect(0,0,247,59), menu_start, menu_start, menu_start, start)
b1.init(event_mouse, event_key, display_list)
b1.visibility(True)

b2 = cap_graph_Button(cap_Rect(26,260,247,59), cap_Rect(0,0,247,59), menu_quit, menu_quit, menu_quit, quit)
b2.init(event_mouse, event_key, display_list)
b2.visibility(True)

b3 = cap_graph_Button(cap_Rect(26,320,247,59), cap_Rect(0,0,247,59), menu_about, menu_about, menu_about, about)
b3.init(event_mouse, event_key, display_list)
b3.visibility(True)

running = True
while running:
	screen.fill(background_colour)
	screen.blit(menu_logo, (25,10))

	for clbk in display_list :
		clbk(screen)

	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False

		if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
			for clbk in event_mouse :
				if clbk[0] == event.type and (not hasattr(event, "button") or clbk[1] == event.button):
					if hasattr(event, 'button') :
						button = event.button
					else :
						button = 0
					if clbk[2](event.type, button, event.pos[0], event.pos[1]):
						break