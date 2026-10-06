"""cm14: satellite weak-lensing masses vs the framework's readings (inputs PROVISIONAL: WebSearch summaries of Sifon+2018 MNRAS 478, 1244 / Sifon+2015 /
Dvornik+2020 -- satellites with log<M*> ~ 10.5 [h^-2 Msun] have log M_sub ~ 11.7-12.2 [h^-1 Msun], independent of group-centric distance).
h = 0.7: M* = 10^10.5/h^2, M_sub = 10^(11.7..12.2)/h Msun. Baryons M_b = 1.2 M* (cold gas allowance, satellites gas-poor). Lensing masses are within a
truncation radius r_t; we bracket r_t = 30-150 kpc (fitted subhalo truncation radii are tens of kpc to ~100 kpc; stated).
Readings (declared before the run), each M_lens(<r_t) = baryons + phantom + retained cold (0.13 x 5.36 x M_b, cm08's galaxy level):
  A full MOND boost, point mass: phantom = (nu(y) - 1) M_b, y = G M_b / (r_t^2 a0);
  B boost reduced by the host's external field: nu evaluated at (g_N + g_ext)/a0 (1-D approximation), g_ext = 0.05-0.2 a0 (group host at 0.3-1 Mpc);
  C candidate B's hierarchical ownership: a satellite bound inside a host owns NO phantom -> M = M_b (1 + 0.70).
Verdict per reading: CONSISTENT if its [min, max] over the r_t / g_ext brackets overlaps the measured [10^11.7, 10^12.2]/h; else EXCLUDED (factor reported).
Run: python3 cm14_satellite_lensing.py | MUTATE=1 sets a0 -> 0 for A (pure Newton; A must then be excluded, check A fails)
"""
import os, sys, math, numpy as np
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
h = 0.7; G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19; a0 = 9.3603e-11
Ms = 10**10.5 / h**2; Mb = 1.2 * Ms; ret = 0.13 * (0.1200 / 0.02237) * Mb
lo, hi = 10**11.7 / h, 10**12.2 / h
def nu(y): return math.sqrt(1 + 1 / y)
print(f"   M* = {Ms:.2e}, M_b = {Mb:.2e}, retained cold = {ret:.2e}; measured M_sub = {lo:.2e} .. {hi:.2e} Msun (ratio to M*: {lo/Ms:.0f}-{hi/Ms:.0f})")
def A(rt):
    if MUTATE: return Mb + ret
    y = G * Mb * Msun / (rt * kpc)**2 / a0; return nu(y) * Mb + ret
def B(rt, ge):
    y = G * Mb * Msun / (rt * kpc)**2 / a0; return nu(y + ge) * Mb + ret
C = Mb + ret
rts = [30, 50, 100, 150]; ges = [0.05, 0.1, 0.2]
Av = [A(r) for r in rts]; Bv = [B(r, g) for r in rts for g in ges]
for r in rts: print(f"   r_t {r:3d} kpc: A {A(r):.2e}   B(g_ext 0.05/0.1/0.2 a0) " + " / ".join(f"{B(r, g):.2e}" for g in ges))
print(f"   C (no phantom, ownership) {C:.2e}")
def verdict(name, vmin, vmax):
    ok = vmax >= lo and vmin <= hi
    fac = lo / vmax if vmax < lo else (vmin / hi if vmin > hi else 1.0)
    print(f"   {name}: [{vmin:.2e}, {vmax:.2e}] -> {'CONSISTENT' if ok else f'EXCLUDED (factor {fac:.1f})'}"); return ok
okA = verdict("A full MOND boost", min(Av), max(Av)); okB = verdict("B boost with host EFE", min(Bv), max(Bv)); okC = verdict("C ownership (no phantom)", C, C)
check("A the full-boost reading reaches the measured satellite masses (MUTATE a0 -> 0 must fail)", okA)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
