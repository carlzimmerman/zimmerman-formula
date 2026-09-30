#!/usr/bin/env python3
"""DR4-READY-1: the CONES-BASED cut 13 for the driver (NEW file; OFFLINE; nothing frozen is edited).  Design and controls: CONES_CUT13_DESIGN_FROZEN.md (9ea1d20e7), written before this code.
DR3 numbers are code-path tests, never results (Amendment 7(e)).

ConeTable holds the neighbour cones of WP1's Q1 (rows with pair_id, comp and cut13_allsource.COLS + phot_g_mean_mag, as q1_full_ranges.py writes them) keyed by PAIR (source_id1, source_id2), so the final-pair cones and a later delta
can be combined.  ConeTable.flags(S, a, b, mode) returns the cut-13 flags of the pairs (rows a, b of stage A): mode 'literal' = the frozen text read literally (PRIMARY, Amendment 16(b)), 'orbit' = the orbit-aware bound (VARIANT),
both by cut13_allsource.evaluate on the COVERED pairs only.  A pair without a cone is never silently treated as 'no third star': missing='error' (default) raises ConeCoverageError; missing='extract-fallback' (a labelled DR3
code-path option while only the final-pair cones exist) uses the builder's own extract-based flags for the uncovered pairs and reports the counts.
Also: build_extract_cones(S, a, b) builds the cones from the EXTRACT itself (the code-path control K1)."""
import sys
sys.dont_write_bytecode = True
import csv
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "catalog_builder_dr4"))
import cut13_allsource as W1                                        # read-only
import cut13                                                        # read-only

NB_COLS = tuple(W1.COLS[1:]) + ("phot_g_mean_mag",)


class ConeCoverageError(RuntimeError):
    pass


def read_neighbour_fits(path):
    """the neighbour table as a dict of lowercase arrays (masked floats -> NaN, masked ints -> -1)."""
    from astropy.table import Table
    T = Table.read(str(path), format="fits")
    nb = {}
    for c in T.colnames:
        col = T[c]
        if hasattr(col, "mask") and col.dtype.kind == "f":
            v = np.asarray(col.filled(np.nan), float)
        elif hasattr(col, "mask") and col.dtype.kind in "iu":
            v = np.asarray(col.filled(-1))
        else:
            v = np.asarray(col)
        nb[c.lower()] = v
    nb["source_id"] = nb["source_id"].astype(np.int64)
    nb["pair_id"] = nb["pair_id"].astype(np.int64)
    nb["comp"] = nb["comp"].astype(np.int64)
    return nb


def read_pairs_csv(path):
    rows = list(csv.DictReader(open(path)))
    return np.array([int(r["source_id1"]) for r in rows], np.int64), np.array([int(r["source_id2"]) for r in rows], np.int64)


