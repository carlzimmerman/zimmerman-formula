#!/usr/bin/env python3
"""DR4-READY-1: offline tests of WP1 (cut13_allsource.py) and WP4 (cut12_nss_union.py) on SYNTHETIC data.

NEW file.  NO NETWORK: every outgoing connection raises (socket guard).  Temporary id files go to a system temp dir, never
into the repo.  The real DR3 dry runs of WP1 and WP4 need archive queries Q1 and Q2 (PLAN.md), which need the owner's go.
Exit 0 only if every test passes AND both removal controls change the result.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_wp1_wp4_offline.py
"""
import sys
sys.dont_write_bytecode = True
import json, socket, tempfile, math
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline test (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cut13_allsource as W1
import cut12_nss_union as W4

RES, LOG = {}, []


def T(name, ok, detail=""):
    RES[name] = bool(ok)
    line = f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else "")
    print(line)
    LOG.append(line)


# ------------------------------------------------------------------ WP1
print("WP1 cut13_allsource (offline, synthetic)")
T("T1 radius = 30 kAU / d(primary) = 30 * plx arcsec", abs(W1.radius_arcsec(4.0) - 120.0) < 1e-12 and abs(W1.radius_arcsec(20.0) - 600.0) < 1e-12,
  f"plx 4 -> {W1.radius_arcsec(4.0):.1f}\", plx 20 -> {W1.radius_arcsec(20.0):.1f}\"")
up = W1.upload_table(np.array([7, 8]), [10.0, 20.0], [5.0, 6.0], [10.01, 20.01], [5.0, 6.0], [4.0, 20.0])
T("T2 upload table: two rows per pair, radius in degrees from the PRIMARY's parallax",
  len(up["pair_id"]) == 4 and list(up["comp"]) == [0, 1, 0, 1] and abs(up["radius_deg"][2] - 600 / 3600) < 1e-15,
  f"radius_deg {np.round(up['radius_deg'] * 3600, 3).tolist()} arcsec")
q3 = W1.adql_cones("gaiadr3.gaia_source")
q4 = W1.adql_cones("gaiadr4.all_source_astrometry", g_table="gaiadr4.all_source_photometry")
T("T3 ADQL: server-side CONTAINS/CIRCLE cone join on the upload; DR4 form joins G from the photometry table",
  "CONTAINS(POINT('ICRS', s.ra, s.dec), CIRCLE('ICRS', u.ra, u.dec, u.radius_deg))" in q3 and "tap_upload.pairs" in q3
  and "s.phot_g_mean_mag AS phot_g_mean_mag" in q3 and "LEFT OUTER JOIN gaiadr4.all_source_photometry AS g" in q4
  and "g.phot_g_mean_mag AS phot_g_mean_mag" in q4)


def synth(drop_planted=False):
    """three pairs at 200 pc (plx 5 mas, radius 150"): pair 0 has a co-moving third at 25 kAU (125"), G 18; pair 1 has a field
    star at 50" (parallax 2 mas) and a co-moving star at 35 kAU (175", outside); pair 2 has a co-moving third with NO G."""
    plx, e_plx, pm, e_pm = 5.0, 0.02, (30.0, -20.0), 0.02
    base_ra = np.array([30.0, 60.0, 90.0]); dec = np.array([10.0, 10.0, 10.0])
    sep_b = 2000 / 200 / 3600                                    # companion at 10 kAU east (deg, before cos(dec))
    pairs = {"source_id_a": np.array([1, 2, 3]), "source_id_b": np.array([11, 12, 13])}
    for suf, ra in (("_a", base_ra), ("_b", base_ra + sep_b * 5 / math.cos(math.radians(10.0)))):
        pairs["ra" + suf] = ra; pairs["dec" + suf] = dec.copy()
        pairs["parallax" + suf] = np.full(3, plx); pairs["parallax_error" + suf] = np.full(3, e_plx)
        pairs["pmra" + suf] = np.full(3, pm[0]); pairs["pmdec" + suf] = np.full(3, pm[1])
        pairs["pmra_error" + suf] = np.full(3, e_pm); pairs["pmdec_error" + suf] = np.full(3, e_pm)
        pairs["phot_g_mean_mag" + suf] = np.array([15.0, 15.5, 16.0]) + (0.5 if suf == "_b" else 0.0)
    d_arc = lambda arcsec: arcsec / 3600 / math.cos(math.radians(10.0))
    nb = {k: [] for k in ("source_id",) + W1.COLS[1:] + ("phot_g_mean_mag", "pair_id", "comp")}
    def add(sid, ra, dc, p, pmx, pmy, g, pid):
        for k, v in zip(("source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error",
                         "phot_g_mean_mag", "pair_id", "comp"), (sid, ra, dc, p, e_plx, pmx, pmy, e_pm, e_pm, g, pid, 0)):
            nb[k].append(v)
    if not drop_planted:
        add(101, base_ra[0], dec[0] + 125 / 3600, plx, pm[0] + 0.01, pm[1], 18.0, 0)                 # the planted third
    add(102, base_ra[1] + d_arc(50), dec[1], 2.0, 5.0, 3.0, 17.0, 1)                                    # field star
    add(103, base_ra[1], dec[1] + 175 / 3600, plx, pm[0], pm[1], 17.5, 1)                               # co-moving, outside
    add(104, base_ra[2], dec[2] - 60 / 3600, plx, pm[0], pm[1], np.nan, 2)                              # co-moving, no G
    return pairs, {k: np.array(v) for k, v in nb.items()}


