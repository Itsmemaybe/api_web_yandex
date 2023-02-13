import pygame
import requests
import sys
import os

COORDS = 37.677751, 55.757718
SPN = '0.016457,0.00619'
bbox = '43.853866,56.348212~43.877595,56.341115'
scale = 1.0
z = 10
type_of_map = 'map'
map_request = f"http://static-maps.yandex.ru/1.x/?ll={COORDS[0]},{COORDS[1]}&spn={SPN}&l={type_of_map}&bbox={bbox}&z={z}&scale={scale}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
clock = pygame.time.Clock()
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Corbel', 35)
text1 = smallfont.render('map', True, color)
text2 = smallfont.render('sat', True, color)
text3 = smallfont.render('skl', True, color)
mouse = pygame.mouse.get_pos()
screen = pygame.display.set_mode((600, 450))
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove(map_file)
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 10 <= mouse[1] <= height + 50:
                type_of_map = 'map'
            if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 60 <= mouse[1] <= height + 100:
                type_of_map = 'sat'
            if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 110 <= mouse[1] <= height + 150:
                type_of_map = 'skl'
    clock.tick(20)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEUP]:
        if scale < 4:
            scale = float(int(scale) + 1)
    if keys[pygame.K_PAGEDOWN]:
        if scale > 1:
            scale = float(int(scale) - 1)
    bbox = bbox.split('~')
    bbox[0] = bbox[0].split(',')
    bbox[1] = bbox[1].split(',')
    if keys[pygame.K_RIGHT]:
        bbox[0][0] = str(float(bbox[0][0]) + 0.02372)
        bbox[1][0] = str(float(bbox[1][0]) + 0.02372)
    if keys[pygame.K_LEFT]:
        bbox[0][0] = str(float(bbox[0][0]) - 0.02372)
        bbox[1][0] = str(float(bbox[1][0]) - 0.02372)
    if keys[pygame.K_DOWN]:
        bbox[1][1] = str(float(bbox[1][1]) + 0.007)
        bbox[0][1] = str(float(bbox[0][1]) + 0.007)
    if keys[pygame.K_UP]:
        bbox[0][1] = str(float(bbox[0][1]) + 0.007)
        bbox[1][1] = str(float(bbox[1][1]) + 0.007)
    bbox[0] = ','.join(bbox[0])
    bbox[1] = ','.join(bbox[1])
    bbox = '~'.join(bbox)
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={COORDS[0]},{COORDS[1]}&spn={SPN}&l={type_of_map}&bbox={bbox}&z={z}&scale={scale}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 10 <= mouse[1] <= height + 50:
        pygame.draw.rect(screen, color_light, [width / 4 * 3, height + 10, 140, 40])
    if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 60 <= mouse[1] <= height + 100:
        pygame.draw.rect(screen, color_light, [width / 4 * 3, height + 60, 140, 40])
    if width / 4 * 3 <= mouse[0] <= width / 4 * 3 + 140 and height + 110 <= mouse[1] <= height + 150:
        pygame.draw.rect(screen, color_light, [width / 4 * 3, height + 110, 140, 40])
    else:
        pygame.draw.rect(screen, color_dark, [width / 4 * 3, height + 10, 140, 40])
        pygame.draw.rect(screen, color_dark, [width / 4 * 3, height + 60, 140, 40])
        pygame.draw.rect(screen, color_dark, [width / 4 * 3, height + 110, 140, 40])
    screen.blit(text1, (width / 4 * 3 + 50, height + 10))
    screen.blit(text2, (width / 4 * 3 + 50, height + 60))
    screen.blit(text3, (width / 4 * 3 + 50, height + 110))
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
