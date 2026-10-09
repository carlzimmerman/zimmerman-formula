"""CFG523 blind sweep S (FROZEN_CRITERIA.md): public obscore rows at s_resolution <= 0.30" in the galaxy-evolution / AGN categories with
sub-mm / starburst / lensing / galaxy-structure keywords. No redshifts: counted and name-matched to the parents only. Metadata only.
"""
import csv, hashlib, io, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg523_work"))
cache = os.path.join(WORK, "alma_rows_sweep.csv")
Q = ("SELECT proposal_id, target_name, s_ra, s_dec, s_resolution, band_list, data_rights, scientific_category, science_keyword, obs_release_date, member_ous_uid "
     "FROM ivoa.obscore WHERE s_resolution <= 0.30 AND data_rights = 'Public' AND scientific_category IN ('Galaxy evolution', 'Active galaxies') "
     "AND (science_keyword LIKE '%Sub-mm%' OR science_keyword LIKE '%Starburst%' OR science_keyword LIKE '%lens%' OR science_keyword LIKE '%Galaxy structure%')")
if not os.path.exists(cache):
    for _ in range(4):
        r = subprocess.run(["curl", "-sSL", "-m", "900", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery", "--data-urlencode", "LANG=ADQL",
                            "--data-urlencode", "FORMAT=csv", "--data-urlencode", "MAXREC=2000000", "--data-urlencode", "QUERY=" + Q], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id"): break
        time.sleep(10)
    else:
        raise SystemExit("TAP failed " + r.stdout[:300])
    open(cache, "w").write(r.stdout)
rows = list(csv.DictReader(open(cache)))
inv = json.load(open(os.path.join(HERE, "cfg523_inventory_results.json")))
props = {r["proposal_id"] for r in rows}; tg = {(r["proposal_id"], r["target_name"]) for r in rows}; names = {r["target_name"] for r in rows}
pid = {i for g in inv["g2_all"] for i in g["ids"]}
matched = sorted({n for n in names for i in pid if i.split(":")[-1].replace("-", "").replace("_", "").lower() in n.replace("-", "").replace("_", "").lower()})
kw = {}
for r in rows:
    for k in r["science_keyword"].split(";"):
        kw[k] = kw.get(k, 0) + 1
res = dict(rows=len(rows), proposals=len(props), proposal_targets=len(tg), unique_target_names=len(names),
           cache_sha256=hashlib.sha256(open(cache, "rb").read()).hexdigest(), keywords=dict(sorted(kw.items(), key=lambda t: -t[1])[:15]),
           names_matching_G2_parents=matched, adql=Q)
json.dump(res, open(os.path.join(HERE, "cfg523_sweep_results.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "adql"}, indent=1))
