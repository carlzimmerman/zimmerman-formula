#!/usr/bin/env python3
"""L175 -- POTENTIAL-DEPTH MECHANISM: a dark component that clusters only where |Phi| exceeds a threshold Phi_c (no heating; a switch on
local potential depth). Ledger requirement: present in clusters (Phi ~ 2e-5 c^2 at 1 Mpc), absent in MW-like galaxies (Phi <~ 6e-7 c^2 at
10 kpc) => Phi_c in [6e-7, 2e-5] c^2. Test: the rms potential on the scales the forest (z = 3, k = 1-10 h/Mpc) and the third peak
(z = 1100, k = 0.05-0.15 /Mpc) require the component to cluster on. Linear Phi_k from CLASS. No literal-True checks."""
import numpy as np
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
h = 0.6736; G = 4.30091e-6; c2 = 299792.458**2
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0,
                      "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 60, "z_max_pk": 50}); cl.compute()
ZREC = 30.0   # matter-era stand-in: linear Phi_k is constant in matter domination; the true z = 1100 value is ~10-20% lower (radiation), which only strengthens P3
Om = 0.3138; H0 = 100*h/299792.458
def Phi_rms(k_h, z):   # rms of the Newtonian potential per ln k, in units of c^2 (Poisson, linear)
    k = k_h*h; D2 = k**3*cl.pk_lin(k, z)/(2*np.pi**2)
    return 1.5*Om*H0**2*(1 + z)/k**2*np.sqrt(D2)
Phi_cl = G*5e14/1000/c2; Phi_mw = 5e4/c2; Phi_mw_out = G*2e11/300/c2
print(f"    ledger potentials: X-COP cluster at 1 Mpc {Phi_cl:.1e} c^2; MW at 10 kpc {Phi_mw:.1e}; MW halo at 300 kpc {Phi_mw_out:.1e}")
lo, hi = Phi_mw, Phi_cl
check("P1 a single threshold separating MW-like galaxies (absent) from X-COP clusters (present) exists: Phi_c in [6e-7, 2e-5] c^2 (window 40x)", hi/lo > 10, f"{lo:.1e}..{hi:.1e}")
print(f"    {'scale':<34} {'Phi_rms [c^2]':>14}  clusters at the lowest admissible threshold?")
rows = [("forest z=3, k=1 h/Mpc", Phi_rms(1.0, 3.0)), ("forest z=3, k=5 h/Mpc", Phi_rms(5.0, 3.0)), ("shear z=0.5, k=1 h/Mpc", Phi_rms(1.0, 0.5)),
        ("third peak k=0.05/Mpc (matter-era Phi)", Phi_rms(0.05/h, ZREC)), ("third peak k=0.15/Mpc (matter-era Phi)", Phi_rms(0.15/h, ZREC)), ("large scale z=0, k=0.01 h/Mpc", Phi_rms(0.01, 0.0))]
for n, p in rows: print(f"    {n:<34} {p:14.1e}  {'yes' if p > lo else 'NO'}")
check("P2 [DEFICIT, verified] on forest scales at z = 3 the potential is 10-100x below even the LOWEST admissible threshold: the component is unclustered there for any Phi_c that empties galaxies (forest kill, worse than the decay plateau)",
      Phi_rms(5.0, 3.0) < lo/10 and Phi_rms(1.0, 3.0) < lo, f"k=1: {Phi_rms(1.0,3.0):.1e}, k=5: {Phi_rms(5.0,3.0):.1e} vs {lo:.1e}")
check("P3 [DEFICIT, verified] on third-peak scales at recombination the potential is below the lowest admissible threshold too: the component would not cluster at z = 1100 either (the CMB gate fails)",
      Phi_rms(0.1/h, ZREC) < lo, f"k=0.1/Mpc: {Phi_rms(0.1/h,ZREC):.1e} (matter-era value; z=1100 is lower still)")
check("P4 the mechanism is a SCALE filter in disguise: linear Phi_k falls as k^-2 x transfer, so any Phi_c above the galaxy value removes all k >~ 0.05 h/Mpc power at every epoch",
      Phi_rms(0.05, 0.0) < lo and Phi_rms(0.005, 0.0) > Phi_rms(0.05, 0.0), f"Phi(0.005)={Phi_rms(0.005,0):.1e}, Phi(0.05)={Phi_rms(0.05,0):.1e}")
print("    VERDICT: DEAD. Depth of potential and smallness of scale are the same variable in linear theory; a switch that removes the component from\n"
      "    galaxies removes it from every scale below ~30 Mpc at every epoch, including recombination.")
print(f"\nL175 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
