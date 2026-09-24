#!/usr/bin/env python3
"""
L05 -- MULTI-OBJECT a0-RADIUS WINDOW TEST (synthetic, observer-facing)
2026-09-23.  Moment channel.  Follows J09 (central window [4/3,2], verified
27/27), J10 (J10-I core = -lnA * r_B/(c d_phys) = (r_B/R)*window), J11 and
K09 (volume window curve).  K07 did NOT land (no K07_results.json on disk;
the K07 .out shows an aborted run).  Per the J11 pre-registration 'K07 if
landed, else J11 values', the volume window curve used here = the J11 values
as re-measured and verified 19/19 in K09 (K09_results.json: C2 table at
tau0=1, the K07_volume_tau_surface 24-point table, thin anchor e0 = 0.3876,
thin window 1.882), transcribed below.

DESIGN (pre-registered)
  * Synthetic BLR sample: N_obj in {1,3,10,30}; log M_b/Msun ~ U[7.5, 9.5];
    rho_B (density-local) ~ log-U[1e-12, 1e-8] kg/m^3; framework radius
    r_B = sqrt(G M_b / a0) with a0(rho_B) = (c/2) sqrt(G rho_B).
  * (tau0, q) per object: CENTRAL-truth targets drawn continuously
    (tau0 ~ U[0.3, 3], q ~ U[0, 10]) subject to atom measurability
    (-ln A <= 5); VOLUME-truth targets are placed EXACTLY on the 18 verified
    J11/K09 cells (tau0 in {0.3, 0.5, 1, 1.5, 2, 3}, q in {0, 3, 10}) --
    the curve is tabular (K07 did not land), so generation and
    classification share the same table with no interpolation.  A_v and
    E[D]_v at each cell are re-measured here with the J02 engine (n = 600k)
    and checked against the published curve (z < 4); only cells with
    measureable atoms (-ln A_v <= 5) are included.
  * Measurables faked: A and d_phys with Gaussian log-noise at the given
    per-object S/N in {10, 30, 100} (relative error 1/SN on each);
    d_phys = E[D] * R / c with R the TRUE cloud radius.
  * Geometry truth: 'central' or 'volume'; radius truth f = R/r_B in
    {1.0, 1.5, 2.0}: f = 1 consistent, f = 1.5/2.0 = wrong radius injected
    (r_B perturbed by 1.5x/2x).
  * Statistic per object: J10-I = -ln A_meas * r_B / (c * d_meas)
    (true value = W_window / f).  Relative measurement error of J10-I:
    sigma_rel^2 = (1/SN)^2 + (1/(SN*|ln A|))^2.
  * Classification (3-sigma rule): measured J10-I does NOT intersect its
    window at 3 sigma.
      central: interval window [4/3, 2] (q- and tau0-free);
      volume:  point window W_v(tau0,q) on the J11/K09 curve, with
      sigma_tot^2 = (J10-I * sigma_rel)^2 + sW_pub^2 + sW_self^2
      (measurement + published curve SE + self-measurement SE -- all
      declared uncertainties paid).
  * Family-wise trial: >= 1 object violating => trial fired.
  * POWER: fraction of trials fired vs (N_obj, S/N, geometry truth):
      f = 1.0 -> false-kill rate (correct reading, all consistent);
      f = 1.5, 2.0 -> detection rate (wrong radius).
  * BUDGET: per-object S/N for a 10-object program to detect a 2x radius
    discrepancy at 3 sigma; required N_obj at fixed S/N = 30 (bars 0.5/0.8/
    0.95; 2000 trials/point).
  * KILL (asymptotic weakness): if at S/N = 100 and N = 30 the test cannot
    detect a 2x radius error at 3 sigma (rate < 0.8 in either geometry
    world), the a0-window test is too weak asymptotically and must be
    reported as such (honest).  Else PASS.

CONTENT / CHECKS
  C1  central window endpoints (analytic): 2.0 / 1.6 / 1.44444 in [4/3,2].
  C2  24-pt engine re-measurement vs published K09 curve, z < 4 (max).
  C3  engine W(tau0=1, q) vs J11 verdict values (1.8970/1.7104/1.3142),
      z < 4.
  C4  E[D]_v(1,0) vs J11-recorded 0.338 anchor.
  C5  A2744-QSO1 anchors: scale 40.9/45 -> central q0 1.818, volume q0
      1.719 (K09 C7: 1.8178 / 1.7281) -- CONSISTENT-OPEN reproduced.
  C6  volume cells: all 18 cells measureable (-ln A_v <= 5) -> included;
      the volume design table has 18/18 cells.
  C7  3-sigma floors: false-kill by noise alone must sit at the
      family-wise 3-sigma floor (central ~<= 1.3e-3/object at the edge;
      volume ~<= 4e-3/object point test), i.e. rate at N=1, S/N=100 < 0.02
      for central and < 0.01 for volume -- guards against a repeat of the
      interpolation-mismatch failure mode.
  KILL asymptotic check.

Files: L05_a0_program.py / .out / L05_results.json / L05_A0_PROGRAM.md.
No git commit (per lane rules).  Synthetic only -- no real data touched.
"""
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate

