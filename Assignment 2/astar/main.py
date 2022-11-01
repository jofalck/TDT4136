from Map import Map_Obj
from Astar import *

# cost:int = 0
# def h(n): 
#     """heuristic search function
#     returns an optimistic estimate of the remaining distance
#     """
#     return (get_goal_pos[0]-get_cell_value(n)[0]) + (get_goal_pos[1]-get_cell_value(n)[1])

# def g(n):
#     """Returns the cost of the currentCell
#     n is the current cell"""
#     cost += get_cell_value(n)
#     return cost

map_obj = Map_Obj(task=1)
astar(map_obj) 
map_obj.show_map()

