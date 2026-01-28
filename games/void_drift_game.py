import pygame
import random
from systems.game import Game

class VoidDriftGame(Game):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.player_width = 40
        self.player_height = 40
        self.player_speed = 6
        self.asteroid_speed = 4
        self.asteroid_spawn_rate = 60  # frames between spawns
        
    def init(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.reset_game()
        
    def reset_game(self):
        # Player
        self.player = pygame.Rect(self.width // 2 - self.player_width // 2, self.height - 100, self.player_width, self.player_height)
        
        # Game state
        self.score = 0
        self.frame_count = 0
        self.asteroids = []
        
    def update(self, dt):
        # Player movement (arrow keys)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.left > 0:
            self.player.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player.right < self.width:
            self.player.x += self.player_speed
        if keys[pygame.K_UP] and self.player.top > 0:
            self.player.y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player.bottom < self.height:
            self.player.y += self.player_speed
        
        # Spawn asteroids
        self.frame_count += 1
        if self.frame_count % self.asteroid_spawn_rate == 0:
            asteroid_width = random.randint(30, 80)
            asteroid_height = random.randint(30, 80)
            asteroid_x = random.randint(0, self.width - asteroid_width)
            self.asteroids.append(pygame.Rect(asteroid_x, -asteroid_height, asteroid_width, asteroid_height))
        
        # Move asteroids and check collisions
        for asteroid in self.asteroids[:]:
            asteroid.y += self.asteroid_speed
            
            # Remove asteroids that go off screen
            if asteroid.top > self.height:
                self.asteroids.remove(asteroid)
                self.score += 1
            
            # Check collision with player
            if self.player.colliderect(asteroid):
                self.reset_game()
                break
                
        # Update score (time survived)
        self.score += dt
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw player
        pygame.draw.rect(screen, (255, 255, 255), self.player)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            pygame.draw.rect(screen, (200, 200, 200), asteroid)
        
        # Draw score
        score_text = self.font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        
    def shutdown(self):
        pass