# ---------------------------------------------------------------- constants
G = 6.6743e-11            # m^3 kg^-1 s^-2
C = 2.99792458e8          # m s^-1
MSUN = 1.9884e30          # kg
LG_LD = 2.59020634112e13  # m per light-day
SN_SET = (10.0, 30.0, 100.0)
N_OBJ_SET = (1, 3, 10, 30)
F_SET = (1.0, 1.5, 2.0)
TAUS_GRID = np.array([0.15, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0])
QS_GRID = np.array([0.0, 3.0, 10.0])
CELL_TAUS = np.array([0.3, 0.5, 1.0, 1.5, 2.0, 3.0])   # volume design cells
CELL_QS = np.array([0.0, 3.0, 10.0])
N_MC = 600000
SEED_MC = 20260923
N_TRIALS = 4000
N_TRIALS_KILL = 5000
LN_A_MAX = 5.0                 # atom measurability: -ln A <= 5

# K09_results.json K07_volume_tau_surface (published J11 values surface,
# verified 19/19 in K09).  Keys: tau0 -> q -> (W, SE).
K09_SURFACE = {
    0.15: {0.0: (1.8825, 0.0223), 3.0: (1.8662, 0.0087), 10.0: (1.8210, 0.0055)},
    0.30: {0.0: (1.8952, 0.0136), 3.0: (1.8402, 0.0098), 10.0: (1.7588, 0.0074)},
    0.50: {0.0: (1.9144, 0.0053), 3.0: (1.8208, 0.0085), 10.0: (1.6371, 0.0076)},
    1.00: {0.0: (1.8814, 0.0100), 3.0: (1.7103, 0.0066), 10.0: (1.3288, 0.0055)},
    1.50: {0.0: (1.8557, 0.0090), 3.0: (1.5663, 0.0056), 10.0: (1.0782, 0.0041)},
    2.00: {0.0: (1.8033, 0.0072), 3.0: (1.4228, 0.0059), 10.0: (0.9184, 0.0029)},
    3.00: {0.0: (1.6981, 0.0050), 3.0: (1.2126, 0.0065), 10.0: (0.7149, 0.0041)},
    5.00: {0.0: (1.4712, 0.0044), 3.0: (0.9316, 0.0054), 10.0: (0.5003, 0.0025)},
}
J11_TAU1 = {0.0: 1.8970, 3.0: 1.7104, 10.0: 1.3142}   # J11 verdict, tau0 = 1
B_L, B_H = 4.0 / 3.0, 2.0                             # central window [4/3, 2]
SCALE_A2744 = 40.9 / 45.0                             # r_B/R = 0.908888...
A2744_CENTRAL = 1.8178          # K09 C7 reading, central q0 (rec. 1.818)
A2744_VOLUME = 1.7281           # K09 C7 reading, volume q0 (rec. 1.719)


def central_w(q):
    """Central window: -lnA/E[D] = (1+q/3)/(1/2+q/4), tau0-free."""
    return (1.0 + q / 3.0) / (0.5 + q / 4.0)


