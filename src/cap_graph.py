import pygame
from pygame.locals import *
from cap_rect import *
from card_type import *

# Graphique
card_bg = pygame.image.load("card/card_bg.png").convert_alpha()
card_fg = pygame.image.load("card/card_fg.png").convert_alpha()
card_title_font = pygame.font.Font('card/BebasNeue.otf', 22);
card_type_font = pygame.font.Font('card/BebasNeue.otf', 12);
card_content_font = pygame.font.Font('card/SugarcubesRegular.ttf', 13);
card_medium_font = pygame.font.Font('card/SugarcubesRegular.ttf', 11);
card_small_font = pygame.font.Font('card/SugarcubesRegular.ttf', 10);

black = (0,0,0)
white = (255,255,255)
green = (14,139,0)
red   = (166,0,0)

def cap_Grap_print(str, font, surface, line_height, color=(0,0,0), startx=0, starty=0):
	while "\n" in str :
		pos = str.find("\n")
		surface.blit(font.render(str[0:pos], 1, color), (startx, starty))
		starty += line_height
		str = str[pos+1:]
	surface.blit(font.render(str, 1, color), (startx, starty))

# Object graphique
class cap_Grap_object:
	# Constructeur
	def __init__(self, rect, rect_click):
		self.rect = rect                                                                               # Taille de l'image & position
		self.rect_click = rect_click                                                                   # Zone de detection du clique (None pour aucune)
		self.visible = False                                                                           # Visibilité de l'image
		self.to_display = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()     # Calque de l'image

	# Initialisation
	def init(self, event_mouse, event_key, display_list):
		# On ajoute à la liste d'affichage
		display_list.append(self.display)
		self.display_list = display_list

	# Update le visuel
	def update(self):
		pass
		
	# Rend visible ou invisible l'image
	def visibility(self, visibility):
		self.visible = visibility

	# Callback d'affichage
	def display(self, window):
		if self.visible :
			window.blit(self.to_display, (self.rect.x, self.rect.y))

# Carte du jeu
class cap_Graph_card(cap_Grap_object):
	# Constructeur
	def __init__(self, bg_img_link, card_obj):
		cap_Grap_object.__init__(self, cap_Rect(0, 0, 212, 291), cap_Rect(12, 12,188, 267))

		self.card_obj = card_obj
		
		# On commence par construire le fond de la carte (celui-ci ne changera pas en cours de jeu)
		self.card_bg = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()
		self.card_bg.blit(card_bg, (0, 0))
		if bg_img_link != None : # Si on a une image de background
			self.bg_img = pygame.image.load(bg_img_link).convert_alpha()
			self.card_bg.blit(self.bg_img, (self.rect_click.x, self.rect_click.y), (0, 0, self.rect_click.w, self.rect_click.h))
		else :
			self.bg_img = None
		self.card_bg.blit(card_fg, (0, 0))

		# On ajoute le nom, car lui aussi ne change pas
		if self.card_obj.cardType == Type.ACTION :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + ActionType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (14, 12))
		elif self.card_obj.cardType == Type.CARD :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + CardType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (14, 12))
		self.card_bg.blit(card_title_font.render(card_obj.name, 1, (0,0,0)), (20, 25))
		cap_Grap_print(card_obj.desc, card_small_font, self.card_bg, 10, (0,0,0), 38, 53)

		# Update des infos
		self.update()

	# Update le visuel de la carte pour prendre en compte les changements
	def update(self):
		self.to_display.blit(self.card_bg, (0, 0))


		if self.card_obj.cardType == Type.ACTION :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.life)), 1, white), (186, 265))
			self.to_display.blit(card_content_font.render("Cible : "+ CardType.get_string(self.card_obj.affectedType), 1, black), (34, 165))

	
		elif self.card_obj.cardType == Type.CARD :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.computedCard.life)), 1, white), (186, 265))

			s = "+" + str(self.card_obj.computedCard.incomePerTurn)
			s += "$ (" + str(self.card_obj.computedCard.costPerTurnModifier) + "%)"
			self.to_display.blit(card_title_font.render(s, 1, green), (34, 135))

			s = "" + str(self.card_obj.computedCard.costPerTurn)
			s += "$ (" + str(self.card_obj.computedCard.costPerTurnModifier) + "%)"
			self.to_display.blit(card_title_font.render(s, 1, red), (34, 159))

		i = 192
		for effect in self.card_obj.effects:
			self.to_display.blit(card_medium_font.render( AffectableValue.get_string(effect.affectedValue) + " :", 1, black), (34, i))
			i += 11
			s = ""
			if effect.value > 0 :
				s = s + "+"
			s = s + str(effect.value)
			if effect.modifierType == ModifierType.PERCENT:
				s = s + " %"
			if effect.modifierType > 0:
				self.to_display.blit(card_medium_font.render(s, 1, green), (34, i))
			else :
				self.to_display.blit(card_medium_font.render(s, 1, red), (34, i))
			i += 11

