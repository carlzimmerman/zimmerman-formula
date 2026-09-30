#!/usr/bin/env python3
"""DR4-READY-1, WP1: the DR3 PILOT of the cut-13 all-source third-star search (Amendment 16(b)-(c)) on the owner-approved
Q1 pilot: neighbour cones (30 kAU / d(primary) around each component) around 500 randomly chosen final DR3 pairs (seed
20261202), fetched by q_fetch_dr3.py.  NO NETWORK (socket guard).  NEW file; frozen modules are imported read-only.

Compares, on the same 500 pairs and the same cones:
  * ALL-SOURCE: every gaia_source row the archive returned in the cones -- literal criterion (PRIMARY, A16(b)) and the
    orbit-aware bound (VARIANT), both from catalog_builder_dr4/cut13.py;
  * EXTRACT: the frozen extract's rows (stage_A, the 12 chunks) inside the same cones -- what the frozen builder could see;
  * the frozen builder's own cut 13 on these pairs is False for all of them by construction (they are final pairs).
Reports: flags under each criterion and base; the neighbours that make the extra all-source hits and which extract
condition each fails; the neighbours with no G (A16(b)'s count); rows per cone against radius, to size the full Q1.
Checks: K1 each cone contains its own component; K2 the extract-based orbit-aware search flags none of the 500 final pairs
(it equals the builder's cut 13, dry_run_driver S3); K3 the per-neighbour attribution reproduces cut13's pair flags.
DR3 numbers are code-path tests, never results (Amendment 7(e)).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp1_cut13_pilot_dr3.py
"""
import sys
sys.dont_write_bytecode = True
import json, socket, time
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline pilot (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "catalog_builder_dr4"))
import cut13_allsource as W1
import cut13                                                     # read-only
from scipy.spatial import cKDTree

WB = REPO / "real_research" / "data" / "widebinaries"
Q = WB / "dr3_extract" / "dr4_ready_1"
EXTRACT_WHERE = "parallax > 3.5 AND parallax_over_error > 5 AND parallax_error < 2 AND phot_g_mean_mag IS NOT NULL AND ABS(b) > 10"
t0 = time.time()
LOG, RES = [], {}


def P(s=""):
    print(s, flush=True)
    LOG.append(s)


