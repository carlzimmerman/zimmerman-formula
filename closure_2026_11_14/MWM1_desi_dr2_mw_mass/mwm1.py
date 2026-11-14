#!/usr/bin/env python3
"""
MWM1: the framework's Milky Way line against DESI DR2's halo-free enclosed-mass curves (NIMBLE), 20-80 kpc.
Criteria: FROZEN_CRITERIA.md (d749c46dcf), committed alone before this script.
Usage: python3 -I -B mwm1.py <figdata.zip> <raw1_model.py> <mwm1_published_numbers.csv> <outdir> [MUTATE]
Reads the zip, the model and the CSV as data only; writes mwm1.out and mwm1_results.json (or mwm1_MUTATE.out).
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sys, os, io, csv, json, math, hashlib, zipfile, importlib.util
import numpy as np

ZIP, MODEL, PUB, OUTD = sys.argv[1:5]
MUT = len(sys.argv) > 5 and sys.argv[5] == "MUTATE"
OUT = open(os.path.join(OUTD, "mwm1_MUTATE.out" if MUT else "mwm1.out"), "w")
def say(s=""):
    print(s); OUT.write(s + "\n")
def sec(t): say("=" * 100); say(t); say("=" * 100)

ZSHA = "1b132abc3f163887160efb29a88d294ce5fb0751d2e389951da9c4c237e35ee1"
A0STD = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
EN = {"canonical": 0.000160, "alt": 0.000110}
RADII = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
FOOT = ("canonical", "alt")
CASES = ("FW_census", "FW_rc")
NIMB = [("nimble-a", "rrl"), ("nimble-a", "bhb"), ("nimble-b", "rrl"), ("nimble-b", "bhb")]
BIAS_T3 = {("nimble-a", "rrl"): 3.9, ("nimble-a", "bhb"): -2.2, ("nimble-b", "rrl"): -4.1, ("nimble-b", "bhb"): -2.1}
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19

# ---- model, loaded read-only by path
spec = importlib.util.spec_from_file_location("raw1_model", MODEL); RM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RM)
AMULT = {f: A0STD[f] / RM.A0[f] for f in FOOT}

# ---- published numbers
PN = list(csv.DictReader(open(PUB)))
def pub(src, q, r=None):
    for x in PN:
        if x["source"] == src and x["quantity"] == q and (r is None or x["r_kpc"] == str(r)): return x
    raise KeyError((src, q, r))
T4 = {r: pub("DESI_DR2_III", "log10M_all", r) for r in RADII}
T4R = {r: pub("DESI_DR2_III", "log10M_RRL", r) for r in RADII}
T4B = {r: pub("DESI_DR2_III", "log10M_BHB", r) for r in RADII}

# ---- zip
zb = open(ZIP, "rb").read(); zsha = hashlib.sha256(zb).hexdigest()
Z = zipfile.ZipFile(io.BytesIO(zb)); P = "desi-dr2-mw-mass-figdata/"
F10 = {}
for x in csv.DictReader(io.TextIOWrapper(Z.open(P + "fig10/desi-dr2-menc.csv"))):
    F10[(x["method"], x["tracer"], float(x["r_kpc"]))] = tuple(float(x[k]) for k in ("Menc_med", "Menc_lo", "Menc_hi"))
F11 = {}
for x in csv.DictReader(io.TextIOWrapper(Z.open(P + "fig11/desi-dr2-joint-menc.csv"))):
    F11[(x["tracer"], float(x["r_kpc"]))] = tuple(float(x[k]) for k in ("Menc_med", "Menc_lo", "Menc_hi"))

# ---- framework line
def M_line(r, case, foot, mult=1.0, bscale=1.0, hot=False, a0m=None):
    """enclosed dynamical mass (1e11 Msun) of the no-field line; bscale scales stars+cold gas; hot adds MB15."""
    r = float(r); st, gs = RM._tab()
    Ms = np.interp(np.log(r), np.log(RM.RTAB), st); Mg = np.interp(np.log(r), np.log(RM.RTAB), gs)
    if case == "FW_rc": Ms = Ms * RM.MSTAR_RC[foot] / RM.MSTAR_CENSUS
    Mb = bscale * (Ms + Mg) + (4.3e10 * (r / 250.0) ** 1.5 * MSUN if hot else 0.0)
    gb = G * Mb / (r * KPC) ** 2
    if case == "N": return mult * Mb / MSUN / 1e11
    a0 = RM.A0[foot] * (AMULT[foot] if a0m is None else a0m)
    return mult * float(RM.nu_fw(gb / a0)) * Mb / MSUN / 1e11
def yb(r, foot):
    st, gs = RM._tab(); Mb = np.interp(np.log(r), np.log(RM.RTAB), st) + np.interp(np.log(r), np.log(RM.RTAB), gs)
    return G * Mb / (r * KPC) ** 2 / A0STD[foot]

# ---- known answers
sec("Known answers (stop before any word if one fails)")
ok_all = True
def ka(name, ok, detail):
    global ok_all; ok_all &= bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
def rm_M(r, model, foot): return float(RM.M_of_g(RM.g_model(r, model, foot), r)) / 1e11
for (r, model, foot, want, tol) in [(80, "FW_census", "canonical", 5.6905, 5e-4), (80, "FW_census", "alt", 6.2183, 5e-4),
        (30, "FW_census", "canonical", 2.331, 2e-3), (30, "FW_census", "alt", 2.526, 2e-3), (50, "FW_census", "canonical", 3.683, 2e-3),
        (50, "FW_census", "alt", 4.012, 2e-3), (30, "FW_rc", "canonical", 2.644, 2e-3), (30, "FW_rc", "alt", 2.725, 2e-3),
        (50, "FW_rc", "canonical", 4.143, 2e-3), (50, "FW_rc", "alt", 4.308, 2e-3)]:
    got = rm_M(r, model, foot); mine = M_line(r, model, foot, a0m=1.0)
    ka(f"KA1 {model} {foot} {r} kpc (RAW1-rounded a0)", abs(got - want) <= tol and abs(mine - got) < 1e-9 * got, f"raw1_model {got:.4f}, this script {mine:.4f}, RAW1 {want}")
g30 = float(RM.g_model(30, "FW_census", "canonical")); Msi = g30 * (30 * 3.0857e19) ** 2 / 6.674e-11 / 1.989e30
ka("KA2 SI M = g r^2 / G", abs(Msi / float(RM.M_of_g(g30, 30)) - 1) < 1e-9, f"{Msi:.6e} Msun vs M_of_g {float(RM.M_of_g(g30, 30)):.6e}")
vc = math.sqrt(6.674e-11 * 6.36e11 * 1.989e30 / (80 * 3.0857e19)) / 1e3
ka("KA3 DESI M(<80) 6.36e11 -> v_c", abs(vc - 185) <= 1, f"{vc:.2f} km/s")
t80 = F11[("total", 80.0)]; t30 = F11[("total", 30.0)]
ka("KA4 zip sha256", zsha == ZSHA, zsha[:16] + "...")
ka("KA4 fig11 total 80 kpc vs Table 4 (6.36, 5.88, 6.89)", max(abs(t80[0] - 6.36), abs(t80[1] - 5.88), abs(t80[2] - 6.89)) <= 0.01, str(t80))
ka("KA4 fig11 total 30 kpc vs Table 4 2.65", abs(t30[0] - 2.65) <= 0.01, str(t30))
nmb = {("nimble-a", "rrl"): (2.449, 6.678), ("nimble-a", "bhb"): (2.481, 5.993), ("nimble-b", "rrl"): (2.787, 6.181), ("nimble-b", "bhb"): (2.569, 6.543)}
for k, (v30, v80) in nmb.items():
    a, b = F10[k + (30.0,)][0], F10[k + (80.0,)][0]
    ka(f"KA5 NMB1 {k[0]} {k[1]} 30/80", abs(a - v30) <= 0.002 and abs(b - v80) <= 0.002, f"{a:.3f}/{b:.3f} vs {v30}/{v80}")
if not ok_all:
    say("A KNOWN ANSWER FAILED: stopping before any word."); sys.exit(2)

# ---- data sets
def ds_nimble(curves, t4, scale=None, extra=()):
    """per radius: D (dex), s_D lower, s_D upper, s_spread"""
    out = {}
    for r in RADII:
        logs = []
        for c in list(curves) + [e for e in extra if r >= 50]:
            m = F10[c + (float(r),)][0]
            if scale: m *= scale(c, r)
            logs.append(math.log10(m * 1e11))
        out[r] = dict(D=float(np.mean(logs)), sl=float(t4[r]["err_minus"]), su=float(t4[r]["err_plus"]),
                      ss=float(np.std(logs, ddof=1)), n=len(logs))
    return out
def scaled(base, f):
    out = {}
    for r, v in base.items():
        v = dict(v); v["D"] += math.log10(f(r)); out[r] = v
    return out
def li_point(corr=False):
    vals = [pub("Li_LAMOST", q) for q in ("M_Jeans_RRL", "M_TME_RRL", "M_Jeans_BHB", "M_TME_BHB")]
    c = 1 / (1 - 0.137) if corr else 1.0
    logs = [math.log10(float(v["value"]) * 1e11 * c) for v in vals]
    errs = [float(v["err_minus"]) / float(v["value"]) / math.log(10) for v in vals]
    return dict(D=float(np.mean(logs)), sl=float(np.mean(errs)), su=float(np.mean(errs)), ss=float(np.std(logs, ddof=1)), n=4, r_eval=82.25)

PRIMARY = ds_nimble(NIMB, T4)
def grade(ds, case, foot, mult=1.0, hot=False, line_override=None):
    rows = []
    for r in RADII:
        d = ds[r]; re_ = d.get("r_eval", r)
        Mf = line_override(r) if line_override else M_line(re_, case, foot, mult=mult, hot=hot)
        lf = math.log10(Mf * 1e11)
        if case == "N": sfw = 0.5 * abs(math.log10(1.1 / 0.9))
        else: sfw = 0.5 * abs(math.log10(M_line(re_, case, foot, bscale=1.1, hot=hot) / M_line(re_, case, foot, bscale=0.9, hot=hot)))
        sD = d["sl"] if lf < d["D"] else d["su"]
        sig = math.sqrt(sD ** 2 + d["ss"] ** 2 + sfw ** 2); z = (lf - d["D"]) / sig
        w = "PASS" if abs(z) <= 2 else ("HIGH" if z > 0 else "LOW")
        rows.append(dict(r=r, r_eval=re_, D=d["D"], M_D=10 ** d["D"] / 1e11, M_line=Mf, sD=sD, ss=d["ss"], sfw=sfw, sigma=sig, z=z, word=w))
    return rows
def row_word(rows):
    bad = [(x["r"], x["word"]) for x in rows if x["word"] != "PASS"]
    return ("PASS", "MW MASS PROFILE PASSES") if not bad else ("FAIL", "STILL FAILS [" + ", ".join(f"{r} {w}" for r, w in bad) + "]")

T1 = ds_nimble([("nimble-a", "rrl"), ("nimble-b", "rrl")], T4R)
T2 = ds_nimble([("nimble-a", "bhb"), ("nimble-b", "bhb")], T4B)
T3 = dict(PRIMARY); T3[80] = li_point(False)
T3c = dict(PRIMARY); T3c[80] = li_point(True)
ALTS = {"T1 RRL only": T1, "T2 BHB only": T2, "T3 Li et al. at 82.25": T3, "T3c Li corrected": T3c}
BR = {
    "B1 bias correction undone": ds_nimble(NIMB, T4, scale=lambda c, r: 1 + BIAS_T3[c] / 100),
    "B2 LMC x0.90": scaled(PRIMARY, lambda r: 0.90),
    "B3 LMC x0.80 at r>=50": scaled(PRIMARY, lambda r: 0.80 if r >= 50 else 1.0),
    "B4 cold debris x1.10 at r>=40": scaled(PRIMARY, lambda r: 1.10 if r >= 40 else 1.0),
    "B5+ beta+0.1 x0.953": scaled(PRIMARY, lambda r: 1 - 0.2 / 4.3),
    "B5- beta-0.1 x1.047": scaled(PRIMARY, lambda r: 1 + 0.2 / 4.3),
    "B6- flattening x0.95": scaled(PRIMARY, lambda r: 0.95),
    "B6+ flattening x1.05": scaled(PRIMARY, lambda r: 1.05),
    "B7 GME added at 50-80": ds_nimble(NIMB, T4, extra=[("gme", "rrl"), ("gme", "bhb")]),
}
T4DS = {r: dict(D=float(T4[r]["value"]), sl=float(T4[r]["err_minus"]), su=float(T4[r]["err_plus"]), ss=0.0, n=1) for r in RADII}

def table(rows, label):
    say(f"  {label}")
    say("    r   D[1e11]  line[1e11]  sD     ss     sFW    sigma   z      word")
    for x in rows:
        say(f"   {x['r']:3d}  {x['M_D']:6.3f}   {x['M_line']:6.3f}    {x['sD']:.3f}  {x['ss']:.3f}  {x['sfw']:.3f}  {x['sigma']:.3f}  {x['z']:+6.2f}  {x['word']}")

RES = {"inputs": {"zip_sha256": zsha}, "data": {}, "cases": {}, "reported": {}, "twins": {}}
if MUT:
    sec("Twins and mutations (FROZEN_CRITERIA section 9)")
    for foot in FOOT:
        line = {r: M_line(r, "FW_census", foot) for r in RADII}
        tw0 = {r: dict(PRIMARY[r], D=math.log10(line[r] * 1e11)) for r in RADII}
        w0 = row_word(grade(tw0, "FW_census", foot))[1]
        say(f"  TW0 {foot}: {w0}  -> {'did not bite (as required)' if w0 == 'MW MASS PROFILE PASSES' else 'BIT (twin failed)'}")
        rng = np.random.default_rng(20261114); npass = 0
        for s in range(200):
            dsn = {r: dict(PRIMARY[r], D=math.log10(line[r] * 1e11) + rng.normal(0, PRIMARY[r]["sl"])) for r in RADII}
            npass += row_word(grade(dsn, "FW_census", foot))[0] == "PASS"
        say(f"  TW1 {foot}: row passes in {npass}/200 -> {'did not bite (>= 160 required)' if npass >= 160 else 'BIT (twin failed)'}")
        for case in CASES:
            rw = grade(PRIMARY, case, foot, mult=0.8); nlow = sum(x["word"] == "LOW" for x in rw)
            say(f"  MU1 {case} {foot} x0.8: {row_word(rw)[1]} -> {'bit' if nlow >= 1 else 'DID NOT BITE'}")
        mu2 = scaled(PRIMARY, lambda r: 1.5 if r >= 50 else 1.0)
        rw = grade(mu2, "FW_census", foot); ok = all(x["word"] == "LOW" for x in rw if x["r"] >= 50)
        say(f"  MU2 {foot} D x1.5 at r>=50: {row_word(rw)[1]} -> {'bit' if ok else 'DID NOT BITE'}")
    OUT.close(); sys.exit(0)

sec("Halo-free DESI data used (fig10 NIMBLE curves, bias-corrected by the paper)")
say("    r   A-RRL  A-BHB  B-RRL  B-BHB  | GME-RRL GME-BHB | emPDF-RRL emPDF-BHB | Table4 all")
for r in RADII:
    v = [F10[c + (float(r),)][0] for c in NIMB]
    g = [F10.get(("gme", t, float(r)), (float("nan"),))[0] for t in ("rrl", "bhb")]
    e = [F10[("empdf", t, float(r))][0] for t in ("rrl", "bhb")]
    say(f"   {r:3d}  " + "  ".join(f"{x:5.3f}" for x in v) + f"  |  {g[0]:5.3f}  {g[1]:5.3f}  |  {e[0]:5.3f}    {e[1]:5.3f}  | {float(pub('DESI_DR2_III','M_all',r)['value']):.2f}")
    RES["data"][r] = dict(nimble=dict(zip(["A-RRL", "A-BHB", "B-RRL", "B-BHB"], v)), gme=g, empdf=e, primary=PRIMARY[r])
with open(os.path.join(OUTD, "mwm1_fig10_used.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["method", "tracer", "r_kpc", "Menc_med", "Menc_lo", "Menc_hi", "source"])
    for r in RADII:
        for c in NIMB + [("gme", "rrl"), ("gme", "bhb")]:
            if c + (float(r),) in F10: w.writerow([c[0], c[1], r] + list(F10[c + (float(r),)]) + ["Zenodo 10.5281/zenodo.23712180 fig10/desi-dr2-menc.csv"])

for case in CASES:
    for foot in FOOT:
        sec(f"{case} / {foot} (a0 {A0STD[foot]:.4e})")
        prim = grade(PRIMARY, case, foot); pw = row_word(prim); table(prim, "PRIMARY: NIMBLE four-curve mean")
        alts = {k: row_word(grade(v, case, foot)) for k, v in ALTS.items()}
        for k, v in alts.items():
            rr = grade(ALTS[k], case, foot); x80 = rr[-1]
            say(f"  {k}: {v[1]}   (80-pt: D {x80['M_D']:.3f} line {x80['M_line']:.3f} z {x80['z']:+.2f})")
        brs = {k: row_word(grade(v, case, foot)) for k, v in BR.items()}
        brs["B8 hot gas MB15"] = row_word(grade(PRIMARY, case, foot, hot=True))
        for k, v in brs.items(): say(f"  {k}: {v[1]}")
        nov = any(v[0] != pw[0] for v in alts.values())
        frag = any(v[0] != pw[0] for v in brs.values())
        word = "NO VERDICT" if nov else pw[1]
        if frag: word += ", FRAGILE"
        say(f"  ==> WORD {case} {foot}: {word}")
        RES["cases"][f"{case}/{foot}"] = dict(word=word, primary=prim, primary_row=pw[1], alternatives={k: v[1] for k, v in alts.items()},
                                              brackets={k: v[1] for k, v in brs.items()})

sec("Reported: Newton (baryons only), Table 4 joint (NFW-dependent), RAW1-rounded a0, external-field diagnostic, 100 kpc")
nw = grade(PRIMARY, "N", "canonical"); table(nw, "Newton, baryons only (census)"); say(f"  Newton row: {row_word(nw)[1]}")
RES["reported"]["Newton"] = dict(rows=nw, word=row_word(nw)[1])
for case in CASES:
    for foot in FOOT:
        rw = grade(T4DS, case, foot); say(f"  Table 4 joint (report only) {case} {foot}: {row_word(rw)[1]}; z = " + " ".join(f"{x['z']:+.2f}" for x in rw))
        RES["reported"][f"T4joint/{case}/{foot}"] = row_word(rw)[1]
        rw = [dict(x) for x in grade(PRIMARY, case, foot, line_override=lambda r: M_line(r, case, foot, a0m=1.0))]
        say(f"  RAW1-rounded a0 {case} {foot}: {row_word(rw)[1]}")
say("  External-field diagnostic nu(sqrt(y^2+e^2))/nu(y), FW census:")
diag = {}
for foot in FOOT:
    vals = []
    for r in RADII:
        y = yb(r, foot); vals.append(float(RM.nu_fw(math.sqrt(y * y + EN[foot] ** 2)) / RM.nu_fw(y)))
    diag[foot] = vals; say(f"    {foot}: y(20) {yb(20, foot):.4f} y(80) {yb(80, foot):.5f}; ratio min {min(vals):.7f} max {max(vals):.7f}")
RES["reported"]["external_field_ratio"] = diag
for foot in FOOT:
    say(f"  100 kpc (report only; GME extrapolated BHB 7.4 / RRL 6.2): FW census {foot} {M_line(100, 'FW_census', foot):.3f}, FW rc {M_line(100, 'FW_rc', foot):.3f}")
say(f"  Newton at 100 kpc {M_line(100, 'N', 'canonical'):.3f}")
json.dump(RES, open(os.path.join(OUTD, "mwm1_results.json"), "w"), indent=1, default=float)
OUT.close()
