#!/usr/bin/env python3
"""P1_dwarf_chemistry -- decide E6 Part C's conditional (zeta = 1, no pre-enrichment) from the satellites' own metallicity
distributions (MDFs) and [Mg/Fe], and recompute the cold-supply ratio q = L_req / L_MDF on both footings.
Criteria: FROZEN_CRITERIA.md (committed alone first, 526a565dec); ledger ASSUMPTION_LEDGER.md.

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 p1_dwarf_chemistry.py          -> p1_dwarf_chemistry.out, p1_dwarf_chemistry_results.json,
                                                                             p1_per_system.csv, p1_inventory.csv
      OMP_NUM_THREADS=1 nice -n 15 python3 p1_dwarf_chemistry.py --mutate -> *_MUTATE.* (k = 0 forced inside the quadrature:
                                                                             zeta = 1 imposed everywhere, E6's premise)
Deterministic (seeded), no network, one thread.  kappa = 1/2 FITTED; footings never pooled; not theory closed.
Read-only inputs: real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv; real_research/data/walker2023/*.dat.gz;
deepseek_push/data2/simon2019_dwarf_tab_ascii_14sep2018.dat; campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/
geha2026_paperII_tableA1.csv; doors_push_2026_10_22/E6_native_fret/e6_per_system.csv; doors_push_2026_10_22/E3_dwarf_excess/
e3_per_system.csv; campaign_fresh_gravity/CFG51_walker_multiepoch/walker_reduced_dispersions.tsv (member counts, info only)."""
import csv, gzip, json, math, os, re, sys
import numpy as np
from scipy.special import exp1, digamma, polygamma
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DSPH = os.path.join(REPO, "real_research", "data", "dsph")
WALK = os.path.join(REPO, "real_research", "data", "walker2023")
E6CSV = os.path.join(REPO, "doors_push_2026_10_22", "E6_native_fret", "e6_per_system.csv")
E3CSV = os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess", "e3_per_system.csv")
S19F = os.path.join(REPO, "deepseek_push", "data2", "simon2019_dwarf_tab_ascii_14sep2018.dat")
GEHAF = os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "geha2026_paperII_tableA1.csv")
CFG51F = os.path.join(REPO, "campaign_fresh_gravity", "CFG51_walker_multiepoch", "walker_reduced_dispersions.tsv")
MUT = "--mutate" in sys.argv
SFX = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None


# ------------------------------------------------------------------ constants (sources: ASSUMPTION_LEDGER.md)
LN10 = math.log(10.0); GAMMA = 0.5772156649015329
LOGY = (-0.5, -0.2, 0.1)                       # CFG317 bracket (CC-dominated Fe yield, solar units)
BAND_LO, BAND_HI = 1.0 / LN10, math.pi / math.sqrt(6.0) / LN10     # A2: zeta = 1, Z0 = 0 width band (dex)
SUP = 5.364; GAS_FAC = 1.33                    # inherited (E6); 5.364 LCDM-PROCESSED, enters only via L_req
LOGY_ALPHA = (0.00, 0.18)                      # CFG317 O-yield statement applied to alpha (EXTERNAL textbook)
NBOOT, SEED = 4000, 20261023
NBOOT_AD = 200
FOOTS = ("canonical", "alt")
CHECKS = []


def ck(k, ok, val, thr, what):
    CHECKS.append((k, bool(ok)))
    P(f"{k} {'PASS' if ok else 'FAIL'} {val} {thr}  -- {what}")


# ============================================================ one-zone family: moments of ln phi_k(t), t ~ Exp(1) on [0, U]
NQ = 400
_xq, _wq = np.polynomial.legendre.leggauss(NQ)
QW = 0.5 * (_xq + 1.0); QWW = 0.5 * _wq
UINF = 60.0                                     # u = infinity evaluated on [0, 60] (e^-60 negligible)


def lnphi(k, t):
    """ln(Z/p0) = ln[(1 - e^{-kt})/k]; k = (zeta-1) eta/(1+eta).  MUTATE: k forced to 0 (zeta = 1, E6's premise)."""
    if MUT or k == 0.0:
        return np.log(t)
    return np.log(-np.expm1(-k * t) / k)


def moments(k, U):
    """g = <ln phi_k>, s2 = Var ln phi_k for t ~ Exp(1) truncated at U (vector U; inf allowed).  Substitution t = U w^4."""
    U = np.atleast_1d(np.asarray(U, float))
    Ue = np.where(np.isfinite(U), U, UINF)[:, None]
    t = Ue * QW[None, :] ** 4
    wt = np.exp(-t) * 4.0 * Ue * QW[None, :] ** 3 * QWW[None, :]
    nrm = wt.sum(1)
    lp = lnphi(k, t)
    g = (wt * lp).sum(1) / nrm
    s2 = (wt * (lp - g[:, None]) ** 2).sum(1) / nrm
    return g, s2


def g0_exact(U):
    """<ln t> for t ~ Exp(1) truncated at U, closed form (independent of E6's code)."""
    if not np.isfinite(U):
        return -GAMMA
    if U < 1.0:                                   # series (the closed form cancels catastrophically at small U)
        lU, num, fac = math.log(U), 0.0, 1.0
        for n in range(40):
            num += (-1) ** n / fac * U ** (n + 1) * (lU / (n + 1) - 1.0 / (n + 1) ** 2)
            fac *= (n + 1)
        return num / (-math.expm1(-U))
    return (-GAMMA - exp1(U) - math.exp(-U) * math.log(U)) / (-math.expm1(-U))


def s20_exact(U):
    if not np.isfinite(U):
        return math.pi ** 2 / 6.0
    m2 = quad(lambda t: math.log(t) ** 2 * math.exp(-t), 0.0, U, limit=400, epsabs=1e-14, epsrel=1e-13)[0] / (-math.expm1(-U))
    return m2 - g0_exact(U) ** 2


P(f"P1_dwarf_chemistry {'MUTATE (k = 0 forced in the quadrature: zeta = 1 imposed)' if MUT else 'normal run'}")
P("kappa = 1/2 FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled. Cold energy, no particle. Not 'theory closed'.")
P("Nothing here says the data favour the framework.  Supply is not mechanism: binding stays open (G2 failed).")
P()

KG = np.concatenate([[0.0], np.logspace(-3, 3, 601)])
UG = np.concatenate([np.logspace(-4, 2, 1201), [np.inf]])
G = np.empty((KG.size, UG.size)); S2 = np.empty_like(G)
for i, k in enumerate(KG):
    G[i], S2[i] = moments(k, UG)
SIG = np.sqrt(S2) / LN10
DEN = np.where(np.isfinite(UG), -np.expm1(-np.where(np.isfinite(UG), UG, 1.0)), 1.0)    # 1 - e^-u
SIG_FMAX = float(SIG[0, -1])                      # family maximum (k = 0, u = inf)
SIG_GMIN = float(SIG.min())                       # smallest width the grid reaches (k = 1000)

# ---------------- K1: quadrature vs exact
errs = []
for U in (1e-3, 0.1, 1.0, 10.0, 60.0, np.inf):
    g, s2 = moments(0.0, [U])
    errs.append(("k0", U, abs(g[0] - g0_exact(U)), abs(s2[0] - s20_exact(U))))
for k in (0.1, 1.0, 10.0, 100.0):
    g, s2 = moments(k, [np.inf])
    ge = float(digamma(1.0) - digamma(1.0 + 1.0 / k) - math.log(k))
    se = float(polygamma(1, 1.0) - polygamma(1, 1.0 + 1.0 / k))
    errs.append((f"k{k:g}", np.inf, abs(g[0] - ge), abs(s2[0] - se)))
mg = max(e[2] for e in errs); ms = max(e[3] for e in errs)
ck("K1", mg <= 1e-6 and ms <= 1e-6, f"max|dg| {mg:.1e} max|ds2| {ms:.1e}", "<=1e-6",
   "quadrature vs exact (k=0 closed form + adaptive quad; u=inf Beta(1,1/k) digamma/trigamma, k 0.1-100)")
