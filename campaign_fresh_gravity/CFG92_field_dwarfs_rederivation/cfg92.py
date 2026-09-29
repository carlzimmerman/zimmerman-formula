"""CFG92 -- independent re-derivation of CFG58's field-dwarf + statistic-C headline.  Frozen spec: CFG92_SPEC_FROZEN.txt (sha256 in CFG92_SPEC_FROZEN.sha256; erratum CFG92_ERRATUM.txt).
Run: python3 cfg92.py (main);  MUTATE=1 python3 cfg92.py (every M_coll / 100 after clamp).  Writes cfg92[_MUTATE].out / _results.json."""
import os, sys, math, json, hashlib
import numpy as np, pandas as pd
from scipy.optimize import brentq

MUTATE = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/dsph"
G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FB = 0.02237 / 0.14237
OMEGA_M = 0.3153; H0 = 67.4e3 / 3.0857e22
RHO_C = 3 * H0**2 / (8 * math.pi * G); RHO_M = OMEGA_M * RHO_C
DELTA_TA = 11.81; X_E = 0.40
RHO_C_MSUN_KPC3 = RHO_C * KPC**3 / MSUN
FAILS = []; LOG = []
def out(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)
def check(name, ok, detail=""):
    out(("[PASS] " if ok else "[FAIL] ") + name + ("  " + detail if detail else ""))
    if not ok: FAILS.append(name)

# ---------------- kernels
def nu_rar(y): y = max(y, 1e-14); return 1.0 / (1.0 - math.exp(-math.sqrt(y)))
def nu_p2(y): y = max(y, 1e-14); return math.sqrt(1.0 + 1.0 / y)
def nu_simple(y): y = max(y, 1e-14); return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
def nu_one(y): return 1.0
KERNELS = {"RAR": nu_rar, "P2": nu_p2, "simple": nu_simple, "one": nu_one}

# ---------------- Moster + NFW
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10.0 ** (np.asarray(logMh, float) - logM1)
    return 10.0 ** np.asarray(logMh, float) * 2 * N / (x ** (-be) + x ** ga)
_LMH = np.linspace(9.0, 15.5, 1301); _LMS = np.log10(moster_mstar(_LMH))
_LMHX = np.linspace(6.0, 15.5, 1901); _LMSX = np.log10(moster_mstar(_LMHX))
def mcoll(Mst, cfg):
    lm = math.log10(Mst)
    if cfg.unclamped: M = 10 ** float(np.interp(lm, _LMSX, _LMHX))
    elif lm < _LMS[0]: M = cfg.clamp if cfg.clamp is not None else 1e9
    else: M = 10 ** float(np.interp(lm, _LMS, _LMH))
    if cfg.small_mcoll is not None and Mst < 1e5: M = cfg.small_mcoll
    return M / cfg.mcoll_div
def _duffy(A, B): return lambda M: A * (M * 0.674 / 2e12) ** B
def conc_DM(M): return 10 ** (0.905 - 0.101 * (math.log10(M * 0.674) - 12.0))
CONC = {"DM14": conc_DM, "Duffy200c_full": _duffy(5.71, -0.084), "Duffy200c_relaxed": _duffy(6.71, -0.091),
        "Duffy200c_full_z0": _duffy(5.74, -0.097), "Duffy200c_relaxed_z0": _duffy(6.67, -0.092), "Duffy200m_full_inconsistent": _duffy(10.14, -0.081)}
def m_nfw(t): return math.log1p(t) - t / (1.0 + t)
def r200_kpc(Mh): return (3 * Mh / (4 * math.pi * 200 * RHO_C_MSUN_KPC3)) ** (1 / 3.0)
def nfw_enclosed(Mh, r_kpc, conc):
    c = conc(Mh); x = r_kpc / r200_kpc(Mh); return Mh * m_nfw(c * x) / m_nfw(c)

