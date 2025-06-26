# scenes/menu/structure_syllable.py
from scenes.core.scenes import Scene
from ui.button_ui import ButtonUI
import pygame
from utils.colors import DARK_GREY
import asyncio
from utils.fontloader import  load_arial_small


class StructureSyllablesScene(Scene, SharedNavigationButtonsMixin):
    def __init__(self):
        super().__init__()
        self.option_values = []
        self.optionSelected = -1
        self.list_options = []
        self.scene_to_go = None
        self.init_nav_buttons()
        self.options_ready = False

    async def initialize_options_async(self):
        self.options_ready = False  # Mark UI as not ready

        self.list_options.clear()
        self.option_values.clear()

        skill_id = GameSelectionDictionary.get_parameter('skill_id')
        syllables_number = GameSelectionDictionary.get_parameter('syllables_number')

        # Default full options list
        full_options = [
            ('Directa', 200, 'D'),
            ('Inversa', 270, 'I'),
            ('Travada', 340, 'T')
        ]

        if skill_id == 4:
            # Case 1: Show all options directly
            options = full_options

        elif skill_id == 12:
            # Case 2: Customize options based on syllables number
            if syllables_number == 1:
                options = [
                    ('Directa', 200, 'D'),
                    ('Travada', 270, 'T')
                ]
            elif syllables_number == 2:
                options = full_options
            else:
                options = []  # Fallback in case of unexpected syllable count

        else:
            # Case 3: Fetch structures from DB and filter options
            available_structure = await get_available_structure_syllables()

            if not available_structure:
                print(
                    "[StructureSyllablesScene] No structures syllables available after await. Skipping option population.")
                self.options_ready = True
                return

            print(f"[StructureSyllablesScene] Available structures syllables from DB: {available_structure}")
            options = [opt for opt in full_options if opt[2] in available_structure]

        # Populate UI buttons
        for label, y, value in options:
            self.list_options.append(ButtonUI(pygame.K_RETURN, label, 480, y, True))
            self.option_values.append(value)

        self.options_ready = True  # Now safe to draw

    def onEnter(self):
        self.optionSelected = 0
        #globals.soundManager.playMusicFade('silent_music')

        # Schedule the coroutine to load the options asynchronously
        future = asyncio.run_coroutine_threadsafe(self.initialize_options_async(), globals.asyncio_loop)
        future.add_done_callback(self.coroutine_callback)


    def input(self, sm, inputStream, screen=None):
        # Check for 'Q' key press to quit the game
        self.input_nav_buttons(sm, inputStream)
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
            self.activate_selection(sm)

        if inputStream.keyboard.isKeyPressed(pygame.K_q):
            exit_game()

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

    def activate_selection(self, sm):
        GameSelectionDictionary.set_parameter('syllable_structure', self.option_values[self.optionSelected])

        # print(f'syllable_structure: {syllable_mapping[self.optionSelected]}')
        from scenes.menu.sound import SoundScene
        self.scene_to_go = SoundScene()  # Avoid using eval for security reasons
        sm.push(self.scene_to_go)
        # sm.push(FadeTransitionScene([self], [self.scene_to_go]))

    def update(self, sm, inputStream):
        self.update_nav_buttons(inputStream)


        for i in range(len(self.list_options)):
            if self.optionSelected == i:
                self.list_options[i].update(inputStream, True)
            else:
                self.list_options[i].update(inputStream, False)

    def draw(self, sm, screen):
        screen.fill(DARK_GREY)
        drawImage(screen, self.menu_path, 0, 0)
        draw_interspersed_drop_shadow_text(screen, "Estructura de la síl•laba", 170, 50)
        self.draw_nav_buttons(screen)

        if not self.options_ready:
            draw_interspersed_drop_shadow_text(screen, "Carregant opcions disponibles...", 200, 300,
                                               font=load_arial_small())
            return


        for i in range(len(self.list_options)):
            self.list_options[i].draw(screen)


    def coroutine_callback(self, future):
        try:
            future.result()
        except Exception as e:
            print(f"[NumberSyllables] Coroutine error: {e}")

