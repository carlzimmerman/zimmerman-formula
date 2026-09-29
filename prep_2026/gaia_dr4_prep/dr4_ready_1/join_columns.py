#!/usr/bin/env python3
"""DR4-READY-1, WP3: join columns by source_id from a second table (Amendment 16(c): "the join code for RUWE,
ipd_frac_multi_peak and radial velocities if DR4 gaia_source lacks them").  NEW file; nothing frozen is touched.

join_by_source_id(base, tables, needed)
    base    dict of equal-length numpy arrays with a 'source_id' column (the extract the builder uses)
    tables  list of (name, dict of equal-length arrays with 'source_id' and some of the needed columns)
    needed  column names to bring into `base`
Returns (joined, report).  `joined` is a new dict: `base` plus every needed column, aligned by source_id.
Rules (declared; each is tested by wp3_join_dryrun_dr3.py):
  * a needed column found in NO table raises (never a silent default);
  * a column found in more than one table raises unless `prefer` names the table (the release-day manifest records it);
  * duplicate source_ids inside a table raise;
  * a base source_id missing from the table gets NaN (float) or the declared integer fill, and is COUNTED per column in
    the report (never silently);
  * a column already present in `base` is not overwritten unless `overwrite=True` (then the report says so).
The report is manifest-ready: per column, its source table, the number of matched and unmatched base ids.
"""
import numpy as np

INT_FILL = -1                                                    # declared fill for integer columns (e.g. flags)


def join_by_source_id(base, tables, needed, prefer=None, overwrite=False):
    prefer = prefer or {}
    if "source_id" not in base:
        raise KeyError("base has no source_id column")
    sid = np.asarray(base["source_id"])
    joined = dict(base)
    report = {"n_base": int(len(sid)), "columns": {}}
    index = {}
    for name, tab in tables:
        if "source_id" not in tab:
            raise KeyError(f"table {name!r} has no source_id column")
        t_sid = np.asarray(tab["source_id"])
        u, c = np.unique(t_sid, return_counts=True)
        if (c > 1).any():
            raise ValueError(f"table {name!r} has {int((c > 1).sum())} duplicated source_id(s)")
        order = np.argsort(t_sid, kind="stable")
        index[name] = (t_sid[order], order, tab)
    for col in needed:
        if col in base and not overwrite:
            report["columns"][col] = {"source": "base (already present)", "n_matched": int(len(sid)), "n_unmatched": 0}
            continue
        owners = [name for name, tab in tables if col in tab]
        if not owners:
            raise KeyError(f"needed column {col!r} is in no table (tables: {[n for n, _ in tables]})")
        if len(owners) > 1:
            if col not in prefer or prefer[col] not in owners:
                raise ValueError(f"column {col!r} is in several tables {owners}; name the source in `prefer`")
            owners = [prefer[col]]
        name = owners[0]
        t_sorted, order, tab = index[name]
        vals = np.asarray(tab[col])[order]
        pos = np.searchsorted(t_sorted, sid)
        pos_c = np.clip(pos, 0, max(len(t_sorted) - 1, 0))
        hit = (pos < len(t_sorted)) & (len(t_sorted) > 0) & (t_sorted[pos_c] == sid)
        if np.issubdtype(vals.dtype, np.integer):
            out = np.full(len(sid), INT_FILL, dtype=vals.dtype)
        else:
            out = np.full(len(sid), np.nan, dtype=np.result_type(vals.dtype, np.float64))
        out[hit] = vals[pos_c[hit]]
        joined[col] = out
        report["columns"][col] = {"source": name, "n_matched": int(hit.sum()), "n_unmatched": int((~hit).sum()),
                                  "overwrote_base": bool(col in base)}
    return joined, report
