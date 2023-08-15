string2paras = { "perm": "@k_u@", "poro": "@phi_u@", "alpha": "@alph_u@", "m": "@m_u@",
        "sr": "@sr@", "rech": "@r_hist@", "dump": "@r_mid@",
        "ph": "@ph_seepage@", "tritium": "@tri_conc_seepage@", "al": "@al_conc_seepage@", "uran": "@uran_conc_seepage@"
        }

paras2string = {
        "@k_u@": "permeability", "@phi_u@": "porosity", "@alph_u@": "alpha", "@m_u@": "m", "@sr@": "sr",  
        "@r_hist@": "recharge rate", "@r_mid@": "dumping rate", 
        "@ph_seepage@": "ph", "@tri_conc_seepage@": "tritium conc", "@al_conc_seepage@": "Al+++ conc", "@uran_conc_seepage@": "uranium conc"

        }

units = {
        "@k_u@": "m^2", "@phi_u@": "", "@alph_u@": "m s^2/kg-water", "@m_u@": "", "@sr@": "",
        "@r_hist@": "mm/s", "@r_mid@": "mm/s",
        "@ph_seepage@":"", "@tri_conc_seepage@": "mol/kg-water", "@al_conc_seepage@": "mol/kg-water", "@uran_conc_seepage@": "mol/kg-water"
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
        par1:  the first parameter 
        par2:  the second parameter 
        
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
    
    df = para_samples.groupby([f'{par1}_bin', f'{par2}_bin']).mean()
    pcm = ax.scatter(df.index.get_level_values(f'{par1}_bin'), df.index.get_level_values(f'{par2}_bin'), c=df['feasible'], s=100, marker='s')
    if colorbar: fig.colorbar(pcm, ax=ax)

    modifylabels(ax, par1, par2, xlabel, ylabel)
    modifyticks(ax, xtick, ytick)
    return 

def addScatterPlot(ax, para_samples, par1, par2, xlabel=True, ylabel=True, xtick=True, ytick=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        ax:   the axe of a plot 
        par1:  the first parameter 
        par2:  the second parameter 
        
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
   
    feas = para_samples[(para_samples['feasible'] == 1)]
    infeas = para_samples[(para_samples['feasible'] == 0)]
    ax.scatter(feas[par1], feas[par2], color='green', label="success", zorder=1, s=1)
    ax.scatter(infeas[par1], infeas[par2], color='red', label="failures", zorder=2, s=1)

    modifylabels(ax, par1, par2, xlabel, ylabel)
    modifyticks(ax, xtick, ytick)
    return 

def add3DScatterPlot(ax, para_samples, par1, par2, par3, xlabel=True, ylabel=True, zlabel=True, xtick=True, ytick=True, ztick=True):
    '''
        Given the axis of a subplot, the function helps adding a scatter plot onto it. 

        ax:   the axe of a plot 
        par1: the first parameter 
        par2: the second parameter 
        par3: the third parameter
        
        para_samples: a pandas dataframe of which each row is a parameter sample used in the simulations
    '''
   
    feas = para_samples[(para_samples['feasible'] == 1)]
    infeas = para_samples[(para_samples['feasible'] == 0)]
    ax.scatter(feas[par1], feas[par2], feas[par3], color='green', label="success", zorder=1, s=1)
    ax.scatter(infeas[par1], infeas[par2], infeas[par3], color='red', label="failures", zorder=2, s=1)

    for i in range(infeas.shape[0]):
        idx = infeas.index[i]
        ax.text(infeas.loc[idx, par1], infeas.loc[idx, par2], infeas.loc[idx, par3], f'{idx}', zorder=5, size=5, color='k')

    modifylabels(ax, par1, par2, par3, xlabel, ylabel, zlabel)
    modifyticks(ax, xtick, ytick, ztick)
    return 