for e in errs:
    if e[2] > 1e-6 or e[3] > 1e-6:
        P(f"   K1 row {e[0]} u={e[1]}: |dg| {e[2]:.2e} |ds2| {e[3]:.2e}")
ck("K6", abs(SIG[0].min() - BAND_LO) <= 2e-3 and abs(SIG[0].max() - BAND_HI) <= 2e-3,
   f"k=0 sigma range [{SIG[0].min():.4f}, {SIG[0].max():.4f}] dex", f"[{BAND_LO:.4f}, {BAND_HI:.4f}] +-2e-3",
   "A2 band: zeta = 1, Z0 = 0 family width")
P(f"   grid: {KG.size} k x {UG.size} u; family sigma max {SIG_FMAX:.4f} dex, grid minimum {SIG_GMIN:.4f} dex (k = 1000)")


# ============================================================ E6-equivalent k = 0 solver (independent code, K2)
def u0_solve(ln_zg_y):
    """closed box (eta = 0) truncation u0 with <ln t>_u0 = ln(Z_g/y); None if even u = inf under-produces."""
    if ln_zg_y >= -GAMMA:
        return None
    f = lambda s: g0_exact(math.exp(s)) - ln_zg_y
    if f(5.0) < 0:
        return math.exp(5.0)
    return math.exp(brentq(f, -60.0, 5.0, xtol=1e-14, rtol=1e-14))


def e6_equiv(feh, y_log, Ms, Mg, form):
    """k = 0 leaky box (zeta = 1, Z0 = 0) minimum L at mean [Fe/H]: form 'W2' (gas-free: min over u >= u0) or 'W1'."""
    lzy = feh * LN10 - y_log * LN10
    if Mg > 0:
        r = Ms / Mg
        h = lambda lo: lzy + lo - g0_exact(math.log1p(math.exp(lo) * r))       # lo = ln(1+eta)
        if h(0.0) >= 0:
            return 1.0, True, 0.0
        grid = np.linspace(0.0, 12.0 * LN10, 400)
        hv = [h(x) for x in grid]
        j = next(i for i in range(1, len(grid)) if hv[i] >= 0)
        lo = brentq(h, grid[j - 1], grid[j], xtol=1e-14, rtol=1e-14)
        ope = math.exp(lo)
        return (ope * Ms + Mg) / (Ms + Mg), False, math.log1p(ope * r)
    if form == "W1":
        ope = math.exp(-lzy - GAMMA)
        return (ope, False, np.inf) if ope >= 1 else (1.0, True, np.inf)
    u0 = u0_solve(lzy)
    if u0 is None:
        return 1.0, True, np.inf
    Lf = lambda U: math.exp(-lzy + g0_exact(U)) / (-math.expm1(-U))
    Us = u0 * np.logspace(0, math.log10(max(60.0 / u0, 1.0000001)), 3000)
    vals = np.array([Lf(U) for U in Us]); vinf = math.exp(-lzy - GAMMA)
    i = int(np.argmin(vals))
    if vinf < vals[i]:
        return vinf, False, np.inf
    if i == 0:
        return 1.0 / (-math.expm1(-u0)), False, u0
    a, b = math.log(Us[i - 1]), math.log(Us[min(i + 1, Us.size - 1)])
    r = minimize_scalar(lambda s: Lf(math.exp(s)), bounds=(a, b), method="bounded", options=dict(xatol=1e-12))
    return (float(r.fun), False, math.exp(r.x)) if r.fun < vals[i] else (float(vals[i]), False, float(Us[i]))


# ============================================================ L_MDF: minimum L over the zeta >= 1 family at a width interval
def lmdf(feh, y_log, Ms, Mg, I):
    """min L over allowed (k,u) with sigma_model in I = (lo, hi) dex.  Returns dict(L, flag, k, u, eta, zeta)."""
    y = 10 ** y_log; lnzg = feh * LN10; lzy = lnzg - y_log * LN10
    if I is None:
        return dict(L=None, flag="NOT TESTED")
    lo, hi = I
    if lo > SIG_FMAX:                                   # wholly above the family: k = 0, u = inf (or gas root), flagged
        L0, under, U0 = e6_equiv(feh, y_log, Ms, Mg, "W1")
        return dict(L=L0, flag="UNDER" if under else "ABOVE", k=0.0, u=U0, eta=L0 - 1 if Mg <= 0 else None, zeta=1.0)
    if lo < SIG_GMIN:
        return dict(L=1.0, flag="NO BOUND", k=None, u=None, eta=None, zeta=None)
    best = dict(L=np.inf)
    if Mg <= 0:
        P0 = np.exp(lnzg - G)
        allowed = np.where(KG[:, None] == 0, P0 <= y * (1 + 1e-12), P0 < y)
        L = (y / P0) / DEN[None, :]
        cand = allowed & (SIG >= lo) & (SIG <= hi)
        if cand.any():
            Lc = np.where(cand, L, np.inf); j = np.unravel_index(int(np.argmin(Lc)), Lc.shape)
            ope = y / P0[j]; kk = KG[j[0]]
            best = dict(L=float(Lc[j]), k=float(kk), u=float(UG[j[1]]), eta=float(ope - 1),
                        zeta=1.0 if kk == 0 else float(1 + kk * ope / (ope - 1)))
            # A1 (post-result, reporting only): the valley of near-minimal L (within 1%) -- how well the minimiser's eta, zeta are fixed
            near = cand & (L <= 1.01 * Lc[j]); kn = np.broadcast_to(KG[:, None], L.shape)[near]; opn = (y / P0)[near]
            etan = opn - 1; zn = np.where(kn == 0, 1.0, 1 + kn * opn / np.maximum(etan, 1e-300))
            best.update(eta_1pct=(float(etan.min()), float(etan.max())), zeta_1pct=(float(zn.min()), float(zn.max())))
        u0 = u0_solve(lzy)                               # exact k = 0, eta = 0 boundary point (E6's minimiser)
        if u0 is not None:
            s0 = math.sqrt(moments(0.0, [u0])[1][0]) / LN10
            L0 = 1.0 / (-math.expm1(-u0))
            if lo <= s0 <= hi and L0 < best["L"]:
                best = dict(L=L0, k=0.0, u=u0, eta=0.0, zeta=1.0)
    else:
        r = Ms / Mg; Uf = UG[:-1]
        # A1 bug fix (post-result): a gas-bearing system's family maximum is its own k = 0 gas root (u fixed by the gas), not the
        # gas-free 0.5570; an interval wholly above it is ABOVE (L at the k = 0 root), as the frozen rule says, not UNDER.
        L0g, underg, U0g = e6_equiv(feh, y_log, Ms, Mg, "W1")
        if not underg and lo > math.sqrt(moments(0.0, [U0g])[1][0]) / LN10:
            return dict(L=L0g, flag="ABOVE", k=0.0, u=U0g, eta=None, zeta=1.0)
        for ik, kk in enumerate(KG):
            Gk = G[ik, :-1]
            ope = y * np.exp(Gk) / math.exp(lnzg)
            F = Uf - np.log1p(ope * r)
            idx = np.where((F[:-1] < 0) & (F[1:] >= 0))[0]
            if not idx.size:
                continue
            j = idx[0]; a = F[j] / (F[j] - F[j + 1])
            gst = Gk[j] + a * (Gk[j + 1] - Gk[j]); s2st = S2[ik, j] + a * (S2[ik, j + 1] - S2[ik, j])
            Ust = Uf[j] + a * (Uf[j + 1] - Uf[j])
            opest = y * math.exp(gst) / math.exp(lnzg)
            if opest < 1 or (kk > 0 and opest <= 1):
                continue
            sg = math.sqrt(s2st) / LN10
            if lo <= sg <= hi:
                Lv = (opest * Ms + Mg) / (Ms + Mg)
                if Lv < best["L"]:
                    best = dict(L=float(Lv), k=float(kk), u=float(Ust), eta=float(opest - 1),
                                zeta=1.0 if kk == 0 else float(1 + kk * opest / (opest - 1)))
        L0, under, U0 = e6_equiv(feh, y_log, Ms, Mg, "W1")
        if not under:
            s0 = math.sqrt(moments(0.0, [U0])[1][0]) / LN10
            if lo <= s0 <= hi and L0 < best["L"]:
                best = dict(L=L0, k=0.0, u=U0, eta=None, zeta=1.0)
    if not np.isfinite(best["L"]):
        return dict(L=1.0, flag="UNDER", k=None, u=None, eta=None, zeta=None)
    best["flag"] = "OK"
    return best


