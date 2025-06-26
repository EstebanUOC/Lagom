import pygame
from constants.global_constants import FONT_ARIAL_ROUNDED_MT_BOLD, FONT_DEJAVU_SANS_BOLD
import os

def load_arial_score(size=90):
    if os.path.exists(FONT_ARIAL_ROUNDED_MT_BOLD):
        try:
            return pygame.font.Font(FONT_ARIAL_ROUNDED_MT_BOLD, size)
        except Exception as e:
            print(f"[FontLoader] Failed to load bundled font: {e}")
    # Fallback to system font
    return pygame.font.SysFont("arial", size)

def load_arial_small(size=39):
    if os.path.exists(FONT_ARIAL_ROUNDED_MT_BOLD):
        try:
            return pygame.font.Font(FONT_ARIAL_ROUNDED_MT_BOLD, size)
        except Exception as e:
            print(f"[FontLoader] Failed to load bundled font: {e}")
    # Fallback to system font
    return pygame.font.SysFont("arial", size)

def load_arial_xs(size=20):
    if os.path.exists(FONT_ARIAL_ROUNDED_MT_BOLD):
        try:
            return pygame.font.Font(FONT_ARIAL_ROUNDED_MT_BOLD, size)
        except Exception as e:
            print(f"[FontLoader] Failed to load bundled font: {e}")
    # Fallback to system font
    return pygame.font.SysFont("arial", size)
