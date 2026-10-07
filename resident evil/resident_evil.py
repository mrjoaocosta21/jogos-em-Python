import pygame
import random

pygame.init()
tela = pygame.display.set_mode(600, 400)
relogio = pygame.time.Clock()
estrelas = [(random.randint(0, 599),
             random.randint(0, 399)) for _ in range(60)]

def sprite(desenho, cor):
    img = pygame.Surface((len(desenho[0]) * 3,
                          len(desenho) * 3),
                          pygame.SRCALPHA)
    for y, linha in enumerate(desenho):
        for x, c in enumerate(linha):
            if c == "#":
                img.fill(cor, (x * 3, y * 3, 3, 3))
    return img

nave = sprite(["......#......",
               ".....###.....",
               ".###########.",
               "#############",
               "#############"], (80, 230, 120))
x = 300

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    x += (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * 5
    x = max(30,)