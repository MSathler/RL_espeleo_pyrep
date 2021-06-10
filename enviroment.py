from pyrep import PyRep
from pyrep.robots.mobiles.p3dx import P3dx
from pyrep.robots.mobiles.espeleo import Espeleo
from pyrep.robots.robot_component import RobotComponent
from pyrep.objects.shape import Shape
from pyrep.backend import sim
from pyrep.objects.object import Object
from pyrep.const import PrimitiveShape
import numpy as np
from pyrep.backend import sim
from lib.py_sensor import sensor
import time
import math
import random
from collections import namedtuple, deque


class ReacherEnv(object):

    def __init__(self,SCENE_FILE, fixed_position = False, use_graphic = True):
        """Initialize an Enviroment object.
        
        Params
        ======
	    SCENE_FILE (string): Coppelia scene file
            fixed_position (bool): initial position of robot
            use_graphic (bool): use CoppeliaSim graphical interface

        """
        self.
        self.first_time = True
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless= use_graphic)
        self.pr.start()

        #self.agent = P3dx()
        self.agent = Espeleo()
        self.sensor = sensor() 
        self.memory_len = 5
        
        self.Gas_handle = sim.simGetObjectHandle('Gas')
        self.World_handle = sim.simGetObjectHandle('World_link')
        #print(sim.simGetObjectPosition(self.Gas_handle,self.World_handle))
        self.save_reads = []
        self.fixed_position = fixed_position
        self.done = False
        self._reward = 0
        self.last_read = 0
        self.gradient = 0
        self.zeros = 0
        self.read = 0.0
        self.wind_angle = 0.0
        self.h = 0
        self.n = 0
        self.x,self.y = 0.0,0.0
        self.m_read = 0.0
        self.concentration_memory = deque(maxlen=self.memory_len)
        self.wind_angle_memory = deque(maxlen=self.memory_len)
        self.distance_memory = deque(maxlen=self.memory_len)
        self.angle_memory = deque(maxlen=self.memory_len)
        self.initiate_Vmemory()
        self.starting_pose = self.agent.get_2d_pose()
        self.s_x, self.s_y, self.s_z = self.starting_pose
        self.sensor_pos_x, self.sensor_pos_y, self.sensor_pos_z = sim.simGetObjectPosition(self.Gas_handle,self.World_handle)
        self.last_x,self.last_y = self.s_x, self.s_y
        self.agent.set_motor_locked_at_zero_velocity(True)
        self.sensor.update(self.sensor_pos_x, self.sensor_pos_y)
        
        
    def _get_state(self):

        ############### Relative Position ####################

        x, y, yaw = self.agent.get_2d_pose()
        distance_n = ( ( ( (x - self.last_x) ** 2 ) + ( (y - self.last_y) ** 2 ) ) ** (1/2) ) / 2
        angle = (yaw + math.pi) / (2 * math.pi)   
        self.last_x = x
        self.last_y = y

        ############### Relative Position end ################

        self.save_reads.append(self.read)
        norm_read = self.read / 400.0 

        #self.wind_angle_memory.append(self.sensor.wind)
        self.concentration_memory.append( norm_read )
        self.distance_memory.append( distance_n )
        self.angle_memory.append( angle )

        return np.concatenate( [ self.concentration_memory, self.distance_memory, self.angle_memory, np.array( [self.gradient] ) ] ) #( self.sensor.read / 10000 ),


    def save_to_plot(self):

        with open("valores.txt",'a') as f:
            f.writelines('\n------\n')
            f.writelines(str(self.save_reads))
            f.close()   

        self.save_reads = []


    def actions(self,action):

        if action == 0:
            return [2.0,2.0]
        elif action == 1:
            return [3.0,1.0]
        elif action == 2:
            return [1.0,3.0,]
        elif action == 3:
            return [2.0,-2.0]
        elif action == 4:
            return [-2.0,2.0]


    def step(self, action):
        
        wheel_action = self.actions(action)
        self.agent.set_joint_target_velocities(wheel_action)  # Execute action
        t = time.clock_gettime(time.CLOCK_MONOTONIC)

        for i in range(20):
            self.pr.step()  # Step the physics simulation
            time.sleep(0.01)

        #print("tempo gasto na iteracao : " + str(time.clock_gettime(time.CLOCK_MONOTONIC) - t))
        self.last_read = self.read
        self.x,self.y,z = self.agent.get_2d_pose()
        self.sensor_pos_x, self.sensor_pos_y, self.sensor_pos_z = sim.simGetObjectPosition(self.Gas_handle,self.World_handle)
        self.sensor.update(self.sensor_pos_x,self.sensor_pos_y)
        self.read = self.sensor.read

        #self.wind_angle = self.sensor.wind
        #print(self.read)

        self.gradient = 1 if (self.read - self.last_read) > 0 else 0
        self.reward()

        return self.done, self._reward, self._get_state()
    

    def reward(self):

        self._reward = -1

        if self.read > 0:
            self._reward += 1
            self.zeros = 0

        else: 
            self.zeros += 1

            if self.zeros >= 10:
                self._reward -= 100
                self.done = True

        if self.gradient > 0:
            self.h += 1 
            self.n = 0
            self._reward += self.h
        else:
            self.h = 0
            self.n += 1
            self._reward -= self.n
           

        if self.read > 350:    
            self._reward += 1000
            self.done = True


    def initiate_Vmemory(self):

        self.wind_angle_memory = deque(maxlen=self.memory_len)
        self.concentration_memory = deque(maxlen=self.memory_len)
        self.distance_memory = deque(maxlen=self.memory_len)
        self.angle_memory = deque(maxlen=self.memory_len)

        for _ in range(4):
            self.wind_angle_memory.append(0.0)
            self.concentration_memory.append(0.0)
            self.distance_memory.append(0)
            self.angle_memory.append(0)


    def x_y_start(self):

        source_size = 0.8
        self.x_start, self.y_start = random.uniform(-2.525,6.4),random.uniform(-2.2,6.4)
        self.sensor_pos_x, self.sensor_pos_y, self.sensor_pos_z = sim.simGetObjectPosition(self.Gas_handle,self.World_handle)
        self.sensor.update(self.sensor_pos_x,self.sensor_pos_y)
        self.read = self.sensor.read

        while (self.x_start < 1.675 + source_size and self.x_start > 1.675 - source_size and self.y_start < 2.35 + source_size and self.y_start > 2.35 - source_size and self.read != 0):
            
            self.x_start, self.y_start = random.uniform(-2.525,6.4),random.uniform(-2.2,6.4)
            self.sensor_pos_x, self.sensor_pos_y, self.sensor_pos_z = sim.simGetObjectPosition(self.Gas_handle,self.World_handle)
            self.sensor.update(self.sensor_pos_x,self.sensor_pos_y)
            self.read = self.sensor.read
            

    def reset(self):
        
        if self.fixed_position == False: # Random initial position
            self.x_y_start()
            self.agent.set_2d_pose([self.x_start, self.y_start,0.0])
            self.x,self.y = self.x_start, self.y_start
        else:
            self.agent.set_2d_pose(self.starting_pose) # Fixed initial position

        self._reward = -1
        self.last_read = 0
        self.gradient = 0
        self.h = 0
        self.n = 0
        self.read = 0.0
        self.wind_angle = 0.0
        self.zeros = 0
        self.initiate_Vmemory()
        self.done = False
        self.last_x,self.last_y = self.s_x, self.s_y

        return self._get_state()


    def shutdown(self):

        # self.sensor.shutdown()
        self.pr.stop()
        self.pr.shutdown()
