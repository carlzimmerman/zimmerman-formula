#!/usr/bin/env python3
"""DWF1 (HY4-9): what moves a hosted dwarf UP under form B, without moving the field population.

Criteria: FROZEN_CRITERIA.md, committed alone as 34a3ee01f0 before any number here existed.
    python3 dwf1.py            -> dwf1.out / dwf1.json           (known answers, then the three candidates)
    python3 dwf1.py --mutate   -> dwf1_MUTATE.out / .json        (M1 X1's host-field bug; M2 overstated infall field;
                                                                  M3 the arm that must FAIL: KA2 must break, exit 1)
Code paths COPIED (not imported) from X1 (rebuild_2026_10_22/X1_hosted_recount/x1_hosted_recount.py: constants, LVD
loader, MC build, host fields, pred_draws/lin3) as RB2 copied them (closure_2026_11_09/RB2_form_b_hosted_rows/rb2.py),
and XF1's boot_median (via RB2).  The D10 solver is imported READ-ONLY.  Committed tables and JSON of X1 and RB2 are
read as data.  kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle.
"""
import os, sys, json, math, csv, time, resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
import d10_solver as S                                    # noqa: E402  (read-only)

MUT = "--mutate" in sys.argv
TAG = "dwf1_MUTATE" if MUT else "dwf1"
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)

# ==================================================================== constants copied from X1 (via RB2)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}
NMC, NBOOT = 2000, 4000
DY = 0.6
R12 = 4.0 / 3.0
A_H = 3.0 * KPC
GE2_8KPC = 2.0592e-10
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
X1D = os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount")
RB2D = os.path.join(REPO, "closure_2026_11_09", "RB2_form_b_hosted_rows")

def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
def load_lvd():
    rows = []
    for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
        for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
            s = fl(r.get("vlos_sigma"))
            rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
            ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
            if not s or s <= 0 or not rh or rh <= 0:
                continue
            if ms is None and mv is not None:
                ms = 0.4 * (4.83 - mv) + 0.301
            if ms is None:
                continue
            rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
            rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
            rows.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s,
                             sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s, ul=bool(r.get("vlos_sigma_ul")),
                             rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                             dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1,
                             dhost=fl(r.get("distance_host")), dist=fl(r.get("distance")),
                             mv=mv, dm31=fl(r.get("distance_m31"))))
    return rows
ALL = load_lvd()
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False):
    """X1's build (copied verbatim)."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl_, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl_, gu
        b = 1.0
        ufd = (r["mv"] is not None and r["mv"] > -7.7)
        if binmode == "free": b = arr_free.get(r["name"], med_free if (ufd or not mvrule) else 1.0)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar)
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, rows=keep)
def lin3(x, xs, v):
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))
def Rh_X1(r):
    if r["host"] == "field":
        return r["dist"] * KPC
    if r["dhost"]:
        return r["dhost"] * KPC
    if r["host"] == "M31" and r["dm31"]:
        return r["dm31"] * KPC
    return r["dist"] * KPC
CLASSICAL = {"Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
INDIV = ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius"]
EXCL = {"LMC", "SMC", "M 32"}
DES = {"NGC 147", "NGC 185", "NGC 205"}
def klass(r):
    n = r["name"]
    if n in EXCL: return None
    if r["host"] == "MW":
        if n in CLASSICAL: return "MW classical"
        if n in INDIV: return "indiv:" + n
        if r["mv"] is not None and r["mv"] > -7.7: return "MW ultra-faint"
        return "MW other"
    if r["host"] == "M31":
        if n in DES: return "M31 dE"
        return "bright M31" if r["logms"] >= 5.0 else "M31 others"
    return "LG field"
SMP = [r for r in ALL if klass(r) is not None]
CLS = {r["name"]: klass(r) for r in SMP}

# host fields (X1's / S1's)
def g_host(R_m, Mb, a0):
    gN = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * KPC + A_H) ** 2 / G / MSUN

# ==================================================================== XF1's C2 statistic (copied via RB2)
def boot_median(vals, sds, nb=4000, seed=11):
    rng = np.random.default_rng(seed); vals = np.asarray(vals); sds = np.asarray(sds); n = len(vals); meds = np.empty(nb)
    for b in range(nb):
        ix = rng.integers(0, n, n); meds[b] = np.median(vals[ix] + rng.normal(0, 1, n) * sds[ix])
    q = np.percentile(meds, [2.5, 50, 97.5])
    return dict(median=float(q[1]), ci95=[float(q[0]), float(q[2])], contains0=bool(q[0] <= 0 <= q[2]), n=int(n))

# ==================================================================== the record's external-field solver
GR = S.Grid2D(nper=24, Nt=16)
NSOLVE = [0]; WORST = [0.0]
def bg(xe):
    return (xe * xe / (1 + xe)) if (MUT and xe > 0) else xe      # MUTATE M1: X1's host-field bug
def logG(y, xe, Lam=0.0, tol=1e-10):
    """X1's logG: log10 g_pred/g_bar (E-W) at r_1/2 = (4/3) R_h, Plummer, solver units a = 1, a0 = 1."""
    sv = S.Solver2D(GR, y, 0.0 if xe <= 0 else bg(xe), Lam, isolated=(xe <= 0))
    U, res, it = sv.solve(tol=tol)
    NSOLVE[0] += 1; WORST[0] = max(WORST[0], res)
    rf, gr = sv.field_monopole()
    _, vir, wo = S.jeans(rf, gr, [])
    return math.log10(6 * wo * R12 / y)

