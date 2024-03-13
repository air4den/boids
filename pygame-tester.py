import pygame
import math
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

buzz = pygame.image.load("buzz.jpg")

class Boid(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
            pygame.sprite.Sprite.__init__(self)

            self.pos = pos
            self.vel = vel

            # Set Sprite image

            self.image = pygame.Surface([150,100])
            
            pygame.draw.polygon(self.image, 'red', [[0, 0], [150,50], [0,100]])
            self.rect = self.image.get_rect(center = (pos.x, pos.y))

            self.image = self.image.convert_alpha()

            self.heading = math.degrees(math.atan2(vel.y, vel.x))     # calculates angle from vel & conv to degrees

            self.image = pygame.transform.rotate(self.image, -150.64224519209148)
            self.rect = self.image.get_rect(center = (pos.x, pos.y))






            # TODO heading <== angle
            

myPos = pygame.Vector2(1280/2, 720/2)
myVel = pygame.Vector2(1,1)
myBoid = Boid(myPos, myVel)
print(f"Heading %d", myBoid.heading)
print(f"x: %f, y: %f", myBoid.pos.x, myBoid.pos.y)
print(f"imgcenter: %d", myBoid.rect.center)

running = True
while(running):

    # Pygame Event Listener 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    pygame.draw.circle(screen, 'blue', (1280/2, 720/2), 15)

    screen.blit(myBoid.image, myBoid.rect)
    pygame.draw.circle(screen, 'green', (myBoid.rect.center), 5)
    


    

    pygame.display.flip()
    
    # Set FPS
    dt = clock.tick(30)

pygame.quit()
