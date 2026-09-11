#!/usr/bin/env python3
"""L177 -- TIME-DEPENDENT DARK COUPLING (the L176 inference): a cold, non-heated component whose gravitational coupling g(a) falls from 1
(recombination) to g0 = 0.58 today (= X-COP requirement = loose galaxy ceiling). Linear two-cold-fluid growth from z = 100 (CLASS ICs),
Poisson source Ob*db + g(a)*Oc*dd, both fluids fall in the total potential, LCDM background. Lensing sees the coupled mass, the forest
sees the baryons. g(a) = 1 - (1-g0) a^n. No literal-True checks. Sub-horizon linear theory; kernel contribution (L176) not added."""
import numpy as np
from scipy.integrate import solve_ivp
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
h = 0.6736; Ob, Oc = 0.02237/h**2, 0.12/h**2; Om = Ob + Oc; OL = 1 - Om
cl = Class(); cl.set({"h": h, "omega_b": 0.02237, "omega_cdm": 0.12, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0,
                      "YHe": 0.2454, "output": "mPk", "P_k_max_h/Mpc": 10, "z_max_pk": 100}); cl.compute()
sig8 = cl.sigma8(); S8_L = sig8*np.sqrt(Om/0.3); f100 = cl.scale_independent_growth_factor_f(100.0)
E = lambda a: np.sqrt(Om*a**-3 + OL)
def grow(g0, n, a_out):
    """returns (db, dd) at a_out normalised to delta_LCDM(a_out); scale-free sub-horizon growth (k drops out)."""
    g = lambda a: 1 - (1 - g0)*a**n
    def rhs(lna, y):
        a = np.exp(lna); db, vb, dd, vd = y                      # v = d delta / d ln a
        src = 1.5*(Ob*db + g(a)*Oc*dd)*a**-3/E(a)**2               # (3/2) Om_eff(a) delta_eff
        damp = 2 + (-1.5*Om*a**-3/E(a)**2)                          # 2 + dlnH/dlna
        return [vb, src - damp*vb, vd, src - damp*vd]
    a0 = 0.01; y0 = [1.0, f100, 1.0, f100]
    sol = solve_ivp(rhs, [np.log(a0), 0.0], y0, t_eval=np.log(a_out), rtol=1e-8, atol=1e-10)
    ref = solve_ivp(lambda l, y: [y[1], 1.5*Om*np.exp(l)**-3/E(np.exp(l))**2*y[0] - (2 - 1.5*Om*np.exp(l)**-3/E(np.exp(l))**2)*y[1]],
                    [np.log(a0), 0.0], [1.0, f100], t_eval=np.log(a_out), rtol=1e-8, atol=1e-10)
    return sol.y[0]/ref.y[0], sol.y[2]/ref.y[0], g
zs = np.array([3.0, 0.5, 0.0]); a_out = 1/(1 + zs)
print(f"    LCDM: sigma8 = {sig8:.4f}, S8 = {S8_L:.4f}; KiDS-Legacy floor 0.767; forest tolerance ~10% at z = 3; galaxies loose <= 0.582, strict <= 0.105; clusters >= 0.576")
print(f"    {'g0':>5} {'n':>3} {'g(z=3)':>7} {'T2_forest(z=3)':>15} {'T2_lens(z=0.5)':>15} {'T2_lens(z=0)':>13} {'S8':>7}")
res = {}
for g0 in (0.58, 0.40):
    for n in (1, 2, 4):
        db, dd, g = grow(g0, n, a_out)
        T2f = db[0]**2
        T2l = ((Ob*db + g(a_out)*Oc*dd)/Om)**2      # coupled-mass contrast relative to LCDM total-matter contrast
        S8 = S8_L*np.sqrt(T2l[2])
        res[(g0, n)] = (g(a_out[0]), T2f, T2l[1], T2l[2], S8)
        print(f"    {g0:5.2f} {n:3d} {g(a_out[0]):7.3f} {T2f:15.3f} {T2l[1]:15.3f} {T2l[2]:13.3f} {S8:7.3f}")
check("C1 [DEFICIT, verified] no g0 = 0.58 ramp (n = 1, 2, 4) reaches S8 >= 0.767: the coupling drop removes 42% of the lensing mass and slows growth, S8 = 0.48-0.54",
      all(res[(0.58, n)][4] < 0.767 for n in (1, 2, 4)), ", ".join(f"n={n}: S8={res[(0.58,n)][4]:.3f}" for n in (1, 2, 4)))
S8eff = {n: S8_L*np.sqrt(res[(0.58, n)][3] + 0.4) for n in (1, 2, 4)}
check("C2 [DEFICIT, verified -- KNIFE-EDGE] crediting the L176 kernel-boosted baryons at their maximum (+0.4 of the band, a PM number added to a linear one, not self-consistent) gives S8_eff = 0.72-0.76 for n = 1-4: still below 0.767, but the latest ramp is within 0.01 of the floor",
      all(v < 0.767 for v in S8eff.values()) and max(S8eff.values()) > 0.75, ", ".join(f"n={n}: S8_eff={v:.3f}" for n, v in S8eff.items()))
check("C3 the forest side would have passed: the late ramps (n >= 2) keep baryon growth at z = 3 within 1% of LCDM", all(res[(0.58, n)][1] > 0.99 for n in (2, 4)))
print("    galaxies: g0 = 0.58 passes the LOOSE ceiling (0.582) and fails the STRICT one (0.105); clusters: 0.58 >= 0.576 passes.")
print("    LIMITS: linear, sub-horizon, LCDM background unchanged, kernel contribution (L176: +0.2-0.4 of the shear band at z = 0.5 from baryons) NOT added;\n"
      "    lensing counts only the coupled mass; no mechanism for g(a).")
print(f"\nL177 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