# ============================================================ inputs
def rd(path):
    return list(csv.DictReader(open(path)))


LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in rd(os.path.join(DSPH, f)):
        LVD[r["name"]] = r
LVD_BY_KEY = {r["key"]: r for r in LVD.values()}
E6 = {(r["footing"], r["name"]): r for r in rd(E6CSV)}
E3 = {(r["footing"], r["name"]): r for r in rd(E3CSV)}
NAMES = sorted({n for (_, n) in E6})
GEHA = {r["full_name"]: r for r in rd(GEHAF)}
GEHA_ALIAS = {"Coma Berenices": "ComaBer", "Canes Venatici II": "CVn II", "Eridanus IV": "Eridanus 4", "Hercules": "Herc",
              "Pegasus III": "Pegasus 3", "Pegasus IV": "Pegasus 4", "Ursa Major I": "UMa 1", "Ursa Major II": "UMa 2"}   # A1, inventory only


def load_s19():
    lines = open(S19F).read().splitlines()
    ref = next(l for l in lines if l.strip().startswith("Sculptor "))
    ends = [m.end() for m in re.finditer(r"\S+", ref)]
    out = {}
    for l in lines:
        toks = [(m.group(), m.end()) for m in re.finditer(r"\S+", l)]
        if len(toks) < 5 or not re.match(r"^[A-Za-z]", toks[0][0]) or not re.match(r"^-?\d", toks[1][0]):
            continue
        cols = {}
        for tk, e in toks[1:]:
            c = int(np.argmin([abs(e - x) for x in ends]))
            if abs(ends[c] - e) <= 3 and c not in cols:
                cols[c] = tk
        name = toks[0][0].replace("~", " ")
        sig = fl(cols.get(20)); ep = fl(cols.get(21)); em = fl(cols.get(22)); up = cols.get(23, "0")
        if sig is None:
            continue
        isul = up.startswith("1")
        out[name] = dict(sig=sig, ep=None if isul or ep is None or ep < 0 else ep,
                         em=None if isul or em is None or em > 0 else -em, ul=sig if isul else None)
    return out


S19 = load_s19()


def lvd_sigma(r):
    """LVD width: spectroscopic (central, em, ep) or UL; photometric fallback flagged."""
    s = fl(r.get("metallicity_spectroscopic_sigma")); ul = fl(r.get("metallicity_spectroscopic_sigma_ul"))
    if s is not None:
        return dict(sig=s, em=fl(r.get("metallicity_spectroscopic_sigma_em")), ep=fl(r.get("metallicity_spectroscopic_sigma_ep")),
                    ul=None, src="LVD-spec", ref=r.get("ref_metallicity_spectroscopic", ""))
    if ul is not None:
        return dict(sig=None, em=None, ep=None, ul=ul, src="LVD-spec-UL", ref=r.get("ref_metallicity_spectroscopic", ""))
    s = fl(r.get("metallicity_photometric_sigma"))
    if s is not None:
        return dict(sig=s, em=fl(r.get("metallicity_photometric_sigma_em")), ep=fl(r.get("metallicity_photometric_sigma_ep")),
                    ul=None, src="LVD-PHOT", ref=r.get("ref_metallicity_photometric", ""))
    return None


def width_class(w):
    if w is None:
        return "NONE"
    if w.get("sig") is None:
        return "NARROW" if w["ul"] < BAND_LO else "UNDETERMINED"
    s, em, ep = w["sig"], w.get("em"), w.get("ep")
    if em is None or ep is None:
        return ("NARROW" if s < BAND_LO else "BROAD" if s > BAND_HI else "CONSISTENT") + "(no err)"
    if s + 2 * ep < BAND_LO:
        return "NARROW"
    if s - 2 * em > BAND_HI:
        return "BROAD"
    return "CONSISTENT"


def intervals(w):
    if w is None or w.get("sig") is None:
        return None, None, None
    s, em, ep = w["sig"], w.get("em"), w.get("ep")
    I0 = (s - 0.005, s + 0.005)
    if em is None or ep is None:
        return I0, I0, I0
    return I0, (max(0.0, s - 2 * em), s + 2 * ep), (s + 2 * ep - 0.005, s + 2 * ep + 0.005)


# ============================================================ Walker 2023 per-star: parse, combine, membership
WCOL = dict(Target=(13, 28, str), Gaia=(72, 90, str), pmRA=(188, 195, float), pmDE=(197, 204, float), epmRA=(206, 210, float),
            epmDE=(212, 216, float), plx=(218, 224, float), eplx=(226, 232, float), ra=(234, 248, float), dec=(250, 264, float),
            v=(700, 706, float), ev=(708, 711, float), logg=(754, 758, float), elogg=(760, 764, float), feh=(779, 784, float),
            efeh=(786, 790, float), mgfe=(806, 812, float), emgfe=(814, 819, float), goodN=(689, 690, int),
            fchi=(846, 846, int), fc=(848, 848, int), rrl=(874, 874, int), agn=(876, 876, int))


def wget(line, key):
    a, b, typ = WCOL[key]; s = line[a - 1:b].strip()
    if not s:
        return None
    try:
        v = typ(s); return v if typ is str or math.isfinite(v) else None
    except Exception:
        return None


def walker_stars():
    per = {}
    for fn in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"):
        seen = set()
        with gzip.open(os.path.join(WALK, fn), "rt") as fh:
            for line in fh:
                tg = wget(line, "Target"); gid = wget(line, "Gaia")
                if tg is None or gid is None or (tg, gid) in seen:
                    continue
                if (wget(line, "goodN") or 0) < 1:
                    continue
                seen.add((tg, gid))
                d = {k: wget(line, k) for k in WCOL}
                per.setdefault((tg, gid), []).append(d)
    stars = []
    for (tg, gid), rows in per.items():
        s = dict(rows[0])
        for q, e in (("v", "ev"), ("feh", "efeh"), ("mgfe", "emgfe"), ("logg", "elogg")):
            ok = [(r[q], r[e]) for r in rows if r[q] is not None and r[e] is not None and r[e] > 0]
            if ok:
                w = np.array([1 / e ** 2 for _, e in ok]); x = np.array([v for v, _ in ok])
                s[q] = float((w * x).sum() / w.sum()); s[e] = float(1 / math.sqrt(w.sum()))
            else:
                s[q] = None; s[e] = None
        for f in ("fchi", "fc", "rrl", "agn"):
            s[f] = max((r[f] or 0) for r in rows)
        s["Target"] = tg; s["nfiles"] = len(rows)
        stars.append(s)
    return stars


