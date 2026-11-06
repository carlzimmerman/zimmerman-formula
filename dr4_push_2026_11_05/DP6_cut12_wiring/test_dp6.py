#!/usr/bin/env python3
"""DP6 checks T0-T7 (criteria FROZEN_CRITERIA.md, ee74edfda2). Socket guard on; DR3 numbers are code-path tests only.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dr4_push_2026_11_05/DP6_cut12_wiring/test_dp6.py
     [MUTATE=1: screen off -> T3 FAILS;  MUTATE=2: every own-pair row exempt -> T2 FAILS]"""
import sys
sys.dont_write_bytecode = True
import hashlib, inspect, json, os, socket, subprocess, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PREP = REPO / "prep_2026" / "gaia_dr4_prep"
READY = PREP / "dr4_ready_1"
CFG816 = REPO / "campaign_fresh_gravity" / "CFG816_dr4_r_statistic_scoring"
DP1 = REPO / "dr4_push_2026_11_05" / "DP1_nss_off_rung"
DR3 = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract"
MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK = [], {}
T_START = time.time()
FROZEN = [PREP / "catalog_builder/build_catalog.py", READY / "dry_run_driver.py", READY / "cut12_nss_union.py",
          PREP / "catalog_builder_dr4/cut12_stub.py", CFG816 / "build_variant_catalogue.py", READY / "seed_sweep.py",
          PREP / "wide_binary_pipeline.py", DP1 / "nss_off_rung.py"]


def P(s=""):
    s = str(s).replace(str(REPO) + "/", "").replace(str(Path.home()), "<home>")
    print(s, flush=True); LOG.append(s)


def X(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def shas():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in FROZEN}


SHA0 = shas()
for p in (str(HERE), str(READY), str(CFG816), str(PREP), str(DP1)):
    sys.path.insert(0, p)
import dry_run_driver as D
D.init(False)                                                        # socket guard ON
import a17_cut12 as A
import cut12_nss_union as U
assert A.B is D.B, "the builder module seen by DP6 is not the driver's"
TMP = Path(tempfile.mkdtemp(prefix="dp6_"))
P("DP6 CHECKS (socket guard on)" + (f"   *** MUTATE={MUT} ***" if MUT else ""))
if MUT == "1":
    A._MUTATE = "screen_off"
if MUT == "2":
    U._MUTATE_A17 = "exempt_all"

# ---------------------------------------------------------------- T1 patch mechanics
orig = D.B.frozen_cuts
fake_man = {"cut12_nss": {"readings": {"A17_primary": {"counted_tables": ["x"]}}}}
pf = A.install(fake_man)
s0 = inspect.getsource(orig).splitlines(); s1 = inspect.getsource(pf).splitlines()
diff = [i for i, (x, y) in enumerate(zip(s0, s1)) if x != y]
A.uninstall()
X("T1 patched source differs from the frozen source in exactly one line; NSS cut line present once; getsource works; uninstall restores the original",
  len(s0) == len(s1) and len(diff) == 1 and "_DP6_NSS" in s1[diff[0]] and "\n".join(s1).count(A.CUT_LINE.strip()) == 1
  and D.B.frozen_cuts is orig, f"changed line {diff}: {s1[diff[0]].strip() if diff else None}")

# ---------------------------------------------------------------- T2 synthetic known answer
n_pair = 5
ids = np.arange(1, 2 * n_pair + 1, dtype=np.int64) + 4_000_000_000_000_000
S = dict(source_id=ids, ra=np.zeros(2 * n_pair) + 10.0, dec=np.repeat(np.arange(n_pair) * 1.0 + 40.0, 2),
         parallax=np.repeat(10.0 + 0.1 * np.arange(n_pair), 2),          # run 2: varies by pair (run 1 constant; make_pair_table refused it)
          parallax_error=np.full(2 * n_pair, 0.05) + 0.001 * np.arange(2 * n_pair),
         pmra=np.full(2 * n_pair, 50.0) + 0.01 * np.arange(2 * n_pair), pmdec=np.full(2 * n_pair, -20.0) + 0.02 * np.arange(2 * n_pair),
         pmra_error=np.full(2 * n_pair, 0.02) + 0.001 * np.arange(2 * n_pair), pmdec_error=np.full(2 * n_pair, 0.03) + 0.001 * np.arange(2 * n_pair),
         phot_g_mean_mag=np.full(2 * n_pair, 12.0) + 0.1 * np.arange(2 * n_pair), ruwe=1.0 + 0.01 * np.arange(2 * n_pair),
         ipd_frac_multi_peak=np.arange(2 * n_pair) % 3, radial_velocity=np.full(2 * n_pair, np.nan),
         radial_velocity_error=np.full(2 * n_pair, np.nan), l=np.zeros(2 * n_pair), b=np.full(2 * n_pair, 40.0))
