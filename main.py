import pygame
import sys
from pygame.locals import *
from math import sqrt, pi

from config import *

from filesys.srh import FileSys

from gfx.render import ItemRender, ItemWheel
from gfx.focus import Focus

class Main:
    def __init__(self):
        self.win = pygame.display.set_mode(WISZ)

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.fs = FileSys('C://')
        self.focus = Focus(self)
        self.renderer = {}

    def update_renders(self):
        tree = self.fs.tree

        centre = [0, 0, 10]
        dim = (5, 5, 5)
        x, y, z = 0, 0, 0
        xstep = 100

        self.renders = {}
        for folder in tree:
            self.renders[folder] = []
            
            self.renders[folder].append(ItemRender(
                tuple(centre), dim, 1
            ))
            x += xstep
            centre[0] = x

            items = tree[folder]
            self.renders[folder].append(ItemWheel(
                tuple(centre.copy()), 3, items
            ))

    def render_tree_items(self):
        pos, focusrot, focusrot2 = self.focus.pos, self.focus.rot, self.focus.rot2

        for folder in self.renders:
            data = self.renders[folder]
            itemren = data[0]
            itemwhe = data[1]

            itemren.vertex_proc(pos, focusrot, focusrot2)
            itemren.render(self.win, pos)

            itemwhe.vertex_proc(pos, focusrot, focusrot2)
            itemwhe.wrender(self.win, pos)

    def get_focused(self):
        curr_folder = self.fs.curr

        if curr_folder in self.renders:
            self.focus.pos = self.renders[curr_folder][0].centre
        else:
            for key in self.renders:
                if curr_folder in self.renders[key]:
                    self.focus.pos = self.renders[key][1].centre


    def search(self, folder):
        self.fs.search(folder)
        self.update_renders()


    def run(self):
        self.search(self.fs.base)
        while 1:
            self.dt = self.clock.tick(10_000) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.QUIT()
                    sys.exit()

            self.get_focused()

            self.win.fill((0, 0, 0))

            self.focus.rot += 10 * self.dt

            self.render_tree_items()

            pygame.display.flip()

if __name__ == '__main__':
    main = Main()
    main.run()



