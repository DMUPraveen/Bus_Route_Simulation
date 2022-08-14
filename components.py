from collections import defaultdict
from queue import PriorityQueue
from turtle import Turtle 
import unittest
class Bus:
    def __init__(self,capacity,speed):
        self.capacity = capacity
        self.speed = speed
        self.passengers = []


class Passenger:
    def __init__(self,start,end):
        self.start = start
        self.end = end

class Graph:
    def __init__(self,edge_list):
        #edge list needs to be given in the (u,v,d) format where u->v road has distance(or time cost) of d
        self.dic = defaultdict(lambda:[]) 
        self.edge_map = {} #stores information about edges  
        for u,v,d in edge_list:
            self.dic[u].append(v)
            self.edge_map[(u,v)] = d#for now it is only the distance
    def get_weight(self,u,v):
        return self.edge_map[(u,v)] 
    def shortest(self,start,end):
        current = (0,start,None) #start node has zero cost (cost,node_index)
        #so that automatic sorting works
        visited = set()
        pq = PriorityQueue()
        pq.put(current)
        pre_map = {}
        while(True):
            current = pq.get()
            if(current[1] in visited):
                continue
            
            current_w,current_node,pre = current
            pre_map[current_node] = pre

            if(current_node == end):
                break


            for child in self.dic[current_node]:
                if(child not in visited):
                    pq.put((current_w+self.get_weight(current_node,child),
                            child,current_node))
            visited.add(current_node)

        path = []
        node = end
        while(node !=None):
            path.append(node)
            node = pre_map[node] 
        return path



class Test_pathfinder(unittest.TestCase):
    def  test_on_example_graph(self):
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
        gg = Graph(full_graph)
        shortest = gg.shortest("S","E")
        print(shortest)
        assert(shortest == ['E', 'G', 'H', 'B', 'S'])



if __name__ == "__main__":
    unittest.main(verbosity=2)