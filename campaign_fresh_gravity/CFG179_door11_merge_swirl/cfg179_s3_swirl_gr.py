#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG179 S3 -- Q-swirl: the swirled river's law, and GR's own swirl (frame dragging) for a Milky-Way-like disc
(FROZEN_QUESTION.md W1-W4).  Seconds.

W1  the river law with vorticity: a rigidly rotating flow reproduces the rotating-frame Coriolis and centrifugal terms.
W2  a steady swirl v = lambda_c V(R) phi-hat: prograde and retrograde tracers feel opposite radial pushes, contrast
    2 lambda_c (1 + s) V^2/R; no force on vertical motion.
W3  GR (1PN): g_0j = -4 U_j/c^3 -> L carries -(4/c^2) U.v -> a_GM = -(4/c^2) u x curl U: a river with shift v_s = 4U/c^2.
W4  numbers: thin exponential disc, M_b = 6e10 Msun, R_d = 3 kpc (2.5, 3.5), V_s(R) = 220 R/sqrt(R^2 + 1) km/s, at z = h =
    0.05 kpc (0.2), R = 8.2 and 10 kpc, prograde tracer at 220 km/s.

MUTATE=1: the vorticity term is dropped (an irrotational river): the W2 contrast and a_GM vanish; the headlines must fail.
"""
import math
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import ellipk, ellipe, i0, i1, k0, k1
from cfg179_common import Run, MUTATE, KPC, YR, MAS_PER_RAD

R = Run("cfg179_s3_swirl_gr")
CURL = 0.0 if MUTATE else 1.0
R.P(f"vorticity term weight = {CURL}  ({'MUTATE: irrotational river' if MUTATE else 'the full river law'})")

# =============================================================================================== W1
R.banner("W1  the river law with vorticity: rigid rotation")
x, y, z, W = sp.symbols("x y z Omega", real=True)
X = sp.Matrix([x, y, z])
Om = sp.Matrix([0, 0, W])
xd = sp.Matrix(sp.symbols("xd yd zd", real=True))


def river_acc(vfield, xdot, curl_w=1):
    J = vfield.jacobian([x, y, z])
    conv = J * vfield                                                   # (v.grad) v  (steady)
    curl = sp.Matrix([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])
    w_ = xdot - vfield
    return sp.simplify(conv - curl_w * w_.cross(curl))


v_rig = Om.cross(X)
a_rig = river_acc(v_rig, xd, CURL)
a_rot = 2 * Om.cross(xd) - Om.cross(Om.cross(X))                     # coordinates rotating at -Omega
ok_w1 = sp.simplify(a_rig - a_rot) == sp.zeros(3, 1)
R.check("W1 a rigidly rotating flow v = Omega x r gives exactly the rotating-frame law xddot = 2 Omega x xdot - Omega x (Omega x r) "
        "(the river's vorticity 2 Omega IS the Coriolis term); a body at rest in the flow is carried round (centripetal "
        "Omega x (Omega x r))", ok_w1, f"residual {list(sp.simplify(a_rig - a_rot))}")

# =============================================================================================== W2
R.banner("W2  a disc swirling the river: v = lambda_c V(R) phi-hat")
lam, u, wz, Rr = sp.symbols("lambda_c u w_z R", real=True)
Vf = sp.Function("V")
rr = sp.sqrt(x**2 + y**2)
v_sw = lam * Vf(rr) * sp.Matrix([-y / rr, x / rr, 0])
pt = {x: Rr, y: 0, z: 0}
a_tr = river_acc(v_sw, sp.Matrix([0, u, 0]), CURL).subs(pt)
a_tr = sp.simplify(a_tr.subs(sp.Abs(Rr), Rr))
s_ = sp.Symbol("s")
Vp = sp.Symbol("Vprime")
a_tr = sp.simplify(a_tr.doit().subs(sp.Derivative(Vf(Rr), Rr), Vp).subs(sp.Subs(sp.Derivative(Vf(x), x), x, Rr), Vp))
V0 = sp.Symbol("V0", positive=True)
aR = sp.simplify(a_tr[0].subs({Vf(Rr): V0}).subs(Vp, s_ * V0 / Rr))
claim = -lam**2 * V0**2 / Rr - (u - lam * V0) * lam * (V0 / Rr) * (1 + s_)
contrast = sp.simplify(aR.subs(u, -V0) - aR.subs(u, V0))
R.P(f"    a_R(tracer at u phi-hat) = {sp.factor(aR)}")
R.P(f"    retrograde minus prograde = {sp.factor(contrast)}")
ok_w2 = sp.simplify(aR - claim) == 0 and sp.simplify(contrast - 2 * lam * (1 + s_) * V0**2 / Rr) == 0
R.check("W2a [HEADLINE] a_R = -lambda_c^2 V^2/R - (u - lambda_c V) lambda_c (V/R)(1 + s): prograde (u = V) and retrograde (u = -V) "
        "tracers differ by 2 lambda_c (1 + s) V^2/R; for a flat curve prograde gets -lambda_c V^2/R (inward) and retrograde "
        "+lambda_c V^2/R (outward)", ok_w2,
        f"a_R(prograde, s=0) = {sp.simplify(aR.subs({u: V0, s_: 0}))}; a_R(retrograde, s=0) = {sp.simplify(aR.subs({u: -V0, s_: 0}))}")
a_vert = river_acc(v_sw, sp.Matrix([0, lam * Vf(rr), wz]), CURL).subs(pt)
R.check("W2b a vertical vorticity exerts no force on vertical motion: the tracer's z-acceleration is zero for any w_z "
        "(a swirl changes the radial force only)", sp.simplify(a_vert[2]) == 0, f"a_z = {sp.simplify(a_vert[2])}",
        load_bearing=False)
R.P("    reading: lambda_c = 1 means the river co-rotates with the stars and carries them (it supplies all of V^2/R): a "
    "prescribed swirl is a restatement of the rotation curve, as door 11 warns for prescribed flows.")

# =============================================================================================== W3
R.banner("W3  GR's swirl: the 1PN gravitomagnetic term is a river shift v_s = 4U/c^2")
cc = sp.Symbol("c", positive=True)
U = [sp.Function(n)(x, y, z) for n in ("U1", "U2", "U3")]
t = sp.Symbol("t")
q = [sp.Function(n)(t) for n in ("qx", "qy", "qz")]
qd = [sp.diff(qq, t) for qq in q]
Uq = [Ui.subs({x: q[0], y: q[1], z: q[2]}) for Ui in U]
Lgm = sum(v_**2 for v_ in qd) / 2 - CURL * 4 / cc**2 * sum(Uq[i] * qd[i] for i in range(3))
EL = [sp.diff(sp.diff(Lgm, qd[i]), t) - sp.diff(Lgm, q[i]) for i in range(3)]
qdd = [sp.diff(qq, t, 2) for qq in q]
sol = sp.solve(EL, qdd, dict=True)[0]
Um = sp.Matrix(U)
curlU = sp.Matrix([sp.diff(U[2], y) - sp.diff(U[1], z), sp.diff(U[0], z) - sp.diff(U[2], x), sp.diff(U[1], x) - sp.diff(U[0], y)])
vv = sp.Matrix(sp.symbols("vx vy vz", real=True))
claim3 = -(4 / cc**2) * vv.cross(curlU)
ok3 = True
for i in range(3):
    lhs = sol[qdd[i]].subs({qd[k]: vv[k] for k in range(3)}).subs({q[0]: x, q[1]: y, q[2]: z})
    ok3 &= sp.simplify(sp.expand(lhs - claim3[i])) == 0
R.check("W3 from g_0j = -4U_j/c^3 the test-body Lagrangian carries -(4/c^2) U.v, and its Euler-Lagrange force is "
        "a_GM = -(4/c^2) v x (curl U) -- the river law's -w x curl(v_s) with shift v_s = 4U/c^2, U_j = G Int rho v_j/|x-x'|",
        ok3, "Euler-Lagrange solved and compared component by component (static U)")

# =============================================================================================== W4
R.banner("W4  GR's swirl for a Milky-Way-like disc (thin exponential disc, prograde tracer at 220 km/s)")
Gk = 4.30091727e-6                                                  # kpc (km/s)^2 / Msun
C_KMS = 299792.458
KMS_KPC_TO_MASYR = 1e3 / KPC * YR * MAS_PER_RAD
MB, VS0, RC = 6e10, 220.0, 1.0


def J1(Rv, a, zz):
    k2 = 4 * Rv * a / ((Rv + a) ** 2 + zz ** 2)
    k = math.sqrt(k2)
    return 4.0 / (k * math.sqrt(Rv * a)) * ((1 - k2 / 2) * ellipk(k2) - ellipe(k2))


def J0(Rv, a, zz):
    k2 = 4 * Rv * a / ((Rv + a) ** 2 + zz ** 2)
    return 4.0 * ellipk(k2) / math.sqrt((Rv + a) ** 2 + zz ** 2)


# control: ring kernels against direct quadrature
dev = 0.0
for Rv, a, zz in [(8.2, 5.0, 0.05), (8.2, 8.0, 0.05), (10.0, 20.0, 0.2), (3.0, 12.0, 1.0)]:
    n1 = quad(lambda p: math.cos(p) / math.sqrt(Rv**2 + a**2 - 2 * Rv * a * math.cos(p) + zz**2), 0, 2 * math.pi,
              points=[0.0], limit=400, epsabs=0, epsrel=1e-12)[0]
    n0 = quad(lambda p: 1.0 / math.sqrt(Rv**2 + a**2 - 2 * Rv * a * math.cos(p) + zz**2), 0, 2 * math.pi,
              points=[0.0], limit=400, epsabs=0, epsrel=1e-12)[0]
    dev = max(dev, abs(J1(Rv, a, zz) / n1 - 1), abs(J0(Rv, a, zz) / n0 - 1))
R.check("C1 CONTROL: the ring kernels Int cos(phi') dphi'/|x-x'| = (4/(k sqrt(R R')))[(1 - k^2/2)K - E] and Int dphi'/|x-x'| = "
        "4K/sqrt((R+R')^2 + z^2) agree with direct quadrature to 1e-8 (4 points)", dev < 1e-8, f"max relative deviation {dev:.1e}")


def disc_fields(Rv, Rd, h):
    Sig0 = MB / (2 * math.pi * Rd**2)
    Sig = lambda a: Sig0 * math.exp(-a / Rd)
    Vs = lambda a: VS0 * a / math.sqrt(a * a + RC * RC)
    top = 40 * Rd

    def I(fun):
        return sum(quad(fun, lo, hi, limit=800, epsabs=0, epsrel=1e-11)[0]
                   for lo, hi in [(1e-9, Rv - 0.5), (Rv - 0.5, Rv), (Rv, Rv + 0.5), (Rv + 0.5, top)])

    Uphi = lambda RR: Gk * I(lambda a: Sig(a) * Vs(a) * a * J1(RR, a, h))
    Phi = lambda RR: -Gk * I(lambda a: Sig(a) * a * J0(RR, a, h))
    d = 1e-3
    U0 = Uphi(Rv)
    Bz = ((Rv + d) * Uphi(Rv + d) - (Rv - d) * Uphi(Rv - d)) / (2 * d) / Rv       # (1/R) d(R U_phi)/dR
    gN = -(Phi(Rv + d) - Phi(Rv - d)) / (2 * d)                                   # radial, negative = inward
    return U0, Bz, gN, Sig0


def freeman_gN(Rv, Rd):
    Sig0 = MB / (2 * math.pi * Rd**2)
    yv = Rv / (2 * Rd)
    V2 = 4 * math.pi * Gk * Sig0 * Rd * yv**2 * (i0(yv) * k0(yv) - i1(yv) * k1(yv))
    return -V2 / Rv


rows = {}
fr_dev = 0.0
for Rd in (3.0, 2.5, 3.5):
    for h in (0.05, 0.2):
        for Rv in (8.2, 10.0):
            U0, Bz, gN, _ = disc_fields(Rv, Rd, h)
            uu = 220.0
            aGM = -CURL * (4.0 / C_KMS**2) * uu * Bz                                  # radial component (R-hat)
            ratio = aGM / gN
            vs_ms = 4.0 * abs(U0) / C_KMS**2 * 1e3
            Om_fd = 2.0 / C_KMS**2 * abs(Bz) * CURL * KMS_KPC_TO_MASYR               # (1/2)|curl v_s| in mas/yr
            Om_gal = VS0 / Rv * KMS_KPC_TO_MASYR
            fg = freeman_gN(Rv, Rd)
            if h == 0.05:
                fr_dev = max(fr_dev, abs(gN / fg - 1))
            rows[(Rd, h, Rv)] = dict(U_phi=U0, B_z=Bz, g_N=gN, a_GM=aGM, ratio=ratio, v_swirl_ms=vs_ms, Omega_drag_masyr=Om_fd,
                                     Omega_gal_masyr=Om_gal, freeman=fg)
            R.P(f"  R_d {Rd:.1f}  h {h:.2f}  R {Rv:4.1f} kpc: g_N {gN:+.2f} (Freeman {fg:+.2f}) (km/s)^2/kpc; a_GM {aGM:+.3e}; "
                f"a_GM/g_N = {ratio:+.2e} ({'same sense as gravity (inward)' if ratio > 0 else 'opposite to gravity (outward)'}); "
                f"swirl speed |4U/c^2| = {vs_ms:.3f} m/s; frame rotation {Om_fd:.2e} mas/yr vs Omega_gal {Om_gal:.2f} mas/yr")
R.check("C2 CONTROL: the disc's Newtonian radial force at h = 0.05 kpc agrees with Freeman's exact thin-disc formula to 2% "
        "(R = 8.2, 10 kpc; R_d = 2.5, 3, 3.5)", fr_dev < 0.02, f"max |g_N/g_Freeman - 1| = {fr_dev:.4f}")
base = rows[(3.0, 0.05, 8.2)]
allr = [abs(v["ratio"]) for v in rows.values()]
R.check("W4 [HEADLINE] GR's swirl is negligible: |a_GM/g_N| below the frozen 1e-5 line (and nonzero) at 8.2 and 10 kpc for "
        "every R_d and h", all(0 < a < 1e-5 for a in allr),
        f"base (R_d 3, h 0.05, R 8.2): {base['ratio']:+.2e}; range {min(allr):.2e} - {max(allr):.2e}; 4V^2/c^2 = "
        f"{4 * (220 / C_KMS) ** 2:.2e}; swirl speed {base['v_swirl_ms']:.3f} m/s; frame rotation {base['Omega_drag_masyr']:.2e} mas/yr "
        f"= {base['Omega_drag_masyr'] / base['Omega_gal_masyr']:.1e} of Omega_gal")
R.num("W4", {f"Rd{k[0]}_h{k[1]}_R{k[2]}": v for k, v in rows.items()})

R.banner("VERDICT (W1-W4)")
R.P("  A swirled river pushes co-moving (prograde) and counter-moving (retrograde) bodies oppositely: that sign flip is the")
R.P(f"  swirl's fingerprint.  GR's own swirl of the Milky Way's river (frame dragging, baryons only) is {min(allr):.1e} - "
    f"{max(allr):.1e} of Newtonian gravity")
R.P(f"  at 8-10 kpc (pushing co-rotating stars outward), a river turning at ~{base['v_swirl_ms']:.2f} m/s, with local frames rotating "
    f"at {base['Omega_drag_masyr']:.1e} mas/yr; no galactic observable can see it.")
R.P("  (First run: the prose here was hard-coded as 'about a millionth' and '~a metre per second', which overstated the printed")
R.P("  numbers; it now prints them.  Checks and numbers are unchanged; see cfg179_s3_swirl_gr_firstrun.out.)")
R.finish()