# ==================================================================== committed data read as data
X1CSV = list(csv.DictReader(open(os.path.join(X1D, "x1_per_system.csv"))))
X1TAB = {f: json.load(open(os.path.join(X1D, f"x1_stage_tables_{f}.json")))["tables"] for f in FOOTS}
RB2J = json.load(open(os.path.join(RB2D, "rb2.json")))
RB2_PS = {f: {r["name"]: r for r in RB2J["footings"][f]["per_system"]} for f in FOOTS}
X1_ROW = {(r["footing"], r["name"]): r for r in X1CSV}
RB2_CLS = {f: RB2J["footings"][f]["classes"] for f in FOOTS}

GRADED = ("MW ultra-faint", "bright M31")
CONTROL = "LG field"
REPORTED = ("MW classical", "M31 others", "M31 dE", "MW other")
RUNGS = (1.0, 1.5, 2.0, 3.0, 4.0, 8.0)      # d_inf / d_today ; plus the x_e = 0 rung ("inf")

# ==================================================================== datasets (X1's RNG call order)
RNG = np.random.default_rng(20261031); DS = {}
for f in FOOTS:
    DS[f] = build(SMP, A0[f], RNG, mvrule=True)
    build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)

def cls_members(f, cls):
    return [(i, r) for i, r in enumerate(DS[f]["rows"]) if CLS[r["name"]] == cls]

def draws_residual(f, pred_fn):
    """per-system Delta draws = lb - pred, for every system in DS[f]; pred_fn(name, i) -> per-draw log10 g_pred/g_bar."""
    X = DS[f]; N = len(X["rows"]); out = np.empty_like(X["lb"])
    for i, r in enumerate(X["rows"]):
        out[i] = X["lb"][i] - pred_fn(r["name"], i)
    return out

def from_table(f, key, est=0):
    TB = X1TAB[f]
    def pf(name, i):
        t = TB[name]
        return lin3(DS[f]["ly"][i], t["ys"], np.asarray(t[key])[:, est])
    return pf

def c2(f, D, cls):
    d = [float(np.median(D[i])) for i, _ in cls_members(f, cls)]
    s = [float(np.std(D[i])) for i, _ in cls_members(f, cls)]
    return boot_median(d, s)

# ==================================================================== KNOWN ANSWERS
KA = {}
P("DWF1 hosted-dwarf offset, %s. kappa = 1/2 FITTED; not theory closed; footings never pooled." % ("MUTATE" if MUT else "MAIN"))
P("criteria 34a3ee01f0 (committed alone before any number here). X1 rows: %d systems." % len(SMP))
P("")
P("=== KNOWN ANSWERS ===")

# KA3 / KA4: the table path reproduces X1's committed per-system columns
D_iso = {}; D_efe = {}
ka4 = 0.0; ka3 = 0.0
for f in FOOTS:
    D_iso[f] = draws_residual(f, from_table(f, "iso0"))
    D_efe[f] = draws_residual(f, from_table(f, "emb0"))
    for i, r in enumerate(DS[f]["rows"]):
        row = X1_ROW[(f, r["name"])]
        ka4 = max(ka4, abs(float(np.median(D_efe[f][i])) - float(row["Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"])))
        ka3 = max(ka3, abs(float(np.median(D_iso[f][i])) - float(row["Delta[iso AQUAL L*0]"])))
