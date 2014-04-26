import pygame
from pygame.locals import *
from cap_rect import *
from card_type import *

#sound
sound_pay = pygame.mixer.Sound("soundAndMusic/money.wav")
sound_get_money = pygame.mixer.Sound("soundAndMusic/caisse_enregistr.wav")

# Graphique
card_bg = pygame.image.load("card/card_bg.png").convert_alpha()
card_fg = pygame.image.load("card/card_fg.png").convert_alpha()
mincard_bg = pygame.image.load("card/mincard_bg.png").convert_alpha()
mincard_fg = pygame.image.load("card/mincard_fg.png").convert_alpha()
mincard_bg_selected = pygame.image.load("card/mincard_bg_selected.png").convert_alpha()
mincard_bg_hovered = pygame.image.load("card/mincard_bg_hover.png").convert_alpha()
back_bg = pygame.image.load("card/back_bg.png").convert_alpha()
back_bg_hover = pygame.image.load("card/back_bg_hover.png").convert_alpha()
msg_bg = pygame.image.load("card/msg_bg.png").convert_alpha()
deck_bg = pygame.image.load("card/deck.png").convert_alpha()
discard_bg = pygame.image.load("card/discard.png").convert_alpha()
modal_bg = pygame.image.load("modal_bg.png").convert_alpha()
modal_bt1 = pygame.image.load("oui.png").convert_alpha()
modal_bt2 = pygame.image.load("non.png").convert_alpha()
depos_bilan_but = pygame.image.load("card/bilan.png").convert_alpha()
pass_turn_but = pygame.image.load("card/fin_tour.png").convert_alpha()
opa_but = pygame.image.load("card/opa.png").convert_alpha()
pass_turn_but_hovered = pygame.image.load("card/fin_tour_ho.png").convert_alpha()
opa_but_hovered = pygame.image.load("card/opa_ho.png").convert_alpha()
modal_bt1_hovered = pygame.image.load("oui_ho.png").convert_alpha()
modal_bt2_hovered = pygame.image.load("non_ho.png").convert_alpha()

# Fonts
modal_font = pygame.font.Font('card/BebasNeue.otf', 30);
player_name_font = pygame.font.Font('card/BebasNeue.otf', 25);
card_title_font = pygame.font.Font('card/BebasNeue.otf', 22);
card_mintitle_font = pygame.font.Font('card/BebasNeue.otf', 14);
card_type_font = pygame.font.Font('card/BebasNeue.otf', 12);
card_content_font = pygame.font.Font('card/SugarcubesBold.ttf', 13);
card_medium_font = pygame.font.Font('card/SugarcubesBold.ttf', 11);
card_small_font = pygame.font.Font('card/SugarcubesBold.ttf', 10);

black = (0,0,0)
grey  = (160,160,160)
white = (255,255,255)
green = (14,139,0)
red   = (166,0,0)

def cap_Graph_print(str, font, surface, line_height, color=(0,0,0), startx=0, starty=0):
	while "\n" in str :
		pos = str.find("\n")
		surface.blit(font.render(str[0:pos], 1, color), (startx, starty))
		starty += line_height
		str = str[pos+1:]
	surface.blit(font.render(str, 1, color), (startx, starty))

def cap_blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

