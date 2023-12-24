import pygame

class InputBox:
	def __init__(self, x, y, font, placeholder, default_color=(200, 200, 200), accent_color=(71, 112, 179), fg_color=(255, 255, 255)):
		self.x = x
		self.y = y
		self.w = 400
		self.h = 30
		self.font = font
		self.user_text = placeholder
		self.default_color = default_color
		self.accent_color = accent_color
		self.fg_color = fg_color
		self.active = False
		self.input_box = pygame.Rect(self.x, self.y, self.w, self.h)

	def update(self):
		m_pos = pygame.mouse.get_pos()
		m_clicked = pygame.mouse.get_pressed()[0]

		if self.input_box.collidepoint(m_pos) and not self.active:
			self.active = True
			self.focus()
		elif m_clicked and self.active:
			self.active = False
			self.focus()

	def focus(self):
		self.default_color = self.accent_color

		if not self.active:
			self.default_color = (200, 200, 200)

	def get_input(self, key_event):
		not_allowed = " !@#$%^&*"

		if self.active:
			if key_event.key == pygame.K_BACKSPACE:
				self.user_text = self.user_text[:-1]
			elif key_event.unicode in not_allowed:
				self.user_text = self.user_text
			else:
				self.user_text += key_event.unicode
				
	def draw(self, surf):
		x_offset = 5
		y_offset = 0
		user_font = self.font.render(self.user_text, True, self.fg_color)

		pygame.draw.rect(surf, self.default_color, self.input_box, 2, 3)
		surf.blit(user_font, (self.x + x_offset, self.y + y_offset))