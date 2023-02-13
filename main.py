import pygame
import requests
import sys
import os

COORDS = 37.677751, 55.757718
SPN = '0.016457,0.00619'
bbox = '43.853866,56.348212~43.877595,56.341115'
scale = 1.0
z = 10
map_request = f"http://static-maps.yandex.ru/1.x/?ll={COORDS[0]},{COORDS[1]}&spn={SPN}&l=map&bbox={bbox}&z={z}&scale={scale}"
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
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove(map_file)
            sys.exit()
    clock.tick(20)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEUP]:
        if scale < 4:
            scale = float(int(scale) + 1)
            print(scale)
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
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={COORDS[0]},{COORDS[1]}&spn={SPN}&l=map&bbox={bbox}&z={z}&scale={scale}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)