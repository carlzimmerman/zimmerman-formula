#!/usr/bin/env python3
"""EUC6 fetch: neighbour counts around wide lenses, their matched controls, a positive control and blank fields.

Frozen criteria: FROZEN_CRITERIA.md (commit 62dbaa183b), sections 1-2.  ESA Euclid archive TAP, anonymous, paced.
One query per target: galaxies brighter than H_E = 22 in 10 kpc rings out to 1000 kpc (counts only, no rows).

Run:  python3 -I euc6_fetch.py --data-dir <dir with the two ECLIPSE csv files>
Resumable.  Writes euc6_targets.csv (samples) and euc6_rings.json (ring counts) next to this script.
"""
import argparse, csv, io, json, math, os, sys, time
import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EUC1_eclipse_saturation_ceiling"))
import euc1 as E
TAP = "https://eas.esac.esa.int/tap-server/tap/sync"
CUT = "flux_h_templfit > 5.75 AND spurious_flag = 0 AND det_quality_flag < 4 AND point_like_prob < 0.7"

def rings(ra, dec, z):
    kpc_deg = math.degrees(E.KPC / float(E.EUCLID.DA(z)))            # degrees per kpc
    dr, rmax = 10.0 * kpc_deg, 1000.0 * kpc_deg
    adql = ("SELECT FLOOR(DISTANCE(POINT('ICRS', right_ascension, declination), POINT('ICRS', %.7f, %.7f)) / %.9f) AS rbin, COUNT(*) AS n "
            "FROM dr1.mer_catalogue_wide_survey WHERE 1=CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', %.7f, %.7f, %.7f)) "
            "AND %s GROUP BY rbin" % (ra, dec, dr, ra, dec, rmax, CUT))
    for k in range(6):
        time.sleep(1.0)
        try:
            r = requests.get(TAP, params=dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=adql), headers={"User-Agent": "generic-client"}, timeout=120)
            if r.status_code == 200 and r.text.lstrip().lower().startswith("rbin"):
                c = [0] * 100
                for row in csv.DictReader(io.StringIO(r.text)):
                    b = int(float(row["rbin"]))
                    if 0 <= b < 100: c[b] += int(float(row["n"]))
                return c
            if r.status_code == 429: time.sleep(60.0)
        except Exception:
            pass
        time.sleep(5.0 * (k + 1))
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    rows, _ = E.load(a.data_dir)
    Sm, _ = E.select(rows, ("A", "B"))
    pos = {}
    with open(os.path.join(a.data_dir, "ECLIPSE_object_catalogue.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): pos[r["Unique_Identifier"]] = (float(r["RA_obj"]), float(r["DEC_obj"]))
    W = sorted([r for r in Sm if r["tE"] >= 1.7], key=lambda r: r["id"])
    cand = [r for r in Sm if r["tE"] < 1.0]; cz = np.array([r["z"] for r in cand]); cm = np.array([r["lm"] for r in cand]); used = np.zeros(len(cand), bool)
    T = []; ndrop = 0
    for i, w in enumerate(W):
        d2 = ((cz - w["z"]) / 0.05) ** 2 + ((cm - w["lm"]) / 0.1) ** 2; d2[used] = np.inf
        j = int(np.argmin(d2))
        if not d2[j] < 4.0: ndrop += 1; continue
        used[j] = True; c = cand[j]
        T.append(dict(key="W:" + w["id"], cls="W", pair=i, id=w["id"], ra=pos[w["id"]][0], dec=pos[w["id"]][1], z=w["z"], lm=w["lm"], tE=w["tE"]))
        T.append(dict(key="C:" + c["id"], cls="C", pair=i, id=c["id"], ra=pos[c["id"]][0], dec=pos[c["id"]][1], z=c["z"], lm=c["lm"], tE=c["tE"]))
    L = sorted([r for r in rows if r["grade"] in ("A", "B") and r["large"] and r["z"] > 0], key=lambda r: r["id"])[:40]
    for r in L: T.append(dict(key="L:" + r["id"], cls="L", pair=-1, id=r["id"], ra=pos[r["id"]][0], dec=pos[r["id"]][1], z=r["z"], lm=r["lm"], tE=r["tE"]))
    for w in W[:60]: T.append(dict(key="R:" + w["id"], cls="R", pair=-1, id=w["id"], ra=pos[w["id"]][0], dec=pos[w["id"]][1] + 0.30, z=w["z"], lm=w["lm"], tE=w["tE"]))
    print("targets: %d (W %d, C %d, L %d, R %d); W lenses without a control: %d" % (len(T), sum(t["cls"] == "W" for t in T), sum(t["cls"] == "C" for t in T),
          sum(t["cls"] == "L" for t in T), sum(t["cls"] == "R" for t in T), ndrop), flush=True)
    with open(os.path.join(HERE, "euc6_targets.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["key", "cls", "pair", "id", "ra", "dec", "z", "lm", "tE"]); w.writeheader()
        for t in T: w.writerow({k: (("%.6f" % t[k]) if isinstance(t[k], float) else t[k]) for k in w.fieldnames})
    jp = os.path.join(HERE, "euc6_rings.json"); R = json.load(open(jp)) if os.path.exists(jp) else {}
    # interleave so that a partial run still holds complete pairs and controls
    order = sorted(T, key=lambda t: (t["pair"] if t["pair"] >= 0 else 10 ** 6, t["cls"]))
    L_R = [t for t in order if t["cls"] in ("L", "R")]; PW = [t for t in order if t["cls"] in ("W", "C")]
    seq = []; k = 0
    for i in range(0, len(PW), 2):
        seq += PW[i:i + 2]
        if (i // 2) % 3 == 0 and k < len(L_R): seq.append(L_R[k]); k += 1
    seq += L_R[k:]
    t0 = time.time(); done = 0
    for t in seq:
        if t["key"] in R: continue
        c = rings(t["ra"], t["dec"], t["z"])
        if c is not None: R[t["key"]] = c
        done += 1
        if done % 25 == 0:
            json.dump(R, open(jp, "w")); print("  %d queried, %d stored of %d  (%.0f s)" % (done, len(R), len(T), time.time() - t0), flush=True)
    json.dump(R, open(jp, "w")); print("done: ring counts for %d of %d targets (%.0f s)" % (len(R), len(T), time.time() - t0), flush=True)

if __name__ == "__main__":
    main()
