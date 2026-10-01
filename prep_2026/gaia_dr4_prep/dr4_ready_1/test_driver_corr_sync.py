#!/usr/bin/env python3
"""DR4-READY-1, item 2 of DR4_Q1_TOOLING_DESIGN_FROZEN.md (6742d206d): OFFLINE equivalence test of the driver's SYNC fallback for stage G's correlation fetch against the frozen builder's async fetch and the on-disk cache (NEW file; NO NETWORK).
The mock archive answers the builder's `launch_job_async` and the driver's `launch_job` from the on-disk DR3 correlation caches (which the builder's own async fetch wrote), in a SHUFFLED order, with the caches' dtypes (int64, float32), and applies the synchronous
endpoint's SILENT 2,000-row cap to sync answers.  astroquery's Gaia object is patched, and the driver's socket guard (installed by D.init(False)) stays, so any leak to the real network raises.
Checks (PASS / FAIL; DR3 numbers are code-path tests, never results):
  S1  the reference run (cache only) reproduces the DR3 CSV (sha256 prefix 6fff64d964ebaa72)
  S2  the run with the BUILDER's async fetch (mock server, empty temporary cache) gives a byte-identical stage-G CSV and a cache equal to the truth at the requested ids
  S3  the run with the SYNC fallback (same) completes, gives the same CSV, and its cache arrays, sorted by source_id, are BYTE-IDENTICAL to the async run's (same dtypes) and equal to the truth
  S4  every sync call carried at most 1,999 ids and the number of calls is ceil(n / 1999); the async run used the builder's 2,000-id chunks
  S5  the SELECT texts of the two transports are identical up to the id list
  S6  the sync run's report records the transport (calls, ids, largest chunk); the reference and async reports carry no such key
  S7  a seed-sweep build (seed offset 1) with a PARTIAL primary cache fetches ONLY the missing ids through the sync query (one call) and gives the same CSV as the offline seed build
  S8  the driver's own self-test still passes 7/7 and --corr-transport sync without --allow-network is refused
MUTATE=1: sync chunks of 2,000 ids (S4 must FAIL).  =2: the last row of every sync answer dropped (the completeness guard stops the run: S3 must FAIL).  =3: the correlations cast to float64 (the byte-identity in S3 must FAIL).  =4: the two correlation columns swapped in the sync answers (S3 must FAIL).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_driver_corr_sync.py"""
import sys
sys.dont_write_bytecode = True
import json, math, os, re, subprocess, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import dry_run_driver as D
D.init(False)                                                                       # the socket guard stays
from astropy.table import Table
import types
# NOTE: importing the REAL astroquery.gaia opens a connection (GaiaClass.__init__ calls get_status_messages: an HTTP GET to the archive; it is also where the 'archive is in evolution' banner comes from), which the
# guard blocks.  The test therefore installs a FAKE astroquery.gaia module BEFORE anything imports the real one; the builder's fetch_correlations and the driver's sync fallback both do `from astroquery.gaia import Gaia` inside the call.

MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK = [], {}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def C(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


P("DRIVER SYNC FALLBACK FOR STAGE G'S CORRELATION FETCH: offline equivalence test (DR3 code-path numbers)" + (f"   *** MUTATE={MUT}: " + {"1": "sync chunks of 2,000 ids (S4 must FAIL)", "2": "the last row of every sync answer dropped (S3 must FAIL)", "3": "correlations cast to float64 (S3 must FAIL)", "4": "the correlation columns swapped (S3 must FAIL)"}[MUT] + " ***" if MUT else ""))
ext = D.extract_dir("dr3", "primary")
zs = [np.load(ext / f) for f in ("stage_G_corr.npz", "stage_G_corr_elbadry.npz")]
sid = np.concatenate([z["source_id"] for z in zs])
u, first = np.unique(sid, return_index=True)
TRUTH = {c: np.concatenate([z[c] for z in zs])[first] for c in ("parallax_pmra_corr", "parallax_pmdec_corr")}
TRUTH["source_id"] = u                                                              # sorted, unique; dtypes int64 / float32 as the caches hold them
P(f"truth: {len(u):,d} stars from the two on-disk builder caches ({TRUTH['source_id'].dtype}, {TRUTH['parallax_pmra_corr'].dtype})")

LOGQ = []                                                                           # (transport, n_ids, template)
rng = np.random.default_rng(7)
ID_RE = re.compile(r"WHERE source_id IN \(([0-9,]+)\)")


def truth_at(ids):
    """the correlations the mock archive holds for `ids`: the on-disk values; the few ids the on-disk caches do not cover get 0.0, exactly the zero fill the OFFLINE path (offline_correlations) applies, so that the offline,
    async and sync runs all see identical values"""
    pos = np.clip(np.searchsorted(TRUTH["source_id"], ids), 0, len(u) - 1)
    ok = TRUTH["source_id"][pos] == ids
    return {c: np.where(ok, TRUTH[c][pos], np.float32(0)).astype(np.float32) for c in ("parallax_pmra_corr", "parallax_pmdec_corr")}, ok


def answer(q, transport, cap):
    m = ID_RE.search(q)
    assert m, f"an unexpected query: {q[:100]}"
    ids = np.array([int(x) for x in m.group(1).split(",")], np.int64)
    LOGQ.append((transport, len(ids), ID_RE.sub("WHERE source_id IN (...)", q)))
    ids = ids[rng.permutation(len(ids))]                                            # server order is arbitrary
    if cap and len(ids) > cap:
        ids = ids[:cap]                                                             # the synchronous endpoint's SILENT cap
    vals, _ = truth_at(ids)
    return Table({"source_id": ids, "parallax_pmra_corr": vals["parallax_pmra_corr"], "parallax_pmdec_corr": vals["parallax_pmdec_corr"]})


class FakeJob:
    def __init__(self, t):
        self.t = t

    def get_results(self):
        return self.t


class FakeGaia:
    ROW_LIMIT = 50

    def launch_job_async(self, q, *a, **k):
        return FakeJob(answer(q, "async", None))

    def launch_job(self, q, dump_to_file=False, output_file=None, output_format="votable_gzip", **k):
        t = answer(q, "sync", 2000)
        if dump_to_file:                                                            # the pattern _gaia_sync uses (the one the real Q1 fetches used): a FITS file, read back
            assert output_format == "fits" and output_file, "the sync fallback must dump a FITS file"
            t.write(output_file, format="fits", overwrite=True)
        return FakeJob(t)


Gaia = FakeGaia()
_fake_mod = types.ModuleType("astroquery.gaia")
_fake_mod.Gaia = Gaia
sys.modules["astroquery.gaia"] = _fake_mod

orig_ccp, orig_bd = D.corr_cache_path, D.build_dir
if MUT == "1":
    D.SYNC_IDS_PER_CALL = 2000
if MUT in ("2", "3", "4"):
    orig_q = D._sync_corr_query

    def mutated(release, ids, query=None):
        def q2(q):
            r = (query or D._gaia_sync)(q)
            return r[:-1] if MUT == "2" else r
        out = orig_q(release, ids, query=q2)
        if MUT == "3":
            out = {k: (v.astype(np.float64) if k != "source_id" else v) for k, v in out.items()}
        if MUT == "4":
            out = dict(out); out["parallax_pmra_corr"], out["parallax_pmdec_corr"] = out["parallax_pmdec_corr"], out["parallax_pmra_corr"]
        return out
    D._sync_corr_query = mutated

tmp = Path(tempfile.mkdtemp())

# ------------------------------------------------------------------ S1 the reference (cache only)
bA, rA = D.run("dr3", "primary", "extract-builder", None, False)
C("S1 the reference run (on-disk cache only) reproduces the DR3 CSV (sha256 prefix 6fff64d964ebaa72)", rA["sha256"].startswith(D.REF_SHA_DR3), f"{rA['n_pairs']:,d} pairs, {rA['sha256'][:16]}")

# ------------------------------------------------------------------ S2 the builder's async fetch (mock server, empty temporary cache)
if True:
    D.corr_cache_path = lambda e, v: tmp / "async" / f"stage_G_corr_{v}.npz"
    (tmp / "async").mkdir()
    n0 = len(LOGQ)
    bB, rB = D.run("dr3", "primary", "extract-builder", None, True)
    qB = LOGQ[n0:]
zB = np.load(tmp / "async" / "stage_G_corr_primary.npz")
ids_B = np.sort(zB["source_id"])
tB, okB = truth_at(zB["source_id"])
eqB = all(np.array_equal(zB[c], tB[c]) for c in ("parallax_pmra_corr", "parallax_pmdec_corr"))
C("S2 the run with the builder's ASYNC fetch (mock server, empty temporary cache) gives a byte-identical stage-G CSV and a cache equal to the truth at the requested ids", bB == bA and eqB and len(qB) > 0,
  f"{len(zB['source_id']):,d} ids in {len(qB)} async calls (largest {max(n for _, n, _ in qB)}; {int((~okB).sum())} ids not in the on-disk caches answered with the offline path's zero fill); CSV identical {bB == bA}; cache values equal truth {eqB}")

# ------------------------------------------------------------------ S3 / S4 / S5 / S6 the sync fallback
exc = None
if True:
    D.corr_cache_path = lambda e, v: tmp / "sync" / f"stage_G_corr_{v}.npz"
    (tmp / "sync").mkdir()
    n0 = len(LOGQ)
    try:
        bC, rC = D.run("dr3", "primary", "extract-builder", None, True, corr_transport="sync")
    except Exception as e:
        bC, rC, exc = None, None, f"{type(e).__name__}: {str(e)[:150]}"
    qC = LOGQ[n0:]
if exc is None:
    zC = np.load(tmp / "sync" / "stage_G_corr_primary.npz")
    oB, oC = np.argsort(zB["source_id"], kind="stable"), np.argsort(zC["source_id"], kind="stable")
    ident = all(zB[c][oB].dtype == zC[c][oC].dtype and zB[c][oB].tobytes() == zC[c][oC].tobytes() for c in ("source_id", "parallax_pmra_corr", "parallax_pmdec_corr"))
    tC, okC = truth_at(zC["source_id"])
    eqC = all(np.array_equal(zC[c], tC[c]) for c in ("parallax_pmra_corr", "parallax_pmdec_corr"))
    C("S3 the SYNC fallback completes, gives the same CSV, and its cache arrays sorted by source_id are BYTE-IDENTICAL to the async run's (same dtypes) and equal to the truth", bC == bA and ident and eqC,
      f"CSV identical {bC == bA}; arrays byte-identical to the async run's {ident}; equal to the truth {eqC}; dtypes {zC['source_id'].dtype}, {zC['parallax_pmra_corr'].dtype}")
    n_ids = len(zC["source_id"])
    sizes = [n for _, n, _ in qC]
    C("S4 every sync call carried at most 1,999 ids and the number of calls is ceil(n / 1999); the async run used the builder's 2,000-id chunks",
      max(sizes) <= 1999 and len(sizes) == math.ceil(n_ids / 1999) and max(n for _, n, _ in qB) == 2000 and len(qB) == math.ceil(n_ids / 2000),
      f"sync: {len(sizes)} calls for {n_ids:,d} ids, largest {max(sizes)}; async: {len(qB)} calls, largest {max(n for _, n, _ in qB)}")
    C("S5 the SELECT texts of the two transports are identical up to the id list", {t for _, _, t in qB} == {t for _, _, t in qC} and len({t for _, _, t in qC}) == 1, f"template: {qC[0][2][:130]}")
    note = [n for n in rC["correlations"] if isinstance(n, dict) and "transport" in n]
    C("S6 the sync run's report records the transport (calls, ids, largest chunk); the reference and async reports carry no such key",
      rC.get("correlation_transport") == "sync" and len(note) == 1 and note[0]["calls"] == len(sizes) and note[0]["ids"] == n_ids and note[0]["max_ids_per_call"] == max(sizes)
      and "correlation_transport" not in rA and "correlation_transport" not in rB and not any("transport" in n for n in rB["correlations"] if isinstance(n, dict)),
      f"note {note}")
else:
    C("S3 the SYNC fallback completes, gives the same CSV, and its cache arrays sorted by source_id are BYTE-IDENTICAL to the async run's (same dtypes) and equal to the truth", False, f"the sync run RAISED: {exc}")
    sizes = [n for t, n, _ in LOGQ if t == "sync"]
    C("S4 every sync call carried at most 1,999 ids and the number of calls is ceil(n / 1999); the async run used the builder's 2,000-id chunks", bool(sizes) and max(sizes) <= 1999, f"sync call sizes {sizes[:6]}")
    C("S5 the SELECT texts of the two transports are identical up to the id list", True, "not evaluated (the sync run raised)")
    C("S6 the sync run's report records the transport", False, "not evaluated (the sync run raised)")

# ------------------------------------------------------------------ S7 a seed-sweep build with a PARTIAL primary cache
D.corr_cache_path, D.build_dir = orig_ccp, orig_bd
bK, rK = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=1)                        # the offline seed build 1 (builder files)
partial_ids = np.sort(ids_B)[::-1][:50]                                                                # 50 ids removed from the primary's cache
keep = ~np.isin(zB["source_id"], partial_ids)
(tmp / "partial").mkdir()
np.savez(tmp / "partial" / "stage_G_corr_primary.npz", **{c: zB[c][keep] for c in ("source_id", "parallax_pmra_corr", "parallax_pmdec_corr")})
exc7 = None
if True:
    D.corr_cache_path = lambda e, v: tmp / "partial" / f"stage_G_corr_{v}.npz"
    D.build_dir = lambda e, k: tmp / f"seed_k{k}"
    n0 = len(LOGQ)
    try:
        bK2, rK2 = D.run("dr3", "primary", "extract-builder", None, True, seed_offset=1, corr_transport="sync")
    except Exception as e:
        bK2, rK2, exc7 = None, None, f"{type(e).__name__}: {str(e)[:150]}"
    qK = LOGQ[n0:]