S["dec"][1::2] += 100 / 3600.0                                       # 100 arcsec at 100 pc = 10 kAU
a, b = np.arange(0, 2 * n_pair, 2), np.arange(1, 2 * n_pair, 2)
R = np.full(n_pair, 0.001)
extra = {"third": np.zeros(n_pair, bool)}
S_col = dict(S, non_single_star=np.zeros(2 * n_pair, int))
base_keep, _, tab = orig(S_col, a, b, R, extra)
rp = np.array
one = TMP / "one_src.npz"
np.savez(one, source_id=np.array([ids[a[0]]], np.int64))
two = TMP / "nss_resolved_pair.npz"
np.savez(two, source_id=np.array([ids[a[1]], ids[b[2]], ids[a[3]]], np.int64),
         source_id_secondary=np.array([ids[b[1]], ids[a[2]], 4_100_000_000_000_000], np.int64),
         solution_type=np.array(["ResolvedPairFixed", "Orbital", "ResolvedPairFixed"]))
man2 = {"cut12_nss": {"id_files": {"one_src": str(one), "nss_resolved_pair": str(two)}, "two_source_tables": ["nss_resolved_pair"],
                      "solution_types_recorded": {"nss_resolved_pair": ["ResolvedPairFixed", "ResolvedPairLinear", "Orbital"]},
                      "excluded": {}, "diagnostic": {},
                      "readings": {"A17_primary": {"counted_tables": ["one_src", "nss_resolved_pair"],
                                                   "own_pair_exempt": {"nss_resolved_pair": ["ResolvedPairFixed", "ResolvedPairLinear"]}}}}}
truth_reject = np.array([True, False, True, True, False])
A.install(man2)
try:
    keep2, flow2, _ = D.B.frozen_cuts(S, a, b, R, extra)             # S has NO non_single_star column
finally:
    A.uninstall()
ref_flags, _ = U.run_a17(json.loads(json.dumps(man2)), ids[a], ids[b])
X("T2 synthetic: patched frozen_cuts keep = base keep & ~(run_a17 A17_primary) = hand truth (exempt own pair kept, non-exempt own pair, third-source, solution-on-star rejected, untouched kept)",
  bool(base_keep.all()) and np.array_equal(keep2, ~truth_reject) and np.array_equal(ref_flags["A17_primary"], truth_reject),
  f"base keep {base_keep.tolist()}; patched keep {keep2.tolist()}; run_a17 reject {ref_flags['A17_primary'].tolist()}; truth reject {truth_reject.tolist()}")

# T5b: the unpatched frozen function on the fake S without the column raises (O8 is real)
try:
    orig(S, a, b, R, extra); raised = False
except KeyError:
    raised = True

# ---------------------------------------------------------------- T6 refusals + T7 per-star file
r1 = r2 = False
try:
    A.install(man2, reading="nope")
except KeyError:
    r1 = True
A.uninstall()
A.install({"cut12_nss": {"id_files": {}}})
try:
    D.B.frozen_cuts(S, a, b, R, extra)
except ValueError:
    r2 = True
A.uninstall()
A.install(man2); A.install(man2); idem = D.B.frozen_cuts is not orig and A._STATE["original"] is orig; A.uninstall()
X("T6 refusals: undeclared reading refuses at install; no readings refuses at the first call (run_a17's rule); install twice idempotent",
  r1 and r2 and idem and D.B.frozen_cuts is orig, f"undeclared {r1}, no readings {r2}, idempotent {idem}")

sa = TMP / "stage_A_fake.npz"; np.savez(sa, **S)
ps = A.write_per_star(sa, TMP / "per_star.npz")
z0, z1 = np.load(sa), np.load(ps)
same = all(np.array_equal(z0[k], z1[k], equal_nan=z0[k].dtype.kind == "f") and z0[k].dtype == z1[k].dtype for k in z0.files)
import make_pair_table as MPT
cat = {k: np.asarray(v) for k, v in tab.items()}
try:
    out7, rep7 = MPT.build(cat, z1, declare_neutral=("non_single_star",)); ok7 = rep7["n_pairs"] == n_pair and np.all(out7["nss1"] == 0)
except SystemExit as e:
    ok7, rep7 = False, str(e)
X("T7 per-star file: stage-A columns preserved, non_single_star all 0, accepted by make_pair_table with --declare-neutral non_single_star",
  same and set(z1.files) == set(z0.files) | {"non_single_star"} and not z1["non_single_star"].any() and ok7, f"{rep7}")

# ---------------------------------------------------------------- T3 DR3 equivalence, column removed
za = np.load(DR3 / "stage_A.npz")
proxy = TMP / "dr3_nss_proxy.npz"
np.savez(proxy, source_id=np.asarray(za["source_id"][za["non_single_star"] > 0], np.int64))
n_proxy = int((za["non_single_star"] > 0).sum()); del za
man3 = {"cut12_nss": {"id_files": {"dr3_nss_proxy": str(proxy)}, "two_source_tables": [], "excluded": {}, "diagnostic": {},
                      "readings": {"A17_primary": {"counted_tables": ["dr3_nss_proxy"]}}}}