def K(name, ok, detail=""):
    RES[name] = bool(ok)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def galactic_b(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    ra_gp, dec_gp = np.radians(192.85948), np.radians(27.12825)
    sb = np.sin(dec) * np.sin(dec_gp) + np.cos(dec) * np.cos(dec_gp) * np.cos(ra - ra_gp)
    return np.degrees(np.arcsin(np.clip(sb, -1, 1)))


# ------------------------------------------------------------------------------------------------ load
from astropy.table import Table
T = Table.read(Q / "q1_pilot_neighbours.fits", format="fits")
nb = {}
for c in T.colnames:
    col = T[c]
    v = np.asarray(col.filled(np.nan) if hasattr(col, "filled") and col.dtype.kind == "f" else col)
    if hasattr(col, "mask") and col.dtype.kind in "iu":
        v = np.asarray(col.filled(-1))
    nb[c.lower()] = v
nb["source_id"] = nb["source_id"].astype(np.int64)
man_q = json.loads((HERE / "manifest_q_dr3.json").read_text())["queries"]["Q1_pilot"]
Z = np.load(Q / "q1_pilot_pairs.npz")
pick, sa, sb_ = Z["pick"], Z["source_id_a"].astype(np.int64), Z["source_id_b"].astype(np.int64)
P(f"Q1 pilot: {len(T):,d} rows from {len(pick)} pairs ({man_q['bytes'] / 1e6:.1f} MB, sha256 {man_q['sha256'][:16]}); "
  f"radius {man_q['radius_arcsec_range'][0]:.0f}-{man_q['radius_arcsec_range'][1]:.0f} arcsec")
S = np.load(WB / "dr3_extract" / "stage_A.npz")
sid = S["source_id"]
order = np.argsort(sid)


def rows_of(ids):
    i = np.searchsorted(sid[order], ids)
    i = np.clip(i, 0, len(sid) - 1)
    r = order[i]
    return r, sid[r] == ids


ra_, oka = rows_of(sa)
rb_, okb = rows_of(sb_)
assert oka.all() and okb.all()
cols = W1.COLS[1:] + ("phot_g_mean_mag",)
pairs = {"source_id_a": sa, "source_id_b": sb_}
for suf, r in (("_a", ra_), ("_b", rb_)):
    for c in cols:
        pairs[c + suf] = np.asarray(S[c], float)[r]

# ------------------------------------------------------------------------------------------------ K1 geometry
own = 0
for i, (x, y) in enumerate(zip(sa, sb_)):
    m = nb["pair_id"] == pick[i]
    ca = set(nb["source_id"][m & (nb["comp"] == 0)].tolist())
    cb = set(nb["source_id"][m & (nb["comp"] == 1)].tolist())
    own += int(x in ca) + int(y in cb)
K("K1 every cone contains its own component (the cone join is centred correctly)", own == 2 * len(pick), f"{own}/{2 * len(pick)}")

# ------------------------------------------------------------------------------------------------ all-source search
lit, orb, man_all = W1.evaluate(pairs, nb)
P(f"\nALL-SOURCE: literal flags {int(lit.flags.sum())}, orbit-aware flags {int(orb.flags.sum())}; neighbours {lit.n_neigh:,d}, "
  f"without G {lit.n_no_g:,d} (kinematic matches without G {lit.n_no_g_kin}), without kinematics {lit.n_no_kin:,d}")

# ------------------------------------------------------------------------------------------------ extract search, same cones
xyz = np.column_stack([np.cos(np.radians(S["dec"])) * np.cos(np.radians(S["ra"])),
                       np.cos(np.radians(S["dec"])) * np.sin(np.radians(S["ra"])), np.sin(np.radians(S["dec"]))])
tree = cKDTree(xyz)
th = np.radians(W1.radius_arcsec(pairs["parallax_a"]) / 3600)
chord = 2 * np.sin(th / 2)
ext_rows = set()
for i in range(len(pick)):
    for r in (ra_[i], rb_[i]):
        ext_rows.update(tree.query_ball_point(xyz[r], r=chord[i]))
ext_rows = np.array(sorted(ext_rows))
nb_ext = {"source_id": S["source_id"][ext_rows]}
for c in cols:
    nb_ext[c] = np.asarray(S[c], float)[ext_rows]
lit_e, orb_e, man_e = W1.evaluate(pairs, nb_ext)
P(f"EXTRACT (same cones, {len(ext_rows):,d} extract rows): literal flags {int(lit_e.flags.sum())}, orbit-aware flags "
  f"{int(orb_e.flags.sum())}")
K("K2 the extract-based orbit-aware search flags none of the 500 final pairs (it equals the builder's cut 13, dry-run S3)",
  int(orb_e.flags.sum()) == 0, f"{int(orb_e.flags.sum())} flagged")

# ------------------------------------------------------------------------------------------------ attribution (K3)
cat, a_idx, b_idx = W1.assemble(pairs, nb)
f = {k: np.asarray(cat[k], float) for k in cut13.REQUIRED}
in_extract = np.isin(cat["source_id"], S["source_id"])
bcat = galactic_b(cat["ra"], cat["dec"])


def fails(j):
    out = []
    p, e, g = f["parallax"][j], f["parallax_error"][j], cat["phot_g_mean_mag"][j]
    if not np.isfinite(p) or not p > 3.5:
        out.append("parallax <= 3.5 or null")
    if not (np.isfinite(p) and np.isfinite(e) and e > 0 and p / e > 5):
        out.append("parallax_over_error <= 5")
    if not (np.isfinite(e) and e < 2):
        out.append("parallax_error >= 2 or null")
    if not np.isfinite(g):
        out.append("G null")
    if not abs(bcat[j]) > 10:
        out.append("|b| <= 10")
    return out or ["passes every extract condition (so it should be in the extract)"]


attr = {"literal": [], "orbit": []}
re_flags = {"literal": np.zeros(len(a_idx), bool), "orbit": np.zeros(len(a_idx), bool)}
for i, js in cut13._search(cat, a_idx, b_idx, cut13.RADIUS_KAU):
    if len(js) == 0:
        continue
    k = a_idx[i]
    dpar = np.abs(f["parallax"][k] - f["parallax"][js]) / np.hypot(f["parallax_error"][k], f["parallax_error"][js])
    dmu, sdmu = cut13._delta_mu_and_sigma(f["pmra"][k], f["pmdec"][k], f["pmra"][js], f["pmdec"][js],
                                          f["pmra_error"][k], f["pmdec_error"][k], f["pmra_error"][js], f["pmdec_error"][js])
    thk = cut13._ang_sep_arcsec(f["ra"][k], f["dec"][k], f["ra"][js], f["dec"][js])
    g = f["phot_g_mean_mag"][js]
    with np.errstate(invalid="ignore"):
        for kind, bound in (("literal", cut13.N_SIGMA_PM * sdmu),
                            ("orbit", cut13.orbit_allowance(f["parallax"][k], thk) + cut13.SDMU_MULT * sdmu)):
            hit = (dpar < cut13.N_SIGMA_PLX) & (dmu < bound) & (g < cut13.G_MAX)
            re_flags[kind][i] = bool(hit.any())
            for j in js[hit]:
                attr[kind].append(dict(pair=int(i), neighbour=int(cat["source_id"][j]), in_extract=bool(in_extract[j]),
                                       fails=[] if in_extract[j] else fails(j), G=float(g[js == j][0]),
                                       sep_kAU=float(thk[js == j][0] * 1000 / f["parallax"][k] / 1000)))
K("K3 the per-neighbour attribution reproduces cut13's pair flags (literal and orbit-aware)",
  np.array_equal(re_flags["literal"], lit.flags) and np.array_equal(re_flags["orbit"], orb.flags),
  f"literal {int(re_flags['literal'].sum())} vs {int(lit.flags.sum())}; orbit {int(re_flags['orbit'].sum())} vs {int(orb.flags.sum())}")

P("\nEXTRA HITS (all-source flags that the extract search does not raise):")
summary = {}
for kind, fa, fe in (("literal", lit.flags, lit_e.flags), ("orbit", orb.flags, orb_e.flags)):
    new = np.flatnonzero(fa & ~fe)
    lost = np.flatnonzero(~fa & fe)
    hits = [h for h in attr[kind] if h["pair"] in set(new.tolist())]
    reasons = {}
    for h in hits:
        if not h["in_extract"]:
            for r in h["fails"]:
                reasons[r] = reasons.get(r, 0) + 1
    summary[kind] = dict(all_source=int(fa.sum()), extract=int(fe.sum()), new=int(len(new)), lost=int(len(lost)),
                         hitting_neighbours_of_new=len(hits), non_extract_hitting=sum(1 for h in hits if not h["in_extract"]),
                         reasons=reasons)
    P(f"  {kind:8s}: all-source {int(fa.sum())}, extract {int(fe.sum())}, NEW {len(new)} (of 500 = {len(new) / 5:.1f}%), lost {len(lost)}; "
      f"hitting neighbours of the new pairs {len(hits)}, of which not in the extract {summary[kind]['non_extract_hitting']}; "
      f"extract conditions they fail: {reasons}")

# ------------------------------------------------------------------------------------------------ sizing the full Q1
counts = {}
for pid, comp in zip(nb["pair_id"], nb["comp"]):
    counts[(int(pid), int(comp))] = counts.get((int(pid), int(comp)), 0) + 1
rad = np.repeat(W1.radius_arcsec(pairs["parallax_a"]), 2)
cnt = np.array([counts.get((int(p_), c_), 0) for p_ in pick for c_ in (0, 1)])
area = np.pi * (rad / 3600) ** 2
dens = cnt.sum() / area.sum()
rows_all = __import__("csv").DictReader(open(WB / "dr3_extract" / "wide_binaries_dr3.csv"))
ids_a = np.array([int(r["source_id1"]) for r in rows_all], np.int64)
r_full, ok_full = rows_of(ids_a)
area_full = 2 * np.pi * (W1.radius_arcsec(np.asarray(S["parallax"], float)[r_full]) / 3600) ** 2
bytes_per_row = man_q["bytes"] / max(len(T), 1)
pred_rows = dens * area_full.sum()
P(f"\nSIZING: pilot {cnt.sum():,d} rows over {area.sum():.2f} deg^2 of cones ({dens:,.0f} rows/deg^2; median per cone "
  f"{int(np.median(cnt))}, max {cnt.max()}); full Q1 = {len(ids_a):,d} pairs, {area_full.sum():.1f} deg^2 of cones -> about "
  f"{pred_rows:,.0f} rows, about {pred_rows * bytes_per_row / 1e6:,.0f} MB at the pilot's {bytes_per_row:.0f} bytes/row "
  f"(overlapping cones counted twice, so an upper estimate)")
out = dict(pilot=dict(rows=int(len(T)), bytes=man_q["bytes"], sha256=man_q["sha256"]),
           all_source=man_all, extract=man_e, summary=summary, checks=RES,
           sizing=dict(rows_per_deg2=float(dens), pilot_area_deg2=float(area.sum()), full_area_deg2=float(area_full.sum()),
                       full_rows_estimate=float(pred_rows), full_MB_estimate=float(pred_rows * bytes_per_row / 1e6)),
           attributions={k: v[:200] for k, v in attr.items()}, seconds=round(time.time() - t0, 1))
ok = all(RES.values())
P(f"\n{sum(RES.values())}/{len(RES)} checks pass -> {'ALL PASS' if ok else 'FAILURES'}  ({time.time() - t0:.0f} s)")
(HERE / "wp1_cut13_pilot_dr3.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
(HERE / "wp1_cut13_pilot_dr3.out").write_text("\n".join(LOG) + "\n")
sys.exit(0 if ok else 1)
