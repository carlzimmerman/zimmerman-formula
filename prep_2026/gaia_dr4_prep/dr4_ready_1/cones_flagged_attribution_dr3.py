#!/usr/bin/env python3
"""DR4-READY-1: POST-HOC attribution of the cones paths' cut-13 flags to the stars that trigger them (NEW file; OFFLINE; written AFTER the real run of cones_all_candidates_dr3.py, whose first run is kept as it is;
descriptive, NOT scored, not in the frozen design; DR3 code-path numbers, Amendment 7(e)).
For every candidate flagged by cones-literal or cones-orbit (and every pair an extract path flags), the neighbours that satisfy the criterion: source_id, G, the projected separation from the primary and from the secondary (kAU),
the parallax difference (sigma), the proper-motion difference against the criterion's bound, whether the star is in the extract and, if not, which extract condition it fails (parallax > 3.5 mas, parallax / error > 5, parallax error < 2,
G not null, |b| > 10 deg; the conditions the DR3 extract was built with, from wp1_cut13_full_dr3.py).
Control (can fail): the attribution reproduces every pair's cones flag (flagged iff at least one hitting neighbour), for the flagged pairs AND 40 unflagged pairs drawn at random (seed 20261231), both criteria.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/cones_flagged_attribution_dr3.py"""
import sys
sys.dont_write_bytecode = True
import json, tempfile, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import cones_cut13 as CC
import cut13_allsource as W1

T0 = time.time()
D.init(False)
cut13 = W1.cut13
WB = REPO / "real_research" / "data" / "widebinaries"
IN = WB / "dr3_extract" / "dr4_ready_1"
LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


ext = D.extract_dir("dr3", "primary")
S = dict(np.load(ext / "stage_A.npz"))
sid = S["source_id"]
order = np.argsort(sid)
rows_of = lambda ids: order[np.searchsorted(sid[order], ids)]
tmp = Path(tempfile.mkdtemp()) / "candidates.csv"
b_ref, r_ref = D.run("dr3", "primary", "extract-builder", None, False, dump_candidates=str(tmp))
assert r_ref["sha256"].startswith(D.REF_SHA_DR3)
c1, c2 = CC.read_pairs_csv(tmp)
f1, f2 = CC.read_pairs_csv(WB / "dr3_extract" / "wide_binaries_dr3.csv")
d1, d2 = CC.read_pairs_csv(IN / "q1_delta_pairs.csv")
a_rows, b_rows = rows_of(c1), rows_of(c2)
final = {(int(x), int(y)) for x, y in zip(f1.tolist(), f2.tolist())}
is_final = np.array([(int(x), int(y)) in final for x, y in zip(c1.tolist(), c2.tolist())])
cones = CC.ConeTable().add(CC.read_neighbour_fits(IN / "q1_full_neighbours.fits"), f1, f2).add(CC.read_neighbour_fits(IN / "q1_delta_neighbours.fits"), d1, d2)
fl = {k: np.asarray(cones.flags(S, a_rows, b_rows, m)[0], bool) for k, m in (("literal", "literal"), ("orbit", "orbit"))}
fx = {k: np.asarray(D.third_function(k, S)(S, a_rows, b_rows), bool) for k in ("extract-literal", "extract-builder")}
P("POST-HOC ATTRIBUTION of the cut-13 flags (descriptive, not scored; DR3 code-path numbers)")
P(f"cones-literal flags {int(fl['literal'].sum())}, cones-orbit {int(fl['orbit'].sum())}; extract-literal {int(fx['extract-literal'].sum())}, extract-builder {int(fx['extract-builder'].sum())} of {len(c1):,d} candidates")

rng = np.random.default_rng(20261231)
flagged = np.flatnonzero(fl["literal"] | fl["orbit"] | fx["extract-literal"] | fx["extract-builder"])
unflagged = rng.choice(np.setdiff1d(np.arange(len(c1)), flagged), 40, replace=False)
idx = np.concatenate([flagged, unflagged])


def galactic_b(ra, dec):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    return SkyCoord(ra=np.asarray(ra) * u.deg, dec=np.asarray(dec) * u.deg).galactic.b.deg


# the subset's pairs and neighbours, exactly as ConeTable.flags assembles them
sa, sb = c1[idx], c2[idx]
internal = np.array([cones.key_to_id[(int(x), int(y))] for x, y in zip(sa.tolist(), sb.tolist())], np.int64)
tab = cones._table()
sel = np.isin(tab["pair_id"], internal)
remap = {int(v): i for i, v in enumerate(internal)}
nbs = {k: v[sel] for k, v in tab.items()}
nbs["pair_id"] = np.array([remap[int(p)] for p in nbs["pair_id"]], np.int64)
pairs = {"source_id_a": sa, "source_id_b": sb}
for suf, rows in (("_a", a_rows[idx]), ("_b", b_rows[idx])):
    for c in CC.NB_COLS:
        pairs[c + suf] = np.asarray(S[c], float)[rows]
cat, a_idx, b_idx = W1.assemble(pairs, nbs)
f = {k: np.asarray(cat[k], float) for k in cut13.REQUIRED}
in_extract = np.isin(cat["source_id"], sid)
bcat = galactic_b(cat["ra"], cat["dec"])


def fails(j):
    out = []
    p, e, g = f["parallax"][j], f["parallax_error"][j], f["phot_g_mean_mag"][j] if "phot_g_mean_mag" in f else cat["phot_g_mean_mag"][j]
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
    return out or ["passes every extract condition"]


