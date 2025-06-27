import pygame

def render_check_if_order_correct(frame, color_ranges, targets, screen, position=(50, 50)):
    check_image_path = 'assets/GUI/Background/done.png'
    check_image = pygame.image.load(check_image_path).convert_alpha()
    screen.blit(check_image, position)