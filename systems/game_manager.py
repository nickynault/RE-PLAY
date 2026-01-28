import pygame

class GameManager:
    def __init__(self, launcher_class=None):
        self.active_game = None
        self.running = True
        self.in_game = False
        self.launcher_class = launcher_class
    def set_game_by_index(self, game_class, screen):
        if self.active_game:
            self.active_game.shutdown()
        self.active_game = game_class()
        self.active_game.init(screen)
        self.in_game = True
    def return_to_launcher(self, launcher_class):
        if self.active_game:
            self.active_game.shutdown()
        # Set launcher as active game
        self.active_game = launcher_class()
        self.active_game.init(pygame.display.get_surface())
        self.in_game = True
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
                    if self.in_game and self.active_game.__class__.__name__ != 'LauncherGame':
                        self.return_to_launcher(self.launcher_class)
                    else:
                        self.running = False
                elif self.in_game and self.active_game.__class__.__name__ == 'LauncherGame':
                    if event.key == pygame.K_DOWN:
                        self.active_game.selected_game = (self.active_game.selected_game + 1) % len(self.active_game.games)
                    elif event.key == pygame.K_UP:
                        self.active_game.selected_game = (self.active_game.selected_game - 1) % len(self.active_game.games)
                    elif event.key == pygame.K_RETURN:
                        if self.active_game.selected_game < len(self.active_game.game_classes) and self.active_game.game_classes[self.active_game.selected_game]:
                            self.set_game_by_index(self.active_game.game_classes[self.active_game.selected_game], self.active_game.screen)
