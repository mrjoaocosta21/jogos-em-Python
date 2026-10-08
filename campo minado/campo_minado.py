import pygame
import random

pygame.init()

LARGURA = 600
ALTURA = 400
TAMANHO_CASA = 40
COLUNAS = LARGURA // TAMANHO_CASA
LINHAS = ALTURA // TAMANHO_CASA
QUANTIDADE_MINAS = 22

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Campo Minado")
relogio = pygame.time.Clock()
fonte = pygame.font.Font(None, 40)
fonte_fim = pygame.font.Font(None, 64)

casas = [(x, y) for x in range(COLUNAS) for y in range(LINHAS)]
minas = set(random.sample(casas, QUANTIDADE_MINAS))
abertas = set()
bandeiras = set()

perdeu = False
ganhou = False

cores = [None, "blue", "green4", "red", "navy", "maroon", "teal", "black", "gray"]


def vizinhas(casa):
    """Retorna as casas vizinhas válidas de uma posição."""
    lista = []
    x, y = casa

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):          
            if dx == 0 and dy == 0:
                continue

            vizinha = (x + dx, y + dy)

            if vizinha in casas:
                lista.append(vizinha)

    return lista

def numero(casa):
    """Conta quantas minas existem ao redor da casa."""
    return len(minas.intersection(vizinhas(casa)))


def abrir(casa):
    """Abre uma casa e expande automaticamente regiões sem minas próximas."""
    fila = [casa]

    while fila:
        atual = fila.pop()

        if atual in abertas or atual in bandeiras:
            continue

        abertas.add(atual)

        if atual not in minas and numero(atual) == 0:
            fila.extend(vizinhas(atual))


def alternar_bandeira(casa):
    """Coloca ou remove uma bandeira de uma casa fechada."""
    if casa in abertas:
        return

    if casa in bandeiras:
        bandeiras.remove(casa)
    else:
        bandeiras.add(casa)


rodando = True

while rodando:    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and not perdeu and not ganhou:
            x, y = evento.pos
            casa = (x // TAMANHO_CASA, y // TAMANHO_CASA)
            
            if evento.button == 3:
                alternar_bandeira(casa)
            
            elif evento.button == 1:
                abrir(casa)

                if casa in minas and casa in abertas:
                    perdeu = True

                elif len(abertas) == len(casas) - len(minas):
                    ganhou = True
    
    tela.fill("gray20")
    mouse = pygame.mouse.get_pos()
    
    for casa in casas:
        x, y = casa
        retangulo = pygame.Rect(
            x * TAMANHO_CASA,
            y * TAMANHO_CASA,
            TAMANHO_CASA,
            TAMANHO_CASA,
        )
        retangulo = retangulo.inflate(-2, -2)
        
        if casa in minas and perdeu:
            pygame.draw.rect(tela, "orange", retangulo, border_radius=5)
            pygame.draw.circle(tela, "black", retangulo.center, 9)
        
        elif casa in abertas:
            pygame.draw.rect(tela, "gainsboro", retangulo, border_radius=5)

            quantidade = numero(casa)

            if quantidade:
                imagem = fonte.render(str(quantidade), True, cores[quantidade])
                posicao = imagem.get_rect(center=retangulo.center)
                tela.blit(imagem, posicao)
        
        else:
            cor_casa = "steelblue"

            if retangulo.collidepoint(mouse) and not perdeu and not ganhou:
                cor_casa = "lightskyblue"
            
            if ganhou and casa in minas:
                cor_casa = "mediumseagreen"

            pygame.draw.rect(tela, cor_casa, retangulo, border_radius=5)
            
            if casa in bandeiras:
                centro_x, centro_y = retangulo.center
                cabo = (centro_x - 8, centro_y - 13, 3, 26)
                pygame.draw.rect(tela, "black", cabo)

                pontos = [
                    (centro_x - 5, centro_y - 13),
                    (centro_x + 11, centro_y - 6),
                    (centro_x - 5, centro_y + 1),
                ]
                pygame.draw.polygon(tela, "red", pontos)
    
    if perdeu:
        texto = fonte_fim.render("DERROTA!", True, "red")
        sombra = fonte_fim.render("DERROTA!", True, "black")
        posicao = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

        tela.blit(sombra, posicao.move(2, 2))
        tela.blit(texto, posicao)

    elif ganhou:
        texto = fonte_fim.render("VITÓRIA!", True, "lawngreen")
        sombra = fonte_fim.render("VITÓRIA!", True, "black")
        posicao = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))

        tela.blit(sombra, posicao.move(2, 2))
        tela.blit(texto, posicao)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
