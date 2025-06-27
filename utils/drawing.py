#drawing.py
import pygame

_image_cache = {}
def get_image(path):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path).convert_alpha()
    return _image_cache[path]


def drawImage(screen, img, x, y, opacity=255):
    if screen is None:
        return
    try:
        if isinstance(img, str):
            img = get_image(img)  # Use cache
        img.set_alpha(opacity)
        screen.blit(img, (x, y))
    except Exception as e:
        print(f'[u][drawing][drawImage] error screen: {screen} img: {img}  exception: {e}')



from utils.colors import WHITE, GREY  # if you have them separated

def draw_interspersed_drop_shadow_text(
    screen,
    text,
    x,
    y,
    font=None,
    text_color=WHITE,
    shadow_color=GREY,
    interletter_spacing=5,
    shadow_offset=3
    ):

    if callable(font):
        font = font()

    from utils.fontloader import load_arial_small  # loads size 62 by default
    # Use default title font if not provided
    if font is None:
        font = load_arial_small()

    start_x = x
    for char in text:
        char_surface = font.render(char, True, text_color)
        shadow_surface = font.render(char, True, shadow_color)
        char_x = start_x
        shadow_x = char_x + shadow_offset
        char_y = y
        shadow_y = y + shadow_offset
        screen.blit(shadow_surface, (shadow_x, shadow_y))
        screen.blit(char_surface, (char_x, char_y))
        start_x += char_surface.get_width() + interletter_spacing



def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)
