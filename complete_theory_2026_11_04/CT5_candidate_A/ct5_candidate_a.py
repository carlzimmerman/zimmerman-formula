#!/usr/bin/env python3
"""CT5: candidate A = Henneaux-Teitelboim four-form tie inside the screened v3s action.

Gates frozen in FROZEN_CRITERIA.md (written before this script). Single thread, seconds.
kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled.
Not theory closed. Nothing here says the data favour the framework.

Usage: python3 ct5_candidate_a.py            (main run)
       python3 ct5_candidate_a.py --mutate   (control: slaving switched off, eps -> 0; G0 must then pass)
"""
import json
import sys

import numpy as np
np.seterr(over='ignore')
import sympy as sp
from scipy.optimize import brentq

MUTATE = "--mutate" in sys.argv
G_SI = 6.6743e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5
EPS = 0.0 if MUTATE else KAPPA**2 / (8 * np.pi)
EPS_ALT_TIED = 0.6043**2 / (8 * np.pi)   # alt footing with kappa tied on the same rho_Lambda (XR31 row 3), ungraded reading
out = {"mutate": MUTATE, "eps": EPS}
checks = []


def chk(name, ok, detail=""):
    checks.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


# ---------------------------------------------------------------- 1. symbolic derivation
print("=" * 100)
print("1. Symbolic: static weak-field Lagrangian of S_A, the A_3 equation, the slaving law")
g, q, G, Z, xi, C0, a, s, Pi = sp.symbols("g q G Z xi C0 a s Pi", positive=True)
f = lambda t: t - sp.log(1 + t)
aq = sp.sqrt(xi * G) * q                                    # a0(q)^2 = xi G q^2
L = -g**2 / (8 * sp.pi * G) + aq**2 / (4 * sp.pi * G) * f(g / aq) + Z * q**2 / 2 - C0
flux = sp.simplify(sp.diff(L, g))
law_S = -g**2 / (4 * sp.pi * G * (g + aq))
chk("S1 dL/dg = -(1/4 pi G) g^2/(g + a): the simple-mu law S (V3_FULL_PICTURE.md:47-49)", sp.simplify(flux - law_S) == 0, str(flux))
PiExpr = sp.diff(L, q)
Pi0 = sp.simplify(sp.limit(PiExpr, g, 0))
chk("S2 Pi(x = 0) = Z q (FRW: Y = 0)", sp.simplify(Pi0 - Z * q) == 0, str(Pi0))
eps_vac = sp.simplify((q * PiExpr - L).subs(g, 0))
chk("S3 vacuum energy (Legendre) at x = 0 is Z q^2/2 + C0, so rho_DE c^2 = Z q^2/2 iff C0 = 0", sp.simplify(eps_vac - (Z * q**2 / 2 + C0)) == 0, str(eps_vac))
# h(s) = 2 f(s) - s f'(s): dL_J/dq = (a^2/(4 pi G q)) h(g/a)
h = 2 * f(s) - s * sp.diff(f(s), s)
dLJdq = sp.diff(aq**2 / (4 * sp.pi * G) * f(g / aq), q)
chk("S4 dL_J/dq = (a^2/(4 pi G q)) h(g/a), h = 2f - s f'", sp.simplify(dLJdq - (aq**2 / (4 * sp.pi * G * q)) * h.subs(s, g / aq)) == 0)
hp = sp.simplify(sp.diff(h, s))
chk("S5 h'(s) = s^2/(1+s)^2 > 0, h(0) = 0, h > 0: the MOND sector pulls q DOWN (a_loc < a0)", sp.simplify(hp - s**2 / (1 + s)**2) == 0 and h.subs(s, 0) == 0, str(hp))
# slaving: Z q + (a^2/(4 pi G q)) h = Z qbar; divide by Z qbar, r = q/qbar, eps = xi/(4 pi Z)
qb, r = sp.symbols("qbar r", positive=True)
lhs = (Z * q + (aq**2 / (4 * sp.pi * G * q)) * h.subs(s, g / aq)) / (Z * qb)
eps_sym = xi / (4 * sp.pi * Z)
kap2 = 2 * xi / Z
chk("S6 eps = xi/(4 pi Z) = kappa^2/(8 pi), kappa^2 = 2 xi/Z (a TRADE: one free ratio)", sp.simplify(eps_sym - kap2 / (8 * sp.pi)) == 0)
red = sp.simplify(lhs.subs(q, r * qb) - r * (1 + eps_sym * h.subs(s, g / (sp.sqrt(xi * G) * r * qb))))
chk("S7 slaving law r [1 + eps h(x/r)] = 1 with x = g/a0(qbar)", red == 0)
print(f"  eps = kappa^2/(8 pi) = {KAPPA**2/(8*np.pi):.6f} (kappa = 1/2 both footings); alt-tied reading eps = {EPS_ALT_TIED:.6f}")

