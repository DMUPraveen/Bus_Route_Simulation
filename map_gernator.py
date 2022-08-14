from random import randint
from components import Bus,Passenger
def generate_square_grid_map(n,distance,width,height):


    def get_adjacenecy_list(i,j):
        l = []
        steps = [(1,0),(0,1),(-1,0),(0,-1)]
        for a,b in steps:
            na,nb = i+a,j+b
            if(0<=na<=(n-1)  and 0<=nb<=(n-1)):
                l.append(na*n+nb)
        return l

    GRID_SPACING = 50
    OFFSETX = (width - GRID_SPACING*(n-1))/2
    OFFSETY =  (height - GRID_SPACING*(n-1))/2
    positions = {}
    connections =[] 
    for i in range(n):
        for j in range(n):
            node = i*n+j 
            position = (GRID_SPACING*i+OFFSETX,GRID_SPACING*j+OFFSETY)
            positions[node] = position
            cn = get_adjacenecy_list(i,j)
            connections.extend((node,c,distance) for c in cn)
            connections.extend((c,node,distance) for c in cn)

    return connections,positions


def generate_random_passenger(count,limit):
    return [Passenger(randint(0,limit-1),randint(0,limit-1)) for _ in range(count)]
    
def generate_random_bus_positions(count,limit):
    return [Bus(float('inf'),0.3,randint(0,limit-1)) for _ in range(count)]