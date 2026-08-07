import sys
import pygame
import os
import time

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FOLDER_NAME = 'media'

IMAGES_DIR = os.path.join(BASE_DIR, IMAGE_FOLDER_NAME)

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

images = {}
for i in range(1, 15):
    image_path = os.path.join(IMAGES_DIR, f'{i}.bmp')

    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")

    images[i] = pygame.image.load(image_path).convert()

clock = pygame.time.Clock()

current_state = 1
timer_start = 0
r_pressed = False

running = True
while running:
    dt = clock.tick(60) # Limit to 60 FPS (NTSC)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            key = event.key

            if current_state == 1:
                if key == pygame.K_h:
                    current_state = 2

            elif current_state == 2:
                if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    current_state = 3
                    pygame.mixer.music.load(os.path.join('sfx', 'beep.wav'))
                    pygame.mixer.music.play()

            elif current_state == 3:
                if key == pygame.K_F1:
                    current_state = 4

            elif current_state == 4:
                if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    current_state = 5
                    timer_start = current_time
                    pygame.mixer.music.load(os.path.join('sfx', 'beep.wav'))
                    pygame.mixer.music.play()

            elif current_state == 11:
                if key == pygame.K_ESCAPE:
                    current_state = 12
                elif key == pygame.K_r:
                    r_pressed = True
                elif key in (pygame.K_1, pygame.K_KP1) and r_pressed:
                    current_state = 14
                    pygame.mixer.music.load(os.path.join('sfx', 'error.wav'))
                    pygame.mixer.music.play()

            elif current_state == 12:
                if key == pygame.K_s:
                    current_state = 101
                    timer_start = current_time
                elif key == pygame.K_ESCAPE:
                    current_state = 11

            elif current_state == 14:
                if key == pygame.K_F4:
                    current_state = 11

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                r_pressed = False

    elapsed = (current_time - timer_start) / 1000.0

    if current_state == 5 and elapsed >= 2.5:
        current_state = 6
        timer_start = current_time
    elif current_state == 6 and elapsed >= 3.0:
        current_state = 7
        timer_start = current_time
    elif current_state == 7 and elapsed >= 0.5:
        current_state = 8
        timer_start = current_time
    elif current_state == 8 and elapsed >= 0.75:
        current_state = 9
        pygame.mixer.music.load(os.path.join('sfx', 'startup.wav'))
        pygame.mixer.music.play()
        timer_start = current_time
    elif current_state == 9 and elapsed >= 3.0:
        current_state = 10
        timer_start = current_time
    elif current_state == 10 and elapsed >= 2.75:
        current_state = 11

    elif current_state == 101 and elapsed >= 1.75:
        current_state = 13
        pygame.mixer.music.load(os.path.join('sfx', 'shutdown.wav'))
        pygame.mixer.music.play()
        timer_start = current_time
    elif current_state == 13 and elapsed >= 3.0:
        current_state = 106
        timer_start = current_time
    elif current_state == 106 and elapsed >= 1.25:
        running = False

    display_img_num = current_state
    if current_state == 101:
        display_img_num = 10
    elif current_state == 106:
        display_img_num = 6

    screen.blit(images[display_img_num], (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
