import pygame
from pygame.locals import *

from interface_rect import *
from interface_button import *

w_top = pygame.image.load("w_top.png").convert_alpha()
w_top_left = pygame.image.load("w_top_left.png").convert_alpha()
w_top_right = pygame.image.load("w_top_right.png").convert_alpha()
w_bottom = pygame.image.load("w_bottom.png").convert_alpha()
w_bottom_left = pygame.image.load("w_bottom_left.png").convert_alpha()
w_bottom_right = pygame.image.load("w_bottom_right.png").convert_alpha()
w_left = pygame.image.load("w_left.png").convert_alpha()
w_right = pygame.image.load("w_right.png").convert_alpha()
w_center = pygame.image.load("w_center.png").convert_alpha()

w_b1 = pygame.image.load("w_b1.png").convert_alpha()
w_b2 = pygame.image.load("w_b2.png").convert_alpha()

# Window
class vz_Window:

	def __init__(self, rect, content, name=None, visible=True):
		
		self.visible = visible
		self.rect = rect
		self.header_size = vz_Rect(0, 0, rect.w, w_top.get_height())

		self.toDisplay = pygame.Surface((rect.w, rect.h), SRCALPHA, 32).convert_alpha()

		self.state = 0; # 0 = normal // 1 = click

		self.to_display = None
		self.event_mouse = None

		# Formation de la fenêtre
		# Background
		i = 0
		y = 0
		while y <= rect.h :
			i = 0
			while i <= rect.w :
				self.toDisplay.blit(w_center, (i,y))  
				i = i + w_center.get_width()
			y = y + w_center.get_height()
		# Haut
		i = w_top_left.get_width()
		while i <= rect.w - w_top_right.get_width() :
			self.toDisplay.blit(w_top, (i, 0))
			i = i + w_top.get_width()
		# Haut droit
		self.toDisplay.blit(w_top_right, (rect.w - w_top_right.get_width(), 0))
		# Droit
		i = w_top_right.get_height()
		while i <= rect.h - w_bottom_right.get_height() :
			self.toDisplay.blit(w_right, (rect.w - w_right.get_width(), i))
			i = i + w_right.get_height()
		# Bas droit
		self.toDisplay.blit(w_bottom_right, (rect.w - w_bottom_right.get_width(), rect.h - w_bottom_right.get_height()))
		# Bas
		i = rect.w - (w_bottom_right.get_width() + w_bottom.get_width())
		while i >= w_bottom_left.get_width() :
			self.toDisplay.blit(w_bottom, (i, rect.h - w_bottom.get_height()))
			i = i - w_bottom.get_width()
		# Bas gauche
		self.toDisplay.blit(w_bottom_left, (0, rect.h - w_bottom_left.get_height()))
		# Gauche
		i = rect.h - w_bottom_left.get_height()
		while i >= w_top_left.get_height() :
			self.toDisplay.blit(w_left, (0, i))
			i = i - w_left.get_height()
		# Haut gauche
		self.toDisplay.blit(w_top_left, (0, 0))  

		# Label
		if name != None :
			smallText = pygame.font.Font('freesansbold.ttf', 18);
			label = smallText.render(name, 1, (0,0,0))
			self.toDisplay.blit(label, (5, 5))

		# Bouton
		self.button = vz_Button(vz_Rect(rect.x + rect.w - 3 - w_b1.get_width(), rect.y + 3, 0, 0) , w_b1, w_b2)

	# Initialisation
	def init(self, event_mouse, to_display):
		# Sur le mouve de la souris, pas de boutton, position, callback
		self.move_motion = (MOUSEMOTION, 0, self.move)
		event_mouse.insert(0, self.move_motion)

		self.move_down = (MOUSEBUTTONDOWN, 1, self.move)
		event_mouse.insert(0, self.move_down)

		self.move_up = (MOUSEBUTTONUP, 1, self.move)
		event_mouse.insert(0, self.move_up)
		# On ajoute à la liste d'affichage
		to_display.append(self.display)
		self.button.init(event_mouse, to_display)

		self.to_display = to_display
		self.event_mouse = event_mouse

	def isInHeader(self, x, y):
		x = x - self.rect.x
		y = y - self.rect.y

		return (x > 0 and x <= self.header_size.w) and (y > 0 and y <= self.header_size.h)

	def move(self, event_type, event_code, x, y):
		if event_type == MOUSEBUTTONDOWN :
			if self.isInHeader(x, y) :
				self.state = 1
				self._tmp_mouse_pos = (x, y)
				pygame.mouse.set_cursor(*pygame.cursors.diamond)
				self.focus()
				return True
			elif self.rect.isIn(x, y):
				self.focus()
				return True
		elif event_type == MOUSEMOTION:
			# Si on a cliqué et qu'on drag
			if self.state == 1 :
				self.rect.x = self.rect.x - (self._tmp_mouse_pos[0] - x)
				self.rect.y = self.rect.y - (self._tmp_mouse_pos[1] - y)
				self._tmp_mouse_pos = (x, y)
				self.focus()
				return True # On triche
		else:
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
			self.state = 0

		if self.rect.isIn(x, y):
			return True
		else :
			return False

	def focus(self):
		self.to_display.append(self.to_display.pop(self.to_display.index(self.display)))

		self.event_mouse.remove(self.move_motion)
		self.event_mouse.remove(self.move_down)
		self.event_mouse.remove(self.move_up)

		self.event_mouse.insert(0, self.move_motion)
		self.event_mouse.insert(0, self.move_down)
		self.event_mouse.insert(0, self.move_up)

	# Affichage
	def display(self, window):
		if self.visible :
			window.blit(self.toDisplay, (self.rect.x, self.rect.y))

