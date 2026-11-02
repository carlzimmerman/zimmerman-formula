#!/usr/bin/env python3
"""HM1 KiDS (FROZEN_CRITERIA.md): KN1's path, X53's harness, with the response on the native halo. KN1, X53 read only; outputs land here. HM1_F=f KN1_TAG=t KN1_MASS=em1 KN1_NORM=tot|fc1 KN1_SNAP=0.25 python3 hm1_kn1.py. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SGN = 1; F_ = float(os.environ["HM1_F"])
_x = open(os.path.join(RB, "X39_baryonic_contraction", "x39_contraction.py")).read(); exec(_x[_x.index("def contract(r, Mb, M0, F, gnedin=None):"):_x.index('P("\\n=== checks")')])
def hm1_kn(r, Mb, M0):
    if F_ == 0: return M0
    return M0 + F_ * (contract(r, np.maximum.accumulate(Mb), M0, float(Mb[-1] / M0[-1]))[0] - M0)
t = open(os.path.join(RB, "KN1_kids_native_halos", "kn1_kids.py")).read()
for a, b in (("return Mb + Mh_, (10 ** lc_, Rr_, 0.0, True)", "return Mb + hm1_kn(RGRID_PC, Mb, Mh_), (10 ** lc_, Rr_, 0.0, True)"), ('ns = {"__file__": SRC, "__name__": "__main__"}', 'ns = {"__file__": SRC, "__name__": "__main__", "hm1_kn": hm1_kn}')):
    assert t.count(a) == 1, a; t = t.replace(a, b)
exec(compile(t, os.path.abspath(__file__), "exec"), {"__file__": os.path.abspath(__file__), "__name__": "__main__", "hm1_kn": hm1_kn, "os": os})