KA["KA3_iso_vs_X1_csv"] = dict(ok=ka3 < 1e-9, value=ka3, threshold=1e-9, what="my isolated prediction (X1's iso0 table) vs X1's committed per-system Delta[iso AQUAL L*0]")
KA["KA4_efe_vs_X1_csv"] = dict(ok=ka4 < 1e-9, value=ka4, threshold=1e-9, what="my EFE prediction (X1's emb0 table) vs X1's committed Delta[AQUAL + EFE L*0]")
P("KA3 %s  X1 iso column reproduced through pred_draws(iso0): max |d| %.1e (line 1e-9)" % ("PASS" if ka3 < 1e-9 else "FAIL", ka3))
P("KA4 %s  X1 EFE column reproduced through pred_draws(emb0): max |d| %.1e (line 1e-9)" % ("PASS" if ka4 < 1e-9 else "FAIL", ka4))

# KA1: RB2's B row from X1's columns through XF1's C2
ka1 = {}; B_C2 = {}
for f in FOOTS:
    for cls in GRADED + (CONTROL, "MW classical"):
        st = c2(f, D_iso[f], cls)
        B_C2[(f, cls)] = st
        ref = RB2_CLS[f][cls]["stats"]["prim"]
        d = max(abs(st["median"] - ref["median"]), abs(st["ci95"][0] - ref["ci95"][0]), abs(st["ci95"][1] - ref["ci95"][1]))
        ka1[(f, cls)] = d
k1 = max(ka1.values())
KA["KA1_RB2_B_row"] = dict(ok=k1 < 0.01, value=k1, threshold=0.01,
                           what="RB2's B (prim) class medians and 95% intervals recomputed from X1's columns through XF1's C2")
P("KA1 %s  RB2's B row reproduced (UF, bright M31, LG field, MW classical; both footings): max |d| %.4f dex (line 0.01)"
  % ("PASS" if k1 < 0.01 else "FAIL", k1))

# KA5: RB2's per-system B residual and r_J read as data; RB2's estimator limits re-checked on the copied code
ka5 = {}
ka5["a_rb2_iso_vs_x1_iso"] = max(abs(RB2_PS[f][n]["Delta"]["iso"] - float(X1_ROW[(f, n)]["Delta[iso AQUAL L*0]"]))
                                 for f in FOOTS for n in RB2_PS[f])
def gl(gN):
    gN = np.asarray(gN, float); return 0.5 * gN + np.sqrt(0.25 * gN * gN + gN)
def gNp(r, y):
    return y * r / (1.0 + r * r) ** 1.5
ygrid = np.geomspace(1e-6, 1e3, 50)
ka5["b_rJ_inf_is_iso"] = float(np.max(np.abs(gl(gNp(R12, ygrid)) / gl(gNp(R12, ygrid)) - 1.0)))
ka5["c_newton_limit"] = float(max(abs(math.log10(gl(y) / y)) for y in (1e6, 1e8, 1e10)))
ok5 = ka5["a_rb2_iso_vs_x1_iso"] < 0.01 and ka5["b_rJ_inf_is_iso"] < 1e-12 and ka5["c_newton_limit"] < 1e-6
KA["KA5_rb2_and_estimator"] = dict(ok=ok5, value=ka5, threshold=dict(a=0.01, b=1e-12, c=1e-6),
                                   what="RB2's per-system B residual vs X1's iso column; the law's r_J -> inf and deep-Newton limits")
P("KA5 %s  RB2 per-system B vs X1 iso: max |d| %.4f dex (line 0.01); law limits r_J->inf and y->inf ok"
  % ("PASS" if ok5 else "FAIL", ka5["a_rb2_iso_vs_x1_iso"]))

# KA2 (graded after the solves) and KA6 are filled in below.
P("")

# ==================================================================== (a) the host's external field
P("=== CANDIDATE (a): the host's external field (record's exact AQUAL solve, x_e = g_host(d)/a0, screening off) ===")
EFE_C2 = {}; SHIFT_A = {}; SHIFT_A_V3 = {}
for f in FOOTS:
    for cls in GRADED + (CONTROL,) + REPORTED:
        if not cls_members(f, cls): continue
        EFE_C2[(f, cls)] = c2(f, D_efe[f], cls)
    for cls in GRADED + (CONTROL,):
        b = B_C2[(f, cls)]["median"]; e = EFE_C2[(f, cls)]["median"]
        SHIFT_A[(f, cls)] = e - b
        # secondary reading: X1's v3 L*floor column (screening at the L* floor, external field on)
        rows = cls_members(f, cls)
        d3 = [float(X1_ROW[(f, r["name"])]["Delta[v3 L*floor]"]) for _, r in rows]
        s3 = [float(X1_ROW[(f, r["name"])]["sdMC[v3 L*floor]"]) for _, r in rows]
        st3 = boot_median(d3, s3)
        SHIFT_A_V3[(f, cls)] = st3["median"] - b
