#!/usr/bin/env python3
"""X64_oblique_object_keys: does one COMBINED (oblique) object variable separate the classes that must RETAIN cold dark
energy {dwarfs, groups, clusters} from those EXCLUDED from it {L* galaxies and lenses} (X58's pattern)?
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (ea43d24f22, committed alone).

Run:   OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 15 python3 x64_oblique_keys.py            -> .out, _results.json, _classes.csv
       X64_MUTATE=1 ... python3 x64_oblique_keys.py                                           -> *_MUTATE.* (KL, K2 must FAIL; exit 1)
kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Cold dark energy is not matter.
Not "theory closed".
"""
import contextlib, csv, io, itertools, json, math, os, resource, sys, time

import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)
REPO = os.path.dirname(RB)
MUT = os.environ.get("X64_MUTATE", "") == "1"
TAG = "_MUTATE" if MUT else ""
OUTL = []
CHECKS = {}


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(name, ok, value, line=""):
    CHECKS[name] = dict(ok=bool(ok), value=str(value), line=line)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value}" + (f"   (line {line})" if line else ""))


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)


P("X64_oblique_object_keys  " + ("MUTATE (labels MW ultra-faint<->SPARC large, Clusters T3<->KiDS lenses swapped)" if MUT else "normal run"))
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy is not matter; environment variables out (peer X62_environment_keyed_switch); not theory closed")

# =====================================================================================  STEP 0: X19 rebuilt read-only
P("\n=== STEP 0: X19_selector_rank_test executed read-only (truncated before its output writes)")
X19D = os.path.join(RB, "X19_selector_rank_test")
X19SRC = os.path.join(X19D, "x19_selector_rank_test.py")
src = open(X19SRC).read()
cut = src.index('json.dump(clean(OUT), open(os.path.join(HERE, f"x19_selector_rank_test_results{TAG}.json")')
src = src[:cut]
os.environ.pop("X19_MUTATE", None)
NS = {"__file__": X19SRC, "__name__": "x19_ro"}
argv0 = sys.argv; sys.argv = [X19SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, X19SRC, "exec"), NS)
sys.argv = argv0
FOOTS = NS["FOOTS"]; A0 = NS["A0"]; G = NS["G"]; MSUN = NS["MSUN"]; PC = NS["PC"]; KPC = NS["KPC"]; MPC = NS["MPC"]; CL = NS["CL"]
GYR = NS["GYR"]; TH = NS["TH"]; law = NS["law"]; SYS19 = NS["SYS"]; INT19 = NS["INT"]; ETAB = NS["ETAB"]; CLASSES19 = NS["CLASSES"]
VN19 = NS["VN"]; VREP19 = NS["VREP"]; RES19 = NS["RESULTS"]; VERD19 = NS["VERDICT"]

# (i) class table vs committed CSV
rows_bad = set(); ncell = 0
for r in csv.DictReader(open(os.path.join(X19D, "x19_classes.csv"))):
    f, nm = r["footing"], r["class"]
    T = ETAB[(f, "iso")][nm]; L = RES19["labels"][f][nm]
    for key, val in (("E_iso", T["E"]), ("s_iso", T["s"]), ("Z_iso", T["Z"])):
        ncell += 1
        if not (float(r[key]) == val or abs(float(r[key]) - val) <= 1e-9 * max(1.0, abs(val))):
            rows_bad.add((f, nm))
    if r["label_LS"] != L:
        rows_bad.add((f, nm))
    for v in VN19 + VREP19:
        iv = INT19[(f, False)][nm][v]
        for j, suf in enumerate(("p16", "p84", "med")):
            ref = r[f"{v}_{suf}"]
            ncell += 1
            if iv is None:
                if ref not in ("", "nan", "None", "NA"):
                    rows_bad.add((f, nm))
                continue
            refv = float(ref) if ref not in ("", "None") else float("nan")
            if not (abs(refv - iv[j]) <= 1e-9 * max(1e-300, abs(iv[j])) or (math.isnan(refv) and math.isnan(iv[j]))):
                rows_bad.add((f, nm))
        if iv is not None and r[f"{v}_N"] not in ("", "None", "NA") and int(float(r[f"{v}_N"])) != iv[3]:
            rows_bad.add((f, nm))
