import pygame

class GameManager:
    def __init__(self):
        self.active_game = None
        self.running = True
        self.in_game = False
    def set_game_by_index(self, game_class, screen):
        if self.active_game:
            self.active_game.shutdown()
        self.active_game = game_class()
        self.active_game.init(screen)
        self.in_game = True
    def return_to_launcher(self):
        if self.active_game:
            self.active_game.shutdown()
        self.active_game = None
        self.in_game = False
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
                    if self.in_game:
                        self.return_to_launcher()
                    else:
                        self.running = False
