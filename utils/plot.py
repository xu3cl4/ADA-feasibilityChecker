paras2string = {
        
        }

units = {
        
        }


def modifylabels(ax, par1, par2, par3=None, xlabel=True, ylabel=True, zlabel=False):

    if xlabel:
        unit1, name1 = units[par1], paras2string[par1]
        ax.set_xlabel(f"{name1}{' (' + unit1 + ')' if len(unit1) > 0 else ''}", fontsize=8)
    else: 
        ax.set_xlabel(None) 

    if ylabel:
        unit2, name2 = units[par2], paras2string[par2]
        ax.set_ylabel(f"{name2}{' (' + unit2 + ')' if len(unit2) > 0 else ''}", fontsize=8)
    else:
        ax.set_ylabel(None)

    if zlabel:
        unit3, name3 = units[par3], paras2string[par3]
        ax.set_zlabel(f"{name2}{' (' + unit2 + ')' if len(unit2) > 0 else ''}", fontsize=8)
    else:
        ax.set_zlabel(None)
    return 

def modifyticks(ax, xtick=True, ytick=True, ztick=False):

    if xtick:
        ax.tick_params(axis='x', labelsize=5, labelrotation = 45)
        tx = ax.xaxis.get_offset_text()
        tx.set_x(1.1)
        tx.set_fontsize(5)
        '''
        tx.set_visible(False)
        axs[r,c].text(1.05, -0.05, str(tx), fontsize=5,transform=axs[r,c].transAxes)
        '''
    else:
        ax.set_xticks([]) 
    
    if ytick:
        ax.tick_params(axis='y', labelsize=5, labelrotation = 45)
        ty = ax.yaxis.get_offset_text()
        ty.set_x(-0.1)
        ty.set_fontsize(5)
    else:
        ax.set_yticks([]) 

    if ztick:
        ax.tick_params(axis='z', labelsize=5, labelrotation = 45)
        tz = ax.yaxis.get_offset_text()
        tz.set_x(-0.1)
        tz.set_fontsize(5)
    else:
        ax.set_zticks([]) 
    return 

def addBinPlot(ax, para_samples, par1, par2, fig, xlabel=True, ylabel=True, xtick=True, ytick=True, colorbar=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        ax:   the axe of a plot 
        idx:   the index of subplot on which we would like to add a bin scatter plot 
        par1:  the first parameter 
        par2:  the second parameter 
        
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
    
    df = para_samples.groupby([f'{par1}_bin', f'{par2}_bin']).mean()
    pcm = ax.scatter(df.index.get_level_values(f'{par1}_bin'), df.index.get_level_values(f'{par2}_bin'), c=df['feasible'], s=100, marker='s')
    if colorbar: fig.colorbar(pcm, ax=ax)

    modifylabels(ax, par1, par2, xlabel, ylabel)
    modifyticks(ax, par1, par2, xtick, ytick)
    return 

def addScatterPlot(ax, para_samples, par1, par2, xlabel=True, ylabel=True, xtick=True, ytick=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        ax:   the axe of a plot 
        idx:   the index of subplot on which we would like to add a scatter plot 
        par1:  the first parameter 
        par2:  the second parameter 
        
        FSB_res: a dictionary storing the indices for feasible, infeasible and other simulations 
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
    
    ax.scatter(para_samples[(para_samples['feasible'] == 1), [par1]], para_samples[(para_samples['feasible'] == 1), [par2]], color='green', label="success", zorder=1, s=1)
    ax.scatter(para_samples[(para_samples['feasible'] == 0), [par1]], para_samples[(para_samples['feasible'] == 0), [par2]], color='red', label="failures", zorder=2, s=1)

    modifylabels(axs, idx, unit1, unit2, name1, name2, xlabel, ylabel)
    modifyticks(axs, idx, unit1, unit2, name1, name2, xtick, ytick)
    return 