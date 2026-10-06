import pygame as pg
import random
import sys

class Snake_game:
    def __init__(self):
        # Cores do Jogo
        self.color = {
            'black': (15, 15, 15),
            'gray': (50, 50, 50),
            'light_gray': (150, 150, 150),
            'white': (255, 255, 255),
            'red': (230, 40, 40),
            'green': (40, 230, 40),
            'blue': (40, 40, 230)
        }

        # Inicializar fontes
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", 40, bold=True)
        self.font_small = pg.font.SysFont("Courier New", 25, bold=True)

        self.map_size = (53, 30)
        self.grid_size = 24  # Tamanho de cada bloco (Janela será 1272 x 720)
        
        self.reset_game()

    def reset_game(self):
        self.snake_position = [(25, 15), (26, 15), (27, 15)]
        self.snake_direction = (-1, 0)
        self.next_direction = (-1, 0)  # Evita virar na direção oposta instantaneamente
        self.score = 0
        self.end_game = False
        self.sort_apple_position()

    def snake_change_direction(self, event_key):
        if event_key in [pg.K_w, pg.K_UP] and self.snake_direction != (0, 1):
            self.next_direction = (0, -1)
        elif event_key in [pg.K_a, pg.K_LEFT] and self.snake_direction != (1, 0):
            self.next_direction = (-1, 0)
        elif event_key in [pg.K_s, pg.K_DOWN] and self.snake_direction != (0, -1):
            self.next_direction = (0, 1)
        elif event_key in [pg.K_d, pg.K_RIGHT] and self.snake_direction != (-1, 0):
            self.next_direction = (1, 0)

    def sort_apple_position(self):
        # Melhoria: Garante que a maçã não nasça dentro do corpo da cobra
        while True:
            x = random.randint(0, self.map_size[0] - 1)
            y = random.randint(0, self.map_size[1] - 1)
            self.apple_position = (x, y)
            if self.apple_position not in self.snake_position:
                break

    def update_snake_position(self):
        if self.end_game:
            return

        self.snake_direction = self.next_direction
        
        # Move a cabeça
        new_head = (
            self.snake_position[0][0] + self.snake_direction[0],
            self.snake_position[0][1] + self.snake_direction[1]
        )
        
        # Insere nova cabeça
        self.snake_position.insert(0, new_head)

        # Verifica se comeu a maçã
        if new_head == self.apple_position:
            self.score += 1
            self.sort_apple_position()
        else:
            # Se não comeu, remove a cauda para manter o tamanho estável
            self.snake_position.pop()

    def check_collisions(self):
        head = self.snake_position[0]
        # 1. Colisão com as bordas
        if head[0] < 0 or head[1] < 0 or head[0] >= self.map_size[0] or head[1] >= self.map_size[1]:
            self.end_game = True

        # 2. Colisão com si mesma
        if head in self.snake_position[1:]:
            self.end_game = True

    def draw_elements(self, window):
        # Desenhar Maçã
        apple_rect = pg.Rect(self.apple_position[0] * self.grid_size, self.apple_position[1] * self.grid_size, self.grid_size, self.grid_size)
        pg.draw.rect(window, self.color['red'], apple_rect, border_radius=5)

        # Desenhar Cobra
        for i, pos in enumerate(self.snake_position):
            snake_rect = pg.Rect(pos[0] * self.grid_size, pos[1] * self.grid_size, self.grid_size, self.grid_size)
            # Cabeça tem tom de verde diferente do corpo
            cor = (50, 255, 50) if i == 0 else self.color['green']
            pg.draw.rect(window, cor, snake_rect, border_radius=4)

        # Desenhar Placar
        score_text = self.font.render(f'Score: {self.score}', True, self.color['white'])
        window.blit(score_text, (20, 20))


# --- GERENCIADOR DE INTERFACE NATIVA DO PYGAME ---
class Game_Manager:
    def __init__(self):
        self.width = 1272
        self.height = 720
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Snake Game Melhorado")
        self.clock = pg.time.Clock()
        self.state = "MENU" # MENU, JOGANDO, PAUSA, FIM DE JOGO
        self.game = Snake_game()
        
        # Evento customizado para controlar a velocidade da cobra (Cobra se move a cada 100ms)
        self.SNAKE_MOVE = pg.USEREVENT
        pg.time.set_timer(self.SNAKE_MOVE, 100)

    def run(self):
        while True:
            self.clock.tick(60) # Roda a interface a 60 FPS estáveis
            
            if self.state == "MENU":
                self.screen_menu()
            elif self.state == "JOGANDO":
                self.screen_game()
            elif self.state == "PAUSA":
                self.screen_pause()
            elif self.state == "FIM DE JOGO":
                self.screen_game_over()

    def screen_menu(self):
        self.window.fill(self.game.color['black'])
        
        title = self.game.font.render("O JOGO DA COBRINHA", True, self.game.color['green'])
        start_lbl = self.game.font_small.render("Pressione [ESPAÇO] para iniciar", True, self.game.color['white'])
        
        self.window.blit(title, title.get_rect(center=(self.width//2, self.height//2 - 50)))
        self.window.blit(start_lbl, start_lbl.get_rect(center=(self.width//2, self.height//2 + 30)))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.game.reset_game()
                    self.state = "JOGANDO"

    def screen_game(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self.game.snake_change_direction(event.key)
                if event.key == pg.K_ESCAPE:
                    self.state = "PAUSA"
            if event.type == self.SNAKE_MOVE:
                self.game.update_snake_position()
                self.game.check_collisions()
                if self.game.end_game:
                    self.state = "FIM DE JOGO"

        self.window.fill(self.game.color['black'])
        self.game.draw_elements(self.window)
        pg.display.update()

    def screen_pause(self):
        # Desenha a tela de pausa com efeito transparente sobre o jogo parado
        pause_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        pause_surface.fill((0, 0, 0, 5)) # Leve escurecimento parcial
        self.window.blit(pause_surface, (0,0))

        title = self.game.font.render("JOGO PAUSADO", True, self.game.color['blue'])
        resume_lbl = self.game.font_small.render("Pressione [ESC] para continuar ou [M] para o Menu", True, self.game.color['white'])
        
        self.window.blit(title, title.get_rect(center=(self.width//2, self.height//2 - 40)))
        self.window.blit(resume_lbl, resume_lbl.get_rect(center=(self.width//2, self.height//2 + 30)))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.state = "JOGANDO"
                if event.key == pg.K_m:
                    self.state = "MENU"

    def screen_game_over(self):
        self.window.fill(self.game.color['black'])
        
        title = self.game.font.render("FIM DE JOGO!", True, self.game.color['red'])
        score_lbl = self.game.font_small.render(f"Pontuação Final: {self.game.score}", True, self.game.color['white'])
        restart_lbl = self.game.font_small.render("Pressione [ESPAÇO] para reiniciar ou [M] para ir ao Menu", True, self.game.color['light_gray'])
        
        self.window.blit(title, title.get_rect(center=(self.width//2, self.height//2 - 60)))
        self.window.blit(score_lbl, score_lbl.get_rect(center=(self.width//2, self.height//2)))
        self.window.blit(restart_lbl, restart_lbl.get_rect(center=(self.width//2, self.height//2 + 60)))
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.game.reset_game()
                    self.state = "JOGANDO"
                if event.key == pg.K_m:
                    self.state = "MENU"

if __name__ == "__main__":
    manager = Game_Manager()
    manager.run()