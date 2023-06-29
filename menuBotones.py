#main Menu
import pygame
import sys
#Modulos
from TR_Record import TextModule,AudioModule,TR_Record
from TS_Record import TextModule,AudioModule,TS_Record
import pygame_textinput

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('DreamTech')
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))


font = pygame.font.SysFont("arialblack.ttf", 50)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    while True:
        screen.fill((255, 255, 255))
        draw_text('DreamTech', font, (0, 0, 0), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_width = 250
        button_height = 80
        button_x = (screen_width - button_width) // 2
        button_1_y = (screen_height - button_height) // 2 - 80
        button_2_y = (screen_height - button_height) // 2 + 80

        button_1 = pygame.Rect(button_x, button_1_y, button_width, button_height)
        button_2 = pygame.Rect(button_x, button_2_y, button_width, button_height)

        if button_1.collidepoint((mx, my)):
            if click:
                app = TR_Record()
                app.run()
        if button_2.collidepoint((mx, my)):
            if click:
                app = TS_Record()
                app.run()
        
        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)

        draw_text('Training', font, (255, 255, 255), screen, button_x+55, button_1_y+25)
        draw_text('Testing', font, (255, 255, 255), screen, button_x+60, button_2_y+25)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

main_menu()
