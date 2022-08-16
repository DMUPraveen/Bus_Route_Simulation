from components import Bus,Passenger,EdgeGroups,Graph,EdgeParameters,GlobalClock
import logging
from typing import List,Iterable,Any



logging.basicConfig(level=logging.DEBUG)
def disfunc(e:EdgeParameters):
    return e.distance

def upgrade(e:EdgeParameters):
    e.weight += 1

def downgrade(e:EdgeParameters,val=1):
    e.weight -=val

def edge_iterator(path:List[Any])->Iterable[Any]:
    return ((path[i],path[i+1]) for i in range(0,len(path)-1))
    

class Simulation_Engine:
    def __init__(self,graph_conections):
        self.roads = Graph(graph_conections)
        self.passengers:List[Passenger] = []
        self.buses:List[Bus] = []
        self.edgegroups = EdgeGroups()
        self.global_clock =GlobalClock() 
    def simulation_time(self):
        return self.global_clock.now()
    def finished(self)->bool:
        for pas in self.passengers:
            if(not pas.goal_reached):
                return False
        return True
    def add_passenger(self,pas:Passenger):
        # logging.info("Adding Passenger")
        if(pas.start == pas.end):
            logging.info("Passengers destination is the same as the starting position --IGNORING")
            return
        # pas = Passenger(start,end)
        self.passengers.append(pas)
        pas.calculate_path(self.roads,disfunc)
        for u,v in edge_iterator(pas.path):
            upgrade(self.roads.get_edge_parameter(u,v))
        self.edgegroups.add_passenger(pas)
    def add_bus(self,bus:Bus):
        self.buses.append(bus)
    def run_iteration(self):
        delta = 1
        self.global_clock.tick(delta)
        for bus in self.buses:
            arrived = bus.update_bus_pos(delta)
            if(not arrived):
                continue
            #The bus has arrived at its destination
            passengers = bus.arrive_and_unload_passengers()
            for pas in passengers:
                pas.move()
            self.edgegroups.load_passengers(passengers)
            
            #Now the passengers have been unloaded

            #Its time to load more passengers
            current_node = bus.current
            best_edge = self.edgegroups.best_of(list((current_node,child) for child in self.roads.get_children(current_node)))
            if(best_edge is not None):
                #We have found a descent edge to follow next we have to load the appropriate passengers and update the weight of the graph as well
                passengers = self.edgegroups.get_passsengers(*best_edge)
                downgrade(self.roads.get_edge_parameter(*best_edge),len(passengers))

                bus.load_passengers_and_start(passengers,best_edge[0],best_edge[1],self.roads.get_edge_parameter(*best_edge).distance)
                

            else:
                #There are no passengers going from the current node now we have to find a node that does!
                best = None
                best_distance = float('inf')
                for u,v in self.edgegroups.dic:
                    if(self.edgegroups.dic[(u,v)]):
                       path,dis = self.roads.shortest(current_node,u)
                       if(dis < best_distance):
                            best = path[1]
                if(best is not None):
                    bus.load_passengers_and_start([],current_node,best,self.roads.get_edge_parameter(current_node,best).distance)
            
