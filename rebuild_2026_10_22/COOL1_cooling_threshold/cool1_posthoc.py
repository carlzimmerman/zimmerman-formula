#!/usr/bin/env python3
"""COOL1 POST-HOC (no verdict depends on it): the Birnboim-Dekel form at r_s = R200c came nearest W at Z 0.
One read of how firm that is: Z and f_g one at a time on that form. Uses cool1.py's functions unchanged."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cool1.py")).read().split("# ---------------------------------------------------------------- checks")[0]
exec(src)
for kw in (dict(), dict(Z=.03), dict(Z=.1), dict(Z=.3), dict(Z=1), dict(fg=.5), dict(fg=.2)):
    a = mthr(0.0, form="BD", **kw); b, z = desc(ZH, 0.5, form="BD", **kw)
    P(f"BD r_s/R 1 {str(kw):16s} P0 {fm(a)}{' IN W' if inw(a) else ''}  Pf {fm(b)}{' IN W' if inw(b) else ''}  (z_half {z:.2f})")
open(os.path.join(HERE, "cool1_posthoc.out"), "w").write("\n".join(OUT) + "\n")
