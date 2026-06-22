import pybullet as p
from multiprocessing import Pool

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

        # add floor
        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
        floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)

        xml_file = 'temp' + str(self.sim_id) + '.urdf'
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
        pool_args = []

        for i in range(len(pop.creatures)):
            sim_id = i % self.pool_size
            print("eval_pop: c ind", i, "sim_ind", sim_id)

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

        for cr in new_creatures:
            print(cr.get_distance_travelled())

        pop.creatures = new_creatures

# code from video that does not work
# class ThreadedSim():
#     def __init__(self, pool_size):
#         self.sims = [Simulation(i) for i in range(pool_size)]

#     # no state, doesn't need to access self
#     @staticmethod
#     def static_run_creature(sim, cr, iterations):
#         sim.run_creature(cr, iterations)
#         # in threaded mode, in multiprocessor mode, 
#         # it's going to create a copy of the creature, 
#         # so it passes by value rather than by reference. 
#         # so need to return creature
#         return cr 

#     def eval_population(self, pop, iterations):
#         pool_args = [] # mega array
#         start_ind = 0
#         pool_size = len(self.sims)
#         # outer loop creates whole array
#         while start_ind < len(pop.creatures): 
#             this_pool_args = []
#             # inner loop creates iteration
#             for i in range(start_ind, start_ind + pool_size):
#                 if i == len(pop.creatures): # the end
#                     break
#                 # work out the sim ind
#                 sim_ind = i % len(self.sims)
#                 print("eval_pop: c ind", start_ind, "sim_ind", sim_ind)

#                 this_pool_args.append([
#                     self.sims[sim_ind],
#                     pop.creatures[i],
#                     iterations]
#                 )
#             pool_args.append(this_pool_args)
#             start_ind = start_ind + pool_size


#         new_creatures = []
#         for pool_argset in pool_args:
#             # pool from python api that runs process in 
#             with Pool(pool_size) as p:
#                 # it works on a copy of the creatures, so receive
#                 creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
#                 # and now put those creatures back into the main
#                 # self.creatures array
#                 new_creatures.extend(creatures)
#         # for interest, print
#         for cr in new_creatures:
#             print(cr.get_distance_travelled())
#         pop.creatures = new_creatures










