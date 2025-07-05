import pygame
import sys
import random
import math
import os
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
MAX_SMILEYS = 25

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
LIGHT_GREEN = (144, 238, 144)
PURPLE = (221, 160, 221)

def generate_simple_pop_sound():
    """Generate a simple pop sound without numpy"""
    try:
        duration = 0.1  # seconds
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create a simple pop sound using basic math
        arr = []
        for i in range(frames):
            time = float(i) / sample_rate
            # Simple sine wave with decay
            wave = math.sin(2 * math.pi * 800 * time) * math.exp(-time * 8)
            # Convert to 16-bit signed integer
            sample = int(wave * 16000)
            arr.append([sample, sample])  # Stereo
        
        # Convert to pygame Sound
        sound_array = pygame.array.array('h', [item for sublist in arr for item in sublist])
        sound = pygame.sndarray.make_sound(sound_array.reshape((frames, 2)))
        return sound
    except Exception:
        return None

class Particle:
    """Sparkle particle for visual effects"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.color = random.choice([YELLOW, ORANGE, PINK, WHITE, (255, 255, 150), (150, 255, 255)])
        self.size = random.randint(2, 6)
        self.shape = random.choice(['circle', 'star'])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity effect
        self.life -= 1
        # Fade effect
        alpha = self.life / self.max_life
        self.size = max(1, self.size * alpha)
    
    def draw(self, screen):
        if self.life > 0:
            alpha = max(0, min(255, int(255 * self.life / self.max_life)))
            color_with_alpha = (*self.color[:3], alpha)
            
            if self.shape == 'star':
                # Draw a simple star shape
                size = int(self.size)
                points = []
                for i in range(10):
                    angle = i * math.pi / 5
                    radius = size if i % 2 == 0 else size // 2
                    px = self.x + radius * math.cos(angle)
                    py = self.y + radius * math.sin(angle)
                    points.append((px, py))
                if len(points) >= 3:
                    try:
                        pygame.draw.polygon(screen, self.color, points)
                    except:
                        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
            else:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Smiley:
    """Happy smiley face sprite"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_size = random.randint(25, 45)
        self.size = self.base_size
        self.color = random.choice([YELLOW, ORANGE, PINK, LIGHT_GREEN])
        self.base_color = self.color
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.clicked = False
        self.click_timer = 0
        self.bounce_timer = 0
        self.rotation = 0
        
    def update(self):
        # Move the smiley
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off edges with gentle motion
        if self.x - self.size <= 0 or self.x + self.size >= SCREEN_WIDTH:
            self.vx *= -0.8  # Add some damping for gentler bounces
            self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
            
        if self.y - self.size <= 0 or self.y + self.size >= SCREEN_HEIGHT:
            self.vy *= -0.8
            self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
        
        # Handle click animation
        if self.clicked:
            self.click_timer -= 1
            # Pulsing effect
            pulse = math.sin(self.click_timer * 0.3) * 5
            self.size = self.base_size + pulse + 10
            self.rotation += 5
            
            if self.click_timer <= 0:
                self.clicked = False
                self.size = self.base_size
                self.color = self.base_color
                self.rotation = 0
        
        # Add gentle floating motion
        self.bounce_timer += 0.1
        self.y += math.sin(self.bounce_timer) * 0.2
    
    def handle_click(self, mouse_pos):
        """Check if smiley was clicked and trigger reaction"""
        distance = math.sqrt((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)
        if distance <= self.size:
            self.clicked = True
            self.click_timer = 60  # 1 second at 60 FPS
            # Change to a brighter, happier color
            bright_colors = [(255, 255, 100), (255, 100, 255), (100, 255, 255), (255, 200, 100)]
            self.color = random.choice(bright_colors)
            return True
        return False
    
    def draw(self, screen):
        # Draw smiley body with optional rotation
        if self.rotation != 0:
            # Create a surface for rotation
            surf_size = int(self.size * 2.5)
            temp_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
            
            # Draw on temp surface
            center = surf_size // 2
            pygame.draw.circle(temp_surf, self.color, (center, center), int(self.size))
            pygame.draw.circle(temp_surf, (0, 0, 0), (center, center), int(self.size), 2)
            
            # Eyes
            eye_offset = self.size // 3
            pygame.draw.circle(temp_surf, (0, 0, 0), (center - eye_offset, center - eye_offset//2), 3)
            pygame.draw.circle(temp_surf, (0, 0, 0), (center + eye_offset, center - eye_offset//2), 3)
            
            # Smile
            smile_rect = pygame.Rect(center - eye_offset, center, eye_offset * 2, eye_offset)
            pygame.draw.arc(temp_surf, (0, 0, 0), smile_rect, 0, math.pi, 3)
            
            # Rotate and blit
            rotated_surf = pygame.transform.rotate(temp_surf, self.rotation)
            rotated_rect = rotated_surf.get_rect(center=(self.x, self.y))
            screen.blit(rotated_surf, rotated_rect)
        else:
            # Draw normally
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
            pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), int(self.size), 2)
            
            # Eyes
            eye_offset = self.size // 3
            pygame.draw.circle(screen, (0, 0, 0), 
                             (int(self.x - eye_offset), int(self.y - eye_offset//2)), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (int(self.x + eye_offset), int(self.y - eye_offset//2)), 3)
            
            # Smile
            smile_rect = pygame.Rect(self.x - eye_offset, self.y, eye_offset * 2, eye_offset)
            pygame.draw.arc(screen, (0, 0, 0), smile_rect, 0, math.pi, 3)

class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Smiley Splash - Click the Smileys!")
        self.clock = pygame.time.Clock()
        self.smileys = []
        self.particles = []
        self.spawn_timer = 0
        
        # Generate click sound
        self.click_sound = generate_simple_pop_sound()
        
        # Create initial smileys
        for _ in range(8):
            self.spawn_smiley()
    
    def spawn_smiley(self):
        """Spawn a new smiley at a random location"""
        if len(self.smileys) < MAX_SMILEYS:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.smileys.append(Smiley(x, y))
    
    def create_particles(self, x, y):
        """Create sparkle particles at the given position"""
        for _ in range(8):
            self.particles.append(Particle(x, y))
    
    def play_click_sound(self):
        """Play the click sound if available"""
        if self.click_sound:
            try:
                self.click_sound.play()
            except Exception:
                pass  # Fail silently if sound doesn't work
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if any smiley was clicked
                    for smiley in self.smileys:
                        if smiley.handle_click(event.pos):
                            self.create_particles(smiley.x, smiley.y)
                            self.play_click_sound()
                            break
        return True
    
    def update(self):
        """Update game state"""
        # Update smileys
        for smiley in self.smileys:
            smiley.update()
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
        # Spawn new smileys occasionally
        self.spawn_timer += 1
        if self.spawn_timer >= 180:  # Every 3 seconds
            self.spawn_smiley()
            self.spawn_timer = 0
    
    def draw(self):
        """Draw everything"""
        # Clear screen with a pleasant gradient-like background
        self.screen.fill(LIGHT_BLUE)
        
        # Add some background decorations (simple clouds)
        for i in range(3):
            x = (i * 300 + 100) % SCREEN_WIDTH
            y = 50 + i * 30
            # Simple cloud shapes
            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), 25, 0)
            pygame.draw.circle(self.screen, WHITE, (int(x + 20), int(y)), 20, 0)
            pygame.draw.circle(self.screen, WHITE, (int(x - 20), int(y)), 20, 0)
            pygame.draw.circle(self.screen, WHITE, (int(x + 10), int(y - 10)), 15, 0)
        
        # Draw smileys
        for smiley in self.smileys:
            smiley.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Add a subtle title
        if hasattr(pygame, 'font'):
            try:
                font = pygame.font.Font(None, 36)
                title_text = font.render("Click the Smileys!", True, (100, 100, 100))
                text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
                self.screen.blit(title_text, text_rect)
            except:
                pass  # Font not available
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 