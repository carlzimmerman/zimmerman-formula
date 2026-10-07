#!/usr/bin/env python3
"""CFG470 -- a second radiatively efficient hole (1.1-2e9 Msun) to pair with PG 1426+015 against the light end
(2.01-4.35e-20 eV), plus the PG 1426+015 feasibility exclusion grid.
Frozen: FROZEN_CRITERIA.md (0b70d2b38). Executes CFG367's committed cfg367_superradiance.py from its bytes (sha256 checked)
with __file__ pointed at runs/<tag>/ (CFG394/CFG444 wrapper method); the decider mask is CFG444's dmask, re-stated
verbatim (CFG444 is a script that rewrites its own outputs when run, so it is read, not executed).
Inputs (data/): mr22_t5_halpha.tsv, mr22_t6_hbeta.tsv (Mejia-Restrepo+22, J/ApJS/261/5), koss22_t9_general.tsv
(Koss+22, J/ApJS/261/2), oh18_bat105.tsv (Oh+18, J/ApJS/235/4), agnmass_db_index.html (AGN BH Mass Database);
read-only: CFG444 data/vdb16_t3.tsv and CFG444/CFG394 results JSON.
CFG470_MUTATE=1: every spin floor set to 0 -> all fractions must vanish; detected -> exit 1, not detected -> exit 2."""
import os, csv, json, math, hashlib, contextlib, io, re, html
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
SRC = os.path.join(HERE, "..", "CFG367_superradiance_window")
C444 = os.path.join(HERE, "..", "CFG444_light_end_gravity_mass")
MUT = os.environ.get("CFG470_MUTATE", "0") == "1"
SLUG = "cfg470_second_hole" + ("_MUTATE" if MUT else "")
CODE_SHA = "d78a38121a865094d8d333108533bd67e378f6c7aabc0ad6edcf74ae8bb0237e"
CSV_SHA = "6b3b1c496c4194b7bbe453baf07ab87287c6499608b65b5c6dd5c91f5d41d963"
LIGHT = (2.012653280876046e-20, 4.3452552089909754e-20)
LEDD = 1.26e38; KBOL_BAT = 8.0; MPC = 3.0857e24
KLINES = {"Bry": 2.1661, "Paa": 1.8756}           # um, rest (as CFG444)
KBAND = (2.00, 2.45)
SIG_VIR = 0.30; NPT = 21; E_DEF = 0.10
LOG, CH, OUT = [], [], {"lane": "CFG470", "frozen": "0b70d2b38", "mutate": MUT, "light_end": LIGHT}


def P(s=""):
    print(s); LOG.append(s)


def check(n, ok, v=""):
    CH.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {n} {v}")


def spin(a):
    return 0.0 if MUT else a


# ---------------- K0 + CFG367 namespace (control run on CFG367's own CSV)
code = open(os.path.join(SRC, "cfg367_superradiance.py"), "rb").read()
check("K0 CFG367 code sha256 identical", hashlib.sha256(code).hexdigest() == CODE_SHA)
if hashlib.sha256(code).hexdigest() != CODE_SHA:
    raise SystemExit("code hash mismatch: stop (frozen rule)")
