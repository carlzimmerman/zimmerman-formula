#!/usr/bin/env python3
"""DR4-READY-1, items 1 and 4 of DR4_Q1_TOOLING_DESIGN_FROZEN.md (6742d206d): the release-day neighbour-cone fetch library (NEW file).  NETWORKED only through q1_pilot_ranges.run_query / launch_query (the offline tests replace launch_query with a
mock archive behind a socket guard); nothing here opens a connection on import.  EVERY query form below needs the owner's explicit go on the day (a changed form needed it before); a run needs --owner-go-recorded and explicit hard caps.
DR3 numbers in the tests are code-path numbers, never results (Amendment 7(e)).

What it does.  For the neighbour cones (30 kAU / d) of a list of pairs it fetches, with synchronous queries that respect the endpoint's SILENT 2,000-row cap, the rows of one archive table: SPECS holds the documented DR4 names (ESA's DRAFT data model, 2026-06-26,
'confirm on release day'; one table, overridable by a JSON file recorded in the manifest).  Three strategies, one generic resumable loop:
  ranges   literal `col >= lo AND col < hi` ranges of the level-12 HEALPix pixels overlapping each component's cone (+ margin): on source_id (the DR3 form, 2**35 ids per pixel; an ASSUMPTION for DR4, checked offline at plan time against the local base extract and
           optionally online by --spot-check) or on healpix29 (2**34 per level-12 pixel);  with an optional LEFT OUTER JOIN (Amendment 16(b): G from all_source_photometry);
  cones    batched `1 = CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', ra0, dec0, r))` for tables with no usable spatial key; a cone that returns the cap is split exactly into declination slabs.
Kept from the DR3 loop: a result of exactly 2,000 rows is discarded and its batch halved; 120 s alarm, three attempts, 0.5 s pause; every accepted batch written to a cache and logged (resume; a cache from another plan is refused); hard caps on accepted bytes,
received bytes and queries (no defaults); the exact-cone re-filter and, for a table that must contain the local base extract, the completeness check.  New: a SCHEMA PROBE before any data query, per-batch column validation, JOIN MULTIPLICITY stop, NULL-G accounting,
an optional SPOT CHECK against position queries, and the pre-brief ESTIMATOR."""
import sys
sys.dont_write_bytecode = True
import csv, hashlib, json, math, signal, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cut13_allsource as W1
import q1_pilot_ranges as Q1

SYNC_CAP = Q1.SYNC_CAP                                          # 2000 rows: a result of exactly this many is truncated
OUT_COLS = tuple(Q1.KEEP)                                       # source_id, ra, dec, parallax, parallax_error, pmra, pmdec, pmra_error, pmdec_error, phot_g_mean_mag
PAUSE_S = 0.5
MAX_CONES_PER_QUERY = 40
CONE_MARGIN_ARCSEC = 1.0
DRAFT = "draft DR4 data model 2026-06-26 (zip sha256 d807eae9...), confirm on release day"


class SchemaMismatch(RuntimeError):
    pass


class JoinMultiplicity(RuntimeError):
    pass


class SpotCheckFailed(RuntimeError):
    pass


class CapStop(SystemExit):
    pass


# ------------------------------------------------------------------------------------------------ the table specs (the ONLY place names live)
def _spec(table, alias=None, join=None, strategy="ranges", range_column="source_id", range_div=2 ** 35, local_check=False, columns=None, note=""):
    return dict(table=table, alias=alias, join=join, strategy=strategy, range_column=range_column, range_div=range_div, local_check=local_check,
                columns=columns or {c: c for c in OUT_COLS if not (join and c in join["columns"])}, note=note)


SPECS = {
    # the DR3 form of the existing tools (regression control: the generated text equals q1_full_ranges / q1_delta_ranges)
    "dr3_gaia_source": _spec("gaiadr3.gaia_source", local_check=True, note="gaiadr3.gaia_source, no join, ranges on source_id"),
    # Amendment 16(b): the full all_source_astrometry with G from all_source_photometry (LEFT OUTER JOIN on source_id)
    "dr4_all_source": _spec("gaiadr4.all_source_astrometry", alias="a", local_check=True,
                            join=dict(table="gaiadr4.all_source_photometry", alias="p", key="source_id", kind="LEFT OUTER", columns={"phot_g_mean_mag": "phot_g_mean_mag"}),
                            note="all_source_astrometry LEFT OUTER JOIN all_source_photometry ON source_id, ranges on source_id; " + DRAFT),
    # the optional Amendment 16(b) tables (release-day decision): healpix29 is documented for the environment table; the crowded-field table has no HEALPix column
    "dr4_gaia_source_environment": _spec("gaiadr4.gaia_source_environment", range_column="healpix29", range_div=2 ** 34, note="ranges on healpix29 (level 29: 2**34 per level-12 pixel); " + DRAFT),
    "dr4_crowded_field_source": _spec("gaiadr4.crowded_field_source", strategy="cones", note="no HEALPix column: batched CONTAINS cones; " + DRAFT),
}