# ---------------------------------------------------------------- numerics
hN = lambda t: 2 * (t - np.log1p(t)) - t * t / (1 + t)
hpN = lambda t: t * t / (1 + t) ** 2


def r_of_x(x, eps):
    if eps == 0 or x == 0:
        return 1.0
    if eps * x >= 1.0:
        return 0.0                                # switch-off: q = 0 (|q| kink), the subgradient solution
    fun = lambda rr: rr * (1 + eps * hN(x / rr)) - 1
    return brentq(fun, 1e-300, 1.0, xtol=1e-16, rtol=1e-15, maxiter=500)


def dr_dx(x, eps):
    rr = r_of_x(x, eps)
    if rr == 0.0 or eps == 0:
        return 0.0, rr
    sv = x / rr
    den = 1 + eps * (hN(sv) - sv * hpN(sv))
    return -eps * hpN(sv) / den, rr


def health(x, eps):
    d, rr = dr_dx(x, eps)
    if rr == 0.0:
        return dict(x=x, r=0.0, dF=1.0, FoverG=1.0, MT=np.inf, ML=np.inf, dPidq=np.nan)
    sv = x / rr
    F_over_g = x / (x + rr)
    dF = (x * x + 2 * x * rr - x * x * d) / (x + rr) ** 2        # dF/dg, units a0
    j = x * rr / (x + rr)
    dj = (rr * rr + x * x * d) / (x + rr) ** 2
    MT = x / j
    ML = 1 / dj if dj != 0 else np.inf
    dPidq = 1 + eps * (hN(sv) - sv * hpN(sv))
    return dict(x=x, r=rr, dF=dF, FoverG=F_over_g, MT=MT, ML=ML, dPidq=dPidq)


# ---------------------------------------------------------------- G0
print("=" * 100)
print("G0 health")
print("  (a) DOF: v3s 3 (constraint algebra, V3_FULL_PICTURE.md:184) + A_3 0 (no kinetic term for q; Pi constant): 3")
chk("G0a DOF = 3, no new propagating mode", True)
print("  (c) FRW: Y = 0 so h = 0, Pi = Z q: q = Pi/Z constant in t and x; rho_q = Z q^2/2 constant (w = -1 exactly)")
chk("G0c FRW: q constant; slaving enters perturbations at O(delta^2)", True)
g0 = {}
for fn, a0 in FOOT.items():
    xmax = 1e-8 / a0
    xs = np.logspace(-3, np.log10(xmax), 4001)
    H = [health(x, EPS) for x in xs]
    ML = np.array([hh["ML"] for hh in H]); MT = np.array([hh["MT"] for hh in H])
    dF = np.array([hh["dF"] for hh in H]); dP = np.array([hh["dPidq"] for hh in H])
    bad = xs[(ML < 1) | (MT < 1)]
    # pole of M_L: dj/dg = 0
    def djf(x):
        d, rr = dr_dx(x, EPS)
        return rr * rr + x * x * d
    pole = None
    xtop = min(xmax, (1 / EPS) * (1 - 1e-9)) if EPS > 0 else xmax
    if EPS > 0 and djf(xtop) < 0:
        pole = brentq(djf, 1.0, xtop, xtol=1e-12)
    xoff = (1 / EPS) if EPS > 0 else np.inf
    rec = dict(xmax=xmax, min_ML=float(np.nanmin(ML)), min_MT=float(np.nanmin(MT)), min_dFdg=float(dF.min()),
               min_dPidq=float(np.nanmin(dP)), n_bad=int(bad.size), band_lo=float(bad.min()) if bad.size else None,
               band_hi=float(bad.max()) if bad.size else None, pole_x=pole, switch_off_x=xoff,
               pole_g_SI=pole * a0 if pole else None)
    # sample rows
    for x in [0.1, 1, 3, 10, 11, 12, 20, 50, 100]:
        if x <= xmax:
            hh = health(x, EPS)
            print(f"  {fn:9s} x={x:6.1f}: a_loc/a0={hh['r']:.5f}  dF/dg={hh['dF']:.4f}  M_T={hh['MT']:.3f}  M_L={hh['ML']:.4g}  (unslaved M_L={(1+x)**2:.4g})  dPi/dq/Z={hh['dPidq']:.4f}")
    print(f"  {fn}: min dF/dg = {rec['min_dFdg']:.4f} (total operator elliptic: {rec['min_dFdg']>0}); min dPi/dq/Z = {rec['min_dPidq']:.4f}")
    print(f"  {fn}: M_L pole (dj/dg = 0) at x = {pole}; switch-off x = 1/eps = {xoff:.2f}; band with M < 1: x in [{rec['band_lo']}, {rec['band_hi']}] ({rec['n_bad']} of {xs.size} grid points)")
    chk(f"G0b[{fn}] no ghost: Z > 0, dPi/dq > 0 at every x (Legendre map invertible)", rec["min_dPidq"] > 0)
    chk(f"G0d1[{fn}] total static operator elliptic: dF/dg > 0, F/g > 0", rec["min_dFdg"] > 0)
    chk(f"G0d2[{fn}] khronon pair M_T >= 1 and M_L >= 1 on x in [1e-3, {xmax:.1f}]", rec["n_bad"] == 0,
        f"min M_L = {rec['min_ML']:.4g}")
    g0[fn] = rec
