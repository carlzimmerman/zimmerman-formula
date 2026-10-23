#!/usr/bin/env python3
"""X1_hosted_recount -- v3 on ALL Local Group satellites (no mass cut), with published-MOND controls, and T3 bookkeeping.
Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md + LITERATURE_LOOKUP.md (committed alone first, cfd0ae45fb).

Stages (each one process, OMP_NUM_THREADS=1 nice -n 15, < 1 GB, <= 30 min):
  --stage controls            step 0 (S1's headline reproduced, K0) + step 1 (C0-C3, published MOND controls) -> x1_stage_controls.json
  --stage tables --foot F     step-2 per-system v3 tables for every LG system with a measured sigma (footing F)  -> x1_stage_tables_F.json
  --stage final               KT, step-2 class statistics and verdict, step-3 T3 bookkeeping                     -> .out, _results.json, CSVs
  --mutate                    (with --stage controls) S1's host-field bug: the solver background is the Newtonian y_e instead of
                              the total x_e.  K0 and C3b must FAIL.  Writes *_MUTATE.* only.

S1's code paths (loader, MC, 3x3 grids, bootstrap, host fields, CFG691 recipe) are COPIED from
rebuild_2026_10_22/S1_v3_hosted_small/s1_v3_hosted_small.py at commit 2b6bb658a1 (S1's script runs on import, so it cannot be
imported); the D10 solver and F2's AQUAL solver are imported read-only.  Deterministic (seeded), no network.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import csv, json, math, os, resource, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar"))
sys.path.insert(0, os.path.join(REPO, "rebuild_2026_10_22", "F2_outer_lensing"))
import d10_solver as S   # noqa: E402  (read-only)
import f2_aqual as F2    # noqa: E402  (read-only)

ARGV = sys.argv[1:]
MUT = "--mutate" in ARGV
STAGE = ARGV[ARGV.index("--stage") + 1] if "--stage" in ARGV else None
FOOT_ARG = ARGV[ARGV.index("--foot") + 1] if "--foot" in ARGV else None
if STAGE not in ("controls", "tables", "final"):
    sys.exit("usage: --stage controls|tables|final [--foot canonical|alt] [--mutate]")
if MUT and STAGE != "controls":
    sys.exit("--mutate runs with --stage controls only (FROZEN_CRITERIA section 4)")
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(k, ok, val, thr, what):
    CHK[k] = dict(ok=bool(ok), value=val, threshold=thr, what=what)
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  ({what})")
def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)

# ------------------------------------------------------------------ constants (S1's)
G, MSUN, PC = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
LFLOOR = {"canonical": 21.68, "alt": 22.85}
def LSETS(f): return [("floor", LFLOOR[f]), ("24", 24.0), ("90", 90.0)]
A_H = 3.0 * KPC
GE2_8KPC = 2.0592e-10
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
NMC, NBOOT = 2000, 4000
DY, DL = 0.6, 0.3
FW_N = 2.0 * (4 / 3) ** 3 / (1 + (4 / 3) ** 2) ** 1.5
FV_N = math.pi / 4.0
R12 = 4.0 / 3.0
UPS_PRIOR = 0.15          # dex: Upsilon_V 1-4 read as +-2 sigma about 2 (FROZEN section 2)
UPS4 = math.log10(2.0)    # Upsilon_V 4 vs 2 (T3 conservative edge)
S1_REF = {"canonical": (1.3307203762661644, 0.14735364394782058, 45), "alt": (1.2989961780852868, 0.1474219349862198, 46)}

# ------------------------------------------------------------------ solver wrappers (S1's)
GR = S.Grid2D(nper=24, Nt=16)
WORST = [0.0]; NSOLVE = [0]
def bg(xe):
    return (xe * xe / (1 + xe)) if (MUT and xe > 0) else xe        # MUTATE: Newtonian y_e passed as the total field
def solve(y, xe, Lam, grid=None, tol=1e-10, track=True):
    grid = GR if grid is None else grid
    iso = xe <= 0
    sv = S.Solver2D(grid, y, 0.0 if iso else bg(xe), Lam, isolated=iso)
    U, res, it = sv.solve(tol=tol)
    if track:
        WORST[0] = max(WORST[0], res); NSOLVE[0] += 1
    rf, gr = sv.field_monopole()
    _, vir, wo = S.jeans(rf, gr, [])
    return dict(rf=rf, gr=gr, vir=vir, wo=wo, res=res)
def logG(y, xe, Lam):
    """log10 g_pred/g_bar (E3 convention G(M/2)/r12^2) for E-W and E-V; solver units a = 1, a0 = 1."""
    d = solve(y, xe, Lam)
    return math.log10(6 * d["wo"] * R12 / y), math.log10(6 * d["vir"] * R12 / y)
def lin3(x, xs, v):
    x = np.asarray(x, float)
    s0 = (v[1] - v[0]) / (xs[1] - xs[0]); s1 = (v[2] - v[1]) / (xs[2] - xs[1])
    return np.where(x < xs[1], v[1] + s0 * (x - xs[1]), v[1] + s1 * (x - xs[1]))
def interp2(ly, lL, ys, Ls, T):
    rows = [lin3(lL, Ls, T[i]) for i in range(3)]
    s0 = (rows[1] - rows[0]) / (ys[1] - ys[0]); s1 = (rows[2] - rows[1]) / (ys[2] - ys[1])
    return np.where(ly < ys[1], rows[1] + s0 * (ly - ys[1]), rows[1] + s1 * (ly - ys[1]))

# ------------------------------------------------------------------ host fields (S1's)
def g_host(R_m, Mb, a0):
    gN = G * Mb * MSUN / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * KPC + A_H) ** 2 / G / MSUN
def host_mass(host, ek, a0):
    frac = {"E_lo": 4.0e10 / 6.0e10, "E_mid": 1.0, "E_hi": Mb_hi(a0) / 6.0e10}[ek]
    return MHOST[host] * frac

# ------------------------------------------------------------------ data (S1's loader + M_V, distance_m31)
DATA = os.path.join(REPO, "real_research", "data")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
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
arr_f07 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values()))); med_f07 = float(np.median(list(arr_f07.values())))
GEH = {}
for r in csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))):
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")):
        GEH[r["lvd_name"]] = (float(r["geha_sigma"]), fl(r.get("geha_e_sigma_ll")) or 0.1, fl(r.get("geha_e_sigma_ul")) or 0.1)
def sample_E3(a0):
    mcrit = a0 * (24.0 * PC) ** 2 / G / MSUN
    return [r for r in ALL if r["logms"] < math.log10(mcrit)]

def split_normal(rng, c, em, ep, n):
    z = rng.standard_normal(n); return c + np.where(z < 0, z * em, z * ep)
def build(rows, a0, rng, ups=2.0, binmode="free", sig_src="lvd", drop_ul=False, mvrule=False):
    """S1's build (copied); mvrule=True applies the median binary ratio only to M_V > -7.7 (FROZEN section 2, step 2)."""
    keep = [r for r in rows if not (drop_ul and r["ul"])]
    N = len(keep)
    lb = np.empty((N, NMC)); ly = np.empty((N, NMC)); la = np.empty((N, NMC)); Md = np.empty((N, NMC)); Ms_ = np.empty((N, NMC))
    for i, r in enumerate(keep):
        s, sem, sep = r["sigma"], r["sem"], r["sep"]
        if sig_src == "lower" and r["name"] in GEH:
            gs, gl, gu = GEH[r["name"]]
            if gs < s: s, sem, sep = gs, gl, gu
        b = 1.0
        ufd = (r["mv"] is not None and r["mv"] > -7.7)
        if binmode == "free": b = arr_free.get(r["name"], med_free if (ufd or not mvrule) else 1.0)
        elif binmode == "f07": b = arr_f07.get(r["name"], med_f07 if (ufd or not mvrule) else 1.0)
        fD = 10 ** (split_normal(rng, 0.0, r["dmem"], r["dmep"], NMC) / 5.0)
        sig = np.abs(split_normal(rng, s, sem, sep, NMC)) * b
        rh = np.abs(split_normal(rng, r["rh"], r["rhem"], r["rhep"], NMC)) * fD
        ms = ups / 2.0 * 10 ** r["logms"] * fD ** 2
        r12 = R12 * rh * PC
        gobs = 3.0 * (sig * 1e3) ** 2 / r12; gbar = G * (ms / 2) * MSUN / r12 ** 2
        lb[i] = np.log10(gobs / gbar); Md[i] = gobs * r12 ** 2 / G / MSUN; Ms_[i] = ms
        ly[i] = np.log10(G * ms * MSUN / ((rh * PC) ** 2 * a0)); la[i] = np.log10(rh)
    return dict(lb=lb, ly=ly, la=la, Md=Md, Ms=Ms_, rows=keep)
