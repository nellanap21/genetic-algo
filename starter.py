# from terminal, type this command: ipython 
# within ipython, type following command: run starter.py

import pybullet as p
import time
import pybullet_data as pd

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# add floor
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

# add robot
rob1 = p.loadURDF("test.urdf")

p.setGravity(0, 0, -10)

# needed for mac users to interact
while True:
    p.stepSimulation()
    time.sleep(1.0/240)