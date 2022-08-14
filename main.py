
import pygame
from map_gernator import generate_random_bus_positions,generate_random_passenger,generate_square_grid_map
from Graphic_Engine import Graphic_Engine
from Simulation_Engine import Simulation_Engine



SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
TITLE = "Bus Route Simulation"
NUMBER_OF_PASSENGERS = 200
NUMBER_OF_BUSSES = 10
GRID_SIZE = 10 #10x10 grid
GRID_DISTANCE = 10
BUS_SPEED = 0.3
def main():
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    running = True
    clock = pygame.time.Clock()
    connections,positions = generate_square_grid_map(GRID_SIZE,GRID_DISTANCE,SCREEN_WIDTH,SCREEN_HEIGHT) 
    simulation = Simulation_Engine(connections)
    
    for pas in generate_random_passenger(NUMBER_OF_PASSENGERS,100):
        simulation.add_passenger(pas) 
    for bus in generate_random_bus_positions(NUMBER_OF_BUSSES,100,BUS_SPEED):
        simulation.add_bus(bus)

    gfx = Graphic_Engine(positions,connections,screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gfx.draw_all(simulation.buses,simulation.passengers)
        simulation.run_iteration()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()