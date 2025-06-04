import pygame
import random

class Particle:
    def __init__(self, x, y, color=(0, 120, 255, 180)):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(1, 3)
        self.vx = speed * random.uniform(0.5, 1.0) * random.choice([-1, 1])
        self.vy = speed * random.uniform(0.5, 1.0) * random.choice([-1, 1])
        self.radius = random.randint(4, 7)
        self.life = random.randint(15, 25)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1 
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (self.radius, self.radius), self.radius)
            screen.blit(surf, (self.x - self.radius, self.y - self.radius))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=12, color=(0, 120, 255, 180)):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)