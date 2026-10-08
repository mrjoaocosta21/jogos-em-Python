import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 38)
y = 231
partes = [
    (111, 0, 36, 26), (107, 6, 12, 45),
    (118, 30, 26, 6), (91, 38, 34, 25),
    (78, 49, 49, 29),
    (85, 76, 10, 24), (108, 76, 10, 24),
    (122, 46, 9, 7)
]
vel = 0
cactos = []
pontuados = set()
quadro = 0
pontos = 0

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and y == 231:
                vel = -13

    vel += 0.8
    y = min(231, y + vel)
    if y == 231:
        vel = 0      

    quadro += 1
    if quadro % 65 == 1:
        altura = random.choice([38, 50])
        cactos.append(pygame.Rect(600, 331-altura, 20, altura))

    velocidade = min(10, 5 + pontos)
    for cacto in cactos[:]:
        cacto.x -= velocidade
        chave = id(cacto)
        if cacto.right < 54 and chave not in pontuados:
            pontuados.add(chave)
            pontos += 1
        if cacto.right < -7:
            cactos.remove(cacto)
            pontuados.discard(chave)

    corpo = pygame.Rect(78, int(y)+38, 49, 62)
    cabeca = pygame.Rect(107, int(y), 40, 36)
    cauda_hit = pygame.Rect(54, int(y)+44, 26, 28)
    partes_hit = (corpo, cabeca, cauda_hit)
    if any(c.colliderect(p) for c in cactos
           for p in partes_hit):
        y, vel, pontos, quadro = 231, 0, 0, 0
        cactos.clear()
        pontuados.clear()

    tela.fill("white")
    pygame.draw.rect(tela, "black", (0, 331, 600, 3))
    for x, dy, largura, altura in partes:
        pygame.draw.rect(tela, "#535353", (x, y+dy, largura, altura))
    cauda = [(54, y+44), (59, y+60), (80, y+72), (80, y+52)]
    pygame.draw.polygon(tela, "#535353", cauda) 
    pygame.draw.rect(tela, "white", (117, y+8, 5, 5))
    for cacto in cactos:
        pygame.draw.rect(tela, "black", cacto)
        braco = (cacto.x-7, cacto.y+17, 8, 7)
        pygame.draw.rect(tela, "black", braco)
        braco = (cacto.x-7, cacto.y+9, 5, 15)
        pygame.draw.rect(tela, "black", braco)
    placar = fonte.render(f"Pontos: {pontos}", 1, "black")
    tela.blit(placar, (20, 18)) 
    ritmo = fonte.render(f"Vel: {velocidade}", 1, "black")
    tela.blit(ritmo, (475, 18))
    pygame.display.flip()
    relogio.tick(30)

pygame.quit()               