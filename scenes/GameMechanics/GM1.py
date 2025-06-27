# scenes/GM1.py
from system.camera_scanner import CameraScanner
from scenes.core.scenes import Scene
import pygame
import globals
from utils.colors import DARK_GREY
from ui.shared_ui import SharedNavigationButtonsMixin
from utils.color_sequence_checker import are_objects_in_correct_order
from utils.helpers_render import render_check_if_order_correct

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
            self.targets = {}  # <-- Initialize targets
        except Exception as e:
            print(f'[GM1][init] Error: {e}')

    def onEnter(self):
        try:
            # Setup targets based on counter_scene_played
            if globals.counter_scene_played == 0:
                self.targets = {
                    'red': (450, 500),
                    'yellow': (800, 500)
                }
            elif globals.counter_scene_played == 1:
                self.targets = {
                    'yellow': (450, 500),
                    'green': (670, 500),
                    'red': (350, 400)
                }
            elif globals.counter_scene_played == 2:
                self.targets = {
                    'blue': (550, 500),
                    'red': (350, 300),
                    'green': (670, 300),
                    'yellow': (550, 100)
                }
        except Exception as e:
            print(f'[GM1][onEnter] Error: {e}')

    def onExit(self):
        try:
            self.camera_scanner.stop()
        except Exception as e:
            print(f'[GM1][onExit] Error: {e}')

    def input(self, sm, inputStream, screen=None):
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            self.next_level(sm)
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
                    self.order_correct = are_objects_in_correct_order(frame, self.camera_scanner.color_ranges, self.targets)


        except Exception as e:
            print(f'[GM1][update] Error: {e}')


    def next_level(self, sm):
        """Method to handle transition to the next level."""
        print("[GM1] Next level triggered.")
        globals.counter_scene_played += 1
        sm.pop()

    def draw(self, sm, screen):
        try:
            screen.fill((128, 128, 128))  # DARK_GREY
            self.camera_scanner.update(screen)

            outline_size = 300
            border_thickness = 4

            # Dynamic outline positions
            outline_positions = []
            if globals.counter_scene_played == 0:
                outline_positions = [(300, 350), (650, 350)]
            elif globals.counter_scene_played == 1:
                outline_positions = [(250, 350), (650, 350), (450, 150)]
            elif globals.counter_scene_played == 2:
                outline_positions = [(400, 350), (250, 150), (650, 150), (400, 50)]

            # Draw outlines based on positions
            for pos in outline_positions:
                pygame.draw.rect(screen, DARK_GREY, pygame.Rect(pos, (outline_size, outline_size)),
                                 width=border_thickness)

            # Render check mark if correct
            if self.order_correct:
                render_check_if_order_correct(screen, position=(100, 100))

        except Exception as e:
            print(f'[GM1][draw] Error: {e}')
