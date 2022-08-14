import pygame
# from collections import defaultdict
from random import random,seed
from components import Passenger,Bus

from map_gernator import generate_square_grid_map,generate_random_bus_positions,generate_random_passenger
from typing import List

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

NODE_SIZE = 5 
NODE_COLOR = BLACK
ROAD_COLOR = BLACK




class Graphic_Enign:
    def __init__(self,node_positions,connections,pygame_surface):
        self.node_positions = node_positions
        self.connections = connections
        self.surface = pygame_surface

    def draw_roads(self):
        for i,j,_ in self.connections:
            p1 = self.node_positions[i]
            p2 = self.node_positions[j]

            pygame.draw.circle(self.surface,NODE_COLOR,p1,NODE_SIZE)
            
            pygame.draw.circle(self.surface,NODE_COLOR,p2,NODE_SIZE)
            pygame.draw.line(self.surface,ROAD_COLOR,p1,p2)


    def draw_passenger(self,passenger:Passenger):
        OFFSET_LIMIT= 10
        PASS_SIZE = 3
        FINISHED_PASSENGER = BLUE
        UNFINISHED_PASSENGER = RED
        PASSENGER_COLOR = FINISHED_PASSENGER if passenger.goal_reached else UNFINISHED_PASSENGER 
        if(passenger.limbo):
            return
        draw_pos = self.node_positions[passenger.current]
        seed(passenger.start*passenger.end*passenger.current)
        draw_pos = tuple(i+(random()-0.5)*OFFSET_LIMIT for i in draw_pos)
        pygame.draw.circle(self.surface,PASSENGER_COLOR,draw_pos,PASS_SIZE) 



    def draw_bus(self,bus:Bus):
        HEIGHT= 7
        WIDTH = 10
        BUS_COLOR = YELLOW
        draw_pos1 = self.node_positions[bus.current]
        if(bus.destination is None):
            draw_pos = draw_pos1
        else:
            draw_pos2 = self.node_positions[bus.destination]
            percentage = bus.fractional_progress()
            draw_pos  = tuple(a+percentage*(b) for a,b in zip(draw_pos1,draw_pos2))
        draw_pos = [draw_pos[0] - WIDTH/2,draw_pos[1]-HEIGHT/2]
        pygame.draw.rect(self.surface,BUS_COLOR,(*draw_pos,WIDTH,HEIGHT))

    def draw_all(self,lb:List[Bus],lp:List[Passenger]):
        self.surface.fill(WHITE)
        self.draw_roads()
        for bus in lb:
            self.draw_bus(bus)
        for pas in lp:
            self.draw_passenger(pas)
















def main_test():
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 500
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Testing the Graphics")
    running = True
    clock = pygame.time.Clock()
    connections,positions = generate_square_grid_map(10,10) 

    passengers = generate_random_passenger(200,100) 
    busses = generate_random_bus_positions(10,100)

    gfx = Graphic_Enign(positions,connections,screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gfx.draw_all(busses,passengers)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    

if __name__ == "__main__":
    main_test()