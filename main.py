
import pygame
from map_gernator import generate_random_bus_positions,generate_random_passenger,generate_square_grid_map
from Graphic_Engine import Graphic_Engine
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
TITLE = "Bus Route Simulation"
def main():
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    running = True
    clock = pygame.time.Clock()
    connections,positions = generate_square_grid_map(10,10) 

    passengers = generate_random_passenger(200,100) 
    busses = generate_random_bus_positions(10,100)

    gfx = Graphic_Engine(positions,connections,screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        gfx.draw_all(busses,passengers)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()