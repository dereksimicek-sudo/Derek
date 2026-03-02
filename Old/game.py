import pygame
import random
pygame.init() #inicializace pygame modulu
SIRKA, VYSKA = 800, 600
CERNA = (0, 0, 0)       # NASTAVENI BAREV
BILA = (255, 255, 255)
CERVENA = (255, 0, 0)
ORANGE = (255, 165, 0)
velikost_ctverce = 50
ctverec_x = SIRKA // 2 - velikost_ctverce // 2
ctverec_y = VYSKA // 2 - velikost_ctverce // 2
rychlost = 5
okno = pygame.display.set_mode((SIRKA, VYSKA)) #nastaveni velikosti okna
pygame.display.set_caption("Souradny system") #nastaveni titulku okna
pismo = pygame.font.SysFont("Arial", 24) #nastaveni pisma
bezi = True
hodiny = pygame.time.Clock() #nastaveni hodin pro regulaci FPS
while bezi:
    for udalost in pygame.event.get(): #ziskani vsech udalosti
        if udalost.type == pygame.QUIT: #pokud uzivatel zavre okno
            bezi = False #ukonceni smyck
    klavesa = pygame.key.get_pressed() #ziskani stisknutych klaves
    if klavesa[pygame.K_LEFT] or klavesa[pygame.K_a]: #pokud je stisknuta leva sipka
        ctverec_x -= rychlost #posunuti ctverce doleva
    if klavesa[pygame.K_RIGHT] or klavesa[pygame.K_d]: #pokud je stisknuta prava sipka
        ctverec_x += rychlost #posunuti ctverce doprava
    if klavesa[pygame.K_UP] or klavesa[pygame.K_w]: #pokud je stisknuta horni sipka
        ctverec_y -= rychlost #posunuti ctverce nahoru
    if klavesa[pygame.K_DOWN] or klavesa[pygame.K_s]: #pokud je stisknuta dolni sipka
        ctverec_y += rychlost #posunuti ctverce dolu

    # Logic to ensure the square stays within the window
    if ctverec_x < 0:
        ctverec_x = 0
    elif ctverec_x + velikost_ctverce > SIRKA:
        ctverec_x = SIRKA - velikost_ctverce
        
    if ctverec_y < 0:
        ctverec_y = 0
    elif ctverec_y + velikost_ctverce > VYSKA:
        ctverec_y = VYSKA - velikost_ctverce
    
    # Generace random černých kostek
    kostky = []
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 2000)
    #inside game loop
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezi = False
        elif udalost.type == SPAWN_EVENT:
            rx = random.randint(0, SIRKA - velikost_ctverce)
            ry = random.randint(0, VYSKA - velikost_ctverce)
            kostky.append(pygame.Rect(rx, ry, velikost_ctverce, velikost_ctverce))
    
    #inside drawing section
    okno.fill(BILA)
    
    # Draw black cubes
    for k in kostky:
        pygame.draw.rect(okno, CERNA, k)
    
    # vykresleni pozadi
    okno.fill(BILA)

    pygame.draw.rect(okno, ORANGE, (ctverec_x, ctverec_y, velikost_ctverce, velikost_ctverce)) #vykresleni ctverce
    # regulace FPS
    hodiny.tick(60) #nastaveni FPS na 60
    
    pygame.display.flip() #aktualizace obrazovky

pygame.quit() # Ukončí Pygame
