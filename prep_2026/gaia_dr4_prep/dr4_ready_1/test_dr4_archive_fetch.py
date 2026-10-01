#!/usr/bin/env python3
"""DR4-READY-1, items 1 and 4 of DR4_Q1_TOOLING_DESIGN_FROZEN.md (6742d206d): OFFLINE test of dr4_archive_fetch.py / q1_cones_dr4.py / dr4_q1_estimate.py against a MOCK ARCHIVE (NEW file; NO NETWORK: a socket guard blocks every connection and the real
astroquery.gaia, whose import opens one, is never imported).
The mock archive evaluates the SQL TEXT the tools generate with its OWN parser (table and column existence, LEFT OUTER versus inner JOIN, literal ranges, CONTAINS cones with declination slabs, TOP, the SILENT 2,000-row cap, injected flaky / hanging / crashing
queries), over tables with the DOCUMENTED DR4 names: all_source_astrometry + all_source_photometry (some sources without a photometry row), gaia_source_environment (ids unrelated to HEALPix, healpix29 given), crowded_field_source (no HEALPix column; one dense cluster
that needs the declination split).  Real DR3 stage-A sources (real ids) are planted inside the cones so the completeness check is exercised.  DR3 numbers are code-path numbers, never results (Amendment 7(e)).
T1 all-source fetch (crash + resume) = brute force incl. NULL-G rows;  T2 truncation exercised, none in the output;  T3 rows without G present and counted;  T4 local completeness 0 missing;  T5 schema probe: SchemaMismatch, exactly one query;  T6 mid-run column drift
caught (upper-case names accepted);  T7 join multiplicity stops the run;  T8 caps, plan-hash refusal, refusals without go text / caps, --plan-only: no query;  T9 crowded_field_source (cones, dense cone split) and gaia_source_environment (healpix29 ranges) = brute force;
T10 DR3 regression: the DR3 spec's SQL text equals the existing tools' and the rows equal the existing DR3 tool's on the same mock;  T11 estimator within 6 % of both DR3 runs, linear, monotone in density and pace;  T12 spot check agrees on a clean mock and DETECTS planted
source ids that no longer encode their pixel;  T13 the driver's --neighbours-manifest includes / excludes tables and records it;  T15 the planner at full size reproduces the existing DR3 delta tool's plan and the command line behaves; T14 the real manifests and DR3 data directory untouched.
MUTATE=1 truncation detection off (T1 must FAIL); =2 inner JOIN instead of LEFT OUTER (T1, T3, T4 must FAIL); =3 probe and per-batch validation off (T5, T6 must FAIL); =4 join-multiplicity check off (T7 must FAIL); =5 spot check off (T12 must FAIL);
=6 density and pace ignored in the estimator (T11 must FAIL).  Outputs go to separate files.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_dr4_archive_fetch.py"""
import sys
sys.dont_write_bytecode = True
import contextlib, hashlib, io, json, os, re, socket, tempfile, time
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline test (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import dr4_archive_fetch as F
import q1_pilot_ranges as Q1
import q1_delta_ranges as QD
from astropy.table import Table
from scipy.spatial import cKDTree
import healpy as hp

MUT = os.environ.pop("MUTATE", "").strip()
SFX = f"_MUTATE{MUT}" if MUT else ""
LOG, CHK = [], {}
T0 = time.time()
WB = REPO / "real_research" / "data" / "widebinaries"
STAGE_A = WB / "dr3_extract" / "stage_A.npz"
PAIRS = WB / "dr3_extract" / "dr4_ready_1" / "q1_delta_pairs.csv"
NP = 150


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def C(name, ok, detail=""):
    CHK[name.split()[0]] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


_sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest() if Path(p).exists() else None
REAL = {p: _sha(p) for p in (HERE / "manifest_q1_full.json", HERE / "manifest_q1_delta.json", HERE / "q1_delta_pairs_dr3.json")}
DATADIR = WB / "dr3_extract" / "dr4_ready_1"
DATA_BEFORE = sorted(os.listdir(DATADIR))


# ================================================================================================ the mock archive
class MockArchive:
    """a tiny SQL evaluator for exactly the query forms the tools generate; its own regexes, independent of the tools' builders"""
    CAP = 2000

    def __init__(self):
        self.tables, self.calls, self.log = {}, 0, []
        self.flaky_at = self.hang_at = self.crash_at = self.drift_after = None
        self.flaky_done = self.hang_done = False
        self.upper = False
        self.data_calls = 0

    def add(self, name, cols):
        self.tables[name] = {k: np.asarray(v) for k, v in cols.items()}

    @staticmethod
    def split_depth0(s, sep):
        out, depth, cur, i = [], 0, "", 0
        while i < len(s):
            if s[i] == "(":
                depth += 1
            elif s[i] == ")":
                depth -= 1
            if depth == 0 and s.startswith(sep, i):
                out.append(cur); cur = ""; i += len(sep); continue
            cur += s[i]; i += 1
        out.append(cur)
        return out

    def query(self, q):
        self.calls += 1
        self.log.append(q)
        if self.crash_at and self.calls == self.crash_at:
            raise KeyboardInterrupt("simulated crash")
        if self.flaky_at and self.calls == self.flaky_at and not self.flaky_done:
            self.flaky_done = True
            raise ConnectionError("simulated dropped connection")
        if self.hang_at and self.calls == self.hang_at and not self.hang_done:
            self.hang_done = True
            t_end = time.time() + 4.0
            while time.time() < t_end:
                pass
        m = re.match(r"^SELECT (?:TOP (\d+) )?(.+?) FROM (.+?) WHERE (.+)$", q, re.S)
        if not m:
            raise RuntimeError(f"syntax error near: {q[:80]}")
        top, sel, frm, where = m.groups()
        fm = re.match(r"^(\S+)(?: AS (\w+))?(?: (LEFT OUTER JOIN|JOIN) (\S+) AS (\w+) ON (\w+)\.(\w+) = (\w+)\.(\w+))?$", frm)
        if not fm:
            raise RuntimeError(f"syntax error in FROM: {frm[:80]}")
        t1, a1, jkind, t2, a2, ja, jc, ba, bc = fm.groups()
        for t in (t1, t2):
            if t and t not in self.tables:
                raise RuntimeError(f'relation "{t}" does not exist')
        base = self.tables[t1]
        n = len(next(iter(base.values())))
        # WHERE
        mask = np.zeros(n, bool)
        for grp in self.split_depth0(where, " OR "):
            g = grp.strip()
            assert g.startswith("(") and g.endswith(")"), f"unexpected group {g[:60]}"
            ok = np.ones(n, bool)
            for atom in self.split_depth0(g[1:-1], " AND "):
                atom = atom.strip()
                am = re.match(r"^(?:(\w+)\.)?(\w+) (>=|<) (-?[0-9.eE+-]+)$", atom)
                cm = re.match(r"^1 = CONTAINS\(POINT\('ICRS', (?:(\w+)\.)?(\w+), (?:(\w+)\.)?(\w+)\), CIRCLE\('ICRS', (-?[0-9.eE+-]+), (-?[0-9.eE+-]+), ([0-9.eE+-]+)\)\)$", atom)
                if am:
                    al, col, op, val = am.groups()
                    if al not in (None, a1):
                        raise RuntimeError(f"the WHERE clause references {al}, not the base table")
                    if col not in base:
                        raise RuntimeError(f'column "{col}" does not exist')
                    v = int(val) if re.fullmatch(r"-?\d+", val) else float(val)
                    ok &= (base[col] >= v) if op == ">=" else (base[col] < v)
                elif cm:
                    _, rc, _, dc, x, y, r = cm.groups()
                    if rc not in base or dc not in base:
                        raise RuntimeError(f'column "{rc}" or "{dc}" does not exist')
                    ra, dec = np.radians(base[rc].astype(float)), np.radians(base[dc].astype(float))
                    x, y, r = np.radians(float(x)), np.radians(float(y)), np.radians(float(r))
                    cosd = np.sin(dec) * np.sin(y) + np.cos(dec) * np.cos(y) * np.cos(ra - x)
                    ok &= np.arccos(np.clip(cosd, -1, 1)) <= r
                else:
                    raise RuntimeError(f"cannot parse atom: {atom[:80]}")
            mask |= ok
        rows = np.flatnonzero(mask)
        # JOIN
        if t2:
            jt = self.tables[t2]
            if bc not in base or jc not in jt:
                raise RuntimeError(f'column "{bc}" / "{jc}" does not exist')
            index = {}
            for j, k in enumerate(jt[jc].tolist()):
                index.setdefault(k, []).append(j)
            brow, jrow = [], []
            for r in rows.tolist():
                hits = index.get(int(base[bc][r]), [])
                if hits:
                    for j in hits:
                        brow.append(r); jrow.append(j)
                elif jkind == "LEFT OUTER JOIN":
                    brow.append(r); jrow.append(-1)
            brow, jrow = np.array(brow, int), np.array(jrow, int)
        else:
            brow, jrow = rows, None
        # SELECT
        cols = {}
        for item in sel.split(", "):
            im = re.match(r"^(?:(\w+)\.)?(\w+)(?: AS (\w+))?$", item.strip())
            if not im:
                raise RuntimeError(f"cannot parse select item: {item}")
            al, col, out = im.groups()
            out = out or col
            if t2 and al == a2:
                if col not in jt:
                    raise RuntimeError(f'column "{al}.{col}" does not exist')
                arr = jt[col]
                v = np.where(jrow >= 0, arr[np.clip(jrow, 0, len(arr) - 1)], np.nan if arr.dtype.kind == "f" else 0)
                cols[out] = v.astype(arr.dtype) if arr.dtype.kind == "f" else v
            else:
                if col not in base:
                    raise RuntimeError(f'column "{col}" does not exist')
                cols[out] = base[col][brow]
        if self.drift_after is not None and self.data_calls >= self.drift_after and "phot_g_mean_mag" in cols:
            cols["phot_g_mean_mag_v2"] = cols.pop("phot_g_mean_mag")
        if top is None:
            self.data_calls += 1
        n_out = len(next(iter(cols.values())))
        lim = int(top) if top else n_out
        k = min(lim, n_out)
        if k > self.CAP:
            k = self.CAP                                                            # the synchronous endpoint's SILENT cap
        T = Table({(c.upper() if self.upper else c): v[:k] for c, v in cols.items()})
        self.last_truncated = (k < n_out)
        return T


def install(archive):
    def fake_launch(q, path):
        T = archive.query(q)
        T.write(path, format="fits", overwrite=True)
    Q1.launch_query = fake_launch
    Q1.TIMEOUT_S = 1
    Q1.PAUSE_S = 0.0
    F.PAUSE_S = 0.0
    time.sleep = lambda s: None


# ================================================================================================ the mock sky
spec_all = F.load_spec("dr4_all_source")[0]
plan0 = F.plan_pairs(STAGE_A, PAIRS, spec_all, NP)
A = plan0["A"]
rng = np.random.default_rng(1711)


def disc_points(v, rad_deg, m):
    th = np.sqrt(rng.random(m)) * np.radians(rad_deg); ph = rng.random(m) * 2 * np.pi
    e1 = np.cross(v, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)
    pts = v[None, :] * np.cos(th)[:, None] + np.sin(th)[:, None] * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
    return np.degrees(np.arctan2(pts[:, 1], pts[:, 0])) % 360, np.degrees(np.arcsin(np.clip(pts[:, 2], -1, 1)))


def build_sky(plan, bad_id_fraction=0.0, dup_phot=False):
    cols = {k: [] for k in ("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error", "healpix29")}
    gvals, dense = [], rng.random(len(plan["R"])) < 0.2
    for k in range(len(plan["R"])):
        for v in (plan["va"][k], plan["vb"][k]):
            rad = (plan["R"][k] + 45.0) / 3600.0
            m = rng.poisson((3 * 7.0e3 if dense[k] else 7.0e3) * np.pi * rad ** 2)
            if m == 0:
                continue
            ra, dec = disc_points(v, rad, m)
            pix = hp.ang2pix(2 ** 12, ra, dec, nest=True, lonlat=True).astype(np.int64)
            sid = pix * 2 ** 35 + rng.integers(0, 2 ** 35, m)
            if bad_id_fraction:
                bad = rng.random(m) < bad_id_fraction
                sid = np.where(bad, ((pix + 1000) % (12 * 4 ** 12)) * 2 ** 35 + rng.integers(0, 2 ** 35, m), sid)       # ids that no longer encode their pixel
            for c, val in (("source_id", sid), ("ra", ra), ("dec", dec)):
                cols[c].append(val)
            cols["parallax"].append(rng.uniform(0.1, 6, m)); cols["parallax_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
            cols["pmra"].append(rng.normal(0, 8, m)); cols["pmdec"].append(rng.normal(0, 8, m))
            cols["pmra_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32)); cols["pmdec_error"].append(rng.uniform(0.02, 0.5, m).astype(np.float32))
            cols["healpix29"].append(pix * 2 ** 34 + rng.integers(0, 2 ** 34, m))
            gvals.append(rng.uniform(8, 21, m).astype(np.float32))
    tree_A = cKDTree(Q1.vec(np.asarray(A["ra"], float), np.asarray(A["dec"], float)))
    real = set()
    for k in range(len(plan["R"])):
        for v in (plan["va"][k], plan["vb"][k]):
            real.update(tree_A.query_ball_point(v, r=2 * np.sin(np.radians((plan["R"][k] + 45.0) / 3600) / 2)))
    real = np.array(sorted(real), int)
    pix_real = hp.ang2pix(2 ** 12, np.asarray(A["ra"], float)[real], np.asarray(A["dec"], float)[real], nest=True, lonlat=True).astype(np.int64)
    for c in ("source_id", "ra", "dec"):
        cols[c].append(np.asarray(A[c])[real])
    for c, lo, hi in (("parallax", 0.1, 6), ("pmra", -8, 8), ("pmdec", -8, 8)):
        cols[c].append(np.asarray(A[c], float)[real] if c in A else rng.uniform(lo, hi, len(real)))
    for c in ("parallax_error", "pmra_error", "pmdec_error"):
        cols[c].append(rng.uniform(0.02, 0.5, len(real)).astype(np.float32))
    cols["healpix29"].append(pix_real * 2 ** 34 + rng.integers(0, 2 ** 34, len(real)))
    gvals.append(rng.uniform(8, 17, len(real)).astype(np.float32))
    ast = {k: np.concatenate(v) for k, v in cols.items()}
    order = np.argsort(ast["source_id"], kind="stable")
    ast = {k: v[order] for k, v in ast.items()}
    _, uq = np.unique(ast["source_id"], return_index=True)
    uq = np.sort(uq)
    ast = {k: v[uq] for k, v in ast.items()}
    g = np.concatenate(gvals)[order][uq]
    has_phot = rng.random(len(g)) > 0.15                                              # ~15 % of the sources have NO photometry row (LEFT JOIN -> NULL G)
    sid_real = set(np.asarray(A["source_id"])[real].tolist())
    is_real = np.array([s in sid_real for s in ast["source_id"].tolist()])
    has_phot[is_real] = rng.random(int(is_real.sum())) > 0.10                          # and some REAL base sources too (the MUTATE-2 bite)
    phot = {"source_id": ast["source_id"][has_phot], "phot_g_mean_mag": g[has_phot]}
    if dup_phot:
        d = np.flatnonzero(has_phot)[:60]
        phot = {"source_id": np.concatenate([phot["source_id"], ast["source_id"][d]]), "phot_g_mean_mag": np.concatenate([phot["phot_g_mean_mag"], g[d] + 0.1])}
    return ast, phot, is_real


def brute_truth(plan, base, g_by_sid=None, ids=None):
    """(pair, comp, source_id) -> G (NaN if none) for every table row inside the exact cones"""
    tree = cKDTree(Q1.vec(np.asarray(base["ra"], float), np.asarray(base["dec"], float)))
    out = {}
    for k in range(len(plan["R"])):
        chord = 2 * np.sin(np.radians(plan["R"][k] / 3600) / 2)
        for c, vc in ((0, plan["va"][k]), (1, plan["vb"][k])):
            for j in tree.query_ball_point(vc, r=chord):
                s = int(base["source_id"][j])
                out[(int(plan["pick"][k]), c, s)] = (g_by_sid.get(s, np.nan) if g_by_sid is not None else (float(base["phot_g_mean_mag"][j]) if "phot_g_mean_mag" in base else np.nan))
    return out


def result_dict(path):
    E = Table.read(path, format="fits")
    return {(int(p), int(c), int(s)): float(g) for p, c, s, g in zip(E["pair_id"], E["comp"], E["source_id"], np.asarray(E["phot_g_mean_mag"].filled(np.nan) if hasattr(E["phot_g_mean_mag"], "filled") else E["phot_g_mean_mag"], float))}


def same(a, b):
    if a.keys() != b.keys():
        return False
    return all((np.isnan(a[k]) and np.isnan(b[k])) or abs(a[k] - b[k]) < 1e-5 for k in a)


P("DR4 RELEASE-DAY CONE FETCH: offline test against a mock archive (DR3 code-path numbers)" + (f"   *** MUTATE={MUT}: " + {"1": "truncation detection off (T1 must FAIL)", "2": "inner JOIN instead of LEFT OUTER (T1, T3, T4 must FAIL)", "3": "probe and per-batch validation off (T5, T6 must FAIL)",
                                                                                                  "4": "join-multiplicity check off (T7 must FAIL)", "5": "spot check off (T12 must FAIL)", "6": "density and pace ignored in the estimator (T11 must FAIL)"}[MUT] + " ***" if MUT else ""))
ast, phot, is_real = build_sky(plan0)
g_by_sid = {int(s): float(g) for s, g in zip(phot["source_id"], phot["phot_g_mean_mag"])}
truth = brute_truth(plan0, ast, g_by_sid)
n_nog = sum(1 for v in truth.values() if np.isnan(v))
P(f"mock sky: {len(ast['source_id']):,d} sources ({int(is_real.sum())} real stage-A ones), {len(phot['source_id']):,d} photometry rows; {NP} pairs; brute-force truth {len(truth):,d} (pair, comp, source) rows of which {n_nog:,d} without G; {len(plan0['units'])} planned ranges")

if MUT == "1":
    Q1.SYNC_CAP = 10 ** 9
    F.SYNC_CAP = 10 ** 9
if MUT == "2":
    F.SPECS["dr4_all_source"]["join"]["kind"] = "JOIN"                                 # the inner join (a missing join row)
if MUT == "3":
    F.probe_schema = lambda spec, P_, launch=None: {}
    F._VALIDATE = False
if MUT == "4":
    F._CHECK_MULT = False
if MUT == "5":
    F._SPOT = False
if MUT == "6":
    _orig_est = F.estimate
    F.estimate = lambda n_pairs, density=1.0, pace=1.0, cal=None: _orig_est(n_pairs, 1.0, 1.0, cal)

arch = MockArchive()
arch.add("gaiadr4.all_source_astrometry", ast)
arch.add("gaiadr4.all_source_photometry", phot)
install(arch)
GO, CAPS = "test: offline mock archive", dict(accepted_bytes=200_000_000, received_bytes=400_000_000, max_queries=100_000)


def run(td, archive_=None, spec="dr4_all_source", tag="t", caps=None, go=GO, **kw):
    arch_ = archive_ or arch
    install(arch_)
    try:
        man = F.run_fetch(spec, STAGE_A, PAIRS, Path(td), Path(td) / "manifest.json", tag, caps=caps or CAPS, go_text=go, max_pairs=NP, cal=F.calibration(), **kw)
        return None, man
    except KeyboardInterrupt:
        return "CRASH", None
    except (SystemExit, Exception) as e:                                           # any failure is a result to be judged by the checks (a MUTATEd tool may fail less gracefully)
        return f"{type(e).__name__}: {str(e)[:200]}", None


def man_of(td):
    f = Path(td) / "manifest.json"
    return json.loads(f.read_text()) if f.exists() else {}


# ------------------------------------------------------------------------------------------------ T1-T4 the all-source fetch (crash + resume)
with tempfile.TemporaryDirectory() as td:
    arch.calls = 0; arch.crash_at, arch.flaky_at, arch.hang_at = 20, 5, 9
    arch.flaky_done = arch.hang_done = False
    errA, _ = run(td)
    cacheA = len(list((Path(td) / "q1_t_cache").glob("b*.fits")))
    P(f"run A ended with: {errA} after {arch.calls} calls; the cache holds {cacheA} accepted batches")
    arch.crash_at = None; calls_before = arch.calls
    errB, man = run(td)
    man = man or man_of(td)
    P(f"run B (resume) ended with: {errB}; {arch.calls - calls_before} new calls; manifest queries_total {man.get('queries_total')}")
    got = result_dict(Path(td) / "q1_t_neighbours.fits") if (Path(td) / "q1_t_neighbours.fits").exists() else {}
    t1 = same(got, truth)
    C(f"T1 the all-source fetch (crash + resume, LEFT OUTER JOIN) equals the brute-force truth including the NULL-G rows (missing {len(set(truth) - set(got))}, spurious {len(set(got) - set(truth))})", t1)
    C(f"T2 the truncation path was exercised and no truncated result reached the output (manifest {man.get('truncated_results_discarded')} discarded)", (man.get("truncated_results_discarded", 0) > 0) and t1)
    ex_nog_truth = sum(1 for v in truth.values() if np.isnan(v))
    C(f"T3 the rows without G are present with NULL G and counted (exact {man.get('rows_without_g_exact')} vs truth {ex_nog_truth}; raw {man.get('rows_without_g_raw')})", man.get("rows_without_g_exact") == ex_nog_truth and ex_nog_truth > 0)
    C(f"T4 the local completeness check reports 0 missing of {man.get('local_extract_sources_in_cones')} and the output is marked usable", man.get("local_extract_sources_missing_from_fetch") == 0 and man.get("usable") is True)
    C(f"T4b the resumed run used the cache (batches resumed {man.get('batches_resumed_from_cache')}), probed the schema again at its start, and the manifest keeps the first session's probe and start time besides the probe, caps, approval text and spec", errA == "CRASH" and man.get("batches_resumed_from_cache", 0) > 0 and "schema_probe" in (man_of(td) or man)
      and "schema_probe_first_session" in man and "utc_start_first_session" in man
      and man.get("approval") == GO and man.get("spec", {}).get("table") == "gaiadr4.all_source_astrometry" and man.get("caps", {}).get("max_queries") == CAPS["max_queries"])
    # T8 pieces on the same plan
    st = json.loads((Path(td) / "q1_t_cache" / "state.json").read_text())
    (Path(td) / "q1_t_cache" / "state.json").write_text(json.dumps({"plan_hash": "0" * 16}))
    errH, _ = run(td)
    C("T8a a cache that belongs to a different plan is refused", errH is not None and "different plan" in errH, (errH or "")[:100])
with tempfile.TemporaryDirectory() as td:
    arch.crash_at = arch.flaky_at = arch.hang_at = None; arch.calls = 0
    e1, _ = run(td, caps=dict(accepted_bytes=300_000, received_bytes=400_000_000, max_queries=100_000))
    cache_n = len(list((Path(td) / "q1_t_cache").glob("b*.fits")))
    C(f"T8b the accepted-bytes cap stops the run, writes the reason and keeps the cache ({(e1 or '')[:70]})", bool(e1) and "STOPPED" in e1 and "stopped" in man_of(td) and cache_n > 0)
with tempfile.TemporaryDirectory() as td:
    e2, _ = run(td, caps=dict(accepted_bytes=200_000_000, received_bytes=400_000, max_queries=100_000))
    C(f"T8c the transfer cap stops the run ({(e2 or '')[:70]})", bool(e2) and "STOPPED" in e2)
with tempfile.TemporaryDirectory() as td:
    e3, _ = run(td, caps=dict(accepted_bytes=200_000_000, received_bytes=400_000_000, max_queries=6))
    C(f"T8d the query-count cap stops the run ({(e3 or '')[:70]})", bool(e3) and "STOPPED" in e3 and "more than 6 queries" in e3)
with tempfile.TemporaryDirectory() as td:
    arch.calls = 0
    e4, _ = run(td, go="  ")
    c4 = arch.calls
    e5, _ = run(td, caps=dict(accepted_bytes=0, received_bytes=0, max_queries=0))
    c5 = arch.calls
    e6, _ = run(td, plan_only=True)
    c6 = arch.calls
    C(f"T8e a run without a go text, without caps, and --plan-only each issue NO query (calls {c4}, {c5 - c4}, {c6 - c5}); the first two are refused", c4 == 0 and c5 == c4 and c6 == c5 and "refused" in (e4 or "") and "refused" in (e5 or "") and e6 is None and not (Path(td) / "q1_t_neighbours.fits").exists())

# ------------------------------------------------------------------------------------------------ T5 / T6 schema
bad = {k: v for k, v in ast.items()}
bad["parallax_err"] = bad.pop("parallax_error")
arch5 = MockArchive(); arch5.add("gaiadr4.all_source_astrometry", bad); arch5.add("gaiadr4.all_source_photometry", phot)
with tempfile.TemporaryDirectory() as td:
    e, _ = run(td, archive_=arch5)
    C(f"T5 a mock whose column is renamed (parallax_error -> parallax_err): SchemaMismatch naming it, after exactly ONE query (the probe) ({arch5.calls} queries; {(e or '')[:90]})",
      bool(e) and e.startswith("SchemaMismatch") and "parallax_error" in e and arch5.calls == 1)
arch6 = MockArchive(); arch6.add("gaiadr4.all_source_astrometry", ast); arch6.add("gaiadr4.all_source_photometry", phot); arch6.drift_after = 6
with tempfile.TemporaryDirectory() as td:
    e, _ = run(td, archive_=arch6)
    drift_ok = bool(e) and e.startswith("SchemaMismatch") and "phot_g_mean_mag" in e
arch6u = MockArchive(); arch6u.add("gaiadr4.all_source_astrometry", ast); arch6u.add("gaiadr4.all_source_photometry", phot); arch6u.upper = True
with tempfile.TemporaryDirectory() as td:
    eu, manu = run(td, archive_=arch6u)
    upper_ok = eu is None and bool(manu) and same(result_dict(Path(td) / "q1_t_neighbours.fits"), truth)
C(f"T6 a column that drifts mid-run (after 6 data queries) raises SchemaMismatch at that batch; upper-case column names from the archive are accepted and give the same rows ({(e or '')[:70]})", drift_ok and upper_ok)

# ------------------------------------------------------------------------------------------------ T7 join multiplicity
ast7, phot7, _ = ast, None, None
phot_dup = {"source_id": np.concatenate([phot["source_id"], phot["source_id"][:80]]), "phot_g_mean_mag": np.concatenate([phot["phot_g_mean_mag"], phot["phot_g_mean_mag"][:80] + 0.1])}
arch7 = MockArchive(); arch7.add("gaiadr4.all_source_astrometry", ast); arch7.add("gaiadr4.all_source_photometry", phot_dup)
with tempfile.TemporaryDirectory() as td:
    e, _ = run(td, archive_=arch7)
    mult = bool(e) and e.startswith("JoinMultiplicity")
    # is the duplicated photometry actually inside the cones (so the control CAN fire)?
    dup_ids = phot["source_id"][:80]
    lo_ = np.array([r[0] for r in plan0["rng"]]); hi_ = np.array([r[1] for r in plan0["rng"]])
    jj = np.clip(np.searchsorted(lo_, dup_ids, side="right") - 1, 0, len(lo_) - 1)
    inside = int(((dup_ids >= lo_[jj]) & (dup_ids < hi_[jj])).sum())
C(f"T7 a duplicated photometry row (the join multiplies rows) stops the run with JoinMultiplicity ({inside} of the 80 duplicated ids lie inside the planned ranges, so the control can fire; {(e or '')[:90]})", mult and inside > 0)

# ------------------------------------------------------------------------------------------------ T9 the optional tables
plan_c = F.plan_pairs(STAGE_A, PAIRS, F.load_spec("dr4_crowded_field_source")[0], NP)
n_env, n_cf = 3000, 900
env_ra, env_dec = [], []
cf_ra, cf_dec = [], []
for k in range(0, NP, 3):
    v = plan_c["va"][k]
    ra, dec = disc_points(v, (plan_c["R"][k] + 30) / 3600, 25)
    env_ra.append(ra); env_dec.append(dec)
    ra, dec = disc_points(plan_c["vb"][k], (plan_c["R"][k] + 30) / 3600, 8)
    cf_ra.append(ra); cf_dec.append(dec)
dense_v = plan_c["va"][5]                                                              # a dense cluster inside one cone: more than 2,000 sources (needs the declination split)
dra, ddec = disc_points(dense_v, 25.0 / 3600, 2600)
cf_ra.append(dra); cf_dec.append(ddec)
env_ra, env_dec, cf_ra, cf_dec = [np.concatenate(x) for x in (env_ra, env_dec, cf_ra, cf_dec)]


def optional_table(ra, dec, with_hp):
    m = len(ra)
    t = dict(source_id=rng.integers(1, 2 ** 62, m), ra=ra, dec=dec, parallax=rng.uniform(0.1, 6, m), parallax_error=rng.uniform(0.02, 0.5, m).astype(np.float32), pmra=rng.normal(0, 8, m), pmdec=rng.normal(0, 8, m),
             pmra_error=rng.uniform(0.02, 0.5, m).astype(np.float32), pmdec_error=rng.uniform(0.02, 0.5, m).astype(np.float32), phot_g_mean_mag=rng.uniform(12, 21, m).astype(np.float32))
    if with_hp:
        t["healpix29"] = hp.ang2pix(2 ** 12, ra, dec, nest=True, lonlat=True).astype(np.int64) * 2 ** 34 + rng.integers(0, 2 ** 34, m)
    return t


env_t, cf_t = optional_table(env_ra, env_dec, True), optional_table(cf_ra, cf_dec, False)
arch9 = MockArchive(); arch9.add("gaiadr4.gaia_source_environment", env_t); arch9.add("gaiadr4.crowded_field_source", cf_t)
with tempfile.TemporaryDirectory() as td:
    arch9.calls = 0
    eE, mE = run(td, archive_=arch9, spec="dr4_gaia_source_environment", tag="env")
    truthE = brute_truth(plan0, env_t)
    gotE = result_dict(Path(td) / "q1_env_neighbours.fits") if eE is None else {}
    envq = [q for q in arch9.log if "healpix29 >= " in q]
    eC, mC = run(td, archive_=arch9, spec="dr4_crowded_field_source", tag="cf")
    truthC = brute_truth(plan_c, cf_t)
    gotC = result_dict(Path(td) / "q1_cf_neighbours.fits") if eC is None else {}
    split_used = any(" AND dec >= " in q for q in arch9.log)
C(f"T9 gaia_source_environment (ranges on healpix29, ids unrelated to HEALPix) and crowded_field_source (batched cones, the dense cone of 2,600 sources split by declination) equal their brute-force truths",
  eE is None and eC is None and same(gotE, truthE) and same(gotC, truthC) and len(envq) > 0 and not any("source_id >=" in q for q in arch9.log) and split_used and mE.get("truncated_results_discarded", 0) >= 0 and mC.get("truncated_results_discarded", 0) > 0,
  f"environment: {len(gotE):,d} rows (truth {len(truthE):,d}), {len(envq)} healpix29 range queries, no source_id range query; crowded: {len(gotC):,d} rows (truth {len(truthC):,d}), truncated {mC.get('truncated_results_discarded')}, slab split used {split_used}; errors {eE}, {eC}")

# ------------------------------------------------------------------------------------------------ T10 DR3 regression
spec3 = F.load_spec("dr3_gaia_source")[0]
sample = [(1 * 2 ** 35, 3 * 2 ** 35), (7 * 2 ** 35, 8 * 2 ** 35)]
old_text = f"SELECT {', '.join(Q1.KEEP)} FROM gaiadr3.gaia_source WHERE " + " OR ".join(f"(source_id >= {lo} AND source_id < {hi})" for lo, hi in sample)
text_ok = F.build_query(spec3, F.where_ranges(spec3, sample)) == old_text
phot3 = {"source_id": ast["source_id"], "phot_g_mean_mag": np.array([g_by_sid.get(int(s), np.nan) for s in ast["source_id"]], np.float32)}
dr3tab = {k: v for k, v in ast.items() if k != "healpix29"}
dr3tab["phot_g_mean_mag"] = phot3["phot_g_mean_mag"]
arch10 = MockArchive(); arch10.add("gaiadr3.gaia_source", dr3tab)
with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as td2:
    arch10.calls = 0
    e10, m10 = run(td, archive_=arch10, spec="dr3_gaia_source", tag="r3")
    new_rows = result_dict(Path(td) / "q1_r3_neighbours.fits") if e10 is None else {}
    # the existing DR3 delta tool on the same mock
    install(arch10)
    QD.OUT = Path(td2); QD.CACHE = Path(td2) / "q1_delta_cache"; QD.MAN = Path(td2) / "manifest.json"; QD.PAUSE_S = 0.0
    sys.argv = ["q1_delta_ranges.py", "--owner-go-recorded", "test", "--max-pairs", str(NP)]
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            QD.main(); old_ok = True
        except Exception as ex:
            old_ok = False
    old_rows = result_dict(Path(td2) / "q1_delta_neighbours.fits") if old_ok else {}
C(f"T10 DR3 regression: the DR3 spec's SQL text equals the existing tools' ({text_ok}) and its rows equal the existing q1_delta_ranges tool's on the same mock archive ({len(new_rows):,d} vs {len(old_rows):,d}; errors {e10})",
  text_ok and e10 is None and old_ok and same(new_rows, old_rows) and len(new_rows) > 0)

# ------------------------------------------------------------------------------------------------ T11 the estimator
cal = F.calibration()
full, delta = cal["runs"]["full_q1_dr3"], cal["runs"]["delta_q1_dr3"]
errs = []
for r in (full, delta):
    e = F.estimate(r["pairs"], 1.0, 1.0, cal)
    errs += [abs(e["queries"] / r["queries"] - 1), abs(e["accepted_mb"] * 1e6 / r["accepted_bytes"] - 1), abs(e["hours"] * 3600 / r["seconds"] - 1)]
e1, e2 = F.estimate(1000, 1.0, 1.0, cal), F.estimate(2000, 1.0, 1.0, cal)
txt, brief = F.pre_brief(49000, cal)
rows = brief["rows"]
mono = rows["high"]["queries"] > rows["central"]["queries"] > rows["low"]["queries"] and rows["central"]["hours_if_2x_slower"] > 1.9 * rows["central"]["hours"] and F.estimate(1000, 2.0, 2.0, cal)["hours"] > 3.9 * e1["hours"]
C(f"T11 the estimator reproduces both DR3 runs within 6 % (worst {100 * max(errs):.1f} %), is linear in the pair count, and is monotone in density and pace (central 49,000 pairs: {rows['central']['queries']:,.0f} queries, {rows['central']['accepted_mb']:,.0f} MB, {rows['central']['hours']:.0f} h)",
  max(errs) < 0.06 and abs(e2["queries"] / e1["queries"] - 2) < 1e-9 and mono and "PRE-BRIEF" in txt and "suggested hard caps" in txt)

# ------------------------------------------------------------------------------------------------ T12 the spot check
arch12 = MockArchive(); arch12.add("gaiadr4.all_source_astrometry", ast); arch12.add("gaiadr4.all_source_photometry", phot)
with tempfile.TemporaryDirectory() as td:
    eclean, mclean = run(td, archive_=arch12, spot_n=14)
    sc = (mclean or man_of(td)).get("spot_check", {})
    clean_ok = eclean is None and sc.get("n") == 14 and not sc.get("disagree") and sc.get("agree", 0) > 0
ast_bad, phot_bad, _ = build_sky(plan0, bad_id_fraction=0.25)
arch12b = MockArchive(); arch12b.add("gaiadr4.all_source_astrometry", ast_bad); arch12b.add("gaiadr4.all_source_photometry", phot_bad)
with tempfile.TemporaryDirectory() as td:
    ebad, _ = run(td, archive_=arch12b, spot_n=14)
    mb = man_of(td)
    detected = bool(ebad) and ebad.startswith("SpotCheckFailed") and mb.get("usable") is False and len(mb.get("spot_check", {}).get("disagree", [])) > 0
C(f"T12 the spot check agrees on a clean mock ({sc.get('agree')} of {sc.get('n')} cones, {sc.get('skipped_truncated')} skipped) and DETECTS planted source ids that no longer encode their pixel ({(ebad or '')[:80]}; usable {mb.get('usable')})", clean_ok and detected)

# ------------------------------------------------------------------------------------------------ T13 the driver's --neighbours-manifest switch
import dry_run_driver as D
import cones_cut13 as CC
with tempfile.TemporaryDirectory() as td:
    D.init(False)
    ext = D.extract_dir("dr3", "primary")
    S = dict(np.load(ext / "stage_A.npz"))
    sid = S["source_id"]; order = np.argsort(sid)
    rows_of = lambda ids: order[np.searchsorted(sid[order], ids)]
    cand = Path(td) / "cand.csv"
    D.run("dr3", "primary", "extract-builder", None, False, dump_candidates=str(cand))
    c1, c2 = CC.read_pairs_csv(cand)
    files = {}
    for name, sl in (("all_source", slice(0, 60)), ("crowded_field_source", slice(60, 100))):
        a_, b_ = rows_of(c1[sl]), rows_of(c2[sl])
        nb, s1, s2 = CC.build_extract_cones(S, a_, b_)
        Table({k: v for k, v in nb.items()}).write(Path(td) / f"{name}.fits", format="fits", overwrite=True)
        (Path(td) / f"{name}.csv").write_text("source_id1,source_id2\n" + "".join(f"{int(x)},{int(y)}\n" for x, y in zip(s1, s2)))
        files[name] = (str(Path(td) / f"{name}.fits"), str(Path(td) / f"{name}.csv"))

    def drive(inc):
        m = [dict(table=t, neighbours=files[t][0], pairs=files[t][1], include=inc.get(t)) for t in files]
        (Path(td) / "nm.json").write_text(json.dumps(m))
        buf = io.StringIO()
        sys.argv = ["dry_run_driver.py", "--cut13", "cones-literal", "--missing-cones", "extract-fallback", "--neighbours-manifest", str(Path(td) / "nm.json")]
        with contextlib.redirect_stdout(buf):
            D.main()
        txt_ = buf.getvalue()
        return json.loads(txt_[txt_.index("{"):])
    r_a = drive({"all_source": True, "crowded_field_source": False})
    r_b = drive({"all_source": False, "crowded_field_source": True})
    r_ab = drive({"all_source": True, "crowded_field_source": True})
    covered = lambda r: r["cut13_cones"]["n_covered"]
    C(f"T13 the driver's --neighbours-manifest includes exactly the tables marked include and records the choice (covered pairs {covered(r_a)} / {covered(r_b)} / {covered(r_ab)} for A only / B only / both)",
      covered(r_a) == 60 and covered(r_b) == 40 and covered(r_ab) == 100 and r_a["neighbours_manifest"]["included"] == ["all_source"] and r_a["neighbours_manifest"]["left_out"] == ["crowded_field_source"]
      and r_b["neighbours_manifest"]["included"] == ["crowded_field_source"] and len(r_ab["neighbours_manifest"]["sha256"]) == 64)

# ------------------------------------------------------------------------------------------------ T15 the planner at FULL size and the command line
import q1_cones_dr4 as CLI
with tempfile.TemporaryDirectory() as td:
    full3 = F.plan_pairs(STAGE_A, PAIRS, spec3)
    old_plan = QD.plan_delta(PAIRS)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = CLI.main(["--spec", "dr3_gaia_source", "--stage-a", str(STAGE_A), "--pairs-csv", str(PAIRS), "--tag", "x", "--out-dir", td, "--manifest", str(Path(td) / "m.json"), "--plan-only"])
    out_txt = buf.getvalue()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            CLI.main(["--spec", "dr3_gaia_source", "--stage-a", str(STAGE_A), "--pairs-csv", str(PAIRS), "--tag", "x", "--out-dir", td, "--manifest", str(Path(td) / "m.json"), "--max-pairs", "40"])
        refused_cli = False
    except SystemExit as e:
        refused_cli = "refused" in str(e)
    try:
        CLI.main(["--spec", "dr3_gaia_source"]); missing_ok = False
    except SystemExit as e:
        missing_ok = "required" in str(e)
C(f"T15 the generic planner at FULL size reproduces the existing DR3 delta tool's plan ({full3['n_pix']:,d} pixels, {len(full3['rng']):,d} ranges), the command line's --plan-only runs offline, and the command line refuses without a go text or without its required arguments",
  full3["n_pix"] == old_plan["n_pix"] == 387987 and full3["rng"] == old_plan["rng"] and rc == 0 and "4,021 pairs" in out_txt and "387,987" in out_txt and refused_cli and missing_ok)

# ------------------------------------------------------------------------------------------------ T14 nothing real was touched
C("T14 the real manifests and the DR3 data directory are exactly as before the test (no file added, none changed)", all(_sha(p) == h for p, h in REAL.items()) and sorted(os.listdir(DATADIR)) == DATA_BEFORE,
  f"data dir entries before {len(DATA_BEFORE)}, after {len(os.listdir(DATADIR))}")

if MUT:
    expect = {"1": ("T1",), "2": ("T1", "T3", "T4"), "3": ("T5", "T6"), "4": ("T7",), "5": ("T12",), "6": ("T11",)}[MUT]
    bit = all(not CHK.get(k, True) for k in expect)
    P(f"\n[MUTATE CONTROL] MUTATE={MUT}: {', '.join(expect)} {'FAILED as designed' if bit else 'did NOT all fail: the control does not bite'}; checks that failed: {[k for k, v in CHK.items() if not v]}")
    ok = bit
else:
    ok = all(CHK.values())
    P(f"\n{sum(CHK.values())}/{len(CHK)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - T0:.0f} s)")
(HERE / f"test_dr4_archive_fetch{SFX}.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
