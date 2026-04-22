import math

# --------------------------------------------------
# DISTANCE BETWEEN TWO POINTS
# Used when finding the closest planet to the player
# --------------------------------------------------
def get_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # Pythagorean theorem
    return math.sqrt(dx * dx + dy * dy)


# --------------------------------------------------
# NORMALIZE A VECTOR
# Turns any vector into length 1 while keeping
# the same direction
# --------------------------------------------------
def normalize(dx, dy):
    magnitude = math.sqrt(dx * dx + dy * dy)

    if magnitude == 0:
        return 0, 0

    return dx / magnitude, dy / magnitude


# --------------------------------------------------
# GET THE DIRECTION OF GRAVITY
# Returns nx, ny which point toward the planet
# --------------------------------------------------
def get_gravity_direction(player_x, player_y, planet):
    dx = planet.x - player_x
    dy = planet.y - player_y

    return normalize(dx, dy)


# --------------------------------------------------
# APPLY GRAVITY TO VELOCITY
# nx, ny is the direction toward the planet
# strength controls how strong the gravity is
# --------------------------------------------------
def apply_gravity(vx, vy, nx, ny, strength):
    vx += nx * strength
    vy += ny * strength

    return vx, vy