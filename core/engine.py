import pygame
import globals
import logging

# sys.path.append("C:\\Users\\Esteban\\anaconda3\\envs\\envProduction\\Lib\\site-packages")


logger = logging.getLogger(__name__)


class System():
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, inputStream, entity)

    def updateEntity(self, screen, inputStream, entity):
        pass



class Position:
    def __init__(self, x, y, w=0, h=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        # print(f'Position x: {x} y: {y} w: {w} h: {h} rect: {self.rect}')

class VelocityComponent:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


class CameraComponent:
    def __init__(self):
        self.capture = []
        self.on = False
        self.face_detection = []
        self.hands = None


class Input:
    def __init__(self, r):
        self.r = r