import pygame
from Load_image import load_image
import sys
def terminate():
    pygame.quit()
    sys.exit()
def start_screen(screen):
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('стартовое окно.png'), (1280, 720))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(60)