cb = open(os.path.join(SRC, "bh_spins_reynolds2021.csv"), "rb").read()
check("K0b CFG367 CSV sha256 identical", hashlib.sha256(cb).hexdigest() == CSV_SHA)
d = os.path.join(HERE, "runs", "CONTROL_CFG367"); os.makedirs(d, exist_ok=True)
open(os.path.join(d, "bh_spins_reynolds2021.csv"), "wb").write(cb)
os.environ["CFG367_MUTATE"] = "0"
NS = {"__file__": os.path.join(d, "cfg367_superradiance.py"), "__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    try:
        exec(compile(code, NS["__file__"], "exec"), NS); rc = 0
    except SystemExit as e:
        rc = e.code
ref = json.load(open(os.path.join(SRC, "cfg367_superradiance_results.json")))
ctl = json.load(open(os.path.join(d, "cfg367_superradiance_results.json")))
check("K0c control run reproduces CFG367's committed intervals; internal checks pass", rc == 0 and all(ctl[k] == ref[k] for k in ("smbh", "xrb", "primary", "per_object")), f"exit {rc}")

# ---------------- decider (CFG444 dmask, verbatim logic)
mg = np.logspace(math.log10(LIGHT[0]), math.log10(LIGHT[1]), 200)
_cache = {}


def mrow(M, e):
    M6 = M / 1e6
    return dict(set="smbh", mass_1e6=f"{M6:.6g}", err_lo=f"{e * M6:.6g}", err_hi=f"{e * M6:.6g}", approx="0")


def dmask_row(r, a):
    lo, hi = NS["mass_range"](r); Ms = np.logspace(math.log10(lo), math.log10(hi), 9)
    return np.array([all(NS["excluded"](m, M, a, NS["TAU"]["smbh"]) for M in Ms) for m in mg])


def mask(M, e, a):
    a = spin(a); k = (f"{M:.6g}", e, a)
    if k not in _cache:
        _cache[k] = dmask_row(mrow(M, e), a)
    return _cache[k]


f1 = lambda M, e, a: float(mask(M, e, a).mean())
f2 = lambda M1, M2, e1, e2, a: float((mask(M1, e1, a) | mask(M2, e2, a)).mean())

# ---------------- K1/K2: CFG444 reproductions
r444 = json.load(open(os.path.join(C444, "cfg444_light_end_gravity_results.json")))
rb = [s for k, s in r444["decider"].items() if k.startswith("ROUTE B")][0]
pg = [t for t in rb if t["name"] == "PG1426+015"][0]
M_PG = float(pg["M"])
P(f"PG 1426+015 (CFG444 route B): M = {M_PG:.4e}; CFG444 frac a>=0.9/0.98 = {pg['frac']['0.9']:.6f}/{pg['frac']['0.98']:.6f}")
# CFG444's row(c, err=0.10) formats mass_1e6 with %.6g of M/1e6 and err = 0.10 * M6 -> identical to mrow
k90, k98 = f1(M_PG, 0.10, 0.9), f1(M_PG, 0.10, 0.98)
if not MUT:
    check("K1 reproduce CFG444 PG 1426+015 a>=0.9 (0.34)", abs(k90 - pg["frac"]["0.9"]) < 1e-12, f"{k90:.6f}")
    check("K1 reproduce CFG444 PG 1426+015 a>=0.98 (0.56)", abs(k98 - pg["frac"]["0.98"]) < 1e-12, f"{k98:.6f}")
    q = [t for t in rb if t["name"] == "Q2237+305"][0]
    pr = [p for p in r444["pairs_top"] if {p["a"].split(" [")[0], p["b"].split(" [")[0]} == {"PG1426+015", "Q2237+305"} and p["a_lo"] == 0.98][0]
    k2 = f2(M_PG, float(q["M"]), 0.10, 0.10, 0.98)
    check("K2 reproduce CFG444 pair PG 1426+015 + Q2237+305 a>=0.98 (0.87)", abs(k2 - pr["frac"]) < 1e-12, f"{k2:.6f} vs {pr['frac']:.6f}")
OUT["PG1426"] = dict(M=M_PG, f90=k90, f98=k98)


# ---------------- tables
def vtab(fn):
    L = [l.rstrip("\n") for l in open(os.path.join(D, fn)) if not l.startswith("#") and l.strip()]
    hh = [x.strip() for x in L[0].split("\t")]
    return [dict(zip(hh, [x.strip() for x in l.split("\t")])) for l in L[3:]]


def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return None


ha = {}
for r in vtab("mr22_t5_halpha.tsv"):
    i = int(r["ID"]); m = fl(r["logMbh(bHa)"])
    if m is None: continue
    q_ = fl(r["fQ(Ha)"]) or 9
    if i not in ha or q_ < ha[i]["q"]:
        ha[i] = dict(logM=m, q=q_, z=fl(r["z-corr(SII)"]) or fl(r["z-ref"]), type=r["DR2Type"], fwhm=fl(r["FWHM(bHa)"]))
hb = {}
for r in vtab("mr22_t6_hbeta.tsv"):
    m = fl(r["logMbh(bHb)"])
    if m is not None: hb.setdefault(int(r["ID"]), m)
ko = {int(r["ID"]): r for r in vtab("koss22_t9_general.tsv") if r["m_ID"] in ("", "A")}
oh = {int(r["Seq"]): r for r in vtab("oh18_bat105.tsv")}
P(f"\nTABLES: MR22 Halpha masses {len(ha)}, Hbeta {len(hb)}; Koss22 table9 {len(ko)}; Oh18 BAT105 {len(oh)}")
BROAD = ("Sy1", "Sy1.2", "Sy1.4", "Sy1.5", "Sy1.8", "Sy1.9")

cands, near, audit = [], [], {"S1": 0, "S2": 0, "S3": 0, "S4": 0, "S5": 0, "S6": 0}
for i in sorted(set(ha) | set(ko)):
    k, h, o = ko.get(i), ha.get(i), oh.get(i)
    if h is not None:
        logM, meth = h["logM"], "MR22 broad Halpha"
    elif k is not None and fl(k["logMBH"]) is not None:
        logM, meth = fl(k["logMBH"]), "Koss22 best (" + k["Method"] + ")"
    else:
        continue
    M = 10**logM
    name = (k["CName"] if k else (o["CName"] if o else str(i))) or str(i)
    z = fl(k["z"]) if k and fl(k["z"]) is not None else (h["z"] if h else (fl(o["z"]) if o else None))
    dec = fl(k["DEJ2000"]) if k else (fl(o["DECdeg"]) if o else None)
    typ = (k["Type"] if k else "") or (h["type"] if h else "") or (o["Type"] if o else "")
    lam, lam_src = None, None
    if k and fl(k["logEdd"]) is not None and meth.startswith("Koss"):
        lam, lam_src = 10**fl(k["logEdd"]), "Koss22 logEdd"
    elif k and fl(k["logLbol"]) is not None:
        lam, lam_src = 10**fl(k["logLbol"]) / (LEDD * M), "Koss22 logLbol / L_Edd(M used)"
    elif o and fl(o["logL"]) is not None:
        lam, lam_src = KBOL_BAT * 10**fl(o["logL"]) / (LEDD * M), "8 x L(14-195) (CFG444 estimator)"
    bat = fl(o["Flux"]) * 1e-12 if o and fl(o["Flux"]) is not None else None
    lines = [n for n, l in KLINES.items() if z is not None and KBAND[0] <= l * (1 + z) <= KBAND[1]]
    rec = dict(id=i, name=name, logM=logM, M=M, method=meth, logM_Hb=hb.get(i), logM_koss=fl(k["logMBH"]) if k else None, koss_method=k["Method"] if k else None,
               z=z, dec=dec, type=typ, lam=lam, lam_src=lam_src, bat_flux=bat, klines=lines,
               telluric_flag=bool(z is not None and "Paa" in lines and 1.8756 * (1 + z) < 2.06 and "Bry" not in lines))
    s = [1.1e9 <= M <= 2.0e9, z is not None and 0 < z <= 0.31, bool(lines), dec is not None and dec <= 30,
         lam is not None and lam >= 0.01, h is not None or typ in BROAD]
    rec["cuts"] = s
    for j, ok in enumerate(s):
        if ok: audit[f"S{j + 1}"] += 1
    if all(s):
        cands.append(rec)
    elif all(s[1:]) and (0.8e9 <= M < 1.1e9 or 2.0e9 < M <= 3.0e9):
        near.append(rec)
P(f"  objects passing each cut alone: {audit}")

# reverberation compilations (S1-S4 only: no lambda/BAT needed to show they are absent)
rm = []
t = open(os.path.join(D, "agnmass_db_index.html")).read()
for r in re.findall(r"<tr.*?</tr>", t, re.S):
    c = [html.unescape(re.sub("<.*?>", "", x)).strip() for x in re.findall(r"<t[dh].*?</t[dh]>", r, re.S)]
    if len(c) == 7 and re.match(r"^\d", c[2]) and re.match(r"^[+\-\u2212]?\d+:\d+", c[4]):
        lm = float(c[2].split()[0]); dg = c[4].replace("−", "-"); dd = float(dg.split(":")[0])
        dd = (abs(dd) + float(dg.split(":")[1]) / 60) * (-1 if dg.startswith("-") else 1)
        rm.append(dict(name=c[1], logM=lm, z=float(c[5]), dec=dd, src="AGN BH Mass Database"))
for r in vtab(os.path.join("..", "..", "CFG444_light_end_gravity_mass", "data", "vdb16_t3.tsv")):
    if r.get("Meth") == "reverb" and fl(r["logBHMass"]) is not None:
        rm.append(dict(name=r["Name"], logM=fl(r["logBHMass"]), z=None, dec=fl(r.get("_DE")), src="vdB16 table3"))
rm_sel = [x for x in rm if 1.1e9 <= 10**x["logM"] <= 2.0e9 and (x["z"] is None or x["z"] <= 0.31) and (x["dec"] is None or x["dec"] <= 30)]
P(f"  RM compilations: {len(rm)} rows ({sum(x['src'].startswith('AGN') for x in rm)} AGN BH Mass DB, {sum(x['src'].startswith('vdB') for x in rm)} vdB16 reverb); "
  f"in 1.1-2e9 with z<=0.31, dec<=+30: {[(x['name'], x['logM'], x['src']) for x in rm_sel] or 'none'}")
OUT["rm_selected"] = rm_sel

# ---------------- ranking (frozen metric)
xs = np.linspace(-2.5, 2.5, NPT); w = np.exp(-0.5 * xs**2); w /= w.sum()
for c in cands + near:
    Ms = 10**(c["logM"] + SIG_VIR * xs)
    p98 = np.array([f2(M_PG, M, E_DEF, E_DEF, 0.98) for M in Ms])
    c["E98"] = float((w * p98).sum())
    c["E90"] = float((w * np.array([f2(M_PG, M, E_DEF, E_DEF, 0.9) for M in Ms])).sum())
    c["Pclose"] = float(w[p98 >= 0.99].sum())
    c["C98"], c["C90"] = f2(M_PG, c["M"], E_DEF, E_DEF, 0.98), f2(M_PG, c["M"], E_DEF, E_DEF, 0.9)
    c["single98"], c["single90"] = f1(c["M"], E_DEF, 0.98), f1(c["M"], E_DEF, 0.9)
    m98 = mask(c["M"], E_DEF, 0.98) | mask(M_PG, E_DEF, 0.98)
    c["unexcluded98"] = [float(mg[0]), float(mg[~m98][-1])] if (~m98).any() else None


def key(c):
    return (-round(c["E98"] / 0.005), -c["E90"], -(c["bat_flux"] or 0))


cands.sort(key=key); near.sort(key=lambda c: -c["E98"])


def show(i, c):
    P(f"  {i:2d}. {c['name']:22s} BAT{c['id']:<5d} logM {c['logM']:.2f} [{c['method']}; Hb {c['logM_Hb']}; Koss {c['logM_koss']} {c['koss_method']}] z {c['z']:.4f} "
      f"dec {c['dec']:+.1f} {c['type']} lam {c['lam']:.3f} ({c['lam_src']}) BAT {c['bat_flux']:.2e} K:{c['klines']}{' TELLURIC-Paa' if c['telluric_flag'] else ''} | "
      f"E98 {c['E98']:.3f} E90 {c['E90']:.3f} P(close) {c['Pclose']:.3f} | C98 {c['C98']:.3f} C90 {c['C90']:.3f} | single98 {c['single98']:.3f} single90 {c['single90']:.3f}"
      + (f" | unexcluded at a>=0.98 up to {c['unexcluded98'][1]:.2e}" if c["unexcluded98"] else " | CLOSES at catalogue mass"))


P(f"\nRANKED CANDIDATES (S1-S6 pass): {len(cands)}  [pair with PG 1426+015, both +/-{E_DEF:.0%}; E = average over true mass, sigma {SIG_VIR} dex]")
for i, c in enumerate(cands, 1): show(i, c)
P(f"\nNEAR MISSES (fail S1 only; 0.8-1.1e9 or 2-3e9): {len(near)}")
for i, c in enumerate(near, 1): show(i, c)

best = cands[0] if cands else None
bC98 = max((c["C98"] for c in cands), default=0.0)
VERD = "CANDIDATE FOUND" if bC98 >= 0.99 else ("PARTIAL" if bC98 >= 0.80 else "NONE")
P(f"\nPART A VERDICT: {VERD} (best C98 {bC98:.3f}; top-ranked {best['name'] if best else 'none'} E98 {best['E98'] if best else 0:.3f})")

# ---------------- part B grid (frozen)
EG, AG = (0.05, 0.10, 0.15, 0.20, 0.30), (0.7, 0.9, 0.95, 0.98)
grid = {"PG1426_single": {f"{e}": {f"{a}": f1(M_PG, e, a) for a in AG} for e in EG}}
P("\nPART B GRID: PG 1426+015 alone, frac of the light end excluded (rows e = 1-sigma fractional mass error; cols spin floor)")
P("   e    " + "  ".join(f"a>={a:<4}" for a in AG))
for e in EG: P(f"  {e:.2f}  " + "  ".join(f"{grid['PG1426_single'][f'{e}'][f'{a}']:.3f}  " for a in AG))
if best:
    grid["pair_best"] = {f"{e}": {f"{a}": f2(M_PG, best["M"], e, e, a) for a in AG} for e in EG}
    grid["best_single"] = {f"{e}": {f"{a}": f1(best["M"], e, a) for a in AG} for e in EG}
    P(f"PART B GRID: PG 1426+015 + {best['name']} (catalogue mass {best['M']:.2e}), both at e:")
    P("   e    " + "  ".join(f"a>={a:<4}" for a in AG))
    for e in EG: P(f"  {e:.2f}  " + "  ".join(f"{grid['pair_best'][f'{e}'][f'{a}']:.3f}  " for a in AG))
    P(f"PART B GRID: {best['name']} alone:")
    for e in EG: P(f"  {e:.2f}  " + "  ".join(f"{grid['best_single'][f'{e}'][f'{a}']:.3f}  " for a in AG))
OUT.update(verdict_A=VERD, best_C98=bC98, candidates=cands, near_misses=near, grid=grid, cut_audit=audit)


# ---------------- departure D3 (labelled): spin floors set by W25's quoted reflection systematic (Delta a* ~ 0.1)
AX = (0.85, 0.89)
grid_x = {"PG1426_single": {f"{e}": {f"{a}": f1(M_PG, e, a) for a in AX} for e in EG}}
if best: grid_x["pair_best"] = {f"{e}": {f"{a}": f2(M_PG, best["M"], e, e, a) for a in AX} for e in EG}
P("\nDEPARTURE D3 (not frozen): spin floors 0.85 / 0.89 (= a_true 0.95 / 0.998 minus W25's systematic 0.1)")
for g, v in grid_x.items():
    P(f"  {g}: " + "; ".join(f"e={e}: " + "/".join(f"{v[f'{e}'][f'{a}']:.3f}" for a in AX) for e in EG))
OUT["grid_departure_D3"] = grid_x


def r_isco(a):
    z1 = 1 + (1 - a * a)**(1 / 3) * ((1 + a)**(1 / 3) + (1 - a)**(1 / 3)); z2 = math.sqrt(3 * a * a + z1 * z1)
    return 3 + z2 - math.copysign(math.sqrt((3 - z1) * (3 + z1 + 2 * z2)), a)


# ESTIMATE (labelled): W25 hard band (NuSTAR 105 ks + pn 71 ks good) gives only a* >~ -0.15 at 90% (Delta chi2 = 2.71 at
# a*=-0.15 relative to a near-maximal best fit, assumed). If Delta chi2 scales with exposure T and with (Delta r_isco)^2,
# excluding a* < 0.9 at 90% from the hard band alone needs T_factor = [(r(-0.15)-r(0.998)) / (r(0.9)-r(0.998))]^2.
rr = {a: r_isco(a) for a in (-0.15, 0.7, 0.9, 0.998)}
tf = ((rr[-0.15] - rr[0.998]) / (rr[0.9] - rr[0.998]))**2
P(f"\nESTIMATE (labelled; Part B): r_isco(-0.15/0.7/0.9/0.998) = {rr[-0.15]:.2f}/{rr[0.7]:.2f}/{rr[0.9]:.2f}/{rr[0.998]:.2f} r_g; "
  f"hard-band exposure factor to push the 90% edge from -0.15 to 0.9 (true a=0.998): x{tf:.0f} -> NuSTAR ~{tf * 105 / 1000:.1f} Ms, pn ~{tf * 71 / 1000:.1f} Ms good time")
P(f"  robust edge under W25's quoted systematic Delta a* ~ 0.1: a_true 0.95 -> {0.95 - 0.1:.2f}; 0.998 -> {0.998 - 0.1:.3f} (below 0.9 in both)")
OUT["exposure_estimate"] = dict(r_isco=rr, T_factor=tf, nustar_Ms=tf * 0.105, pn_Ms=tf * 0.071, note="ESTIMATE: Delta chi2 ~ T (Delta r_isco)^2; true a=0.998 assumed")

# ---------------- informational (departure D2): 2MASS K and archive X-ray exposures (fetch_aux.py)
import warnings
from astropy.io.votable import parse_single_table
AUXD = os.path.join(D, "aux"); aux = {}
for fn in sorted(os.listdir(AUXD)) if os.path.isdir(AUXD) else []:
    kind, nm = fn.split("_", 1); nm = nm.rsplit(".", 1)[0]; a_ = aux.setdefault(nm, {})
    if kind == "2mass":
        L = [l.split("\t") for l in open(os.path.join(AUXD, fn)) if l.strip() and not l.startswith("#")]
        a_["Kmag"] = fl(L[3][3]) if len(L) > 3 else None
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore"); tb = parse_single_table(os.path.join(AUXD, fn)).to_table()
        col = "exposure_a" if kind == "nustar" else "pn_time"
        a_[kind] = [(str(r[0]), None if np.ma.is_masked(r[col]) else float(r[col]) / 1e3, str(r[-1])) for r in tb]
P("\nINFORMATIONAL (D2): 2MASS K (mag, incl. host) and archive exposures (ks; NuSTAR FPMA; XMM pn; negative = planned, accepted)")
for nm, a_ in aux.items():
    P(f"  {nm:22s} K={a_.get('Kmag')}  NuSTAR {a_.get('nustar')}  XMM {a_.get('xmm')}")
OUT["aux"] = aux

# ---------------- MUTATE
allf = [v for g in list(grid.values()) + list(grid_x.values()) for row_ in g.values() for v in row_.values()] + [c[k] for c in cands + near for k in ("E98", "E90", "C98", "C90")] + [k90, k98]
nz = sum(1 for v in allf if v != 0)
if MUT:
    det = nz == 0
    P(f"\nMUTATE (all spins 0): {len(allf)} fractions, {nz} non-zero -> {'DETECTED (exit 1)' if det else 'NOT DETECTED (exit 2)'}")
else:
    P(f"\n{sum(CH)}/{len(CH)} checks pass")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=str)
if MUT:
    raise SystemExit(1 if nz == 0 else 2)
raise SystemExit(0 if all(CH) else 1)
