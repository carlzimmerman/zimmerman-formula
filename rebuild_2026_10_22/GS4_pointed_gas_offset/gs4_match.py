#!/usr/bin/env python3
"""GS4 (criteria 1bf15a0aff): the pointed-to-eRASS1 gas offset d = lg(Mgas500 pointed / Mgas500 eRASS1), same clusters, same radius, same h.
    python3 -I gs4_match.py                # gs4_match.out, gs4_results.json, gs4_matched.csv
    GS4_MUTATE=ra python3 -I gs4_match.py  # RA + 1 degree, separate outputs
    GS4_MUTATE=shuffle python3 -I gs4_match.py
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, sys, csv, json, math
import numpy as np
from astropy.io import fits
MUT = os.environ.get("GS4_MUTATE", ""); TAG = f"_MUTATE_{MUT}" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); DATA = os.path.join(REPO, "real_research", "data"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
LINE = 0.093; SLOPE = 1.19; LO, HI = 4.4e13, 5.6e14; T1, T2 = 1.364e14, 2.390e14; PIV = 14.25; NB = 10000
E = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
ER, ED, EZ = [np.asarray(E[k], float) for k in ("RA", "DEC", "BEST_Z")]; EM = np.asarray(E["M500"], float) * 1e13; EG = np.asarray(E["MGAS500"], float) * 1e11; ERK = np.asarray(E["R500"], float); EC = np.asarray(E["CTS500"], float); EN = [str(n).strip() for n in E["NAME"]]
LEN = set(str(x) for x in np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz"))["name"])
def DA(z, h, Om):
    x = np.linspace(0, z, 400); return 299792.458 / (100 * h) * np.trapz(1 / np.sqrt(Om * (1 + x) ** 3 + 1 - Om), x) / (1 + z)   # Mpc, flat
def sep(ra, de): return np.degrees(np.arccos(np.clip(np.sin(np.radians(de)) * np.sin(np.radians(ED)) + np.cos(np.radians(de)) * np.cos(np.radians(ED)) * np.cos(np.radians(ER - ra)), -1, 1)))
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
CAT = []
for r in csv.DictReader(open(os.path.join(HERE, "gs4_inputs.csv"))): CAT.append(dict(cat=r["cat"], inst=r["inst"], name=r["name"], ra=float(r["ra"]), dec=float(r["dec"]), z=float(r["z"]), Mgas=float(r["Mgas"]), R=float(r["R500"]), h=float(r["h"]), Om=float(r["Om"])))
XT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json"))); XP = {}
for n, v in XT.items():
    p = os.path.join(DATA, "xcop", n, f"{n}_fgas_profile.fits")
    if not os.path.exists(p): continue
    with fits.open(p) as h: g = h[1].data.copy(); rg = float(h[1].header["R500"]); ra = float(h[1].header["RA"]); de = float(h[1].header["DEC"])
    XP[n] = (g["RADIUS"] * rg, g["MGAS"]); CAT.append(dict(cat="XC", inst="XMM", name=n, ra=ra, dec=de, z=v["z"], Mgas=li(*XP[n], v["R500"] * 1e3), R=v["R500"] * 1e3, h=.7, Om=.3))
def match(rmax, s=SLOPE):
    best = {}
    for c in CAT:
        ra = (c["ra"] + 1.0) % 360 if MUT == "ra" else c["ra"]; q = sep(ra, c["dec"]); ok = (q <= rmax / 60) & (np.abs(EZ - c["z"]) < 0.01) & (EG > 0) & (ERK > 0) & (EM > 0)
        if not ok.any(): continue
        j = int(np.where(ok)[0][np.argmin(q[ok])]); k = (c["cat"], j)
        if k in best and best[k]["sep"] <= q[j] * 60: continue
        qd = DA(c["z"], .70, .30) / DA(c["z"], c["h"], c["Om"]); Mc = c["Mgas"] * qd ** 2.5; Rc = c["R"] * qd; own = math.log10(Mc / EG[j])
        if c["cat"] == "XC": dv = math.log10(li(*XP[c["name"]], ERK[j]) / EG[j]); how = "profile"
        else: dv = math.log10(Mc * (ERK[j] / Rc) ** s / EG[j]); how = "slope"
        best[k] = dict(cat=c["cat"], inst=c["inst"], name=c["name"], j=j, erass=EN[j], sep=float(q[j] * 60), z=c["z"], lgM=float(np.log10(EM[j])), d=dv, d_own=own, dlgR=math.log10(ERK[j] / Rc), how=how, cts=float(EC[j]), lgMgp=math.log10(Mc), inlens=EN[j] in LEN)
    return list(best.values())
RNG = np.random.default_rng(0)
def boot_med(x):
    x = np.asarray(x); rng = np.random.default_rng(0); idx = rng.integers(0, len(x), (NB, len(x))); return float(np.median(x)), float(np.std(np.median(x[idx], axis=1)))
def fit(xv, d):
    xv, d = np.asarray(xv), np.asarray(d); f = lambda a, b: np.polyfit(a - PIV, b, 1); s, c = f(xv, d); rng = np.random.default_rng(0); B = np.array([f(xv[i], d[i])[0] for i in (rng.integers(0, len(xv), len(xv)) for _ in range(2000))]); return float(s), float(np.std(B)), float(c)
def cls(m, se, n=None):
    if n is not None and n < 5: return "TOO FEW"
    if abs(m) < 2 * se: return "NO OFFSET"
    if m - se >= LINE: return "ABOVE THE LINE"
    if m + se <= LINE: return "BELOW THE LINE"
    return "ON THE LINE"
def per_cluster(rows, primary=True):
    D = {}
    for r in rows:
        if primary and r["cat"] == "V09": continue
        if not (LO <= 10 ** r["lgM"] <= HI): continue
        D.setdefault(r["j"], []).append(r)
    return D
def stat(D, key="d"):
    v = np.array([np.median([r[key] for r in L]) for L in D.values()]); return v
def line(lab, D, key="d"):
    if len(D) == 0: P(f"  {lab}: N 0"); return dict(n=0)
    v = stat(D, key)
    if len(v) < 2: P(f"  {lab}: N {len(v)}, d {v[0]:+.3f}"); return dict(n=1, med=float(v[0]))
    m, se = boot_med(v); c = cls(m, se, len(v)); rms = float(np.std(v)); P(f"  {lab}: N {len(v)}, median d {m:+.3f} +- {se:.3f}, rms {rms:.3f}: {c}"); return dict(n=len(v), med=m, se=se, rms=rms, cls=c)
if __name__ == "__main__":
    P(f"GS4_pointed_gas_offset{TAG} (criteria 1bf15a0aff): d = lg(Mgas500 pointed / eRASS1) at eRASS1's R500, h 0.70, Om 0.30; line {LINE}; kappa = 1/2 FITTED; not theory closed")
    rows = match(3.0); RES = dict(line=LINE, slope_s=SLOPE, n_rows=len(rows))
    if MUT == "shuffle":
        d0 = per_cluster(rows); v0 = stat(d0); rng = np.random.default_rng(1); pm = rng.permutation(len(rows)); gp = np.array([r["lgMgp"] - r["dlgR"] * 0 for r in rows]); dlg = np.array([r["d"] - r["lgMgp"] for r in rows]); ds = gp[pm] + dlg
        for r, x in zip(rows, ds): r["d"] = float(x)
    if MUT == "ra" and not rows: P("MUTATE RA + 1 degree: no match at all, against 181 real rows: BITES"); open(os.path.join(HERE, f"gs4_match{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
    D = per_cluster(rows); v = stat(D); lgm = np.array([np.median([r["lgM"] for r in L]) for L in D.values()]); lgg = np.array([np.median([r["lgMgp"] for r in L]) for L in D.values()])
    P(f"rows matched {len(rows)}, unique clusters in M500 range, V09 out {len(D)}; in lensing sample {sum(any(r['inlens'] for r in L) for L in D.values())}")
    P("\nPRIMARY"); pr = line("all", D); RES["primary"] = pr
    s, ss, c0 = fit(lgm, v); P(f"  fit d = {c0:+.3f} + ({s:+.3f} +- {ss:.3f}) (lg M500 - {PIV}) against eRASS1's M500, {abs(s) / ss:.1f} sigma"); s2, ss2, c2 = fit(lgg, v); P(f"  same against pointed lg Mgas, not graded, pivot {PIV}: slope {s2:+.3f} +- {ss2:.3f}, {abs(s2) / ss2:.1f} sigma"); RES["fit"] = dict(c0=c0, s=s, se=ss, s_vs_pointed_gas=s2, se_vs_pointed_gas=ss2); MD = abs(s) > 2 * ss
    P("\nBY LENSING M500 TERCILE"); ter = {}
    for lab, a, b in (("M1 4.4e13-1.36e14", LO, T1), ("M2 1.36e14-2.39e14", T1, T2), ("M3 2.39e14-5.6e14", T2, HI)): ter[lab] = line(lab, {k: L for k, L in D.items() if a <= 10 ** L[0]["lgM"] < b or (b == HI and 10 ** L[0]["lgM"] == HI)})
    RES["tercile"] = ter
    P("\nBY CATALOGUE, in M500 range: d at eRASS1's R500 (first), d at the catalogue's own R500 (second)"); bc = {}
    for ca in ("XC", "L20", "L15", "C08", "E16", "M08", "L13", "S09", "M13", "V09"):
        Dc = per_cluster([r for r in rows if r["cat"] == ca], False); bc[ca] = line(ca, Dc); bc[ca]["own"] = line(ca + " own R500", Dc, "d_own"); bc[ca]["ter"] = {}
        for lab, a, b in (("M1", LO, T1), ("M2", T1, T2), ("M3", T2, HI * 1.0001)):
            Dt = {k: L for k, L in Dc.items() if a <= 10 ** L[0]["lgM"] < b}; vt = stat(Dt) if Dt else []; bc[ca]["ter"][lab] = dict(n=len(vt), med=float(np.median(vt)) if len(vt) else None, se=boot_med(vt)[1] if len(vt) > 1 else None)
        Dr = [r for r in rows if r["cat"] == ca]; bc[ca]["rows_all_mass"] = len(Dr)
    RES["catalogue"] = bc
    P("\nBY INSTRUMENT GROUP"); inst = {}
    for g_ in ("XMM", "Chandra", "MIXED"): inst[g_] = line(g_, per_cluster([r for r in rows if r["inst"] == g_]))
    RES["instrument"] = inst; ID = inst["XMM"].get("cls") != inst["Chandra"].get("cls")
    P("\nSENSITIVITY, not graded"); sens = {}
    sens["own R500"] = line("each catalogue's own R500", D, "d_own")
    for s_ in (1.0, 1.4): sens[f"s {s_}"] = line(f"gas slope {s_}", per_cluster(match(3.0, s_)))
    sens["6 arcmin"] = line("6 arcmin", per_cluster(match(6.0)))
    sens["profile"] = line("profile-read rows only (X-COP)", per_cluster([r for r in rows if r["how"] == "profile"])); sens["slope"] = line("slope-converted rows only", per_cluster([r for r in rows if r["how"] == "slope"]))
    medc = np.median([L[0]["cts"] for L in D.values()])
    sens["cts hi"] = line(f"eRASS1 CTS500 above matched median {medc:.0f}", {k: L for k, L in D.items() if L[0]["cts"] >= medc}); sens["cts lo"] = line("CTS500 below", {k: L for k, L in D.items() if L[0]["cts"] < medc})
    sens["z lo"] = line("z < 0.2", {k: L for k, L in D.items() if L[0]["z"] < .2}); sens["z hi"] = line("z >= 0.2", {k: L for k, L in D.items() if L[0]["z"] >= .2}); sens["hse free"] = line("M13 and E16 (no hydrostatic radius)", per_cluster([r for r in rows if r["cat"] in ("M13", "E16")]))
    sens["no M13"] = line("primary without M13", per_cluster([r for r in rows if r["cat"] != "M13"])); sens["lens"] = line("clusters in the lensing sample", {k: L for k, L in D.items() if L[0]["inlens"]}); RES["sensitivity"] = sens
    # K1
    SM = json.load(open(os.path.join(RB, "SM1_cluster_sample_match", "sm1_cluster_sample_match_results.json")))["matched"]; RFX = {q["xcop"]: q for q in json.load(open(os.path.join(RB, "RF3_cluster_keys_hse_free", "rf3_inputs.json")))["XF"]["rows"]}; A = {r["name"]: r for r in rows if r["cat"] == "XC"}; k1 = 0.0; P("\nK1")
    for q in SM:
        if q["xcop"] in A: a = A[q["xcop"]]; k1 = max(k1, abs(a["d_own"] + q["dlogMgas500"]), abs(a["d"] - RFX[q["xcop"]]["dex_at_eRASS_R500"]))
        else: k1 = 9.9
    P(f"  X-COP row against SM1 (own R500) and RF3 (eRASS1's R500), {len(SM)} clusters: max |d| {k1:.1e}: {'PASS' if k1 <= 1e-3 else 'FAIL'}"); RES["K1a"] = k1; fi = {}
    for q in SM:
        j = EN.index(q["erass"]); o = [r for r in rows if r["j"] == j and r["cat"] != "XC"]; P(f"  {q['xcop']:7s} SM1 own-R500 {-q['dlogMgas500']:+.3f}, at eRASS1 R500 {RFX[q['xcop']]['dex_at_eRASS_R500']:+.3f}; other tables: " + (", ".join(f"{r['cat']} own {r['d_own']:+.3f}, at eRASS1 {r['d']:+.3f}" for r in o) or "none"))
        for r in o: fi.setdefault(q["xcop"], []).append(abs(r["d"] - RFX[q["xcop"]]["dex_at_eRASS_R500"]))
    if fi: mf = float(np.median([x for L in fi.values() for x in L])); P(f"  median |d_table - d_X-COP| at eRASS1's R500 over {sum(map(len, fi.values()))} rows: {mf:.3f}, line 0.05: {'PASS' if mf <= .05 else 'OVER'}"); RES["K1b"] = mf
    # K2
    pairs = []; M2 = {}
    for j in {r["j"] for r in rows}:
        L = [r for r in rows if r["j"] == j]
        for i_ in range(len(L)):
            for k_ in range(i_ + 1, len(L)): pairs.append(abs(L[i_]["d"] - L[k_]["d"])); a, b = sorted((L[i_]["cat"], L[k_]["cat"])); M2.setdefault(a + "-" + b, []).append(L[i_]["d"] - L[k_]["d"] if L[i_]["cat"] == a else L[k_]["d"] - L[i_]["d"])
    k2 = float(np.median(pairs)) if pairs else float("nan"); P(f"\nK2 clusters in two or more catalogues: {len(pairs)} pairs, median |difference| {k2:.3f}, line 0.05: {'PASS' if k2 <= .05 else 'OVER, catalogue scatter'}"); RES["K2"] = k2
    for k, x in sorted(M2.items()): P(f"  {k}: N {len(x)}, median {np.median(x):+.3f}")
    RES["pairs"] = {k: dict(n=len(x), med=float(np.median(x))) for k, x in M2.items()}
    V = cls(pr["med"], pr["se"]) if pr["n"] >= 20 else "UNDECIDED"; TAGS = (" [MASS-DEPENDENT]" if MD else "") + (" [INSTRUMENT-DEPENDENT]" if ID else ""); P(f"\nVERDICT{TAG}: {V}{TAGS}; median {pr['med']:+.3f} +- {pr['se']:.3f}, N {pr['n']}"); RES.update(verdict=V, tags=TAGS)
    json.dump(RES, open(os.path.join(HERE, f"gs4_results{TAG}.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"gs4_match{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    if not MUT: w = csv.DictWriter(open(os.path.join(HERE, "gs4_matched.csv"), "w"), list(rows[0].keys())); w.writeheader(); w.writerows(rows)
