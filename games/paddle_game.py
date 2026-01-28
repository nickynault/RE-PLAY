import pygame
from systems.game import Game

class PaddleGame(Game):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.paddle_width = 10
        self.paddle_height = 100
        self.ball_size = 15
        self.paddle_speed = 8
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        
    def init(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.reset_game()
        
    def reset_game(self):
        # Paddles
        self.left_paddle = pygame.Rect(50, self.height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)
        self.right_paddle = pygame.Rect(self.width - 50 - self.paddle_width, self.height // 2 - self.paddle_height // 2, self.paddle_width, self.paddle_height)
        
        # Ball
        self.ball = pygame.Rect(self.width // 2 - self.ball_size // 2, self.height // 2 - self.ball_size // 2, self.ball_size, self.ball_size)
        
        # Scores
        self.left_score = 0
        self.right_score = 0
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        
        # Left paddle (W/S)
        if keys[pygame.K_w] and self.left_paddle.top > 0:
            self.left_paddle.y -= self.paddle_speed
        if keys[pygame.K_s] and self.left_paddle.bottom < self.height:
            self.left_paddle.y += self.paddle_speed
            
        # Right paddle (Up/Down)
        if keys[pygame.K_UP] and self.right_paddle.top > 0:
            self.right_paddle.y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.right_paddle.bottom < self.height:
            self.right_paddle.y += self.paddle_speed
        
        # Ball movement
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        
        # Wall collisions
        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            self.ball_speed_y *= -1
            
        # Paddle collisions
        # Left paddle
        if self.ball.colliderect(self.left_paddle) and self.ball_speed_x < 0:
            self.ball_speed_x *= -1
            self.ball.left = self.left_paddle.right  # push out

        # Right paddle
        if self.ball.colliderect(self.right_paddle) and self.ball_speed_x > 0:
            self.ball_speed_x *= -1
            self.ball.right = self.right_paddle.left  # push out

            
        # Scoring
        if self.ball.left <= 0:
            self.right_score += 1
            self.reset_ball()
        if self.ball.right >= self.width:
            self.left_score += 1
            self.reset_ball()
            
    def reset_ball(self):
        self.ball.center = (self.width // 2, self.height // 2)
        self.ball_speed_x *= -1
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw paddles and ball
        pygame.draw.rect(screen, (255, 255, 255), self.left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), self.right_paddle)
        pygame.draw.ellipse(screen, (255, 255, 255), self.ball)
        
        # Draw scores
        score_text = self.font.render(f"{self.left_score} - {self.right_score}", True, (255, 255, 255))
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 20))
        
        pygame.display.flip()
        
    def shutdown(self):
        pass
