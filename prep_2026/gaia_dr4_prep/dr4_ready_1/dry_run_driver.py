#!/usr/bin/env python3
"""DR4-READY-1, WP5: the dry-run / release-day driver SKELETON (NEW file; nothing frozen is edited).

It runs the frozen builder's stage G (catalog_builder/build_catalog.py, imported READ-ONLY; main()'s orchestration is
COPIED here, not edited) with the Amendment 15/16 pieces plugged in:
  * WP3  columns the base table lacks are joined by source_id (join_columns.py) from the tables the manifest names;
  * WP4  cut 12 = the union over the manifest's counted nss_* tables (cut12_nss_union.py) -> the non_single_star flag;
  * WP1  cut 13 = the literal criterion (PRIMARY) or the orbit-aware bound (VARIANT) on a neighbour catalogue
         (cut13_allsource.py; on DR3 the extract can stand in for the neighbour table -- a code-path test only);
  * a column the manifest maps to nothing, or to a missing column, makes its cut UNIMPLEMENTABLE (Amendment 15(d)): the
    cut is disabled (the column is set to a value that passes it), the run proceeds, and the report FLAGS it -- never a
    substitute quantity;
  * each base (primary / allsource_15c) has its OWN correlation cache (<extract>/stage_G_corr_<variant>.npz), because the
    frozen builder overwrites its single cache instead of merging (found in WP3);
  * NETWORK: a socket guard is installed unless --allow-network is given; offline, correlations come from the on-disk
    caches (the per-variant file if present, else the union of the builder's two files), uncovered ids get zero correlation
    and are counted.
Run:
  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/dry_run_driver.py --self-test          (DR3, offline, ~20 s)
  python3 .../dry_run_driver.py --release dr3 --variant primary --cut13 extract-literal   (a single offline run)
DR3 numbers are code-path tests, never results (Amendment 7(e)).

AMENDMENT 18 TOOLING (added 2026-09-30, NEW CODE ONLY; every default reproduces the behaviour above byte for byte; design SEED_SWEEP_DESIGN_FROZEN.md, be8a6405d):
  --seed-offset k   build k of a seed sweep: the stage-G velocity-error MC is seeded SEED + k and passed EXPLICITLY (vt_error_mc's seed is a default argument bound at import, so patching
                    build_catalog.SEED alone would not move it); the build has its OWN correlation cache <extract>/seed_k<k>/stage_G_corr_<variant>.npz (never the primary's or the builder's shared one);
                    stages E and F of build k come from --stage-dir (seeded_build.py rebuilds them; the driver itself only re-seeds G);
  --stage-dir DIR   the directory holding this build's stage_F.npz (default: the extract, i.e. the primary's own);
  --out-csv PATH    write the final catalogue (the default prints the report only).
  Online (--allow-network) a build k > 0 fetches only the correlation ids its cache (primed from the primary's file, read-only) lacks (fetch_correlations_delta).

CONES-BASED CUT 13 (added 2026-09-30, NEW CODE ONLY, OFFLINE; design CONES_CUT13_DESIGN_FROZEN.md, 9ea1d20e7; every default unchanged):
  --cut13 cones-literal | cones-orbit   the WP1 all-source search on neighbour cones (cones_cut13.ConeTable) instead of the extract stand-ins: literal = PRIMARY (Amendment 16(b)), orbit-aware = VARIANT
  --neighbours FITS  --neighbour-pairs CSV   (repeatable, matched in order) the Q1 neighbour table(s) and the pairs file whose row index is their pair_id
  --missing-cones error | extract-fallback   a pair that reaches cut 13 without a cone raises ConeCoverageError (default); 'extract-fallback' (a labelled DR3 code-path option) uses the builder's own flags for it and reports the counts
  --dump-candidates PATH   write the pairs that reach cut 13 (source_id1, source_id2) so a Q1 can be planned on them
  The report gains a 'cut13_cones' block only when a cones kind is used.

DR4 RELEASE-DAY TOOLING (added 2026-10-01, NEW CODE ONLY, OFFLINE-TESTED; design DR4_Q1_TOOLING_DESIGN_FROZEN.md, 6742d206d; every default unchanged):
  --corr-transport async|sync   how stage G's correlations are fetched when --allow-network is given: async (default) = the frozen builder's own fetch_correlations; sync = fetch_correlations_sync, the SAME SELECT run
                                SYNCHRONOUSLY in chunks of at most 1,999 ids (a result of exactly 2,000 rows would be indistinguishable from the endpoint's silent truncation), 120 s alarm, three attempts, every id must come back.
                                A run that uses it records `correlation_transport`, the calls, ids and the largest chunk in its report (and must be recorded in the release manifest).
  --neighbours-manifest PATH    a JSON list of {table, neighbours, pairs, include}: the entries with include true are used as --neighbours / --neighbour-pairs, and the report records which tables were included or left out
                                (the Amendment 16(b) release-day decision on crowded_field_source / gaia_source_environment as one recorded switch).
"""
import sys
sys.dont_write_bytecode = True
import argparse, contextlib, csv, hashlib, io, json, signal, socket, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
REF_SHA_DR3 = "6fff64d964ebaa72"                                  # the on-disk wide_binaries_dr3.csv (WP3 R0), prefix


