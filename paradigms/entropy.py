#!/usr/bin/env python

"""
This module includes functions for calculating average conditional entropy as
described in:

    Ackerman, Farrell, James P. Blevins, & Robert Malouf. 2009. "Parts and wholes: 
        Patterns of relatedness in complex morphological systems and why they matter."
        In Analogy in Grammar: Form and Acquisition, ed. by James P. Blevins & Juliette 
        Blevins, 54-82. Oxford: Oxford University Press.

    Ackerman, Farrell and Robert Malouf. 2013. "Morphological organization: The Low 
      Conditional Entropy Conjecture." Language 89:429-464.


Copyright 2013 Rob Malouf
"""      
      

import random

import numpy as np
import pandas as pd

def entropy(paradigm):
    """Calculate the entropy for each cell in an inflectional paradigm"""

    result = pd.Series(index=list(paradigm.columns))
    for cell in paradigm.columns:
        v = paradigm[cell].value_counts(normalize=True)
        result[cell] = -sum(v * np.log2(v))
    return result
    
def cond_entropy(paradigm):
    """Calculate the pairwise conditional entropy cells in an inflectional paradigm"""

    result = pd.DataFrame(index=paradigm.columns,columns=paradigm.columns)
    for r in paradigm.columns:
        v = paradigm[r].value_counts(normalize=True)
        H = -sum(v * np.log2(v))
        for c in paradigm.columns:
            if r != c:
                v = (paradigm[r] + ':' + paradigm[c]).value_counts(normalize=True)
                result[c][r] = -sum(v * np.log2(v)) - H            
    return result
    
def bootstrap(paradigm,R=99):
    """Perform a bootstrap simulation to estimate the average conditional entropy one
       would expect to find in a given paradigm (absent implicational relations)."""

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




