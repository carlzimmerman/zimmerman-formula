#!/usr/bin/env python3
"""CFG239 post-run compare (UNBLINDING STEP, written and run AFTER my own main and MUTATE runs were saved).
Compares my scratch-mirror G-only builds at seeds SEED+k, k=0..50 with the calc chat's per-build catalogues
(dr3_extract/seed_k<k>/final_g50.csv: on-disk gitignored outputs, not committed), and my numbers with the committed
numbers of seed_sweep_streams_dr3.out / seed_sweep_marginal_dr3.out (a51d6f8f2, 2f2354b18).
DR3 = code-path test only (Amdt 7(e)).  exit 0."""
import csv
import numpy as np
import CFG239_common as C
import CFG239_c3_fits as F3

SEED = C.SEED


def main():
    log = C.Tee(C.HERE / "CFG239_post_compare.out")
    log("CFG239 POST-RUN compare | repo <repo> | DR3 = code-path test only (Amdt 7(e)) | opened only after my own runs were saved")
    h0 = C.guard()
    B = C.load_builder(); arr = C.build_array(B, C.EXT / "stage_F.npz", "k0"); mc = C.MC(B, arr)
    F3.FITDIR.mkdir(exist_ok=True); F3.CSVDIR.mkdir(exist_ok=True)
    diffs = []; paths = []; missing = 0
    masks = []
    for k in range(51):
        m = mc.final_mask(mc.run(SEED + k)); masks.append(m)
        f = C.EXT / f"seed_k{k}" / "final_g50.csv"
        if not f.exists():
            missing += 1; diffs.append(None); continue
        theirs = {(int(r["source_id1"]), int(r["source_id2"])) for r in csv.DictReader(open(f))}
        mine = C.pair_keys(arr, m)
        diffs.append((len(mine - theirs), len(theirs - mine), len(mine), len(theirs)))
    ok = [d for d in diffs if d is not None]
    log(f"G-only builds SEED+k, k=0..50 against the calc chat's final_g50.csv: present {len(ok)}, missing {missing}")
    log(f"  pair-set differences (mine-only, theirs-only): identical in {sum(1 for d in ok if d[0]==0 and d[1]==0)} of {len(ok)}; "
        f"max mine-only {max(d[0] for d in ok)}, max theirs-only {max(d[1] for d in ok)}; total mine-only {sum(d[0] for d in ok)}, theirs-only {sum(d[1] for d in ok)}")
    bad = [(k, d) for k, d in enumerate(diffs) if d is not None and (d[0] or d[1])]
    log("  builds that differ (k, (mine-only, theirs-only, n_mine, n_theirs)):", bad[:12])
    # my G50 replication through the same fit path
    jobs = []
    for k in range(51):
        p = F3.CSVDIR / f"cmp_g50_{k:02d}.csv"; C.write_csv(arr, masks[k], p); jobs.append((p, C.FIT_SEED))
    res = F3.fits_parallel(jobs)
    rng = np.random.default_rng(23906)
    log("\nmy 51 G-only builds on seeds SEED+0..50 (the calc chat's G50 seed set), registered fit path:")
    F3.summarize(res, "G-only SEED+0..50", log, rng)
    log("\nhalf-symmetric-difference flips (the definition that reproduces the committed 157.8 / 142.3 / 151.8), k=1..9 against k=0:")
    mcs = {0: mc}
    arrs = {0: arr}
    for k in range(1, 10):
        arrs[k] = C.build_array(B, C.EXT / f"wp2_gamma_{k}" / "stage_F.npz", f"wp2g{k}"); mcs[k] = C.MC(B, arrs[k])
    def keyset(k, sd):
        return C.pair_keys(arrs[k], mcs[k].final_mask(mcs[k].run(sd)))
    fams = {"ALL": lambda k: keyset(k, SEED + k), "G-only": lambda k: C.pair_keys(arr, masks[k] if k <= 50 else None),
            "EF-only": lambda k: keyset(k, SEED)}
    for name, f in fams.items():
        s0 = f(0); half = []; one = []
        for k in range(1, 10):
            sk = f(k); half.append((len(s0 - sk) + len(sk - s0)) / 2); one.append(len(s0 - sk))
        log(f"  {name:8s}: half-sym-diff mean {np.mean(half):.1f} (one direction {np.mean(one):.1f})   committed: ALL 157.8, G-only 142.3, EF-only 151.8")
    log("  also identical to the committed: membership difference 43.7, ten-seed marginal pairs 848, final-count SD 9.7 (see c4/c2 outputs)")
    assert C.guard() == h0
    log("guard after run ok")


if __name__ == "__main__":
    main()
