#ui/shared_ui.py
import pygame
from ui.button_ui import ButtonUI
import globals
import constants.global_constants as global_constants
import constants.image_constants as image_constants
from utils.helpers_paths import get_resource_path


class SharedNavigationButtonsMixin:
    def init_nav_buttons(self, include_next=False, include_back=True, include_menu=True, tracking_button_config=None):
        try:
            self.has_next_button = include_next
            self.has_back_button = include_back
            self.has_menu_button = include_menu

            btn_next_path = get_resource_path(global_constants.BackgroundPath,image_constants.btn_next_path)
            btn_back_path = get_resource_path(global_constants.BackgroundPath, image_constants.btn_back_path)
            btn_menu_path = get_resource_path(global_constants.BackgroundPath, image_constants.btn_menu_path)
            #print(f'[SharedNavigationButtonsMixin] init_nav_buttons btn_next_path: {btn_next_path}')

            if self.has_next_button:
                self.next_button = ButtonUI(
                    keyCode=pygame.K_RETURN,
                    text="",
                    x=1150,
                    y=590,
                    is_list=False,
                    isImage=True,
                    image= btn_next_path
                )

            if self.has_back_button:
                self.back_button = ButtonUI(
                    keyCode=pygame.K_ESCAPE,
                    text="Back",
                    x=5,
                    y=2,
                    is_list=False,
                    isImage=True,
                    image=btn_back_path
                )

            if self.has_menu_button:
                self.menu_button = ButtonUI(
                    keyCode=None,
                    text="",
                    x=1150,
                    y=2,
                    is_list=False,
                    isImage=True,
                    image=btn_menu_path
                )

            self.tracking_button = None
            if tracking_button_config:
                image_path = get_resource_path(global_constants.BackgroundPath, tracking_button_config["image"])
                self.tracking_button = ButtonUI(
                    keyCode=None,
                    text="",
                    x=tracking_button_config.get("x", 600),
                    y=tracking_button_config.get("y", 300),
                    is_list=False,
                    isImage=True,
                    image=image_path,
                    init_paint_color=tracking_button_config.get("init_paint_color", (175, 255, 255))
                )
        except Exception as e:
            print(f'[SharedNavigationButtonsMixin] init_nav_buttons exception: {e}')
            raise e


    def input_nav_buttons(self, sm, inputStream):
       try:
            mouse = inputStream.mouse

            if self.has_back_button and self.back_button.rect.collidepoint(mouse.currentPos):
                if mouse.isButtonPressed(0):
                    if hasattr(globals, 'soundManager') and globals.soundManager is not None:
                        globals.soundManager.stopIfPlaying()
                    # Call custom back handler if available
                    if hasattr(self, "on_back_pressed") and callable(self.on_back_pressed):
                        self.on_back_pressed(sm)
                    else:
                        sm.pop()

            if self.has_menu_button and self.menu_button.rect.collidepoint(mouse.currentPos):
                if mouse.isButtonPressed(0):
                    globals.soundManager.stopIfPlaying()
                    print(f'[ui] has_menu_button pressed')
                    print("[DEBUG] Stack before pop_until_unit_scene:", sm.scenes)
                    sm.pop_until_unit_scene()
                    print("[DEBUG] Stack after pop_until_unit_scene:", sm.scenes)

            if self.has_next_button and self.next_button.rect.collidepoint(mouse.currentPos):
                if mouse.isButtonPressed(0):
                    if hasattr(globals, 'soundManager') and globals.soundManager is not None:
                        globals.soundManager.stopIfPlaying()

                    self.on_next_pressed(sm)

            if self.tracking_button and self.tracking_button.visible and self.tracking_button.rect.collidepoint(
                    mouse.currentPos):
                if mouse.isButtonPressed(0):
                    self.tracking_button.visible = False  # ✅ Disappear on click
                    if hasattr(self, "on_tracking_pressed") and callable(self.on_tracking_pressed):
                        self.on_tracking_pressed()

       except Exception as e:
            print(f'[SharedNavigationButtonsMixin] input_nav_buttons exception: {e}')
            raise e

    def update_nav_buttons(self, inputStream):
        try:
            if self.has_back_button:
                self.back_button.update(inputStream, selected=False)
            if self.has_menu_button:
                self.menu_button.update(inputStream, selected=False)
            if self.has_next_button:
                self.next_button.update(inputStream, selected=False)
            if self.tracking_button:
                self.tracking_button.update(inputStream, selected=self.tracking_button.selected)

        except Exception as e:
            print(f'[SharedNavigationButtonsMixin] update_nav_buttons exception: {e}')
            raise e

    def draw_nav_buttons(self, screen):
        try:
            if self.has_back_button:
                self.back_button.draw(screen)
            if self.has_menu_button:
                self.menu_button.draw(screen)
            if self.has_next_button:
                self.next_button.draw(screen)
            if self.tracking_button:
                self.tracking_button.draw(screen)

        except Exception as e:
            print(f'[SharedNavigationButtonsMixin] draw_nav_buttons exception: {e}')
            raise e

    def reset_tracking_button(self):
        if self.tracking_button:
            self.tracking_button.visible = True