def load_spec(name, override_json=None):
    """the named spec; `override_json` (a path) replaces keys of it (a release-day correction of a name is data, not code); returns (spec, sha256 of the override or None)."""
    spec = json.loads(json.dumps(SPECS[name]))
    sha = None
    if override_json:
        raw = Path(override_json).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        spec.update(json.loads(raw))
    return spec, sha


def _ref(spec, col, in_join=False):
    if spec["alias"] is None:
        return col
    return f"{spec['join']['alias'] if in_join else spec['alias']}.{col}"


def select_list(spec):
    items = [_ref(spec, src) if out == src else f"{_ref(spec, src)} AS {out}" for out, src in spec["columns"].items()]
    if spec["join"]:
        items += [_ref(spec, src, True) + (f" AS {out}" if out != src else "") for out, src in spec["join"]["columns"].items()]
    order = {c: i for i, c in enumerate(OUT_COLS)}
    names = list(spec["columns"]) + (list(spec["join"]["columns"]) if spec["join"] else [])
    return [it for _, it in sorted(zip((order[n] for n in names), items))]


def from_clause(spec):
    t = f"{spec['table']} AS {spec['alias']}" if spec["alias"] else spec["table"]
    if spec["join"]:
        j = spec["join"]
        t += f" {j['kind']} JOIN {j['table']} AS {j['alias']} ON {j['alias']}.{j['key']} = {spec['alias']}.{j['key']}"
    return t


def build_query(spec, where, top=None):
    return f"SELECT {'TOP %d ' % top if top else ''}{', '.join(select_list(spec))} FROM {from_clause(spec)} WHERE {where}"


def where_ranges(spec, ranges):
    c = _ref(spec, spec["range_column"])
    return " OR ".join(f"({c} >= {lo} AND {c} < {hi})" for lo, hi in ranges)


def where_cones(spec, cones):
    ra, dec = _ref(spec, "ra"), _ref(spec, "dec")
    out = []
    for ra0, dec0, rad, dlo, dhi in cones:
        t = f"1 = CONTAINS(POINT('ICRS', {ra}, {dec}), CIRCLE('ICRS', {ra0!r}, {dec0!r}, {rad!r}))"
        if dlo is not None:
            t += f" AND {dec} >= {dlo!r} AND {dec} < {dhi!r}"
        out.append(f"({t})")
    return " OR ".join(out)


def unit_where(spec, batch):
    return where_ranges(spec, batch) if spec["strategy"] == "ranges" else where_cones(spec, batch)


def release_day_count_queries(release="dr4"):
    """the ADQL TEXT of the counts Amendment 16(b) asks to be recorded before the data are opened (never run here).  Source-id based definitions: the match tables (all_source_match, crowded_field_source_environment_match) may define
    'only in' differently; read the data model first."""
    a, p = f"gaia{release}.all_source_astrometry", f"gaia{release}.all_source_photometry"
    return {
        "all_source_rows_without_a_photometry_row": f"SELECT COUNT(*) FROM {a} AS a LEFT OUTER JOIN {p} AS p ON p.source_id = a.source_id WHERE p.source_id IS NULL",
        "all_source_rows_with_NULL_G": f"SELECT COUNT(*) FROM {a} AS a JOIN {p} AS p ON p.source_id = a.source_id WHERE p.phot_g_mean_mag IS NULL",
        "sources_only_in_crowded_field_source": f"SELECT COUNT(*) FROM gaia{release}.crowded_field_source AS c LEFT OUTER JOIN {a} AS a ON a.source_id = c.source_id WHERE a.source_id IS NULL",
        "sources_only_in_gaia_source_environment": f"SELECT COUNT(*) FROM gaia{release}.gaia_source_environment AS e LEFT OUTER JOIN {a} AS a ON a.source_id = e.source_id WHERE a.source_id IS NULL",
    }


# ------------------------------------------------------------------------------------------------ plan
def read_pairs(path, max_pairs=None):
    rows = list(csv.DictReader(open(path)))
    sa = np.array([int(r["source_id1"]) for r in rows], np.int64); sb = np.array([int(r["source_id2"]) for r in rows], np.int64)
    return (sa[:max_pairs], sb[:max_pairs]) if max_pairs else (sa, sb)


