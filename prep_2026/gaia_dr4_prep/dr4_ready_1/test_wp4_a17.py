#!/usr/bin/env python3
"""DR4-READY-1, WP4: offline tests of the Amendment 17 readings in cut12_nss_union.run_a17 (the amendment is a DRAFT, NOT
FILED: prep_2026/gaia_dr4_prep/AMENDMENT17_DRAFT_NOT_FILED.md revision 2).  SYNTHETIC data; table names are the draft data
model's (2026-06-26, confirm on release day) but every row is invented.  NO NETWORK (socket guard).  Temporary files go to a
system temp dir, never into the repo.
Exit 0 only if every test passes AND each of the three MUTATE controls makes at least one test fail.
First run (kept as test_wp4_a17_firstrun.out): G6 failed because this harness's manifest() treated readings={} as "use the
default readings" (`readings or {...}`); fixed to `readings if readings is not None`.  Second run: 19/19 passed and 3/3
mutations were detected, but the exit was 1 because the expected-failure check compared the short id ("A1") with the full
test names; fixed to compare the id.  run_a17 itself was not changed by either fix.
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/test_wp4_a17.py
"""
import sys
sys.dont_write_bytecode = True
import json, socket, tempfile
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline test (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cut12_nss_union as W4

TMP = Path(tempfile.mkdtemp(prefix="dr4ready_a17_"))
RP = ["ResolvedPairFixed", "ResolvedPairLinear", "ResolvedPairAcceleration", "ResolvedPairJerk", "DiverseAcceleration",
      "DiverseJerk"]                                     # A17 draft section 2; the stored strings are recorded on release day
COUNTED = ["nss_acceleration_astro", "nss_multiple_orbits", "nss_non_linear_spectro", "nss_resolved_pair",
           "nss_two_body_orbit", "nss_vim_fl"]


def csv_write(name, header, rows):
    p = TMP / name
    p.write_text(",".join(header) + "\n" + "".join(",".join("" if v is None else str(v) for v in r) + "\n" for r in rows))
    return str(p)


# pipeline pairs k = 0..5: (1,11) (2,12) (3,13) (4,14) (5,15) (6,16)
PA, PB = np.array([1, 2, 3, 4, 5, 6]), np.array([11, 12, 13, 14, 15, 16])


def files(extra_rp_rows=()):
    rp = [(11, 1, "ResolvedPairLinear"),                 # own pair 0, stored SWAPPED (secondary = component a)
          (2, 12, "DiverseAcceleration"),                # own pair 1, likely hierarchical -> rejects
          (3, 999, "ResolvedPairFixed"),                 # component of pair 2 with a THIRD source -> rejects
          (888, 777, "ResolvedPairFixed")] + list(extra_rp_rows)  # touches no component
    return {
        "nss_resolved_pair": csv_write("rp.csv", ["source_id", "source_id_secondary", "solution_type"], rp),
        "nss_two_body_orbit": csv_write("tbo.csv", ["source_id", "solution_type"], [(14, "Orbital"), (4242, "SB1")]),
        "nss_acceleration_astro": csv_write("acc.csv", ["source_id", "solution_type"], [(5151, "Acceleration7")]),
        "nss_multiple_orbits": csv_write("mo.csv", ["source_id", "solution_type"], []),
        "nss_non_linear_spectro": csv_write("nls.csv", ["source_id", "solution_type"], []),
        "nss_vim_fl": csv_write("vim.csv", ["source_id", "solution_type"], []),
        "nss_masses": csv_write("masses.csv", ["source_id"], [(5,)]),                     # only-uncounted component
        "nss_multiplicity": csv_write("mult.csv", ["source_id", "number_of_pairs"], [(1, 1), (11, 1)]),
        "optical_pair": csv_write("opt.csv", ["source_id", "source_id_secondary", "acceleration_flag"],
                                  [(6, 5000, 1), (16, 6, 0), (13, 4000, None)]),
        "nss_epoch_flags": csv_write("epoch.csv", ["source_id", "source_id_secondary", "solution_type"], [(1, 11, "x")]),
    }


def manifest(f, readings=None, **over):
    c = {"id_files": f, "two_source_tables": ["nss_resolved_pair", "optical_pair"],
         "solution_types_recorded": {"nss_resolved_pair": RP},
         "diagnostic": {"uncounted_tables": ["nss_masses", "nss_multiplicity"], "optical_pair_table": "optical_pair",
                        "optical_pair_flag_column": "acceleration_flag"},
         "excluded": {"nss_epoch_flags": "DataLink-only, not TAP; per-transit flags, no solution parameters (A17 (a))"},
         "readings": readings if readings is not None else {
             "A17_primary": {"counted_tables": COUNTED,
                             "own_pair_exempt": {"nss_resolved_pair": ["ResolvedPairFixed", "ResolvedPairLinear"]}},
             "V17a": {"counted_tables": COUNTED, "own_pair_exempt": {}},
             "V17b": {"counted_tables": [t for t in COUNTED if t != "nss_resolved_pair"], "own_pair_exempt": {}}}}
    c.update(over)
    return {"cut12_nss": c}


def suite(verbose=True):
    res, log = {}, []

    def T(name, ok, detail=""):
        res[name] = bool(ok)
        line = f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else "")
        log.append(line)
        if verbose:
            print(line)

    out, rep = W4.run_a17(manifest(files()), PA, PB)
    p, a, b = out["A17_primary"].tolist(), out["V17a"].tolist(), out["V17b"].tolist()
    T("A1 own-pair ResolvedPairLinear stored in swapped order is matched as an unordered pair and KEPT by the primary", not p[0],
      f"primary {p}")
    T("A2 own-pair DiverseAcceleration REJECTS under the primary", p[1])
    T("A3 third-source ResolvedPairFixed REJECTS under the primary", p[2])
    T("A4 a one-source counted row (nss_two_body_orbit on component 14) rejects under every reading", p[3] and a[3] and b[3])
    T("A5 primary = [F,T,T,T,F,F]; V17a (no exemption) = [T,T,T,T,F,F]; V17b (nss_resolved_pair not counted) = [F,F,F,T,F,F]",
      p == [False, True, True, True, False, False] and a == [True, True, True, True, False, False]
      and b == [False, False, False, True, False, False], f"primary {p}, V17a {a}, V17b {b}")
    rr = rep["readings"]
    T("A6 the diagnostic counts the component found only in nss_masses (5) and the nonzero optical flag without a counted row "
      "(6); V17b also counts 1 and 11 (in nss_multiplicity, whose resolved-pair row is not counted there); nothing is rejected "
      "for it", rr["A17_primary"]["diagnostic"]["n_components_only_in_uncounted_tables"] == 1
      and rr["A17_primary"]["diagnostic"]["n_components_nonzero_optical_flag_without_counted_row"] == 1
      and rr["V17b"]["diagnostic"]["n_components_only_in_uncounted_tables"] == 3
      and rr["A17_primary"]["diagnostic"]["flag_nonzero"] and not p[4] and not p[5],
      json.dumps({k: v["diagnostic"] for k, v in rr.items()}))
    T("A7 per-table / per-solution_type counts of rows touching the sample; own-pair and third-source entries by type",
      rep["per_table"]["nss_resolved_pair"]["by_solution_type"] == {"ResolvedPairLinear": 1, "DiverseAcceleration": 1,
                                                                   "ResolvedPairFixed": 1}
      and rep["own_pair_entries_by_type"] == {"nss_resolved_pair": {"ResolvedPairLinear": 1, "DiverseAcceleration": 1}}
      and rep["third_source_entries_by_type"] == {"nss_resolved_pair": {"ResolvedPairFixed": 1}}
      and rep["per_table"]["nss_two_body_orbit"]["rows_touching_sample"] == 1
      and rr["A17_primary"]["n_pairs_kept_only_by_the_exemption"] == 1 and rr["V17a"]["n_pairs_kept_only_by_the_exemption"] == 0,
      json.dumps(rep["per_table"]["nss_resolved_pair"]))
    T("A8 optical_pair: the own-pair row (16,6) is reported, the null flag on a sample row is counted, neither rejects",
      rep["diagnostic_tables"]["optical_pair_own_pair_rows (reported only)"] == 1
      and rep["diagnostic_tables"]["optical_rows_touching_sample_with_null_flag"] == 1)
    out9, rep9 = W4.run_a17(manifest(files(extra_rp_rows=[(4, 14, "ResolvedPairWeird"), (15, 5, "ResolvedPairLinear")])), PA, PB)
    T("A9 a solution_type not in the recorded list is reported and never exempt; a recorded linear own-pair row is still kept",
      rep9["types_seen_not_recorded"] == {"nss_resolved_pair": ["ResolvedPairWeird"]} and out9["A17_primary"][3]
      and not out9["A17_primary"][4], f"{rep9['types_seen_not_recorded']}")

    def raises(fn, exc):
        try:
            fn()
            return False
        except exc:
            return True
    f = files()
    T("G1 an exempt type missing from the recorded strings raises (a typo cannot silently disable the exemption)",
      raises(lambda: W4.run_a17(manifest(f, readings={"r": {"counted_tables": COUNTED, "own_pair_exempt": {
          "nss_resolved_pair": ["ResolvedPairLinaer"]}}}), PA, PB), ValueError))
    T("G2 an exemption without recorded solution_type strings raises (A17 (d))",
      raises(lambda: W4.run_a17(manifest(f, solution_types_recorded={}), PA, PB), ValueError))
    T("G3 a two-source table not declared two-source raises (it would otherwise be half-matched)",
      raises(lambda: W4.run_a17(manifest(f, two_source_tables=["optical_pair"], readings={
          "r": {"counted_tables": COUNTED, "own_pair_exempt": {}}}), PA, PB), ValueError))
    f_bad = dict(f, nss_resolved_pair=csv_write("rp_noseq.csv", ["source_id", "solution_type"], [(1, "ResolvedPairLinear")]))
    T("G4 a declared two-source table without source_id_secondary raises",
      raises(lambda: W4.run_a17(manifest(f_bad), PA, PB), KeyError))
    f_stray = dict(f, some_new_table=csv_write("new.csv", ["source_id"], [(1,)]))
    T("G5 a supplied table that is neither counted, diagnostic nor excluded with a reason raises",
      raises(lambda: W4.run_a17(manifest(f_stray), PA, PB), ValueError))
    T("G6 undeclared readings raise", raises(lambda: W4.run_a17(manifest(f, readings={}), PA, PB), ValueError))
    T("G7 the pre-amendment run() refuses a two-source table (it matches source_id only)",
      raises(lambda: W4.run({"cut12_nss": {"counted_tables": ["nss_resolved_pair"], "excluded": {},
                                          "id_files": {"nss_resolved_pair": f["nss_resolved_pair"]}}}, PA, PB), ValueError))
    q1, q2 = W4.adql_nss("gaiadr4.nss_resolved_pair", two_source=True), W4.adql_nss("gaiadr4.nss_two_body_orbit")
    T("Q1 release-day query text: a two-source table is searched on BOTH id columns, a one-source table on source_id",
      len(q1) == 2 and "ON t.source_id = u.source_id" in q1[0] and "ON t.source_id_secondary = u.source_id" in q1[1]
      and "t.source_id_secondary" in q1[0] and len(q2) == 1 and "source_id_secondary" not in q2[0])
    one = {t: f[t] for t in ("nss_two_body_orbit", "nss_acceleration_astro")}
    fl_old, _ = W4.run({"cut12_nss": {"counted_tables": list(one), "excluded": {}, "id_files": one}}, PA, PB)
    out_new, _ = W4.run_a17({"cut12_nss": {"id_files": one, "readings": {"all": {"counted_tables": list(one)}}}}, PA, PB)
    T("B1 one-source tables only: run_a17 reproduces the pre-amendment run() pair flags", fl_old.tolist() == out_new["all"].tolist(),
      f"run {fl_old.tolist()}, run_a17 {out_new['all'].tolist()}")
    from astropy.table import Table, MaskedColumn
    fp = TMP / "rp.fits"
    Table({"source_id": np.array([11, 3], np.int64),
           "source_id_secondary": MaskedColumn(np.array([1, 0], np.int64), mask=[False, True]),
           "solution_type": np.array(["ResolvedPairLinear", "ResolvedPairFixed"])}).write(fp, format="fits", overwrite=True)
    e = W4.load_entries(fp, two_source=True)
    T("F1 FITS loader: masked source_id_secondary -> None (a one-source row), strings decoded", e["source_id_secondary"] == [1, None]
      and e["solution_type"] == ["ResolvedPairLinear", "ResolvedPairFixed"], f"{e['source_id_secondary']}, {e['solution_type']}")
    return res, log


