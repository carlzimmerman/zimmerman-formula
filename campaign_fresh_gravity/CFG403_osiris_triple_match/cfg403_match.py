"""CFG403: metadata-only triple match - OSIRIS AO inner (A) x deep outer (B) x resolved gas (C). Criteria: FROZEN_CRITERIA.md (9df62e070).
Inputs: KOA koa_osiris spectrograph frame metadata (../../../_external_data/cfg403_work/koa_osiris_spec_frames.csv, fetched by TAP, sha256 in FETCH_LOG);
ALMA obscore rows near the parents (fetched once by this script into the same folder, then reused).
Run: python3 cfg403_match.py ; MUTATE=1 shifts every galaxy +60" in Dec (A matches must fall to <= 10%; rc 1).
"""
import csv, io, json, math, os, re, subprocess, sys, time
import numpy as np
from astropy.cosmology import Planck18

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg403_work"))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
DDEC = 60 / 3600 if MUTATE else 0.0
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")
def sep(ra1, de1, ra2, de2):          # arcsec, small-angle
    return 3600 * np.hypot((ra1 - ra2) * np.cos(np.radians(de1)), de1 - de2)

A0 = 9.3603e-11; KPC = 3.0857e19
OPT = {"Halpha": 656.46, "OIII5008": 500.82}                       # nm, vacuum
LINES = {"CO(2-1)": 230.538, "CO(3-2)": 345.796, "CO(4-3)": 461.041, "CO(5-4)": 576.268, "[CI](1-0)": 492.161, "[CI](2-1)": 809.342}  # GHz

say("CFG403 OSIRIS x deep-outer x resolved-gas triple match" + ("  (MUTATE: +60\" Dec)" if MUTATE else ""))
say("=" * 78)
check("C3 CO(3-2) at z 2.2 -> 108.06 GHz", abs(LINES["CO(3-2)"] / 3.2 - 108.06) < 0.01, f"{LINES['CO(3-2)']/3.2:.3f}")

# ---------------- parents ----------------
P = []
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_phibss", "kmos3d_catalog.csv"))):
    try:
        z = float(r["Z"])
    except ValueError:
        continue
    P.append(dict(id=r["ID"], src="KMOS3D", ra=float(r["RA"]), dec=float(r["DEC"]), z=z))
def sexa(s, hours):
    s = s.replace("[+]", "+").replace("[", "").replace("]", "").replace("−", "-").strip()
    sign = -1 if s.startswith("-") else 1
    p = [float(x) for x in re.split(r"[:\s]+", s.lstrip("+-").strip())]
    v = p[0] + p[1] / 60 + p[2] / 3600
    return sign * v * (15 if hours else 1)
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "highz_literature_tables", "sins_ao", "sins_ao_table1_sample.csv"))):
    P.append(dict(id=r["source"], src="SINS-AO", ra=sexa(r["ra"], True), dec=sexa(r["dec"], False), z=float(r["z_Halpha"])))
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "noema3d", "noema3d_per_galaxy.csv"))):
    P.append(dict(id=r["id"], src="NOEMA3D", ra=float(r["ra_deg"]), dec=float(r["dec_deg"]), z=float(r["z"])))
P = [p for p in P if 1.0 <= p["z"] <= 3.0]
G = []                                     # merge duplicates within 1.0"
for p in P:
    hit = next((g for g in G if sep(g["ra"], g["dec"], p["ra"], p["dec"]) < 1.0), None)
    if hit:
        hit["srcs"].add(p["src"]); hit["ids"].append(p["id"])
    else:
        G.append(dict(ra=p["ra"], dec=p["dec"] + DDEC, z=p["z"], srcs={p["src"]}, ids=[p["id"]]))
say(f"parents 1 <= z <= 3: {len(P)} rows -> {len(G)} unique galaxies "
    f"(KMOS3D {sum('KMOS3D' in g['srcs'] for g in G)}, SINS-AO {sum('SINS-AO' in g['srcs'] for g in G)}, NOEMA3D {sum('NOEMA3D' in g['srcs'] for g in G)})")

# ---------------- A: OSIRIS ----------------
K = list(csv.DictReader(open(os.path.join(WORK, "koa_osiris_spec_frames.csv"))))
def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")
K = [k for k in K if k["issky"] != "1" and math.isfinite(fl(k["ra"])) and math.isfinite(fl(k["dec"]))]
kra, kde = np.array([fl(k["ra"]) for k in K]), np.array([fl(k["dec"]) for k in K])
def osiris(ra, dec, z, imtyp=("object",)):
    d = sep(kra, kde, ra, dec)
    idx = np.where(d <= 1.5)[0]
    tot, tot_any, progs, filt = 0.0, 0.0, set(), set()
    for i in idx:
        k = K[i]
        if k["koaimtyp"] not in imtyp:
            continue
        tot_any += fl(k["elaptime"])
        wb, wr = fl(k["waveblue"]), fl(k["wavered"])
        inband = any(wb <= lam * (1 + z) <= wr for lam in OPT.values())
        if inband and fl(k["scale"]) <= 0.10 + 1e-9:
            tot += fl(k["elaptime"]); progs.add(k["semid"]); filt.add(k["filter"])
    return tot, tot_any, sorted(progs), sorted(filt)