# Object graphique
class cap_Graph_object:
	# Constructeur
	def __init__(self, rect, rect_click):
		self.rect = rect                                                                               # Taille de l'image & position
		self.rect_click = rect_click                                                                   # Zone de detection du clique (None pour aucune)
		self.visible = False                                                                           # Visibilité de l'image
		self.inAnim = False
		self.to_display = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()     # Calque de l'image
		self.opacity = 255

	# Initialisation
	def init(self, event_mouse, event_key, display_list):
		# On ajoute à la liste d'affichage
		display_list.append(self.display)
		self.display_list = display_list

	# Update le visuel
	def update(self):
		pass

	def erase(self):
		self.to_display.fill(0)

	# Rend visible ou invisible l'image
	def visibility(self, visibility):
		self.visible = visibility

	# Animation
	def animate(self, x, y, timer=2000, opacity=0):
		self.anim_timer_start = pygame.time.get_ticks()
		self.anim_start = cap_Rect(self.rect.x, self.rect.y, 0, 0)
		self.anim_end = cap_Rect(x, y, 0, 0)
		self.anim_timer = timer
		self.inAnim = True
		self.anim_opacity = opacity

		if opacity == -1 :
			self.opacity = 0
		else :
			self.opacity = 255

	# Callback d'affichage
	def display(self, window):
		if self.inAnim :
			when = (pygame.time.get_ticks() - self.anim_timer_start) / self.anim_timer

			if(when < 1) :
				self.rect.x = ((self.anim_end.x - self.anim_start.x) * when) + self.anim_start.x
				self.rect.y = ((self.anim_end.y - self.anim_start.y) * when) + self.anim_start.y
				if self.anim_opacity == -1 :
					self.opacity = 255 - (255 * when)
				elif self.anim_opacity == 1 :
					self.opacity = 255 * when
			else :
				self.rect.x = self.anim_end.x
				self.rect.y = self.anim_end.y
				if self.anim_opacity == -1 :
					self.opacity = 0
					self.visible = False
				elif self.anim_opacity == 1 :
					self.opacity = 255
				self.inAnim = False

		if self.visible :
			cap_blit_alpha(window, self.to_display, (self.rect.x, self.rect.y), self.opacity)

# Fenêtre modale
class cap_graph_Modal(cap_Graph_object):
	def __init__(self):
		cap_Graph_object.__init__(self, cap_Rect(0,0,1280,800), cap_Rect(0,0,1280,800))
		self.bg_image = modal_bg

		self.msg = ""
		self.onYes = None
		self.onYesRect = cap_Rect(410, 545, 62, 44)
		self.onNo = None
		self.onNoRect = cap_Rect(785, 545, 62, 44)
		self.ignoreNext = False
		self.hovered = 0

		self.bg = pygame.Surface((1280, 800), SRCALPHA, 32).convert_alpha()
		self.bg.blit(modal_bg, (0, 0))

	# Initialisation
	def init(self, event_mouse, event_key, display_list):
		# On ajoute à la liste d'affichage
		display_list.append(self.display)
		self.display_list = display_list
		# Button
		event_mouse.append((MOUSEBUTTONUP, 1, self.buttons_check))
		event_mouse.append((MOUSEMOTION, 0, self.buttons_hover))
		event_key.append((KEYDOWN, K_RETURN, self.buttons_key))

	def set_msg(self, msg, onYes, onNo, ignoreNext=False):
	
		self.onYes = onYes
		self.onNo = onNo
		self.msg = msg
		self.visible = True
		self.ignoreNext = ignoreNext

		self.update()

	def update(self):

		self.erase()

		self.to_display.blit(self.bg, (0, 0))
		cap_Graph_print(self.msg, modal_font, self.to_display, 28, black, 219, 181)

	def buttons_hover(self, event_type, event_code, x, y):
		# Oui
		if self.onYesRect.isIn(x, y):
			self.hovered = 1
		# Non
		elif self.onNoRect.isIn(x, y):
			self.hovered = 2
		else :
			self.hovered = 0

	def buttons_check(self, event_type, event_code, x, y):
		# Oui
		if self.onYesRect.isIn(x, y):
			if self.onYes != None : self.onYes()
			if not self.ignoreNext :
				self.visible = False
		# Non
		elif self.onNoRect.isIn(x, y):
			if self.onNo != None : self.onNo()
			if not self.ignoreNext :
				self.visible = False
		self.ignoreNext = False

	def buttons_key(self, event_type, event_code, x, y):
		if event_code == K_ESCAPE :
			if self.onNo != None : self.onNo()
			if not self.ignoreNext :
				self.visible = False
		elif event_code == K_RETURN :
			if self.onYes != None : self.onYes()
			if not self.ignoreNext :
				self.visible = False
		self.ignoreNext = False

	def display(self, window):
		cap_Graph_object.display(self, window)

		if self.visible:
			if self.hovered == 1 :
				window.blit(modal_bt1_hovered, (self.onYesRect.x, self.onYesRect.y))
			else :
				window.blit(modal_bt1, (self.onYesRect.x, self.onYesRect.y))

			if self.hovered == 2 :
				window.blit(modal_bt2_hovered, (self.onNoRect.x, self.onNoRect.y))
			else :
				window.blit(modal_bt2, (self.onNoRect.x, self.onNoRect.y))

