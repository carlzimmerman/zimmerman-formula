#!/usr/bin/env python3
"""Build highz_sigma_mstar.csv for L328 from the transcribed source tables in sources/ (every number from a published
TABLE or sentence -- provenance per row in the table_or_section / notes columns and in sources/*_notes.txt).

CONSTRUCTION RULES (fixed before the L328 statistic was computed):
  R1  z >= 4, a stellar mass, sigma_flag == 'det' (widths NOT corrected for instrumental broadening -- 'upper' -- would
      OVERESTIMATE sigma and bias a lower-bound test toward passing; 'lower' limits cannot violate a floor).
  R2  drop per-ring rows and rows flagged as outer-ring/duplicate measurements (not system-level).
  R3  the floor constrains the TOTAL kinetic energy <v^2>/3.  Integrated line widths (rotation not removed) are used as
      they are.  A rotation-removed sigma_0 is used ONLY with its rotation velocity: sigma_eff^2 = sigma_0^2 + V^2/3
      (= <v^2>/3 for a thin disk with isotropic sigma_0), V from v/sigma or from a tabulated V_rot; otherwise dropped.
  R4  one row per galaxy: priority (a) sigma_0 + V (deprojected, orientation-free) over (b) integrated widths; a lower-
      priority row within |dz| < 0.003 of a kept row is dropped (conservative: may drop distinct galaxies, never
      double-counts one; dropping at random does not bias the mean statistic).
"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = [os.path.join(HERE, "sources", f) for f in ("core.csv", "jwst_ifu.csv", "alma.csv")]
rows = []
for f in SRC:
    for r in csv.DictReader(open(f)):
        rows.append(r)


def num(x):
    try:
        return float(str(x).strip().lstrip("<=>~"))
    except ValueError:
        return None


cand, log = [], {"R1": 0, "R2": 0, "R3": 0}
for r in rows:
    z, s, m = num(r["z"]), num(r["sigma"]), num(r["logMstar"])
    if z is None or s is None or m is None or z < 4 or r["sigma_flag"].strip() != "det":
        log["R1"] += 1; continue
    if "ring R=" in r["name"] or "[sigma_ext]" in r["name"] or "DUPLICATE" in r["notes"]:
        log["R2"] += 1; continue
    es = num(r["sigma_err"]) or 0.0
    if r["rotation_removed"].strip().lower().startswith("yes"):
        vs = num(r["v_over_sigma"])
        V = vs * s if vs is not None else None
        if V is None:
            mm = re.search(r"V_rot\(R_e\)\s*=\s*([0-9.]+)", r["notes"])
            V = float(mm.group(1)) if mm else None
        if V is None:
            log["R3"] += 1; continue
        seff = (s * s + V * V / 3) ** 0.5
        pri, how = 0, f"sigma0={s:g} (+/-{es:g}), V={V:.1f}: sigma_eff=sqrt(sigma0^2+V^2/3)"
        es_eff = es * s / seff
    else:
        seff, pri, how, es_eff = s, 1, "integrated width (rotation included)", es
    cand.append(dict(name=r["name"], z=z, sigma=round(seff, 2), sigma_err=round(es_eff, 2), logMstar=m,
                     logMstar_err=num(r["logMstar_err"]) or 0.3, kinematic_type=r["kinematic_type"],
                     source_arXiv=r["source_arXiv"], construction=how, pri=pri))
cand.sort(key=lambda c: (c["pri"], c["source_arXiv"], c["name"]))
kept, dropped = [], 0
for c in cand:
    if any(abs(c["z"] - k["z"]) < 0.003 for k in kept):
        dropped += 1; continue
    kept.append(c)
kept.sort(key=lambda c: c["z"])
out = os.path.join(HERE, "highz_sigma_mstar.csv")
cols = ["name", "z", "sigma", "sigma_err", "logMstar", "logMstar_err", "kinematic_type", "source_arXiv", "construction"]
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(kept)
print(f"source rows {len(rows)}; dropped R1 {log['R1']}, R2 {log['R2']}, R3 (sigma_0 without V) {log['R3']}; "
      f"candidates {len(cand)}; dedup dropped {dropped}; KEPT {len(kept)} "
      f"({sum(1 for k in kept if k['pri']==0)} sigma_0+V, {sum(1 for k in kept if k['pri']==1)} integrated) from "
      f"{len(set(k['source_arXiv'] for k in kept))} papers -> {os.path.basename(out)}")
