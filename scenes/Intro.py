# scenes/menu/structure_syllable.py
from scenes.core.scenes import Scene
from ui.button_ui import ButtonUI
import pygame
from utils.colors import DARK_GREY
import asyncio
from utils.fontloader import  load_arial_small
from ui.shared_ui import SharedNavigationButtonsMixin

class IntroScene(Scene, SharedNavigationButtonsMixin):
    def __init__(self):
        super().__init__()
        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None
        self.init_nav_buttons()
        self.options_ready = False



    def onEnter(self):
      pass


    def input(self, sm, inputStream, screen=None):
        # Check for 'Q' key press to quit the game
        self.input_nav_buttons(sm, inputStream)
        mouse = inputStream.mouse
        mouse_pos = mouse.currentPos

        # Detect mouse hover and left click on skill options
        for i, button in enumerate(self.list_options):
            if button.rect.collidepoint(mouse_pos):  # Mouse is over this button
                self.optionSelected = i  # Highlight it

                if mouse.isButtonPressed(0):  # Left click
                    self.activate_selection(sm)
                    return


        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            self.activate_selection(sm)

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
        #draw_interspersed_drop_shadow_text(screen, "Estructura de la síl•laba", 170, 50)
        self.draw_nav_buttons(screen)


        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)