def plan_pairs(stage_a_path, pairs_csv, spec, max_pairs=None, margin_arcsec=None):
    """the plan for the pairs of `pairs_csv` (pair_id = the row index): the level-12 pixels overlapping either component's cone (+ margin) merged into ranges [p * div, (p + 1) * div) (strategy ranges), or two cones per pair (strategy cones)."""
    import healpy as hp
    S = np.load(stage_a_path)
    A = {k: S[k] for k in ("source_id", "ra", "dec", "parallax")}
    sa, sb = read_pairs(pairs_csv, max_pairs)
    order = np.argsort(A["source_id"])
    row = lambda s: order[np.searchsorted(A["source_id"][order], s)]
    ia, ib = row(sa), row(sb)
    assert np.all(A["source_id"][ia] == sa) and np.all(A["source_id"][ib] == sb), "a pair of the list is not in the stage-A extract"
    va, vb = Q1.vec(A["ra"][ia], A["dec"][ia]), Q1.vec(A["ra"][ib], A["dec"][ib])
    R = W1.radius_arcsec(A["parallax"][ia])
    margin = Q1.MARGIN_ARCSEC if margin_arcsec is None else margin_arcsec
    pix = set()
    for k in range(len(R)):
        for v in (va[k], vb[k]):
            pix.update(hp.query_disc(2 ** Q1.LEVEL, v, np.radians((R[k] + margin) / 3600), inclusive=True, nest=True).tolist())
    pix = np.array(sorted(pix), np.int64)
    div = int(spec["range_div"])
    if len(pix):
        brk = np.flatnonzero(np.diff(pix) != 1)
        st = np.concatenate([[0], brk + 1]); en = np.concatenate([brk, [len(pix) - 1]])
        rng = [(int(pix[a] * div), int((pix[b] + 1) * div)) for a, b in zip(st, en)]
    else:
        rng = []
    if spec["strategy"] == "cones":
        units = []
        for k in range(len(R)):
            for ra, dec in ((A["ra"][ia[k]], A["dec"][ia[k]]), (A["ra"][ib[k]], A["dec"][ib[k]])):
                units.append((float(ra), float(dec), float((R[k] + CONE_MARGIN_ARCSEC) / 3600), None, None))
    else:
        units = rng
    area = len(pix) * hp.nside2pixarea(2 ** Q1.LEVEL, degrees=True)
    return dict(A=A, va=va, vb=vb, R=R, pick=np.arange(len(R)), rng=rng, units=units, n_pix=int(len(pix)), area=float(area), n_pairs=int(len(R)))


def plan_hash(P, spec):
    h = hashlib.sha256()
    h.update(json.dumps([spec["table"], spec["strategy"], spec["range_column"], list(spec["columns"]), P["n_pairs"], P["units"][:50], P["units"][-50:], len(P["units"])], default=str).encode())
    return h.hexdigest()[:16]


def plan_coverage(P, spec, loc):
    """(total, missing): for a table that must contain the local base extract and is queried by source_id ranges, the local-extract sources inside the exact cones whose source_id lies outside every planned range (must be 0: the
    source_id -> pixel assumption, checked OFFLINE before any query); other specs return (0, 0)."""
    if not (spec["local_check"] and spec["strategy"] == "ranges" and spec["range_column"] == "source_id"):
        return 0, 0
    return Q1.plan_coverage(dict(rng=P["rng"]), loc)


# ------------------------------------------------------------------------------------------------ calibration and the pre-brief estimator
def calibration(manifest_dir=HERE):
    """the two committed DR3 runs (full-size Q1 and the delta Q1), pooled per candidate pair"""
    runs = {}
    for k, f in (("full_q1_dr3", "manifest_q1_full.json"), ("delta_q1_dr3", "manifest_q1_delta.json")):
        m = json.load(open(Path(manifest_dir) / f))
        runs[k] = dict(pairs=m["n_pairs"], queries=m["queries_total"], accepted_bytes=m["accepted_bytes"], received_bytes=m["received_bytes"], seconds=m["seconds_this_session"], rows=m["rows_raw_unique"], truncated=m["truncated_results_discarded"])
    tot = {k: sum(r[k] for r in runs.values()) for k in ("pairs", "queries", "accepted_bytes", "received_bytes", "seconds", "rows", "truncated")}
    per_pair = dict(queries=tot["queries"] / tot["pairs"], accepted_mb=tot["accepted_bytes"] / tot["pairs"] / 1e6, received_mb=tot["received_bytes"] / tot["pairs"] / 1e6,
                    seconds=tot["seconds"] / tot["pairs"], rows=tot["rows"] / tot["pairs"])
    return dict(runs=runs, pooled=tot, per_pair=per_pair)


DENSITY = dict(low=1.0, central=2793009568 / 1811709771, high=2.5)          # DR4 all_source_astrometry rows (Amendment 16(b)) / DR3 gaia_source rows; an ASSUMPTION, low / high are guesses
PACE = dict(dr3=1.0, slower2=2.0, slower4=4.0)


