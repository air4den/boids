import pygame
import math
import random

SCREEN_HEIGHT = 1280
SCREEN_WIDTH = 720
NUM_BOIDS = 100
SPEED_INIT = 15
SPEED_MAX = 15
SPEED_MIN = 3

FACTOR_MATCHING_NEARBY_VEL = 0.1
FACTOR_CENTERING = 0.1
FACTOR_AVOID = 0.01
MIN_AVOID_DISTANCE = 15
SIGHT_RANGE = 70

pygame.init()
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock();
running = True

# initial list of boids
# TODO switch back to sprite group
boids = []

# TODO: obstacles

def init_boids():
    for i in range(NUM_BOIDS):
        pos = pygame.Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        vel = pygame.Vector2(random.randint(0, SPEED_MAX), random.randint(0, SPEED_MAX))
        b = Boid(pos, vel)
        boids.append(b)
    return



def move_boids_new_positions(boids):
    v1 = pygame.Vector2()
    v2 = pygame.Vector2()
    v3 = pygame.Vector2()

    for b in boids:
        v1 = flyToCenter(b)
        v2 = noCrashing(b)
        v2 = matchNearbyVel(b)

        b.vel += v1 + v2 + v3
        limitVel(b)
        b.pos += b.vel

        # Pacman border
        if b.pos.x > 1280:
            b.pos.x = b.pos.x - 1280
        if b.pos.x < 0:
            b.pos.x += 1280
        if b.pos.y < 0:
            b.pos.y += 720
        if b.pos.y > 720:
            b.pos.y -= 720    

        print(f'x,y: {b.pos.x},{b.pos.y}')
        print(f'angle: {b.angle}')
        b.update()

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

def noCrashing(b):

    # Direction vector
    c = pygame.Vector2((0,0))

    # Turn in cumulative opposite direction of all other near boids
    for bd in boids:
        if (bd != b):
            dist = pygame.Vector2(b.pos - bd.pos)
            if (abs(dist.length()) < MIN_AVOID_DISTANCE):
                c += (b.pos - bd.pos)

    return c * FACTOR_AVOID

def matchNearbyVel(b):
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
    def __init__(self, pos, vel):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.vel = vel
        # TODO heading <== angle
        self.angle = -math.degrees(math.atan2(vel.y, vel.x)) - 45     # calculates angle from vel & conv to degrees

        image = pygame.image.load("darwizzy.png")
        self.image = pygame.transform.scale_by(image, 0.05)
        #self.image = pygame.Surface([15,10], pygame.SRCALPHA).convert()
        #self.image.fill('red')
        self.rect = self.image.get_rect(center = (pos.x, pos.y))

    # TODO fix angle rotation
    def update(self):
        self.angle = -math.degrees(math.atan2(self.vel.y, self.vel.x)) - 90
        dangle =  (-math.degrees(math.atan2(self.vel.y, self.vel.x)) - 90) - self.angle
        self.image = pygame.transform.rotate(self.image, dangle)

        self.rect.center = (self.pos.x, self.pos.y)

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
    dt = clock.tick(30)

pygame.quit()