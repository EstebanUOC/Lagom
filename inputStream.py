import pygame

class Mouse:
    def __init__(self):
        self.currentButtonStates = None
        self.previousButtonStates = None
        self.currentPos = (0, 0)
        self.previousPos = (0, 0)

    def processInput(self):
        # Save previous states before updating
        self.previousButtonStates = self.currentButtonStates
        self.previousPos = self.currentPos
        # Update with current states
        self.currentButtonStates = pygame.mouse.get_pressed()  # returns (left, middle, right)
        self.currentPos = pygame.mouse.get_pos()

    def isButtonDown(self, button):
        # button: 0 = left, 1 = middle, 2 = right
        if self.currentButtonStates is None:
            return False
        return self.currentButtonStates[button]

    def isButtonPressed(self, button):
        if self.currentButtonStates is None or self.previousButtonStates is None:
            return False
        # Button pressed: currently down and was not down in the previous frame
        return self.currentButtonStates[button] and not self.previousButtonStates[button]

    def isButtonReleased(self, button):
        if self.currentButtonStates is None or self.previousButtonStates is None:
            return False
        # Button released: currently up but was down in the previous frame
        return (not self.currentButtonStates[button]) and self.previousButtonStates[button]

class Keyboard:
    def __init__(self):
        self.currentKeyStates = None
        self.previousKeyStates = None

    def processInput(self):
        try:
            self.previousKeyStates = self.currentKeyStates
            self.currentKeyStates = pygame.key.get_pressed()
        except pygame.error:
            self.currentKeyStates = []
            print("[InputStream] Warning: Tried to read keyboard state after Pygame was quit.")

    def isKeyDown(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True

    def isKeyPressed(self, keyCode):
        # print("Enter  keyCode={} ".format(keyCode))
        # print("isKeyPressed: previou={} current={} ".format(self.currentKeyStates[keyCode], self.currentKeyStates[keyCode]))
        # print("isKeyPressed: previou={} current={} ".format(self.previousKeyStates, self.currentKeyStates))
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        # if self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False:
            # print("isKeyPressed: previou={} current={} ".format(self.previousKeyStates[keyCode], self.currentKeyStates[keyCode]))
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False

    def isKeyReleased(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        # print('Current', self.currentKeyStates[keyCode], 'Previous', self.previousKeyStates[keyCode],'1if',self.currentKeyStates[keyCode] == False, '2if', self.previousKeyStates[keyCode] == True)
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True




class InputStream:
    def __init__(self):
        self.keyboard = Keyboard()
        self.mouse = Mouse()  # Add the mouse instance
        self.typed_characters = []  # 🆕 List of typed characters

    def processInput(self, events):
        self.keyboard.processInput()
        self.mouse.processInput()
        self.typed_characters = []  # ✅ Reset every frame

        for event in events:  # ✅ Use the passed-in events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.typed_characters.append("BACKSPACE")
                elif event.key == pygame.K_RETURN:
                    self.typed_characters.append("RETURN")
                elif event.key == pygame.K_TAB:
                    pass  # ❌ Skip adding '\t' to text input
                elif event.unicode != '':
                    self.typed_characters.append(event.unicode)