for cls in GRADED + (CONTROL,):
    for f in FOOTS:
        b = B_C2[(f, cls)]; e = EFE_C2[(f, cls)]
        P("  [%9s] %-14s N %2d  before (B, isolated) %+0.3f [%+0.3f,%+0.3f]  after (a) %+0.3f [%+0.3f,%+0.3f]  shift %+0.3f dex"
          % (f, cls, e["n"], b["median"], b["ci95"][0], b["ci95"][1], e["median"], e["ci95"][0], e["ci95"][1], SHIFT_A[(f, cls)]))
    P("             v3 L*floor reading (screening on): shift %+0.3f / %+0.3f dex (canonical / alt)" % (SHIFT_A_V3[("canonical", cls)], SHIFT_A_V3[("alt", cls)]))
per_system_a = {}
for f in FOOTS:
    per_system_a[f] = {}
    for i, r in enumerate(DS[f]["rows"]):
        if CLS[r["name"]] not in GRADED: continue
        per_system_a[f][r["name"]] = dict(
            cls=CLS[r["name"]], before=float(np.median(D_iso[f][i])), after=float(np.median(D_efe[f][i])),
            shift=float(np.median(D_efe[f][i]) - np.median(D_iso[f][i])),
            x_e=float(X1TAB[f][r["name"]]["xe"]["E_mid"]), y0=float(X1TAB[f][r["name"]]["y0"]),
            d_kpc=float(X1TAB[f][r["name"]]["Rh_kpc"]))
for f in FOOTS:
    ss = sorted(per_system_a[f].items(), key=lambda kv: kv[1]["shift"])
    P("  [%9s] per-system shift (a): smallest %s %+0.3f | median %+0.3f | largest %s %+0.3f (graded rows only)"
      % (f, ss[0][0], ss[0][1]["shift"], float(np.median([v["shift"] for v in per_system_a[f].values()])), ss[-1][0], ss[-1][1]["shift"]))
P("")

# ==================================================================== new solves: rungs for (c) and KA2/KA6
P("=== NEW SOLVES (this lane's own; D10 2-D AQUAL with a uniform background, Lam = 0) ===")
NEWTAB = {}; k2 = 0.0; k2_rows = []
for f in FOOTS:
    a0 = A0[f]; NEWTAB[f] = {}
    for r in SMP:
        t = X1TAB[f][r["name"]]
        ys = list(t["ys"]); xe_mid = t["xe"]["E_mid"]; d_today_kpc = t["Rh_kpc"]
        iso = [logG(10 ** ly, 0.0) for ly in ys]
        emb = [logG(10 ** ly, xe_mid) for ly in ys]
        for k in range(3):
            dd = max(abs(iso[k] - t["iso0"][k][0]), abs(emb[k] - t["emb0"][k][0]))
            k2 = max(k2, dd)
            if dd > 0.05: k2_rows.append((f, r["name"], dd))
        rungs = {}
        for rg in RUNGS:
            xe_r = g_host(rg * d_today_kpc * KPC, MHOST[r["host"]], a0) / a0
            rungs[rg] = dict(xe=xe_r, v=[logG(10 ** ly, xe_r) for ly in ys])
        NEWTAB[f][r["name"]] = dict(ys=ys, iso=iso, emb=emb, xe_mid=xe_mid, d_kpc=d_today_kpc, rungs=rungs)
    P("  [%9s] %d systems solved (iso + x_e_mid + %d rungs, 3 y each): %d solves, worst residual %.1e, %.0f s"
      % (f, len(SMP), len(RUNGS), NSOLVE[0], WORST[0], time.time() - T0))
KA["KA2_my_emb_vs_X1_emb0"] = dict(ok=(k2 < 1e-3) if not MUT else (len(k2_rows) > 0), value=k2, threshold=1e-3,
                                   what="my solves at (y, x_e_mid) vs X1's committed emb0 table" + (" (MUTATE: must FAIL, > 0.05 dex on some row)" if MUT else ""))
