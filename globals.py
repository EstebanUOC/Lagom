#globals.py

events = []  # declare at init if not yet
SCREEN_SIZE = (1280, 720)

CAMERACV_WIDTH = 1280
CAMERACV_HEIGHT = 720

player1 = None
world = None
parameters = None

secondsButtonPressed = 1 #48
# secondsBubblePressed = 30

DEVELOPMENT_MODE = False

# Initialize SessionAsync to be used across the app
SessionAsync = None

# Add a flag to track DB initialization status
db_initialized = False

# Image sets
LLUNI_NEUTRAL = None
LLUNI_POSITIVE = None
YES_PRESSED = None
NO_PRESSED = None
# Image sets for Circle
CIRCLE_POSITIVE = None
CIRCLE_NEUTRAL = None
BUBBLE_PRESSED = None
MICRO_RECORD = None
# Playful Scene
CLOUDS_EXPLOSIONS_SET = None
FRIENDS_ANIMATION_SET = None


# Flag of system
hand_tracking_system = None
face_tracking_system = None

# Flag to track if HandTrackingAI is ready
hand_tracking_ready = False
hand_tracking_playful_ready = False
face_tracking_ready = False



# Flag order scenes
counter_scene_played = 0