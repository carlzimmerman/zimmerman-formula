#!/usr/bin/env python3
"""
PLT1 -- the framework's enclosed mass at 100 kpc and beyond against the literature compilation of DESI DR2
Results III Figure 13, in two classes: H (field halo stars) and S (satellites, globular clusters, streams).

Criteria: FROZEN_CRITERIA.md (committed alone, e51543aa5e, before this file existed).
Usage:    python3 -I plt1.py /path/to/desi-dr2-mw-mass-figdata.zip
Writes:   plt1.out, plt1_results.json, plt1_mut.out   (next to this file)

Order is fixed: KA1..KA5, then the mutations, then the graded numbers. A failed known-answer check stops the
script before any graded number. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import sys, os, io, csv, json, math, hashlib, zipfile
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = sys.argv[1]
P = "desi-dr2-mw-mass-figdata/"
MD5 = "5b0cc3aa9947286eb9348e947d01182d"

# ---------------------------------------------------------------- constants (the record's values, as DW1 / G239)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
PC = KPC / 1000.0; MSUN_PC2 = MSUN / PC ** 2
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
E_N = 0.01273
FLOOR = 0.20
T4_ALL = dict(zip([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
                  [1.94, 2.30, 2.65, 3.05, 3.54, 4.08, 4.51, 4.88, 5.19, 5.56, 5.88, 6.14, 6.36]))

OUT = open(os.path.join(HERE, "plt1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 118); say(t); say("=" * 118)
KA_FAIL = []
def ka(name, ok, detail=""):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))
    if not ok: KA_FAIL.append(name)
def stop_if_failed():
    if KA_FAIL:
        say("\nSTOPPED: known-answer check failed -> NO VERDICT as frozen. No graded number was computed.")
        json.dump({"lane": "PLT1", "label": "NO VERDICT (stopped at " + KA_FAIL[0].split()[0] + ")"},
                  open(os.path.join(HERE, "plt1_results.json"), "w"), indent=1)
        sys.exit(0)

# ---------------------------------------------------------------- McMillan 2017 baryons (ported verbatim from dw1.py)
MC = dict(thin =dict(S0=896.0*MSUN_PC2, Rd=2.50*KPC, zd=0.300*KPC, Rm=0.0, vert="exp"),
          thick=dict(S0=183.0*MSUN_PC2, Rd=3.02*KPC, zd=0.900*KPC, Rm=0.0, vert="exp"),
          HI   =dict(Sfid=10.0*MSUN_PC2, Rfid=8.33*KPC, Rd=7.00*KPC, zd=0.085*KPC, Rm=4.0*KPC,  vert="sech2"),
          H2   =dict(Sfid= 2.0*MSUN_PC2, Rfid=8.33*KPC, Rd=1.50*KPC, zd=0.045*KPC, Rm=12.0*KPC, vert="sech2"))
MBULGE, ABULGE = 9.23e9 * MSUN, 0.70 * KPC
def S0_of(c):
    return c["S0"] if "S0" in c else c["Sfid"] / math.exp(-c["Rm"] / c["Rfid"] - c["Rfid"] / c["Rd"])
def sigma_of_R(c, R):
    R = np.maximum(np.asarray(R, float), 1e-6 * KPC)
    return S0_of(c) * np.exp(-c.get("Rm", 0.0) / R - R / c["Rd"])
def disc_mass(c):
    Rg = np.geomspace(1e-5 * KPC, 600 * KPC, 20000)
    return float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg), Rg))
_ZC = {}
def zprofile(c, n=1201):
    key = (c["vert"], round(c["zd"], 9))
    if key in _ZC: return _ZC[key]
    zg = np.linspace(-10 * c["zd"], 10 * c["zd"], n)
    zz = (np.exp(-np.abs(zg) / c["zd"]) / (2 * c["zd"]) if c["vert"] == "exp"
          else 1.0 / np.cosh(zg / (2 * c["zd"])) ** 2 / (4 * c["zd"]))
    cum = np.concatenate([[0.0], np.cumsum((zz[1:] + zz[:-1]) / 2 * np.diff(zg))]); cum /= cum[-1]
    _ZC[key] = (zg, zz, cum); return _ZC[key]
_MS = {}
def M_sph(r_kpc):
    if r_kpc in _MS: return _MS[r_kpc]
    r = float(r_kpc) * KPC
    tot = MBULGE * r ** 2 / (r + ABULGE) ** 2
    Rg = np.linspace(1e-4 * KPC, min(r, 60 * KPC), 4000)
    h = np.sqrt(np.maximum(r ** 2 - Rg ** 2, 0.0))
    for k, c in MC.items():
        zg, zz, cum = zprofile(c)
        tot += float(TRAPZ(2 * np.pi * Rg * sigma_of_R(c, Rg) * np.interp(h, zg, cum), Rg))
    _MS[r_kpc] = tot; return tot
MB = sum(disc_mass(c) for c in MC.values()) + MBULGE

# ---------------------------------------------------------------- the line
def nu(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, float), 1e-14))))
MU = np.linspace(-1.0, 1.0, 4001)
def M_line(r_kpc, a0, eN=0.0, A=1.0):
    """enclosed dynamical mass [1e11 Msun]; eN = 0 is E0, eN > 0 is G239's QUMOND angle average"""
    Mb = A * M_sph(r_kpc)
    gb = G * Mb / (r_kpc * KPC) ** 2 / a0
    if eN == 0.0:
        return float(nu(gb)) * Mb / MSUN / 1e11
    gm = np.sqrt(gb * gb + eN * eN + 2 * gb * eN * MU)
    return float(TRAPZ(nu(gm) * (gb + eN * MU), MU) / 2.0) / gb * Mb / MSUN / 1e11