class cap_graph_Button(cap_Graph_object):
	def __init__(self, rect, rect_click, bg_image, bg_image_hover, bg_image_click, callback):
		cap_Graph_object.__init__(self, rect, rect_click)
		self.bg_image = bg_image
		self.bg_image_click = bg_image_click
		self.bg_image_hover = bg_image_hover
		self.callback = callback
		self.state = 0 # 0 = rien, 1 = hover, 2 = click

	def onClick(self, event_type, event_code, x, y):
		if self.rect_click.isIn(x-self.rect.x, y-self.rect.y):
			self.state = 2
			self.update()
		else:
			self.state = 0
			self.update()

	def onHover(self, event_type, event_code, x, y):
		if self.rect_click.isIn(x-self.rect.x, y-self.rect.y):
			self.state = 1
			self.update()
		else:
			self.state = 0
			self.update()

	def update(self):
		self.erase()
		if self.state == 0:
			self.to_display.blit(self.bg_image, (0, 0))
		elif self.state == 1:
			self.to_display.blit(self.bg_image_hover, (0, 0))
		elif self.state == 2:
			self.to_display.blit(self.bg_image_click, (0, 0))

	def init(self, event_mouse, event_key, display_list):
		cap_Graph_object.init(self, event_mouse, event_key, display_list)
		event_mouse.insert(0, (MOUSEMOTION, 0, self.onHover))
		event_mouse.insert(0, (MOUSEBUTTONDOWN, 1, self.onClick))
		event_mouse.insert(0, (MOUSEBUTTONUP, 1, self.onAction))
		self.update()

	def onAction(self, event_type, event_code, x, y):
		if self.rect_click.isIn(x-self.rect.x, y-self.rect.y):
			self.callback()

# Pop-up & log
class cap_Graph_msg(cap_Graph_object):
	"""docstring for cap_Graph_mincard"""
	def __init__(self):
		cap_Graph_object.__init__(self, cap_Rect(0, 0, 1280, 800), cap_Rect(0, 0, 0, 0))

		self.log_zone = pygame.Surface((315, 146), SRCALPHA, 32).convert_alpha()
		self.msg_zone = pygame.Surface((600, 200), SRCALPHA, 32).convert_alpha()

		# Update des infos
		self.update()

	# Affiche un message
	def msg(self, msg):
		print("Message : "+msg)

		# On remet à zéro
		self.msg_zone.fill(0)
		self.visible = True
		self.opacity = 255
		self.msg_zone.blit(msg_bg, (0, 0))

		# On écrit le message
		self.msg_zone.blit(player_name_font.render(msg, 1, black), (68, 52))
		self.to_display.blit(self.msg_zone, (0,0))

		# On fait disparaitre
		self.animate(0, 0, 6000, -1)

	# Ajoute une entrée au log
	def log(self, msg, color=black):
		print("Log : "+msg)

		# On blit en décalant d'une ligne
		tmp = pygame.Surface((315, 146), SRCALPHA, 32).convert_alpha()
		tmp.blit(self.log_zone, (0, 13))
		self.log_zone = tmp

		# On écrit le message
		self.log_zone.blit(card_content_font.render(msg, 1, color), (2, 0))

	# Affichage modifié
	def display(self, window):
		# On appel l'ancien pour l'animation
		cap_Graph_object.display(self, window)

		# On affiche notre log
		window.blit(self.log_zone, (9, 370))

