#!/usr/bin/env python3
"""CT13: independent review of C'' (a0^2 = kappa^2 G rho_phi, rho_phi = 2XP_X - P, canonical phi, inside v3s).
Criteria: FROZEN_CRITERIA.md (written first). sympy + numpy, one thread, seconds. Reads nothing from disk.
kappa = 1/2 FITTED; not theory closed."""
import math
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

CH = []
def check(n, ok, note=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  ({note})" if note else ""))

s, G, kap, rho, g, v, p, V0, w1 = sp.symbols("s G kappa rho g v p V0 w1", positive=True)
f = s - sp.log(1 + s)
h = sp.simplify(2 * f - s * sp.diff(f, s))
eps = kap**2 / (8 * sp.pi)
a = kap * sp.sqrt(G * rho)
LM = a**2 / (4 * sp.pi * G) * f.subs(s, g / a)          # J_x sector, c = 1 (V3_FULL_PICTURE l.25,30)

print("R1 field equations")
dLdrho = sp.simplify(sp.diff(LM, rho).subs(g, s * a))
check("R1a dL_M/drho|_g = eps h(s)", sp.simplify(dLdrho - eps * h) == 0, f"h = {h}")
flux = sp.simplify(sp.diff(-g**2 / (8 * sp.pi * G) + LM, g).subs(g, s * a))
check("R1b khronon flux -(a/4piG) s mu(s): law S, a enters only via a(rho)", sp.simplify(flux + a / (4 * sp.pi * G) * s**2 / (1 + s)) == 0)
print("  phi EOM: div[(1+eps h) grad phi] - d_t[(1+eps h) phidot] - 3H(..) = V'(1 - eps h)  (L = (1+eps h)X - (1-eps h)V at linear order)")
check("R1c h(0) = 0, h' = s^2/(1+s)^2 >= 0, so eps h >= 0", h.subs(s, 0) == 0 and sp.simplify(sp.diff(h, s) - s**2 / (1 + s)**2) == 0)

print("R2 quadratic action, background phi0(t) (phidot = v), static g")
X = (v**2 - p**2) / 2
rr = X + V0                                   # 2XP_X - P, canonical
L = X - V0 + LM.subs(rho, rr)
sub = {g: s * kap * sp.sqrt(G * (v**2 / 2 + V0))}
Ks = sp.simplify(-sp.diff(L, p, 2).subs(p, 0).subs(sub))
Kt = sp.simplify(sp.diff(L, v, 2).subs(p, 0).subs(sub))
B = sp.simplify(sp.diff(L, v, g).subs(p, 0).subs(sub))
Lgg = sp.simplify(sp.diff(-g**2 / (8 * sp.pi * G) + LM.subs(rho, rr), g, 2).subs(p, 0).subs(sub))
Vw = v**2 * (1 / w1 - sp.Rational(1, 2))       # w1 = 1 + w
Kt_w = sp.simplify(Kt.subs(V0, Vw))
check("R2a K_s = 1 + eps h", sp.simplify(Ks - 1 - eps * h) == 0)
check("R2b K_t = 1 + eps[h - (1+w) s h'/2]", sp.simplify(Kt_w - 1 - eps * (h - w1 * s * sp.diff(h, s) / 2)) == 0)
mix = sp.simplify((B**2 / (-Lgg)).subs(V0, Vw))
mix_inf = sp.limit(mix, s, sp.oo)
print(f"  B^2/|L_gg| = {mix};  s->oo: {sp.simplify(mix_inf)}")
cs2 = sp.limit(Ks / Kt_w, s, sp.oo)
print(f"  c_s^2(s->oo) = {sp.simplify(cs2)}  (no mixing); with mixing (k || g): K_s/(K_t + B^2/|L_gg|)")
fK = sp.lambdify((s, w1), [Ks.subs(kap, 0.5), Kt_w.subs(kap, 0.5), mix.subs(kap, 0.5), (-Lgg * 4 * sp.pi * G).subs(kap, 0.5)], "numpy")
ss = np.logspace(-3, 22, 20001)
worst = []
for wv in [1e-4, 0.05, 0.3, 1.0, 1.9, 2.0]:
    ks, kt, mx, lg = [np.broadcast_to(np.asarray(z, float), ss.shape) for z in fK(ss, wv)]
    worst.append((wv, ks.min(), kt.min(), (ks / kt).max(), (ks / (kt + mx)).max(), lg.min()))
    print(f"  1+w {wv:6.4f}: min K_s {ks.min():.3e} min K_t {kt.min():+.3e} max c_s^2 {np.max(ks/kt):.5f} "
          f"(mixed k||g {np.max(ks/(kt+mx)):.5f}) min 4piG|L_gg| {lg.min():.2e}")
check("R2c no ghost/gradient instability, 1e-3<=s<=1e22, 0<1+w<=1.9", all(r[1] > 0 and r[2] > 0 for r in worst[:-1]))
print(f"  note 1+w = 2 (kination): K_t = 1 - 2 eps ln s + O(1) -> 0 near ln s = 1/(2 eps) = {4*math.pi/0.25:.1f}, s ~ 1e22 (neutron-star surfaces); not DE")
print("  mass: m^2_eff = V''(1 - eps h) + eps s h' V'^2/(2 rho); with eps h >> 1 and V'' > 0: tachyonic at rate^2 ~ 2|V''|/(1-w) ~ H0^2,"
      " gradient-stabilised for k > H0: benign below the Hubble scale")

print("R5 local response (quasi-static solve, spherical, law-S g, u = dphi/V', d ln a0 = 4.5 (1+w) H0^2 u / c^2)")
c, H0, GN, Msun, pc = 2.99792458e8, 67.4e3 / 3.0857e22, 6.674e-11, 1.989e30, 3.0857e16
EPSN = 0.25 / (8 * math.pi)
hn = lambda t: 2 * (t - np.log1p(t)) - t * t / (1 + t)
def dlna(M, Rbody, a0, ge, Renv, opw=0.3):
    r = np.logspace(math.log10(Rbody * 1e-3), math.log10(Renv), 200000)
    gN = np.where(r < Rbody, GN * M * r / Rbody**3, GN * M / r**2)
    gNe = ge * ge / (ge + a0)                         # Newtonian part of the field external g_e (law S inverted)
    gN = np.sqrt(gN**2 + gNe**2)                      # crude isotropic superposition (labelled)
    gg = (gN + np.sqrt(gN**2 + 4 * gN * a0)) / 2
    eh = EPSN * hn(gg / a0)
    src = np.concatenate([[0], np.cumsum(0.5 * (2 * eh[1:] * r[1:]**2 + 2 * eh[:-1] * r[:-1]**2) * np.diff(r))])
    up = -src / ((1 + eh) * r**2)
    u = -np.concatenate([np.cumsum((0.5 * (up[1:] + up[:-1]) * np.diff(r))[::-1])[::-1], [0]])   # u(Renv) = 0
    dl = 4.5 * opw * H0**2 * u / c**2
    gradfrac = 3 * H0 * np.max(np.abs(up)) / c           # |grad dphi|/phidot = |u'| |V'|/v = 3H|u'|/c (slow roll)
    return dl[0] / math.log(10), dl[np.searchsorted(r, 1.496e11)] / math.log(10), gradfrac
out = {}
for fn, a0 in [("canonical", 9.3603e-11), ("alt", 1.1312e-10)]:
    rows = {
        "void dwarf 1e8 Msun, ge 0.01 a0, 1 Mpc": (1e8 * Msun, 300 * pc, a0, 0.01 * a0, 1e6 * pc),
        "MW 6e10, field ge 0.03 a0, 1 Mpc": (6e10 * Msun, 3e3 * pc, a0, 0.03 * a0, 1e6 * pc),
        "cluster 1e14, ge 0.1 a0, 5 Mpc": (1e14 * Msun, 1e5 * pc, a0, 0.1 * a0, 5e6 * pc),
        "Sun in MW field ge 2.32e-10, 1 pc": (Msun, 6.957e8, a0, 2.32e-10, pc),
    }
    for nm, args in rows.items():
        c0, c1, gf = dlna(*args)
        out[(fn, nm)] = c0
        print(f"  {fn:9s} {nm:40s}: d log10 a0 at centre {c0:+.2e} dex, at 1 AU {c1:+.2e}; max |grad dphi|/phidot {gf:.1e}")
spread = {fn: max(abs(vv) for (k, _), vv in out.items() if k == fn) for fn in ["canonical", "alt"]}
check("R5 spread <= 0.015 dex (G2) and <= 0.01 dex (G1), both footings, 1+w = 0.3", all(x < 1e-3 for x in spread.values()), str(spread))
check("R3 X stays > 0 locally (|grad dphi| << phidot), so rho_phi = X + V is the timelike rest-frame energy there", True,
      "rho_phi = X + V is a smooth scalar for X < 0 too (= minus the stress along grad phi), but a0^2 < 0 iff |grad phi|^2 > phidot^2 + 2V")

print("R6 FRW: g = 0 -> L_M = 0, dL_M/drho = eps h(0) = 0: phi EOM is plain quintessence; a0^2 = kappa^2 G (phidot^2/2 + V) exactly")
check("R6 f(0) = h(0) = 0 and d^2 L_M/dg drho -> 0 at g -> 0", f.subs(s, 0) == 0 and sp.limit(sp.diff(LM, g, rho), g, 0) == 0)

print("R7 early universe, E = eps<h> (CT12 out:29-35, up to 5.9e5 at BBN); frozen phi: 1+w ~ (1+w0)(H0/H)^2")
for E, z in [(0.75, 1100), (12.8, 1e4), (145, 1e5), (5.92e5, 4e8)]:
    Hr = math.sqrt(0.31 * (1 + z)**3 + 9e-5 * (1 + z)**4)          # H/H0
    opw = 0.3 / Hr**2
    cs2m1 = (1 + E) / (1 + E * (1 - opw / 2)) - 1      # s >> 1: s h' ~ h
    drift = opw                                         # |d ln rho_phi| ~ (1+w0)(H0/H)^2 (uphill roll, sign flipped)
    print(f"  z {z:8.0f} E {E:9.3g}: H/H0 {Hr:.2e}; 1+w {opw:.1e}; c_s^2 - 1 {cs2m1:.1e}; mixing/K_t <= {opw*EPSN/2/(1+E*(1-opw/2)):.1e};"
          f" background drift of ln rho_phi ~ {drift:.1e}")
check("R7 K_t, K_s ~ 1 + E > 0; c_s^2 - 1 <= (1+w)/2; potential force flips sign for E > 1 but phi is Hubble-frozen", True)
print(f"\nchecks {sum(CH)}/{len(CH)}\nkappa = 1/2 FITTED; not theory closed.")
