import os
import sys
import pygame
from random import randint

# Ocultar prompt do pygame no terminal
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# --- CONFIGURAÇÕES DA TELA E GRID ---
WIDTH = 1200
HEIGHT = 600
CELL_SIZE = 40
COLS = WIDTH // CELL_SIZE   # 30 colunas
ROWS = HEIGHT // CELL_SIZE  # 15 linhas

# --- Funções Utilitárias ---
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_images(path, prefix, count, scale=1):
    images = []
    for i in range(1, count + 1):
        img_path = os.path.join(path, f"{prefix}{i}.png")
        try:
            image = pygame.image.load(img_path).convert_alpha()
            if scale != 1:
                w, h = image.get_size()
                image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
            images.append(image)
        except FileNotFoundError:
            surf = pygame.Surface((CELL_SIZE, CELL_SIZE))
            surf.fill('Blue') # Cor padrão se faltar a imagem da garota
            images.append(surf)
    return images

# --- Algoritmo de Busca A* (A-Estrela) ---
class Node:
    def __init__(self, col, row, parent=None):
        self.col = col
        self.row = row
        self.parent = parent
        self.g = 0 
        self.h = 0 
        self.f = 0 

def heuristica_manhattan(node_atual, node_objetivo):
    return abs(node_atual.col - node_objetivo.col) + abs(node_atual.row - node_objetivo.row)

def a_star(start_col, start_row, goal_col, goal_row, obstacles):
    start_node = Node(start_col, start_row)
    goal_node = Node(goal_col, goal_row)
    
    open_list = [start_node]
    closed_list = set()
    
    while open_list:
        current_node = min(open_list, key=lambda o: o.f)
        open_list.remove(current_node)
        closed_list.add((current_node.col, current_node.row))
        
        if current_node.col == goal_node.col and current_node.row == goal_node.row:
            path = []
            current = current_node
            while current is not None:
                path.append((current.col, current.row))
                current = current.parent
            return path[::-1]
            
        vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        for move in vizinhos:
            node_col = current_node.col + move[0]
            node_row = current_node.row + move[1]
            
            # Limites da tela inteira
            if node_col < 0 or node_col >= COLS or node_row < 0 or node_row >= ROWS:
                continue
                
            if (node_col, node_row) in obstacles:
                continue
                
            if (node_col, node_row) in closed_list:
                continue
                
            novo_node = Node(node_col, node_row, current_node)
            custo_passo = 1.4 if move[0] != 0 and move[1] != 0 else 1.0 
            novo_node.g = current_node.g + custo_passo
            novo_node.h = heuristica_manhattan(novo_node, goal_node)
            novo_node.f = novo_node.g + novo_node.h
            
            is_in_open = False
            for open_node in open_list:
                if novo_node.col == open_node.col and novo_node.row == open_node.row and novo_node.g > open_node.g:
                    is_in_open = True
                    break
            
            if not is_in_open:
                open_list.append(novo_node)
                
    return None 

# --- Classes Visuais ---
class Player(pygame.sprite.Sprite):
    def __init__(self, start_col, start_row):
        super().__init__()
        self.walk_frames = load_images('./graphics/Girl/walking', 'walk', 12, scale=1)
        self.image = self.walk_frames[0] if self.walk_frames else pygame.Surface((CELL_SIZE, CELL_SIZE))
        
        self.col = start_col
        self.row = start_row
        self.rect = self.image.get_rect(center=self.get_pixel_pos())
        
        self.path = []
        self.path_index = 0
        self.anim_index = 0
        
        self.pixel_x = self.rect.x
        self.pixel_y = self.rect.y
        self.speed = 8 

    def get_pixel_pos(self):
        return (self.col * CELL_SIZE + CELL_SIZE//2, self.row * CELL_SIZE + CELL_SIZE//2)

    def follow_path_smoothly(self):
        if self.path and self.path_index < len(self.path):
            target_col, target_row = self.path[self.path_index]
            target_x = target_col * CELL_SIZE + CELL_SIZE//2 - self.rect.width//2
            target_y = target_row * CELL_SIZE + CELL_SIZE//2 - self.rect.height//2
            
            self.anim_index += 0.3
            if self.anim_index >= len(self.walk_frames):
                self.anim_index = 0
            self.image = self.walk_frames[int(self.anim_index)]
            
            moved = False
            if abs(self.pixel_x - target_x) > self.speed:
                self.pixel_x += self.speed if target_x > self.pixel_x else -self.speed
                moved = True
            else:
                self.pixel_x = target_x
                
            if abs(self.pixel_y - target_y) > self.speed:
                self.pixel_y += self.speed if target_y > self.pixel_y else -self.speed
                moved = True
            else:
                self.pixel_y = target_y
                
            self.rect.x = int(self.pixel_x)
            self.rect.y = int(self.pixel_y)
            
            if not moved:
                self.col = target_col
                self.row = target_row
                self.path_index += 1
                
            return False 
        return True 

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, col, row):
        super().__init__()
        try:
            # Carrega a imagem padronizada do obstáculo
            img = pygame.image.load('./graphics/obstaculo.png').convert_alpha()
        except FileNotFoundError:
            # Se você esquecer de colocar a imagem lá, ele desenha um quadrado vermelho para avisar
            img = pygame.Surface((CELL_SIZE, CELL_SIZE))
            img.fill('#FF5252')
            
        # Ajusta a imagem para caber perfeitamente no bloco do grid
        self.image = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(col * CELL_SIZE, row * CELL_SIZE))

