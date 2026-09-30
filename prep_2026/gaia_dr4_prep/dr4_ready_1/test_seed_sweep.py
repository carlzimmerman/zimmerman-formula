#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 tooling: the controls C1-C11 of SEED_SWEEP_DESIGN_FROZEN.md (be8a6405d) for seeded_build.py, the driver's --seed-offset / --stage-dir and seed_sweep.py (NEW file).
OFFLINE (socket guard in this process; the pipeline and sweep runs are subprocesses that never touch the network).  DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_seed_sweep.py             (quick: C1, C3-C10; about 10 min)
      FULL=1 python3 .../test_seed_sweep.py                                        (adds C2, the E/F rebuild at N_SHIFT = 30 against the builder's own stage_E/F, about 15 min, and C11, the full-path smoke at N_SHIFT = 3)
      MUTATE=1 / MUTATE=2: plant a fault (E-shift stride +k instead of +100k; the G seed taken from a patched B.SEED instead of passed explicitly) -- the checks must FAIL (outputs *_MUTATE*)."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, shutil, subprocess, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
MUT = os.environ.pop("MUTATE", "").strip()
FULL = os.environ.pop("FULL", "").strip() == "1"
SFX = f"_MUTATE{MUT}" if MUT else ""
import dry_run_driver as D
import seeded_build as SB
D.init(False)
B = SB.import_builder()
LOG, RES = [], {}
T0 = time.time()
REF_SHA = "6fff64d964ebaa72"


def P(s=""):
    print(s, flush=True); LOG.append(s)


def K(name, ok, detail=""):
    RES[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def run_cmd(args, env=None, timeout=3600):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    e.update(env or {})
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=str(REPO), env=e)
    return r


ext = D.extract_dir("dr3", "primary")
P("SEED SWEEP TOOLING: controls C1-C11 (DR3 numbers are code-path tests, never results)" + (f"; MUTATE = {MUT}" if MUT else "") + ("; FULL" if FULL else ""))

# ---------------------------------------------------------------- C1 byte identity at k = 0
b0, r0 = D.run("dr3", "primary", "extract-builder", None, False)
b1, r1 = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=0, stage_dir=None)
st = run_cmd([sys.executable, "-B", str(HERE / "dry_run_driver.py"), "--self-test"])
K("C1 the driver with no new option and with --seed-offset 0 reproduces the reference DR3 CSV byte for byte, and its own self-test (S0-S6) still passes",
  r0["sha256"].startswith(REF_SHA) and b0 == b1 and "7/7 pass -> ALL PASS" in st.stdout and "seed_offset" not in r0,
  f"sha256 {r0['sha256'][:16]}; the default report carries no new key; self-test: {st.stdout.strip().splitlines()[-1] if st.stdout.strip() else st.stderr[-100:]}")

# ---------------------------------------------------------------- C3 seed sets
if MUT == "1":
    SB.E_SHIFT_STRIDE = 1                                                                # the planted fault: +k instead of +100 k
n_seeds, n_dup = SB.seed_sets_disjoint(range(11), 30, 400)
sites = SB.scan_random_sites()
tmpd = Path(tempfile.mkdtemp())
fake = tmpd / "build_catalog_fake.py"
fake.write_text(SB.BUILDER_PATH.read_text() + "\n_extra = np.random.default_rng(5)\n")
sites_fake = SB.scan_random_sites(fake)
K("C3 the per-block stage-E seeds of builds 0..10 (N_SHIFT 30, 400 blocks) are all distinct; the builder has exactly the four known random-draw sites and the scan catches a planted fifth",
  n_dup == 0 and len(sites["default_rng"]) == 4 and len(sites["seed=r + 1"]) == 1 and not sites["other"] and len(sites_fake["default_rng"]) == 5,
  f"{n_seeds:,d} seeds, {n_dup:,d} duplicates; default_rng sites at lines {[x[0] for x in sites['default_rng']]}; seed=r + 1 at {[x[0] for x in sites['seed=r + 1']]}; planted fifth site found: {len(sites_fake['default_rng']) == 5}")

