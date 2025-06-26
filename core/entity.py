from systems.animations import Animations

class Entity:
    def __init__(self):
        self.camera = None
        self.position = None
        self.input = None
        self.button = None
        self.type = None
        # self.text = None
        self.buttonPressed = None  # To Know the button pressed by the player
        self.wordSpoken = None
        #self.hand = None
        self.animations = Animations()  # crea un empty animations component
        self.state = 'idle'
        # self.action = None
        self.character = None
        self.microphone = None
        self.listImages = []
        # self.is_correct = False
        self.name = None
        self.timer = 0
        self.hit = False
        self.velocity = None
        # Add a configuration for hand tracking
        self.hand_tracking_config = None
        self.path = None

    def add_component(self, component):
        self.__dict__.update(component.__dict__)