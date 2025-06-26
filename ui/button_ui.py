#ui/button_ui.py
import pygame
from constants.global_constants import FONT_ARIAL_ROUNDED_MT_BOLD
from utils.colors import WHITE, AQUA, SCREAMING_GREEN, GREEN
from utils.drawing import draw_interspersed_drop_shadow_text

pygame.font.init()

class ButtonUI:
    def __init__(self, keyCode, text, x, y, is_list=False, isImage=False, image=None, font=None, init_paint_color=None):
        try:
            self.keyCode = keyCode
            self.text = text
            self.x = x
            self.y = y
            self.selected = False
            self.pressed = False
            self.on = False
            self.timer = 40
            self.isList = is_list
            self.isImage = isImage
            self.image = image
            self.init_paint_color = init_paint_color  # This is safe and generic
            self.visible = True  # Default to visible
            self.font = None
            self.hovered = False  # New flag to track mouse hover
            # ✅ Define clickable area (rect) for mouse input
            if self.isImage and self.image:
                try:
                    image_surface = pygame.image.load(self.image).convert_alpha()
                    self.rect = pygame.Rect(self.x, self.y, image_surface.get_width(), image_surface.get_height())
                except Exception as e:
                    print(f"[ButtonUI] Failed to load image for rect: {self.image} – {e}")
                    self.rect = pygame.Rect(self.x, self.y, 100, 50)  # Fallback size
            else:
                text_width, text_height = self.font.size(self.text)
                self.rect = pygame.Rect(self.x, self.y, text_width, text_height)

        except Exception as e:
            print(f'Exception {e} in ButtonUI.__init__() image: {self.image} text: {self.text}')
            raise e

    def update(self, inputStream, selected=False):
        try:
            self.selected = selected
            self.pressed = False
            if self.keyCode is not None:
                self.pressed = inputStream.keyboard.isKeyPressed(self.keyCode)

            # New: check if mouse is hovering
            mouse_pos = inputStream.mouse.currentPos
            self.hovered = self.rect.collidepoint(mouse_pos)

            if self.isImage and self.pressed:
                self.on = True
            if self.isList and self.selected and self.pressed:
                self.on = True
            elif not self.isList and self.pressed:
                self.on = True

            if self.on:
                self.timer -= 1
                if self.timer <= 0:
                    self.on = False
                    self.timer = 40
        except Exception as e:
            print(f'Exception {e} in ButtonUI.update() image: {self.image} text: {self.text}')
            raise e


    def draw(self, screen, alpha=255):
        try:
            if self.isImage and self.image is not None:
                if not self.visible:
                    return
                button_image = pygame.image.load(self.image).convert_alpha()

                # Initial paint color
                if self.init_paint_color:
                    paint_surface = pygame.Surface(button_image.get_size(), pygame.SRCALPHA)
                    paint_surface.fill(self.init_paint_color)
                    button_image.blit(paint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                # Overlay green on hover or on
                if self.on or self.hovered:
                    overlay = pygame.Surface(button_image.get_size(), pygame.SRCALPHA)
                    overlay.fill(GREEN)
                    button_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                # Overlay white on selected
                if self.selected:
                    overlay = pygame.Surface(button_image.get_size(), pygame.SRCALPHA)
                    overlay.fill(WHITE)
                    button_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                screen.blit(button_image, (self.x, self.y))
            else:
                if self.on:
                    #print(f'draw {self.text} on {self.on}')
                    colour = AQUA
                elif self.selected:
                    colour = SCREAMING_GREEN
                else:
                    colour = WHITE
                draw_interspersed_drop_shadow_text(screen, self.text, self.x, self.y,  self.font, colour)
        except Exception as e:
            print(f'Exception {e} in ButtonUI.draw() image: {self.image} text: {self.text}')
            raise e