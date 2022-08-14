from collections import defaultdict
from queue import PriorityQueue
import unittest
from typing import List,Dict,Tuple,Any
import logging
logging.basicConfig(level=logging.DEBUG)


class GlobalClock:
    def __init__(self):
        self.time = 0
    def now(self):
        return self.time
    def tick(self,delta = 1):
        self.time +=delta 
class EdgeParameters:
    def __init__(self,distance):
        self.distance = distance
        self.weight = 0



class Graph:
    def __init__(self,edge_list):
        #edge list needs to be given in the (u,v,d) format where u->v road has distance(or time cost) of d
        self.dic = defaultdict(lambda:[]) 
        self.edge_map = {} #stores information about edges  
        for u,v,d in edge_list:
            self.dic[u].append(v)
            self.edge_map[(u,v)] = EdgeParameters(d)
    def get_edge_parameter(self,u,v)->EdgeParameters:
        return self.edge_map[(u,v)]
    def default_disfunc(self,edgeparameter):
        return edgeparameter.distance
    def get_children(self,node):
        return self.dic[node][::]
    def shortest(self,start,end,disfunc=None):
        '''
        Finds the shortest distance between start and end
        Usefull when finding shortest routes for the busses to take
        Implementation of Dijkstra
        '''
        if(disfunc is None):
            disfunc =self.default_disfunc
        current = (0,start,None) #start node has zero cost (cost,node_index)
        #so that automatic sorting works
        visited = set()
        pq = PriorityQueue()
        pq.put(current)
        pre_map = {}
        end_weight = None
        while(not pq.empty()):
            current = pq.get()
            if(current[1] in visited):
                continue
            
            current_w,current_node,pre = current
            pre_map[current_node] = pre

            if(current_node == end):
                end_weight = current_w
                break


            for child in self.dic[current_node]:
                if(child not in visited):
                    weight = disfunc(self.edge_map[current_node,child])
                    pq.put((current_w+weight,
                            child,current_node))
            visited.add(current_node)
        else:
            raise Exception(f"Desitnation is unrachable {start}->{end}")
        path = []
        node = end
        while(node !=None):
            path.append(node)
            node = pre_map[node] 
        return list(reversed(path)),end_weight


class Passenger:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.current = start
        self.path = []
        self.goal_reached = False
        self.limbo = False
    def calculate_path(self,graph:Graph,disfunc):
        self.path,_ = graph.shortest(self.start,self.end,disfunc)
    def move(self):
        if(len(self.path) < 2):
            raise Exception("Called move on already reached passenger")
        start = self.path.pop(0)
        end = self.path[0]
        if(len(self.path) == 1):
            self.goal_reached = True
        
        return (start,end)

    def path_to_go(self):
        if(len(self.path) < 2):
            logging.warning(f"The path is too small {self.path,self.end,self.start}")
            raise Exception("Passenger has no where to go!")
        return (self.path[0],self.path[1])


    def score(self):
        return 1
class Bus:
    def __init__(self,capacity,speed,node):
        self.capacity = capacity
        self.speed = speed
        self.passengers = []
        self.current = node
        self.destination = None
        self.distance_to_go = None
        self.total_distance = None
    def load_passengers_and_start(self,passengers:List[Passenger],current,destination,distance):
        self.passengers = passengers
        for pas in passengers:
            pas.limbo = True
        assert(current == self.current)
        self.destination = destination
        self.distance_to_go = distance
        self.total_distance = self.distance_to_go
        
    def arrive_and_unload_passengers(self):
        ret =  self.passengers[::]
        self.passengers.clear()
        self.current = self.destination
        self.distance_to_go = 0
        self.total_distance = self.distance_to_go
        for pas in ret:
            pas.limbo = False   
        return ret
    def update_bus_pos(self,delta)->bool:
        '''
        Updates the position of the bus according to the time passed and returns whether it has reached its destination or not
        '''
        if(self.distance_to_go is None):
            self.destination = self.current
            return True
        self.distance_to_go -= delta*self.speed
        if(self.distance_to_go <= 0):
            self.distance_to_go = 0
            return True
        return False
    def fractional_progress(self)->float:
        '''
        returns how much progress has been made by the bus on its journey as a floating point value between 0 and 1
        '''
        if(self.distance_to_go == 0):
            return 0
        return self.distance_to_go/self.total_distance

class EdgeGroups:
    def __init__(self):
        '''
        stores all the passengers who are awaiting to follow a certain edge
        also handles updating the path information of the passengers 
        '''
        self.dic:Dict[Tuple[Any,Any],List[Passenger]] = defaultdict(lambda:[])
        
    def get_passsengers(self,u,v)->List[Passenger]:
        '''
        returns the passengers waiting to go along a certain edge.
        Does not move them (does not call .move method) this must be done before they are passe into the bus
        '''
        
        ret = self.dic[(u,v)][::]
        self.dic[(u,v)].clear()
        return ret
    def load_passengers(self,passengers:List[Passenger]):
        for passenger in passengers:
            if(passenger.goal_reached):
                continue
            else:
                u,v = passenger.path_to_go()
                self.dic[u,v].append(passenger)
    def add_passenger(self,passenger:Passenger):
        u,v = passenger.path_to_go()
        self.dic[u,v].append(passenger)
        

    

    def calculate_passegner_score(self,u,v):
        return sum(p.score() for p in self.dic[(u,v)])

    def best_of(self,edge_list:List[Tuple[Any,Any]]):
        best_score = 0
        best_edge = None
        for u,v in edge_list:
            score = self.calculate_passegner_score(u,v)
            if(score > best_score):
                best_score = score
            best_edge = (u,v)
        return best_edge









class Test_pathfinder(unittest.TestCase):
    def setUp(self) -> None:
        
        example_graph = [
            ("S","A",7),
            ("S","B",2),
            ("A","B",3),
            ("S","C",3),
            ("C","L",2),
            ("L","J",4),
            ("L","I",4),
            ("I","J",6),
            ("J","K",4),
            ("I","K",4),
            ("K","E",5),
            ("A","D",4),
            ("B","D",4),
            ("B","H",1),
            ("D","F",5),
            ("H","F",3),
            ("H","G",2),
            ("G","E",2)

        ]
        reverse_graph = [(j,i,d) for(i,j,d) in example_graph]
        full_graph = example_graph+reverse_graph
        self.gg = Graph(full_graph)
    def test_path1(self):
        shortest,dis = self.gg.shortest("S","E")
        print(shortest)
        assert(shortest == ['S', 'B', 'H', 'G', 'E'])
        assert(dis == 7)
    def test_path_no_path(self):
        shortest,dis = self.gg.shortest("S","S")
        print(shortest)
        assert(shortest == ["S"])
        assert(dis == 0)

    def test_update_edge_parameter(self):
        self.gg.get_edge_parameter("S","A").weight = 4
        assert(self.gg.get_edge_parameter("S","A").weight == 4)

class Test_Bus(unittest.TestCase):
    def setUp(self) -> None:
        self.testbus = Bus(float('inf'),1,0)
    def test_load_and_update(self):
        p = Passenger(0,1)
        self.testbus.load_passengers_and_start([p],0,1,10)
        count = 0
        while (not self.testbus.update_bus_pos(1)):
            assert(p.limbo)
            print(self.testbus.fractional_progress())
            count +=1
        assert(count !=0)
        a = self.testbus.arrive_and_unload_passengers()
        assert(self.testbus.current == 1)
        assert(self.testbus.distance_to_go == 0)
        assert(not p.limbo)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)