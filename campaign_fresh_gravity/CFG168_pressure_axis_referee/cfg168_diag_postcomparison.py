#!/usr/bin/env python3
# CFG168 post-comparison diagnostics (written AFTER CFG162's script/out/json were opened; not part of the frozen main).
#  D1: break-evens at s=1 with inc_sfr_deg (my CFG165's column) -> does 2.14/0.65 come from the inclination column?
#  D2: A3 geometric-mean placement of P3 excluding the disc whose P3 correction is exactly 0.
#  D3: the README's own bracketing (0.25 grid, then brentq) vs my continuous root, at K21 s=1 (already equal to 3 decimals in main).
import sys
sys.dont_write_bytecode = True
from cfg168_common import *   # noqa
A = load_A()
for col in ("inc_star_deg", "inc_sfr_deg"):
    S = load_S(col)
    bf = breakeven_mu(lambda m: K21cell(S, A, 1.0, m)["flat"]["dprime"]); bh = breakeven_mu(lambda m: K21cell(S, A, 1.0, m)["H"]["dprime"])
    c = crossings(S, A)
    P(f"D1 {col}: break-even flat {bf:.3f} rival {bh:.3f}; s_mid {c['s_mid']:.4f} s_f2 {c['s_f2']:.4f} s_h2 {c['s_h2']:.4f}")
S = load_S()
C, _ = M.corr(S, M.spec("P3")); C1, _ = M.corr(S, spec_k21(1.0))
r = C / C1
P("D2 P3/K21 correction ratio per disc:", dict(zip(S.ids, np.round(r, 3))))
m = r > 0
P(f"D2 geometric mean excluding zero-correction discs: {float(np.exp(np.mean(np.log(r[m])))):.3f}; median {float(np.median(r)):.3f}; (base s_eq 1.617)")
P("D2 zero-correction disc(s):", [S.ids[i] for i in range(len(r)) if r[i] == 0], "sigma gradient d(sigma^2)/dR:", np.round(S.grad2, 1))
