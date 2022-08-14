import pygame
# from collections import defaultdict
from random import random,randint,seed
from components import Passenger,Bus

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

NODE_SIZE = 5 
NODE_COLOR = BLACK
ROAD_COLOR = BLACK
def draw_roads(surface,node_position,connections):
    for i,j in connections:
        p1 = node_position[i]
        p2 = node_position[j]

        pygame.draw.circle(surface,NODE_COLOR,p1,NODE_SIZE)
        
        pygame.draw.circle(surface,NODE_COLOR,p2,NODE_SIZE)
        pygame.draw.line(surface,ROAD_COLOR,p1,p2)

def generate_random_map(n):


    def get_adjacenecy_list(i,j):
        l = []
        steps = [(1,0),(0,1),(-1,0),(0,-1)]
        for a,b in steps:
            na,nb = i+a,j+b
            if(0<=na<=(n-1)  and 0<=nb<=(n-1)):
                l.append(na*n+nb)
        return l

    GRID_SPACING = 30
    OFFSET = 10
    positions = {}
    connections =[] 
    for i in range(n):
        for j in range(n):
            node = i*n+j 
            position = (GRID_SPACING*i+OFFSET,GRID_SPACING*j+OFFSET)
            positions[node] = position
            cn = get_adjacenecy_list(i,j)
            connections.extend([(node,c) for c in cn])
            connections.extend([c,node] for c in cn)

    return connections,positions


def draw_passenger(surface,passenger:Passenger,node_positions):
    OFFSET_LIMIT= 10
    PASS_SIZE = 3
    FINISHED_PASSENGER = BLUE
    UNFINISHED_PASSENGER = RED
    PASSENGER_COLOR = FINISHED_PASSENGER if passenger.goal_reached else UNFINISHED_PASSENGER 
    if(passenger.limbo):
        return
    draw_pos = node_positions[passenger.current]
    seed(passenger.start*passenger.end*passenger.current)
    draw_pos = tuple(i+(random()-0.5)*OFFSET_LIMIT for i in draw_pos)
    pygame.draw.circle(surface,PASSENGER_COLOR,draw_pos,PASS_SIZE) 



def draw_bus(surface,bus:Bus,node_positions):
    HEIGHT= 7
    WIDTH = 10
    BUS_COLOR = YELLOW
    draw_pos = node_positions[bus.current]
    draw_pos = [draw_pos[0] - WIDTH/2,draw_pos[1]-HEIGHT/2]
    pygame.draw.rect(surface,BUS_COLOR,(*draw_pos,WIDTH,HEIGHT))
def generate_random_passenger(count,limit):
    return [Passenger(randint(0,limit-1),randint(0,limit-1)) for _ in range(count)]
    
def generate_random_bus_positions(count,limit):
    return [Bus(float('inf'),1,randint(0,limit-1)) for _ in range(count)]



















def main_test():
    
    pygame.init()
    
    # Set the width and height of the screen [width, height]
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("My Game")
    
    # Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    connections,positions = generate_random_map(10) 
    passengers = generate_random_passenger(200,100) 
    busses = generate_random_bus_positions(10,100)
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
        # --- Game logic should go here
    
        # --- Screen-clearing code goes here
    
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)
        draw_roads(screen,positions,connections) 
        # --- Drawing code should go here
        for passenger in passengers:
            
            draw_passenger(screen,passenger,positions)
        for bus in busses:
            draw_bus(screen,bus,positions)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()
    

if __name__ == "__main__":
    main_test()