def mc_point(args):
    n, tau0, q, seed = args
    r = simulate(n, tau0, q, "volume", seed=seed)
    D = r["D"]
    atom = (r["N"] == 0).astype(float)
    A = float(np.mean(atom))
    sA = float(np.std(atom, ddof=1) / np.sqrt(n))
    ED = float(np.mean(D))
    sD = float(np.std(D, ddof=1) / np.sqrt(n))
    cov = float(np.cov(atom, D, ddof=1)[0, 1] / n)
    W = -np.log(A) / ED
    gA, gD = -1.0 / (A * ED), np.log(A) / (ED * ED)
    sW = float(np.sqrt(gA ** 2 * sA ** 2 + gD ** 2 * sD ** 2
                        + 2.0 * gA * gD * cov))
    return dict(tau0=tau0, q=q, A=A, sA=sA, ED=ED, sD=sD, W=W, sW=sW)


def se_ratio(trials, phat):
    return float(np.sqrt(phat * (1.0 - phat) / max(1, trials)))


def full_draw(rng, n, max_iter=80):
    """Continuous (tau0, q) draw for central truth with atom measurability
    (-ln A_c = tau0 (1+q/3) <= LN_A_MAX => A >= e^-5)."""
    t = np.zeros(n)
    q = np.zeros(n)
    acc = np.zeros(n, dtype=bool)
    it = 0
    while not acc.all() and it < max_iter:
        tt = rng.uniform(TAUS_GRID[1], 3.0, size=n)
        qq = rng.uniform(0.0, 10.0, size=n)
        keep = (~acc) & (tt * (1.0 + qq / 3.0) <= LN_A_MAX)
        t[keep], q[keep] = tt[keep], qq[keep]
        acc |= keep
        it += 1
    if not acc.all():
        raise RuntimeError("central draw did not converge")
    return t, q


def cell_draw(rng, n, cells):
    """Uniform draw over the accepted volume design cells."""
    idx = rng.integers(0, len(cells), size=n)
    return cells[idx]["t"].copy(), cells[idx]["q"].copy()


def build_cells(grid, Wpub_fn, Spub_fn):
    """Volume design cells = 18 (tau0,q) on the verified grid with
    measureable atoms.  Returns structured array t, q, A_v, ED_v, sW_self,
    sW_pub, W_pub, lnA_minus."""
    rows = []
    for t in CELL_TAUS:
        for q in CELL_QS:
            m = next(g for g in grid if g["tau0"] == t and g["q"] == q)
            Wpub, Spub = Wpub_fn(t, q)
            if -np.log(m["A"]) <= LN_A_MAX and m["A"] > 1e-5:
                rows.append(dict(t=t, q=q, A=m["A"], ED=m["ED"],
                                 sW_self=m["sW"], sW_pub=Spub,
                                 W_pub=Wpub, lnA=-np.log(m["A"])))
    d = {k: np.array([r[k] for r in rows], dtype=float) for k in
         ("t", "q", "A", "ED", "sW_self", "sW_pub", "W_pub")}
    d["lnA"] = np.array([r["lnA"] for r in rows])
    return d


def sigma_rel_of(SN, lnA_m):
    """Relative error of J10-I from per-observable S/N at (A, d_phys)."""
    sa = 1.0 / (SN * np.abs(lnA_m))
    return np.sqrt(sa ** 2 + (1.0 / SN) ** 2)


def classify_central(J10I, sig_rel):
    """3-sigma rule vs the central interval window [4/3, 2]."""
    lo = J10I * (1.0 - 3.0 * sig_rel)
    hi = J10I * (1.0 + 3.0 * sig_rel)
    return (hi < B_L) | (lo > B_H)


def gen_batch_central(rng, n, SN, f):
    """Vectorized central-truth object batch."""
    logM = rng.uniform(7.5, 9.5, size=n)
    rho = 10.0 ** rng.uniform(-12.0, -8.0, size=n)
    a0 = 0.5 * C * np.sqrt(G * rho)
    rB = np.sqrt(G * 10.0 ** logM * MSUN / a0)
    tau0, q = full_draw(rng, n)
    A_t = np.exp(-tau0 * (1.0 + q / 3.0))
    ED_t = tau0 * (0.5 + q / 4.0)
    d_phys = ED_t * f * rB / C                       # s (true cloud R = f r_B)
    sn = np.full(n, SN) if np.ndim(SN) == 0 else np.asarray(SN, dtype=float)
    lnA_m = np.log(A_t) + rng.normal(0.0, 1.0 / sn, size=n)
    lnd_m = np.log(d_phys) + rng.normal(0.0, 1.0 / sn, size=n)
    J10I = rB * (-lnA_m) / (C * np.exp(lnd_m))
    sig = sigma_rel_of(sn, lnA_m)
    return dict(J10I=J10I, sig=sig, viol=classify_central(J10I, sig),
                lag_d=d_phys / 86400.0, rb_ld=rB / LG_LD, t=tau0, q=q)


