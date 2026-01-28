import pygame
import sys
from systems.game_manager import GameManager
from games.paddle_game import PaddleGame
from games.brickfall_game import BrickfallGame
from games.void_drift_game import VoidDriftGame

class LauncherGame:
    def __init__(self):
        self.selected_game = 0
        self.games = ["Paddle Duel", "Brickfall", "Void Drift"]
        self.game_classes = [PaddleGame, BrickfallGame, VoidDriftGame]  # Paddle Duel, Brickfall, Void Drift
        
    def init(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
    def update(self, dt):
        pass
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        title = self.font.render("RE:PLAY", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
        
        for i, game_name in enumerate(self.games):
            color = (255, 255, 255) if i == self.selected_game else (100, 100, 100)
            text = self.small_font.render(f"> {game_name}" if i == self.selected_game else f"  {game_name}", True, color)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 200 + i * 50))
            
        instructions = self.small_font.render("Use UP/DOWN to navigate, ENTER to select, ESC to quit", True, (200, 200, 200))
        screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, screen.get_height() - 50))
        
        pygame.display.flip()
        
    def shutdown(self):
        pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RE:PLAY")
    
    manager = GameManager(LauncherGame)
    launcher = LauncherGame()
    launcher.init(screen)
    manager.set_game_by_index(type(launcher), screen)
    
    clock = pygame.time.Clock()
    
    while manager.running:
        dt = clock.tick(60) / 1000.0
        manager.handle_events()
        manager.update(dt)
        manager.draw(screen)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
