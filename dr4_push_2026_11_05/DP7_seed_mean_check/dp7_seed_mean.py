#!/usr/bin/env python3
"""DP7: the seed-mean NSS-off entry, DR3 code-path check (FROZEN_CRITERIA.md 1b87706e49; draft 4d8711da63 section 4). NEW CODE ONLY.

A sweep wrapper over DP1's `rung_build(...)` (dr4_push_2026_11_05/DP1_nss_off_rung/nss_off_rung.py, imported read-only, unchanged)
and the registered base build at the same stage-G seed offset k, both in the same cut-13 mode, fitted one footing at a time by
  --fit-path pipeline : the registered path, the frozen pipeline's own `--catalog` run at seed 20261216 (the call of DP1's
                        SS.fit_via_pipeline_cli, identical argv, here under /usr/bin/time -l so the fit's peak RSS is recorded)
  --fit-path d2       : DP1's D2Estimator.fit_fresh (K1 only: the exact reproduction of DP1's P4 ensemble)
Per k and footing: gamma_hat(base_k), gamma_hat(rung_k), Delta_k = gamma_hat(rung_k) - gamma_hat(base_k), sigma_fit of each.
Then Delta_bar = mean_{k=1..K} Delta_k, its SD (ddof 1) and SE = SD / sqrt(K), and the seed-mean entry gamma_hat_0 + Delta_bar
with gamma_hat_0 the k = 0 primary fit of the same run; the single-seed shift Delta_0 is printed beside it.

  python3 -B dp7_seed_mean.py --cut13 extract-builder --fit-path d2 --K 8 --out k1              (K1: DP1 P4 bit for bit)
  python3 -B dp7_seed_mean.py --cut13 extract-builder --fit-path pipeline --K 0 --out k2        (K2: DP1 P3 at k = 0)
  python3 -B dp7_seed_mean.py --cut13 cones-literal --fit-path pipeline --K 50 --out dp7        (the graded sweep; K3, K4, K6 inside)
  ... --mutate-k0 --out dp7_MUTATE1        (M1: the k = 0 paired difference returned for every k)
  ... --keep-nss  --out dp7_MUTATE2        (M2: drop_nss = False, the rung equals the base)
AMENDMENT_A1: the graded sweep and M1 / M2 carry --rung-missing-cones extract-fallback (the RUNG's pairs reaching cut 13 with no DR3
cone, the 139 NSS-flagged pairs, take the frozen builder's third-star flag on the extract; the BASE stays strict cones-literal), and
  ... --cut13 cones-literal --fit-path pipeline --rung-missing-cones extract-fallback --control-c1 --out dp7_C1
flags one randomly chosen uncovered pair (numpy default_rng seed 1103) in the k = 0 rung and refits it: the change in gamma_hat per
footing is the measured bias bound (must be < 1e-3, else reported beside the label).
Checkpoint: one json per k in parts/ (resumed on restart, so a SIGTERM loses at most one k). Offline: a socket guard is
installed at import; DR3 inputs are read from the extract root the DP3 dry run used. No frozen file is edited (K5 checks the
sha256 of the five DP1-pinned files and the 27 DP3-pinned files before and after). DR4 (untested; every k >= 1 stage-G fetch is an
archive query needing the owner's go on release day): --release dr4 --manifest M.json --neighbours-manifest NM.json --allow-network.
NON-SCORING: DR3 numbers are code-path tests, never results (Amendment 7(e)). kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
sys.dont_write_bytecode = True
import argparse, csv, hashlib, io, json, math, re, resource, signal, socket, subprocess, time
from pathlib import Path


def _no_net(*a, **k):
    raise RuntimeError("network access forbidden (DP7 seed-mean check)")


socket.socket.connect = _no_net
socket.create_connection = _no_net
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DP1 = REPO / "dr4_push_2026_11_05" / "DP1_nss_off_rung"
DP3 = REPO / "dr4_push_2026_11_05" / "DP3_release_day"
sys.path.insert(0, str(DP1))
import nss_off_rung as NR                       # DP1, read-only (it imports dry_run_driver, build_variant_catalogue, seed_sweep, wide_binary_pipeline read-only)
D, BV, SS = NR.D, NR.BV, NR.SS
FOOTS = NR.FOOTS
FIT_SEED = NR.FIT_SEED
PIPE_SHA = NR.PIPE_SHA
READY = NR.PREP / "dr4_ready_1"
G50_MANIFEST = READY / "seed_sweep_manifest_g50_dr3.json"
K3_REF = dict(n_pairs=6180, sha256_prefix="c5cb89e8f95bfe3d")     # the DP3 dry run's cones-literal base (D2, DRY_RUN_2026-11-05.md)
PARTS = HERE / "parts"
WORK = HERE / "work"                                              # derived CSVs and the fit cache; not committed
STOP = {"flag": False}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def rss_self_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3          # macOS: bytes


# ------------------------------------------------------------------ frozen files (K5)
def pinned_dp3():
    """the 27 (sha256, path) pairs pinned in dr4_release_day.sh (its HASHES block), paths repo-relative."""
    txt = (DP3 / "dr4_release_day.sh").read_text()
    sub = {"$PREP": "prep_2026/gaia_dr4_prep", "$READY": "prep_2026/gaia_dr4_prep/dr4_ready_1", "$CFG": "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring"}
    out = []
    for m in re.finditer(r"^([0-9a-f]{64}) (\S+)$", txt, re.M):
        p = m.group(2)
        for k, v in sub.items():
            p = p.replace(k, v)
        out.append((m.group(1), p))
    return out


def frozen_now():
    """sha256 of every pinned file now: DP1's five (NR.frozen_shas) and DP3's 27, keyed by repo-relative path."""
    out = {f"DP1:{k}": v for k, v in NR.frozen_shas().items()}
    for pinned, rel in pinned_dp3():
        p = REPO / rel
        out[rel] = sha256(p.read_bytes()) if p.exists() else "MISSING"
    return out


def frozen_check(sh0, sh1):
    pinned = {rel: h for h, rel in pinned_dp3()}
    drift = sorted(k for k in sh0 if sh0[k] != sh1.get(k))
    off_pin = sorted(rel for rel, h in pinned.items() if sh1.get(rel) != h)
    pipe_ok = sh1["DP1:wide_binary_pipeline.py"] == PIPE_SHA
    return dict(passed=(not drift and not off_pin and pipe_ok), n_files=len(sh0), changed_during_run=drift, off_pinned_value=off_pin,
                pipeline_sha256=sh1["DP1:wide_binary_pipeline.py"], pipeline_is_7c884e0e=pipe_ok)


# ------------------------------------------------------------------ the two fit paths
def parse_time_l(stderr):
    m = re.search(r"^\s*(\d+)\s+maximum resident set size", stderr, re.M)
    w = re.search(r"^\s*([0-9.]+) real", stderr, re.M)
    return (int(m.group(1)) / 1024 ** 3 if m else None), (float(w.group(1)) if w else None)


def fit_pipeline(csv_path, seed=FIT_SEED, timeout=1800):
    """the registered fit path: SS.fit_via_pipeline_cli's exact argv ([python, -B, wide_binary_pipeline.py, --catalog, CSV, --seed, SEED],
    cwd REPO), run under /usr/bin/time -l so the subprocess's peak RSS is recorded; parsed by SS.interpret_pipeline_run (unchanged)."""
    argv = [sys.executable, "-B", str(SS.PIPELINE), "--catalog", str(csv_path), "--seed", str(int(seed))]
    t0 = time.time()
    r = subprocess.run(["/usr/bin/time", "-l"] + argv, capture_output=True, text=True, timeout=timeout, cwd=str(SS.REPO))
    out = SS.interpret_pipeline_run(r.returncode, r.stdout, r.stderr)
    out["seed"], out["stdout_sha256"] = int(seed), sha256(r.stdout.encode())
    out["rss_gb"], out["time_real_s"] = parse_time_l(r.stderr)
    out["wall_s"] = time.time() - t0
    out.pop("risk_lines", None)
    return out


