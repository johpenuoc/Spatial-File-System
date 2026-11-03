import pygame
import sys
from math import cos, sin, radians, pi, sqrt


from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import *

class Renderer:
    def __init__(self):
        self.fov = 0

    def translate_coord(self, x, y):
        return x + (WISZ[0] / 2), y + (WISZ[1] / 2)

    def point(self, x, y, s):
        pygame.draw.rect(self.main.dis, (255, 255, 255), (x, y, s, s))

    def translate_Z(self, x, y, z):
        return (x / z) * RENDER_SCALE, (y / z) * RENDER_SCALE,

    def yrotate(self, x, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (z * s)
        _z = (x * s) + (z * c)

        return _x, _z

    def xrotate(self, y, z, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _y = (y * c) - (z * s)
        _z = (y * s) + (z * c)

        return _y, _z

    def zrotate(self, x, y, theta):
        c = cos(radians(theta))
        s = sin(radians(theta))
        _x = (x * c) - (y * s)
        _y = (x * s) + (y * c)

        return _x, _y

    def connect(self, p1, p2, dis):
        pygame.draw.line(dis, (255, 255, 255), (p1[0], p1[1]), (p2[0], p2[1]))

    def vertex_proc(self, pos, focusrot, focusrot2):
        points = self.obj[0]
        centre = self.obj[1]

        focuspos = pos
        for id, p in enumerate(points):
            perspx = focuspos[0] - p[0] + centre[0]
            perspy = focuspos[1] - p[1] + centre[1]
            perspz = focuspos[2] - p[2] + centre[2]

            x, z = self.yrotate(perspx, perspz, focusrot)
            y, z = self.xrotate(perspy, z, focusrot2)

            buf = [0, 0, (x, y, z)]

            x, y = self.translate_Z(x, y, z)
            x, y = self.translate_coord(x, y)


            buf[0] = x
            buf[1] = y
            points[id][-1] = buf

    def render(self, dis, focuspos):
        points = self.obj[0]
        points_index = self.obj[2]

        for id, p_id in enumerate(points_index):
            if (id + 1) % 3 == 0:
                i1 = points_index[id - 1]
                i2 = points_index[id - 2]

                p = points[p_id][-1]
                p1 = points[i1][-1]
                p2 = points[i2][-1]

                p = p[:2]
                p1 = p1[:2]
                p2 = p2[:2]

                colour = tuple(self.obj[3])
                pygame.draw.polygon(dis, colour, (p, p1, p2))
                #print(p)

    def wrender(self, dis, focuspos):
        points = self.obj[0]
        points_index = self.obj[2]

        for id, p_id in enumerate(points_index):
            i1 = points_index[id - 1]

            p = points[p_id][-1]
            p1 = points[i1][-1]

            p = p[:2]
            p1 = p1[:2]

            colour = tuple(self.obj[3])
            
            pygame.draw.line(dis, (255, 255, 255), p, p1)
            pygame.draw.rect(dis, colour, (p1[0], p1[1], 5, 5), 1)

                
COLOURS = {
    0 : (0, 0, 0),
    1 : (255, 0, 0),
    2 : (0, 255, 0),
    3 : (0, 0, 255),
    4 : (255, 255, 0),
    5 : (255, 0, 255),
    6 : (0, 255, 255),
    7 : (255, 255, 255)
}
class ItemRender(Renderer):
    def __init__(self, centre, dim, colour):
        super().__init__()
        self.centre = centre
        width2 = dim[0] / 2
        height2 = dim[1] / 2
        depth2 = dim[2] / 2
        points = [
            # top left                      bottom left                 top right                    bottom right
            [-width2, -height2, -depth2], [-width2, height2, -depth2], [width2, -height2, -depth2], [width2, height2, -depth2],
            [-width2, -height2, depth2], [-width2, height2, depth2], [width2, -height2, depth2], [width2, height2, depth2]
        ]
        points = [[*i, i] for i in points]

        index = [

            # back
            0, 1, 2,
            3, 2, 1,

            # top
            0, 2, 6,
            6, 4, 0,

            # front
            4, 5, 7,
            7, 6, 4,

            # bottom
            1, 3, 7,
            7, 5, 1,

            # left
            0, 1, 5,
            5, 4, 0,

            # right
            2, 3, 7,
            7, 6, 2

        ]

        self.obj = [
            points, centre, index, COLOURS[colour]
        ]

class ItemWheel(Renderer):
    def __init__(self, centre, colour, items):
        super().__init__()
        self.items = items
        self.centre = centre

        rad = len(self.items)
        t_step = 360 / (len(items) - 2)#sqrt(dim[0]**2 + dim[1]**2)

        # generate circle
        theta = 0
        points = []
        print(self.centre)
        for i in range(len(items)):
            z = rad * cos(radians(theta))
            y = rad * sin(radians(theta))

            points.append([self.centre[0], self.centre[1] + y, self.centre[2] - z, theta, items[i]])

            theta += t_step

        points = [[i[0], i[1], i[2], i] for i in points]

        index = [i for i in range(len(points) - 1)]
        #index.append(0)

        self.obj = [
            points, centre, index, COLOURS[colour]
        ]