class NoNetwork(RuntimeError):
    pass


def install_guard():
    def _blocked(*a, **k):
        raise NoNetwork("network access attempted without --allow-network (blocked by design)")
    socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked


# the modules are imported only after the guard decision (see main)
B = cut13 = join_by_source_id = W4 = None


def extract_dir(release, variant):
    base = REPO / "real_research" / "data" / "widebinaries"
    return base / (f"{release}_extract" if variant == "primary" else f"{release}_extract_{variant}")


def corr_cache_path(ext, variant):
    return ext / f"stage_G_corr_{variant}.npz"


def build_dir(ext, k):
    """the per-build directory of seed-sweep build k (gitignored with the extract)."""
    return ext / f"seed_k{int(k)}"


def corr_cache_path_k(ext, variant, k):
    """build k's OWN correlation cache: k = 0 is the current per-variant path (unchanged); k > 0 a file in build k's directory, never shared."""
    return corr_cache_path(ext, variant) if not k else build_dir(ext, k) / f"stage_G_corr_{variant}.npz"


_CORR_COLS = ("source_id", "parallax_pmra_corr", "parallax_pmdec_corr")


def _builder_corr_query(release, ids):
    """the builder's own correlation query text (build_catalog.fetch_correlations), for the ids given; networked."""
    from astroquery.gaia import Gaia
    got = {c: [] for c in _CORR_COLS}
    for j in range(0, len(ids), 2000):
        chunk = ",".join(str(int(x)) for x in ids[j:j + 2000])
        r = Gaia.launch_job_async(f"SELECT source_id, parallax_pmra_corr, parallax_pmdec_corr FROM gaia{release}.gaia_source WHERE source_id IN ({chunk})").get_results()
        for c in got:
            got[c].append(np.array(r[c]))
    return {c: np.concatenate(v) for c, v in got.items()}


def fetch_correlations_delta(release, source_ids, cache, prime_from=None, query_fn=None):
    """a seed-sweep build's correlations: the ids already in `cache` (or in `prime_from`, the primary's file, READ-ONLY) are reused and ONLY the missing ids are queried; the merged table is
    written to `cache` (the build's own file).  The builder's fetch_correlations re-queries every id when one is missing and overwrites its file, which is why builds must not share one."""
    ids = np.unique(np.asarray(source_ids))
    have = {c: np.zeros(0, np.int64 if c == "source_id" else float) for c in _CORR_COLS}
    for f in (cache, prime_from):
        if f is not None and Path(f).exists():
            z = np.load(f)
            have = {c: np.concatenate([have[c], z[c]]) for c in _CORR_COLS}
    _, first = np.unique(have["source_id"], return_index=True)
    have = {c: have[c][first] for c in _CORR_COLS}
    missing = ids[~np.isin(ids, have["source_id"])]
    if len(missing):
        got = (query_fn or _builder_corr_query)(release, missing)
        have = {c: np.concatenate([have[c], np.asarray(got[c])]) for c in _CORR_COLS}
    Path(cache).parent.mkdir(parents=True, exist_ok=True)
    np.savez(cache, **have)
    return have


SYNC_IDS_PER_CALL = 1999                                     # a result of exactly 2,000 rows would be indistinguishable from the synchronous endpoint's silent truncation
SYNC_TIMEOUT_S = 120
_SYNC_STATS = dict(calls=0, ids=0, max_chunk=0)


class SyncTimeout(Exception):
    pass


