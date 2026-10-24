#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O1_ownership_action: can an action in the v3s family give Z*'s R2 (ownership)?  Frozen: FROZEN_CRITERIA.md (45d70e5e2f).

v3s PN system (H5 A1, U1 header):  Xi = Phi - sigma_t + |grad sigma|^2/2 ;  4 pi G rho_tau = div[(1 - mu) grad Xi] (mu_K = 0) ;
lap Phi = 4 pi G (rho_b + rho_tau) ;  khronon: D v/Dt = -grad(Phi - Xi), v = -grad sigma ;  baryons: -grad Phi ;  mu = x/(1+x).

Run:     OMP_NUM_THREADS=1 nice -n 15 python3 o1_ownership_action.py            -> .out, _results.json  (exit 0 if all K pass)
Mutate:  O1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 o1_ownership_action.py -> _MUTATE.out, _results_MUTATE.json (exit 1 by design)
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; not theory closed; cold energy, no particle.
"""
import os, sys, json, math, time, csv, resource
import numpy as np
import sympy as sp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(HERE)                      # rebuild_2026_10_22
REPO = os.path.dirname(R)
MUT = os.environ.get("O1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"o1_ownership_action{TAG}.out"), "w")
RES = {"lane": "O1_ownership_action", "mutate": MUT, "frozen": "45d70e5e2f"}
CHECKS = {}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, val, note=""):
    CHECKS[name] = {"pass": bool(ok), "value": str(val), "note": note}
    P(f"{name} {'PASS' if ok else 'FAIL'} :: {val}  {note}")


def rss_gb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r / 1e6


# ---------------------------------------------------------------------------------------------------------------------
# constants (SI)
G = 6.674e-11; MSUN = 1.989e30; GMSUN = 1.32712e20; PC = 3.0857e16; KPC = 1e3 * PC; AU = 1.495979e11
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
EPS_B = {"canonical": 0.344, "alt": 0.317}          # CFG945 README
MW_MB = 6e10                                        # D10 MW_Mb E_mid (both footings)
FS = 5.364                                          # Z1 supply ratio (LCDM-processed; Z* reading only)
HEES, PARK = 9.0e-27, 5.2e-27                       # D7d / C6 lines (s^-2)
RHO_SUN = {"canonical": 0.0447, "alt": 0.0514}      # Galactic phantom at the Sun, Msun/pc^3 (X3 README, H4 solver)
GPC = 4.30091e-3                                    # G in pc (km/s)^2 / Msun

P("=" * 118)
P(f"O1_ownership_action  {'MUTATE' if MUT else 'main'}   frozen 45d70e5e2f   kappa = 1/2 FITTED; footings never pooled")
P("=" * 118)

# =====================================================================================================================
# PART A: theorems (sympy)
# =====================================================================================================================
P("\n--- K1 (T-G): Xi is invariant under arbitrary time-dependent translations; grad Xi = khronon proper acceleration ---")
xp, yp, zp, t = sp.symbols("xp yp zp t", real=True)
Dv = [sp.Function(f"D{i}")(t) for i in range(3)]
X = [xp + Dv[0], yp + Dv[1], zp + Dv[2]]
sig = sp.Function("sigma"); Phi = sp.Function("Phi"); fT = sp.Function("f")(t)
# sigma enters Xi only through sigma_t and grad sigma at the point, so a quadratic polynomial with symbolic
# coefficients in (x, y, z, t) is fully generic for this identity (avoids sympy's Subs-of-shifted-argument forms)
xs, ys, zs = sp.symbols("xs ys zs", real=True)
mons = [m for m in sp.itermonomials([xs, ys, zs, t], 2)]
cs = sp.symbols(f"c0:{len(mons)}")
sig_poly = sum(c * m for c, m in zip(cs, mons))
Xp = [xp, yp, zp]
sigX = sig_poly.subs({xs: X[0], ys: X[1], zs: X[2]}, simultaneous=True)
PhiX = Phi(*X, t)
sigp = sigX + sum(sp.diff(Dv[i], t) * Xp[i] for i in range(3)) + fT
Phip = PhiX + sum(sp.diff(Dv[i], t, 2) * Xp[i] for i in range(3))
Xip = Phip - sp.diff(sigp, t) + sum(sp.diff(sigp, c) ** 2 for c in Xp) / 2
Xi_poly = Phi(xs, ys, zs, t) - sp.diff(sig_poly, t) + sum(sp.diff(sig_poly, c) ** 2 for c in (xs, ys, zs)) / 2
Xi_atX = Xi_poly.subs({xs: X[0], ys: X[1], zs: X[2]}, simultaneous=True)
diffK1 = sp.expand(Xip - Xi_atX)
target = -sp.diff(fT, t) + sum(sp.diff(Dv[i], t) ** 2 for i in range(3)) / 2
resK1a = sp.simplify(diffK1 - sp.expand(target))
Xi_un = Phi(xs, ys, zs, t) - sp.diff(sig(xs, ys, zs, t), t) + sum(sp.diff(sig(xs, ys, zs, t), c) ** 2 for c in (xs, ys, zs)) / 2
# grad Xi = grad Phi + D v/Dt with v = -grad sigma (unprimed)
s3 = sig(xs, ys, zs, t); c3 = (xs, ys, zs)
v = [-sp.diff(s3, c) for c in c3]
DvDt = [sp.diff(v[i], t) + sum(v[j] * sp.diff(v[i], c3[j]) for j in range(3)) for i in range(3)]
resK1b = [sp.simplify(sp.diff(Xi_un, c3[i]) - sp.diff(Phi(xs, ys, zs, t), c3[i]) - DvDt[i]) for i in range(3)]
check("K1", resK1a == 0 and all(r == 0 for r in resK1b),
      f"Xi' - Xi - (|D'|^2/2 - f') = {resK1a}; grad Xi - grad Phi - Dv/Dt = {resK1b}",
      "choose f' = |D'|^2/2: Xi is a Milne scalar; x = |a_khronon - g|/a0 (the khronon's proper acceleration)")
RES["K1"] = {"Xi_shift": str(target), "grad_identity": "grad Xi = grad Phi + Dv_tau/Dt"}

P("\n--- K2 (T-W, 1D exact): total force on everything in [z1, z2] is a boundary function ---")
z = sp.symbols("z", real=True); fourpiG = sp.symbols("K", positive=True)
p = sp.Function("p")(z)          # Phi_z
q = sp.Function("q")(z)          # Xi_z
rb = sp.Function("rho_b")(z)
ff = sp.Function("F")            # hold flux f(s) = (1 - mu) s  (generic)
U = sp.Function("U")             # generic local stiffness energy of the charge
beta, vb, vt = sp.symbols("beta v_b v_tau", real=True)
rt = sp.diff(ff(q), z) / fourpiG                      # rho_tau
s_ = sp.symbols("s_")
Up = sp.diff(U(s_), s_); Upp = sp.diff(U(s_), s_, 2)
# force density: gravity on all, hold on khronon, stiffness on khronon, plus an internal action-reaction pair (drag)
drag = beta * rb * (vt - vb)
force = -(rb + rt) * p + rt * q - rt * Upp.subs(s_, rt) * sp.diff(rt, z) + drag - drag
# boundary function B: -p^2/2K + H(q)/K - [rho U'(rho) - U(rho)], with dH/dz = q F'(q) q'
dB = -p * sp.diff(p, z) / fourpiG + q * sp.diff(ff(q), z) / fourpiG \
     - sp.diff(rt * Up.subs(s_, rt) - U(rt), z)
resK2 = sp.simplify((dB - force).subs(sp.diff(p, z), fourpiG * (rb + rt)).doit())
check("K2", resK2 == 0, f"dB/dz - force density = {resK2}",
      "any odd hold flux, any local stiffness U, any internal action-reaction pair: F[z1,z2] = B(z2) - B(z1)")

P("\n--- K3: H is even and increasing in |s|; ownership <=> ambient khronon unheld ---")
ss = sp.symbols("s", positive=True)
f_pos = ss / (1 + ss)                                   # a0 = 1, s >= 0 branch; f odd by construction
H_pos = sp.integrate(sp.symbols("tt", positive=True) / (1 + sp.symbols("tt", positive=True)) ** 2,
                     (sp.symbols("tt", positive=True), 0, ss))
H_pos = sp.simplify(H_pos)
dH = sp.simplify(sp.diff(H_pos, ss) - ss * sp.diff(f_pos, ss))
P(f"   H(s) = {H_pos} for s >= 0 (H' - s f' = {dH}); H(-s) = H(s) since f' is even")


def f_num(s, even=False):
    return (abs(s) / (1 + abs(s))) if even else s / (1 + abs(s))


def H_num(s, even=False):
    a = abs(s)
    h = math.log1p(a) + 1 / (1 + a) - 1
    return (math.copysign(h, s) if even else h)       # even flux -> odd H (mutate Mu4)


def slab_ratio(E, S, even=False):
    """1D slab, 4 pi G = 1, a0 = 1, both edges HOVERING (Xi_z = Phi_z): composite acceleration / mean field."""
    p1, p2 = E - S / 2, E + S / 2
    Stau = f_num(p2, even) - f_num(p1, even)
    F = -(p2 ** 2 - p1 ** 2) / 2 + (H_num(p2, even) - H_num(p1, even))
    return F / S / (-E), Stau / S


iff_ok = True
rows3 = []
for E in (-0.05, -0.3, -1.0):
    for S in (0.01, 0.1, 0.5):
        r, fh = slab_ratio(E, S, even=MUT)
        rows3.append((E, S, r, fh, 1 - fh))
        P(f"   g_ext {-E:5.2f} a0, column {S:5.2f}: a/g_ext = {r:+.5f}; held share {fh:.4f}; 1 - held share = {1 - fh:.5f}")
        # hovering edges with net held charge must NOT fall at g_ext
        if abs(fh) > 1e-9 and abs(r - 1) < 1e-6:
            iff_ok = False
# antisymmetric edges (ambient unheld): falls at g_ext with held charge
p1, p2 = -0.4, 0.4
Fa = -(p2 ** 2 - p1 ** 2) / 2 + (H_num(p2, MUT) - H_num(p1, MUT))
anti_ok = abs(Fa) < 1e-12 and abs(f_num(p2, MUT) - f_num(p1, MUT)) > 0.1
check("K3", dH == 0 and iff_ok and anti_ok,
      f"H' - s f' = {dH}; hovering edges never give a = g_ext with held charge: {iff_ok}; antisymmetric (unheld) edges: "
      f"Khronon force {Fa:.2e} with held column {f_num(p2, MUT) - f_num(p1, MUT):.3f}",
      "Mu4 (even flux) must FAIL this check")
RES["K3_slab"] = rows3

P("\n--- K4 (T-W, 3D): linear-medium stress identity, force on a held charge in a uniform Xi gradient ---")
xx, yy, zz = sp.symbols("x y z", real=True); qch, Ef, Rr, th, ph = sp.symbols("q E R theta phi", positive=True)
rr = sp.sqrt(xx ** 2 + yy ** 2 + zz ** 2)
GG = sp.symbols("G", positive=True)
Xi_c = Ef * zz - GG * qch / rr                    # lap(-G q / r) = 4 pi G q delta  -> charge q
gX = [sp.diff(Xi_c, c) for c in (xx, yy, zz)]
Tz = [(gX[2] * gX[j] - (sp.Rational(1, 2) if j == 2 else 0) * sum(c ** 2 for c in gX)) / (4 * sp.pi * GG) for j in range(3)]
nvec = [sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)]
sub = {xx: Rr * nvec[0], yy: Rr * nvec[1], zz: Rr * nvec[2]}
integrand = sp.simplify(sum(Tz[j].subs(sub) * nvec[j] for j in range(3)) * Rr ** 2 * sp.sin(th))
Fz = sp.simplify(sp.integrate(sp.integrate(integrand, (ph, 0, 2 * sp.pi)), (th, 0, sp.pi)))
resK4 = sp.simplify(Fz - qch * Ef)
check("K4", resK4 == 0, f"surface force - q E = {resK4}",
      "with grad Xi_amb = grad Phi_amb (held host): net host force on the composite = M_b g (U1 D7/N4: nonlinear to <= 8.7e-5)")

P("\n--- K5 (T-E): spherical host, any khronon motion: |grad Xi_amb| = f^-1(G M_tau(<r)/r^2); held AQUAL host -> eps = 1 ---")
gs, yN = sp.symbols("g y", positive=True)
mu = gs / (1 + gs)
aq = sp.Eq(mu * gs, yN)                         # AQUAL: mu(g) g = g_N  (a0 = 1)
Mph_term = gs - yN                              # G M_ph / r^2
resK5 = sp.simplify((Mph_term - gs / (1 + gs)).subs(yN, mu * gs))
check("K5", resK5 == 0, f"G M_ph/r^2 - f(g) = {resK5} on the AQUAL branch",
      "so f^-1(G M_ph/r^2) = g: the held phase's ambient anti-weight equals g_host, eps = 1, at every radius")


def finv(u):
    return u / (1 - u)


def law_g(y):
    return y / 2 + math.sqrt(y * y / 4 + y)


P("\n--- N1: eps(r) for a MW-like host (M_b 6e10), held v3s host and Z*'s supply-edge statics ---")
N1 = {}
for foot, a0 in FOOT.items():
    rM = math.sqrt(GMSUN * MW_MB / a0)
    rs = rM * math.sqrt(FS * (FS + 1))
    N1[foot] = {"r_M_kpc": rM / KPC, "r_s_kpc": rs / KPC, "rows": []}
    P(f"   [{foot}] r_M {rM / KPC:.2f} kpc, Z* supply edge r_s {rs / KPC:.1f} kpc")
    for rk in (20, 50, 100, 250, 400):
        r = rk * KPC
        y = GMSUN * MW_MB / (r * r * a0)
        g = law_g(y)
        uph = g - y
        eps_held = finv(uph) / g
        if MUT:
            eps_held = 0.0                                # Mu1: satellite's held phase invisible to the host Xi
        if r <= rs:
            eps_z = eps_held
        else:
            ut = FS * GMSUN * MW_MB / (r * r * a0)
            eps_z = 0.0 if MUT else finv(ut) / (ut + y)
        own = (eps_held <= EPS_B[foot]) and (eps_z <= EPS_B[foot])
        N1[foot]["rows"].append({"r_kpc": rk, "g_host_a0": g, "eps_held_v3s": eps_held, "eps_Zstar": eps_z, "OWN": own})
        P(f"      r {rk:4d} kpc: g_host {g:.4f} a0; eps (held v3s host) {eps_held:.6f}; eps (Z* statics) {eps_z:.4f}; "
          f"eps_B {EPS_B[foot]}: OWN {'PASS' if own else 'FAIL'}")
RES["N1"] = N1
own_any = any(rw["OWN"] for f_ in N1 for rw in N1[f_]["rows"] if rw["r_kpc"] in (50, 100, 250))
check("N1-OWN", not own_any,
      f"OWN passes at any of 50/100/250 kpc: {own_any}", "frozen M1a line; Mu1 must flip it")

P("\n--- N2: what OWN would cost the host: largest phantom fraction phi inside r with eps <= eps_B ---")
N2 = {}
for foot, a0 in FOOT.items():
    N2[foot] = []
    for rk in (50, 100, 250):
        r = rk * KPC
        y = GMSUN * MW_MB / (r * r * a0)
        g = law_g(y); u = g - y
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            e = finv(mid * u) / (y + mid * u)
            (lo, hi) = (mid, hi) if e <= EPS_B[foot] else (lo, mid)
        phi = lo
        vc = math.sqrt(g * a0 * r) / 1e3
        vcp = math.sqrt((y + phi * u) * a0 * r) / 1e3
        N2[foot].append({"r_kpc": rk, "phi_max": phi, "vc_law_kms": vc, "vc_at_phi_kms": vcp})
        P(f"   [{foot}] r {rk:3d} kpc: phi_max {phi:.4f}; host v_c {vc:6.1f} km/s (law) -> {vcp:6.1f} km/s (with phi_max)")
RES["N2"] = N2

P("\n--- K6 (T-N): per-label khronons: separate continuity; N labels static in one galaxy -> floor at x = N - 1 ---")
tt = sp.symbols("t"); zz1 = sp.symbols("z")
s1 = sp.Function("sigma1")(zz1, tt); s2 = sp.Function("sigma2")(zz1, tt); Ph = sp.Function("Phi")(zz1, tt)
Wf = sp.Function("W")
Xi1 = Ph - sp.diff(s1, tt) + sp.diff(s1, zz1) ** 2 / 2
Xi2 = Ph - sp.diff(s2, tt) + sp.diff(s2, zz1) ** 2 / 2
Lag = Wf(sp.diff(Xi1, zz1)) + Wf(sp.diff(Xi2, zz1))
from sympy.calculus.euler import euler_equations
el = euler_equations(Lag, [s1, s2], [zz1, tt])
# the s1 equation must not contain sigma2 (separate conservation): check free functions
el1 = el[0].lhs
dep_on_s2 = el1.has(s2)
dep_on_s1_in_el2 = el[1].lhs.has(s1)
Nn = sp.symbols("N", positive=True); xg = sp.symbols("x", positive=True)
coef = 1 - Nn * (1 - xg / (1 + xg))
floor = sp.solve(sp.Eq(coef, 0), xg)
Nval = 1 if MUT else 2
floor_ok = (floor == [Nn - 1]) and (Nval - 1 > 0)
check("K6", (not dep_on_s2) and (not dep_on_s1_in_el2) and floor_ok,
      f"EL(sigma1) contains sigma2: {dep_on_s2}; EL(sigma2) contains sigma1: {dep_on_s1_in_el2}; "
      f"N-label coefficient 1 - N(1 - mu) = 0 at x = {floor}; at N = {Nval}: floor x = {Nval - 1}",
      "each label's charge is a separate Noether charge (no merging); Mu2 (N = 1) must flip")
# over-hold with labelled capacity (deep limit, co-spatial supplies): sum sqrt(M_i)/sqrt(sum M_i)
over = {n: math.sqrt(n) for n in (2, 4, 10, 100)}
P("   with per-label capacity (deep limit, co-spatial labelled supplies, N equal progenitors): held/demand = "
  + ", ".join(f"N={n}: {v:.2f} (+{math.log10(v):.2f} dex in g)" for n, v in over.items()))
RES["K6"] = {"floor_x": "N-1", "overhold_equal_progenitors": over}

P("\n--- K7 (T-R): a flat rotation curve is not curl-free; the khronon flow is ---")
Rc, vc_s = sp.symbols("R v_c", positive=True)
curl = sp.simplify(sp.diff(Rc * vc_s, Rc) / Rc)
check("K7", sp.simplify(curl - vc_s / Rc) == 0, f"(curl v_b)_z = {curl}; curl(-grad sigma) = 0",
      "a2 (v_tau = v_b where rho_b > 0) has no solution in any rotating disc; c's mean-flow khronon likewise")

P("\n--- K8 (T-X): an inter-label exchange V(sigma1 - sigma2) ---")
Vf = sp.Function("V")
Lag2 = Lag - Vf(s1 - s2)
el2 = euler_equations(Lag2, [s1, s2], [zz1, tt])
src1 = sp.simplify(el2[0].lhs - el[0].lhs)
src2 = sp.simplify(el2[1].lhs - el[1].lhs)
check("K8", sp.simplify(src1 + src2) == 0 and src1 != 0,
      f"source in label-1 continuity {src1}; label-2 {src2}; sum {sp.simplify(src1 + src2)}",
      "total conserved, each label not: where V' != 0 and rho = 0, equal and opposite charges appear (one negative)")

P("\n--- K9 (a1): baryon-khronon drag -(beta/2) rho_b |v_tau - v_b|^2 enters the khronon equation as a charge flux ---")
sg = sp.Function("sigma")(zz1, tt); rbf = sp.Function("rho_b")(zz1, tt); vbf = sp.Function("v_b")(zz1, tt)
Xi0 = Ph - sp.diff(sg, tt) + sp.diff(sg, zz1) ** 2 / 2
Ld = Wf(sp.diff(Xi0, zz1)) - beta / 2 * rbf * (-sp.diff(sg, zz1) - vbf) ** 2
eld = euler_equations(Ld, [sg], [zz1, tt])[0].lhs
el0 = euler_equations(Wf(sp.diff(Xi0, zz1)), [sg], [zz1, tt])[0].lhs
extra = sp.simplify(eld - el0)
target9 = -sp.diff(beta * rbf * (-sp.diff(sg, zz1) - vbf), zz1)
check("K9", sp.simplify(extra - target9) == 0 or sp.simplify(extra + target9) == 0,
      f"extra term = {extra}",
      "d_t rho + d_z[rho v_tau + beta rho_b (v_tau - v_b)] = 0: drag re-routes charge (can create rho < 0 where rho = 0), "
      "does not change D v_tau/Dt = -d(Phi - Xi)")

P("\n--- K10 (T-M): v3s's covector P carries no memory (beta = eta = 0) ---")
Pz = sp.Function("P")(zz1, tt)
gfun = sp.Function("g"); Kc = sp.symbols("K", positive=True)
LP = -(sp.diff(Ph, zz1) - Kc * Pz) ** 2 / (2 * Kc) - gfun(Kc * Pz) - sp.symbols("gamma_L") / 2 * sp.diff(Pz, zz1) ** 2
elP = euler_equations(LP, [Pz], [zz1, tt])[0].lhs
has_tdot = elP.has(sp.Derivative(Pz, tt))
check("K10", not has_tdot, f"EL(P) contains d_t P: {has_tdot}",
      "the PN state is (rho_tau, v_tau, Xi); two parcels at one point with one velocity are identical: no formation memory")

P("\n--- K11 (T-C): a zero-charge exterior label flow is geodesic; radial infall from rest in a flat-curve host ---")
r0, rr_ = sp.symbols("r_0 r", positive=True); uu = sp.symbols("u", positive=True)
tff = sp.integrate(r0 * sp.exp(-uu) / sp.sqrt(2 * uu), (uu, 0, sp.oo))     # r = r0 e^{-u}, v = v_c sqrt(2u)
check("K11", sp.simplify(tff - r0 * sp.sqrt(sp.pi / 2)) == 0, f"t_centre * v_c = {sp.simplify(tff)}",
      "every exterior streamline reaches the centre at t = sqrt(pi/2) r0/v_c: the innermost at once -> caustic at the host centre")
K11num = {}
for rk in (1, 10, 50):
    K11num[rk] = math.sqrt(math.pi / 2) * rk * KPC / 200e3 / 3.156e13
P("   at v_c = 200 km/s: r0 = " + ", ".join(f"{k} kpc -> {v:.1f} Myr" for k, v in K11num.items()))
RES["K11_Myr"] = K11num

# =====================================================================================================================
# PART B: record reproduced first, then the VS tiles
# =====================================================================================================================
P("\n--- K12: record reproduced ---")
ok12 = []
rs_c = N1["canonical"]["r_s_kpc"]
ok12.append(abs(rs_c - 55) <= 2)
P(f"   Z1 r_s (MW-like, canonical) {rs_c:.2f} kpc vs 55 (Z1 DESIGN risk 4)")
d10 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json")))
cells = d10["band_cells"]
dN = {k: v["dchi2_Newton"] for k, v in cells.items()}
dA = {k: v["dchi2_AQUAL"] for k, v in cells.items()}
ok12.append(len(dN) == 18 and abs(max(dN.values()) - 2.47) < 0.01 and abs(min(dA.values()) - 4.89) < 0.01)
P(f"   D10: {len(dN)} cells, max dchi2_Newton {max(dN.values()):.3f} (README <= 2.5), dchi2_AQUAL {min(dA.values()):.2f}-{max(dA.values()):.2f}")
u1 = json.load(open(os.path.join(R, "U1_v3_dust_content/u1_v3_dust_content_results.json")))["numbers"]["N5"]
sat = {f: u1["satellites"][f]["stats"]["B0"] for f in FOOT}
coma = {f: u1["coma"][f]["B0"] for f in FOOT}
tdg = {f: u1["tdg"][f]["TDG_B0"] for f in FOOT}
ok12.append(abs(sat["canonical"][0] - 2.00) < 0.01 and abs(sat["alt"][0] - 1.99) < 0.01 and abs(coma["canonical"]["dex"] - 1.41) < 0.01)
P(f"   U1 N5 B0: satellites {sat['canonical'][0]:+.3f} +- {sat['canonical'][1]:.3f} / {sat['alt'][0]:+.3f} +- {sat['alt'][1]:.3f}; "
  f"Coma {coma['canonical']['dex']:+.2f} dex z_sys {coma['canonical']['z_sys']:.2f}; TDG {tdg['canonical']['rbar']:+.3f} +- {tdg['canonical']['se']:.3f}")
h5rows = list(csv.DictReader(open(os.path.join(R, "H5_v3s_lobe_growth/h5_per_system.csv"))))
gcs = {}
for rw in h5rows:
    if rw["class"].startswith("a_glob") and rw["foot"] == "canonical" and rw["name"] not in gcs:
        gcs[rw["name"]] = rw
rc_rep = max(float(rw["r_cap_pc"]) for rw in gcs.values())
rc_mine = max(2 * GPC * float(rw["Mb_Msun"]) / float(rw["V_kms"]) ** 2 for rw in gcs.values())
ok12.append(abs(rc_rep - 0.2489) < 1e-3 and abs(rc_mine - rc_rep) / rc_rep < 0.01)
P(f"   H5 r_cap (globulars, PROXY speed): max {rc_rep:.4f} pc; this lane's 2 G M_b/V^2 {rc_mine:.4f} pc")
check("K12", all(ok12), f"{ok12}", "Z1 r_s, D10 cells, U1 N5, H5 r_cap")
RES["record"] = {"D10_dchi2_Newton": dN, "D10_dchi2_AQUAL": dA, "U1_sat_B0": sat,
                 "U1_coma_B0": {f: coma[f]["dex"] for f in FOOT}, "U1_coma_zsys": {f: coma[f]["z_sys"] for f in FOOT},
                 "U1_TDG_B0": {f: [tdg[f]["rbar"], tdg[f]["se"]] for f in FOOT}}

P("\n--- N3 (VS): capture radii and the Solar-System tide with gamma_L removed ---")
VS = {}
for V in (220.0, 250.0):
    rcap = 2 * GMSUN / (V * 1e3) ** 2
    VS[f"Sun_rcap_AU_V{int(V)}"] = rcap / AU
    P(f"   Sun at {V:.0f} km/s: r_cap = {rcap / AU:.4f} AU = {rcap / 6.957e8:.1f} R_sun; x there = {GMSUN / rcap ** 2 / FOOT['canonical']:.2e}")
tide_rows = []
for foot, a0 in FOOT.items():
    rho = RHO_SUN[foot] * MSUN / PC ** 3
    wp2 = 4 * math.pi * G * rho
    rM = math.sqrt(GMSUN / a0)
    for V in (220.0, 250.0):
        Vs = V * 1e3
        supp = wp2 * rM ** 2 / Vs ** 2
        for rau in (1.0, 9.5, 30.0):
            T = 4 * math.pi * G * rho * GMSUN / (Vs ** 2 * rau * AU)
            tide_rows.append({"foot": foot, "V": V, "r_AU": rau, "tide_s2": T, "over_Hees": T / HEES, "over_Park": T / PARK,
                              "suppression_at_rM": supp})
        P(f"   [{foot}] V {V:.0f}: rho {RHO_SUN[foot]} Msun/pc^3, omega_p {math.sqrt(wp2):.2e} s^-1, r_M {rM / AU:.0f} AU, "
          f"(omega_p r_M/V)^2 = {supp:.2e}; wake tide at 1/9.5/30 AU: "
          + " / ".join(f"{rw['tide_s2']:.1e}" for rw in tide_rows[-3:]) + " s^-2")
tmax = max(rw["tide_s2"] for rw in tide_rows)
cass = tmax <= min(HEES, PARK)
VS["solar_tide_max"] = tmax; VS["Cassini"] = "PASS" if cass else "FAIL"
P(f"   max wake tide {tmax:.2e} s^-2 vs Hees {HEES:.1e} / Park {PARK:.1e}: ratio {tmax / PARK:.1e} -> Cassini (VS, gamma_L = 0) {VS['Cassini']}")

P("   outer globulars (H5 PROXY speed and V_apo,10), r_cap vs r_hl:")
gc_ok = True
gc_rows = []
for nm, rw in gcs.items():
    Mb = float(rw["Mb_Msun"]); V = float(rw["V_kms"]); Va = float(rw["V_apo10_kms"]); a = float(rw["a_pc"])
    rc1 = 2 * GPC * Mb / V ** 2; rc2 = 2 * GPC * Mb / Va ** 2
    gc_rows.append({"name": nm, "Mb": Mb, "r_hl_pc": a, "rcap_PROXY_pc": rc1, "rcap_Vapo10_pc": rc2})
    gc_ok = gc_ok and rc2 < a
    P(f"      {nm:9s} M_b {Mb:.2e}: r_cap {rc1:.4f} pc (V {V:.0f}) / {rc2:.3f} pc (V {Va:.0f}); r_hl {a:.1f} pc")
dN_use = dA if MUT else dN                              # Mu3: AQUAL column in place of Newton
gc_chi = max(dN_use.values()) < 3.84
VS["globulars"] = "PASS" if (gc_ok and gc_chi) else "FAIL"
VS["globular_rows"] = gc_rows
P(f"   D10 dchi2 at Newton (velocity-screened = Newton): max {max(dN_use.values()):.2f} {'(Mu3: AQUAL column)' if MUT else ''} "
  f"< 3.84: {gc_chi}; r_cap < r_hl at both speeds: {gc_ok} -> outer globulars (VS, gamma_L = 0) {VS['globulars']}")
check("VS-GC", VS["globulars"] == "PASS", VS["globulars"], "Mu3 must FAIL this")
iso_rcap = 2 * GPC * 1e9 / 0.03 ** 2
VS["isolated_rcap_pc_1e9_at_0.03kms"] = iso_rcap
P(f"   isolated galaxy (M_b 1e9, V_rel 0.03 km/s streaming, khronon chargeless on FRW so geodesic): r_cap {iso_rcap:.1e} pc -> RAR kept")
VS["satellites"] = {f: {"B0": sat[f], "z": sat[f][0] / sat[f][1], "class": "FAIL" if sat[f][0] / sat[f][1] > 3 else "PASS"} for f in FOOT}
VS["coma"] = {f: {"dex": coma[f]["dex"], "z_sys": coma[f]["z_sys"], "class": "FAIL" if coma[f]["z_sys"] > 3 else "PASS"} for f in FOOT}
VS["tdg"] = {f: {"rbar": tdg[f]["rbar"], "se": tdg[f]["se"], "class": "PASS" if abs(tdg[f]["rbar"]) < 2 * tdg[f]["se"] else "FAIL"} for f in FOOT}
for f in FOOT:
    P(f"   [{f}] satellites (dust-free, U1 B0) {sat[f][0]:+.2f} +- {sat[f][1]:.2f} dex ({VS['satellites'][f]['class']}); "
      f"Coma {coma[f]['dex']:+.2f} dex z_sys {coma[f]['z_sys']:.1f} ({VS['coma'][f]['class']}); "
      f"TDG {tdg[f]['rbar']:+.3f} +- {tdg[f]['se']:.3f} ({VS['tdg'][f]['class']})")
RES["VS"] = VS

P("\n--- N4 (g, reported): gas loss needed if satellites keep only released FREE dust (held part stripped, eps = 1) ---")
X1cls = {"MW classical": (0.28, 0.24), "MW ultra-faint": (0.63, 0.59), "bright M31": (0.25, 0.21), "M31 others": (0.64, 0.59)}
N4 = {}
for nm, (dc, da) in X1cls.items():
    N4[nm] = {}
    for foot, D in (("canonical", dc), ("alt", da)):
        fz = 1 - 10 ** (-2 * D)
        ff_ = 1 - (1 + 10 ** D) ** -2
        N4[nm][foot] = {"Delta": D, "lost_Zstar": fz, "lost_free_only": ff_}
    P(f"   {nm:15s}: Z* (owned held + free) lost {N4[nm]['canonical']['lost_Zstar']:.2f} / {N4[nm]['alt']['lost_Zstar']:.2f}; "
      f"free-only lost {N4[nm]['canonical']['lost_free_only']:.3f} / {N4[nm]['alt']['lost_free_only']:.3f}")
u1rows = list(csv.DictReader(open(os.path.join(R, "U1_v3_dust_content/u1_satellites_per_system.csv"))))
leoT = {rw["footing"]: rw for rw in u1rows if rw["name"] == "Leo T"}
for f in FOOT:
    if f in leoT:
        P(f"   Leo T [{f}] (gas-rich, no release): LIT/VS Delta {float(leoT[f]['Delta_B0']):+.3f} dex; "
          f"MS acceleration-stripping Delta {float(leoT[f]['Delta_B1_MS']):+.3f} dex (U1 csv)")
RES["N4"] = N4
RES["LeoT"] = {f: {"LIT_B0": float(leoT[f]["Delta_B0"]), "MS_B1": float(leoT[f]["Delta_B1_MS"])} for f in leoT}

# =====================================================================================================================
# PART C: candidate scores (frozen rule)
# =====================================================================================================================
P("\n--- candidate scores (M1a OWN, M1b slope, M2 TDG/DF, M3 isolated + merged, M4 Cassini, M5 health, M6 s=1, M7 constants, M8 action) ---")
C = {
 "a1 drag":            dict(M1a="FAIL (K2/K4/K5: internal term, eps = 1)", M1b="PASS trivially (Newtonian), amplitude FAIL +2.0 dex",
                            M2="PASS", M3="FAIL (rotating discs: drag term nonzero, new term in the law)", M4="not reached",
                            M5="FAIL (K9: charge re-routed, rho < 0 where rho = 0)", M6="PASS", M7="FAIL (+1: beta)", M8="PASS",
                            cls="EXCLUDED BY THEOREM"),
 "a2 alignment":       dict(M1a="FAIL (K2/K4/K5)", M1b="n/a", M2="PASS", M3="FAIL (K7: no solution in discs)", M4="not reached",
                            M5="FAIL (over-determined)", M6="PASS", M7="PASS", M8="PASS", cls="EXCLUDED BY THEOREM"),
 "a3 gate |Phi_int|>|Phi_ext|": dict(M1a="FAIL", M1b="n/a", M2="PASS", M3="n/a", M4="n/a", M5="n/a", M6="PASS", M7="PASS",
                            M8="FAIL (Phi_int not a local field, K1); local proxies reduce to a1/a2", cls="NOT VIABLE"),
 "b CM-frame hold":    dict(M1a="FAIL (single Xi: K2/K4/K5) unless the domain's Xi is a separate field (-> e)", M1b="n/a", M2="PASS",
                            M3="PASS (isolated, single owner)", M4="not reached", M5="n/a", M6="PASS", M7="PASS",
                            M8="FAIL (X_q = centroid of a domain: non-local)", cls="EXCLUDED BY THEOREM"),
 "c MS mean-flow khronon": dict(M1a="FAIL (same-point + K2/K4/K5, eps = 1)", M1b="n/a", M2="PASS", M3="FAIL (K7: mean flow not curl-free in discs)",
                            M4="not reached", M5="n/a", M6="PASS", M7="PASS", M8="FAIL (posited particles; slaving has no action)",
                            cls="EXCLUDED BY THEOREM"),
 "d formation memory": dict(M1a="FAIL (K10: no memory variable)", M1b="n/a", M2="PASS", M3="PASS", M4="PASS", M5="PASS", M6="PASS",
                            M7="PASS", M8="PASS", cls="EXCLUDED BY THEOREM"),
 "e per-owner khronons": dict(M1a="PASS only if the exterior label flow free-falls (eps = 0); hovering exterior gives eps = 1",
                            M1b="PASS (no EFE in the owned frame)", M2="PASS (labels from formation)",
                            M3="FAIL (K6: labels never merge; N-label floor x = N-1, capped over-hold sqrt(N))",
                            M4="PASS", M5="FAIL (K11: free-falling exterior label flows caustic at the host centre)", M6="PASS",
                            M7="PASS (no continuous constant; one field per owner)", M8="PASS (local, variational)",
                            cls="EXCLUDED BY THEOREM"),
 "f e + exchange V":   dict(M1a="as e", M1b="as e", M2="PASS", M3="open", M4="PASS", M5="FAIL (K8: opposite-sign pair creation)",
                            M6="PASS", M7="FAIL (+1 function V)", M8="PASS", cls="NOT VIABLE"),
}
for k, v in C.items():
    P(f"   {k:28s} -> {v['cls']}")
    for m in ("M1a", "M1b", "M2", "M3", "M4", "M5", "M6", "M7", "M8"):
        P(f"        {m}: {v[m]}")
RES["candidates"] = C
classes = [v["cls"] for v in C.values()]
overall = "DERIVED" if "DERIVED" in classes else ("CONDITIONAL" if "CONDITIONAL" in classes else "NO-GO")
RES["overall"] = overall
P(f"\nOVERALL (frozen rule): {overall}. Blocking must-keep: M3 - the host's own phantom inside the satellite's orbit "
  f"(its Gauss field anti-weights any held phase, eps = 1 for a held host; OWN needs phi <= {N2['canonical'][1]['phi_max']:.3f} "
  f"of it at 100 kpc, v_c {N2['canonical'][1]['vc_law_kms']:.0f} -> {N2['canonical'][1]['vc_at_phi_kms']:.0f} km/s), "
  f"with alpha = 1 forced by the same law; labelled escapes fail M3(ii) (no merging) and M5 (exterior caustics).")

P("\nVS tiles (gamma_L removed): Cassini " + VS["Cassini"] + "; outer globulars " + VS["globulars"]
  + "; WB Newtonian (prediction; DR4 decides); TDG/DF2/DF4 " + VS["tdg"]["canonical"]["class"]
  + " (U1 B0); isolated RAR kept (r_cap >> R_last); satellites " + VS["satellites"]["canonical"]["class"]
  + "; Coma UDGs " + VS["coma"]["canonical"]["class"] + "; UMa group members DEPENDS (U1 F5).")
P("Constants if L* goes: kappa (FITTED) + cold abundance (FITTED initial condition) + the cold-sector rule (mu_K in v3, or Z*'s R1).")

ok_rss = rss_gb() < 1.0
check("K13", ok_rss, f"peak RSS {rss_gb():.3f} GB", "< 1 GB")
RES["checks"] = CHECKS
RES["runtime_s"] = time.time() - T0
RES["peak_rss_GB"] = rss_gb()
json.dump(RES, open(os.path.join(HERE, f"o1_ownership_action_results{TAG}.json"), "w"), indent=1, default=str)
npass = sum(1 for c in CHECKS.values() if c["pass"])
P(f"\nO1 {'MUTATE' if MUT else 'main'} COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time() - T0:.0f} s]")
OUT.close()
sys.exit(0 if npass == len(CHECKS) else 1)
