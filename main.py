
import pygame
from pygame.locals import *
import random
import math

# KEYBINDINGS:
# Press 'q': End Simulation
# Press 'r': Chaos Mode
# Press 'e': Populate Area
# Press 'w': Increase Gravitational Constant (Double)
# Press 's': Decrease Gravitational Constant (Half)
# Press 't': Increase Friction (-10%)
# Press 'g': Decrease Frcition (+10%)
# Mouse, Left Click: Add Atom with Random Velocity

class Game:
    def __init__(self, running, width, height):
        # initialising pygame
        self.MAX_FORCE= 9.81
        self.DISTANCE_CAP = 20
        self.FRICTION = 0.3
        self.SIZE_RECT = 8
        self.TICK = 30

        pygame.init()
        self.width = width
        self.v_abs_samples = []
        self.height = height
        self.Particles = []
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Alex Particle")
        self.screen.fill(0)
        self.col_thresh = 5
        pygame.display.update()
        self.running = running

        self.clock = pygame.time.Clock()


    def addRandomSpeedParticle(self, x,y):
        self.Particles.append([x,y,(random.random()-0.5)*20,(random.random()-0.5)*20])

    def addParticle(self, x, y):
        self.Particles.append([x,y,0,0])

    def createParticle(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, self.SIZE_RECT, self.SIZE_RECT))

    def getColorFromSpeed(self, vx,vy):
        v_abs = math.sqrt(vx**2 + vy**2)
        self.v_abs_samples.append(v_abs)
        if len(self.v_abs_samples) > 200:
            length = len(self.v_abs_samples)-200
            self.v_abs_samples = self.v_abs_samples[length-150:]
        if v_abs > self.col_thresh:
            a = 255
        else:
            a = 255*v_abs/self.col_thresh
        blue = 255 - a 
        return (a, 0, blue)
    
    def gameLoop(self):
        # defining particles
        bool_addParticle = True
        bool_addFixParticle = True
        self.Particles = []
        for _ in range(50):
            x = 1400*random.random()
            y = 1000*random.random()
            self.Particles.append([x,y,(random.random()-0.5)*20,(random.random()-0.5)*20])
            self.createParticle(x, y, (200,200,200))  

        while self.running:
            # DRAW
            for particle in self.Particles:
                self.createParticle(particle[0],particle[1],self.getColorFromSpeed(particle[2],particle[3]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # ADD MANUAL ATOMS
                if pygame.mouse.get_pressed()[0]:
                    if bool_addParticle:
                        (x,y) = pygame.mouse.get_pos()
                        self.addRandomSpeedParticle(x, y)
                        bool_addParticle = False
                elif not pygame.mouse.get_pressed()[0]:
                    bool_addParticle = True
                elif pygame.mouse.get_pressed()[2]:
                    if bool_addFixParticle:
                        (x,y) = pygame.mouse.get_pos()
                        self.addParticle(x, y)
                        bool_addFixParticle = False
                elif not pygame.mouse.get_pressed()[2]:
                        bool_addFixParticle = True
            for i in range(len(self.Particles)):
                (a_x, a_y, a_vx, a_vy) = self.Particles[i]
                for j in range(len(self.Particles)):
                    if i == j:
                        continue
                    (b_x, b_y) = self.Particles[j][0], self.Particles[j][1]
                    dx = b_x - a_x
                    dy = b_y - a_y
                    d = math.sqrt(dx**2 + dy**2)
                    if d > 0:
                        if d < self.DISTANCE_CAP:
                            F = self.MAX_FORCE/(self.DISTANCE_CAP**2)  
                        else:
                            F = self.MAX_FORCE/(d**2)

                        fx = (dx / d) * F
                        fy = (dy / d) * F
                        a_vx += fx
                        a_vy += fy
                        a_x += a_vx
                        a_y += a_vy

                        self.Particles[i][0] = a_x
                        self.Particles[i][1] = a_y
                        self.Particles[i][2] = a_vx*self.FRICTION
                        self.Particles[i][3] = a_vy*self.FRICTION


                        if self.Particles[i][0] >= 1400 or self.Particles[i][0] <= 0:
                            self.Particles[i][2] *= (-1)
                        if self.Particles[i][1] >= 1000 or self.Particles[i][1] <= 0:
                            self.Particles[i][3] *= (-1)

            self.col_thresh = max(self.v_abs_samples)*0.9
            # updating the display
            pygame.display.update()
            self.clock.tick(self.TICK)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == 'r':
                        self.Particles = []
                        for _ in range(300):
                            x = 1400*random.random()
                            y = 1000*random.random()
                            self.Particles.append([x,y,(random.random()-0.5)*20,(random.random()-0.5)*20])
                            self.createParticle(x, y, (200,200,200))  
                    elif pygame.key.name(event.key) == 'e':
                        self.Particles = []
                        for _ in range(5):
                            x = 1400*random.random()
                            y = 1000*random.random()
                            self.Particles.append([x,y,(random.random()-0.5)*20,(random.random()-0.5)*20])
                            self.createParticle(x, y, (200,200,200))  
                    elif pygame.key.name(event.key) == 'q':
                        self.running = not self.running
                    elif pygame.key.name(event.key) == 'w':
                                self.MAX_FORCE *= 2
                    elif pygame.key.name(event.key) == 's':
                                self.MAX_FORCE *= 1/2
                    elif pygame.key.name(event.key) == 't': 
                                self.FRICTION += 0.1 
                    elif pygame.key.name(event.key) == 'g':
                                self.FRICTION -= 0.1
            self.screen.fill(0)
        pygame.quit()

# the main function


def main():
    particleLife = Game(True, 1400, 1000)
    particleLife.gameLoop()

if __name__ == "__main__":
    main()