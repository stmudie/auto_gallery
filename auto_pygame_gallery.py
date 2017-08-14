import pygame
from glob import glob
from time import sleep
from os.path import getmtime, join
import inotify.adapters
import inotify.constants
from pygame.locals import*
"""
aspect_scale.py - Scaling surfaces keeping their aspect ratio
Raiser, Frank - Sep 6, 2k++
crashchaos at gmx.net

This is a pretty simple and basic function that is a kind of
enhancement to pygame.transform.scale. It scales a surface
(using pygame.transform.scale) but keeps the surface's aspect
ratio intact. So you will not get distorted images after scaling.
A pretty basic functionality indeed but also a pretty useful one.

Usage:
is straightforward.. just create your surface and pass it as
first parameter. Then pass the width and height of the box to
which size your surface shall be scaled as a tuple in the second
parameter. The aspect_scale method will then return you the scaled
surface (which does not neccessarily have the size of the specified
box of course)

Dependency:
a pygame version supporting pygame.transform (pygame-1.1+)
"""
def aspect_scale(img, bx, by):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))

pygame.init()

path = b'/home/mudies/Downloads/'

black = (0, 0, 0)
w = 1600
h = 900
screen = pygame.display.set_mode((w, h))
screen.fill((black))
running = 1

i = inotify.adapters.Inotify()
i.add_watch(path)

font = pygame.font.SysFont('Arial Bold', 50)
pygame.display.set_caption('Box Test')

files = glob(join(path.decode(), '*.jpg'))
files.sort(key=getmtime, reverse=True)
index = 0

try:
    for event in i.event_gen():
        print('key')
        print(sum(pygame.key.get_pressed()))
        if event is not None:
            (header, type_names, watch_path, filename) = event
            if header.mask & inotify.constants.IN_CREATE:
                files = glob(join(path.decode(), '*.jpg'))
                files.sort(key=getmtime, reverse=True)
                index = 0
        if event is None:
            img = pygame.image.load(files[index])
            img = aspect_scale(img, 1600, 900)
            screen.fill((black))
            x, y = img.get_size()
            screen.blit(img, ((1600 - x) // 2, (900 - y) // 2))
            screen.blit(font.render('To Purchase: goo.glo/', True, (0, 0, 0)), (302, 852))
            screen.blit(font.render('To Purchase: goo.glo/', True, (200, 200, 200)), (300, 850))
            pygame.display.flip()
            sleep(3)
            index = index + 1 if index < len(files) - 1 else 0

finally:
    i.remove_watch(path)
