#!/usr/bin/env python3
"""P01 -- E[int r^6 ds] CLOSED-FORM HUNT (door: M05's open 0.212857, uncertified).
Measure EXACTLY as M05_geometric_anchors.first_flight_moments: r_birth uniform
in the unit ball, mu isotropic, chord = -R mu + sqrt(1 - R^2 + R^2 mu^2),
I3 = int_0^chord (R^2 + 2 R mu s + s^2)^3 ds.
Pre-registered kills in PWAVE_BRIEF.md (K1-K3), written before this run."""
import json, math, os, sys
import numpy as np
from mpmath import mp, mpf, quad, sqrt as msqrt

mp.dps = 40
BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

def chord(R, mu): return -R*mu + msqrt(1 - R**2 + R**2*mu**2)
def moment(g):
    # split the mu integral at 0: chord has a kink at mu=0 when R=1 (sqrt|R^2mu^2+..|)
    inner = lambda R: quad(lambda mu: 0.5*g(R, mu), [-1, 0, 1])
    return 3*quad(lambda R: R**2 * inner(R), [0, 1])
ch = moment(lambda R, mu: chord(R, mu))
I1 = moment(lambda R, mu: R**2*chord(R,mu) + R*mu*chord(R,mu)**2 + chord(R,mu)**3/3)
I2 = moment(lambda R, mu: (R**4*chord(R,mu) + 2*R**3*mu*chord(R,mu)**2
        + (2*R**2*mu**2 + R**2)*chord(R,mu)**3/3
        + R*mu*chord(R,mu)**4/2 + chord(R,mu)**5/5))
I3 = moment(lambda R, mu: (R**6*chord(R,mu) + 3*R**5*mu*chord(R,mu)**2
        + R**4*chord(R,mu)**3 + 4*R**4*mu**2*chord(R,mu)**3
        + 3*R**3*mu*chord(R,mu)**4 + (3*R**2/5)*chord(R,mu)**5
        + 2*R**3*mu**3*chord(R,mu)**4 + (12*R**2*mu**2*chord(R,mu)**5)/5
        + R*mu*chord(R,mu)**6 + chord(R,mu)**7/7))
gate = (abs(ch - mpf(3)/4) < mpf('1e-12') and abs(I1 - mpf(5)/12) < mpf('1e-12')
        and abs(I2 - mpf(1)/4) < mpf('1e-12'))
check("G1 mpmath route reproduces 3/4, 5/12, 1/4 at 1e-12", gate,
      f"ch={mp.nstr(ch,14)} I1={mp.nstr(I1,14)} I2={mp.nstr(I2,14)}")

# route 2: per-R exact mu->t change of variables. t = chord is monotone in mu on
# [-1,1]; mu(t) = (1 - R^2 - t^2)/(2 R t); t in [1-R, 1+R];
# |dt/dmu| = R t/(t + R mu) with t + R mu = (1 - R^2 + t^2)/2
#   => joint density p(R,t) = 3R^2 * (1/2) * (1 - R^2 + t^2)/(2 R t) = (3R/4t)(1 - R^2 + t^2)
def muof(R, t): return (1 - R**2 - t**2)/(2*R*t)
def moment_route2(g_of_Rt):
    inner = lambda R: quad(lambda t: (3*R/4)*((t**2 + 1 - R**2)/t**2) * g_of_Rt(R, t),
                           [1 - R, (1 - R + 1 + R)/2, 1 + R])
    return quad(lambda R: inner(R), [0, 0.5, 1])
ch_b = moment_route2(lambda R, t: t)
I1_b = moment_route2(lambda R, t: R**2*t + R*muof(R,t)*t**2 + t**3/3)
I2_b = moment_route2(lambda R, t: R**4*t + 2*R**3*muof(R,t)*t**2
        + (2*R**2*muof(R,t)**2 + R**2)*t**3/3 + R*muof(R,t)*t**4/2 + t**5/5)
I3_b = moment_route2(lambda R, t: (R**6*t + 3*R**5*muof(R,t)*t**2 + R**4*t**3
        + 4*R**4*muof(R,t)**2*t**3 + 3*R**3*muof(R,t)*t**4 + (3*R**2/5)*t**5
        + 2*R**3*muof(R,t)**3*t**4 + (12*R**2*muof(R,t)**2/5)*t**5
        + R*muof(R,t)*t**6 + t**7/7))
