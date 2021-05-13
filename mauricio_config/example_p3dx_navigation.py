"""
A turtlebot reaches for 4 randomly places targets.
This script contains examples of:
    - Non-linear mobile paths to reach a target with collision avoidance
"""
from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.mobiles.p3dx import P3dx
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
import numpy as np
from pyrep.backend import sim
import time
from py_sensor import sensor

# class ReacherEnv(object):

#     def __init__(self,SCENE_FILE):
#         self.pr = PyRep()
#         self.pr.launch(SCENE_FILE, headless=False)
#         self.pr.start()
#         self.agent = P3dx()
#         # self.agent.set_control_loop_enabled(False)
#         self.agent.set_motor_locked_at_zero_velocity(True)
#         self.target = Shape('target')
#         self.agent_ee_tip = self.agent.get_tip()
#         self.initial_joint_positions = self.agent.get_joint_positions()

#     def _get_state(self):
#         # Return state containing arm joint angles/velocities & target position
#         return np.concatenate([self.agent.get_joint_positions(),
#                                self.agent.get_joint_velocities(),
#                                self.target.get_position()])

#     def reset(self):
#         # Get a random position within a cuboid and set the target position
#         pos = list(np.random.uniform(POS_MIN, POS_MAX))
#         self.target.set_position(pos)
#         self.agent.set_joint_positions(self.initial_joint_positions)
#         return self._get_state()

#     def step(self, action):
#         self.agent.set_joint_target_velocities(action)  # Execute action on arm
#         self.pr.step()  # Step the physics simulation
#         ax, ay, az = self.agent_ee_tip.get_position()
#         tx, ty, tz = self.target.get_position()
#         # Reward is negative distance to target
#         reward = -np.sqrt((ax - tx) ** 2 + (ay - ty) ** 2 + (az - tz) ** 2)
#         return reward, self._get_state()

#     def shutdown(self):
#         self.pr.stop()
#         self.pr.shutdown()
    

LOOPS = 4
SCENE_FILE = join(dirname(abspath(__file__)), 'p3dx_scene.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()
agent = P3dx()
sensor = sensor()

# We could have made this target in the scene, but lets create one dynamically
target = Shape.create(type=PrimitiveShape.SPHERE,
                      size=[0.05, 0.05, 0.05],
                      color=[1.0, 0.1, 0.1],
                      static=True, respondable=False)

position_min, position_max = [-0.5, 1, 0.1], [0.5, 1.5, 0.1]
#sim.simSetFloatSignal("sensor_Signal",100.0)
#print(sim.simGetFloatSignal("sensor_Signal"))
starting_pose = agent.get_2d_pose()

agent.set_motor_locked_at_zero_velocity(True)

for i in range(LOOPS):
    agent.set_2d_pose(starting_pose)

    # Get a random position within a cuboid and set the target position
    pos = list(np.random.uniform(position_min, position_max))
    target.set_position(pos)

    path = agent.get_nonlinear_path(position=pos, angle=0)

    path.visualize()
    done = False
    #print(sim.simGetFloatSignal("D"))
    t = time.clock_gettime(time.CLOCK_MONOTONIC)
    sensor.update()
    while not done:
        if (time.clock_gettime(time.CLOCK_MONOTONIC) - t) >= 0.45:
            sensor.update()
        #time.sleep(0.6)
            print(sensor.read)
            t = time.clock_gettime(time.CLOCK_MONOTONIC)
        done = path.step()
        pr.step()

    path.clear_visualization()

    print('Reached target %d!' % i)

sensor.shutdown()
pr.stop()
pr.shutdown()
