import numpy as np
import time
from mpmath import rand
import random
from encodings.rot_13 import rot13
import math
from pygame.transform import rotate
from collections import deque

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        
        
        self.possible_ways = []
        self.dict_ways = {0:-90, 1: 0, 2: 90}
        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.state = ()
        self.Q = {}
        self.alpha = 0.1
        self.gamma = 1.0
        self.i = 0
        self.action = 0
        self.min_rotations = []
        self.track_history = set()
        self.dict_heading = {'up': (0, -1), 'down' : (0, 1), 'left' : (-1, 0), 'right' : (1, 0),
                             'u': (0, -1), 'd' : (0, 1), 'l' : (-1, 0), 'r' : (1, 0)}
        self.finish = (self.maze_dim/2, self.maze_dim/2)
            
    def next_move(self, sensors, location, heading):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''

        movement = 1
        rotation = 0
        # Updating state
        possible_rotations = []
        self.location = (location[0], location[1])
        center = (self.maze_dim/2, self.maze_dim/2)
        
        # Defining possible ways to go
        for next_action in sensors:
            if next_action > 0:
                possible_rotations.append(self.dict_ways
                                          [sensors.index(next_action)])
        my_arr = []
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                self.Q[(x, y)] = (abs(center[0] - x) + abs(center[1] - y))
                my_arr.append((abs(center[0] - x) + abs(center[1] - y)) )
        self.track_history.add(self.location)
        print self.track_history
        for next_action in possible_rotations:
            min_action = -1
            if self.Q[self.location] > self.Q[self.get_valid_neighbour(next_action, heading)]:
                rotation = next_action
                #print self.Q[self.location], ' > ', self.Q[self.get_valid_neighbour(next_action, heading)]
            else:
                for previous_actions in self.track_history:
                    self.Q[previous_actions] += 1
                    rotation = next_action
                    print self.Q[previous_actions]
        if self.location == center:
            return ('Reset', 'Reset')
        #print self.Q[self.get_valid_neighbour(rotation, heading)]
        new_arr = np.array(my_arr).reshape(12, 12)
        #print new_arr
        time.sleep(0)
        #print self.track_history
            
        # print self.location
        return rotation, movement
    
    def get_valid_neighbour(self, rotation, heading):
        if heading == 'u' or heading == 'up':
            if rotation == 90:
                return (self.location[0] + 1, self.location[1])
            elif rotation == -90:
                return (self.location[0] - 1, self.location[1])
            else:
                return (self.location[0], self.location[1] + 1)
        elif heading == 'l' or heading == 'left':
            if rotation == 90:
                return (self.location[0], self.location[1] + 1)
            elif rotation == -90:
                return (self.location[0], self.location[1] - 1)
            else:
                return (self.location[0] - 1, self.location[1])
        elif heading == 'r' or heading == 'right':
            if rotation == 90:
                return (self.location[0], self.location[1] - 1)
            elif rotation == -90:
                return (self.location[0], self.location[1] + 1)
            else:
                return (self.location[0] + 1, self.location[1])
        else:
            if rotation == 90:
                return (self.location[0] + 1, self.location[1])
            elif rotation == -90:
                return (self.location[0] - 1, self.location[1])
            else:
                return (self.location[0], self.location[1] - 1)
