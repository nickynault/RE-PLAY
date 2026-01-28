import pygame

class GameManager:
    def __init__(self):
        self.active_game = None
        self.running = True
    def set_game(self, game):
        if self.active_game:
            self.active_game.shutdown()
        self.active_game = game
    def update(self, dt):
        if self.active_game:
            self.active_game.update(dt)
    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.active_game:
            self.active_game.draw(screen)
        pygame.display.flip()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False