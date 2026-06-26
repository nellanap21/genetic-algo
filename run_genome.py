# from terminal, type this command: 
# > ipython
# > import pybullet as p
# > p.connect(p.GUI) 
# within ipython, type following command: run motor_test.py

import pybullet as p
import pybullet_data as pd
import time
import creature
import genome as genlib
import sys
import os
import environment as envt


def main(csv_file):
    assert os.path.exists(csv_file), "Tried to load " + csv_file + "but it does not exist"
    
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

    p.resetDebugVisualizerCamera(
        cameraDistance=10,
        cameraYaw=45,
        cameraPitch=-35,
        cameraTargetPosition=[0, 0, 2]
    )

    # add arena
    arena_size = 20
    envt.make_arena(arena_size=arena_size)

    # set gravity
    p.setGravity(0, 0, -10)

    c = creature.Creature(gene_count = 2)

    dna = genlib.Genome.from_csv(csv_file)
    c.set_dna(dna)

    # save it to XML
    with open('temp/test.urdf', 'w') as f:
        c.get_expanded_links()
        f.write(c.to_xml())
    # load it into the sim
    cid = p.loadURDF('temp/test.urdf')

    # assume creature sitting at origin
    c.update_position([0,0,0])

    # sets position to slightly above the ground to fix the flying problem
    p.resetBasePositionAndOrientation(cid, [0, -6, 1], [0,0,0,2])

    # needed for mac users to interact
    while True:
        for jid in range(p.getNumJoints(cid)):
            m = c.get_motors()[jid]

            # position control
            print(m.get_output())
            p.setJointMotorControl2(cid, 
                                    jid,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPosition=m.get_output(),
                                    force = 5,
                                    maxVelocity = 5)

        pos, orn = p.getBasePositionAndOrientation(cid)
        c.update_position(pos)

        # automatically sets the camera to follow the creature
        #p.resetDebugVisualizerCamera(5, 0, 200, pos)

        p.stepSimulation()
        # time.sleep(0.1) # 10 times a second
        time.sleep(1.0/240) # pybullet is 240 frames per second
    

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python run_genome.py csv_filename"
    main(sys.argv[1])