# Info joueur
class cap_Graph_playerinfo(cap_Graph_object):
	"""docstring for cap_Graph_mincard"""
	def __init__(self, pos, player):
		cap_Graph_object.__init__(self, cap_Rect(pos.x, pos.y, 220, 120), cap_Rect(0, 0, 220, 120))

		self.player = player

		# On commence par le fond (qui ne change pas)
		self.anim = cap_Graph_object(cap_Rect(141, 574, 150, 25), cap_Rect(0, 0, 150, 25))
		self.bg = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()
		self.bg.blit(player_name_font.render(self.player.name, 1, black), (0, 0))

		# Update des infos
		self.update()

	# Animation cool
	def changeMoney(self, howMuch, otherPlayer=False):
		self.anim.to_display.fill(0)

		if not otherPlayer:
			self.anim.rect.x = 141
			if howMuch >= 0:
				sound_get_money.play()
				self.anim.to_display.blit(card_title_font.render( '+%.2f$' % howMuch, 1, green), (0, 0))
				self.anim.rect.y = 560
				self.anim.animate(141, 584, 2000, -1)
			else :
				sound_pay.play()
				self.anim.to_display.blit(card_title_font.render( '%.2f$' % howMuch, 1, red), (0, 0))
				self.anim.rect.y = 574
				self.anim.animate(141, 435, 2000, -1)
		else:
			self.anim.rect.x = 1134
			if howMuch >= 0:
				sound_get_money.play()
				self.anim.to_display.blit(card_title_font.render( '+%.2f$' % howMuch, 1, green), (0, 0))
				self.anim.rect.y = 90
				self.anim.animate(1134, 136, 2000, -1)
			else :
				sound_pay.play()
				self.anim.to_display.blit(card_title_font.render( '%.2f$' % howMuch, 1, red), (0, 0))
				self.anim.rect.y = 136
				self.anim.animate(1134, 80, 2000, -1)

		self.anim.visibility(True)

	# Update le visuel de la carte pour prendre en compte les changements
	def update(self):
		self.erase()
		self.to_display.blit(self.bg, (0, 0))
		self.to_display.blit(card_title_font.render( "  Capital         : "+('%.2f' % self.player.money)+"$", 1, green), (5, 23))
		total = self.player.estimateNextIncome()
		if total >= 0 :
			self.to_display.blit(card_title_font.render( "  Prévisions : "+('%.2f' % total)+"$", 1, green), (5, 41))
		else :
			self.to_display.blit(card_title_font.render( "  Prévisions : "+('%.2f' % total)+"$", 1, red), (5, 41))


	def init(self, event_mouse, event_key, display_list):
		display_list.append(self.display)
		self.display_list = display_list
		self.anim.init(event_mouse, event_key, display_list)

# Pioche
class cap_Graph_deck_base(cap_Graph_object):

	def __init__(self, deck, bg, pos):
		cap_Graph_object.__init__(self, pos, cap_Rect(11, 9, 178, 125))

		self.deck = deck
		self.hovered = False

		# On commence par le fond (qui ne change pas)
		self.card_bg = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()
		self.card_bg.blit(bg, (0, 0))

		# Update des infos
		self.update()

	# Update le visuel de la carte pour prendre en compte les changements
	def update(self):

		self.to_display.fill(0)

		if self.hovered :
			self.to_display.blit(back_bg_hover, (0, 0))
		
		self.to_display.blit(self.card_bg, (0, 0))

		# Affichage du nombre

	# Initialisation
	def init(self, event_mouse, event_key, display_list):
		# On ajoute à la liste d'affichage
		event_mouse.insert(0, (MOUSEMOTION, 0, self.hover))
		event_mouse.insert(0, (MOUSEBUTTONUP, 1, self.click))

		display_list.append(self.display)
		self.display_list = display_list

	def hover(self, event_type, event_code, x, y):
		if self.rect_click.isIn(x - self.rect.x, y - self.rect.y):
			if not self.hovered :
				self.hovered = True
				self.update()
		elif self.hovered :
				self.hovered = False
				self.update()

	def click(self, event_type, event_code, x, y):
		pass


class cap_Graph_deck(cap_Graph_deck_base):

	def __init__(self, deck):
		cap_Graph_deck_base.__init__(self, deck, deck_bg, cap_Rect(50, 188, 200, 143))


class cap_Graph_discard(cap_Graph_deck_base):

	def __init__(self, deck):
		cap_Graph_deck_base.__init__(self, deck, discard_bg, cap_Rect(1037, 552, 200, 143))


