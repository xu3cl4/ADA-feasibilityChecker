# import from built-in modules 
from argparse             import ArgumentParser, RawTextHelpFormatter as RT
from itertools            import combinations as comb
from mpl_toolkits.mplot3d import Axes3D
from pathlib              import Path
from re                   import search

import matplotlib.pyplot as plt
import pandas            as pd
import sys 
import matplotlib

# import from personal modules 
from utils.extract import listNlines, getBounds
from utils.plot    import add3DSurfacePlot, paras2string
from utils.others  import checkFeasibility, getSuccessRate

# constants 
FPATH = Path(__file__)
DIR = FPATH.parent

string2paras = { "perm": "@k_u@", "poro": "@phi_u@", "alpha": "@alph_u@", "m": "@m_u@", 
        "sr": "@sr@", "rech": "@r_hist@", "dump": "@r_mid@",
        "ph": "@ph_seepage@", "tritium": "@tri_conc_seepage@", "al": "@al_conc_seepage@", "uran": "@uran_conc_seepage@" 
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
    parser.add_argument('--paras',  type = str, help='''the list of parameters of interest, including\nperm, poro, alpha, m, sr, rech, dump, ph, tritium, al, uran''',          
            nargs='*', default=["perm", "rech", "dump"])
    parser.add_argument('--svar',   type = str, help="the parameter to be stratified over", default="")
    parser.add_argument('--ipt_rg', type = str, help="the path to the file storing the range of the parameter to be stratified over")
    parser.add_argument('--n_row',  type = int, help="number of plots per row", default=1000)
    parser.add_argument('--n_stra', type = int, help="number of equal intervals that the stratified parameter would be divide into\n\n", default=3)

    return parser.parse_args()

def main():
    ''' the basic plotting structure of the python scripts '''  
    args = getArguments()

    ipt_sim  = DIR.joinpath(args.ipt_sim)
    ipt_para = DIR.joinpath(args.ipt_para)
    paras    = [string2paras[para] for para in args.paras]
    if len(paras) < 3: sys.exit('3 or more parameters need to be specified.')

    svar     = string2paras[args.svar] if len(args.svar) > 0 else None 
    N_STRA   = args.n_stra
    stratified = False if svar is None else True

    ipt_rg   = DIR.joinpath(args.ipt_rg) if stratified else None
    fname_out= f"{ipt_para.stem}_feasibility3DSurface.pdf" if not stratified else f"{ipt_para.stem}_feasibility3DSurface_stratify{args.svar}_{N_STRA}.pdf"
    opt      = DIR.joinpath(args.opt).joinpath(fname_out)

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
        print(f"Detect unexpected endings from simulations: {[i + 1 for i in res['other']]}")

    success_rate = getSuccessRate( len(res['feasible']), len(res['infeasible']), len(res['other']) )
    print(f"simulation success rate: {success_rate} %")

    # read the parameters used in simulations 
    para_samples = pd.read_csv(ipt_para)

    # encode feasibility 
    para_samples['feasible'] = 0
    para_samples.loc[res['feasible'], ['feasible']] = 1
    para_samples.drop(index=res['other'], inplace=True)

    # plotting  
    groups = list(comb(paras, 3))
    N_PLOTS_PER_ROW = min(len(groups), args.n_row)

    nrow, ncol = len(groups)//N_PLOTS_PER_ROW, N_PLOTS_PER_ROW
    if len(groups) % N_PLOTS_PER_ROW != 0: nrow += 1

    # create more rows for stratifying 
    if stratified:
        nrow *= N_STRA

    fig = plt.figure(figsize=(5*ncol + 1, 5*nrow))
   
    for i, group in enumerate(groups):
        par1, par2, par3 = group
        idx = ncol*i 

        if stratified:

            lb, ub = getBounds(svar, ipt_rg)
            int_width = (ub - lb)/N_STRA
            lb_sub, ub_sub = lb, lb + int_width
            for j in range(N_STRA):  
                ax = fig.add_subplot(nrow, ncol, idx + 1, projection='3d') # index starts with 1 

                sub_para_samples = para_samples[ (para_samples[svar] >= lb_sub) & (para_samples[svar] < ub_sub) ]
                add3DSurfacePlot(ax, sub_para_samples, par1, par2, par3, fig)

                if idx == 0: # only need one legend
                    coord = (0.32, 1) if ncol > 1 else (0.22, 1)
                    ax.legend(bbox_to_anchor=coord, loc="lower left", frameon=False,
                        mode='expand', borderaxespad=0, ncol=2, prop = {'size':8})

                ax.set_title(f'{paras2string[svar]} in [{lb_sub:.2e},{ub_sub:.2e})', loc='right', fontsize=8)

                idx += 1 
                lb_sub += int_width
                ub_sub += int_width

        else:
            ax = fig.add_subplot(nrow, ncol, idx + 1, projection='3d') # index starts with 1 
            add3DSurfacePlot(ax, para_samples, par1, par2, par3, fig)
            if idx == 0: # only need one legend
                coord = (0.32, 1) if ncol > 1 else (0.22, 1)
                ax.legend(bbox_to_anchor=coord, loc="lower left", frameon=False,
                    mode='expand', borderaxespad=0, ncol=2, prop = {'size':8})

    fig.suptitle(f'success rate = {success_rate} %', y=0.99)
    fig.tight_layout()
    fig.savefig(opt)

if __name__ == "__main__":
    main()