class FitCache:
    """pipeline fits keyed by (csv sha256, seed, pipeline sha): the registered fit is deterministic at its seed on identical bytes
    (K2 re-derives DP1 P3 from a fresh run; the dry run D3 reproduced the 10-09 fit). A hit is recorded as cached = True in the part."""
    def __init__(self, path, enabled=True):
        self.path, self.enabled = path, enabled
        self.d = json.loads(path.read_text()) if (enabled and path.exists()) else {}

    def fit(self, csv_path, csv_bytes):
        key = f"{sha256(csv_bytes)}|{FIT_SEED}|{PIPE_SHA[:16]}"
        if self.enabled and key in self.d:
            return dict(self.d[key], cached=True)
        f = fit_pipeline(csv_path)
        f["cached"] = False
        if self.enabled:
            self.d[key] = {k: v for k, v in f.items() if k != "cached"}
            tmp = self.path.with_suffix(".tmp"); tmp.write_text(json.dumps(self.d, indent=0)); tmp.replace(self.path)
        return f


def fit_d2(est, csv_bytes):
    rows = NR.rows_of(csv_bytes)
    out = {}
    for fo in FOOTS:
        f = est.fit_fresh(rows, fo)
        out[fo] = dict(g=f["gamma"], s=f["sigma_fit"], kappa=f["kappa"], N=f["N"])
    out["self_test_passed"] = None
    return out


# ------------------------------------------------------------------ cones (cut 13, release-day primary form)
def load_cones(a):
    import cones_cut13
    ext = D.extract_dir(a.release, a.variant)
    if a.neighbours_manifest:
        for e in json.loads(Path(a.neighbours_manifest).read_text()):
            if e.get("include") is True:
                a.neighbours.append(e["neighbours"]); a.neighbour_pairs.append(e["pairs"])
    if not a.neighbours and a.release == "dr3":                                         # the DP3 dry run's DR3 cones files (dr4_release_day.sh lines 252-253)
        a.neighbours = [str(ext / "dr4_ready_1" / "q1_full_neighbours.fits"), str(ext / "dr4_ready_1" / "q1_delta_neighbours.fits")]
        a.neighbour_pairs = [str(ext / "wide_binaries_dr3.csv"), str(ext / "dr4_ready_1" / "q1_delta_pairs.csv")]
    if len(a.neighbours) != len(a.neighbour_pairs) or not a.neighbours:
        raise SystemExit("a cones kind needs --neighbours and --neighbour-pairs (or --neighbours-manifest)")
    for p in a.neighbours + a.neighbour_pairs:
        if not Path(p).exists():
            raise SystemExit(f"MISSING DR3 input (stop, do not fetch): {Path(p).relative_to(REPO) if Path(p).is_relative_to(REPO) else p}")
    t0 = time.time()
    cones = cones_cut13.ConeTable.from_files(zip(a.neighbours, a.neighbour_pairs))
    files = [str(Path(p).relative_to(REPO)).replace("real_research/data/widebinaries/", "<external>/") for p in a.neighbours + a.neighbour_pairs]
    return cones, dict(files=files, load_s=round(time.time() - t0, 1))


