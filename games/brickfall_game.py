import pygame
import random
from systems.game import Game
import json
import os

class HighScoreManager:
    """Manages persistent high scores for games"""
    
    def __init__(self, save_file="high_scores.json"):
        self.save_file = save_file
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    # Ensure all expected games exist with default 0 values
                    if "void_drift" not in data:
                        data["void_drift"] = 0
                    if "brickfall" not in data:
                        data["brickfall"] = 0
                    return data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        
        # Return default scores if file doesn't exist or is corrupted
        return {
            "void_drift": 0,
            "brickfall": 0
        }
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def get_high_score(self, game_name):
        """Get high score for a specific game"""
        return self.scores.get(game_name, 0)
    
    def update_high_score(self, game_name, new_score):
        """Update high score for a specific game"""
        current_high = self.get_high_score(game_name)
        if new_score > current_high:
            self.scores[game_name] = new_score
            self.save_scores()
            return True
        return False

class BrickfallGame(Game):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.paddle_width = 100
        self.paddle_height = 15
        self.ball_size = 15
        self.paddle_speed = 8
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.block_width = 75
        self.block_height = 25
        self.block_gap = 5
        
    def init(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        
        # Initialize high score manager
        self.high_score_manager = HighScoreManager()
        self.current_high_score = self.high_score_manager.get_high_score('brickfall')
        
        self.reset_game()
        
    def reset_game(self):
        # Game state
        self.score = 0
        self.lives = 3
        self.game_won = False
        self.win_timer = 0
        
        # Paddle
        self.paddle = pygame.Rect(self.width // 2 - self.paddle_width // 2, self.height - 50, self.paddle_width, self.paddle_height)
        
        # Ball
        self.ball = pygame.Rect(self.width // 2 - self.ball_size // 2, self.height // 2 - self.ball_size // 2, self.ball_size, self.ball_size)
        
        # Blocks (3 rows, 5 columns)
        # Replace block setup in reset_game()
        self.blocks = []
        cols = self.width // (self.block_width + self.block_gap)
        for row in range(3):
            for col in range(cols):
                x = col * (self.block_width + self.block_gap)
                y = 50 + row * (self.block_height + self.block_gap)
                self.blocks.append(pygame.Rect(x, y, self.block_width, self.block_height))

                
    def update(self, dt):
        if self.game_won:
            self.win_timer += dt
            if self.win_timer > 2.0:
                self.reset_game()
            return
            
        keys = pygame.key.get_pressed()
        
        # Paddle movement (Left/Right arrows)
        if keys[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.x -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle.right < self.width:
            self.paddle.x += self.paddle_speed
        
        # Ball movement
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        
        # Wall collisions
        if self.ball.left <= 0 or self.ball.right >= self.width:
            self.ball_speed_x *= -1
        if self.ball.top <= 0:
            self.ball_speed_y *= -1
            
        # Paddle collision
        if self.ball.colliderect(self.paddle) and self.ball_speed_y > 0:
            self.ball_speed_y *= -1
            self.ball.top = self.paddle.top - self.ball.height  # push ball above paddle
            # Adjust x speed based on where ball hits paddle
            paddle_center = self.paddle.centerx
            ball_center = self.ball.centerx
            hit_position = (ball_center - paddle_center) / (self.paddle_width / 2)
            self.ball_speed_x = hit_position * 6  # Vary horizontal speed
            self.ball_speed_x += random.uniform(-0.5, 0.5)  # Add slight randomness
        
        # Block collisions
        for block in self.blocks[:]:
            if self.ball.colliderect(block):
                self.blocks.remove(block)
                # Determine which side we hit
                if abs(self.ball.bottom - block.top) < 10 and self.ball_speed_y > 0:
                    self.ball_speed_y *= -1
                    self.ball.bottom = block.top
                elif abs(self.ball.top - block.bottom) < 10 and self.ball_speed_y < 0:
                    self.ball_speed_y *= -1
                    self.ball.top = block.bottom
                else:
                    self.ball_speed_x *= -1
                self.score += 1
                break
                
        # Check win condition
        if len(self.blocks) == 0:
            self.game_won = True
            
        # Reset ball if it goes off bottom
        if self.ball.bottom >= self.height:
            self.lives -= 1
            if self.lives <= 0:
                # Update persistent high score when game is over
                self.high_score_manager.update_high_score('brickfall', self.score)
                self.current_high_score = self.high_score_manager.get_high_score('brickfall')
                self.reset_game()
            else:
                self.ball.center = (self.width // 2, self.height // 2)
                self.ball_speed_x = 5
                self.ball_speed_y = 5
            
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        if self.game_won:
            win_text = self.font.render("You Win!", True, (255, 255, 255))
            screen.blit(win_text, (self.width // 2 - win_text.get_width() // 2, self.height // 2))
        else:
            # Draw paddle and ball
            pygame.draw.rect(screen, (255, 255, 255), self.paddle)
            pygame.draw.ellipse(screen, (255, 255, 255), self.ball)
            
            # Draw blocks
            for block in self.blocks:
                pygame.draw.rect(screen, (0, 255, 0), block)
            
            # Draw UI
            score_text = self.font.render(f"Score: {self.score}  Lives: {self.lives}", True, (255, 255, 255))
            high_score_text = self.font.render(f"High Score: {self.current_high_score}", True, (255, 215, 0))  # Gold color
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 10))
            screen.blit(high_score_text, (self.width // 2 - high_score_text.get_width() // 2, 60))
            
        pygame.display.flip()
        
    def shutdown(self):
        pass