def boot_ix(rng, N):
    return rng.integers(0, N, (NBOOT, N)), rng.integers(0, NMC, (NBOOT, N))
def boot_median(X, ix):
    idx, col = ix
    meds = np.median(X[idx, col], axis=1)
    return float(np.median(meds)), float(np.std(meds))

def pred_draws(TABf, X, key, est, Lst=None, shift=None):
    """S1's: per-draw log10(g_pred/g_bar) under table `key` ('iso0','emb0','emb_floor',...); est 0 = E-W, 1 = E-V."""
    out = np.empty_like(X["lb"])
    for i, r in enumerate(X["rows"]):
        t = TABf[r["name"]]
        if key in ("iso0", "emb0"):
            v = lin3(X["ly"][i], t["ys"], np.asarray(t[key])[:, est])
        else:
            lab = key.split("_", 1)[1]
            lL = math.log10(Lst) - X["la"][i]
            v = interp2(X["ly"][i], lL, t["ys"], t[f"Ls_{lab}"], np.asarray(t[key])[:, :, est])
        if shift is not None:
            v = v + shift(t, est)
        out[i] = v
    return out

# host-distance rules
def Rh_S1(r):                      # S1's code rule (step 0)
    return (r["dhost"] if r["dhost"] else r["dist"]) * KPC
def Rh_X1(r):                      # this lane's step-2 rule (FROZEN section 2)
    if r["host"] == "field":
        return r["dist"] * KPC
    if r["dhost"]:
        return r["dhost"] * KPC
    if r["host"] == "M31" and r["dm31"]:
        return r["dm31"] * KPC
    return r["dist"] * KPC

# classes (FROZEN section 2)
CLASSICAL = {"Carina", "Draco", "Fornax", "Leo I", "Leo II", "Sculptor", "Sextans", "Ursa Minor"}
INDIV = ["Crater II", "Antlia II", "Canes Venatici I", "Sagittarius"]
EXCL = {"LMC": "rotation-supported disc (Wolf estimator does not apply)", "SMC": "rotation-supported disc/irregular (Wolf does not apply)",
        "M 32": "compact elliptical 6.5 kpc from M31 (uniform-field model does not apply)"}
DES = {"NGC 147", "NGC 185", "NGC 205"}
VCLS = ["MW classical", "MW ultra-faint", "bright M31", "M31 others"]
RCLS = ["M31 dE", "LG field"]
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

def save_json(obj, name):
    json.dump(obj, open(os.path.join(HERE, name), "w"), indent=1, default=float)

# ================================================================== STAGE: controls (step 0 + step 1)
def mm13_rows():
    """LITERATURE-INPUT (PROVISIONAL web look-up, LITERATURE_LOOKUP.md): name, LVD name, L_V [1e5 Lsun], r_1/2 [pc], sig_iso, sig_efe."""
    T = [("And I", "Andromeda I", 45., 832, 9.2, 8.0), ("And II", "Andromeda II", 93., 1660, 11.0, None),
         ("And III", "Andromeda III", 10., 525, 6.3, 5.4), ("And V", "Andromeda V", 5.9, 292, 5.5, 7.0),
         ("And VI", "Andromeda VI", 34., 440, 8.6, None), ("And VII", "Andromeda VII", 178., 977, 13.0, None),
         ("And IX", "Andromeda IX", 1.5, 552, 3.9, 1.5), ("And X", "Andromeda X", 0.76, 309, 3.3, 2.3),
         ("And XI", "Andromeda XI", 0.49, 145, 3.0, 3.2), ("And XII", "Andromeda XII", 0.31, 289, 2.6, 1.7),
         ("And XIII", "Andromeda XIII", 0.41, 203, 2.8, 2.5), ("And XIV", "Andromeda XIV", 2.1, 537, 4.3, 3.6),
         ("And XV", "Andromeda XV", 7.1, 355, 5.8, 6.1), ("And XVI", "Andromeda XVI", 4.1, 178, 5.0, None),
         ("And XVIII", "Andromeda XVIII", 6.3, 417, 5.6, None), ("And XXI", "Andromeda XXI", 4.6, 1023, 5.2, 3.7),
         ("And XXII", "Andromeda XXII", 0.35, 340, 2.7, 2.3),
         ("And XVII", "Andromeda XVII", 2.6, 381, 4.5, 2.5), ("And XIX", "Andromeda XIX", 4.1, 2244, 5.0, 2.6),
         ("And XX", "Andromeda XX", 0.28, 165, 2.6, 2.1), ("And XXIII", "Andromeda XXIII", 10., 1372, 6.4, 4.4),
         ("And XXIV", "Andromeda XXIV", 0.94, 489, 3.5, 2.8), ("And XXV", "Andromeda XXV", 6.5, 945, 5.7, 3.5),
         ("And XXVI", "Andromeda XXVI", 0.59, 296, 3.1, 2.0), ("And XXVII", "Andromeda XXVII", 1.2, 579, 3.7, 1.8),
         ("And XXVIII", "Andromeda XXVIII", 2.1, 284, 4.3, None), ("And XXIX", "Andromeda XXIX", 1.8, 481, 4.1, 3.8),
         ("And XXX", "Cassiopeia II", 1.4, 356, 3.8, 3.5), ("And XXXI", "Lacerta I", 41., 1216, 9.0, None),
         ("And XXXII", "Cassiopeia III", 71., 1941, 10.3, 10.3)]
    return T
