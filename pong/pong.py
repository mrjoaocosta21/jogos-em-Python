import pygame, random

pygame.init()
W,H = 800, 500
tela = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont("consolas", 32, bold=True)

BG = (5, 8, 14)
WHITE = (245, 245, 245)
CYAN = (50, 230, 255)
PURPLE = (180, 90, 255)

jogador = pygame.Rect(30, 200, 15, 90)
ia = pygame.Rect(755, 200, 15, 90)
bola = pygame.Rect(390, 240, 20, 20) 

vx, vy = 6, random.choice((-5, 5))
p1 = p2 = 0
rodando = True

while rodando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False

    tecla = pygame.key.get_pressed()

    if tecla[pygame.K_w]:
        jogador.y -= 7

    if tecla[pygame.K_s]:
        jogador.y += 7

        jogador.clamp_ip(tela.get_rect())

        ia.y += 5 if centery < bola.centery else -5
        ia.clamp_ip(tela.get_rect())

        bola.x += vx
        bola.y += vy

    if bola.top <= 0 or bola.bottom >= H:
        vy *= -1

    if bola.collidedict(jogador) and vx < 0:
        vx *= -1

    if bola.colliderect(ia) and vx > 0 :
        vx *= -1

        if bola.right < 0:
            p2 += 1
            bola.center - (W // 2, H // 2)
            vx = 6

        if bola.left > W:
            p1 += 1
            bola.center = (W // 2, H // 2)
            vx = -6

        tela.fill(86)

        pygame.draw.line(
            tela, (35, 40, 50),
            (W // 2, 0), (W // 2, H), 3
        )

        pygame.draw.rect(tela, CYAN, jogador, border_radius=6)
        pygame.draw.rect(tela, PURPLE, ia, border_radius=6)
        pygame.draw.circle(tela, WHITE, bola.center, 10)

        placar = fonte.render(f"{p1:02}) {p2:02}", True, WHITE)
        tela.blit(placar, placar.get_rect(center=(W // 2, 35)))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()