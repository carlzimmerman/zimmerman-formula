#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A3_cold_coupling -- G1-C (the cold-component budget test), G3 reaction, control C7 (twin-matter sum rule as an OUTCOME of my reduction).
Cold component at CFG44's target profile M_c(<r) (cold_mass 'encl'; closed form M(sqrt(1+x^2)-1) for the P2 point mass) coupled
  (c-g)   like the baryons (sources the same field equations, Gauss on g-coupled mass)
  (c-gh)  to the second metric (twin-type: a source in the g-hat equations)
  13c: (c-Einstein) kernel-blind, feels/sources only the Einstein-frame Newtonian potential; (c-chi) conformally like the baryons.
MUTATE M5: swap (c-g) -> (c-gh): the G1-C sign flips.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A3_cold_coupling")
MUT = R.mutate
P = R.P
bite = []
Bc = C.B
masses = np.geomspace(1e9, 1e12, 7)
NU = {"P2": C.nu_p2, "nu_mono": C.nu_mono}
DES = {kn: C.Design(NU[kn], beta=1.0, gamma=1.0, sigma=+1) for kn in NU}


def profile(name, M):
    return Bc.point_mass(M) if name == "point" else Bc.exp_sphere(M, 2.0)


def cold_profile(prof, rr):
    rg, w, u, uN = Bc.cold_mass(prof, "encl", a0=C.A0_KPC)
    return np.interp(rr, rg, w), np.interp(rr, rg, u)


# ------------------------------------------------------------------------------------------------ hand check (point mass)
R.banner("Hand check (frozen 1.6): (c-g) at the target profile, point mass: g_tot/g_target = nu(g_target/a0)")
xs = np.array([0.1, 0.4, 0.483, 0.5, 1.0, 3.0, 30.0])
d = DES["P2"]
rows = []
for x in xs:
    yb = 1.0 / x ** 2
    gt = math.sqrt(yb * yb + yb)
    yc = gt - yb
    f_ = C.forward(d.mfun, 1.0, 1.0, +1, yb + yc)
    ratio = f_["Phi"] / gt
    rows.append((x, ratio, float(C.nu_p2(gt))))
    P(f"  x = {x:7.3f}: g_tot/g_target = {ratio:.4f}   nu(g_target) = {float(C.nu_p2(gt)):.4f}")
R.check("(c-g) hand identity g_tot/g_target = nu(g_target/a0) holds numerically for the designed BIMOND law (point mass, cold at the target profile)", max(abs(a - b) for _, a, b in rows) < 5e-3, f"max diff {max(abs(a-b) for _,a,b in rows):.2e}")
xc = None
from scipy.optimize import brentq
xc = brentq(lambda x: float(C.nu_p2(math.sqrt(x ** -4 + x ** -2))) - 1.10, 0.2, 2.0)
P(f"  the 10% line g_tot/g_target = 1.10 is crossed at x = {xc:.3f} (frozen hand: 0.48)")

