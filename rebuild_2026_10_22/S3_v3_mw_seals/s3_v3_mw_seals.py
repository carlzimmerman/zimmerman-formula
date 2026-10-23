#!/usr/bin/env python3
"""S3_v3_mw_seals lane checker: aggregates the four parts' committed results (one line per check) and the headline numbers.

Parts (run first, each OMP_NUM_THREADS=1 nice -n 15, every AQUAL solve in a short-lived child process):
  s3_partA_mw.py (MW outer slope), s3_partB_kappa.py (kappa), s3_partC_seal.py (sealed DR4 file), s3_partD_alma.py (ALMA).
--mutate: reads the Part A / Part D MUTATE results (mu == 1 inside the solver); A7 and D6 must FAIL (frozen §6).
Writes s3_v3_mw_seals.out / _results.json (or *_MUTATE).  Exit 0 iff every check passes.
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = "--mutate" in sys.argv or os.environ.get("S3_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(s)


parts = [("A", "s3_partA_mw_results"), ("D", "s3_partD_alma_results")] if MUT else \
        [("A", "s3_partA_mw_results"), ("B", "s3_partB_kappa_results"), ("C", "s3_partC_seal_results"), ("D", "s3_partD_alma_results")]
checks, summary = [], {}
P(f"S3_v3_mw_seals lane checker {'(MUTATE: mu == 1)' if MUT else ''}")
for lab, stem in parts:
    fn = os.path.join(HERE, f"{stem}{TAG}.json")
    if not os.path.exists(fn):
        P(f"{lab}-MISSING FAIL {fn} not found"); checks.append(False); continue
    d = json.load(open(fn))
    for c in d["checks"]:
        P(f"{lab}:{c['name']} {'PASS' if c['ok'] else 'FAIL'} {c['detail']}")
        checks.append(bool(c["ok"]))
    if lab == "A":
        summary["A"] = {"reading": d.get("reading"), "v3_step": d.get("reading", {}).get("primary_step")}
    if lab == "B":
        st = d["steps"]
        summary["B"] = {k: {f: dict(kappa=st[k][f]["kappa"], err=st[k][f]["kappa_err"], verdict=st[k][f]["verdict"]) for f in ("canonical", "alt")}
                        for k in ("record_numono", "K_kernel_nu1", "A_aqual_disc")}
        summary["B"]["label"] = d["label"]
    if lab == "C":
        summary["C"] = dict(sha256=d.get("sha256_this_run"), use3d=d.get("use3d"))
        rr = os.path.join(HERE, "s3_partC_seal_results_C1RERUN.json")
        if os.path.exists(rr):
            for c in json.load(open(rr))["checks"]:
                if c["name"] == "C1":
                    P(f"C:C1 {'PASS' if c['ok'] else 'FAIL'} {c['detail']}"); checks.append(bool(c["ok"]))
        else:
            P("C:C1 FAIL independent rerun missing"); checks.append(False)
    if lab == "D":
        summary["D"] = dict(decision=d["decision"], sha256=d.get("sealed_sha256"))
n, ok = len(checks), sum(checks)
P(json.dumps(summary, indent=1, default=str))
P(f"S3_V3_MW_SEALS COMPLETE: {ok}/{n} checks PASS.")
json.dump(dict(mutate=MUT, n_checks=n, n_pass=ok, summary=summary), open(os.path.join(HERE, f"s3_v3_mw_seals_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"s3_v3_mw_seals{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok == n else 1)
