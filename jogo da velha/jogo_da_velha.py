import pygame
import sys
import random

pygame.init()

# Cores do jogo
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (0, 0, 255)     # Cor do X
RED = (255, 0, 0)      # Cor do O

# Dimensões da janela
largura = 300
altura = 370 # Aumentei um pouco para acomodar o placar e rodapé
linha_espessura = 15

# Criar janela e controle de FPS
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Velha com Menu e Placar")
clock = pygame.time.Clock() # Melhoria 1: Controle de processamento

# Inicialização do estado do jogo
tabuleiro = [[None]*3 for _ in range(3)]
jogador_atual = "X"
game_over = False
estado_jogo = "MENU" 
modo_jogo = None     

# Sistema de Placar (Melhoria 2)
placar = {"X": 0, "O": 0, "Empates": 0}

# Fontes
fonte_grande = pygame.font.SysFont(None, 80)
fonte_media = pygame.font.SysFont(None, 35)
fonte_pequena = pygame.font.SysFont(None, 22)

def desenhar_linhas():
    pygame.draw.line(tela, BLACK, (100, 0), (100, 300), linha_espessura)
    pygame.draw.line(tela, BLACK, (200, 0), (200, 300), linha_espessura)
    pygame.draw.line(tela, BLACK, (0, 100), (300, 100), linha_espessura)
    pygame.draw.line(tela, BLACK, (0, 200), (300, 200), linha_espessura)
    pygame.draw.line(tela, BLACK, (0, 300), (300, 300), 5)

def desenhar_simb():
    for linha in range(3):
        for coluna in range(3):
            simbolo = tabuleiro[linha][coluna]
            if simbolo is not None:
                cor = BLUE if simbolo == "X" else RED
                texto = fonte_grande.render(simbolo, True, cor)
                pos_x = coluna * 100 + 50
                pos_y = linha * 100 + 50
                texto_rect = texto.get_rect(center=(pos_x, pos_y))
                tela.blit(texto, texto_rect)

