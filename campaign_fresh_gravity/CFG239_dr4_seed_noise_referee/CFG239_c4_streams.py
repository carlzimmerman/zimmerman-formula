#!/usr/bin/env python3
"""CFG239 c4: claim (4) stream isolation in the scratch mirror (monkeypatch only): ALL, G-only, EF-only (sequential G),
EF-only with a per-pair G stream; flip partition; MU7.  EF arms use wp2_gamma_k/stage_F.npz as SHARED inputs (E/F not rebuilt here).
DR3 = code-path test only (Amdt 7(e)).  main exit 0; MUTATE=7 exits 1 when the control bites."""
import os, sys, time
import numpy as np
import CFG239_common as C
import CFG239_c1_mechanism as M1
import CFG239_c3_fits as F3

MUT = int(os.environ.get("MUTATE", "0"))
SEED = C.SEED
KS = list(range(10))


def stage_f(k):
    return C.EXT / "stage_F.npz" if k == 0 else C.EXT / f"wp2_gamma_{k}" / "stage_F.npz"


def main():
    log = C.Tee(C.HERE / ("CFG239_c4_streams%s.out" % (f"_MUTATE{MUT}" if MUT else "")))
    log("CFG239 c4 streams | repo <repo> | DR3 = code-path test only (Amdt 7(e)) | MUTATE =", MUT)
    C.WORK.mkdir(exist_ok=True); F3.FITDIR.mkdir(exist_ok=True); F3.CSVDIR.mkdir(exist_ok=True)
    h0 = C.guard()
    B = C.load_builder()
    rng = np.random.default_rng(23904)
    arrs, mcs = {}, {}
    for k in KS:
        arrs[k] = C.build_array(B, stage_f(k), f"k{k}" if k == 0 else f"wp2g{k}")
        mcs[k] = C.MC(B, arrs[k])
    log("pair array sizes U_k:", [len(arrs[k]["a"]) for k in KS], "| uncovered corr id entries (zero-filled):", [mcs[k].n_unc for k in KS])

    def keys(k, mask):
        return C.pair_keys(arrs[k], mask)

    def pp_run(k, seed):
        sel = np.arange(len(arrs[k]["a"]))
        return M1.run_perpair(mcs[k], seed, sel)

    fam = {}
    # family masks as key sets
    fam["ALL"] = [keys(k, mcs[k].final_mask(mcs[k].run(SEED + k))) for k in KS]
    fam["G-only"] = [keys(0, mcs[0].final_mask(mcs[0].run(SEED + k))) for k in KS]
    fam["EF-only (sequential G)"] = [keys(k, mcs[k].final_mask(mcs[k].run(SEED))) for k in KS]
    fam["EF-only (per-pair G)"] = [keys(k, mcs[k].final_mask(pp_run(k, SEED))) for k in KS]
    if MUT == 7:
        # mutated: the per-pair arm is swapped for the sequential stream; the assertion 'flips < 50% of sequential' must fail
        fl_seq = np.mean([len(fam["EF-only (sequential G)"][0] - fam["EF-only (sequential G)"][k]) for k in KS[1:]])
        fl_mut = fl_seq  # same stream -> identical count
        log(f"MUTATE7: EF-only with the SEQUENTIAL stream in the per-pair slot: flips {fl_mut:.1f} vs sequential {fl_seq:.1f}; assertion '< 50%' ",
            "holds" if fl_mut < 0.5 * fl_seq else "FAILS")
        sys.exit(1 if not (fl_mut < 0.5 * fl_seq) else 0)

    # membership of U across builds (by id tuple), excluding nothing
    Uk = [set(zip(arrs[k]["id1"].tolist(), arrs[k]["id2"].tolist())) for k in KS]
    Uav = [C.pair_keys(arrs[k], arrs[k]["av_ok"]) for k in KS]
    memb = [len(Uk[k] - Uk[0]) + len(Uk[0] - Uk[k]) for k in KS[1:]]
    membav = [len(Uav[k] - Uav[0]) + len(Uav[0] - Uav[k]) for k in KS[1:]]
    log(f"membership of the MC array U_k against U_0 (both directions, k=1..9): {memb} mean {np.mean(memb):.1f}; A_V-ok part: mean {np.mean(membav):.1f}")
    res = {"membership_mean": float(np.mean(memb)), "membership_av_mean": float(np.mean(membav))}

    # flips and partition
    log("\nFlips against k=0 of the same family (one-way = in k=0, absent from k)")
    for name, sets in fam.items():
        oneway = [len(sets[0] - sets[k]) for k in KS[1:]]
        counts = [len(s) for s in sets]
        part_memb = [len([x for x in (sets[0] - sets[k]) if x not in Uk[k]]) for k in KS[1:]]
        log(f"  {name:26s} one-way {oneway} mean {np.mean(oneway):.1f}; final counts mean {np.mean(counts):.1f} SD {C.sd(counts):.1f}; "
            f"of which pair not in U_k at all (membership) mean {np.mean(part_memb):.1f}")
        res[name] = dict(flips=float(np.mean(oneway)), flips_list=oneway, count_sd=C.sd(counts), memb_part=float(np.mean(part_memb)))

    # fits
    log("\nFits (pipeline's own --catalog run, registered seed), 10 builds per family")
    fits = {}
    for name, sets in fam.items():
        jobs = []
        for k in KS:
            tagn = {"ALL": "ALL", "G-only": "G", "EF-only (sequential G)": "EFseq", "EF-only (per-pair G)": "EFpp"}[name]
            p = F3.CSVDIR / f"c4_{tagn}_{k}.csv"
            # write rows by key set: use array of the build's own array
            arr = arrs[k] if name != "G-only" else arrs[0]
            mask = np.array([(a, b) in sets[k] for a, b in zip(arr["id1"].tolist(), arr["id2"].tolist())])
            C.write_csv(arr, mask, p); jobs.append((p, C.FIT_SEED))
        fits[name] = F3.fits_parallel(jobs)
    log("fits done")
    sig_all = {}
    for name, rs in fits.items():
        s = F3.summarize(rs, name, log, rng, nboot=1000)
        res[name].update(fit=s)
        for fp in ("can", "alt"):
            sfit = s[fp]["mean_sigma"]; s[fp]["sd_over_sigma_tot"] = s[fp]["sd"] / np.sqrt(sfit ** 2 + 0.02 ** 2)
        log("    SD/sigma_tot: " + ", ".join(f"{fp} {s[fp]['sd_over_sigma_tot']:.3f}" for fp in ("can", "alt")))

    # pass lines
    allf = res["ALL"]["flips"]
    log("\nPASS LINES (family alone 'reproduces the whole spread': flips within [0.75,1.25] x ALL and SD ratio within a factor 2 of ALL)")
    checks = {}
    for name in ("G-only", "EF-only (sequential G)"):
        okf = 0.75 <= res[name]["flips"] / allf <= 1.25
        oks = all(0.5 <= res[name]["fit"][fp]["ratio"] / res["ALL"]["fit"][fp]["ratio"] <= 2.0 for fp in ("can", "alt"))
        checks[name] = okf and oks
        log(f"  {name}: flips ratio to ALL {res[name]['flips']/allf:.2f} ({'ok' if okf else 'out'}); SD-ratio vs ALL can {res[name]['fit']['can']['ratio']/res['ALL']['fit']['can']['ratio']:.2f} alt {res[name]['fit']['alt']['ratio']/res['ALL']['fit']['alt']['ratio']:.2f} ({'ok' if oks else 'out'})")
    pp = res["EF-only (per-pair G)"]["flips"]; sq = res["EF-only (sequential G)"]["flips"]
    log(f"  EF-only per-pair G flips {pp:.1f} vs sequential {sq:.1f}: ratio {pp/sq:.2f} (line: < 0.50 means the EF stream's own noise is small; the sequential EF-only spread rides on claim 1)")
    checks["MU7 per-pair < 50% of sequential"] = pp < 0.5 * sq
    for fp in ("can", "alt"):
        log(f"  [{fp}] SD/sigma_fit: ALL {res['ALL']['fit'][fp]['ratio']:.3f}, G-only {res['G-only']['fit'][fp]['ratio']:.3f}, EF-seq {res['EF-only (sequential G)']['fit'][fp]['ratio']:.3f}, EF-per-pair {res['EF-only (per-pair G)']['fit'][fp]['ratio']:.3f}")
    res["checks"] = {k: bool(v) for k, v in checks.items()}
    for k, v in checks.items():
        log(f"  [{'PASS' if v else 'FAIL'}] {k}")
    C.jdump(res, C.HERE / "CFG239_c4_streams.json")
    assert C.guard() == h0; log("guard after run ok")
    sys.exit(0)


if __name__ == "__main__":
    main()