# ------------------------------------------------------------------------------------------------ G1-C
R.banner("G1-C: total force on the baryons with the cold component at the target profile; 7 masses x 2 profiles x P2/nu_mono; x in [0.1, 30]")
res = {}
XS = np.geomspace(0.1, 30.0, 41)
for kn in ("P2", "nu_mono"):
    d = DES[kn]
    for pname in ("point", "exp"):
        wcg, wcgh, wchi, wein = 0.0, 0.0, 0.0, 0.0
        wsign = 0
        for M in masses:
            prof = profile(pname, M)
            rM = math.sqrt(C.G * M / C.A0_KPC)
            rr = XS * rM
            w, u = cold_profile(prof, rr)
            gNb = prof.gN(rr)
            yb = gNb / C.A0_KPC
            yc = (w / rr ** 2) / C.A0_KPC
            gC = u / rr ** 2 / C.A0_KPC                                    # CFG44 target for the total (units a0)
            gL = yb * C.KERNELS[kn](yb)                                    # law target nu(g_N) g_N
            cg, cgh = [], []
            for i in range(len(rr)):
                f1 = C.forward(d.mfun, 1.0, 1.0, +1, float(yb[i] + yc[i]))
                f2 = C.forward(d.mfun, 1.0, 1.0, +1, float(yb[i]), ghN=float(yc[i]))
                cg.append(f1["Phi"] / gC[i] - 1 if f1["ok"] else np.nan)
                cgh.append(f2["Phi"] / gC[i] - 1 if f2["ok"] else np.nan)
            cg, cgh = np.array(cg), np.array(cgh)
            wcg = max(wcg, float(np.nanmax(np.abs(cg))))
            wcgh = max(wcgh, float(np.nanmax(np.abs(cgh))))
            wsign = min(wsign, float(np.nanmin(cgh)))
            # 13c: (c-chi): total source in chi = P2 applied to total; (c-Einstein): Newtonian pull of all mass + chi from baryons
            h_b = C.KERNELS[kn](yb) * yb - yb                                # |grad chi| sourced by the baryons alone (designed: nu g_N - g_N)
            g_cchi = C.KERNELS[kn](yb + yc) * (yb + yc)
            g_cein = (yb + yc) + h_b
            wchi = max(wchi, float(np.max(np.abs(g_cchi / gC - 1))))
            wein = max(wein, float(np.max(np.abs(g_cein / gC - 1))))
        res[(kn, pname)] = dict(cg=wcg, cgh=wcgh, cgh_min=wsign, chi=wchi, ein=wein)
        P(f"  {kn:8s} {pname:5s}: max|g_tot/g_C - 1|:  (c-g) {wcg:.3f} | (c-gh) {wcgh:.3f} (min of g_tot/g_C - 1 = {wsign:.2f}) | 13c (c-chi) {wchi:.3f} | 13c (c-Einstein) {wein:.3f}")
R.num("G1C", {"|".join(k): v for k, v in res.items()})
allcg = min(v["cg"] for v in res.values()); allcgh = min(v["cgh"] for v in res.values())
allchi = min(v["chi"] for v in res.values()); allein = min(v["ein"] for v in res.values())
R.check("G1-C (13a/13b, cold coupled to g): FAILS the 10% line for every kernel and profile (double counting by nu(g_target))", allcg > 0.10, f"smallest max-deviation over the cases = {allcg:.3f}", kind="result")
R.check("G1-C (13a/13b, cold coupled to g-hat): FAILS the 10% line for every kernel and profile", allcgh > 0.10, f"smallest = {allcgh:.3f}; most negative g_tot/g_C - 1 = {min(v['cgh_min'] for v in res.values()):.2f}", kind="result")
R.check("G1-C (13c, cold conformal like baryons): FAILS the 10% line", allchi > 0.10, f"smallest = {allchi:.3f}", kind="result")
R.check("G1-C (13c, cold in the Einstein frame, kernel-blind): FAILS the 10% line", allein > 0.10, f"smallest = {allein:.3f}", kind="result")
R.verdict("G1-C 13a/13b (c-g)", "FAIL" if allcg > 0.10 else "PASS", f"max deviation {min(v['cg'] for v in res.values()):.2f}..{max(v['cg'] for v in res.values()):.2f} across cases")
R.verdict("G1-C 13a/13b (c-gh)", "FAIL" if allcgh > 0.10 else "PASS", "twin-type coupling reduces the force and can reverse its sign")
R.verdict("G1-C 13c", "FAIL" if min(allchi, allein) > 0.10 else "PASS", "both couplings")

# ------------------------------------------------------------------------------------------------ C7 twin sum rule
R.banner("C7: my reduction with a test mass in g-hat: F_TM = dPhi'/d(g-hat_N) at fixed baryon source, against the record's theorem F_TM = 1 - nu(y)")
d = DES["P2"]
rows7 = []
for yb in (0.01, 0.1, 1.0, 10.0, 100.0):
    eps_ = 1e-6 * yb
    f0 = C.forward(d.mfun, 1.0, 1.0, +1, yb)
    f1 = C.forward(d.mfun, 1.0, 1.0, +1, yb, ghN=eps_)
    FTM = (f1["Phi"] - f0["Phi"]) / eps_
    Fb = f0["Phi"] / yb
    rows7.append((yb, FTM, 1 - float(C.nu_p2(yb)), Fb, float(C.nu_p2(yb))))
    P(f"  y_b = {yb:7.2f}: F_TM (mine) = {FTM:8.4f}   record 1-nu = {1-float(C.nu_p2(yb)):8.4f}   F_b = {Fb:.4f} (nu = {float(C.nu_p2(yb)):.4f})   F_b+F_TM = {Fb+FTM:.4f}")
