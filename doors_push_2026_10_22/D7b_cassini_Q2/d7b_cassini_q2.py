#!/usr/bin/env python3
"""D7b_cassini_Q2 -- Cassini quadrupole Q2 of the canonical law with and without the P5 turn-off.

Canonical law g_N = g^2/(g+a0):  w(y) = nu-1 = (sqrt(1+4/y)-1)/2,  y = |g_N|/a0  (QUMOND).
P5 turn-off:                     w_fix(y) = w(y)/(1+(y/y_t)^2).
Sun (point mass) + uniform Newtonian external field g_Ne; phantom rho_ph = -div[w_fix g_N]/(4 pi G).
Q2 in the BN11 / Hees convention: dU = (1/2) Q2 (z^2 - r^2/3), U = -Phi (MOND prediction positive).

Route M: Milgrom 2009 / Desmond+2024 eq-12 integral, written with v^2 = eN s:
   q = (3/4) eN^{3/2} Int_0^inf ds s^{-1/2} Int_{-1}^{1} dxi w(eN R) [-2 P3(xi) - 2 s P2(xi)],
   R = sqrt(1 + s^2 + 2 s xi),   Q2 = -(3 a0^{3/2} / (2 sqrt(GM))) q.
Route G: axisymmetric log-r x Gauss-Legendre grid, closed-form rho_ph, P2 projection, Green integrals.
Frozen criteria: FROZEN_CRITERIA.md (commit c6a0b6f3c7).  Deterministic, no network, single thread.
"""
import json
import math
import os
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import integrate
from scipy.optimize import brentq

MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, f"d7b_cassini_q2{TAG}.out")
OUT_JSON = os.path.join(HERE, f"d7b_cassini_q2_results{TAG}.json")

# ------------------------------------------------------------------ inputs (labelled in FROZEN_CRITERIA.md)
GM = 1.32712440018e20            # IAU
AU = 1.495978707e11
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
KAPPA_TH = Z / (4.0 * math.pi)
N_LAMBDA_QUOTED = 100.405845      # A4 D5: Lambda c^4/a0^2 at quoted Lambda, canonical a0
GNE_A60 = 6.913e-11               # A60 sec 1.3: framework MW model, Newtonian field at the Sun
GE_KIN = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}  # record band (branchB lane)
HEES = (3.0e-27, 3.0e-27)         # Hees+2014 Q2 = (3 +/- 3)e-27 s^-2
PARK = (1.6e-27, 1.8e-27)         # Park+2026 (secondary)
BOUND_H = HEES[0] + 2 * HEES[1]   # 9.0e-27
BOUND_P = PARK[0] + 2 * PARK[1]   # 5.2e-27
DESMOND_ANCHORS = {1.0: 0.094, 1.5: 0.159, 2.0: 0.221}  # simple-nu |q| at g_e/a0 (record transcription)
BN11_MU1 = (3.8e-26, 1.2e-10, 1.9e-10)                  # Q2, a0, g_e (AQUAL)
R_SAT = 9.5826 * AU

lines = []


def say(s=""):
    print(s)
    lines.append(s)


