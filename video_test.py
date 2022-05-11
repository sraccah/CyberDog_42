import sys
import time
# Pad Controller
import pygame
from pygame.locals import *
# Video Handling
import moviepy.editor
import cv2

video = cv2.VideoCapture("42logo_anim.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
resolution = video_image.shape[1::-1]
flags = FULLSCREEN | HWSURFACE | DOUBLEBUF

info = pygame.display.Info()
print(info)
window = pygame.display.set_mode(resolution, flags)
clock = pygame.time.Clock()

run = success
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    success, video_image = video.read()
    if success:
        video_surf = pygame.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
    else:
        run = False
    window.blit(video_surf, (0, 0))
    pygame.display.flip()

pygame.quit()
