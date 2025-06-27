from scenes.core.scenes import Scene
import pygame
from utils.colors import DARK_GREY
from ui.shared_ui import SharedNavigationButtonsMixin
from utils.drawing import drawImage, draw_interspersed_drop_shadow_text
from scenes.GameMechanics.GM1 import GM1Scene
import globals

class OrderScene(Scene, SharedNavigationButtonsMixin):
    def __init__(self):
        super().__init__()
        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None
        self.init_nav_buttons(include_next=True, include_back=True, include_menu=True)
        self.options_ready = False
        self.image_order = None



    def onEnter(self):
      if globals.counter_scene_played == 0:
          self.image_order = pygame.image.load('assets/GUI/Order/order_1.png')



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
            print('[OrderScene] Enter pressed')
            sm.push(GM1Scene())

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
        drawImage(screen, self.image_order, 0, 0)
        draw_interspersed_drop_shadow_text(screen, "Order Scene", 550, 50)

        self.draw_nav_buttons(screen)

        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)

