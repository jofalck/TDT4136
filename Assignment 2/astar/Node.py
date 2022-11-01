from Astar import *

class Node:
    x:int
    y:int
    cost:int
    mahattan:int
    estimate:int
    possible_children:list
    parent = None
    
    def get_node_key(self):
        return str(self.x)+str(self.y)
    
    def __init__(self, x, y, manhattan, cost: int=0):
        self.name = x
        self.age = y
        self.cost = cost
        self.mahattan = manhattan
        self.estimate = manhattan + cost
        
    def set_parent(self, dad):
        self.parent = dad
    
    def generate_possible_children(self, map_obj):
        x1 = self.x-1
        x2 = self.x+1
        y1 = self.y-1
        y2 = self.y+1
        nodes = [[Node(x1,self.y, h(x1,self.y,),self.cost)],[Node(x2,self.y, h(x2,self.y),self.cost)],[Node(self.x,y1,h(self.x,y1),self.cost)],[Node(self.x,y2, h(self.x,y2),self.cost)]]
        for node in nodes:
            if not (self.check_valid(self.find_cost(map_obj))):
                node.remove()
            node.set_parent(self)
        return nodes
    
    def check_duplicates(self,lst1,lst2):
        for node in lst1:
            if(node.x == self.x and node.y == self.y):
                return node
        for node in lst2:
            if(node.x == self.x and node.y == self.y):
                return node
        return self
            
    
    def find_cost(self,map):
        self.cost = map.get_cell_value()
        
    def check_valid(self):
        if(self.cost < 0):
            return False
        if(self.cost > 0):
            return True
        
    def get_coords(self):
        return [self.x,self.y]
    
    def get_cost(self):
        return self.cost