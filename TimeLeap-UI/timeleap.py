import pygame
import pyautogui
import sys
import os
import json

from widgets.button import Button
from widgets.label import Label 
from widgets.input_box import InputBox

pygame.init()

def scale_img(img, factor):
	size = round(img.get_width() * factor), round(img.get_height() * factor)
	return pygame.transform.scale(img, size)

def load_path(_path):
	path = _path.split("/")
	return os.path.join(*path)

def load_img(_path):
	path = load_path(_path)
	return pygame.image.load(path).convert_alpha()

def is_folder_empty(path):
	folder = os.listdir(load_path(path))

	for file in folder:
		if file.startswith("."):
			folder.remove(file)

	if folder:
		return True
	return False

def show_recordings(output_dir):
	try:
		os.startfile(output_dir + os.sep)
	except:
		os.system(f"open {output_dir}")

def take_screenshot(count):
	image = pyautogui.screenshot()
	image.save(load_path(f"screenshots/image_{count}.png"))

def clear_screenshots():
	files = os.listdir("screenshots")

	for file in files:
		file_path = load_path(f"screenshots/{file}")
		os.remove(file_path)

def render_video(fps, name, output_path):
	render_cmd = f'cd screenshots && ffmpeg -framerate {fps} -i "image_%d.png" {name}.mp4'

	os.system(render_cmd)
	os.rename(load_path(f"screenshots/{name}.mp4"), load_path(f"{output_path}/{name}.mp4"))
	clear_screenshots()

def load_settings(path):
	data = None

	with open(load_path(path), "r") as save_file:
		data = json.load(save_file)

	return data

class App:
	def __init__(self):
		self.size = (700, 700)
		self.win = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

	def setup(self):	
		self.timer = pygame.USEREVENT + 1
		self.count = 0
		self.recording = False
		self.rendering = False
		self.font = pygame.font.Font("res/RandyGGRegular.ttf", 20)
		pygame.time.set_timer(self.timer, 2000)

		if not os.path.exists("screenshots"):
			os.makedirs("screenshots")

		self.timelapse_data = load_settings("res/settings.json")

		self.images = {
			"logo": scale_img(load_img("res/logo.png"), 2),
			"icon": load_img(load_path("res/clock.png"))
		}

		pygame.display.set_icon(self.images["icon"])

		self.buttons = {
			"record": Button(150, 600, "Record", self.font, lambda: self.record()),
			"show_recordings": Button(350, 600, "Show Recordings", self.font, lambda: show_recordings(self.timelapse_data["output_dir"])),
			"save": Button(400, 400, "Save Settings", self.font, lambda: self.save_settings()) 
		}

		self.labels = {
			"name": Label(85, 200, "Name: ", (255, 255, 255), self.font),
			"output_dir": Label(40, 260, "Location: ", (255, 255, 255), self.font),
			"fps": Label(100, 330, "FPS: ", (255, 255, 255), self.font)
		}

		self.input_boxes = {
			"name": InputBox(150, 195, self.font, self.timelapse_data["name"]),
			"output_dir": InputBox(150, 260, self.font, self.timelapse_data["output_dir"]),
			"fps": InputBox(150, 330, self.font, self.timelapse_data["fps"])
		}

		return self

	def save_settings(self):
		self.check_settings()

		if not is_folder_empty("screenshots") and not self.recording:
			save_data = json.dumps(self.timelapse_data, indent=4)

			with open("res/settings.json", "w") as save_file:
				save_file.write(save_data)

	def check_settings(self):
		for data in self.timelapse_data:
			if self.timelapse_data[data] == "":
				default_settings = load_settings("res/default_settings.json")
				self.timelapse_data[data] = default_settings[data]

	def record(self):
		if self.recording == False:
			self.buttons["record"].text = "Stop"
			self.recording = True
		else:
			self.buttons["record"].text = "Record"
			self.count = 0
			self.recording = False

	def update_widgets(self, *widgets):
		for widget in widgets:
			for i in widget:
				widget[i].update()

	def render_widgets(self, *widgets):
		for widget in widgets:
			for i in widget:
				widget[i].draw(self.win)

	def draw(self):
		while True:
			self.win.fill((29, 37, 46))

			self.win.blit(self.images["logo"], (150, 0))

			self.timelapse_data = {
				"name": self.input_boxes["name"].user_text,
				"output_dir": self.input_boxes["output_dir"].user_text,
				"fps": self.input_boxes["fps"].user_text
			}

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.update_widgets(self.buttons, self.input_boxes)	
				if event.type == pygame.KEYDOWN:
					for input_box in self.input_boxes:
						self.input_boxes[input_box].get_input(event)
				if event.type == self.timer:
					if self.recording:
						self.count += 1
						take_screenshot(self.count)

			self.render_widgets(self.buttons, self.labels, self.input_boxes)

			if is_folder_empty("screenshots") and self.recording == False:
				render_video(self.timelapse_data["fps"], self.timelapse_data["name"], self.timelapse_data["output_dir"])				
			
			pygame.display.update()
			self.clock.tick(60)

if __name__ == "__main__":
	app = App()
	app.setup()
	app.draw()
