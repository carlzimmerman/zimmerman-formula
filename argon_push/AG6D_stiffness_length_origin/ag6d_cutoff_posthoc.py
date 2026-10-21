#!/usr/bin/env python3
"""AG6D Part C1 POST-HOC diagnostics (NOT in the frozen criteria; reported with no class weight).
  P1  L*_IC refined below the frozen grid floor (1 pc): T(k_Ny) >= 0.9 scan over L* in [1e-3, 1] pc.
  P2  integrator cross-check: DOP853 (frozen) vs Radau at three (k, L*) points.
  P3  sigma(R) suppression weighted by the framework's OWN native linear spectrum (CFG654 cfg654_ics_tables.npz, Plin0,
      read-only): sigma_cut/sigma at R = 8, 1, 0.5 Mpc/h for L* = 24, 56.8 (B8), 100, 1000 pc.
  P4  switch-on epoch: if the stiffness acts on the free medium only for a > a_on, the latest z_on that still leaves
      T(k_Ny) >= 0.9 (L* = 24 pc and 56.8 pc).
Reuses the frozen equations by executing the definitions block of ag6d_cutoff.py (everything before its run section).
"""
import json, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "ag6d_cutoff.py")).read().split('res = {"lane"')[0]
ns = {"__file__": os.path.join(HERE, "ag6d_cutoff.py")}
os.environ["AG6D_MUTATE"] = "0"
exec(src, ns)
T, grow, a_entry, rhs_factory = ns["T"], ns["grow"], ns["a_entry"], ns["rhs_factory"]
h, kNy, a_dec, a_end, fc, fb = ns["h"], ns["kNy"], ns["a_dec"], ns["a_end"], ns["fc"], ns["fb"]
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    out_lines.append(s)


res = {"lane": "AG6D", "part": "C1-posthoc"}
t0 = time.time()
# P1
grid = np.logspace(-3, 0, 31)
Tg = np.array([T(kNy, L) for L in grid])
idx = next((i for i, t in enumerate(Tg) if t < 0.9), None)
if idx is None or idx == 0:
    LIC = None if idx == 0 else 1.0
else:
    LIC = float(np.exp(brentq(lambda x: T(kNy, np.exp(x)) - 0.9, np.log(grid[idx - 1]), np.log(grid[idx]), xtol=1e-4)))
P(f"P1 L*_IC (uncapped, IC d'=1, first crossing of T(k_Ny)=0.9 scanning up from 1e-3 pc): "
  f"{LIC if LIC is None else f'{LIC:.4f}'} pc; floor/L*_IC = {24.0/LIC if LIC else float('nan'):.0f}")
res["P1_L_IC_pc"] = LIC
res["P1_grid"] = {"L_pc": grid.tolist(), "T": Tg.tolist()}


# P2
def grow_method(k, Lpc, method):
    Lmpc = Lpc * 1e-6
    aH = a_entry(k)
    rhs = rhs_factory(k, Lmpc, False)
    xs = [np.log(aH), np.log(a_dec), np.log(a_end)]
    s = [1.0, 1.0, 0.0, 0.0]
    for x0, x1 in zip(xs[:-1], xs[1:]):
        sol = solve_ivp(rhs, (x0, x1), s, method=method, rtol=1e-10, atol=1e-14)
        s = sol.y[:, -1]
    return fc * s[0] + fb * s[2]


P2 = []
for k, L in ((0.94, 24.0), (0.4, 100.0), (10.89, 1.0)):
    a = grow_method(k, L, "DOP853") / grow_method(k, 0.0, "DOP853")
    b = grow_method(k, L, "Radau") / grow_method(k, 0.0, "Radau")
    P2.append({"k": k, "L": L, "T_DOP853": a, "T_Radau": b})
    P(f"P2 k = {k:6.2f}/Mpc, L* = {L:6.1f} pc: T DOP853 {a:.6f}  Radau {b:.6f}  (diff {abs(a-b):.1e})")
res["P2"] = P2

# P3 sigma(R) with the native spectrum
tab = np.load(os.path.join(HERE, "..", "..", "campaign_fresh_gravity", "CFG654_independent_inputs", "cfg654_ics_tables.npz"))
kh_tab, Plin0 = np.array(tab["kh"]), np.array(tab["Plin0"])
P(f"P3 native table: kh {kh_tab.min():.2e}..{kh_tab.max():.2e} h/Mpc, h_table = {float(tab['h']):.4f}")


def W(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3


P3 = {}
kev = np.logspace(np.log10(0.02), np.log10(60.0), 90)  # h/Mpc
for L in (24.0, 56.8, 100.0, 1000.0):
    Tk = []
    for kk in kev:
        kM = kk * h
        Tk.append(T(kM, L) if kM >= 0.05 else 1.0)
    Tk = np.array(Tk)
    Ti = np.interp(np.log(kh_tab), np.log(kev), Tk, left=1.0, right=0.0)
    row = {}
    for R in (8.0, 1.0, 0.5):
        integ = Plin0 * kh_tab**3 * W(kh_tab * R)**2
        s0 = np.trapz(integ, np.log(kh_tab))
        s1 = np.trapz(integ * Ti**2, np.log(kh_tab))
        row[f"R={R}"] = float(np.sqrt(s1 / s0))
    P3[f"{L}"] = row
    P(f"P3 L* = {L:6.1f} pc: sigma_cut/sigma at R = 8 / 1 / 0.5 Mpc/h = {row['R=8.0']:.3f} / {row['R=1.0']:.3f} / "
      f"{row['R=0.5']:.3f}   [{time.time()-t0:.0f} s]")
res["P3"] = P3


# P4 switch-on epoch
def T_on(k, Lpc, a_on):
    Lmpc = Lpc * 1e-6
    aH = a_entry(k)
    base = rhs_factory(k, Lmpc, False)
    free = rhs_factory(k, 0.0, False)

    def rhs(x, s):
        return base(x, s) if np.exp(x) >= a_on else free(x, s)

    pts = sorted(set([np.log(aH), np.log(a_dec), np.log(a_end)] + ([np.log(a_on)] if aH < a_on < a_end else [])))
    s = [1.0, 1.0, 0.0, 0.0]
    for x0, x1 in zip(pts[:-1], pts[1:]):
        sol = solve_ivp(rhs, (x0, x1), s, method="DOP853", rtol=1e-9, atol=1e-13)
        s = sol.y[:, -1]
    return (fc * s[0] + fb * s[2]) / grow(k, 0.0)


P4 = {}
for L in (24.0, 56.8):
    lna = np.linspace(np.log(a_entry(kNy)), np.log(a_end), 60)
    vals = [T_on(kNy, L, np.exp(x)) for x in lna]
    # earliest switch-on that keeps T >= 0.9 for every later switch-on on the grid
    ok = [v >= 0.9 for v in vals]
    j = next((i for i in range(len(ok)) if all(ok[i:])), None)
    z_on = float(1 / np.exp(lna[j]) - 1) if j is not None else None
    P4[f"{L}"] = {"z_on_max": z_on}
    P(f"P4 L* = {L:5.1f} pc: the stiffness must act on the free medium only after z ~ {z_on:.0f} "
      f"(T(k_Ny) >= 0.9 for every later switch-on)   [{time.time()-t0:.0f} s]")
res["P4"] = P4
with open(os.path.join(HERE, "ag6d_cutoff_posthoc_results.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, "ag6d_cutoff_posthoc.out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
