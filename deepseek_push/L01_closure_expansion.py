#!/usr/bin/env python3
"""L01 -- THE THIN-OPACITY EXPANSION OF THE CLOSURE RATIO
2026-09-23.  Lane: moment channel, continuation of J01/J02/K04 on the
JWST_EQUATION_TARGET Thomson-sphere transport model (kappa = tau0(1+q r^2),
T = 1, central source, exact optical-depth bisection engine, no
null-collision thinning).

PREMISE ON RECORD (from the lane brief):  R = 1 + Cov(D,ang)/(E[D]E[ang])
with E[D ang] = tau0^2 r1(q) + tau0^3 r2(q) + ... ;  test "does R-1 scale as
tau0 times an O(1) coefficient".

WHAT THE FIRST-FLIGHT + ONE-COLLISION STRUCTURE GIVES (this file verifies):
  D = sum_j s_j (1 - u_j . u_final)   (telescoping, ANY source, exact)
  N=0: (D, ang) = (0,0).  N=1: D = s1(1-mu), ang = (1-mu), s1 _|_ mu.
  E[D ang] = r1(q) tau0 + r2(q) tau0^2 + O(tau0^3),
      r1(q) = (7/5)(1/2 + q/4)          [exact: E[(1-mu)^2] = 7/5 Thomson]
  E[ang]   = E[N] = (1+q/3) tau0 + c2(q) tau0^2 + O(tau0^3),  c2 = K04(6)
  E[D]     = (1/2 + q/4) tau0           [exact, frozen Theorem 1]
  ==>  R = (7/5)/[(1+q/3) tau0] (1 + g(q) tau0) + O(tau0),  g = r2/r1 - c2/(1+q/3)
  ==>  R - 1 = (7/5)/[(1+q/3) tau0] - 1 + O(1):  NO O(tau0) expansion of R-1
      exists;  the closure ratio DIVERGES as (7/5)/((1+q/3) tau0) - 1.

Pre-registered kill condition: leading-coefficient mismatch beyond 5 SE =
wrong derivation.  Squarely applied: (i) the premised form (no tau0 term in
E[D ang]) is refuted at 5 SE; (ii) the derived r1(q) = (7/5)(1/2+q/4) is
tested against the same runs (deep probes + N=1-sector exact quadrature) at
5 SE.

Deliverables: L01_CLOSURE_EXPANSION.md, L01_closure_expansion.out,
L01_results.json.  Append-only: no edits to earlier lanes, no git commit.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")
from J02_moment_hierarchy import simulate, se          # noqa: E402
from K04_inversion import c2_analytic                  # noqa: E402

OUT = []
def log(m=""):
    OUT.append(str(m)); print(m, flush=True)

def block_ratio(x, y, z, b=8):
    """R = mean(x)/(mean(y)*mean(z)) with SE by b independent blocks."""
    xb = np.array_split(x, b); yb = np.array_split(y, b); zb = np.array_split(z, b)
    Rk = np.array([np.mean(xi) / (np.mean(yi) * np.mean(zi))
                   for xi, yi, zi in zip(xb, yb, zb)])
    return float(np.mean(Rk)), float(np.std(Rk, ddof=1) / np.sqrt(b))

# ---------------------------------------------------------------- analytics
def r1_analytic(q):
    return (7.0 / 5.0) * (1.0 / 2.0 + q / 4.0)         # E[(1-mu)^2] = 7/5

def N1_quadrature(q, tau0, nr=2400, nmu=500):
    """EXACT N=1-sector integrals (first flight + escape after one collision,
    all orders in tau0): returns (P1, ED1, EDa1) with
      P1   = E[1{N=1}],  ED1 = E[D 1{N=1}],  EDa1 = E[D*ang 1{N=1}]
    from the central-source integrands with kappa = tau0(1+q s^2)."""
    s, ws = np.polynomial.legendre.leggauss(nr); s = 0.5 * (s + 1.0); ws = 0.5 * ws
    m, wm = np.polynomial.legendre.leggauss(nmu)
    S, M = np.meshgrid(s, m, indexing="ij")
    kap = tau0 * (1.0 + q * S * S)
    L1 = tau0 * (S + q * S ** 3 / 3.0)
    s2 = -S * M + np.sqrt(S * S * M * M + 1.0 - S * S)
    L2 = tau0 * (s2 + q * (S * S * s2 + S * M * s2 ** 2 + s2 ** 3 / 3.0))
    L = L1 + L2
    p3 = (3.0 / 8.0) * (1.0 + M * M)
    P1 = float(np.sum(kap * np.exp(-L) * p3 * ws[:, None] * wm))
    ED1 = float(np.sum(S * (1.0 - M) * kap * np.exp(-L) * p3 * ws[:, None] * wm))
    EDa1 = float(np.sum(S * (1.0 - M) ** 2 * kap * np.exp(-L) * p3 * ws[:, None] * wm))
    return P1, ED1, EDa1

def r2_one_collision(q, nr=2000, nmu=500):
    """O(tau0^2) coefficient of E[D ang] from the N=1 sector alone:
    -int int s1 kappat (1-mu)^2 p (L1t + L2t)  (e^{-L} -> 1 - L)."""
    s, ws = np.polynomial.legendre.leggauss(nr); s = 0.5 * (s + 1.0); ws = 0.5 * ws
    m, wm = np.polynomial.legendre.leggauss(nmu)
    S, M = np.meshgrid(s, m, indexing="ij")
    kap = 1.0 + q * S * S
    L1t = S + q * S ** 3 / 3.0
    s2 = -S * M + np.sqrt(S * S * M * M + 1.0 - S * S)
    L2t = s2 + q * (S * S * s2 + S * M * s2 ** 2 + s2 ** 3 / 3.0)
    p = (3.0 / 8.0) * (1.0 + M * M)
    w = (1.0 - M) ** 2 * p
    return -float(np.sum(S * kap * w * (L1t + L2t) * ws[:, None] * wm))

def A_v_analytic(q):
    """E[D]_vol = tau0 * A_v(q) + O(tau0^2);  A_v(q) = 2/5 + (8/35) q (closed)."""
    return 2.0 / 5.0 + (8.0 / 35.0) * q

def Lwall_vol(q, nr=2400, nmu=500):
    """Leading coefficient of E[N]_vol = E[Lambda_wall]:
    <s_w + q(r0^2 s_w + r0 mu s_w^2 + s_w^3/3)> over x0 uniform in ball,
    u isotropic."""
    r, wr = np.polynomial.legendre.leggauss(nr); r = 0.5 * (r + 1.0); wr = 0.5 * wr
    m, wm = np.polynomial.legendre.leggauss(nmu)
    R, M = np.meshgrid(r, m, indexing="ij")
    sw = -R * M + np.sqrt(R * R * M * M + 1.0 - R * R)
    f = sw + q * (R * R * sw + R * M * sw ** 2 + sw ** 3 / 3.0)
    return float(np.sum(3.0 * R * R * f * wr[:, None] * wm) / 2.0)

# ------------------------------------------------------------------- MC grid
GRID = [(t, q) for t in (0.02, 0.05, 0.1, 0.2) for q in (0.0, 3.0, 10.0)]
PROBE = [(0.002, 0.0), (0.002, 3.0), (0.002, 10.0),
         (0.005, 0.0), (0.005, 3.0), (0.005, 10.0),
         (0.01, 0.0), (0.01, 3.0), (0.01, 10.0),
         (0.3, 0.0), (0.5, 0.0)]
VOL   = [(t, q) for t in (0.02, 0.05, 0.2) for q in (0.0, 3.0, 10.0)]
VOLPR = [(0.002, 0.0), (0.002, 3.0), (0.002, 10.0), (0.005, 0.0), (0.005, 3.0), (0.005, 10.0)]
SEEDS = {p: 2701 + 17 * i for i, p in enumerate(GRID)}
PSEED = {p: 8101 + 17 * i for i, p in enumerate(PROBE)}
VSEED = {p: 5401 + 17 * i for i, p in enumerate(VOLPR + VOL)}
NC, NV = 4_000_000, 4_000_000

def run_grid(points, seeds, n, label, sector=False):
    res = {}
    for p, seed in zip(points, seeds.values()):
        t, q = p
        t0 = time.time()
        r = simulate(n, t, q, "central", seed)
        D, ang, Nv = r["D"], r["ang"], r["N"].astype(float)
        X = D * ang
        m = dict(tau0=t, q=q, n=n)
        if sector:
            m["P1"] = float(np.mean(Nv == 1)); m["sP1"] = se(Nv == 1)
            m["P2"] = float(np.mean(Nv >= 2)); m["sP2"] = se(Nv >= 2)
            m["ED_N1"] = float(np.mean(D * (Nv == 1)))
            m["EDa_N1"] = float(np.mean(X * (Nv == 1)))
            m["sEDa_N1"] = se(X * (Nv == 1))
            m["EDa_Nge2"] = float(np.mean(X * (Nv >= 2)))
            m["sEDa_Nge2"] = se(X * (Nv >= 2))
        m.update(ED=float(np.mean(D)), sD=se(D), E_ang=float(np.mean(ang)),
                 s_ang=se(ang), EN=float(np.mean(Nv)), sN=se(Nv),
                 EDa=float(np.mean(X)), sEDa=se(X), cov=float(np.mean(X) - np.mean(D) * np.mean(ang)),
                 P0=float(np.mean(Nv == 0)))
        R, sR = block_ratio(X, D, ang)
        m["R"] = R; m["sR"] = sR
        m["secs"] = time.time() - t0
        res[p] = m
        log(f"[{label}] tau0={t:5.3f} q={q:5.1f}: E[D]={m['ED']:.6f}+-{m['sD']:.2e} "
            f"E[ang]={m['E_ang']:.6f}+-{m['s_ang']:.2e} E[D*ang]={m['EDa']:.6e}+-{m['sEDa']:.2e} "
            f"R={R:9.3f}+-{sR:.3f}  (R-1 = {R-1:+.3f}); {m['secs']:.1f}s")
    return res

def weighted_fit(x, y, sig, order=2):
    w = 1.0 / np.maximum(sig, 1e-300)
    coef, cov = np.polyfit(x, y, order, w=w, cov=True)
    chi2 = float(np.sum(((y - np.polyval(coef, x)) * w) ** 2))
    scale = max(1.0, chi2 / max(1, len(x) - (order + 1)))
    return coef, np.sqrt(np.diag(cov) * scale), chi2

def main():
    log("=" * 100)
    log("L01 THE THIN-OPACITY EXPANSION OF THE CLOSURE RATIO R = 1 + Cov(D,ang)/(E[D] E[ang])")
    log("kappa = tau0(1+q r^2), T=1, Thomson, central source; n = 4e6 per run; SEs everywhere")
    log("=" * 100)
    res = {"checks": {}, "fits": {}, "measurements": {}, "analytic": {}}
    ok = True

    res["analytic"] = {f"q{q:g}": dict(r1=r1_analytic(q), c2=c2_analytic(q),
                                       r2_one_coll=r2_one_collision(q),
                                       A_v=A_v_analytic(q), Lwall_vol=Lwall_vol(q))
                       for q in (0.0, 3.0, 10.0)}
    log("Analytic: r1(q) = (7/5)(1/2+q/4) = "
        f"{[round(r1_analytic(q), 6) for q in (0., 3., 10.)]}; "
        f"c2 = {[round(c2_analytic(q), 8) for q in (0., 3., 10.)]}; "
        f"r2[N=1 only] = {[round(r2_one_collision(q), 4) for q in (0., 3., 10.)]}; "
        f"A_v(q) = 2/5+8q/35 = {[round(A_v_analytic(q), 6) for q in (0., 3., 10.)]}; "
        f"<Lambda_wall>_vol = {[round(Lwall_vol(q), 6) for q in (0., 3., 10.)]}")

    # ---------------- central grid + probes -------------------------
    log("\n[1] Central thin grid MC (n=4e6)")
    meas = run_grid(GRID, SEEDS, NC, "C")
    log("\n[1b] Deep probes q in {0,3,10} at tau0 = 0.002, 0.005, 0.01  (+ q=0 at 0.3, 0.5), n=8e6")
    meas.update(run_grid(PROBE, PSEED, 8_000_000, "P"))
    res["measurements"]["central"] = {f"t{float(p[0]):g}_q{float(p[1]):g}": meas[p]
                                      for p in GRID + PROBE}

    # ---------------- term-by-term z ---------------------------------
    log("\n[2] Term-by-term z-scores (Marginals: E[D] exact law; E[ang] 2-term law;")
    log("    E[ang] = E[N] identity;  E[D ang] leading law r1*tau0)")
    for p in GRID + PROBE:
        t, q = p; m = meas[p]
        zD = (m["ED"] - (0.5 + q / 4.0) * t) / m["sD"]
        c2 = c2_analytic(q)
        zA2 = (m["E_ang"] - ((1.0 + q / 3.0) * t + c2 * t * t)) / m["s_ang"]
        zAN = (m["E_ang"] - m["EN"]) / (m["s_ang"] + m["sN"])
        zR1 = (m["EDa"] - r1_analytic(q) * t) / m["sEDa"]
        m.update(zE_D=zD, zE_ang2=zA2, zE_angN=zAN, z_r1_lead=zR1)
        if p in GRID:
            res["checks"][f"E_D_t{float(t):g}_q{float(q):g}"] = bool(abs(zD) < 5.0)
            res["checks"][f"angEQN_t{float(t):g}_q{float(q):g}"] = bool(abs(zAN) < 5.0)
            ok &= abs(zD) < 5.0 and abs(zAN) < 5.0
            log(f"  tau0={t:5.3f} q={q:5.1f}: z(E[D])={zD:+6.2f}  z(E[ang] 2-term)={zA2:+6.2f}  "
                f"z(E[ang]=E[N])={zAN:+6.2f}  z(r1*tau0)={zR1:+6.2f}  P0={m['P0']:.5f}")
        else:
            if p[0] <= 0.005 and q <= 3.0 or (p[0] <= 0.002 and q == 10.0):
                res["checks"][f"r1_lead_t{float(t):g}_q{float(q):g}"] = bool(abs(zR1) < 5.0)
                ok &= abs(zR1) < 5.0
            log(f"  tau0={t:5.3f} q={q:5.1f}: z(r1*tau0)={zR1:+6.2f}  (probe)")

    # ---------------- N=1 sector exact tests --------------------------
    log("\n[2b] First-flight + one-collision sector, EXACT quadrature vs MC (all orders in tau0)")
    log("  (sector masks computed from dedicated runs)")
    sector_runs = {}
    for (t, q) in [(0.02, 0.0), (0.02, 3.0), (0.02, 10.0), (0.05, 0.0), (0.05, 3.0), (0.05, 10.0)]:
        r = simulate(NC, t, q, "central", seed=SEEDS[(t, q)] + 5000)
        D, ang, Nv = r["D"], r["ang"], r["N"].astype(float)
        X = D * ang
        m1 = (Nv == 1)
        P1, sP1 = float(np.mean(m1)), se(m1)
        ED1, sED1 = float(np.mean(D * m1)), se(D * m1)
        EDa1, sEDa1 = float(np.mean(X * m1)), se(X * m1)
        EDa2, sEDa2 = float(np.mean(X * (Nv >= 2))), se(X * (Nv >= 2))
        P1a, ED1a, EDa1a = N1_quadrature(q, t)
        sector_runs[(t, q)] = dict(P1=P1, sP1=sP1, ED1=ED1, sED1=sED1,
                                   EDa1=EDa1, sEDa1=sEDa1, EDa2=EDa2, sEDa2=sEDa2)
        zP = (P1 - P1a) / sP1; zE = (ED1 - ED1a) / sED1; zX = (EDa1 - EDa1a) / sEDa1
        res["checks"][f"N1_t{t:g}_q{q:g}_P"] = abs(zP) < 5.0
        res["checks"][f"N1_t{t:g}_q{q:g}_ED"] = abs(zE) < 5.0
        res["checks"][f"N1_t{t:g}_q{q:g}_EDa"] = abs(zX) < 5.0
        ok &= abs(zP) < 5.0 and abs(zE) < 5.0 and abs(zX) < 5.0
        log(f"  tau0={t:5.3f} q={q:5.1f}: P1 MC={P1:.6f} an={P1a:.6f} z={zP:+6.2f} | "
            f"E[D|N=1] MC={ED1:.6e} an={ED1a:.6e} z={zE:+6.2f} | "
            f"E[D*ang|N=1] MC={EDa1:.6e} an={EDa1a:.6e} z={zX:+6.2f} | "
            f"N>=2 share E[D*ang]={EDa2:.4e}")
    res["measurements"]["sector"] = {f"t{float(t):g}_q{float(q):g}": v
                                     for (t, q), v in sector_runs.items()}

    # --------------- fits: leading + quadratic coefficients --------------
    log("\n[3] Weighted fits over deep probes + grid:  y = E[D*ang]/tau0 = r1 + r2 x + r3 x^2")
    fits = {}
    for q in (0.0, 3.0, 10.0):
        pts = [p for p in GRID + PROBE if p[1] == q]
        x = np.array([p[0] for p in pts]); y = np.array([meas[p]["EDa"] / p[0] for p in pts])
        sig = np.array([meas[p]["sEDa"] / p[0] for p in pts])
        coef, sd, chi2 = weighted_fit(x, y, sig, order=2)   # coef: [r3, r2, r1]
        r1f, s1 = coef[2], sd[2]
        zkill = abs(r1f - r1_analytic(q)) / s1
        fits[q] = dict(r1_fit=float(r1f), s1=float(s1), r2_fit=float(coef[1]),
                       s2=float(sd[1]), r3_fit=float(coef[0]), chi2=chi2,
                       z_r1_vs_analytic=float(zkill))
        res["checks"][f"KILL_r1_q{q:g}"] = bool(zkill < 5.0)
        ok &= zkill < 5.0
        log(f"  q={q:5.1f}: r1_fit={r1f:.4f}+-{s1:.4f} vs an {r1_analytic(q):.4f} "
            f"z={zkill:5.2f} ; r2_fit={coef[1]:+.4f}+-{sd[1]:.4f} (N=1-only an "
            f"{r2_one_collision(q):+.4f}) ; chi2={chi2:8.2f}")
    res["fits"]["EDa"] = fits

    log("\n[3a] E[ang]/tau0 = (1+q/3) + c2 x + c3 x^2 fits (c2 tests K04's analytic)")
    fitsA = {}
    for q in (0.0, 3.0, 10.0):
        pts = [p for p in GRID + PROBE if p[1] == q and p[0] <= 0.3]
        x = np.array([p[0] for p in pts]); y = np.array([meas[p]["E_ang"] / p[0] for p in pts])
        sig = np.array([meas[p]["s_ang"] / p[0] for p in pts])
        coef, sd, chi2 = weighted_fit(x, y, sig, order=2)
        zc = abs(coef[1] - c2_analytic(q)) / sd[1]
        fitsA[q] = dict(lead_fit=float(coef[2]), lead_an=1.0 + q / 3.0,
                        c2_fit=float(coef[1]), s2=float(sd[1]), z_c2=float(zc), chi2=chi2)
        res["checks"][f"C2_q{q:g}"] = bool(zc < 5.0)
        ok &= zc < 5.0
        log(f"  q={q:5.1f}: (1+q/3) fit {coef[2]:.4f}+-{sd[2]:.4f} (an {1+q/3:.4f}); "
            f"c2 fit {coef[1]:+.5f}+-{sd[1]:.5f} vs an {c2_analytic(q):.6f} z={zc:5.2f}; "
            f"chi2={chi2:7.2f}")
    res["fits"]["Eang"] = fitsA

    # ---------------- premise tests ------------------------------------
    log("\n[3b] Premised form  R-1 = C*tau0 : fit over the grid; residual test")
    for q in (0.0, 3.0, 10.0):
        pts = [(t, meas[(t, q)]) for t in (0.02, 0.05, 0.1, 0.2)]
        x = np.array([t for t, _ in pts]); y = np.array([m["R"] - 1 for _, m in pts])
        w = np.array([1.0 / m["sR"] for _, m in pts])
        C = float(np.sum(x * y * w ** 2) / np.sum(x * x * w ** 2))
        zres = (y - C * x) * w
        res["fits"][f"premise_q{q:g}"] = dict(C=C, zmax=float(np.max(np.abs(zres))),
                                             zmax_at=float(pts[int(np.argmax(np.abs(zres)))][0]))
        res["checks"][f"PREMISE_q{q:g}_killed"] = bool(np.max(np.abs(zres)) > 5.0)
        ok &= np.max(np.abs(zres)) > 5.0
        log(f"  q={q:5.1f}: C_fit={C:.4f}, max|resid|/SE = {np.max(np.abs(zres)):8.2f} "
            f"at tau0={pts[int(np.argmax(np.abs(zres)))][0]:5.2f}  -> premise KILLED"
            f"{'' if np.max(np.abs(zres)) > 5 else ' (no)'}")

    log("\n[3c] Derived leading law for R:  R*tau0*(1+q/3)*5/7 -> 1 + g*tau0 as tau0 -> 0")
    for q in (0.0, 3.0, 10.0):
        r2f = fits[q]["r2_fit"]
        g = r2f / r1_analytic(q) - c2_analytic(q) / (1.0 + q / 3.0)
        for t in (0.002, 0.005, 0.01):
            m = meas[(t, q)]
            P = m["R"] * t * (1.0 + q / 3.0) * (5.0 / 7.0)
            sP = P * m["sR"] / m["R"]
            g_fit = g * t
            res["checks"][f"Rpref_t{float(t):g}_q{q:g}"] = bool(
                abs(P - (1.0 + g_fit)) < 5.0 * sP + 0.02 * t)
            ok &= abs(P - (1.0 + g_fit)) < 5.0 * sP + 0.02 * t
            log(f"  tau0={t:5.3f} q={q:5.1f}: R*tau0*(1+q/3)*(5/7) = {P:.4f}+-{sP:.4f} "
                f"(-> 1 + {g:.2f}*tau0 = {1.0 + g_fit:.4f})")

    # ---------------- break depth --------------------------------------
    log("\n[4] Break depth (first sampled depth with |residual| > 5 SE)")
    for q in (0.0, 3.0, 10.0):
        r2f = fits[q]["r2_fit"]
        d_lead = d_2t = None
        for p in GRID + PROBE:
            if p[1] != q:
                continue
            t, m = p[0], meas[p]
            if d_lead is None and abs(m["z_r1_lead"]) > 5.0:
                d_lead = t
            z2 = (m["EDa"] - (r1_analytic(q) * t + r2f * t * t)) / m["sEDa"]
            if d_2t is None and abs(z2) > 5.0:
                d_2t = t
        res["measurements"][f"break_q{q:g}"] = dict(leading=d_lead, two_term=d_2t)
        log(f"  q={q:5.1f}: leading law r1*tau0 valid through tau0 < {d_lead}; "
            f"two-term law valid through tau0 < {d_2t}")

    # ---------------- volume face ---------------------------------------
    log("\n[5] Volume face:  E[D]_vol = tau0*(2/5+8q/35) + O(tau0^2);  E[ang]_vol leading = tau0*<Lambda_wall>")
    vmeas = {}
    for p in VOLPR + VOL:
        t, q = p
        r = simulate(NV, t, q, "volume", seed=VSEED[p])
        D, ang = r["D"], r["ang"]
        ED, sD = float(np.mean(D)), se(D)
        av = A_v_analytic(q); lw = Lwall_vol(q)
        z = (ED - t * av) / sD
        Ea, sA = float(np.mean(ang)), se(ang)
        zN = (Ea - t * lw) / sA
        vmeas[p] = dict(ED=ED, sD=sD, z_single_term=z, E_ang=Ea, s_ang=sA, z_Nlead=zN)
        if t <= 0.002:
            res["checks"][f"vol_Av_t{float(t):g}_q{q:g}"] = bool(abs(z) < 5.0)
            ok &= abs(z) < 5.0
        if t <= 0.002 and q == 0.0:
            res["checks"][f"vol_Nlead_t{float(t):g}_q{float(q):g}"] = bool(abs(zN) < 5.0)
            ok &= abs(zN) < 5.0
        log(f"  tau0={t:5.3f} q={q:5.1f}: E[D]_vol={ED:.6e}+-{sD:.2e} tau0*A_v={t*av:.6e} "
            f"z={z:+6.2f} | E[ang]={Ea:.6f}+-{sA:.2e} tau0*<Lam>={t*lw:.6f} z={zN:+6.2f}")
    res["measurements"]["volume"] = {f"t{float(p[0]):g}_q{float(p[1]):g}": vmeas[p]
                                     for p in VOLPR + VOL}

    log("\n[5b] Volume fit  E[D]_vol/tau0 = A + b*tau0 + c*tau0^2  (6 depths per q)")
    for q in (0.0, 3.0, 10.0):
        pts = [p for p in VOLPR + VOL if p[1] == q]
        x = np.array([p[0] for p in pts]); y = np.array([vmeas[p]["ED"] / p[0] for p in pts])
        sig = np.array([vmeas[p]["sD"] / p[0] for p in pts])
        coef, sd, chi2 = weighted_fit(x, y, sig, order=2)
        zA = abs(coef[2] - A_v_analytic(q)) / sd[2]
        res["checks"][f"KILL_Av_q{q:g}"] = bool(zA < 5.0)
        ok &= zA < 5.0
        log(f"  q={q:5.1f}: A_fit={coef[2]:.4f}+-{sd[2]:.4f} vs an {A_v_analytic(q):.4f} "
            f"z={zA:5.2f} ; b_fit={coef[1]:+.4f}+-{sd[1]:.4f} ; chi2={chi2:6.2f}")
        res["fits"][f"volD_q{q:g}"] = dict(A_fit=float(coef[2]), sA=float(sd[2]),
                                          A_an=A_v_analytic(q), z=float(zA))

    res["total_checks"] = len(res["checks"])
    res["passed"] = int(sum(1 for v in res["checks"].values() if v))
    res["ALL_PASSED"] = bool(ok)
    res["verdict"] = ("PASS: derived expansion (r1 = (7/5)(1/2+q/4), 1/tau0 law for R-1) "
                      "survives its own 5-SE gate; the PREMISED O(tau0) expansion of R-1 is "
                      "refuted at 5+ SE" if ok else "FAIL: see checks")
    with open("L01_results.json", "w") as fh:
        json.dump(res, fh, indent=1, allow_nan=False)
    log("=" * 100)
    log(f"CHECKS {res['passed']}/{res['total_checks']}  ALL_PASSED={bool(ok)}")
    log(res["verdict"])
    log("=" * 100)
    with open("L01_closure_expansion.out", "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())