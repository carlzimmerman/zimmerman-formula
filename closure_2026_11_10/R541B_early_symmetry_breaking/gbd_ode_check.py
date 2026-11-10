"""R541B family (d), step 3 of the frozen plan: full-ODE re-run (stiff regime included) of the subset that the Q ~ 1
quadrature cannot settle. Subset chosen AFTER reading gbd_zero_constant.out (stated in RESULT.md):
 part P: p = 3/2, q = 1 (A = beta rho_DE c^2 y^(3/2), T = 1/(mu_K c)). In the radiation era R is then independent of
         mu_K: V0 a_s^3 = beta rho_DE sqrt(G rho_DE)^(-3/2) (2 sqrt(Omega_r) H0)^(3/2) (hand), so these forms carry no
         free number at all; the ODE gives R at mu_K = Jeans and BBN lines, every beta, both shapes, both footings.
 part S: p = 2, q = 1 (A = beta mu_K^2 c^4 / G, T = 1/(mu_K c)): K V0 / mu^2 = 4 pi beta, stiff regime; the quadrature
         is not valid. R(mu_K) on a grid >= the Jeans line, every beta, exponential shape, canonical.
Run: python3 gbd_ode_check.py P   (or S)."""
import os, sys, math, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from r541b_core import cosmo, m_of_mu, Pot, run, t_rad, OMEGA_R

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G, c = 6.674e-11, 2.99792458e8
H0SI = 67.4e3 / 3.0856775814913673e22
rhoc0 = 3 * H0SI**2 / (8 * math.pi * G)
BETA = {"1/(8pi)": 1 / (8 * math.pi), "1/(4pi)": 1 / (4 * math.pi), "1/4": 0.25, "1/2": 0.5, "1": 1.0, "2": 2.0,
        "4": 4.0, "4pi": 4 * math.pi, "8pi": 8 * math.pi}
WIDTH = 0.065


def setup(foot):
    rhoDE = (2 * A0[foot] / c)**2 / G
    return rhoDE / rhoc0, math.sqrt(G * rhoDE) / H0SI


def R_run(foot, p, q, b, mu, shape):
    Om, sGr = setup(foot)
    cp = cosmo(foot); m = m_of_mu(mu); y = m / sGr
    V0 = b * Om * y**p; T = y**(-q) / sGr
    a_s = math.sqrt(2 * math.sqrt(cp["Or"]) * T)          # radiation-era a at t = T
    if shape == "exp":
        pot = Pot("exp", V0, T); seg = [(math.log(a_s) - 6, math.log(a_s) + 6, 0.02)]
    else:
        pot = Pot("tanh", V0, T, D=1e-3 * T); seg = [(math.log(a_s) - 0.05, math.log(a_s) + 0.05, 2e-5)]
    s = run(pot, cp, m, a_ini=min(1e-3 * a_s, 1e-12), segs=seg)
    R = s.Cfin() / cp["Ob"]
    z99 = s.z_of_frac(0.99)
    qm = max(s.state(a)["x"] for a in np.geomspace(1e-2 * a_s, 1, 150))
    return R, z99, qm, 1 / a_s - 1


part = sys.argv[1]
if part == "P":
    print("part P: p = 3/2, q = 1. Hand plateau (step): R = beta rho_DE/rho_c0 sGr^-1.5 (2 sqrt(Omega_r))^1.5 / Omega_b; "
          "exponential x Gamma(5/2)")
    for foot in ("canonical", "alt"):
        Om, sGr = setup(foot); cp = cosmo(foot)
        hand = Om * sGr**-1.5 * (2 * math.sqrt(cp["Or"]))**1.5 / cp["Ob"]
        print(f"\n footing {foot}: hand plateau R / beta = {hand:.4f} (step), {hand * math.gamma(2.5):.4f} (exp); "
              f"beta that would give R = {cp['R']}: {cp['R'] / hand:.3f} (step), {cp['R'] / hand / math.gamma(2.5):.3f} (exp)")
        print(" beta | shape | mu_K | z_s | R (ODE) | |R - target| / 0.065 | z99 | max Q-1")
        for bl, b in BETA.items():
            for shape in ("step", "exp"):
                for mu in (2.512e4, 8.89e6):
                    R, z99, qm, zs = R_run(foot, 1.5, 1, b, mu, shape)
                    print(f" {bl} | {shape} | {mu:.3e} | {zs:.3e} | {R:.4f} | {abs(R - cp['R']) / WIDTH:.1f} | "
                          f"{z99:.3e} | {qm:.2e}")
if part == "S":
    print("part S: p = 2, q = 1, exponential, canonical. R(mu_K) with the full ODE (stiff regime included).")
    print(" beta | mu_K | z_s | R (ODE) | z99 | max Q-1")
    for bl, b in BETA.items():
        for mu in (2.512e4, 1e5, 1e6, 8.89e6, 1e8, 1e10):
            try:
                R, z99, qm, zs = R_run("canonical", 2, 1, b, mu, "exp")
                print(f" {bl} | {mu:.3e} | {zs:.3e} | {R:.4e} | {z99:.3e} | {qm:.2e}")
            except Exception as e:
                print(f" {bl} | {mu:.3e} | ODE failed: {e}")
