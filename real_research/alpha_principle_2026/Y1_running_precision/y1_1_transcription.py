#!/usr/bin/env python3
"""y1_1_transcription.py -- Part 1 of Y1_PREREGISTRATION.md: cross-checks of the typed beta-function coefficients (checks T1-T9).
Run:    python3 y1_1_transcription.py            (exit 0 iff every check passes; exit 2 if a real check fails)
MUTATE: python3 y1_1_transcription.py MUTATE     (the control flips the sign of the largest three-loop coefficient of beta_1 in form M; it must fail: exit 1; exit 3 if it does not bite)
Imports lane X1's `x1_lib` READ-ONLY (path-relative) for check T2.  Writes nothing except its .out via shell redirection; no bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "X1_spectrum_meets_boundary"))
sys.path.insert(0, os.path.join(HERE, "..", "B_rg_asymptotic_safety"))
sys.path.insert(0, os.path.join(HERE, "..", "N1_joint_couplings"))
sys.path.insert(0, os.path.join(HERE, "..", "U3_invented_uv_boundary"))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import y1_lib as L
import x1_lib as X1

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
fails = []
nchk = 0


def chk(name, ok, info=""):
    global nchk
    nchk += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)


def relmax(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.max(np.abs(a - b) / np.maximum(np.abs(a), np.abs(b))))


rng = np.random.default_rng(20260929)


def random_point(with_bt=False):
    g = rng.uniform(0.15, 1.4, 3)
    yt = rng.uniform(0.05, 1.0)
    lam = rng.uniform(0.0, 0.3)
    yb = rng.uniform(0.0, 0.05) if with_bt else 0.0
    ytau = rng.uniform(0.0, 0.05) if with_bt else 0.0
    u = np.array([g[0], g[1], g[2], yt, yb, ytau, lam])
    al = np.array([u[0], u[1], u[2], u[3], u[4], u[5], u[6]]) / (4 * PI)     # alpha_lambda-hat = lambda/(4 pi)
    return u, al


print("=" * 110)
print("Y1-1 transcription checks -- mode:", "MUTATE" if MUT else "REAL RUN")
print("=" * 110)

# ---------------------------------------------------------------------------------------------- T1: four typings of the three-loop gauge betas
worst = {"D-M": 0, "D-S": 0, "D-B": 0, "M-S": 0, "M-B": 0, "S-B": 0}
for _ in range(25):
    u, al = random_point(False)
    D3 = L.beta_D_alpha_pi(al, 3)
    if MUT:
        M3 = L.beta_alpha_pi(al, 3, bt=False, mutate=True)
    else:
        M3 = L.beta_alpha_pi(al, 3, bt=False)
    S3 = L.beta_S_alpha_pi(al)
    B3 = L.gauge_B(u, 3) / (4 * PI ** 2)
    for nm, (x, y) in {"D-M": (D3, M3), "D-S": (D3, S3), "D-B": (D3, B3), "M-S": (M3, S3), "M-B": (M3, B3), "S-B": (S3, B3)}.items():
        worst[nm] = max(worst[nm], relmax(x, y))
for nm, w in worst.items():
    chk(f"T1 {nm} three-loop gauge betas agree (25 random points, alpha_b = alpha_tau = 0)", w < 1e-11, f"worst relative difference {w:.2e}")

# same with alpha_b, alpha_tau non-zero: M (traces) versus B at one and two loops (B has b, tau only to two loops)
wbt = 0
for _ in range(25):
    u, al = random_point(True)
    M2 = L.beta_M_alpha_pi(al, 2)
    B2 = L.gauge_B(u, 2) / (4 * PI ** 2)
    wbt = max(wbt, relmax(M2, B2))
chk("T1b M and B agree at two loops with alpha_b, alpha_tau != 0 (25 points)", wbt < 1e-11, f"worst {wbt:.2e}")

# ---------------------------------------------------------------------------------------------- T2: group-theory build of lane X1 versus D at one and two loops
worst2 = 0
worst1 = 0
for _ in range(25):
    u, al = random_point(False)
    g1s, g2s, g3s, yts = u[0], u[1], u[2], u[3]
    gYs = 3.0 / 5.0 * g1s
    g2v = np.array([gYs, g2s, g3s])
    for loops, store in ((1, "1"), (2, "2")):
        b = X1.B_SM_F
        two = (X1.BM_SM_F @ g2v - X1.CY_TOP * yts) / (16 * PI ** 2) if loops == 2 else 0.0
        da_x1 = -(b + two) / (2 * PI)                       # d a_i / d ln mu, Y normalisation for i = 1
        beta = L.beta_D_alpha_pi(al, loops)                 # d(alpha_i/pi)/d ln mu^2 in GUT normalisation
        dalpha = 2 * PI * beta                              # d alpha_i / d ln mu
        da_gut = -dalpha / np.array([al[0], al[1], al[2]]) ** 2
        da_mine = np.array([da_gut[0] * 5.0 / 3.0, da_gut[1], da_gut[2]])   # a_Y = (5/3) a_1
        # note alpha_i here are the alpha = g^2/(4 pi) ; d(1/alpha)/dt = -dalpha/alpha^2
        e = relmax(da_x1, da_mine)
        if loops == 1:
            worst1 = max(worst1, e)
        else:
            worst2 = max(worst2, e)
chk("T2a one-loop b_i: form D equals the group-theory build of lane X1", worst1 < 1e-10, f"worst {worst1:.2e}")
chk("T2b two-loop gauge B_ij and top-Yukawa C_i: form D equals the group-theory build of lane X1", worst2 < 1e-10, f"worst {worst2:.2e}")

# ---------------------------------------------------------------------------------------------- T3: pure-QCD limit versus RunDec (n_f = 6, top massless in the unbroken theory)
b6 = L.qcd_beta(6)
ok3 = True
lines = []
for ell in range(1, 5):
    c = float(sum(float(c0) + float(z) * L.ZETA3 for (c0, z, m) in L.D_BR[3][ell] if set(m) <= {"3"}))
    expect = -b6[ell - 1] * 4 ** (ell + 1)
    good = abs(c - expect) / abs(expect) < 1e-9
    ok3 &= good
    lines.append(f"{ell}-loop: D {c:.9f} vs RunDec -b_{ell - 1} 4^{ell + 1} = {expect:.9f}")
for ln in lines:
    print("      " + ln)
chk("T3a pure alpha_3 terms of form D (1-4 loops) equal RunDec beta_0..beta_3 for n_f = 6", ok3)
K = -256.0 * b6[3]
chk("T3b four-loop pure-QCD coefficient of dg_3^2/dln mu^2: RunDec-derived value equals Buttazzo's printed -2472.28", abs(K + 2472.28) / 2472.28 < 5e-6, f"derived {K:.4f}")
c4D = float(sum(float(c0) + float(z) * L.ZETA3 for (c0, z, m) in L.D_BR[3][4] if m == "333"))
chk("T3c form D's alpha_3^5 coefficient reproduces Buttazzo's -2472.28 (c4/4)", abs(c4D / 4 + 2472.28) / 2472.28 < 5e-6, f"c4/4 = {c4D / 4:.4f}")

# ---------------------------------------------------------------------------------------------- T4/T5: Mihaila long paper two-loop Yukawa betas versus Buttazzo
def beta_M_yukawa(al, nG=3):
    a1, a2, a3, at, ab, atau, lh = al
    k1 = 1 / (4 * PI) ** 2
    k2 = 1 / (4 * PI) ** 3
    tr = 12 * at + 12 * ab + 4 * atau
    bt = at * (k1 * (-6 * ab + 6 * at + tr - 17 * a1 / 5 - 9 * a2 - 32 * a3)
               + k2 * (9 * a1 ** 2 / 50 - 9 * a1 * a2 / 5 - 35 * a2 ** 2 + 76 * a1 * a3 / 15 + 36 * a2 * a3 - 1616 * a3 ** 2 / 3 + nG * (116 * a1 ** 2 / 45 + 4 * a2 ** 2 + 320 * a3 ** 2 / 9)
                       + 24 * lh ** 2 + 393 * a1 * at / 20 + 225 * a2 * at / 4 + 144 * a3 * at - 48 * lh * at - 48 * at ** 2
                       + 7 * a1 * ab / 20 + 99 * a2 * ab / 4 + 16 * a3 * ab - 11 * at * ab - ab ** 2 + 15 * a1 * atau / 2 + 15 * a2 * atau / 2 - 9 * at * atau + 5 * ab * atau - 9 * atau ** 2))
    bb = ab * (k1 * (6 * ab - 6 * at + tr - a1 - 9 * a2 - 32 * a3)
               + k2 * (-29 * a1 ** 2 / 50 - 27 * a1 * a2 / 5 - 35 * a2 ** 2 + 124 * a1 * a3 / 15 + 36 * a2 * a3 - 1616 * a3 ** 2 / 3 + nG * (-4 * a1 ** 2 / 45 + 4 * a2 ** 2 + 320 * a3 ** 2 / 9)
                       + 24 * lh ** 2 + 91 * a1 * at / 20 + 99 * a2 * at / 4 + 16 * a3 * at - at ** 2 + 237 * a1 * ab / 20 + 225 * a2 * ab / 4 + 144 * a3 * ab - 48 * lh * ab - 11 * at * ab - 48 * ab ** 2
                       + 15 * a1 * atau / 2 + 15 * a2 * atau / 2 + 5 * at * atau - 9 * ab * atau - 9 * atau ** 2))
    bta = atau * (k1 * (6 * atau + tr - 9 * a1 - 9 * a2)
                  + k2 * (51 * a1 ** 2 / 50 + 27 * a1 * a2 / 5 - 35 * a2 ** 2 + nG * (44 * a1 ** 2 / 5 + 4 * a2 ** 2) + 24 * lh ** 2 + 17 * a1 * at / 2 + 45 * a2 * at / 2 + 80 * a3 * at - 27 * at ** 2
                          + 5 * a1 * ab / 2 + 45 * a2 * ab / 2 + 80 * a3 * ab + 6 * at * ab - 27 * ab ** 2 + 537 * a1 * atau / 20 + 165 * a2 * atau / 4 - 48 * lh * atau - 27 * at * atau - 27 * ab * atau - 12 * atau ** 2))
    return np.array([bt, bb, bta])


w4 = 0
for _ in range(25):
    u, al = random_point(True)
    dyt, dyb, dytau, dlam = L.yuk_lam_B(u, 2)
    mine = beta_M_yukawa(al) * 4 * PI ** 2                 # d y^2 / d ln mu^2
    w4 = max(w4, relmax([dyt, dyb, dytau], mine))
chk("T4/T5 two-loop y_t, y_b, y_tau betas: Mihaila long paper equals Buttazzo Appendix B (25 random points, b and tau kept)", w4 < 1e-11, f"worst {w4:.2e}")

# ---------------------------------------------------------------------------------------------- T6: Davies et al size statement
al_mz = np.array([0.0169225, 0.033735, 0.1173, 0.07514, 2.064e-5, 8.077e-6, 0.13 / (4 * PI)])       # Mihaila et al eq. (values) at m_Z
def ratio4_3_brackets(al):
    out = []
    for i in (1, 2, 3):
        c3, e3 = L.gauge_poly(i, 3, "D")
        c4, e4 = L.gauge_poly(i, 4, "D")
        a = np.array(al, float).copy(); a[4] = 0.0; a[5] = 0.0
        t3 = np.prod(a[None, :] ** e3, axis=1) @ c3 / (4 * PI) ** 4
        t4 = np.prod(a[None, :] ** e4, axis=1) @ c4 / (4 * PI) ** 5
        out.append(100 * t4 / t3)
    return out
r_mz = ratio4_3_brackets(al_mz)
print(f"      four-loop / three-loop bracket ratio at the m_Z couplings: beta_1 {r_mz[0]:.1f}%  beta_2 {r_mz[1]:.1f}%  beta_3 {r_mz[2]:.1f}%   (Davies et al. state 8%, 5%, 127%)")
# Amendment A3: the source states MAGNITUDES ("amount to 8%, 5% and 127%"), so the comparison is of |ratio|; the sign (negative) is a result, not tested against text.
chk("T6 Davies et al. 'four-loop is 8%, 5%, 127% of three-loop' reproduced at the m_Z couplings, magnitudes (+- 1 percentage point)",
    abs(abs(r_mz[0]) - 8) <= 1 and abs(abs(r_mz[1]) - 5) <= 1 and abs(abs(r_mz[2]) - 127) <= 1, f"got {r_mz[0]:.1f} / {r_mz[1]:.1f} / {r_mz[2]:.1f}")

# ---------------------------------------------------------------------------------------------- T7 / T8: Mihaila numerical statements (their inputs, run to 1e16 GeV, yukawa and lambda at two loops)
MZ = 91.1876
u0 = np.array([al_mz[0], al_mz[1], al_mz[2], al_mz[3], al_mz[4], al_mz[5], 0.13 / (4 * PI)]) * 4 * PI
u0[6] = 0.13


def run_to(mu1, gl, yl=2, drop3=(), extra_qcd4=False, bt=True):
    o = L.Opts(gauge_loops=gl, yuk_loops=yl, bt=bt, drop3=drop3)
    def f(t, y):
        r = 2.0 * L.rhs_lnmu2(y, o)
        if extra_qcd4:
            r[2] += 2.0 * (-256.0 * b6[3]) * y[2] ** 5 / (4 * PI) ** 8
        return r
    s = solve_ivp(f, [math.log(MZ), math.log(mu1)], list(u0), method="DOP853", rtol=1e-12, atol=1e-14)
    y = s.y[:, -1]
    return np.array([4 * PI / y[0], 4 * PI / y[1], 4 * PI / y[2]])      # a_1 (GUT), a_2, a_3


a2 = run_to(1e16, 2)
a3 = run_to(1e16, 3)
a3nol = run_to(1e16, 3, drop3=(4, 5, 6))
d32 = a3 - a2
dsmall = a3 - a3nol
frac = np.abs(dsmall / d32) * 100
print(f"      at 1e16 GeV: a(2-loop) {np.round(a2, 5)}  a(3-loop) {np.round(a3, 5)}  |terms with b, tau, lambda| / |3-loop - 2-loop| = {np.round(frac, 4)} %")
chk("T7 Mihaila: three-loop terms containing alpha_b, alpha_tau or lambda are < 0.2% of the (3-loop - 2-loop) difference at 1e16 GeV (statement: < 0.1%)", bool(np.all(frac < 0.2)))
a3q = run_to(1e16, 3, extra_qcd4=True)
frac4 = (a3q[2] - a3[2]) / (a3[2] - a2[2]) * 100
print(f"      four-loop pure-QCD term shifts a_3(1e16) by {a3q[2] - a3[2]:+.5f} = {frac4:+.1f}% of the (3-loop - 2-loop) difference (Mihaila state -58% for alpha_3 at an unspecified scale)")
chk("T8 Mihaila: four-loop alpha_s^5 term is about -58% of the (3-loop - 2-loop) alpha_3 difference (+- 15 points; weak check, scale not stated)", abs(frac4 + 58) <= 15, f"got {frac4:+.1f}%")

# ---------------------------------------------------------------------------------------------- T9: RunDec eq. (22) versus eq. (25)
# Amendment A4: the residual of (22) x (25) is O(a^4) with an a^4 coefficient of about 15 at L = 1, so a fixed 3e-6 threshold is wrong.  The test is that the residual is O(a^4):
# |1 - product| / a^3 < 0.05 at alpha_s = 0.003 for every L (an error of >= 0.05 in a three-loop coefficient would show), and the residual scales like a^4 (ratio for doubling alpha_s in [12, 22]).
ok9 = True
worst_o3 = 0
worst_sc = []
for Lg in (-1.0, -0.3, 0.0, 0.4, 1.0):
    d = []
    for als in (0.003, 0.006):
        z2 = L.zeta_g2_OS(als, Lg, 5)
        prod = z2 * L.inv_zeta_g2_OS(z2 * als, Lg, 5)
        d.append(abs(1 - prod))
    a = 0.003 / PI
    worst_o3 = max(worst_o3, d[0] / a ** 3)
    ratio = d[1] / d[0] if d[0] > 0 else float("inf")
    worst_sc.append(ratio)
    if not (12 <= ratio <= 22):
        ok9 = False
print(f"      residual/a^3 at alpha_s = 0.003: worst {worst_o3:.4f}; doubling ratios {np.round(worst_sc, 2)}")
chk("T9 RunDec decoupling: eq. (22) x eq. (25) = 1 up to an O(alpha_s^4) residual (|1-product|/a^3 < 0.05 at alpha_s = 0.003; doubling ratio in [12, 22])", ok9 and worst_o3 < 0.05)

print(f"\nY1-1: {nchk} checks, {len(fails)} failed" + (f": {fails}" if fails else ""))
if MUT:
    print("MUTATE control:", "BITES (a check failed as required) -> exit 1" if fails else "BROKEN (no check failed) -> exit 3")
    sys.exit(1 if fails else 3)
sys.exit(0 if not fails else 2)
