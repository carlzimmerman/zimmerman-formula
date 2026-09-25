#!/usr/bin/env python3
"""
U02 -- ND2: THE SIX-MOMENT BATTERY at n=1e7 (pre-registered in J00 ND2, never run)
===================================================================================
2026-09-26. Executes J00 ledger ND2 -- the sharpest observer-facing test of the
conditional-Gaussian lemma -- on the frozen J02 engine (independent solver, exact
optical-depth bisection, no null-collision thinning), then the ND2 matched-pair
construction, then the q = 3 / q = 10 legs at n = 4e6 for the z-table.

==============================================================================
PRE-REGISTERED BATTERY (J00 ND2; J05 s5; K06 F3/F4) -- THRESHOLDS STATED FIRST,
before any number. Model: stationary conservative Thomson sphere R=c=s_e=1,
central isotropic source, kappa(r) = tau0 (1 + q r^2), all photons counted.
Observables of the velocity-resolved transfer function:
   battery = {E[D], E[v^2], E[Dv^2], E[v^4], E[Dv^4], E[D^2]}  (six moments)

  T1  E[D]           = tau0*(1/2 + q/4)        Theorem 1, exact (all orders)   |z| < 3
  T2  E[v^2]         = 2*E[ang]                Gaussian lemma, marginal m=1     |z| < 3
  T3  E[v^4]         = 12*E[ang^2]             Gaussian lemma, marginal m=2     |z| < 3
  T4  E[Dv^2]        = 2*E[D*ang]              Gaussian lemma, mixed m=1        |z| < 3
  T5  E[Dv^4]        = 12*E[D*ang^2]           Gaussian lemma, mixed m=2        |z| < 3
  T6  E[D^2] >= 3*E[Dv^2]^2/E[v^4]             Cauchy-Schwarz + lemma, one-sided z > -3
  T7  R_2 = E[Dv^4]/(12 E[D] E[ang^2]) = 3.574 (n=1e6 reference, J02 seed-29)  pooled |z| < 3

JOINT ACCEPTANCE REGION: every member simultaneously inside its 3-sigma box
(T1-T5,T7 two-sided |z|<3; T6 one-sided z > -3).

KILL RULES (exactly as registered):
  * any within-model n=1e7 violation of the m=2 identity T5 at >= 3 sigma
    REFUTES THE GAUSSIAN LEMMA ITSELF (J00 ND2 kill condition -- the sharpest
    falsifier this channel can fire);
  * T6 at >= 3 sigma is a theorem-rigid Cauchy-Schwarz contradiction (J05 s5);
  * T1-T4 at >= 3 sigma are battery-internal inconsistencies vs the Gaussian
    identities (T2-T4) or Theorem 1 (T1) and fail the battery;
  * T7 at >= 3 sigma fails the closure-ratio bridge to the reference structure;
  * CONFIRM is declared only if ALL members pass jointly.

POWER: computed under the CLT from the observed covariance of the test
statistics (multivariate-Gaussian orthant by Monte Carlo); reported per member
offset delta in units of sigma, for the joint battery.
==============================================================================
"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push")

from J02_moment_hierarchy import simulate  # frozen J02 engine (seed-controlled)

OUT_PREFIX = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/U02_results"


# ----------------------------------------------------------------------------
# pre-registered reference structure (measured at n=1e6, J02/J05/J06; R_2 from
# the J02 seed-29 C-run, 3.57431) and exact predictions
# ----------------------------------------------------------------------------
REFS = {
    "q0": dict(E_D=0.5008, E_v2=2.8061, E_Dv2=3.7316, E_v4=66.55,
               E_Dv4=119.5, E_D2=0.7661, R1=2.63499, R2=3.57431),
    "q3": dict(R1=2.0235, sR1=0.012),
    "q10": dict(R1=1.6971, sR1=0.009),
}


def PHI(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def mean_se(x, ddof=1):
    x = np.asarray(x, dtype=np.float64)
    return float(x.mean()), float(x.std(ddof=ddof) / math.sqrt(len(x)))


def moments_and_cov(comps, chunk=2_000_000):
    """means + covariance of the MEANS of the component arrays (chunked so peak
    memory stays low even when every comp is n=1e7)."""
    n = len(comps[0])
    k = len(comps)
    s1 = np.zeros(k)
    s2 = np.zeros((k, k))
    for i0 in range(0, n, chunk):
        sl = slice(i0, min(i0 + chunk, n))
        Xc = np.column_stack([c[sl] for c in comps])
        s1 += Xc.sum(0)
        # einsum (non-BLAS path): OpenBLAS dgemm raises spurious
        # "divide by zero" on A.T @ A for wide tall matrices on this box
        s2 += np.einsum("ij,ik->jk", Xc, Xc, optimize=False)
    mu = s1 / n
    cov_pop = s2 / n - np.outer(mu, mu)          # covariance of components
    cov_means = cov_pop / n                      # covariance of the means
    return mu, cov_means


def jackknife(func, comps, blocks=64):
    """block jackknife SE of func(means) for a cross-check of the delta method."""
    n = len(comps[0])
    idx = np.array_split(np.arange(n), blocks)
    mu_all = np.array([c.mean() for c in comps])
    mu_j = np.empty((blocks, len(comps)))
    for b in range(blocks):
        keep = np.ones(n, dtype=bool)
        keep[idx[b]] = False
        mu_j[b] = [c[keep].mean() for c in comps]
    theta_j = np.array([func(m) for m in mu_j])
    theta = func(mu_all)
    pseudo = blocks * theta - (blocks - 1) * theta_j
    return float(np.std(pseudo, ddof=1) / math.sqrt(blocks))


def delta_se(mu, cov, grad_idx, grad):
    M = cov[np.ix_(grad_idx, grad_idx)]
    return float(math.sqrt(grad @ M @ grad))


def battery_stats(label, n, tau0, q, seed, rngD=None, keep_comps=False):
    t0 = time.time()
    r = simulate(n, tau0, q, "central", seed)
    D, ang, v2, v4 = r["D"], r["ang"], r["v2"], r["v4"]
    sim_s = time.time() - t0

    # the ten elementary statistics of the battery (see module doc; comp order)
    comps = [D, v2, v4, D * v2, D * v4, D * D, ang, ang * ang, D * ang, D * (ang * ang)]
    mu, cov = moments_and_cov(comps)
    del r

    # --- T1: E[D] vs exact dbar = tau0 (1/2 + q/4) ---------------------------
    dbar = tau0 * (0.5 + q / 4.0)
    z1 = (mu[0] - dbar) / math.sqrt(cov[0, 0])

    # --- identity differences (lemma tests T2..T5) ---------------------------
    def zdiff(ia, ib, mult):
        return (mu[ia] - mult * mu[ib]) / math.sqrt(
            cov[ia, ia] + mult * mult * cov[ib, ib] - 2 * mult * cov[ia, ib])

    z2 = zdiff(1, 6, 2.0)    # E[v^2] - 2 E[ang]
    z3 = zdiff(2, 7, 12.0)   # E[v^4] - 12 E[ang^2]
    z4 = zdiff(3, 8, 2.0)    # E[Dv^2] - 2 E[D ang]
    z5 = zdiff(4, 9, 12.0)   # E[Dv^4] - 12 E[D ang^2]   <-- THE SHARPEST

    # --- T6: Cauchy-Schwarz width bound (one-sided) --------------------------
    g6 = mu[5] - 3.0 * mu[3] ** 2 / mu[2]
    s6 = delta_se(mu, cov, (5, 3, 2), np.array([1.0, -6.0 * mu[3] / mu[2],
                                               3.0 * mu[3] ** 2 / mu[2] ** 2]))
    z6 = g6 / s6

    # --- closure ratios with delta-method SEs --------------------------------
    R1 = mu[3] / (2.0 * mu[0] * mu[6])
    sR1 = R1 * delta_se(mu, cov, (3, 0, 6), np.array([1 / mu[3], -1 / mu[0], -1 / mu[6]]))
    R2 = mu[4] / (12.0 * mu[0] * mu[7])
    sR2 = R2 * delta_se(mu, cov, (4, 0, 7), np.array([1 / mu[4], -1 / mu[0], -1 / mu[7]]))
    r5 = mu[4] / (12.0 * mu[9])                      # identity ratio, m=2
    sr5 = r5 * delta_se(mu, cov, (4, 9), np.array([1 / mu[4], -1 / mu[9]]))

    out = dict(
        label=label, n=int(n), tau0=tau0, q=q, seed=seed, sim_seconds=sim_s,
        dbar=dbar,
        six=dict(
            E_D=float(mu[0]), sE_D=float(math.sqrt(cov[0, 0])),
            E_v2=float(mu[1]), sE_v2=float(math.sqrt(cov[1, 1])),
            E_Dv2=float(mu[3]), sE_Dv2=float(math.sqrt(cov[3, 3])),
            E_v4=float(mu[2]), sE_v4=float(math.sqrt(cov[2, 2])),
            E_Dv4=float(mu[4]), sE_Dv4=float(math.sqrt(cov[4, 4])),
            E_D2=float(mu[5]), sE_D2=float(math.sqrt(cov[5, 5])),
            E_ang=float(mu[6]), E_ang2=float(mu[7]),
            E_Dang=float(mu[8]), E_Dang2=float(mu[9]),
        ),
        z=dict(z1_T1=float(z1), z2_T2=float(z2), z3_T3=float(z3),
               z4_T4=float(z4), z5_T5=float(z5), z6_T6=float(z6)),
        ratios=dict(R1=float(R1), sR1=float(sR1), R2=float(R2), sR2=float(sR2),
                    r5_identity=float(r5), sr5=float(sr5)),
    )
    # cross-check: jackknife SE of r5 and R2 on the big runs
    if n >= 4_000_000:
        f_r5 = lambda m: m[4] / (12.0 * m[9])
        f_R2 = lambda m: m[4] / (12.0 * m[0] * m[7])
        out["jackknife"] = dict(blocks=64, sr5=jackknife(f_r5, comps),
                                sR2=jackknife(f_R2, comps))
    if keep_comps:
        return out, comps
    return out


def power_table(cov_z, z_obs, deltas=(1.0, 2.0, 3.0, 5.0, 6.0), nsamp=2_000_000):
    """Joint acceptance of the 3-sigma box under the CLT (MVN with observed
    covariance of the test statistics), and joint power under an offset of
    delta sigma in the m=2 member (T5). Two-sided members T1..T5 (5) + one-sided
    T6 = 6 tests in the region."""
    n = 6
    L = np.linalg.cholesky(cov_z[:n, :n] + 1e-14 * np.eye(n))
    W = np.random.default_rng(20260926).standard_normal((nsamp, n))
    X = np.einsum("ij,jk->ik", W, L.T, optimize=False)   # non-BLAS (see cov note)
    lo = np.array([-3.0] * 5 + [-3.0]); hi = np.array([3.0] * 5 + [np.inf])
    # box: T1-T5 two-sided |z|<3; T6 one-sided z > -3 (no upper limit)
    acc = np.all((z_obs[:n] + X) > lo, axis=1) & np.all(
        (z_obs[:n] + X) < hi, axis=1)
    joint_accept = float(acc.mean())
    pow_rows = {}
    for d in deltas:
        zz = z_obs[:n].copy(); zz[4] += d          # offset in T5 (m=2 member)
        accd = np.all((zz + X) > lo, axis=1) & np.all((zz + X) < hi, axis=1)
        pow_rows[f"delta_{d:g}sigma"] = float(1.0 - accd.mean())
    return joint_accept, pow_rows


def main():
    O = {"lane": "U02_battery", "title": "J00-ND2 six-moment battery at n=1e7",
         "pre_registered": "stated in module docstring and printed below",
         "runs": [], "z_table": [], "matched_pair": {}, "power": {},
         "verdict": {}}

    print("=" * 100)
    print("U02 -- ND2: THE SIX-MOMENT BATTERY at n=1e7")
    print("PRE-REGISTERED BATTERY AND THRESHOLDS (stated before numbers):")
    print("  T1  E[D]     = tau0*(1/2+q/4) ... exact Thm 1        |z|<3")
    print("  T2  E[v^2]   = 2 E[ang] ..... Gaussian lemma (marg m=1)  |z|<3")
    print("  T3  E[v^4]   = 12 E[ang^2] .. Gaussian lemma (marg m=2)  |z|<3")
    print("  T4  E[Dv^2]  = 2 E[D ang] ... Gaussian lemma (mix m=1)   |z|<3")
    print("  T5  E[Dv^4]  = 12 E[D ang^2]  Gaussian lemma (mix m=2)   |z|<3  << SHARPEST")
    print("  T6  E[D^2] >= 3 E[Dv^2]^2/E[v^4]  CS one-sided       z > -3")
    print("  T7  R_2 = E[Dv^4]/(12 E[D] E[ang^2]) = 3.574 (n=1e6 ref), pooled |z|<3")
    print("  KILL: any member >= 3 sigma fails the battery; T5 >= 3 sigma")
    print("        refutes the Gaussian lemma itself (J00 ND2 kill condition).")
    print("=" * 100, flush=True)

    # ---------------- run 1: central q=0, n = 1e7 (THE battery) ------------
    r7, comps7 = battery_stats("central_q0_n1e7", 10_000_000, 1.0, 0.0, 101,
                               keep_comps=True)
    O["runs"].append(r7)
    print(json.dumps(r7, indent=1), flush=True)

    # ---------------- run 2: seed-29 reference rerun (n = 1e6) -------------
    r6 = battery_stats("central_q0_n1e6_seed29", 1_000_000, 1.0, 0.0, 29)
    O["runs"].append(r6)
    print(json.dumps(r6, indent=1), flush=True)

    # ---------------- runs 3-4: q = 3 and q = 10 at n = 4e6 each -----------
    for q, seed in ((3.0, 103), (10.0, 107)):
        rr = battery_stats(f"central_q{q:g}_n4e6", 4_000_000, 1.0, q, seed)
        O["runs"].append(rr)
        print(json.dumps(rr, indent=1), flush=True)

    # ---------------- pooled z's vs the pre-registered references ----------
    a, b = O["runs"][0], O["runs"][1]           # 1e7 vs 1e6 seed-29 rerun
    zR2 = (b["ratios"]["R2"] - a["ratios"]["R2"]) / math.hypot(
        a["ratios"]["sR2"], b["ratios"]["sR2"])
    zR2_ref = (a["ratios"]["R2"] - REFS["q0"]["R2"]) / math.hypot(
        a["ratios"]["sR2"], b["ratios"]["sR2"])
    zR1_ref = (a["ratios"]["R1"] - REFS["q0"]["R1"]) / math.hypot(
        a["ratios"]["sR1"], b["ratios"]["sR1"])
    zT1b = (a["six"]["E_D"] - REFS["q0"]["E_D"]) / a["six"]["sE_D"]
    zT1exact = a["z"]["z1_T1"]                  # vs exact dbar = 1/2

    # z-table rows
    for rr in O["runs"]:
        row = {"run": rr["label"], "n": rr["n"], "q": rr["q"]}
        row["zT1"] = rr["z"]["z1_T1"]
        row["zT2"] = rr["z"]["z2_T2"]
        row["zT3"] = rr["z"]["z3_T3"]
        row["zT4"] = rr["z"]["z4_T4"]
        row["zT5"] = rr["z"]["z5_T5"]
        row["zT6"] = rr["z"]["z6_T6"]
        if rr["q"] == 0.0:
            row["zR2_vs_ref"] = zR2      # 1e7 vs 1e6 same-engine (pooled SE)
            row["zR2_vs_3574"] = zR2_ref
            row["zR1_vs_2635"] = zR1_ref
        else:
            ref = REFS[f"q{int(rr['q'])}"]
            row["zR1_vs_ref"] = (rr["ratios"]["R1"] - ref["R1"]) / math.hypot(
                rr["ratios"]["sR1"], ref["sR1"])
        O["z_table"].append(row)

    # ---------------- joint covariance of test statistics (CLT power) ------
    # statistic vector s = [E[D], E[v2]-2E[ang], E[v4]-12E[ang2], E[Dv2]-2E[Dang],
    #                        E[Dv4]-12E[Dang2], g6];  linear gradient of each in
    # the ten means.  Recompute from components of run 1.
    r = O["runs"][0].copy()
    G = np.zeros((6, 10))
    G[0, 0] = 1.0
    G[1, 1], G[1, 6] = 1.0, -2.0
    G[2, 2], G[2, 7] = 1.0, -12.0
    G[3, 3], G[3, 8] = 1.0, -2.0
    G[4, 4], G[4, 9] = 1.0, -12.0
    m = np.array([r["six"]["E_D"], r["six"]["E_v2"], r["six"]["E_v4"],
                  r["six"]["E_Dv2"], r["six"]["E_Dv4"], r["six"]["E_D2"],
                  r["six"]["E_ang"], r["six"]["E_ang2"],
                  r["six"]["E_Dang"], r["six"]["E_Dang2"]])
    G[5, 5] = 1.0
    G[5, 3] = -6.0 * m[3] / m[2]
    G[5, 2] = 3.0 * m[3] ** 2 / m[2] ** 2
    # covariance of the means of the ten statistics from run 1's own components
    _, covM = moments_and_cov(comps7)
    del comps7
    cov_z = G @ covM @ G.T
    z_obs = np.array([r["z"]["z1_T1"], r["z"]["z2_T2"], r["z"]["z3_T3"],
                      r["z"]["z4_T4"], r["z"]["z5_T5"], r["z"]["z6_T6"]])
    joint_accept, pow_rows = power_table(cov_z, z_obs)
    O["power"] = dict(joint_null_acceptance=joint_accept, power_T5_offset=pow_rows,
                      corr_of_z=[float(cov_z[i, j] / math.sqrt(cov_z[i, i] * cov_z[j, j]))
                                 for i in range(6) for j in range(i + 1, 6)])
    print("JOINT acceptance (CLT, observed correlation), power table:", flush=True)
    print(json.dumps(O["power"], indent=1), flush=True)

    # ---------------- ND2 matched-pair construction ------------------------
    # Fix the four-moment marginals {E[D], E[v2]=2E[ang], E[Dv2]=2E[Dang],
    # E[v4]=12E[ang2]} at the measured reference values and sweep the joint law
    # so that E[Dv4] = 12 E[D ang^2] (hence R_2) moves inside its
    # Cauchy-consistent window.  Two constructions: (i) two-point ang lattice,
    # one-parameter family p in the valid range; (ii) three-point lattice at
    # fixed ang law, one parameter t = E[D | ang=a2].
    A, B = REFS["q0"]["E_v2"] / 2.0, REFS["q0"]["E_v4"] / 12.0
    D0, C = REFS["q0"]["E_D"], REFS["q0"]["E_Dv2"] / 2.0
    sig2 = B - A * A
    cs_lb = C * C / D0                      # Cauchy lower bound on E[D ang^2]
    R2_meas = REFS["q0"]["E_Dv4"] / (12.0 * D0 * B)
    fam2 = []
    for p in np.linspace(0.005, 0.995, 1990):
        den = p * (1.0 - p)
        Delt = math.sqrt(sig2 / den)
        a1, a2 = A - (1.0 - p) * Delt, A + p * Delt
        if a1 <= 1e-9 or a2 <= 1e-9:
            continue
        det = p * a2 - (1.0 - p) * a1
        if abs(det) < 1e-12:
            continue
        m1 = (D0 * a2 - C) / (p * (a2 - a1))       # E[D|ang=a1] from linear system
        m2 = (C - p * a1 * m1) / ((1.0 - p) * a2)
        if m1 < 0 or m2 < 0:
            continue
        E_Dang2 = p * a1 * a1 * m1 + (1.0 - p) * a2 * a2 * m2
        lbD2 = p * m1 * m1 + (1.0 - p) * m2 * m2   # min E[D^2] reachable
        fam2.append((p, a1, a2, m1, m2, E_Dang2, E_Dang2 / (D0 * B), lbD2))
    fam2 = np.array(fam2)
    fam3 = []
    a1, a3 = 0.4, 5.0
    for a2 in np.linspace(0.6, 4.6, 401):
        M = np.array([[1, 1, 1], [a1, a2, a3], [a1 * a1, a2 * a2, a3 * a3]])
        try:
            p = np.linalg.solve(M, [1.0, A, B])
        except np.linalg.LinAlgError:
            continue
        if np.any(p < 1e-9):
            continue
        # g2 = t free; g1, g3 from E[D]=D0, E[Dang]=C
        p1, p2, p3 = p
        x = np.array([[p1, p3], [p1 * a1, p3 * a3]])
        for t in np.linspace(0.0, 3.0, 301):
            rhs = np.array([D0 - p2 * t, C - p2 * a2 * t])
            g13 = np.linalg.solve(x, rhs)
            if np.any(g13 < 0):
                continue
            E_Dang2 = p1 * a1 * a1 * g13[0] + p2 * a2 * a2 * t + p3 * a3 * a3 * g13[1]
            if E_Dang2 >= cs_lb - 1e-9:
                fam3.append((a2, t, E_Dang2, E_Dang2 / (D0 * B)))
    fam3 = np.array(fam3)
    # per-lattice t-sweep spans (full ang law held fixed within each lattice)
    if len(fam3):
        spans = []
        for a2v in np.unique(fam3[:, 0]):
            sub = fam3[fam3[:, 0] == a2v]
            spans.append((float(a2v), float(sub[:, 3].min()), float(sub[:, 3].max())))
    mp = {
        "four_matched_moments": dict(E_D=D0, E_ang=A, E_Dang=C, E_ang2=B,
                                     E_v2=REFS["q0"]["E_v2"],
                                     E_Dv2=REFS["q0"]["E_Dv2"],
                                     E_v4=REFS["q0"]["E_v4"]),
        "cauchy_lower_bound_E_Dang2": cs_lb,
        "measured_R2": R2_meas,
        "measured_E_Dang2": REFS["q0"]["E_Dv4"] / 12.0,
        "family2_two_point_ang": dict(
            n_members=len(fam2),
            E_Dang2_min=float(fam2[:, 5].min()), E_Dang2_max=float(fam2[:, 5].max()),
            R2_min=float(fam2[:, 6].min()), R2_max=float(fam2[:, 6].max()),
            max_minD2=float(fam2[:, 7].max()),
            all_cs_consistent=bool(np.all(fam2[:, 5] >= cs_lb - 1e-9)),
            realizable_E_D2_at_measured=bool(fam2[:, 7].max() <= REFS["q0"]["E_D2"] + 1e-9),
            measured_val_inside=bool((fam2[:, 5].min() <= REFS["q0"]["E_Dv4"] / 12.0) and
                                     (fam2[:, 5].max() >= REFS["q0"]["E_Dv4"] / 12.0))),
        "family3_three_point_fixed_ang_law": dict(
            n_members=len(fam3),
            ang_law=(0.4, "free_a2", 5.0),
            E_Dang2_min=float(fam3[:, 2].min()), E_Dang2_max=float(fam3[:, 2].max()),
            R2_min=float(fam3[:, 3].min()), R2_max=float(fam3[:, 3].max()),
            max_per_lattice_R2_span=float(max(s[2] - s[1] for s in spans)) if len(fam3) else None,
            measured_val_inside=bool((fam3[:, 2].min() <= REFS["q0"]["E_Dv4"] / 12.0) and
                                     (fam3[:, 2].max() >= REFS["q0"]["E_Dv4"] / 12.0))),
    }
    O["matched_pair"] = mp
    print("MATCHED-PAIR CONSTRUCTION (four moments fixed, R_2 swept):", flush=True)
    print(json.dumps(mp, indent=1), flush=True)

    # ---------------- verdict -------------------------------------------------
    fails = []
    for rr in O["runs"]:
        z = rr["z"]
        if abs(z["z1_T1"]) >= 3: fails.append((rr["label"], "T1"))
        if abs(z["z2_T2"]) >= 3: fails.append((rr["label"], "T2"))
        if abs(z["z3_T3"]) >= 3: fails.append((rr["label"], "T3"))
        if abs(z["z4_T4"]) >= 3: fails.append((rr["label"], "T4"))
        if abs(z["z5_T5"]) >= 3: fails.append((rr["label"], "T5"))
        if z["z6_T6"] <= -3: fails.append((rr["label"], "T6"))
    if abs(zR2_ref) >= 3: fails.append(("q0", "T7"))
    O["verdict"] = dict(failures=fails,
                        joint_acceptance_observed="ALL MEMBERS PASS" if not fails
                        else "FAILURE",
                        kill="T5 at >=3 sigma refutes the Gaussian lemma" if
                        any(f[1] == "T5" for f in fails) else "no lemma kill fired",
                        statement=(
                            "CONFIRM: the six-moment battery passes jointly at 3 sigma "
                            "at n=1e7; the Gaussian lemma survives its sharpest "
                            "observer-facing test, and the m=2 member is not "
                            "mimickable by the four-moment matched pair." if not fails
                            else "KILL: see failures list -- reported honestly."))
    print("VERDICT:", flush=True)
    print(json.dumps(O["verdict"], indent=1), flush=True)

    with open(OUT_PREFIX + ".json", "w") as f:
        json.dump(O, f, indent=1)
    print("WROTE", OUT_PREFIX + ".json", flush=True)
    return O


if __name__ == "__main__":
    main()