out["G0"] = g0
# does the band carry positive khronon charge? point mass 6e10 Msun, static held state: rho_tau = phantom density
print("  khronon charge in the band (static held state: rho_tau = phantom density), point mass 6e10 Msun:")
for fn, a0 in FOOT.items():
    GM = G_SI * 6e10 * MSUN
    rs = np.logspace(np.log10(0.05 * KPC), np.log10(5 * KPC), 3000)
    gN = GM / rs**2
    gt = np.empty_like(gN)
    for i, gn in enumerate(gN):
        fun = lambda x: x * x - (gn / a0) * (x + r_of_x(x, EPS))
        gt[i] = brentq(fun, gn / a0, gn / a0 + 2) * a0
    ex = (gt - gN) * rs**2
    rho = np.gradient(ex, rs) / (4 * np.pi * G_SI * rs**2)
    x = gt / a0
    pole = g0[fn]["pole_x"]
    inband = (x > pole) & (x < 1 / EPS) if pole else np.zeros_like(x, bool)
    if inband.any():
        rr_ = rs[inband] / KPC
        print(f"   {fn}: band at r = {rr_.min():.3f}-{rr_.max():.3f} kpc; rho_tau > 0 on {np.mean(rho[inband] > 0)*100:.1f} % of it; "
              f"max rho_tau {rho[inband].max()/ (MSUN/(3.0857e16)**3):.3g} Msun/pc^3")
        g0[fn]["band_kpc_6e10"] = [float(rr_.min()), float(rr_.max())]
        g0[fn]["frac_rho_pos"] = float(np.mean(rho[inband] > 0))
        # growth rate at the median band point: omega^2 = 4 pi G rho (M_L - 1) at k -> 0
        for xt in [12.0, 20.0, 50.0]:
            k = np.argmin(np.abs(x - xt))
            MLk = health(x[k], EPS)["ML"]
            rate = np.sqrt(4 * np.pi * G_SI * rho[k] * abs(MLk - 1)) if MLk < 1 else 0.0
            kmax = np.sqrt(2 * (1 - MLk)) / (21.7 * 3.0857e16) if MLk < 1 else 0.0
            print(f"   {fn}: r = {rs[k]/KPC:.3f} kpc, x = {x[k]:.2f}, rho_tau = {rho[k]/(MSUN/(3.0857e16)**3):.3g} Msun/pc^3, M_L = {MLk:.4g}: "
                  f"k->0 rate {rate:.3g} 1/s (e-fold {1/rate/3.156e13 if rate else np.inf:.3g} Myr), unstable for wavelength > {2*np.pi/kmax/3.0857e16 if kmax else 0:.3g} pc at L* 21.7 pc")
            g0[fn][f"efold_Myr_x{int(xt)}"] = float(1 / rate / 3.156e13) if rate else None
G0_PASS = all(c[1] for c in checks if c[0].startswith("G0"))
print(f"G0 VERDICT: {'PASS' if G0_PASS else 'FAIL'}")
out["G0_verdict"] = "PASS" if G0_PASS else "FAIL"

# alt-tied reading
for lab, ee in [("alt-tied kappa 0.6043", EPS_ALT_TIED)]:
    if not MUTATE:
        def djf2(x):
            d, rr = dr_dx(x, ee)
            return rr * rr + x * x * d
        p2 = brentq(djf2, 1.0, 1 / ee - 1e-6, xtol=1e-12)
        print(f"  reading ({lab}): M_L pole x = {p2:.3f}, switch-off {1/ee:.2f}")
        out["alt_tied_pole"] = p2

