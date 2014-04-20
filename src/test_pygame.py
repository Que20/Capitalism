import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((1280, 800))

background = pygame.image.load("background.jpeg").convert()
quit = False
window.blit(background, (0,0))

event_mouse = []
event_key   = []

to_display  = []

# Rectangle
class vz_Rect:

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	# Test si des coordonées son dans le rectangle
	def isIn(self, x, y):
		return (x >= self.x and x <= self.x + self.w) and (y >= self.y and y <= self.y + self.h)


# Bouton
class vz_Button:

	def __init__(self, rect, image, image_hover=None, image_click=None, on_click=None, on_hover=None):
		self.image = image
		self.image_hover = image_hover
		self.image_click = image_click
		self.rect = rect

		self.state = 0;   # 0 = defaut / 1 = hover / 2 = click

	# Initialisation
	def init(self):
		# Sur le mouve de la souris, pas de boutton, position, callback
		event_mouse.append((MOUSEMOTION, 0, self.on))
		event_mouse.append((MOUSEBUTTONDOWN, 1, self.click))
		event_mouse.append((MOUSEBUTTONUP, 1, self.click))
		# On ajoute à la liste d'affichage
		to_display.append(self.display)

	# Affichage
	def display(self):
		if self.state == 1 and self.image_hover != None :
			window.blit(self.image_hover, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		elif self.state == 2 and self.image_click != None :
			window.blit(self.image_click, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		else :
			window.blit(self.image, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

	# Callback du hover
	def on(self, event_type, event_code, x, y):
		print("Update : type : "+str(event_type)+"| code : "+str(event_code)+"| x : "+str(x)+"| y :"+str(y))
		if self.state < 2 :
			if self.rect.isIn(x, y) :
				self.state = 1
			else :
				self.state = 0

	# Callback du click
	def click(self, event_type, event_code, x, y):
		print("Click : type : "+str(event_type)+"| code : "+str(event_code)+"| x : "+str(x)+"| y :"+str(y))
		if event_type == MOUSEBUTTONDOWN :
			if self.rect.isIn(x, y) :
				self.state = 2
			else :
				if self.rect.isIn(x, y) :
					self.state = 1
				else :
					self.state = 0
		else :
			if self.rect.isIn(x, y) :
				self.state = 1
			else :
				self.state = 0
				

# Création bouton
b = vz_Button(vz_Rect(20, 20, 300, 300), pygame.image.load("b1.png").convert_alpha(), pygame.image.load("b2.png").convert_alpha(), pygame.image.load("b3.png").convert_alpha())
b.init()

while not quit :
	window.blit(background, (0,0))

	# Affichage des choses à afficher
	for clbk in to_display :
		clbk()

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
					clbk[2](event.type, button, event.pos[0], event.pos[1])

	pass