print("WP4 Amendment 17 readings (offline, synthetic; the amendment is NOT filed)")
RES, LOG = suite()
MUT = {}
for m, wanted in (("ordered", "A1"), ("exempt_all", "A2"), ("third_as_own", "A3")):
    W4._MUTATE_A17 = m
    try:
        r, _ = suite(verbose=False)
        failed = sorted(k for k, v in r.items() if not v)
    except Exception as exc:                            # a crash under a mutation also counts as detected
        failed = [f"crash: {type(exc).__name__}"]
    finally:
        W4._MUTATE_A17 = None
    MUT[m] = dict(failed=failed, detected=bool(failed), expected_to_fail=wanted,
                  expected_failed=any(f.split(" ")[0] == wanted or f.startswith("crash") for f in failed))
    line = f"  [{'DETECTED' if failed else 'MISSED'}] MUTATE {m}: failing tests {failed}"
    print(line)
    LOG.append(line)
ok = all(RES.values()) and all(v["detected"] and v["expected_failed"] for v in MUT.values())
print(f"\n{sum(RES.values())}/{len(RES)} pass; mutations detected {sum(v['detected'] for v in MUT.values())}/3 -> "
      f"{'ALL PASS' if ok else 'FAILURES'}")
(HERE / "test_wp4_a17_results.json").write_text(json.dumps(dict(results=RES, mutate=MUT), indent=1) + "\n")
(HERE / "test_wp4_a17.out").write_text("\n".join(LOG) + f"\n{sum(RES.values())}/{len(RES)} pass; mutations detected "
                                        f"{sum(v['detected'] for v in MUT.values())}/3\n")
sys.exit(0 if ok else 1)