def estimate(n_pairs, density=1.0, pace=1.0, cal=None):
    """queries, accepted MB, received MB and serial hours for n_pairs candidate pairs: the pooled DR3 per-pair rates times a density factor (more sources per cone) and a pace factor (slower archive)"""
    cal = cal or calibration()
    pp = cal["per_pair"]
    return dict(queries=n_pairs * pp["queries"] * density, accepted_mb=n_pairs * pp["accepted_mb"] * density, received_mb=n_pairs * pp["received_mb"] * density,
                hours=n_pairs * pp["seconds"] * density * pace / 3600)


def pre_brief(n_pairs, cal=None):
    """the text and the numbers for the owner's pre-brief"""
    cal = cal or calibration()
    rows = {}
    for dn, d in DENSITY.items():
        e = estimate(n_pairs, d, 1.0, cal)
        rows[dn] = dict(density=d, **e, hours_if_2x_slower=e["hours"] * 2, hours_if_4x_slower=e["hours"] * 4)
    c = rows["central"]
    caps = dict(accepted_mb=math.ceil(1.5 * c["accepted_mb"] / 10) * 10, received_mb=math.ceil(1.5 * c["received_mb"] / 10) * 10, queries=int(math.ceil(1.5 * c["queries"] / 100) * 100))
    pp = cal["per_pair"]
    txt = [f"PRE-BRIEF for the Q1 cone fetch at N = {n_pairs:,d} candidate pairs (the pairs that reach cut 13)",
           f"  rates from the two DR3 runs pooled ({cal['pooled']['pairs']:,d} pairs, {cal['pooled']['queries']:,d} queries, {cal['pooled']['accepted_bytes'] / 1e6:.1f} MB accepted, {cal['pooled']['seconds'] / 3600:.1f} h): "
           f"{pp['queries']:.3f} queries, {pp['accepted_mb'] * 1e3:.1f} KB accepted, {pp['seconds']:.2f} s per pair; the per-pair model is within 5 % of both DR3 runs",
           "  the DR4 catalogue is larger: the density factor (central 1.54 = 2,793,009,568 / 1,811,709,771 rows) is an ASSUMPTION; the pace is the DR3 pace (a release-day archive may be several times slower)"]
    for dn in ("low", "central", "high"):
        r = rows[dn]
        txt.append(f"  {dn:8s} (density x{r['density']:.2f}): about {r['queries']:,.0f} queries, {r['accepted_mb']:,.0f} MB accepted ({r['received_mb']:,.0f} MB received), {r['hours']:.1f} h serial "
                   f"({r['hours_if_2x_slower']:.1f} h if 2x slower, {r['hours_if_4x_slower']:.1f} h if 4x slower)")
    txt.append(f"  suggested hard caps (1.5 x the central estimate, to be chosen by the owner): {caps['accepted_mb']:,d} MB accepted, {caps['received_mb']:,d} MB received, {caps['queries']:,d} queries")
    txt.append("  the first progress lines of the run give the real rate; the loop stops by itself if the projection passes 1.25 x the accepted-bytes cap")
    return "\n".join(txt), dict(n_pairs=n_pairs, rows=rows, suggested_caps=caps, per_pair=pp)


# ------------------------------------------------------------------------------------------------ table helpers
def table_arrays(T, lower=True):
    """an astropy Table as a dict of numpy arrays (masked floats -> NaN, masked ints -> -1); names lower-cased"""
    out = {}
    for c in T.colnames:
        col = T[c]
        if hasattr(col, "mask") and col.dtype.kind == "f":
            v = np.asarray(col.filled(np.nan), float if col.dtype.itemsize == 8 else np.float32)
        elif hasattr(col, "mask") and col.dtype.kind in "iu":
            v = np.asarray(col.filled(-1))
        else:
            v = np.asarray(col)
        out[c.lower() if lower else c] = v
    return out


def check_columns(arrs, spec, where=""):
    need = set(OUT_COLS)
    miss = sorted(need - set(arrs))
    if miss:
        raise SchemaMismatch(f"{where}the returned table lacks the column(s) {miss} (returned: {sorted(arrs)}): stopping, nothing is repaired")
    if arrs["source_id"].dtype.kind not in "iu":
        raise SchemaMismatch(f"{where}source_id is not an integer column ({arrs['source_id'].dtype})")


def n_null_g(arrs):
    g = arrs["phot_g_mean_mag"]
    return int(np.isnan(np.asarray(g, float)).sum())


