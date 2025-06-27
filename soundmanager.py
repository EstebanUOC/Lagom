import pygame
import constants.global_constants as constants
from utils.helpers_paths import get_resource_path


# Get the current volume
#system_volume = Volumen.Volume()  # this is the original code
# system_volume = 0 # this is for make it silent
# print(f'system_volume = {system_volume}')

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 1
        self.musicVolume = 1
        self.targetMusicVolume = 1
        music_path = get_resource_path(constants.MusicPath, '')
        self.sounds = {
            'secen_done': pygame.mixer.Sound(music_path + 'btnTono5.ogg'),
            'btn_pressed_click': pygame.mixer.Sound(music_path + 'click.ogg'),
            'btn_pop': pygame.mixer.Sound(music_path + 'pop.ogg')
        }
        self.music = {}

    def add_music(self, musicName, musicPath):
        self.music[musicName] = musicPath

    def delete_all_music(self):
        pygame.mixer.music.stop()
        self.music.clear()
        print(f'delete_all_music: {self.music}')

    def playSound(self, soundName):
        self.sounds[soundName].set_volume(self.soundVolume)
        self.sounds[soundName].play()

    def playMusic(self, musicName):
        try:
            if musicName not in self.music:
                print(f"[SM][playMusic] musicName '{musicName}' not found. Using 'silent' instead.")
                musicName = "silent"

            print(f'[SM][playMusic]  loading: {musicName} -> {self.music[musicName]}')
            pygame.mixer.music.load(self.music[musicName])
            pygame.mixer.music.set_volume(self.musicVolume)
            pygame.mixer.music.play(0)

        except Exception as e:
            print(f'[SM][playMusic] Error: {e}')

    def playMusicFade(self, musicName):
        # Fade not important anymore, simply play directly
        self.playMusic(musicName)

    def stopIfPlaying(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print('[SoundManager] Stopped currently playing music.')

    def update(self):
        # Update volume toward target if necessary
        if self.musicVolume < self.targetMusicVolume:
            self.musicVolume = min(self.musicVolume + 0.5, self.targetMusicVolume)
            pygame.mixer.music.set_volume(self.musicVolume)