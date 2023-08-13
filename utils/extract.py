# import from the built-in modules 
from os   import SEEK_END, SEEK_CUR
from yaml import safe_load as load

def getBounds(var, fname_yaml):

    with open(fname_yaml, 'r') as f:
        params_ranges = load(f)
        
        if var in params_ranges['amanzi']:
            lb, ub = params_ranges['amanzi'][var]['low'], params_ranges['amanzi'][var]['up']
            return (lb, ub)
        
        if var in params_ranges['pflo']:
            lb, ub = params_ranges['amanzi'][var]['low'], params_ranges['amanzi'][var]['up']
            return (lb, ub)

        print(f'The bounds for {var} is not found')
        return 


def listNlines(fname, n = 1):
    '''implementation source: https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python''' 

    '''Returns the nth before last line of a file as a list of string(s)
       n=1 gives last line, i.e., a list of length 1
    '''
    numl = 0
    with open(fname, 'rb') as f:
        try:
            f.seek(-2, SEEK_END)
            while numl < n:
                f.seek(-2, SEEK_CUR)
                if f.read(1) == b'\n':
                    numl += 1
        except OSError:
            f.seek(0)
        
        lines = []
        for i in range(n):
            lines.append(f.readline().decode())
    return lines