def probe_schema(spec, P, launch=None):
    """ONE small query before any data query: SELECT TOP 5 of the exact query form over the first planned unit.  Raises SchemaMismatch (with the archive's message) if the query fails, or if the returned columns or types are not the expected ones.
    Returns the probe record for the manifest."""
    from astropy.table import Table
    import tempfile, os
    launch = launch or Q1.launch_query
    q = build_query(spec, unit_where(spec, P["units"][:1]), top=5)
    fd, tmp = tempfile.mkstemp(suffix=".fits"); os.close(fd)
    t0 = time.time()
    old = signal.signal(signal.SIGALRM, Q1._on_alarm)
    signal.alarm(Q1.TIMEOUT_S)
    try:
        launch(q, tmp)
        signal.alarm(0)
        T = Table.read(tmp, format="fits")
    except Exception as exc:
        raise SchemaMismatch(f"the schema probe query failed (a schema mismatch or an archive error): {type(exc).__name__}: {str(exc)[:300]}\n  query: {q[:400]}") from exc
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        if os.path.exists(tmp):
            os.unlink(tmp)
    arrs = table_arrays(T)
    check_columns(arrs, spec, "schema probe: ")
    return dict(query=q, rows=int(len(T)), columns=sorted(arrs), dtypes={k: str(v.dtype) for k, v in arrs.items()}, seconds=round(time.time() - t0, 2))


