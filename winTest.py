import pygame,sys
from pygame.locals import *
import json
import time

#Get the instructions
def getInstructions(path):
    with open(path) as inst:
            text = inst.read()

    inst_labels = text.split('#')
    return inst_labels
consignas=getInstructions(r"C:\Users\Usuario\Documents\DreamTech\data\Instrucciones.txt")
print(consignas)
#Get the data
with open(r"C:\Users\Usuario\Documents\DreamTech\data\data.json","r") as f:
   data = json.load(f)
audio_context=data['audio']
audio_word=data['audio_p']
audio_sil=data['audio_s']
sil=data['silaba']
words = ["MIGAJA","RULETA","ENVASE","BUTACA","PILOTO",u'MUÑECA',"SOTANA",u'PEZUÑA',"CASINO","FATIGA","VERANO","COMETA","NOVELA","BOBINA","ALMEJA","MANADA","GUSANO","PAYASO","TIJERA","ZAPATO","RELATO","JUGADA","VISITA",u'LAGAÑA',"MELENA","FOGATA","TOCADO","ESQUINA","NEVADA","DUREZA"]

order_d = [10,2,8,3,5,11,7,1,9,12,6,14,15,4,24,29,17,22,18,23,21,25,16,27,19,26,28,13,30,20]  #displaying order 
order_t = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] #testing order

# initiallize the app
pygame.init()
clock = pygame.time.Clock()
run = True
#screen set up
screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
BG =(255,255,255)
black=(0,0,0)
font = pygame.font.SysFont('arialblack', 32)
# create a text surface object, on which text is drawn on it.
text = font.render('Vas a ver una lista de palabras, presta atención', True, black)
# create a rectangular object for the text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
textRect.center = (w//2, h//2)
#Counts parts of the training, it includes instructions as a separated part.
#Now there are 4 parts: 0 - instructions of the beggining of training, 1 - Training, 2- instructions of the "testing" of training, 3-"testing" of training
counter=3
i=0
#App loop
while run:

    screen.fill(BG)
    if counter == 0:
        if i >= len(consignas):
            i=0
        else:
            # create a text surface object, on which text is drawn on it.
            text = font.render(consignas[i], True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2)
            # copying the text surface object to the display surface object at the center coordinate.
            screen.blit(text, textRect)
            i+=1
           

    elif counter == 1: 
        if i >= 30:
            i=0
            counter +=1
        else:
            screen.fill(BG)
            sound=pygame.mixer.Sound(audio_context[order_d[i]-1])
            sound.play()
            pygame.display.update()
            time.sleep(3)
            text = font.render(words[order_d[i]-1], True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2)
            aud=pygame.mixer.Sound(audio_word[order_d[i]-1])
            aud.play()
            i+=1
    elif counter == 2:
        if i >= 1:
            i=0
        else:
            text = font.render('Presione ESPACIO para continuar a la segunda parte', True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2) 

    elif counter == 3: 
        if i >= 30:
            text = font.render('Presione ESC para cerrar', True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2)
        else:
            screen.fill(BG)
            sound=pygame.mixer.Sound(audio_context[order_t[i]-1])
            sound.play()
            pygame.display.update()
            time.sleep(3)
            text = font.render(sil[order_t[i]-1], True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2)
            # copying the text surface object to the display surface object at the center coordinate.
            screen.blit(text, textRect)
            pygame.display.update()
            aud=pygame.mixer.Sound(audio_sil[order_t[i]-1])
            aud.play()
            time.sleep(1.5)
            screen.fill(BG)
            pygame.display.update()
            time.sleep(5)
            text = font.render(words[order_t[i]-1], True, black)
            textRect = text.get_rect()
            textRect.center = (w//2, h//2)
            # copying the text surface object to the display surface object at the center coordinate.
            screen.blit(text, textRect)
            pygame.display.update()
            aud=pygame.mixer.Sound(audio_word[order_t[i]-1])
            aud.play()
            
            i+=1
    # copying the text surface object to the display surface object at the center coordinate.
    screen.blit(text, textRect)

    for event in pygame.event.get():
        #Terminate with x
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            #Terminate with escape
            if event.key in [K_ESCAPE]:
                run = False
            if event.key in [K_SPACE]:
                counter+=1
                i=0

    #update display
    pygame.display.update()
    time.sleep(1.5)
    
pygame.quit()