# ---------------------------------------------------------------- C4 the G seed is explicit
S = dict(np.load(ext / "stage_A.npz"))
F = dict(np.load(ext / "stage_F.npz"))
n = 300
a, b, th = F["a"][:n], F["b"][:n], F["th"][:n]
ids = np.concatenate([S["source_id"][a], S["source_id"][b]])
note = []
corr = D.offline_correlations(ext, "primary", note)("dr3", ids, None)
g_default = np.asarray(B.vt_error_mc(S, a, b, th, corr))
g_explicit0 = np.asarray(B.vt_error_mc(S, a, b, th, corr, seed=B.SEED))
g_k1 = np.asarray(B.vt_error_mc(S, a, b, th, corr, seed=B.SEED + 1))
SEED0 = B.SEED
B.SEED = SEED0 + 1
g_patched = np.asarray(B.vt_error_mc(S, a, b, th, corr))                                  # the pitfall: a patched module SEED does NOT reach the default argument
B.SEED = SEED0
if MUT == "2":
    g_k1 = g_patched                                                                      # the planted fault: build k's G seed taken from the patched SEED
K("C4 vt_error_mc with seed = SEED equals the default call, seed = SEED + 1 differs from it, and patching build_catalog.SEED alone does NOT change the default-seeded output (so G's seed must be passed explicitly)",
  np.array_equal(g_default, g_explicit0) and not np.array_equal(g_default, g_k1) and np.array_equal(g_default, g_patched),
  f"{n} pairs: seed SEED == default {np.array_equal(g_default, g_explicit0)}; SEED + 1 differs {not np.array_equal(g_default, g_k1)} (max |diff| {np.max(np.abs(g_default - g_k1)):.3g}); patched SEED unchanged {np.array_equal(g_default, g_patched)}")

# ---------------------------------------------------------------- C5 hash guard
h_before = SB.assert_builder_frozen("test, before")
planted = tmpd / "build_catalog_planted.py"
txt = SB.BUILDER_PATH.read_text()
planted.write_text(txt.replace("N_SHIFT = 30", "N_SHIFT = 31", 1))
try:
    SB.assert_builder_frozen("planted", path=planted)
    raised = False
except RuntimeError:
    raised = True
h_after = SB.assert_builder_frozen("test, after")
K("C5 the builder's sha256 equals the frozen value before and after, and a planted one-character edit of a temporary copy makes the guard raise", h_before == h_after == SB.FROZEN_BUILDER_SHA256 and raised,
  f"{h_before[:16]} == {h_after[:16]}; planted edit raises: {raised}")

# ---------------------------------------------------------------- C6 cache paths; delta fetch
paths = [D.corr_cache_path_k(ext, "primary", k) for k in range(11)]
shared = {ext / "stage_G_corr.npz", ext / "stage_G_corr_elbadry.npz"}
K("C6 build caches: k = 0 is the driver's current per-variant path, k = 1..10 are ten distinct files in seed_k<k>/, none equal to the builder's shared caches",
  paths[0] == D.corr_cache_path(ext, "primary") and len(set(paths)) == 11 and not (set(paths) & shared) and all(paths[k].parent.name == f"seed_k{k}" for k in range(1, 11)),
  f"{paths[0].name}; {paths[1].parent.name}/{paths[1].name} ... {paths[10].parent.name}/{paths[10].name}")
prime, cache = tmpd / "prime.npz", tmpd / "sub" / "k1.npz"
ids1 = np.arange(1001, 1101)
np.savez(prime, source_id=ids1, parallax_pmra_corr=ids1 * 1e-4, parallax_pmdec_corr=-ids1 * 1e-4)
h_prime = hashlib.sha256(prime.read_bytes()).hexdigest()
calls = []


def fake_query(release, ids):
    calls.append(np.array(ids))
    return {"source_id": np.asarray(ids), "parallax_pmra_corr": np.asarray(ids) * 1e-4, "parallax_pmdec_corr": -np.asarray(ids) * 1e-4}


out = D.fetch_correlations_delta("dr3", np.arange(1001, 1151), cache, prime_from=prime, query_fn=fake_query)
out2 = D.fetch_correlations_delta("dr3", np.arange(1001, 1151), cache, prime_from=prime, query_fn=fake_query)
K("C6b the delta fetch queries only the ids its cache (primed from the primary's file, read-only) lacks, merges into the build's own file, leaves the primary's file byte-identical, and a repeat queries nothing",
  len(calls) == 1 and np.array_equal(np.sort(calls[0]), np.arange(1101, 1151)) and len(np.unique(out["source_id"])) == 150 and hashlib.sha256(prime.read_bytes()).hexdigest() == h_prime and len(out2["source_id"]) == 150,
  f"queried {len(calls[0]) if calls else 0} ids (expected 50); merged {len(np.unique(out['source_id']))} unique; primary file unchanged; repeat queries: {len(calls) - 1}")

