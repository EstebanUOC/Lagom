# scenes/menu/structure_syllable.py
import globals
from scenes.core.scenes import Scene
import pygame
from utils.colors import DARK_GREY
from ui.shared_ui import SharedNavigationButtonsMixin
from utils.drawing import draw_interspersed_drop_shadow_text
from scenes.Order import OrderScene
from utils.loaders import load_activity

class IntroScene(Scene, SharedNavigationButtonsMixin):
    def __init__(self):
        super().__init__()
        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None
        self.init_nav_buttons(include_next=True, include_back=False, include_menu=False)
        self.options_ready = False

    def onEnter(self):
        load_activity()
        print('[IntroScene] onEnter load_activity')
        print(f'[IntroScene] onEnter globals.world: {globals.world}')
        print(f'[IntroScene] onEnter globals.world.entities: {globals.world.entities:}')


    def input(self, sm, inputStream, screen=None):
        # Check for 'Q' key press to quit the game
        self.input_nav_buttons(sm, inputStream)
        mouse = inputStream.mouse
        mouse_pos = mouse.currentPos

        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            print('[IntroScene] Enter pressed')
            sm.push(OrderScene())

        if inputStream.keyboard.isKeyPressed(pygame.K_q):
            #exit_game()
            pass

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()
            #sm.push(FadeTransitionScene([self], []))
        if inputStream.keyboard.isKeyPressed(pygame.K_UP):
            if self.optionSelected > 0:
                self.optionSelected -= 1
                #print(f'up {self.optionSelected}')
        if inputStream.keyboard.isKeyPressed(pygame.K_DOWN):
            if self.optionSelected < 2:
                self.optionSelected += 1
                #print(f'down {self.optionSelected}')



    def update(self, sm, inputStream):
        self.update_nav_buttons(inputStream)


        for i in range(len(self.list_options)):
            if self.optionSelected == i:
                self.list_options[i].update(inputStream, True)
            else:
                self.list_options[i].update(inputStream, False)

    def draw(self, sm, screen):
        screen.fill(DARK_GREY)
        #drawImage(screen, self.menu_path, 0, 0)
        draw_interspersed_drop_shadow_text(screen, "Intro", 550, 50)
        self.draw_nav_buttons(screen)

        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)