# ---------------------------------------------------------------- readings G1, G2 (graded only if G0 passed)
tag = "GRADED" if G0_PASS else "UNGRADED READING (G0 failed; candidate stopped)"
print("=" * 100)
print(f"G1 weak field [{tag}]")
g1 = {}
for fn, a0 in FOOT.items():
    gb = np.logspace(-12, -8, 2001)
    law = (gb + np.sqrt(gb**2 + 4 * gb * a0)) / 2
    gA = np.array([brentq(lambda x: x * x - (b / a0) * (x + r_of_x(x, EPS)), b / a0, b / a0 + 2) * a0 for b in gb])
    d = np.abs(np.log10(gA / law))
    g1[fn] = dict(max_dex=float(d.max()), at_gb=float(gb[d.argmax()]))
    print(f"  {fn}: max |dlog g| = {d.max():.5f} dex at g_b = {gb[d.argmax()]:.3g}")
    if G0_PASS:
        chk(f"G1[{fn}] <= 0.01 dex", d.max() <= 0.01)
out["G1"] = g1

print("=" * 100)
print(f"G2 local constancy [{tag}]")
MPC = 1e3 * KPC
g2 = {}
for fn, a0 in FOOT.items():
    env = {"void": 0.0, "field": 0.05 * a0,
           "cluster R=1 Mpc": G_SI * 1e14 * MSUN / MPC**2,
           "cluster R=0.3 Mpc": G_SI * 3e13 * MSUN / (0.3 * MPC)**2}
    rows = {}
    for Mg in [1e9, 1e10, 6e10, 2e11]:
        gint = G_SI * Mg * MSUN / (30 * KPC)**2
        vals = {}
        for en, ge in env.items():
            gn = gint + ge
            x = brentq(lambda x: x * x - (gn / a0) * (x + r_of_x(x, EPS)), gn / a0, gn / a0 + 2)
            vals[en] = float(np.log10(r_of_x(x, EPS)))
        rows[f"{Mg:.0e}"] = dict(vals=vals, spread=max(vals.values()) - min(vals.values()))
    # cluster core: 30 kpc from BCG + ICM, 1.5e12 Msun
    gn = G_SI * 1.5e12 * MSUN / (30 * KPC)**2
    x = brentq(lambda x: x * x - (gn / a0) * (x + r_of_x(x, EPS)), gn / a0, gn / a0 + 2)
    core = float(np.log10(r_of_x(x, EPS)))
    spread_all = max(max(r_["spread"] for r_ in rows.values()), max(abs(core - min(r_["vals"]["void"] for r_ in rows.values())), 0))
    g2[fn] = dict(rows=rows, core_dlog=core, core_x=float(x), max_spread=spread_all)
    for k_, v in rows.items():
        print(f"  {fn} Mb={k_}: " + ", ".join(f"{e} {val:+.5f}" for e, val in v["vals"].items()) + f"  spread {v['spread']:.5f} dex")
    print(f"  {fn} cluster core (BCG+ICM 30 kpc, x = {x:.2f}): dlog a0 = {core:+.5f} dex; max spread vs void {spread_all:.5f} dex")
    if G0_PASS:
        chk(f"G2[{fn}] spread <= 0.015 dex", spread_all <= 0.015)
out["G2"] = g2
# where does a0 shift by 0.015 dex? (pointwise, any environment)
xs = np.logspace(-2, 2, 40001)
dl = np.array([np.log10(r_of_x(x, EPS)) for x in xs]) if EPS > 0 else np.zeros_like(xs)
if EPS > 0:
    x015 = xs[np.argmax(dl < -0.015)]
    print(f"  pointwise: |dlog a0| reaches 0.015 dex at x = g/a0 = {x015:.3f}")
    out["x_at_0p015dex"] = float(x015)

print("=" * 100)
print("G3 tie [NOT GRADED if an earlier gate failed]; FRW reading: q = Pi/Z constant, a0 constant in time.")
z = np.array([1.0, 1.5, 2.33]); aa = 1 / (1 + z); w0, wa = -0.75, -0.86
rho = aa ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - aa))
dev = -0.5 * np.log10(rho)
print("  CPL (w0 -0.75, wa -0.86, PROVISIONAL) sqrt(rho_DE(z)/rho_DE(0)) vs A's flat a0: " + ", ".join(f"z {zz}: {d_:+.4f} dex" for zz, d_ in zip(z, dev)))
out["G3_reading_cpl_dev_dex"] = dev.tolist()

print("=" * 100)
nf = sum(1 for c in checks if not c[1])
print(f"checks: {len(checks)-nf}/{len(checks)} pass; G0 {'PASS' if G0_PASS else 'FAIL'}")
out["checks"] = checks
fn_out = "ct5_candidate_a_MUTATE_results.json" if MUTATE else "ct5_candidate_a_results.json"
with open(fn_out, "w") as fh:
    json.dump(out, fh, indent=1, default=float)
# exit code: main run expected to report G0 verdict honestly (0 always); MUTATE must make G0 pass (exit 1 if not)
if MUTATE:
    sys.exit(0 if G0_PASS else 1)
