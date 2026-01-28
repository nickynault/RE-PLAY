import pygame
import sys
from systems.game_manager import GameManager
from games.dummy_game import DummyGame

class MenuState:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.selected_game = 0
        self.games = ["Dummy Game", "Paddle Duel", "Brickfall", "Void Drift"]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_DOWN:
                    self.selected_game = (self.selected_game + 1) % len(self.games)
                elif event.key == pygame.K_UP:
                    self.selected_game = (self.selected_game - 1) % len(self.games)
                elif event.key == pygame.K_RETURN:
                    return self.selected_game
        return None
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        title = self.font.render("RE:PLAY", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))
        
        for i, game_name in enumerate(self.games):
            color = (255, 255, 255) if i == self.selected_game else (100, 100, 100)
            text = self.small_font.render(f"> {game_name}" if i == self.selected_game else f"  {game_name}", True, color)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200 + i * 50))
            
        instructions = self.small_font.render("Use UP/DOWN to navigate, ENTER to select, ESC to quit", True, (200, 200, 200))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, self.screen.get_height() - 50))
        
        pygame.display.flip()
        return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RE:PLAY")
    
    manager = GameManager()
    menu = MenuState(screen)
    
    clock = pygame.time.Clock()
    
    while manager.running:
        result = menu.handle_events()
        if result is False:
            manager.running = False
        elif isinstance(result, int):
            # Start selected game
            if result == 0:  # Dummy Game
                dummy_game = DummyGame()
                dummy_game.init(screen)
                manager.set_game(dummy_game)
                # Run game loop
                while manager.running and manager.active_game:
                    dt = clock.tick(60) / 1000.0
                    manager.handle_events()
                    manager.update(dt)
                    manager.draw(screen)
                # Return to menu
                manager.active_game = None
                continue
        
        menu.draw()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()