class ConeTable:
    def __init__(self):
        self.key_to_id = {}
        self._chunks = []
        self.nb = None

    def add(self, nb, sid1, sid2):
        """nb['pair_id'] indexes the rows of (sid1, sid2); the pair keys are (source_id1, source_id2)."""
        ids = np.empty(len(sid1), np.int64)
        for i, (x, y) in enumerate(zip(sid1.tolist(), sid2.tolist())):
            ids[i] = self.key_to_id.setdefault((int(x), int(y)), len(self.key_to_id))
        nb2 = dict(nb)
        nb2["pair_id"] = ids[nb["pair_id"]]
        self._chunks.append(nb2)
        self.nb = None
        return self

    @classmethod
    def from_files(cls, files):
        """files: iterable of (neighbour FITS path, pairs CSV path)."""
        t = cls()
        for fits_path, pairs_csv in files:
            s1, s2 = read_pairs_csv(pairs_csv)
            t.add(read_neighbour_fits(fits_path), s1, s2)
        return t

    def _table(self):
        if self.nb is None:
            keys = list(self._chunks[0])
            nb = {k: np.concatenate([c[k] for c in self._chunks]) for k in keys}
            # the same (pair, component, source) row in two files counts once
            tag = np.column_stack([nb["pair_id"], nb["comp"], nb["source_id"]])
            _, first = np.unique(tag, axis=0, return_index=True)
            first.sort()
            self.nb = {k: v[first] for k, v in nb.items()}
        return self.nb

    def covered_mask(self, sid_a, sid_b):
        return np.array([(int(x), int(y)) in self.key_to_id for x, y in zip(np.asarray(sid_a).tolist(), np.asarray(sid_b).tolist())], bool)

    def flags(self, S, a, b, mode="literal", missing="error", fallback=None):
        """cut-13 flags (True = a third star was found: the pair is rejected) for the pairs (rows a, b of S); returns (flags, info)."""
        if mode not in ("literal", "orbit"):
            raise ValueError("mode must be 'literal' or 'orbit'")
        a, b = np.asarray(a), np.asarray(b)
        sid = S["source_id"]
        sa, sb = sid[a], sid[b]
        cov = self.covered_mask(sa, sb)
        n_missing = int((~cov).sum())
        info = dict(mode=mode, n_pairs=int(len(a)), n_covered=int(cov.sum()), n_missing=n_missing, missing_policy=missing)
        if n_missing:
            if missing == "error":
                first = [(int(x), int(y)) for x, y in zip(sa[~cov][:3].tolist(), sb[~cov][:3].tolist())]
                raise ConeCoverageError(f"{n_missing} of {len(a)} pairs that reach cut 13 have NO neighbour cone (covered {int(cov.sum())}); "
                                        f"a pair without a cone is never treated as 'no third star'; fetch cones for them (first uncovered: {first})")
            if missing != "extract-fallback":
                raise ValueError("missing must be 'error' or 'extract-fallback'")
            if fallback is None:
                raise ValueError("missing='extract-fallback' needs a fallback function")
        flags = np.zeros(len(a), bool)
        if cov.any():
            ia = np.flatnonzero(cov)
            pid = np.array([self.key_to_id[(int(x), int(y))] for x, y in zip(sa[ia].tolist(), sb[ia].tolist())], np.int64)
            nb = self._table()
            sel = np.isin(nb["pair_id"], pid)
            nbs = {k: v[sel] for k, v in nb.items()}
            pairs = {"source_id_a": sa[ia], "source_id_b": sb[ia]}
            for suf, rows in (("_a", a[ia]), ("_b", b[ia])):
                for c in NB_COLS:
                    pairs[c + suf] = np.asarray(S[c], float)[rows]
            lit, orb, man = W1.evaluate(pairs, nbs)
            res = lit if mode == "literal" else orb
            flags[ia] = res.flags
            info.update(n_flagged_cones=int(res.flags.sum()), n_neighbours=int(res.n_neigh), n_no_g=int(res.n_no_g), n_no_g_kin=int(res.n_no_g_kin), n_no_kin=int(res.n_no_kin),
                        literal_flagged=int(lit.flags.sum()), orbit_flagged=int(orb.flags.sum()), n_neighbour_rows=int(sel.sum()))
        if n_missing and missing == "extract-fallback":
            fb = np.asarray(fallback(S, a[~cov], b[~cov]), bool)
            flags[~cov] = fb
            info["n_flagged_fallback"] = int(fb.sum())
        info["n_flagged_total"] = int(flags.sum())
        return flags, info


def build_extract_cones(S, a, b, radius_kau=None):
    """cones built from the EXTRACT itself for the pairs (rows a, b of S): every stage-A row within the search radius 30 kAU / d(primary) = radius_kau x parallax [arcsec] of either component, as the Q1 query would return them
    from a catalogue equal to the extract; pair_id = the pair's index in (a, b), comp 0 = a (the primary), 1 = b.  Returns (neighbour dict, source_id1 array, source_id2 array)."""
    from scipy.spatial import cKDTree
    radius_kau = W1.RADIUS_KAU if radius_kau is None else radius_kau
    ra, dec = np.asarray(S["ra"], float), np.asarray(S["dec"], float)
    xyz = np.column_stack([np.cos(np.radians(dec)) * np.cos(np.radians(ra)), np.cos(np.radians(dec)) * np.sin(np.radians(ra)), np.sin(np.radians(dec))])
    tree = cKDTree(xyz)
    a, b = np.asarray(a), np.asarray(b)
    th = np.radians(W1.radius_arcsec(np.asarray(S["parallax"], float)[a], radius_kau) / 3600)
    chord = 2 * np.sin(th / 2)
    pid, comp, rows = [], [], []
    for i in range(len(a)):
        for c, r in ((0, a[i]), (1, b[i])):
            js = tree.query_ball_point(xyz[r], r=chord[i])
            pid += [i] * len(js); comp += [c] * len(js); rows += js
    rows = np.array(rows, np.int64)
    nb = {"pair_id": np.array(pid, np.int64), "comp": np.array(comp, np.int64), "source_id": np.asarray(S["source_id"])[rows].astype(np.int64)}
    for c in W1.COLS[1:]:
        nb[c] = np.asarray(S[c], float)[rows]
    nb["phot_g_mean_mag"] = np.asarray(S["phot_g_mean_mag"], float)[rows]
    return nb, np.asarray(S["source_id"])[a].astype(np.int64), np.asarray(S["source_id"])[b].astype(np.int64)