# ------------------------------------------------------------------ one k
def one_k(k, a, cones, fitter, est, ext, manifest):
    k_eff = 0 if a.mutate_k0 else k
    drop = not a.keep_nss
    t0 = time.time()
    tb = time.time()
    bb, rb = NR.rung_build(False, 30, a.release, a.variant, a.cut13, manifest, a.allow_network, seed_offset=k_eff, cones=cones)
    t_base = time.time() - tb
    tb = time.time()
    br, rr = NR.rung_build(drop, 30, a.release, a.variant, a.cut13, manifest, a.allow_network, seed_offset=k_eff, cones=cones, missing_cones=a.rung_missing_cones)
    t_rung = time.time() - tb
    part = dict(k=k, k_eff=k_eff, cut13=a.cut13, fit_path=a.fit_path, mutate_k0=a.mutate_k0, keep_nss=a.keep_nss, drop_nss=drop, rung_missing_cones=a.rung_missing_cones,
                base=dict(n_pairs=rb["n_pairs"], sha256=rb["sha256"], build_s=round(t_base, 2), stage_G_seed=rb.get("stage_G_seed", "default (SEED)"),
                          correlations=rb.get("correlations")),
                rung=dict(n_pairs=rr["n_pairs"], sha256=rr["sha256"], build_s=round(t_rung, 2), label=rr["rung"], switches=rr["variant_switches"],
                          correlations=rr.get("correlations"), cut13_cones=rr.get("cut13_cones")),
                rung_equals_base_bytes=(bb == br), n_builds=2)
    # K4: the extract-builder base_k against the G10/G50 build on disk (DP1's base_equals_g50_build, repeated)
    g50 = ext / f"seed_k{k_eff}" / "final_g50.csv"
    if a.cut13 == "extract-builder":
        eb = bb
    else:
        tb = time.time()
        eb, _ = NR.rung_build(False, 30, a.release, a.variant, "extract-builder", manifest, a.allow_network, seed_offset=k_eff)
        part["k4_extract_builder_build_s"] = round(time.time() - tb, 2); part["n_builds"] = 3
    part["K4"] = dict(g50_exists=g50.exists(), base_equals_g50_build=(g50.exists() and eb == g50.read_bytes()), extract_builder_sha256=sha256(eb)[:16],
                      g50=str(g50.relative_to(REPO)).replace("real_research/data/widebinaries/", "<external>/") if g50.exists() else None)
    if k_eff == 0:
        ref = ext / "wide_binaries_dr3.csv"
        part["K4"]["extract_builder_equals_registered_csv"] = bool(ref.exists() and eb == ref.read_bytes())
    if k == 0 and a.cut13 == "cones-literal" and a.release == "dr3":                  # K3
        part["K3"] = dict(n_pairs=rb["n_pairs"], sha256_prefix=rb["sha256"][:16], ref=K3_REF, passed=(rb["n_pairs"] == K3_REF["n_pairs"] and rb["sha256"].startswith(K3_REF["sha256_prefix"])))
        dry = DP3 / "dry_run_dr3" / "wb_dr3_cones_literal.csv"
        part["K3"]["equals_dry_run_csv_on_disk"] = (bb == dry.read_bytes()) if dry.exists() else "dry-run csv not on disk (sha compared instead)"
    # fits
    wk = WORK / f"k{k:02d}_{a.cut13}_{a.fit_path}{'_M1' if a.mutate_k0 else ''}{'_M2' if a.keep_nss else ''}"
    wk.mkdir(parents=True, exist_ok=True)
    pb, pr = wk / "base.csv", wk / "rung.csv"
    pb.write_bytes(bb); pr.write_bytes(br)
    if a.fit_path == "pipeline":
        fb = fitter.fit(pb, bb); fr = fitter.fit(pr, br)
    else:
        fb, fr = fit_d2(est, bb), fit_d2(est, br)
    part["n_fits"] = 2
    for fo in FOOTS:
        part[fo] = dict(base=fb[fo]["g"], rung=fr[fo]["g"], sigma_fit_base=fb[fo]["s"], sigma_fit_rung=fr[fo]["s"], delta=fr[fo]["g"] - fb[fo]["g"],
                        kappa_base=fb[fo]["kappa"], kappa_rung=fr[fo]["kappa"])
    part["fit"] = dict(base=dict(self_test_passed=fb.get("self_test_passed"), rss_gb=fb.get("rss_gb"), wall_s=fb.get("wall_s"), cached=fb.get("cached", False), stdout_sha256=fb.get("stdout_sha256")),
                       rung=dict(self_test_passed=fr.get("self_test_passed"), rss_gb=fr.get("rss_gb"), wall_s=fr.get("wall_s"), cached=fr.get("cached", False), stdout_sha256=fr.get("stdout_sha256")))
    part["K6"] = dict(base_self_test_passed=fb.get("self_test_passed"), rung_self_test_passed=fr.get("self_test_passed"),
                      flagged=(a.fit_path == "pipeline" and not (fb.get("self_test_passed") and fr.get("self_test_passed"))))
    part["wall_s"] = round(time.time() - t0, 1)
    part["wrapper_rss_gb_so_far"] = round(rss_self_gb(), 3)
    return part


def part_path(k, a):
    return PARTS / f"{a.out}_k{k:02d}.json"


def part_matches(p, a, k):
    return (p.get("k") == k and p.get("cut13") == a.cut13 and p.get("fit_path") == a.fit_path and bool(p.get("mutate_k0")) == a.mutate_k0 and bool(p.get("keep_nss")) == a.keep_nss
            and p.get("rung_missing_cones", "error") == a.rung_missing_cones)