class FinishLine(pygame.sprite.Sprite):
    def __init__(self, col, row):
        super().__init__()
        try:
            img = pygame.image.load('./graphics/chegada.png').convert_alpha()
            self.image = pygame.transform.scale(img, (80, 250))
            self.rect = self.image.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2))
        except:
            self.image = pygame.Surface((CELL_SIZE, CELL_SIZE * 3))
            self.image.fill('#4CAF50')
            self.rect = self.image.get_rect(center=(col * CELL_SIZE + CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2))

# --- Jogo Principal ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Simulação A* (A-Estrela)')
        self.clock = pygame.time.Clock()
        
        try:
            font_path = resource_path('./font/Pixeltype.ttf')
            self.custom_font = pygame.font.Font(font_path, size=50)
            self.small_font = pygame.font.Font(font_path, size=35)
        except:
            self.custom_font = pygame.font.SysFont(None, 50)
            self.small_font = pygame.font.SysFont(None, 35)

        self.state = 'START'
        
        # Início e fim centralizados verticalmente
        self.start_pos = (1, ROWS // 2) 
        self.goal_pos = (COLS - 3, ROWS // 2) 
        
        self.obstacles_pos = []
        self.show_path_line = True 

    def gerar_mapa_aleatorio(self):
        """Gera 'paredões' com buracos forçando a IA a costurar o mapa."""
        self.obstacles_pos.clear()
        
        col_atual = 5
        while col_atual < COLS - 5:
            # Sorteia onde fica o buraco na parede e o tamanho dele
            buraco_y = randint(1, ROWS - 5)
            tamanho_buraco = randint(3, 5) # 3 a 5 blocos de espaço para passar
            
            for row in range(ROWS):
                # Se a linha atual não fizer parte do buraco, coloca um obstáculo
                if not (buraco_y <= row < buraco_y + tamanho_buraco):
                    self.obstacles_pos.append((col_atual, row))
            
            # Pula de 4 a 6 colunas para criar o próximo paredão
            col_atual += randint(4, 6)

    def setup_sprites(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(self.start_pos[0], self.start_pos[1])
        self.player_group.add(self.player)
        
        self.obstacle_group = pygame.sprite.Group()
        for col, row in self.obstacles_pos:
            # Chama o obstáculo sem precisar passar tipo (mosca/caracol)
            self.obstacle_group.add(Obstacle(col, row))
            
        self.finish_group = pygame.sprite.GroupSingle()
        self.finish_group.add(FinishLine(self.goal_pos[0], self.goal_pos[1]))

    def run_ai(self):
        path = a_star(self.start_pos[0], self.start_pos[1], self.goal_pos[0], self.goal_pos[1], self.obstacles_pos)
        
        if path:
            self.player.path = path
            self.player.path_index = 0
            self.state = 'MOVING'
        else:
            # Se gerar um mapa impossível por acidente, tenta de novo
            self.gerar_mapa_aleatorio()
            self.setup_sprites()
            self.run_ai()

    def draw_path_line(self):
        if self.player.path and self.show_path_line:
            for i in range(len(self.player.path) - 1):
                p1 = (self.player.path[i][0] * CELL_SIZE + CELL_SIZE//2, self.player.path[i][1] * CELL_SIZE + CELL_SIZE//2)
                p2 = (self.player.path[i+1][0] * CELL_SIZE + CELL_SIZE//2, self.player.path[i+1][1] * CELL_SIZE + CELL_SIZE//2)
                pygame.draw.line(self.screen, 'Red', p1, p2, 4)

    def draw_grid(self):
        """Desenha uma grade sutil de fundo para dar cara de laboratório de IA"""
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, '#E0E0E0', (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, '#E0E0E0', (0, y), (WIDTH, y))

    def run(self):
        while True:
            # Fundo branco "Clean"
            self.screen.fill('#F8F9FA') 
            self.draw_grid()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if self.state in ['START', 'VICTORY'] and event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.gerar_mapa_aleatorio()
                    self.setup_sprites()
                    self.run_ai()
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    self.show_path_line = not self.show_path_line

            if self.state == 'START':
                text = self.custom_font.render("Pressione 1 para Gerar Labirinto e Iniciar IA", False, 'Black')
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT // 2 - 50))
            
            elif self.state == 'MOVING':
                self.draw_path_line()
                
                info_text = self.small_font.render("Algoritmo: A* (A-Estrela) | Heuristica: Manhattan | Aperte 'H' para esconder a linha", False, 'Black')
                self.screen.blit(info_text, (20, 20))
                
                chegou = self.player.follow_path_smoothly()
                if chegou:
                    self.state = 'VICTORY'
            
            elif self.state == 'VICTORY':
                self.draw_path_line()
                text = self.custom_font.render("OBJETIVO ALCANCADO! (Pressione 1 para novo labirinto)", False, '#4CAF50')
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))

            if self.state != 'START':
                self.finish_group.draw(self.screen)
                self.obstacle_group.draw(self.screen)
                self.player_group.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    jogo = Game()
    jogo.run()