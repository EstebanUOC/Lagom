#scenes/core/scenes.py
import pygame

class Scene:
    def __init__(self):
        super().__init__()

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self, sm, inputStream):
        pass

    def update(self, sm, inputStream):
        pass

    def draw(self, sm, screen):
        pass

class SceneManager:
    def __init__(self):
        self.scenes = []

    def isEmpty(self):
        return len(self.scenes) == 0

    def input(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self, inputStream)

    def enterScene(self):
        if len(self.scenes) > 0:
            # print(f'escenes: {self.scenes}')
            self.scenes[-1].onEnter()

    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()

    def update(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, inputStream)

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
        # La sig linea sirve para ver cuantas escenas hay en el stack
        #drawText(screen, str(len(self.scenes)), 0, 0, utils.WHITE, 255)
        #print(f'draw scenes list: {self.scenes}')
        # present screen
        pygame.display.flip()

    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        #print('scene to push: ' + str(scene) + ' count: ' + str(len(self.scenes)))
        #print(f' push scenes list: {self.scenes}')
        self.enterScene()

    def pop(self):
        self.exitScene()
        print(f'[SM] scene to pop: {self.scenes[-1]}')
        print(f'[SM] scenes list: {self.scenes}')
        self.scenes.pop()
        self.enterScene()

    def set(self, scenes):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scene
        for s in scenes:
            self.push(s)

    def pop_multiple(self, n):
        for _ in range(n):
            if not self.isEmpty():
                self.pop()

    def pop_until_unit_scene(self):
        from scenes.menu.unity_scene import UnityScene
        from scenes.loading.loading_initialization import LoadingInitializationScene

        while self.scenes:
            top_scene = self.scenes[-1]
            print("Type of top scene:", type(top_scene))
            print("Is UnityScene?", isinstance(top_scene, UnityScene))

            # If it's a LoadingInitializationScene, remove it too
            if isinstance(top_scene, LoadingInitializationScene):
                print("[SM] Popping LoadingInitializationScene to reach UnityScene")
                self.pop()
                continue

            if isinstance(top_scene, UnityScene):
                print("[SM] Found UnityScene, stopping pop.")
                return

            self.pop()

        print("Warning: UnityScene not found in scene stack.")

