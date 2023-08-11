# import from built-in modules 
from argparse import ArgumentParser, RawTextHelpFormatter as RT
from math     import inf
from pathlib  import Path
from re       import search

import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# import from personal modules 
from utils.extract import listNlines
from utils.others  import checkFeasibility

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
    parser.add_argument('opt',      type = str, help="the file path to store the 'feasibility plot")
    parser.add_argument('--paras',  type = str, help='''the list of parameters of interest, including\nperm, poro, alpha, m, sr, rech, dump, ph, tritium, al, uran\n\n''',          
            nargs='*', default=["perm", "rech", "dump"])

    return parser.parse_args()

def main():
    ''' the basic plotting structure of the python scripts '''  
    args = getArguments()

    ipt_sim  = DIR.joinpath(args.ipt_sim)
    ipt_para = DIR.joinpath(args.ipt_para)
    opt      = DIR.joinpath(args.opt)
    paras    = [string2paras[para] for para in args.paras]
    
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

    success_rate = round(100*len(res["feasible"])/( len(res['feasible']) + len(res['infeasible']) + len(res['other']) ), 2)
    print(f"simulation success rate: {success_rate} %")
'''
    fig.suptitle(f'{wells[well]}', y=0.95)
    fig.tight_layout()

    fig.savefig(opt)
    '''

if __name__ == "__main__":
    main()
