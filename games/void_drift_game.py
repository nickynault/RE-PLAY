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
        self.high_score = 0
        self.hit_flash_timer = 0 
        self.game_over = False
        self.game_over_timer = 0  
        
    def init(self, screen):
        self.screen = screen 
        self.font = pygame.font.Font(None, 36)        # main score
        self.small_font = pygame.font.Font(None, 24)  # smaller scores
        self.game_over_font = pygame.font.Font(None, 72) # Game Over text
        self.reset_game() 
        
    def reset_game(self):
        self.player = pygame.Rect(self.width // 2 - self.player_width // 2, 
            self.height - 100, self.player_width, self.player_height) # Player object
        
        # Game state
        self.score = 0
        self.frame_count = 0
        self.asteroids = []
        self.hit_flash_timer = 0
        self.game_over = False
        self.game_over_timer = 0
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.game_over:
            # Countdown Game Over timer
            self.game_over_timer = max(0, self.game_over_timer - dt)  # Prevent negative values
            if self.game_over_timer <= 0:
                # Reset player and asteroids manually
                self.player.x = self.width // 2 - self.player_width // 2
                self.player.y = self.height - 100
                self.asteroids.clear()
                self.score = 0
                self.frame_count = 0
                self.game_over = False
                self.hit_flash_timer = 0
                self.game_over_timer = 0
            # Don't process movement or asteroids, but continue the loop
        else:
            # Player movement
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
                if asteroid.top > self.height:
                    self.asteroids.remove(asteroid)
                    self.score += 1
                if self.player.colliderect(asteroid):
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.hit_flash_timer = 0.2
                    self.game_over = True
                    self.game_over_timer = 4.0
                    self.asteroids.remove(asteroid)

        # Update score (time survived)
        if not self.game_over:
            self.score += dt

        return True

        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw player
        player_color = (255, 0, 0) if self.hit_flash_timer > 0 else (255, 255, 255)
        pygame.draw.rect(screen, player_color, self.player)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            pygame.draw.rect(screen, (200, 200, 200), asteroid)
        
        # Draw score
        score_text = self.font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {int(self.high_score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

         # Draw Game Over text
        if self.game_over:
            go_text = self.game_over_font.render("GAME OVER!", True, (255, 0, 0))
            screen.blit(go_text, (self.width//2 - go_text.get_width()//2,
                                  self.height//2 - go_text.get_height()//2))
        
        pygame.display.flip()
        
    def shutdown(self):
        pass