# Desenha as informações e o placar no rodapé da janela
def desenhar_rodape(mensagem):
    # Fundo do rodapé
    pygame.draw.rect(tela, LIGHT_GRAY, (0, 302, 300, 68))
    
    # Texto de status (turno/vitória)
    texto_msg = fonte_pequena.render(mensagem, True, BLACK)
    tela.blit(texto_msg, texto_msg.get_rect(center=(largura // 2, 320)))
    
    # Exibição do Placar
    txt_placar = f"X: {placar['X']}  |  Velha: {placar['Empates']}  |  O: {placar['O']}"
    texto_plc = fonte_pequena.render(txt_placar, True, (80, 80, 80))
    tela.blit(texto_plc, texto_plc.get_rect(center=(largura // 2, 348)))

def checar_vencedor():
    for linha in tabuleiro:
        if linha.count(linha[0]) == 3 and linha[0] is not None:
            return linha[0]
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] and tabuleiro[0][col] is not None:
            return tabuleiro[0][col]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None:
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None:
        return tabuleiro[0][2]    
    return None

def checar_empate():
    for linha in tabuleiro:
        if None in linha:
            return False
    return True

# Melhoria 3: IA Inteligente (Tenta vencer ou bloquear o jogador)
def jogada_ia():
    global jogador_atual, game_over
    casas_vazias = []
    for l in range(3):
        for c in range(3):
            if tabuleiro[l][c] is None:
                casas_vazias.append((l, c))
                
    if not casas_vazias or game_over:
        return

    # 1. Tenta vencer: simula a própria jogada da IA ("O")
    for l, c in casas_vazias:
        tabuleiro[l][c] = "O"
        if checar_vencedor() == "O":
            finalizar_turno_ia()
            return
        tabuleiro[l][c] = None # Desfaz se não vencer

    # 2. Tenta bloquear: simula a jogada do Humano ("X") para evitar a vitória dele
    for l, c in casas_vazias:
        tabuleiro[l][c] = "X"
        if checar_vencedor() == "X":
            tabuleiro[l][c] = "O" # Bloqueia colocando o O ali
            finalizar_turno_ia()
            return
        tabuleiro[l][c] = None # Desfaz se não for ameaça

    # 3. Se não puder vencer nem bloquear, escolhe uma casa aleatória
    linha, coluna = random.choice(casas_vazias)
    tabuleiro[linha][coluna] = "O"
    finalizar_turno_ia()

def finalizar_turno_ia():
    global game_over, jogador_atual
    vencedor = checar_vencedor()
    if vencedor:
        placar[vencedor] += 1
        game_over = True       
    elif checar_empate():
        placar["Empates"] += 1
        game_over = True
    else:
        jogador_atual = "X"

def reiniciar_jogo():
    global tabuleiro, jogador_atual, game_over
    tabuleiro = [[None]*3 for _ in range(3)]
    jogador_atual = "X"
    game_over = False

def desenhar_menu():
    tela.fill(WHITE)
    titulo = fonte_media.render("JOGO DA VELHA", True, BLACK)
    tela.blit(titulo, titulo_rect := titulo.get_rect(center=(largura // 2, 60)))
    
    # Botão 1
    pygame.draw.rect(tela, GRAY, (40, 130, 220, 50), border_radius=10)
    txt_pvp = fonte_pequena.render("1 vs 1 (Local)", True, BLACK)
    tela.blit(txt_pvp, txt_pvp.get_rect(center=(largura // 2, 155)))
    
    # Botão 2
    pygame.draw.rect(tela, GRAY, (40, 210, 220, 50), border_radius=10)
    txt_pve = fonte_pequena.render("Contra Computador", True, BLACK)
    tela.blit(txt_pve, txt_pve.get_rect(center=(largura // 2, 235)))

# Loop Principal
while True:
    clock.tick(60) # Garante que o jogo não passe de 60 atualizações por segundo
    
    if estado_jogo == "MENU":
        desenhar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 40 <= mx <= 260 and 130 <= my <= 180:
                    modo_jogo = "PvP"
                    estado_jogo = "JOGANDO"
                    placar = {"X": 0, "O": 0, "Empates": 0} # Zera o placar geral ao mudar de modo
                    reiniciar_jogo()
                if 40 <= mx <= 260 and 210 <= my <= 260:
                    modo_jogo = "PvE"
                    estado_jogo = "JOGANDO"
                    placar = {"X": 0, "O": 0, "Empates": 0}
                    reiniciar_jogo()

    elif estado_jogo == "JOGANDO":
        tela.fill(WHITE)
        desenhar_linhas()
        desenhar_simb()
        
        vencedor = checar_vencedor()
        if vencedor:
            msg_rodape = f"Jogador {vencedor} Venceu! [Espaço]"
        elif checar_empate():
            msg_rodape = "Deu Velha! Empate. [Espaço]"
        else:
            msg_rodape = f"Turno do jogador: {jogador_atual}"
            
        desenhar_rodape(msg_rodape)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                if y < 300:
                    coluna = x // 100
                    linha = y // 100
                    
                    if tabuleiro[linha][coluna] is None:
                        tabuleiro[linha][coluna] = jogador_atual
                        vencedor = checar_vencedor()
                        
                        if vencedor:
                            placar[vencedor] += 1
                            game_over = True       
                        elif checar_empate():
                            placar["Empates"] += 1
                            game_over = True
                        else:
                            jogador_atual = "O" if jogador_atual == "X" else "X"
                            
                        if modo_jogo == "PvE" and jogador_atual == "O" and not game_over:
                            pygame.display.update() # Força desenho do 'X' do jogador humano antes da IA pensar
                            pygame.time.wait(250) 
                            jogada_ia()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and game_over:
                    reiniciar_jogo()
                if evento.key == pygame.K_ESCAPE:
                    estado_jogo = "MENU"

    pygame.display.update()