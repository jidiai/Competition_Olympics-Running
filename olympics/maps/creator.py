import pygame
import numpy as np
import sys
import math
import json

COLORS = {
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'yellow': [255, 255, 0],
    'grey':  [176,196,222],
    'purple': [160, 32, 240],
    'black': [0, 0, 0],
    'white': [255, 255, 255],
    'light green': [127,255,170],
    'sky blue': [0,191,255]
}

elements_wall = {
1: "draw_straight_1",
2: "draw_straight_2",
3: "draw_straight_corner_1",
4: "draw_straight_corner_2",
5: "draw_straight_corner_3",
6: "draw_straight_corner_4",
7: "draw_arc_corner_1",
8: "draw_arc_corner_2",
9: "draw_arc_corner_3",
10: "draw_arc_corner_4",
}
elements_agent = {
1: "draw_agent_to_east",
2: "draw_agent_to_north",
3: "draw_agent_to_west",
4: "draw_agent_to_south"
}
elements_cross = {
1: "draw_cross_to_east",
2: "draw_cross_to_north",
3: "draw_cross_to_west",
4: "draw_cross_to_south",
}
elements_triangle = {
1: "draw_triangle_to_east",
2: "draw_triangle_to_north",
3: "draw_triangle_to_west",
4: "draw_triangle_to_south",
5: "draw_triangle_5",
6: "draw_triangle_6",
7: "draw_triangle_7",
8: "draw_triangle_8",
9: "draw_triangle_9",
10: "draw_triangle_10",
11: "draw_triangle_11",
12: "draw_triangle_12",

}
def draw_straight_1(s_width, s_height, width, degree=None):
    points = [ [[s_width/2 - width/2,0], [s_width/2 - width/2, s_height]],
               [[s_width/2 + width/2,0], [s_width / 2 + width / 2, s_height]]]
    return points


def draw_straight_2(s_width, s_height, width, degree=None):
    points = [[[0, s_height / 2 - width / 2], [s_width, s_height / 2 - width / 2]],
              [[0, s_height / 2 + width / 2], [s_width, s_height / 2 + width / 2]]]
    return points

def draw_straight_corner_1(s_width, s_height, width, degree):
    points = [
        [[0, s_height / 2 - width / 2], [s_width / 2 + width / 2, s_height / 2 - width / 2]],
        [[0, s_height / 2 + width / 2], [s_width / 2 - width / 2, s_height / 2 + width / 2]],
        [[s_width / 2 - width / 2, s_height / 2 + width / 2], [s_width / 2 - width / 2, s_height]],
        [[s_width / 2 + width / 2, s_height / 2 - width / 2], [s_width / 2 + width / 2, s_height]]
    ]
    return points

def draw_straight_corner_2(s_width, s_height, width, degree):
    points = [
        [[s_height, s_height / 2 - width / 2], [s_width / 2 - width / 2, s_height / 2 - width / 2]],
        [[s_height, s_height / 2 + width / 2], [s_width / 2 + width / 2, s_height / 2 + width / 2]],
        [[s_width / 2 - width / 2, s_height / 2 - width / 2], [s_width / 2 - width / 2, s_height]],
        [[s_width / 2 + width / 2, s_height / 2 + width / 2], [s_width / 2 + width / 2, s_height]]
    ]
    return points

def draw_straight_corner_3(s_width, s_height, width, degree):
    points =  [
        [[0, s_height / 2 - width / 2], [s_width / 2 - width / 2, s_height / 2 - width / 2]],
        [[0, s_height / 2 + width / 2], [s_width / 2 + width / 2, s_height / 2 + width / 2]],
        [[s_width / 2 - width / 2, 0], [s_width / 2 - width / 2, s_height / 2 - width / 2]],
        [[s_width / 2 + width / 2, s_height / 2 + width / 2], [s_width / 2 + width / 2, 0]]
    ]
    return points

