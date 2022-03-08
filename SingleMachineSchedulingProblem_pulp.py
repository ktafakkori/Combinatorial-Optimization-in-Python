import pulp as op
import itertools as it

#Developer: @KeivanTafakkori, 8 March 2022

def model(I,J,p,s,dispmodel="y",solve="y", dispresult="y"):
    m = op.LpProblem("SingleMachineSchedulingProblem", op.LpMinimize)
    x = {(i,j): op.LpVariable(f"x{i}{j}", 0,1, op.LpBinary) for i,j in it.product(I, J)}
    c = {j: op.LpVariable(f"c{j}", 0, None, op.LpContinuous) for j in J}
    objs = {0: sum(w[j]*c[j] for j in J)} 
    cons = {0: {i: (sum(x[(i,j)] for j in J) == 1, f"eq1_{i}") for i in I},
            1: {j: (sum(x[(i,j)] for i in I) == 1, f"eq2_{j}") for j in J},
            2: {j: (c[j] >= c[j-1] + sum(x[(i,j)]*p[i] for i in I), f"eq3_{j}") for j in J if j!=0},
            3: {0: (c[0] == s + sum(x[(i,0)]*p[i] for i in I), "eq4_")}}
    m += objs[0]
    for keys1 in cons: 
        for keys2 in cons[keys1]: m += cons[keys1][keys2]
        if dispmodel=="y":
            print("Model --- \n",m)
        if solve == "y":
            result = m.solve(op.PULP_CBC_CMD(timeLimit=None))
            print("Status --- \n", op.LpStatus[result])
            if dispresult == "y" and op.LpStatus[result] =='Optimal':
                print("Objective --- \n", op.value(m.objective))
                print("Decision --- \n", [(variables.name,variables.varValue) for variables in m.variables() if variables.varValue!=0])
    return m, c, x

w = [0.1, 0.4, 0.15, 0.35] #Priority weight of each job
p = [  7,   3,    9,    4] #Processing time of each job
s = 5 #Setup time of the machine
I = range(len(p)) #Set of jobs
J = range(len(I)) #Set of positions

m, c, x = model(I,J,p,s) #Model and solve the problem
