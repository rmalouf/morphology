#!/usr/bin/env python

import numpy as np
import pandas as pd
import random

def entropy(paradigm):
    result = pd.Series(index=list(paradigm.columns))
    for cell in paradigm.columns:
        v = paradigm[cell].value_counts(normalize=True)
        result[cell] = -sum(v * np.log2(v))
    return result
    
def cond_entropy(paradigm):
    result = pd.DataFrame(index=paradigm.columns,columns=paradigm.columns)
    for r in paradigm.columns:
        v = paradigm[r].value_counts(normalize=True)
        H = -sum(v * np.log2(v))
        for c in paradigm.columns:
            if r != c:
                v = (paradigm[r] + ':' + paradigm[c]).value_counts(normalize=True)
                result[c][r] = -sum(v * np.log2(v)) - H            
    return result
    
def bootstrap(paradigm,R):
    Hs = [ cond_entropy(paradigm).mean().mean() ]
    p = paradigm.copy()
    for i in xrange(R):
        for cell in p.columns:
            vals = paradigm[cell].values
            for row in p[cell].index:
                p[cell][row] = random.choice(vals)
        Hs.append(cond_entropy(p).mean().mean())
    return pd.Series(Hs)
    
if __name__ == '__main__':
    
    import sys

    pd.set_option('display.float_format',lambda x : '%.3f'%x)
    paradigm = pd.read_table(sys.argv[1],index_col=0,encoding='utf-8')

    print '** Paradigm'
    print
    print paradigm    
    print 'Declension entropy = %.3f bits'%(np.log2(len(paradigm.index)))

    print
    print '** Cell entropy'
    print
    print entropy(paradigm)
    print 'Avg. cell entropy  = %.3f bits'%(entropy(paradigm).mean())

    print
    print '** Conditional entropy'
    print
    print cond_entropy(paradigm)
    print 'Avg. cond. entropy = %.3f bits'%(cond_entropy(paradigm).mean().mean())

    print
    print '** Bootstrap'
    print

    boot = bootstrap(paradigm,99)
    print 'Bootstrap avg. = %.3f bits'%(boot.mean())
    print 'Bootstrap p    = %.3f'%(1.0 - sum(boot >= boot[0]) / 500.)




