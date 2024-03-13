import pygame
import math
import random

SCREEN_HEIGHT = 1280
SCREEN_WIDTH = 720
FRAMERATE = 24

NUM_BOIDS = 100
SPEED_INIT = 10
SPEED_MAX = 12
SPEED_MIN = 3

FACTOR_MATCHING_NEARBY_VEL = 0.05
FACTOR_CENTERING = 0.05
FACTOR_AVOID = 0.15
MIN_AVOID_DISTANCE = 10
SIGHT_RANGE = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()
running = True

# initi list of boids
# TODO switch back to sprite group
boids = []

# initialize boid sprite PyGame Surface
init_triangle = pygame.Surface([15,10])
init_triangle.set_colorkey('black')
pygame.draw.polygon(init_triangle, 'red', [[0,0], [15,5], [0,10]])     # initially points in direction (1,0)

# TODO: obstacles

def init_boids():
    for i in range(NUM_BOIDS):
        pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        vel = pygame.Vector2(random.randint(-SPEED_MAX, SPEED_MAX), random.randint(-SPEED_MAX, SPEED_MAX))
        b = Boid(pos, vel)
        boids.append(b)
    return



def move_boids_new_positions(boids):
    v1 = pygame.Vector2()
    v2 = pygame.Vector2()
    v3 = pygame.Vector2()

    for b in boids:
        v1 = flyToCenter(b)
        v2 = avoidOtherBoids(b)
        v2 = matchNearbyVel(b)

        v1adj = pygame.Vector2(v1.x, -v1.y)
        v2adj = pygame.Vector2(v2.x, -v2.y)
        v3adj = pygame.Vector2(v3.x, -v3.y)

        b.vel += v1adj + v2adj + v3adj
        limitVel(b)
        b.update_boid_heading()
        b.pos.x += b.vel.x
        b.pos.y -= b.vel.y

        # Pacman border
        if b.pos.x > 1280:
            b.pos.x = b.pos.x - 1280
        if b.pos.x < 0:
            b.pos.x += 1280
        if b.pos.y < 0:
            b.pos.y += 720
        if b.pos.y > 720:
            b.pos.y -= 720    

        print(f'x: {b.pos.x} | y: {b.pos.y}')
        print(f'vel x: {b.vel.x} | vel y: {b.vel.y}')

        print(f'angle {b.heading}')
    

# Rules
def flyToCenter(b):

    # Percieved Center Position Vector
    center = pygame.Vector2()
    num_neighbors = 0

    for bd in boids:
        if (bd != b):
            dist = pygame.Vector2(b.pos - bd.pos)
            if (abs(dist.length()) < SIGHT_RANGE):
                center += bd.pos
                num_neighbors += 1

    if num_neighbors > 0:
        center = center / num_neighbors

    return (center - b.pos) * FACTOR_CENTERING

def avoidOtherBoids(b):

    # Direction vector
    c = pygame.Vector2((0,0))

    # Turn in cumulative opposite direction of all other near boids
    for bd in boids:
        if (bd != b):
            dist = pygame.Vector2(b.pos - bd.pos)
            if (abs(dist.length()) < MIN_AVOID_DISTANCE):
                c += -(b.pos - bd.pos)

    return c * FACTOR_AVOID

def matchNearbyVel(b):
    if (NUM_BOIDS <= 1):
        return pygame.Vector2(0,0)
    
    # Percieved Velocity Vector
    vPV = pygame.Vector2()

    for bd in boids:
        if bd != b:
            vPV += b.vel

    vPV /= NUM_BOIDS-1

    # Add a small portion (~1/8) of percieved velocity to boid's curret vel
    return (vPV - b.vel) * FACTOR_MATCHING_NEARBY_VEL

def limitVel(b):
    if b.vel.magnitude() > SPEED_MAX:
        b.vel = (b.vel / b.vel.magnitude())  * SPEED_MAX
    if b.vel.magnitude() < SPEED_MIN:
        b.vel = (b.vel / b.vel.magnitude())  * SPEED_MIN
    return



class Boid(pygame.sprite.Sprite):
    # TODO Fix negaive/positive y coordiates when calculating velocity
    def __init__(self, pos, vel):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.vel = vel

        # Set Sprite image as Triangle
        # Heading - point boid in direction of vel vector
        self.heading = math.degrees(math.atan2(vel.y, vel.x))               # calculates angle from vel & conv to degrees
        self.image = pygame.transform.rotate(init_triangle.convert_alpha(), self.heading)
        self.rect = self.image.get_rect(center = (pos.x, pos.y))            # sets boid's center

    def update_boid_heading(self):
        self.heading = math.degrees(math.atan2(self.vel.y, self.vel.x))
        self.image = pygame.transform.rotate(init_triangle.convert_alpha(), self.heading)
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))

        print('updated!')


# MAIN BOIDS ALGROITHM:

# Add boids to Sprite Group
init_boids()

# Main boids loop
while(running):

    # Pygame Event Listener 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    move_boids_new_positions(boids)
    for boid in boids:
        screen.blit(boid.image, boid.rect.center)

    pygame.display.flip()
    
    # Set FPS
    dt = clock.tick(FRAMERATE)

pygame.quit()