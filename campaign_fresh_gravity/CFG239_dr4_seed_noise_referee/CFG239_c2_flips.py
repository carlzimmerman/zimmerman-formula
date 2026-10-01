#!/usr/bin/env python3
"""CFG239 c2: claim (2) flip prediction sum p(1-p) (their M4), threshold distance, MU4, MU5.
DR3 = code-path test only (Amdt 7(e)).  main exit 0; MUTATE=4|5 exit 1 when the control bites."""
import os, sys, time
import numpy as np
import CFG239_common as C

MUT = int(os.environ.get("MUTATE", "0"))
SEED = C.SEED
EST = [SEED + 1000 + j for j in range(200)]
FRO = [SEED + k for k in range(10)]
VAL = [SEED + 5000 + j for j in range(10)]


def omat(B):
    """M[i,j] = number of pairs in build i but not in build j (one-way)."""
    B = B.astype(np.int32)
    return np.einsum('ip,jp->ij', B, 1 - B).astype(np.float64)   # exact integer counts


def null_stats(p, reps, rng, nb=10, chunk=200):
    """simulate nb independent builds from pass probabilities p; statistics: mean N(0->k) k=1..nb-1, mean over ordered pairs."""
    a, b = [], []
    for _ in range(reps // chunk):
        for _ in range(chunk):
            B = rng.random((nb, len(p))) < p
            M = omat(B)
            a.append(M[0, 1:].mean()); b.append((M.sum() / (nb * (nb - 1))))
    return np.array(a), np.array(b)


def main():
    log = C.Tee(C.HERE / ("CFG239_c2_flips%s.out" % (f"_MUTATE{MUT}" if MUT else "")))
    log("CFG239 c2 flips | repo <repo> | DR3 = code-path test only (Amdt 7(e)) | MUTATE =", MUT)
    C.WORK.mkdir(exist_ok=True)
    h0 = C.guard()
    B = C.load_builder()
    arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    n = len(arr["a"]); av = mc.av_ok; thr = mc.thr
    log(f"array U = {n}, U' (A_V ok) = {int(av.sum())}; seeds: frozen SEED+0..9, estimation SEED+1000..1199, validation SEED+5000..5009")
    rng = np.random.default_rng(23902)
    t0 = time.time()

    def sims(seeds, nt=212):
        return np.array([mc.run(s, n_trials=nt) for s in seeds])

    Sv = sims(VAL)
    Pv = (Sv <= thr) & av
    if MUT == 4:
        # control: same assertion "848-trial flips are ~0.5x of 212-trial flips" with 212 on both sides
        Sv2 = sims([s + 77 for s in VAL])
        ratio = omat((Sv2 <= thr) & av).sum() / omat(Pv).sum()
        log(f"MUTATE4: flips(212, other seeds)/flips(212) = {ratio:.3f}; assertion ratio in [0.40,0.65] ",
            "holds" if 0.40 <= ratio <= 0.65 else "FAILS")
        sys.exit(1 if not (0.40 <= ratio <= 0.65) else 0)
    Sf = sims(FRO); Pf = (Sf <= thr) & av
    Se = sims(EST); Pe = (Se <= thr) & av
    log(f"MC runs: {len(Sv)+len(Sf)+len(Se)} in {time.time()-t0:.0f} s")
    res = {}

    # --- estimators
    K = len(EST)
    p3 = Pe.mean(0)
    q3 = p3 * (1 - p3)
    E3 = q3.sum() * K / (K - 1)
    pf_ = Pf.mean(0); E1 = (pf_ * (1 - pf_)).sum(); E2 = E1 * 10 / 9
    # all-U variants (no A_V restriction)
    Pf_all = Sf <= thr; pfa = Pf_all.mean(0); E1_all = (pfa * (1 - pfa)).sum()
    Pe_all = Se <= thr; pea = Pe_all.mean(0); E3_all = (pea * (1 - pea)).sum() * K / (K - 1)
    log(f"\nEstimators of the expected one-way flips between two independent draws")
    log(f"  E1 (ten seeds SEED+0..9, p-hat steps of 0.1, A_V ok) = {E1:.1f}    [all U incl. A_V-failing: {E1_all:.1f}]")
    log(f"  E2 = E1 x 10/9 = {E2:.1f}")
    log(f"  E3 (K=200 disjoint seeds, x K/(K-1)) = {E3:.1f}    [all U: {E3_all:.1f}]")
    log(f"  number of pairs with 0 < p-hat < 1 (E3): {int(((p3>0)&(p3<1)).sum())};  ten-seed marginal pairs: {int(((pf_>0)&(pf_<1)).sum())}")
    res.update(E1=E1, E2=E2, E3=E3, E1_all=E1_all, E3_all=E3_all)

    # --- observed
    Mf = omat(Pf); obs_f = Mf[0, 1:]; obs_f_rev = Mf[1:, 0]
    Mv = omat(Pv)
    val_ordered = Mv[~np.eye(10, dtype=bool)]
    log("\nObserved one-way flips")
    log(f"  frozen seeds, reference k=0, k=1..9: {[int(x) for x in obs_f]}  mean {obs_f.mean():.1f} (reverse direction mean {obs_f_rev.mean():.1f}); final counts {[int(x) for x in Pf.sum(1)]}")
    log(f"  validation seeds: 90 ordered counts mean {val_ordered.mean():.1f} SD {val_ordered.std(ddof=1):.1f}; reference=val0 k=1..9 mean {Mv[0,1:].mean():.1f}; final counts {[int(x) for x in Pv.sum(1)]}")
    fin = Pf[0].sum()
    log(f"  as fraction of final pairs ({int(fin)}): frozen-set mean one-way {obs_f.mean()/fin*100:.2f}%  (symmetric difference ~ {2*obs_f.mean()/fin*100:.2f}%)")
    res.update(obs_frozen_mean=float(obs_f.mean()), obs_frozen=[int(x) for x in obs_f], obs_val_mean=float(val_ordered.mean()))

    # --- null
    a, b = null_stats(p3, 4000, rng)
    a_m = a.mean(); a_sd = a.std(ddof=1); b_m = b.mean(); b_sd = b.std(ddof=1)
    def pv(x, arr):
        lo = (arr <= x).mean(); hi = (arr >= x).mean(); return min(1, 2 * min(lo, hi))
    log(f"\nNull (Poisson-binomial from E3 p-hat; 4000 reps of 10 independent builds)")
    log(f"  mean over k=1..9 of N(0->k): null mean {a_m:.1f}, SD {a_sd:.1f};  observed frozen {obs_f.mean():.1f}: z={(obs_f.mean()-a_m)/a_sd:+.2f}, p={pv(obs_f.mean(), a):.3f}")
    log(f"  mean over all 90 ordered pairs: null mean {b_m:.1f}, SD {b_sd:.1f};  observed validation {val_ordered.mean():.1f}: z={(val_ordered.mean()-b_m)/b_sd:+.2f}, p={pv(val_ordered.mean(), b):.3f}")
    log(f"  the calc chat's numbers: 133.5 (their p-hat, ten seeds) vs 142.3 observed: difference 8.8 = {8.8/a_sd:.2f} null SD of the mean (frozen-structure statistic)")
    log(f"  what a 10/9 correction does: 133.5 x 10/9 = {133.5*10/9:.1f} vs 142.3: difference {133.5*10/9-142.3:+.1f} = {(133.5*10/9-142.3)/a_sd:+.2f} SD")
    res.update(null_mean=float(a_m), null_sd=float(a_sd), null_all_mean=float(b_m), null_all_sd=float(b_sd),
               z_frozen=float((obs_f.mean() - a_m) / a_sd), z_val=float((val_ordered.mean() - b_m) / b_sd))

    # --- pair-level calibration
    def calib(p):
        q = p * (1 - p)
        flips_in = np.zeros(n); # per pair count of ordered flips in validation
        for i in range(10):
            for j in range(10):
                if i != j:
                    flips_in += (Pv[i] & ~Pv[j])
        tot = flips_in.sum()
        mid = (p > 0.02) & (p < 0.98)
        frac_mid = flips_in[mid].sum() / tot
        hi = q > 0.1
        obs_hi = flips_in[hi].sum() / 90; pred_hi = q[hi].sum() * K / (K - 1)
        return frac_mid, obs_hi, pred_hi, flips_in
    frac_mid, obs_hi, pred_hi, flips_in = calib(p3)
    log("\nPair-level calibration (validation flips, 90 ordered counts)")
    log(f"  share of flips in pairs with p-hat in (0.02,0.98): {frac_mid*100:.1f}%   (line >= 95%)")
    log(f"  pairs with p-hat(1-p-hat)>0.1: observed flips/count {obs_hi:.1f} vs predicted {pred_hi:.1f} (ratio {obs_hi/pred_hi:.3f}; line within 15%)")
    cal_ok = frac_mid >= 0.95 and abs(obs_hi / pred_hi - 1) < 0.15
    res.update(frac_mid=float(frac_mid), calib_ratio=float(obs_hi / pred_hi))
    # MU5 shuffle
    perm = rng.permutation(n)
    fm5, oh5, ph5, _ = calib(p3[perm])
    cal5 = fm5 >= 0.95 and abs(oh5 / ph5 - 1) < 0.15
    log(f"  MU5 (p-hat shuffled across pairs): share in mid {fm5*100:.1f}%, ratio {oh5/ph5:.3f} -> calibration {'passes (control toothless)' if cal5 else 'FAILS (control bites)'}")
    res["MU5_bites"] = not cal5
    if MUT == 5:
        log("MUTATE5: control bites (exit 1)" if not cal5 else "MUTATE5: toothless (exit 0)")
        sys.exit(1 if not cal5 else 0)

    # --- threshold distance and scatter
    mean_s = Se.mean(0); lr = np.abs(np.log(mean_s / thr))
    sel_pairs = av & (p3 > 0) & (p3 < 1)
    rel = Se.std(0, ddof=1) / Se.mean(0)
    log("\nThreshold-distance analysis (r = 200-seed mean sigma_vt / threshold)")
    tot = flips_in.sum()
    log(f"  share of validation flips with |ln r| <= 0.25: {flips_in[lr<=0.25].sum()/tot*100:.1f}%   (line >= 90%);  <= 0.15: {flips_in[lr<=0.15].sum()/tot*100:.1f}%;  <= 0.10: {flips_in[lr<=0.10].sum()/tot*100:.1f}%")
    Uav = av
    c1 = Uav & (lr < 0.05); c2 = Uav & (lr > 0.30)
    r1 = flips_in[c1].sum() / max(1, c1.sum()); r2 = flips_in[c2].sum() / max(1, c2.sum())
    log(f"  flips per pair: |ln r|<0.05 ({int(c1.sum())} pairs) {r1:.3f}; |ln r|>0.30 ({int(c2.sum())} pairs) {r2:.4f}; ratio {r1/max(r2,1e-9):.0f}  (line >= 20)")
    log(f"  per-pair relative scatter of sigma_vt over 200 seeds: median {np.median(rel):.4f} (Gaussian 0.0487), p90 {np.quantile(rel,.9):.4f}; near-threshold pairs (|ln r|<0.1) median {np.median(rel[lr<0.1]):.4f}")
    thr_ok = flips_in[lr <= 0.25].sum() / tot >= 0.90 and r1 / max(r2, 1e-9) >= 20
    res.update(share025=float(flips_in[lr <= 0.25].sum() / tot), flip_rate_ratio=float(r1 / max(r2, 1e-9)),
               rel_median=float(np.median(rel)), rel_p90=float(np.quantile(rel, .9)), rel_near=float(np.median(rel[lr < 0.1])))

    # --- MU4: 848 trials
    Sv4 = sims(VAL, nt=848); Pv4 = (Sv4 <= thr) & av
    f212 = omat(Pv).sum() / 90; f848 = omat(Pv4).sum() / 90
    relchg = np.median(np.abs(Sv4[1] - Sv4[0]) / Sv4[0]); relchg0 = np.median(np.abs(Sv[1] - Sv[0]) / Sv[0])
    log(f"\nMU4 n_trials x4: mean one-way flips between independent draws {f212:.1f} (212) -> {f848:.1f} (848), ratio {f848/f212:.3f} (band [0.40,0.65]); median relative seed-to-seed change {relchg0:.4f} -> {relchg:.4f} (ratio {relchg/relchg0:.3f}, sqrt law 0.5)")
    mu4_ok = 0.40 <= f848 / f212 <= 0.65
    res.update(mu4_ratio=float(f848 / f212), mu4_rel_ratio=float(relchg / relchg0))

    # --- assertions vs frozen criteria
    a_ok = abs(obs_f.mean() - E3) <= 2 * a_sd and 0.90 <= obs_f.mean() / E3 <= 1.10
    a2 = abs(obs_f.mean() - 142.3) <= max(10, 2 * a_sd)
    log("\nASSERTIONS (frozen pass lines)")
    for k, v in {
        "(i) observed frozen-seed mean within 2 null SD of E3 and ratio in [0.90,1.10]": a_ok,
        "(ii) observed frozen-seed mean within max(10, 2 SD) of 142.3": a2,
        "(iii-a) pair-level calibration (95% in mid-p, hi-q within 15%)": cal_ok,
        "(iii-b) threshold-distance (90% within |ln r|<=0.25; ratio >= 20)": thr_ok,
        "MU4 n_trials x4 flips ratio in [0.40,0.65]": mu4_ok,
        "MU5 shuffled p-hat breaks calibration": not cal5,
        "E1 replicates 133.5 within +-3": abs(E1 - 133.5) <= 3,
        "E3 in [135,160]": 135 <= E3 <= 160,
    }.items():
        log(f"  [{'PASS' if v else 'FAIL'}] {k}"); res.setdefault("checks", {})[k] = bool(v)
    C.jdump(res, C.HERE / "CFG239_c2_flips.json")
    assert C.guard() == h0
    log("guard after run ok")
    sys.exit(0)


if __name__ == "__main__":
    main()