# ------------------------------------------------------------------ kernels
def w_can(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 2.0 / (y * (np.sqrt(1.0 + 4.0 / y) + 1.0))      # = (sqrt(1+4/y)-1)/2, stable


def dlnw_can(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    s = np.sqrt(1.0 + 4.0 / y)
    # w = (s-1)/2, dw/dy = -1/(y^2 s);  dln w/dln y = y w'/w
    return -2.0 / (y * s * (s - 1.0))


def make_fix(yt):
    if yt is None:
        return w_can, dlnw_can

    def w(y):
        y = np.asarray(y, float)
        return w_can(y) / (1.0 + (y / yt) ** 2)

    def dlnw(y):
        y = np.asarray(y, float)
        x2 = (y / yt) ** 2
        return dlnw_can(y) - 2.0 * x2 / (1.0 + x2)
    return w, dlnw


def w_unit(y):                     # nu-1 = 1/y exactly (analytic limit)
    return 1.0 / np.maximum(np.asarray(y, float), 1e-300)


def dlnw_unit(y):
    return -np.ones_like(np.asarray(y, float))


def w_standard(y):                 # mu = x/sqrt(1+x^2) (only for information)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y ** 2))) - 1.0


# ------------------------------------------------------------------ Route M
TN, TW = leggauss(400)
TAU = 0.5 * (TN + 1.0)
TAUW = 0.5 * TW
XI_M = -1.0 + 2.0 * TAU ** 2      # clusters at xi = -1 (stagnation side)
JAC_M = 4.0 * TAU * TAUW
P2M = 0.5 * (3 * XI_M ** 2 - 1)
P3M = 0.5 * (5 * XI_M ** 3 - 3 * XI_M)


def inner_xi(s, w, eN, sqrtD_bug):
    R = np.sqrt(np.maximum(1.0 + s * s + 2.0 * s * XI_M, 0.0))
    Y = eN * R
    f = w(Y) * (-2.0 * P3M - 2.0 * s * P2M)
    if sqrtD_bug:                  # record's /sqrt(D) transcription bug: D = (v^2 ... ) -> Y
        f = f / np.maximum(Y, 1e-300)
    return float(np.sum(f * JAC_M))


def q_route_m(w, eN, split=1.0, sqrtD_bug=False):
    # s in [0, S]: s = S u^2 ; s in [S, inf): s = S / u^2 ;  both u in (0, 1]
    S = split

    def f_lo(u):
        s = S * u * u
        # s^{-1/2} ds = sqrt(S) * 2 du
        return 2.0 * math.sqrt(S) * inner_xi(s, w, eN, sqrtD_bug)

    def f_hi(u):
        if u <= 0.0:
            return 0.0
        s = S / (u * u)
        # s^{-1/2} ds = (u/sqrt S) * (2 S / u^3) du = 2 sqrt(S) / u^2 du
        return 2.0 * math.sqrt(S) / (u * u) * inner_xi(s, w, eN, sqrtD_bug)

    pts_lo = [math.sqrt(1.0 / S)] if S > 1.0 else None
    pts_hi = [math.sqrt(S)] if S < 1.0 else None
    a, _ = integrate.quad(f_lo, 0.0, 1.0, points=pts_lo, limit=400, epsabs=1e-13, epsrel=1e-10)
    b, _ = integrate.quad(f_hi, 0.0, 1.0, points=pts_hi, limit=400, epsabs=1e-13, epsrel=1e-10)
    return 0.75 * eN ** 1.5 * (a + b)


def Q2_from_q(q, a0):
    return -(3.0 * a0 ** 1.5) / (2.0 * math.sqrt(GM)) * q


# ------------------------------------------------------------------ Route G
def q2_route_g(w, dlnw, gNe, a0, Nr=6000, Nxi=256, rlo=1e-5, rhi=1e4, r_eval=None, fd_check=False):
    """Q2 [s^-2] (BN11 convention) from an axisymmetric grid. r in units of r_e = sqrt(GM/gNe)."""
    r_e = math.sqrt(GM / gNe)
    r = r_e * np.logspace(math.log10(rlo), math.log10(rhi), Nr)
    tn, tw = leggauss(Nxi)
    tau = 0.5 * (tn + 1.0)
    xi = 1.0 - 2.0 * tau ** 2      # clusters at xi = +1 (stagnation point is on the +z axis)
    wx = 4.0 * tau * 0.5 * tw
    R = r[:, None]
    XI = xi[None, :]
    gs = GM / R ** 2
    Y = np.sqrt(np.maximum(gs ** 2 + gNe ** 2 - 2.0 * gs * gNe * XI, 1e-300))
    y = Y / a0
    wv = w(y)
    dw_dY = wv * dlnw(y) / Y
    gdotgrad = gs / (R * Y) * (2.0 * (gs - gNe * XI) ** 2 - gNe ** 2 * (1.0 - XI ** 2))
    rho_ph = -(dw_dY * gdotgrad) / (4.0 * math.pi * 6.674e-11)   # G cancels below; kept explicit
    P2 = 0.5 * (3.0 * XI ** 2 - 1.0)
    rho2 = 2.5 * np.sum(rho_ph * P2 * wx[None, :], axis=1)
    lnr = np.log(r)
    Gc = 6.674e-11
    # interior coefficient at the origin: Phi_2 = C r^2 P2, C = -(4piG/5) Int rho2 / r dr
    C0 = -(4.0 * math.pi * Gc / 5.0) * np.trapz(rho2, x=lnr)
    out = {"Q2_origin": -3.0 * C0}
    if r_eval is not None:
        m_in = r <= r_eval
        m_out = r >= r_eval
        I_in = np.trapz(rho2[m_in] * r[m_in] ** 5, x=lnr[m_in]) if m_in.sum() > 3 else 0.0
        I_out = np.trapz(rho2[m_out], x=lnr[m_out])
        C = -(4.0 * math.pi * Gc / 5.0) * (I_in / r_eval ** 5 + I_out)
        out["Q2_at_r"] = -3.0 * C
    if fd_check:
        # brute-force divergence of w g_N at a few interior points vs the closed form
        errs = []
        for (rr, xx) in [(0.3, 0.2), (1.1, 0.7), (2.5, -0.4), (0.8, 0.95)]:
            x0 = rr * r_e * math.sqrt(1 - xx ** 2)
            z0 = rr * r_e * xx

            def F(x, z):
                rad = math.hypot(x, z)
                g = np.array([-GM * x / rad ** 3, -GM * z / rad ** 3 + gNe])
                return float(w(np.array([np.linalg.norm(g) / a0]))[0]) * g
            h = 1e-5 * rr * r_e
            # axisymmetric divergence in cylindrical (x = rho): (1/rho) d(rho F_rho)/drho + dF_z/dz
            div = ((x0 + h) * F(x0 + h, z0)[0] - (x0 - h) * F(x0 - h, z0)[0]) / (2 * h * x0) \
                + (F(x0, z0 + h)[1] - F(x0, z0 - h)[1]) / (2 * h)
            gs0 = GM / (rr * r_e) ** 2
            Y0 = math.sqrt(gs0 ** 2 + gNe ** 2 - 2 * gs0 * gNe * xx)
            y0 = Y0 / a0
            cf = float((w(np.array([y0])) * dlnw(np.array([y0])))[0]) / Y0 * gs0 / (rr * r_e * Y0) * \
                (2 * (gs0 - gNe * xx) ** 2 - gNe ** 2 * (1 - xx ** 2))
            errs.append(abs(div - cf) / abs(cf))
        out["fd_rel_err_max"] = max(errs)
    return out


# ------------------------------------------------------------------ closure
def F_can(Y):
    f = lambda th: float(w_can(np.array([Y * math.tan(th)]))[0]) * Y * math.tan(th)
    v, _ = integrate.quad(f, 0.0, math.pi / 2, limit=400, epsabs=1e-12, epsrel=1e-12)
    return Y * v


def yt_root(N):
    return brentq(lambda Y: F_can(Y) - N, 1.0, 1e4, xtol=1e-12)


def gNe_from_total(ge, a0, w):
    return brentq(lambda e: e * (1.0 + float(w(np.array([e / a0]))[0])) - ge, 1e-14, ge, xtol=1e-25)


# ================================================================== run
checks = []
res = {"inputs": {"GM": GM, "a0": A0, "Z": Z, "kappa_thermal": KAPPA_TH, "gNe_A60": GNE_A60,
                  "ge_kinematic_total": GE_KIN, "Hees2014": HEES, "Park2026": PARK,
                  "bound_Hees_2sigma": BOUND_H, "bound_Park_2sigma": BOUND_P,
                  "Desmond_anchors_simple_absq": DESMOND_ANCHORS, "BN11_mu1": BN11_MU1,
                  "mutate": MUTATE}}


def check(name, ok, value, thr):
    checks.append(bool(ok))
    say(f"{name} {'PASS' if ok else 'FAIL'} {value} {thr}")


say("=" * 100)
say("D7b_cassini_Q2 -- Cassini Q2 of the canonical law, with and without the P5 turn-off" + (" [MUTATE]" if MUTATE else ""))
say("=" * 100)

# ---- K7 closure roots (needed for the y_t grid)
yt_32pi = yt_root(32.0 * math.pi)
yt_quoted = yt_root(N_LAMBDA_QUOTED)
N_th = 8.0 * math.pi / KAPPA_TH ** 2
yt_th = yt_root(N_th)
kap_lo = math.sqrt(8 * math.pi / F_can(140.0))
kap_hi = math.sqrt(8 * math.pi / F_can(60.0))
res["closure"] = {"yt_32pi": yt_32pi, "yt_quotedLambda": yt_quoted, "yt_thermal": yt_th, "N_thermal": N_th,
                  "kappa_at_yt140": kap_lo, "kappa_at_yt60": kap_hi}

# ---- K1 analytic limit
k1 = {}
for eN in (0.5, 2.0, 8.0):
    qa = -(16.0 / 49.0) * math.sqrt(eN)
    qn = q_route_m(w_unit, eN, sqrtD_bug=MUTATE)
    k1[str(eN)] = {"q_num": qn, "q_exact": qa, "rel": abs(qn / qa - 1)}
res["K1_analytic_unit_tail"] = k1
k1max = max(v["rel"] for v in k1.values())
check("K1", k1max < 1e-3, f"max_rel={k1max:.2e} (q=-(16/49)sqrt(eN) at eN=0.5,2,8)", "<1e-3")

# ---- K2 Route G on the analytic limit (eN = 2, physical units with canonical a0)
a0c = A0["canonical"]
gNe2 = 2.0 * a0c
qa2 = -(16.0 / 49.0) * math.sqrt(2.0)
Q2a = Q2_from_q(qa2, a0c)
g2 = q2_route_g(w_unit, dlnw_unit, gNe2, a0c, fd_check=True)
k2rel = abs(g2["Q2_origin"] / Q2a - 1)
res["K2_routeG_analytic"] = {"Q2_exact": Q2a, "Q2_grid": g2["Q2_origin"], "rel": k2rel,
                             "fd_divergence_rel_err": g2["fd_rel_err_max"]}
check("K2", k2rel < 0.01 and g2["fd_rel_err_max"] < 1e-4,
      f"grid/exact-1={k2rel:.2e} fd_div_err={g2['fd_rel_err_max']:.1e}", "<1e-2 (fd<1e-4)")

# ---- K4 published anchors (simple nu = canonical law, no turn-off), a0 = 1.2e-10 units irrelevant (q is pure)
k4 = {}
for et, anc in DESMOND_ANCHORS.items():
    eN = brentq(lambda e: e * (1.0 + float(w_can(np.array([e]))[0])) - et, 1e-9, et)
    q = q_route_m(w_can, eN, sqrtD_bug=MUTATE)
    k4[str(et)] = {"eN": eN, "absq": abs(q), "anchor": anc, "ratio": abs(q) / anc}
res["K4_Desmond_anchors"] = k4
k4dev = max(abs(v["ratio"] - 1) for v in k4.values())
check("K4", k4dev < 0.03, "ratios=" + ",".join(f"{v['ratio']:.4f}" for v in k4.values()), "within 3%")

# ---- K5 BN11 AQUAL mu1
Qbn, a0bn, gebn = BN11_MU1
eNbn = brentq(lambda e: e * (1.0 + float(w_can(np.array([e]))[0])) - gebn / a0bn, 1e-9, gebn / a0bn)
Q2bn = Q2_from_q(q_route_m(w_can, eNbn, sqrtD_bug=MUTATE), a0bn)
r5 = Q2bn / Qbn
res["K5_BN11"] = {"Q2_QUMOND": Q2bn, "BN11_AQUAL": Qbn, "ratio": r5}
check("K5", 0.70 <= r5 <= 1.05, f"QUMOND/BN11={r5:.4f} (Q2={Q2bn:.3e})", "[0.70,1.05]")

# ---- main grid
YT = [("none", None), ("60", 60.0), ("66.3803", yt_32pi), ("77.876", yt_th), ("140", 140.0)]
grid = {}
k3dev = 0.0
k3sign = True
for foot, a0 in A0.items():
    grid[foot] = {}
    for ytlab, yt in YT:
        w, dlnw = make_fix(yt)
        row = {}
        Es = [("E0", GNE_A60, None)] + [(k, None, v) for k, v in GE_KIN.items()]
        for elab, gNe, ge in Es:
            if gNe is None:
                gNe = gNe_from_total(ge, a0, w)
            eN = gNe / a0
            qM = q_route_m(w, eN, sqrtD_bug=MUTATE)
            QM = Q2_from_q(qM, a0)
            gG = q2_route_g(w, dlnw, gNe, a0, r_eval=R_SAT)
            QG = gG["Q2_origin"]
            k3dev = max(k3dev, abs(QG / QM - 1))
            k3sign = k3sign and (QG > 0) == (QM > 0)
            row[elab] = {"gNe": gNe, "eN": eN, "ge_total": gNe * (1 + float(w(np.array([eN]))[0])),
                         "q": qM, "Q2_M": QM, "Q2_G_origin": QG, "Q2_G_Saturn": gG["Q2_at_r"],
                         "over_Hees": QM / BOUND_H, "over_Park": QM / BOUND_P}
        grid[foot][ytlab] = row
res["grid"] = grid
check("K3", k3dev < 0.02 and k3sign, f"max|G/M-1|={k3dev:.2e} sign_agree={k3sign}", "<2e-2")

# ---- K6 limits
w66, dl66 = make_fix(yt_32pi)
q0 = q_route_m(w66, 1e-12)            # g_Ne -> 0
qE2 = grid["canonical"]["66.3803"]["E2"]["q"]
wbig, _ = make_fix(1e8)
eNE2 = grid["canonical"]["none"]["E2"]["eN"]
qbig = q_route_m(wbig, eNE2)
qnone = grid["canonical"]["none"]["E2"]["q"]
k6a = abs(Q2_from_q(q0, a0c)) / abs(Q2_from_q(qE2, a0c))
k6b = abs(qbig / qnone - 1)
res["K6_limits"] = {"ratio_ge0": k6a, "rel_yt1e8_vs_none": k6b}
check("K6", k6a < 1e-6 and k6b < 1e-5, f"ge0_ratio={k6a:.1e} yt1e8_rel={k6b:.1e}", "<1e-6, <1e-5")

# ---- K7
r7 = max(abs(yt_32pi / 66.3803 - 1), abs(yt_quoted / 66.2999 - 1), abs(yt_th / 77.876 - 1))
check("K7", r7 < 1e-3, f"yt(32pi)={yt_32pi:.4f} yt(quoted)={yt_quoted:.4f} yt(thermal,N={N_th:.3f})={yt_th:.4f}",
      "1e-3 vs 66.3803/66.2999/77.876")

# ---- K8 convergence
w_, dl_ = make_fix(yt_32pi)
eNc = grid["canonical"]["66.3803"]["E2"]["eN"]
qa_ = q_route_m(w_, eNc, split=1.0)
qb_ = q_route_m(w_, eNc, split=2.0)
gNc = eNc * a0c
ga_ = q2_route_g(w_, dl_, gNc, a0c)["Q2_origin"]
gb_ = q2_route_g(w_, dl_, gNc, a0c, Nr=12000, Nxi=512, rlo=1e-6, rhi=3e4)["Q2_origin"]
c8m = abs(qb_ / qa_ - 1)
c8g = abs(gb_ / ga_ - 1)
res["K8_convergence"] = {"routeM_split_rel": c8m, "routeG_doubling_rel": c8g}
check("K8", c8m < 5e-3 and c8g < 1e-2, f"M_split={c8m:.1e} G_double={c8g:.1e}", "<5e-3, <1e-2")

# ---- diagnostic (not a check): is the K4 anchor gap a v-truncation effect? (record's branchB tail-CAL claim)
trunc = {}
for et in DESMOND_ANCHORS:
    eN = k4[str(et)]["eN"]
    S = 3600.0 / eN                                  # v_max = 60  <=>  s_max = 3600/eN
    f = lambda u: 2.0 * math.sqrt(S) * inner_xi(S * u * u, w_can, eN, MUTATE)
    a_, _ = integrate.quad(f, 0.0, 1.0, points=[math.sqrt(1.0 / S)], limit=800, epsabs=1e-13, epsrel=1e-10)
    trunc[str(et)] = abs(0.75 * eN ** 1.5 * a_) / k4[str(et)]["absq"]
res["diag_vmax60_over_full"] = trunc
say("  diag: q(v<=60)/q(full) = " + ",".join(f"{v:.6f}" for v in trunc.values())
    + "  (truncation cannot explain the K4 anchor gap)")

# ================================================================== results (frozen lines)
say("")
say("Q2 [s^-2], Route M (BN11/Hees sign), per footing x y_t x external field  [ratio to Hees 2sigma 9.0e-27]")
say("  E0 = A60 framework MW (g_Ne=6.913e-11); E1/E2/E3 = kinematic total g_e = 1.9/2.2/2.6 x 9.36e-11")
verdicts = {}
for foot in A0:
    for ytlab, _ in YT:
        row = grid[foot][ytlab]
        vals = [row[e]["Q2_M"] for e in ("E0", "E1", "E2", "E3")]
        def vd(b):
            if all(v <= b for v in vals):
                return "PASS"
            if all(v > b for v in vals):
                return "FAIL"
            return "E-DEPENDENT"
        none = grid[foot]["none"]
        eff = [row[e]["Q2_M"] / none[e]["Q2_M"] - 1 for e in ("E0", "E1", "E2", "E3")]
        verdicts[f"{foot}|{ytlab}"] = {"Hees": vd(BOUND_H), "Park": vd(BOUND_P),
                                       "Q2": vals, "turnoff_effect": eff,
                                       "min_over_Hees": min(vals) / BOUND_H, "max_over_Hees": max(vals) / BOUND_H}
        say(f"  R {foot:9s} y_t={ytlab:8s} Q2=" + " ".join(f"{v:.3e}" for v in vals)
            + f"  x[{min(vals)/BOUND_H:.2f},{max(vals)/BOUND_H:.2f}]  Hees:{vd(BOUND_H)}  Park:{vd(BOUND_P)}"
            + "  dQ2/Q2(none)=" + ",".join(f"{e:+.4f}" for e in eff))
res["verdicts"] = verdicts

# band statement
spread = {}
for foot in A0:
    for e in ("E0", "E1", "E2", "E3"):
        spread[f"{foot}|{e}"] = abs(grid[foot]["60"][e]["Q2_M"] - grid[foot]["140"][e]["Q2_M"])
max_spread = max(spread.values())
same = len({v["Hees"] for k, v in verdicts.items()}) == 1
cannot_see = same and max_spread < HEES[1]
res["band"] = {"Q2_spread_yt60_vs_140": spread, "max_spread": max_spread, "sigma_Hees": HEES[1],
               "max_spread_over_sigma_Hees": max_spread / HEES[1], "same_verdict_all_yt": same,
               "Q2_cannot_see_yt": cannot_see}
sat = {f"{f}|{e}": grid[f]["66.3803"][e]["Q2_G_Saturn"] / grid[f]["66.3803"][e]["Q2_G_origin"] - 1
       for f in A0 for e in ("E0", "E1", "E2", "E3")}
res["Saturn_vs_origin_rel_yt66"] = sat
say("")
say(f"  y_t band: max |Q2(60)-Q2(140)| = {max_spread:.3e} s^-2 = {max_spread/HEES[1]:.4f} sigma_Hees; "
    f"same Hees verdict at all y_t (incl. none): {same}")
say(f"  Q2 at Saturn vs origin (Route G, y_t=66.38): max rel diff {max(abs(v) for v in sat.values()):.1e}")
say(f"  closure: y_t(kappa=1/2, 32pi)={yt_32pi:.4f}  y_t(quoted Lambda)={yt_quoted:.4f}  "
    f"y_t(thermal)={yt_th:.4f};  band [60,140] <-> kappa in [{kap_lo:.4f},{kap_hi:.4f}]")
outcome = ("Q2 CANNOT SEE y_t" if cannot_see else "see band/verdict table") + \
    f"; canonical law Q2 verdict vs Hees 2sigma: {sorted({v['Hees'] for v in verdicts.values()})}"
res["outcome"] = outcome
say(f"  OUTCOME: {outcome}")

n_ok = sum(checks)
say("")
say(f"D7B_CASSINI_Q2 COMPLETE: {n_ok}/{len(checks)} checks PASS.")
res["checks_pass"] = n_ok
res["checks_total"] = len(checks)
with open(OUT_TXT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(OUT_JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=float)
sys.exit(0 if n_ok == len(checks) else 1)