A0_MM, V_M31 = 1.21e-10, 230e3
mu_s = lambda x: x / (1.0 + x)

def stage_controls():
    R = dict(lane="X1_hosted_recount", stage="controls", mutate=MUT, frozen="cfd0ae45fb", s1_commit="2b6bb658a1")
    P("=" * 110)
    P("X1_hosted_recount -- stage controls: step 0 (S1 reproduced) + step 1 (published-MOND controls)"
      + ("   *** MUTATE: Newtonian y_e as the background ***" if MUT else ""))
    P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10, never pooled; controls use the papers' own a0")
    P("=" * 110)
    # ---------------- C3: solver physics
    P("\n--- C3: solver physics (D10 read-only; F2 read-only; Route F) ---")
    c3a = []
    for y in (1e-5, 1e-4):
        d = solve(y, 0.0, 0.0, track=False)
        ex = (2.0 / 9.0) * math.sqrt(y)               # (4/81 G M a0)^(1/2) in solver units
        c3a.append(abs(0.5 * math.log10(d["vir"] / ex))); P(f"   C3a y {y:.0e}: E-V sigma^2 {d['vir']:.6e} vs (2/9)sqrt(y) {ex:.6e}  |dlog sigma| {c3a[-1]:.2e}")
    check("C3a", max(c3a) <= 0.005, f"{max(c3a):.2e} dex", "<= 0.005 dex", "isolated deep MOND: solver E-V vs sigma^4 = (4/81) G M a0 (exact)")
    c3b = []
    for xe, Lam in ((0.05, 0.0), (0.05, 0.5), (0.05, 2.0), (0.5, 0.0), (0.5, 0.5), (0.5, 2.0), (0.076, 0.0), (0.3, 0.0)):
        y = 1e-4 * xe
        d = solve(y, xe, Lam, tol=1e-14, track=False)
        Fv, _ = S.routeF_monopole(y, xe, Lam, 1.0)
        g2 = float(np.interp(0.0, np.log(d["rf"]), d["gr"]))
        c3b.append(abs(g2 / Fv - 1)); P(f"   C3b x_e {xe} Lam {Lam}: 2D {g2:.6e} Route F {Fv:.6e} rel {c3b[-1]:.2e}")
    check("C3b", max(c3b) < 2e-2, f"{max(c3b):.2e}", "< 2e-2", "linear EFE: D10 2D monopole at r = a vs Route F (C6 kernel)")
    c3c = []
    for xe in (0.1, 0.5):
        y = 100.0
        d = solve(y, xe, 0.0, track=False)
        ye = xe * xe / (1 + xe)
        f2 = F2.solve_efe(ye)
        for s in (3.0, 10.0):
            ra = s * math.sqrt(y)
            Md10 = ra * ra * float(np.interp(math.log(ra), np.log(d["rf"]), d["gr"])) / y
            Mf2 = float(np.interp(math.log(s), np.log(f2["r"]), f2["M"]))
            c3c.append(abs(Md10 / Mf2 - 1)); P(f"   C3c x_e {xe} r/r_M {s}: M_eff D10 {Md10:.5f} F2 {Mf2:.5f} rel {c3c[-1]:.2e}")
    check("C3c", max(c3c) < 2e-2, f"{max(c3c):.2e}", "< 2e-2", "embedded AQUAL: D10 2D vs F2's independent point-mass solver")

    # ---------------- step 1: MM13 + Crater II
    P("\n--- step 1: published MOND controls (LITERATURE-INPUT, PROVISIONAL; papers' own a0; S1's solver at L* = 0, AQUAL + EFE) ---")
    LVDM31 = {r["name"]: r for r in csv.DictReader(open(os.path.join(DATA, "dsph", "lvd_dwarf_m31.csv")))}
    rows = []
    c0 = []
    for (nm, lvd, LV, rhalf, s_iso, s_efe) in mm13_rows():
        M = 2.0 * LV * 1e5; GM = G * M * MSUN; rh_m = rhalf * PC
        si_calc = (4.0 / 81.0 * GM * A0_MM) ** 0.25 / 1e3
        c0.append(abs(math.log10(si_calc / s_iso)))
        dh = fl(LVDM31[lvd]["distance_host"]) if lvd in LVDM31 else None
        xe_lvd = V_M31 ** 2 / (dh * KPC * A0_MM) if dh else None
        se_lvd = math.sqrt(GM / (3 * rh_m * mu_s(xe_lvd))) / 1e3 if xe_lvd else None
        rows.append(dict(name=nm, lvd=lvd, LV=LV, rhalf=rhalf, s_iso=s_iso, s_efe=s_efe, si_calc=si_calc, dhost=dh,
                         xe_lvd=xe_lvd, se_lvd=se_lvd, M=M))
    # Crater II (McGaugh 2016)
    CR = dict(M=3.3e5, Re=1066.0, xe=0.076, a0=1.2e-10, pub=2.1, s_iso_pub=4.0)
    GMc = G * CR["M"] * MSUN; rhc = R12 * CR["Re"] * PC
    cr_iso = (4.0 / 81.0 * GMc * CR["a0"]) ** 0.25 / 1e3
    cr_efe = math.sqrt(CR["a0"] * GMc / (3 * CR["xe"] * CR["a0"] * rhc)) / 1e3
    c0 += [abs(math.log10(cr_iso / CR["s_iso_pub"])), abs(math.log10(cr_efe / CR["pub"]))]
    P(f"   C0 Crater II: Eq.(1) {cr_iso:.3f} km/s (printed ~4); Eq.(2) {cr_efe:.3f} km/s (printed 2.1)")
    check("C0", max(c0) <= 0.02, f"max |dlog sigma| {max(c0):.4f} dex over {len(c0)} values", "<= 0.02 dex",
          "transcription: Eq.(2)/(1) from transcribed L_V reproduce every printed sigma_iso; Crater II Eq.(1)/(2) reproduce 4 and 2.1")
    # C1 (reported): on-disk distances
    c1 = [abs(math.log10(r["se_lvd"] / r["s_efe"])) for r in rows if r["s_efe"] and r["se_lvd"]]
    c1_med = float(np.median(c1))
    P(f"   C1 (reported): Eq.(3), mu = x/(1+x), V_M31 230, LVD distance_host vs printed sigma_efe: median |dlog sigma| {c1_med:.4f} dex "
      f"over {len(c1)} rows (max {max(c1):.3f}); flag line 0.05 -> {'METHOD READING UNCERTAIN' if c1_med > 0.05 else 'consistent'}")
    # control set: drop And XVIII (no distance_host, no printed sigma_efe)
    ctl = [r for r in rows if not (r["s_efe"] is None and r["dhost"] is None)]
    dropped = [r["name"] for r in rows if r not in ctl]
    P(f"   control rows: {len(ctl)} (dropped: {dropped})")
    for r in ctl:
        GM = G * r["M"] * MSUN; rh_m = r["rhalf"] * PC
        if r["s_efe"] is not None:
            mu = GM / (3 * rh_m * (r["s_efe"] * 1e3) ** 2); r["xe"] = mu / (1 - mu); r["xe_src"] = "backed out of printed sigma_efe"
        else:
            r["xe"] = r["xe_lvd"]; r["xe_src"] = "V^2/D, LVD distance_host"
        r["D0"] = min(r["s_iso"], r["s_efe"]) if r["s_efe"] is not None else r["s_iso"]
        e3 = math.sqrt(GM / (3 * rh_m * mu_s(r["xe"]))) / 1e3
        r["D1"] = min(r["si_calc"], e3)
        siW = (GM * A0_MM / 18.0) ** 0.25 / 1e3; seW = math.sqrt(GM / 2 / (3 * rh_m * mu_s(r["xe"]))) / 1e3
        r["D2"] = min(siW, seW)
        a = 0.75 * rh_m; y = GM / (a * a * A0_MM)
        d = solve(y, r["xe"], 0.0)
        r["y"] = y; r["D3"] = math.sqrt(d["wo"] * A0_MM * a) / 1e3; r["D3V"] = math.sqrt(d["vir"] * A0_MM * a) / 1e3
        r["d_tot"] = math.log10(r["D3"] / r["D0"]); r["d_mass"] = math.log10(r["D2"] / r["D1"]); r["d_rem"] = math.log10(r["D3"] / r["D2"])
        r["d_in"] = math.log10(r["D1"] / r["D0"]); r["d_totV"] = math.log10(r["D3V"] / r["D0"])
        P(f"   {r['name']:10s} x_e {r['xe']:.3f} ({'pub' if r['s_efe'] is not None else 'LVD'}) y {y:.2e} | pub {r['D0']:5.2f} | D1 {r['D1']:5.2f} "
          f"D2(Wolf M/2) {r['D2']:5.2f} | solver E-W {r['D3']:5.2f} E-V {r['D3V']:5.2f} | dlog: tot {r['d_tot']:+.3f} mass {r['d_mass']:+.3f} rem {r['d_rem']:+.3f}")
    # Crater II steps
    a = CR["Re"] * PC; y = GMc / (a * a * CR["a0"])
    d = solve(y, CR["xe"], 0.0)
    cr = dict(D0=CR["pub"], D1=min(cr_iso, cr_efe),
              D2=min((GMc * CR["a0"] / 18.0) ** 0.25 / 1e3, cr_efe / math.sqrt(2.0)),
              D3=math.sqrt(d["wo"] * CR["a0"] * a) / 1e3, D3V=math.sqrt(d["vir"] * CR["a0"] * a) / 1e3, y=y, xe=CR["xe"])
    cr.update(d_tot=math.log10(cr["D3"] / cr["D0"]), d_mass=math.log10(cr["D2"] / cr["D1"]), d_rem=math.log10(cr["D3"] / cr["D2"]),
              d_in=math.log10(cr["D1"] / cr["D0"]), d_totV=math.log10(cr["D3V"] / cr["D0"]))
    P(f"   Crater II  x_e 0.076 (pub) y {y:.2e} | pub 2.10 | D1 {cr['D1']:.2f} D2 {cr['D2']:.2f} | solver E-W {cr['D3']:.2f} E-V {cr['D3V']:.2f} "
      f"| dlog: tot {cr['d_tot']:+.3f} mass {cr['d_mass']:+.3f} rem {cr['d_rem']:+.3f}")
    C2abs = float(np.median([abs(r["d_tot"]) for r in ctl]))
    m_tot = float(np.median([r["d_tot"] for r in ctl])); m_mass = float(np.median([r["d_mass"] for r in ctl]))
    m_rem = float(np.median([r["d_rem"] for r in ctl])); m_in = float(np.median([r["d_in"] for r in ctl]))
    m_totV = float(np.median([r["d_totV"] for r in ctl])); C2absV = float(np.median([abs(r["d_totV"]) for r in ctl]))
    c2_pass = (C2abs <= 0.10) and (abs(cr["d_tot"]) <= 0.10)
    P(f"   C2 (control): MM13 median |dlog sigma| {C2abs:.3f} dex (signed {m_tot:+.3f}; E-V {C2absV:.3f} / {m_totV:+.3f}) over {len(ctl)}; "
      f"Crater II {cr['d_tot']:+.3f} (E-V {cr['d_totV']:+.3f}) -> C2 {'PASS' if c2_pass else 'FAIL'} (line 0.10 dex)")
    P(f"   decomposition (signed medians, dex in sigma): input step {m_in:+.3f}; mass convention (Wolf M/2) {m_mass:+.3f}; "
      f"remainder (exact AQUAL solve vs Wolf-convention formula) {m_rem:+.3f}; total {m_tot:+.3f}")
    def approx_ok(t, m, rr):
        return (np.sign(m) == np.sign(t)) and abs(m) >= 0.5 * abs(t) and (-0.10 <= rr <= 0.02)
    ap_mm = approx_ok(m_tot, m_mass, m_rem); ap_cr = approx_ok(cr["d_tot"], cr["d_mass"], cr["d_rem"])
    R["step1"] = dict(MM13_rows=[{k: v for k, v in r.items()} for r in ctl], dropped=dropped, crater_ii=cr,
                      C1_median_abs=c1_med, C1_n=len(c1), C1_flag=c1_med > 0.05,
                      C2_median_abs=C2abs, C2_signed=m_tot, C2_median_abs_EV=C2absV, C2_signed_EV=m_totV, C2_pass=c2_pass,
                      m_in=m_in, m_mass=m_mass, m_rem=m_rem, approx_rule_MM13=bool(ap_mm), approx_rule_CrII=bool(ap_cr))

    # ---------------- step 0: S1's headline, S1's code path and seed
    P("\n--- step 0 (K0): S1's headline on E3's sample, S1's code path, seed 20261023 ---")
    RNG0 = np.random.default_rng(20261023)
    SAMP = {f: sample_E3(A0[f]) for f in FOOTS}
    DS = {}
    for f in FOOTS:
        a0 = A0[f]
        DS[(f, "primary")] = build(SAMP[f], a0, RNG0)
        DS[(f, "raw")] = build(SAMP[f], a0, RNG0, binmode="none")
        DS[(f, "W")] = build(SAMP[f], a0, RNG0, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True)
    BOOT = {k: boot_ix(RNG0, len(v["rows"])) for k, v in DS.items()}
    TAB0 = {f: {} for f in FOOTS}
    for f in FOOTS:
        a0 = A0[f]
        for r in SAMP[f]:
            M0 = 10 ** r["logms"]; a = r["rh"] * PC
            y0 = G * M0 * MSUN / (a * a * a0)
            xe = g_host(Rh_S1(r), host_mass(r["host"], "E_mid", a0), a0) / a0
            ys = math.log10(y0) + np.array([-DY, 0.0, DY])
            Ls = math.log10(LFLOOR[f] / r["rh"]) + np.array([-DL, 0.0, DL])
            T = np.array([[logG(10 ** ly_, xe, 10 ** lL) for lL in Ls] for ly_ in ys])
            TAB0[f][r["name"]] = dict(ys=ys, Ls_floor=Ls, emb_floor=T, xe=xe, y0=y0)
        P(f"   [{f}] {len(SAMP[f])} systems tabulated at the floor ({NSOLVE[0]} solves so far, {time.time() - T0:.0f} s)")
    k0, step0 = [], {}
    for f in FOOTS:
        X = DS[(f, "primary")]
        D = X["lb"] - pred_draws(TAB0[f], X, "emb_floor", 0, LFLOOR[f])
        m, s = boot_median(D, BOOT[(f, "primary")])
        ref = S1_REF[f]
        step0[f] = dict(Delta=m, sd=s, N=len(X["rows"]), S1=ref[0], S1_sd=ref[1])
        k0 += [abs(m - ref[0]), abs(s - ref[1])]
        P(f"   [{f}] v3 floor E-W Delta {m:+.5f} +- {s:.5f} (N {len(X['rows'])})  vs S1 {ref[0]:+.5f} +- {ref[1]:.5f}")
    nok = len(SAMP["canonical"]) == 45 and len(SAMP["alt"]) == 46
    check("K0", nok and max(k0) <= 0.005, f"N {len(SAMP['canonical'])}/{len(SAMP['alt'])}; max |diff| {max(k0):.2e} dex", "45/46 and <= 0.005 dex",
          "S1's headline (+1.331/+1.299 at the floor) reproduced with S1's solver, code path and seed")
    R["step0"] = step0
    R["step0_tables"] = {f: {n: dict(ys=t["ys"].tolist(), Ls_floor=t["Ls_floor"].tolist(), emb_floor=t["emb_floor"].tolist(), xe=t["xe"])
                             for n, t in TAB0[f].items()} for f in FOOTS}

    # ---------------- C3d convergence at two control cells
    c3d = []
    FINE, FAR = S.Grid2D(nper=48, Nt=32), S.Grid2D(nper=24, Nt=16, rout=1e5)
    a1 = [r for r in ctl if r["name"] == "And I"][0]
    for (y, xe, lab) in ((cr["y"], cr["xe"], "Crater II"), (a1["y"], a1["xe"], "And I")):
        b = solve(y, xe, 0.0, track=False); fn = solve(y, xe, 0.0, grid=FINE, track=False); fa = solve(y, xe, 0.0, grid=FAR, track=False)
        dd = [abs(math.sqrt(o[k] / b[k]) - 1) for o in (fn, fa) for k in ("wo", "vir")]
        c3d.append(max(dd)); P(f"   C3d {lab}: max |d sigma/sigma| (fine, far; E-W, E-V) {max(dd):.2e}")
    check("C3d", max(c3d) < 5e-3, f"{max(c3d):.2e}", "< 5e-3", "convergence at the Crater II and And I control cells")
    R["validation"] = dict(C3a=c3a, C3b=c3b, C3c=c3c, C3d=c3d, C0=c0)

    # ---------------- step-1 outcome (FROZEN section 3)
    base_ok = all(CHK[k]["ok"] for k in ("K0", "C0", "C3a", "C3b", "C3c", "C3d"))
    if base_ok and c2_pass:
        outcome = "CONTROLS PASS"
    elif base_ok and ap_mm and ap_cr:
        outcome = "CONTROL FAIL, PUBLISHED APPROXIMATION"
    else:
        outcome = "CONTROL FAIL, UNEXPLAINED"
    R["step1"]["outcome"] = outcome; R["step1"]["proceed_to_step2"] = outcome != "CONTROL FAIL, UNEXPLAINED"
    P(f"\n   STEP-1 OUTCOME: {outcome}  (approximation rule MM13 {ap_mm}, Crater II {ap_cr}; base checks {base_ok})")
    check("KS_controls", WORST[0] < 1e-8, f"{WORST[0]:.1e} over {NSOLVE[0]} solves", "< 1e-8", "every production solve converged (controls stage)")
    check("KR_controls", rss_gb() < 1.0, f"{rss_gb():.3f} GB", "< 1 GB", "peak RSS (controls stage)")
    npass = sum(v["ok"] for v in CHK.values())
    R["checks"] = CHK; R["runtime_s"] = time.time() - T0; R["solves"] = NSOLVE[0]; R["worst_residual"] = WORST[0]; R["out"] = OUT
    P(f"\nSTAGE CONTROLS COMPLETE: {npass}/{len(CHK)} checks PASS.  {time.time() - T0:.0f} s, {NSOLVE[0]} production solves" + ("  (MUTATE)" if MUT else ""))
    if MUT:
        R["out"] = OUT
        save_json(R, "x1_hosted_recount_results_MUTATE.json")
        open(os.path.join(HERE, "x1_hosted_recount_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    else:
        save_json(R, "x1_stage_controls.json")
    sys.exit(0 if npass == len(CHK) else 1)

# ================================================================== STAGE: tables (step 2, one footing)
def lg_sample():
    return [r for r in ALL if klass(r) is not None]
def stage_tables(f):
    C = json.load(open(os.path.join(HERE, "x1_stage_controls.json")))
    if not C["step1"]["proceed_to_step2"]:
        P(f"STOP: step-1 outcome {C['step1']['outcome']} -> step 2 is not run (FROZEN section 3)."); sys.exit(2)
    a0 = A0[f]
    SMP = lg_sample()
    P(f"--- stage tables [{f}]: {len(SMP)} LG systems (excluded: {sorted(EXCL)}) ---")
    TAB = {}
    for r in SMP:
        M0 = 10 ** r["logms"]; a = r["rh"] * PC
        y0 = G * M0 * MSUN / (a * a * a0)
        Rh = Rh_X1(r)
        xe = {ek: g_host(Rh, host_mass(r["host"], ek, a0), a0) / a0 for ek in ("E_lo", "E_mid", "E_hi")}
        ys = math.log10(y0) + np.array([-DY, 0.0, DY])
        t = dict(y0=y0, xe=xe, ys=ys.tolist(), Rh_kpc=Rh / KPC)
        t["iso0"] = [list(logG(10 ** ly_, 0.0, 0.0)) for ly_ in ys]
        t["emb0"] = [list(logG(10 ** ly_, xe["E_mid"], 0.0)) for ly_ in ys]
        for lab, Lst in LSETS(f):
            Ls = math.log10(Lst / r["rh"]) + np.array([-DL, 0.0, DL])
            t[f"Ls_{lab}"] = Ls.tolist()
            t[f"emb_{lab}"] = [[list(logG(10 ** ly_, xe["E_mid"], 10 ** lL)) for lL in Ls] for ly_ in ys]
        for ek in ("E_lo", "E_hi"):
            t[f"{ek}_floor"] = list(logG(y0, xe[ek], LFLOOR[f] / r["rh"]))
        TAB[r["name"]] = t
        if len(TAB) % 10 == 0:
            P(f"   [{f}] {len(TAB)}/{len(SMP)} systems ({NSOLVE[0]} solves, worst residual {WORST[0]:.1e}, {time.time() - T0:.0f} s)")
    R = dict(stage="tables", footing=f, tables=TAB, solves=NSOLVE[0], worst_residual=WORST[0], rss_gb=rss_gb(), runtime_s=time.time() - T0)
    P(f"   [{f}] done: {len(TAB)} systems, {NSOLVE[0]} solves, worst residual {WORST[0]:.1e}, peak RSS {rss_gb():.3f} GB, {time.time() - T0:.0f} s")
    R["out"] = OUT
    save_json(R, f"x1_stage_tables_{f}.json")

# ================================================================== STAGE: final (step 2 statistics, step 3, verdicts)
def stage_final():
    C = json.load(open(os.path.join(HERE, "x1_stage_controls.json")))
    R = dict(lane="X1_hosted_recount", frozen="cfd0ae45fb", s1_commit="2b6bb658a1")
    for l in C["out"]: OUT.append(l)
    for k, v in C["checks"].items(): CHK[k] = v
    R["step0"] = C["step0"]; R["step1"] = C["step1"]; R["validation"] = C["validation"]
    proceed = C["step1"]["proceed_to_step2"]
    TB = {}
    if proceed:
        for f in FOOTS:
            T = json.load(open(os.path.join(HERE, f"x1_stage_tables_{f}.json")))
            for l in T["out"]: OUT.append(l)
            TB[f] = T
    P("\n" + "=" * 110)
    P("X1_hosted_recount -- stage final: step 2 (all LG satellites, no mass cut) and step 3 (T3 bookkeeping)")
    P("=" * 110)
    SMP = lg_sample()
    RNG = np.random.default_rng(20261031)
    DS = {}
    for f in FOOTS:
        DS[(f, "primary")] = build(SMP, A0[f], RNG, mvrule=True)
        DS[(f, "W")] = build(SMP, A0[f], RNG, ups=4.0, binmode="f07", sig_src="lower", drop_ul=True, mvrule=True)
    names = [r["name"] for r in SMP]
    CLS = {r["name"]: klass(r) for r in SMP}
    groups = {}
    for n in names:
        groups.setdefault(CLS[n], []).append(n)
    P(f"   sample: {len(SMP)} systems; excluded {sorted(EXCL)}; classes: " + ", ".join(f"{k} {len(v)}" for k, v in sorted(groups.items())))
    R["sample"] = {k: v for k, v in sorted(groups.items())}; R["excluded"] = EXCL

    # ---------------- KT determinism (step-2 floor tables vs step-0 floor tables)
    if proceed:
        kt = 0.0; nkt = 0
        for f in FOOTS:
            for n, t0 in C["step0_tables"][f].items():
                t = TB[f]["tables"][n]
                kt = max(kt, float(np.max(np.abs(np.asarray(t["emb_floor"]) - np.asarray(t0["emb_floor"])))), abs(t["xe"]["E_mid"] - t0["xe"]))
                nkt += 1
        check("KT", kt <= 1e-9, f"max |diff| {kt:.1e} over {nkt} system-footings", "<= 1e-9", "step-2 floor tables reproduce step-0 tables (E3 systems)")
        ws = max(TB[f]["worst_residual"] for f in FOOTS)
        check("KS", ws < 1e-8, f"{ws:.1e} over {sum(TB[f]['solves'] for f in FOOTS)} solves", "< 1e-8", "every step-2 production solve converged")
        rmax = max([TB[f]["rss_gb"] for f in FOOTS] + [rss_gb()])
        check("KR", rmax < 1.0, f"{rmax:.3f} GB", "< 1 GB", "peak RSS (tables and final stages)")

    def mm13_recipe(X, f):
        """published MM13 recipe per draw (STANDARD-MOND-MACHINERY side row): min(Eq.2, Eq.3), mu = x/(1+x), full M, r_1/2 = 4/3 R_e."""
        out = np.empty_like(X["lb"]); a0 = A0[f]
        for i, r in enumerate(X["rows"]):
            xe = TB[f]["tables"][r["name"]]["xe"]["E_mid"]
            M = X["Ms"][i] * MSUN; rh = 10 ** X["la"][i] * PC; r12 = R12 * rh
            si = (4.0 / 81.0 * G * M * a0) ** 0.25; se = np.sqrt(G * M / (3 * r12 * mu_s(xe)))
            s = np.minimum(si, se)
            out[i] = np.log10((3 * s * s / r12) / (G * (M / 2) / r12 ** 2))
        return out

    # ---------------- per-system draws for every prediction row
    ROWS = {}
    for f in FOOTS:
        for ds in ("primary", "W"):
            X = DS[(f, ds)]
            ROWS[(f, ds, "Newton")] = X["lb"] - math.log10(FW_N)
            if not proceed:
                continue
            TBf = TB[f]["tables"]
            ROWS[(f, ds, "iso AQUAL L*0")] = X["lb"] - pred_draws(TBf, X, "iso0", 0)
            ROWS[(f, ds, "AQUAL + EFE L*0 (exact MOND + EFE)")] = X["lb"] - pred_draws(TBf, X, "emb0", 0)
            for lab, Lst in LSETS(f):
                ROWS[(f, ds, f"v3 L*{lab}")] = X["lb"] - pred_draws(TBf, X, f"emb_{lab}", 0, Lst)
                ROWS[(f, ds, f"v3 L*{lab} E-V")] = X["lb"] - pred_draws(TBf, X, f"emb_{lab}", 1, Lst)
            for ek in ("E_lo", "E_hi"):
                sh = (lambda t, e, ek=ek: t[f"{ek}_floor"][e] - t["emb_floor"][1][1][e])
                ROWS[(f, ds, f"v3 L*floor bracket {ek}")] = X["lb"] - pred_draws(TBf, X, "emb_floor", 0, LFLOOR[f], shift=sh)
            ROWS[(f, ds, "published MM13 recipe (side row)")] = X["lb"] - mm13_recipe(X, f)
    # per-system central values, s_i, k_i
    PER = []
    for f in FOOTS:
        X = DS[(f, "primary")]
        for i, r in enumerate(X["rows"]):
            row = dict(footing=f, name=r["name"], host=r["host"], cls=CLS[r["name"]], logMstar=r["logms"], M_V=r["mv"], rh_pc=r["rh"],
                       sigma=r["sigma"], log_gobs_gbar_med=float(np.median(X["lb"][i])))
            for key in [k for k in ROWS if k[0] == f and k[1] == "primary"]:
                v = ROWS[key][i]; row[f"Delta[{key[2]}]"] = float(np.median(v)); row[f"sdMC[{key[2]}]"] = float(np.std(v))
            if proceed:
                t = TB[f]["tables"][r["name"]]
                row.update(d_host_kpc=t["Rh_kpc"], x_e_mid=t["xe"]["E_mid"], y_plummer=t["y0"], Lam_floor=LFLOOR[f] / r["rh"])
                T = np.asarray(t["emb_floor"])
                row["k_i"] = abs(1.0 + (T[2, 1, 0] - T[0, 1, 0]) / (2 * DY))
                row["s_i"] = math.hypot(row["sdMC[v3 L*floor]"], UPS_PRIOR * row["k_i"])
            row["zN_ups4"] = (row["Delta[Newton]"] - UPS4) / row["sdMC[Newton]"]
            PER.append(row)
    R["per_system"] = PER

    # ---------------- class statistics
    def stat(f, ds, key, members):
        X = DS[(f, ds)]
        idx = [i for i, r in enumerate(X["rows"]) if r["name"] in members]
        ix = IXS[(f, ds, tuple(sorted(members)))]
        return boot_median(ROWS[(f, ds, key)][idx], ix)
    IXS = {}
    allgroups = {k: v for k, v in groups.items()}
    for f in FOOTS:
        for ds in ("primary", "W"):
            X = DS[(f, ds)]
            for g, mem in sorted(allgroups.items()):
                IXS[(f, ds, tuple(sorted(mem)))] = boot_ix(RNG, len([r for r in X["rows"] if r["name"] in mem]))
    CLSTAT = {}
    keys = sorted({k[2] for k in ROWS})
    P("\n--- step 2: class statistics (bootstrap median over systems of Delta = log10 g_obs/g_pred, dex in g; +- bootstrap sd) ---")
    if not proceed:
        P("   STEP 2 NOT RUN (step-1 outcome UNEXPLAINED); only the Newton rows below (no solver) are computed for step 3.")
    for f in FOOTS:
        for g in sorted(allgroups):
            mem = allgroups[g]
            for ds in ("primary", "W"):
                for key in keys:
                    if (f, ds, key) not in ROWS: continue
                    m, s = stat(f, ds, key, mem)
                    CLSTAT[f"{f}|{g}|{ds}|{key}"] = dict(median=m, sd=s, N=len(mem))
    R["class_stats"] = CLSTAT
    order = ["Newton", "iso AQUAL L*0", "AQUAL + EFE L*0 (exact MOND + EFE)", "v3 L*floor", "v3 L*24", "v3 L*90", "v3 L*floor E-V",
             "v3 L*floor bracket E_lo", "v3 L*floor bracket E_hi", "published MM13 recipe (side row)"]
    for f in FOOTS:
        P(f"\n   [{f}]")
        for g in [c for c in VCLS + RCLS + sorted(x for x in allgroups if x.startswith("indiv:") or x == "MW other") if c in allgroups]:
            line = f"   {g:22s} N {len(allgroups[g]):2d} |"
            for key in order:
                k = f"{f}|{g}|primary|{key}"
                if k in CLSTAT:
                    short = {"Newton": "N", "iso AQUAL L*0": "iso", "AQUAL + EFE L*0 (exact MOND + EFE)": "MOND+EFE", "v3 L*floor": "v3fl",
                             "v3 L*24": "v3_24", "v3 L*90": "v3_90", "v3 L*floor E-V": "v3fl_EV", "v3 L*floor bracket E_lo": "Elo",
                             "v3 L*floor bracket E_hi": "Ehi", "published MM13 recipe (side row)": "MM13rec"}[key]
                    line += f" {short} {CLSTAT[k]['median']:+.2f}" + (f"+-{CLSTAT[k]['sd']:.2f}" if key in ("v3 L*floor", "Newton") else "")
            kW = f"{f}|{g}|W|v3 L*floor"
            if kW in CLSTAT: line += f" | W v3fl {CLSTAT[kW]['median']:+.2f}+-{CLSTAT[kW]['sd']:.2f}"
            P(line)

    # ---------------- class status, chi2, verdict (step 2)
    V = {}
    if proceed:
        STATUS = {}
        for f in FOOTS:
            for ds in ("primary", "W"):
                for g in VCLS:
                    mem = allgroups[g]
                    st = CLSTAT[f"{f}|{g}|{ds}|v3 L*floor"]
                    pr = [p for p in PER if p["footing"] == f and p["name"] in mem]
                    if ds == "primary":
                        chi2 = float(sum((p["Delta[v3 L*floor]"] / p["s_i"]) ** 2 for p in pr))
                    else:   # W: per-system draws of the W dataset, same k_i
                        X = DS[(f, "W")]; kk = {p["name"]: p["k_i"] for p in PER if p["footing"] == f}
                        chi2 = 0.0
                        for i, r in enumerate(X["rows"]):
                            if r["name"] in mem:
                                v = ROWS[(f, "W", "v3 L*floor")][i]
                                chi2 += (float(np.median(v)) / math.hypot(float(np.std(v)), UPS_PRIOR * kk[r["name"]])) ** 2
                    N = len(mem); ok_chi = chi2 / N <= 1 + 3 * math.sqrt(2.0 / N)
                    med, sd = st["median"], st["sd"]
                    if abs(med) <= 0.15 and ok_chi: s_ = "PASS-LIKE"
                    elif abs(med) > 0.15 and abs(med) >= 3 * sd: s_ = "FAIL"
                    else:
                        why = []
                        if not ok_chi: why.append("chi2 unacceptable")
                        if abs(med) > 0.15 and abs(med) < 3 * sd: why.append("|median| > 0.15 but < 3 sd")
                        s_ = "UNRESOLVED (" + "; ".join(why) + ")"
                    STATUS[(f, ds, g)] = dict(status=s_, median=med, sd=sd, chi2=chi2, N=N, chi2_per_N=chi2 / N, chi2_line=1 + 3 * math.sqrt(2.0 / N))
        P("\n--- step 2: class status at the L* floor (E-W), FROZEN section 2 ---")
        for (f, ds, g), v in STATUS.items():
            P(f"   [{f:9s} {ds:7s}] {g:15s} N {v['N']:2d}  median {v['median']:+.3f} +- {v['sd']:.3f} ({v['median'] / v['sd']:+.1f} sd)  "
              f"chi2/N {v['chi2_per_N']:.1f} (line {v['chi2_line']:.2f})  -> {v['status']}")
        stp = {f: {g: STATUS[(f, "primary", g)]["status"] for g in VCLS} for f in FOOTS}
        if all(stp[f]["MW classical"] == "PASS-LIKE" and stp[f]["bright M31"] == "PASS-LIKE" and stp[f]["MW ultra-faint"] == "FAIL" for f in FOOTS):
            v2 = "SAMPLE-DRIVEN"
        elif all(stp[f][g] == "FAIL" for f in FOOTS for g in VCLS):
            v2 = "GENERIC"
        else:
            v2 = "CLASS-GRADED"
        labels = []
        if any(stp["canonical"][g] != stp["alt"][g] for g in VCLS): labels.append("FOOTING-SPLIT")
        if any(STATUS[(f, "W", g)]["status"] != STATUS[(f, "primary", g)]["status"] for f in FOOTS for g in VCLS): labels.append("W-SENSITIVE")
        V["step2"] = dict(verdict=v2, labels=labels, status={f"{f}|{ds}|{g}": v for (f, ds, g), v in STATUS.items()},
                          estimator_note=("exact estimator (E-W on the solved field); published MOND sits above it by the step-1 m_tot"
                                          if C["step1"]["outcome"] != "CONTROLS PASS" else "controls pass"))
        P(f"\n   STEP-2 VERDICT (Q1): {v2}" + (f"  [{', '.join(labels)}]" if labels else "") + f"   (step-1 outcome: {C['step1']['outcome']})")
        # individual systems
        P("\n--- step 2: individual systems (per-system median of MC draws; s_i includes the Upsilon prior) ---")
        for f in FOOTS:
            for n in INDIV:
                p = [p for p in PER if p["footing"] == f and p["name"] == n][0]
                P(f"   [{f:9s}] {n:16s} x_e {p['x_e_mid']:.3f} y {p['y_plummer']:.1e} | Newton {p['Delta[Newton]']:+.2f} MOND+EFE "
                  f"{p['Delta[AQUAL + EFE L*0 (exact MOND + EFE)]']:+.2f} v3 floor {p['Delta[v3 L*floor]']:+.2f} +- {p['s_i']:.2f} "
                  f"(24 {p['Delta[v3 L*24]']:+.2f}, 90 {p['Delta[v3 L*90]']:+.2f}) MM13 recipe {p['Delta[published MM13 recipe (side row)]']:+.2f}")
    else:
        V["step2"] = dict(verdict="NOT RUN (step-1 outcome UNEXPLAINED)")

    # ---------------- step 3: T3 bookkeeping
    P("\n--- step 3: T3 bookkeeping (hosted systems vs Newton on their baryons; z at Upsilon_V = 4) ---")
    T3 = {}
    for f in FOOTS:
        rows = []
        for n in ("Crater II", "Antlia II"):
            p = [p for p in PER if p["footing"] == f and p["name"] == n][0]
            rows.append(dict(row=n, kind="individual", Delta_N=p["Delta[Newton]"], sd=p["sdMC[Newton]"], z=p["zN_ups4"], independent=True))
        for g in VCLS:
            st = CLSTAT[f"{f}|{g}|primary|Newton"]
            pr = [p for p in PER if p["footing"] == f and p["cls"] == g]
            rows.append(dict(row=g, kind="class", N=len(pr), Delta_N=st["median"], sd=st["sd"], z=(st["median"] - UPS4) / st["sd"],
                             n_members_z3=int(sum(p["zN_ups4"] >= 3 for p in pr)), independent=True))
        R948 = json.load(open(os.path.join(CFG, "CFG948_nocapture_vs_udgs", "cfg948_results.json")))
        RU1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content", "u1_v3_dust_content_results.json")))
        RA2 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "U1_v3_dust_content", "u1_a2_field_frame_results.json")))
        zc948 = R948["byfoot"][f]["primary"]["H_newton"]["z"]; zcu1 = RU1["numbers"]["N5"]["coma"][f]["B0"]["z_sys"]
        rows.append(dict(row="Coma UDGs (9)", kind="read", Delta_N_ln=R948["byfoot"][f]["primary"]["H_newton"]["Delta"], z=min(zc948, zcu1),
                         z_CFG948=zc948, z_U1_B0=zcu1, keys="cfg948 byfoot.<f>.primary.H_newton.z; U1 numbers.N5.coma.<f>.B0.z_sys", independent=True))
        A4 = RA2["numbers"]["F5"]["footings"][f]["A4"]
        za, zb = A4["any_radius"]["per_galaxy"]["z_from_Newton"], A4["beyond_rf"]["per_galaxy"]["z_from_Newton"]
        rows.append(dict(row="UMa members (27 galaxies)", kind="read", z=min(za, zb), z_any_radius=za, z_beyond_rf=zb,
                         mean_dex=A4["beyond_rf"]["per_galaxy"]["mean"], Newton_dex=A4["beyond_rf"]["per_galaxy"]["Newton"],
                         keys="U1 A2 numbers.F5.footings.<f>.A4.{any_radius,beyond_rf}.per_galaxy.z_from_Newton", independent=True))
        tdg = RU1["numbers"]["N5"]["tdg"][f]
        rows.append(dict(row="TDGs (6), booked", kind="T3-consistent", rbar=tdg["TDG_B0"]["rbar"], se=tdg["TDG_B0"]["se"], z=tdg["TDG_B0"]["z"], independent=False))
        rows.append(dict(row="DF2/DF4, booked", kind="T3-consistent", rbar_ln=tdg["DF_B0"]["rbar"], se=tdg["DF_B0"]["se"], z=tdg["DF_B0"]["z"], independent=False))
        T3[f] = rows
        for r in rows:
            extra = ""
            if r["kind"] == "class": extra = f" N {r['N']}, members with z_i >= 3: {r['n_members_z3']}"
            if r["kind"] == "individual" or r["kind"] == "class":
                P(f"   [{f:9s}] {r['row']:26s} Delta_N {r['Delta_N']:+.2f} +- {r['sd']:.2f} dex (Ups 2) -> z(Ups 4) {r['z']:+.1f}{extra}")
            elif r["kind"] == "read":
                P(f"   [{f:9s}] {r['row']:26s} z vs Newton {r['z']:+.1f} (read: " + ", ".join(f"{k} {v:.2f}" for k, v in r.items() if k.startswith("z_")) + ")")
            else:
                P(f"   [{f:9s}] {r['row']:26s} T3-consistent: B0 offset {r.get('rbar', r.get('rbar_ln')):+.3f} +- {r['se']:.3f} (z {r['z']:+.2f})")
    n5 = {f: sum(1 for r in T3[f] if r["independent"] and r["z"] >= 5) for f in FOOTS}
    n3 = {f: sum(1 for r in T3[f] if r["independent"] and r["z"] >= 3) for f in FOOTS}
    if all(n5[f] >= 2 for f in FOOTS): v3 = "T3 PREMISE CONTRADICTED"
    elif all(n3[f] == 0 for f in FOOTS): v3 = "T3 PREMISE SUPPORTED"
    else: v3 = "MIXED"
    V["step3"] = dict(verdict=v3, n_rows_ge5=n5, n_rows_ge3=n3,
                      booking=("TDG/DF2/DF4 native pass is T3-consistent in those systems while T3 fails in the contradicting sets; not an independent success"
                               if v3 == "T3 PREMISE CONTRADICTED" else "as computed"))
    R["T3"] = T3
    P(f"\n   STEP-3 VERDICT (Q2): {v3}  (independent hosted rows >= 5 sigma: canonical {n5['canonical']}, alt {n5['alt']}; >= 3 sigma: {n3['canonical']} / {n3['alt']})")
    R["verdict"] = V

    # ---------------- outputs
    with open(os.path.join(HERE, "x1_per_system.csv"), "w", newline="") as fh:
        keysall = []
        for p in PER:
            for k in p:
                if k not in keysall: keysall.append(k)
        w = csv.DictWriter(fh, fieldnames=keysall); w.writeheader(); [w.writerow(p) for p in PER]
    npass = sum(v["ok"] for v in CHK.values())
    R["checks"] = CHK; R["runtime_s_final"] = time.time() - T0
    P(f"\nX1_HOSTED_RECOUNT COMPLETE: {npass}/{len(CHK)} checks PASS.  Step-1 outcome: {C['step1']['outcome']}.  Q1: {V['step2']['verdict']}.  Q2: {v3}.")
    P("kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed; nothing here says the data favour the framework.")
    save_json(R, "x1_hosted_recount_results.json")
    open(os.path.join(HERE, "x1_hosted_recount.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if npass == len(CHK) else 1)

if STAGE == "controls":
    stage_controls()
elif STAGE == "tables":
    if FOOT_ARG not in FOOTS: sys.exit("--stage tables needs --foot canonical|alt")
    stage_tables(FOOT_ARG)
else:
    stage_final()