hits = {"literal": {}, "orbit": {}}
for i, js in cut13._search(cat, a_idx, b_idx, cut13.RADIUS_KAU):
    if len(js) == 0:
        continue
    k, kb = a_idx[i], b_idx[i]
    dpar = np.abs(f["parallax"][k] - f["parallax"][js]) / np.hypot(f["parallax_error"][k], f["parallax_error"][js])
    dmu, sdmu = cut13._delta_mu_and_sigma(f["pmra"][k], f["pmdec"][k], f["pmra"][js], f["pmdec"][js], f["pmra_error"][k], f["pmdec_error"][k], f["pmra_error"][js], f["pmdec_error"][js])
    thk = cut13._ang_sep_arcsec(f["ra"][k], f["dec"][k], f["ra"][js], f["dec"][js])
    thb = cut13._ang_sep_arcsec(f["ra"][kb], f["dec"][kb], f["ra"][js], f["dec"][js])
    g = cat["phot_g_mean_mag"][js]
    with np.errstate(invalid="ignore"):
        for kind, bound in (("literal", cut13.N_SIGMA_PM * sdmu), ("orbit", cut13.orbit_allowance(f["parallax"][k], thk) + cut13.SDMU_MULT * sdmu)):
            hit = (dpar < cut13.N_SIGMA_PLX) & (dmu < bound) & (g < cut13.G_MAX)
            hits[kind][int(i)] = [dict(neighbour=int(cat["source_id"][j]), G=float(g[m]), sep_primary_kAU=float(thk[m] / f["parallax"][k]), sep_secondary_kAU=float(thb[m] / f["parallax"][k]),
                                       dparallax_sigma=float(dpar[m]), dmu_masyr=float(dmu[m]), dmu_bound_masyr=float(bound[m]), in_extract=bool(in_extract[j]),
                                       extract_fails=[] if in_extract[j] else fails(j)) for m, j in zip(np.flatnonzero(hit), js[hit])]
ok_ctrl = True
for kind in ("literal", "orbit"):
    for n, ci in enumerate(idx):
        has = len(hits[kind].get(n, [])) > 0
        ok_ctrl &= (has == bool(fl[kind][ci]))
P(f"[{'PASS' if ok_ctrl else 'FAIL'}] CONTROL the attribution reproduces every pair's cones flag (flagged iff >= 1 hitting neighbour): {len(flagged)} flagged and {len(unflagged)} unflagged pairs, both criteria")
RES = dict(control_ok=bool(ok_ctrl), pairs=[])
for n, ci in enumerate(flagged):
    ci = int(ci)
    r0, r1 = a_rows[ci], b_rows[ci]
    sep_pair = float(cut13._ang_sep_arcsec(S["ra"][r0], S["dec"][r0], S["ra"][r1], S["dec"][r1]) / S["parallax"][r0])
    P(f"\ncandidate {ci}: source_id1 {int(c1[ci])}, source_id2 {int(c2[ci])}; {'final' if is_final[ci] else 'delta'}; parallax {float(S['parallax'][r0]):.2f} mas; projected separation {sep_pair:.2f} kAU; "
      f"flagged by: cones-literal {bool(fl['literal'][ci])}, cones-orbit {bool(fl['orbit'][ci])}, extract-literal {bool(fx['extract-literal'][ci])}, extract-builder {bool(fx['extract-builder'][ci])}")
    entry = dict(index=ci, source_id1=int(c1[ci]), source_id2=int(c2[ci]), final=bool(is_final[ci]), parallax=float(S["parallax"][r0]), sep_pair_kAU=sep_pair,
                 flags=dict(cones_literal=bool(fl["literal"][ci]), cones_orbit=bool(fl["orbit"][ci]), extract_literal=bool(fx["extract-literal"][ci]), extract_builder=bool(fx["extract-builder"][ci])), hits={})
    for kind in ("literal", "orbit"):
        hh = hits[kind].get(n, [])
        entry["hits"][kind] = hh
        for h in hh:
            P(f"   {kind:7s} hit: source_id {h['neighbour']}  G {h['G']:.2f}  {h['sep_primary_kAU']:.2f} kAU from the primary, {h['sep_secondary_kAU']:.2f} kAU from the secondary;  "
              f"dparallax {h['dparallax_sigma']:.2f} sigma;  dmu {h['dmu_masyr']:.3f} against a bound {h['dmu_bound_masyr']:.3f} mas/yr;  "
              f"{'IN the extract' if h['in_extract'] else 'NOT in the extract: ' + '; '.join(h['extract_fails'])}")
    RES["pairs"].append(entry)
nh = [h for e in RES["pairs"] for h in e["hits"]["literal"]]
if nh:
    P(f"\nSUMMARY (literal hits over the flagged pairs): {len(nh)} hitting neighbours; in the extract {sum(h['in_extract'] for h in nh)}; not in the extract {sum(not h['in_extract'] for h in nh)} "
      f"(by failed extract condition: " + ", ".join(f"{c} {sum(c in h['extract_fails'] for h in nh)}" for c in sorted({c for h in nh for c in h['extract_fails']})) + ")")
P(f"\n({time.time() - T0:.0f} s)")
(HERE / "cones_flagged_attribution_dr3.out").write_text("\n".join(LOG) + "\n")
(HERE / "cones_flagged_attribution_dr3.json").write_text(json.dumps(RES, indent=1) + "\n")
sys.exit(0 if ok_ctrl else 1)