def draw_straight_corner_4(s_width, s_height, width, degree):
    points = [
        [[s_width / 2 - width / 2, 0], [s_width / 2 - width / 2, s_height / 2 + width / 2]],
        [[s_width / 2 + width / 2, 0], [s_width / 2 + width / 2, s_height / 2 - width / 2]],
        [[s_width / 2 + width / 2, s_height / 2 - width / 2], [s_width, s_height / 2 - width / 2]],
        [[s_width / 2 - width / 2, s_height / 2 + width / 2], [s_width, s_height / 2 + width / 2]]
    ]
    return points


def draw_arc_corner_1(s_width, s_height, width, degree):
    """
    arc = [[x,y], 2*raidus, radian_s, radian_end]
    """
    arc1 = [[-s_width/2-s_width/4, s_height / 2 - width / 2], 2*(s_width/2+s_width/4), 0, 90]
    arc2 = [ [-s_width/2+s_width/4, s_height / 2 + width / 2], 2*(s_width/2-s_width/4), 0, 90]
    return [arc1, arc2]

def draw_arc_corner_2(s_width, s_height, width, degree):
    arc1 = [[s_width/4, s_height / 2 - width / 2], 2*(s_width/2+s_width/4), 90, 180]
    arc2 = [ [3*s_width/4, s_height / 2 + width / 2], 2*(s_width/2-s_width/4), 90, 180]
    return [arc1, arc2]

def draw_arc_corner_3(s_width, s_height, width, degree):
    arc1 = [[-s_width/2-s_width/4, -s_height + s_height / 2 - width / 2], 2*(s_width/2+s_width/4), -90, 0]
    arc2 = [ [-s_width/2+s_width/4, -s_height + s_height / 2 + width / 2], 2*(s_width/2-s_width/4), -90, 0]
    return [arc1, arc2]

def draw_arc_corner_4(s_width, s_height, width, degree):
    arc1 = [[s_width/4, -s_height + s_height / 2 - width / 2], 2*(s_width/2+s_width/4), -180, -90]
    arc2 = [ [3*s_width/4, -s_height + s_height / 2 + width / 2], 2*(s_width/2-s_width/4), -180, -90]
    return [arc1, arc2]

def draw_agent_to_east(s_width, s_height, width, degree):
    r = (s_height / 2 - (s_height / 2 + s_height /4) /2 ) / 2
    agent1 = [[r*2,  (s_height / 2 + s_height /4) /2 ], r ]
    agent2 = [[r*2,  (s_height / 2 + 3*s_height /4) /2 ], r ]
    return [agent1, agent2]

def draw_agent_to_north(s_width, s_height, width, degree):
    r = (s_height / 2 - (s_height / 2 + s_height /4) /2 ) / 2
    agent1 = [[(s_width / 2 + s_width /4) /2 , s_height-r*2], r ]
    agent2 = [[(s_width / 2 + 3*s_width /4) /2 , s_height-r*2], r ]
    return [agent1, agent2]

def draw_agent_to_west(s_width, s_height, width, degree):
    r = (s_height / 2 - (s_height / 2 + s_height /4) /2 ) / 2
    agent1 = [[s_width-r*2, (s_height / 2 + s_height /4) /2 ], r ]
    agent2 = [[s_width-r*2, (s_height / 2 + 3*s_height /4) /2 ], r ]
    return [agent1, agent2]

def draw_agent_to_south(s_width, s_height, width, degree):
    r = (s_height / 2 - (s_height / 2 + s_height / 4) / 2) / 2
    agent1 = [[(s_width / 2 + s_width / 4) / 2, r*2], r]
    agent2 = [[(s_width / 2 + 3 * s_width / 4) / 2, r*2], r]
    return [agent1, agent2]

def draw_cross_to_east(s_width, s_height, width, degree):
    points = [
        [[0, s_height / 2 - width / 2], [0, s_height / 2 + width / 2]]
    ]
    return points

def draw_cross_to_north(s_width, s_height, width, degree):
    points = [
        [[s_width / 2 - width / 2,s_height], [s_width / 2 + width / 2,s_height]]
    ]
    return points