def _sync_alarm(signum, frame):
    raise SyncTimeout(f"no answer within {SYNC_TIMEOUT_S} s")


def _gaia_sync(q, tries=3):
    """one SYNCHRONOUS archive query (astroquery's launch_job) with a hard SIGALRM timeout (main thread) and three attempts; returns the astropy Table.  Networked: the offline tests replace astroquery's Gaia object."""
    from astroquery.gaia import Gaia
    Gaia.ROW_LIMIT = -1
    for att in range(tries):
        old = signal.signal(signal.SIGALRM, _sync_alarm)
        signal.alarm(SYNC_TIMEOUT_S)
        try:
            r = Gaia.launch_job(q).get_results()
            signal.alarm(0)
            return r
        except Exception as exc:
            signal.alarm(0)
            print(f"  sync correlation query attempt {att + 1} failed ({type(exc).__name__}: {str(exc)[:120]}); retrying in {20 * (att + 1)} s", flush=True)
            time.sleep(20 * (att + 1))
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old)
    raise RuntimeError("a synchronous correlation query failed 3 times")


def _sync_corr_query(release, ids, query=None):
    """the builder's correlation SELECT (build_catalog.fetch_correlations, the same text), run SYNCHRONOUSLY in chunks of at most SYNC_IDS_PER_CALL ids; every requested id must come back (otherwise it raises: the builder would only fail later, on
    a KeyError in vt_error_mc); returns the arrays sorted by source_id.  `query` replaces the network call (offline tests)."""
    query = query or _gaia_sync
    ids = np.unique(np.asarray(ids))
    got = {c: [] for c in _CORR_COLS}
    for j in range(0, len(ids), SYNC_IDS_PER_CALL):
        chunk_ids = ids[j:j + SYNC_IDS_PER_CALL]
        chunk = ",".join(str(int(x)) for x in chunk_ids)
        r = query(f"SELECT source_id, parallax_pmra_corr, parallax_pmdec_corr FROM gaia{release}.gaia_source WHERE source_id IN ({chunk})")
        _SYNC_STATS["calls"] += 1; _SYNC_STATS["ids"] += int(len(chunk_ids)); _SYNC_STATS["max_chunk"] = max(_SYNC_STATS["max_chunk"], int(len(chunk_ids)))
        if len(r) != len(chunk_ids) or not np.array_equal(np.sort(np.array(r["source_id"])), chunk_ids):
            raise RuntimeError(f"the synchronous correlation query returned {len(r)} rows for {len(chunk_ids)} requested ids (missing or extra ids): stopping, nothing is repaired")
        for c in got:
            got[c].append(np.array(r[c]))
    if not got["source_id"]:
        return {c: np.zeros(0, np.int64 if c == "source_id" else np.float32) for c in _CORR_COLS}
    out = {c: np.concatenate(v) for c, v in got.items()}
    o = np.argsort(out["source_id"], kind="stable")
    return {c: v[o] for c, v in out.items()}


def fetch_correlations_sync(release, source_ids, cache, query=None):
    """the sync fallback with the frozen builder's fetch_correlations semantics: a cache that holds every id is used as it is; else the correlations are fetched by _sync_corr_query and saved (np.savez) to `cache`."""
    _SYNC_STATS.update(calls=0, ids=0, max_chunk=0)
    if Path(cache).exists():
        z = np.load(cache)
        if np.isin(source_ids, z["source_id"]).all():
            return {k: z[k] for k in z.files}
    out = _sync_corr_query(release, source_ids, query=query)
    np.savez(cache, **out)
    return out


def offline_correlations(ext, variant, note, cache_file=None):
    """cache-only correlation source (never queries): the variant's own file if it exists, else the union of the builder's
    two on-disk files; uncovered ids get zero correlation and are counted in `note`."""
    def fetch(release, source_ids, cache):
        if cache_file is not None and Path(cache_file).exists():                  # a seed-sweep build's own cache (new)
            files = [Path(cache_file)]
        else:
            files = [corr_cache_path(ext, variant)] if corr_cache_path(ext, variant).exists() else \
                [ext / "stage_G_corr.npz", ext / "stage_G_corr_elbadry.npz"]
        zs = [np.load(f) for f in files if f.exists()]
        cols = ("parallax_pmra_corr", "parallax_pmdec_corr")
        sid = np.concatenate([z["source_id"] for z in zs]) if zs else np.zeros(0, np.int64)
        u, first = np.unique(sid, return_index=True)
        ids = np.unique(np.asarray(source_ids))
        pos = np.clip(np.searchsorted(u, ids), 0, max(len(u) - 1, 0))
        hit = (len(u) > 0) & (u[pos] == ids) if len(u) else np.zeros(len(ids), bool)
        out = {"source_id": ids}
        for c in cols:
            allv = np.concatenate([z[c] for z in zs]) if zs else np.zeros(0)
            v = np.zeros(len(ids))
            v[hit] = allv[first[pos[hit]]]
            out[c] = v
        note.append(dict(files=[f.name for f in files], n_uncovered=int((~hit).sum())))
        return out
    return fetch


