#PARTICLE SWARM OPTIMIZATION FOR 1 SATELLITE - V1
#UPDATED VERSION SAVED IN DIFFERENT FILES
from __future__ import division
import random
import math
import matplotlib.pyplot as plt
import numpy as np

#---COST FUNCTION---
# function we are attempting to optimize (minimize)
def func1(x):
    total = 0
    for i in range(len(x)):
        total+=x[i]**2
    return total

#---MAIN---
class Particle:
    def __init__(self, x0):
        self.position_i = []    #particle position
        self.velocity_i = []    #particle velocity
        self.pos_best_i = []    #best position individual
        self.err_best_i = -1    #best error individual
        self.err_i = -1         #error individual

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(x0[i])

    # eval current fitness
    def evaluate(self, costfunc):
        self.err_i = costfunc(self.position_i)

        # check if current position is better than individual best position
        if self.err_i < self.err_best_i or self.err_best_i == -1:
            self.pos_best_i = self.position_i
            self.err_best_i = self.err_i

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        w = 0.5 # constant intertia weight, or how much to weigh the previous velocity
        c1 = 1  # cognative constant
        c2 = 2  # social constant

        for i in range(0,num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=w * self.velocity_i[i] + vel_cognitive + vel_social
    
    # update particle positions based on new velocity
    def update_position(self, bounds):
        for i in range(0, num_dimensions):
           self.position_i[i] = self.position_i[i] + self.velocity_i[i]

        #adjust maximum position as needed 
        if self.position_i[i] > bounds[i][1]:
            self.position_i[i] = bounds[i][1]

        # adjust minimum position as needed
        if self.position_i[i] < bounds[i][0]:
            self.position_i[i] = bounds[i][0]

class PSO():
    def __init__(self,costfunc, x0, bounds, num_particles, maxiter):
        global num_dimensions

        num_dimensions = len(x0)
        err_best_g = -1
        pos_best_g = []

        #establish the swarm here
        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        i = 0
        while i <maxiter:
            #print i,err_best_g
            # cycle through particles in swarm and evaluate fitness

            for j in range(0, num_particles):
                swarm[j].evaluate(costfunc)

                #determine if particle is global best
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i+=1
        
        # print final results
        print("FINAL:")
        print(pos_best_g)
        print(err_best_g)

        # Calculate z-coordinate (cost function value at best position)
        z_best = costfunc(pos_best_g)
        
        print("X co ordinate: ", pos_best_g[0])
        print("Y co ordinate: ", pos_best_g[1])
        print("Z co ordinate (cost):", z_best)

        # Create 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the best point
        ax.scatter(pos_best_g[0], pos_best_g[1], z_best, c='r', marker='o', s=100, label='Best Position')

        # Create a mesh grid for visualization
        x = np.linspace(bounds[0][0], bounds[0][1], 100)
        y = np.linspace(bounds[1][0], bounds[1][1], 100)
        X, Y = np.meshgrid(x, y)
        Z = np.array([costfunc([xi, yi]) for xi, yi in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

        # Plot the surface
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Cost')
        ax.set_title("PSO Optimization Result")
        plt.colorbar(surf)
        plt.legend()
        plt.show()


if __name__ == "__PSO__":
    main()

#--- RUN ----------------------------------------------------------------------+

initial=[5,5]               # initial starting location [x1,x2...]
bounds=[(-10,10),(-10,10)]  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
PSO(func1,initial,bounds,num_particles=15,maxiter=30)

#--- END ----------------------------------------------------------------------+
'''
Additions:
1. Use meta optimization approach: where another algorithm (like a genetic algorithm) optimizes the PSO parameters.
2. Implement adaptive parameter strategies that adjust w, c1, and c2 during the optimization process based on the swarm's behavior.
3. 
'''