"""CFG88 -- independent re-derivation of CFG42's satellites headline.  The frozen spec is CFG88_SPEC_FROZEN.txt (sha256 in CFG88_SPEC_FROZEN.sha256),
written before this file was first run.  MUTATE=1: every M_coll / 100 after clamp.  Run: python3 cfg88.py   (main)   MUTATE=1 python3 cfg88.py"""
import os, sys, math, json, hashlib
import numpy as np, pandas as pd
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CFG88_SPEC_FROZEN.txt")
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/dsph"
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FB = 0.02237 / 0.14237
OMEGA_M = 0.3153; H0 = 67.4e3 / 3.0857e22          # s^-1
RHO_C = 3 * H0**2 / (8 * math.pi * G)               # kg/m^3
RHO_M = OMEGA_M * RHO_C
DELTA_TA = 11.81; X_E = 0.40
RHO_C_MSUN_KPC3 = RHO_C * KPC**3 / MSUN

FAILS = []; LOG = []
def out(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)
def check(name, ok, detail=""):
    out(("[PASS] " if ok else "[FAIL] ") + name + ("  " + detail if detail else ""))
    if not ok: FAILS.append(name)

# ------------------------------------------------------------------ kernels
def nu_rar(y): y = max(y, 1e-14); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))
def nu_p2(y): y = max(y, 1e-14); return math.sqrt(1.0 + 1.0 / y)
def nu_simple(y): y = max(y, 1e-14); return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
def nu_one(y): return 1.0
KERNELS = {"RAR": nu_rar, "P2": nu_p2, "simple": nu_simple}

# ------------------------------------------------------------------ Moster + NFW + concentrations
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10.0 ** (np.asarray(logMh, float) - logM1)
    return 10.0 ** np.asarray(logMh, float) * 2 * N / (x ** (-be) + x ** ga)
_LMH = np.linspace(9.0, 15.5, 1301); _LMS = np.log10(moster_mstar(_LMH))
_LMH_X = np.linspace(6.0, 15.5, 1901); _LMS_X = np.log10(moster_mstar(_LMH_X))
def mcoll_from_mstar(Mstar, clamp=None, unclamped=False):
    """M_200c from the inverse Moster relation.  Default: grid 9..15.5 with np.interp clamp (=1e9 below M_*(1e9)); clamp=X sets X where clamped."""
    lm = math.log10(Mstar)
    if unclamped: return 10 ** float(np.interp(lm, _LMS_X, _LMH_X))
    if lm < _LMS[0]:
        return 1e9 if clamp is None else clamp
    return 10 ** float(np.interp(lm, _LMS, _LMH))
def conc_DM(M): return 10 ** (0.905 - 0.101 * (math.log10(M * 0.674) - 12.0))
def _duffy(A, B):
    return lambda M: A * (M * 0.674 / 2e12) ** B
CONC = {"DM14": conc_DM, "Duffy200c_full": _duffy(5.71, -0.084), "Duffy200c_relaxed": _duffy(6.71, -0.091),
        "Duffy200c_full_z0": _duffy(5.74, -0.097), "Duffy200c_relaxed_z0": _duffy(6.67, -0.092), "Duffy200m_full(inconsistent)": _duffy(10.14, -0.081)}
def m_nfw(t): return math.log1p(t) - t / (1.0 + t)
def r200_kpc(Mh): return (3 * Mh / (4 * math.pi * 200 * RHO_C_MSUN_KPC3)) ** (1 / 3.0)
def nfw_enclosed(Mh, r_kpc, conc):
    c = conc(Mh); x = r_kpc / r200_kpc(Mh)
    return Mh * m_nfw(c * x) / m_nfw(c)

