#!/usr/bin/env python3
"""AM1 POST-RESULT, reported only: all the choices that lower the match, stacked: all galaxies, M* + 0.2 dex, Sheth-Tormen [BORROWED FIT], and the n_b it would take to reach EM1 at lg M_b 10. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); T = open(os.path.join(HERE, "am1_match.py")).read(); J = json.load(open(os.path.join(HERE, "am1_sigma.json"))) if os.path.exists(os.path.join(HERE, "am1_sigma.json")) else None
B = json.load(open(os.path.join(HERE, "am1_bmf.json"))); GR = np.array(B["grid"]); LM = np.array(J["lMg"]); SIG = np.sqrt(np.array(J["s2"])); RHO = J["rhom0"]; DC = J["DC"]; dln = np.gradient(np.log(SIG), np.log(10 ** LM)); nu = DC / SIG; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
fPS = np.sqrt(2 / np.pi) * nu * np.exp(-nu ** 2 / 2); a_, p_, A_ = 0.707, 0.3, 0.3222; fST = A_ * np.sqrt(2 * a_ / np.pi) * (1 + (a_ * nu ** 2) ** (-p_)) * nu * np.exp(-a_ * nu ** 2 / 2)
def cum(f): d = RHO / 10 ** LM * f * np.abs(dln) * math.log(10); dl = LM[1] - LM[0]; return np.concatenate([np.cumsum(0.5 * (d[1:] + d[:-1])[::-1] * dl)[::-1], [0.0]])
cP, cS = cum(fPS), cum(fST); inv = lambda c, n: float(np.interp(math.log(n), np.log(c[c > 1e-30])[::-1], LM[c > 1e-30][::-1]))
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("AM1 generous stack, POST-RESULT, reported only; kappa = 1/2 FITTED; not theory closed"); nall = float(np.interp(10.0, GR, B["all"])); nplus = None
GRID = GR; allplus = float(np.interp(10.0 - 0.2, GR, B["all"])); cenplus = float(np.interp(10.0, GR, B["cen_plus"]))
for lab, n, c in (("frozen: centrals, PS", float(np.interp(10.0, GR, B["cen"])), cP), ("all galaxies, PS", nall, cP), ("centrals, M* + 0.2, PS", cenplus, cP), ("all galaxies, M* + 0.2 (approx: n_b at lg M_b 9.8), PS", allplus, cP), ("all galaxies, M* + 0.2 (approx), ST [BORROWED FIT]", allplus, cS)):
    v = inv(c, n); P(f"  {lab}: n_b(>1e10) {n:.3e}/Mpc^3; total M_t {v:.3f}; cold M200 {v + math.log10(FC):.3f}; Delta from EM1 {v + math.log10(FC) - 11.18:+.3f}")
Mt = 11.18 - math.log10(FC); nH = float(np.interp(Mt, LM, cP)); P(f"EM1's relation says M_b 1e10 sits at M_t 10^{Mt:.2f}: PS n(>M_t) {nH:.3e}/Mpc^3 against n_b(>1e10) {float(np.interp(10.0, GR, B['cen'])):.3e} (centrals), {nall:.3e} (all): {nH / float(np.interp(10.0, GR, B['cen'])):.1f} and {nH / nall:.1f} halos per galaxy; ST n {float(np.interp(Mt, LM, cS)):.3e}")
for lb in (9.0, 9.5, 10.5, 11.0): Mt_ = 11.18 + 0.90 * (lb - 10) - math.log10(FC); P(f"  lg M_b {lb}: EM1's M_t 10^{Mt_:.2f}: PS n {float(np.interp(Mt_, LM, cP)):.3e}, n_b centrals {float(np.interp(lb, GR, B['cen'])):.3e}, ratio {float(np.interp(Mt_, LM, cP)) / float(np.interp(lb, GR, B['cen'])):.1f}")
open(os.path.join(HERE, "am1_generous.out"), "w").write("\n".join(OUT) + "\n")
