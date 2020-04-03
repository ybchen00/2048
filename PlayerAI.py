"""
author@Yibing Chen(yc3578)
"""
import random
from BaseAI_3 import BaseAI
import sys
import time

class PlayerAI(BaseAI):
    weights = [1, 150]
    def getMove(self, grid):
        return self.action(grid)
    
    def action(self, grid):)
        initial_time = time.process_time()
        maxTuple = self.maximize(grid, 0, -sys.maxsize, sys.maxsize, initial_time)
        return maxTuple[0]
    
    
    def minimize(self, grid, depth, a, b, time_now): 
        availableCells = grid.getAvailableCells() #list of (x,y) of available cells
        availableMoves = grid.getAvailableMoves() #list of (int, Grid) of available moves
        
        if len(availableMoves) == 0 or len(availableCells) == 0 or time.process_time()-time_now >= 0.16 or depth >=4:
            return(None, self.utility(grid))
            
        minTuple = (None, sys.maxsize)
        
        for cell in availableCells:
            newGrid_2 = grid.clone() #Inserting a 2-tile
            newGrid_2.insertTile(cell, 2)
            tuple_2 = self.maximize(newGrid_2, depth +1, a, b, time_now) 
            util_2 = tuple_2[1]*0.9
            
            newGrid_4 = grid.clone() #Inserting a 4-tile
            newGrid_4.insertTile(cell, 4)
            tuple_4 = self.maximize(newGrid_4, depth +1, a, b, time_now)
            util_4 = tuple_4[1]*0.1
            
            # final util = the average utility of tile 2 and tile 4
            util = (util_2+util_4)/2
            if util < minTuple[1]:
                minTuple = (None, util)
                
            # alpha-beta pruning
            if minTuple[1] <= a:
                #print("BREAK MIN()")
                break
            
            if minTuple[1] < b:
                b = minTuple[1]
        #print("minTuple = " + str(minTuple))
        #(action: utility)
        return minTuple
            
                
    def maximize(self, grid, depth, a, b, time_now):
        # Maximize according to predicted Computer's minimizing move
        # Returns tuple (int action, int utility)
        availableMoves = grid.getAvailableMoves() #list of (int, Grid) of available moves
        if len(availableMoves) == 0 or time.process_time()-time_now >= 0.16 or depth >=4:
            return(None, self.utility(grid))
            
        maxTuple = (None, -sys.maxsize)
        
        for action in availableMoves:
            minTuple = self.minimize(action[1], depth+1, a, b, time_now) 
            if minTuple[1] > maxTuple[1]:
                maxTuple = (action[0], minTuple[1])
        
            if maxTuple[1] >= b:
                #print("BREAK MAX()")
                break
            
            if maxTuple[1] > a:
                a = maxTuple[1]
                
        #print("maxTuple = " + str(maxTuple))
        #(action: utility)
        return maxTuple
    
          
    def utility(self, grid):
        """
        Heuristics: 1. gradient: awarding s-shaped configuration of board, where the max-valued tiles are at the corners
                    2. diff: punish if huge differences in neighboring tiles. The larger the difference between neighboring tiles, the larger the punishment
                    3. availableCells in the grid: award when more empty tiles are in the grid. To encourage merging tiles when possible
                    4. availableMoves in the grid: award when having more options to move tiles. To decrease the possibility of running into a deadlock and being forced to take unfavorable moves
        """
        # Four configurations of the grid where the most valued tiles are at different corners
        gradient_grid_1 = [ [4**0, 4**1, 4**2, 4**3],
                            [4**1, 4**2, 4**3, 4**4],
                            [4**2, 4**3, 4**4, 4**5],
                            [4**3, 4**4, 4**5, 4**6]
                          ]
        gradient_grid_2 = [ [4**3, 4**2, 4**1, 4**0],
                            [4**4, 4**3, 4**2, 4**1],
                            [4**5, 4**4, 4**3, 4**2],
                            [4**6, 4**5, 4**4, 4**3]                
                          ]
        gradient_grid_3 = [ [4**6, 4**5, 4**4, 4**3],
                            [4**5, 4**4, 4**3, 4**2],
                            [4**4, 4**3, 4**2, 4**1],
                            [4**3, 4**2, 4**1, 4**0]
                          ]
        gradient_grid_4 = [ [4**3, 4**4, 4**5, 4**6],
                            [4**2, 4**3, 4**4, 4**5],
                            [4**1, 4**2, 4**3, 4**4],
                            [4**0, 4**1, 4**2, 4**3]
                          ]
        gradient_1 = 0
        gradient_2 = 0
        gradient_3 = 0
        gradient_4 = 0
        diff = 0

        for x in range(4):
            
            for y in range(4):
                grid_val = grid.map[x][y]
                gradient_1 += gradient_grid_1[x][y]*grid_val
                gradient_2 += gradient_grid_2[x][y]*grid_val
                gradient_3 += gradient_grid_3[x][y]*grid_val
                gradient_4 += gradient_grid_4[x][y]*grid_val
                
                diff_x = 0
                diff_y = 0
                if y < 3:
                    diff_y += abs(grid.map[x][y] - grid.map[x][y+1])
                    #print("y differences = " + str(diff))
                if x < 3:
                    diff_x += abs(grid.map[x][y] - grid.map[x+1][y])
                
                diff += min(diff_y, diff_x)
                
                
        # Choose the best grid options among four configurations
        max_gradient = max(gradient_1, gradient_2, gradient_3, gradient_4)

        maxTile = grid.getMaxTile()
        
        
            
        # diff*maxTile*100:  scale the diff punishment as game progresses to larger-valued tiles
        return max_gradient*len(grid.getAvailableCells())*(len(grid.getAvailableMoves()))-diff*maxTile*100
        #return max_gradient
