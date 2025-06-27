import globals
from scenes.core.scenes import Scene
import pygame
import pandas as pd
import os

class LeaderBoard(Scene):
    def __init__(self):
        super().__init__()

        self.w, self.h = 1280, 720
        self.font = pygame.font.Font("assets\Fonts\Dongle-Light.ttf", 40)
        self.title_font = pygame.font.Font("assets\Fonts\Dongle-Bold.ttf", 90)

        self.background = pygame.image.load('assets/GUI/Background/bg-board.jpg')
        self.background = pygame.transform.scale(self.background, (self.w, self.h))

        self.filename = "leaderboard.csv"
        self.player = getattr(globals, "nickname", "Unknown")
        self.time = getattr(globals, "timer", 9999)
        self.time = (pygame.time.get_ticks() - self.time) // 1000
        self.put_in_leaderboard(self.player, self.time)
        self.records = self.get_leaderboard()

    def put_in_leaderboard(self, name, time):
        if os.path.isfile(self.filename):
            lb = pd.read_csv(self.filename)
        else:
            lb = pd.DataFrame(columns=["name", "time"])
        new_row = pd.DataFrame([{"name": name, "time": time}])
        lb = pd.concat([lb, new_row], ignore_index=True)
        lb.to_csv(self.filename, index=False)

    def get_leaderboard(self):
        if not os.path.isfile(self.filename):
            return []
        file = pd.read_csv(self.filename)
        leaderboard = list(zip(file["name"], file["time"]))
        leaderboard.sort(key=lambda x: x[1])
        return leaderboard

    def input(self, sm, inputStream, screen=None):
        # Sem navegação
        pass

    def update(self, sm, inputStream):
        pass

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))

        # Título
        t_x = int(self.w * 0.1)
        t_y = int(self.h * 0.20)
        title = "Top 10 Fastest Players and YOU"
        rendered_title = self.title_font.render(title, True, (0, 0, 0))
        screen.blit(rendered_title, (t_x, t_y))

        # Registos
        r_x = int(self.w * 0.25)
        r_y = int(self.h * 0.55) - int(self.h * 0.2)
        i = 1
        for record in self.records[:10]:
            if record[0] == self.player and record[1] == self.time:
                text_color = (255, 0, 0)
            else:
                text_color = (0, 0, 0)

            time_str = str(int(record[1]))
            num = 60 - len(record[0]) - len(str(i)) - len(time_str)
            line = f"{i}.  {record[0]}" + '.' * num + f"{time_str}"
            rendered_text = self.font.render(line, True, text_color)
            screen.blit(rendered_text, (r_x, r_y))
            r_y += int(0.05 * self.h)
            i += 1

        # Player outside of the top 10
        try:
            index = self.records.index((self.player, self.time))
            if index >= 10:
                time_str = str(int(self.time))
                num = 60 - len(self.player) - len(str(index + 1)) - len(time_str)
                last_line = f"{index + 1}.  {self.player}" + '.' * num + f"{time_str}"
                rendered_last = self.font.render(last_line, True, (255, 0, 0))
                screen.blit(rendered_last, (r_x, r_y))
        except ValueError:
            pass