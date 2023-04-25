import pygame
import json
import os
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import sys


class TextModule:
    def __init__(self,screen, screen_width, screen_height, instruction_file_path, font_file_path):
        #self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((screen_width, screen_height))
        with open(instruction_file_path) as f:
            self.instructions = f.read().split('#')
        self.font = pygame.font.SysFont(font_file_path, 90)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen=screen
        self.text_surface = None

    def render_text(self, text, center=None):
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        if center:
            self.text_rect = self.text_surface.get_rect(center=center)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.text_surface, self.text_rect)

    def show_message(self, message):
        self.render_text(message, center=(self.screen_width//2, self.screen_height//2))
        self.draw(self.screen)
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

    def record_voice(self, word,duration=5):
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
        file_name = f'out/TR_sujeto/{word}_{timestamp}.wav'
        if not os.path.exists(f'out/TR_sujeto'):
            os.makedirs(f'out/TR_sujeto')

        write(file_name, fs, recording)  # Save as WAV file
        
        
        #return file_name



class App:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.text_module = TextModule(self.screen,self.screen_width, self.screen_height, "C:/Users/Usuario/Documents/DreamTech/data/Instrucciones.txt", "arialblack.ttf")
        self.audio_module = AudioModule("C:/Users/Usuario/Documents/DreamTech/data/data.json")
        self.running = True
        self.counter = 0
        self.i = 0

    def wait_for_space(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.counter=1
                    return event.key
                
    def wait_for_escape(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running=False
                    return event.key
                
    def wait_ticks(self,clock, seconds):
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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.counter==1
                        
            '''
            self.text_module.show_message("Vas a ver una lista de palabras, presta atención")
            if self.counter==0:
                for _, word_idx in enumerate(self.audio_module.display_order):
                    self.screen.fill((255,255,255))
                    pygame.display.flip()
                    self.audio_module.play_sound(self.audio_module.audio_context[word_idx-1])
                    #self.wait_ticks(self.clock,3) #No se porque con esto no anda
                    pygame.time.wait(3*1000) #es como time sleep pero en milisegundos
                    self.text_module.show_message(self.audio_module.words[word_idx-1])
                    self.audio_module.play_sound(self.audio_module.audio_word[word_idx-1])
                    pygame.time.wait(1500) #es como time sleep pero en milisegundos
            '''
            self.text_module.show_message("Presione ESPACIO para continuar a la segunda parte")
            self.wait_for_space()
            
            if self.counter==1:
                for _, syllable_idx in enumerate(self.audio_module.testing_order):
                    self.screen.fill((255,255,255))
                    pygame.display.flip()
                    pygame.time.wait(1000) #es como time sleep pero en milisegundos
                    self.audio_module.play_sound(self.audio_module.audio_context[syllable_idx-1])
                    #self.wait_ticks(self.clock,3) #No se porque con esto no anda
                    pygame.time.wait(3*1000) #es como time sleep pero en milisegundos
                    self.text_module.show_message(self.audio_module.sil[syllable_idx-1])
                    self.audio_module.play_sound(self.audio_module.audio_sil[syllable_idx-1])
                    pygame.time.wait(1500) #es como time sleep pero en milisegundos
                    self.show_image("assets/images/mic.png")
                    self.audio_module.record_voice(self.audio_module.words[syllable_idx-1])
                    #pygame.time.wait(2*1000) #es como time sleep pero en milisegundos
                    self.screen.fill((255,255,255))
                    pygame.display.flip()
                    pygame.time.wait(100) #es como time sleep pero en milisegundos
                    self.text_module.show_message(self.audio_module.words[syllable_idx-1])
                    pygame.display.flip()
                    self.audio_module.play_sound(self.audio_module.audio_word[syllable_idx-1])
                  

            self.text_module.show_message("Presione ESC para cerrar")
            self.wait_for_escape


if __name__ == '__main__':
    app = App()
    app.run()
