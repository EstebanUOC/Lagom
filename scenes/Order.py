from scenes.core.scenes import Scene
import pygame
from utils.colors import DARK_GREY
from utils.drawing import drawImage, draw_interspersed_drop_shadow_text
from scenes.GameMechanics.GM1 import GM1Scene
import globals
from constants.audio_constants import background_music
import soundmanager
from scenes.leaderboard import LeaderBoard

class OrderScene(Scene):
    def __init__(self):
        super().__init__()
        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None

        self.options_ready = False
        self.image_order = None
        self.finished_session = False



    def onEnter(self):

        globals.soundManager.add_music('background_music', background_music)
        globals.soundManager.playMusicFade('background_music')

        if globals.counter_scene_played == 0:
            self.image_order = pygame.image.load('assets/GUI/Order/0.jpg')
        elif globals.counter_scene_played == 1:
            self.image_order = pygame.image.load('assets/GUI/Order/1.jpg')
        elif globals.counter_scene_played == 2:
            self.image_order = pygame.image.load('assets/GUI/Order/2.jpg')
        elif globals.counter_scene_played >= 3:
            self.finished_session = True


        print('[OrderScene] onEnter load_activity globals.counter_scene_played :', globals.counter_scene_played)



    def input(self, sm, inputStream, screen=None):
        # Check for 'Q' key press to quit the game
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

        if self.finished_session:
            sm.push(LeaderBoard())

        for i in range(len(self.list_options)):
            if self.optionSelected == i:
                self.list_options[i].update(inputStream, True)
            else:
                self.list_options[i].update(inputStream, False)

    def draw(self, sm, screen):
        screen.fill(DARK_GREY)
        drawImage(screen, self.image_order, 0, 0)
        draw_interspersed_drop_shadow_text(screen, "Order Scene", 550, 50)



        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)


