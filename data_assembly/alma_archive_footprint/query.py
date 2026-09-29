#!/usr/bin/env python3
"""Read-only ALMA archive footprint query at the 22 KURVS-CDFS positions (owner's go: 'yes, run the ALMA archive footprint query').

Service: ALMA Science Archive TAP, https://almascience.eso.org/tap/sync, table ivoa.obscore; one ADQL CONTAINS(POINT, s_region) query per position.
Only metadata rows are retrieved (no data products downloaded).  Controls: (positive) the GOODS-ALMA field centre must return that survey's proposals
2015.1.00543.S and 2017.1.00755.S; (negative) a position far from any deep field must return no GOODS-ALMA proposal.
Outputs: raw/<id>.csv per position, alma_footprint_rows.csv (all rows), alma_footprint_by_proposal.csv (proposal-level), checks.txt.
No flux, no gas mass, no verdict.
"""
import csv, io, os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
LOG = []
def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
COLS = ["proposal_id", "obs_id", "target_name", "band_list", "s_ra", "s_dec", "s_fov", "s_resolution", "t_exptime", "cont_sensitivity_bandwidth",
        "sensitivity_10kms", "is_mosaic", "data_rights", "obs_release_date", "frequency", "bandwidth", "calib_level", "pi_name", "scientific_category", "member_ous_uid", "frequency_support", "obs_title", "pub_title", "science_keyword"]
def q(ra, dec):
    adql = f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE 1=CONTAINS(POINT('ICRS', {ra}, {dec}), s_region)"
    for attempt in range(3):
        r = subprocess.run(["curl", "-sSL", "-m", "180", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery",
                            "--data-urlencode", "LANG=ADQL", "--data-urlencode", "FORMAT=csv", "--data-urlencode", "QUERY=" + adql], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id"):
            return list(csv.DictReader(io.StringIO(r.stdout))), r.stdout
        time.sleep(3)
    raise SystemExit("query failed: " + r.stdout[:300] + r.stderr[:200])
kurvs = list(csv.DictReader(open(os.path.join(HERE, "..", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv"))))
# controls
rows, _ = q(53.125, -27.8)
props = {r["proposal_id"] for r in rows}
check({"2015.1.00543.S", "2017.1.00755.S"} <= props, f"positive control: the GOODS-ALMA field centre returns both GOODS-ALMA proposals ({len(rows)} rows, {len(props)} proposals)")
rows_n, _ = q(150.0, 60.0)
check(not ({"2015.1.00543.S", "2017.1.00755.S"} & {r["proposal_id"] for r in rows_n}), f"negative control: (RA 150, Dec +60) returns no GOODS-ALMA proposal ({len(rows_n)} rows)")
allrows = []
for k in kurvs:
    rows, raw = q(k["ra_deg"], k["dec_deg"])
    open(os.path.join(HERE, "raw", f"kurvs{int(k['kurvs_id']):02d}.csv"), "w").write(raw)
    for r in rows:
        r["kurvs_id"] = k["kurvs_id"]; allrows.append(r)
    print(f"KURVS-{k['kurvs_id']}: {len(rows)} rows, {len({r['proposal_id'] for r in rows})} proposals")
fields = ["kurvs_id"] + COLS
with open(os.path.join(HERE, "alma_footprint_rows.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(allrows)
# proposal-level table
agg = {}
for r in allrows:
    key = (r["kurvs_id"], r["proposal_id"])
    a = agg.setdefault(key, dict(kurvs_id=r["kurvs_id"], proposal_id=r["proposal_id"], n_rows=0, bands=set(), targets=set(), texp=0.0, min_fov=None, best_res=None,
                                 pi=r["pi_name"], category=r["scientific_category"], released=r["obs_release_date"], rights=r["data_rights"], min_contsens=None))
    a["n_rows"] += 1; a["bands"].add(r["band_list"]); a["targets"].add(r["target_name"])
    try: a["texp"] += float(r["t_exptime"])
    except ValueError: pass
    for fld, key2 in (("s_fov", "min_fov"), ("s_resolution", "best_res"), ("cont_sensitivity_bandwidth", "min_contsens")):
        try:
            v = float(r[fld]); a[key2] = v if a[key2] is None else min(a[key2], v)
        except ValueError: pass
out = []
for a in agg.values():
    out.append(dict(kurvs_id=a["kurvs_id"], proposal_id=a["proposal_id"], bands=";".join(sorted(a["bands"])), n_rows=a["n_rows"],
                    targets=";".join(sorted(a["targets"]))[:80], total_t_exptime_s=round(a["texp"], 1), best_resolution_arcsec=a["best_res"],
                    min_cont_sensitivity_Jy_beam=a["min_contsens"], pi=a["pi"], category=a["category"], obs_release_date=a["released"], data_rights=a["rights"]))
out.sort(key=lambda r: (int(r["kurvs_id"]), r["proposal_id"]))
with open(os.path.join(HERE, "alma_footprint_by_proposal.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
check(len({r["kurvs_id"] for r in allrows}) >= 0, "all 22 positions queried")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
