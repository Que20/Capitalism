import pygame
from pygame.locals import *

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