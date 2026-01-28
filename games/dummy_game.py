import pygame
from systems.game import Game

class DummyGame(Game):
    def init(self, screen):
        self.font = pygame.font.Font(None, 36)
    def draw(self, screen):
        text = self.font.render("Dummy Game - Press ESC to quit", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))