check("G2 route 2 (exact mu->t change of variables) reproduces 3/4, 5/12, 1/4, I3",
      abs(ch_b - mpf(3)/4) < mpf('1e-12') and abs(I1_b - mpf(5)/12) < mpf('1e-12')
      and abs(I2_b - mpf(1)/4) < mpf('1e-12') and abs(I3_b - I3) < mpf('1e-20'),
      f"route2: ch={mp.nstr(ch_b,16)} I1={mp.nstr(I1_b,16)} I2={mp.nstr(I2_b,16)} "
      f"I3={mp.nstr(I3_b,18)}; diff vs route1 = {mp.nstr(I3_b - I3, 4)}")

# rational reconstruction: continued-fraction convergents of I3
def convergents(x, qmax):
    xx = mp.mpf(x); p2, p1, q2, q1 = 0, 1, 1, 0
    for _ in range(60):
        a = int(mp.floor(xx))
        pp = a*p1 + p2; qq = a*q1 + q2
        p2, p1 = p1, pp; q2, q1 = q1, qq
        if qq == 0 or qq > qmax: break
        yield pp, qq
        fr = xx - a
        if abs(fr) < mpf('1e-30'): break
        xx = 1/fr
best = None; near = []
for p, q in convergents(mpf(I3), 10**4):
    err = abs(mpf(p)/q - I3)
    near.append((p, q, float(err)))
    if err < mpf('1e-12'):
        best = (p, q, float(err)); break
near = sorted(near, key=lambda t: t[2])[:5]

# (d) MC confirmation 1e8 samples, seeded + jackknife SE (20 blocks)
rng = np.random.default_rng(20260924)
def block_mean(n):
    R = rng.random(n)**(1/3); MU = rng.uniform(-1, 1, n)
    cord = -R*MU + np.sqrt(np.maximum(0.0, 1.0 - R**2*(1.0 - MU**2)))
    return float(np.mean(R**6*cord + 3*R**5*MU*cord**2 + R**4*cord**3
        + 4*R**4*MU**2*cord**3 + 3*R**3*MU*cord**4 + 0.6*R**2*cord**5
        + 2*R**3*MU**3*cord**4 + 2.4*R**2*MU**2*cord**5 + R*MU*cord**6 + cord**7/7))
blocks = 20; per = 5*10**6
accs = np.array([block_mean(per) for _ in range(blocks)])
mc = float(accs.mean())
jk = np.array([(accs.sum() - a)/(blocks - 1) for a in accs])
se_mc = float(math.sqrt((blocks - 1)/blocks * np.sum((jk - jk.mean())**2)))
check("G3 MC (1e8 total, jackknife SE) agrees with the 40-digit value at 4 SE",
      abs(mc - float(I3)) < 4*se_mc,
      f"MC={mc:.9f} +/- {se_mc:.2e} vs exact {mp.nstr(I3,12)} (z={abs(mc-float(I3))/se_mc:.2f})")

claim = best is not None and gate and checks[-1]["pass"]
res = {
 "lane": "P01_r6_moment", "date": "2026-09-24",
 "measure": "M05 first-flight measure (r uniform in ball, mu isotropic)",
 "E_int_r6_40digit": mp.nstr(I3, 20),
 "E_int_r6_float": float(I3),
 "M05_registered": 0.212857,
 "route2_value": mp.nstr(I3_b, 20),
 "convergents_top5": near,
 "closed_form_claim": None if best is None else {"p_over_q": f"{best[0]}/{best[1]}", "abs_err": best[2]},
 "mc": {"value": mc, "jackknife_se": se_mc, "N": blocks*per, "seed": 20260924},
 "checks": checks,
 "verdict": (f"CLOSED FORM CLAIMED: E[int r^6 ds] = {best[0]}/{best[1]} (err {best[2]:.2e}; "
             "pending Lean certification)" if claim else
             f"OPEN: no rational p/q (q<=1e4) within 1e-12 of {mp.nstr(I3,12)}; "
             "top convergents published; value stays M05-uncertified"),
 "summary": f"{sum(1 for c in checks if c['pass'])}/{len(checks)} checks PASS",
 "exit_ok": gate and bool(checks[-1]["pass"]),
}
with open(os.path.join(BASE, "P01_results.json"), "w") as f: json.dump(res, f, indent=1)
with open(os.path.join(BASE, "P01.out"), "w") as f:
    f.write(f"P01 E[int r^6 ds]: {res['summary']}\n{res['verdict']}\n")
    for c in checks: f.write(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}  {c['detail']}\n")
print(open(os.path.join(BASE, "P01.out")).read())
sys.exit(0 if res["exit_ok"] else 1)