NEUTRAL = {"ruwe": 0.0, "ipd_frac_multi_peak": 0, "radial_velocity": np.nan, "radial_velocity_error": np.nan,
           "non_single_star": 0}                                   # values that PASS the cut that reads the column
CUT_OF = {"ruwe": "RUWE<1.4 both", "ipd_frac_multi_peak": "ipd_frac_multi_peak<=2 both", "radial_velocity": "RV screen",
          "radial_velocity_error": "RV screen", "non_single_star": "NSS screen"}


def apply_manifest_columns(S, manifest, report):
    """WP3 + the UNIMPLEMENTABLE rule for the columns the frozen cuts read.  A mapping of None or to a column absent from
    the named table disables that cut (value that passes it) and flags it; a mapping to another table joins by source_id."""
    cols = (manifest or {}).get("columns") or {}
    S = dict(S)
    for col in ("ruwe", "ipd_frac_multi_peak", "radial_velocity", "radial_velocity_error"):
        spec = cols.get(col)
        if not isinstance(spec, dict) or spec.get("confirmed") in (None, "base") and not spec.get("unavailable"):
            continue                                               # not declared -> the base table's own column is used
        if spec.get("unavailable"):
            S[col] = np.full(len(S["source_id"]), NEUTRAL[col], dtype=float if isinstance(NEUTRAL[col], float) else int)
            report["unimplementable"].append(dict(column=col, cut=CUT_OF[col], reason=spec.get("reason", "not in DR4")))
            continue
        tab_file = spec.get("join_file")
        if tab_file:
            z = dict(np.load(tab_file))
            if col not in z:
                S[col] = np.full(len(S["source_id"]), NEUTRAL[col], dtype=float if isinstance(NEUTRAL[col], float) else int)
                report["unimplementable"].append(dict(column=col, cut=CUT_OF[col], reason=f"{col!r} absent from {Path(tab_file).name}"))
                continue
            base = {k: v for k, v in S.items() if k != col}
            S, rep = join_by_source_id(base, [(Path(tab_file).name, z)], [col])
            report["joins"][col] = rep["columns"][col]
    return S