J19 = json.load(open(os.path.join(X19D, "x19_selector_rank_test_results.json")))
st_ok = all(RES19["single"][f][v]["status"] == J19["results"]["single"][f][v]["status"] for f in FOOTS for v in VN19)
verd_ok = (VERD19 == J19["verdict"])
P(f"  class table: {ncell} cells compared with the committed x19_classes.csv; rows failing: {sorted(rows_bad) if rows_bad else 'none'}")
P(f"  X19 primary verdict rebuilt: '{VERD19}' (committed '{J19['verdict']}'); per-variable statuses equal: {st_ok}")
for f in FOOTS:
    P(f"  [{f}] X19 statuses: " + ", ".join(f"{v} {RES19['single'][f][v]['status']}" for v in VN19))
STOP = (not (st_ok and verd_ok)) or len(rows_bad) > 2
check("K0", (not rows_bad) and st_ok and verd_ok, f"rows failing {len(rows_bad)}; verdict equal {verd_ok}; statuses equal {st_ok}",
      "every cell within 1e-9; verdict NO LOW-DIMENSIONAL SELECTOR")
if STOP:
    P("  STEP-0 STOP RULE FIRES: verdict UNDECIDED")

# =====================================================================================  members: radius, Phi_int, lenses
P("\n=== STEP 1: per-member quantities (X19 members + KiDS lens class)")
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
RE_GROUP = {}
for l in open(TIAN):
    if l.startswith("#"):
        continue
    r = l.rstrip("\n").split("\t")
    if len(r) < 13 or not r[0].strip().isdigit() or r[1].strip() != "Galaxy group":
        continue
    RE_GROUP[r[2].strip()] = float(r[10]) * KPC
PRESS = {"LG field", "MW classical", "MW ultra-faint", "bright M31", "M31 others", "Crater II", "Antlia II", "Coma UDGs", "DF2/DF4"}
CLASSES = [c for c in CLASSES19 if c != "Cosmic background"] + ["KiDS lenses"]
MEM = {f: {c: [] for c in CLASSES} for f in FOOTS}
k1_dev = 0.0; k1_mw = None; k1_cl = 0.0
for f in FOOTS:
    a0 = A0[f]
    for c in CLASSES19:
        if c == "Cosmic background":
            continue
        for row in SYS19[f][c]:
            rho = row["rho_b"] * MSUN / PC ** 3                     # kg/m^3
            if c == "Groups":
                r = RE_GROUP[row["name"]]
            else:
                r = 3 * row["x"] * a0 / (4 * math.pi * G * rho)
            Mr = row["rho_b"] * 4 / 3 * math.pi * (r / PC) ** 3      # Msun (exact round trip by construction for non-groups)
            if c != "Groups":
                k1_dev = max(k1_dev, abs(G * Mr * MSUN / r ** 2 / a0 / row["x"] - 1))
            if c == "MW disc":
                k1_mw = r / KPC
            if c.startswith("Clusters"):
                k1_cl = max(k1_cl, abs(r / (0.548 * MPC) - 1))
            Mb = row["M_b"]
            if c in PRESS:
                phi_int = G * Mb * MSUN / math.sqrt(r ** 2 + (0.75 * r) ** 2) / CL ** 2
            elif c.startswith("Clusters"):
                phi_int = row["Phi"]
            else:
                phi_int = G * Mb * MSUN / r / CL ** 2
            MEM[f][c].append(dict(name=row["name"], r=r, Mr=Mr, Mb=Mb, rho_b=row["rho_b"], sigma=row["sigma"], x=row["x"], phi_int=phi_int,
                                  phi_host=row["Phi"], f_b=row["f_b"]))
check("K1", k1_dev < 1e-9 and abs(k1_mw - 8.122) < 1e-9 * 8.122 and k1_cl < 1e-9,
      f"x round trip max dev {k1_dev:.1e}; MW r {k1_mw:.6f} kpc; clusters max |r/0.548 Mpc - 1| {k1_cl:.1e}", "1e-9; 8.122 kpc; 548 kpc")

# ---- KiDS lens class (A2)
F2J = json.load(open(os.path.join(RB, "F2_outer_lensing", "f2_outer_lensing_results.json")))["inventory"]
H_NAT = 0.679
LENS_R_MPC = (0.035, 0.104, 0.31)
LENS = []
for b in range(4):
    lm70 = F2J[f"bin{b + 1}"]["meanlogMs70"]; lm = lm70 + 2 * math.log10(0.70 / H_NAT)
    Ms = 10 ** lm; Mc = 10 ** (lm + (-0.69 * lm70 + 6.63)); Mh = 0.5 * Ms
    LENS.append(dict(bin=b + 1, lm=lm, Ms=Ms, Mc=Mc, Mh=Mh))