# ---------------------------------------------------------------- C7, C8 the fit through the pipeline's own CLI
import seed_sweep as SS
ref_csv = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract" / "wide_binaries_dr3.csv"
f1 = SS.fit_via_pipeline_cli(ref_csv, 20261216)
f2 = SS.fit_via_pipeline_cli(ref_csv, 20261216)
f3 = SS.fit_via_pipeline_cli(ref_csv, 20261217)
EXP = {"canonical": (1.0750, 0.0550, 1.0232), "alt": (1.0775, 0.0512, 1.0247)}
ok7 = all(abs(f1[f]["g"] - EXP[f][0]) < 5e-5 and abs(f1[f]["s"] - EXP[f][1]) < 5e-5 and abs(f1[f]["kappa"] - EXP[f][2]) < 5e-5 for f in EXP)
try:
    SS.parse_pipeline_stdout("  catalog [a0 canonical]             gamma_inf = 1.0750 +- 0.0550  (chi2/bin=2.13, bins=6, kappa=1.0232)\n")
    raised_p = False
except ValueError:
    raised_p = True
K("C7 the parser reproduces gamma-hat, sigma_fit and kappa of both footings for the reference DR3 CSV (canonical 1.0750 / 0.0550 / 1.0232; alt 1.0775 / 0.0512 / 1.0247) and raises when a footing line is missing",
  ok7 and raised_p, f"canonical {f1['canonical']['g']:.4f} / {f1['canonical']['s']:.4f} / {f1['canonical']['kappa']:.4f}; alt {f1['alt']['g']:.4f} / {f1['alt']['s']:.4f} / {f1['alt']['kappa']:.4f}; missing line raises: {raised_p}; risk lines {len(f1['risk_lines'])}")
same = all(f1[f] == f2[f] for f in EXP) and f1["stdout_sha256"] == f2["stdout_sha256"]
diff = any(f1[f]["g"] != f3[f]["g"] or f1[f]["s"] != f3[f]["s"] for f in EXP)
K("C8 two pipeline runs on one CSV with one seed give identical output; a run with --seed 20261217 differs (the forward model and the bootstrap are live)", same and diff,
  f"identical: {same}; seed 20261217: canonical {f3['canonical']['g']:.4f} +- {f3['canonical']['s']:.4f}, alt {f3['alt']['g']:.4f} +- {f3['alt']['s']:.4f}")

# ---------------------------------------------------------------- C15 the pipeline's exit code is its own self-test, not a crash
ok_txt = ("  catalog [a0 canonical]             gamma_inf = 1.0750 +- 0.0550  (chi2/bin=2.13, bins=6, kappa=1.0232)\n  catalog [a0 alt footing]           gamma_inf = 1.0775 +- 0.0512  (chi2/bin=1.85, bins=6, kappa=1.0247)\n")
i0 = SS.interpret_pipeline_run(0, ok_txt + "PIPELINE SELF-TEST: PASS (x)\n")
i1 = SS.interpret_pipeline_run(1, ok_txt + "PIPELINE SELF-TEST: FAIL (x)\n")
def _raises(fn, exc):
    try:
        fn(); return False
    except exc:
        return True
r_a = _raises(lambda: SS.interpret_pipeline_run(1, "PIPELINE SELF-TEST: FAIL (x)\n"), ValueError)
r_b = _raises(lambda: SS.interpret_pipeline_run(2, ok_txt), RuntimeError)
r_c = _raises(lambda: SS.interpret_pipeline_run(1, ok_txt + "PIPELINE SELF-TEST: PASS (x)\n"), RuntimeError)
f_real = SS.fit_via_pipeline_cli(ref_csv, 20261228)                                      # a REAL seed whose own self-test FAILS (exit 1, both footing lines printed)
if MUT == "4":
    i1["self_test_passed"] = True                                                        # (a planted misread must fail the check)
