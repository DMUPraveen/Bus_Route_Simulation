import pygame
# from collections import defaultdict

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
    
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(60)
    
    # Close the window and quit.
    pygame.quit()
    

if __name__ == "__main__":
    main_test()