def members(stars, lv):
    v0 = fl(lv["vlos_systemic"]); sgl = fl(lv["vlos_sigma"]) or fl(lv["vlos_sigma_ul"]) or 5.0
    sgl = max(sgl, 2.0); d = fl(lv["distance"])
    pmr, pmd = fl(lv["pmra"]), fl(lv["pmdec"])
    epr = np.nanmean([fl(lv["pmra_em"]) or np.nan, fl(lv["pmra_ep"]) or np.nan])
    epd = np.nanmean([fl(lv["pmdec_em"]) or np.nan, fl(lv["pmdec_ep"]) or np.nan])
    epr = 0.0 if not np.isfinite(epr) else epr; epd = 0.0 if not np.isfinite(epd) else epd
    ra0, de0 = fl(lv["ra"]), fl(lv["dec"]); rh = fl(lv["rhalf"]); ell = fl(lv["ellipticity"]) or 0.0
    pa = math.radians(fl(lv["position_angle"]) or 0.0)
    s_int2 = (sgl / (4.74 * d)) ** 2
    out = []
    for s in stars:
        if s["v"] is None or s["ev"] is None or s["logg"] is None or s["pmRA"] is None or s["pmDE"] is None:
            continue
        if s["rrl"] or s["agn"] or s["fc"] or s["fchi"] or s["logg"] >= 4.0:
            continue
        if abs(s["v"] - v0) >= 3 * math.sqrt(sgl ** 2 + s["ev"] ** 2):
            continue
        sr2 = (s["epmRA"] or 0) ** 2 + 0.05 ** 2 + epr ** 2 + s_int2
        sd2 = (s["epmDE"] or 0) ** 2 + 0.05 ** 2 + epd ** 2 + s_int2
        if (s["pmRA"] - pmr) ** 2 / sr2 + (s["pmDE"] - pmd) ** 2 / sd2 >= 9.21:
            continue
        if s["plx"] is not None and s["eplx"] is not None:
            if abs(s["plx"] - 1.0 / d) >= 3 * math.sqrt(s["eplx"] ** 2 + 0.03 ** 2):
                continue
        dx = (s["ra"] - ra0) * math.cos(math.radians(de0)) * 60.0; dy = (s["dec"] - de0) * 60.0
        xm = dx * math.sin(pa) + dy * math.cos(pa); ym = dx * math.cos(pa) - dy * math.sin(pa)
        if math.sqrt(xm ** 2 + (ym / (1.0 - ell)) ** 2) > 5.0 * rh:
            continue
        out.append(s)
    return out


SGRID = np.arange(0.0, 2.0001, 0.001)


def gmle(x, e):
    """Gaussian intrinsic sigma with known per-star errors; profile Delta(-2lnL) = 1 interval."""
    s2 = SGRID[:, None] ** 2 + e[None, :] ** 2
    w = 1.0 / s2; mu = (w * x).sum(1) / w.sum(1)
    m2 = (np.log(s2) + (x[None, :] - mu[:, None]) ** 2 / s2).sum(1)
    i = int(np.argmin(m2)); ok = m2 <= m2[i] + 1.0
    return float(SGRID[i]), float(SGRID[i] - SGRID[ok].min()), float(SGRID[ok].max() - SGRID[i]), float(mu[i])


# ---------------- P-S: k = 0 family shape test (PIT + Anderson-Darling, parametric bootstrap)
WG0, DW = -8.0, 0.005
WGRID = np.arange(WG0, 4.5 + 1e-9, DW)
NF = 8192
UFIT = np.concatenate([np.logspace(-3, 2, 41), [np.inf]])
NUF = np.fft.rfftfreq(NF, d=DW)


def base_density(U):
    t = 10.0 ** WGRID
    d = LN10 * t * np.exp(-t)
    if np.isfinite(U):
        d[t > U] = 0.0
    return d / (d.sum() * DW)


BASEF = [np.fft.rfft(base_density(U), NF) for U in UFIT]


def ad_stat(uu):
    uu = np.sort(np.clip(uu, 1e-12, 1 - 1e-12)); n = uu.size; i = np.arange(1, n + 1)
    return float(-n - np.sum((2 * i - 1) * (np.log(uu) + np.log(1 - uu[::-1]))) / n)


def shape_test(x, e, rng):
    D = np.empty((UFIT.size, x.size, WGRID.size), dtype=np.float32)        # A1: float32, in place (memory)
    for ju in range(UFIT.size):
        for i in range(x.size):
            D[ju, i] = np.fft.irfft(BASEF[ju] * np.exp(-2.0 * (math.pi * NUF * e[i]) ** 2), NF)[:WGRID.size]
    np.clip(D, 1e-30, None, out=D)
    C = np.cumsum(D, axis=2, dtype=np.float32); C *= DW; np.clip(C, 0.0, 1.0, out=C)
    rows = np.arange(x.size)

    def interp(A, ju, wq):
        f = np.clip((wq - WG0) / DW, 0, WGRID.size - 1.000001); i0 = np.floor(f).astype(int); fr = f - i0
        return A[ju, rows[None, :], i0] * (1 - fr) + A[ju, rows[None, :], i0 + 1] * fr

    def fit(xx):
        mx = xx.mean(); LPG = np.arange(mx - 1.0, mx + 4.0 + 1e-9, 0.01)
        best = (-np.inf, 0, 0.0)
        for ju in range(UFIT.size):
            ll = np.log(np.clip(interp(D, ju, xx[None, :] - LPG[:, None]), 1e-300, None)).sum(1)
            j = int(np.argmax(ll))
            if ll[j] > best[0]:
                best = (float(ll[j]), ju, float(LPG[j]))
        _, ju, lp = best
        pit = interp(C, ju, (xx - lp)[None, :])[0]
        return ju, lp, ad_stat(pit)
    ju, lp, A_obs = fit(x)
    U = UFIT[ju]; nb = 0
    for _ in range(NBOOT_AD):
        r = rng.random(x.size)
        t = -np.log1p(-r * (-math.expm1(-U))) if np.isfinite(U) else -np.log1p(-r)
        xb = lp + np.log10(t) + e * rng.standard_normal(x.size)
        nb += fit(xb)[2] >= A_obs
    return dict(u=float(U), log_p0=lp, AD=A_obs, p=(1 + nb) / (1 + NBOOT_AD))


def mgfe_test(fe, mg, emg):
    w = 1 / emg ** 2; m = float((w * mg).sum() / w.sum())
    chi = float((w * (mg - m) ** 2).sum() / max(mg.size - 1, 1)); infl = math.sqrt(max(1.0, chi))
    em = infl / math.sqrt(w.sum())
    X = np.vstack([np.ones_like(fe), fe]).T; A = X.T @ (w[:, None] * X); cov = np.linalg.inv(A)
    b = cov @ (X.T @ (w * mg)); res = float((w * (mg - X @ b) ** 2).sum() / max(mg.size - 2, 1))
    sb = math.sqrt(cov[1, 1] * max(1.0, res))
    if b[1] + 2 * sb < 0:
        cls = "DECLINE"
    elif m - 2 * em >= 0.15:
        cls = "PLATEAU"
    elif m + 2 * em < 0.15:
        cls = "LOW"
    else:
        cls = "UNDETERMINED"
    lo = LOGY_ALPHA[0] - (m + 2 * em); hi = LOGY_ALPHA[1] - (m - 2 * em)
    ycls = "BELOW" if hi < -0.5 else "ABOVE" if lo > 0.1 else "IN"
    return dict(mean=m, err=em, slope=float(b[1]), slope_err=sb, cls=cls, logyFe_alpha=(lo, hi), ycls=ycls, n=int(mg.size))


# ============================================================ K2: E6 reproduced by independent k = 0 code
def mass_g(name):
    mhi = fl(LVD[name].get("mass_HI")) if name in LVD else None
    return GAS_FAC * 10 ** mhi if mhi is not None else 0.0


worst = 0.0; nk2 = 0
for n in NAMES:
    r = E6.get(("canonical", n))
    if r is None or fl(r["feh"]) is None or fl(r["Lmin_-0.5|W2"]) is None:
        continue
    feh = fl(r["feh"]); Ms = 10 ** fl(r["logMstar"]); Mg = mass_g(n)
    a = e6_equiv(feh, -0.5, Ms, Mg, "W2")[0]; b = e6_equiv(feh, 0.1, Ms, Mg, "W1")[0]
    worst = max(worst, abs(a / fl(r["Lmin_-0.5|W2"]) - 1), abs(b / fl(r["Lmin_+0.1|W1"]) - 1)); nk2 += 1
