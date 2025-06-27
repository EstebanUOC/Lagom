# scenes/GM1.py
from system.camera_scanner import CameraScanner
from scenes.core.scenes import Scene
from ui.button_ui import ButtonUI
import pygame
import globals
from utils.colors import DARK_GREY
from ui.shared_ui import SharedNavigationButtonsMixin
from utils.drawing import drawImage, draw_interspersed_drop_shadow_text
from utils.helpers_paths import get_resource_path
import constants.global_constants as global_constants
import constants.image_constants as image_constants
from utils.color_sequence_checker import are_objects_in_correct_order
from utils.helpers_render import render_check_if_order_correct
# scenes/GM1.py

class GM1Scene(Scene, SharedNavigationButtonsMixin):
    def __init__(self):
        try:
            super().__init__()
            self.camera_scanner = CameraScanner()
            self.activate_buttons = False
            self.button_already_selected = False
            self.btn_correct = None
            self.nomenclature = None
            self.current_index = None
            self.init_nav_buttons(include_next=True, include_back=True, include_menu=True)
            self.order_correct = False



        except Exception as e:
            print(f'[GM1][init] Error: {e}')


    def onEnter(self):
        try:
            pass



        except Exception as e:
            print(f'[GM1][onEnter] Error: {e}')


    def onExit(self):
        try:
            self.camera_scanner.stop()
        except Exception as e:
            print(f'[GM1][onExit] Error: {e}')


    def input(self, sm, inputStream, screen=None):


        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
           pass

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop_multiple(2)

        if inputStream.keyboard.isKeyPressed(pygame.K_q):
            pass

    def update(self, sm, inputStream):
        try:
            self.order_correct = False  # Reset each frame

            camera_entity = next((e for e in globals.world.entities if hasattr(e, "camera")), None)
            if camera_entity:
                frame = self.camera_scanner.get_current_frame(camera_entity)
                if frame is not None:
                    targets = {
                        'blue': (450, 500),
                        'yellow': (880, 500)
                    }
                    self.order_correct = are_objects_in_correct_order(frame, self.camera_scanner.color_ranges, targets)

                    if self.order_correct:
                        print("[GM1] ✅ Objects correct - popping scene.")
                        globals.counter_scene_played += 1
                        sm.pop()

        except Exception as e:
            print(f'[GM1][update] Error: {e}')

    def draw(self, sm, screen):
        try:
            screen.fill((128, 128, 128))  # DARK_GREY
            self.camera_scanner.update(screen)

            # Draw a 200x200 gray-outlined square with transparent inside
            outline1_pos = (250, 350)  # position on screen
            outline2_pos = (650, 350)  # position on screen
            outline_size = 300
            border_thickness = 4  # thickness of the border

            pygame.draw.rect(screen, DARK_GREY, pygame.Rect(outline1_pos, (outline_size, outline_size)),
                             width=border_thickness)

            pygame.draw.rect(screen, DARK_GREY, pygame.Rect(outline2_pos, (outline_size, outline_size)),
                             width=border_thickness)
            # Get frame for rendering condition
            camera_entity = next((e for e in globals.world.entities if hasattr(e, "camera")), None)
            if camera_entity:
                frame = self.camera_scanner.get_current_frame(camera_entity)
                if frame is not None:
                    targets = {
                        'blue': (450, 500),
                        'yellow': (880, 500)
                    }

                    if self.order_correct:
                        render_check_if_order_correct(screen, position=(100, 100))
        except Exception as e:
            print(f'[GM1][draw] Error: {e}')



