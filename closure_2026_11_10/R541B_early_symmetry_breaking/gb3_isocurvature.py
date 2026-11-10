"""R541B GB3: isocurvature from the clock's own offset while V' != 0; KA7, MU5 (criteria: FROZEN_CRITERIA.md).
Separate-universe reading: on scales outside the horizon at generation (CMB scales, generation at z >= 1e5), a patch
whose clock is offset by delta tau_rel against the adiabatic time makes a different charge; S = delta ln C."""
import os, sys, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r541b_core import cosmo, m_of_mu, Pot, run, t_rad, OMEGA_R, H0_SI

S_LINE = 9e-6   # |S| <= sqrt(0.04 * 2.1e-9): Planck 2018 X, uncorrelated CDM isocurvature (INDICATIVE, PROVISIONAL)
print(f"GB3 line |S| <= {S_LINE:.1e}  (= sqrt(0.04) x 4.6e-5)")

cp = cosmo("canonical")
rad = dict(Ob=0.0, Or=OMEGA_R, OL=0.0, R=1.0)
mbig = 1e16

# KA7: sharp step in radiation, S = (3/2) dtau / t_s
zs = 1e6; a_s = 1 / (1 + zs); ts = t_rad(a_s, rad); eps = 1e-3
seg = [(np.log(a_s) - 0.02, np.log(a_s) + 0.02, 2e-6)]
Cp = run(Pot("tanh", 1e17, ts, D=1e-4 * ts), rad, mbig, a_ini=1e-12, tau_off=+eps * ts, segs=seg).Cfin()
Cm = run(Pot("tanh", 1e17, ts, D=1e-4 * ts), rad, mbig, a_ini=1e-12, tau_off=-eps * ts, segs=seg).Cfin()
S_num = (math.log(Cp) - math.log(Cm)) / 2       # per +eps t_s offset: clock AHEAD switches off EARLIER
S_ana = -1.5 * eps
print(f"KA7 sharp step: dlnC per +1e-3 t_s offset = {S_num:.5e}, analytic -(3/2)(1e-3) = {S_ana:.5e}, "
      f"ratio {S_num / S_ana:.4f}  {'PASS' if abs(S_num / S_ana - 1) <= 0.02 else 'FAIL'}")

# Per family: dlnC/d(tau_i / tau_s), required synchronisation, and whether the offset is damped before generation
print("\nfamily | mu_K line | z_s | dlnC/d(tau_i/tau_s) | required |delta tau_rel|/tau_s for |S| <= line | "
      "offset at 50% generation / initial offset")
fams = [("exp", {}), ("tanh", {"D": 0.1}), ("power", {"n": 3})]
reqs = {}
for lab, mu in {"Jeans": 2.512e4, "BBN": 8.89e6}.items():
    m = m_of_mu(mu)
    for zs in (1e5, 1e6):
        a_s = 1 / (1 + zs); ts = t_rad(a_s, cp)
        V0 = 0.12 / (1.3 * a_s**3)
        segs = [(np.log(a_s) - 6, np.log(a_s) + 6, 0.02)]
        for kind, kw0 in fams:
            kw = {k: (v * ts if k == "D" else v) for k, v in kw0.items()}
            e = 1e-3
            sp_ = run(Pot(kind, V0, ts, **kw), cp, m, a_ini=1e-3 * a_s, tau_off=+e * ts, segs=segs)
            sm_ = run(Pot(kind, V0, ts, **kw), cp, m, a_ini=1e-3 * a_s, tau_off=-e * ts, segs=segs)
            d = (math.log(sp_.Cfin()) - math.log(sm_.Cfin())) / (2 * e)
            z50 = sp_.z_of_frac(0.5)
            a50 = 1 / (1 + z50)
            off50 = (sp_.state(a50)["tau"] - sm_.state(a50)["tau"]) / (2 * e * ts)
            req = S_LINE / abs(d)
            reqs[(kind, lab, zs)] = req
            print(f"{kind}{kw0 if kw0 else ''} | {lab} | {zs:.0e} | {d:+.4f} | {req:.2e} | {off50:.4f} "
                  f"({'NOT damped' if off50 > 0.1 else 'damped'})")

# MU5: offset 1e-3 t_s with the exponential
d_exp = None
print("\nMU5 offset delta tau_rel = 1e-3 tau_s, exponential: |S| = 1e-3 x |dlnC/d(tau_i/tau_s)| ~ 1e-3 >> 9e-6 -> "
      "GB3 FAIL (bites)")

# (iv) crude inflationary estimate (c_s = 1 assumed; action (A) has c_s = 0 at Q = 1, see RESULT)
GEV_PER_INV_MPC = 1.97327e-16 / 3.0856775814913673e22   # hbar c / Mpc in GeV
HBAR_GEV_S = 6.582119569e-25
MPL = 2.435e18
print("\n(iv) crude: delta pi = H_inf / (2 pi sqrt2 M_pl mu_K) (canonical field phi = sqrt2 M_pl mu_K pi, c_s = 1).")
print("Largest H_inf [GeV] allowed by |S| = |dlnC/d(tau_i/tau_s)| delta pi / tau_s <= 9e-6, exponential family:")
for lab, mu in {"Jeans": 2.512e4, "BBN": 8.89e6}.items():
    for zs in (1e5, 1e6):
        a_s = 1 / (1 + zs); ts_s = t_rad(a_s, cp) / H0_SI          # seconds
        ts_gev = ts_s / HBAR_GEV_S                                  # 1/GeV
        mu_gev = mu * GEV_PER_INV_MPC
        req = reqs[("exp", lab, zs)]
        Hmax = req * ts_gev * 2 * math.pi * math.sqrt(2) * MPL * mu_gev
        print(f"  mu_K {lab} ({mu:.3e}/Mpc), z_s {zs:.0e} (tau_s {ts_s:.3e} s): H_inf <= {Hmax:.3e} GeV")
print("  (for comparison, the tensor bound r < 0.036 allows H_inf up to about 5e13 GeV: PROVISIONAL, from memory)")
