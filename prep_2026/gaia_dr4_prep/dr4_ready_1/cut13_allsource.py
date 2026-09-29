#!/usr/bin/env python3
"""DR4-READY-1, WP1 (offline half): the cut-13 third-star search against the FULL catalogue (Amendment 16(b), 16(c)).

NEW file.  NO NETWORK in this module: it builds the upload table and the ADQL text for a server-side cone search, and it
evaluates the returned neighbours with catalog_builder_dr4/cut13.py (literal = PRIMARY, orbit-aware = reported VARIANT).
Running a query is a separate, explicit step that needs the owner's go (PLAN.md, Q1); nothing here opens a connection.

Geometry (identical to cut13.py `_search`): the search radius is 30 kAU / d(primary) = 30 * parallax_primary [arcsec]
around EACH component of the pair; the evaluation re-applies exactly that radius, so the cones only need to contain it.

upload_table(pair_id, ra_a, dec_a, ra_b, dec_b, plx_a)  -> dict of arrays, two rows per pair (comp 0 = primary, 1 = b)
adql_cones(search_table, g_table=None, upload="pairs")  -> ADQL text (DR3: search_table = 'gaiadr3.gaia_source', G in it;
                                                          DR4: 'gaiadr4.all_source_astrometry' + g_table
                                                          'gaiadr4.all_source_photometry' joined on source_id -- names are
                                                          re-confirmed on release day, Amendment 15(d))
assemble(pairs, neighbours)                             -> (cat, a, b): one de-duplicated catalogue (pair members + every
                                                          returned neighbour) and the pair row indices, ready for cut13
evaluate(pairs, neighbours)                             -> both criteria's ThirdResult plus manifest counts
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "catalog_builder_dr4"))
import cut13                                                    # read-only (NEW-file scaffolding of 2026-09-28)

RADIUS_KAU = cut13.RADIUS_KAU
COLS = ("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error")


def radius_arcsec(plx_primary_mas, radius_kau=RADIUS_KAU):
    """radius_kau * 1000 AU / d(primary), d = 1000/plx  ->  radius_kau * plx  [arcsec]."""
    return radius_kau * np.asarray(plx_primary_mas, float)


def upload_table(pair_id, ra_a, dec_a, ra_b, dec_b, plx_a, radius_kau=RADIUS_KAU):
    r = radius_arcsec(plx_a, radius_kau)
    n = len(np.asarray(pair_id))
    return {"pair_id": np.repeat(np.asarray(pair_id), 2), "comp": np.tile([0, 1], n),
            "ra": np.column_stack([ra_a, ra_b]).ravel(), "dec": np.column_stack([dec_a, dec_b]).ravel(),
            "radius_deg": np.repeat(r / 3600.0, 2)}


def adql_cones(search_table, g_table=None, upload="pairs"):
    s_cols = ", ".join(f"s.{c}" for c in COLS)
    g_sel = "g.phot_g_mean_mag" if g_table else "s.phot_g_mean_mag"
    join_g = f" LEFT OUTER JOIN {g_table} AS g ON g.source_id = s.source_id" if g_table else ""
    return (f"SELECT u.pair_id, u.comp, {s_cols}, {g_sel} AS phot_g_mean_mag "
            f"FROM tap_upload.{upload} AS u JOIN {search_table} AS s "
            f"ON 1 = CONTAINS(POINT('ICRS', s.ra, s.dec), CIRCLE('ICRS', u.ra, u.dec, u.radius_deg))" + join_g)


def assemble(pairs, neighbours):
    """pairs: dict with source_id_a, source_id_b and, for each, the COLS + phot_g_mean_mag (suffix _a / _b);
    neighbours: dict of arrays as the query returns them (pair_id, comp, COLS, phot_g_mean_mag).
    Returns (cat, a, b) with one row per unique source_id."""
    keys = COLS[1:] + ("phot_g_mean_mag",)
    rows = {k: [] for k in ("source_id",) + keys}
    for suf in ("_a", "_b"):
        rows["source_id"].append(np.asarray(pairs["source_id" + suf]))
        for k in keys:
            rows[k].append(np.asarray(pairs[k + suf], float))
    rows["source_id"].append(np.asarray(neighbours["source_id"]))
    for k in keys:
        rows[k].append(np.asarray(neighbours[k], float))
    allsid = np.concatenate(rows["source_id"])
    u, first = np.unique(allsid, return_index=True)
    cat = {k: np.concatenate(rows[k])[first] for k in keys}
    cat["source_id"] = u
    a = np.searchsorted(u, np.asarray(pairs["source_id_a"]))
    b = np.searchsorted(u, np.asarray(pairs["source_id_b"]))
    return cat, a, b


def evaluate(pairs, neighbours, reference="primary"):
    cat, a, b = assemble(pairs, neighbours)
    lit = cut13.third_star_literal(cat, a, b, reference=reference)
    orb = cut13.third_star_orbit_aware(cat, a, b)
    manifest = {"n_pairs": int(len(a)), "n_catalogue_rows": int(len(cat["ra"])),
                "literal": {"n_hit": lit.n_hit, "n_neigh": lit.n_neigh, "n_no_g": lit.n_no_g, "n_no_g_kin": lit.n_no_g_kin,
                            "n_no_kin": lit.n_no_kin},
                "orbit_aware": {"n_hit": orb.n_hit, "n_neigh": orb.n_neigh, "n_no_g": orb.n_no_g, "n_no_g_kin": orb.n_no_g_kin,
                                "n_no_kin": orb.n_no_kin},
                "n_disagree": int((lit.flags != orb.flags).sum())}
    return lit, orb, manifest
