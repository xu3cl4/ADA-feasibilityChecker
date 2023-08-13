# import from built-in modules 
from argparse  import ArgumentParser, RawTextHelpFormatter as RT
from itertools import combinations as comb
from math      import inf
from pathlib   import Path
from re        import search

import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# import from personal modules 
from utils.extract import listNlines
from utils.others  import checkFeasibility, getIndices, getSuccessRate

FPATH = Path(__file__)
DIR = FPATH.parent

string2paras = { "perm": "@k_u@", "poro": "@phi_u@", "alpha": "@alph_u@", "m": "@m_u@", 
        "sr": "@sr@", "rech": "@r_hist@", "dump": "@r_mid@",
        "ph": "@ph_seepage@", "tritium": "@tri_conc_seepage@", "al": "@al_conc_seepage@", "uran": "@uran_conc_seepage@" 
        }

paras2string = { "@k_u@": "permeability", "@phi_u@": "porosity", "@alph_u@": "alpha", "@m_u@": "m", 
        "@sr@": "sr", "@r_hist@": "recharge rate", "@r_mid@": "dumping rate",
        "@ph_seepage@": "pH", "@tri_conc_seepage@": "Tritium conc", "@al_conc_seepage@": "Al+++ conc", "@uran_conc_seepage@": "Urianium conc"
        }

units = { "@k_u@": "m^2", "@phi_u@": "poro", "@alph_u@": "", "@m_u@": "",
        "@sr@": "", "@r_hist@": "mm/s", "@r_mid@": "mm/s",
        "@ph_seepage@": "mol/kg-water", "@tri_conc_seepage@": "mol/kg-water", "@al_conc_seepage@": "mol/kg-water", "@uran_conc_seepage@": "mol/kg-water"
        }

def getArguments():
    ''' parse the command-line interface
        the command line takes 3 required argument 

        ipt_sim:  the directory including the .out files from AMANZI
        ipt_para: the path to the file storing the parameters that AMANZI uses
        opt:      the directory to output the 'feasibility' plot 
    '''  
    parser = ArgumentParser(formatter_class=RT)
    parser.add_argument('ipt_sim',  type = str, help="the directory including the .out files from AMANZI")
    parser.add_argument('ipt_para', type = str, help="the path to the file storing the parameters that AMANZI uses")
    parser.add_argument('opt',      type = str, help="the directory to store the 'feasibility' plot")
    parser.add_argument('--paras',  type = str, help='''the list of parameters of interest, including\nperm, poro, alpha, m, sr, rech, dump, ph, tritium, al, uran\n\n''',          
            nargs='*', default=["perm", "rech", "dump"])
    parser.add_argument('--svar',   type = str, help="the parameter to be stratified over", default="poro")

    return parser.parse_args()

def main():
    ''' the basic plotting structure of the python scripts '''  
    args = getArguments()

    ipt_sim  = DIR.joinpath(args.ipt_sim)
    ipt_para = DIR.joinpath(args.ipt_para)
    fname_out= f"{ipt_para.stem}_feasibility.pdf"
    opt      = DIR.joinpath(args.opt).joinpath(fname_out)
    paras    = [string2paras[para] for para in args.paras]
    svar     = string2paras[args.svar]
    
    # get the indices for feasible/infeasible sets of parameters
    res = {
            "feasible": [],
            "infeasible": [],
            "other": []
        }

    # record if a simulation is successful 
    files = Path(ipt_sim).glob('*.out')
    for f in files:
        fname = Path(f).stem
        match = search('\d+', fname)
        idx = int(fname[match.start():match.end()]) - 1

        lastTwoLines = listNlines(f, 2)
        cat = checkFeasibility(lastTwoLines) 
        res[cat].append(idx)

    if len(res['other']) != 0:
        print(f'Detect unexpected endings from simulations: {[i + 1 for i in other]}')

    success_rate = getSuccessRate( len(res['feasible']), len(res['infeasible']), len(res['other']) )
    print(f"simulation success rate: {success_rate} %")
    

    # plotting  
    pairs = list(comb(paras, 2))
    nrow, ncol = len(pairs)//3, 3
    if len(pairs) % 3 != 0: nrow += 1
    fig, axs = plt.subplots(nrow, ncol,figsize=(10, 3.5*nrow))
   
    paras_samples = pd.read_csv(ipt_para)
    for i, pair in enumerate(pairs):
        r, c = getIndices(i, ncol)
        idx = c if len(pairs) == 3 else (r, c)
        par1, par2 = pair
        axs[idx].scatter(paras_samples.loc[res['feasible'], [par1]], paras_samples.loc[res['feasible'], [par2]], color='green', label="success", zorder=1, s=1)
        axs[idx].scatter(paras_samples.loc[res['infeasible'], [par1]], paras_samples.loc[res['infeasible'], [par2]], color='red', label="failures", zorder=2, s=1)

        unit1, unit2 = units[par1], units[par2]
        axs[idx].set_xlabel(f"{paras2string[par1]}{' (' + unit1 + ')' if len(unit1) > 0 else ''}", fontsize=8)
        axs[idx].set_ylabel(f"{paras2string[par2]}{' (' + unit2 + ')' if len(unit2) > 0 else ''}", fontsize=8)
        axs[idx].tick_params(labelrotation=45, labelsize=5)
        tx = axs[idx].xaxis.get_offset_text()
        tx.set_x(1.1)
        tx.set_fontsize(5)
        '''
        tx.set_visible(False)
        axs[r,c].text(1.05, -0.05, str(tx), fontsize=5,transform=axs[r,c].transAxes)
        '''
        ty = axs[idx].yaxis.get_offset_text()
        ty.set_x(-0.1)
        ty.set_fontsize(5)

        if r + c == 0: # only need one legend
            axs[idx].legend(bbox_to_anchor=(0.62, 1.02), loc="lower right", frameon=False,
                 mode='expand', borderaxespad=0, ncol=2, prop = {'size':8})

    fig.suptitle(f'success rate = {success_rate} %', y=0.95)
    fig.tight_layout()
    fig.savefig(opt)

if __name__ == "__main__":
    main()
