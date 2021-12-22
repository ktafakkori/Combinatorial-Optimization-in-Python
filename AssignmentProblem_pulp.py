import pulp as op
import itertools as it

#Developer: @KeivanTafakkori, 22 December 2021

def model(I,J,c,dispmodel="y",solve="y", dispresult="y"):
    m = op.LpProblem("AssignmentProblem", op.LpMinimize)
    x = {(i,j): op.LpVariable(f"x{i}{j}", 0,1, op.LpBinary) for i,j in it.product(I, J)}
    objs = {0: sum(c[i][j]*x[(i,j)] for i,j in it.product(I, J))} 
    cons = {0: {i: (sum(x[(i,j)] for j in J) == 1, f"eq1_{i}") for i in I},
            1: {j: (sum(x[(i,j)] for i in I) == 1, f"eq2_{j}") for j in J}}
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
                print("Slack --- \n", [(name,constraint.slack) for name, constraint in m.constraints.items() if constraint.slack!=0])    
            return m

I = range(3) #Set of agents
J = range(3) #Set of tasks
c = [[7, 3, 1],
     [2, 9, 5],  #Cost matrix for agent-task assignment
     [6, 8, 4]]

m = model(I,J,c) #Model and solve the problem
