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

# Optional: increase friction
# p.changeDynamics(robot_id, -1, lateralFriction=2.0)
# for j in range(num_joints):
#     p.changeDynamics(robot_id, j, lateralFriction=2.0)

# Main simulation loop
t = 0

num_legs = 20
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


"""
This is the URDF of the creature I want to test. Works with this current motor

<robot name="climber">
	<link name="0">
		<visual>
			<geometry>
				<cylinder length="1" radius="0.25"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="1" radius="0.25"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.018615131243520218"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>
	</link>
	<link name="11">
		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>
	</link>
	<link name="12">
		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>
	</link>
	<link name="13">
		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>
	</link>
	<link name="14">
		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>
	</link>
	<link name="15">

		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>

	</link>

	<link name="16">

		<visual>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</visual>
		<collision>
			<geometry>
				<cylinder length="0.5" radius="0.05"/>
			</geometry>
			<origin xyz="0 0 0.5"/>
		</collision>
		<inertial>
			<mass value="0.08478927124562911"/>
			<inertia ixx="0.03" iyy="0.03" izz="0.03" ixy="0" ixz="0" iyz="0"/>
		</inertial>

	</link>	
	<joint name="11_to_0" type="revolute">
		<parent link="0"/>
		<child link="11"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 1.5 0" xyz="0 0 0"/>
	</joint>
	<joint name="12_to_0" type="revolute">
		<parent link="0"/>
		<child link="12"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 -1.5 0" xyz="0 0 0"/>
	</joint>
	<joint name="13_to_0" type="revolute">
		<parent link="0"/>
		<child link="13"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 1.5 0" xyz="0 0 1"/>
	</joint>
	<joint name="14_to_0" type="revolute">
		<parent link="0"/>
		<child link="14"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 -1.5 0" xyz="0 0 1"/>
	</joint>
	<joint name="15_to_0" type="revolute">
		<parent link="0"/>
		<child link="15"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 1.5 0" xyz="0 0 0.5"/>
	</joint>

	<joint name="16_to_0" type="revolute">
		<parent link="0"/>
		<child link="16"/>
		<axis xyz="1 0 0"/>
		<limit upper="0.6" lower="-0.6"/>
		<origin rpy="0 -1.5 0" xyz="0 0 0.5"/>
	</joint>
</robot>


"""