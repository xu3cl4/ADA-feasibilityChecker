def modifylabels(axs, idx, unit1, uni2, name1, name2, xlabel=True, ylabel=True):
    if xlabel:
        axs[idx].set_xlabel(f"{name1}{' (' + unit1 + ')' if len(unit1) > 0 else ''}", fontsize=8)
    else: 
        axs[idx].set_xlabel(None) 

    if ylabel:
        axs[idx].set_ylabel(f"{name2}{' (' + unit2 + ')' if len(unit2) > 0 else ''}", fontsize=8)
    else:
        axs[idx].set_ylable(None)
    return 

def modifyticks(axs, idx, unit1, unit2, name1, name2, xlabel=True, ylabel=True):
    if xtick:
        axs[idx].tick_param(axis='x', labelsize=5, labelrotation = 45)
        tx = axs[idx].xaxis.get_offset_text()
        tx.set_x(1.1)
        tx.set_fontsize(5)
        '''
        tx.set_visible(False)
        axs[r,c].text(1.05, -0.05, str(tx), fontsize=5,transform=axs[r,c].transAxes)
        '''
    else:
        axs[idx].set_xticks([]) 
    
    if ytick:
        axs[idx].tick_param(axis='y', labelsize=5, labelrotation = 45)
        ty = axs[idx].yaxis.get_offset_text()
        ty.set_x(-0.1)
        ty.set_fontsize(5)
    else:
        axs[idx].set_yticks([]) 
    return 

def addBinPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, para_samples, xlabel=True, ylabel=True, xtick=True, ytick=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        axs:   the axes of all plots 
        idx:   the index of subplot on which we would like to add a scatter plot 
        par1:  the first parameter 
        par2:  the second parameter 
        unit1: the unit of the first parameter 
        unit2: the unit of the second parameter 
        name1: the human-writtable name of the first parameter 
        name2: the human-writtable name of the second parameter
        
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
    
    axs[idx].scatter(para_samples.loc[idx_feas, [par1]], para_samples.loc[idx_feas, [par2]], s=1)
    axs[idx].scatter(para_samples.loc[idx_infeas, [par1]], para_samples.loc[idx_infeas, [par2]], s=1)

    modifylabels(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    modifyticks(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    return 

def addScatterPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, FSB_res, para_samples, xlabel=True, ylabel=True, xtick=True, ytick=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        axs:   the axes of all plots 
        idx:   the index of subplot on which we would like to add a scatter plot 
        par1:  the first parameter 
        par2:  the second parameter 
        unit1: the unit of the first parameter 
        unit2: the unit of the second parameter 
        name1: the human-writtable name of the first parameter 
        name2: the human-writtable name of the second parameter
        
        FSB_res: a dictionary storing the indices for feasible, infeasible and other simulations 
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
    
    idx_feas = para_samples.index.intersection(FSB_res['feasible'])
    idx_infeas = para_samples.index.intersection(FSB_res['infeasible'])
    axs[idx].scatter(para_samples.loc[idx_feas, [par1]], para_samples.loc[idx_feas, [par2]], color='green', label="success", zorder=1, s=1)
    axs[idx].scatter(para_samples.loc[idx_infeas, [par1]], para_samples.loc[idx_infeas, [par2]], color='red', label="failures", zorder=2, s=1)

    modifylabels(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    modifyticks(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    return 

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

def getIndices(i, ncol, f=1):
    r, c = i//ncol, i%ncol
    return (r*f, c)

def indexFormatter(r, c, nrow, ncol):
    if nrow != 1 and ncol != 1:
        return (r, c)
    if nrow == 1:
        return c
    if ncol == 1:
        return r  
