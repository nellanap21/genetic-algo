import pybullet as p
from multiprocessing import Pool
import environment as envt

class Simulation():
    def __init__(self, sim_id=0):
        # p.DIRECT means it runs in offline mode
        self.physicsClientId = p.connect(p.DIRECT) 
        self.sim_id = sim_id

    # because it's stateful, it needs access to the simulation, so we need self
    # pybullet runs 240 times a second, so 2400 iterations -> 10 seconds
    def run_creature(self, cr, iterations=2400):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId=pid)
        p.setGravity(0, 0, -10, physicsClientId=pid)
        # set to false, so it won't reuse same file
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid) 

        # add arena
        arena_size = 20
        envt.make_arena(arena_size=arena_size)

        #xml_file = 'temp' + str(self.sim_id) + '.urdf'
        xml_file = f"temp/temp{self.sim_id}.urdf"
        xml_str = cr.to_xml()
        with open(xml_file, 'w') as f:
            f.write(xml_str)
        
        # call loadURDF to load the file into simulation
        cid = p.loadURDF(xml_file, physicsClientId=pid)

        # sets position to slightly above the ground to fix the flying problem
        # start at side to have consistent starting position
        p.resetBasePositionAndOrientation(cid, [0,-8,1], [0,0,0,2], physicsClientId=pid)

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


class ThreadedSim():
    def __init__(self, pool_size):
        self.pool_size = pool_size

    @staticmethod
    def static_run_creature(sim_id, cr, iterations):
        # cannot pass a connected PyBullet simulation into a worker.
        # creates the simulation inside the worker process
        sim = Simulation(sim_id)
        sim.run_creature(cr, iterations)
        p.disconnect(sim.physicsClientId)
        return cr

    def eval_population(self, pop, iterations):
        """
        pop is a Population object
        iterations is frames in pybullet to run for at 240fps
        """
        pool_args = []

        for i in range(len(pop.creatures)):
            sim_id = i % self.pool_size
            # print("eval_pop: c ind", i, "sim_ind", sim_id)

            pool_args.append([
                sim_id,
                pop.creatures[i],
                iterations
            ])

        with Pool(self.pool_size) as pool:
            new_creatures = pool.starmap(
                ThreadedSim.static_run_creature,
                pool_args
            )

        # for cr in new_creatures:
        #     print(cr.get_distance_to_peak())

        pop.creatures = new_creatures










