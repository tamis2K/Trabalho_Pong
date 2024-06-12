import pygame
from raquete import Raquete
from bola import Bola
from pygame import mixer
import sys
import time

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
largura = 800
altura = 600

screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong")


pygame.init()  

# Configuração da fonte
font_file = "font/PressStart2P-Regular.ttf"
font = pygame.font.Font(font_file, 36)
fonte_score = pygame.font.Font(font_file, 16)


some = mixer.Sound("audios/Sound_A.wav")

clock = pygame.time.Clock()

class JogoPong:
    def __init__(self):
        self.raquete_player_1 = Raquete(largura - 20, altura // 2 - 30, 10, 60, 5)
        self.raquete_pc = Raquete(10, altura // 2 - 30, 10, 60, 5)
        self.bolas = [Bola(largura // 2 - 5, altura // 2 - 5, 10, 3, 3)]
        self.score_player_1 = 0
        self.score_pc = 0
        self.vencedor = ""
        self.controle = False
        self.rodando = True
        self.tempo_inicial = time.time()
        self.tempo_ultima_bola = time.time()
        self.tempo_ultimo_aumento_velocidade = time.time()
        self.tempo_ultima_diminuicao_velocidade = time.time()

    def menu_principal(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.controle = True
                        return
            # Renderiza o texto do menu
            screen.fill(PRETO)
            texto_menu = font.render("Pong", True, BRANCO)
            text_menu_rect = texto_menu.get_rect(center=(largura // 2, altura // 2))
            screen.blit(texto_menu, text_menu_rect)

            tempo = pygame.time.get_ticks()
            if tempo % 2000 < 1000:
                texto_iniciar = font.render("Pressione Espaço", True, BRANCO)
                texto_iniciar_rect = texto_iniciar.get_rect(center=(largura // 2, 450))
                screen.blit(texto_iniciar, texto_iniciar_rect)

            clock.tick(1)
            pygame.display.flip()

    def fim_jogo(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.controle = True
                        self.posicao_inicial()
                        return
            # Renderiza o texto do menu
            screen.fill(PRETO)
            texto_fim = font.render(f"Vencedor: {self.vencedor}", True, BRANCO)
            text_fim_rect = texto_fim.get_rect(center=(largura // 2, altura // 2))
            screen.blit(texto_fim, text_fim_rect)

            pygame.display.flip()

    def posicao_inicial(self):
        self.raquete_pc.rect.topleft = (10, altura // 2 - self.raquete_pc.rect.height // 2)
        self.raquete_player_1.rect.topright = (largura - 20, altura // 2 - self.raquete_player_1.rect.height // 2)
        self.bolas = [Bola(largura // 2 - 5, altura // 2 - 5, 10, 3, 3)]
        self.score_player_1 = 0
        self.score_pc = 0
        self.tempo_inicial = time.time()
        self.tempo_ultima_bola = time.time()
        self.tempo_ultimo_aumento_velocidade = time.time()
        self.tempo_ultima_diminuicao_velocidade = time.time()

    def adicionar_bola(self):
        nova_bola = Bola(largura // 2 - 5, altura // 2 - 5, 10, 3, 3)
        self.bolas.append(nova_bola)

    def aumentar_velocidade(self):
        for bola in self.bolas:
            if bola.velocidade_x > 0:
                bola.velocidade_x += 1
            else:
                bola.velocidade_x -= 1
            if bola.velocidade_y > 0:
                bola.velocidade_y += 1
            else:
                bola.velocidade_y -= 1

    def diminuir_velocidade(self):
        for bola in self.bolas:
            bola.diminuir_velocidade()

    def rodar(self):
        self.menu_principal()
        self.posicao_inicial()

        while self.rodando:
            if not self.controle:
                self.fim_jogo()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.rodando = False

                screen.fill(PRETO)

                # Movendo as bolas
                for bola in self.bolas:
                    bola.mover()

                # Colisão das bolas com as raquetes
                for bola in self.bolas:
                    if bola.rect.colliderect(self.raquete_pc.rect) or bola.rect.colliderect(self.raquete_player_1.rect):
                        bola.velocidade_x = -bola.velocidade_x
                        bola.mudar_direcao()
                        bola.mudar_cor()
                        some.play()

                    # Posicionar a bola no início do jogo
                    if bola.rect.left <= 0:
                        bola.resetar_posicao(largura // 2 - bola.rect.width // 2, altura // 2 - bola.rect.height // 2)
                        self.score_player_1 += 1
                        if self.score_player_1 == 5:
                            self.vencedor = "Player 1"
                            self.controle = False

                    if bola.rect.right >= largura:
                        bola.resetar_posicao(largura // 2 - bola.rect.width // 2, altura // 2 - bola.rect.height // 2)
                        self.score_pc += 1
                        if self.score_pc == 5:
                            self.vencedor = "PC"
                            self.controle = False

                # Movendo a raquete do pc para seguir a bola mais próxima
                bola_mais_proxima = min(self.bolas, key=lambda b: abs(b.rect.centery - self.raquete_pc.rect.centery))
                if self.raquete_pc.rect.centery < bola_mais_proxima.rect.centery:
                    self.raquete_pc.mover(self.raquete_pc.velocidade)
                elif self.raquete_pc.rect.centery > bola_mais_proxima.rect.centery:
                    self.raquete_pc.mover(-self.raquete_pc.velocidade)

                # Controle Teclado do Player_1
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and self.raquete_player_1.rect.top > 0:
                    self.raquete_player_1.mover(-self.raquete_player_1.velocidade)
                if keys[pygame.K_DOWN] and self.raquete_player_1.rect.bottom < altura:
                    self.raquete_player_1.mover(self.raquete_player_1.velocidade)

                # Mostrar Score no jogo
                score_texto = fonte_score.render(f"Score PC: {self.score_pc}       Score Player_1: {self.score_player_1}", True, BRANCO)
                score_rect = score_texto.get_rect(center=(largura // 2, 30))
                screen.blit(score_texto, score_rect)

                # Desenhar elementos do jogo
                pygame.draw.rect(screen, BRANCO, self.raquete_pc.rect)
                pygame.draw.rect(screen, BRANCO, self.raquete_player_1.rect)
                for bola in self.bolas:
                    pygame.draw.ellipse(screen, bola.cor, bola.rect)
                pygame.draw.aaline(screen, BRANCO, (largura // 2, 0), (largura // 2, altura))

                # Adicionar nova bola a cada 20 segundos
                if time.time() - self.tempo_ultima_bola >= 20:
                    self.adicionar_bola()
                    self.tempo_ultima_bola = time.time()

                # Aumentar velocidade das bolas a cada 20 segundos
                if time.time() - self.tempo_ultimo_aumento_velocidade >= 30:
                    self.aumentar_velocidade()
                    self.tempo_ultimo_aumento_velocidade = time.time()

                # Diminuir velocidade das bolas a cada 40 segundos
                if time.time() - self.tempo_ultima_diminuicao_velocidade >= 60:
                    self.diminuir_velocidade()
                    self.tempo_ultima_diminuicao_velocidade = time.time()

                pygame.display.flip()

                clock.tick(60)

        pygame.quit()
        sys.exit()
