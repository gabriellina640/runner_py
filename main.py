import os
import sys
import pygame
from random import randint, choice

# Ocultar prompt do pygame no terminal
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

user_name = input("Projeto feito para da matéria de Inteligência Artificial, Professora Ana Marina. Digite seu nome para começar: ")

# --- Funções Utilitárias ---
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_images(path, prefix, count, scale=2):
    images = []
    for i in range(1, count + 1):
        img_path = os.path.join(path, f"{prefix}{i}.png")
        try:
            image = pygame.image.load(img_path).convert_alpha()
            if scale == 2:
                image = pygame.transform.scale2x(image)
            elif scale != 1:
                w, h = image.get_size()
                image = pygame.transform.scale(image, (w * scale, h * scale))
            images.append(image)
        except FileNotFoundError:
            surf = pygame.Surface((50, 50))
            surf.fill('Red')
            images.append(surf)
    return images

# --- Classes dos Atores (Sprites) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_index = 0
        self.player_jumping_index = 0
        self.gravity = 0
        
        self.player_walk = load_images('./graphics/Girl/walking', 'walk', 12, scale=1)
        self.player_jumping = load_images('./graphics/Girl/jumping', 'jumping', 4, scale=1)

        self.image = self.player_walk[self.player_index] if self.player_walk else pygame.Surface((50,50))
        self.rect = self.image.get_rect(midbottom=(80, 300))

        try:
            self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
            self.jump_sound.set_volume(0.1)
        except FileNotFoundError:
            self.jump_sound = None

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -16
            if self.jump_sound:
                self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.player_jumping_index += 0.15
            if self.player_jumping_index >= len(self.player_jumping):
                self.player_jumping_index = len(self.player_jumping) - 1
            self.image = self.player_jumping[int(self.player_jumping_index)]
        else:
            self.player_index += 0.25
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

    def reset_position(self):
        self.rect.midbottom = (80, 300)
        self.gravity = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        self.animation_index = 0
        
        if obstacle_type == 'fly':
            try:
                fly_1 = pygame.image.load('./graphics/Fly/Fly1.png').convert_alpha()
                fly_2 = pygame.image.load('./graphics/Fly/Fly2.png').convert_alpha()
                self.frames = [fly_1, fly_2]
            except FileNotFoundError:
                surf = pygame.Surface((40, 30))
                surf.fill('Blue')
                self.frames = [surf, surf]
            y_pos = 210
        else:
            try:
                snail_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
                snail_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
                self.frames = [snail_1, snail_2]
            except FileNotFoundError:
                surf = pygame.Surface((50, 40))
                surf.fill('Green')
                self.frames = [surf, surf]
            y_pos = 300

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(900, y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self, current_speed):
        self.animation_state()
        self.rect.x -= current_speed
        if self.rect.x <= -100:
            self.kill()

