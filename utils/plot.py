def modifylabels(ax, unit1, unit2, name1, name2, xlabel=True, ylabel=True, zlabel=True):

    if xlabel:
        ax.set_xlabel(f"{name1}{' (' + unit1 + ')' if len(unit1) > 0 else ''}", fontsize=8)
    else: 
        ax.set_xlabel(None) 

    if ylabel:
        ax.set_ylabel(f"{name2}{' (' + unit2 + ')' if len(unit2) > 0 else ''}", fontsize=8)
    else:
        ax.set_ylable(None)
    return 

def modifyticks(ax, unit1, unit2, name1, name2, xtick=True, ytick=True, ztick=True):
    if xtick:
        ax.tick_params(axis='x', labelsize=5, labelrotation = 45)
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
        axs[idx].tick_params(axis='y', labelsize=5, labelrotation = 45)
        ty = axs[idx].yaxis.get_offset_text()
        ty.set_x(-0.1)
        ty.set_fontsize(5)
    else:
        axs[idx].set_yticks([]) 

    return 

def addBinPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, para_samples, fig, xlabel=True, ylabel=True, xtick=True, ytick=True, colorbar=True):
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
    
    df = para_samples.groupby([f'{par1}_bin', f'{par2}_bin']).mean()
    pcm = axs[idx].scatter(df.index.get_level_values(f'{par1}_bin'), df.index.get_level_values(f'{par2}_bin'), c=df['feasible'], s=100, marker='s')
    if colorbar: fig.colorbar(pcm, ax=axs[idx])

    modifylabels(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    modifyticks(axs, idx, unit1, unit2, name1, name2, xtick, ytick)
    return 

def addScatterPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, para_samples, xlabel=True, ylabel=True, xtick=True, ytick=True):
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
    
    axs[idx].scatter(para_samples[(para_samples['feasible'] == 1), [par1]], para_samples[(para_samples['feasible'] == 1), [par2]], color='green', label="success", zorder=1, s=1)
    axs[idx].scatter(para_samples[(para_samples['feasible'] == 0), [par1]], para_samples[(para_samples['feasible'] == 0), [par2]], color='red', label="failures", zorder=2, s=1)

    modifylabels(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    modifyticks(axs, idx, unit1, unit2, name1, name2, xtick, ytick)
    return 
