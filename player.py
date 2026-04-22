import random
import pygame
import physics
import math

class Player:
    def __init__(self, x, y):
        self.particles = []

        # ==========================================
        # PLAYER POSITION
        # ==========================================
        self.x = x
        self.y = y

        # ==========================================
        # PLAYER SIZE
        # ==========================================
        self.size = 20

        # ==========================================
        # PLAYER VELOCITY
        # ==========================================
        self.vel_x = 0
        self.vel_y = 0

        # ==========================================
        # THRUSTER SETTINGS
        # ==========================================
        self.thrust_power = 0.4
        self.up_thrust_power = 0.8
        self.max_speed = 12

        # ==========================================
        # WALKING SETTINGS
        # ==========================================
        self.walk_acceleration = 0.2

        # ==========================================
        # FUEL SYSTEM
        # ==========================================
        
        self.fuel = 100.0
        self.max_fuel = 100.0

        # ==========================================
        # PLAYER STATE
        # ==========================================
        self.on_ground = False
        self.is_alive = True
        self.did_win = False
        self.angle = 0

    def update(self, planets):

        # Stop updating if the player is dead
        if not self.is_alive:
            return

        # ==========================================
        # FIND THE CLOSEST PLANET
        # ==========================================
        closest_planet = None
        closest_distance = float("inf")

        for planet in planets:

            distance = physics.get_distance(
                self.x,
                self.y,
                planet.x,
                planet.y
            )

            if distance < closest_distance:
                closest_distance = distance
                closest_planet = planet

        # ==========================================
        # CALCULATE GRAVITY DIRECTION
        # nx, ny points toward the center of planet
        # ==========================================
        nx, ny = physics.get_gravity_direction(
            self.x,
            self.y,
            closest_planet
        )

        # ==========================================
        # CALCULATE PLAYER ROTATION
        # ==========================================
        self.angle = math.degrees(math.atan2(ny, nx)) + 90

        # ==========================================
        # APPLY GRAVITY
        # ==========================================
        self.vel_x, self.vel_y = physics.apply_gravity(
            self.vel_x,
            self.vel_y,
            nx,
            ny,
            closest_planet.gravity_strength
        )

        # ==========================================
        # CREATE SURFACE TANGENT DIRECTION
        # tangent_x and tangent_y point sideways
        # along the surface of the planet
        # ==========================================
        tangent_x = -ny
        tangent_y = nx

        # Get current keyboard input
        keys = pygame.key.get_pressed()

        # ==========================================
        # THRUSTER CONTROLS
        # A = left thruster
        # D = right thruster
        # W = upward rocket thrust
        # ==========================================
        if self.fuel > 0:
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] and self.fuel > 0:
                self.particles.append([[self.x, self.y], [random.uniform(-1, 1), random.uniform(-1, 1)], 15]) 
            if keys[pygame.K_a]:
                self.vel_x -= tangent_x * self.thrust_power
                self.vel_y -= tangent_y * self.thrust_power
                self.fuel -= 0.02

            if keys[pygame.K_d]:
                self.vel_x += tangent_x * self.thrust_power
                self.vel_y += tangent_y * self.thrust_power
                self.fuel -= 0.02

            if keys[pygame.K_w]:
                self.vel_x -= nx * self.up_thrust_power
                self.vel_y -= ny * self.up_thrust_power
                self.fuel -= 0.05

        # Prevent fuel from going negative
        if self.fuel < 0:
            self.fuel = 0

        # ==========================================
        # WALKING CONTROLS
        # Only works while touching the ground
        # Arrow keys walk around the planet surface
        # ==========================================
        if self.on_ground:

            if keys[pygame.K_LEFT]:
                self.vel_x -= tangent_x * self.walk_acceleration
                self.vel_y -= tangent_y * self.walk_acceleration

            if keys[pygame.K_RIGHT]:
                self.vel_x += tangent_x * self.walk_acceleration
                self.vel_y += tangent_y * self.walk_acceleration

        # ==========================================
        # LIMIT PLAYER SPEED
        # ==========================================
        speed = math.sqrt(
            self.vel_x * self.vel_x +
            self.vel_y * self.vel_y
        )

        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vel_x *= scale
            self.vel_y *= scale

        # ==========================================
        # MOVE THE PLAYER
        # ==========================================
        self.x += self.vel_x
        self.y += self.vel_y

        # ==========================================
        # RECALCULATE DISTANCE AFTER MOVEMENT
        # ==========================================
        closest_distance = physics.get_distance(
            self.x,
            self.y,
            closest_planet.x,
            closest_planet.y
        )

        # ==========================================
        # COLLISION WITH THE PLANET
        # ==========================================
        surface_distance = closest_planet.radius + (self.size / 2)

        if closest_distance < surface_distance:
            if closest_planet.color == (255, 0, 0):# Red planet is deadly
                self.is_alive = False
                return
            if closest_planet.color == (0, 255, 0):# Yellow planet is the goal
                self.did_win = True
                return
            # How far inside the planet the player is
            penetration = surface_distance - closest_distance

            # Push the player back outside the planet
            self.x -= nx * penetration
            self.y -= ny * penetration

            # Remove velocity pointing into the planet
            dot = self.vel_x * nx + self.vel_y * ny

            if dot > 0:
                self.vel_x -= nx * dot
                self.vel_y -= ny * dot

            # Apply friction while grounded
            self.vel_x *= (1 - closest_planet.friction)
            self.vel_y *= (1 - closest_planet.friction)

            self.on_ground = True

        else:
            self.on_ground = False

    def draw(self, screen, camera_x, camera_y):

        # Create a transparent surface to draw the player
        player_surface = pygame.Surface(
            (self.size, self.size * 2),
            pygame.SRCALPHA
        )
        for p in self.particles:
            size = int(p[2]/3)
            if size > 0:
                pygame.draw.circle(screen, (255, 140, 0), (int(p[0][0]-camera_x), int(p[0][1]-camera_y)), size)
        # Draw the player's body
        pygame.draw.rect(
            player_surface,
            (255, 255, 255),
            (0, 10, self.size, self.size)
        )

        # Draw a red circle for the player's head
        pygame.draw.circle(
            player_surface,
            (255, 0, 0),
            (self.size // 2, 15),
            5
        )

        # Rotate the player so it matches the planet surface
        rotated_surface = pygame.transform.rotate(
            player_surface,
            -self.angle
        )

        # Convert world coordinates into screen coordinates
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        rotated_rect = rotated_surface.get_rect(
            center=(int(draw_x), int(draw_y))
        )

        # Draw the player
        screen.blit(rotated_surface, rotated_rect.topleft)

        for p in self.particles[:]:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2] -= 1
            if p[2] <= 0: 
                self.particles.remove(p)