# ------------------------------------------------------------------ data
def mstar_from_MV(MV, ups=2.0): return ups * 10 ** (-0.4 * (MV - 4.83))
def load():
    mw = pd.read_csv(f"{DATA}/lvd_dwarf_mw.csv"); m31 = pd.read_csv(f"{DATA}/lvd_dwarf_m31.csv"); lf = pd.read_csv(f"{DATA}/lvd_dwarf_local_field.csv")
    def rows(df, pop, ul_ok=False):
        R = []
        for _, r in df.iterrows():
            ul = pd.isna(r.vlos_sigma)
            if ul and not (ul_ok and pd.notna(r.vlos_sigma_ul)): continue
            sig = r.vlos_sigma_ul if ul else r.vlos_sigma
            err = 0.0 if ul else 0.5 * (r.vlos_sigma_em + r.vlos_sigma_ep)
            R.append(dict(name=r["name"], host=r["host"], pop=pop, MV=r.M_V, Re_pc=r.rhalf_sph_physical, Re_maj_pc=r.rhalf_physical, sig=sig, err=err, ul=bool(ul),
                          lgHI=r.mass_HI if pd.notna(r.mass_HI) else None, ell=r.ellipticity, dist=r.distance, key=r["key"]))
        return R
    mwr = rows(mw, "mw", ul_ok=True)
    ufd = [s for s in mwr if s["MV"] > -7.7]; cls = [s for s in mwr if s["MV"] <= -7.7]
    for s in ufd: s["pop"] = "ufd"
    for s in cls: s["pop"] = "classical"
    lvd = rows(m31, "m31lvd")
    return ufd, cls, lvd, lf

def load_collins():
    lines = [l.rstrip("\n") for l in open(f"{DATA}/collins2013_m31_dsph.tsv") if not l.startswith("#") and l.strip()]
    hdr = lines[0].split("\t"); body = [l.split("\t") for l in lines[3:]]
    df = pd.DataFrame(body, columns=hdr)
    R = []
    for _, r in df.iterrows():
        sg = float(r["sigV"])
        if sg <= 0: continue
        R.append(dict(name=r["Gal"].strip(), host="m_031", pop="collins", MV=float(r["VMag"]), Re_pc=float(r["rh"]), Re_maj_pc=float(r["rh"]), sig=sg,
                      err=0.5 * (float(r["E_sigV"]) + float(r["e_sigV"])), ul=False, lgHI=None, ell=np.nan, dist=float(r["Dist"]), key=r["Gal"].strip()))
    return R

def calib_set(lf):
    C = []
    for _, r in lf.iterrows():
        if pd.isna(r.M_V) or pd.isna(r.mass_stellar): continue
        if pd.notna(r.mass_HI): q = 1.33 * 10 ** r.mass_HI / 10 ** r.mass_stellar; C.append((r.mass_stellar, q, "det", q))
        elif pd.notna(r.mass_HI_ul): C.append((r.mass_stellar, 0.0, "ul", 1.33 * 10 ** r.mass_HI_ul / 10 ** r.mass_stellar))
    return C

# ------------------------------------------------------------------ config
class Cfg:
    def __init__(self, **kw):
        self.kernel = "RAR"; self.conc = "DM14"; self.ups = 2.0; self.clamp = None; self.unclamped = False; self.phi = 1.0
        self.fixed_mcoll = None; self.gas = "A1"; self.foot = "canonical"; self.mcoll_div = 1.0; self.small_mcoll = None; self.re_key = "Re_pc"
        self.__dict__.update(kw)
    def copy(self, **kw): c = Cfg(); c.__dict__.update(self.__dict__); c.__dict__.update(kw); return c

def gas_ratio(s, cfg, CAL):
    """infall gas ratio to M_* : current gas, and (in range) the expectation over the 5 nearest calibration dwarfs."""
    lgL2 = math.log10(mstar_from_MV(s["MV"], 2.0))
    Mst = mstar_from_MV(s["MV"], cfg.ups)
    r_cur = (1.33 * 10 ** s["lgHI"] / Mst) if s["lgHI"] is not None else 0.0
    if cfg.gas == "none": return 0.0
    if s["pop"] == "ufd": return 0.0  # UFD: stars only (R4)
    lo, hi = 4.98, 9.65
    if not (lo <= lgL2 <= hi):
        return r_cur
    order = sorted(CAL, key=lambda c: abs(c[0] - lgL2))[:5]
    if cfg.gas == "A1":  return float(np.mean([max(r_cur, c[1]) for c in order]))
    if cfg.gas == "A2":  return max(r_cur, float(np.mean([c[1] for c in order])))
    if cfg.gas == "ulatlimit": return float(np.mean([max(r_cur, c[3]) for c in order]))
    raise ValueError

