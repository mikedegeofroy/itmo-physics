import pygame
import pygame_gui

WIDTH, HEIGHT = 1000, 600

class Gui :
  def __init__(self):
    self.font = pygame.font.Font(None, 24)
    self.gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    self.last_input = 0

  def draw_input(self, text):
    box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((10, self.last_input + 10), (100, 30)),
        manager=self.gui_manager
    )
    self.last_input += 40
    box.set_text(text)
    return box
  
  def draw_button(self, text):
    box = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 170), (100, 30)),
        text=text,
        manager=self.gui_manager
      )
    self.last_input += 40
    return box
  
  def render_text(self, text):
    return self.font.render(text, True, (255, 255, 255))