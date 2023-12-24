import pygame

class Button:
	def __init__(self, x, y, text, font, func, color=(71, 112, 179)):
		self.x = x
		self.y = y
		self.text = text
		self.font = font
		self.border_width = 2
		self.color = color
		self.active = False
		self.button = pygame.Rect(self.x, self.y, 0, 0)
		self.func = func

	def update(self):
		m_pos = pygame.mouse.get_pos()

		if self.button.collidepoint(m_pos):
			self.func()

	def focus(self):
		m_pos = pygame.mouse.get_pos()


		if self.button.collidepoint(m_pos):
			self.active = True
			self.border_width = 0
		else:
			self.active = False
			self.border_width = 2

	def draw(self, surf):
		self.focus()
		x_offset = 15
		y_offset = 10
		btn_txt = self.font.render(self.text, True, (255, 255, 255))
		self.button.w, self.button.h = btn_txt.get_width() + 30, btn_txt.get_height() + 20
		
		pygame.draw.rect(surf, self.color, self.button, self.border_width, 10)
		surf.blit(btn_txt, (self.x + x_offset, self.y + y_offset))