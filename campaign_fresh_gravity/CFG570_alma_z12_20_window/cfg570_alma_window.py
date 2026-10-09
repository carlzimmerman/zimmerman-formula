#!/usr/bin/env python3
"""CFG570: read-only ALMA archive metadata survey of the z 1.2-2.0 window (FROZEN_CRITERIA.md). Run: python3 cfg570_alma_window.py [--mutate]
No data products are downloaded. TAP helper and line parser follow CFG568_alma_archive_rc41_lowv/cfg568_alma.py."""
import csv, io, os, re, sys, subprocess, time, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; DDEC = 1.0 if MUT else 0.0
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
COLS = ["proposal_id", "obs_id", "target_name", "band_list", "s_ra", "s_dec", "s_fov", "s_resolution", "t_exptime", "sensitivity_10kms", "data_rights", "obs_release_date", "pi_name", "frequency_support", "obs_title"]
def tap(adql):
    for _ in range(3):
        r = subprocess.run(["curl", "-sSL", "-m", "600", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery", "--data-urlencode", "LANG=ADQL",
                            "--data-urlencode", "FORMAT=csv", "--data-urlencode", "MAXREC=500000", "--data-urlencode", "QUERY=" + adql], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id"): return list(csv.DictReader(io.StringIO(r.stdout)))
        time.sleep(5)
    raise SystemExit("query failed: " + r.stdout[:200] + r.stderr[:200])
contains = lambda ra, dec: tap(f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE 1=CONTAINS(POINT('ICRS', {ra}, {dec}), s_region)")
norm = lambda s: s.replace(" ", "").replace("_", "").upper()
fl = lambda x: float(x) if x not in ("", None) else float("nan")

# ---- sample ----
cat = list(csv.DictReader(open(os.path.join(ROOT, "data_assembly/kmos3d_phibss/kmos3d_catalog.csv"))))
rc100 = {norm(r["name"]) for r in csv.DictReader(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg90_per_object_RC100FIX.csv"))) if r["survey"] == "RC100"}
rc41 = {norm(r["id"]) for r in csv.DictReader(open(os.path.join(ROOT, "data_assembly/price2021_rc41/price2021_rc41.csv")))}
hisn = {norm(r["ID"]) for r in csv.DictReader(open(os.path.join(ROOT, "data_assembly/kmos3d_cubes/k3d_fits_main_final.csv"))) if r["quality"] == "highSN"}
S = []
for r in cat:
    if r["Z"] and 1.2 <= float(r["Z"]) <= 2.0:
        ids = {norm(r["ID"]), norm(r["ID_TARGETED"])}
        tags = [t for t, s in (("RC100", rc100), ("RC41", rc41), ("K3D-highSN", hisn)) if ids & s]
        S.append(dict(name=r["ID"], field=r["FIELD"], ra=float(r["RA"]), dec=float(r["DEC"]) + DDEC, z=float(r["Z"]), lmstar=fl(r["LMSTAR"]), K=tags))
for r in csv.DictReader(open(os.path.join(ROOT, "data_assembly/arxiv_tables/kurvs_positions/kurvs_positions.csv"))):
    if 1.2 <= float(r["z_halpha"]) <= 2.0:
        S.append(dict(name="KURVS-" + r["kurvs_id"], field="GS", ra=float(r["ra_deg"]), dec=float(r["dec_deg"]) + DDEC, z=float(r["z_halpha"]), lmstar=fl(r["logMstar"]), K=["KURVS"]))
rc100_win = [r["name"] for r in csv.DictReader(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg90_per_object_RC100FIX.csv"))) if r["survey"] == "RC100" and 1.2 <= float(r["z"]) <= 2.0]
have = {norm(n) for s in S for n in [s["name"]]} | {norm(r["ID_TARGETED"]) for r in cat if r["Z"] and 1.2 <= float(r["Z"]) <= 2.0}
nopos = [n for n in rc100_win if norm(n) not in have]
P(f"sample: {len(S)} galaxies at 1.2<=z<=2.0 ({sum(1 for s in S if s['K'])} with the deep-kinematics flag); RC100 window discs without a position on disk: {len(nopos)} {nopos}")

LINES = {"CO(2-1)": 230.538, "CO(3-2)": 345.796, "CO(4-3)": 461.041, "CO(5-4)": 576.268, "[CI](1-0)": 492.161, "[CI](2-1)": 809.342}
pat = re.compile(r"\[([\d.]+)\.\.([\d.]+)GHz,([\d.]+)kHz,([\d.]+)(mJy|uJy|Jy)/beam@10km/s"); scale = {"Jy": 1e3, "mJy": 1.0, "uJy": 1e-3}
def sep_deg(a1, d1, a2, d2):
    a1, d1, a2, d2 = map(math.radians, (a1, d1, a2, d2))
    return math.degrees(math.acos(min(1.0, math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2))))
def tier_of(rows, z):
    best, cov = "E" if not rows else "D", []
    for r in rows:
        wins = [(float(a), float(b), float(d) * scale[u]) for a, b, c, d, u in pat.findall(r["frequency_support"])]
        rs = fl(r["s_resolution"])
        for ln, nu0 in LINES.items():
            nu = nu0 / (1 + z); hit = [w for w in wins if w[0] <= nu <= w[1]]
            if hit:
                t = "A" if rs <= 0.25 else ("B" if rs <= 0.5 else "C")
                cov.append(dict(line=ln, tier=t, proposal=r["proposal_id"], pi=r["pi_name"], band=r["band_list"], res=rs, sens=min(w[2] for w in hit), t_exp=fl(r["t_exptime"]), rights=r["data_rights"], release=r["obs_release_date"][:10], title=r["obs_title"][:70]))
    if cov: best = min(c["tier"] for c in cov)
    return best, cov

# ---- per-field box queries ----
fields = {}
for s in S: fields.setdefault(s["field"], []).append(s)
rows_by = {}
for f, ss in fields.items():
    ras, decs = [s["ra"] for s in ss], [s["dec"] for s in ss]
    q = (f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE s_ra BETWEEN {min(ras) - 0.5} AND {max(ras) + 0.5} AND s_dec BETWEEN {min(decs) - 0.5} AND {max(decs) + 0.5}")
    rows_by[f] = tap(q); P(f"field {f}: {len(ss)} galaxies, {len(rows_by[f])} archive rows in the box")
def covered(s, rows): return [r for r in rows if r["s_fov"] and sep_deg(s["ra"], s["dec"], fl(r["s_ra"]), fl(r["s_dec"])) < fl(r["s_fov"]) / 2]

# ---- controls ----
c1rows = contains(53.070583, -27.834461 + DDEC); t1, cov1 = tier_of(c1rows, 1.613)
c1 = any(c["proposal"] == "2018.1.00164.S" and c["line"] == "CO(2-1)" and c["tier"] == "A" for c in cov1)
k15 = next((s for s in S if s["name"] == "KURVS-15"), None)
c1b = k15 is not None and any(c["proposal"] == "2018.1.00164.S" and c["tier"] == "A" for c in tier_of(covered(k15, rows_by["GS"]), k15["z"])[1])
c2 = len(contains(150.0, 60.0)) == 0
P(f"C1 positive (KURVS-15 CO(2-1) <=0.25\" from 2018.1.00164.S): CONTAINS {'PASS' if c1 else 'FAIL'}; box+s_fov {'PASS' if c1b else 'FAIL'}")
P(f"C2 negative (empty RA150 Dec+60): {'PASS' if c2 else 'FAIL'}")

# ---- tiers ----
res = {}
for s in S:
    t, cov = tier_of(covered(s, rows_by[s["field"]]), s["z"])
    res[s["name"]] = dict(s, tier_box=t, tier=t, lines=cov)
cand = [k for k, v in res.items() if v["tier"] in "AB"]
P(f"\nbox+s_fov tiers before confirmation: " + ", ".join(f"{t}:{sum(1 for v in res.values() if v['tier'] == t)}" for t in "ABCDE"))
dis = 0
for k in cand:
    v = res[k]; t, cov = tier_of(contains(v["ra"], v["dec"]), v["z"])
    if t != v["tier_box"]: dis += 1
    v["tier"], v["lines"] = t, cov
P(f"CONTAINS confirmation of {len(cand)} A/B candidates: {dis} disagree (CONTAINS used)")
counts = {t: sum(1 for v in res.values() if v["tier"] == t) for t in "ABCDE"}
P("final tiers: " + ", ".join(f"{t}:{n}" for t, n in counts.items()))
use = sorted([v for v in res.values() if v["tier"] in "AB" and v["K"]], key=lambda v: (v["tier"], v["z"]))
P(f"\nUSABLE for CFG385 at metadata level (tier A/B + deep kinematics): {len(use)}")
for v in use:
    P(f"  {v['name']:12s} z {v['z']:.3f} logM* {v['lmstar']:.2f} [{'/'.join(v['K'])}] tier {v['tier']}")
    seen = set()
    for c in sorted(v["lines"], key=lambda c: (c["res"], c["sens"])):
        key = (c["proposal"], c["line"])
        if key in seen or c["tier"] not in "AB": continue
        seen.add(key); P(f"      {c['line']:9s} {c['proposal']} PI {c['pi']} B{c['band']} res {c['res']:.2f}\" sens {c['sens']:.2f} mJy/bm@10km/s t {c["t_exp"]:.0f}s {c["rights"]} {c["release"]} | {c["title"]}")
other = sorted([v for v in res.values() if v["tier"] in "AB" and not v["K"]], key=lambda v: (v["tier"], v["z"]))
P(f"\ntier A/B WITHOUT deep kinematics (gas map possible, Halpha curve not deep): {len(other)}")
for v in other: P(f"  {v['name']:12s} z {v['z']:.3f} logM* {v['lmstar']:.2f} tier {v['tier']} " + ", ".join(sorted({c['proposal'] + ' ' + c['line'] for c in v['lines'] if c['tier'] in 'AB'})))
kc = [v for v in res.values() if v["K"]]
P(f"\ndeep-kinematics discs ({len(kc)}) by tier: " + ", ".join(f"{t}:{sum(1 for v in kc if v['tier'] == t)}" for t in "ABCDE"))
json.dump(dict(controls=dict(C1_contains=c1, C1_box=c1b, C2=c2), counts=counts, n_usable=len(use), no_position=nopos, results=res),
          open(os.path.join(HERE, f"cfg570_alma_window{TAG}_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg570_alma_window{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg570_alma_window_results.json")))["counts"]
    ch = (base["A"] + base["B"]) != (counts["A"] + counts["B"]); P(f"MUTATE: tier A+B count {base['A'] + base['B']} -> {counts['A'] + counts['B']}: {'detected (exit 1)' if ch else 'NOT detected'}")
    open(os.path.join(HERE, f"cfg570_alma_window{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ch else 0)
sys.exit(0 if (c1 and c1b and c2) else 1)