K("C15 interpret_pipeline_run: exit 0 + PASS accepted (self_test_passed True); exit 1 + FAIL + both footing lines accepted (False); exit 1 without footing lines, exit 2, and an exit code that disagrees with the printed line all raise; the REAL output of seed 20261228 (its own self-test FAILS, exit 1) is accepted and flagged",
  i0["self_test_passed"] is True and i1["self_test_passed"] is False and r_a and r_b and r_c and f_real["self_test_passed"] is False and set(("canonical", "alt")) <= set(f_real) and f_real["self_test_line"].startswith("PIPELINE SELF-TEST: FAIL"),
  f"synthetic: pass {i0['self_test_passed']}, fail {i1['self_test_passed']}; raises: no footing lines {r_a}, exit 2 {r_b}, disagreement {r_c}; real seed 20261228: {f_real['self_test_line'][:45]}, canonical {f_real['canonical']['g']:.4f} +- {f_real['canonical']['s']:.4f}, alt {f_real['alt']['g']:.4f} +- {f_real['alt']['s']:.4f}")

# ---------------------------------------------------------------- C9 MUTATE (identical seeds -> sigma_build = 0) and the un-mutated sweep; C10 manifest
sweep = HERE / "seed_sweep.py"
out_dir = ext / "seed_sweep"
r_mut = run_cmd([sys.executable, "-B", str(sweep), "--release", "dr3", "--K", "2", "--mode", "g-only", "--fit", "--tag", "test"], env={"MUTATE": "1"})
mm = json.load(open(out_dir / "seed_sweep_manifest_test_MUTATE.json"))
shas = {b["csv_sha256"] for b in mm["builds"]}
sbm = mm["sigma_build"]
K("C9 MUTATE: K + 1 = 3 builds all run with the IDENTICAL seed set: one final-CSV sha256, zero pair flips, and sigma_build = 0 exactly on both footings",
  len(shas) == 1 and mm["flips_vs_k0"] == [[0, 0], [0, 0]] and sbm["canonical"]["sigma_build"] == 0.0 and sbm["alt"]["sigma_build"] == 0.0,
  f"{len(shas)} distinct sha256; flips {mm['flips_vs_k0']}; sigma_build canonical {sbm['canonical']['sigma_build']}, alt {sbm['alt']['sigma_build']}; gammas {sbm['canonical']['gammas']}")
r_real = run_cmd([sys.executable, "-B", str(sweep), "--release", "dr3", "--K", "2", "--mode", "g-only", "--fit", "--tag", "test"])
mr = json.load(open(out_dir / "seed_sweep_manifest_test.json"))
planted_ok = all(mr["plan"]["seed_sets"][k]["stage_G_velocity_mc"] == B.SEED + k and mr["plan"]["seed_sets"][k]["stage_E_shift_seeds"][0] == 1 + 100 * k for k in range(3))
shas_r = [b["csv_sha256"] for b in mr["builds"]]
direct = [(len(SS.pair_set(REPO / mr["builds"][0]["csv"]) - SS.pair_set(REPO / b["csv"])), len(SS.pair_set(REPO / b["csv"]) - SS.pair_set(REPO / mr["builds"][0]["csv"]))) for b in mr["builds"][1:]]
K("C9b the un-mutated stage-G-only sweep (k = 0, 1, 2): the seed sets are the declared ones, the flips equal a direct set comparison; the per-build sha256 list and sigma_build are reported (stage-G-only builds may flip few or no pairs: a code-path number, NOT the WP2-gamma quantity)",
  planted_ok and [tuple(x) for x in mr["flips_vs_k0"]] == direct and "sigma_build" in mr,
  f"seed sets ok {planted_ok}; sha256 prefixes {[s[:8] for s in shas_r]}; flips {mr['flips_vs_k0']} (direct {direct}); uncovered ids {[b['uncovered_corr_ids'] for b in mr['builds']]}; sigma_build canonical {mr['sigma_build']['canonical']['sigma_build']:.4f}, alt {mr['sigma_build']['alt']['sigma_build']:.4f}")
