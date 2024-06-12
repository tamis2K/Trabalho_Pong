import pygame

class Raquete:
    def __init__(self, x, y, largura, altura, velocidade):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = velocidade

    def mover(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 600:
            self.rect.bottom = 600