# ------------------------------------------------------------------ control C1 (AMENDMENT_A1 item 3)
def control_c1(a, cones, fitter, manifest, P):
    """flag one randomly chosen uncovered pair (seed 1103) inside the k = 0 rung's extract-fallback and refit by the registered path."""
    br, rr = NR.rung_build(True, 30, a.release, a.variant, a.cut13, manifest, a.allow_network, seed_offset=0, cones=cones, missing_cones="extract-fallback")
    orig = D.B.third_star_flags
    pick = dict(calls=0)

    def patched(S_, a_, b_):                                                     # the fallback is the only caller of B.third_star_flags in a cones build
        f = np.asarray(orig(S_, a_, b_), bool).copy()
        i = int(np.random.default_rng(1103).integers(len(f)))
        pick.update(calls=pick["calls"] + 1, n_uncovered=int(len(f)), index=i, pair=[int(S_["source_id"][a_[i]]), int(S_["source_id"][b_[i]])], already_flagged=bool(f[i]),
                    fallback_flagged_before=int(f.sum()))
        f[i] = True
        return f
    D.B.third_star_flags = patched
    try:
        bc, rc = NR.rung_build(True, 30, a.release, a.variant, a.cut13, manifest, a.allow_network, seed_offset=0, cones=cones, missing_cones="extract-fallback")
    finally:
        D.B.third_star_flags = orig
    wk = WORK / "c1"; wk.mkdir(parents=True, exist_ok=True)
    pr, pc = wk / "rung_k0_fallback.csv", wk / "rung_k0_fallback_one_flagged.csv"
    pr.write_bytes(br); pc.write_bytes(bc)
    fr, fc = fitter.fit(pr, br), fitter.fit(pc, bc)

    def pair_set(b):                                                             # final-catalogue pair ids, to see what one flag at cut 13 moves
        rows = list(csv.DictReader(io.StringIO(b.decode())))
        ks = [c for c in rows[0] if "source_id" in c][:2]
        return {(r[ks[0]], r[ks[1]]) for r in rows}
    A, Bs = pair_set(br), pair_set(bc)
    setdiff = dict(only_in_reference=len(A - Bs), only_in_one_flagged=len(Bs - A), symmetric_difference=len(A ^ Bs),
                   note="the stage-G vtilde-error MC (B.vt_error_mc, seed SEED + k) is drawn over the post-cut-13 pair set; one pair fewer at cut 13 "
                        "re-aligns that stream, so the final catalogue changes by many pairs, not one: the measured change is one draw of the stage-G "
                        "seed noise (the quantity this lane measures), not the bias of the one pair")
    res = dict(control="C1 (AMENDMENT_A1 item 3)", seed=1103, pick=pick, reference=dict(n_pairs=rr["n_pairs"], sha256=rr["sha256"], cut13_cones=rr.get("cut13_cones")),
               one_flagged=dict(n_pairs=rc["n_pairs"], sha256=rc["sha256"], cut13_cones=rc.get("cut13_cones")), pair_removed_from_final=(rr["n_pairs"] - rc["n_pairs"]),
               final_pair_set_difference=setdiff, fallback_called_once=(pick["calls"] == 1), threshold=1e-3)
    ok = pick["calls"] == 1
    for fo in FOOTS:
        ch = fc[fo]["g"] - fr[fo]["g"]
        res[fo] = dict(gamma_reference=fr[fo]["g"], sigma_fit_reference=fr[fo]["s"], gamma_one_flagged=fc[fo]["g"], sigma_fit_one_flagged=fc[fo]["s"], change=ch, below_1e3=abs(ch) < 1e-3,
                       self_test=[fr.get("self_test_passed"), fc.get("self_test_passed")], rss_gb=[fr.get("rss_gb"), fc.get("rss_gb")])
        ok &= abs(ch) < 1e-3
        P(f"  C1 {fo:9s} rung k=0 (fallback) {fr[fo]['g']:.4f}+-{fr[fo]['s']:.4f}  one uncovered pair flagged {fc[fo]['g']:.4f}+-{fc[fo]['s']:.4f}  change {ch:+.6f}  (< 1e-3: {abs(ch) < 1e-3})")
    res["passed"] = ok
    P(f"C1: flagged pair {pick.get('pair')} (index {pick.get('index')} of {pick.get('n_uncovered')} uncovered; fallback called {pick['calls']} time(s); already flagged {pick.get('already_flagged')}); "
      f"final pairs {rr['n_pairs']} -> {rc['n_pairs']}; bias bound {'BELOW 1e-3 on both footings' if ok else 'NOT below 1e-3: the measured change is reported beside the label'}")
    P(f"C1 final pair sets: only in reference {setdiff['only_in_reference']}, only in one-flagged {setdiff['only_in_one_flagged']}, symmetric difference {setdiff['symmetric_difference']} "
      f"(one flag at cut 13 re-aligns the seeded stage-G vtilde-error MC stream: the change is one draw of the stage-G seed noise, not a one-pair bias)")
    return res