pl = out_dir / "seed_sweep_planned_test.json"
first_csv = REPO / mr["builds"][0]["csv"]
need = {"csv_sha256", "n_pairs", "uncovered_corr_ids", "fit", "correlation_cache"}
g_c = [b["fit"]["canonical"]["g"] for b in mr["builds"]]
K("C10 manifest: the seed list was written BEFORE the first build's CSV; afterwards the builder hash before/after equals the frozen value, and every build carries sha256, pair count, uncovered-correlation count, gamma-hat, sigma_fit and kappa; sigma_build is the SD with ddof = 1",
  pl.exists() and json.load(open(pl))["status"] == "planned" and pl.stat().st_mtime < first_csv.stat().st_mtime and mr["plan"]["builder_sha256"] == mr["builder_sha256_after"] == SB.FROZEN_BUILDER_SHA256
  and all(need <= set(b) for b in mr["builds"]) and abs(mr["sigma_build"]["canonical"]["sigma_build"] - float(np.std(g_c, ddof=1))) < 1e-15,
  f"planned file mtime < first csv mtime: {pl.stat().st_mtime < first_csv.stat().st_mtime}; sigma_build recomputed {np.std(g_c, ddof=1):.6f}")

# ---------------------------------------------------------------- C12 driver fidelity against WP2-gamma's own ten builds
eqs, unc = [], []
for k in range(10):
    wd = ext / f"wp2_gamma_{k}"
    bk, rk = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=(k + 1 if MUT == "2" else k), stage_dir=wd)       # MUTATE=2: a wrong G seed (k + 1) must break the byte identity
    eqs.append(hashlib.sha256(bk).hexdigest() == hashlib.sha256((wd / "final.csv").read_bytes()).hexdigest())
    unc.append(rk["correlations"][0]["n_uncovered"])
K("C12 the driver with --seed-offset k --stage-dir wp2_gamma_k reproduces WP2-gamma's own final.csv BYTE FOR BYTE for k = 0..9 (an independent implementation of the same seed sets); the per-build uncovered-correlation count is recorded",
  all(eqs), f"identical for k = {[k for k in range(10) if eqs[k]]}; uncovered correlation ids per build {unc}")
RES_EXTRA = dict(uncovered_correlation_ids_wp2_gamma_builds=unc)

# ---------------------------------------------------------------- C13 ladder post-filter rungs against independent direct counts
import csv as _csv
refp = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract" / "wide_binaries_dr3.csv"
head_, rungs_ = SS.ladder_rungs(refp, ext / "stage_A.npz")
rows_ = list(_csv.DictReader(open(refp)))
zA = np.load(ext / "stage_A.npz")
ruwe_of = dict(zip(zA["source_id"].tolist(), zA["ruwe"].tolist()))
nR = sum(float(r["R_chance"]) < 0.001 for r in rows_)
nS = sum(3.0 < float(r["sep_kAU"]) < 20.0 for r in rows_)
nW = sum(ruwe_of[int(r["source_id1"])] < 1.2 and ruwe_of[int(r["source_id2"])] < 1.2 for r in rows_)
_, rungs_planted = SS.ladder_rungs(refp, ext / "stage_A.npz", ruwe_max=1.25)
if MUT == "3":
    nW += 1                                                                               # (a planted miscount must fail the check)
K("C13 the ladder post-filter rungs (R_chance < 0.001; separation 3-20 kAU; RUWE < 1.2 on both components) have the pair counts of independent direct counts on the reference CSV, and a planted wrong RUWE threshold changes the count",
  len(rungs_["R_chance<0.001"]) == nR and len(rungs_["sep 3-20 kAU"]) == nS and len(rungs_["RUWE<1.2 both"]) == nW and len(rungs_planted["RUWE<1.25 both"]) > len(rungs_["RUWE<1.2 both"]),
  f"counts {len(rungs_['R_chance<0.001'])} / {len(rungs_['sep 3-20 kAU'])} / {len(rungs_['RUWE<1.2 both'])} (direct {nR} / {nS} / {nW}) of {len(rows_):,d}; RUWE < 1.25 gives {len(rungs_planted['RUWE<1.25 both'])}")