def stage_g(S, F, ext, variant, release, third, correlations_note, allow_network, seed_offset=0, cache_path=None, candidates_out=None, corr_transport="async"):
    """frozen stage G as build_catalog.main() runs it (COPIED), with `third` supplied (cut 13) and the per-variant cache."""
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    if candidates_out is not None:                                                  # the pairs that reach cut 13 (new option only)
        with open(candidates_out, "w") as fh:
            fh.write("source_id1,source_id2\n")
            for x, y in zip(S["source_id"][F["a"][idx]].tolist(), S["source_id"][F["b"][idx]].tolist()):
                fh.write(f"{int(x)},{int(y)}\n")
    extra["third"][idx] = third(S, F["a"][idx], F["b"][idx])
    pre2, _, tab0 = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    sync_fb = bool(allow_network and corr_transport == "sync")
    if sync_fb:                                                                    # the SYNC fallback (DR4 tooling): the same SELECT, a different transport
        _SYNC_STATS.update(calls=0, ids=0, max_chunk=0)
        if seed_offset:
            fetch = lambda rel, ids, cache: fetch_correlations_delta(rel, ids, cache, prime_from=corr_cache_path(ext, variant), query_fn=_sync_corr_query)
        else:
            fetch = fetch_correlations_sync
    elif allow_network and seed_offset:                                            # a sweep build: delta fetch into its own cache
        fetch = lambda rel, ids, cache: fetch_correlations_delta(rel, ids, cache, prime_from=corr_cache_path(ext, variant))
    else:
        fetch = B.fetch_correlations if allow_network else offline_correlations(ext, variant, correlations_note, cache_file=cache_path)
    corr = fetch(release, np.concatenate([S["source_id"][F["a"][idx2]], S["source_id"][F["b"][idx2]]]),
                 cache_path if cache_path is not None else corr_cache_path(ext, variant))
    if sync_fb:
        correlations_note.append(dict(transport="sync (driver fallback, the builder's SELECT, at most %d ids per call)" % SYNC_IDS_PER_CALL, calls=_SYNC_STATS["calls"], ids=_SYNC_STATS["ids"],
                                      max_ids_per_call=_SYNC_STATS["max_chunk"], from_cache=bool(_SYNC_STATS["calls"] == 0)))
    if seed_offset:                                                                 # build k > 0: the G seed SEED + k, passed explicitly
        sig_vt = B.vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr, seed=B.SEED + int(seed_offset))
    else:
        sig_vt = B.vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr)
    from wide_binary_pipeline import G as GN, MSUN, AU
    vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
    ok = np.zeros(len(F["a"]), bool)
    ok[idx2] = sig_vt <= 0.1 * np.maximum(1.0, (tab0["v_perp_kms"][idx2] / vc0) / 2)
    extra["vt_err_ok"] = ok
    z = B.av_sfd98(S, ext / "AV_sfd98.npz")
    if z is not None:
        extra["AV_ok"] = (z["av"][F["a"]] < 0.5) & (z["av"][F["b"]] < 0.5)
    keepG, flow, table = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    cols = list(table)
    w.writerow(cols)
    for i in np.flatnonzero(keepG):
        w.writerow([table[c][i] for c in cols])
    return buf.getvalue().encode(), flow


def third_function(kind, S, cones=None, missing="error"):
    """cut 13 source: 'extract-builder' (the frozen builder's own function), 'extract-orbit' / 'extract-literal' (cut13.py on
    the extract as a stand-in neighbour catalogue: code path only; the real search is WP1's all-source cones)."""
    if kind in ("cones-literal", "cones-orbit"):
        if cones is None:
            raise ValueError("a cones kind needs a ConeTable (--neighbours / --neighbour-pairs)")
        mode = "literal" if kind == "cones-literal" else "orbit"

        def fn(S_, a, b):
            flags, info = cones.flags(S_, a, b, mode=mode, missing=missing, fallback=lambda S__, a_, b_: B.third_star_flags(S__, a_, b_))
            fn.info = info
            return flags
        fn.info = None
        return fn
    if kind == "extract-builder":
        return lambda S_, a, b: B.third_star_flags(S_, a, b)
    fn = cut13.third_star_orbit_aware if kind == "extract-orbit" else cut13.third_star_literal
    return lambda S_, a, b: fn(S_, a, b).flags


def run(release, variant, cut13_kind, manifest, allow_network, seed_offset=0, stage_dir=None, cones=None, missing_cones="error", dump_candidates=None, corr_transport="async"):
    ext = extract_dir(release, variant)
    cache_path = corr_cache_path_k(ext, variant, seed_offset) if seed_offset else None
    report = {"release": release, "variant": variant, "cut13": cut13_kind, "extract": ext.name,
              "correlation_cache": (cache_path or corr_cache_path(ext, variant)).name, "unimplementable": [], "joins": {},
              "network_allowed": bool(allow_network)}
    if seed_offset or stage_dir:                                                    # keys added ONLY for a sweep build, so the default report is unchanged
        report.update(seed_offset=int(seed_offset), stage_F_dir=str(stage_dir or ext.name), stage_G_seed=(B.SEED + int(seed_offset)) if seed_offset else "default (SEED)",
                      correlation_cache_dir=(cache_path.parent.name if cache_path else ext.name))
    S = dict(np.load(ext / "stage_A.npz"))
    F = dict(np.load(Path(stage_dir or ext) / "stage_F.npz"))
    S = apply_manifest_columns(S, manifest, report)
    note = []
    third_fn = third_function(cut13_kind, S, cones, missing_cones)
    with contextlib.redirect_stdout(io.StringIO()):
        csv_bytes, flow = stage_g(S, F, ext, variant, release, third_fn, note, allow_network, seed_offset=seed_offset, cache_path=cache_path, candidates_out=dump_candidates, corr_transport=corr_transport)
    if getattr(third_fn, "info", None) is not None:                                 # only for a cones kind
        report["cut13_cones"] = third_fn.info
    if corr_transport != "async":                                                   # key added ONLY when the sync fallback was requested, so the default report is unchanged
        report["correlation_transport"] = corr_transport
    report.update(n_pairs=csv_bytes.count(b"\n") - 1, sha256=hashlib.sha256(csv_bytes).hexdigest(), cut_flow=flow,
                  correlations=note)
    return csv_bytes, report


