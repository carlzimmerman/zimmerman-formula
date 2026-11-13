#!/usr/bin/env python3
"""Conditional finite-radius field for Mc/Mb=59.5 as a plateau *identification*.

This chooses an external field to realize an effective monopole enhancement of
60.5; it does not derive that field or identify the signed source with cold mass.
The solver, grids and diagnostics are identical to corrected_aqual.py.
"""
import sys
sys.dont_write_bytecode=True
from scipy.optimize import brentq
import corrected_aqual
from corrected_core import aqual_asymptote,mu_simple

if __name__=='__main__':
    cold_excess_target=59.5
    x=brentq(lambda x:aqual_asymptote(x)-(1+cold_excess_target),.001,.1,xtol=1e-15)
    corrected_aqual.Y_EXTERNAL=x*float(mu_simple(x))
    print('CONDITIONAL CAPACITY INPUT: Mc/Mb=59.5 identified with effective excess; total F_A=60.5.',flush=True)
    corrected_aqual.main()
