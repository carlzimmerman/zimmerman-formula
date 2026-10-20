"""CFG920 -- is the D-i route's post-formation baryon loss compatible with each dwarf's own chemistry?
Criteria: FROZEN_CRITERIA.md (a229bb78c), committed alone before this script.

CFG915 route D-i: required loss L_req = M_b,form / M_b,now = exp(4E), E = ln(sigma_obs / sigma_law) (CFG827 code path, both footings).
Declared bound: one-zone homogeneous leaky box (instantaneous recycling and mixing, no inflow, Z0 = 0, wind at ISM metallicity),
Fe yield log y in {-0.5, -0.2, +0.1}, outflow forms W1 (continuous wind, CFG317's estimator) and W2 (W1 + terminal unprocessed strip,
gas-free dwarfs); unseen loss only raises L, so corner k allows [L_min,k, inf).  Timing map vs Weisz+14 SFHs; metal-enhanced-wind
price zeta_need and inflow are reported escapes.
Run (from this directory):  OMP_NUM_THREADS=1 nice -n 10 python3 cfg920.py          (exit 0 = every K passes)
                            CFG920_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg920.py   (exit 1 = tooth bites)
Read-only inputs: real_research/data/dsph (E-MILES SSPs, Weisz+14, LVD, Collins+13); CFG824/827/828/852/915/317 result JSONs.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, csv, json, math
import numpy as np
from scipy.stats import spearmanr
from scipy.special import exp1
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
DS = os.path.join(REPO, "real_research", "data", "dsph"); WZ = os.path.join(DS, "weisz2014_dl")
MUT = os.environ.get("CFG920_MUTATE") == "1"; OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt"); WID = 0.15
LOGY = (-0.5, -0.2, 0.1); MDF_ALLOW = 0.1; GAMMA = 0.5772156649015329; LN10 = math.log(10.0)
T_ONSET = 13.3          # Gyr: CFG827's first-bin age = SF onset of the timing clock
NBOOT, SEED = 2000, 920
CLS_C, CLS_X, CLS_U = "COMPATIBLE", "CONTRADICTED", "UNDERDETERMINED"


def rd(rel):
    return json.load(open(os.path.join(LANES, rel)))


# ============================================================================ CFG827 code path (reimplemented, K1-checked)
def fnum(x):
    try: return float(x)
    except: return None


SSP = {}
for l in open(os.path.join(DS, "emiles_ml_dl", "UBBVRIJHK_ku_iPp0.00.MAG")).readlines()[1:]:
    v = l.split(); Z, age, Mn, mlV = float(v[2]), float(v[3]), float(v[4]), float(v[17])
    SSP.setdefault(Z, []).append((age, Mn, mlV))
for Z in SSP: SSP[Z] = np.array(sorted(SSP[Z]))


def ssp(Z, t):
    a = SSP[Z]; t = min(max(t, a[0, 0]), a[-1, 0]); lt = math.log10(t); la = np.log10(a[:, 0])
    Mn = float(np.interp(lt, la, a[:, 1])); ml = float(np.interp(lt, la, a[:, 2])); return Mn, Mn / ml


def read_tsv(fn):
    L = [l.rstrip("\n") for l in open(fn) if not l.startswith("#") and l.strip()]
    hdr = L[0].split("\t"); return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in L[3:] if len(l.split("\t")) == len(hdr)]


def fgrid(r):
    fk = {float(k[1:]): fnum(v) for k, v in r.items() if k.startswith("f") and k[1:].replace(".", "").isdigit() and fnum(v) is not None}
    g = sorted(fk, reverse=True); return np.array(g), np.array([fk[x] for x in g])


def bins(r):
    g, f = fgrid(r); out = [(13.3, f[0])]
    for i in range(1, len(g)):
        dm = f[i] - f[i - 1]
        if dm > 0: out.append((10 ** (0.5 * (g[i - 1] + g[i])) / 1e9, dm))
    return out


def ups_sfh(B, Z):
    m = sum(dm * ssp(Z, t)[0] for t, dm in B); l = sum(dm * ssp(Z, t)[1] for t, dm in B); return m / l


NAMEMAP = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "DDO 210": "Aquarius",
           "Pegasus": "Pegasus dIrr", "Sag DIG": "Sagittarius dIrr", "M32": "M 32"}
T6 = {r["ID"]: r for r in read_tsv(os.path.join(WZ, "table6.tsv"))}
SFH, WROW = {}, {}
for r in read_tsv(os.path.join(WZ, "table5.tsv")):
    nm = NAMEMAP.get(r["ID"], r["ID"])
    if nm in SFH: continue
    WROW[nm] = T6.get(r["ID"], r); SFH[nm] = bins(WROW[nm])
R24 = rd("CFG824_dwarf_age_fossil/cfg824_results.json")["rows"]
LVD, LVDR = {}, {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DS, fn))):
        LVD[r["name"]] = dict(MV=fnum(r.get("M_V")), rhl=fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")))
        LVDR[r["name"]] = r


def wolf(M, rhl): return math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3


def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))


def law_M(M, rhl, a0):
    y = G * (M / 2) * Msun / ((4 / 3) * rhl * PC) ** 2 / a0
    return wolf(M, rhl) * math.sqrt(nu(y))


def law(MV, rhl, a0, ups): return law_M(ups * 10 ** (0.4 * (4.83 - MV)), rhl, a0)


ROWS = {}
for nm, v in R24.items():
    d = dict(name=nm, train=v["train"], so=v["so"], eso=v["eso"], tau50=v["tau50"], tau90=v["tau90"], **LVD[nm])
    d["ups"] = ups_sfh(SFH[nm], -1.31); d["LV"] = 10 ** (0.4 * (4.83 - d["MV"])); d["Ms"] = d["ups"] * d["LV"]
    d["E"] = {f: math.log(d["so"] / law(d["MV"], d["rhl"], A0[f], d["ups"])) for f in FOOTS}
    d["sE"] = math.sqrt((d["eso"] / d["so"]) ** 2 + (LN10 * WID / 2) ** 2)
    ROWS[nm] = d
OOS = [d for d in ROWS.values() if not d["train"]]; TRN = [d for d in ROWS.values() if d["train"]]


# ============================================================================ chemistry: homogeneous leaky box (CFG317 form)
def elnx(X):
    """E[ln u] for u ~ e^-u truncated to (0, X) (CFG317's closed form); X = inf -> -gamma."""
    if not np.isfinite(X):
        return -GAMMA
    if X < 1.0:      # exact series sum_n (-1)^n/n! X^(n+1) [ln X/(n+1) - 1/(n+1)^2] (avoids cancellation at small X)
        lX, s, term = math.log(X), 0.0, X
        for n in range(40):
            s += term * (lX / (n + 1) - 1.0 / (n + 1) ** 2)
            term *= -X / (n + 1)
        return s / (-math.expm1(-X))
    return (-GAMMA - exp1(X) - math.exp(-X) * math.log(X)) / (1.0 - math.exp(-X))


def w1(feh, Ms, Mg, logy):
    """W1 continuous homogeneous wind (CFG317 estimator).  Returns (eta, L_W1, underproduce_flag)."""
    if Mg <= 0:
        le = logy - GAMMA / LN10 - feh                        # log10(1 + eta), exhausted box
        if le <= 0:
            return 0.0, 1.0, True
        eta = 10 ** le - 1.0
        return eta, 1.0 + eta, False

    def g(le):
        X = math.log((Mg + 10 ** le * Ms) / Mg)
        return logy - le + elnx(X) / LN10 - feh
    if g(0.0) <= 0:
        return 0.0, 1.0, True
    grid = np.linspace(0, 12.0, 241); vals = [g(x) for x in grid]
    k = next(i for i in range(1, len(grid)) if vals[i] <= 0)
    le = brentq(g, grid[k - 1], grid[k], xtol=1e-14, rtol=1e-14)
    eta = 10 ** le - 1.0
    return eta, ((1 + eta) * Ms + Mg) / (Ms + Mg), False


def u0_of(feh, logy):
    """eta = 0 endpoint of the W2 family (closed box truncated at u0 then stripped): ln y + E[ln u | u < u0] = [Fe/H] ln10.
    None if even the exhausted closed box falls below the observed [Fe/H] (chemistry under-produces)."""
    tgt = (feh - logy) * LN10
    if -GAMMA <= tgt:
        return None
    lo, hi = -40.0, 0.0
    while elnx(math.exp(hi)) < tgt and hi < 6.0:
        hi += 1.0
    if elnx(math.exp(hi)) < tgt:
        return float("inf")
    return math.exp(brentq(lambda s: elnx(math.exp(s)) - tgt, lo, hi, xtol=1e-15, rtol=1e-15))


def onepluseta_w2(u, feh, logy):
    """1 + eta along the zeta = 1 W2 family at truncation u (closed form)."""
    return math.exp(logy * LN10 + elnx(u) - feh * LN10)


def L_w2(u, feh, logy):
    ope = onepluseta_w2(u, feh, logy)
    return ope if not np.isfinite(u) else ope / (-math.expm1(-u))


def family_min(fun, u0, ngrid=200, umax=60.0):
    """min over u in [u0, inf] of fun(u) (grid in ln u + inf, then bounded refinement)."""
    if u0 is None:
        return None
    if not np.isfinite(u0) or u0 >= umax:
        return fun(float("inf")), float("inf")
    s_lo = math.log(u0)
    S = np.linspace(s_lo, math.log(umax), ngrid)
    vals = [fun(math.exp(s)) for s in S]; vinf = fun(float("inf"))
    i = int(np.argmin(vals))
    if vinf <= vals[i]:
        return vinf, float("inf")
    a, b = S[max(i - 1, 0)], S[min(i + 1, ngrid - 1)]
    if b > a:
        r = minimize_scalar(lambda s: fun(math.exp(s)), bounds=(a, b), method="bounded", options=dict(xatol=1e-12))
        if r.fun < vals[i]:
            return float(r.fun), math.exp(r.x)
    return float(vals[i]), math.exp(S[i])


def w2(feh, logy):
    """W2: returns (L_min, u_at_min, eta_at_min, underproduce_flag)."""
    u0 = u0_of(feh, logy)
    if u0 is None:
        return 1.0, float("inf"), 0.0, True
    Lm, um = family_min(lambda u: L_w2(u, feh, logy), u0)
    return Lm, um, onepluseta_w2(um, feh, logy) - 1.0, False


def chem_corners(feh, Ms, Mg):
    """L_min per corner (logy, form).  W2 == W1 for gas-bearing dwarfs."""
    out = {}
    for ly in LOGY:
        e1, L1, f1 = w1(feh, Ms, Mg, ly)
        out[(ly, "W1")] = dict(L=L1, eta=e1, under=f1)
        if Mg <= 0:
            L2, u2, e2, f2 = w2(feh, ly)
            out[(ly, "W2")] = dict(L=L2, eta=e2, u=u2, under=f2)
        else:
            out[(ly, "W2")] = dict(L=L1, eta=e1, under=f1, same_as_W1=True)
    return out


# ---------------------------------------------------------------- metal-enhanced wind (zeta > 1), reported escape only
NGL = 96
XL, WL = np.polynomial.legendre.leggauss(NGL)
XG, WG = np.polynomial.laguerre.laggauss(NGL)


def lnphi(x):
    x = np.asarray(x, dtype=float)
    small = x < 1e-7
    xs = np.where(small, 1.0, x)
    return np.where(small, -0.5 * x, np.log(-np.expm1(-xs) / xs))


def Phi(k, uq):
    """E[ln phi(k u)], phi(x) = (1 - e^-x)/x, u ~ e^-u truncated to (0, uq)."""
    if k <= 0:
        return 0.0
    if not np.isfinite(uq) or uq > 50.0:
        return float(np.sum(WG * lnphi(k * XG)))
    u = 0.5 * uq * (XL + 1.0); w = 0.5 * uq * WL
    return float(np.sum(w * np.exp(-u) * lnphi(k * u)) / (-math.expm1(-uq)))


def Z_closed(u, y, eta, zeta):
    if zeta == 1.0:
        return y * u / (1 + eta)
    return y / ((zeta - 1) * eta) * (1 - math.exp(-(zeta - 1) * eta / (1 + eta) * u))


def mean_lnZ(eta, zeta, uq, logy):
    k = (zeta - 1.0) * eta / (1.0 + eta)
    return logy * LN10 - math.log1p(eta) + elnx(uq) + Phi(k, uq)


def eta_zeta(uq, zeta, feh, logy):
    g = lambda le: mean_lnZ(math.expm1(le), zeta, uq, logy) - feh * LN10
    g0 = g(0.0)
    if g0 < 0:
        return None
    if g0 == 0:
        return 0.0
    hi = 1.0
    while g(hi) > 0 and hi < 40:
        hi *= 2.0
    if g(hi) > 0:
        return None
    return math.expm1(brentq(g, 0.0, hi, xtol=1e-12, rtol=1e-12))


def Lmin_zeta(zeta, feh, Ms, Mg, logy):
    if Mg <= 0:
        u0 = u0_of(feh, logy)
        if u0 is None:
            return 1.0

        def fun(u):
            e = eta_zeta(u, zeta, feh, logy)
            if e is None:
                return float("inf")
            return (1 + e) if not np.isfinite(u) else (1 + e) / (-math.expm1(-u))
        return family_min(fun, u0, ngrid=40)[0]
    # gas-bearing: truncation set by the present gas
    g = lambda le: mean_lnZ(math.expm1(le), zeta, math.log((Mg + math.exp(le) * Ms) / Mg), logy) - feh * LN10
    if g(0.0) <= 0:
        return 1.0
    hi = 1.0
    while g(hi) > 0 and hi < 40:
        hi *= 2.0
    e = math.expm1(brentq(g, 0.0, hi, xtol=1e-12, rtol=1e-12))
    return ((1 + e) * Ms + Mg) / (Ms + Mg)


def zeta_need(Lreq, feh, Ms, Mg, logy=-0.5):
    if Lreq <= 1.0:
        return "none (L_req <= 1)"
    if Lmin_zeta(1.0, feh, Ms, Mg, logy) <= Lreq:
        return 1.0
    if Lmin_zeta(1000.0, feh, Ms, Mg, logy) > Lreq:
        return "> 1000"
    lz = brentq(lambda z: Lmin_zeta(10 ** z, feh, Ms, Mg, logy) - Lreq, 0.0, 3.0, xtol=1e-4)
    return float(10 ** lz)


# ---------------------------------------------------------------- timing map
def Lpost_min(F, feh, Ms, Mg, logy):
    if Mg <= 0:
        u0 = u0_of(feh, logy)
        if u0 is None:
            return 1.0

        def fun(u):
            ope = onepluseta_w2(u, feh, logy)
            L = ope if not np.isfinite(u) else ope / (-math.expm1(-u))
            return L - (ope - 1.0) * F
        return family_min(fun, u0, ngrid=120)[0]
    e, L1, _ = w1(feh, Ms, Mg, logy)
    return L1 - e * F * Ms / (Ms + Mg)


def t_of_F(nm, F):
    g, f = fgrid(WROW[nm])
    la = np.concatenate([[math.log10(T_ONSET * 1e9)], g]); Fc = np.maximum.accumulate(np.concatenate([[0.0], f]))
    if F <= 0:
        return T_ONSET
    for i in range(1, len(la)):
        if Fc[i] >= F:
            if Fc[i] == Fc[i - 1]:
                return 10 ** la[i] / 1e9
            w = (F - Fc[i - 1]) / (Fc[i] - Fc[i - 1])
            return 10 ** (la[i - 1] + w * (la[i] - la[i - 1])) / 1e9
    return 10 ** la[-1] / 1e9


def timing(d, Lreq, logy):
    feh, Ms, Mg = d["feh"], d["Ms"], d["Mg"]
    if Lpost_min(0.0, feh, Ms, Mg, logy) <= Lreq:
        return dict(F_need=0.0, t_need=T_ONSET, reading="AT FORMATION")
    if Lpost_min(1.0, feh, Ms, Mg, logy) > Lreq:
        return dict(F_need=None, t_need=None, reading="NONE")
    F = brentq(lambda x: Lpost_min(x, feh, Ms, Mg, logy) - Lreq, 0.0, 1.0, xtol=1e-6)
    return dict(F_need=float(F), t_need=float(t_of_F(d["name"], F)), reading="EARLY" if F <= 0.5 else "LATE")


# ---------------------------------------------------------------- classes
def classify(Lp, Lm, C_fav, C_unf):
    """Lp/Lm = favourable/unfavourable L_req; C_fav/C_unf = corner L_min at [Fe/H]+s / [Fe/H]-s."""
    if all(Lm >= C_unf[k] for k in C_unf):
        return CLS_C
    if not any(Lp >= C_fav[k] for k in C_fav):
        return CLS_X
    return CLS_U


def corners_of(d, shift):
    return {k: v["L"] for k, v in chem_corners(d["feh"] + shift, d["Ms"], d["Mg"]).items()}


def ck(k): return f"{k[0]:+.1f}|{k[1]}"


def median_class(Lreq, Cmat, idx):
    """Lreq: array (N,), Cmat: dict corner -> array (N,), idx: (NBOOT, N) bootstrap indices."""
    Mreq = float(np.median(Lreq)); res = {}
    for k, C in Cmat.items():
        r = np.median(Lreq[idx], axis=1) / np.median(C[idx], axis=1)
        res[ck(k)] = dict(M_req=Mreq, M_k=float(np.median(C)), ratio=Mreq / float(np.median(C)), p16=float(np.percentile(r, 16)),
                          p84=float(np.percentile(r, 84)), median_per_dwarf_ratio=float(np.median(Lreq / C)))
    if all(v["p16"] >= 1 for v in res.values()):
        cl = CLS_C
    elif all(v["p84"] < 1 for v in res.values()):
        cl = CLS_X
    else:
        cl = CLS_U
    return cl, res


# ============================================================================ sample assembly
def metal(nm, collins=False):
    r = LVDR[nm]; fe = fnum(r.get("metallicity"))
    if fe is not None and np.isfinite(fe):
        em, ep = fnum(r.get("metallicity_em")), fnum(r.get("metallicity_ep"))
        em = em if (em is not None and np.isfinite(em)) else None; ep = ep if (ep is not None and np.isfinite(ep)) else None
        err = 0.5 * (em + ep) if (em is not None and ep is not None) else (em or ep or 0.2)
        return fe, (err if err > 0 else 0.2), "LVD " + (r.get("metallicity_type") or "-")
    if collins and nm.startswith("Andromeda "):
        c = COLL.get(nm.replace("Andromeda ", "And "))
        if c and c[0] is not None:
            return c[0], c[1], "Collins+13"
    return None, None, None


COLL = {}
for line in open(os.path.join(DS, "collins2013_m31_dsph.tsv"), encoding="latin-1"):
    if line.startswith("#") or not line.strip():
        continue
    f_ = line.split("\t")
    if len(f_) < 30 or not f_[0].strip().isdigit():
        continue
    COLL[f_[1].strip()] = (fnum(f_[28]), fnum(f_[29]) or 0.2)


def gas_of(nm):
    mh = fnum(LVDR[nm].get("mass_HI"))
    return 1.33 * 10 ** mh if (mh is not None and np.isfinite(mh)) else 0.0


def prep(d, collins=False):
    fe, err, src = metal(d["name"], collins)
    if fe is None:
        return None
    x = dict(d); x.update(feh=fe, efeh=err, s=math.hypot(err, MDF_ALLOW), msrc=src, Mg=gas_of(d["name"]))
    x["gas"] = x["Mg"] > 0
    x["Cfull"] = chem_corners(fe, x["Ms"], x["Mg"])
    x["C"] = {0: {k: v["L"] for k, v in x["Cfull"].items()}}
    for sh in (+1, -1, +2, -2):
        x["C"][sh] = corners_of(x, sh * x["s"])
    return x


def dwarf_classes(x, Lreq_fn):
    """Lreq_fn(f, nsig) -> L_req.  Returns graded (1 sigma), central and 2 sigma classes per footing."""
    out = {}
    for f in FOOTS:
        L0 = Lreq_fn(f, 0)
        out[f] = dict(L_req=L0, graded=classify(Lreq_fn(f, +1), Lreq_fn(f, -1), x["C"][+1], x["C"][-1]),
                      central=classify(L0, L0, x["C"][0], x["C"][0]),
                      two_sigma=classify(Lreq_fn(f, +2), Lreq_fn(f, -2), x["C"][+2], x["C"][-2]))
    return out


def Lreq_E(x, key="E"):
    return lambda f, n: math.exp(4 * (x[key][f] + n * x["sE"]))


# ============================================================================ run
RES = dict(lane="CFG920", criteria="a229bb78c", mutate=MUT, settings=dict(A0=A0, LOGY=LOGY, MDF_ALLOW=MDF_ALLOW, WID=WID,
           T_ONSET_Gyr=T_ONSET, NBOOT=NBOOT, SEED=SEED, gas_factor=1.33, ups="SFH [M/H] -1.31 (CFG827)"))
P("CFG920  D-i post-formation baryon loss vs the dwarfs' own chemistry (homogeneous leaky box)" + ("  [MUTATE]" if MUT else ""))
P("        kappa = 1/2 FITTED; footings never pooled; raw data + framework-native only; not theory closed")
P()
T = [x for x in (prep(d) for d in OOS) if x is not None]
NT = [d["name"] for d in OOS if prep(d) is None]
rng = np.random.default_rng(SEED); IDX = rng.integers(0, len(T), size=(NBOOT, len(T)))

if MUT:
    P(f"MUTATE: L_req replaced by 1 (M1) and by 20 (M2) for all {len(T)} tested dwarfs; chemistry unchanged; no errors on L.")
    MR = {}
    for tag, Lc in (("M1", 1.0), ("M2", 20.0)):
        per = {x["name"]: classify(Lc, Lc, x["C"][+1], x["C"][-1]) for x in T}
        Cmat = {k: np.array([x["C"][0][k] for x in T]) for k in T[0]["C"][0]}
        mc, mres = median_class(np.full(len(T), Lc), Cmat, IDX)
        MR[tag] = dict(L=Lc, per_dwarf=per, counts={c: sum(v == c for v in per.values()) for c in (CLS_C, CLS_U, CLS_X)}, median_class=mc, median=mres)
        P(f"  {tag} (L = {Lc:g}): per-dwarf {MR[tag]['counts']}; sample-median class {mc}")
    nchg = sum(MR["M1"]["per_dwarf"][n] != MR["M2"]["per_dwarf"][n] for n in MR["M1"]["per_dwarf"])
    bites = (MR["M1"]["median_class"] != MR["M2"]["median_class"]) and nchg >= 0.5 * len(T)
    P(f"  per-dwarf classes changed: {nchg} of {len(T)}; median class {MR['M1']['median_class']} -> {MR['M2']['median_class']}")
    P(f"  MUTATE tooth {'BITES' if bites else 'DOES NOT BITE (control FAILED)'}")
    RES.update(M=MR, n_changed=nchg, bites=bites, tested=[x["name"] for x in T])
    json.dump(RES, open(os.path.join(HERE, "cfg920_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg920_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if bites else 0)

# ---------------------------------------------------------------------------- K tests
K = {}


def kline(name, ok, msg):
    K[name] = dict(ok=bool(ok), msg=msg); P(f"  {name:6s} {'PASS' if ok else 'FAIL'}  {msg}")


P("K TESTS")
R827 = rd("CFG827_dwarf_age_sfh_ml/cfg827_results.json")
dE = max(abs(ROWS[n]["E"]["canonical"] - v["E_SFH"]) for n, v in R827["rows"].items())
t90 = [d["tau90"] for d in OOS]; ra, _ = spearmanr([d["E"]["alt"] for d in OOS], t90, alternative="greater")
LF = rd("CFG915_population_label_mobility/cfg915_results.json")["D"]["loss_factor"]
Lc = np.exp(4 * np.array([v["E_SFH"] for v in R827["rows"].values() if not v["train"]]))
Lm = np.exp(4 * np.array([d["E"]["canonical"] for d in OOS]))
mine = dict(median=float(np.median(Lm)), p16=float(np.percentile(Lm, 16)), p84=float(np.percentile(Lm, 84)), n_le1=int((Lm <= 1).sum()), N=int(Lm.size))
k1 = (dE <= 1e-9 and abs(ra - R827["alt"]["rho"]) <= 1e-9 and all(abs(mine[q] / LF[q] - 1) <= 1e-9 for q in ("median", "p16", "p84"))
      and mine["n_le1"] == LF["n_le1"] == 3 and mine["N"] == LF["N"] == 28)
kline("K1", k1, f"CFG827 E_SFH max|dE| {dE:.1e} over {len(R827['rows'])} rows; alt rho {ra:+.6f} vs {R827['alt']['rho']:+.6f}; CFG915 loss factor "
      f"median {mine['median']:.6f} (stored {LF['median']:.6f}), p16 {mine['p16']:.6f}, p84 {mine['p84']:.4f}, n_le1 {mine['n_le1']}, N {mine['N']}")

# K2: CFG852 through this code path
R28 = {r["name"]: r for r in rd("CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json")["canonical|nu_e"]["rows"]}
EXCL852 = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
nu852 = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))


def delta_ups2(r):
    MV, s, rh = fnum(r.get("M_V")), fnum(r.get("vlos_sigma")), fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if None in (MV, s, rh): return None
    r12 = (4 / 3) * rh * PC; Ms_ = 2.0 * 10 ** (0.4 * (4.83 - MV)); gb = G * (Ms_ / 2) * Msun / r12 ** 2
    return math.log10(3 * (s * 1e3) ** 2 / r12 / (gb * nu852(gb / A0["canonical"]))), math.log10(gb)


def s852(primary):
    S = []
    for nm, r in LVDR.items():
        Zm, MV = fnum(r.get("metallicity")), fnum(r.get("M_V"))
        if Zm is None or MV is None or nm in EXCL852: continue
        if primary:
            if nm not in R28: continue
            dd, lg = R28[nm]["delta"], R28[nm]["lgbar"]
        else:
            xx = delta_ups2(r)
            if xx is None: continue
            dd, lg = xx
        S.append((dd, lg, Zm, 0.4 * (4.83 - MV)))
    a = np.array(S); dd, lg, Zm, lL = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    c1, c0 = np.polyfit(lL, Zm, 1); dZ = Zm - (c0 + c1 * lL)
    A = np.vstack([np.ones_like(lg), lg]).T
    rdd = dd - A @ np.linalg.lstsq(A, dd, rcond=None)[0]; rz = dZ - A @ np.linalg.lstsq(A, dZ, rcond=None)[0]
    return len(S), float(c1), float(spearmanr(rz, rdd)[0])


R852 = rd("CFG852_gas_loss_metallicity/cfg852_results.json")
n1, c1p, r1p = s852(True); n2, c1s, r1s = s852(False)
k2 = (n1 == R852["primary"]["N"] and n2 == R852["secondary"]["N"] and abs(c1p - R852["primary"]["c1"]) <= 1e-9 and abs(r1p - R852["primary"]["rho"]) <= 1e-9
      and abs(c1s - R852["secondary"]["c1"]) <= 1e-9 and abs(r1s - R852["secondary"]["rho"]) <= 1e-9)
kline("K2", k2, f"CFG852 primary N {n1} slope {c1p:.6f} rho {r1p:+.6f} (stored {R852['primary']['c1']:.6f} / {R852['primary']['rho']:+.6f}); "
      f"secondary N {n2} slope {c1s:.6f} rho {r1s:+.6f} (stored {R852['secondary']['c1']:.6f} / {R852['secondary']['rho']:+.6f})")

# K3: CFG317 estimator through this code path
EST = rd("CFG317_baryon_loss_cold_mass/cfg317_baryon_loss_results.json")["numbers"]["EST"]
n3, de3, dl3 = 0, 0.0, 0.0
for key, lst in EST.items():
    ly = float(key.split("|")[0])
    for o in lst:
        if o is None: continue
        e_, R_, _ = w1(o["feh"], o["Ms"], o["Mg"], ly); n3 += 1
        de3 = max(de3, abs(e_ - o["eta"]) / max(o["eta"], 1e-30) if o["eta"] > 0 else abs(e_))
        dl3 = max(dl3, abs(math.log10(R_) - o["lR"]))
kline("K3", n3 > 0 and de3 <= 1e-8 and dl3 <= 1e-9, f"CFG317 EST reproduced for {n3} object-yield entries: max rel d(eta) {de3:.1e}, max |d log R_ind| {dl3:.1e}")

# K4: numerics
y_, e_, z_ = 10 ** -0.5, 5.0, 4.0
sol = solve_ivp(lambda u, Z: [(y_ - (z_ - 1) * e_ * Z[0]) / (1 + e_)], (0, 6), [0.0], rtol=1e-12, atol=1e-15, dense_output=True)
dz = max(abs(Z_closed(u, y_, e_, z_) / sol.sol(u)[0] - 1) for u in (0.5, 2.0, 6.0))
dq = 0.0
for X in (0.05, 0.7, 2.3, 9.0):
    num = quad(lambda u: math.log(y_ * u / (1 + e_)) * math.exp(-u), 0, X, limit=400, epsabs=1e-14, epsrel=1e-13)[0] / (1 - math.exp(-X))
    dq = max(dq, abs(num - (math.log(y_ / (1 + e_)) + elnx(X))))
de0 = 0.0
for fe_, ly_ in ((-1.7, -0.5), (-2.6, 0.1), (-1.1, -0.2)):
    u0 = u0_of(fe_, ly_); de0 = max(de0, abs(L_w2(u0, fe_, ly_) - 1.0 / (-math.expm1(-u0))), abs(onepluseta_w2(u0, fe_, ly_) - 1.0))
kline("K4", dz <= 1e-6 and dq <= 1e-9 and de0 <= 1e-9, f"zeta>1 closed form vs ODE max rel {dz:.1e}; zeta=1 quadrature mean ln Z vs closed form {dq:.1e}; "
      f"W2 eta=0 endpoint vs closed-box truncation {de0:.1e}")
# implementation checks (not frozen K): Gauss quadrature of Phi vs adaptive quad; zeta = 1 family min equals W2
dphi = 0.0
for kk, uq in ((0.3, 1.5), (3.0, 8.0), (20.0, 0.4), (2.0, float("inf")), (50.0, float("inf"))):
    up = uq if np.isfinite(uq) else np.inf
    ref = quad(lambda u: float(lnphi(kk * u)) * math.exp(-u), 0, up, limit=400, epsabs=1e-13)[0] / ((-math.expm1(-uq)) if np.isfinite(uq) else 1.0)
    dphi = max(dphi, abs(Phi(kk, uq) - ref))
dz1 = max(abs(Lmin_zeta(1.0, fe_, 1.0, 0.0, ly_) - w2(fe_, ly_)[0]) / w2(fe_, ly_)[0] for fe_, ly_ in ((-1.7, -0.5), (-2.6, 0.1)))
P(f"  impl.  (not frozen) Gauss-quadrature Phi vs adaptive quad max abs {dphi:.1e}; zeta = 1 family min vs W2 rel {dz1:.1e}")
RES["K"] = K; RES["impl_checks"] = dict(phi_abs=dphi, zeta1_vs_W2=dz1)
P()

# ---------------------------------------------------------------------------- main: per dwarf
P(f"SAMPLE: CFG827 out-of-sample N {len(OOS)}; tested (LVD [Fe/H]) {len(T)}; NOT TESTED (no LVD metallicity): {', '.join(NT)}")
P("  corners: yield log y in {-0.5, -0.2, +0.1} x form {W1 continuous wind, W2 + terminal strip (gas-free only; W2 = W1 if gas-bearing)}")
P("  allowed set per corner: [L_min, inf) (unseen unprocessed loss only raises L).  graded class at 1 sigma (E and [Fe/H]).")
P()
hdr = (f"  {'dwarf':17s} {'gas':3s} {'[Fe/H]':>6s} {'s':>5s} {'E_can':>6s} {'L_req can/alt':>14s} | L_min W2/W1 @-0.5   @-0.2   @+0.1  "
       f"| graded can / alt          | central can")
P(hdr)
ROWOUT = {}
for x in T:
    x["cls"] = dwarf_classes(x, Lreq_E(x))
    C0 = x["C"][0]
    P(f"  {x['name']:17s} {'yes' if x['gas'] else 'no':3s} {x['feh']:+6.2f} {x['s']:5.2f} {x['E']['canonical']:+6.3f} "
      f"{x['cls']['canonical']['L_req']:6.2f}/{x['cls']['alt']['L_req']:6.2f} | "
      + "  ".join(f"{C0[(ly, 'W2')]:6.2f}/{C0[(ly, 'W1')]:6.2f}" for ly in LOGY)
      + f" | {x['cls']['canonical']['graded']:15s} / {x['cls']['alt']['graded']:15s} | {x['cls']['canonical']['central']}")
P()
flags = sorted({x["name"] for x in T for k, v in x["Cfull"].items() if v["under"]})
P(f"  chemistry under-produces [Fe/H] at some corner (eta = 0, L_min = 1, pre-enrichment needed): {flags or 'none'}")
w2feas = [(x["name"], ly) for x in T if not x["gas"] for ly in LOGY if not x["Cfull"][(ly, "W2")]["under"]]
w2end = sum(1 for n, ly in w2feas if abs(next(x for x in T if x["name"] == n)["Cfull"][(ly, "W2")]["eta"]) < 1e-9)
P(f"  W2 minimum at the eta = 0 endpoint (pure closed box + strip) in {w2end} of {len(w2feas)} feasible gas-free dwarf-yield cases "
  f"({3 * sum(1 for x in T if not x['gas']) - len(w2feas)} under-produce)")
RES["W2_endpoint"] = dict(at_endpoint=w2end, feasible=len(w2feas))
P()

# per-footing counts and sample median
SUMM = {}
for f in FOOTS:
    cnt = {c: [x["name"] for x in T if x["cls"][f]["graded"] == c] for c in (CLS_C, CLS_U, CLS_X)}
    cntc = {c: sum(x["cls"][f]["central"] == c for x in T) for c in (CLS_C, CLS_U, CLS_X)}
    Lr = np.array([x["cls"][f]["L_req"] for x in T]); Cmat = {k: np.array([x["C"][0][k] for x in T]) for k in T[0]["C"][0]}
    mc, mres = median_class(Lr, Cmat, IDX)
    allL = np.exp(4 * np.array([d["E"][f] for d in OOS])); h = float(np.median(allL))
    SUMM[f] = dict(per_dwarf=cnt, counts={c: len(v) for c, v in cnt.items()}, central_counts=cntc, median_class=mc, median=mres,
                   headline_median_all28=h, headline_vs_Mk={ck(k): h / float(np.median(C)) for k, C in Cmat.items()})
    P(f"[{f}] per-dwarf graded: COMPATIBLE {len(cnt[CLS_C])}, UNDERDETERMINED {len(cnt[CLS_U])}, CONTRADICTED {len(cnt[CLS_X])}  "
      f"(central values: {cntc[CLS_C]} / {cntc[CLS_U]} / {cntc[CLS_X]})")
    for c in (CLS_C, CLS_X):
        P(f"     {c}: {', '.join(cnt[c]) or '-'}")
    P(f"     sample median: M_req {mres[ck((-0.5, 'W2'))]['M_req']:.2f} over the tested {len(T)} (CFG915 headline, all 28: {h:.2f})")
    for k in Cmat:
        v = mres[ck(k)]
        P(f"       corner {ck(k):9s}: median L_min {v['M_k']:7.2f}; ratio {v['ratio']:.3f} [16-84% {v['p16']:.3f}-{v['p84']:.3f}]; "
          f"median per-dwarf ratio {v['median_per_dwarf_ratio']:.3f}; headline/M_k {SUMM[f]['headline_vs_Mk'][ck(k)]:.3f}")
    P(f"     SAMPLE-MEDIAN CLASS [{f}]: {mc}")
    P()
overall = SUMM["canonical"]["median_class"] if SUMM["canonical"]["median_class"] == SUMM["alt"]["median_class"] else \
    f"SPLIT (canonical {SUMM['canonical']['median_class']} / alt {SUMM['alt']['median_class']})"
P(f"OVERALL CFG920 CLASS (sample median, both footings): {overall}")
P()

# ---------------------------------------------------------------------------- per-dwarf diagnostics, timing, zeta_need
P("DIAGNOSTICS (reported): E_pred = ln(L_min)/4 at (-0.5, W2) and (-0.2, W1) vs E_obs; unseen-loss factor L_req / L_W1(-0.2)")
for x in T:
    C0 = x["C"][0]
    x["diag"] = dict(Epred_m05_W2=math.log(C0[(-0.5, "W2")]) / 4, Epred_m02_W1=math.log(C0[(-0.2, "W1")]) / 4,
                     unseen_factor_can=x["cls"]["canonical"]["L_req"] / C0[(-0.2, "W1")], unseen_factor_alt=x["cls"]["alt"]["L_req"] / C0[(-0.2, "W1")])
    P(f"  {x['name']:17s} E_obs {x['E']['canonical']:+.3f} (alt {x['E']['alt']:+.3f}, sE {x['sE']:.3f})  E_pred {x['diag']['Epred_m05_W2']:+.3f} / "
      f"{x['diag']['Epred_m02_W1']:+.3f}  unseen x{x['diag']['unseen_factor_can']:.2f}")
# POST-HOC REPORTING SUMMARY (added after the first full run, 2026-10-20; counts of values already computed; no class weight)
SPLIT = {}
for f in FOOTS:
    SPLIT[f] = {}
    for grp, sel in (("gas-free", False), ("gas-bearing", True)):
        S = [x for x in T if x["gas"] == sel]
        SPLIT[f][grp] = dict(N=len(S), graded={c: sum(x["cls"][f]["graded"] == c for x in S) for c in (CLS_C, CLS_U, CLS_X)},
                             central={c: sum(x["cls"][f]["central"] == c for x in S) for c in (CLS_C, CLS_U, CLS_X)},
                             overpred_m05_W2=sum(x["diag"]["Epred_m05_W2"] > x["E"][f] for x in S),
                             overpred_m02_W1=sum(x["diag"]["Epred_m02_W1"] > x["E"][f] for x in S),
                             Lreq_range=[min(x["cls"][f]["L_req"] for x in S), max(x["cls"][f]["L_req"] for x in S)],
                             Lmin_m02_W2_range=[min(x["C"][0][(-0.2, "W2")] for x in S), max(x["C"][0][(-0.2, "W2")] for x in S)],
                             Lmin_m05_W2_range=[min(x["C"][0][(-0.5, "W2")] for x in S), max(x["C"][0][(-0.5, "W2")] for x in S)])
        v = SPLIT[f][grp]
        P(f"  [post-hoc summary, {f}] {grp} N {v['N']}: graded {v['graded']}; E_pred > E_obs (D-i over-predicts) at (-0.5,W2) "
          f"{v['overpred_m05_W2']}, at (-0.2,W1) {v['overpred_m02_W1']}; L_req {v['Lreq_range'][0]:.2f}-{v['Lreq_range'][1]:.2f}; "
          f"L_min(-0.5,W2) {v['Lmin_m05_W2_range'][0]:.2f}-{v['Lmin_m05_W2_range'][1]:.2f}; L_min(-0.2,W2) {v['Lmin_m02_W2_range'][0]:.2f}-{v['Lmin_m02_W2_range'][1]:.2f}")
RES["posthoc_split"] = SPLIT
P()
P("TIMING MAP (central values; binding after a fraction F of the star formation; Weisz+14 clock, onset 13.3 Gyr)")
P(f"  {'dwarf':17s} {'tau50':>6s} {'tau90':>6s} | yield -0.5: F_need  t_need  reading     | yield -0.2: F_need  t_need  reading   [canonical; alt]")
for x in T:
    x["timing"] = {}
    for f in FOOTS:
        x["timing"][f] = {f"{ly:+.1f}": timing(x, x["cls"][f]["L_req"], ly) for ly in (-0.5, -0.2)}

    def fm(tm):
        if tm["F_need"] is None: return f"{'-':>6s} {'-':>6s}  {tm['reading']:10s}"
        return f"{tm['F_need']:6.3f} {tm['t_need']:6.2f}  {tm['reading']:10s}"
    tc, ta = x["timing"]["canonical"], x["timing"]["alt"]
    P(f"  {x['name']:17s} {x['tau50']:6.2f} {x['tau90']:6.2f} | {fm(tc['-0.5'])}  | {fm(tc['-0.2'])} [alt: {ta['-0.5']['reading']} / {ta['-0.2']['reading']}]")
TSUM = {f: {ly: {r_: sum(x["timing"][f][ly]["reading"] == r_ for x in T) for r_ in ("AT FORMATION", "EARLY", "LATE", "NONE")} for ly in ("-0.5", "-0.2")} for f in FOOTS}
for f in FOOTS:
    P(f"  [{f}] readings at yield -0.5: {TSUM[f]['-0.5']}; at -0.2: {TSUM[f]['-0.2']}")
P()
P("METAL-ENHANCED-WIND PRICE (reported escape, no class weight): zeta_need at yield -0.5 for the central L_req")
for x in T:
    x["zeta_need"] = {f: zeta_need(x["cls"][f]["L_req"], x["feh"], x["Ms"], x["Mg"]) for f in FOOTS}
    fz = lambda z: f"{z:8.2f}" if isinstance(z, float) else f"{z:>8s}"
    P(f"  {x['name']:17s} zeta_need canonical {fz(x['zeta_need']['canonical'])}   alt {fz(x['zeta_need']['alt'])}")
ZS = {}
for f in FOOTS:
    zz = [x["zeta_need"][f] for x in T]
    num = [z if isinstance(z, float) else (1e9 if z.startswith(">") or z.startswith("none") else np.nan) for z in zz]
    ZS[f] = dict(n_eq1=sum(1 for z in zz if z == 1.0), n_gt1000=sum(1 for z in zz if isinstance(z, str) and z.startswith(">")),
                 n_none=sum(1 for z in zz if isinstance(z, str) and z.startswith("none")), median=float(np.median(num)))
    P(f"  [{f}] zeta_need = 1 (held by the homogeneous box at -0.5): {ZS[f]['n_eq1']}; > 1000: {ZS[f]['n_gt1000']}; none (L_req <= 1): "
      f"{ZS[f]['n_none']}; median zeta_need {ZS[f]['median']:.2f} (> 1000 / none counted as infinite)")
P()

# ---------------------------------------------------------------------------- variants (reported, not graded)
P("VARIANTS (reported, not graded)")
VAR = {}
# V-NOUNSEEN
for f in FOOTS:
    nc = [x["name"] for x in T if x["cls"][f]["L_req"] > x["C"][0][(0.1, "W1")]]
    nr = [x["name"] for x in T if math.exp(4 * (x["E"][f] - x["sE"])) > x["C"][-1][(0.1, "W1")]]
    VAR.setdefault("NOUNSEEN", {})[f] = dict(central=nc, one_sigma=nr)
    P(f"  V-NOUNSEEN [{f}]: L_req > L_W1(+0.1) (needs unseen loss even at the most generous chemistry): central {len(nc)} {nc}; at 1 sigma {len(nr)} {nr}")
# V-2sigma
for f in FOOTS:
    c2 = {c: [x["name"] for x in T if x["cls"][f]["two_sigma"] == c] for c in (CLS_C, CLS_U, CLS_X)}
    VAR.setdefault("TWO_SIGMA", {})[f] = c2
    P(f"  V-2sigma [{f}]: COMPATIBLE {len(c2[CLS_C])}, UNDERDETERMINED {len(c2[CLS_U])}, CONTRADICTED {len(c2[CLS_X])} {c2[CLS_X]}")
# V-GAS
gasrows = {}
for x in T:
    if not x["gas"]: continue
    Eg = {f: math.log(x["so"] / law_M(x["Ms"] + x["Mg"], x["rhl"], A0[f])) for f in FOOTS}
    xg = dict(x); xg["Eg"] = Eg
    cg = dwarf_classes(xg, Lreq_E(xg, "Eg"))
    gasrows[x["name"]] = dict(E_gas=Eg, L_req_gas={f: cg[f]["L_req"] for f in FOOTS}, graded={f: cg[f]["graded"] for f in FOOTS})
    P(f"  V-GAS {x['name']:17s} E {x['E']['canonical']:+.3f} -> {Eg['canonical']:+.3f}; L_req {x['cls']['canonical']['L_req']:.2f} -> "
      f"{cg['canonical']['L_req']:.2f}; graded {x['cls']['canonical']['graded']} -> {cg['canonical']['graded']} (alt -> {cg['alt']['graded']})")
VAR["GAS"] = gasrows
# V-COL
TC = [x for x in (prep(d, collins=True) for d in OOS) if x is not None]
colrows = {}
for x in TC:
    if x["msrc"] == "Collins+13":
        x["cls"] = dwarf_classes(x, Lreq_E(x))
        colrows[x["name"]] = dict(feh=x["feh"], s=x["s"], L_req={f: x["cls"][f]["L_req"] for f in FOOTS}, graded={f: x["cls"][f]["graded"] for f in FOOTS},
                                  L_min={ck(k): v for k, v in x["C"][0].items()})
        P(f"  V-COL {x['name']:17s} [Fe/H] {x['feh']:+.2f} (Collins+13); L_req {x['cls']['canonical']['L_req']:.2f}; L_min(-0.5,W2) {x['C'][0][(-0.5, 'W2')]:.2f}; "
          f"graded {x['cls']['canonical']['graded']} / alt {x['cls']['alt']['graded']}")
    else:
        x["cls"] = next(y["cls"] for y in T if y["name"] == x["name"])
idxc = np.random.default_rng(SEED).integers(0, len(TC), size=(NBOOT, len(TC)))
VAR["COL"] = dict(rows=colrows, N=len(TC), median_class={})
for f in FOOTS:
    mcc, mrc = median_class(np.array([x["cls"][f]["L_req"] for x in TC]), {k: np.array([x["C"][0][k] for x in TC]) for k in TC[0]["C"][0]}, idxc)
    VAR["COL"]["median_class"][f] = dict(cls=mcc, corners=mrc)
    P(f"  V-COL [{f}] sample median over {len(TC)}: {mcc} (most favourable corner -0.5|W2 ratio {mrc[ck((-0.5, 'W2'))]['ratio']:.3f}, "
      f"p84 {mrc[ck((-0.5, 'W2'))]['p84']:.3f})")
# V-TR
trrows = {}
for d in TRN:
    x = prep(d)
    if x is None: continue
    x["cls"] = dwarf_classes(x, Lreq_E(x))
    trrows[x["name"]] = dict(feh=x["feh"], L_req={f: x["cls"][f]["L_req"] for f in FOOTS}, graded={f: x["cls"][f]["graded"] for f in FOOTS},
                             L_min={ck(k): v for k, v in x["C"][0].items()})
    P(f"  V-TR  {x['name']:17s} [Fe/H] {x['feh']:+.2f}; E {x['E']['canonical']:+.3f}; L_req {x['cls']['canonical']['L_req']:.2f}; "
      f"L_min(-0.5,W2) {x['C'][0][(-0.5, 'W2')]:.2f}, (+0.1,W1) {x['C'][0][(0.1, 'W1')]:.2f}; graded {x['cls']['canonical']['graded']} / alt {x['cls']['alt']['graded']}")
VAR["TR"] = trrows
P()

# ---------------------------------------------------------------------------- write
for x in T:
    ROWOUT[x["name"]] = dict(gas=x["gas"], feh=x["feh"], efeh=x["efeh"], s=x["s"], msrc=x["msrc"], Ms=x["Ms"], Mg=x["Mg"], ups=x["ups"],
                             E=x["E"], sE=x["sE"], tau50=x["tau50"], tau90=x["tau90"],
                             L_req={f: x["cls"][f]["L_req"] for f in FOOTS}, classes=x["cls"],
                             L_min={str(sh): {ck(k): v for k, v in x["C"][sh].items()} for sh in x["C"]},
                             eta={ck(k): v["eta"] for k, v in x["Cfull"].items()}, under={ck(k): v["under"] for k, v in x["Cfull"].items()},
                             diag=x["diag"], timing=x["timing"], zeta_need=x["zeta_need"])
RES.update(tested=[x["name"] for x in T], not_tested=NT, rows=ROWOUT, summary=SUMM, overall=overall, timing_summary=TSUM, zeta_summary=ZS,
           variants=VAR, under_flags=flags)
allK = all(v["ok"] for v in K.values())
P(f"K: {sum(v['ok'] for v in K.values())}/{len(K)} PASS")
json.dump(RES, open(os.path.join(HERE, "cfg920_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg920.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if allK else 1)
