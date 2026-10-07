import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
pygame.mouse.set_visible(False)

def novo_pato():
    x = random.randint(150, 400)
    vx = random.choice([-4, 4])
    return pygame.Rect(x, 270, 44, 30), [vx,-3]

pato, vel = novo_pato()

def desenhar_pato()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill("skyblue")
    pygame.draw.rect(tela, "peru", (60, 170, 26, 150))
    pygame.draw.circle(tela, "darkgreen", (73, 150), 60)
    pygame.draw.rect(tela, "olivedrab", (0, 310, 600, 90))
    pygame.draw.rect(tela, "sienna", (0, 360, 600, 40))
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(tela, "red", (mx, my), 18, 3)
    for dx, dy in ((26, 0), (0, 26)):
        a, b = (mx - dx, my - dy), (mx + dx, my + dy)
        pygame.draw.line(tela, "red", a, b, 3)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
    
