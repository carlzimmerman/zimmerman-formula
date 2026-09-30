#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 tooling: the SEED SWEEP -- K + 1 builds (k = 0 the frozen builder), each fitted by the pipeline's OWN `--catalog` run, and the build-to-build spread sigma_build (NEW file; nothing frozen is edited).
Design and controls: SEED_SWEEP_DESIGN_FROZEN.md (be8a6405d), written before this code.  DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.

Modes:  full    each build k > 0 re-runs stages E and F with its seed set (seeded_build.rebuild_EF, in memory, the builder's sha256 checked before and after) and then the driver's stage G with the G seed SEED + k
        g-only  only the stage-G velocity-error MC is re-seeded (fast; a code-path test of the driver option, NOT the WP2-gamma quantity)
Every build has its own correlation cache (seed_k<k>/stage_G_corr_<variant>.npz).  The fit of every build is `wide_binary_pipeline.py --catalog <csv> --seed 20261216` (the registered path; ~30 s), its printed
`gamma_inf = g +- s (chi2/bin=.., bins=.., kappa=k)` lines parsed for both footings.  FIT-ONLY CONTROL: the k = 0 catalogue refitted with `--seed 20261216 + j`, j = 1..K (the pipeline's seed feeds both its forward-model
population and its bootstrap).  sigma_build = SD (ddof = 1) of gamma-hat over the K + 1 builds, per footing, REPORTED ONLY.
MUTATE=1: every build is run with the IDENTICAL seed set (k forced to 0) and the identical fit seed: the final CSVs must have one sha256 and sigma_build must be 0 exactly (outputs *_MUTATE).
The seed list is written to seed_sweep_planned.json BEFORE any build; the values to seed_sweep_manifest.json afterwards.
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seed_sweep.py --release dr3 --K 2 --mode g-only [--fit] [--ladder] [--tag NAME]"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, os, re, subprocess, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
sys.path.insert(0, str(HERE))
PIPELINE = PREP / "wide_binary_pipeline.py"
FIT_SEED = 20261216                                                                # the registered fit seed
FOOT = {"canonical": "canonical", "alt footing": "alt"}
FIT_RE = re.compile(r"^\s*catalog \[a0 (canonical|alt footing)\]\s+gamma_inf = (\S+) \+- (\S+)\s+\(chi2/bin=(\S+), bins=(\d+), kappa=(\S+)\)", re.M)
RISK_RE = re.compile(r"^\s*\[7\(e\)\].*risk.*$", re.M)


def parse_pipeline_stdout(text):
    """gamma-hat, sigma_fit, chi2/bin, bins and kappa of both footings from the pipeline's --catalog output; raises if a footing line is missing."""
    out = {}
    for m in FIT_RE.finditer(text):
        out[FOOT[m.group(1)]] = dict(g=float(m.group(2)), s=float(m.group(3)), chi2_bin=float(m.group(4)), bins=int(m.group(5)), kappa=float(m.group(6)))
    if set(out) != {"canonical", "alt"}:
        raise ValueError(f"the pipeline output lacks a footing line: found {sorted(out)}")
    out["risk_lines"] = [m.group(0).strip() for m in RISK_RE.finditer(text)]
    return out


def fit_via_pipeline_cli(csv_path, seed=FIT_SEED, timeout=1800):
    """the registered fit path: the pipeline's own `--catalog` run as a subprocess (same on DR3 and on release day)."""
    r = subprocess.run([sys.executable, "-B", str(PIPELINE), "--catalog", str(csv_path), "--seed", str(int(seed))], capture_output=True, text=True, timeout=timeout, cwd=str(REPO))
    if r.returncode != 0:
        raise RuntimeError(f"pipeline exit {r.returncode}: {r.stderr[-400:]}")
    out = parse_pipeline_stdout(r.stdout)
    out["seed"], out["stdout_sha256"] = int(seed), hashlib.sha256(r.stdout.encode()).hexdigest()
    return out


def sd1(x):
    x = np.asarray(x, float)
    return float(np.std(x, ddof=1)) if len(x) > 1 else float("nan")


def pair_set(csv_bytes_or_path):
    txt = Path(csv_bytes_or_path).read_text() if not isinstance(csv_bytes_or_path, (bytes, bytearray)) else csv_bytes_or_path.decode()
    lines = txt.strip().split("\n")
    head = lines[0].split(",")
    i1, i2 = head.index("source_id1"), head.index("source_id2")
    return {tuple(sorted((int(c[i1]), int(c[i2])))) for c in (l.split(",") for l in lines[1:])}


def ruwe_lookup(stage_a_path):
    """source_id -> ruwe from stage A (only the two arrays are read)."""
    z = np.load(stage_a_path)
    sid, ruwe = z["source_id"], z["ruwe"]
    o = np.argsort(sid)
    sid, ruwe = sid[o], ruwe[o]

    def get(ids):
        ids = np.asarray(ids, dtype=np.int64)
        pos = np.clip(np.searchsorted(sid, ids), 0, len(sid) - 1)
        ok = sid[pos] == ids
        return np.where(ok, ruwe[pos], np.nan)
    return get


def ladder_rungs(csv_path, stage_a_path=None, ruwe_max=1.2):
    """(header, {rung name: rows}) for the ladder rungs that are post-filters of the final table with the columns the CSV carries: R_chance 0.01 -> 0.001, separation 2-30 -> 3-20 kAU and (with stage A)
    RUWE 1.4 -> 1.2 on both components.  RUWE 1.2 needs stage_a_path (a join by source_id); the RV-screened subsample and NSS-off are NOT implemented."""
    lines = Path(csv_path).read_text().strip().split("\n")
    head = lines[0].split(",")
    iR, iS = head.index("R_chance"), head.index("sep_kAU")
    rows = [l.split(",") for l in lines[1:]]
    rungs = {"R_chance<0.001": [c for c in rows if float(c[iR]) < 0.001], "sep 3-20 kAU": [c for c in rows if 3.0 < float(c[iS]) < 20.0]}
    if stage_a_path is not None:
        rl = ruwe_lookup(stage_a_path)
        i1, i2 = head.index("source_id1"), head.index("source_id2")
        r1 = rl([int(c[i1]) for c in rows])
        r2 = rl([int(c[i2]) for c in rows])
        rungs[f"RUWE<{ruwe_max} both"] = [c for c, x, y in zip(rows, r1, r2) if x < ruwe_max and y < ruwe_max]
    return head, rungs


def ladder_post_filters(csv_path, work, fit_seed=FIT_SEED, stage_a_path=None, ruwe_max=1.2):
    """each post-filter rung of the final table fitted by the pipeline's own --catalog run."""
    head, rungs = ladder_rungs(csv_path, stage_a_path, ruwe_max)
    out = {}
    for name, sel in rungs.items():
        p = Path(work) / ("ladder_" + re.sub(r"[^0-9A-Za-z]+", "_", name) + ".csv")
        p.write_text("\n".join([",".join(head)] + [",".join(c) for c in sel]) + "\n")
        out[name] = dict(n=len(sel), fit=fit_via_pipeline_cli(p, fit_seed))
    out["NOT_IMPLEMENTED"] = ["RV-screened subsample only (definition not fixed in code)", "NSS screen OFF (needs the superset table)"] + ([] if stage_a_path is not None else ["RUWE 1.4 -> 1.2 (pass stage_a_path)"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", choices=("dr3", "dr4"), default="dr3")
    ap.add_argument("--variant", choices=("primary", "allsource_15c"), default="primary")
    ap.add_argument("--cut13", choices=("extract-builder", "extract-orbit", "extract-literal"), default="extract-builder")
    ap.add_argument("--K", type=int, default=2, help="K further builds, k = 1..K (the primary is k = 0)")
    ap.add_argument("--mode", choices=("full", "g-only"), default="g-only")
    ap.add_argument("--n-shift", type=int, default=None, help="full mode: N_SHIFT (default the builder's own, 30)")
    ap.add_argument("--rebuild-k0", action="store_true", help="full mode: also rebuild k = 0 from the shared A-D inputs instead of using the extract's own stage_F")
    ap.add_argument("--fit", action="store_true", help="fit every build (and the fit-only control) by the pipeline's own --catalog run")
    ap.add_argument("--jobs", type=int, default=1, help="run this many pipeline fits at a time (each is a single-threaded subprocess)")
    ap.add_argument("--ladder", action="store_true", help="also the two ladder rungs that are post-filters of the final table (needs --fit)")
    ap.add_argument("--tag", default="")
    ap.add_argument("--allow-network", action="store_true")
    args = ap.parse_args()
    mut = os.environ.pop("MUTATE", "").strip() == "1"
    import dry_run_driver as D
    import seeded_build as SB
    D.init(args.allow_network)
    B = SB.import_builder()
    ext = D.extract_dir(args.release, args.variant)
    sfx = ("_" + args.tag if args.tag else "") + ("_MUTATE" if mut else "")
    out_dir = ext / "seed_sweep"
    out_dir.mkdir(exist_ok=True)
    ks = list(range(args.K + 1))
    n_shift = args.n_shift if (args.mode == "full" and args.n_shift) else B.N_SHIFT
    sha0 = SB.assert_builder_frozen("sweep start")
    plan = dict(status="planned", release=args.release, variant=args.variant, mode=args.mode, K=args.K, n_shift=n_shift, mutate_identical_seeds=mut, builder_sha256=sha0,
                seed_sets=[SB.seed_set(0 if mut else k, n_shift, B) for k in ks], fit="pipeline --catalog, seed %d" % FIT_SEED,
                fit_only_control_seeds=[FIT_SEED + j for j in range(1, args.K + 1)], time=time.strftime("%Y-%m-%d %H:%M:%S"))
    (out_dir / f"seed_sweep_planned{sfx}.json").write_text(json.dumps(plan, indent=1) + "\n")
    lines = []

    def P(s=""):
        print(s, flush=True); lines.append(s)

    P(f"SEED SWEEP ({args.release} {args.variant}, mode {args.mode}, K = {args.K}{', MUTATE: identical seed sets' if mut else ''}; N_SHIFT {n_shift}; DR3 numbers are code-path tests, never results)")
    P(f"  builder sha256 {sha0[:16]} (frozen value checked); seed list written BEFORE the builds to seed_sweep_planned{sfx}.json")
    builds = []
    for k in ks:
        ke = 0 if mut else k
        t0 = time.time()
        stage_dir, sec_ef = None, 0.0
        if args.mode == "full" and (ke > 0 or args.rebuild_k0):
            stage_dir = D.build_dir(ext, ke) / f"EF_nshift{n_shift}"                # the directory name carries N_SHIFT (a smoke build must never be reused as a real one)
            _, _, sec_ef = SB.rebuild_EF(ext, stage_dir, ke, n_shift, reuse=True)
        csv_bytes, rep = D.run(args.release, args.variant, args.cut13, None, args.allow_network, seed_offset=ke, stage_dir=stage_dir)
        bdir = D.build_dir(ext, k) if not mut else out_dir
        bdir.mkdir(exist_ok=True)
        csv_path = bdir / (f"final{sfx}.csv" if not mut else f"final_k{k}{sfx}.csv")
        csv_path.write_bytes(csv_bytes)
        SB.assert_builder_frozen("after build %d" % k)
        b = dict(k=k, seed_set_used=ke, n_pairs=rep["n_pairs"], csv=str(csv_path.relative_to(REPO)), csv_sha256=rep["sha256"], uncovered_corr_ids=[c.get("n_uncovered") for c in rep["correlations"]],
                 correlation_cache=rep["correlation_cache"], seconds_EF=round(sec_ef, 1), seconds=round(time.time() - t0, 1))
        builds.append(b)
        P(f"  build k = {k} (seed set {ke}): {b['n_pairs']:,d} pairs, csv sha256 {b['csv_sha256'][:16]}, uncovered correlation ids {b['uncovered_corr_ids']}, cache {b['correlation_cache']}  ({b['seconds']} s)")
    # ---- pair flips against k = 0
    sets = [pair_set(Path(REPO / b["csv"])) for b in builds]
    flips = [(len(sets[0] - s), len(s - sets[0])) for s in sets[1:]]
    P(f"  one-way flips against k = 0 (in k = 0 only, in build k only): {flips}")
    res = dict(plan=plan, builds=builds, flips_vs_k0=flips, builder_sha256_after=SB.assert_builder_frozen("sweep end"))
    if args.fit:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max(1, args.jobs)) as ex:
            fits = list(ex.map(lambda b: fit_via_pipeline_cli(REPO / b["csv"], FIT_SEED), builds))
            ctl = list(ex.map(lambda j: fit_via_pipeline_cli(REPO / builds[0]["csv"], FIT_SEED + j), range(1, args.K + 1))) if args.K >= 1 else []
        for b, f_ in zip(builds, fits):
            b["fit"] = f_
            P(f"  fit k = {b['k']}: canonical {b['fit']['canonical']['g']:.4f} +- {b['fit']['canonical']['s']:.4f} (kappa {b['fit']['canonical']['kappa']:.4f}); alt {b['fit']['alt']['g']:.4f} +- {b['fit']['alt']['s']:.4f} (kappa {b['fit']['alt']['kappa']:.4f})")
        res["fit_only_control"] = ctl
        sb, st = {}, {}
        for f in ("canonical", "alt"):
            g = [b["fit"][f]["g"] for b in builds]
            ms = float(np.mean([b["fit"][f]["s"] for b in builds]))
            co = [builds[0]["fit"][f]["g"]] + [c[f]["g"] for c in ctl]
            sb[f] = dict(sigma_build=sd1(g), mean_sigma_fit=ms, ratio=sd1(g) / ms, gammas=g, kappas=[b["fit"][f]["kappa"] for b in builds], fit_only_sd_incl_registered=sd1(co), fit_only_gammas=co)
            P(f"  {f:9s}: sigma_build = SD over {len(g)} builds = {sb[f]['sigma_build']:.4f} = {sb[f]['ratio']:.3f} of the mean sigma_fit {ms:.4f}; fit-only control SD {sb[f]['fit_only_sd_incl_registered']:.4f} over {len(co)} fits")
        res["sigma_build"] = sb
        if args.ladder:
            for b in builds:
                b["ladder"] = ladder_post_filters(REPO / b["csv"], D.build_dir(ext, b["k"]) if not mut else out_dir, stage_a_path=ext / "stage_A.npz")
                P(f"  ladder k = {b['k']}: " + "; ".join(f"{n} N={v['n']:,d} gamma {v['fit']['canonical']['g']:.4f} (shift {v['fit']['canonical']['g'] - b['fit']['canonical']['g']:+.4f} = {(v['fit']['canonical']['g'] - b['fit']['canonical']['g']) / b['fit']['canonical']['s']:+.2f} sigma_fit)"
                                                    for n, v in b["ladder"].items() if n != "NOT_IMPLEMENTED"))
    res["status"] = "done"
    (out_dir / f"seed_sweep_manifest{sfx}.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    (out_dir / f"seed_sweep{sfx}.out").write_text("\n".join(lines) + "\n")
    return res


if __name__ == "__main__":
    main()
