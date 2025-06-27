import globals
from scenes.core.scenes import Scene
import pygame
from ui.shared_ui import SharedNavigationButtonsMixin
from scenes.Order import OrderScene
from utils.loaders import load_activity
from scenes.leaderboard import LeaderBoard


class IntroScene(Scene):
    def __init__(self):
        super().__init__()

        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None
        self.options_ready = False

        # --- NOVO ---
        self.w, self.h = 1280, 720
        self.font_size = int(0.05 * self.w)
        self.font = pygame.font.Font("assets\Fonts\Dongle-Regular.ttf", self.font_size)

        # background
        self.background = pygame.image.load('assets/GUI/Background/bg.jpg')

        self.background = pygame.transform.scale(self.background, (self.w, self.h))

        # textBox
        ri_w_p, ri_h_p = 0.70, 0.10
        ri_w, ri_h = int(self.w * ri_w_p), int(self.h * ri_h_p)
        ri_x = (self.w - ri_w) // 2
        ri_y = int(self.h * 0.80) - ri_h
        self.input_box = pygame.Rect(ri_x, ri_y, ri_w, ri_h)

        # Button
        b_w_p, b_h_p = 0.40, 0.10
        b_w, b_h = int(self.w * b_w_p), int(self.h * b_h_p)
        b_x = (self.w - b_w) // 2
        b_y = int(self.h * 0.95) - b_h
        self.button = pygame.Rect(b_x, b_y, b_w, b_h)


        # estado do input
        self.input_text = ""
        self.placeholder = "Insert your nickname..."
        self.placeholder_color = (160, 160, 160)
        self.active = True
        self.max_chars = 20
        # --------------

    def onEnter(self):
        load_activity()
        print('[IntroScene] onEnter load_activity')
        print(f'[IntroScene] onEnter globals.world: {globals.world}')
        print(f'[IntroScene] onEnter globals.world.entities: {globals.world.entities:}')

    def input(self, sm, inputStream, screen=None):

        mouse = inputStream.mouse
        mouse_pos = mouse.currentPos

        # ---  input box---
        for event in inputStream.typed_characters:
            if event == "BACKSPACE":
                self.input_text = self.input_text[:-1]
            elif event == "RETURN":
                if self.input_text:
                    self.start_game(sm)
            elif len(self.input_text) < self.max_chars:
                self.input_text += event

        if inputStream.mouse.isButtonPressed(0):  # botao esquerdo clicado nesta frame
            mouse_pos = inputStream.mouse.currentPos
            if self.button.collidepoint(mouse_pos) and self.input_text:
                self.start_game(sm)
        # ----------------------------------------------

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            print('[IntroScene] Enter pressed')
            sm.push(OrderScene())

        if inputStream.keyboard.isKeyPressed(pygame.K_l):
            sm.push(LeaderBoard())

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()

        if inputStream.keyboard.isKeyPressed(pygame.K_UP):
            if self.optionSelected > 0:
                self.optionSelected -= 1

        if inputStream.keyboard.isKeyPressed(pygame.K_DOWN):
            if self.optionSelected < 2:
                self.optionSelected += 1

    def update(self, sm, inputStream):


        for i in range(len(self.list_options)):
            if self.optionSelected == i:
                self.list_options[i].update(inputStream, True)
            else:
                self.list_options[i].update(inputStream, False)

    def draw(self, sm, screen):
        # Fundo com a imagem
        screen.blit(self.background, (0, 0))

        # Texto das regras em múltiplas linhas
        rules_text = "1. Memorize\n2. Replicate hands only with no Help\n3. Check your results in the leaderboard"
        rules_lines = rules_text.split('\n')

        t_x = (self.w - int(self.w * 0.8)) // 2
        t_y = int(self.h * 0.33)
        line_height = self.font.get_height()

        y_offset = t_y
        for line in rules_lines:
            line_surf = self.font.render(line, True, (0, 0, 0))
            screen.blit(line_surf, (t_x, y_offset))
            y_offset += line_height

        # Caixa de input (com placeholder se estiver vazia)
        if self.input_text:
            txt_surface = self.font.render(self.input_text, True, (0, 0, 0))
        else:
            txt_surface = self.font.render(self.placeholder, True, self.placeholder_color)
        pygame.draw.rect(screen, (200, 200, 200), self.input_box, 2)
        text_rect = txt_surface.get_rect(center=self.input_box.center)
        screen.blit(txt_surface, text_rect)

        # Botão Start
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(screen, self.button, "Start", self.font, mouse_pos)




        # Desenhar opções anteriores (se houver)
        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)

    def draw_button(self, surface, rect, text, font, mouse_pos):
        color = (100, 200, 255) if rect.collidepoint(mouse_pos) else (70, 130, 180)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

    def start_game(self, sm):
        print("Started game with name:", self.input_text)
        globals.nickname = self.input_text
        globals.timer = pygame.time.get_ticks()
        sm.push(OrderScene())