import pyomo.environ as op
import itertools as it
import os

#Developer: @KeivanTafakkori, 4 April 2022 

def model(I,J,a,dispmodel="y",solve="y", dispresult="y"):
    m = op.ConcreteModel("QuadraticAssignmentProblem")  
    m.I = op.Set(initialize=I)
    m.J = op.Set(initialize=J)
    m.K = op.SetOf(m.I)
    m.L = op.SetOf(m.J)
    m.x = op.Var(m.I,m.J, domain=op.Binary)
    objs = {0: sum(a[(i,j,k,l)]*m.x[i,j]*m.x[k,l] for i,j,k,l in it.product(m.I,m.J,m.K,m.L))} 
    cons = {0: {j: (sum(m.x[i,j] for i in m.I) == 1) for j in m.J},
            1: {i: (sum(m.x[i,j] for j in m.J) == 1) for i in m.I}}
    m.OBJ = op.Objective(expr=objs[0],sense=op.minimize)
    m.constraint = op.ConstraintList()
    for keys1 in cons: 
        for keys2 in cons[keys1]: m.constraint.add(expr=cons[keys1][keys2])
        if dispmodel=="y":
            print("Model --- \n",m)
        if solve == "y":
            os.environ['NEOS_EMAIL'] = 'myemail@email.com' 
            solver_manager = op.SolverManagerFactory('neos')
            results = solver_manager.solve(m, solver = "bonmin")
            if dispresult == "y":
                print(results)
                op.display(m)
    return m

w = [[0,3,0,2], 
     [3,0,0,1], #Flow matrix (between assignees)
     [0,0,0,4],
     [2,1,4,0]]

d = [[0,22,53,53],
     [22,0,40,62], #Distance matrix (between assignments)
     [53,40,0,55],
     [53,62,55,0]]

I = range(len(w)) #Set of assignees
K = I

J = range(len(w[0])) #Set of assignments
L = J

a ={(i,j,k,l): w[i][k]*d[j][l] for i,j,k,l in it.product(I,J,K,L)} #Relative cost matrix

m = model(I,J,a) #Model and sovle the problem
