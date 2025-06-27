# systems/camera_scanner.py

import cv2
import numpy as np
import threading
import pygame
import logging

from core.engine import System, Position
import globals


logger = logging.getLogger(__name__)

class CameraScanner(System):
    def __init__(self):
        super().__init__()
        self.running = False
        self.thread = None
        self.capture = None
        self.should_draw = True
        self.initialized = False

        self.color_ranges = {
            'red': [(0, 100, 100), (10, 255, 255)],
            'green': [(40, 70, 70), (80, 255, 255)],
            'blue': [(100, 150, 0), (140, 255, 255)],
            'yellow': [(20, 100, 100), (30, 255, 255)],
        }

    def check(self, entity):
        #print(f"[CameraScanner] Checking if entity has a camera component: {entity.type}")
        #return entity.type == 'player'
        return True


    def stop(self):
        self.running = False
        if self.capture:
            self.capture.release()
            self.capture = None
        cv2.destroyAllWindows()
        logger.debug("[CameraScanner] Stopped and released camera")

    def updateEntity(self, screen, inputStream, entity):


        if not self.initialized:
            entity.camera.capture = cv2.VideoCapture(0)
            entity.camera.capture.set(3, globals.CAMERACV_WIDTH)
            entity.camera.capture.set(4, globals.CAMERACV_HEIGHT)
            self.initialized = True
            #print("[CameraScanner] Camera initialized")
            logger.debug("[CameraScanner] Initialized camera capture")

        if not self.initialized:
            self.initialize()

        if not entity.camera.capture or not entity.camera.capture.isOpened():
            print("[CameraScanner] Capture not available")
            logger.warning("[CameraScanner] Capture not available")
            return

        success, frame = entity.camera.capture.read()
        if not success:
            return

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for color, (lower, upper) in self.color_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) > 800:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Resize for display
        frame = cv2.resize(frame, (globals.CAMERACV_WIDTH, globals.CAMERACV_HEIGHT))
        imgRGB = np.rot90(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        surf = pygame.surfarray.make_surface(imgRGB).convert()

        if self.should_draw and screen:
            screen.set_clip(0, 0, globals.CAMERACV_WIDTH, globals.CAMERACV_HEIGHT)
            screen.blit(surf, (0, 0))
            screen.set_clip(None)

    def get_current_frame(self, entity):
        """
        Fetches and returns the latest flipped frame from the entity's camera.
        """
        if not hasattr(entity, "camera") or not hasattr(entity.camera, "capture"):
            print("[CameraScanner] ❌ Entity has no valid camera or capture attribute")
            return None

        capture = entity.camera.capture

        if not capture or not capture.isOpened():
            print("[CameraScanner] ❌ Camera is not opened or initialized")
            return None

        success, frame = capture.read()
        if not success:
            print("[CameraScanner] ❌ Failed to read frame from camera")
            return None

        return cv2.flip(frame, 1)  # Ensure consistency with updateEntity


