import pygame
from utils.drawing import drawImage
from utils.helpers_paths import get_resource_path
from utils.color_sequence_checker import are_objects_in_correct_order

def render_check_if_order_correct(frame, color_ranges, targets, screen, position=(50, 50)):
    if are_objects_in_correct_order(frame, color_ranges, targets):
        check_image_path = 'assets/GUI/Background/done.png'
        check_image = pygame.image.load(check_image_path).convert_alpha()
        screen.blit(check_image, position)