_EP = {}
def edge_phantom(Mb, a0, kname):
    key = (round(math.log10(Mb), 12), a0, kname)
    if key in _EP: return _EP[key]
    nu = KERNELS[kname]; Mb_kg = Mb * MSUN
    def Mlaw(r): return Mb_kg * nu(G * Mb_kg / (r * r * a0))
    f = lambda lr: 3 * Mlaw(math.exp(lr)) / (4 * math.pi * math.exp(lr) ** 3) - DELTA_TA * RHO_M
    rta = math.exp(brentq(f, math.log(1e-3 * KPC), math.log(1e6 * KPC), xtol=1e-13, rtol=1e-13))
    v = ((Mlaw(X_E * rta) - Mb_kg) / MSUN, rta / KPC); _EP[key] = v; return v

def fex_of(Mb, Mst, cfg, a0):
    Mc = mcoll(Mst, cfg); Mph, rta = edge_phantom(Mb, a0, cfg.kernel)
    return max(0.0, 1.0 - Mph / ((1 - FB) * Mc)), Mc, Mph

# ---------------- data
def Mst_of(MV, ups=2.0): return ups * 10 ** (-0.4 * (MV - 4.83))
def load():
    D = {}
    for k, f in (("mw", "lvd_dwarf_mw.csv"), ("m31", "lvd_dwarf_m31.csv"), ("field", "lvd_dwarf_local_field.csv")): D[k] = pd.read_csv(f"{DATA}/{f}")
    rows = []
    for pop, df in D.items():
        for _, r in df[df.vlos_sigma.notna()].iterrows():
            hi_det = pd.notna(r.mass_HI); hi_ul = (not hi_det) and pd.notna(r.mass_HI_ul)
            rows.append(dict(pop=pop, name=r["name"], host=r["host"], MV=r.M_V, Re_sph=r.rhalf_sph_physical, Re_maj=r.rhalf_physical,
                             sig=r.vlos_sigma, err=0.5 * (r.vlos_sigma_em + r.vlos_sigma_ep),
                             HI=(10 ** r.mass_HI if hi_det else 0.0), HI_ul=(10 ** r.mass_HI_ul if hi_ul else 0.0), has_hi_ul=hi_ul,
                             dgc=r.distance_gc, dm31=r.distance_m31, dh=r.distance_host))
    return rows

class Cfg:
    def __init__(self, **kw):
        self.kernel = "RAR"; self.conc = "DM14"; self.ups = 2.0; self.clamp = None; self.unclamped = False; self.phi = 1.0
        self.foot = "canonical"; self.mcoll_div = 1.0; self.small_mcoll = None; self.re_key = "Re_sph"; self.est = "FG"; self.ul_at_limit = False
        self.halo_ups = 2.0; self.__dict__.update(kw)
    def copy(self, **kw): c = Cfg(); c.__dict__.update(self.__dict__); c.__dict__.update(kw); return c

def masses(s, cfg):
    Mst = Mst_of(s["MV"], cfg.ups); gas = 1.33 * (s["HI"] + (s["HI_ul"] if cfg.ul_at_limit else 0.0))
    return Mst, Mst + gas
def predict(s, cfg, detail=False):
    a0 = A0[cfg.foot]; nu = KERNELS[cfg.kernel]; conc = CONC[cfg.conc]
    Mst, Mb = masses(s, cfg)
    Mst_h = Mst_of(s["MV"], cfg.halo_ups)                      # what the halo (M_coll) sees
    if cfg.est == "FG":
        r = 4.0 / 3.0 * s[cfg.re_key] * 1e-3 * KPC; gN = G * (Mb * MSUN / 2.0) / (r * r); g = nu(gN / a0) * gN; kfac = 1.0 / 3.0
        rr = r
    else:
        r = s[cfg.re_key] * 1e-3 * KPC; gN = G * Mb * MSUN / (r * r); g = nu(gN / a0) * gN; kfac = 2.0 / 9.0
        rr = r
    dark = 0.0; det = dict(Mb=Mb, Mst=Mst)
    if cfg.phi != 0.0:
        fex, Mc, Mph = fex_of(Mb, Mst_h, cfg, a0)
        Mn = nfw_enclosed(Mc, rr / KPC, conc)
        dark = cfg.phi * G * fex * (1 - FB) * Mn * MSUN / (rr * rr)
        det.update(fex=fex, Mc=Mc, Mph=Mph, Mn=Mn)
    sig2 = (g + dark) * rr * kfac if cfg.est == "FG" else kfac * (g + dark) * rr
    sig = math.sqrt(sig2) / 1e3
    return (sig, det) if detail else sig