# ---------------------------------------------------------------- the statistic
def pull(Ml, M, elo, ehi, floor, sym=False):
    slo = math.log10(M / (M - elo)); shi = math.log10((M + ehi) / M)
    if sym: slo = shi = 0.5 * (slo + shi)
    s = math.log10(1.0 + floor) if floor > 0 else 0.0
    side = slo if Ml < M else shi
    return (math.log10(Ml) - math.log10(M)) / math.sqrt(side * side + s * s)
def label_of(zm):
    if abs(zm) <= 2: return "PASSES"
    return ("FAILS LOW" if zm < 0 else "FAILS HIGH") + (" (beyond 3)" if abs(zm) > 3 else "")
def grade(rows, linefn, floor=FLOOR, sym=False):
    z = [pull(linefn(r["r"]), r["M"], r["lo"], r["hi"], floor, sym) for r in rows]
    zm = float(np.median(z))
    return dict(z=z, zmed=zm, label=label_of(zm), n=len(z))

# ---------------------------------------------------------------- file access
Z = zipfile.ZipFile(ZIP)
def rows(name):
    return list(csv.DictReader(io.TextIOWrapper(Z.open(P + name), encoding="utf-8")))
def fnum(x):
    try: return float(x)
    except Exception: return float("nan")

# ====================================================================================================
sec("PLT1  the framework's enclosed mass at >= 100 kpc vs the Figure 13 literature compilation   (criteria e51543aa5e)")
say("     TEST lane. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

sec("KNOWN-ANSWER CHECKS")
md5 = hashlib.md5(open(ZIP, "rb").read()).hexdigest()
ka("KA1 the file is the one named in the criteria", md5 == MD5, f"md5 {md5}")
stop_if_failed()

J = {round(fnum(r["r_kpc"])): fnum(r["Menc_Msun"]) / 1e11 for r in rows("fig13/desi-dr2-joint-menc.csv")}
w2 = max(abs(J.get(k, float("nan")) - v) for k, v in T4_ALL.items())
ka("KA2 fig13's joint file reproduces Table 4's All column (13 values, each within 0.011e11)", w2 <= 0.011,
   f"largest difference {w2:.4f} e11; masses in the file are in Msun")

f30, f80 = M_sph(30.0) / MB, M_sph(80.0) / MB
ka("KA3 the baryon model as ported (total 6.681e10 within 0.1 %; M_sph/M_b 0.9777 at 30, 0.9972 at 80, within 0.0005)",
   abs(MB / MSUN / 6.681e10 - 1) <= 1e-3 and abs(f30 - 0.9777) <= 5e-4 and abs(f80 - 0.9972) <= 5e-4,
   f"M_b = {MB/MSUN:.4e}; M_sph/M_b = {f30:.4f}, {f80:.4f}")

ref = {("canonical", 0.0, 80.0): 5.691, ("alt", 0.0, 80.0): 6.219,
       ("canonical", E_N, 80.0): 4.977, ("canonical", E_N, 150.0): 5.252, ("canonical", E_N, 200.0): 5.264, ("canonical", E_N, 300.0): 5.270,
       ("alt", E_N, 80.0): 5.109, ("alt", E_N, 150.0): 5.257, ("alt", E_N, 200.0): 5.266, ("alt", E_N, 300.0): 5.270}
w4 = max(abs(M_line(r, A0[f], e) / v - 1) for (f, e, r), v in ref.items())
se = math.sqrt(E_N); ex = math.exp(-se); nue = 1 / (1 - ex); dnu = -nue * nue * ex / (2 * se)
closed = (nue + E_N * dnu / 3.0) * MB / MSUN / 1e11
w4b = max(abs(M_line(2000.0, A0[f], E_N) / closed - 1) for f in A0)
ka("KA4 the line reproduces the record (E0 at 80; E1 at 80, 150, 200, 300; within 0.5 %) and the closed-form plateau",
   w4 <= 0.005 and w4b <= 0.005, f"worst vs record {w4:.3%}; closed form {closed:.3f} e11, worst at 2000 kpc {w4b:.3%}")

syn = [dict(r=100.0, M=5.0e11, lo=0.5e11, hi=0.6e11), dict(r=150.0, M=8.0e11, lo=1.0e11, hi=1.0e11), dict(r=200.0, M=1.0e12, lo=2e11, hi=3e11)]
def three_below(r):
    row = [x for x in syn if x["r"] == r][0]
    stot = math.sqrt(math.log10(row["M"] / (row["M"] - row["lo"])) ** 2 + math.log10(1 + FLOOR) ** 2)
    return row["M"] / 1e11 * 10 ** (-3 * stot)
# synthetic rows are in Msun; convert to the 1e11 unit the line uses
def grade_units(rws, fn, **kw):
    return grade([dict(r=x["r"], M=x["M"] / 1e11, lo=x["lo"] / 1e11, hi=x["hi"] / 1e11) for x in rws], fn, **kw)
on = grade_units(syn, lambda r: {100.0: 5.0, 150.0: 8.0, 200.0: 10.0}[r]); lowg = grade_units(syn, three_below)
ka("KA5 the statistic on synthetic rows (on the line: z = 0, PASSES; three sigma above: z = -3, FAILS LOW; median of -4,-1,0,1,4 is 0)",
   max(abs(v) for v in on["z"]) < 1e-12 and on["label"] == "PASSES"
   and max(abs(v + 3) for v in lowg["z"]) < 1e-9 and lowg["label"] == "FAILS LOW" and float(np.median([-4, -1, 0, 1, 4])) == 0.0,
   f"on-line pulls {on['z']}; three-sigma pulls {[round(v, 6) for v in lowg['z']]} -> {lowg['label']}")
stop_if_failed()

# ---------------------------------------------------------------- the rows (first read of the literature values)
def load(name, mcol, tcol):
    good, bad = [], []
    for r in rows(name):
        rk = fnum(r["r_kpc"])
        if not (rk >= 100.0): continue
        M, lo, hi = fnum(r[mcol]) / 1e11, fnum(r["err_lo_Msun"]) / 1e11, fnum(r["err_hi_Msun"]) / 1e11
        d = dict(label=r["label"], tracer=r[tcol], method=r["method"], r=rk, M=M, lo=lo, hi=hi)
        (good if (M > 0 and 0 < lo < M and hi > 0) else bad).append(d)
    return sorted(good, key=lambda d: (d["r"], d["M"])), bad
H, Hbad = load("fig13/literature-halo-stars.csv", "Menc_Msun", "halo_stars_tracer")
S, Sbad = load("fig13/literature-other-tracers.csv", "value_Msun", "tracer")
CLS = {"H": H, "S": S}

CASES = [("E1", "canonical", E_N), ("E1", "alt", E_N), ("E0", "canonical", 0.0), ("E0", "alt", 0.0)]
def line_fn(f, e, a0mult=1.0, A=1.0):
    return lambda r: M_line(r, A0[f] * a0mult, e, A)

# ---------------------------------------------------------------- mutations (separate output)
MUT = open(os.path.join(HERE, "plt1_mut.out"), "w")
MUT.write("PLT1 mutations (criteria e51543aa5e). Each must bite in each class.\n")
POWER = {}
for c, rws in CLS.items():
    ok = len(rws) >= 3
    if ok:
        for f in A0:
            g1 = grade(rws, line_fn(f, 0.05)); b1 = g1["label"].startswith("FAILS LOW")
            g2 = grade(rws, line_fn(f, 0.0, 16.0)); b2 = g2["label"].startswith("FAILS HIGH")
            MUT.write(f"class {c} {f:9s}: M1 e_N = 0.05 z_med {g1['zmed']:+.2f} -> {g1['label']} [{'bites' if b1 else 'DOES NOT BITE'}];  "
                      f"M2 a0 x 16 z_med {g2['zmed']:+.2f} -> {g2['label']} [{'bites' if b2 else 'DOES NOT BITE'}]\n")
            ok &= b1 and b2
    else:
        MUT.write(f"class {c}: fewer than three usable rows\n")
    POWER[c] = ok
MUT.close()
sec("MUTATIONS")
say("  written to plt1_mut.out: " + "; ".join(f"class {c}: {'both bite' if POWER[c] else 'NO POWER'}" for c in CLS))

# ====================================================================================================
sec("THE ROWS  (every row of the two files with r >= 100 kpc; masses in 1e11 Msun; z = pull with the 20 per cent floor)")
say(f"  excluded for an unusable error: H {len(Hbad)}, S {len(Sbad)}" + ("".join(f"\n     {b}" for b in Hbad + Sbad)))
say("  class  r     M      +hi    -lo    tracer            method               label                             z: E1can  E1alt  E0can  E0alt")
for c, rws in CLS.items():
    for r in rws:
        zz = [pull(M_line(r["r"], A0[f], e), r["M"], r["lo"], r["hi"], FLOOR) for _, f, e in CASES]
        say(f"  {c}   {r['r']:5.0f}  {r['M']:6.2f} {r['hi']:6.2f} {r['lo']:6.2f}   {r['tracer'][:16]:16s}  {r['method'][:19]:19s}  {r['label'][:32]:32s}   "
            + "  ".join(f"{v:+5.2f}" for v in zz))
say("\n  the line at selected radii [1e11 Msun]:   r     E1 can   E1 alt   E0 can   E0 alt")
for r in (100.0, 125.0, 150.0, 200.0, 250.0, 300.0):
    say(f"                                          {r:5.0f}   " + "   ".join(f"{M_line(r, A0[f], e):6.2f}" for _, f, e in CASES))

sec("THE GATE   class median pull, |z_med| <= 2 passes.  Negative = line below the published masses")
RES = {}
def variants(rws, fn):
    v = {}
    far = [r for r in rws if r["r"] >= 150.0]
    v["r >= 150 only"] = grade(far, fn)["label"] if len(far) >= 3 else None
    v["symmetric errors"] = grade(rws, fn, sym=True)["label"]
    v["10 per cent floor"] = grade(rws, fn, floor=0.10)["label"]
    v["30 per cent floor"] = grade(rws, fn, floor=0.30)["label"]
    loo = [grade(rws[:i] + rws[i + 1:], fn)["label"] for i in range(len(rws))]
    v["any single row dropped"] = loo
    return v
for rd, f, e in CASES:
    fn = line_fn(f, e); key = f"{rd}_{f}"; RES[key] = {}
    say(f"\n  {rd} {f}:")
    labs = {}
    for c, rws in CLS.items():
        if not POWER[c]:
            labs[c] = "NO POWER"; say(f"     class {c}: NO POWER ({len(rws)} rows)"); RES[key][c] = dict(label="NO POWER", n=len(rws)); continue
        g = grade(rws, fn); v = variants(rws, fn)
        base = g["label"].replace(" (beyond 3)", "")
        flips = [k for k, lab in v.items() if lab is not None and (
                 any(x.replace(" (beyond 3)", "") != base for x in lab) if isinstance(lab, list) else lab.replace(" (beyond 3)", "") != base)]
        lab = g["label"] + (", FRAGILE" if flips else "")
        labs[c] = lab
        n2 = sum(1 for z in g["z"] if abs(z) > 2)
        g0 = grade(rws, fn, floor=0.0)
        say(f"     class {c}: n = {g['n']}, z_med = {g['zmed']:+.2f}, range [{min(g['z']):+.2f}, {max(g['z']):+.2f}], rows beyond 2 sigma: {n2}  ->  {lab}")
        say(f"        variants: " + "; ".join(
            f"{k}: " + ("skipped (fewer than 3 rows)" if lab is None else (("all " + lab[0]) if isinstance(lab, list) and len(set(lab)) == 1
                         else ("/".join(sorted(set(lab))) if isinstance(lab, list) else lab))) for k, lab in v.items()))
        say(f"        reported, published errors only: z_med = {g0['zmed']:+.2f} -> {g0['label']}")
        RES[key][c] = dict(label=lab, n=g["n"], zmed=g["zmed"], z=g["z"], rows_beyond_2=n2, flips=flips, zmed_published_only=g0["zmed"])
    hb, sb = labs["H"].split(",")[0].replace(" (beyond 3)", ""), labs["S"].split(",")[0].replace(" (beyond 3)", "")
    if hb == "NO POWER" and sb == "NO POWER": head = "NO POWER"
    elif hb == "NO POWER": head = labs["S"] + " (S only)"
    elif sb == "NO POWER": head = labs["H"] + " (H only)"
    elif hb == sb: head = hb + (", FRAGILE" if ("FRAGILE" in labs["H"] or "FRAGILE" in labs["S"]) else "")
    else: head = "SPLIT"
    RES[key]["headline"] = head; RES[key]["case_label"] = f"H: {labs['H']} / S: {labs['S']}"
    say(f"     CASE LABEL: H: {labs['H']} / S: {labs['S']}     HEADLINE: {head}")

sec("REPORTED, NOT GRADED")
N = sorted([(fnum(r["r_kpc"]), fnum(r["Menc_Msun"]) / 1e11) for r in rows("fig13/extrapolated-nfw-menc.csv")])
def nfw(r):
    if r < N[0][0] or r > N[-1][0]: return float("nan")
    return float(np.exp(np.interp(math.log(r), [math.log(a) for a, _ in N], [math.log(m) for _, m in N])))
say(f"  the paper's NFW extrapolation (file range {N[0][0]:.0f} to {N[-1][0]:.0f} kpc): {nfw(100):.2f} at 100, {nfw(150):.2f} at 150, {nfw(200):.2f} at 200 kpc")
RES["nfw"] = {}
for c, rws in CLS.items():
    use = [r for r in rws if nfw(r["r"]) == nfw(r["r"])]
    if len(use) >= 3:
        g = grade(use, nfw); RES["nfw"][c] = dict(zmed=g["zmed"], label=g["label"], n=g["n"])
        say(f"     class {c}: n = {g['n']} (of {len(rws)}), z_med = {g['zmed']:+.2f}, range [{min(g['z']):+.2f}, {max(g['z']):+.2f}] -> {g['label']}")
    else:
        say(f"     class {c}: fewer than three rows inside the file's range")
say("\n  field window: e_N in [0, 0.05] for which a class passes (step 0.0005); record 0.01273; rotation curve [0, 0.008]")
EG = [round(0.0005 * i, 4) for i in range(0, 101)]
def window(flags):
    out, start = [], None
    for e, ok in zip(EG, flags):
        if ok and start is None: start = e
        if (not ok) and start is not None: out.append((start, prev)); start = None
        prev = e
    if start is not None: out.append((start, EG[-1]))
    return ", ".join(f"[{a:.4f}, {b:.4f}]" for a, b in out) if out else "empty"
RES["window"] = {}
for f in A0:
    fl = {c: [abs(grade(rws, line_fn(f, e))["zmed"]) <= 2 for e in EG] if POWER[c] else [False] * len(EG) for c, rws in CLS.items()}
    both = [a and b for a, b in zip(fl["H"], fl["S"])]
    RES["window"][f] = dict(H=window(fl["H"]), S=window(fl["S"]), both=window(both))
    say(f"     {f:9s}: H passes for {window(fl['H'])};  S passes for {window(fl['S'])};  both for {window(both)}")
say("\n  baryon amplitude A that centres a class under E1 (z_med = 0):")
RES["A_centre"] = {}
for f in A0:
    parts = []
    for c, rws in CLS.items():
        if not POWER[c]: continue
        lo_, hi_ = 0.3, 8.0
        for _ in range(60):
            mid = 0.5 * (lo_ + hi_)
            if grade(rws, line_fn(f, E_N, 1.0, mid))["zmed"] < 0: lo_ = mid
            else: hi_ = mid
        parts.append(f"class {c}: A = {0.5*(lo_+hi_):.2f}"); RES["A_centre"][f"{f}_{c}"] = 0.5 * (lo_ + hi_)
    say(f"     {f:9s}: " + "; ".join(parts))
say("\n  matched-field value of today's correction lane (4.94 / 4.95 e11 at 200 kpc) against rows at r >= 150 kpc:")
for f, v in (("canonical", 4.939944), ("alt", 4.954813)):
    for c, rws in CLS.items():
        far = [r for r in rws if r["r"] >= 150.0]
        if far:
            g = grade(far, lambda r: v)
            say(f"     {f:9s} class {c}: n = {g['n']}, pulls " + ", ".join(f"{z:+.2f}" for z in g["z"]) + f"; median {g['zmed']:+.2f}")
say("\n  row 32's kill as first registered (a measured M(<200 kpc) >= 1.0e12), on the rows at r >= 150 kpc:")
RES["row32"] = []
for c, rws in CLS.items():
    for r in rws:
        if r["r"] >= 150.0:
            cen = r["M"] >= 10.0; two = (r["M"] - 2 * r["lo"]) >= 10.0
            RES["row32"].append(dict(cls=c, r=r["r"], M=r["M"], lo=r["lo"], central=cen, two_sigma=two))
            say(f"     class {c} r = {r['r']:.0f} kpc: {r['M']:.2f} (-{r['lo']:.2f}) e11  ->  central value {'>= 1.0e12' if cen else '< 1.0e12'};  "
                f"at two published sigma {'>= 1.0e12' if two else 'not >= 1.0e12'}")

sec("LABELS")
for rd, f, e in CASES:
    k = f"{rd}_{f}"; say(f"  {rd} {f:9s}: {RES[k]['case_label']}   ->  {RES[k]['headline']}")
json.dump(dict(lane="PLT1", criteria="e51543aa5e", date="2026-11-12", zip_md5=md5, floor=FLOOR,
               rows={c: rws for c, rws in CLS.items()}, excluded=dict(H=Hbad, S=Sbad), cases=RES),
          open(os.path.join(HERE, "plt1_results.json"), "w"), indent=1)
say("\nPLT1 COMPLETE. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
