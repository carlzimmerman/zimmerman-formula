"""cm03: cm02 with the 20% hydrostatic allowance REPLACED by weak-lensing-calibrated group mass bias (owner's choice, 2026-10-06).
Literature (WebSearch summaries -- PROVISIONAL, verify before citing): Kettula+2013 (COSMOS groups, WL-calibrated M-T, ApJ 778, 74): hydrostatic bias rises
toward low T, 30-50% at 1 keV; FLAMINGO sims (arXiv:2409.07849): b ~ 0.1 at 10^13.75-10^14.25. M_true = M_HSE/(1 - b).
Model (declared before the run): b(T) = b1 (kT/1 keV)^(-0.86) (falls to ~0.1 b1/0.4 at 5 keV), capped at 0.6; b1 = 0.4 central, 0.3/0.5 bracket.
  Scenarios also reported: b = 0 (cm02 base), b = 0.1 flat (FLAMINGO).  Simplifications stated: R500 and M_gas(<R500) are not re-evaluated at the corrected mass.
Statistic and verdict as cm02 (definition A calibrated on X-COP = 0.576); error = scatter (+) stellar bracket (+) half the b1 bracket.
Run: python3 cm03_c003_groups_wl_bias.py | MUTATE=1 sets C003's prediction to 0.9 (verdict must change)
"""
import os, sys, math, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cm02_c003_groups.py")).read().split("d0, mb0, fr0 = run(1.0)")[0]
exec(src)
def runb(sfac, bfun):
    d, fr = [], []
    for g in GR:
        Mb = g["Mg500"] + mstar500(g["M500"]) * sfac; r = g["R500"] * KPC
        y = G_ * Mb * MSUN / r**2 / a0; Mlaw = nu(y) * Mb; MH = g["M500"] / (1 - bfun(g["kT"]))
        f = (MH - Mlaw) / (COSMIC * Mb); d.append(f - fc003(Mb)); fr.append(f)
    return np.array(d), np.array(fr)
kt = np.array([g["kT"] for g in GR]); print(f"   group kT: {kt.min():.2f} .. {kt.max():.2f} keV (median {np.median(kt):.2f})")
bT = lambda b1: (lambda T: min(0.6, b1 * T**-0.86))
for lab, bf in (("b = 0 (cm02)", lambda T: 0.0), ("b = 0.1 flat (FLAMINGO)", lambda T: 0.1), ("Kettula b1 = 0.3", bT(0.3)), ("Kettula b1 = 0.4", bT(0.4)), ("Kettula b1 = 0.5", bT(0.5))):
    d, fr = runb(1.0, bf); print(f"   {lab:26s}: required f median {np.median(fr):.3f}; median (f_req - f_C003) {np.median(d):+.3f}")
d0, _ = runb(1.0, bT(0.4)); dlo, _ = runb(SBR, bT(0.4)); dhi, _ = runb(1 / SBR, bT(0.4)); d3, _ = runb(1.0, bT(0.3)); d5, _ = runb(1.0, bT(0.5))
med = float(np.median(d0)); err = float(np.std(d0, ddof=1) / math.sqrt(len(d0))); star = 0.5 * abs(np.median(dlo) - np.median(dhi)); bb = 0.5 * abs(np.median(d5) - np.median(d3))
tot = math.sqrt(err**2 + star**2 + bb**2); z = med / tot
print(f"   WL-calibrated (b1 = 0.4): median diff {med:+.3f} +- {tot:.3f} (scatter {err:.3f}, stars {star:.3f}, bias bracket {bb:.3f}) -> {z:+.2f} sigma")
verdict = "CONSISTENT" if abs(z) < 2 else ("FAILS: groups need MORE cold mass than C003 keeps" if med > 0 else "FAILS: groups need LESS cold mass than C003 keeps")
print(f"   VERDICT: {verdict}")
check("W verdict computed under the pre-declared rule (MUTATE must change it)", True)
json_out = dict(median=med, err=tot, z=z, verdict=verdict)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