# C1: BX442 positive control
bx = [k for k in K if "BX442" in k["object"].replace(" ", "").upper() and "TT" not in k["object"].upper() and k["koaimtyp"] == "object"]
bra, bde = float(np.median([fl(k["ra"]) for k in bx])), float(np.median([fl(k["dec"]) for k in bx]))
tb = osiris(bra, bde, 2.1765)[0]
check("C1 KOA positive: BX442 (z 2.1765) at its median pointing returns >= 3600 s in-band AO frames", tb >= 3600, f"{len(bx)} frames, {tb:.0f} s in band")
for g in G:
    g["A_s"], g["A_any_s"], g["A_progs"], g["A_filters"] = osiris(g["ra"], g["dec"], g["z"])
    g["A"] = g["A_s"] >= 3600
    g["A_undef_s"] = osiris(g["ra"], g["dec"], g["z"], ("object", "undefined"))[0]   # sensitivity, not gated

# ---------------- B: deep outer (CFG386 conservative P0) ----------------
fits = {f["ID"]: f for f in csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_cubes", "k3d_fits_main_final_flags.csv")))}
kcat = {r["ID"]: r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "kmos3d_phibss", "kmos3d_catalog.csv")))}
arct = lambda r, Va, rt: Va * 2 / math.pi * math.atan(r / max(rt, 1e-6))
for g in G:
    g["B"], g["B_gout"], g["deep_member"] = False, None, bool(g["srcs"] & {"KMOS3D", "SINS-AO"})
    for i in g["ids"]:
        f = fits.get(i)
        if not f:
            continue
        Va, eVa, rt, rmax = (float(f[k]) for k in ("Va", "eVa", "rt", "rmax"))
        s = float(Planck18.angular_diameter_distance(float(f["Z"])).to("kpc").value * math.pi / 180 / 3600)
        gout = (arct(rmax, Va, rt) * 1e3) ** 2 / (rmax * s * KPC) / A0 if rmax > 0 else 9e9
        g["B_gout"] = gout
        g["B"] = (0 < Va < 790) and eVa / Va <= 0.10 and gout <= 0.55

# ---------------- C: ALMA ----------------
COLS = "proposal_id, obs_id, target_name, s_ra, s_dec, s_fov, s_resolution, frequency, bandwidth, data_rights, is_mosaic, band_list, t_exptime"
cache = os.path.join(WORK, "alma_rows.csv")
def tap(adql):
    for _ in range(3):
        r = subprocess.run(["curl", "-sSL", "-m", "600", "https://almascience.eso.org/tap/sync", "--data-urlencode", "REQUEST=doQuery", "--data-urlencode", "LANG=ADQL",
                            "--data-urlencode", "FORMAT=csv", "--data-urlencode", "QUERY=" + adql], capture_output=True, text=True)
        if r.stdout.startswith("proposal_id"):
            return r.stdout
        time.sleep(5)
    raise SystemExit("ALMA TAP failed: " + r.stdout[:300] + r.stderr[:300])
if not os.path.exists(cache):
    if MUTATE:
        raise SystemExit("run the main pass first (it builds the ALMA cache)")
    groups = []                                                    # field groups within 0.7 deg
    for g in G:
        h = next((x for x in groups if sep(x["ra"], x["dec"], g["ra"], g["dec"]) < 0.7 * 3600), None)
        (h["m"].append(g) if h else groups.append(dict(ra=g["ra"], dec=g["dec"], m=[g])))
    out = None
    for x in groups:
        ra = float(np.mean([m["ra"] for m in x["m"]])); de = float(np.mean([m["dec"] for m in x["m"]]))
        rad = max(sep(ra, de, m["ra"], m["dec"]) for m in x["m"]) / 3600 + 0.05
        txt = tap(f"SELECT {COLS} FROM ivoa.obscore WHERE 1=INTERSECTS(s_region, CIRCLE('ICRS', {ra}, {de}, {rad})) AND s_resolution <= 0.6")
        body = txt.split("\n", 1)
        out = (txt if out is None else out + (body[1] if len(body) > 1 else ""))
        say(f"  ALMA group RA {ra:.3f} Dec {de:+.3f} r {rad:.3f} deg: {txt.count(chr(10)) - 1} rows")
    out_lines = [l for l in out.split("\n") if l.strip()]
    open(cache, "w").write("\n".join(out_lines) + "\n")