def gen_batch_volume(rng, n, SN, f, cells):
    """Vectorized volume-truth batch: targets ON the verified cells only.
    True J10-I = -ln A_v / (ED_v * f) = W_pub / f (up to self-measurement
    noise, paid in sW_self)."""
    logM = rng.uniform(7.5, 9.5, size=n)
    rho = 10.0 ** rng.uniform(-12.0, -8.0, size=n)
    a0 = 0.5 * C * np.sqrt(G * rho)
    rB = np.sqrt(G * 10.0 ** logM * MSUN / a0)
    idx = rng.integers(0, len(cells["t"]), size=n)
    A_t = cells["A"][idx]
    ED_t = cells["ED"][idx]
    W_pub = cells["W_pub"][idx]
    sW_tot = np.hypot(cells["sW_self"][idx], cells["sW_pub"][idx])
    d_phys = ED_t * f * rB / C
    sn = np.full(n, SN) if np.ndim(SN) == 0 else np.asarray(SN, dtype=float)
    lnA_m = np.log(A_t) + rng.normal(0.0, 1.0 / sn, size=n)
    lnd_m = np.log(d_phys) + rng.normal(0.0, 1.0 / sn, size=n)
    J10I = rB * (-lnA_m) / (C * np.exp(lnd_m))
    sig = sigma_rel_of(sn, lnA_m)
    sig_total = np.hypot(J10I * sig, sW_tot)
    viol = np.abs(J10I - W_pub) > 3.0 * sig_total
    return dict(J10I=J10I, sig=sig, viol=viol, W_pub=W_pub,
                sW_tot=sW_tot, lag_d=d_phys / 86400.0, rb_ld=rB / LG_LD,
                t=cells["t"][idx], q=cells["q"][idx])


def power_cell(rng, truth, N, SN, f, cells, trials, mixed=False):
    fired = np.zeros(trials, dtype=bool)
    gen = gen_batch_central if truth == "central" else gen_batch_volume
    if mixed:
        sn_all = np.array([SN_SET[i % 3] for i in range(N)])
        for it in range(trials):
            o = gen(rng, N, sn_all, f, cells) if truth == "volume" \
                else gen(rng, N, sn_all, f)
            fired[it] = o["viol"].any()
    else:
        for it in range(trials):
            o = gen(rng, N, SN, f, cells) if truth == "volume" \
                else gen(rng, N, SN, f)
            fired[it] = o["viol"].any()
    return fired