man3_path = TMP / "a17_manifest_dr3.json"; man3_path.write_text(json.dumps(man3))
orig_amc = D.apply_manifest_columns


def strip_amc(S_, m_, r_):
    S_ = dict(orig_amc(S_, m_, r_)); S_.pop("non_single_star"); return S_


D.apply_manifest_columns = strip_amc
A.install(man3)
t0 = time.time()
try:
    csv3, rep3 = D.run("dr3", "primary", "extract-builder", None, False)
    rep_a17 = A.last_report()
finally:
    A.uninstall()
X("T3 DR3 equivalence (per-star column REMOVED from S; cut 12 from a one-table A17 manifest): 6,210 pairs, sha 6fff64d964ebaa72",
  rep3["n_pairs"] == 6210 and rep3["sha256"].startswith("6fff64d964ebaa72"),
  f"{rep3['n_pairs']:,d} pairs, sha {rep3['sha256'][:16]}; proxy ids {n_proxy:,d}; A17 rejected {rep_a17['n_rejected']:,d} of {rep_a17['n_pairs']:,d} stage-F pairs [{time.time() - t0:.0f} s]")

# ---------------------------------------------------------------- T4 DP1 rung composes
import nss_off_rung as RG
A.install(man3)
t0 = time.time()
try:
    csv4, rep4 = RG.rung_build(True, 30, "dr3", "primary", "extract-builder", None, False)
finally:
    A.uninstall(); D.apply_manifest_columns = orig_amc
X("T4 DP1 rung on the patched builder (column removed): 6,282 pairs, sha 1dbdf21a",
  rep4["n_pairs"] == 6282 and rep4["sha256"].startswith("1dbdf21a"), f"{rep4['n_pairs']:,d} pairs, sha {rep4['sha256'][:16]} [{time.time() - t0:.0f} s]")

# ---------------------------------------------------------------- T5 launcher (subprocess) + T5b
out5 = TMP / "launcher_dr3.csv"
t0 = time.time()
cmd = [sys.executable, "-B", str(HERE / "dp6_with_a17.py"), "--a17-manifest", str(man3_path), "--report-json", str(TMP / "rep5.json"),
       "--", str(READY / "dry_run_driver.py"), "--release", "dr3", "--cut13", "extract-builder", "--out-csv", str(out5)]
env = dict(os.environ, OMP_NUM_THREADS="1", **({"DP6_MUTATE": MUT} if MUT else {}))
r5 = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO), env=env)
sha5 = hashlib.sha256(out5.read_bytes()).hexdigest() if out5.exists() else None
rep5 = json.loads((TMP / "rep5.json").read_text()) if (TMP / "rep5.json").exists() else {}
active5 = bool(rep5.get("report")) and rep5["report"]["n_rejected"] > 0
X("T5 launcher subprocess (dry_run_driver.py as __main__) writes the T3 CSV, with the A17 screen active in that process; T5b the unpatched frozen_cuts raises KeyError without the column",
  r5.returncode == 0 and sha5 is not None and sha5.startswith("6fff64d964ebaa72") and active5 and raised,
  f"exit {r5.returncode}; sha {sha5[:16] if sha5 else None}; A17 report in subprocess: rejected {rep5.get('report', {}) and rep5['report']['n_rejected']}; T5b raised {raised} [{time.time() - t0:.0f} s]"
  + (f"\n         stderr tail: {r5.stderr[-400:]}" if r5.returncode else ""))

# ---------------------------------------------------------------- T0 frozen files
SHA1 = shas()
X("T0 frozen files unchanged (sha256 before = after)", SHA0 == SHA1, ", ".join(f"{k} {v[:12]}" for k, v in SHA1.items()))

P(f"\nchecks: {sum(CHK.values())} of {len(CHK)} pass  ({time.time() - T_START:.0f} s)")
if MUT:
    exp = {"1": "T3", "2": "T2"}[MUT]
    P(f"[MUTATE CONTROL] MUTATE={MUT}: {exp} {'FAILED as designed' if not CHK[exp] else 'did NOT fail: the control does not bite'}")
(HERE / f"test_dp6{SFX}.out").write_text("\n".join(LOG) + "\n")
(HERE / f"test_dp6{SFX}.json").write_text(json.dumps(dict(checks=CHK, mutate=MUT or None, frozen_sha256=SHA1), indent=1) + "\n")
sys.exit((0 if not CHK[{"1": "T3", "2": "T2"}[MUT]] else 1) if MUT else (0 if all(CHK.values()) else 1))
