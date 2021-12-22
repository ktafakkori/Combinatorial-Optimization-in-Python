import pulp as op

#Developer: @KeivanTafakkori, 18 December 2021  

def model(J,w,W,p,dispmodel="y",solve="y", dispresult="y"):
    m = op.LpProblem("KnapsackProblem", op.LpMaximize)
    x = {j: op.LpVariable(f"x{j}", 0,1, op.LpBinary) for j in J}
    objs = {0: sum(p[j]*x[j] for j in J)} 
    cons = {0: {0: (sum(w[j]*x[j] for j in J) <= W, "eq1")}}
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

J = range(7) #Set of the items
w = [40,50,30,10,10,40,30] #Weight of the items
W = 100 #Capacity of the knapsack
p = [40,60,10,10,3 ,20,60] #Value of the items

m = model(J,w,W,p) #Model and sovle the problem