P("KA2 %s  my solves at (y, x_e_mid) vs X1's emb0 table: max |d| %.2e (line 1e-3)%s"
  % ("PASS" if (k2 < 1e-3) else "FAIL", k2, ("; rows over 0.05 dex: %d" % len(k2_rows)) if k2_rows else ""))

# KA6: monotone non-increasing in x_e (the clean case of KILL C1)
ka6 = []
for y in (1e-4, 1e-3, 1e-2):
    v = [logG(y, 0.0)] + [logG(y, x) for x in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5)]
    ka6.append(all(v[k + 1] <= v[k] + 1e-9 for k in range(len(v) - 1)))
KA["KA6_monotone_in_x_e"] = dict(ok=all(ka6), value=ka6, threshold="all True",
                                 what="logG(y, x_e) non-increasing in x_e on y in {1e-4,1e-3,1e-2} x x_e in {0,...,0.5}")
P("KA6 %s  logG non-increasing in x_e on the KA6 grid: %s" % ("PASS" if all(ka6) else "FAIL", ka6))
P("")

# ==================================================================== (c) the amount set at infall
P("=== CANDIDATE (c): the amount set when the dwarf fell in, at the host's field (ladder d_inf / d_today) ===")
C_C2 = {}; SHIFT_C = {}
for f in FOOTS:
    for rg in RUNGS:
        def pf(name, i, rg=rg, f=f):
            t = NEWTAB[f][name]
            return lin3(DS[f]["ly"][i], t["ys"], np.asarray(t["rungs"][rg]["v"]))
        Dc = draws_residual(f, pf)
        for cls in GRADED + (CONTROL,):
            C_C2[(f, rg, cls)] = c2(f, Dc, cls)
            SHIFT_C[(f, rg, cls)] = C_C2[(f, rg, cls)]["median"] - B_C2[(f, cls)]["median"]
for cls in GRADED:
    for f in FOOTS:
        line = "  [%9s] %-14s " % (f, cls)
        for rg in RUNGS:
            line += "d_inf=%gx: %+0.3f  " % (rg, SHIFT_C[(f, rg, cls)])
        P(line + "| no field at infall (x_e=0, kindest): %+0.3f" % B_C2[(f, cls)]["median"])
for f in FOOTS:
    P("  [%9s] %-14s no-field rung %+0.3f | rungs: %s" % (f, CONTROL, B_C2[(f, CONTROL)]["median"],
      "  ".join("d_inf=%gx: %+0.3f" % (rg, SHIFT_C[(f, rg, CONTROL)]) for rg in RUNGS)))
# per-system (c) at the rungs, graded rows
per_system_c = {}
for f in FOOTS:
    per_system_c[f] = {}
    for i, r in enumerate(DS[f]["rows"]):
        if CLS[r["name"]] not in GRADED: continue
        t = NEWTAB[f][r["name"]]
        per_system_c[f][r["name"]] = dict(cls=CLS[r["name"]], y0=t["iso"][1],
            before=float(np.median(D_iso[f][i])),
            rungs={str(rg): dict(xe=t["rungs"][rg]["xe"],
                                 shift=float(np.median(DS[f]["lb"][i] - lin3(DS[f]["ly"][i], t["ys"], np.asarray(t["rungs"][rg]["v"]))) - np.median(D_iso[f][i])))
                   for rg in RUNGS})
# C1: the amount at any external field never exceeds the isolated amount
c1_bad = []
for f in FOOTS:
    for n, t in NEWTAB[f].items():
        for rg in RUNGS:
            if any(t["rungs"][rg]["v"][k] > t["iso"][k] + 1e-9 for k in range(3)):
                c1_bad.append((f, n, rg))
C1_fires = (len(c1_bad) == 0)
# C2: the kindest rung (no field at infall) returns B unchanged
c2_bad = []
for f in FOOTS:
    for n, t in NEWTAB[f].items():
        if max(abs(t["iso"][k] - X1TAB[f][n]["iso0"][k][0]) for k in range(3)) > 0.01:
            c2_bad.append((f, n))
C2_fires = (len(c2_bad) == 0)
P("  KILL C1 (amount at any x_e <= isolated amount): %s (%d violations of %d row-rungs)"
  % ("FIRES" if C1_fires else "does not fire", len(c1_bad), sum(len(NEWTAB[f]) * len(RUNGS) for f in FOOTS)))