D.corr_cache_path, D.build_dir = orig_ccp, orig_bd
C("S7 a seed-sweep build with a PARTIAL primary cache fetches ONLY the missing ids through the sync query (one call, 50 ids) and gives the same CSV as the offline seed build",
  exc7 is None and bK2 == bK and len(qK) == 1 and qK[0][0] == "sync" and qK[0][1] == 50,
  f"offline seed build {rK['n_pairs']:,d} pairs {rK['sha256'][:16]}; networked sync {'RAISED ' + exc7 if exc7 else str(rK2['n_pairs']) + ' pairs ' + rK2['sha256'][:16]}; calls {[(t, n) for t, n, _ in qK]}")

# ------------------------------------------------------------------ S8 the driver's self-test and the refusal
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
st = subprocess.run([sys.executable, "-B", str(HERE / "dry_run_driver.py"), "--self-test"], capture_output=True, text=True, cwd=str(REPO), env=env)
rf = subprocess.run([sys.executable, "-B", str(HERE / "dry_run_driver.py"), "--corr-transport", "sync"], capture_output=True, text=True, cwd=str(REPO), env=env)
C("S8 the driver's own self-test still passes 7/7, and --corr-transport sync without --allow-network is refused", "7/7 pass -> ALL PASS" in st.stdout and rf.returncode != 0 and "--allow-network" in (rf.stderr + rf.stdout),
  f"self-test: {st.stdout.strip().splitlines()[-1][:60]}; refusal: {(rf.stderr or rf.stdout).strip().splitlines()[-1][:110]}")

if MUT:
    expect = {"1": ("S4",), "2": ("S3",), "3": ("S3",), "4": ("S3",)}[MUT]
    bit = all(not CHK.get(k, True) for k in expect)
    P(f"\n[MUTATE CONTROL] MUTATE={MUT}: {', '.join(expect)} {'FAILED as designed' if bit else 'did NOT fail: the control does not bite'}; checks that failed: {[k for k, v in CHK.items() if not v]}")
    ok = bit
else:
    ok = all(CHK.values())
    P(f"\n{sum(CHK.values())}/{len(CHK)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / f"test_driver_corr_sync{SFX}.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