# ------------------------------------------------------------------ K1 against DP1
def k1_compare(parts):
    ref = json.loads((DP1 / "dr3_check.json").read_text())
    ens = {e["k"]: e for e in ref["ensemble"]}
    rows, exact = [], True
    for p in parts:
        k = p["k"]
        if k not in ens:
            continue
        e = ens[k]
        for fo in FOOTS:
            for nm, mine, theirs in (("base", p[fo]["base"], e[fo]["base"]), ("rung", p[fo]["rung"], e[fo]["rung"]), ("sigma_fit_base", p[fo]["sigma_fit_base"], e[fo]["sigma_fit_base"]),
                                     ("rung-base", p[fo]["delta"], e[fo]["rung"] - e[fo]["base"])):
                ok = (mine == theirs)
                exact &= ok
                rows.append(dict(k=k, footing=fo, quantity=nm, dp7=mine, dp1=theirs, bit_identical=ok))
        nok = (p["base"]["n_pairs"] == e["N"]["base"] and p["rung"]["n_pairs"] == e["N"]["rung"] and bool(p["K4"]["base_equals_g50_build"]) == bool(e["base_equals_g50_build"]))
        exact &= nok
        rows.append(dict(k=k, footing="-", quantity="N base/rung, base==G50", dp7=[p["base"]["n_pairs"], p["rung"]["n_pairs"], p["K4"]["base_equals_g50_build"]],
                         dp1=[e["N"]["base"], e["N"]["rung"], e["base_equals_g50_build"]], bit_identical=nok))
    means = {}
    for fo in FOOTS:
        sr = np.array([p[fo]["delta"] for p in parts if p["k"] in ens])
        m, s = float(sr.mean()), float(sr.std(ddof=1))
        rm, rs = ref["P4"][fo]["mean_rung_shift"], ref["P4"][fo]["sd_rung_shift"]
        means[fo] = dict(mean=m, sd=s, dp1_mean=rm, dp1_sd=rs, mean_within_1e6=abs(m - rm) <= 1e-6, sd_within_1e6=abs(s - rs) <= 1e-6, mean_exact=(m == rm), sd_exact=(s == rs))
    ks = sorted(k for k in ens if any(p["k"] == k for p in parts))
    passed = exact and ks == list(range(1, 9)) and all(means[f]["mean_within_1e6"] and means[f]["sd_within_1e6"] for f in FOOTS)
    return dict(passed=passed, n_values=len(rows), n_bit_identical=sum(r["bit_identical"] for r in rows), ks=ks, means=means, rows=rows)


