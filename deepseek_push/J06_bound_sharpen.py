#!/usr/bin/env python3
"""
J06 -- SHARPENING THE J05 TRANSFER-FUNCTION BOUND + THE VOLUME PORT
2026-09-23.  Continuation of J05 on the JWST_EQUATION_TARGET moment channel.
Append-only: J05 files untouched; this file adds J06 artifacts only.

CONTENT
  (1) The m-th order bound chain.  Cauchy-Schwarz on (D, ang^m):
          E[D ang^m]^2 <= E[D^2] E[ang^{2m}]
      with the exact conditional-Gaussian relations (J01/J02, all m)
          E[D ang^m]  = E[D v^{2m}] / ((2m-1)!! * 2^m)
          E[ang^{2m}] = E[v^{4m}]  / ((4m-1)!! * 2^{2m})
      gives the exact chain (the task's candidate coefficient 12 is WRONG;
      the exact m=2 coefficient is 35/3 = 11.6667, i.e. 12 * 35/36):
          E[D^2] >= B_m := C_m * E[D v^{2m}]^2 / E[v^{4m}],
          C_m = (4m-1)!! / ((2m-1)!!)^2,    C_1=3, C_2=35/3, C_3=10395/225.
      Which of B_1, B_2, B_3 is tightest is decided empirically per cloud
      (the fourth powers ang^2 -> v^8 -> v^12 make the rate of the MC
      estimator heavier with m; block-jackknife SEs are reported everywhere).

  (2) Slack analysis.  With rho0_m := E[D ang^m]/sqrt(E[D^2] E[ang^{2m}])
      (correlation about the ORIGIN -- here means are positive, so the
      centered Pearson correlation differs), the slack is EXACTLY
          slack_m = E[D^2]/B_m = E[D^2] E[ang^{2m}] / E[D ang^m]^2 = 1/rho0_m^2.
      Both forms are computed independently (v-moments vs ang-moments) and
      forced to agree -- that is the machine check of the whole chain.
      The Pearson version 1/rho_Pearson^2 is measured and its discrepancy
      from the exact slack is quantified (honest edge).

  (3) Sharpness.  (a) BY CONSTRUCTION: the pair D = c*ang (pointwise) with
      v | ang ~ N(0, 2*ang) satisfies EVERY exact relation of the model at
      every order, and for it slack_1 = 1 exactly: the bound is attained
      inside the moment-constrained family -- the inequalities alone cannot
      be improved.  (b) IN THE MODEL: as q -> inf the mean number of
      scatterings per photon diverges and (D, ang) become driven by the same
      accumulating trajectory, so corr -> 1 and slack -> 1.  Measured on a
      q-scan q = 0,3,10,30,100 (central).

  (4) The volume port of the falsifier.  The CS inequality is source-agnostic
      (it uses only joint moments that exist for either source), so
          E[D^2]_vol >= B_1, B_2
      must hold on the volume clouds as well -- verified.  The MEAN relation
      does not port: the observer must use E[D]_vol = E[tau]_vol - E[Q] with
      the Dynkin compensation E[tau]_vol = int r kappa dr + E[mu_exit]
      - (1/2) E[F(r0)]; for kappa = tau0(1+q r^2), tau0 = 1, R = 1:
          E[tau]_vol = (1/2 + q/4) + E[mu_exit] - (3/10 + 3q/28).
      Q is measured per cloud and the full Dynkin statement is verified at
      q = 0, 3, 10 (E[mu_exit] by a dedicated escape-face estimator).

Every number below is machine-checked on the J01/J02 independent solver
(exact optical-depth bisection; no null-collision thinning), numpy only.
"""
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from J02_moment_hierarchy import simulate, simulate_Q, thomson_mu, rate_integral

OUT = "J06_results.json"


def ddf_2m_minus_1(m):
    """(2m-1)!!"""
    return math.prod(range(1, 2 * m, 2))


def C_m(m):
    """Exact bound coefficient (4m-1)!!/((2m-1)!!)^2 : 3, 35/3, 10395/225,..."""
    return ddf_2m_minus_1(2 * m) / ddf_2m_minus_1(m) ** 2