def main():
    t_start = time.time()
    print("=" * 78)
    print("L05 -- MULTI-OBJECT a0-RADIUS WINDOW TEST (synthetic, "
          "observer-facing)")
    print("=" * 78)

    res = {"meta": {"engine": "deepseek_push/J02_moment_hierarchy.py::simulate",
                    "n_mc_per_point": N_MC, "n_trials": N_TRIALS,
                    "date": "2026-09-23",
                    "curve_note": "K07 did not land; volume curve = J11 "
                                  "values re-measured and verified 19/19 in "
                                  "K09 (K07_volume_tau_surface) + thin "
                                  "anchor e0 = 0.3876, thin window 1.882",
                    "design_note": "volume-truth targets placed exactly on "
                                   "the 18 verified J11/K09 cells; central-"
                                   "truth targets drawn continuously within "
                                   "atom measurability"},
           "checks": {}, "power": {}, "budget": {}, "sample": {},
           "verdict": {}}
    ok = True

    # ---------------- C1: central window endpoints (analytic) ---------------
    print("-" * 78)
    print("C1  central window endpoints (1+q/3)/(1/2+q/4) at q = 0/3/10")
    for qq in (0.0, 3.0, 10.0):
        w = central_w(qq)
        inw = bool(B_L <= w <= B_H)
        res["checks"][f"C1_central_q{int(qq)}"] = inw
        ok &= inw
        print(f"    q={qq:5.1f}: W_c = {w:.6f}   in [4/3, 2] = {inw}")

    # ---------------- MC grid: A_v, E[D]_v on the K09 surface --------------
    print("-" * 78)
    print(f"C2  engine re-measurement on the 24-pt K09 grid (n={N_MC}/pt)")
    tasks = [(N_MC, t, q, SEED_MC + int(t * 10) * 10 + int(q))
             for t in TAUS_GRID for q in QS_GRID]
    with Pool(min(16, os.cpu_count() or 1)) as pool:
        grid = pool.map(mc_point, tasks)
    max_z, max_z_at = 0.0, ""
    for m in grid:
        Wpub, Spub = K09_SURFACE[m["tau0"]][m["q"]]
        z = abs(m["W"] - Wpub) / np.sqrt(m["sW"] ** 2 + Spub ** 2)
        res["checks"][f"C2_t{str(m['tau0'])}_q{int(m['q'])}"] = bool(z < 4.0)
        ok &= z < 4.0
        if z > max_z:
            max_z, max_z_at = z, f"t{m['tau0']}_q{int(m['q'])}"
        print(f"    tau0={m['tau0']:5.2f} q={m['q']:5.1f}: "
              f"A={m['A']:.4f} E[D]={m['ED']:.4f} W={m['W']:.4f} "
              f"(pub {Wpub:.4f}) z={z:5.2f}")
    res["checks"]["C2_max_z"] = bool(max_z < 4.0)
    ok &= max_z < 4.0
    print(f"    max z = {max_z:.2f} at {max_z_at} -- engine = published curve")

    # ---------------- C3: tau0 = 1 row vs J11 verdict -----------------------
    print("-" * 78)
    print("C3  engine W(tau0=1, q) vs J11 verdict values (1.8970/1.7104/"
          "1.3142)")
    for jj, qq in enumerate(QS_GRID):
        m = next(g for g in grid if g["tau0"] == 1.0 and g["q"] == qq)
        z = abs(m["W"] - J11_TAU1[qq]) / m["sW"]
        res["checks"][f"C3_q{int(qq)}"] = bool(z < 4.0)
        ok &= z < 4.0
        print(f"    q={qq:4.0f}: W = {m['W']:.4f} vs J11 {J11_TAU1[qq]:.4f}  "
              f"z = {z:.2f}")

    # ---------------- C4: E[D]_v(1,0) vs J11 0.338 anchor -------------------
    print("-" * 78)
    m10 = next(g for g in grid if g["tau0"] == 1.0 and g["q"] == 0.0)
    z4 = abs(m10["ED"] - 0.338) / m10["sD"]
    res["checks"]["C4_ED10"] = bool(z4 < 4.0)
    ok &= z4 < 4.0
    print(f"C4  E[D]_v(1,0) = {m10['ED']:.5f} vs J11 anchor 0.338  "
          f"z = {z4:.2f}")

    # ---------------- C5: A2744-QSO1 anchors --------------------------------
    print("-" * 78)
    cen = SCALE_A2744 * central_w(0.0)
    vol = SCALE_A2744 * m10["W"]
    res["checks"]["C5_anchor_central"] = bool(abs(cen - A2744_CENTRAL) < 0.02)
    res["checks"]["C5_anchor_volume"] = bool(abs(vol - A2744_VOLUME) < 0.04)
    ok &= (res["checks"]["C5_anchor_central"]
           and res["checks"]["C5_anchor_volume"])
    print(f"C5  A2744-QSO1 (r_B/R = {SCALE_A2744:.5f}): central q0 reading "
          f"{cen:.3f} (record 1.818)  volume q0 {vol:.3f} (record 1.719)")

    # ---------------- C6: volume design cells -------------------------------
    def Wpub_fn(t, q):
        return K09_SURFACE[t][q]
    cells = build_cells(grid, Wpub_fn, None)
    res["sample"]["n_cells"] = len(cells["t"])
    res["checks"]["C6_all_cells_measureable"] = bool(len(cells["t"]) == 18)
    ok &= len(cells["t"]) == 18
    print("-" * 78)
    print(f"C6  volume design cells: {len(cells['t'])}/18 cells with "
          "measureable atoms (-ln A <= 5)")
    for i in range(len(cells["t"])):
        print(f"    t={cells['t'][i]:4.2f} q={cells['q'][i]:4.0f}: "
              f"A={cells['A'][i]:.4f} -lnA={-np.log(cells['A'][i]):.3f} "
              f"E[D]={cells['ED'][i]:.4f} W_pub={cells['W_pub'][i]:.4f} "
              f"+- {cells['sW_pub'][i]:.4f}")

    # ---------------- sample table (N=10, f=1, mixed S/N) -------------------
    print("-" * 78)
    print("sample realization (N=10, f=1.0 consistent, mixed S/N design):")
    rng = np.random.default_rng(7)
    o_mix = []
    for i in range(10):
        truth_i = "central" if i < 5 else "volume"
        o = gen_batch_central(rng, 1, SN_SET[i % 3], 1.0) if truth_i == \
            "central" else gen_batch_volume(rng, 1, SN_SET[i % 3], 1.0, cells)
        o_mix.append(o)
        print(f"    obj {i+1:2d} truth={truth_i:7s} S/N={SN_SET[i % 3]:5.0f} "
              f"T={o['t'][0]:4.2f} Q={o['q'][0]:4.0f} "
              f"rB={o['rb_ld'][0]:6.1f} ld lag={o['lag_d'][0]:7.1f} d "
              f"J10I={o['J10I'][0]:.3f}")
    res["sample"]["table"] = [dict(
        obj=i + 1, truth=("central" if i < 5 else "volume"),
        sn=SN_SET[i % 3], t=round(float(o_mix[i]["t"][0]), 2),
        q=round(float(o_mix[i]["q"][0]), 1),
        rb_ld=round(float(o_mix[i]["rb_ld"][0]), 1),
        lag_d=round(float(o_mix[i]["lag_d"][0]), 1),
        J10I=round(float(o_mix[i]["J10I"][0]), 3)) for i in range(10)]

    # ---------------- POWER: homogeneous per-object S/N ---------------------
    print("-" * 78)
    print(f"POWER  homogeneous per-object S/N; family-wise P(>=1 violation "
          f"at 3 sigma); {N_TRIALS} trials/cell")
    for truth in ("central", "volume"):
        for N in N_OBJ_SET:
            for SN in SN_SET:
                for f in F_SET:
                    rng = np.random.default_rng(
                        int(1000 + 1000 * N + 100 * SN + 10 * f +
                            (0 if truth == "central" else 1)))
                    fired = power_cell(rng, truth, N, SN, f, cells, N_TRIALS)
                    p = float(fired.mean())
                    res["power"][f"{truth}_N{N}_SN{int(SN)}_f{int(f*10)}"] = \
                        dict(rate=round(p, 4),
                             se=round(se_ratio(N_TRIALS, p), 4))
                    kind = "FALSE-KILL" if f == 1.0 else "DETECTION"
                    print(f"    {truth:8s} N={N:2d} S/N={SN:4.0f} f={f:3.1f} "
                          f"{kind}: {p:.4f} +- {se_ratio(N_TRIALS, p):.4f}")

    # ---------------- POWER: mixed program design ---------------------------
    print("-" * 78)
    print(f"POWER  MIXED program design (S/N cycles 10/30/100); "
          f"{N_TRIALS} trials/cell")
    for truth in ("central", "volume"):
        for N in N_OBJ_SET:
            for f in F_SET:
                rng = np.random.default_rng(
                    5000 + 1000 * N + 100 * int(f * 10) +
                    (0 if truth == "central" else 1))
                fired = power_cell(rng, truth, N, None, f, cells, N_TRIALS,
                                   mixed=True)
                p = float(fired.mean())
                res["power"][f"mixed_{truth}_N{N}_f{int(f*10)}"] = \
                    dict(rate=round(p, 4),
                         se=round(se_ratio(N_TRIALS, p), 4))
                kind = "FALSE-KILL" if f == 1.0 else "DETECTION"
                print(f"    {truth:8s} N={N:2d} f={f:3.1f} {kind}: "
                      f"{p:.4f} +- {se_ratio(N_TRIALS, p):.4f}")

    # ---------------- C7: 3-sigma floor guards ------------------------------
    print("-" * 78)
    print("C7  3-sigma floor guards at N=1, S/N=100 (interpolation-mismatch "
          "regression guard)")
    for truth in ("central", "volume"):
        rng = np.random.default_rng(60000 +
                                    (0 if truth == "central" else 1))
        fired = power_cell(rng, truth, 1, 100.0, 1.0, cells, 8000)
        p = float(fired.mean())
        res["power"][f"floor_{truth}"] = dict(rate=round(p, 5),
                                              se=round(se_ratio(8000, p), 5))
        bound = 0.008 if truth == "volume" else 0.02
        res["checks"][f"C7_floor_{truth}"] = bool(p < bound)
        ok &= p < bound
        print(f"    {truth:8s} false-kill N=1 SN=100 = {p:.5f} "
              f"(bound < {bound})")

    # ---------------- BUDGET ------------------------------------------------
    print("-" * 78)
    print("BUDGET  (a) per-object S/N at N=10 for 2x (f=2.0) detection at 3"
          " sigma;  (b) required N at fixed S/N=30 (bars 0.5/0.8/0.95; "
          "2000 trials/point)")
    SN_SCAN = (5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 30.0, 40.0, 60.0, 80.0,
               100.0)
    N_SCAN = (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50)
    for bar in (0.5, 0.8, 0.95):
        for truth in ("central", "volume"):
            need_sn, need_n = None, None
            for sn in SN_SCAN:
                rng = np.random.default_rng(70000 + int(10 * sn) +
                                            (0 if truth == "central" else 1))
                fired = power_cell(rng, truth, 10, sn, 2.0, cells, 2000)
                if float(fired.mean()) >= bar:
                    need_sn = sn
                    break
            for n in N_SCAN:
                rng = np.random.default_rng(80000 + 100 * n +
                                            (0 if truth == "central" else 1))
                fired = power_cell(rng, truth, n, 30.0, 2.0, cells, 2000)
                if float(fired.mean()) >= bar:
                    need_n = n
                    break
            res["budget"][f"bar{bar}_{truth}"] = dict(
                sn_N10_2x=need_sn, n_SN30_2x=need_n)
            print(f"    bar={bar:.2f} {truth:8s}: S/N(2x|N=10) >= "
                  f"{need_sn if need_sn else '>100'};  N(2x|S/N=30) >= "
                  f"{need_n if need_n else '>50'}")

    # ---------------- KILL: asymptotic weakness check -----------------------
    print("-" * 78)
    print("KILL  asymptotic check: detection(2x | N=30, S/N=100) per truth")
    for truth in ("central", "volume"):
        rng = np.random.default_rng(90000 +
                                    (0 if truth == "central" else 1))
        fired = power_cell(rng, truth, 30, 100.0, 2.0, cells, N_TRIALS_KILL)
        p = float(fired.mean())
        res["verdict"][f"detect2x_{truth}"] = dict(
            rate=round(p, 4), se=round(se_ratio(N_TRIALS_KILL, p), 4),
            trials=N_TRIALS_KILL, bar=0.8)
        print(f"    {truth:8s}: detection(2x, N=30, S/N=100) = {p:.4f} +- "
              f"{se_ratio(N_TRIALS_KILL, p):.4f}")
    dC = res["verdict"]["detect2x_central"]["rate"]
    dV = res["verdict"]["detect2x_volume"]["rate"]
    too_weak = (dC < 0.8) or (dV < 0.8)
    if too_weak:
        res["verdict"]["verdict"] = (
            "TOO_WEAK -- the a0-window test cannot detect a 2x radius error "
            "at 3 sigma at S/N=100, N=30 in some geometry world; reported "
            "honestly as asymptotically too weak.")
    else:
        res["verdict"]["verdict"] = (
            f"PASS -- the a0-window test detects a 2x radius discrepancy at "
            f"3 sigma with P = {dC:.3f} (central truth) / {dV:.3f} (volume "
            f"truth) at N=30, S/N=100, far above the 0.8 bar: NOT "
            f"asymptotically too weak.  False-kill under the correct "
            f"consistent reading is the 3-sigma family floor"
            f" (central ~<=1.3e-3/obj edge effects; volume point test "
            f"~<=4e-3/obj incl. curve SEs), verified in C7.")
    res["checks"]["KILL_check"] = bool(not too_weak)
    ok &= not too_weak
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["elapsed_s"] = round(time.time() - t_start, 1)
    with open(os.path.join(HERE, "L05_results.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print(f"elapsed {res['elapsed_s']} s")
    print("ALL L05 CHECKS PASSED" if ok else "L05 CHECK FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)