P("  KILL C2 (kindest rung returns B unchanged, |d| < 0.01 dex): %s (%d rows off)" % ("FIRES" if C2_fires else "does not fire", len(c2_bad)))
# ---- reported: the CEILING.  with the field on, the prediction saturates as y -> 0, so the
# amount frozen in at the infall field is capped; the ceiling residual is the best (c) can do.
YDEEP = 1e-2
YFLOOR = 1e-7       # the D10 2-D solve turns Newtonian below y about 5e-8 (KA7)
MED = {}; req = {}; CEILC2 = {}; plat = {}
for f in FOOTS:
    rows = [r for _, r in cls_members(f, "MW ultra-faint")]
    y0_med = float(np.median([X1TAB[f][r["name"]]["y0"] for r in rows]))
    d_med = float(np.median([X1TAB[f][r["name"]]["Rh_kpc"] for r in rows]))
    need = B_C2[(f, "MW ultra-faint")]["median"]       # dex of extra prediction needed
    MED[f] = dict(y0=y0_med, d=d_med, need=need)
    # (i) the infall size that would close the gap, at each rung's field
    req[f] = {}
    for rg in RUNGS:
        xe_r = g_host(rg * d_med * KPC, MHOST["MW"], A0[f]) / A0[f]
        base = logG(y0_med, 0.0)
        lb_ = (lambda yy: logG(max(yy, YFLOOR), xe_r))
        f_lo, f_hi = 0.0, 3.0                            # log10 of the size factor: y_inf = y0 / 10**f
        if lb_(y0_med) - base >= need:
            req[f][rg] = None; continue
        if lb_(y0_med / 10 ** f_hi) - base < need:
            req[f][rg] = dict(x_e=xe_r, r_h_infall_over_today=None, y_ratio=None, note="not reachable")
            continue
        for _ in range(40):
            mid = 0.5 * (f_lo + f_hi)
            if lb_(y0_med / 10 ** mid) - base >= need: f_hi = mid
            else: f_lo = mid
        ans = 0.5 * (f_lo + f_hi)                          # y_inf / y0 = 10 ** (-ans)
        req[f][rg] = dict(x_e=xe_r, y_ratio=10 ** (-ans), r_h_infall_over_today=10 ** (0.5 * ans),
                          y0_inf=y0_med / 10 ** ans)
    # (ii) the ceiling residual at each rung: y -> 0 gives the most (c) can ever reach
    CEIL = {n: {str(rg): logG(max(10 ** t["ys"][1] * YDEEP, YFLOOR), t["rungs"][rg]["xe"]) for rg in RUNGS}
            for n, t in NEWTAB[f].items()}
    for rg in RUNGS:
        for cls in GRADED + (CONTROL,):
            idx = [i for i, _ in cls_members(f, cls)]
            dvals = [float(np.median(DS[f]["lb"][i]) - CEIL[DS[f]["rows"][i]["name"]][str(rg)]) for i in idx]
            svals = [float(np.std(D_iso[f][i])) for i in idx]
            CEILC2[(f, rg, cls)] = boot_median(dvals, svals)
    # (iii) plateau: the deep value must be flat against a 100x shallower depth
    for cls in GRADED:
        yv = float(np.median([X1TAB[f][r["name"]]["y0"] for r in [r for _, r in cls_members(f, cls)]]))
        for rg in RUNGS:
            xe_r = g_host(rg * d_med * KPC, MHOST["MW"], A0[f]) / A0[f]
            plat[(f, cls, rg)] = abs(logG(max(yv * YDEEP * 1e-1, YFLOOR), xe_r) - logG(max(yv * YDEEP, YFLOOR), xe_r))
    yb = X1TAB[f]["Bootes III"]["y0"]
    for rg in RUNGS:
        xe_r = g_host(rg * d_med * KPC, MHOST["MW"], A0[f]) / A0[f]
        plat[(f, "Bootes III", rg)] = abs(logG(max(yb * YDEEP * 1e-1, YFLOOR), xe_r) - logG(max(yb * YDEEP, YFLOOR), xe_r))
    P("  [%9s] (c) ceiling (y -> 0 at that rung's field) residual, by rung:" % f)
    for cls in GRADED + (CONTROL,):
        cells = "  ".join("d_inf=%gx: %+0.3f" % (rg, CEILC2[(f, rg, cls)]["median"]) for rg in RUNGS)
        P("            %-14s %s" % (cls, cells))
    P("            plateau check (deep vs 100x shallower), max |d| %.4f dex" % max(plat.values()))
    cells = []
    for rg in RUNGS:
        r = req[f][rg]
        cells.append("d_inf=%gx: %s" % (rg, ("%.1f x r_h(today)" % r["r_h_infall_over_today"])
                                        if (r and r.get("r_h_infall_over_today")) else "NOT REACHED"))
    P("  [%9s] (c) infall size that would close the %+0.3f dex gap, median UF row (y0 %.2e, d %.0f kpc):\n            %s"
      % (f, MED[f]["need"], MED[f]["y0"], MED[f]["d"], "  ".join(cells)))