def offs(P, cfg): return np.array([math.log10(s["sig"] / predict(s, cfg)) for s in P])

# ---------------- statistics
def boot_med(x, nb=4000, seed=92):
    rng = np.random.default_rng(seed); n = len(x); return float(np.std([np.median(x[rng.integers(0, n, n)]) for _ in range(nb)], ddof=1))
def row(P, cfg, coll_floor, boot=False, propagate=False):
    x = offs(P, cfg); m = float(np.median(x))
    stat = boot_med(x) if boot else 1.2533 * float(np.std(x, ddof=1)) / math.sqrt(len(x))
    kw = (lambda u: dict(ups=u, halo_ups=u)) if propagate else (lambda u: dict(ups=u))
    ms = [float(np.median(offs(P, cfg.copy(**kw(u))))) for u in (1.0, 2.0, 4.0)]
    fU = 0.5 * (max(ms) - min(ms)); fC = 0.0
    if coll_floor and cfg.phi != 0.0:
        mc = [float(np.median(offs(P, cfg.copy(small_mcoll=v)))) for v in (1e8, 1e9, 1e10)]; fC = 0.5 * (max(mc) - min(mc))
    tot = math.sqrt(stat**2 + fU**2 + fC**2)
    return dict(off=m, stat=stat, fU=fU, fC=fC, tot=tot, z=m / tot, x=x)

# ---------------- statistic C
def gext_vec(P, foot, MMW=6.0e10, MM31=1.2e11):
    a0 = A0[foot]; v = []
    for s in P:
        c = [(s["dgc"], MMW), (s["dm31"], MM31)] if s["pop"] == "field" else [(s["dgc"], MMW)] if s["pop"] == "mw" else [(s["dm31"], MM31)]
        D, M = max(c, key=lambda t: t[1] / t[0] ** 2)
        y = G * M * MSUN / (D * KPC) ** 2 / a0; v.append(y * nu_rar(y))
    return np.array(v)
def design_slope(lg, ly, lM, lr):
    X = np.column_stack([np.ones(len(lg)), lg, lM, lr, lM**2, lr**2, lM * lr]); b, *_ = np.linalg.lstsq(X, ly, rcond=None); return float(b[1])
def slope_boot(lg, ly, lM, lr, nb=4000, seed=92):
    rng = np.random.default_rng(seed); n = len(lg); s = np.empty(nb)
    for b in range(nb):
        i = rng.integers(0, n, n); s[b] = design_slope(lg[i], ly[i], lM[i], lr[i])
    return float(np.std(s, ddof=1))
def statC(P, cfg, sig_pred_fn=None):
    """observed slope, bootstrap error, predicted slope under cfg (isolated law/rule), offset in sigma"""
    ge = gext_vec(P, cfg.foot); lg = np.log10(ge)
    Mb = np.array([masses(s, cfg)[1] for s in P]); lM = np.log10(Mb); lr = np.log10(np.array([s["Re_maj"] for s in P]))
    lo = np.log10([s["sig"] for s in P]); obs = design_slope(lg, lo, lM, lr); err = slope_boot(lg, lo, lM, lr)
    lp = np.log10([predict(s, cfg) for s in P]); pred = design_slope(lg, lp, lM, lr)
    return dict(obs=obs, err=err, pred=pred, z=(obs - pred) / err)

def switchoff(ratio, cfg, foot):
    """smallest M_b (log grid + brentq) at which f_ex reaches 0 for M_* = ratio*M_b; also checks the crossing is single."""
    a0 = A0[foot]
    h = lambda lMb: (edge_phantom(10 ** lMb, a0, cfg.kernel)[0] - (1 - FB) * mcoll(ratio * 10 ** lMb, cfg))
    grid = np.linspace(3.0, 11.0, 801); v = np.array([h(l) for l in grid]); sgn = v >= 0
    crossings = int(np.sum(sgn[1:] != sgn[:-1]))
    i = int(np.argmax(sgn)); root = brentq(h, grid[i - 1], grid[i], xtol=1e-12) if i > 0 else grid[0]
    return 10 ** root, crossings

