#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MS1 -- THE GATE VARIED ON V0's CHASSIS: WHICH SWITCH VARIABLE KEEPS THE DARK COMPONENT KERNEL-INVISIBLE?

WHY.  The construction's dark component is kernel-invisible (L353): the MOND kernel reads the baryons' field only, so by
reciprocity the dark component feels Newtonian gravity only.  CV1 (real_research/chk_v0_2026, commit cc2b55bbb) carries
that property to the region kernel -- but with the gate f PRESCRIBED.  CV3 (the gate varied as an action term) is
"awaiting the gate functional", and the author's 2026-09-26 decision opened every reading of the switch variable as its
own door.  Once f = W(U) is varied, whatever U reads feels the gate: if U reads the dark component's density (directly,
or through the curvature it sources), the dark component feels a force at every region's edge and is no longer
kernel-invisible.  This lane derives, on CV1's own Lagrangian, which readings keep reciprocity exact.

THE LAGRANGIAN: CV1's, term for term (C-H's chassis, the region kernel, the region field, L353's pair with its projected
source, L361's web self-term), with the prescribed gate replaced by f = W(U) and the screening mass M^2 = m^2 (1 - f)
varying with it, as CV1 defines it.  One dimension, S = 1 (CV1 A1's reduction), a concrete non-trivial kernel (CV1's
q = c1 s^(3/2) + d1 log(1 + s)) and a generic gate function W.
THE FOUR DOORS (switch variables; C > 0 is the gate's normalisation, (3/2)[Omega_L/Omega_L0]^p / rho_crit):
  (a) curvature    U = C lap Phi            the leaf curvature, the reading CV1 A6 uses (DE1/DE2's upper branch reads
                                            the same density: baryons + dark component + phantom)
  (b) matter       U = C (rho_b + rho_d)    the particle-mesh runs' matter-only reading (L377, L380, L388)
  (c) MOND sector  U = C lap(Phi - v)       Phi minus the dark component's own potential v (L353's pair):
                                            lap(Phi - v) = 4 pi G (rho_b + <rho_d>) + lap(f P) + (the gate's own term),
                                            i.e. the baryons and their phantom; the carrier enters only as its mean
  (d) baryons      U = C rho_b              the baryons alone

CHECKS
  A1 CONTROL [sympy]: with f prescribed, CV1's six field equations are reproduced (zero residual) -- the chassis is CV1's.
  A2 [sympy] for each door, the Euler-Lagrange equations with f = W(U) varied have the stated closed form (zero residual):
       dPhi: lap u = 4 pi G rho - lap(C W'(U) B)/2          (doors a, c)   /   lap u = 4 pi G rho     (doors b, d)
       dv:   lap lam = -lap(f Psi) + lap(C W'(U) B)         (door c)       /   lap lam = -lap(f Psi)  (doors a, b, d)
       du, dlam, dw, dPsi: CV1's, unchanged
     with B = 8 pi G dL/df = a0^2 q - Psi lap(u - v) + m^2 Psi w + sigma m^2 w^2 (sympy's, not hand-typed).
  A3 THE RECIPROCITY TEST [sympy]: on the integrated solution (u = u_N + gate term, v = v_N, Phi = u + f Psi/2, lam as
     above), the potential the dark component feels, V_d = -dL/drho_d, minus the Newtonian potential u_N of all matter:
       (c) and (d): V_d - u_N = 0 identically -- the dark component stays exactly Newtonian with the gate varied;
       (a): -(1/2) C W'(U) B;   (b): -C W'(U) B/(8 pi G)   -- a force at every region's edge, where W' != 0.
     The baryons' potential Phi carries the gate's term on doors (a) and (c) and -C W'(U) B/(8 pi G) on doors (b), (d):
     the edge layer is a property of the baryons on every door, of the dark component only on (a) and (b).
  A4 [the homogeneous zero, CV1 A6's requirement for every door] on flat FRW the contrast of door (c) is
     lap(Phi - v) - 4 pi G (<rho_b> + <rho_d>) = 0 and of door (d) rho_b - <rho_b> = 0, so W and all its derivatives
     vanish there (CV1's C-infinity gate): both readings keep the kernel out of the homogeneous background.
  N1 (numbers, both footings) the size of the leak on doors (a) and (b) in two spherical hosts, from A3's closed forms
     with the kernel term of B (a0^2 q, the term present for every sigma and m; CV1's sigma-layer adds to it): an L*
     KiDS lens at z = 0.25 and a flagship host at z = 2.5, at the linear vacuum gate (p = 1, x_c0 = 2.5), for gate
     widths Delta = 0.1-1 in ln U: the leaked force on the carrier as a fraction of its Newtonian gravity at the edge,
     and the depth of the edge well (the host sits in the mean density; its carrier is the untruncated NFW excess).
MUTATE=1 adds the carrier's density to the MOND-sector variable (U = C lap(Phi - v) + C rho_d): the leak must reappear on
door (c) and A3 must FAIL (rc = 1).

SCOPE.  Non-relativistic, one-dimensional symbolic reduction (CV1 A1's), S = 1; the numbers keep only the kernel term of
B and treat the carrier's response to the leaked potential as first order.  The construction's switch cell, trigger and
kick are untouched here; MS2 and MS3 score the door's phenomenology.

Run from the repository root:  python3 real_research/mond_sector_gate_2026/MS1_gate_variation_reciprocity.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "MS1", "MS1_gate_variation_reciprocity"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the carrier's density is added to the MOND-sector variable (door c); A3 must FAIL ***")

# ============================================================================================ the chassis (CV1's Lagrangian)
x = sp.symbols("x", real=True)
G_, a0_, c1, d1, m2, C = sp.symbols("G a0 c1 d1 m2 C", positive=True)
sig, rdbar = sp.symbols("sigma rhobar_d", real=True)
Phi, u, v, lam, w, Psi = [sp.Function(n)(x) for n in ("Phi", "u", "v", "lam", "w", "Psi")]
rb, rd = [sp.Function(n)(x) for n in ("rho_b", "rho_d")]
fP = sp.Function("f")(x)                                                    # CV1's prescribed gate
W = sp.Function("W")                                                        # a generic gate function
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)             # CV1's concrete kernel, q = Q - Z
qcp = lambda s: sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)
d_ = lambda F, n=1: sp.diff(F, x, n)
wp = d_(w); s_w = wp ** 2 / a0_ ** 2
EPG = 8 * sp.pi * G_


def lagrangian(f, M2):
    """CV1's L (chassis + region kernel + region field + L353's pair + web self-term), gate f, screening mass M2."""
    return (-(rb + rd) * Phi - (2 * d_(Phi) * d_(u) - d_(u) ** 2) / EPG
            + a0_ ** 2 * f * qc(s_w) / EPG
            + Psi * (d_(w, 2) - M2 * w - f * (d_(u, 2) - d_(v, 2))) / EPG
            + lam * (d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar)) / EPG
            - sig * M2 * w ** 2 / EPG)


FIELDS = (Phi, u, v, lam, w, Psi)


def EL_of(L):
    return {str(F_.func): sp.expand(sp.euler_equations(L, [F_], x)[0].lhs * EPG) for F_ in FIELDS}


# ============================================================================================ A1 control: CV1 reproduced
banner("A1  CONTROL: with f prescribed (and M^2 = m^2 (1 - f)), CV1's field equations are reproduced")
M2P = m2 * (1 - fP)
EL1 = EL_of(lagrangian(fP, M2P))
tgt1 = {
    "Phi": 2 * d_(u, 2) - EPG * (rb + rd),
    "lam": d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar),
    "Psi": d_(w, 2) - M2P * w - fP * (d_(u, 2) - d_(v, 2)),
    "w": d_(Psi, 2) - M2P * Psi - 2 * d_(fP * qcp(s_w) * wp) - 2 * sig * M2P * w,
    "u": 2 * d_(Phi, 2) - 2 * d_(u, 2) - d_(fP * Psi, 2),
    "v": d_(lam, 2) + d_(fP * Psi, 2),
}
dev1 = {k_: sp.simplify(EL1[k_] - tgt1[k_]) for k_ in tgt1}
for k_ in tgt1:
    P(f"    delta {k_:3s}: residual against CV1's field equation = {dev1[k_]}")
check("A1 CONTROL: CV1's six Euler-Lagrange equations (f prescribed, M^2 = m^2(1 - f)) are reproduced with zero residual",
      {k_: str(v_) for k_, v_ in dev1.items()}, all(v_ == 0 for v_ in dev1.values()), load_bearing=False)

# B = 8 pi G dL/df, computed by sympy from CV1's L (the f-linear coefficient, M^2 = m^2 (1 - f) included)
fs = sp.Symbol("fs")
B = sp.expand(sp.diff(lagrangian(fs, m2 * (1 - fs)), fs) * EPG)
P(f"    B = 8 pi G dL/df = {B}")
OUT["numbers"]["B"] = str(B)

# ============================================================================================ A2 the four doors, varied
banner("A2  THE GATE VARIED: f = W(U) on each door; the Euler-Lagrange equations in closed form")
xi = sp.Symbol("xi")
DOORS = {
    "a_curvature": C * d_(Phi, 2),
    "b_matter": C * (rb + rd),
    "c_mond_sector": C * (d_(Phi, 2) - d_(v, 2)) + (C * rd if MUTATE else 0),
    "d_baryons": C * rb,
}
A2, SOL = {}, {}
for door, U in DOORS.items():
    f = W(U)
    L = lagrangian(f, m2 * (1 - f))
    EL = EL_of(L)
    Wp = sp.Subs(sp.Derivative(W(xi), xi), xi, U)                           # W'(U)
    BW = C * Wp * B                                                          # C W'(U) B
    reads_phi = door in ("a_curvature", "c_mond_sector")
    reads_v = door == "c_mond_sector"
    tgt = {
        "Phi": 2 * d_(u, 2) - EPG * (rb + rd) + (d_(BW, 2) if reads_phi else 0),
        "lam": d_(v, 2) - 4 * sp.pi * G_ * (rd - rdbar),
        "Psi": d_(w, 2) - m2 * (1 - f) * w - f * (d_(u, 2) - d_(v, 2)),
        "w": d_(Psi, 2) - m2 * (1 - f) * Psi - 2 * d_(f * qcp(s_w) * wp) - 2 * sig * m2 * (1 - f) * w,
        "u": 2 * d_(Phi, 2) - 2 * d_(u, 2) - d_(f * Psi, 2),
        "v": d_(lam, 2) + d_(f * Psi, 2) - (d_(BW, 2) if reads_v else 0),
    }
    dev = {k_: sp.simplify(sp.expand(EL[k_] - tgt[k_])) for k_ in tgt}
    A2[door] = dev
    P(f"    door {door:14s}: residuals " + ", ".join(f"{k_} {dev[k_]}" for k_ in tgt))
    SOL[door] = dict(L=L, f=f, BW=BW, reads_phi=reads_phi, reads_v=reads_v)
a2_ok = all(v_ == 0 for dev in A2.values() for v_ in dev.values())
check("A2 for every door the varied Euler-Lagrange equations have the stated closed form (zero residual): the gate adds "
      "lap(C W' B) to the Phi equation when U reads lap Phi, and to the v equation when U reads lap v",
      {d: {k_: str(v_) for k_, v_ in dev.items()} for d, dev in A2.items()}, a2_ok)

# ============================================================================================ A3 the reciprocity test
banner("A3  THE RECIPROCITY TEST: the potential the dark component feels, minus the Newtonian potential of all matter")
uN, vN = sp.Function("u_N")(x), sp.Function("v_N")(x)                     # lap u_N = 4 pi G rho; lap v_N = 4 pi G (rho_d - <rho_d>)
Bs, Wps, fsym = sp.symbols("B Wp fval")                                     # the gate term's value and the gate's value on the solution
A3 = {}
for door, S_ in SOL.items():
    L = S_["L"]
    # the integrated solution (harmonic pieces fixed by the boundary conditions, CV1's convention)
    gate_u = -sp.Rational(1, 2) * C * Wps * Bs if S_["reads_phi"] else 0
    u_s = uN + gate_u
    Phi_s = u_s + fsym * Psi / 2
    lam_s = -fsym * Psi + (C * Wps * Bs if S_["reads_v"] else 0)
    # V_d = -dL/d rho_d (its coupling: -rho_d Phi - rho_d lam/2, plus the gate wherever U reads rho_d)
    rds = sp.Symbol("rds")
    Vd = -sp.diff(L.subs(rd, rds), rds)
    Vd = Vd.replace(lambda e: isinstance(e, sp.Subs), lambda e: Wps)                     # W'(U) -> Wp
    Vd = Vd.replace(lambda e: isinstance(e, sp.Function) and e.func == W, lambda e: fsym)  # W(U) -> its value
    Vd = sp.expand(Vd.subs(rds, rd).subs({Phi: Phi_s, lam: lam_s}))
    A3[door] = sp.simplify(sp.expand(Vd - uN))
    P(f"    door {door:14s}: V_d - u_N = {A3[door]}")
ok_c = A3["c_mond_sector"] == 0
ok_d = A3["d_baryons"] == 0
ok_a = sp.simplify(A3["a_curvature"] + sp.Rational(1, 2) * C * Wps * Bs) == 0
lb = sp.simplify(sp.expand(A3["b_matter"] + C * Wps * B / EPG))                          # door (b): -C W'(U) (dL/df)
ok_b = lb == 0
P(f"    door b_matter: V_d - u_N + C W'(U) B/(8 pi G) = {lb}")
OUT["numbers"]["A3_leaks"] = {k_: str(v_) for k_, v_ in A3.items()}
check("A3 THE RECIPROCITY TEST: with the gate varied, the dark component's potential is EXACTLY Newtonian (V_d = u_N) on "
      "the MOND-sector door (c) and the baryons door (d), and carries the gate's edge term on the curvature door (a), "
      "-(1/2) C W'(U) B, and the matter door (b), -C W'(U) B/(8 pi G)",
      f"(c) {A3['c_mond_sector']}; (d) {A3['d_baryons']}; (a) {A3['a_curvature']}; (b) matches -C W' B/8piG: {ok_b}",
      ok_c and ok_d and ok_a and ok_b,
      "a switch variable that reads the carrier -- directly (matter) or through the curvature it sources -- hands the "
      "gate's variation to the carrier; one that reads only the baryons and their phantom (lap(Phi - v)) does not")

# ============================================================================================ A4 the homogeneous zero
banner("A4  THE HOMOGENEOUS ZERO (CV1 A6's requirement for every door)")
# flat FRW, Newtonian gauge on the expanding background: the peculiar potentials vanish, rho = <rho>.  Door (c)'s contrast:
rbb, rdb = sp.symbols("rhobar_b rhobar_d", positive=True)
lap_u_hom = 4 * sp.pi * G_ * (rbb + rdb)                                     # lap u = 4 pi G rho (the mean belongs to FRW)
lap_v_hom = 4 * sp.pi * G_ * (rdb - rdb)                                     # the pair's projected source
lap_fP_hom = 0                                                               # no gate, no phantom on the background
contrast_c = sp.simplify(lap_u_hom + lap_fP_hom - lap_v_hom - 4 * sp.pi * G_ * (rbb + rdb))
contrast_d = sp.simplify(rbb - rbb)
P(f"    door (c) contrast on flat FRW: lap(Phi - v) - 4 pi G (<rho_b> + <rho_d>) = {contrast_c};  door (d): rho_b - <rho_b> = {contrast_d}")
check("A4 on flat FRW the contrast of the MOND-sector door and of the baryons door vanishes, so CV1's C-infinity gate and "
      "all its derivatives are zero there: the homogeneous background is off-plateau for both",
      f"(c) {contrast_c}; (d) {contrast_d}", contrast_c == 0 and contrast_d == 0, load_bearing=False)

# ============================================================================================ N1 the size of the leak
banner("N1  THE SIZE OF THE LEAK ON DOORS (a) AND (b): two spherical hosts at the linear vacuum gate (p = 1, x_c0 = 2.5)")
# units: kpc, km/s, Msun
Gk = 4.30091e-6                                                             # kpc (km/s)^2 / Msun
ACC = 3.0857e19 / 1e6                                                       # m/s^2 -> (km/s)^2/kpc factor: a [m/s^2] * ACC
A0 = {"canonical": 9.3619e-11 * ACC, "alt": 1.1279e-10 * ACC}                # (km/s)^2 / kpc
H0 = 67.36 / 1000.0                                                         # km/s/kpc
OMG = 0.3138                                                                 # the gate's background (L359/L347)
FB = 0.02237 / (0.02237 + 0.1200)
E2 = lambda z: OMG * (1 + z) ** 3 + 1 - OMG
rho_crit = lambda z: 3 * (H0 ** 2 * E2(z)) / (8 * math.pi * Gk)            # Msun/kpc^3
rho_bar = lambda z: OMG * (1 + z) ** 3 * rho_crit(0.0)
nu = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y)))                       # nu_RAR (= nu_mono below y = 2.337, XC4)


def qB(y, a0):
    """the kernel term of B: a0^2 q(y^2) = a0^2 * 2 int_0^y (nu(s) - 1) s ds (q'(Z) = nu(sqrt Z) - 1)."""
    return a0 ** 2 * 2 * quad(lambda s: (nu(s) - 1) * s, 0.0, y, limit=200)[0]


def nfw(Mh, c, z):
    r200 = (3 * Mh / (4 * math.pi * 200 * rho_crit(z))) ** (1 / 3); rs = r200 / c
    mfn = math.log(1 + c) - c / (1 + c); rho_s = Mh / (4 * math.pi * rs ** 3 * mfn)
    dens = lambda r: rho_s / ((r / rs) * (1 + r / rs) ** 2)
    mass = lambda r: Mh * (math.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / mfn
    return dens, mass, r200


def gate_W(lnU, lnU0, D):
    """CV1's C-infinity gate W(t) = g(t)/(g(t) + g(1 - t)), g = exp(-1/t), on t = (ln U - ln U0 + D)/(2 D); and dW/d lnU."""
    t = (lnU - lnU0 + D) / (2 * D)
    g = lambda s: math.exp(-1.0 / s) if s > 0 else 0.0
    if t <= 0: return 0.0, 0.0
    if t >= 1: return 1.0, 0.0
    W_ = g(t) / (g(t) + g(1 - t))
    h = 1e-6
    t1, t2 = min(t + h, 1 - 1e-12), max(t - h, 1e-12)
    dWdt = (g(t1) / (g(t1) + g(1 - t1)) - g(t2) / (g(t2) + g(1 - t2))) / (t1 - t2)
    return W_, dWdt / (2 * D)


HOSTS = {"KiDS L* lens, z = 0.25": dict(z=0.25, Mb=6e10, Mh=1.5e12, c=8.0, S=1.0),
         "flagship host, z = 2.5": dict(z=2.5, Mb=1e11, Mh=1.6e12, c=4.0, S=0.06)}
P_GATE, XC0 = 1.0, 2.5
N1 = {}
for hname, Hh in HOSTS.items():
    z = Hh["z"]; gatefac = (1.0 / E2(z)) ** P_GATE * 1.0                     # [Omega_L(z)/Omega_L0]^p = E(z)^(-2p)
    dens, mass, r200 = nfw(Hh["Mh"] * (1 - FB), Hh["c"], z)
    for foot, a0 in A0.items():
        rr = np.geomspace(5.0, 30000.0, 6000)
        gN = Gk * Hh["Mb"] / rr ** 2                                         # the kernel's argument: in-region baryons (point mass)
        Mph = np.array([(nu(g / a0) - 1) * Hh["Mb"] for g in gN])
        rho_ph = np.gradient(Mph, rr) / (4 * math.pi * rr ** 2)
        # the host embedded in the mean: the carrier's (untruncated) NFW excess on top of rho_bar; point baryons off-grid
        rho_c = np.array([Hh["S"] * dens(r) for r in rr])                    # the carrier's density contrast
        con_a = rho_c + rho_ph                                                # door (a): dynamical density contrast
        con_b = rho_c                                                        # door (b): matter density contrast
        Ua = 1.5 * con_a / rho_crit(z) * gatefac
        Ub = 1.5 * con_b / rho_crit(z) * gatefac
        gcN = np.array([Gk * (Hh["Mb"] + Hh["S"] * mass(r)) / r ** 2 for r in rr])   # the carrier's Newtonian pull
        qv = np.array([qB(g / a0, a0) for g in gN])
        row = {}
        for D in (0.1, 0.25, 0.5, 1.0):
            for door, U_, rho_read in (("a", Ua, con_a), ("b", Ub, con_b)):
                if not np.any(U_ > XC0):
                    row[f"{door}/{D}"] = None; continue
                dW = np.array([gate_W(math.log(max(Uv, 1e-300)), math.log(XC0), D)[1] if Uv > 0 else 0.0 for Uv in U_])
                # A3's closed forms in 3-D, contrast reading U = C (rho_read): C W'(U) = (dW/dlnU)/rho_read, so on both doors
                # dV = -(dW/dlnU) B / (8 pi G rho_read), rho_read = the door's own density contrast (a: dynamical, b: matter)
                dV = -(dW * qv) / (8 * math.pi * Gk * np.maximum(rho_read, 1e-300))
                F = -np.gradient(dV, rr)
                if dW.max() <= 0:
                    row[f"{door}/{D}"] = None; continue
                layer = dW > 1e-3 * dW.max()
                ratio = float(np.max(np.abs(F[layer]) / gcN[layer]))
                i_e = int(np.argmax(dW))
                depth = float(np.min(dV))
                v2 = Gk * (Hh["Mb"] + Hh["S"] * mass(rr[i_e])) / rr[i_e]
                row[f"{door}/{D}"] = dict(r_edge_kpc=float(rr[i_e]), force_ratio_max=ratio, well_depth_kms2=depth,
                                          depth_over_vc2=abs(depth) / v2)
        N1[f"{hname}/{foot}"] = row
        for door in ("a", "b"):
            P(f"    {hname:24s} {foot:9s} door ({door}): " + "; ".join(
                (f"D = {D}: edge {row[f'{door}/{D}']['r_edge_kpc']:6.0f} kpc, max |F_leak|/g_N {row[f'{door}/{D}']['force_ratio_max']:.3f}, "
                 f"well {row[f'{door}/{D}']['depth_over_vc2']:.4f} v_c^2") if row[f"{door}/{D}"] else f"D = {D}: no region"
                for D in (0.1, 0.25, 0.5, 1.0)))
OUT["numbers"]["N1"] = N1
vals = [v_["force_ratio_max"] for r_ in N1.values() for v_ in r_.values() if v_]
check("N1 (reported) the leaked edge force on the carrier, doors (a) and (b), kernel term of B only, is non-zero in every "
      "host with a region; doors (c) and (d) leak nothing by A3",
      f"max |F_leak|/g_N over hosts, footings, widths: {max(vals):.3f}; min {min(vals):.3g}", len(vals) > 0 and min(vals) > 0,
      load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P("""  Varying the gate on CV1's own Lagrangian decides the switch-variable doors by reciprocity alone.  A switch that reads the
  dark component -- directly (the particle-mesh runs' matter-only reading) or through the curvature it sources (the leaf
  curvature, DE1/DE2's upper branch) -- makes the dark component feel the gate's variation at every region's edge, so it
  is no longer kernel-invisible once f is an action term.  Two readings keep L353's reciprocity exact with the gate varied:
  the MOND-sector density lap(Phi - v) = 4 pi G (rho_b + <rho_d>) + lap(f P) + ... (baryons and their phantom; the carrier
  only as its mean), and the baryons alone.  Their homogeneous backgrounds are off-plateau (CV1 A6).  On every door the
  BARYONS carry the gate's edge term (CV1's sigma layer is one part of it).  The leak on doors (a) and (b) is NOT small
  (N1, kernel term only): for gate widths Delta = 0.1-1 in ln U the edge force on the carrier is 0.06-6x its Newtonian
  gravity for an L* KiDS lens on the curvature door and 0.6-60x on the matter door, and at z = 2.5 around a flagship host
  1.5-150x (well 0.3-3 v_c^2) and 23-2300x (well 4-41 v_c^2).  A varied gate on those doors would pile the carrier into
  every region's edge -- physics the prescribed-mask runs (L377-L388) do not contain.  MS2 scores the MOND-sector door's
  phenomenology; CV3 (the gate varied) can take lap(Phi - v) as its functional and keep the kernel-invisible carrier.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