for f in FOOTS:
    a0 = A0[f]
    for L_ in LENS:
        for rm in LENS_R_MPC:
            r = rm * MPC; Rh = 0.1 * MPC
            Mr = L_["Ms"] + L_["Mc"] + L_["Mh"] * min(1.0, (r / Rh) ** 3)
            gN = G * Mr * MSUN / r ** 2; g = float(law(gN, a0)); V = math.sqrt(g * r)
            phi = G * (L_["Ms"] + L_["Mc"]) * MSUN / r + (G * L_["Mh"] * MSUN * (3 * Rh ** 2 - r ** 2) / (2 * Rh ** 3) if r < Rh else G * L_["Mh"] * MSUN / r)
            MEM[f]["KiDS lenses"].append(dict(name=f"bin{L_['bin']}@{rm}", r=r, Mr=Mr, Mb=L_["Ms"] + L_["Mc"] + L_["Mh"], rho_b=Mr / (4 / 3 * math.pi * (r / PC) ** 3),
                                              sigma=V / math.sqrt(2) / 1e3, x=gN / a0, phi_int=phi / CL ** 2, phi_host=phi / CL ** 2, f_b=gN / g,
                                              lMbrel=math.log10(L_["Ms"] + L_["Mc"]), r_mpc=rm))
P("  KiDS lens bins (native h 0.679): lg M* " + " / ".join(f"{L_['lm']:.3f}" for L_ in LENS) + "; lg(M*+M_cold) "
  + " / ".join(f"{math.log10(L_['Ms'] + L_['Mc']):.3f}" for L_ in LENS) + f"; radii {LENS_R_MPC} Mpc")

# =====================================================================================  EPS machinery (EM1 background A, read-only)
EM1SRC = os.path.join(RB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
seg = TE[TE.index("# ---------------- backgrounds: CLASS"):TE.index("okc = all(")]
seg = seg.replace('for tag in ("A_c2b_refit", "B_cfg886_bg"):', 'for tag in ("A_c2b_refit",):')
from classy import Class  # noqa: E402
NE = dict(os=os, json=json, math=math, np=np, Class=Class, HERE=os.path.join(RB, "EM1_emergent_dust_law"), G=6.67430e-11, MPC=3.0857e22,
          LM=np.round(np.arange(8.0, 14.0001, 0.02), 2))
if not hasattr(np, "trapz"):
    np.trapz = np.trapezoid
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(seg, EM1SRC, "exec"), NE)
bgA = NE["BGS"]["A_c2b_refit"]; cc = bgA["c"]; hA = bgA["h"]; sigf = bgA["cB"].__defaults__[1]
RHOM0 = float(cc.Omega_m()) * 2.775e11 * hA ** 2
ZG = np.linspace(0, 30, 3001); DG = np.array([cc.scale_independent_growth_factor(z) for z in ZG]); DG /= DG[0]
LMG = np.linspace(7.0, 16.5, 191); S2G = np.array([float(sigf(10 ** l)[0]) ** 2 for l in LMG])
DC, OMEGA = 1.686, 0.974
BGT = cc.get_background(); TZ = np.array(BGT["z"]); TT = np.array(BGT["proper time [Gyr]"])
order = np.argsort(TZ); TZ, TT = TZ[order], TT[order]
T_NOW = float(np.interp(0.0, TZ, TT))


def s2(lm):
    return np.interp(lm, LMG, S2G)


def D(z):
    return np.interp(z, ZG, DG)


def zform(lm, zobs=0.0):
    if lm < LMG[0] + math.log10(2) or lm > LMG[-1]:
        return float("nan")
    S = math.sqrt(max(float(s2(lm - math.log10(2)) - s2(lm)), 0.0))
    Df = DC / (DC / float(D(zobs)) + OMEGA * S)
    return float(np.interp(-Df, -DG, ZG))


def t_of_z(z):
    return float(np.interp(z, TZ, TT))


