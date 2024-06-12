import pygame
import random

class Bola:
    def __init__(self, x, y, tamanho, velocidade_x, velocidade_y):
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.cor = (255, 255, 255)  # Cor inicial da bola (branco)

    def mover(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.velocidade_y = -self.velocidade_y
            self.mudar_direcao()
            self.mudar_cor()

    def resetar_posicao(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.velocidade_x = -self.velocidade_x

    def mudar_direcao(self):
        # Alterar a direção da bola aleatoriamente dentro de certos limites
        self.velocidade_y += random.choice([-1, 1])
        self.velocidade_x += random.choice([-1, 1])

    def mudar_cor(self):
        # Mudar a cor da bola de maneira aleatória
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def diminuir_velocidade(self):
        if self.velocidade_x > 0:
            self.velocidade_x -= 1
        else:
            self.velocidade_x += 1

        if self.velocidade_y > 0:
            self.velocidade_y -= 1
        else:
            self.velocidade_y += 1
