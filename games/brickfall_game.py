import pygame
from systems.game import Game

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
        self.reset_game()
        
    def reset_game(self):
        # Paddle
        self.paddle = pygame.Rect(self.width // 2 - self.paddle_width // 2, self.height - 50, self.paddle_width, self.paddle_height)
        
        # Ball
        self.ball = pygame.Rect(self.width // 2 - self.ball_size // 2, self.height // 2 - self.ball_size // 2, self.ball_size, self.ball_size)
        
        # Blocks (3 rows, 5 columns)
        self.blocks = []
        for row in range(3):
            for col in range(5):
                x = 50 + col * (self.block_width + self.block_gap)
                y = 50 + row * (self.block_height + self.block_gap)
                self.blocks.append(pygame.Rect(x, y, self.block_width, self.block_height))
                
    def update(self, dt):
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
            # Adjust x direction based on where ball hits paddle
            paddle_center = self.paddle.centerx
            ball_center = self.ball.centerx
            if ball_center < paddle_center:
                self.ball_speed_x = -abs(self.ball_speed_x)
            else:
                self.ball_speed_x = abs(self.ball_speed_x)

        
        # Block collisions
        for block in self.blocks[:]:
            if self.ball.colliderect(block):
                self.blocks.remove(block)
                self.ball_speed_y *= -1
                break
                
        # Reset ball if it goes off bottom
        if self.ball.bottom >= self.height:
            self.ball.center = (self.width // 2, self.height // 2)
            self.ball_speed_x = 5
            self.ball_speed_y = 5
            
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw paddle and ball
        pygame.draw.rect(screen, (255, 255, 255), self.paddle)
        pygame.draw.ellipse(screen, (255, 255, 255), self.ball)
        
        # Draw blocks
        for block in self.blocks:
            pygame.draw.rect(screen, (0, 255, 0), block)
            
        pygame.display.flip()
        
    def shutdown(self):
        pass