# ---------------------------------------------------------------- C14 the committed seed list
sl = json.load(open(HERE / "seed_sets_dr4.json"))
K("C14 seed_sets_dr4.json (committed before DR4) equals the seed list the code produces (full E-G rebuilds k = 0..10 and the G-only seeds SEED + k for k = 1..100), carries the frozen builder hash, and its G-only seeds equal the G seeds of the full-rebuild seed sets for k = 1..10",
  sl == json.loads(json.dumps(SB.seed_list(10, None, B, 100))) and sl["builder_sha256"] == SB.FROZEN_BUILDER_SHA256 and sl["K"] == 10 and sl["K_G"] == 100 and all(sl["g_only_stage_G_seeds"][k - 1] == sl["seed_sets"][k]["stage_G_velocity_mc"] for k in range(1, 11)),
  f"{len(sl['seed_sets'])} full-rebuild seed sets; {len(sl['g_only_stage_G_seeds'])} G-only seeds ({sl['g_only_stage_G_seeds'][0]} ... {sl['g_only_stage_G_seeds'][-1]}); builder {sl['builder_sha256'][:16]}; fit seed {sl['fit_seed']}; control seeds {sl['fit_only_control_seeds'][:3]} ...")

# ---------------------------------------------------------------- C2, C2b, C11 (FULL)
if FULL:
    work = tmpd / "k0_rebuild"
    E_, F_, sec = SB.rebuild_EF(ext, work, 0, None)
    E_ref, F_ref = dict(np.load(ext / "stage_E.npz")), dict(np.load(ext / "stage_F.npz"))
    eq = lambda X, Y: set(X) == set(Y) and all(np.array_equal(X[k], Y[k]) for k in X)
    K("C2 rebuild_EF(k = 0) at the builder's N_SHIFT = 30 reproduces dr3_extract/stage_E.npz and stage_F.npz exactly (every key)", eq(E_, E_ref) and eq(F_, F_ref),
      f"E keys {len(E_)} equal {eq(E_, E_ref)}; F keys {sorted(F_)} equal {eq(F_, F_ref)}; {sec:.0f} s")
    E1, F1, sec1 = SB.rebuild_EF(ext, tmpd / "k1_rebuild", 1, None)
    E1r, F1r = dict(np.load(ext / "wp2_gamma_1" / "stage_E.npz")), dict(np.load(ext / "wp2_gamma_1" / "stage_F.npz"))
    K("C2b rebuild_EF(k = 1) at N_SHIFT = 30 reproduces WP2-gamma's own wp2_gamma_1/stage_E.npz and stage_F.npz exactly (every key): the seeds r + 1 + 100 k and SEED + k are the ones WP2-gamma used", eq(E1, E1r) and eq(F1, F1r),
      f"E equal {eq(E1, E1r)}; F equal {eq(F1, F1r)}; {sec1:.0f} s")
    r_full = run_cmd([sys.executable, "-B", str(sweep), "--release", "dr3", "--K", "1", "--mode", "full", "--n-shift", "3", "--rebuild-k0", "--fit", "--tag", "smoke_n3"])
    mf = json.load(open(out_dir / "seed_sweep_manifest_smoke_n3.json"))
    K("C11 full-path smoke at N_SHIFT = 3 (k = 0 and k = 1 both rebuilt through E, F and G, fitted by the pipeline CLI; the builder hash holds): k = 1 differs from k = 0, both fits parse",
      r_full.returncode == 0 and mf["builds"][0]["csv_sha256"] != mf["builds"][1]["csv_sha256"] and sum(mf["flips_vs_k0"][0]) > 0 and mf["builder_sha256_after"] == SB.FROZEN_BUILDER_SHA256 and all("fit" in b for b in mf["builds"]),
      f"pairs {[b['n_pairs'] for b in mf['builds']]}; flips {mf['flips_vs_k0']}; sigma_build canonical {mf['sigma_build']['canonical']['sigma_build']:.4f} (2 builds: a code-path number); E/F seconds {[b['seconds_EF'] for b in mf['builds']]}")
else:
    P("  [not run here] C2 (E/F rebuild fidelity at N_SHIFT = 30, about 15 min) and C11 (full-path smoke at N_SHIFT = 3): FULL=1")
shutil.rmtree(tmpd, ignore_errors=True)
ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / f"test_seed_sweep{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"test_seed_sweep_results{SFX}.json").write_text(json.dumps(dict(results=RES, full=FULL, mutate=MUT, seconds=round(time.time() - T0, 1), **RES_EXTRA), indent=1) + "\n")
sys.exit(0 if ok else 1)
