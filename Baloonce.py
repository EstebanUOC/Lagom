import logging
import pygame
import threading
import asyncio
from input_stream import InputStream
from scenes.core.scenes import SceneManager
from scenes.Intro import IntroScene
import core.engine as engine
import globals
from factories.player_factory import makePlayer

# Set up logging
logging.basicConfig(filename='Baloonce_logs.log', level=logging.DEBUG)

def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def is_event_loop_running():
    try:
        loop = asyncio.get_running_loop()
        # print("An event loop is running.")
        return True
    except RuntimeError:
        # print("No event loop is running.")
        return False

def check_event_loop_state(loop):
    if loop.is_closed():
        print("The event loop is closed.")
    else:
        print("The event loop is running.")

# Initialize pygame
pygame.init()

# Set up the Pygame display
screen = pygame.display.set_mode(globals.SCREEN_SIZE)
pygame.display.set_caption('PICOFON V1.2')
clock = pygame.time.Clock()

# Create a player
if globals.player1 is None:
    print('[main] Creating player entity')
    globals.player1 = makePlayer()
    print('[main] Player created:', globals.player1)

globals.player1.camera = engine.CameraComponent()
print(f'[main] globals.player1.camera = {globals.player1.camera}')
globals.player1.position = engine.Position(0, 0, 0, 0)
globals.player1.input = engine.Input(pygame.K_r)

# Initialize the scene manager and other components
inputStream = InputStream()
sceneManager = SceneManager()
sceneManager.push(IntroScene())



# Start the asyncio loop in a separate thread
asyncio_loop = asyncio.new_event_loop()
asyncio_thread = threading.Thread(target=start_asyncio_loop, args=(asyncio_loop,), daemon=True)
asyncio_thread.start()

# Store the asyncio loop in globals for easy access
globals.asyncio_loop = asyncio_loop

# Check if the event loop is running
is_event_loop_running()
check_event_loop_state(globals.asyncio_loop)

# Main game loop
running = True
while running:
    events = pygame.event.get()  # ✅ Get events once here

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    inputStream.processInput(events)  # ✅ Pass the events down

    if sceneManager.isEmpty():
        running = False

    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    clock.tick(60)

# At the end of Baloonce.py before quitting:
if hasattr(globals.player1, "camera_scanner"):
    globals.player1.camera_scanner.stop()

# Clean up
pygame.quit()

# Stop the asyncio loop
asyncio_loop.call_soon_threadsafe(asyncio_loop.stop)

# Check the event loop state after stopping
check_event_loop_state(globals.asyncio_loop)