import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 500
FPS = 60

VELOCIDADE_JOGADOR = 7
VELOCIDADE_IA = 5
VELOCIDADE_BOLA_X = 6

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("consolas", 32, bold=True)

FUNDO = (5, 8, 14)
BRANCO = (245, 245, 245)
CIANO = (50, 230, 255)
ROXO = (180, 90, 255)
LINHA = (35, 40, 50)

jogador = pygame.Rect(30, 200, 15, 90)
ia = pygame.Rect(755, 200, 15, 90)
bola = pygame.Rect(390, 240, 20, 20)

pontos_jogador = 0
pontos_ia = 0


def reiniciar_bola(direcao):
    """Coloca a bola no centro e define uma nova direção."""
    global velocidade_x, velocidade_y

    bola.center = (LARGURA // 2, ALTURA // 2)
    velocidade_x = VELOCIDADE_BOLA_X * direcao
    velocidade_y = random.choice((-5, 5))

reiniciar_bola(random.choice((-1, 1)))

rodando = True

while rodando:    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
   
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]:
        jogador.y -= VELOCIDADE_JOGADOR

    if teclas[pygame.K_s]:
        jogador.y += VELOCIDADE_JOGADOR

    jogador.clamp_ip(tela.get_rect())
    
    if ia.centery < bola.centery:
        ia.y += VELOCIDADE_IA
    elif ia.centery > bola.centery:
        ia.y -= VELOCIDADE_IA

    ia.clamp_ip(tela.get_rect())
  
    bola.x += velocidade_x
    bola.y += velocidade_y

    if bola.top <= 0:
        bola.top = 0
        velocidade_y *= -1
    elif bola.bottom >= ALTURA:
        bola.bottom = ALTURA
        velocidade_y *= -1

    if bola.colliderect(jogador) and velocidade_x < 0:
        bola.left = jogador.right
        velocidade_x *= -1

    if bola.colliderect(ia) and velocidade_x > 0:
        bola.right = ia.left
        velocidade_x *= -1
    
    if bola.right < 0:
        pontos_ia += 1
        reiniciar_bola(1)
    elif bola.left > LARGURA:
        pontos_jogador += 1
        reiniciar_bola(-1)
    
    tela.fill(FUNDO)

    pygame.draw.line(
        tela,
        LINHA,
        (LARGURA // 2, 0),
        (LARGURA // 2, ALTURA),
        3,
    )

    pygame.draw.rect(tela, CIANO, jogador, border_radius=6)
    pygame.draw.rect(tela, ROXO, ia, border_radius=6)
    pygame.draw.circle(tela, BRANCO, bola.center, 10)

    placar = fonte.render(
        f"{pontos_jogador:02}  {pontos_ia:02}",
        True,
        BRANCO,
    )

    tela.blit(
        placar,
        placar.get_rect(center=(LARGURA // 2, 35)),
    )

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