P("")

# ==================================================================== (b) formation amount + tidal stripping
P("=== CANDIDATE (b): formation-time amount + tidal stripping (RB2's own r_J machinery, read as data) ===")
B_C2S = {}; SHIFT_B = {}
for f in FOOTS:
    for cls in GRADED:
        rows = [r for _, r in cls_members(f, cls)]
        d0 = [RB2_PS[f][r["name"]]["Delta"]["prim"] for r in rows]
        s0 = [RB2_PS[f][r["name"]]["sd"]["prim"] for r in rows]
        d1 = [RB2_PS[f][r["name"]]["Delta"]["strong"] for r in rows]
        s1 = [RB2_PS[f][r["name"]]["sd"]["strong"] for r in rows]
        B_C2S[(f, cls)] = (boot_median(d0, s0), boot_median(d1, s1))
        SHIFT_B[(f, cls)] = B_C2S[(f, cls)][1]["median"] - B_C2S[(f, cls)][0]["median"]
for cls in GRADED:
    for f in FOOTS:
        p, s = B_C2S[(f, cls)]
        P("  [%9s] %-14s N %2d  before (B, primary edge) %+0.3f [%+0.3f,%+0.3f]  after (b, strong-tide edge) %+0.3f [%+0.3f,%+0.3f]  shift %+0.3f dex"
          % (f, cls, p["n"], p["median"], p["ci95"][0], p["ci95"][1], s["median"], s["ci95"][0], s["ci95"][1], SHIFT_B[(f, cls)]))
for f in FOOTS:
    w = max(((RB2_PS[f][n]["Delta"]["strong"] - RB2_PS[f][n]["Delta"]["prim"]), n)
            for n in RB2_PS[f] if CLS.get(n) in GRADED)
    P("  [%9s] largest per-system stripping move among the graded rows: %s %+0.3f dex" % (f, w[1], w[0]))
P("  formation-time amount half: HY4-5's reading is NOT ON DISK (no HY4-5 output anywhere in the repository) -> that half of the row is left UNGRADED.")
P("")

# ==================================================================== kills and labels
P("=== KILLS ===")
KILLS = {}
for f in FOOTS:
    KILLS[f] = {}
    for cls in GRADED:
        sh = SHIFT_A[(f, cls)]
        a1 = sh > 0.0
        a2 = not (sh <= -0.30)
        KILLS[f][(cls, "a")] = dict(shift=sh, A1_sign_fires=bool(a1), A2_size_fires=bool(a2), killed=bool(a1 or a2))
    KILLS[f]["field_clause"] = dict(shift=SHIFT_A[(f, CONTROL)], inside_0p05=bool(abs(SHIFT_A[(f, CONTROL)]) <= 0.05))
    KILLS[f]["b"] = {cls: dict(shift=SHIFT_B[(f, cls)], B1_fires=bool(SHIFT_B[(f, cls)] > 0.0),
                               killed=bool(SHIFT_B[(f, cls)] > 0.0)) for cls in GRADED}
    KILLS[f]["c"] = dict(C1_fires=bool(C1_fires), C2_fires=bool(C2_fires),
                         best_rung_residual=B_C2[(f, "MW ultra-faint")]["median"],
                         rung1_residual=C_C2[(f, 1.0, "MW ultra-faint")]["median"],
                         killed=bool(C1_fires and C2_fires))
    P("  [%9s] (a) UF shift %+0.3f dex: A1 (wrong sign) %s, A2 (size < 0.3 dex the right way) %s -> %s"
      % (f, SHIFT_A[(f, "MW ultra-faint")], "FIRES" if KILLS[f][("MW ultra-faint", "a")]["A1_sign_fires"] else "no",
         "FIRES" if KILLS[f][("MW ultra-faint", "a")]["A2_size_fires"] else "no",
         "KILLED" if KILLS[f][("MW ultra-faint", "a")]["killed"] else "survives"))
    P("  [%9s] (a) bright M31 shift %+0.3f dex -> %s ; LG field control shift %+0.3f dex (inside +-0.05: %s)"
      % (f, SHIFT_A[(f, "bright M31")], "KILLED" if KILLS[f][("bright M31", "a")]["killed"] else "survives",
         SHIFT_A[(f, CONTROL)], KILLS[f]["field_clause"]["inside_0p05"]))
    P("  [%9s] (b) stripping: UF shift %+0.3f dex (B1 %s), bright M31 %+0.3f dex -> %s"
      % (f, SHIFT_B[(f, "MW ultra-faint")], "FIRES" if KILLS[f]["b"]["MW ultra-faint"]["B1_fires"] else "no",
         SHIFT_B[(f, "bright M31")], "KILLED" if all(KILLS[f]["b"][c]["killed"] for c in GRADED) else "survives"))
    P("  [%9s] (c) C1 %s, C2 %s: best rung %+0.3f (unchanged), d_inf = d_today rung %+0.3f -> %s"
      % (f, "FIRES" if C1_fires else "no", "FIRES" if C2_fires else "no", B_C2[(f, "MW ultra-faint")]["median"],
         C_C2[(f, 1.0, "MW ultra-faint")]["median"], "KILLED" if KILLS[f]["c"]["killed"] else "survives"))

