# import from built-in modules 
from argparse  import ArgumentParser, RawTextHelpFormatter as RT
from itertools import combinations as comb
from pathlib   import Path
from re        import search

import matplotlib.pyplot as plt
import pandas            as pd

# import from personal modules 
from utils.extract import listNlines, getBounds
from utils.plot    import addBinPlot
from utils.others  import checkFeasibility, getIndices, getSuccessRate, indexFormatter

# constants 
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
    parser.add_argument('ipt_rg', type = str, help="the path to the file storing the range of the parameters")
    parser.add_argument('opt',      type = str, help="the directory to store the 'feasibility' plot")
    parser.add_argument('--paras',  type = str, help='''the list of parameters of interest, including\nperm, poro, alpha, m, sr, rech, dump, ph, tritium, al, uran''',          
            nargs='*', default=["perm", "rech", "dump"])
    parser.add_argument('--svar',   type = str, help="the parameter to be stratified over", default="")
    parser.add_argument('--n_row',  type = int, help="number of plots per row", default=1000)
    parser.add_argument('--n_stra', type = int, help="number of equal intervals that the stratified parameter would be divide into", default=3)
    parser.add_argument('--n_bin',  type = int, help="number of bins for each parameter\n\n", default=5)

    return parser.parse_args()

def main():
    ''' the basic plotting structure of the python scripts '''  
    args = getArguments()

    ipt_sim  = DIR.joinpath(args.ipt_sim)
    ipt_para = DIR.joinpath(args.ipt_para)
    paras    = [string2paras[para] for para in args.paras]
    svar     = string2paras[args.svar] if len(args.svar) > 0 else None 
    N_STRA   = args.n_stra
    N_BIN    = args.n_bin
    
    stratified = False if svar is None else True
    ipt_rg   = DIR.joinpath(args.ipt_rg)
    fname_out= f"{ipt_para.stem}_feasibilityBinning.pdf" if not stratified else f"{ipt_para.stem}_feasibilityBinning_stratify{args.svar}_{N_STRA}.pdf"
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
        print(f'Detect unexpected endings from simulations: {[i + 1 for i in other]}')

    success_rate = getSuccessRate( len(res['feasible']), len(res['infeasible']), len(res['other']) )
    print(f"simulation success rate: {success_rate} %")
    
    # read the parameters used in simulations 
    para_samples = pd.read_csv(ipt_para)
    
    # encode feasibility 
    para_samples['feasible'] = 0
    print(para_samples.index)
    para_samples.loc[res['feasible'], ['feasible']] = 1
    para_samples.drop(index=res['other'], inplace=True)

    # binning 
    for para in paras:
        lb, ub = getBounds(para, ipt_rg)
        int_width = (ub - lb)/N_BIN
        bins = [lb]
        labels = [] 
        for i in range(1, N_BIN + 1):
            bins.append(lb + i*int_width)
            labels.append( (bins[i] + bins[i-1])/2 )
        para_samples[f'{para}_bin'] = pd.cut(para_samples[para], bins=bins, labels=labels)


    # plotting  
    pairs = list(comb(paras, 2))
    N_PLOTS_PER_ROW = min(len(pairs), args.n_row)

    nrow, ncol = len(pairs)//N_PLOTS_PER_ROW, N_PLOTS_PER_ROW
    if len(pairs) % N_PLOTS_PER_ROW != 0: nrow += 1
    idx_f = 1

    # create more rows for stratifying 
    if stratified:
        idx_f = N_STRA
        nrow *= N_STRA

    fig, axs = plt.subplots(nrow, ncol, figsize=(3.3*ncol + 1, 3.3*nrow))
   
    for i, pair in enumerate(pairs):
        r, c = getIndices(i, ncol, idx_f)
        legend = True if r + c == 0 else False

        par1, par2 = pair
        unit1, unit2 = units[par1], units[par2]
        name1, name2 = paras2string[par1], paras2string[par2]
        
        if stratified:

            lb, ub = getBounds(svar, ipt_rg)
            int_width = (ub - lb)/N_STRA
            lb_sub, ub_sub = lb, lb + int_width
            for i in range(N_STRA):  
                sub_para_samples = para_samples[ (para_samples[svar] >= lb_sub) & (para_samples[svar] < ub_sub) ]
                idx = indexFormatter(r, c, nrow, ncol)

                if i != N_STRA - 1:
                    addBinPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, sub_para_samples, fig, xlabel=False, xtick=False)
                else:
                    addBinPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, sub_para_samples, fig)

                if c == ncol - 1:
                    '''axs[idx].set_title(f'{paras2string[svar]} in [{lb_sub:.2e},{ub_sub:.2e})', rotation=-90, position=(1, 0.5), fontsize=8)'''
                    axs[idx].set_title(f'{paras2string[svar]} in [{lb_sub:.2e},{ub_sub:.2e})', loc='right', fontsize=8)

                r += 1
                lb_sub += int_width
                ub_sub += int_width

        else:
            idx = indexFormatter(r, c, nrow, ncol)
            addBinPlot(axs, idx, par1, par2, unit1, unit2, name1, name2, para_samples, fig)

        if legend: # only need one legend
            idx = indexFormatter(0, 0, nrow, ncol)
            coord = (0.32, 1) if ncol > 1 else (0.22, 1.08)
            axs[idx].legend(bbox_to_anchor=coord, loc="lower left", frameon=False,
                 mode='expand', borderaxespad=0, ncol=2, prop = {'size':8})

    fig.suptitle(f'success rate = {success_rate} %', y=0.98)
    fig.tight_layout()
    fig.savefig(opt)

if __name__ == "__main__":
    main()
