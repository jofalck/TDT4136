from ast import Continue
from distutils.log import info
from queue import PriorityQueue
from typing import Optional
from Map import Map_Obj
from Node import Node
import logging


"""
A-Star algoritm class
https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar
"""    

def astar(map_obj):
    open = list[Node]
    closed : list[Node]
    visited: list[Node]
    cost_so_far : dict[Node, int]
    n0 = Node(map_obj.get_start_pos()[0],map_obj.get_start_pos()[1])
    GOAL = map_obj.get_goal_pos()
    g = 0
    open.add(n0,g) #hvilken rekkefølge på n0 og g?
    while (open.size() != 0):
        x = open.get()
        closed.append(x)
        if(x.get_coords() == map_obj.get_goal_pos):
            logging.info("Goal position reached")
            print("SUCCESS")
            return x.get_coords(), closed
        children = x.get_possible_children(map_obj)
            #children skal nå kun ha frontier-nodes den kan gå til
        
        for child in children:  
            if (child.get_coords)          
            if not (child in open or child in closed):
                attach_and_eval(child, x, map_obj)
                open.append(child)
                
    logging.log("Open list is empty")
    return None
    
    
def h(c,g):
    return abs(c.x-g.x)+abs(c.y-g.y)

def attach_and_eval(child,parent,map_obj):
    new_cost = parent.cost + map_obj.get_cell_value(list[child.x,child.y])
    if (new_cost<child.cost):
        child.set_parent(parent)
        child.set_cost(new_cost)

#map_obj = Map_Obj(task=1)
# def astar(self):
#     init = get_start_pos()
#     goal = get_goal_pos()
#     reached = list[list[int,int]]
#     reached.append(init)
#     while (init != goal):
#         pass
