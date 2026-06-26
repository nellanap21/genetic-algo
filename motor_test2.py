# use this to load creature from urdf
# and test motor control parameters

import pybullet as p
import pybullet_data
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

# Load your creature
robot_id = p.loadURDF(
    "temp/test.urdf",
    basePosition=[0, 0, 1],
    useFixedBase=False
)

# Print joint information
num_joints = p.getNumJoints(robot_id)
print("Number of joints:", num_joints)

for j in range(num_joints):
    info = p.getJointInfo(robot_id, j)
    print("Joint", j, info[1].decode("utf-8"), "type:", info[2])

# Your URDF has one joint, so joint index 0
joint_id = 0

# Optional: increase friction
# p.changeDynamics(robot_id, -1, lateralFriction=2.0)
# for j in range(num_joints):
#     p.changeDynamics(robot_id, j, lateralFriction=2.0)

# Main simulation loop
t = 0

while True:
    # Sine-wave target joint angle
    target_angle = math.sin(t) * 3  # radians


    target_angle2 = np.sin(t) * 2
    print(target_angle, target_angle2)
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=target_angle2,
        force = 5,
        maxVelocity = 5)

    p.stepSimulation()
    time.sleep(1 / 240)

    t += 0.03