def edge_phantom(Mb, a0, nu):
    """M_ph(<x_e r_ta) [Msun] for a baryonic mass Mb [Msun], monopole law M_law(r) = Mb nu(G Mb/(r^2 a0))."""
    Mb_kg = Mb * MSUN
    def Mlaw(r): return Mb_kg * nu(G * Mb_kg / (r * r * a0))
    def f(lr):
        r = math.exp(lr); return 3 * Mlaw(r) / (4 * math.pi * r ** 3) - DELTA_TA * RHO_M
    rta = math.exp(brentq(f, math.log(1e-3 * KPC), math.log(1e5 * KPC), xtol=1e-13, rtol=1e-13))
    re = X_E * rta
    return (Mlaw(re) - Mb_kg) / MSUN, rta / KPC

def predict(s, cfg, CAL, want_detail=False):
    a0 = A0[cfg.foot]; nu = KERNELS[cfg.kernel]; conc = CONC[cfg.conc]
    Mst = mstar_from_MV(s["MV"], cfg.ups)
    rg = gas_ratio(s, cfg, CAL)
    Mb = Mst * (1.0 + rg)
    r = 4.0 / 3.0 * s[cfg.re_key] * 1e-3 * KPC          # m
    gN = G * (Mb * MSUN / 2.0) / (r * r)
    g = nu(gN / a0) * gN
    dark_g = 0.0; det = {}
    if cfg.phi != 0.0:
        Mc = mcoll_from_mstar(Mst, clamp=cfg.clamp, unclamped=cfg.unclamped)
        if cfg.small_mcoll is not None and Mst < 1e5: Mc = cfg.small_mcoll
        if cfg.fixed_mcoll is not None: Mc = cfg.fixed_mcoll
        Mc = Mc / cfg.mcoll_div
        Mph, rta = edge_phantom(Mb, a0, nu)
        fex = max(0.0, 1.0 - Mph / ((1 - FB) * Mc))
        Mn = nfw_enclosed(Mc, r / KPC, conc)
        dark_g = cfg.phi * G * fex * (1 - FB) * Mn * MSUN / (r * r)
        det = dict(Mc=Mc, fex=fex, Mph=Mph, rta=rta, Mn=Mn, Mb=Mb, Mst=Mst)
    sig = math.sqrt((g + dark_g) * r / 3.0) / 1e3
    return (sig, det) if want_detail else sig

def offsets(systems, cfg, CAL):
    return np.array([math.log10(s["sig"] / predict(s, cfg, CAL)) for s in systems])

# ------------------------------------------------------------------ statistics
def km_median(x, cens):
    """left-censored KM: x = offsets, cens=True means the true value is BELOW x."""
    y = -np.asarray(x, float); c = np.asarray(cens, bool)   # right-censored in y
    order = np.lexsort((c, y))                               # ties: events (False) before censors (True)
    y = y[order]; c = c[order]
    n = len(y); S = 1.0; at_risk = n
    for i in range(n):
        if not c[i]:
            S *= (1 - 1.0 / at_risk)
            if S <= 0.5: return -y[i]
        at_risk -= 1
    return -y[-1]
def med(x, cens):
    return km_median(x, cens) if np.any(cens) else float(np.median(x))
def boot_stat(x, cens, nb=4000, seed=88):
    rng = np.random.default_rng(seed); n = len(x); m = np.empty(nb)
    for b in range(nb):
        i = rng.integers(0, n, n); m[b] = med(x[i], cens[i])
    return float(np.std(m, ddof=1))