def k2_compare(part0):
    ref = json.loads((DP1 / "dr3_check.json").read_text())["P3"]["fits"]
    rows, ok = [], True
    for nm in ("base", "rung"):
        for fo in FOOTS:
            for q, mine, theirs in (("g", part0[fo][nm], ref[nm][fo]["g"]), ("s", part0[fo]["sigma_fit_" + nm], ref[nm][fo]["s"])):
                d = abs(mine - theirs); ok &= d <= 1e-4
                rows.append(dict(catalogue=nm, footing=fo, quantity=q, dp7=mine, dp1_P3=theirs, abs_diff=d, within_1e4=d <= 1e-4))
    rung_sha_ok = part0["rung"]["sha256"].startswith("1dbdf21a461a2f3b")
    base_sha_ok = part0["base"]["sha256"].startswith(D.REF_SHA_DR3)
    return dict(passed=ok and rung_sha_ok and base_sha_ok, rows=rows, base_sha_is_registered=base_sha_ok, rung_sha_is_dp1_rung=rung_sha_ok)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cut13", choices=("extract-builder", "cones-literal"), required=True)
    ap.add_argument("--fit-path", choices=("d2", "pipeline"), required=True)
    ap.add_argument("--K", type=int, required=True)
    ap.add_argument("--out", required=True, help="output prefix: OUT.json, OUT.out, parts/OUT_kNN.json")
    ap.add_argument("--mutate-k0", action="store_true", help="MUTATE M1: the k = 0 paired difference for every k")
    ap.add_argument("--keep-nss", action="store_true", help="MUTATE M2: drop_nss = False (the rung equals the base)")
    ap.add_argument("--no-fit-cache", action="store_true", help="refit identical bytes instead of serving the sha-keyed fit cache")
    ap.add_argument("--rung-missing-cones", choices=("error", "extract-fallback"), default="error",
                    help="AMENDMENT_A1: the RUNG's cut-13 pairs with no cone take the frozen builder's third-star flag on the extract (the base stays strict)")
    ap.add_argument("--control-c1", action="store_true", help="AMENDMENT_A1 item 3: flag one random uncovered pair (seed 1103) in the k = 0 rung, refit, report the change")
    ap.add_argument("--release", choices=("dr3", "dr4"), default="dr3"); ap.add_argument("--variant", choices=("primary",), default="primary")
    ap.add_argument("--manifest", default=None); ap.add_argument("--allow-network", action="store_true")
    ap.add_argument("--neighbours", action="append", default=[]); ap.add_argument("--neighbour-pairs", action="append", default=[])
    ap.add_argument("--neighbours-manifest", default=None)
    a = ap.parse_args()
    if a.allow_network:
        if a.release != "dr4":
            raise SystemExit("--allow-network is for --release dr4 only (every k >= 1 fetch is an archive query needing the owner's go)")
        raise SystemExit("DR4 path: not run in DP7 (archive queries need the owner's go on release day); the command is recorded in RESULT.md")
    if a.mutate_k0 and a.keep_nss:
        raise SystemExit("one mutation at a time")
    PARTS.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
    lines = []

    def P(s=""):
        print(s, flush=True); lines.append(s)

    def on_term(signum, frame):
        STOP["flag"] = True; P(f"SIGTERM received: finishing k in progress, then stopping (parts/ keeps the checkpoint)")
    signal.signal(signal.SIGTERM, on_term)
    t0 = time.time()
    D.init(a.allow_network)
    sh0 = frozen_now()
    ext = D.extract_dir(a.release, a.variant)
    manifest = json.loads(Path(a.manifest).read_text()) if a.manifest else None
    P("=" * 110)
    P(f"DP7 seed-mean NSS-off entry: {a.release} {a.variant} cut13 {a.cut13}, fit path {a.fit_path}, K = {a.K}, rung missing cones: {a.rung_missing_cones}" +
      (" [MUTATE M1 --mutate-k0]" if a.mutate_k0 else "") + (" [MUTATE M2 --keep-nss]" if a.keep_nss else "") + (" [CONTROL C1]" if a.control_c1 else ""))
    P("NON-SCORING: DR3 numbers are code-path tests, never results (Amendment 7(e)). kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    P("=" * 110)
    P(f"frozen files pinned: {len(sh0)} (DP1 five + DP3 27); pipeline sha {sh0['DP1:wide_binary_pipeline.py'][:8]}; OMP_NUM_THREADS {os.environ.get('OMP_NUM_THREADS')}; nice {os.nice(0)}")
    cones, cones_info = (None, None)
    if a.cut13 == "cones-literal":
        cones, cones_info = load_cones(a)
        P(f"cones loaded: {cones_info['files']} [{cones_info['load_s']} s, wrapper RSS {rss_self_gb():.2f} GB]")
    est = None
    if a.fit_path == "d2":
        tb = time.time(); est = NR.D2Estimator(); P(f"D2 estimator built (1e6 master, seed {FIT_SEED}) [{time.time() - tb:.0f} s, wrapper RSS {rss_self_gb():.2f} GB]")
    fitter = FitCache(WORK / "fit_cache.json", enabled=not a.no_fit_cache)
    if a.control_c1:
        if a.cut13 != "cones-literal" or a.fit_path != "pipeline":
            raise SystemExit("--control-c1 is the cones-literal, pipeline-fit control")
        res = control_c1(a, cones, fitter, manifest, P)
        res["K5"] = frozen_check(sh0, frozen_now())
        P(f"K5 (frozen files unchanged): {'PASS' if res['K5']['passed'] else 'FAIL'}  {res['K5']['n_files']} files")
        P(f"C1 done [{time.time() - t0:.0f} s; wrapper peak RSS {rss_self_gb():.2f} GB]")
        (HERE / f"{a.out}.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
        (HERE / f"{a.out}.out").write_text("\n".join(lines) + "\n")
        return 0
    parts = []
    for k in range(0, a.K + 1):
        pp = part_path(k, a)
        if pp.exists():
            p = json.loads(pp.read_text())
            if part_matches(p, a, k):
                p["resumed_from_checkpoint"] = True; parts.append(p)
                P(f"  k={k:2d} (checkpoint) " + "  ".join(f"{fo}: base {p[fo]['base']:.4f} rung {p[fo]['rung']:.4f} delta {p[fo]['delta']:+.4f}" for fo in FOOTS))
                continue
        p = one_k(k, a, cones, fitter, est, ext, manifest)
        tmp = pp.with_suffix(".tmp"); tmp.write_text(json.dumps(p, indent=1, default=float) + "\n"); tmp.replace(pp)
        parts.append(p)
        P(f"  k={k:2d} k_eff={p['k_eff']:2d}  N base/rung {p['base']['n_pairs']}/{p['rung']['n_pairs']}  base==G50 {p['K4']['base_equals_g50_build']}  " +
          "  ".join(f"{fo}: base {p[fo]['base']:.4f}+-{p[fo]['sigma_fit_base']:.4f} rung {p[fo]['rung']:.4f} delta {p[fo]['delta']:+.4f}" for fo in FOOTS) +
          f"  self-test {p['K6']['base_self_test_passed']}/{p['K6']['rung_self_test_passed']}" + (f"  fit RSS {p['fit']['base']['rss_gb'] or 0:.2f}/{p['fit']['rung']['rss_gb'] or 0:.2f} GB" if a.fit_path == 'pipeline' else "") +
          f"  [{p['wall_s']:.0f} s; {time.time() - t0:.0f} s total]" + ("  (fit cache hit)" if p['fit']['base']['cached'] or p['fit']['rung']['cached'] else ""))
        if STOP["flag"]:
            P("stopped after a clean checkpoint"); break
    done = len(parts) == a.K + 1
    # summary
    sweep = [p for p in parts if p["k"] >= 1]
    res = dict(release=a.release, variant=a.variant, cut13=a.cut13, fit_path=a.fit_path, K=a.K, mutate_k0=a.mutate_k0, keep_nss=a.keep_nss, fit_cache=not a.no_fit_cache, rung_missing_cones=a.rung_missing_cones,
               complete=done, n_k_done=len(parts), cones=cones_info, fit_seed=FIT_SEED, criteria="dr4_push_2026_11_05/DP7_seed_mean_check/FROZEN_CRITERIA.md (1b87706e49)",
               non_scoring="DR3 numbers are code-path tests, never results (Amendment 7(e)); kappa = 1/2 FITTED; footings never pooled; not theory closed")
    p0 = next((p for p in parts if p["k"] == 0), None)
    P("")
    for fo in FOOTS:
        d = np.array([p[fo]["delta"] for p in sweep]) if sweep else np.zeros(0)
        n = len(d)
        dbar = float(d.mean()) if n else None
        sd = float(d.std(ddof=1)) if n > 1 else (0.0 if n == 1 else None)
        se = (sd / math.sqrt(n)) if (n and sd is not None) else None
        g0 = p0[fo]["base"] if p0 else None
        d0 = p0[fo]["delta"] if p0 else None
        res[fo] = dict(K_done=n, delta_bar=dbar, sd=sd, se=se, gamma_0=g0, sigma_fit_0=(p0[fo]["sigma_fit_base"] if p0 else None), single_seed_shift=d0,
                       gamma_rung_0=(p0[fo]["rung"] if p0 else None), seed_mean_entry=(g0 + dbar) if (g0 is not None and dbar is not None) else None,
                       single_seed_entry=(g0 + d0) if (g0 is not None and d0 is not None) else None,
                       deltas={p["k"]: p[fo]["delta"] for p in sweep}, bases={p["k"]: p[fo]["base"] for p in parts}, rungs={p["k"]: p[fo]["rung"] for p in parts},
                       n42_seed_mean=(NR.n42_reading(dbar, p0[fo]["sigma_fit_base"]) if (p0 and dbar is not None) else None),
                       n42_single_seed=(NR.n42_reading(d0, p0[fo]["sigma_fit_base"]) if p0 else None))
        if dbar is not None:
            P(f"  {fo:9s} Delta_bar {dbar:+.6f}  SD {sd:.6f}  SE {se:.6f}  (K = {n});  single-seed shift Delta_0 {d0:+.6f};  gamma_0 {g0:.4f} +- {p0[fo]['sigma_fit_base']:.4f}  ->  "
              f"seed-mean NSS-off entry {g0 + dbar:.6f}  (single-seed entry {g0 + d0:.6f});  N4.2 on Delta_bar: {res[fo]['n42_seed_mean']}")
    # K3, K4, K5, K6 of this run
    res["K3"] = p0.get("K3") if p0 else None
    if p0 and a.cut13 == "cones-literal" and p0["rung"].get("cut13_cones"):                 # AMENDMENT_A1 item 3: the bias bound of the rung's extract-fallback
        cc, cb = p0["rung"]["cut13_cones"], (p0.get("K3") or {})
        rate = (cc.get("n_flagged_cones", 0) / max(1, cc.get("n_covered", 1)))
        res["bias_bound"] = dict(rung_n_missing=cc.get("n_missing"), rung_n_covered=cc.get("n_covered"), fallback_flagged=cc.get("n_flagged_fallback"), cones_flag_rate=rate,
                                 expected_flagged_by_cones=rate * cc.get("n_missing", 0), policy=cc.get("missing_policy"))
        P(f"  bias bound (AMENDMENT_A1): rung k=0 has {cc.get('n_missing')} cut-13 pairs without a cone, policy {cc.get('missing_policy')}; fallback flagged {cc.get('n_flagged_fallback')}; "
          f"cones flag {cc.get('n_flagged_cones')} of {cc.get('n_covered')} ({rate:.2e}) -> ~{rate * cc.get('n_missing', 0):.2f} pair expected; measured by control C1 (dp7_C1.out)")
    k4 = [p["K4"] for p in parts]
    res["K4"] = dict(passed=all(x["base_equals_g50_build"] for x in k4 if x["g50_exists"]), n_with_g50=sum(x["g50_exists"] for x in k4), n_equal=sum(bool(x["base_equals_g50_build"]) for x in k4),
                     k_without_g50=[p["k"] for p in parts if not p["K4"]["g50_exists"]], k_unequal=[p["k"] for p in parts if p["K4"]["g50_exists"] and not p["K4"]["base_equals_g50_build"]])
    res["K6"] = dict(passed=not any(p["K6"]["flagged"] for p in parts), flagged_k=[p["k"] for p in parts if p["K6"]["flagged"]],
                     n_fits=sum(p["n_fits"] for p in parts), applies=(a.fit_path == "pipeline"))
    sh1 = frozen_now()
    res["K5"] = frozen_check(sh0, sh1)
    res["frozen_sha256"] = sh1
    if a.fit_path == "d2" and a.cut13 == "extract-builder":
        res["K1"] = k1_compare(parts)
        P(f"\nK1 (DP1 P4 bit for bit, k 1..8): {'PASS' if res['K1']['passed'] else 'FAIL'}  {res['K1']['n_bit_identical']}/{res['K1']['n_values']} values bit-identical; " +
          "; ".join(f"{fo} mean {res['K1']['means'][fo]['mean']:+.7f} vs DP1 {res['K1']['means'][fo]['dp1_mean']:+.7f} (exact {res['K1']['means'][fo]['mean_exact']}), SD {res['K1']['means'][fo]['sd']:.6f} vs {res['K1']['means'][fo]['dp1_sd']:.6f} (exact {res['K1']['means'][fo]['sd_exact']})" for fo in FOOTS))
        for r in res["K1"]["rows"]:
            if not r["bit_identical"]:
                P(f"   MISMATCH k={r['k']} {r['footing']} {r['quantity']}: dp7 {r['dp7']!r} vs dp1 {r['dp1']!r}")
    if a.fit_path == "pipeline" and a.cut13 == "extract-builder" and p0:
        res["K2"] = k2_compare(p0)
        P(f"\nK2 (registered fit at k = 0 reproduces DP1 P3 to 1e-4): {'PASS' if res['K2']['passed'] else 'FAIL'}  base sha registered {res['K2']['base_sha_is_registered']}, rung sha = DP1 rung {res['K2']['rung_sha_is_dp1_rung']}")
        for r in res["K2"]["rows"]:
            P(f"   {r['catalogue']:4s} {r['footing']:9s} {r['quantity']}: dp7 {r['dp7']:.4f} vs DP1 {r['dp1_P3']:.4f}  |diff| {r['abs_diff']:.2e}  {'ok' if r['within_1e4'] else 'MISMATCH'}")
    if res["K3"]:
        P(f"K3 (cones-literal k = 0 base = the dry run): {'PASS' if res['K3']['passed'] else 'FAIL'}  {res['K3']['n_pairs']} pairs, sha256 {res['K3']['sha256_prefix']} (ref {K3_REF['n_pairs']}, {K3_REF['sha256_prefix']}); bytes equal the dry-run csv on disk: {res['K3']['equals_dry_run_csv_on_disk']}")
    P(f"K4 (extract-builder base_k = G50 build on disk): {'PASS' if res['K4']['passed'] else 'FAIL'}  equal at {res['K4']['n_equal']} of {res['K4']['n_with_g50']} k with a G50 file; without a file: {res['K4']['k_without_g50']}; unequal: {res['K4']['k_unequal']}")
    P(f"K5 (frozen files unchanged): {'PASS' if res['K5']['passed'] else 'FAIL'}  {res['K5']['n_files']} files; changed during run {res['K5']['changed_during_run']}; off pinned value {res['K5']['off_pinned_value']}; pipeline {res['K5']['pipeline_sha256'][:8]}")
    P(f"K6 (pipeline self-test at the registered seed on every fitted catalogue): {'PASS' if res['K6']['passed'] else 'FAIL'}  {res['K6']['n_fits']} fits; flagged k {res['K6']['flagged_k']}" + ("" if res['K6']['applies'] else "  (d2 fit path: not applicable)"))
    # MUTATE readings
    if a.mutate_k0 and p0:
        # "exactly" is read at float precision (1e-12): the mean of K identical doubles and gamma_0 + (rung_0 - base_0) can differ from the
        # inputs by an ulp; the raw differences and the per-k bit identity to Delta_0 are recorded beside the reading.
        res["M1"] = {fo: dict(delta_bar_minus_single_seed=res[fo]["delta_bar"] - res[fo]["single_seed_shift"], delta_bar_equals_single_seed=(abs(res[fo]["delta_bar"] - res[fo]["single_seed_shift"]) <= 1e-12),
                              every_delta_k_bit_identical_to_delta_0=all(x == res[fo]["single_seed_shift"] for x in res[fo]["deltas"].values()),
                              sd=res[fo]["sd"], sd_is_zero=(abs(res[fo]["sd"]) <= 1e-12),
                              entry_minus_gamma_rung_0=res[fo]["seed_mean_entry"] - res[fo]["gamma_rung_0"], entry_equals_registered_single_seed=(abs(res[fo]["seed_mean_entry"] - res[fo]["gamma_rung_0"]) <= 1e-12)) for fo in FOOTS}
        res["M1"]["bites"] = all(v["delta_bar_equals_single_seed"] and v["sd_is_zero"] and v["entry_equals_registered_single_seed"] and v["every_delta_k_bit_identical_to_delta_0"] for v in res["M1"].values() if isinstance(v, dict))
        P(f"M1 (--mutate-k0): Delta_bar == single-seed shift and SD == 0 and entry == gamma_hat(rung_0) (at 1e-12; every Delta_k bit-identical to Delta_0) on both footings: {'BITES' if res['M1']['bites'] else 'DOES NOT BITE'}  " +
          "; ".join(f"{fo} Delta_bar {res[fo]['delta_bar']:+.6f} vs Delta_0 {res[fo]['single_seed_shift']:+.6f} (diff {res['M1'][fo]['delta_bar_minus_single_seed']:+.1e}), SD {res[fo]['sd']:.1e}, entry diff {res['M1'][fo]['entry_minus_gamma_rung_0']:+.1e}" for fo in FOOTS))
    if a.keep_nss:
        res["M2"] = {fo: dict(max_abs_delta=max(abs(x) for x in res[fo]["deltas"].values()) if res[fo]["deltas"] else None, delta_bar_within_1e9=(abs(res[fo]["delta_bar"]) <= 1e-9 if res[fo]["delta_bar"] is not None else False),
                              every_k_within_1e9=all(abs(x) <= 1e-9 for x in res[fo]["deltas"].values())) for fo in FOOTS}
        res["M2"]["rung_equals_base_bytes_every_k"] = all(p["rung_equals_base_bytes"] for p in parts)
        res["M2"]["bites"] = all(res["M2"][fo]["delta_bar_within_1e9"] and res["M2"][fo]["every_k_within_1e9"] for fo in FOOTS)
        P(f"M2 (--keep-nss): Delta_k == 0 within 1e-9 at every k, both footings: {'BITES' if res['M2']['bites'] else 'DOES NOT BITE'}  " +
          "; ".join(f"{fo} max |Delta_k| {res['M2'][fo]['max_abs_delta']:.1e}" for fo in FOOTS) + f"; rung bytes == base bytes at every k: {res['M2']['rung_equals_base_bytes_every_k']}")
    # cost
    fits = [p["fit"][x] for p in parts for x in ("base", "rung")]
    rss = [f["rss_gb"] for f in fits if f.get("rss_gb")]
    res["cost"] = dict(n_k=len(parts), builds=sum(p["n_builds"] for p in parts), fits=sum(p["n_fits"] for p in parts), fits_from_cache=sum(1 for f in fits if f.get("cached")),
                       wall_total_s=round(time.time() - t0, 1), wall_per_k_s=[p["wall_s"] for p in parts],
                       build_s_base=[p["base"]["build_s"] for p in parts], build_s_rung=[p["rung"]["build_s"] for p in parts],
                       fit_rss_gb_per_k=[[p["fit"]["base"]["rss_gb"], p["fit"]["rung"]["rss_gb"]] for p in parts], fit_rss_gb_max=(max(rss) if rss else None),
                       fit_wall_s=[f["wall_s"] for f in fits if f.get("wall_s")], wrapper_peak_rss_gb=round(rss_self_gb(), 3), omp_num_threads=os.environ.get("OMP_NUM_THREADS"), nice=os.nice(0))
    P(f"\ncost: {res['cost']['builds']} builds, {res['cost']['fits']} fits ({res['cost']['fits_from_cache']} from the sha-keyed cache), wall {res['cost']['wall_total_s']:.0f} s; fit peak RSS "
      f"{(res['cost']['fit_rss_gb_max'] or 0):.2f} GB (the registered pipeline's own --catalog run); wrapper peak RSS {res['cost']['wrapper_peak_rss_gb']:.2f} GB")
    P(f"{'COMPLETE' if done else 'INCOMPLETE'}: {len(parts)} of {a.K + 1} k  [{time.time() - t0:.0f} s]")
    (HERE / f"{a.out}.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    (HERE / f"{a.out}.out").write_text("\n".join(lines) + "\n")
    return 0 if done else 2


if __name__ == "__main__":
    sys.exit(main())