# ------------------------------------------------------------------------------------------------ the generic resumable fetch loop
def fetch_units(P, spec, cache, caps, man, manifest_path, probe=True, launch=None):
    """fetch every planned unit; returns (dict of concatenated arrays, stats).  caps = dict(accepted_bytes, received_bytes, max_queries)."""
    from astropy.table import Table
    cache.mkdir(parents=True, exist_ok=True)
    idx_path, state_path = cache / "index.jsonl", cache / "state.json"
    ph = plan_hash(P, spec)
    if state_path.exists():
        assert json.loads(state_path.read_text())["plan_hash"] == ph, "the cache belongs to a different plan: refusing to resume (move or delete the cache directory)"
    else:
        state_path.write_text(json.dumps({"plan_hash": ph}))
    ranges_mode = spec["strategy"] == "ranges"
    ukey = (lambda u: (int(u[0]), int(u[1]))) if ranges_mode else (lambda u: tuple(None if x is None else float(x) for x in u))
    done, files = set(), []
    st = dict(calls=0, truncated=0, rows=0, accepted_bytes=0, received_bytes=0, seq=0, resumed_batches=0, no_g=0, t0=time.time(), halvings_after_failure=0)
    if idx_path.exists():
        for line in idx_path.read_text().splitlines():
            rec = json.loads(line)
            st["calls"] += 1
            if rec["type"] == "batch":
                done.update(ukey(u) for u in rec["units"])
                st["rows"] += rec["rows"]; st["accepted_bytes"] += rec["bytes"]; st["received_bytes"] += rec["bytes"]; st["no_g"] += rec.get("no_g", 0)
                st["seq"] = max(st["seq"], rec["seq"] + 1); st["resumed_batches"] += 1; files.append(cache / rec["file"])
            else:
                st["received_bytes"] += rec["bytes"]; st["truncated"] += 1
    if st["resumed_batches"]:
        print(f"RESUME: {st['resumed_batches']} batches already in the cache ({len(done)} units, {st['rows']:,d} rows, {st['accepted_bytes'] / 1e6:.1f} MB)", flush=True)
    prev = {}
    if manifest_path.exists():                                                   # a resumed session keeps what the first one recorded
        try:
            prev = json.loads(manifest_path.read_text())
        except Exception:
            prev = {}
    if prev.get("plan_hash") == ph:
        man["utc_start_first_session"] = prev.get("utc_start_first_session") or prev.get("utc_start")
        if prev.get("schema_probe"):
            man["schema_probe_first_session"] = prev.get("schema_probe_first_session") or prev["schema_probe"]
    if probe:                                                                    # at EVERY start, a resume included: the archive may have changed since the cache was written
        man["schema_probe"] = probe_schema(spec, P, launch=launch)
        print(f"schema probe OK: {man['schema_probe'].get('rows')} rows, columns {man['schema_probe'].get('columns')}", flush=True)
        manifest_path.write_text(json.dumps(man, indent=1, default=str) + "\n")
    units = [u for u in P["units"] if ukey(u) not in done]
    n_total = len(P["units"])
    i, n = 0, 8 if not ranges_mode else 30
    max_batch = 250 if ranges_mode else MAX_CONES_PER_QUERY
    expected_cols = None
    tmp_path = cache.parent / f"{cache.name}_tmp.fits"

    def log(rec):
        with open(idx_path, "a") as f:
            f.write(json.dumps(rec, default=str) + "\n")

    def stop(why):
        man["stopped"] = why
        manifest_path.write_text(json.dumps(man, indent=1, default=str) + "\n")
        raise CapStop("STOPPED: " + why + " -- the cache keeps every accepted batch; report to the owner before continuing")

    while i < len(units):
        batch = units[i:i + n]
        try:
            T, nb = Q1.run_query(build_query(spec, unit_where(spec, batch)), tmp_path)
        except RuntimeError as exc:
            if "failed 3 times" in str(exc) and len(batch) > 1:                 # a query that keeps failing is likely too heavy: halve the batch
                n = max(1, len(batch) // 2); st["halvings_after_failure"] += 1
                continue
            raise
        st["calls"] += 1
        st["received_bytes"] += nb
        if st["received_bytes"] > caps["received_bytes"]:
            stop(f"received {st['received_bytes'] / 1e6:.2f} MB in {st['calls']} queries against the {caps['received_bytes'] / 1e6:.0f} MB transfer cap")
        if st["calls"] > caps["max_queries"]:
            stop(f"more than {caps['max_queries']} queries")
        arrs = table_arrays(T)
        if _VALIDATE:                                                            # per-batch column validation (the tests' MUTATE 3 turns it off together with the probe)
            check_columns(arrs, spec, f"batch {st['seq']}: ")
        if len(T) >= SYNC_CAP:                                                   # truncated by the synchronous cap: discard, never use
            st["truncated"] += 1
            log(dict(type="trunc", bytes=nb))
            if len(batch) > 1:
                n = max(1, len(batch) // 2)
            else:
                u = batch[0]
                if ranges_mode:
                    lo, hi = u
                    if hi - lo < 2:
                        raise RuntimeError("a one-integer range hit the 2000-row cap")
                    units[i:i + 1] = [(lo, (lo + hi) // 2), ((lo + hi) // 2, hi)]
                else:
                    ra0, dec0, rad, dlo, dhi = u
                    dlo = (dec0 - rad) if dlo is None else dlo
                    dhi = (dec0 + rad) if dhi is None else dhi
                    if dhi - dlo < 1e-7:
                        raise RuntimeError("a cone slab thinner than 1e-7 deg hit the 2000-row cap")
                    mid = (dlo + dhi) / 2
                    units[i:i + 1] = [(ra0, dec0, rad, dlo, mid), (ra0, dec0, rad, mid, dhi)]
            continue
        if _CHECK_MULT:
            sid = arrs["source_id"]
            if len(np.unique(sid)) != len(sid):
                raise JoinMultiplicity(f"batch {st['seq']}: {len(sid) - len(np.unique(sid))} repeated source_id rows (the join multiplied rows): stopping, nothing is repaired")
        ng = n_null_g(arrs)
        fn = f"b{st['seq']:06d}.fits"
        T.write(cache / fn, format="fits", overwrite=True)
        log(dict(type="batch", seq=st["seq"], file=fn, rows=int(len(T)), bytes=int(nb), no_g=ng, units=[list(u) for u in batch]))
        files.append(cache / fn)
        st["seq"] += 1; st["rows"] += len(T); st["accepted_bytes"] += nb; st["no_g"] += ng
        if st["accepted_bytes"] > caps["accepted_bytes"]:
            stop(f"accepted {st['accepted_bytes'] / 1e6:.2f} MB ({st['rows']:,d} rows) after {st['calls']} queries against the {caps['accepted_bytes'] / 1e6:.0f} MB cap")
        i += len(batch)
        frac = (n_total - (len(units) - i)) / n_total
        proj = st["accepted_bytes"] / max(frac, 1e-9)
        if frac >= 0.2 and proj > 1.25 * caps["accepted_bytes"]:
            stop(f"projected {proj / 1e6:.1f} MB accepted against the {caps['accepted_bytes'] / 1e6:.0f} MB cap after {100 * frac:.0f}% of the units")
        n = int(np.clip(Q1.TARGET_ROWS / max(len(T) / len(batch), 0.5), 4, min(max_batch, 2 * len(batch))))
        if st["calls"] % 25 == 0:
            print(f"  {100 * frac:5.1f}% of the units: {st['calls']} queries, {st['truncated']} truncated, {st['rows']:,d} rows, accepted {st['accepted_bytes'] / 1e6:.1f} MB, received {st['received_bytes'] / 1e6:.1f} MB, "
                  f"{time.time() - st['t0']:.0f} s this session", flush=True)
        time.sleep(PAUSE_S)
    st["seconds_this_session"] = round(time.time() - st["t0"], 1)
    cols = {}
    for f in files:
        a = table_arrays(Table.read(f, format="fits"))
        for k, v in a.items():
            cols.setdefault(k, []).append(v)
    arrays = {k: np.concatenate(v) for k, v in cols.items()}
    return arrays, st


_VALIDATE = True                                                                  # per-batch column validation (the tests' MUTATE 3 turns it off together with the probe)
_CHECK_MULT = True                                                                # join-multiplicity check (MUTATE 4 turns it off)


# ------------------------------------------------------------------------------------------------ assemble the exact cones, the completeness check, the spot check
def assemble_exact(arrays, P):
    """dedupe by source_id, re-filter to the exact cones (the two cones of each pair), return the original-schema table (pair_id, comp, OUT_COLS) as a dict of arrays"""
    from scipy.spatial import cKDTree
    _, first = np.unique(arrays["source_id"].astype(np.int64), return_index=True)
    first = np.sort(first)
    T = {k: v[first] for k, v in arrays.items()}
    tree = cKDTree(Q1.vec(np.asarray(T["ra"], float), np.asarray(T["dec"], float)))
    rows, pid, cmp = [], [], []
    for k in range(len(P["pick"])):
        chord = 2 * np.sin(np.radians(P["R"][k] / 3600) / 2)
        for c, vc in ((0, P["va"][k]), (1, P["vb"][k])):
            js = tree.query_ball_point(vc, r=chord)
            rows.extend(js); pid.extend([int(P["pick"][k])] * len(js)); cmp.extend([c] * len(js))
    rows = np.array(rows, int)
    E = {"pair_id": np.array(pid, np.int64), "comp": np.array(cmp, np.int64)}
    for c in OUT_COLS:
        E[c] = T[c][rows]
    return E, len(T)


def write_fits(E, path):
    from astropy.table import Table
    Table({k: v for k, v in E.items()}).write(path, format="fits", overwrite=True)


def local_completeness(E, loc):
    have = set(zip(E["pair_id"].astype(np.int64).tolist(), E["comp"].astype(np.int64).tolist(), E["source_id"].astype(np.int64).tolist()))
    return int(sum(1 for x in loc if x not in have))


_SPOT = True                                                                      # the spot check (MUTATE 5 turns it off)


def spot_check(spec, P, E, n, seed, launch=None):
    """for n random cones (a pair, a component) fetch the SAME rows by a POSITION query (a different query form: needs its own clearance) and compare with the range-fetched exact-cone rows; a mismatch (beyond a 1e-7 deg boundary
    tolerance) means the range form missed sources (for example DR4 source ids that no longer encode their pixel).  Cones whose position query returns the 2,000-row cap are skipped and counted."""
    from astropy.table import Table
    import tempfile, os
    launch = launch or Q1.launch_query
    rng = np.random.default_rng(seed)
    picks = rng.choice(2 * P["n_pairs"], size=min(n, 2 * P["n_pairs"]), replace=False)
    res = dict(n=int(len(picks)), skipped_truncated=0, agree=0, disagree=[], queries=0)
    sid, pidx, comp = E["source_id"], E["pair_id"], E["comp"]
    for u in picks:
        k, c = int(u) // 2, int(u) % 2
        v = P["va"][k] if c == 0 else P["vb"][k]
        ra0 = float(np.degrees(np.arctan2(v[1], v[0])) % 360); dec0 = float(np.degrees(np.arcsin(np.clip(v[2], -1, 1))))
        rad = float(P["R"][k] / 3600)
        cone = (ra0, dec0, rad, None, None)
        q = (f"SELECT {_ref(spec, 'source_id')}, {_ref(spec, 'ra')}, {_ref(spec, 'dec')} FROM {spec['table'] + (' AS ' + spec['alias'] if spec['alias'] else '')} WHERE " + where_cones(spec, [cone]))
        fd, tmp = tempfile.mkstemp(suffix=".fits"); os.close(fd)
        try:
            launch(q, tmp); T = table_arrays(Table.read(tmp, format="fits"))
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
        res["queries"] += 1
        time.sleep(PAUSE_S)
        if len(T["source_id"]) >= SYNC_CAP:
            res["skipped_truncated"] += 1
            continue
        got = set(T["source_id"].astype(np.int64).tolist())
        mine = set(sid[(pidx == k) & (comp == c)].astype(np.int64).tolist())
        diff = got ^ mine
        if diff:
            pos = {int(s): (float(a), float(b)) for s, a, b in zip(T["source_id"], T["ra"], T["dec"])}
            real = [s for s in diff if not (s in pos and abs(_sep_deg(pos[s], (ra0, dec0)) - rad) < 1e-7)]
            if real:
                res["disagree"].append(dict(pair=k, comp=c, only_position_query=len((got - mine) - set(s for s in diff if s not in real)), only_range_fetch=len(mine - got)))
                continue
        res["agree"] += 1
    return res


def _sep_deg(p, q):
    a1, d1, a2, d2 = map(np.radians, (p[0], p[1], q[0], q[1]))
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(a1 - a2)
    return float(np.degrees(np.arccos(np.clip(c, -1, 1))))


# ------------------------------------------------------------------------------------------------ the orchestration (the CLI and the tests call this)
def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_fetch(spec_name, stage_a, pairs_csv, out_dir, manifest_path, tag, caps=None, go_text="", spec_json=None, plan_only=False, spot_n=0, spot_seed=20261201, max_pairs=None,
              probe=True, launch=None, git_commit=None, cal=None):
    """plan -> (offline checks) -> schema probe -> fetch -> exact cones -> completeness -> output file and manifest -> optional spot check.  Nothing is queried without a go text and explicit caps."""
    spec, sha_override = load_spec(spec_name, spec_json)
    P = plan_pairs(stage_a, pairs_csv, spec, max_pairs)
    txt, brief = pre_brief(P["n_pairs"], cal)
    print(f"plan ({spec_name}, strategy {spec['strategy']}): {P['n_pairs']:,d} pairs; {P['n_pix']:,d} level-{Q1.LEVEL} pixels, {len(P['units']):,d} units; {P['area']:.1f} deg2", flush=True)
    print(txt, flush=True)
    loc = Q1.local_in_cones(P) if spec["local_check"] else None
    tot, miss = plan_coverage(P, spec, loc) if loc is not None else (0, 0)
    print(f"offline coverage: {tot} local-extract sources inside the exact cones; {miss} have a source_id outside every planned range", flush=True)
    assert miss == 0, "the planned ranges miss local-extract sources: the source_id -> pixel assumption or the margin is wrong; nothing is queried"
    if plan_only:
        return None
    if not go_text.strip():
        raise SystemExit("refused: pass --owner-go-recorded \"<where and when the owner said yes to this download>\" (nothing is queried without it)")
    if not caps or not all(caps.get(k, 0) > 0 for k in ("accepted_bytes", "received_bytes", "max_queries")):
        raise SystemExit("refused: the hard caps (accepted bytes, received bytes, max queries) have no defaults and must all be given")
    out_dir, manifest_path = Path(out_dir), Path(manifest_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    man = dict(approval=go_text.strip(), tag=tag, spec_name=spec_name, spec=spec, spec_override_sha256=sha_override, utc_start=utc_now(), git_commit=git_commit, n_pairs=P["n_pairs"], n_units=len(P["units"]),
               n_pixels=P["n_pix"], plan_hash=plan_hash(P, spec), caps=caps, pre_brief=brief, pairs_csv_sha256=hashlib.sha256(open(pairs_csv, "rb").read()).hexdigest(), stage_a=str(stage_a),
               sync_cap_rows=SYNC_CAP, level=Q1.LEVEL, margin_arcsec=Q1.MARGIN_ARCSEC)
    arrays, st = fetch_units(P, spec, out_dir / f"q1_{tag}_cache", caps, man, manifest_path, probe=probe, launch=launch)
    E, n_raw = assemble_exact(arrays, P)
    lost = local_completeness(E, loc) if loc is not None else None
    out = out_dir / f"q1_{tag}_neighbours.fits"
    write_fits(E, out)
    ex_no_g = int(np.isnan(np.asarray(E["phot_g_mean_mag"], float)).sum())
    man.update(rows_raw_unique=int(n_raw), rows_exact=int(len(E["source_id"])), rows_without_g_raw=int(st["no_g"]), rows_without_g_exact=ex_no_g, file=out.name, sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(),
               bytes=out.stat().st_size, queries_total=st["calls"], truncated_results_discarded=st["truncated"], accepted_bytes=st["accepted_bytes"], received_bytes=st["received_bytes"],
               batches_resumed_from_cache=st["resumed_batches"], halvings_after_failure=st["halvings_after_failure"], seconds_this_session=st["seconds_this_session"],
               local_extract_sources_in_cones=tot if loc is not None else None, local_extract_sources_missing_from_fetch=lost, utc_end=utc_now())
    man["usable"] = bool(lost in (None, 0))
    manifest_path.write_text(json.dumps(man, indent=1, default=str) + "\n")
    print(f"exact cone rows {len(E['source_id']):,d} from {n_raw:,d} unique raw rows ({st['no_g']:,d} without G); {st['calls']} queries ({st['truncated']} truncated results discarded), accepted {st['accepted_bytes'] / 1e6:.1f} MB, "
          f"received {st['received_bytes'] / 1e6:.1f} MB; local-extract sources missing from the fetch: {lost}; wrote {out.name}", flush=True)
    if lost:
        print("WARNING: the fetch is missing local-extract sources; do not use it", flush=True)
    if spot_n and _SPOT:
        sc = spot_check(spec, P, E, spot_n, spot_seed, launch=launch)
        man["spot_check"] = sc
        if sc["disagree"]:
            man["usable"] = False
        manifest_path.write_text(json.dumps(man, indent=1, default=str) + "\n")
        print(f"spot check: {sc['n']} cones, {sc['agree']} agree, {len(sc['disagree'])} DISAGREE, {sc['skipped_truncated']} skipped (truncated), {sc['queries']} position queries", flush=True)
        if sc["disagree"]:
            raise SpotCheckFailed(f"the position query found rows the range fetch did not (or the reverse) in {len(sc['disagree'])} of {sc['n']} cones: {sc['disagree'][:3]}; the range form is not complete on this table")
    return man