class FinishLine(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('./graphics/chegada.png').convert_alpha()
        except FileNotFoundError:
            print("Aviso: ./graphics/chegada.png não encontrada.")
            self.image = pygame.Surface((50, 300))
            self.image.fill('Yellow')
            
        self.rect = self.image.get_rect(midbottom=(700, 300))

# --- Classe Gerenciadora do Jogo ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Runner')
        self.clock = pygame.time.Clock()
        
        try:
            font_path = resource_path('./font/Pixeltype.ttf')
            self.custom_font = pygame.font.Font(font_path, size=50)
        except FileNotFoundError:
            self.custom_font = pygame.font.SysFont(None, 50)

        self.state = 'START' 
        self.start_time = 0
        self.score = 0
        self.target_score = 30 
        self.current_speed = 6
        
        # --- SISTEMA DE CONFETES ---
        self.confetti = [] # Lista para guardar os pedaços de confete
        self.colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff']
        
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, randint(900, 1500)) 

        try:
            self.sky_surf = pygame.image.load('./graphics/Sky.png').convert()
            self.ground_surf = pygame.image.load('./graphics/ground.png').convert()
            self.game_over_surf = pygame.transform.scale(
                pygame.image.load('./graphics/game_over1.png').convert_alpha(), (800, 400)
            )
            self.game_start_surf = pygame.transform.scale(
                pygame.image.load('./graphics/game_start.png').convert_alpha(), (800, 400)
            )
        except FileNotFoundError:
            self.sky_surf = pygame.Surface((800, 400)); self.sky_surf.fill('LightBlue')
            self.ground_surf = pygame.Surface((800, 100)); self.ground_surf.fill('Brown')
            self.game_over_surf = pygame.Surface((800, 400)); self.game_over_surf.fill('Black')
            self.game_start_surf = pygame.Surface((800, 400)); self.game_start_surf.fill('Black')

        self.start_info = self.custom_font.render("Press 1 to START", False, 'Yellow')
        self.start_info_rect = self.start_info.get_rect(midtop=(400, 10))
        self.restart_info = self.custom_font.render("Press 1 to Restart", False, 'Yellow')

        self.player_group = pygame.sprite.GroupSingle()
        self.player_sprite = Player()
        self.player_group.add(self.player_sprite)
        self.obstacle_group = pygame.sprite.Group()
        self.finish_line_group = pygame.sprite.GroupSingle()

    def display_score(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surf = self.custom_font.render(f'Score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(400, 50))
        self.screen.blit(score_surf, score_rect)
        return current_time

    # --- FUNÇÃO GERADORA DE CONFETES ---
    def draw_confetti(self):
        # A cada frame, tem uma chance de criar novos confetes no topo da tela
        if randint(0, 10) > 2: # Controla a quantidade de confete caindo
            x = randint(0, 800)
            y = -10
            speed_y = randint(2, 6)
            speed_x = randint(-2, 2)
            color = choice(self.colors)
            size = randint(4, 10)
            # Guarda: [x, y, speed_x, speed_y, cor, tamanho]
            self.confetti.append([x, y, speed_x, speed_y, color, size])

        # Atualiza a posição e desenha os confetes que já existem
        for particle in self.confetti[:]:
            particle[0] += particle[2] # Move de lado
            particle[1] += particle[3] # Cai (gravidade do confete)
            
            # Desenha o retangulo na tela
            pygame.draw.rect(self.screen, particle[4], (particle[0], particle[1], particle[5], particle[5]))
            
            # Remove o confete da lista se ele passar do chão para não pesar a memória
            if particle[1] > 400:
                self.confetti.remove(particle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.state == 'START':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.state = 'PLAYING'
                    self.start_time = int(pygame.time.get_ticks() / 1000)

            elif self.state == 'PLAYING':
                if event.type == self.obstacle_timer and self.score < self.target_score:
                    self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                    novo_tempo = randint(900, 1600)
                    pygame.time.set_timer(self.obstacle_timer, novo_tempo)

            elif self.state in ['GAME_OVER', 'VICTORY']:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.state = 'PLAYING'
                    self.start_time = int(pygame.time.get_ticks() / 1000)
                    self.player_sprite.reset_position()
                    self.current_speed = 6
                    self.finish_line_group.empty()
                    self.obstacle_group.empty()
                    self.confetti.clear() # Limpa os confetes antigos
                    pygame.time.set_timer(self.obstacle_timer, randint(900, 1500))

    def draw_start_screen(self):
        self.screen.blit(self.game_start_surf, (0, 0))
        self.screen.blit(self.start_info, self.start_info_rect)

    def draw_playing_screen(self):
        self.screen.blit(self.sky_surf, (0, 0))
        self.screen.blit(self.ground_surf, (0, 300))
        self.score = self.display_score()
        
        self.current_speed = 6 + (self.score // 5)
        
        if self.score >= self.target_score:
            self.state = 'FINISHING'
            self.obstacle_group.empty() 
            self.finish_line_group.add(FinishLine()) 

        self.player_group.draw(self.screen)
        self.player_group.update()
        
        self.obstacle_group.update(self.current_speed)
        self.obstacle_group.draw(self.screen)
        
        if pygame.sprite.spritecollide(self.player_group.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            self.state = 'GAME_OVER'

    def draw_finishing_screen(self):
        self.screen.blit(self.sky_surf, (0, 0))
        self.screen.blit(self.ground_surf, (0, 300))
        
        self.finish_line_group.draw(self.screen)
        
        self.player_group.draw(self.screen)
        self.player_group.update()
        
        # Chama a chuva de confetes!
        self.draw_confetti()
        
        # O personagem anda sozinho, ignorando inputs do teclado
        self.player_sprite.rect.x += 3
        
        if pygame.sprite.spritecollide(self.player_sprite, self.finish_line_group, False):
            self.state = 'VICTORY'

    def draw_game_over_screen(self):
        self.screen.blit(self.game_over_surf, (0, 0))
        self.screen.blit(self.restart_info, (250, 20))

        player_name = self.custom_font.render(f'Hello {user_name}', False, 'Yellow')
        score_info = self.custom_font.render(f'Your Score: {self.score}', False, 'Yellow')
        self.screen.blit(player_name, (280, 340))
        self.screen.blit(score_info, (280, 370))

    def draw_victory_screen(self):
        self.screen.fill('#84a59d') 
        
        # Mantém a chuva de confetes na tela final!
        self.draw_confetti()
        
        victory_text = self.custom_font.render('VOCE VENCEU!', False, 'White')
        self.screen.blit(victory_text, (280, 150))
        
        score_info = self.custom_font.render(f'Final Score: {self.score}', False, 'White')
        self.screen.blit(score_info, (280, 200))
        
        restart_text = self.custom_font.render("Press 1 to Play Again", False, 'White')
        self.screen.blit(restart_text, (250, 280))

    def run(self):
        while True:
            self.handle_events()

            if self.state == 'START':
                self.draw_start_screen()
            elif self.state == 'PLAYING':
                self.draw_playing_screen()
            elif self.state == 'FINISHING':
                self.draw_finishing_screen()
            elif self.state == 'GAME_OVER':
                self.draw_game_over_screen()
            elif self.state == 'VICTORY':
                self.draw_victory_screen()

            pygame.display.update()
            self.clock.tick(60)

# --- Execução do Jogo ---
if __name__ == '__main__':
    jogo = Game()
    jogo.run()