ck("K2", worst <= 1e-3 and nk2 > 0, f"max rel {worst:.1e} over {nk2} systems", "<=1e-3",
   "E6 Lmin(-0.5,W2) and Lmin(+0.1,W1) reproduced by independent k = 0 code")

# ---------------- K3: direction of pre-enrichment (A3)
def lmin_pre(feh, y_log, z0f):
    """E6's mean-only zeta = 1 minimum with pre-enrichment Z0 = z0f * Z_g (min over u; p <= y)."""
    zg = 10 ** feh; y = 10 ** y_log; Z0 = z0f * zg; best = np.inf
    for U in np.concatenate([np.logspace(-4, math.log10(60.0), 300), [np.inf]]):
        Ue = UINF if not np.isfinite(U) else U
        t = Ue * QW ** 4; wt = np.exp(-t) * 4 * Ue * QW ** 3 * QWW; wt = wt / wt.sum()
        m = lambda p: float((wt * np.log(Z0 + p * t)).sum()) - math.log(zg)
        if m(y) < 0:
            continue
        p = brentq(m, 1e-14, y, xtol=1e-16, rtol=1e-13) if m(1e-14) < 0 else 1e-14
        best = min(best, (y / p) / (1.0 if not np.isfinite(U) else -math.expm1(-U)))
    return best


k3i = [(feh, lmin_pre(feh, -0.5, 0.0), lmin_pre(feh, -0.5, 0.3)) for feh in (-2.0, -2.5, -3.0)]
k3ii = []
for z0p in (1.0, 3.0, 10.0):
    for U in (0.1, 1.0, np.inf):
        Ue = UINF if not np.isfinite(U) else U
        t = Ue * QW ** 4; wt = np.exp(-t) * 4 * Ue * QW ** 3 * QWW; wt = wt / wt.sum()
        lz = np.log(z0p + t); mlz = float((wt * lz).sum()); sd = math.sqrt(float((wt * (lz - mlz) ** 2).sum())) / LN10
        Ltrue = 30.0 / (1.0 if not np.isfinite(U) else -math.expm1(-U))
        res = lmdf(mlz / LN10, math.log10(30.0), 1.0, 0.0, (sd - 0.005, sd + 0.005))
        k3ii.append((z0p, U, sd, Ltrue, res["L"], res["flag"]))
ok3 = all(b > a for _, a, b in k3i) and all(r[4] <= r[3] for r in k3ii)
ck("K3", ok3, f"(i) L_min Z0=0 -> 0.3Zg: " + ", ".join(f"{f:+.1f}: {a:.1f}->{b:.1f}" for f, a, b in k3i)
   + f"; (ii) L_MDF/L_true max {max(r[4] / r[3] for r in k3ii):.3f}", "(i) rises x3; (ii) <=1 x9",
   "pre-enrichment raises L; the zeta reading is the conservative one")

# ---------------- K4: Gaussian MLE recovers the family's width
rngk4 = np.random.default_rng(SEED + 4)
jA = int(np.argmin(np.abs(SIG[1:, -1] - 0.25))) + 1          # k > 0, u = inf, sigma ~ 0.25
jB = int(np.argmin(np.abs(SIG[0, :-1] - 0.45)))               # k = 0, finite u, sigma ~ 0.45
k4 = []
for (kk, U, smod) in ((KG[jA], np.inf, SIG[jA, -1]), (0.0, UG[jB], SIG[0, jB])):
    rat = []
    for _ in range(300):
        r = rngk4.random(30)
        t = -np.log1p(-r * (-math.expm1(-U))) if np.isfinite(U) else -np.log1p(-r)
        x = lnphi(kk, t) / LN10 + 0.3 * rngk4.standard_normal(30)
        rat.append(gmle(x, np.full(30, 0.3))[0] / smod)
    k4.append((kk, U, smod, float(np.median(rat))))
ck("K4", all(abs(m - 1) <= 0.15 for *_, m in k4), ", ".join(f"sigma_model {s:.3f}: median ratio {m:.3f}" for _, _, s, m in k4),
   "|ratio-1|<=0.15", "Gaussian intrinsic-sigma estimator vs the skewed family (N 30, err 0.3 dex)")
# A1 (post-result diagnostic, not a check): where the K4 bias comes from, and its sign for the verdict
k4d = []
for (kk, U, smod) in ((KG[jA], np.inf, SIG[jA, -1]), (0.0, UG[jB], SIG[0, jB])):
    for (N, err) in ((30, 0.3), (100, 0.3), (30, 0.15)):
        rat = []
        for _ in range(300):
            r = rngk4.random(N)
            t = -np.log1p(-r * (-math.expm1(-U))) if np.isfinite(U) else -np.log1p(-r)
            x = lnphi(kk, t) / LN10 + err * rngk4.standard_normal(N)
            rat.append(gmle(x, np.full(N, err))[0] / smod)
        k4d.append((float(smod), N, err, float(np.median(rat)), float(np.mean(rat))))
P("   A1 K4 diagnostic (post-result): " + "; ".join(f"sig {s:.2f} N {N} e {e:.2f}: median {m:.2f} mean {a:.2f}" for s, N, e, m, a in k4d))
P("   (a low-biased width maps to a lower L_MDF and a higher q: the bias pushes the graded q toward shortfall, i.e. conservative)")

# ============================================================ Step 1: inventory (+ Walker per-star analysis)
P()
P("== Step 1: inventory (46 systems: 45 canonical + Andromeda XXVIII alt) ==")
STARS = walker_stars()
TARGETS = sorted({s["Target"] for s in STARS})
CFG51 = {r["name"]: r for r in csv.DictReader(open(CFG51F), delimiter="\t")}
WRES = {}
rng_ad = np.random.default_rng(SEED + 7)
k5 = []
for tg in TARGETS:
    lv = LVD_BY_KEY.get(tg.lower())
    if lv is None or lv["name"] not in NAMES:
        continue
    nm = lv["name"]
    mem = members([s for s in STARS if s["Target"] == tg], lv)
    fe = [(s["feh"], s["efeh"]) for s in mem if s["feh"] is not None and s["efeh"] is not None and s["efeh"] > 0]
    mg = [(s["feh"], s["mgfe"], s["emgfe"]) for s in mem if s["mgfe"] is not None and s["emgfe"] is not None and s["emgfe"] > 0
          and s["feh"] is not None]
    W = dict(target=tg, N_mem=len(mem), N_Fe=len(fe), N_Mg=len(mg), cfg51_n=CFG51.get(tg, {}).get("n_members"))
    if mem:
        W["v_med"] = float(np.median([s["v"] for s in mem])); W["dv"] = W["v_med"] - fl(lv["vlos_systemic"])
        if len(mem) >= 10:
            k5.append((nm, W["dv"]))
    if len(fe) >= 1:
        x = np.array([a for a, _ in fe]); e = np.array([b for _, b in fe])
        W["feh_mean"] = float(x.mean()); W["N_EMP"] = int(np.sum(x + 2 * e < -3.0))
        W["e_med"] = float(np.median(e))
    if len(fe) >= 10:
        s, em, ep, mu = gmle(x, e)
        W.update(sig=s, em=em if s - em > 0 else s, ep=ep, mu=mu)
        W["shape"] = shape_test(x, e, rng_ad)
    if len(mg) >= 5:
        W["mg"] = mgfe_test(np.array([a for a, _, _ in mg]), np.array([b for _, b, _ in mg]), np.array([c for _, _, c in mg]))
    WRES[nm] = W
ck("K5", len(k5) > 0 and all(abs(d) <= 3.0 for _, d in k5), f"max |dv| {max(abs(d) for _, d in k5):.2f} km/s over {len(k5)} systems",
   "<=3 km/s", "Walker membership: member median velocity vs LVD systemic (N_mem >= 10)")

