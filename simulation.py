import pybullet as p


class Simulation():
    def __init__(self):
        self.physicsClientId = p.connect(p.DIRECT)

    # because it's stateful, it needs access to the simulation, so we need self
    # pybullet runs 240 times a second, so 2400 iterations -> 10 seconds
    def run_creature(self, cr, iterations=2400):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId=pid)
        p.setGravity(0, 0, -10, physicsClientId=pid)
        # set to false, so it won't reuse same file
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid) 

        # add floor
        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
        floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)

        xml_file = 'temp.urdf'
        xml_str = cr.to_xml()
        with open(xml_file, 'w') as f:
            f.write(xml_str)
        
        cid = p.loadURDF(xml_file, physicsClientId=pid)

        # sets position to slightly above the ground to fix the flying problem
        p.resetBasePositionAndOrientation(cid, [0,0,3], [0,0,0,1], physicsClientId=pid)

        for step in range(iterations):
            p.stepSimulation(physicsClientId=pid)
            if step % 24 == 0:
                self.update_motors(cid=cid, cr=cr)
            
            # get position and pass to creature
            pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
            cr.update_position(pos)



    def update_motors(self, cid, cr):
        """
        cid is teh id in physics engine
        cr is a creature object
        """
        for jid in range(p.getNumJoints(cid, 
                                        physicsClientId=self.physicsClientId)):
            # get the motors of the creature
            m = cr.get_motors()[jid]
            # set joint velocity to the output of motor
            p.setJointMotorControl2(cid, jid,
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocity=m.get_output(),
                                    force = 5,
                                    physicsClientId=self.physicsClientId)






