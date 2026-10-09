#!/usr/bin/env python3
"""CFG568: read-only ALMA archive metadata query for the five low-V RC41 discs (FROZEN_CRITERIA.md). Run: python3 cfg568_alma.py [--mutate]
No data products are downloaded. Column list and line parser copied from data_assembly/alma_archive_footprint/{query,lines}.py."""
import csv, io, os, re, sys, subprocess, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
COLS = ["proposal_id", "obs_id", "target_name", "band_list", "s_ra", "s_dec", "s_resolution", "t_exptime", "sensitivity_10kms", "data_rights", "obs_release_date", "pi_name", "frequency_support", "obs_title"]
def tap(adql):
    for _ in range(3):
        r = subprocess.run(["curl", "-sSL", "-m", "180", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery", "--data-urlencode", "LANG=ADQL",
                            "--data-urlencode", "FORMAT=csv", "--data-urlencode", "QUERY=" + adql], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id"): return list(csv.DictReader(io.StringIO(r.stdout)))
        time.sleep(3)
    raise SystemExit("query failed: " + r.stdout[:200] + r.stderr[:200])
pos = lambda ra, dec: tap(f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE 1=CONTAINS(POINT('ICRS', {ra}, {dec}), s_region)")
props = {r["proposal_id"] for r in pos(53.125, -27.8)}; c1 = {"2015.1.00543.S", "2017.1.00755.S"} <= props
c2 = not ({"2015.1.00543.S", "2017.1.00755.S"} & {r["proposal_id"] for r in pos(150.0, 60.0)})
P(f"positive control (GOODS-ALMA centre): {'PASS' if c1 else 'FAIL'}; negative control: {'PASS' if c2 else 'FAIL'}")
T = [("GS4_13143", 53.08810043, -27.85064125, 0.76014), ("GS4_03228", 53.12320709, -27.90134621, 0.8224987),
     ("COS3_22796", 150.07936096, 2.40546036, 0.906835), ("U3_05138", 34.24954224, -5.25209522, 0.809762)]
LINES = {"CO(1-0)": 115.271, "CO(2-1)": 230.538, "CO(3-2)": 345.796, "CO(4-3)": 461.041, "[CI](1-0)": 492.161, "[CI](2-1)": 809.342}
pat = re.compile(r"\[([\d.]+)\.\.([\d.]+)GHz,([\d.]+)kHz,([\d.]+)(mJy|uJy|Jy)/beam@10km/s"); scale = {"Jy": 1e3, "mJy": 1.0, "uJy": 1e-3}
res = {}
def analyse(name, rows, z):
    cov = []
    for r in rows:
        wins = [(float(a), float(b), float(d) * scale[u]) for a, b, c, d, u in pat.findall(r["frequency_support"])]
        for ln, nu0 in LINES.items():
            nu = nu0 / (1 + z); hit = [w for w in wins if w[0] <= nu <= w[1]]
            if hit:
                try: rs = float(r["s_resolution"])
                except ValueError: rs = float("nan")
                cov.append(dict(line=ln, proposal=r["proposal_id"], pi=r["pi_name"], band=r["band_list"], res=rs, sens=min(w[2] for w in hit), title=r["obs_title"][:80]))
    best = [c for c in cov if c["res"] <= 0.5]
    v = "GAS-MAP CANDIDATE" if best else ("COVERAGE ONLY" if rows else "NONE")
    res[name] = dict(n_rows=len(rows), proposals=sorted({r["proposal_id"] for r in rows}), lines=cov, verdict=v)
    P(f"{name} (z {z:.3f}): {len(rows)} rows, {len(res[name]['proposals'])} proposals; line windows {len(cov)}; -> {v}")
    for c in sorted(cov, key=lambda c: c["res"])[:6]:
        P(f"     {c['line']:9s} {c['proposal']} PI {c['pi']} band {c['band']} res {c['res']:.2f}\" sens {c['sens']:.2f} mJy/beam@10km/s | {c['title']}")
for name, ra, dec, z in T:
    analyse(name, pos(ra, dec + (1.0 if MUT else 0.0)), z)
zrows = tap(f"SELECT {', '.join(COLS)} FROM ivoa.obscore WHERE target_name LIKE '%405501%'")
analyse("zC_405501 (by target name)", [] if MUT else zrows, 2.154)
json.dump(dict(controls=[c1, c2], results=res), open(os.path.join(HERE, f"cfg568_alma{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg568_alma{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg568_alma_results.json")))["results"]
    changed = any(base[k]["n_rows"] != res[k]["n_rows"] for k in res); P(f"MUTATE: coverage changed -> {'detected (exit 1)' if changed else 'NOT detected'}"); sys.exit(1 if changed else 0)
sys.exit(0 if (c1 and c2) else 1)
