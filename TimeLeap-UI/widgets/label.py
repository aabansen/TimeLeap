import pygame

class Label:
	def __init__(self, x, y, text, color, font):
		self.x = x 
		self.y = y
		self.text = font.render(text, True, color)	

	def draw(self, surf):
		surf.blit(self.text, (self.x, self.y))