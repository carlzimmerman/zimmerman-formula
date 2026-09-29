#!/usr/bin/env python3
"""occ03_refined_classification.py -- separate REAL exponential instability from polynomial sourcing and from
frozen-coefficient artefacts, for the occ02 finite-k system (imports its matrices; changes nothing in them).

occ02 flagged (a) frozen growing modes at x/H^2 as small as 1e-4, where the frozen approximation drops the
time-dependence of x = k^2/a^2 that the exact system needs (P+Bdot cancels at leading order there), and (b)
'EXPONENTIAL' labels from a 0.15 slope threshold that a t^1.3 power law also crosses over a short window.
Here:
  R1  frozen test only where it is valid: x/H^2 >= 10; growth measured as Re(lambda)/sqrt(x) (per unit frequency)
      and as Re(lambda)/H, both reported.
  R2  exact evolution, LONG run (T = 24 e-folds-ish), with a two-window classifier: exponential iff the log-slope in
      the last window is >= 0.8 x the log-slope in the middle window AND above 0.1/H; a power law's slope falls ~ 1/t.
  R3  the same classifier on the tachyonic control (must be EXPONENTIAL) and on a plain t^2 signal (must be POLY).
"""
import math
import sys
import numpy as np
import occ02_finite_k_matrix as o

ok = []
def check(c, m):
    ok.append(bool(c)); print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(t): print("\n" + "=" * 100 + f"\n  {t}\n" + "=" * 100)


def classify2(tt, ser, thr=0.10):
    T = tt[-1]
    i1, i2 = np.searchsorted(tt, T / 3), np.searchsorted(tt, 2 * T / 3)
    s_mid = (math.log(ser[i2]) - math.log(ser[i1])) / (tt[i2] - tt[i1])
    s_late = (math.log(ser[-1]) - math.log(ser[i2])) / (tt[-1] - tt[i2])
    if s_late > thr and s_late >= 0.8 * s_mid:
        return s_mid, s_late, 'EXPONENTIAL'
    if ser[-1] > 3 * ser[i1] and s_late > 0:
        return s_mid, s_late, 'polynomial'
    return s_mid, s_late, 'bounded'


banner("R3  classifier controls with a known answer")
tt = np.linspace(0.0, 24.0, 25)
for nm, f, want in (("t^2 signal", lambda t: 1 + t**2, 'polynomial'), ("exp(0.3 t)", lambda t: np.exp(0.3 * t), 'EXPONENTIAL'),
                    ("decaying oscillator", lambda t: np.exp(-0.2 * t) * (1.3 + np.cos(t)), 'bounded')):
    sm, sl, cl = classify2(tt, f(tt))
    check(cl == want, f"R3 {nm:<20} -> {cl}  (mid slope {sm:.3f}, late slope {sl:.3f}; wanted {want})")

banner("R1  frozen-coefficient test restricted to x/H^2 >= 10 (where it is valid) -- 300 random sets x 4 snapshots")
rng = np.random.default_rng(20260928)
worst = (-1e9, None); n_pts = 0; n_bad = 0
worst_rel = -1e9
for _ in range(300):
    mm = o.random_model(rng); yy = o.random_state(rng, mm)
    try:
        states, _ = o.snapshot_states(mm, yy, np.array([0.0, 2.0, 5.0, 10.0]))
    except Exception:
        continue
    for y in states:
        H = mm.H_of(y); a = math.exp(y[10])
        for xr in np.logspace(1, 3, 15):
            lam, gmin, _, d = o.frozen_growth(mm, y, math.sqrt(xr) * H * a)
            n_pts += 1
            n_bad += lam > 1e-3
            rel = lam * H / math.sqrt(d['x'])
            worst_rel = max(worst_rel, rel)
            if lam > worst[0]:
                worst = (lam, (mm.alpha, mm.c2, mm.ell, mm.xi, math.sqrt(mm.mu2), math.sqrt(mm.mH2), math.sqrt(mm.mL2), mm.gamma, xr))
print(f"  {n_pts} sub-horizon points; frozen Re(lambda)/H > 1e-3 at {n_bad}; max Re(lambda)/H = {worst[0]:+.4f}; max Re(lambda)/sqrt(x) = {worst_rel:+.4f}")
if n_bad:
    print(f"  worst (alpha,c2,ell,xi,mu,mH,mL,gamma,x/H2) = {tuple(round(v,3) for v in worst[1])}")
print(f"  R1 verdict: {'NO frozen growing mode at any sub-horizon point' if n_bad == 0 else 'frozen growing modes EXIST at sub-horizon x -- see the worst case'}")

banner("R2  exact time-dependent evolution, long run, two-window classifier")
print(f"  {'case':<28}{'k/(aH)_0':>9}{'sigma(T)':>12}{'mid slope':>10}{'late slope':>11}   class")
cases = []
phi0 = np.array([0.35, -0.2, 0.15, 0.25, 0.4]); v0 = np.array([0.30, 0.10, -0.20, 0.15, 0.05])
cases.append(("baseline mu=0.6", o.Model(), None))
cases.append(("heavy s, mu=2.5", o.Model(mu=2.5), None))
rng2 = np.random.default_rng(7)
for j in range(3):
    mm = o.random_model(rng2); yy = o.random_state(rng2, mm)
    cases.append((f"random #{j} mu={math.sqrt(mm.mu2):.2f}", mm, yy))
n_exp = 0; n_run = 0
for lab, mm, yy in cases:
    if yy is None:
        yy = o.initial_background(mm, phi0, v0)
    Hh = mm.H_of(yy)
    for kr in (0.1, 1.0, 5.0):
        tt, ser, st = o.timed_evolution(mm, yy, kr * Hh, 24.0, limit=120, npts=25)
        if st == 'TIMEOUT':
            print(f"  {lab:<28}{kr:>9.2f}   TIMEOUT (stiff; not classified)"); n_run += 1; continue
        sm, sl, cl = classify2(tt, ser)
        n_run += 1; n_exp += cl == 'EXPONENTIAL'
        print(f"  {lab:<28}{kr:>9.2f}{ser[-1]:>12.3e}{sm:>10.3f}{sl:>11.3f}   {cl}" + ("" if st == 0 else f"  [solver status {st}]"))
print(f"\n  exponential growth in {n_exp} of {n_run} long runs")

banner("R3b classifier on the tachyonic-gradient mutation in the exact evolution")
mmut = o.Model(mut='gradient_sign')
tt, ser, st = o.full_evolution(mmut, o.initial_background(mmut, phi0, v0), 2.0 * mmut.H_of(o.initial_background(mmut, phi0, v0)), 4.0, npts=25)
sm, sl, cl = classify2(tt, ser)
check(cl == 'EXPONENTIAL', f"R3b tachyonic mutation classified {cl} (mid {sm:.2f}, late {sl:.2f})")

banner("RESULT")
print(f"  {sum(ok)}/{len(ok)} control checks held; findings are the R1 and R2 tables above.")
sys.exit(0 if all(ok) else 1)