# Miniature de carte
class cap_Graph_mincard(cap_Graph_object):
	"""docstring for cap_Graph_mincard"""
	def __init__(self, bg_img_link, card_obj):
		cap_Graph_object.__init__(self, cap_Rect(100, 250, 145, 60), cap_Rect(10, 7, 127, 46))

		self.card_obj = card_obj
		self.selected = False
		self.hovered = False
		
		# On commence par construire le fond de la carte (celui-ci ne changera pas en cours de jeu)
		self.card_bg = pygame.Surface((self.rect.w, self.rect.h), SRCALPHA, 32).convert_alpha()
		self.card_bg.blit(mincard_bg, (0, 0))
		if bg_img_link != None : # Si on a une image de background
			self.bg_img = pygame.image.load(bg_img_link).convert_alpha()
			self.card_bg.blit(self.bg_img, (self.rect_click.x, self.rect_click.y), (0, 0, self.rect_click.w, self.rect_click.h))
		else :
			self.bg_img = None
		self.card_bg.blit(mincard_fg, (0, 0))

		# On ajoute le nom, car lui aussi ne change pas
		if self.card_obj.cardType == Type.ACTION :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + ActionType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (11, 7))
		elif self.card_obj.cardType == Type.CARD :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + CardType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (11, 7))
		

		if card_obj.colorname == "white" :
			self.card_bg.blit(card_mintitle_font.render(card_obj.name, 1, white), (15, 20))
		else :
			self.card_bg.blit(card_mintitle_font.render(card_obj.name, 1, black), (15, 20))

		# Update des infos
		self.update()

	# Update le visuel de la carte pour prendre en compte les changements
	def update(self):

		self.to_display.fill(0)

		if self.selected :
			self.to_display.blit(mincard_bg_selected, (0, 0))

		if self.hovered :
			self.to_display.blit(mincard_bg_hovered, (0, 0))

		self.to_display.blit(self.card_bg, (0, 0))

		if self.card_obj.cardType == Type.ACTION :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.life)), 1, white), (125, 40))
			self.to_display.blit(card_content_font.render("Cible : "+ CardType.get_string(self.card_obj.affectedType), 1, black), (14, 34))

	
		elif self.card_obj.cardType == Type.CARD :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.computedCard.life)), 1, white), (125, 40))

			total = self.card_obj.computedCard.incomePerTurn - self.card_obj.computedCard.costPerTurn

			if total > 0 :
				s = "+" + ('%.2f' % total) + "$ (" + ('%.2f' % self.card_obj.computedCard.costPerTurnModifier) + "%)"
				self.to_display.blit(card_mintitle_font.render(s, 1, green), (14, 34))
			else :
				s = ('%.2f' % total) + "$ (" + ('%.2f' % self.card_obj.computedCard.costPerTurnModifier) + "%)"
				self.to_display.blit(card_mintitle_font.render(s, 1, red), (14, 34))

	# Initialisation
	def init(self, event_mouse, event_key, display_list):
		# On ajoute à la liste d'affichage
		event_mouse.insert(0, (MOUSEMOTION, 0, self.hover))
		event_mouse.insert(0, (MOUSEBUTTONUP, 1, self.click))

		display_list.append(self.display)
		self.display_list = display_list

	def hover(self, event_type, event_code, x, y):
		if self.visible :
			if self.rect_click.isIn(x - self.rect.x, y - self.rect.y):
				self.card_obj.grap_card.visibility(True)
				if not self.hovered :
					self.hovered = True
					self.update()
			elif self.card_obj.grap_card.visible :
				self.card_obj.grap_card.visibility(False)
				if self.hovered :
					self.hovered = False
					self.update()
		else :
			self.card_obj.grap_card.visibility(False)


	def click(self, event_type, event_code, x, y):
		if self.visible :
			if self.rect_click.isIn(x - self.rect.x, y - self.rect.y) :
				if not self.selected:
					self.selected = True
					self.update()
				else :
					self.selected = False
					self.update()
			elif self.selected :
				self.selected = False
				self.update()

