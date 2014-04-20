import pygame
from pygame.locals import *

from interface_rect import *


# Bouton
class vz_Button:

	def __init__(self, rect, image, image_hover=None, image_click=None, on_click=None, on_hover=None):
		self.image = image
		self.image_hover = image_hover
		self.image_click = image_click
		self.rect = rect

		self.on_click = on_click
		self.on_hover = on_hover

		self.state = 0;   # 0 = defaut / 1 = hover / 2 = click

	# Initialisation
	def init(self, event_mouse, to_display):
		# Sur le mouve de la souris, pas de boutton, position, callback
		event_mouse.insert(0, (MOUSEMOTION, 0, self.on))
		event_mouse.insert(0, (MOUSEBUTTONDOWN, 1, self.click))
		event_mouse.insert(0, (MOUSEBUTTONUP, 1, self.click))
		# On ajoute à la liste d'affichage
		to_display.append(self.display)

	# Affichage
	def display(self, window):
		if self.state == 1 and self.image_hover != None :
			window.blit(self.image_hover, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		elif self.state == 2 and self.image_click != None :
			window.blit(self.image_click, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		else :
			window.blit(self.image, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

	# Callback du hover
	def on(self, event_type, event_code, x, y):
		print("Update : type : "+str(event_type)+"| code : "+str(event_code)+"| x : "+str(x)+"| y :"+str(y))

		if self.rect.isIn(x, y) :
			if self.state < 2 :
				self.state = 1
				if self.on_hover != None :
					self.on_hover()
			return True
		else :
			self.state = 0
			return False

	# Callback du click
	def click(self, event_type, event_code, x, y):
		print("Click : type : "+str(event_type)+"| code : "+str(event_code)+"| x : "+str(x)+"| y :"+str(y))

		if event_type == MOUSEBUTTONDOWN :
			if self.rect.isIn(x, y) :
				self.state = 2
				return True
			else :
				self.state = 0
		else :
			if self.rect.isIn(x, y) :
				self.state = 1
				if self.on_click != None :
					self.on_click()
				return True
			else :
				self.state = 0

		return False
