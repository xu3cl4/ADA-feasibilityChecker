def checkFeasibility(last2lines):
    if "SIMULATION_SUCCESSFUL" in last2lines[1]:
        return "feasible"
    else:
        if "SIMULATION_FAILED" in last2lines[1] and "timestep too small" in last2lines[0]:
            return "infeasible"
        else:
            return "other"

def getSuccessRate(n_success, n_failure, n_other=0):
   return round(100*n_success/(n_success + n_failure + n_other), 2) 

def getIndices(i, ncol):
    r, c = i//ncol, i%ncol
    return (r, c)