def self_test():
    res, log = {}, []
    def T(name, ok, detail=""):
        res[name] = bool(ok)
        line = f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else "")
        print(line)
        log.append(line)
    t0 = time.time()
    try:
        socket.create_connection(("gea.esac.esa.int", 443), timeout=1)
        T("S0 the socket guard blocks outgoing connections", False)
    except NoNetwork:
        T("S0 the socket guard blocks outgoing connections", True)
    ext = extract_dir("dr3", "primary")
    p1, p2 = corr_cache_path(ext, "primary"), corr_cache_path(extract_dir("dr3", "allsource_15c"), "allsource_15c")
    T("S1 each base has its own correlation cache path, never the builder's shared stage_G_corr.npz",
      p1 != p2 and p1.name != "stage_G_corr.npz" and p2.name != "stage_G_corr.npz", f"{p1.parent.name}/{p1.name} vs {p2.parent.name}/{p2.name}")
    b0, r0 = run("dr3", "primary", "extract-builder", None, False)
    T("S2 the driver's copied stage G with the builder's own cut 13 reproduces the reference DR3 CSV byte-identically",
      r0["sha256"].startswith(REF_SHA_DR3), f"{r0['n_pairs']:,d} pairs, sha256 {r0['sha256'][:16]}; correlations {r0['correlations']}")
    b1, r1 = run("dr3", "primary", "extract-orbit", None, False)
    T("S3 cut13.py's orbit-aware variant on the extract reproduces the builder's cut 13 exactly (same CSV)", b1 == b0,
      f"{r1['n_pairs']:,d} pairs")
    b2, r2 = run("dr3", "primary", "extract-literal", None, False)
    T("S4 (reported) the literal PRIMARY criterion on the extract runs end to end", r2["n_pairs"] > 0,
      f"{r2['n_pairs']:,d} pairs (orbit-aware {r1['n_pairs']:,d}); a code-path number, not a result")
    man = {"columns": {"ruwe": {"confirmed": "a table without it", "unavailable": True, "reason": "planted mis-mapping (test)"}}}
    b3, r3 = run("dr3", "primary", "extract-builder", man, False)
    T("S5 (planted control) a column the manifest marks unavailable makes its cut UNIMPLEMENTABLE: flagged, disabled, run completes",
      any(u["cut"] == "RUWE<1.4 both" for u in r3["unimplementable"]) and b3 != b0 and r3["n_pairs"] >= r0["n_pairs"],
      f"unimplementable {r3['unimplementable']}; {r3['n_pairs']:,d} pairs (reference {r0['n_pairs']:,d})")
    tmp = HERE / "_selftest_tmp_join.npz"
    try:
        S = dict(np.load(ext / "stage_A.npz"))
        rng = np.random.default_rng(1)
        perm = rng.permutation(len(S["source_id"]))
        np.savez(tmp, source_id=S["source_id"][perm], ipd_frac_multi_peak=S["ipd_frac_multi_peak"][perm])
        man6 = {"columns": {"ipd_frac_multi_peak": {"confirmed": "second table", "join_file": str(tmp)}}}
        b6, r6 = run("dr3", "primary", "extract-builder", man6, False)
        T("S6 (WP3 inside the driver) a column joined from a second table by source_id leaves the CSV byte-identical", b6 == b0,
          f"join report {r6['joins'].get('ipd_frac_multi_peak')}")
    finally:
        if tmp.exists():
            tmp.unlink()
    ok = all(res.values())
    print(f"\n{sum(res.values())}/{len(res)} pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - t0:.0f} s)")
    out = dict(results=res, reference=r0, orbit=r1, literal=r2, planted_unimplementable=r3, join=r6 if 'r6' in dir() else None)
    (HERE / "dry_run_driver_selftest_results.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    (HERE / "dry_run_driver_selftest.out").write_text("\n".join(log) + f"\n{sum(res.values())}/{len(res)} pass\n")
    return 0 if ok else 1


def init(allow_network=False):
    """install the socket guard (unless networked) and import the frozen builder and the WP1/WP3/WP4 modules READ-ONLY (what main() does; reusable by seed_sweep.py)."""
    global B, cut13, join_by_source_id, W4
    if not allow_network:
        install_guard()
    sys.path.insert(0, str(PREP / "catalog_builder"))
    sys.path.insert(0, str(PREP))
    sys.path.insert(0, str(PREP / "catalog_builder_dr4"))
    sys.path.insert(0, str(HERE))
    import build_catalog as _B
    import cut13 as _c13
    from join_columns import join_by_source_id as _j
    import cut12_nss_union as _w4
    B, cut13, join_by_source_id, W4 = _B, _c13, _j, _w4


def main():
    global B, cut13, join_by_source_id, W4
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--release", choices=("dr3", "dr4"), default="dr3")
    ap.add_argument("--variant", choices=("primary", "allsource_15c"), default="primary")
    ap.add_argument("--cut13", choices=("extract-builder", "extract-orbit", "extract-literal", "cones-literal", "cones-orbit"), default="extract-literal")
    ap.add_argument("--neighbours", action="append", default=[], help="Q1 neighbour FITS (repeatable, matched in order with --neighbour-pairs)")
    ap.add_argument("--neighbour-pairs", action="append", default=[], help="pairs CSV (source_id1, source_id2) whose row index is the FITS pair_id")
    ap.add_argument("--missing-cones", choices=("error", "extract-fallback"), default="error")
    ap.add_argument("--dump-candidates", default=None, help="write the pairs that reach cut 13 here")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--allow-network", action="store_true", help="off by default: without it every connection raises")
    ap.add_argument("--seed-offset", type=int, default=0, help="Amendment 18 seed sweep: build k (stage-G seed SEED + k, own correlation cache); 0 = the frozen seeds, unchanged")
    ap.add_argument("--stage-dir", default=None, help="the directory holding this build's stage_F.npz (default: the extract)")
    ap.add_argument("--out-csv", default=None, help="write the final catalogue here")
    ap.add_argument("--corr-transport", choices=("async", "sync"), default="async", help="stage G's correlation fetch with --allow-network: the builder's own async fetch (default) or the driver's sync fallback (same SELECT, at most 1,999 ids per call)")
    ap.add_argument("--neighbours-manifest", default=None, help="JSON list of {table, neighbours, pairs, include}: the entries with include true are used as --neighbours / --neighbour-pairs; the report records the choice")
    args = ap.parse_args()
    if args.corr_transport == "sync" and not args.allow_network:
        raise SystemExit("--corr-transport sync only matters with --allow-network (offline, the correlations come from the on-disk caches)")
    init(args.allow_network)
    if args.self_test:
        return self_test()
    manifest = json.loads(Path(args.manifest).read_text()) if args.manifest else None
    nm_report = None
    if args.neighbours_manifest:
        nm_text = Path(args.neighbours_manifest).read_bytes()
        entries = json.loads(nm_text)
        for e in entries:
            if e.get("include") is True:
                args.neighbours.append(e["neighbours"]); args.neighbour_pairs.append(e["pairs"])
        nm_report = dict(path=str(args.neighbours_manifest), sha256=hashlib.sha256(nm_text).hexdigest(), included=[e["table"] for e in entries if e.get("include") is True],
                         left_out=[e["table"] for e in entries if e.get("include") is not True])
    cones = None
    if args.cut13.startswith("cones-"):
        import cones_cut13
        if not args.neighbours or len(args.neighbours) != len(args.neighbour_pairs):
            raise SystemExit("a cones kind needs --neighbours and --neighbour-pairs, repeated the same number of times")
        cones = cones_cut13.ConeTable.from_files(zip(args.neighbours, args.neighbour_pairs))
    csv_bytes, report = run(args.release, args.variant, args.cut13, manifest, args.allow_network, seed_offset=args.seed_offset, stage_dir=args.stage_dir, cones=cones, missing_cones=args.missing_cones,
                            dump_candidates=args.dump_candidates, corr_transport=args.corr_transport)
    if nm_report is not None:
        report["neighbours_manifest"] = nm_report
    if args.out_csv:
        Path(args.out_csv).write_bytes(csv_bytes)
    print(json.dumps(report, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
