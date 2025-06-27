# scenes/GM1.py
from system.camera_scanner import CameraScanner
from scenes.core.scenes import Scene
import pygame
import globals
from utils.colors import DARK_GREY
from utils.color_sequence_checker import are_objects_in_correct_order
from utils.helpers_render import render_check_if_order_correct
from constants.audio_constants import fast_music
import asyncio
import globals
import time

class GM1Scene(Scene):
    def __init__(self):
        super().__init__()
        self.correct_answer = False
        self.waiting = False
        self.font = pygame.font.SysFont(None, 72)
        self.camera_scanner = CameraScanner()


    def onEnter(self):
        try:
            if globals.start_time is None:
                globals.start_time = time.time()  # Start timer once

            # Setup targets based on counter_scene_played
            globals.soundManager.add_music('background_music', fast_music)
            globals.soundManager.playMusicFade('background_music')

            self.order_correct = False
            self.waiting = False

            if globals.counter_scene_played == 0:
                self.targets = {
                    'red': (450, 500),
                    'yellow': (800, 500)
                }
            elif globals.counter_scene_played == 1:
                self.targets = {
                    'yellow': (450, 500),
                    'green': (670, 500),
                    'red': (450, 400)
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
        if self.waiting:
            return  # Block input while waiting

        if inputStream.keyboard.isKeyPressed(pygame.K_c):
            self.handle_correct(sm)

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            print("[GM1Scene] Escape pressed, going back to previous scene.")
            sm.pop()



    def update(self, sm, inputStream):
        try:
            self.order_correct = False  # Reset each frame

            camera_entity = next((e for e in globals.world.entities if hasattr(e, "camera")), None)
            if camera_entity:
                frame = self.camera_scanner.get_current_frame(camera_entity)
                if frame is not None:
                    self.order_correct = are_objects_in_correct_order(frame, self.camera_scanner.color_ranges, self.targets)

            if self.order_correct and not self.waiting:
                self.handle_correct(sm)

        except Exception as e:
            print(f'[GM1][update] Error: {e}')

    def handle_correct(self, sm):
        print("[GM1Scene] Correct answer triggered!")
        self.order_correct = True
        self.waiting = True
        asyncio.run_coroutine_threadsafe(self.delayed_scene_change(sm), globals.asyncio_loop)

    async def delayed_scene_change(self, sm):
        print("[GM1Scene] Showing 'done' image for 3 seconds...")
        await asyncio.sleep(3)
        print("[GM1Scene] Transitioning to next scene.")
        globals.counter_scene_played += 1
        sm.pop()  # Or sm.push(NextScene()) if advancing

    def next_level(self, sm):
        """Method to handle transition to the next level."""
        print("[GM1] Next level triggered.")
        globals.counter_scene_played += 1
        sm.pop()

    def draw(self, sm, screen):
        try:
            screen.fill((211, 211, 211))  # DARK_GREY
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
                outline_positions = [(500, 400), (150, 150), (800, 150), (500, 50)]

            # Draw outlines based on positions
            for pos in outline_positions:
                pygame.draw.rect(screen, DARK_GREY, pygame.Rect(pos, (outline_size, outline_size)),
                                 width=border_thickness)


            if self.waiting:
                # Show the "done" image
                print("[GM1Scene] Drawing check mark for correct order.")
                render_check_if_order_correct(screen, position=(100, 100))
            else:
                print("[GM1Scene] Drawing targets.")


            # Draw timer at top-right corner
            if globals.start_time is not None:
                elapsed = int(time.time() - globals.start_time)
                timer_text = self.font.render(f"Time: {elapsed}s", True, (0, 0, 0))
                screen.blit(timer_text, (screen.get_width() - timer_text.get_width() - 20, 20))

        except Exception as e:
            print(f'[GM1][draw] Error: {e}')

