import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont('segoeuiemoji', 24)
letra = pygame.font.Font(None, 34)
grande = pygame.font.Font(None, 48)          

VEL = (-2, -1, 1, 2)
EMOJI = {
    "pedra":   "\U0001FAA8",
    "papel":   "\U0001F4C4",
    "tesoura": "\u2702",
}
VENCE = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}

imagens = {t: fonte.render(e, 1, "white") for t, e in EMOJI.items()}

pecas = []
for i, tipo in enumerate(EMOJI):
    for _ in range(15):
        x = random.randint(i * 200, i * 200 + 170)
        y = random.randint(40, 370)
        v = [random.choice(VEL), random.choice(VEL)]
        pecas.append([tipo, pygame.Rect(x, y, 30, 30), v])


def move(r, v):
    r.move_ip(v)
    if r.left < 0:
        r.left = 0
        v[0] = -v[0]
    elif r.right > 600:
        r.right = 600
        v[0] = -v[0]
    if r.top < 40:
        r.top = 40
        v[1] = -v[1]
    elif r.bottom > 400:
        r.bottom = 400
        v[1] = -v[1]


rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for _, r, v in pecas:
        move(r, v)
    
    for a in pecas:
        for b in pecas:
            if a is b:
                continue
            if a[1].colliderect(b[1]) and VENCE[a[0]] == b[0]:
                b[0] = a[0]

    tela.fill((30, 30, 45))
    for tipo, r, _ in pecas:
        img = imagens[tipo]
        tela.blit(img, img.get_rect(center=r.center))

    tipos = [p[0] for p in pecas]
    for i, tipo in enumerate(EMOJI):
        tela.blit(imagens[tipo], (10 + i * 100, 4))
        qtd = letra.render(str(tipos.count(tipo)), 1, "white")
        tela.blit(qtd, (50 + i * 100, 10))

    if len(set(tipos)) == 1:
        fim = grande.render(f"{tipos[0]} venceu!", 1, "gold")
        caixa = fim.get_rect(center=(300, 220))
        pygame.draw.rect(tela, "black", caixa.inflate(30, 20), 0, 12)
        tela.blit(fim, caixa)

    pygame.display.flip()
    relogio.tick(30)

pygame.quit()