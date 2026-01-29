import pygame
import random
from systems.game import Game

class Asteroid:
    """Asteroid object that stores both rect and image for proper collision and rendering"""
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        # Create a mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(image)

class VoidDriftGame(Game):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.player_width = 40
        self.player_height = 40
        self.player_speed = 6
        self.asteroid_speed = 4
        self.asteroid_spawn_rate = 60  # frames between spawns
        self.score_multiplier = 10  # Score increases by 10 per second
        self.high_score = 0
        self.hit_flash_timer = 0 
        self.game_over = False
        self.game_over_timer = 0  
        self.depixelation_progress = 0  # 0 to 1 for depixelation effect
        
        
        # Visual assets
        self.player_image = None
        self.asteroid_images = []  # List of different asteroid images
        self.starfield_image = None
        
    def init(self, screen):
        self.screen = screen 
        self.font = pygame.font.Font(None, 36)        # main score
        self.small_font = pygame.font.Font(None, 24)  # smaller scores
        self.game_over_font = pygame.font.Font(None, 72) # Game Over text
        
        # Load assets
        try:
            self.player_image = pygame.image.load("assets/player_ship.png").convert_alpha()
            # Load multiple asteroid variants
            asteroid_variants = ["assets/asteroid.png", "assets/asteroid_1.png", "assets/asteroid_2.png", 
                               "assets/asteroid_3.png", "assets/asteroid_4.png"]
            for variant in asteroid_variants:
                try:
                    asteroid_img = pygame.image.load(variant).convert_alpha()
                    self.asteroid_images.append(asteroid_img)
                except pygame.error:
                    print(f"Warning: Could not load {variant}")
            
            self.starfield_image = pygame.image.load("assets/starfield.png").convert()
            
            if not self.asteroid_images:
                print("Warning: No asteroid images loaded, using fallback")
                self.asteroid_images = [None]  # Fallback
        except pygame.error as e:
            print(f"Warning: Could not load assets: {e}")
            # Fallback to simple shapes if assets fail to load
            self.player_image = None
            self.asteroid_images = [None]  # Fallback
            self.starfield_image = None
            
        # Starfield scrolling
        self.starfield_y = 0
        self.starfield_speed = 1  # Slower than asteroids
        
        self.reset_game()
        
    def reset_game(self):
        self.player = pygame.Rect(self.width // 2 - self.player_width // 2, 
            self.height - 100, self.player_width, self.player_height) # Player object
        
        # Game state
        self.score = 0
        self.frame_count = 0
        self.asteroids = []  # List of asteroid objects with their own images
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
                # Adjust asteroid sizes - remove very small ones, add bigger ones
                asteroid_width = random.randint(40, 120)  # Increased minimum from 30 to 40, max from 80 to 120
                asteroid_height = random.randint(40, 120)
                asteroid_x = random.randint(0, self.width - asteroid_width)
                # Select a random asteroid image
                asteroid_image = random.choice(self.asteroid_images)
                # Scale the image to match the desired size
                scaled_image = pygame.transform.scale(asteroid_image, (asteroid_width, asteroid_height))
                # Create Asteroid object with pixel-perfect collision
                self.asteroids.append(Asteroid(asteroid_x, -asteroid_height, asteroid_width, asteroid_height, scaled_image))

            # Move asteroids and check collisions
            for asteroid in self.asteroids[:]:
                # Size-based speed variation: bigger asteroids move slower
                # Base speed modified by size factor (larger = slower)
                size_factor = 1.0 - (min(asteroid.rect.width, asteroid.rect.height) - 40) / 160  # 40 to 120 range
                size_factor = max(0.5, size_factor)  # Don't go below 50% speed
                asteroid_speed_adjusted = self.asteroid_speed * size_factor
                
                asteroid.rect.y += asteroid_speed_adjusted
                if asteroid.rect.top > self.height:
                    self.asteroids.remove(asteroid)
                    self.score += 1
                
                # Pixel-perfect collision detection
                if self.player.colliderect(asteroid.rect):
                    # Create a mask for the player (approximate since player is a rect)
                    player_mask = pygame.mask.Mask((self.player.width, self.player.height), fill=True)
                    player_pos = (self.player.x, self.player.y)
                    
                    # Check pixel-perfect collision
                    offset = (asteroid.rect.x - self.player.x, asteroid.rect.y - self.player.y)
                    if asteroid.mask.overlap(player_mask, offset):
                        # Handle collision (death)
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.hit_flash_timer = 0.2
                        self.game_over = True
                        self.game_over_timer = 4.0
                        self.depixelation_progress = 0  # Start depixelation
                        self.asteroids.remove(asteroid)


        # Update score (time survived with multiplier)
        if not self.game_over:
            self.score += dt * self.score_multiplier
            
        # Difficulty ramping - increase asteroid speed based on score
        # Soft cap: speed increases but slows down at higher values
        base_speed = 4
        max_speed = 12
        speed_factor = 0.05  # How quickly speed increases
        self.asteroid_speed = min(max_speed, base_speed + (self.score * speed_factor))
        
        # Update starfield scrolling
        if not self.game_over:
            self.starfield_y += self.starfield_speed
            # Reset starfield when it scrolls off screen
            if self.starfield_y >= self.height:
                self.starfield_y = 0

        return True

    def draw(self, screen):
        # Draw scrolling starfield background
        if self.starfield_image:
            # Draw starfield at current scroll position
            screen.blit(self.starfield_image, (0, self.starfield_y - self.height))
            # Draw second copy to create seamless scrolling
            screen.blit(self.starfield_image, (0, self.starfield_y))
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
            if asteroid.image:
                # Use the asteroid's own pre-scaled image
                screen.blit(asteroid.image, asteroid.rect)
            else:
                # Fallback to rectangle
                pygame.draw.rect(screen, (200, 200, 200), asteroid.rect)
        
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