EM1J = json.load(open(os.path.join(RB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]
aR, bR = EM1J["a"], EM1J["b"]
X51J = json.load(open(os.path.join(RB, "X51_dwarf_cooling_floor", "x51_dwarfs_results.json")))["footings"]
zf12 = zform(12.0)
lens_m200 = [aR + bR * (math.log10(L_["Ms"] + L_["Mc"]) - 10) for L_ in LENS]
X53REF = (11.35, 11.72, 11.90, 12.05)
check("K4", max(abs(a - b) for a, b in zip(lens_m200, X53REF)) <= 0.10 and abs(zf12 - 0.944) <= 0.01,
      f"lens lgM200 (EM1 R1 on M*+M_cold) {' / '.join(f'{v:.2f}' for v in lens_m200)} vs X53 {X53REF}; z_f(1e12) {zf12:.3f} (X59 0.944); t0 {T_NOW:.3f} Gyr",
      "<= 0.10 dex; 0.944 +- 0.01")
DWARFS = {"LG field", "MW classical", "MW ultra-faint", "bright M31", "M31 others", "Crater II", "Antlia II"}


def m200_of(f, c, m, variant):
    if c in DWARFS and variant == "x51":
        return math.log10(X51J[f]["classes"]["MW ultra-faint"]["M200"])
    if c == "KiDS lenses":
        return aR + bR * (m["lMbrel"] - 10)
    return aR + bR * (math.log10(m["Mb"]) - 10)


# =====================================================================================  candidates
NU1 = (1 + math.sqrt(5)) / 2
SIGA0 = {f: A0[f] / (2 * math.pi * G) for f in FOOTS}                 # kg/m^2
CAND = ["Q_b", "Q_dyn", "vir", "tcross", "trelax", "fbSigma_law", "dynage", "vesc_vc"]
CAND_REP = ["fbSigma"]
CDESC = {"Q_b": "C1 rho_b/sigma^3 [Msun pc^-3 (km/s)^-3]", "Q_dyn": "C1d 9/(4 pi G r^2 sigma) [Msun pc^-3 (km/s)^-3]", "vir": "C2 sigma^2/|Phi_int|",
         "tcross": "C3a t_cross/t_H", "trelax": "C3b t_relax/t_H (m 0.5 Msun)", "fbSigma_law": "C4L (1/nu(x)) Sigma_b/Sigma_a0 (= f(x))",
         "dynage": "C5 [t0 - t(z_f)]/t_cross", "vesc_vc": "C6 v_esc/v_c at r_a0", "fbSigma": "C4 f_b Sigma_b/Sigma_a0 (REPORTED ONLY)"}
KEYTYPE = {"Q_b": "K1", "Q_dyn": "K1", "vir": "K3", "tcross": "K2", "trelax": "K1", "fbSigma_law": "K3", "dynage": "K2", "vesc_vc": "K3", "fbSigma": "K3"}


def nu(y):
    return 0.5 + math.sqrt(0.25 + 1.0 / y)


def cand_values(f, c, m, phi="int", m200v="x51"):
    a0 = A0[f]; s = m["sigma"]
    out = {k: float("nan") for k in CAND + CAND_REP}
    r = m["r"]; Mr = m["Mr"]; Mb = m["Mb"]
    Sig = Mr * MSUN / (math.pi * r ** 2)
    out["fbSigma_law"] = (1.0 / nu(m["x"])) * Sig / SIGA0[f]
    out["fbSigma"] = m["f_b"] * Sig / SIGA0[f] if math.isfinite(m["f_b"]) else float("nan")
    ph = m["phi_int"] if phi == "int" else m["phi_host"]
    ra0 = math.sqrt(G * Mb * MSUN / a0)
    out["vesc_vc"] = math.sqrt(2 * ph * CL ** 2 / (NU1 * a0 * ra0))
    if not (math.isfinite(s) and s > 0):
        return out
    sm = s * 1e3
    out["Q_b"] = m["rho_b"] / s ** 3
    rho_dyn = 9 * sm ** 2 / (4 * math.pi * G * r ** 2) / MSUN * PC ** 3
    out["Q_dyn"] = rho_dyn / s ** 3
    out["vir"] = (sm / CL) ** 2 / ph
    tc = r / sm / GYR
    out["tcross"] = tc / TH
    N = Mb / 0.5
    out["trelax"] = N / (8 * math.log(N)) * tc / TH
    lm2 = m200_of(f, c, m, m200v)
    zf = zform(lm2)
    out["dynage"] = (T_NOW - t_of_z(zf)) / tc if math.isfinite(zf) else float("nan")
    return out


def interval(vals, strict=False):
    v = np.array([u for u in vals if math.isfinite(u) and u > 0], float)
    if v.size == 0:
        return None
    lv = np.log10(v)
    if strict or v.size < 3:
        return (float(lv.min()), float(lv.max()), float(np.median(lv)), int(v.size))
    return (float(np.percentile(lv, 16)), float(np.percentile(lv, 84)), float(np.median(lv)), int(v.size))


def build_int(f, strict=False, phi="int", m200v="x51", lens_single=False):
    I = {}
    for c in CLASSES:
        mem = MEM[f][c]
        if c == "KiDS lenses" and lens_single:
            mem = [m for m in mem if m["r_mpc"] == 0.104]
        vals = [cand_values(f, c, m, phi, m200v) for m in mem]
        I[c] = {k: interval([v[k] for v in vals], strict) for k in CAND + CAND_REP}
    return I


# =====================================================================================  labels
RET_P = ["MW ultra-faint", "bright M31", "M31 others", "Groups", "Clusters T1", "Clusters T2", "Clusters T3"]
EXC_P = ["KiDS lenses", "SPARC large", "MW disc"]
FROZEN = {"P": (RET_P, EXC_P),
          "G": ([c for c in RET_P if c not in ("Groups", "Clusters T1")], EXC_P),
          "W": (RET_P + ["MW classical"], EXC_P + ["UMa members", "TDGs", "DF2/DF4", "Crater II"])}


def labels_of(scheme):
    ret, exc = FROZEN[scheme]
    L = {c: ("RETAIN" if c in ret else "EXCLUDED" if c in exc else "-") for c in CLASSES}
    if MUT:
        for a, b in (("MW ultra-faint", "SPARC large"), ("Clusters T3", "KiDS lenses")):
            L[a], L[b] = L[b], L[a]
    return L


# =====================================================================================  separation rule
def separate(X, L):
    """X: class -> (lo, hi, med, N) in log10 or None. Returns dict."""
    dec = [c for c in X if L.get(c) in ("RETAIN", "EXCLUDED")]
    na = [c for c in dec if X[c] is None]
    use = [c for c in dec if X[c] is not None]
    R = [c for c in use if L[c] == "RETAIN"]; E = [c for c in use if L[c] == "EXCLUDED"]
    res = dict(not_placeable=na, n_retain=len(R), n_excl=len(E))
    if not R or not E:
        res.update(status="NO CONTRAST", separates=False); return res
    edges = sorted({X[c][0] for c in use} | {X[c][1] for c in use})
    cands = [edges[0] - 1] + [0.5 * (a + b) for a, b in zip(edges[:-1], edges[1:])] + [edges[-1] + 1]
    best = None
    for d in ("UP", "DOWN"):
        for t in cands:
            if d == "UP":
                off = [c for c in E if X[c][1] >= t] + [c for c in R if X[c][0] <= t]
            else:
                off = [c for c in R if X[c][1] >= t] + [c for c in E if X[c][0] <= t]
            if best is None or len(off) < len(best[2]):
                best = (d, t, off)
    gU = max(X[c][1] for c in E) < min(X[c][0] for c in R)
    gD = max(X[c][1] for c in R) < min(X[c][0] for c in E)
    res.update(best_direction=best[0], best_threshold_log=best[1], offenders=best[2])
    if gU or gD:
        lo = max(X[c][1] for c in E) if gU else max(X[c][1] for c in R)
        hi = min(X[c][0] for c in R) if gU else min(X[c][0] for c in E)
        res.update(status="SEPARATES" + (" (INCOMPLETE)" if na else ""), separates=True, direction="UP" if gU else "DOWN",
                   vstar_log=0.5 * (lo + hi), margin_dex=hi - lo, gap_log=(lo, hi), complete=not na)
    else:
        # overlap depth (dex) between the two groups at the best direction, for reporting
        if best[0] == "UP":
            ov = max(X[c][1] for c in E) - min(X[c][0] for c in R)
        else:
            ov = max(X[c][1] for c in R) - min(X[c][0] for c in E)
        res.update(status="FAILS" + (" (INCOMPLETE)" if na else ""), separates=False, overlap_dex=ov, complete=not na)
    return res


def enum_p(I, L, keys):
    dec = [c for c in CLASSES if L.get(c) in ("RETAIN", "EXCLUDED")]
    nE = sum(1 for c in dec if L[c] == "EXCLUDED")
    n_any = 0; n_k = {k: 0 for k in keys}; tot = 0
    for comb in itertools.combinations(dec, nE):
        LL = {c: ("EXCLUDED" if c in comb else "RETAIN") for c in dec}
        tot += 1; hit = False
        for k in keys:
            if separate({c: I[c][k] for c in CLASSES}, LL)["separates"]:
                n_k[k] += 1; hit = True
        n_any += hit
    return {k: n_k[k] / tot for k in keys}, n_any / tot, tot


# ---- K3 unit tests
synthX = {"a": (0, 1, .5, 5), "b": (0.2, 0.8, .5, 5), "c": (2, 3, 2.5, 5), "d": (2.5, 3.5, 3, 5)}
r_sep = separate(synthX, {"a": "EXCLUDED", "b": "EXCLUDED", "c": "RETAIN", "d": "RETAIN"})
r_not = separate(synthX, {"a": "EXCLUDED", "b": "RETAIN", "c": "EXCLUDED", "d": "RETAIN"})
CL_SAVE = CLASSES
CLASSES = ["s1", "s2", "s3", "s4", "s5", "s6"]
Ip = {c: {"v": (i, i, i, 1)} for i, c in enumerate(CLASSES)}
pk, pany, ntot = enum_p(Ip, {c: ("EXCLUDED" if i < 2 else "RETAIN") for i, c in enumerate(CLASSES)}, ["v"])
CLASSES = CL_SAVE
check("K3", r_sep["separates"] and r_sep["direction"] == "UP" and abs(r_sep["margin_dex"] - 1.0) < 1e-12 and not r_not["separates"] and abs(pk["v"] - 2 / 15) < 1e-12,
      f"separable {r_sep['status']} margin {r_sep['margin_dex']:.2f}; non-separable {r_not['status']}; perfect-order p {pk['v']:.4f} (2/C(6,2) = {2 / 15:.4f})",
      "SEPARATES 1.00 / FAILS / 0.1333")

# =====================================================================================  run
RESULTS = {}; CLSV = {}
P("\n=== STEP 3: candidates per class (log10 median [16-84 %], N), and the separation test")
for f in FOOTS:
    I = build_int(f)
    CLSV[f] = I
    L = labels_of("P")
    P(f"\n  [{f}] labels used: RETAIN {[c for c in CLASSES if L[c] == 'RETAIN']}; EXCLUDED {[c for c in CLASSES if L[c] == 'EXCLUDED']}")
    P("  " + f"{'class':16s}{'label':9s}" + "".join(f"{k:>24s}" for k in CAND + CAND_REP))
    for c in CLASSES:
        P("  " + f"{c:16s}{L[c]:9s}" + "".join((f"{I[c][k][2]:+7.2f} [{I[c][k][0]:+.2f},{I[c][k][1]:+.2f}]".rjust(24) if I[c][k] else f"{'N/A':>24s}") for k in CAND + CAND_REP))
    RESULTS[f] = {}
    for k in CAND + CAND_REP:
        rr = separate({c: I[c][k] for c in CLASSES}, L)
        RESULTS[f][k] = rr
    pk, pany, ntot = enum_p(I, L, CAND)
    RESULTS[f]["_p"] = dict(p_k=pk, p_any=pany, n_labellings=ntot)
    P(f"\n  [{f}] separation (labelling P, 16-84 %, Phi_int); trials: {ntot} relabellings, p_any (verdict-bearing) = {pany:.4f}")
    for k in CAND + CAND_REP:
        rr = RESULTS[f][k]
        tail = (f" dir {rr['direction']} V* = 10^{rr['vstar_log']:+.3f}, margin {rr['margin_dex']:.3f} dex" if rr["separates"]
                else f" overlap {rr.get('overlap_dex', float('nan')):.3f} dex; best dir {rr.get('best_direction')} offenders {rr.get('offenders')}")
        P(f"    {KEYTYPE[k]} {CDESC[k]:44s} {rr['status']:24s}{tail}" + (f"  p_k {pk[k]:.4f}" if k in pk else "  [REPORTED ONLY]"))

# ---- K2 oracle and KL
k2 = {}
for f in FOOTS:
    ret, exc = FROZEN["P"]
    X = {c: ((1.0, 1.0, 1.0, 1) if c in ret else (0.0, 0.0, 0.0, 1) if c in exc else None) for c in CLASSES}
    k2[f] = separate(X, labels_of("P"))["separates"]
check("K2", all(k2.values()), f"oracle from frozen labels separates: {k2}", "True on both footings")
Lp = labels_of("P")
check("KL", all(Lp[c] == "RETAIN" for c in RET_P) and all(Lp[c] == "EXCLUDED" for c in EXC_P), "labels used equal FROZEN_CRITERIA section 1 (P)", "equal")

# ---- verdict
sep_f = {f: [k for k in CAND if RESULTS[f][k]["separates"] and RESULTS[f][k].get("complete")] for f in FOOTS}
sep_inc = {f: [k for k in CAND if RESULTS[f][k]["separates"] and not RESULTS[f][k].get("complete")] for f in FOOTS}
pany_f = {f: RESULTS[f]["_p"]["p_any"] for f in FOOTS}
if STOP:
    VERDICT = "UNDECIDED (step-0 stop rule)"
elif not any(sep_f[f] or sep_inc[f] for f in FOOTS):
    VERDICT = "NO OBLIQUE KEY"
else:
    common = [k for k in sep_f["canonical"] if k in sep_f["alt"]]
    if common and all(pany_f[f] <= 0.05 for f in FOOTS):
        VERDICT = "OBLIQUE KEY FOUND: " + ", ".join(f"{k} (V* 10^{RESULTS['canonical'][k]['vstar_log']:+.3f} / 10^{RESULTS['alt'][k]['vstar_log']:+.3f})" for k in common)
    elif common:
        VERDICT = f"UNDECIDED (separation at chance level: {common}; p_any {pany_f['canonical']:.3f} / {pany_f['alt']:.3f} > 0.05)"
    elif sep_f["canonical"] or sep_f["alt"]:
        VERDICT = f"UNDECIDED (footings disagree: canonical {sep_f['canonical']}, alt {sep_f['alt']})"
    else:
        VERDICT = f"UNDECIDED (only INCOMPLETE separations: {sep_inc})"
P(f"\n=== VERDICT (primary): {VERDICT}")

# =====================================================================================  qualifiers
P("\n=== QUALIFIERS (reported, no verdict weight)")
QUAL = {}
VAR = {"G": dict(scheme="G"), "W": dict(scheme="W"), "strict": dict(strict=True), "Phi_host": dict(phi="host"),
       "lens_r0.104": dict(lens_single=True), "dwarf_M200_EM1": dict(m200v="em1")}
for tag, opt in VAR.items():
    QUAL[tag] = {}
    for f in FOOTS:
        I = build_int(f, strict=opt.get("strict", False), phi=opt.get("phi", "int"), m200v=opt.get("m200v", "x51"), lens_single=opt.get("lens_single", False))
        L = labels_of(opt.get("scheme", "P"))
        rr = {k: separate({c: I[c][k] for c in CLASSES}, L) for k in CAND + CAND_REP}
        pk, pany, ntot = enum_p(I, L, CAND)
        QUAL[tag][f] = dict(results=rr, p_any=pany, n_labellings=ntot)
        s = [f"{k}{'(INC)' if not rr[k].get('complete') else ''} {rr[k]['margin_dex']:.2f}" for k in CAND + CAND_REP if rr[k]["separates"]]
        P(f"  {tag:15s} [{f:9s}] separating: {s if s else 'none'}; p_any {pany:.4f} ({ntot}); fewest offenders: "
          + "; ".join(f"{k} {len(rr[k].get('offenders', []))}" for k in CAND))

# =====================================================================================  step 4 (only if separation)
STEP4 = {}
if any(RESULTS[f][k]["separates"] for f in FOOTS for k in CAND):
    P("\n=== STEP 4 (reported only): R1 forest and L* progenitors at z 2, 3")
    OMB_A = float(cc.Omega_b()); RHOCR0 = 2.775e11 * hA ** 2 / 1e18           # Msun/pc^3
    KB, MP = 1.380649e-23, 1.67262192e-27
    for f in FOOTS:
        STEP4[f] = {}
        for k in CAND:
            rr = RESULTS[f][k]
            if not rr["separates"]:
                continue
            rows = []
            for z in (2.0, 3.0):
                Hz = cc.Hubble(z) * 299792458.0 / MPC
                for dlt in (0.0, 10.0):
                    for T in (1e4, 2e4):
                        rho = (1 + dlt) * OMB_A * RHOCR0 * (1 + z) ** 3; sm = math.sqrt(KB * T / (0.6 * MP))
                        rhoSI = rho * MSUN / PC ** 3
                        rJ = sm * math.sqrt(math.pi / (G * max(rhoSI / OMB_A * float(cc.Omega_m()), 1e-40)))
                        m = dict(r=rJ, Mr=rho * 4 / 3 * math.pi * (rJ / PC) ** 3, Mb=rho * 4 / 3 * math.pi * (rJ / PC) ** 3, rho_b=rho, sigma=sm / 1e3,
                                 x=G * rho * 4 / 3 * math.pi * (rJ / PC) ** 3 * MSUN / rJ ** 2 / A0[f], phi_int=G * rho * 4 / 3 * math.pi * (rJ / PC) ** 3 * MSUN / rJ / CL ** 2,
                                 phi_host=float("nan"), f_b=float("nan"))
                        v = cand_values(f, "forest", m)[k]
                        rows.append(dict(kind="forest", z=z, delta=dlt, T=T, logV=math.log10(v) if v > 0 and math.isfinite(v) else None))
                for lm0 in (11.35, 12.05):
                    S = math.sqrt(max(float(s2(lm0 - math.log10(2)) - s2(lm0)), 0.0))
                    # EPS main-progenitor median mass at z: S(M_z) - S(M0) = ... use the half-mass rule on the grid: M_z with
                    # delta_c (1/D(z) - 1) = 0.974 sqrt(S(M_z) - S(M0)) (X59's own relation, inverted on the grid)
                    target = (DC * (1 / float(D(z)) - 1) / OMEGA) ** 2 + float(s2(lm0))
                    lmz = float(np.interp(-target, -S2G, LMG))
                    Mz = 10 ** lmz; rho200 = 200 * 3 * Hz ** 2 / (8 * math.pi * G)
                    R200 = (3 * Mz * MSUN / (4 * math.pi * rho200)) ** (1 / 3); V200 = math.sqrt(G * Mz * MSUN / R200)
                    r = 0.015 * R200; fb = 0.157; Mb = fb * Mz
                    m = dict(r=r, Mr=Mb / 2, Mb=Mb, rho_b=(Mb / 2) / (4 / 3 * math.pi * (r / PC) ** 3), sigma=V200 / math.sqrt(2) / 1e3,
                             x=G * (Mb / 2) * MSUN / r ** 2 / A0[f], phi_int=G * Mb * MSUN / r / CL ** 2, phi_host=float("nan"), f_b=float("nan"))
                    m["lMbrel"] = math.log10(Mb)
                    v = cand_values(f, "KiDS lenses", m)[k]
                    rows.append(dict(kind=f"L* progenitor of 10^{lm0}", z=z, lgM200_z=lmz, logV=math.log10(v) if v > 0 and math.isfinite(v) else None))
            side = lambda lv: None if lv is None else ("RETAIN" if ((lv > rr["vstar_log"]) == (rr["direction"] == "UP")) else "EXCLUDED")
            for rw in rows:
                rw["side"] = side(rw["logV"])
            STEP4[f][k] = rows
            P(f"  [{f}] {k}: V* 10^{rr['vstar_log']:+.3f} ({rr['direction']}): " + "; ".join(
                f"{rw['kind']} z{rw['z']:.0f}" + (f" d{rw['delta']:.0f} T{rw['T']:.0e}" if rw["kind"] == "forest" else f" (lgM {rw['lgM200_z']:.2f})")
                + f" {rw['logV'] if rw['logV'] is None else round(rw['logV'], 2)} -> {rw['side']}" for rw in rows))
else:
    P("\n=== STEP 4: not run (no candidate separates on either footing; frozen)")

rss = rss_gb()
check("K5", rss < 1.0, f"{rss:.3f} GB", "< 1 GB")
ok_all = all(c["ok"] for c in CHECKS.values())
P(f"\nchecks {sum(c['ok'] for c in CHECKS.values())}/{len(CHECKS)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
if MUT:
    P(f"MUTATE: KL {'FAILS' if not CHECKS['KL']['ok'] else 'PASSES'} (required FAIL); K2 {'FAILS' if not CHECKS['K2']['ok'] else 'PASSES'} (required FAIL)")


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


OUT = dict(lane="X64_oblique_object_keys", criteria="ea43d24f22", mutate=MUT, verdict=VERDICT, results=RESULTS, qualifiers=QUAL, step4=STEP4,
           class_intervals_log10=CLSV, labels_P=labels_of("P"), lens_bins=LENS, checks=CHECKS, x19_rows_failing=sorted(rows_bad),
           runtime_s=time.time() - T0, peak_rss_GB=rss)
json.dump(clean(OUT), open(os.path.join(HERE, f"x64_oblique_keys_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"x64_oblique_keys{TAG}.out"), "w").write("\n".join(OUTL).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<parent>") + "\n")
with open(os.path.join(HERE, f"x64_classes{TAG}.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["footing", "class", "label_P"] + [f"{k}_{s}" for k in CAND + CAND_REP for s in ("log_p16", "log_p84", "log_med", "N")])
    for f in FOOTS:
        Lp = labels_of("P")
        for c in CLASSES:
            row = [f, c, Lp[c]]
            for k in CAND + CAND_REP:
                iv = CLSV[f][c][k]
                row += list(iv) if iv else ["", "", "", 0]
            w.writerow(row)
if MUT:
    sys.exit(1)
sys.exit(0 if ok_all else 2)
