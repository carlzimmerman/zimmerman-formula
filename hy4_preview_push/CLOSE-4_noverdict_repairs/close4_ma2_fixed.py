#!/usr/bin/env python3
"""CLOSE-4 R1 (FROZEN_CRITERIA.md, committed alone before this file ran): the DES Y3 covariance guard.

KL1's MUTATE MA2 halves every effective density n_i and must FAIL KA2's test (ii). It cannot bite on DES Y3 because
KA2's (ii) point set is DEFINED by nfrac = diag(N)/diag(G), which the mutation itself inflates: halving n_i moves
points out of the (ii) set, DES is left with 3 (< 5), the criteria's own escape clause sets ii_pass = None, and
kl1.py scores "None is False" as "does not bite".

R1: the mutation may change the covariance; it may not change the points on which the tests are evaluated.
The (i) and (ii) index sets are computed ONCE at KA2's own configuration (ng_scale = 1.0) and then held fixed.

  OMP_NUM_THREADS=1 nice -n 10 python3 close4_ma2_fixed.py    -> parts/ma2_fixed.json, parts/ma2_fixed.out

Runs KL1's machinery from KL1's own folder (read-only import, bytecode writing off). Nothing in KL1 is edited.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Cold dark energy is a gravitating
field component, never a particle."""
import os, sys, json, math, warnings
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
KL1 = os.path.join(ROOT, "closure_2026_11_10", "KL1_lensing_amplitude_survey_assumptions")
sys.path.insert(0, KL1)
import numpy as np
import kl1_lib as K1

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

def sets_and_stats(S, pub, Pm, ng, fixed_i=None, fixed_ii=None):
    """One KA2 evaluation. If fixed_i / fixed_ii are given, the point sets are NOT re-derived."""
    G1, N1 = K1.gauss_cov(S, pub, K1.cell_full(S, Pm), ng_scale=ng)
    dg = np.diag(G1); nf = np.diag(N1) / dg
    dp = np.diag(S["cov"][np.ix_(pub, pub)])
    nd = (nf >= 0.8) if fixed_i is None else fixed_i
    sd = (nf < 0.5) if fixed_ii is None else fixed_ii
    area = float(1.0 / np.median(dp[nd] / dg[nd]))
    r = dp / (dg / area)
    o = dict(n_noise=int(nd.sum()), n_signal=int(sd.sum()), area_deg2=area * (180 / math.pi) ** 2)
    if nd.sum() >= 5:
        q16, q84 = np.percentile(r[nd], [16, 84]); o.update(i_q16=float(q16), i_q84=float(q84),
                                                            i_pass=bool(q16 >= 0.85 and q84 <= 1.15))
    else: o["i_pass"] = None
    if sd.sum() >= 5:
        o.update(ii_median=float(np.median(r[sd])), ii_min=float(np.min(r[sd])),
                 ii_pass=bool(0.95 <= np.median(r[sd]) <= 1.6 and np.min(r[sd]) >= 0.80))
    else: o["ii_pass"] = None
    return o, nd, sd

RES = dict(lane="CLOSE-4 R1", target="KL1 / KL1R MUTATE MA2 on DES Y3 (inherited by BX1 through KL1's A2 covariance)",
           rule="the (i) and (ii) index sets are frozen at KA2's own configuration and held fixed under the mutation",
           note="post hoc amendment to KL1 and KL1R; kappa = 1/2 FITTED; not theory closed; adopts nothing", rows={})
K1.setP(K1.PZ0)
for ft in K1.FOOTS:
    rows = json.load(open(os.path.join(KL1, "parts", f"rows_{ft}.json")))["rows"]
    Rk = np.array(K1.HM["primary"][ft]["R_tot"])
    for sn, S in K1.SURV.items():
        fid = rows["A0"][sn]["best_sigma8"]
        Pm = K1.Pmat(K1.run_of(Rk, (fid / K1.S8E) ** 2, "resp"), "F")
        pub = np.where(S["pubkeep"])[0]
        # ---- the sets are defined ONCE here, at KA2's own configuration
        base, nd0, sd0 = sets_and_stats(S, pub, Pm, 1.0)
        ctrl, _, _ = sets_and_stats(S, pub, Pm, 1.0, fixed_i=nd0, fixed_ii=sd0)      # control: must reproduce KA2
        mut, _, _ = sets_and_stats(S, pub, Pm, 0.5, fixed_i=nd0, fixed_ii=sd0)       # graded: n_i halved, sets fixed
        # ---- the frozen (re-selecting) version, reported beside it, unchanged
        froz, _, _ = sets_and_stats(S, pub, Pm, 0.5)
        bites = bool(mut["ii_pass"] is False)
        ctrl_ok = bool(ctrl["i_pass"] is True and ctrl["ii_pass"] is True)
        RES["rows"].setdefault(ft, {})[sn] = dict(
            KA2_baseline=base, control_ng1_fixed_sets=ctrl, mutated_ng_half_fixed_sets=mut,
            frozen_reselecting_ng_half=froz, n_signal_fixed=int(sd0.sum()), n_noise_fixed=int(nd0.sum()),
            control_reproduces_KA2=ctrl_ok, bites=bites)
        P(f"[{ft}] {sn}: sets frozen at ng x 1 (|S_i| = {int(nd0.sum())}, |S_ii| = {int(sd0.sum())})")
        P(f"    control  ng x 1 : (i) {ctrl.get('i_q16', float('nan')):.3f}-{ctrl.get('i_q84', float('nan')):.3f} -> {ctrl['i_pass']}; "
          f"(ii) median {ctrl.get('ii_median', float('nan')):.3f}, min {ctrl.get('ii_min', float('nan')):.3f} -> {ctrl['ii_pass']}")
        P(f"    MUTATED  ng x .5: area {mut['area_deg2']:.0f} deg^2; (i) {mut.get('i_q16', float('nan')):.3f}-{mut.get('i_q84', float('nan')):.3f} -> {mut['i_pass']}; "
          f"(ii) median {mut.get('ii_median', float('nan')):.3f}, min {mut.get('ii_min', float('nan')):.3f} -> {mut['ii_pass']} "
          f"=> {'BITES' if bites else 'DOES NOT BITE'}")
        P(f"    frozen re-selecting ng x .5 (reported): |S_ii| = {froz['n_signal']}, ii_pass = {froz['ii_pass']} "
          f"<-- the escape clause that blocked the arm")
os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
json.dump(RES, open(os.path.join(HERE, "parts", "ma2_fixed.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "parts", "ma2_fixed.out"), "w").write("\n".join(OUT) + "\n")
