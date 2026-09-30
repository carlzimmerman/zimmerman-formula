#!/usr/bin/env python3
"""DR4-READY-1, WP4: the DR3 dry run of the cut-12 NSS union on REAL archive output (query Q2, run by q_fetch_dr3.py with the
owner's go).  NO NETWORK (socket guard): reads the four gitignored Q2 FITS files and the frozen DR3 sample.

What it checks: the loaders read the archive's FITS output; run() and run_a17() process the real files end to end; and the
union agrees with the frozen build's DR3 proxy (gaia_source.non_single_star = 0 for every component that entered the sample).
Declared readings (DR3 analogues; the DR3 tables are all one-source):
  * 'A17a_dr3'   counts all four DR3 solution tables -- the DR3 analogue of the Amendment 17 draft's (a) reading of row 12;
  * '15b_dr3'    counts nss_two_body_orbit and nss_acceleration_astro only -- Amendment 15(b)'s narrower wording
                 ("an astrometric orbit, an acceleration solution, or a spectroscopic orbit"); nss_non_linear_spectro and
                 nss_vim_fl are then excluded with that written reason.
DISCLOSURE: these readings were written after q_fetch_dr3.py had printed the Q2 row counts (0 rows in each of the four
tables).  With zero rows every reading necessarily gives the same answer, so the choice could not steer the result.
This is a MECHANICS check with an answer expected by construction (the frozen build already required non_single_star = 0,
which in DR3 marks NSS-table membership); it is not an independent test of the query (no positive control was queried: a
query on known NSS sources was not in the approved scope and needs its own go).
Run: python3 prep_2026/gaia_dr4_prep/dr4_ready_1/wp4_nss_dryrun_dr3.py
"""
import sys
sys.dont_write_bytecode = True
import csv, json, socket
from pathlib import Path
import numpy as np


def _blocked(*a, **k):
    raise RuntimeError("network access attempted in an offline dry run (blocked by design)")


socket.socket.connect = socket.socket.connect_ex = socket.create_connection = socket.getaddrinfo = _blocked
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import cut12_nss_union as W4

WB = REPO / "real_research" / "data" / "widebinaries"
Q = WB / "dr3_extract" / "dr4_ready_1"
TABLES = ("nss_two_body_orbit", "nss_acceleration_astro", "nss_non_linear_spectro", "nss_vim_fl")
REASON_15B = ("Amendment 15(b)'s wording names an astrometric orbit, an acceleration solution or a spectroscopic orbit; this "
              "table holds none of those (trend or variability-induced-mover models)")


def main():
    rows = list(csv.DictReader(open(WB / "dr3_extract" / "wide_binaries_dr3.csv")))
    pa = np.array([int(r["source_id1"]) for r in rows], np.int64)
    pb = np.array([int(r["source_id2"]) for r in rows], np.int64)
    files = {t: str(Q / f"q2_{t}.fits") for t in TABLES}
    man_q = json.loads((HERE / "manifest_q_dr3.json").read_text())
    out = {"n_pairs": int(len(pa)), "n_components": int(len(np.unique(np.concatenate([pa, pb])))),
           "q2_rows": {t: man_q["queries"][f"Q2_{t}"]["rows"] for t in TABLES},
           "q2_sha256": {t: man_q["queries"][f"Q2_{t}"]["sha256"] for t in TABLES}}
    rd = {"A17a_dr3": {"counted": list(TABLES), "excluded": {}},
          "15b_dr3": {"counted": ["nss_two_body_orbit", "nss_acceleration_astro"],
                      "excluded": {"nss_non_linear_spectro": REASON_15B, "nss_vim_fl": REASON_15B}}}
    out["run"] = {}
    for name, r in rd.items():
        fl, rep = W4.run({"cut12_nss": {"counted_tables": r["counted"], "excluded": r["excluded"], "id_files": dict(files)}}, pa, pb)
        out["run"][name] = {"n_pairs_flagged": int(fl.sum()), "row_counts": rep["row_counts"],
                            "n_components_flagged": rep["n_components_flagged"]}
    # run_a17 takes all readings at once: a table counted by one reading and not by another needs no 'excluded' entry (the
    # 15(b) reason above is recorded in the output instead); 'excluded' there is for tables no reading counts
    fl17, rep17 = W4.run_a17({"cut12_nss": {"id_files": dict(files),
                                            "readings": {k: {"counted_tables": v["counted"]} for k, v in rd.items()}}}, pa, pb)
    out["not_counted_reason_15b_dr3"] = REASON_15B
    out["run_a17"] = {k: int(v.sum()) for k, v in fl17.items()}
    out["run_a17_per_table"] = rep17["per_table"]
    S = np.load(WB / "dr3_extract" / "stage_A.npz")
    order = np.argsort(S["source_id"])
    comps = np.unique(np.concatenate([pa, pb]))
    i = order[np.searchsorted(S["source_id"][order], comps)]
    assert np.all(S["source_id"][i] == comps)
    nss = np.asarray(S["non_single_star"])[i]
    out["frozen_proxy"] = {"components_with_non_single_star_nonzero": int((nss != 0).sum()),
                           "extract_sources_with_non_single_star_nonzero": int((np.asarray(S["non_single_star"]) != 0).sum()),
                           "extract_sources": int(len(S["source_id"]))}
    checks = {
        "W1 the four Q2 FITS files load through load_ids (run) and load_entries (run_a17)":
            all(v["row_counts"] == out["q2_rows"] for v in out["run"].values()),
        "W2 every reading flags 0 pairs, in run() and run_a17()":
            all(v["n_pairs_flagged"] == 0 for v in out["run"].values()) and all(v == 0 for v in out["run_a17"].values()),
        "W3 the union agrees with the frozen DR3 proxy (non_single_star = 0 for all components)":
            out["frozen_proxy"]["components_with_non_single_star_nonzero"] == 0,
    }
    out["checks"] = checks
    ok = all(checks.values())
    lines = [f"WP4 DR3 dry run: {out['n_pairs']} pairs, {out['n_components']} components; Q2 rows {out['q2_rows']}"]
    lines += [f"  run() {k}: {v}" for k, v in out["run"].items()]
    lines += [f"  run_a17(): pairs flagged {out['run_a17']}", f"  frozen proxy: {out['frozen_proxy']}"]
    lines += [f"  [{'PASS' if v else 'FAIL'}] {k}" for k, v in checks.items()]
    lines.append("  NOTE: expected by construction (the frozen build required non_single_star = 0); a mechanics check, not an "
                 "independent test of the query (no positive control; see the docstring)")
    print("\n".join(lines))
    (HERE / "wp4_nss_dryrun_dr3.json").write_text(json.dumps(out, indent=1) + "\n")
    (HERE / "wp4_nss_dryrun_dr3.out").write_text("\n".join(lines) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