def draw_cross_to_west(s_width, s_height, width, degree):
    points = [
        [[s_width, s_height / 2 - width / 2], [s_width, s_height / 2 + width / 2]]
    ]
    return points

def draw_cross_to_south(s_width, s_height, width, degree):
    points = [
        [[s_width / 2 - width / 2,0], [s_width / 2 + width / 2,0]]
    ]
    return points

def draw_triangle_to_east(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [
        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)], # AB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + 3*s_height / 4) / 2)], # CB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + 3 * s_height / 4) / 2)],  # CB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]]

    ]
    return points

def draw_triangle_to_south(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [
        [[((s_width / 2 + 3*s_width / 4) / 2), (s_height / 2) - delta], # AB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta], # CB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta],  # AB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta],  # CB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

    ]
    return points

def draw_triangle_to_west(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [
        [[((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)], # AB
         [(s_width / 2) - delta, ((s_height / 2 + 3*s_height / 4) / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)], # CB
         [((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)]],

        [[((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)],  # AB
        [(s_width / 2) + delta, ((s_height / 2 + 3 * s_height / 4) / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)],  # CB
        [((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)]]
               ]
    return points

def draw_triangle_to_north(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [
        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],
        [((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],  # AB
        [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) - delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],
         [((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta]]

    ]
    return points

def draw_triangle_5(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [
        [[((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)],  # AB
         [(s_width / 2) - delta, ((s_height / 2 + 3 * s_height / 4) / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)],  # CB
         [((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],
         [((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta]]

    ]
    return points

def draw_triangle_6(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],
        [((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],  # AB
        [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) - delta]],

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + 3 * s_height / 4) / 2)],  # CB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]]

    ]
    return points

def draw_triangle_7(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[((s_width / 2 + 3*s_width / 4) / 2), (s_height / 2) - delta], # AB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta], # CB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)], # AB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + 3*s_height / 4) / 2)], # CB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

    ]
    return points

def draw_triangle_8(s_width, s_height, width, degree):
    delta = s_width / 4
    points = [

        [[((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta],  # AB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta],  # CB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

        [[((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)],  # AB
        [(s_width / 2) + delta, ((s_height / 2 + 3 * s_height / 4) / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)],  # CB
        [((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)]]
    ]
    return points

def draw_triangle_9(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + 3 * s_height / 4) / 2)],  # CB
         [((s_width / 2 + 3 * s_width / 4) / 2) - delta, (s_height / 2)]],

        [[((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta],  # AB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta],  # CB
         [(s_width / 2), ((s_height / 2 + 3 * s_height / 4) / 2) + delta]],

    ]
    return points

def draw_triangle_10(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[((s_width / 2 + 3*s_width / 4) / 2), (s_height / 2) - delta], # AB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta], # CB
         [(s_width / 2), ((s_height / 2 + 3*s_height / 4) / 2) - delta]],

        [[((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)],  # AB
         [(s_width / 2) - delta, ((s_height / 2 + 3 * s_height / 4) / 2)]],

        [[(s_width / 2) - delta, ((s_height / 2 + s_height / 4) / 2)],  # CB
         [((s_width / 2 + s_width / 4) / 2) - delta, (s_height / 2)]],

    ]
    return points

def draw_triangle_11(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)],  # AB
        [(s_width / 2) + delta, ((s_height / 2 + 3 * s_height / 4) / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)],  # CB
        [((s_width / 2 + s_width / 4) / 2) + delta, (s_height / 2)]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],
        [((s_width / 2 + s_width / 4) / 2), (s_height / 2) - delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) - delta],  # AB
        [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) - delta]],

    ]
    return points

def draw_triangle_12(s_width, s_height, width, degree):
    delta = s_width / 4

    points = [

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],
         [((s_width / 2 + s_width / 4) / 2), (s_height / 2) + delta]],

        [[(s_width / 2), ((s_height / 2 + s_height / 4) / 2) + delta],  # AB
         [((s_width / 2 + 3 * s_width / 4) / 2), (s_height / 2) + delta]],

        [[(s_width / 2) + delta, ((s_height / 2 + s_height / 4) / 2)], # AB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

        [[(s_width / 2) + delta, ((s_height / 2 + 3*s_height / 4) / 2)], # CB
         [((s_width / 2 + 3*s_width / 4) / 2) + delta, (s_height / 2)]],

    ]
    return points



def test_element(s_width, s_height, width):
    pygame.init()
    size = s_width, s_height
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        points = draw_straight_1(s_width, s_height, width)
        pygame.draw.line(screen, [0,0,0], start_pos = points[0][0], end_pos = points[0][1], width = 2)
        pygame.draw.line(screen, [0,0,0], start_pos = points[1][0], end_pos = points[1][1], width = 2)

        points = draw_straight_2(s_width, s_height, width)
        pygame.draw.line(screen, [0, 0, 0], start_pos=points[0][0], end_pos=points[0][1], width=2)
        pygame.draw.line(screen, [0, 0, 0], start_pos=points[1][0], end_pos=points[1][1], width=2)


        # points = draw_straight_corner_4(s_width, s_height, width, degree=None)
        # for p in points:
        #     pygame.draw.line(screen, [0, 0, 0], start_pos=p[0], end_pos=p[1], width=2)

        arc1, arc2 = draw_arc_corner_1(s_width, s_height, width, degree=None)
        pygame.draw.arc(screen, [0, 0, 0], [arc1[0][0], arc1[0][1], arc1[1], arc1[1]], arc1[2]*math.pi/180, arc1[3]*math.pi/180, 2)
        pygame.draw.arc(screen, [0, 0, 0], [arc2[0][0], arc2[0][1], arc2[1], arc2[1]], arc2[2]*math.pi/180, arc2[3]*math.pi/180, 2)

        points = draw_triangle_to_south(s_width, s_height, width, degree=None)
        for p in points:
            pygame.draw.line(screen, [0, 0, 0], start_pos=p[0], end_pos=p[1], width=2)

        pygame.display.flip()



def test_viewer(s_width, s_height, edge, points, arcs, agents, crosses, ends, triangles):
    pygame.init()
    size = s_width+2*edge, s_height+2*edge
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # points = draw_straight_1(s_width, s_height, width)
        # pygame.draw.line(screen, [0,0,0], start_pos = points[0][0], end_pos = points[0][1], width = 2)
        # pygame.draw.line(screen, [0,0,0], start_pos = points[1][0], end_pos = points[1][1], width = 2)
        #
        # points = draw_straight_2(s_width, s_height, width)
        # pygame.draw.line(screen, [0, 0, 0], start_pos=points[0][0], end_pos=points[0][1], width=2)
        # pygame.draw.line(screen, [0, 0, 0], start_pos=points[1][0], end_pos=points[1][1], width=2)

        for p in points:

            pygame.draw.line(screen, COLORS["black"], start_pos=p[0], end_pos=p[1], width=2)

        for arc in arcs:
            pygame.draw.arc(screen, COLORS["black"], [arc[0][0], arc[0][1], arc[1], arc[1]], arc[2] * math.pi / 180,
                            arc[3] * math.pi / 180, 2)

        for agent in agents:
            pygame.draw.circle(screen, COLORS["purple"], agent[0], agent[1], 4)

        for c in crosses:
            pygame.draw.line(screen, COLORS["red"], start_pos=c[0], end_pos=c[1], width=2)

        for e in ends:
            pygame.draw.line(screen, COLORS["black"], start_pos=e[0], end_pos=e[1], width=2)

        for tr in triangles:
            pygame.draw.line(screen, COLORS["sky blue"], start_pos=tr[0], end_pos=tr[1], width=2)

        pygame.display.flip()


def get_all_elements(map_list, s_width, s_height, width, edge, degree=None):
    points_all = list()
    arcs_all = list()
    for i in range(np.array(map_list).shape[0]):
        for j in range(np.array(map_list).shape[1]):
            index = map_list[i][j]
            if (index >0) and (index <=6) :
                points = eval(elements_wall[index])(s_width, s_height, width, degree=None)
                points_ = [[ [p[0]+j*s_width+edge, p[1]+i*s_height+edge] for p in l ] for l in points]
                points_all.extend(points_)
            elif index > 6:
                arcs = eval(elements_wall[index])(s_width, s_height, width, degree=None)
                arcs_ = [[[a[0][0]+j*s_width+edge,a[0][1]+i*s_height+edge],a[1],a[2],a[3]] for a in arcs]
                arcs_all.extend(arcs_)
            else:
                continue
    return points_all, arcs_all

def get_map_json(points_all, arcs_all, agents_all, crosses_all, ends_all, triangles_all, width,height,edge):
    map = { key: {"num":0,  "objects":{} } for key in ["wall", "arc", "cross", "agent"]}
    map["view"] = {"width":width, "height":height,"edge":edge}
    for p, points in enumerate(points_all+ends_all):
        map["wall"]["num"] += 1
        obj = map["wall"]["objects"]
        c = "component"+str(p+1)
        obj[c] = dict()
        obj[c]["initial_position"] = points
        p1, p2 = points
        obj[c]["length"] = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        obj[c]["color"] = "black" # todo1

    for a, arcs in enumerate(arcs_all):
        map["arc"]["num"] += 1
        obj = map["arc"]["objects"]
        c = "component" + str(a + 1)
        obj[c] = dict()
        obj[c]["initial_position"] = [arcs[0][0],arcs[0][1],arcs[1],arcs[1]]
        obj[c]["start_radian"] = arcs[2]
        obj[c]["end_radian"] = arcs[3]
        obj[c]["passable"] = "False"
        obj[c]["color"] = "black"  # todo

    for ag, agent in enumerate(agents_all):
        map["agent"]["num"] += 1
        obj = map["agent"]["objects"]
        c = "component" + str(ag + 1)
        obj[c] = dict()
        obj[c]["initial_position"] = agent[0]
        obj[c]["mass"] = 1
        obj[c]["radius"] = agent[1]
        obj[c]["color"] = "purple"  if ag ==0 else "green" # todo

    for cr, cross in enumerate(crosses_all + triangles_all):
        map["cross"]["num"] += 1
        obj = map["cross"]["objects"]
        c = "component" + str(cr + 1)
        obj[c] = dict()
        obj[c]["initial_position"] = cross
        p1, p2 = cross
        obj[c]["length"] = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        obj[c]["color"] = "red" if cr ==0 else "grey" # todo1

    # for tr, triangle in enumerate(triangles_all):
    #     map["cross"]["num"] += 1
    #     obj = map["cross"]["objects"]
    #     c = "component" + str(tr + 1)
    #     obj[c] = dict()
    #     obj[c]["initial_position"] = triangle
    #     p1, p2 = triangle
    #     obj[c]["length"] = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    #     obj[c]["color"] = "grey"  # todo1

    return map



def get_agent_position(map_list, s_width, s_height, width, edge, degree=None):
    agents_all = list()
    map_shape = np.array(map_list).shape
    for i in range(map_shape[0]):
        for j in range(map_shape[1]):
            index = map_list[i][j]
            if (index > 0):
                agents = eval(elements_agent[index])(s_width, s_height, width, degree=None)
                agents_ = [[[a[0][0] + j * s_width+edge, a[0][1] + i * s_height+edge], a[1]] for a in agents]
                agents_all.extend(agents_)
            else:
                continue
    return agents_all

def get_cross_position(map_list, s_width, s_height, width, edge, degree=None):
    crosses_all = list()
    map_shape = np.array(map_list).shape
    for i in range(map_shape[0]):
        for j in range(map_shape[1]):
            index = map_list[i][j]
            if (index > 0):
                points = eval(elements_cross[index])(s_width, s_height, width, degree=None)
                points_ = [[[p[0] + j * s_width+edge, p[1] + i * s_height+edge] for p in l] for l in points]
                crosses_all.extend(points_)
            else:
                continue
    return crosses_all

def get_triangle_position(map_list, s_width, s_height, width, edge, degree=None):
    points_all = list()
    map_triangle = map_list[4]
    map_corner = map_list[0]
    for i in range(np.array(map_triangle).shape[0]):
        for j in range(np.array(map_triangle).shape[1]):
            index = map_triangle[i][j]
            if (index >0) :
                points = eval(elements_triangle[index])(s_width, s_height, width, degree=None)
                delta = s_height / 4
                # if map_corner[i][j]  == 7:
                #     points_ = [[[p[0] - s_width/8 + j * s_width + edge, p[1] + s_height/8 + i * s_height + edge] for p in l] for l in points[:2]]
                #
                # elif map_corner[i][j] == 8:
                #     points_ = [[[p[0] + s_width/8 + j * s_width + edge, p[1] + s_height/8 + i * s_height + edge] for p in l] for l in points[:2]]
                #
                # elif map_corner[i][j] == 9:
                #     points_ = [[[p[0] - s_width/8 + j * s_width + edge, p[1] - s_height/8 + i * s_height + edge] for p in l] for l in points[:2]]
                #
                # elif map_corner[i][j] == 10:
                #     points_ = [[[p[0] + s_width/8 + j * s_width + edge, p[1] - s_height/8 + i * s_height + edge] for p in l] for l in points[:2]]
                #
                # elif map_corner[i][j] in [3,4,5,6]:
                #     points_ = [[[p[0] + j * s_width + edge, p[1] + i * s_height + edge] for p in l] for l in points[:2]]
                #
                # else:
                #     points_ = [[[p[0] + j * s_width + edge, p[1]  + i * s_height + edge] for p in l] for l in points]
                points_ = [[[p[0] + j * s_width + edge, p[1] + i * s_height + edge] for p in l] for l in points]

                # else:
                #     raise ValueError("Has error !! Need to check map")
                points_all.extend(points_)
            else:
                continue
    return points_all

def store(record, name):
    # with open(name+'.json', 'w') as f:
    #     f.write(json.dumps(record))
    #     f.close()
    fp = open(name+'.json', 'w')
    fp.write(json.dumps(record))
    fp.close()

if __name__ == "__main__":
    # test_element(300,300,150)

    BIG_W, BIG_H = 600, 600
    W, H = 150, 150
    w = W/2
    edge = 50

    # # ===================================== map1:
    # map_list = [[[2, 2, 2, 3], # wall
    #             [4, 2, 2, 5],
    #             [6, 2, 2, 3],
    #              [2, 2, 2, 5]],
    #             [[1,0,0, 0],  # agent
    #              [0,0,0,0],
    #              [0,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 0], # cross
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [1, 0, 0, 0]],
    #             [[1, 0, 0, 0],  # end wall
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[1, 1, 1, 9],  # triangle
    #              [8, 3, 3, 10],
    #              [7, 1, 1, 9],
    #              [3, 3, 3, 10]],
    #             ]

    # ===================================== map2:
    # map_list = [[[8, 2, 2, 7], # wall
    #             [1, 0, 0, 1],
    #             [1, 0, 0, 1],
    #              [10, 2, 2, 9]],
    #             [[0,1,0, 0],  # agent
    #              [0,0,0,0],
    #              [0,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 0], # cross
    #              [4, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[0, 1, 0, 0],  # end wall
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[0, 1, 1, 9],  # triangle
    #              [2, 0, 0, 4],
    #              [2, 0, 0, 4],
    #              [11, 3, 3, 10]],
    #             ]

    # # ===================================== map3:
    # map_list = [[[4, 3, 0, 0], # wall
    #             [5, 1, 4, 3],
    #             [4, 5, 1, 6],
    #              [6, 2, 5, 0]],
    #             [[0,0,0, 0],  # agent
    #              [1,0,0,0],
    #              [0,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 0], # cross
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 3],
    #              [0, 0, 0, 0]],
    #             [[0, 0, 0, 0],  # end wall
    #              [1, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[12, 9, 0, 0],  # triangle
    #              [6, 4, 12, 9],
    #              [8, 10, 2, 7],
    #              [7, 1, 6, 0]],
    #             ]

    # ===================================== map4:
    #
    # BIG_W, BIG_H = 600, 600
    # W, H = 200, 200
    # w = W/2
    # edge = 50
    #
    #
    # map_list = [[[0, 0, 0], # wall
    #             [2, 2, 2],
    #             [0, 0, 0]],
    #             [[0,0,0],  # agent
    #              [1,0,0],
    #              [0,0,0]
    #              ],
    #              [[0, 0, 0], # cross
    #              [0, 0, 3],
    #              [0, 0, 0],
    #              ],
    #             [[0, 0, 0],  # end wall
    #              [1, 0, 0],
    #              [0, 0, 0],
    #              ],
    #             [[0, 0, 0],  # triangle
    #              [1, 1, 1],
    #              [0, 0, 0],
    #              ],
    #             ]

    # # ===================================== map5:

    # BIG_W, BIG_H = 600, 600
    # W, H = 300, 300
    # w = W/2
    # edge = 50
    #
    #
    # map_list = [[[8, 7], # wall
    #             [10, 2]
    #             ],
    #             [[0,0],  # agent
    #              [0,3]
    #              ],
    #              [[0, 2], # cross
    #              [0, 0]
    #              ],
    #             [[0, 0],  # end wall
    #              [0, 3],
    #              ],
    #             [[12, 9],  # triangle
    #              [11, 3]
    #              ],
    #             ]

    # # ===================================== map6:
    # map_list = [[[0, 0, 0, 0], # wall
    #             [8, 7, 8, 7],
    #             [9, 10, 9, 10],
    #              [0, 0, 0, 0]],
    #             [[0,0,0, 0],  # agent
    #              [0,0,0,0],
    #              [1,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 0], # cross
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 3],
    #              [0, 0, 0, 0]],
    #             [[0, 0, 0, 0],  # end wall
    #              [0, 0, 0, 0],
    #              [1, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[0, 0, 0, 0],  # triangle
    #              [12, 9, 12, 9],
    #              [6, 7, 6, 7],
    #              [0, 0, 0, 0]],
    #             ]

    # # ===================================== map7:
    # BIG_W, BIG_H = 600, 600
    # W, H = 120, 120
    # w = W/2
    # edge = 50
    #
    # map_list = [[[3, 0, 0, 0,0], # wall
    #             [6, 3, 0, 0,0,],
    #             [0, 6, 3, 0,0],
    #              [0, 0, 6, 3,0],
    #              [0,0,0,6,3]],
    #             [[1,0,0, 0,0],  # agent
    #              [0,0,0,0,0],
    #              [0,0,0,0,0],
    #              [0,0,0,0,0],
    #              [0,0,0,0,0]],
    #              [[0, 0, 0, 0,0], # cross
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #               [0,0,0,0,2]],
    #             [[1, 0, 0, 0,0],  # end wall
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0,0,0,0,0]],
    #             [[9, 0, 0, 0,0],  # triangle
    #              [7, 9, 0, 0,0],
    #              [0, 7, 9, 0,0],
    #              [0, 0, 7, 9,0],
    #              [0, 0, 0, 7,9]],
    #             ]

    # # ===================================== map8:
    # BIG_W, BIG_H = 600, 600
    # W, H = 120, 120
    # w = W/2
    # edge = 50
    #
    # map_list = [[[8, 2, 7, 0,0], # wall
    #             [9, 8, 10, 2,7],
    #             [0, 10, 7, 8,9],
    #              [8, 2, 9, 10,7],
    #              [10,2,2,2,9]],
    #             [[0,0,0, 0,0],  # agent
    #              [1,0,0,0,0],
    #              [0,0,0,0,0],
    #              [0,0,0,0,0],
    #              [0,0,0,0,0]],
    #              [[0, 0, 0, 0,0], # cross
    #              [0, 3, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #               [0,0,0,0,0]],
    #             [[0, 0, 0, 0,0],  # end wall
    #              [1, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0, 0, 0, 0,0],
    #              [0,0,0,0,0]],
    #             [[12, 1, 9, 0,0],  # triangle
    #              [6, 12, 7, 1,9],
    #              [0, 11, 5, 8,10],
    #              [12, 1, 6, 7,9],
    #              [11, 3, 3, 3,10]],
    #             ]

    # ===================================== map9:
    # map_list = [[[1, 8, 7, 1], # wall
    #             [1, 1, 1, 1],
    #             [1, 1, 1, 1],
    #              [10, 9, 10, 9]],
    #             [[4,0,0, 0],  # agent
    #              [0,0,0,0],
    #              [0,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 4], # cross
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[4, 0, 0, 0],  # end wall
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[4, 12, 9, 2],  # triangle
    #              [4, 2, 4, 2],
    #              [4, 2, 4, 2],
    #              [7, 6, 7, 6]],
    #             ]
    # # # ===================================== map10:
    # map_list = [[[2, 2, 2, 7], # wall
    #             [8, 2, 7, 1],
    #             [1, 2, 9, 1],
    #              [10, 2, 2, 9]],
    #             [[1,0,0, 0],  # agent
    #              [0,0,0,0],
    #              [0,0,0,0],
    #              [0,0,0,0]],
    #              [[0, 0, 0, 0], # cross
    #              [0, 0, 0, 0],
    #              [0, 1, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[1, 0, 0, 0],  # end wall
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0],
    #              [0, 0, 0, 0]],
    #             [[1, 1, 1, 9],  # triangle
    #              [12, 1, 9, 4],
    #              [2, 3, 10, 4],
    #              [11, 3, 3, 10]],
    #             ]
    # # # ====================================== map 11:
    BIG_W, BIG_H = 600, 600
    W, H = 200, 200
    w = W/2
    edge = 50


    map_list = [[[2, 0, 2], # wall
                [0, 1, 0],
                [0, 1, 0]],
                [[0,0,0],  # agent
                 [1,0,0],
                 [0,0,0]
                 ],
                 [[0, 0, 0], # cross
                 [0, 0, 3],
                 [0, 0, 0],
                 ],
                [[0, 0, 0],  # end wall
                 [1, 0, 0],
                 [0, 0, 0],
                 ],
                [[0, 0, 0],  # triangle
                 [1, 1, 1],
                 [0, 0, 0],
                 ],
                ]






    points_in_map, arcs_in_map = get_all_elements(map_list[0], s_width=W, s_height=H, width=w, edge=edge,degree=None)
    print("check points: ", points_in_map)
    print("check arcs: ", arcs_in_map)
    agents_in_map = get_agent_position(map_list[1], s_width=W, s_height=H, width=w, edge=edge, degree=None)
    print("check agents points: ", agents_in_map)
    crosses_in_map = get_cross_position(map_list[2], s_width=W, s_height=H, width=w, edge=edge, degree=None)
    print("check crosses points: ", crosses_in_map)
    ends_in_map = get_cross_position(map_list[3], s_width=W, s_height=H, width=w, edge=edge, degree=None)
    print("check ends points: ", ends_in_map)
    triangles_in_map = get_triangle_position(map_list, s_width=W, s_height=H, width=w, edge=edge, degree=None)
    print("check triangle points: ", triangles_in_map)
    test_viewer(BIG_W, BIG_H, edge, points_in_map, arcs_in_map, agents_in_map,  crosses_in_map, ends_in_map, triangles_in_map)
    #
    map = get_map_json(points_in_map,arcs_in_map,agents_in_map, crosses_in_map, ends_in_map, triangles_in_map, width=BIG_W,height=BIG_H, edge=edge)

    print("map: ", map)
    #store(map,name="test1")