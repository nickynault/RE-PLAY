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
        self.buttons = []
        
    def init(self, screen):
        self.screen = screen
        # Use readable system fonts with arcade feel
        self.font = pygame.font.Font(None, 48)  # Large readable font
        self.small_font = pygame.font.Font(None, 32)  # Medium readable font
        self.update_buttons()
        
    def update_buttons(self):
        """Update button positions based on screen size"""
        self.buttons = []
        for i, game_name in enumerate(self.games):
            text = self.small_font.render(game_name, True, (255, 255, 255))
            x = self.screen.get_width() // 2 - text.get_width() // 2
            y = 200 + i * 50
            width = text.get_width() + 20
            height = text.get_height() + 10
            self.buttons.append({
                'rect': pygame.Rect(x - 10, y - 5, width, height),
                'text': game_name,
                'index': i,
                'text_surface': text
            })
        
        # Add Reset High Scores button
        reset_text = self.small_font.render("Reset High Scores", True, (255, 100, 100))
        reset_x = self.screen.get_width() // 2 - reset_text.get_width() // 2
        reset_y = 200 + len(self.games) * 50 + 30
        reset_width = reset_text.get_width() + 20
        reset_height = reset_text.get_height() + 10
        self.buttons.append({
            'rect': pygame.Rect(reset_x - 10, reset_y - 5, reset_width, reset_height),
            'text': "Reset High Scores",
            'action': 'reset_scores',
            'text_surface': reset_text
        })
        
    def update(self, dt):
        pass
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw title with 3D effect and border
        title_text = "RE:PLAY"
        title_main = self.font.render(title_text, True, (255, 255, 255))
        title_shadow = self.font.render(title_text, True, (0, 255, 255))  # Cyan shadow for 3D effect
        
        title_x = screen.get_width() // 2 - title_main.get_width() // 2
        title_y = 100
        
        # Draw shadow (offset for 3D effect)
        screen.blit(title_shadow, (title_x + 4, title_y + 4))
        # Draw main title
        screen.blit(title_main, (title_x, title_y))
        
        # Draw title border
        title_rect = title_main.get_rect(topleft=(title_x, title_y))
        pygame.draw.rect(screen, (0, 255, 255), title_rect, 3)  # Cyan border
        pygame.draw.rect(screen, (255, 255, 255), title_rect.inflate(8, 8), 2)  # Outer white border
        
        # Draw game buttons with hover effects
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons[:-1]:  # All buttons except reset
            is_hovered = button['rect'].collidepoint(mouse_pos)
            is_selected = button['index'] == self.selected_game
            
            # Determine if this button should be highlighted
            should_highlight = is_hovered or is_selected
            
            # Draw button background if highlighted (either by hover or keyboard selection)
            if should_highlight:
                pygame.draw.rect(screen, (50, 50, 50), button['rect'])
                pygame.draw.rect(screen, (200, 200, 200), button['rect'], 2)
            
            # Draw text
            text_x = button['rect'].x + 10
            text_y = button['rect'].y + 5
            screen.blit(button['text_surface'], (text_x, text_y))
        
        # Draw Reset High Scores button
        reset_button = self.buttons[-1]
        is_hovered = reset_button['rect'].collidepoint(mouse_pos)
        reset_color = (255, 100, 100) if is_hovered else (200, 50, 50)
        
        if is_hovered:
            pygame.draw.rect(screen, (50, 25, 25), reset_button['rect'])
            pygame.draw.rect(screen, (255, 100, 100), reset_button['rect'], 2)
        
        text_x = reset_button['rect'].x + 10
        text_y = reset_button['rect'].y + 5
        screen.blit(reset_button['text_surface'], (text_x, text_y))
            
        instructions = self.small_font.render("Use UP/DOWN to navigate, ENTER to select, ESC to quit", True, (200, 200, 200))
        screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, screen.get_height() - 50))
        
        pygame.display.flip()
        
    def shutdown(self):
        pass
        
    def reset_high_scores(self):
        """Reset all high scores to 0"""
        try:
            import json
            import os
            
            # Reset the high scores file
            high_scores_data = {
                "void_drift": 0,
                "brickfall": 0
            }
            
            with open("high_scores.json", 'w') as f:
                json.dump(high_scores_data, f, indent=2)
            
            print("High scores have been reset to 0!")
            
            # Update current high scores in memory for any active games
            if hasattr(self, 'buttons'):
                self.update_buttons()
                
        except Exception as e:
            print(f"Error resetting high scores: {e}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RE:PLAY")
    
    manager = GameManager(LauncherGame)
    launcher = LauncherGame()
    launcher.init(screen)
    manager.set_game_by_index(type(launcher), screen)
    
    clock = pygame.time.Clock()
    
    try:
        while manager.running:
            dt = clock.tick(60) / 1000.0
            if dt < 0:
                print(f"WARNING: Negative dt value: {dt}")
                dt = 0.016  # Fallback to ~60 FPS
            manager.handle_events()
            manager.update(dt)
            manager.draw(screen)
    except Exception as e:
        print(f"ERROR in main game loop: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Game shutting down...")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