INV = []
for n in NAMES:
    lv = LVD.get(n, {}); w = lvd_sigma(lv) if lv else None; s19 = S19.get(n); gh = GEHA.get(GEHA_ALIAS.get(n, n), {}); W = WRES.get(n, {})
    INV.append(dict(name=n, host=(E6.get(("canonical", n)) or E6.get(("alt", n)))["host"], feh_LVD=fl(lv.get("metallicity")),
                    feh_type=lv.get("metallicity_type", ""), sig_LVD=w and w["sig"], sig_LVD_em=w and w["em"], sig_LVD_ep=w and w["ep"],
                    sig_LVD_ul=w and w["ul"], sig_LVD_src=w and w["src"], sig_LVD_ref=w and w["ref"],
                    sig_S19=s19 and (s19["sig"] if s19["ul"] is None else None), sig_S19_em=s19 and s19["em"],
                    sig_S19_ep=s19 and s19["ep"], sig_S19_ul90=s19 and s19["ul"],
                    N_Geha=fl(gh.get("N_stars")), sig_Geha=(fl(gh.get("sigFeH")) if fl(gh.get("sigFeH")) not in (None, -999) else None),
                    sig_Geha_ul95=(fl(gh.get("sigFeH95")) if fl(gh.get("sigFeH95")) not in (None, -999) else None),
                    walker_target=W.get("target"), N_Walker_mem=W.get("N_mem"), N_Walker_Fe=W.get("N_Fe"),
                    sig_Walker=W.get("sig"), sig_Walker_em=W.get("em"), sig_Walker_ep=W.get("ep"),
                    feh_Walker_mean=W.get("feh_mean"), e_feh_Walker_median=W.get("e_med"), N_Walker_Mg=W.get("N_Mg"),
                    MgFe_mean=W.get("mg", {}).get("mean"), MgFe_err=W.get("mg", {}).get("err"), N_EMP=W.get("N_EMP"),
                    CFG51_n_members=W.get("cfg51_n")))
