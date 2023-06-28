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
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    options = ["Training", "Testing"]
    selected_option = None
    dropdown_visible = False

    while True:
        screen.fill((255, 255, 255))
        draw_text('main menu', font, (0, 0, 0), screen, screen_width // 2, 20)

        mx, my = pygame.mouse.get_pos()

        button_width = 250
        button_height = 80
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2

        button = pygame.Rect(button_x, button_y, button_width, button_height)

        if button.collidepoint((mx, my)):
            if click:
                dropdown_visible = not dropdown_visible

        pygame.draw.rect(screen, (0, 0, 0), button)
        draw_text('Select Option', font, (255, 255, 255), screen, button_x + button_width // 2, button_y + button_height // 2)

        if dropdown_visible:
            dropdown_x = button_x
            dropdown_y = button_y + button_height
            dropdown_width = button_width
            dropdown_height = button_height * len(options)

            dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (0, 0, 0), dropdown_rect)

            for i, option in enumerate(options):
                option_x = dropdown_x + dropdown_width // 2
                option_y = dropdown_y + i * button_height + button_height // 2
                option_rect = pygame.Rect(dropdown_x, dropdown_y + i * button_height, dropdown_width, button_height)

                if option_rect.collidepoint((mx, my)):
                    if click:
                        selected_option = option
                        dropdown_visible = False

                if selected_option == option:
                    color = (255, 0, 0)  # Color para la opción seleccionada
                else:
                    color = (255, 255, 255)  # Color para las opciones no seleccionadas

                draw_text(option, font, color, screen, option_x, option_y)

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

        if selected_option == "Training":
            exec(open("TR_Record.py").read())  # Ejecutar el script "TR.py"
        if selected_option == "Testing":
            exec(open("TS_Record.py").read())  # Ejecutar el script "TR.py"
        pygame.display.update()
        mainClock.tick(60)

main_menu()
