# from terminal, type this command: ipython 
# within ipython, type following command: run motor_test.py

import pybullet as p
import pybullet_data as pd
import time
import creature


p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# add floor
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

# set gravity
p.setGravity(0, 0, -10)

c = creature.Creature(gene_count = 5)

with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

cid = p.loadURDF('test.urdf')

# assume creature sitting at origin
c.update_position([0,0,0])

# sets position to slightly above the ground to fix the flying problem
p.resetBasePositionAndOrientation(cid, [0,0,3], [0,0,0,1])

# needed for mac users to interact
while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]

        p.setJointMotorControl2(cid, jid, 
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=m.get_output(),
                                force = 5)

    pos, orn = p.getBasePositionAndOrientation(cid)
    c.update_position(pos)
    print(c.get_distance_travelled())

    p.stepSimulation()
    # time.sleep(0.1) # 10 times a second
    time.sleep(1.0/240) # pybullet is 240 frames per second