with open(os.path.join(HERE, f"p1_inventory{SFX}.csv"), "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(INV[0].keys())); wr.writeheader(); wr.writerows(INV)
nfe = sum(1 for r in INV if r["feh_LVD"] is not None)
P(f"   LVD mean [Fe/H]: {nfe}/46; LVD sigma central {sum(1 for r in INV if r['sig_LVD'] is not None)} "
  f"(spec {sum(1 for r in INV if r['sig_LVD_src'] == 'LVD-spec')}, phot {sum(1 for r in INV if r['sig_LVD_src'] == 'LVD-PHOT')}), "
  f"LVD UL only {sum(1 for r in INV if r['sig_LVD_ul'] is not None)}; S19 sigma {sum(1 for r in INV if r['sig_S19'] is not None)} "
  f"(+{sum(1 for r in INV if r['sig_S19_ul90'] is not None)} UL); Geha N_stars {sum(1 for r in INV if r['N_Geha'] is not None)}")
P(f"   Walker 2023 per-star: {len(WRES)} E3 systems with a target; N_Fe >= 10 in "
  f"{sum(1 for W in WRES.values() if W['N_Fe'] >= 10)}; N_Mg >= 5 in {sum(1 for W in WRES.values() if W['N_Mg'] >= 5)}")
P(f"   {'system':18s} {'N_mem':>5s} {'N_Fe':>4s} {'(CFG51)':>7s} {'e_med':>5s} {'sig_W':>13s} {'LVD':>13s} {'S19':>13s} {'Mg/Fe':>12s} N_EMP")
for n, W in sorted(WRES.items()):
    r = next(x for x in INV if x["name"] == n)
    sw = f"{W['sig']:.2f}-{W['em']:.2f}+{W['ep']:.2f}" if "sig" in W else "-"
    sl = f"{r['sig_LVD']:.2f}" if r["sig_LVD"] is not None else (f"<{r['sig_LVD_ul']:.2f}" if r["sig_LVD_ul"] else "-")
    ss = f"{r['sig_S19']:.2f}" if r["sig_S19"] is not None else (f"<{r['sig_S19_ul90']:.2f}" if r["sig_S19_ul90"] else "-")
    mgs = f"{W['mg']['mean']:+.2f}+-{W['mg']['err']:.2f}" if "mg" in W else "-"
    P(f"   {n:18s} {W['N_mem']:5d} {W['N_Fe']:4d} {str(W['cfg51_n']):>7s} {W.get('e_med', float('nan')):5.2f} {sw:>13s} {sl:>13s} "
      f"{ss:>13s} {mgs:>12s} {W.get('N_EMP', '-')}")

# ============================================================ Step 2: premise tests
P()
P("== Step 2: premise tests ==")
WCLS = {}
for n in NAMES:
    r = next(x for x in INV if x["name"] == n)
    lv = LVD.get(n); wl = lvd_sigma(lv) if lv else None
    s19 = S19.get(n); W = WRES.get(n, {})
    ws = (dict(sig=s19["sig"], em=s19["em"], ep=s19["ep"], ul=None) if s19 and s19["ul"] is None else
          dict(sig=None, ul=s19["ul"]) if s19 else None)
    ww = dict(sig=W["sig"], em=W["em"], ep=W["ep"], ul=None) if "sig" in W else None
    WCLS[n] = dict(LVD=width_class(wl), S19=width_class(ws), Walker=width_class(ww))
for src in ("LVD", "S19", "Walker"):
    cnt = {}
    for n in NAMES:
        c = WCLS[n][src].replace("(no err)", "")
        cnt[c] = cnt.get(c, 0) + 1
    nar = [n for n in NAMES if WCLS[n][src].startswith("NARROW")]
    P(f"   P-W {src:6s}: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())) + f"   NARROW: {', '.join(nar) if nar else '-'}")
P(f"   (band [{BAND_LO:.4f}, {BAND_HI:.4f}] dex; NARROW = sigma + 2ep below it: the zeta = 1, Z0 = 0, no-inflow box cannot make it)")
nps = 0; psf = []
for n, W in sorted(WRES.items()):
    if "shape" in W:
        nps += 1
        if W["shape"]["p"] < 0.05:
            psf.append(n)
        P(f"   P-S {n:18s} N_Fe {W['N_Fe']:3d}  best k=0 fit u {W['shape']['u']:.3g}  AD {W['shape']['AD']:.2f}  p {W['shape']['p']:.3f}"
          f"  {'FAIL' if W['shape']['p'] < 0.05 else 'pass'}")
P(f"   P-S: {len(psf)}/{nps} FAIL (p < 0.05){': ' + ', '.join(psf) if psf else ''}")
for n, W in sorted(WRES.items()):
    if "mg" in W:
        m = W["mg"]
        P(f"   P-A {n:18s} N_Mg {m['n']:3d}  <[Mg/Fe]> {m['mean']:+.2f}+-{m['err']:.2f}  slope {m['slope']:+.2f}+-{m['slope_err']:.2f}"
          f"  {m['cls']:12s} alpha-anchored log y_Fe [{m['logyFe_alpha'][0]:+.2f}, {m['logyFe_alpha'][1]:+.2f}] {m['ycls']}")
P("   P-0: pre-enrichment raises L (K3); N_EMP ([Fe/H] + 2e < -3) per Walker system listed in the inventory table above.")

# ============================================================ Step 3: supply recomputed from the MDF
P()
P("== Step 3: supply from the MDF (L_MDF = min L over the zeta >= 1 family at the observed width; q = L_req / L_MDF) ==")


def width_for(n, mode):
    """mode LVD (primary), R1 (S19 measured sigma replaces LVD's), R2 (Walker per-star sigma replaces LVD's, N_Fe >= 10)."""
    lv = LVD.get(n); w = lvd_sigma(lv) if lv else None
    if mode == "R1" and n in S19 and S19[n]["ul"] is None:
        s = S19[n]; w = dict(sig=s["sig"], em=s["em"], ep=s["ep"], ul=None, src="S19")
    if mode == "R2" and "sig" in WRES.get(n, {}):
        W = WRES[n]; w = dict(sig=W["sig"], em=W["em"], ep=W["ep"], ul=None, src="Walker")
    return w


LCACHE = {}


def lsys(n, mode):
    key = (n, mode)
    if key in LCACHE:
        return LCACHE[key]
    lv = LVD.get(n); feh = fl(lv.get("metallicity")) if lv else None
    row = E6.get(("canonical", n)) or E6.get(("alt", n))
    Ms = 10 ** fl(row["logMstar"]); Mg = mass_g(n)
    w = width_for(n, mode)
    I0, I2, Ihi = intervals(w)
    res = dict(feh=feh, w=w, Ms=Ms, Mg=Mg)
    if feh is None or I0 is None:
        res["tested"] = False
    else:
        res["tested"] = True
        for y in LOGY:
            res[("I0", y)] = lmdf(feh, y, Ms, Mg, I0)
        res[("I2", -0.5)] = lmdf(feh, -0.5, Ms, Mg, I2)
        res[("Ihi", 0.1)] = lmdf(feh, 0.1, Ms, Mg, Ihi)
        res["E6_W2_-0.5"] = e6_equiv(feh, -0.5, Ms, Mg, "W2")[0]
    LCACHE[key] = res
    return res


def boot(x, rng):
    x = np.asarray(x, float); idx = rng.integers(0, x.size, size=(NBOOT, x.size))
    b = np.median(x[idx], axis=1)
    return float(np.median(x)), float(np.percentile(b, 16)), float(np.percentile(b, 84))


def qtable(mode, foot, acc, y, I="I0"):
    out = []
    for n in NAMES:
        r = E6.get((foot, n))
        if r is None:
            continue
        L = lsys(n, mode)
        if not L["tested"]:
            continue
        Lr = fl(r[f"L_req_{acc}"])
        out.append((n, Lr / L[(I, y)]["L"]))
    return out


def classify(mode):
    rng = np.random.default_rng(SEED + {"LVD": 0, "R1": 1, "R2": 2}[mode])
    st = {}
    for foot in FOOTS:
        qc = [q for _, q in qtable(mode, foot, "F2", -0.5)]
        ql = [q for _, q in qtable(mode, foot, "F2", 0.1)]
        st[foot] = dict(N=len(qc), cons=boot(qc, rng), least=boot(ql, rng))
    conf = all(st[f]["cons"][0] <= 1 and st[f]["cons"][2] <= 1 for f in FOOTS)
    fail = all(st[f]["least"][0] > 1 and st[f]["least"][1] > 1 for f in FOOTS)
    return ("SUPPLY CONFIRMED" if conf else "SUPPLY FAILS" if fail else "UNDECIDABLE"), st


RES = {}
P(f"   {'':10s} {'':3s} {'N':>3s} " + "  ".join(f"{'logy ' + format(y, '+.1f'):>21s}" for y in LOGY) + f"  {'I2 (2sig-low width) -0.5':>26s}")
rngt = np.random.default_rng(SEED + 11)
for foot in FOOTS:
    for acc in ("F2", "F1"):
        cells = []
        for y in LOGY:
            q = [v for _, v in qtable("LVD", foot, acc, y)]
            cells.append(boot(q, rngt))
        qi2 = [v for _, v in qtable("LVD", foot, acc, -0.5, "I2")]
        c2 = boot(qi2, rngt)
        RES[f"{foot}_{acc}"] = dict(N=len(qi2), **{f"I0_{y:+.1f}": cells[i] for i, y in enumerate(LOGY)}, **{"I2_-0.5": c2})
        P(f"   {foot:10s} {acc:3s} {len(qi2):3d} " + "  ".join(f"{m:6.3f} [{a:5.3f},{b:5.3f}]" for m, a, b in cells)
          + f"  {c2[0]:7.3f} [{c2[1]:5.3f},{c2[2]:5.3f}]")
P("   (median q [bootstrap 16-84%]; I0 = central LVD width; graded cell: F2, logy -0.5, I0; E6's same-set ratio for comparison below)")
for foot in FOOTS:
    q6 = [fl(E6[(foot, n)]["L_req_F2"]) / lsys(n, "LVD")["E6_W2_-0.5"] for n in NAMES
          if (foot, n) in E6 and lsys(n, "LVD")["tested"]]
    P(f"   E6 premise (zeta = 1, mean only) on the same {len(q6)} systems, {foot} F2 logy -0.5 W2: median q {np.median(q6):.3f}")
    RES[f"{foot}_F2_E6premise_sameset"] = float(np.median(q6))

CLS = {}
for mode in ("LVD", "R1", "R2"):
    c, st = classify(mode)
    CLS[mode] = dict(cls=c, stats=st)
    P(f"   class [{mode:3s}]: {c:17s} " + "; ".join(
        f"{f} N {st[f]['N']} cons {st[f]['cons'][0]:.3f} [{st[f]['cons'][1]:.3f},{st[f]['cons'][2]:.3f}] "
        f"least {st[f]['least'][0]:.3f} [{st[f]['least'][1]:.3f},{st[f]['least'][2]:.3f}]" for f in FOOTS))

# ---------------- per system table
PER = []
for foot in FOOTS:
    for n in NAMES:
        r = E6.get((foot, n))
        if r is None:
            continue
        L = lsys(n, "LVD"); w = L["w"]
        row = dict(footing=foot, name=n, feh=L["feh"], sig_src=w and w.get("src"), sig=w and w.get("sig"), sig_em=w and w.get("em"),
                   sig_ep=w and w.get("ep"), sig_ul=w and w.get("ul"), PW_LVD=WCLS[n]["LVD"], PW_S19=WCLS[n]["S19"],
                   PW_Walker=WCLS[n]["Walker"], L_req_F1=fl(r["L_req_F1"]), L_req_F2=fl(r["L_req_F2"]), tested=L["tested"])
        if L["tested"]:
            c = L[("I0", -0.5)]
            row.update(L_E6_W2=L["E6_W2_-0.5"], L_MDF_I0_m05=c["L"], flag_I0=c["flag"], k=c.get("k"), u=c.get("u"), eta=c.get("eta"),
                       zeta_MDF=c.get("zeta"), L_MDF_I0_m02=L[("I0", -0.2)]["L"], L_MDF_I0_p01=L[("I0", 0.1)]["L"],
                       L_MDF_I2_m05=L[("I2", -0.5)]["L"], flag_I2=L[("I2", -0.5)]["flag"], L_MDF_hi_p01=L[("Ihi", 0.1)]["L"],
                       eta_1pct=c.get("eta_1pct"), zeta_1pct=c.get("zeta_1pct"))
            Lr2 = row["L_req_F2"]; Lr1 = row["L_req_F1"]
            row["q_F2"] = Lr2 / c["L"]; row["q_F1"] = Lr1 / c["L"]
            row["q_F2_p01"] = Lr2 / L[("I0", 0.1)]["L"]; row["q_F2_I2"] = Lr2 / L[("I2", -0.5)]["L"]
            row["q_F2_E6premise"] = Lr2 / L["E6_W2_-0.5"]
            row["SHORT"] = row["q_F2"] > 1
            row["robust_supply"] = row["q_F2_I2"] <= 1
            e3 = E3.get((foot, n)); qlo = fl(e3["q_fret010_p2p5"]) if e3 else None
            row["robust_shortfall_F1"] = (qlo * 10.0 / L[("Ihi", 0.1)]["L"] > 1) if qlo is not None else None
            row["f_break"] = (1 - row["q_F2"]) if row["q_F2"] < 1 else 0.0
            for mode in ("R1", "R2"):
                Lm = lsys(n, mode)
                row[f"q_F2_{mode}"] = Lr2 / Lm[("I0", -0.5)]["L"] if Lm["tested"] else None
        PER.append(row)
keys = []
for r in PER:
    for k in r:
        if k not in keys:
            keys.append(k)
with open(os.path.join(HERE, f"p1_per_system{SFX}.csv"), "w", newline="") as fh:
    wr = csv.DictWriter(fh, fieldnames=keys); wr.writeheader(); wr.writerows(PER)

P()
for foot in FOOTS:
    T = [r for r in PER if r["footing"] == foot and r["tested"]]
    sh = [r["name"] for r in T if r["SHORT"]]
    rs = [r["name"] for r in T if r["robust_shortfall_F1"]]
    sup = sum(1 for r in T if r["robust_supply"])
    nt = [r["name"] for r in PER if r["footing"] == foot and not r["tested"]]
    P(f"   {foot}: tested {len(T)}; SHORT (F2, -0.5, I0) {len(sh)}: {', '.join(sh)}")
    P(f"   {foot}: robust supply (q <= 1 at the 2sig-low width) {sup}/{len(T)}; robust shortfall (F1 2.5% need, +0.1, 2sig-high width) "
      f"{len(rs)}: {', '.join(rs) if rs else '-'}")
    P(f"   {foot}: NOT TESTED {len(nt)}: {', '.join(nt)}")
    fl_ = {}
    for r in T:
        fl_[r["flag_I0"]] = fl_.get(r["flag_I0"], 0) + 1
    P(f"   {foot}: I0 flags " + ", ".join(f"{k} {v}" for k, v in sorted(fl_.items())) +
      f"; median zeta_MDF {np.median([r['zeta_MDF'] for r in T if r['zeta_MDF'] is not None]):.2f}"
      f"; median eta {np.median([r['eta'] for r in T if r['eta'] is not None]):.1f}")
    vz = [r for r in T if r.get("zeta_1pct") and r["zeta_1pct"][1] > 10]
    P(f"   {foot}: A1 (post-result reading) {len(vz)} systems minimise in the eta -> 0, zeta >> 1 corner (metal-only winds); within 1% of"
      f" their L_MDF, eta spans median [{np.median([r['eta_1pct'][0] for r in vz]):.3f}, {np.median([r['eta_1pct'][1] for r in vz]):.2f}]"
      f" and zeta median [{np.median([r['zeta_1pct'][0] for r in vz]):.0f}, {np.median([r['zeta_1pct'][1] for r in vz]):.0f}]:"
      " the MDF does not fix zeta; it bounds L anyway" if vz else f"   {foot}: no system minimises at zeta >> 1")
    fb = [r["f_break"] for r in T if r["q_F2"] < 1]
    P(f"   {foot}: f_break (unmixed-escape fraction that would close the supply, supplied systems) median {np.median(fb):.2f}, min {min(fb):.2f}"
      if fb else f"   {foot}: no supplied system")

P()
P("   E6's six short systems (canonical | alt), F2 logy -0.5:")
for n in ("Columba I", "Segue 1", "Tucana IV", "Ursa Major I", "Ursa Major II", "Willman 1"):
    parts = []
    for foot in FOOTS:
        r = next((x for x in PER if x["footing"] == foot and x["name"] == n), None)
        if r is None or not r["tested"]:
            parts.append(f"{foot} NOT TESTED ({r and r['sig_src']}, UL {r and r['sig_ul']})")
            continue
        parts.append(f"{foot} q {r['q_F2']:.2f} (E6 premise {r['q_F2_E6premise']:.2f}; I2 {r['q_F2_I2']:.2f}; R1 "
                     f"{'-' if r['q_F2_R1'] is None else format(r['q_F2_R1'], '.2f')}; R2 {'-' if r['q_F2_R2'] is None else format(r['q_F2_R2'], '.2f')})"
                     f" [{r['flag_I0']}, zeta {('-' if r['zeta_MDF'] is None else format(r['zeta_MDF'], '.1f'))}]")
    W = WCLS[n]
    P(f"   {n:14s} P-W LVD {W['LVD']}, S19 {W['S19']}, Walker {W['Walker']} | " + " | ".join(parts))

# ---------------- Upsilon_V sensitivity on F2 (reported only)
P()
for foot in FOOTS:
    line = []
    for f in (0.75, 1.0, 1.25):
        q = []
        for n in NAMES:
            e3 = E3.get((foot, n)); L = lsys(n, "LVD")
            if e3 is None or not L["tested"]:
                continue
            Mst = 10 ** fl(e3["logMstar"]); Md = fl(e3["M_dyn"])
            q.append(((Md - f * Mst / 2) / (SUP * f * Mst)) / L[("I0", -0.5)]["L"])
        line.append(f"Upsilon_V {2 * f:.1f}: median q {np.median(q):.3f}")
    chk = max(abs(((fl(E3[(foot, n)]["M_dyn"]) - 10 ** fl(E3[(foot, n)]["logMstar"]) / 2) / (SUP * 10 ** fl(E3[(foot, n)]["logMstar"])))
                  / fl(E6[(foot, n)]["L_req_F2"]) - 1) for n in NAMES if (foot, n) in E3 and (foot, n) in E6)
    P(f"   {foot} F2 Upsilon sensitivity (gas-free L independent of M*): " + "; ".join(line) + f"  [F2 L_req rebuilt from E3, max rel {chk:.1e}]")
    RES[f"{foot}_upsilon"] = line

# ============================================================ verdict
P()
prim = CLS["LVD"]["cls"]; flips = [m for m in ("R1", "R2") if CLS[m]["cls"] != prim]
if prim == "UNDECIDABLE" or flips:
    verdict = "UNDECIDABLE ON DISK"
else:
    verdict = prim
nnar = sum(1 for n in NAMES if WCLS[n]["LVD"].startswith("NARROW"))
P(f"VERDICT: {verdict}  (primary LVD class {prim}; R1 S19 {CLS['R1']['cls']}; R2 Walker {CLS['R2']['cls']}"
  f"{'; flips: ' + ', '.join(flips) if flips else ''})")
P(f"   graded cell is the central width; at every system's 2sig-low width at once (I2) the median q is "
  f"{RES['canonical_F2']['I2_-0.5'][0]:.2f} canonical / {RES['alt_F2']['I2_-0.5'][0]:.2f} alt (F2, -0.5): not robust at 2sig in the widths")
P(f"   K4 FAILED as frozen: Gaussian sigma of a narrow skewed MDF is low-biased (median); the bias makes the graded q conservative (A1)")
P(f"   zeta = 1 & Z0 = 0 premise (P-W, LVD): NARROW in {nnar} systems; S19: "
  f"{sum(1 for n in NAMES if WCLS[n]['S19'].startswith('NARROW'))}; Walker: {sum(1 for n in NAMES if WCLS[n]['Walker'].startswith('NARROW'))}")
P("   Untested on disk: homogeneous mixing; unmixed escape of fresh ejecta (shape-identical to a lower retained yield; f_break above).")
P("   Supply is not mechanism: even where the supply holds, no binding mechanism puts the cold energy inside r12 (G2 failed).")

npass = sum(1 for _, ok in CHECKS if ok)
P()
P(f"P1_DWARF_CHEMISTRY COMPLETE: {npass}/{len(CHECKS)} checks PASS.")


def js(o):
    if isinstance(o, dict):
        return {str(k): js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(js(dict(mutate=MUT, checks=CHECKS, verdict=verdict, classes=CLS, medians=RES, band=[BAND_LO, BAND_HI],
                  sig_family_max=SIG_FMAX, sig_grid_min=SIG_GMIN, K1=errs, K3i=k3i, K3ii=k3ii, K4=k4, K4_A1_diagnostic=k4d, K5=k5,
                  width_classes=WCLS, walker={n: {k: v for k, v in W.items()} for n, W in WRES.items()}, per_system=PER)),
          open(os.path.join(HERE, f"p1_dwarf_chemistry_results{SFX}.json"), "w"), indent=1)
open(os.path.join(HERE, f"p1_dwarf_chemistry{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
