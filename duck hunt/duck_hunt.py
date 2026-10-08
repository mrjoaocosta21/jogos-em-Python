import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 36)
pygame.mouse.set_visible(False)
pontos = 0
tiro, tiro_ate =(0,0), 0

def novo_pato():
    x = random.randint(150, 400)
    vx = random.choice([-4, 4])
    return pygame.Rect(x, 270, 44, 30), [vx,-3]

pato, vel = novo_pato()
estado = "voando"
balas = 3

def desenhar_pato(r, lado, agora):
    pygame.draw.ellipse(tela, "sienna", r)
    cx, cy = r.centerx + lado * 20, r.top + 2
    bico = (cx + lado * 12, cy + 3)
    pygame.draw.circle(tela, "orange", bico, 7)
    pygame.draw.circle(tela, "darkgreen", (cx, cy), 11)
    olho = (cx + lado * 3, cy - 3)
    pygame.draw.circle(tela, "white", olho, 3)
    asa = -16 if agora // 120 % 2 else 4
    asa = (r.centerx - 14, r.centery + asa, 24, 14)
    pygame.draw.ellipse(tela, "saddlebrown", asa)

def desenhar_cachorro(x, t, rindo):
    y = 330 - min(t // 4, 90)
    if rindo:
        y += t // 100 % 2 * 6
    cabeca = (x - 30, y, 60, 70)
    pygame.draw.ellipse(tela, "chocolate", cabeca)
    for lado in (-1, 1):
        orelha = (x + lado * 30 -10, y + 10, 20, 40)
        pygame.draw.ellipse(tela, "saddlebrown", orelha)
        olho = (x + lado * 12, y + 22)
        pygame.draw.circle(tela, "black", olho, 5)
    focinho = (x - 16, y + 34, 32, 26)
    pygame.draw.ellipse(tela, "tan", focinho)
    pygame.draw.circle(tela, "black", (x, y + 38), 7)
    if rindo:
        boca = (x - 10, y + 48, 20, 12)
        pygame.draw.ellipse(tela, "darkred", boca)
    else:
        r = pygame.Rect(x - 22, y - 30, 44, 30)
        desenhar_pato(r, 1, 0)

rodando = True
while rodando:
    agora = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        clicou = evento.type == pygame.MOUSEBUTTONDOWN
        if clicou and estado == "voando" and balas > 0:
            balas -= 1
            tiro, tiro_ate = evento.pos, agora + 80
            if pato.collidepoint(evento.pos):
                estado, vel = "caindo", [0, 7]
                pontos += 1

    pato.move_ip(vel)
    if estado == "voando":        
        if pato.left < 0 or pato.right > 600:
            vel[0] = -vel[0]
        if pato.top < 0 or pato.bottom > 300:
            vel[1] = -vel[1]
        if balas == 0:
            estado, vel = "fugindo", [0, -6]

    if estado == "caindo" and pato.top > 320:
        estado, inicio, rindo = "cachorro", agora, False
    if estado == "fugindo" and pato.bottom < 0:
        estado, inicio, rindo = "cachorro", agora, True
    if estado == "cachorro" and agora - inicio > 1800:
        pato, vel = novo_pato()
        estado, balas = "voando", 3

    tela.fill("skyblue")
    pygame.draw.rect(tela, "peru", (60, 170, 26, 150))
    pygame.draw.circle(tela, "darkgreen", (73, 150), 60)

    if estado == "cachorro":
        t = agora - inicio
        desenhar_cachorro(pato.centerx, t, rindo)
    else:
        lado = 1 if vel[0] >= 0 else -1
        desenhar_pato(pato, lado, agora)
    pygame.draw.rect(tela, "olivedrab", (0, 310, 600, 90))
    pygame.draw.rect(tela, "sienna", (0, 360, 600, 40))
    texto = f"Pontos: {pontos} Balas: {balas}"
    img = fonte.render(texto, True, "white")
    tela.blit(img, (16, 368))
    if agora < tiro_ate:
        pygame.draw.circle(tela, "yellow", tiro, 22)
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(tela, "red", (mx, my), 18, 3)
    for dx, dy in ((26, 0), (0, 26)):
        a, b = (mx - dx, my - dy), (mx + dx, my + dy)
        pygame.draw.line(tela, "red", a, b, 3)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
    
