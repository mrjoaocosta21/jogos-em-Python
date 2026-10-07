import pygame

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
T = 40
inicio = pygame.Rect(7 * T, 9 * T, T, T)
sapo = inicio.copy()
setas = {
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0 , 1)
}
faixas = [(5, 3, "gold"), (6, -2, "tomato"),
          (7, 2, "violet"), (8, -3, "orange")]
carros = []
for linha, vel, cor in faixas:
    for x in range(0, 600, 200):
        r = pygame.Rect(x, linha * T + 5, 60, 30)
        carros.append((r, vel, cor))
troncos = []
for linha, vel, in ((1, 1), (2, -2), (3, 1)):
    for x in range(0, 600, 240):
        r = pygame.Rect(x, linha * T + 4, 120, 32)
        troncos.append((r, vel))
chegaram = []

def desenhar_sapo(s):
    corpo = s.inflate(-6, 6)
    pygame.draw.rect(tela, "chartreuse", corpo, 0, 12)
    for lado in (-9, 9):
        olho = (s.centerx + lado, s.top + 10)
        pygame.draw.circle(tela, "white", olho, 6)
        pygame.draw.circle(tela, "black", olho, 3)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key in setas:
                dx, dy = setas[evento.key]
                novo = sapo.move(dx * T, dy * T)
                if tela.get_rect().contains(novo):
                    sapo = novo

    for r, vel, cor in carros:
        r.x = (r.x + vel + 60) % 720 - 60
    na_agua = T <= sapo.y < 4 * T
    for r, vel in troncos:
        r.x = (r.x + vel + 120) % 840 - 120
        if r.collidepoint(sapo.center):
            sapo.x += vel
            na_agua = False
    bateu = sapo.collidelist([c[0] for c in carros]) >= 0
    fora = not tela.get_rect().contains(sapo)
    if bateu or na_agua or fora:
        sapo = inicio.copy()
    if sapo.y == 0:
        chegaram.append(sapo)
        sapo = inicio.copy()

    tela.fill("dimgray")
    tela.fill("royalblue", (0, T, 600, 3 * T))
    for y in (0, 4, 9):
        tela.fill("forestgreen", (0, y * T, 600, T))
    for r, vel in troncos:
        pygame.draw.rect(tela,"saddlebrown", r, 0, 14)
    for r, vel, cor in carros:
        pygame.draw.rect(tela, cor, r, 0, 8)
    for s in chegaram + [sapo]:
        desenhar_sapo(sapo)    
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()