def label(f):
    killed = (KILLS[f][("MW ultra-faint", "a")]["killed"] and KILLS[f][("bright M31", "a")]["killed"]
              and all(KILLS[f]["b"][c]["killed"] for c in GRADED) and KILLS[f]["c"]["killed"])
    closed = any(st["contains0"] for st in
                 [EFE_C2[(f, "MW ultra-faint")], C_C2[(f, 1.0, "MW ultra-faint")], B_C2S[(f, "MW ultra-faint")][1]])
    if killed and not closed: return "NO CANDIDATE MOVES A HOSTED DWARF UP"
    if closed: return "A CANDIDATE MOVES A HOSTED DWARF UP"
    return "SPLIT"
LAB = {f: label(f) for f in FOOTS}
P("")
P("=== LABELS ===")
for f in FOOTS:
    P("  %-9s: %s" % (f, LAB[f]))
P("LANE LABEL: %s / %s" % (LAB["canonical"], LAB["alt"]))
P("")
P("runtime %.0f s, peak RSS %.3f GB, %d solves. kappa = 1/2 FITTED; not theory closed. Relabels nothing."
  % (time.time() - T0, rss_gb(), NSOLVE[0]))

# ==================================================================== outputs
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return float(o)
    if isinstance(o, (np.integer, int)): return int(o)
    if isinstance(o, (np.bool_, bool)): return bool(o)
    return o
RES = dict(lane="DWF1", tag=TAG, criteria="34a3ee01f0", mutate=bool(MUT),
           labels=LAB, KA=KA, KA_ok=bool(all(v["ok"] for v in KA.values())) if not MUT else False,
           kills={f: {str(k): v for k, v in KILLS[f].items()} for f in FOOTS},
           before={f: {c: B_C2[(f, c)] for c in GRADED + (CONTROL,)} for f in FOOTS},
           after_a={f: {c: EFE_C2[(f, c)] for c in GRADED + (CONTROL,)} for f in FOOTS},
           shift_a={f: {c: SHIFT_A[(f, c)] for c in GRADED + (CONTROL,)} for f in FOOTS},
           shift_a_v3={f: {c: SHIFT_A_V3[(f, c)] for c in GRADED + (CONTROL,)} for f in FOOTS},
           after_b={f: {c: [B_C2S[(f, c)][0], B_C2S[(f, c)][1]] for c in GRADED} for f in FOOTS},
           shift_b={f: {c: SHIFT_B[(f, c)] for c in GRADED} for f in FOOTS},
           after_c={f: {str(rg): {c: C_C2[(f, rg, c)] for c in GRADED + (CONTROL,)} for rg in RUNGS} for f in FOOTS},
           shift_c={f: {str(rg): {c: SHIFT_C[(f, rg, c)] for c in GRADED + (CONTROL,)} for rg in RUNGS} for f in FOOTS},
           requirement_c={f: {str(rg): req[f][rg] for rg in RUNGS} for f in FOOTS},
           per_system_a=per_system_a, per_system_c=per_system_c,
           solves=NSOLVE[0], runtime_s=time.time() - T0, rss_gb=rss_gb())
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
if MUT:
    sys.exit(0 if not KA["KA2_my_emb_vs_X1_emb0"]["ok"] else 1)   # M3: the mutation arm must fail