# ================================================================== MAIN
def main():
    out("CFG92 main" + (" [MUTATE=1: every M_coll / 100]" if MUTATE else ""))
    out("spec sha256:", hashlib.sha256(open(os.path.join(HERE, "CFG92_SPEC_FROZEN.txt"), "rb").read()).hexdigest())
    ALL = load(); FIELD = [s for s in ALL if s["pop"] == "field"]
    check("C3 counts: 13 field dwarfs (2 with HI upper limits), 92 statistic-C dwarfs (45/34/13)",
          (len(FIELD), sum(s["has_hi_ul"] for s in FIELD), len(ALL), sum(s["pop"] == "mw" for s in ALL), sum(s["pop"] == "m31" for s in ALL)) == (13, 2, 92, 45, 34),
          str((len(FIELD), sum(s["has_hi_ul"] for s in FIELD), len(ALL))))
    mdiv = 100.0 if MUTATE else 1.0
    base = Cfg(mcoll_div=mdiv)
    # ---------- controls C1, C2
    s0 = dict(pop="x", name="t", host=None, MV=-9.0, Re_sph=300.0, Re_maj=300.0, sig=8.0, HI=0.0, HI_ul=0.0, has_hi_ul=False)
    r = 4 / 3 * 0.3 * KPC; Mb0 = Mst_of(-9.0)
    sN = predict(s0, Cfg(kernel="one", phi=0.0)); ref = math.sqrt(G * Mb0 * MSUN / (6 * r)) / 1e3
    check("C1a Newtonian limit: sigma = sqrt(G M_b/(6 r)) to 1e-12", abs(sN / ref - 1) < 1e-12, f"{sN:.6f} vs {ref:.6f}")
    for kn in ("RAR", "P2"):
        st = dict(s0); st["MV"] = 2.5; Mt = Mst_of(2.5); y = G * Mt * MSUN / 2 / r**2 / A0["canonical"]
        sg = predict(st, Cfg(kernel=kn, phi=0.0)); sdm = (G * Mt * MSUN / 2 * A0["canonical"]) ** 0.25 / math.sqrt(3) / 1e3
        check(f"C1b deep-MOND ({kn}): sigma^4 = G M_half a0/9 within 2 sqrt(y) (y={y:.1e})", abs(sg / sdm - 1) < 2 * math.sqrt(y), f"ratio-1={sg/sdm-1:.2e}")
    bad = []; d0 = 0.0; d1 = 0.0; a0 = A0["canonical"]
    for s in ALL:
        sl = predict(s, Cfg(phi=0.0)); sr, d = predict(s, Cfg(phi=1.0), True)
        rr = 4 / 3 * s["Re_sph"] * 1e-3 * KPC; Mb = d["Mb"]; gN = G * Mb * MSUN / 2 / rr**2; g = gN / (1 - math.exp(-math.sqrt(gN / a0)))
        Mc = d["Mc"]; c = conc_DM(Mc); R = r200_kpc(Mc) * KPC; x = rr / R
        Mn = Mc * (math.log(1 + c * x) - c * x / (1 + c * x)) / (math.log(1 + c) - c / (1 + c))
        fex = max(0, 1 - d["Mph"] / ((1 - FB) * Mc)); sr2 = math.sqrt((g + G * fex * (1 - FB) * Mn * MSUN / rr**2) * rr / 3) / 1e3
        d1 = max(d1, abs(sr / sr2 - 1)); d0 = max(d0, abs(sl / (math.sqrt(g * rr / 3) / 1e3) - 1))
        if not (0 <= d["fex"] <= 1): bad.append(s["name"])
    check("C2a phi=0 equals the bare law (independent formula) to 1e-12", d0 < 1e-12, f"max {d0:.1e}")
    check("C2b phi=1 equals S (independent direct formula) to 1e-12", d1 < 1e-12, f"max {d1:.1e}")
    check("C2c f_ex in [0,1] for all 92", not bad)
    Mh = 3.7e10
    check("C2d NFW: M(<R200)=M_h to 1e-12 and monotone", abs(nfw_enclosed(Mh, r200_kpc(Mh), conc_DM) / Mh - 1) < 1e-12 and all(nfw_enclosed(Mh, x1, conc_DM) < nfw_enclosed(Mh, x1 * 1.01, conc_DM) for x1 in np.logspace(-3, 2, 30)))
    dev = []
    for Mb in (1e2, 1e3, 1e4, 1e5):
        Mph, rta = edge_phantom(Mb, a0, "P2"); K = math.sqrt(Mb * MSUN * a0 / G); rcf = math.sqrt(3 * K / (4 * math.pi * DELTA_TA * RHO_M))
        dev.append(abs(Mph / ((X_E * rcf * K) / MSUN - Mb) - 1))
    check("C2e edge phantom root-find = deep-MOND closed form (P2, M_b<=1e5) to <1e-3", max(dev) < 1e-3, f"max {max(dev):.1e}")
    # ---------- P1 switch-off masses
    out("\n=== P1 switch-off masses (f_ex = 0 above; Moster/DM independent of concentration; RAR kernel) ===")
    SW = {}
    for foot in ("canonical", "alt"):
        for ratio in (0.5, 1.0):
            M, nc = switchoff(ratio, base, foot); SW[(foot, ratio)] = M
            out(f"  {foot:9s} M_* = {ratio:.1f} M_b: M_b,switch = {M:.3e}  (sign changes on grid: {nc})")
            if ratio == 0.5 and foot == "canonical": nc0 = nc
    check("C2f f_ex(M_b) crosses zero once (monotone) on the grid", nc0 == 1, f"crossings {nc0}")
    out("  CFG58: 2.3e7 (canonical) / 1.5e7 (alt) for M_*=M_b/2; 5.5e7 canonical for M_*=M_b")
    # ---------- field dwarfs
    RES = {}
    out("\n=== P2 the 13 LV field dwarfs: offsets log10(sigma_obs/sigma_pred), median; E1 recipe (analytic SE + fixed-halo Upsilon floor + collapse floor) ===")
    for foot in ("canonical", "alt"):
        cL = base.copy(phi=0.0, foot=foot); cS = base.copy(phi=1.0, foot=foot)
        L = row(FIELD, cL, False); S = row(FIELD, cS, True)
        RES[foot] = dict(L=L, S=S)
        out(f"  {foot:9s} L {L['off']:+.4f} err {L['tot']:.4f} ({L['z']:+.2f}s) [stat {L['stat']:.4f} U {L['fU']:.4f}] | S {S['off']:+.4f} err {S['tot']:.4f} ({S['z']:+.2f}s) [stat {S['stat']:.4f} U {S['fU']:.4f} C {S['fC']:.4f}]"
            f" | change {S['off']-L['off']:+.4f} dex | S in L's error {S['off']/L['tot']:+.2f}s")
    out("  CFG58: L -0.044 (-0.60s, err 0.073) | S -0.105 (-3.47s, err 0.030) | change 0.061 | S in L's error -1.4 (canonical), alt: L -0.85s, S -2.70s, -1.3s")
    # per-dwarf table
    out("\n  per-dwarf (canonical): name, M_b, f_ex, L off, S off, S-L")
    cLc = base.copy(phi=0.0); cSc = base.copy(phi=1.0); PD = []
    for s in FIELD:
        (sl, dl) = predict(s, cLc, True); (ss, ds) = predict(s, cSc, True)
        xl = math.log10(s["sig"] / sl); xs = math.log10(s["sig"] / ss); PD.append((s["name"], ds["Mb"], ds["fex"], xl, xs))
    for t in sorted(PD, key=lambda t: t[1]): out(f"    {t[0]:17s} M_b {t[1]:.2e}  f_ex {t[2]:.3f}  L {t[3]:+.3f}  S {t[4]:+.3f}  S-L {t[4]-t[3]:+.3f}")
    mL = np.median([t[3] for t in PD]); mS = np.median([t[4] for t in PD])
    # which dominate: leave-one-out on the median of S and L
    out("  leave-one-out (canonical): dropped dwarf -> median L, median S, change")
    LOO = []
    for i, t in enumerate(PD):
        rest = [u for j, u in enumerate(PD) if j != i]; LOO.append((t[0], np.median([u[3] for u in rest]), np.median([u[4] for u in rest])))
        out(f"    drop {t[0]:17s} L {LOO[-1][1]:+.4f}  S {LOO[-1][2]:+.4f}  change {LOO[-1][2]-LOO[-1][1]:+.4f}")
    n0 = sum(t[2] == 0 for t in PD); out(f"  dwarfs with f_ex = 0 (S == L): {n0} of 13; f_ex>0: {13-n0}; order stats: S sorted {[round(v,3) for v in sorted(t[4] for t in PD)]}")
    # ---------- error-recipe variants
    out("\n=== error-recipe variants for the field dwarfs (canonical | alt): S offset/err -> z; L offset/err -> z; S in L's error ===")
    for nm, kw in (("E1 analytic + fixed-halo Ups", dict(boot=False, propagate=False)), ("E2 bootstrap + fixed-halo", dict(boot=True, propagate=False)),
                   ("E3 analytic + propagated Ups", dict(boot=False, propagate=True)), ("E4 bootstrap + propagated", dict(boot=True, propagate=True))):
        line = []
        for foot in ("canonical", "alt"):
            L = row(FIELD, base.copy(phi=0.0, foot=foot), False, **kw); S = row(FIELD, base.copy(phi=1.0, foot=foot), True, **kw)
            line.append(f"L {L['off']:+.3f}/{L['tot']:.3f}={L['z']:+.2f}s  S {S['off']:+.3f}/{S['tot']:.3f}={S['z']:+.2f}s  S|L-err {S['off']/L['tot']:+.2f}s")
        out(f"  {nm:30s} " + " || ".join(line))
    # ---------- concentration / kernel / clamp / estimator / other sensitivities (field dwarfs, canonical | alt)
    out("\n=== field-dwarf sensitivities (canonical | alt; S offset and z in S's own E1 error; L unchanged unless the knob touches it) ===")
    def srow(nm, **kw):
        cells = []
        for foot in ("canonical", "alt"):
            L = row(FIELD, base.copy(phi=0.0, foot=foot, **{k: v for k, v in kw.items() if k not in ("conc", "clamp", "unclamped")}), False)
            S = row(FIELD, base.copy(phi=1.0, foot=foot, **kw), True)
            cells.append(f"L {L['off']:+.3f} S {S['off']:+.3f} ({S['z']:+.2f}s, err {S['tot']:.3f}) chg {S['off']-L['off']:+.3f}")
        out(f"  {nm:34s} " + " || ".join(cells)); return cells
    for c in CONC: srow("conc " + c, conc=c)
    for k in ("P2", "simple"): srow("kernel " + k, kernel=k)
    for cl in (1e8, 3e8, 1e9, 3e9, 1e10): srow(f"Moster clamp {cl:.0e}", clamp=cl)
    srow("Moster unclamped", unclamped=True)
    srow("R_e = rhalf_physical (major axis)", re_key="Re_maj")
    srow("estimator K (k_contrarian: 2/9 nu G M_b/r, r=R_e)", est="K")
    srow("estimator K, r = rhalf_physical", est="K", re_key="Re_maj")
    srow("HI upper limits at the limit", ul_at_limit=True)
    srow("Upsilon_V = 1 (halo propagated)", ups=1.0, halo_ups=1.0); srow("Upsilon_V = 4 (halo propagated)", ups=4.0, halo_ups=4.0)
    FD_noAB = [s for s in FIELD if s["name"] != "Antlia B"]
    for foot in ("canonical", "alt"):
        L = row(FD_noAB, base.copy(phi=0.0, foot=foot), False); S = row(FD_noAB, base.copy(phi=1.0, foot=foot), True)
        out(f"  drop Antlia B ({foot}, n=12): L {L['off']:+.3f} ({L['z']:+.2f}s)  S {S['off']:+.3f} ({S['z']:+.2f}s, err {S['tot']:.3f})")
    # sub-threshold split
    Msw = SW[("canonical", 0.5)]; lo = [s for s in FIELD if masses(s, base)[1] < Msw]; hi = [s for s in FIELD if masses(s, base)[1] >= Msw]
    out(f"  split at my switch-off mass {Msw:.2e}: below n={len(lo)}, above n={len(hi)}")
    for nm, P in (("below", lo), ("above", hi)):
        if len(P) >= 2:
            L = np.median(offs(P, base.copy(phi=0.0))); S = np.median(offs(P, base.copy(phi=1.0))); out(f"    {nm}: median L {L:+.3f} S {S:+.3f}")
    # ---------- statistic C
    out("\n=== P3 statistic C (92 dwarfs): observed slope, bootstrap error, isolated-law (L) and rule (S) predicted slope; offset sigma = (obs-pred)/err ===")
    SC = {}
    for foot in ("canonical", "alt"):
        cL = base.copy(phi=0.0, foot=foot, est="K", re_key="Re_maj"); cS = base.copy(phi=1.0, foot=foot, est="K", re_key="Re_maj")
        L = statC(ALL, cL); S = statC(ALL, cS); SC[foot] = (L, S)
        out(f"  {foot:9s} observed {L['obs']:+.4f} +/- {L['err']:.4f} | L pred {L['pred']:+.4f} -> {L['z']:+.2f}s | S pred {S['pred']:+.4f} -> {S['z']:+.2f}s | delta slope (S-L) {S['pred']-L['pred']:+.4f}")
        fexs = np.array([predict(s, cS, True)[1]["fex"] for s in ALL]); Mbs = np.array([masses(s, cS)[1] for s in ALL])
        out(f"            f_ex>0 in {np.mean(fexs>0)*100:.1f}% of the 92; M_b < my switch-off ({SW[(foot,0.5)]:.2e}) in {np.mean(Mbs<SW[(foot,0.5)])*100:.1f}%; M_b < 2.3e7: {np.mean(Mbs<2.3e7)*100:.1f}%")
    out("  CFG58: L +1.41|+1.42 sigma (pred +0.0143 quoted for L by k_contrarian), S +1.02|+1.13, delta slope 0.013, 86% below the switch-off; observed +0.0800+/-0.0467 | +0.0803+/-0.0469")
    out("  statistic-C sensitivities (canonical | alt): pred L, pred S, z L, z S, delta")
    def scrow(nm, **kw):
        cells = []
        for foot in ("canonical", "alt"):
            kk = dict(est="K", re_key="Re_maj"); kk.update(kw)
            L = statC(ALL, base.copy(phi=0.0, foot=foot, **{k: v for k, v in kk.items() if k not in ("conc", "clamp", "unclamped")})); S = statC(ALL, base.copy(phi=1.0, foot=foot, **kk))
            cells.append(f"pL {L['pred']:+.4f} pS {S['pred']:+.4f} zL {L['z']:+.2f} zS {S['z']:+.2f} d {S['pred']-L['pred']:+.4f}")
        out(f"    {nm:36s} " + " || ".join(cells))
    scrow("baseline (estimator K)")
    scrow("FG001 estimator (R_e = rhalf_physical)", est="FG"); scrow("FG001 estimator, R_e = rhalf_sph", est="FG", re_key="Re_sph")
    for c in ("Duffy200c_full", "Duffy200c_relaxed", "Duffy200m_full_inconsistent"): scrow("conc " + c, conc=c)
    for k in ("P2", "simple"): scrow("kernel " + k, kernel=k)
    for cl in (1e8, 3e8, 1e10): scrow(f"Moster clamp {cl:.0e}", clamp=cl)
    scrow("Moster unclamped", unclamped=True)
    # drop groups
    for nm, P in (("drop 45 MW-catalogue", [s for s in ALL if s["pop"] != "mw"]), ("MW+M31 only (79)", [s for s in ALL if s["pop"] != "field"]),
                  ("brighter than M_V=-6 (62)", [s for s in ALL if s["MV"] < -6.0])):
        L = statC(P, base.copy(phi=0.0, est="K", re_key="Re_maj")); S = statC(P, base.copy(phi=1.0, est="K", re_key="Re_maj"))
        out(f"    subsample {nm:26s} n={len(P):2d}: obs {L['obs']:+.4f}+/-{L['err']:.4f} pL {L['pred']:+.4f} pS {S['pred']:+.4f} zL {L['z']:+.2f} zS {S['z']:+.2f}")
    # ---------- C4 controls on stat C
    L1 = statC(ALL, base.copy(phi=0.0, est="K", re_key="Re_maj", kernel="one"))
    check("C4a nu==1, phi=0: predicted statistic-C slope is exactly 0", abs(L1["pred"]) < 1e-12, f"{L1['pred']:.2e}")
    a_saved = A0["canonical"]; A0["canonical"] = a_saved / 100
    Lsm = statC(ALL, base.copy(phi=0.0, est="K", re_key="Re_maj")); A0["canonical"] = a_saved
    out(f"  C4b info: a0/100 -> predicted L slope {Lsm['pred']:+.4f} (vs {SC['canonical'][0]['pred']:+.4f} canonical): {'collapses toward 0' if abs(Lsm['pred'])<abs(SC['canonical'][0]['pred']) else 'does NOT collapse'}")
    tgt = dict(canonical=(0.0800, 0.0467), alt=(0.0803, 0.0469)); ok = True
    for foot in ("canonical", "alt"):
        o, e = SC[foot][0]["obs"], SC[foot][0]["err"]; ok &= abs(o - tgt[foot][0]) < 5e-4 and abs(e - tgt[foot][1]) < 1.5e-3
    out(f"  C4c info: observed-side reproduction (obs to 5e-4, err to 1.5e-3) of k_contrarian's printed numbers: {'reproduced' if ok else 'differs'}  (own: {SC['canonical'][0]['obs']:+.4f}+/-{SC['canonical'][0]['err']:.4f} | {SC['alt'][0]['obs']:+.4f}+/-{SC['alt'][0]['err']:.4f})")
    # ---------- P4 structure
    mx = 0.0; n0 = 0
    for s in ALL + FIELD:
        for foot in ("canonical", "alt"):
            sr, d = predict(s, base.copy(foot=foot, phi=1.0), True)
            if d["fex"] == 0.0: n0 += 1; mx = max(mx, abs(math.log10(sr / predict(s, base.copy(foot=foot, phi=0.0)))))
    check("P4 S == L to 1e-12 in log sigma wherever f_ex = 0", mx < 1e-12, f"{n0} cases, max {mx:.1e}")
    # ---------- headline flag
    chg = max(RES[f]["S"]["off"] - RES[f]["L"]["off"] for f in RES) if False else max(abs(RES[f]["S"]["off"] - RES[f]["L"]["off"]) for f in RES)
    h1 = chg > 0.05
    out(f"\nH1 (S changes the field-dwarf median by more than 0.05 dex): {'pass' if h1 else 'FAIL'} (max change {chg:.4f} dex)")
    if MUTATE:
        c5 = chg < 0.01 and SW[("canonical", 0.5)] < 2.3e7
        check("C5 MUTATE: field-dwarf S-L change < 0.01 dex and the switch-off mass drops below the un-mutated value", c5, f"change {chg:.4f}, switch-off {SW[('canonical',0.5)]:.2e}")
    out("\nFAILED CONTROLS:", FAILS if FAILS else "none")
    tag = "_MUTATE" if MUTATE else ""
    json.dump(dict(SW={f"{k[0]}|{k[1]}": v for k, v in SW.items()}, field={f: {k: {kk: (vv if kk != 'x' else list(map(float, vv))) for kk, vv in v.items()} for k, v in d.items()} for f, d in RES.items()},
                   statC={f: dict(obs=SC[f][0]["obs"], err=SC[f][0]["err"], pL=SC[f][0]["pred"], pS=SC[f][1]["pred"], zL=SC[f][0]["z"], zS=SC[f][1]["z"]) for f in SC}),
              open(os.path.join(HERE, f"cfg92_results{tag}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg92{tag}.out"), "w").write("\n".join(LOG) + "\n")
    if MUTATE: sys.exit(1 if not h1 else 0)
    sys.exit(1 if FAILS else 0)

if __name__ == "__main__":
    main()
