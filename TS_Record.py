import pygame
import json
import os
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import sys
import pygame_textinput

class TextModule:
    def __init__(self,screen, screen_width, screen_height, instruction_file_path, font_file_path):
        with open(instruction_file_path) as f:
            self.instructions = f.read().split('#')
        self.font = pygame.font.SysFont(font_file_path, 90)
        self.smaller_font = pygame.font.SysFont(font_file_path, 60)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen=screen
        self.text_surface = None

    def render_text(self, text, center=None, big_font=True):
        if big_font:
            self.text_surface = self.font.render(text, True, (0, 0, 0))
        else:
            self.text_surface = self.smaller_font.render(text, True, (0, 0, 0))
        if center:
            self.text_rect = self.text_surface.get_rect(center=center)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.text_surface, self.text_rect)

    def draw_no_bkg(self):
        self.screen.blit(self.text_surface, self.text_rect)

    def show_message(self, message, big_font=True, no_bkg=False):
        self.render_text(message, center=(self.screen_width//2, self.screen_height//2), big_font=big_font)
        if no_bkg:
            self.draw_no_bkg()
        else:
            self.draw()
        pygame.display.flip()


class AudioModule:
    def __init__(self, data_file_path):
        with open(data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.audio_context = data["audio"]
        self.audio_word = data["audio_p"]
        self.audio_sil = data["audio_s"]
        self.sil = data["silaba"]
        self.words = data["palabra"]
        self.display_order = [10, 2, 8, 3, 5, 11, 7, 1, 9, 12, 6, 14, 15, 4, 24, 29, 17, 22, 18, 23, 21, 25, 16, 27, 19, 26, 28, 13, 30, 20]
        self.testing_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

    def play_sound(self, audio_file):
        sound = pygame.mixer.Sound(audio_file)
        sound.play()

    def record_voice(self, word, duration=5, sujeto="sujeto"):
        # Set the sampling frequency and number of channels
        fs = 44100
        channels = 2

        # Start recording
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)

        # Wait for the specified duration
        pygame.time.wait(duration*1000)

        # Stop recording and save the audio to a WAV file
        sd.wait()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'out/TR_{sujeto}/{word}_{timestamp}.wav'
        if not os.path.exists(f'out/TR_{sujeto}'):
            os.makedirs(f'out/TR_{sujeto}')

        write(file_name, fs, recording)  # Save as WAV file


class TS_Record:
    def __init__(self):
        pygame.init()
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.text_module = TextModule(self.screen,self.screen.get_width(), self.screen.get_height(), "./data/Instrucciones.txt", "arialblack.ttf") # USAR RUTAS RELATIVAS
        self.audio_module = AudioModule("./data/data.json") # USAR RUTAS RELATIVAS
        self.running = True
        self.gamestate = "login"
        self.train_idx = 0
        self.test_idx = 0
        self.textinput = pygame_textinput.TextInputVisualizer()
        self.rect = pygame.Rect(self.screen.get_width()/2-290, self.screen.get_height()/2+30, 580, 80)

    def wait_for_space(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.gamestate = "test"
                    return event.key
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running=False
                    return event.key
                
    def wait_for_escape(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running=False
                    return event.key
                
    def wait_ticks(self, seconds):
        clock = pygame.time.Clock()
        ticks=seconds*60
        ticks_elapsed = 0
        while ticks_elapsed < ticks:
            clock.tick(60)
            ticks_elapsed += 1

    def show_image(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        screen_rect = self.screen.get_rect()
        image_rect = image.get_rect()
        image_rect.center = screen_rect.center
        self.screen.blit(image, image_rect)
        pygame.display.flip()

    def login_screen(self):
        self.screen.fill((255, 255, 255))
        self.textinput.update(self.events)
        self.screen.blit(self.textinput.surface, (self.screen.get_width()/2-270, self.screen.get_height()/2+60))
        pygame.draw.rect(self.screen, pygame.Color(0,0,0), self.rect, 4)
        self.text_module.show_message("Inserte código del sujeto", big_font=False, no_bkg=True)

    def start_screen(self):
        self.text_module.show_message("Presione ESPACIO para empezar", big_font=False)
        self.wait_for_space()
      
    def test_word_list(self):
        syllable_idx = self.audio_module.testing_order[self.test_idx]
        self.screen.fill((255,255,255))
        pygame.display.flip()
        self.wait_ticks(1)
        self.audio_module.play_sound(self.audio_module.audio_context[syllable_idx-1])
        self.wait_ticks(3)
        self.text_module.show_message(self.audio_module.sil[syllable_idx-1])
        self.audio_module.play_sound(self.audio_module.audio_sil[syllable_idx-1])
        self.wait_ticks(1.5)
        self.show_image("assets/images/mic.png")
        self.audio_module.record_voice(self.audio_module.words[syllable_idx-1], sujeto=self.textinput.value)
        self.screen.fill((255,255,255))
        pygame.display.flip()
        self.wait_ticks(2)
        pygame.display.flip()


    def run(self):
        while self.running:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        if self.gamestate == 'login' and len(self.textinput.value) > 0:
                            self.gamestate = 'start'

            if self.gamestate == 'login':
                self.login_screen()
            
            elif self.gamestate == 'start':
                self.start_screen()

            elif self.gamestate == 'test':
                if self.test_idx >= len(self.audio_module.testing_order):
                    self.text_module.show_message("Presione ESC para cerrar", big_font=False)
                    self.wait_for_escape()
                else:
                    self.test_word_list()
                    self.test_idx += 1
                
            pygame.display.flip()

if __name__ == '__main__':
    app = TS_Record()
    app.run()
