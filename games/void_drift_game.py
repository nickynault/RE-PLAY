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
        self.depixelation_progress = 0  # 0 to 1 for depixelation effect
        
        # Visual assets
        self.player_image = None
        self.asteroid_image = None
        self.starfield_image = None
        
    def init(self, screen):
        self.screen = screen 
        self.font = pygame.font.Font(None, 36)        # main score
        self.small_font = pygame.font.Font(None, 24)  # smaller scores
        self.game_over_font = pygame.font.Font(None, 72) # Game Over text
        
        # Load assets
        try:
            self.player_image = pygame.image.load("assets/player_ship.png").convert_alpha()
            self.asteroid_image = pygame.image.load("assets/asteroid.png").convert_alpha()
            self.starfield_image = pygame.image.load("assets/starfield.png").convert()
        except pygame.error as e:
            print(f"Warning: Could not load assets: {e}")
            # Fallback to simple shapes if assets fail to load
            self.player_image = None
            self.asteroid_image = None
            self.starfield_image = None
            
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
        self.depixelation_progress = 0
        
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.game_over:
            # Countdown Game Over timer
            self.game_over_timer = max(0, self.game_over_timer - dt)  # Prevent negative values
            # Update depixelation effect
            self.depixelation_progress = min(1.0, self.depixelation_progress + dt * 0.5)  # Depixelate over 2 seconds
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
                self.depixelation_progress = 0
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
                    self.depixelation_progress = 0  # Start depixelation
                    self.asteroids.remove(asteroid)

        # Update score (time survived)
        if not self.game_over:
            self.score += dt

        return True

        
    def draw(self, screen):
        # Draw starfield background
        if self.starfield_image:
            screen.blit(self.starfield_image, (0, 0))
        else:
            screen.fill((0, 0, 0))
        
        # Draw player
        if self.player_image:
            if self.game_over and self.depixelation_progress > 0:
                # Draw depixelation effect
                self.draw_depixelation_effect(screen, self.player, self.depixelation_progress)
            else:
                screen.blit(self.player_image, self.player)
        else:
            # Fallback to rectangle
            player_color = (255, 255, 255)
            pygame.draw.rect(screen, player_color, self.player)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            if self.asteroid_image:
                # Scale asteroid image to match rect size
                scaled_image = pygame.transform.scale(self.asteroid_image, (asteroid.width, asteroid.height))
                screen.blit(scaled_image, asteroid)
            else:
                # Fallback to rectangle
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
        
    def draw_depixelation_effect(self, screen, rect, progress):
        """Draw a depixelation effect that makes the player disintegrate into pixels"""
        if not self.player_image:
            return
            
        # Create a copy of the player image
        player_surface = self.player_image.copy()
        
        # Calculate pixel size based on progress (0 to 1)
        # At progress 0, full detail. At progress 1, completely pixelated/disintegrated
        max_pixel_size = 8
        pixel_size = int(max_pixel_size * progress)
        
        if pixel_size < 1:
            # Still mostly intact, just draw normally
            screen.blit(self.player_image, rect)
            return
            
        # Create pixelation effect
        # Scale down to create pixelation, then scale back up
        original_size = self.player_image.get_size()
        small_size = (max(1, original_size[0] // pixel_size), max(1, original_size[1] // pixel_size))
        
        # Scale down (pixelate)
        small_surface = pygame.transform.scale(player_surface, small_size)
        
        # Scale back up (but with pixelation)
        pixelated_surface = pygame.transform.scale(small_surface, original_size)
        
        # Add disintegration effect - remove random pixels
        if progress > 0.3:
            # Create a mask for disappearing pixels
            for x in range(0, original_size[0], pixel_size):
                for y in range(0, original_size[1], pixel_size):
                    # Random chance to remove this pixel block
                    if random.random() < progress * 0.8:
                        # Make this pixel block transparent
                        pixel_rect = pygame.Rect(x, y, pixel_size, pixel_size)
                        pygame.draw.rect(pixelated_surface, (0, 0, 0, 0), pixel_rect, 0)
        
        # Draw the pixelated/disintegrating ship
        screen.blit(pixelated_surface, rect)
        
    def shutdown(self):
        pass