ok7 = all(abs(a - b) < 0.02 * max(1, abs(b)) for _, a, b, _, _ in rows7)
R.check("C7b (result, my reduction's FULL nonlinear response): F_TM = 1 - nu(y) does NOT hold once M'(Q) is allowed to respond to the twin source: |F_TM| is smaller than |1 - nu| (record's theorem is a fixed-Q statement)", not ok7,
        "; ".join(f"y={y:g}: {a:.3f} vs {b:.3f}" for y, a, b, _, _ in rows7), kind="result")
# C7a: fixed-m linear response reproduces the record's theorem exactly (kernel-blind)
rows7a = []
for yb in (0.01, 0.1, 1.0, 10.0, 100.0):
    f0 = C.forward(d.mfun, 1.0, 1.0, +1, yb)
    mfix = (lambda Q, mm=f0["m"]: mm * np.ones_like(np.asarray(Q, float)))
    eps_ = 1e-6 * yb
    f1 = C.forward(mfix, 1.0, 1.0, +1, yb, ghN=eps_)
    f0f = C.forward(mfix, 1.0, 1.0, +1, yb)
    FTMa = (f1["Phi"] - f0f["Phi"]) / eps_
    rows7a.append((yb, FTMa, 1 - float(C.nu_p2(yb))))
    P(f"  fixed-m response y_b = {yb:7.2f}: F_TM = {FTMa:8.4f}   1 - nu = {1-float(C.nu_p2(yb)):8.4f}")
ok7a = all(abs(a - b) < 1e-3 * max(1, abs(b)) for _, a, b in rows7a)
R.check("C7a Route 6 theorem reproduced in my reduction at FIXED interaction argument: dPhi'/d(g-hat_N)|_m = 1 - nu = -(Phi'/g_N - 1) for beta = gamma, kernel-blind (symbolically: -4x(3+8x)/(s beta D gamma...))", ok7a, "agree" if ok7a else "disagree")
R.num("C7a_rows", rows7a)
R.num("C7_rows", rows7)

# ------------------------------------------------------------------------------------------------ G3 reaction
R.banner("G3 reaction: force on the baryons from the cold component beyond the law, over x in [0.3, 30]")
worst_gh = 0.0
for M in (1e9, 1e10, 1e11, 1e12):
    prof = Bc.point_mass(M)
    rM = math.sqrt(C.G * M / C.A0_KPC)
    for x in np.geomspace(0.3, 30, 25):
        yb = 1.0 / x ** 2
        gt = math.sqrt(yb * yb + yb)
        yc = gt - yb
        f0 = C.forward(d.mfun, 1.0, 1.0, +1, yb)["Phi"]
        f2 = C.forward(d.mfun, 1.0, 1.0, +1, yb, ghN=yc)["Phi"]
        worst_gh = max(worst_gh, abs(f2 - f0) / gt)
P(f"  (c-gh): max |g_b(with twin-coupled cold) - g_b(without)| / g_law over x in [0.3,30] (point mass) = {worst_gh:.3f}   (pass line 0.10)")
R.check("G3 reaction (c-gh): reaction <= 0.10 g_law over x in [0.3, 30]", worst_gh <= 0.10, f"{worst_gh:.3f}", kind="result")
R.verdict("G3 reaction (c-g / c-chi / c-Einstein)", "PASS* (by the frozen definition: zero force beyond -grad Phi; the cold pull is the ordinary Newtonian/law pull, whose excess is the G1-C overshoot)", "field-side law acts on baryons directly")
R.verdict("G3 reaction (c-gh)", "FAIL" if worst_gh > 0.10 else "PASS", f"max {worst_gh:.3f}")

# ============================================================================================ MUTATE
if MUT == "M5":
    R.banner("MUTATE M5: swap (c-g) -> (c-gh)")
    x = 3.0
    yb = 1 / x ** 2
    gt = math.sqrt(yb * yb + yb); yc = gt - yb
    cg = C.forward(d.mfun, 1.0, 1.0, +1, yb + yc)["Phi"] / gt - 1
    cgh = C.forward(d.mfun, 1.0, 1.0, +1, yb, ghN=yc)["Phi"] / gt - 1
    P(f"  x=3: (c-g) g_tot/g_target - 1 = {cg:+.3f} (overshoot); (c-gh) = {cgh:+.3f} (undershoot / reversal)")
    bite.append(cg > 0.1 and cgh < 0)
R.finish(bite if MUT else None)