def row(systems, cfg, CAL, coll_floor, seed=88):
    """offset, stat, floors, total for one population and one config (law = phi 0, rule = phi given)."""
    cens = np.array([s["ul"] for s in systems])
    x = offsets(systems, cfg, CAL); m = med(x, cens); st = boot_stat(x, cens, seed=seed)
    ms = [med(offsets(systems, cfg.copy(ups=u), CAL), cens) for u in (1.0, 2.0, 4.0)]
    fU = 0.5 * (max(ms) - min(ms))
    fC = 0.0
    if coll_floor and cfg.phi != 0.0:
        mc = [med(offsets(systems, cfg.copy(small_mcoll=v), CAL), cens) for v in (1e8, 1e9, 1e10)]
        fC = 0.5 * (max(mc) - min(mc))
    tot = math.sqrt(st ** 2 + fU ** 2 + fC ** 2)
    return dict(off=m, stat=st, fU=fU, fC=fC, tot=tot, z=m / tot, n=len(systems), nlim=int(cens.sum()), x=x)

def fmt(r): return f"{r['off']:+.3f} +/- {r['tot']:.3f} ({r['z']:+.2f}s)  [stat {r['stat']:.3f} U {r['fU']:.3f} C {r['fC']:.3f}]"

# ================================================================== MAIN
def main():
    out("CFG88 main" + (" [MUTATE=1: every M_coll / 100]" if MUTATE else ""))
    out("spec sha256:", hashlib.sha256(open(SPEC, "rb").read()).hexdigest())
    ufd, cls, lvd, lf = load(); col = load_collins(); CAL = calib_set(lf)
    check("C3 sample sizes: UFD 40 (31 resolved + 9 limits), classical 14, M31 LVD 34, Collins 14, calibration 42 (32 det + 10 ul)",
          (len(ufd), sum(s["ul"] for s in ufd), len(cls), len(lvd), len(col), len(CAL), sum(c[2] == "det" for c in CAL)) == (40, 9, 14, 34, 14, 42, 32),
          str((len(ufd), sum(s["ul"] for s in ufd), len(cls), len(lvd), len(col), len(CAL), sum(c[2] == "det" for c in CAL))))
    base = Cfg(); base_mut = base.copy(mcoll_div=100.0) if MUTATE else base
    # ---------------- controls C1, C2
    s0 = dict(name="t", host="x", pop="classical", MV=-9.0, Re_pc=300.0, Re_maj_pc=300.0, sig=8.0, err=1.0, ul=False, lgHI=None)
    Mst = mstar_from_MV(-9.0); r = 4 / 3 * 300e-3 * KPC
    sig_N = math.sqrt(G * Mst * MSUN / 2 / r ** 2 * r / 3) / 1e3
    KERNELS["one"] = nu_one
    sigN = predict(s0, Cfg(kernel="one", phi=0.0, gas="none"), CAL)
    check("C1a Newtonian limit nu=1 equals sqrt(G M_half/(3 r)) to 1e-12", abs(sigN / sig_N - 1) < 1e-12, f"{sigN:.6f} vs {sig_N:.6f}")
    for kn in ("RAR", "P2"):
        st = dict(s0); st["MV"] = 2.5   # first run used MV=20 (y=8e-15 < the 1e-14 kernel floor): control bug, disclosed
        Mst_t = mstar_from_MV(2.5)
        sg = predict(st, Cfg(kernel=kn, phi=0.0, gas="none"), CAL)
        sig_dm = (G * (Mst_t * MSUN / 2) * A0["canonical"]) ** 0.25 / math.sqrt(3) / 1e3
        y = G * (Mst_t * MSUN / 2) / r ** 2 / A0["canonical"]
        check(f"C1b deep-MOND limit ({kn}): sigma^4 = G M_half a0/9 within the analytic sqrt(y)/2 correction (y={y:.1e})", abs(sg / sig_dm - 1) < 2 * math.sqrt(y), f"ratio-1={sg/sig_dm-1:.2e} bound {2*math.sqrt(y):.1e}")
    # C2: phi
    bad = []; dmax0 = 0.0; dmax1 = 0.0
    for s in ufd + cls + lvd + col:
        c0 = Cfg(phi=0.0); c1 = Cfg(phi=1.0)
        sl = predict(s, c0, CAL); sr, d = predict(s, c1, CAL, True)
        # independent direct formula for the sum
        a0 = A0["canonical"]; Mb = d["Mb"]; rr = 4 / 3 * s["Re_pc"] * 1e-3 * KPC
        gN = G * Mb * MSUN / 2 / rr ** 2; g = gN / (1 - math.exp(-math.sqrt(gN / a0)))
        Mc = d["Mc"]; c = conc_DM(Mc); R = r200_kpc(Mc) * KPC; x = rr / R
        Mn = Mc * (math.log(1 + c * x) - c * x / (1 + c * x)) / (math.log(1 + c) - c / (1 + c))
        fex = max(0, 1 - d["Mph"] / ((1 - FB) * Mc))
        sr2 = math.sqrt((g + G * fex * (1 - FB) * Mn * MSUN / rr ** 2) * rr / 3) / 1e3
        dmax1 = max(dmax1, abs(sr / sr2 - 1))
        sl2 = math.sqrt(g * rr / 3) / 1e3; dmax0 = max(dmax0, abs(sl / sl2 - 1))
        if not (0 <= d["fex"] <= 1): bad.append(s["name"])
    check("C2a phi=0 reproduces the bare law (independent formula) to 1e-12", dmax0 < 1e-12, f"max {dmax0:.1e}")
    check("C2b phi=1 reproduces the sum by an independent direct formula to 1e-12", dmax1 < 1e-12, f"max {dmax1:.1e}")
    check("C2c f_ex in [0,1] everywhere", not bad)
    Mh = 3.7e10; c = conc_DM(Mh)
    check("C2d NFW: M(<R200) = M_h to 1e-12 and monotone", abs(nfw_enclosed(Mh, r200_kpc(Mh), conc_DM) / Mh - 1) < 1e-12 and all(nfw_enclosed(Mh, r1, conc_DM) < nfw_enclosed(Mh, r1 * 1.01, conc_DM) for r1 in np.logspace(-3, 2, 30)))
    dev = []
    for Mb in (1e2, 1e3, 1e4, 1e5):
        Mph, rta = edge_phantom(Mb, A0["canonical"], nu_p2)   # P2 -> exact 1/sqrt(y) in deep regime
        Mb_kg = Mb * MSUN; K = math.sqrt(Mb_kg * A0["canonical"] / G)
        rta_cf = math.sqrt(3 * K / (4 * math.pi * DELTA_TA * RHO_M)); Mph_cf = (X_E * rta_cf * K) / MSUN - Mb
        dev.append(abs(Mph / Mph_cf - 1))
    check("C2e edge phantom (root-find) equals the deep-MOND closed form for Mb<=1e5 (P2 kernel) to <1e-3", max(dev) < 1e-3, f"max {max(dev):.1e}")
    # ---------------- reproduction rows
    def pops(cfg_kw):
        return {"ufd": ufd, "classical": cls, "m31lvd": lvd, "collins": col}
    res = {}
    for foot in ("canonical", "alt"):
        for popn, P in pops(None).items():
            law = row(P, Cfg(phi=0.0, foot=foot), CAL, False)
            rule = row(P, Cfg(phi=1.0, foot=foot, mcoll_div=100.0 if MUTATE else 1.0), CAL, True)
            res[(foot, popn)] = (law, rule)
    out("\n=== P1-P5: offsets log10(sigma_obs/sigma_pred): law | rule (canonical / alt)  [CFG42: numbers in the spec] ===")
    for popn in ("ufd", "classical", "collins", "m31lvd"):
        for foot in ("canonical", "alt"):
            law, rule = res[(foot, popn)]
            out(f"{popn:10s} {foot:9s} n={law['n']:2d}(lim {law['nlim']})  LAW  {fmt(law)}")
            out(f"{'':10s} {'':9s}                RULE {fmt(rule)}")
    json.dump({f"{k[0]}|{k[1]}": {"law": {kk: vv for kk, vv in v[0].items() if kk != 'x'}, "rule": {kk: vv for kk, vv in v[1].items() if kk != 'x'}} for k, v in res.items()},
              open(f"cfg88_results{'_MUTATE' if MUTATE else ''}.json", "w"), indent=1)
    # ---------------- P6 f_ex
    def fex_list(P, cfg): return np.array([predict(s, cfg, CAL, True)[1]["fex"] for s in P])
    cfgP = Cfg(mcoll_div=100.0 if MUTATE else 1.0)
    f_u = fex_list(ufd, cfgP); f_c = fex_list(cls, cfgP)
    out(f"\nP6 f_ex: UFD median {np.median(f_u):.3f}, fraction > 0.5 = {np.mean(f_u > 0.5):.3f}; classical median {np.median(f_c):.3f}; LVD median {np.median(fex_list(lvd, cfgP)):.3f}; Collins median {np.median(fex_list(col, cfgP)):.3f}")
    # ---------------- P7 clamp
    Mst_u = np.array([mstar_from_MV(s["MV"]) for s in ufd]); thr = float(moster_mstar(9.0))
    nclamp = int(np.sum(Mst_u < thr)); unc = np.array([mcoll_from_mstar(m, unclamped=True) for m in Mst_u])
    out(f"P7 clamp: M_*(1e9) = {thr:.3e}; UFDs clamped {nclamp}/40; unclamped Moster (grid to 1e6): min {unc.min():.2e} median {np.median(unc):.2e} max {unc.max():.2e}")
    # ---------------- P8 scan
    out("P8 UFD rule KM median vs collapse mass (all UFDs, M_coll set directly; canonical):")
    cens_u = np.array([s["ul"] for s in ufd]); scan = {}
    for Mv in (1e8, 3e7, 2e8, 3e8, 1e9, 6e9, 1e10):
        x = offsets(ufd, Cfg(fixed_mcoll=Mv), CAL)
        scan[Mv] = med(x, cens_u); out(f"    M_coll = {Mv:.1e}: {scan[Mv]:+.3f}")
    out(f"    half-range over 1e8..1e10 = {0.5*(scan[1e8]-scan[1e10]):.3f}  [CFG42 floor 0.133]")
    # ---------------- P9 cusp
    out("P9 enclosed NFW mass at fixed small radius, ratio for 100x halo mass (DM14):")
    for M0, r0 in ((1e9, 0.05), (1e9, 0.1), (1e9, 0.3), (1e8, 0.1), (1e10, 0.1)):
        rat = nfw_enclosed(100 * M0, r0, conc_DM) / nfw_enclosed(M0, r0, conc_DM); out(f"    M {M0:.0e} -> {100*M0:.0e} at r={r0} kpc: {rat:.3f} (slope {math.log10(rat)/2:.3f}); c(M0) = {conc_DM(M0):.1f}")
    # ---------------- C4 mutate
    law_u, rule_u = res[("canonical", "ufd")]
    if MUTATE:
        open_ = abs(rule_u["z"]) > 2
        check("C4 MUTATE: UFD KM rule median stays OPEN (|z| > 2)", open_, f"{rule_u['off']:+.3f} ({rule_u['z']:+.2f} sigma)")
        h3 = np.mean(f_u > 0.5) >= 0.8
        check("C4 MUTATE: H3 (f_ex > 0.5 in >= 80% of UFDs) FAILS", not h3, f"fraction {np.mean(f_u>0.5):.3f}")
    else:
        closes = abs(rule_u["z"]) < 2
        out(f"H1 (UFD rule within 2 sigma): {'pass' if closes else 'FAIL'}; H2 (classical not below -2 sigma): " +
            ", ".join(f"{p}:{res[('canonical',p)][1]['z']:+.2f}/{res[('alt',p)][1]['z']:+.2f}" for p in ("classical", "m31lvd", "collins")))
    out("\nFAILED CONTROLS:", FAILS if FAILS else "none")
    open(f"cfg88{'_MUTATE' if MUTATE else ''}.out", "w").write("\n".join(LOG) + "\n")
    if MUTATE:
        sys.exit(1 if not (abs(rule_u["z"]) < 2) else 0)   # by design: the mutated rule must NOT close the UFDs -> rc 1
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