def jack_se(arrays, stat, B=24):
    """Delete-one-block jackknife SE of stat(list-of-arrays) -> float.
    Arrays are split in lockstep into B contiguous blocks."""
    n = len(arrays[0])
    mask_all = np.ones(n, bool)
    full = float(stat(arrays))
    lo = np.empty(B)
    cuts = np.linspace(0, n, B + 1, dtype=int)
    for i in range(B):
        m = mask_all.copy()
        m[cuts[i]:cuts[i + 1]] = False
        lo[i] = float(stat([a[m] for a in arrays]))
    se = float(np.sqrt((B - 1) / B * np.sum((lo - lo.mean()) ** 2)))
    return full, se


# --------------------------------------------------------------------------
# escape-face estimator of E[mu_exit] (q-cloud version of the J02 estimator)
# --------------------------------------------------------------------------
def mu_exit_estimator(n, q, seed):
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    d0 = rng.normal(size=(n, 3))
    d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
    pos = d0 * rng.random(n)[:, None] ** (1 / 3)
    direc = rng.normal(size=(n, 3))
    direc = direc / np.linalg.norm(direc, axis=1)[:, None]
    mus = np.zeros(n)
    al = np.arange(n)
    while len(al):
        p, u = pos[al], direc[al]
        pd = np.sum(p * u, axis=1)
        r2 = np.sum(p * p, axis=1)
        disc = pd * pd - r2 + 1.0
        wall = -pd + np.sqrt(np.maximum(disc, 0.0))
        U = rng.random(len(al))
        esc = rate_integral(r2, pd, wall, 1.0, q) <= -np.log(U)
        s = wall.copy()
        inside = al[~esc]
        if len(inside):
            p2, u2 = pos[inside], direc[inside]
            pd2 = np.sum(p2 * u2, axis=1)
            r22 = np.sum(p2 * p2, axis=1)
            lo = np.zeros(len(inside))
            hi = wall[~esc]
            Ui = U[~esc]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r22, pd2, mid, 1.0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]
                hi[~tak] = mid[~tak]
            s[~esc] = 0.5 * (lo + hi)
        pos[al] += direc[al] * s[:, None]
        esc_idx = al[esc]
        xh = pos[esc_idx] / np.linalg.norm(pos[esc_idx], axis=1)[:, None]
        mus[esc_idx] = np.sum(xh * direc[esc_idx], axis=1)
        al = al[~esc]
        if len(al) == 0:
            break
        p, u = pos[al], direc[al]
        r2 = np.sum(p * p, axis=1)
        mu = thomson_mu(rng, len(al))
        t = rng.normal(size=(len(al), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        direc[al] = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
    return float(np.mean(mus)), float(np.std(mus, ddof=1) / np.sqrt(n))


# --------------------------------------------------------------------------
# per-cloud bound-chain analysis
# --------------------------------------------------------------------------
def analyze_cloud(n, tau0, q, source, seed, tag):
    t0 = time.time()
    r = simulate(n, tau0, q, source, seed)
    D = r["D"]
    ang = r["ang"]
    v2 = r["v2"]
    dt = time.time() - t0

    arr = dict(D=D, ang=ang, v2=v2, Dv2=D * v2, v4=r["v4"],
               Dv4=D * r["v4"], v8=v2 ** 4, Dv6=D * v2 ** 3, v12=v2 ** 6,
               Dang=D * ang, ang2=ang ** 2, Dang2=D * ang ** 2, ang4=ang ** 4,
               Dang3=D * ang ** 3, ang6=ang ** 6, D2=D ** 2)

    def st(keys, fn):
        return jack_se([arr[k] for k in keys], lambda A: fn(*A))

    mD2, sD2 = st(["D2"], lambda D2: np.mean(D2))
    C1, C2, C3 = C_m(1), C_m(2), C_m(3)

    # bound values B_m (via velocity moments)
    B1, sB1 = st(["Dv2", "v4"], lambda a, b: 3.0 * np.mean(a) ** 2 / np.mean(b))
    B2, sB2 = st(["Dv4", "v8"], lambda a, b: C2 * np.mean(a) ** 2 / np.mean(b))
    B3, sB3 = st(["Dv6", "v12"], lambda a, b: C3 * np.mean(a) ** 2 / np.mean(b))

    # slacks via angular moments  slack_m = E[D^2] E[ang^{2m}]/E[D ang^m]^2
    sl1, ssl1 = st(["D2", "ang2", "Dang"],
                   lambda a, b, c: np.mean(a) * np.mean(b) / np.mean(c) ** 2)
    sl2, ssl2 = st(["D2", "ang4", "Dang2"],
                   lambda a, b, c: np.mean(a) * np.mean(b) / np.mean(c) ** 2)
    sl3, ssl3 = st(["D2", "ang6", "Dang3"],
                   lambda a, b, c: np.mean(a) * np.mean(b) / np.mean(c) ** 2)

    # cross-forms: E[D^2]/B_m must equal slack_m (whole-chain machine check).
    # Both estimators live on the SAME sample.  For m = 2, 3 the velocity
    # path is heavy-tailed (v^8, v^12 per photon), so the SE of the
    # difference is built from per-photon standard errors via the delta
    # method (block jackknife with few blocks underestimates such tails).
    def delta_se(keyA, keyB, C):
        # SE of C * mean(A)^2 / mean(B) by log-delta on per-photon SEs
        A = arr[keyA]
        B = arr[keyB]
        mA = float(np.mean(A))
        mB = float(np.mean(B))
        seA = float(np.std(A, ddof=1) / np.sqrt(len(A)))
        seB = float(np.std(B, ddof=1) / np.sqrt(len(B)))
        se_log = np.sqrt((2.0 * seA / mA) ** 2 + (seB / mB) ** 2)
        return C * mA * mA / mB * se_log

    sc1 = delta_se("Dv2", "v4", 3.0)
    sc2 = delta_se("Dv4", "v8", C2)
    sc3 = delta_se("Dv6", "v12", C3)
    crossz = {1: abs(mD2 / B1 - sl1) / np.sqrt((mD2 / B1 * sc1 / B1) ** 2
                                                 + ssl1 ** 2),
              2: abs(mD2 / B2 - sl2) / np.sqrt((mD2 / B2) ** 2 * (sc2 / B2) ** 2
                                                 + ssl2 ** 2),
              3: abs(mD2 / B3 - sl3) / np.sqrt((mD2 / B3) ** 2 * (sc3 / B3) ** 2
                                                 + ssl3 ** 2)}

    # falsifier z-scores: how many SE the bounds lie below E[D^2]
    def diffstat(keyD2, keyA, keyB, C):
        def f(A):
            return np.mean(A[0]) - C * np.mean(A[1]) ** 2 / np.mean(A[2])
        return jack_se([arr[keyD2], arr[keyA], arr[keyB]], f)

    d1, sd1 = diffstat("D2", "Dv2", "v4", 3.0)
    z1 = d1 / sd1
    d2, sd2 = diffstat("D2", "Dv4", "v8", C2)
    z2 = d2 / sd2

    # hierarchy concordance m = 1,2,3 (E[D v^{2m}] vs (2m-1)!! 2^m E[D ang^m]),
    # z-based exactly as J01/J02 (difference within 5 combined per-photon SE)
    def pairz(keyA, keyB, mult):
        A = arr[keyA]
        B = arr[keyB]
        return abs(float(np.mean(A) - mult * np.mean(B))) / (
            float(np.std(A, ddof=1) / np.sqrt(len(A)))
            + mult * float(np.std(B, ddof=1) / np.sqrt(len(B))))

    hierz = {1: pairz("Dv2", "Dang", 2.0),
             2: pairz("Dv4", "Dang2", 12.0),
             3: pairz("Dv6", "Dang3", 120.0)}
    # Gaussian lemma at m = 2,3: E[v^{4m}] vs (4m-1)!! 2^{2m} E[ang^{2m}]
    gz2 = pairz("v8", "ang4", 1680.0)
    gz3 = pairz("v12", "ang6", 665280.0)

    # correlations: origin (exact) vs Pearson (approximate)
    rho0_1 = mD2 ** -0.5 * np.mean(arr["Dang"]) / np.sqrt(np.mean(arr["ang2"]))
    rho0_2 = mD2 ** -0.5 * np.mean(arr["Dang2"]) / np.sqrt(np.mean(arr["ang4"]))
    rhoP1 = float(np.corrcoef(D, ang)[0, 1])
    rhoP2 = float(np.corrcoef(D, ang ** 2)[0, 1])

    return dict(tag=tag, source=source, tau0=tau0, q=q, n=n, seed=seed,
                secs=round(dt, 1), Nbar=float(np.mean(r["N"])),
                E_D2=mD2, s_E_D2=sD2,
                E_Dv2=float(np.mean(arr["Dv2"])), E_v4=float(np.mean(arr["v4"])),
                E_Dv4=float(np.mean(arr["Dv4"])), E_v8=float(np.mean(arr["v8"])),
                E_Dv6=float(np.mean(arr["Dv6"])), E_v12=float(np.mean(arr["v12"])),
                B1=B1, s_B1=sB1, B2=B2, s_B2=sB2, B3=B3, s_B3=sB3,
                slack1=sl1, s_slack1=ssl1, slack2=sl2, s_slack2=ssl2,
                slack3=sl3, s_slack3=ssl3,
                crossz1=crossz[1], crossz2=crossz[2], crossz3=crossz[3],
                falsifier_z1=z1, falsifier_z2=z2,
                gauss_z2=gz2, gauss_z3=gz3,
                hier_z1=hierz[1], hier_z2=hierz[2], hier_z3=hierz[3],
                rho0_1=rho0_1, rho0_2=rho0_2, rho_pearson_1=rhoP1,
                rho_pearson_2=rhoP2, inv_rhoP1_sq=1.0 / rhoP1 ** 2,
                inv_rhoP2_sq=1.0 / rhoP2 ** 2,
                E_D=float(np.mean(D)), E_tau=float(np.mean(r["elapsed"])),
                E_ang=float(np.mean(ang)))


def main():
    res = {"checks": {}, "clouds": {}, "volume": {}, "sharpness": {}}
    ok = True
    C2 = C_m(2)  # 35/3 ; the naive '12' is off by 35/36

    print("=" * 78)
    print("J06 -- BOUND SHARPENING: chain C_m = (4m-1)!!/((2m-1)!!)^2")
    print("  C_1 = 3, C_2 = 35/3 = %.6f (task candidate 12 is WRONG: factor 35/36),"
          % C2)
    print("  C_3 = 10395/225 = %g" % C_m(3))
    print("=" * 78)

    # ---------------- main clouds: six (source, q) + tau0=2 row ------------
    clouds = [("central", 1.0, 0.0, 1200000, 1007, "central_q0"),
              ("central", 1.0, 3.0, 1200000, 2007, "central_q3"),
              ("central", 1.0, 10.0, 1200000, 3007, "central_q10"),
              ("central", 2.0, 3.0, 1200000, 4007, "central_tau2_q3"),
              ("volume", 1.0, 0.0, 1200000, 5007, "volume_q0"),
              ("volume", 1.0, 3.0, 1200000, 6007, "volume_q3"),
              ("volume", 1.0, 10.0, 1200000, 7007, "volume_q10")]
    for src, tau0, q, n, seed, tag in clouds:
        c = analyze_cloud(n, tau0, q, src, seed, tag)
        res["clouds"][tag] = c
        # whole-chain check: slope of E[D^2]/B_m vs slack_m difference, in
        # jackknife-SE units of the difference itself (both same-sample
        # estimators; the heavy velocity moments dominate the noise)
        for m in (1, 2, 3):
            zch = c[f"crossz{m}"]
            good = zch < 5.0
            res["checks"][f"chain_m{m}_{tag}"] = bool(good)
            ok &= bool(good)
        # hierarchy + Gaussian lemma: z-based, J01/J02 convention (< 5 SE)
        for m in (1, 2, 3):
            good = c[f"hier_z{m}"] < 5.0
            res["checks"][f"hier_m{m}_{tag}"] = bool(good)
            ok &= bool(good)
        for m in (2, 3):
            good = c[f"gauss_z{m}"] < 5.0
            res["checks"][f"gauss_lemma_m{m}_{tag}"] = bool(good)
            ok &= bool(good)
        # falsifier never fires on this model: E[D^2] - B_m > 3 SE
        res["checks"][f"falsifier_m1_holds_{tag}"] = bool(c["falsifier_z1"] > 3.0)
        res["checks"][f"falsifier_m2_holds_{tag}"] = bool(c["falsifier_z2"] > 3.0)
        ok &= c["falsifier_z1"] > 3.0 and c["falsifier_z2"] > 3.0
        # slack identity: slack1 == 1/rho0_1^2  (exact, origin correlation)
        good = abs(c["slack1"] - 1.0 / c["rho0_1"] ** 2) < 6.0 * c["s_slack1"]
        res["checks"][f"slack_rho0_exact_{tag}"] = bool(good)
        ok &= bool(good)
        print(f"[{tag:16s}] E[D^2]={c['E_D2']:.4f}  B1={c['B1']:.4f}  "
              f"B2={c['B2']:.4f}  B3={c['B3']:.4f}  "
              f"slack1={c['slack1']:.4f}+-{c['s_slack1']:.4f}  "
              f"slack2={c['slack2']:.4f}+-{c['s_slack2']:.4f}  "
              f"slack3={c['slack3']:.4f}+-{c['s_slack3']:.4f}  "
              f"rhoP1={c['rho_pearson_1']:.4f} 1/rhoP1^2={c['inv_rhoP1_sq']:.4f}")

    print("-" * 78)
    print("Tightest bound per cloud (B1 vs B2 vs B3, with SE):")
    tight = {}
    for tag, c in res["clouds"].items():
        bs = {"B1": (c["B1"], c["s_B1"]), "B2": (c["B2"], c["s_B2"]),
              "B3": (c["B3"], c["s_B3"])}
        best = max(bs, key=lambda k: bs[k][0])
        tight[tag] = best
        print(f"  {tag:16s} {best} (slack {c[f'slack{int(best[1:])}']:.4f})")
    res["tightest_per_cloud"] = tight

    # ---------------- sharpness (a): attainability by construction ---------
    print("-" * 78)
    print("Sharpness (a): construction D = c*ang, v|ang ~ N(0,2ang) -- all")
    print("exact relations hold and slack_1 = 1 EXACTLY (bound attained).")
    rng = np.random.default_rng(10007)
    Nt = 2000000
    angT = rng.gamma(3.0, 1.0, Nt)
    DT = 2.0 * angT                        # D = c*ang pointwise
    v2T = 2.0 * angT * rng.chisquare(1, Nt)  # v^2|ang ~ 2 ang chi2_1
    v4T = v2T ** 2
    v8T = v2T ** 4
    t = dict(
        slack1=(np.mean(DT ** 2) * np.mean(angT ** 2)) / np.mean(DT * angT) ** 2,
        hier_m1=np.mean(DT * v2T) / (2.0 * np.mean(DT * angT)),
        hier_m2=np.mean(DT * v4T) / (12.0 * np.mean(DT * angT ** 2)),
        gauss_m2=np.mean(v8T) / (1680.0 * np.mean(angT ** 4)),
        B1_over_ED2=3.0 * np.mean(DT * v2T) ** 2 / np.mean(v4T) / np.mean(DT ** 2))
    res["sharpness"]["construction"] = t
    res["checks"]["construction_attains"] = bool(
        abs(t["slack1"] - 1.0) < 2e-3 and abs(t["hier_m1"] - 1.0) < 2e-3
        and abs(t["hier_m2"] - 1.0) < 2e-2 and abs(t["gauss_m2"] - 1.0) < 5e-2)
    ok &= res["checks"]["construction_attains"]
    print(f"  toy slack1 = {t['slack1']:.5f}  hier m1 = {t['hier_m1']:.5f}  "
          f"m2 = {t['hier_m2']:.5f}  gauss m2 = {t['gauss_m2']:.5f}  "
          f"B1/E[D^2] = {t['B1_over_ED2']:.5f}")

    # ---------------- sharpness (b): q-scan toward slack -> 1 -------------
    print("-" * 78)
    print("Sharpness (b): q-scan central (LLN: Nbar -> inf, corr -> 1):")
    qscan = {}
    for q, n, seed in ((0.0, 1200000, 1007), (3.0, 1200000, 2007),
                       (10.0, 1200000, 3007), (30.0, 300000, 8007),
                       (100.0, 300000, 9007)):
        c = res["clouds"].get(f"central_q{int(q)}") or analyze_cloud(
            n, 1.0, q, "central", seed, f"central_q{int(q)}")
        qscan[f"q{int(q)}"] = dict(Nbar=c["Nbar"], slack1=c["slack1"],
                                   s_slack1=c["s_slack1"],
                                   rho0_1=c["rho0_1"], rhoP1=c["rho_pearson_1"])
    res["sharpness"]["q_scan"] = qscan
    qs = [0, 3, 10, 30, 100]
    mono = all(qscan[f"q{q}"]["rho0_1"] <= qscan[f"q{qp}"]["rho0_1"] + 1e-6
               for q, qp in zip(qs, qs[1:]))
    res["checks"]["qscan_rho_increasing"] = bool(mono)
    ok &= bool(mono)
    for q in qs:
        s = qscan[f"q{q}"]
        print(f"  q={q:4d}  Nbar={s['Nbar']:6.2f}  slack1={s['slack1']:.5f} "
              f"+/- {s['s_slack1']:.5f}  rho0_1={s['rho0_1']:.5f}  "
              f"rhoP1={s['rhoP1']:.5f}")

    # ---------------- volume port: Q-coupling + Dynkin ---------------------
    print("-" * 78)
    print("Volume port: E[D]_vol = E[tau]_vol - E[Q],  Dynkin "
          "E[tau]_vol = (1/2+q/4) + E[mu_exit] - (3/10 + 3q/28):")
    for q, seedQ, seedMu in ((0.0, 11007, 14007), (3.0, 12007, 15007),
                             (10.0, 13007, 16007)):
        vc = res["clouds"][f"volume_q{int(q)}"]
        rq = simulate_Q(100000, 1.0, q, "volume", seedQ)
        E_Q = float(np.mean(rq["Q"]))
        s_Q = float(np.std(rq["Q"], ddof=1) / np.sqrt(len(rq["Q"])))
        E_tau = vc["E_tau"]
        Emu, sEmu = mu_exit_estimator(150000, q, seedMu)
        pred_tau = (0.5 + q / 4.0) + Emu - (0.3 + 3.0 * q / 28.0)
        diff_Q = abs(E_Q - (E_tau - vc["E_D"]))
        res["volume"][f"q{int(q)}"] = dict(
            E_Q=E_Q, s_E_Q=s_Q, E_tau=E_tau, E_D=vc["E_D"],
            tau_minus_D=E_tau - vc["E_D"], Q_diff=diff_Q,
            E_mu_exit=Emu, s_mu_exit=sEmu, dynkin_pred=pred_tau,
            dynkin_absdiff=abs(pred_tau - E_tau))
        # Q bookkeeping identity at each q
        good = diff_Q < 6.0 * (s_Q + 1e-6)
        res["checks"][f"Q_identity_q{int(q)}"] = bool(good)
        ok &= bool(good)
        # Dynkin closed form at each q (SE dominated by mu_exit estimator)
        good = abs(pred_tau - E_tau) < 8.0 * max(sEmu, 1e-3) + 1e-3
        res["checks"][f"dynkin_q{int(q)}"] = bool(good)
        ok &= bool(good)
        print(f"  q={int(q)}  E[Q]={E_Q:.4f}+-{s_Q:.5f}  "
              f"E[tau]-E[D]={E_tau - vc['E_D']:.4f}  "
              f"E[mu_exit]={Emu:.4f}  Dynkin pred={pred_tau:.4f}  "
              f"E[tau]_meas={E_tau:.4f}")

    res["checks"]["ALL_PASSED"] = bool(ok)
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["C_m"] = {"C1": 3.0, "C2": 35.0 / 3.0, "C3": 10395.0 / 225.0}

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT),
              "w") as f:
        json.dump(res, f, indent=1)
    print("=" * 78)
    print(f"checks {res['passed']}/{res['total_checks']} passed; saved {OUT}")
    print("ALL J06 CHECKS PASSED" if ok else "J06 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())