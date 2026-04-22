import pygame
import math


class Planet:
    # Set up the planet's position, size, color, and gravity pull
    def __init__(self, x, y, radius, color=(100,100,255), gravity_strength=0.5, friction=0.02):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.gravity_strength = gravity_strength
        self.friction = friction

    # This draws the planet on the screen, adjusted for where the camera is looking
    def draw(self, screen, camera_x, camera_y):
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y - camera_y)

        pulse = math.sin(pygame.time.get_ticks() * 0.002) * 3
        # Draw the main planet body
        pygame.draw.circle(screen, self.color, (draw_x, draw_y), self.radius + pulse)

        # Add Craters
        # Calculate a darker version of the planet color for the craters
        crater_color = (
            max(0, self.color[0] - 40),
            max(0, self.color[1] - 40),
            max(0, self.color[2] - 40)
        )

        # We define a few relative positions for craters so they scale with the radius
        # (x_offset, y_offset, size_multiplier)
        crater_data = [
            (0.3, 0.2, 0.2), 
            (-0.4, -0.3, 0.15), 
            (0.1, -0.6, 0.1),
            (-0.2, 0.4, 0.12)
        ]

        for off_x, off_y, size_mult in crater_data:
            c_x = draw_x + (self.radius * off_x)
            c_y = draw_y + (self.radius * off_y)
            pygame.draw.circle(screen, crater_color, (int(c_x), int(c_y)), int(self.radius * size_mult))

        # Add a subtle "Atmosphere" or Shine
        # Drawing a slightly smaller, thinner circle on one side creates a 3D effect
        shine_color = (
            min(255, self.color[0] + 30),
            min(255, self.color[1] + 30),
            min(255, self.color[2] + 30)
        )
        #Draw the white outline (kept from your original)
        pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), self.radius, 3)