lit, orb, man = W1.evaluate(*synth())
T("T4 planted third (pair 0) flagged by BOTH criteria; field star and the star outside 30 kAU (pair 1) not; no-G third (pair 2) "
  "not flagged but counted", lit.flags.tolist() == [True, False, False] and orb.flags.tolist() == [True, False, False]
  and lit.n_no_g >= 1 and lit.n_no_g_kin >= 1, f"literal {lit.flags.tolist()}, orbit-aware {orb.flags.tolist()}, "
  f"n_no_g {lit.n_no_g}, n_no_g_kin {lit.n_no_g_kin}; manifest {json.dumps(man)}")
lit_m, orb_m, _ = W1.evaluate(*synth(drop_planted=True))
T("M1 (control) removing the planted third removes the flag", lit_m.flags.tolist() == [False, False, False]
  and orb_m.flags.tolist() == [False, False, False], f"literal {lit_m.flags.tolist()}")

# ------------------------------------------------------------------ WP4
print("WP4 cut12_nss_union (offline, synthetic id files in a temp dir)")
tmp = Path(tempfile.mkdtemp(prefix="dr4ready_wp4_"))
np.savez(tmp / "tbo.npz", source_id=np.array([999, 12, 5555], np.int64))                              # plants pair 1's b
(tmp / "acc.csv").write_text("source_id\n777\n888\n")
np.savez(tmp / "mult.npz", source_id=np.array([1, 2, 3], np.int64))                                  # excluded table
man4 = {"cut12_nss": {"counted_tables": ["nss_two_body_orbit", "nss_acceleration_astro"],
                      "excluded": {"nss_multiplicity": "example reason: a pairs table, not a single-star NSS solution"},
                      "id_files": {"nss_two_body_orbit": str(tmp / "tbo.npz"), "nss_acceleration_astro": str(tmp / "acc.csv"),
                                   "nss_multiplicity": str(tmp / "mult.npz")}}}
pa, pb = np.array([1, 2, 3]), np.array([11, 12, 13])
fl, rep = W4.run(man4, pa, pb)
T("T5 planted NSS id (pair 1's component b in a counted table) flags pair 1 only; the excluded table flags nothing",
  fl.tolist() == [False, True, False], f"flags {fl.tolist()}; row counts {rep['row_counts']}")
try:
    W4.run({"cut12_nss": {"counted_tables": None, "id_files": {}}}, pa, pb)
    T("T6 undeclared counted_tables raises", False)
except ValueError:
    T("T6 undeclared counted_tables raises", True)
try:
    W4.run({"cut12_nss": {"counted_tables": ["nss_masses"], "id_files": {}}}, pa, pb)
    T("T7 a counted table without an id file raises", False)
except KeyError:
    T("T7 a counted table without an id file raises", True)
np.savez(tmp / "dr4_pairs.npz", source_id=np.array([3], np.int64))
man6 = {"cut12_nss": {"counted_tables": ["nss_acceleration_astro", "nss_two_body_orbit", "nss_multiple_orbits"],
                      "excluded": {}, "id_files": {"nss_acceleration_astro": str(tmp / "acc.csv"),
                                                   "nss_two_body_orbit": str(tmp / "tbo.npz"),
                                                   "nss_multiple_orbits": str(tmp / "dr4_pairs.npz")}}}
fl6, _ = W4.run(man6, pa, pb)
T("T8 DR4-style table names are run-time data (no DR3 list assumed)", fl6.tolist() == [False, True, True], f"flags {fl6.tolist()}")
np.savez(tmp / "tbo.npz", source_id=np.array([999, 5555], np.int64))
fl_m, _ = W4.run(man4, pa, pb)
T("M2 (control) removing the planted id removes the flag", fl_m.tolist() == [False, False, False], f"flags {fl_m.tolist()}")

ok = all(RES.values())
print(f"\n{sum(RES.values())}/{len(RES)} pass -> {'ALL PASS' if ok else 'FAILURES'}")
(HERE / "test_wp1_wp4_offline_results.json").write_text(json.dumps(dict(results=RES, wp1_manifest=man), indent=1) + "\n")
(HERE / "test_wp1_wp4_offline.out").write_text("\n".join(LOG) + f"\n{sum(RES.values())}/{len(RES)} pass\n")
sys.exit(0 if ok else 1)