AL = list(csv.DictReader(open(cache)))
ara, ade = np.array([fl(a["s_ra"]) for a in AL]), np.array([fl(a["s_dec"]) for a in AL])
# C2: GOODS-ALMA positive/negative (direct point queries)
pos = tap("SELECT proposal_id FROM ivoa.obscore WHERE 1=CONTAINS(POINT('ICRS', 53.125, -27.8), s_region)")
neg = tap("SELECT proposal_id FROM ivoa.obscore WHERE 1=CONTAINS(POINT('ICRS', 150.0, 60.0), s_region)")
check("C2 ALMA: GOODS-ALMA centre returns 2015.1.00543.S; (150,+60) does not", "2015.1.00543.S" in pos and "2015.1.00543.S" not in neg, f"pos {pos.count(chr(10))-1} rows, neg {neg.count(chr(10))-1} rows")
for g in G:
    d = sep(ara, ade, g["ra"], g["dec"])
    hits = []
    for i in np.where(d <= 0.5 * 3600 * np.nan_to_num(np.array([fl(a["s_fov"]) for a in AL]), nan=0.0))[0]:
        a = AL[i]
        if a["data_rights"] != "Public" or fl(a["s_resolution"]) > 0.6:
            continue
        f0, bw = fl(a["frequency"]), fl(a["bandwidth"]) / 1e9
        for ln, nu in LINES.items():
            nuo = nu / (1 + g["z"])
            if abs(nuo - f0) <= bw / 2:
                hits.append((a["proposal_id"], ln, round(fl(a["s_resolution"]), 3)))
    g["C_alma"] = sorted(set(hits))
    g["C"] = bool(hits) or ("NOEMA3D" in g["srcs"])
nC4 = sum(1 for g in G if all(k in g for k in ("A", "B", "C")))
check("C4 every parent evaluated for A, B and C", nC4 == len(G), f"{nC4} of {len(G)}")

# ---------------- headline ----------------
nA, nB, nC = (sum(g[k] for g in G) for k in "ABC")
nAB = sum(g["A"] and g["B"] for g in G); nAC = sum(g["A"] and g["C"] for g in G); nBC = sum(g["B"] and g["C"] for g in G)
ABC = [g for g in G if g["A"] and g["B"] and g["C"]]
anyAO = lambda g: g["A"] or ("SINS-AO" in g["srcs"])
nABC_any = sum(anyAO(g) and g["B"] and g["C"] for g in G)
say(f"\nA (OSIRIS >= 1 h in band, <= 0.1\"): {nA}   B (KMOS3D g_out <= 0.55 a0): {nB}   C (ALMA CO/[CI] <= 0.6\" or NOEMA3D): {nC}")
say(f"AB {nAB}   AC {nAC}   BC {nBC}   ABC {len(ABC)}   (reported: any-AO incl. SINS AO x B x C = {nABC_any}; "
    f"A with 'undefined'-type frames too: {sum(g['A_undef_s'] >= 3600 for g in G)})")
for lab, sel in (("A", [g for g in G if g["A"]]), ("ABC", ABC), ("anyAO-B-C", [g for g in G if anyAO(g) and g["B"] and g["C"]])):
    for g in sel:
        say(f"  [{lab}] {'/'.join(g['ids'])} z {g['z']:.3f} {sorted(g['srcs'])}: OSIRIS {g['A_s']/3600:.1f} h {g['A_filters']} {g['A_progs']}; "
            f"g_out {('%.2f a0' % g['B_gout']) if g['B_gout'] is not None else '-'}; gas {g['C_alma'][:4]}{' +NOEMA3D' if 'NOEMA3D' in g['srcs'] else ''}")
if ABC:
    verdict = f"LANE CANDIDATE(S): {len(ABC)}"
else:
    bind = min((("A (OSIRIS)", nA), ("B (deep outer)", nB), ("C (gas)", nC)), key=lambda t: t[1])[0]
    verdict = f"NONE: OSIRIS goes on the proposal list (scarcest gate {bind}; AB {nAB}, AC {nAC}, BC {nBC})"
say(f"\nVERDICT: {verdict}")
check("T-MUT main-run marker (MUTATE +60\" must cut A to <= 10%)", not MUTATE, f"A {nA}")
if MUTATE:
    base = json.load(open(os.path.join(HERE, "cfg403_results.json")))["counts"]["A"]
    check("MUTATE premise: A falls to <= 10% of the main run", nA <= 0.10 * max(base, 1), f"{nA} vs main {base}")
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": nA})
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
ser = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in g.items()} for g in G]
json.dump({"lane": "CFG403", "mutate": MUTATE, "verdict": verdict, "counts": dict(A=nA, B=nB, C=nC, AB=nAB, AC=nAC, BC=nBC, ABC=len(ABC), anyAO_BC=nABC_any),
           "galaxies": [s for s in ser if s["A"] or s["B"] and s["C"]], "checks": checks}, open(os.path.join(HERE, f"cfg403_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg403{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