# Carte du jeu
class cap_Graph_card(cap_Graph_object):
	# Constructeur
	def __init__(self, bg_img_link, card_obj):
		cap_Graph_object.__init__(self, cap_Rect(1030, 244, 212, 291), cap_Rect(12, 12,188, 267))

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

		# On ajoute le nom/description, car lui aussi ne change pas
		if self.card_obj.cardType == Type.ACTION :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + ActionType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (14, 12))
		elif self.card_obj.cardType == Type.CARD :
			self.card_bg.blit(card_type_font.render(Type.get_string(self.card_obj.cardType) + " (" + CardType.get_string(self.card_obj.type) + ")", 1, (255, 255, 255)), (14, 12))
		
		if card_obj.colorname == "white" :
			self.card_bg.blit(card_title_font.render(card_obj.name, 1, white), (20, 25))
		else :
			self.card_bg.blit(card_title_font.render(card_obj.name, 1, black), (20, 25))

		cap_Graph_print(card_obj.desc, card_small_font, self.card_bg, 10, black, 38, 53)

		# Update des infos
		self.update()

	# Update le visuel de la carte pour prendre en compte les changements
	def update(self):
		self.to_display.blit(self.card_bg, (0, 0))


		if self.card_obj.cardType == Type.ACTION :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.life)), 1, white), (186, 265))
			self.to_display.blit(card_content_font.render("Cible : "+ CardType.get_string(self.card_obj.affectedType), 1, black), (34, 140))

			self.to_display.blit(card_medium_font.render("Coût pose    :", 1, black), (34, 175))
			self.to_display.blit(card_medium_font.render('%.2f$' % self.card_obj.deploymentCost, 1, red), (114, 175))
	
		elif self.card_obj.cardType == Type.CARD :

			self.to_display.blit(card_type_font.render(str(int(self.card_obj.computedCard.life)), 1, white), (186, 265))

			if self.card_obj.type == CardType.CONTRACT :

				self.to_display.blit(card_content_font.render("Cible : "+ CardType.get_string(self.card_obj.affectedType), 1, black), (34, 140))

				s = "-" + ('%.2f' % self.card_obj.computedCard.costPerTurn)
				s += "$ (" + ('%.2f' % self.card_obj.computedCard.costPerTurnModifier) + "%)"
				self.to_display.blit(card_title_font.render(s, 1, red), (34, 159))

			else :
				s = "+" + ('%.2f' % self.card_obj.computedCard.incomePerTurn)
				s += "$ (" + ('%.2f' % self.card_obj.computedCard.incomePerTurnModifier) + "%)"
				self.to_display.blit(card_title_font.render(s, 1, green), (34, 135))

				s = "-" + ('%.2f' % self.card_obj.computedCard.costPerTurn)
				s += "$ (" + ('%.2f' % self.card_obj.computedCard.costPerTurnModifier) + "%)"
				self.to_display.blit(card_title_font.render(s, 1, red), (34, 157))

			self.to_display.blit(card_medium_font.render("Coût pose    :", 1, black), (34, 181))
			self.to_display.blit(card_medium_font.render('%.2f$' % self.card_obj.computedCard.deploymentCost, 1, red), (114, 181))
			self.to_display.blit(card_medium_font.render("Coût retrait :", 1, black), (34, 194))
			self.to_display.blit(card_medium_font.render('%.2f$' % self.card_obj.computedCard.discardCost, 1, red), (114, 194))

		i = 214
		for effect in self.card_obj.effects:
			self.to_display.blit(card_medium_font.render( AffectableValue.get_string(effect.affectedValue) + " :", 1, black), (34, i))
			i += 11
			s = ""
			if effect.value > 0 :
				s = s + "+"
			s = s + ('%.2f' % effect.value)
			if effect.modifierType == ModifierType.PERCENT:
				s = s + " %"
			if effect.modifierType > 0:
				self.to_display.blit(card_medium_font.render(s, 1, green), (34, i))
			else :
				self.to_display.blit(card_medium_font.render(s, 1, red), (34, i))
			i += 11

