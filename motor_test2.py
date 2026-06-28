"""
Pupose: this script is used to help test the motor skills
of a creature. This creature is loaded from a URDF file
"""

import pybullet as p
import time
import math
import numpy as np

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# add floor
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

# Basic world setup
p.setGravity(0, 0, -10)
start_orientation = p.getQuaternionFromEuler([0, math.pi / 2, 0])

# Load your creature
robot_id = p.loadURDF(
    "temp/test.urdf",
    basePosition=[0, 0, 2],
    baseOrientation=start_orientation,
    useFixedBase=False
)

# Print joint information
num_joints = p.getNumJoints(robot_id)
print("Number of joints:", num_joints)

for j in range(num_joints):
    info = p.getJointInfo(robot_id, j)
    print("Joint", j, info[1].decode("utf-8"), "type:", info[2])

# Main simulation loop
t = 0

num_legs = 8
num_pairs = num_legs // 2
phases = []

for pair in range(num_pairs):
    phase = pair * np.pi / 2      # 0, π/2, π
    phases.extend([phase, phase]) # left/right pair use same phase

while True:
    for jid in range(num_joints):
        target_angle = np.sin(t + phases[jid])
        p.setJointMotorControl2(
            bodyUniqueId=robot_id,
            jointIndex=jid,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_angle,
            force=40,
            maxVelocity=3

        )  

    p.stepSimulation()
    time.sleep(1 / 240)

    t += 0.03

