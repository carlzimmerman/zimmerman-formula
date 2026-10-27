#!/usr/bin/env python3
"""CS1_core_surface_density_atlas: each system's cold dark energy core surface density Sigma0 = rho0 r0, measured from its own
data with one method (route E: cold = observed - baryons, Burkert primary, isothermal variant), then the law the data trace.

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (6f303e256b, committed alone before this script).
EM1's SPARC machinery (up to its backgrounds block) and X30's cluster machinery (up to its STEP 0) run read-only in separate
namespaces, as in X38. kappa = 1/2 FITTED; footings never pooled; not theory closed.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs1_atlas.py                -> cs1_atlas.out, _results.json, _atlas.csv, .png
    CS1_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 cs1_atlas.py   -> sigma shuffled across systems (exit 1 = control bites)
"""
import os, sys, io, csv, warnings, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
os.environ.pop("X30_MUTATE", None)
import numpy as np
from scipy.optimize import brentq, minimize_scalar, minimize
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.stats import norm, spearmanr
from astropy.io import fits
warnings.filterwarnings("ignore", category=RuntimeWarning)

T0 = time.time()
MUTATE = os.environ.get("CS1_MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
DATA = os.path.join(REPO, "real_research", "data")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
FEET = ("canonical", "alt")
SREF = 70.50                                                    # km/s, SC1 pivot
LSG = np.round(np.arange(-1.0, 5.0001, 0.01), 2); SG = 10 ** LSG  # log Sigma0 grid [Msun/pc^2]
checks = []
def check(k, ok, msg):
    checks.append((k, bool(ok))); P(f"{k} {'PASS' if ok else 'FAIL'}  {msg}")

# ------------------------------------------------------------------ EM1 (read-only, up to backgrounds)
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; argv0 = sys.argv; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- backgrounds")], EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, pooled, UPS, LAW, NEWT, A0 = (NE[k] for k in ("GALS", "fit_one", "pooled", "UPS", "LAW", "NEWT", "A0"))
GE, MSUN, KPC = NE["G"], NE["MSUN"], NE["KPC_S"]; PC = KPC / 1e3; SPC = MSUN / PC ** 2
P(f"CS1_core_surface_density_atlas  {'MUTATE (sigma shuffled across systems)' if MUTATE else 'normal run'}  (frozen 6f303e256b)")
P("kappa = 1/2 FITTED; footings never pooled; route E (cold dark energy = observed - baryons, Newtonian); not theory closed")
SIGA0 = {f: A0[f] / (2 * math.pi * GE) / SPC for f in FEET}
P(f"Sigma_a0 = a0/(2 pi G): canonical {SIGA0['canonical']:.1f}, alt {SIGA0['alt']:.1f} Msun/pc^2")

# ------------------------------------------------------------------ profiles
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
def mfac(prof, x): return math.pi * B(x) if prof == "burkert" else 4 * math.pi * (np.asarray(x, float) - np.arctan(x))

# K1: closed forms vs quadrature
r0t, Rt, St = 3.0, 10.0, 1.0
qB = quad(lambda r: 4 * math.pi * r * r * (St / r0t) / ((1 + r / r0t) * (1 + (r / r0t) ** 2)), 0, Rt, epsrel=1e-12, limit=400)[0]
qI = quad(lambda r: 4 * math.pi * r * r * (St / r0t) / (1 + (r / r0t) ** 2), 0, Rt, epsrel=1e-12, limit=400)[0]
eB = float(St * r0t ** 2 * mfac("burkert", Rt / r0t)) / qB - 1; eI = float(St * r0t ** 2 * mfac("iso", Rt / r0t)) / qI - 1
check("K1", abs(eB) < 1e-6 and abs(eI) < 1e-6, f"Burkert {eB:+.1e}, isothermal {eI:+.1e} (closed form vs quadrature)")

def profile_fit(y, sy, mask, Kfun, lr0, npar):
    """Model y = Sigma0 * K(r0), linear in Sigma0. y, mask (n, nU); sy (n,); Kfun(r0) -> (n,). Returns the dict of the fit."""
    K = np.array([Kfun(r) for r in 10 ** lr0])                          # (nr, n)
    w = np.where(mask, 1.0 / sy[:, None] ** 2, 0.0)                     # (n, nU)
    F = K ** 2 @ w; b = K @ (w * y); c = (w * y * y).sum(0)             # (nr, nU), (nr, nU), (nU,)
    F = np.maximum(F, 1e-300); Sh = b / F; cm = c[None, :] - b * b / F
    prof = np.full(len(SG), np.inf); arg = np.zeros((len(SG), 2), int)
    for j0 in range(0, len(SG), 100):
        S_ = SG[j0:j0 + 100]
        chi = cm[..., None] + F[..., None] * (S_[None, None, :] - Sh[..., None]) ** 2
        flat = chi.reshape(-1, len(S_)); ia = flat.argmin(0)
        prof[j0:j0 + 100] = flat[ia, np.arange(len(S_))]; arg[j0:j0 + 100] = np.array(np.unravel_index(ia, chi.shape[:2])).T
    jb = int(prof.argmin()); ir, iu = arg[jb]; npts = int(mask[:, iu].sum()); dof = max(npts - npar, 1)
    scale = max(1.0, prof[jb] / dof); d = (prof - prof[jb]) / scale; ok = np.where(d <= 1.0)[0]
    lo, hi = int(ok.min()), int(ok.max())
    kind = ("unconstrained" if lo == 0 and hi == len(SG) - 1 else "lower" if hi == len(SG) - 1 else "upper" if lo == 0 else "two-sided")
    return dict(lS=float(LSG[jb]), lS_lo=float(LSG[lo]), lS_hi=float(LSG[hi]), kind=kind, e=float(0.5 * (LSG[hi] - LSG[lo])),
                lr0=float(lr0[ir]), iu=int(iu), chi2=float(prof[jb]), dof=dof, npts=npts, r0_edge=bool(ir in (0, len(lr0) - 1)))

# ------------------------------------------------------------------ SPARC
LR0_S = np.round(np.arange(-3.0, 3.5001, 0.025), 3)                  # log r0 [kpc]
d_ = os.path.join(DATA, "sparc_data"); mine = {}
for f in sorted(os.listdir(d_)):
    if f.endswith("_rotmod.dat"):
        try: a = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception: continue
        if a.ndim == 2 and a.shape[1] >= 6: mine[f.replace("_rotmod.dat", "")] = a
dmax = 0.0
for q in GALS:
    a = mine[q["name"]]; R = a[:, 0] * KPC
    VB2 = np.sign(a[:, 3])[:, None] * a[:, 3][:, None] ** 2 + UPS[None, :] * a[:, 4][:, None] ** 2 + 1.4 * UPS[None, :] * a[:, 5][:, None] ** 2
    GB = VB2 * 1e6 / R[:, None]; GO = (a[:, 1] * 1e3) ** 2 / R
    dmax = max(dmax, float(np.nanmax(np.abs(GB / q["GB"] - 1))), float(np.nanmax(np.abs(GO / q["GO"] - 1))))
    q["VB2"] = VB2 * 1e6
rowsN = [fit_one(q, np.log10(np.maximum(q["VB2"] / q["Rm"][:, None], 1e-300))) for q in GALS]
myN = pooled([r[0] for r in rowsN], [r[1] for r in rowsN], [r[2] for r in rowsN])
k0a = (dmax < 1e-12 and abs(LAW["canonical"]["rms"] - 0.0541) < 1e-4 and abs(LAW["alt"]["rms"] - 0.0537) < 1e-4
       and abs(myN["rms"] - NEWT["rms"]) < 1e-4)
check("K0a", k0a, f"loader vs EM1 GB/GO max rel {dmax:.1e}; EM1 law rms {LAW['canonical']['rms']:.4f} / {LAW['alt']['rms']:.4f}; "
      f"Newtonian row {myN['rms']:.4f} vs EM1 {NEWT['rms']:.4f}")
def sparc_fit(q, prof, ufix=None):
    R, V, eV = q["Rm"], q["Vobs"] * 1e3, np.clip(q["eV"], 1, None) * 1e3
    y = (V * V)[:, None] - q["VB2"]; mask = q["OK"]
    if ufix is not None:
        iu = int(np.argmin(np.abs(UPS - ufix))); y, mask = y[:, iu:iu + 1], mask[:, iu:iu + 1]
    Kf = lambda r0: GE * SPC * (r0 * KPC) ** 2 * mfac(prof, R / (r0 * KPC)) / R
    out = profile_fit(y, 2 * V * eV, mask, Kf, LR0_S, 3 if ufix is None else 2)
    out["U"] = float(UPS[out["iu"]]) if ufix is None else ufix
    return out
# K2 planted recovery (values on the grids)
q0 = GALS[0]; R = q0["Rm"]; iu5 = int(np.argmin(np.abs(UPS - 0.5))); lSp, lrp = 2.48, 0.475
Vp2 = q0["VB2"][:, iu5] + 10 ** lSp * GE * SPC * (10 ** lrp * KPC) ** 2 * mfac("burkert", R / (10 ** lrp * KPC)) / R
Vp = np.sqrt(np.maximum(Vp2, 1.0))
pf = profile_fit((Vp * Vp - q0["VB2"][:, iu5])[:, None], 2 * Vp * 5e3, np.ones((len(R), 1), bool),
                 lambda r0: GE * SPC * (r0 * KPC) ** 2 * mfac("burkert", R / (r0 * KPC)) / R, LR0_S, 2)
cB = minimize_scalar(lambda lx: float(10 ** (2 * lx) / B(10 ** lx)), bounds=(-2, 2), method="bounded", options={"xatol": 1e-12})
xg = 10 ** np.linspace(-2, 2, 400001); brute = float(np.min(xg ** 2 / B(xg)))
cI = minimize_scalar(lambda lx: float(10 ** (2 * lx) / (4 * (10 ** lx - math.atan(10 ** lx)))), bounds=(-2, 2), method="bounded", options={"xatol": 1e-12})
CMIN = {"burkert": float(cB.fun / math.pi), "iso": float(cI.fun / math.pi)}   # Sigma_min = CMIN * M / r^2
check("K2", abs(pf["lS"] - lSp) <= 0.01 and abs(math.log10(cB.fun / brute)) < 1e-4,
      f"planted log Sigma {lSp} -> {pf['lS']:.2f}, log r0 {lrp} -> {pf['lr0']:.3f}; dwarf min x^2/B(x) {cB.fun:.6f} at x {10 ** cB.x:.3f} vs brute {brute:.6f}")
P(f"  Burkert Sigma_min = {CMIN['burkert']:.5f} M/r^2 (x* = r/r0 = {10 ** cB.x:.3f}); isothermal {CMIN['iso']:.5f} (x* {10 ** cI.x:.3f})")

SP = []
for q in GALS:
    rb = sparc_fit(q, "burkert"); ri = sparc_fit(q, "iso"); r5 = sparc_fit(q, "burkert", ufix=0.50)
    SP.append(dict(cls="SPARC", name=q["name"], sig=float(q["Vobs"][-1] / math.sqrt(2)), lMb=float(q["lMb"]), B=rb, iso=ri, U05=r5))
sref_chk = float(np.median([s["sig"] for s in SP]))
P(f"SPARC: {len(SP)} galaxies fitted; median V_last/sqrt2 {sref_chk:.2f} km/s (SC1 {SREF}); kinds "
  + str({k: sum(s['B']['kind'] == k for s in SP) for k in ('two-sided', 'lower', 'upper', 'unconstrained')})
  + f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ Milky Way (GD1 inputs)
Gk = 4.30091e-6
SEAL = json.load(open(os.path.join(REB, "S3_v3_mw_seals", "SEALED_V3_MW_DR4.json")))
def nfw(M200, c, h0n=67.7):
    rc = 3 * (h0n / 1e3) ** 2 / (8 * math.pi * Gk); r200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); rs = r200 / c
    m = math.log(1 + c) - c / (1 + c); rhos = M200 / (4 * math.pi * rs ** 3 * m)
    return lambda r: Gk * 4 * math.pi * rhos * rs ** 3 * (np.log1p(r / rs) - (r / rs) / (1 + r / rs)) / r ** 2
ou = np.loadtxt(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"), comments="#", skiprows=14)
OR, OV = ou[:, 0], ou[:, 1]; OE = np.hypot(0.5 * (ou[:, 2] + ou[:, 3]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
MW = {}
for sk in sorted(SEAL["NFW_Ou24"]):
    n = SEAL["NFW_Ou24"][sk]; gh = nfw(n["M200"], n["c"])
    Rv = np.array(sorted(float(k[1:]) for k in n["P2_Vc"])); Vt = np.array([n["P2_Vc"][f"R{r:.0f}"] for r in Rv])
    R5 = np.array([30.0, 40, 50, 60]); V5 = np.array([n["P5_Vc"][f"R{r:.0f}"] for r in R5])
    RR = np.concatenate([Rv, R5]); VB2 = np.concatenate([Vt ** 2 - Rv * gh(Rv), V5 ** 2 - R5 * gh(R5)]); o = np.argsort(RR)
    vb2 = np.interp(OR, RR[o], VB2[o]); Mb = float(VB2[RR == 60.0][0] * 60.0 / Gk)
    res = {}
    for prof in ("burkert", "iso"):
        Kf = lambda r0, prof=prof: Gk * 1e6 * r0 ** 2 * mfac(prof, OR / r0) / OR          # Sigma in Msun/pc^2 -> (km/s)^2
        res[prof] = profile_fit((OV * OV - vb2)[:, None], 2 * OV * OE, np.ones((len(OR), 1), bool), Kf, LR0_S, 2)
    MW[sk] = dict(res, lMb=math.log10(Mb))
mw = dict(cls="MW", name="Milky Way", sig=float(OV[-1] / math.sqrt(2)), lMb=MW["1.000000"]["lMb"], B=MW["1.000000"]["burkert"],
          iso=MW["1.000000"]["iso"], band=[MW[s]["burkert"]["lS"] for s in sorted(MW)])
P(f"MW: Burkert log Sigma0 {mw['B']['lS']:.2f} [{mw['B']['lS_lo']:.2f}, {mw['B']['lS_hi']:.2f}] ({mw['B']['kind']}), log r0 {mw['B']['lr0']:.2f} kpc, "
  f"chi2/dof {mw['B']['chi2']:.1f}/{mw['B']['dof']}; s band {[round(v, 2) for v in mw['band']]}; sigma {mw['sig']:.1f}")

# ------------------------------------------------------------------ X-COP (matched-clumping lane's six radii)
Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16
def loginterp(r, m, t):
    if t < r[0] or t > r[-1]: return np.nan
    return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
XC = []; k0b_rows = []
ETT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
for folder in sorted(os.listdir(os.path.join(DATA, "xcop"))):
    p_ = os.path.join(DATA, "xcop", folder); name = folder
    if not os.path.isdir(p_) or not os.path.exists(os.path.join(p_, f"{name}_hydro_mass.fits")): continue
    hasS = os.path.exists(os.path.join(p_, f"{name}_mstar.fits"))
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    st = None
    if hasS:
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    m500 = loginterp(hm["RADIUS"], hm["M_FORW"], r500); rows = []
    for x in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0):
        r = x * r500
        mh, emh = loginterp(hm["RADIUS"], hm["M_FORW"], r), np.interp(r, hm["RADIUS"], hm["EM_FORW"])
        mg = loginterp(gas["RADIUS"] * rg500, gas["MGAS"], r)
        emg = 0.5 * (loginterp(gas["RADIUS"] * rg500, gas["MGAS_HI"], r) - loginterp(gas["RADIUS"] * rg500, gas["MGAS_LO"], r))
        if hasS:
            ms = loginterp(st["RADIUS"], st["MSTAR"], r); ems = 0.5 * (loginterp(st["RADIUS"], st["MSTAR_HI"], r) - loginterp(st["RADIUS"], st["MSTAR_LO"], r))
        else:
            ms, ems = 0.0, 0.0
        if not np.all(np.isfinite([mh, mg, ms])): continue
        rows.append((r, mh, emh, mg, float(np.nan_to_num(emg)), ms, float(np.nan_to_num(ems))))
        if hasS: k0b_rows.append((name, x, Gm * mh * MSm / (r * 1000 * PCm) ** 2, m500))
    a = np.array(rows); r_, yc = a[:, 0], a[:, 1] - a[:, 3] - a[:, 5]; sy = np.sqrt(a[:, 2] ** 2 + a[:, 4] ** 2 + a[:, 6] ** 2)
    res = {}
    for prof in ("burkert", "iso"):
        Kf = lambda r0, prof=prof: (r0 * 1e3) ** 2 * mfac(prof, r_ / r0)                   # r in kpc; Sigma Msun/pc^2 -> Msun
        res[prof] = profile_fit(yc[:, None], sy, np.ones((len(r_), 1), bool), Kf, np.round(np.arange(-1.0, 5.5001, 0.025), 3), 2)
    vc = math.sqrt(Gm * m500 * MSm / (r500 * 1000 * PCm)) / 1e3
    XC.append(dict(cls="XCOP", name=name, primary=hasS, sig=vc / math.sqrt(2), lMb=math.log10(a[-1, 3] + a[-1, 5]), B=res["burkert"],
                   iso=res["iso"], lM200=math.log10(ETT[name]["M200"] * 1e14) if name in ETT else float("nan"), npts=len(r_)))
tg = [r for r in csv.DictReader(open(os.path.join(REPO, "reviews", "matched_clumping_2026_10_24", "run", "targets.csv"))) if r["kind"] == "cluster"]
dk = 0.0
for nm_, x, go, m5 in k0b_rows:
    t = [r for r in tg if r["name"] == nm_ and abs(float(r["xradius"]) - x) < 1e-9]
    dk = max(dk, abs(go / float(t[0]["gobs"]) - 1), abs(m5 / float(t[0]["mhse500"]) - 1)) if t else 1.0
check("K0b", len(k0b_rows) == len(tg) and dk < 1e-6, f"X-COP {len(k0b_rows)} rows vs matched-clumping {len(tg)}; max rel diff {dk:.1e}")
for c in XC:
    P(f"  X-COP {c['name']:8s} {'primary' if c['primary'] else 'M*=0 variant'}: log Sigma0 {c['B']['lS']:.2f} [{c['B']['lS_lo']:.2f}, {c['B']['lS_hi']:.2f}] {c['B']['kind']}, "
      f"log r0 {c['B']['lr0']:.2f} kpc, chi2/dof {c['B']['chi2']:.1f}/{c['B']['dof']}; iso {c['iso']['lS']:.2f} ({c['iso']['kind']}); sigma {c['sig']:.0f}")

# ------------------------------------------------------------------ dwarfs (X1) and groups (P4 T3): Burkert lower bounds
X1R = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
DW = {}
for foot in FEET:
    out = []
    for r in [r for r in X1R if r["footing"] == foot]:
        r12 = 4 / 3 * float(r["rh_pc"]) * PC; Ms = 10 ** float(r["logMstar"]); gN = GE * (Ms * MSUN / 2) / r12 ** 2
        D, sd = float(r["Delta[Newton]"]), float(r["sdMC[Newton]"]); gobs = gN * 10 ** D; ratio = 10 ** D - 1
        sig = math.sqrt(gobs * r12 / 3) / 1e3
        if D <= 0 or ratio < 0.1:
            out.append(dict(cls="dwarf", name=r["name"], sub=r["cls"], detected=False, sig=sig)); continue
        Mc = (gobs - gN) * r12 ** 2 / GE / MSUN; r12pc = r12 / PC; sdh = sd * 10 ** D / ratio
        xs = 10 ** np.linspace(math.log10(1 / 3), math.log10(3), 201)
        out.append(dict(cls="dwarf", name=r["name"], sub=r["cls"], detected=True, sig=sig, lMb=math.log10(Ms),
                        lSmin=math.log10(CMIN["burkert"] * Mc / r12pc ** 2), lSmin_iso=math.log10(CMIN["iso"] * Mc / r12pc ** 2), e=sdh,
                        band=[float(np.log10(Mc * np.min(xs ** 2 / (math.pi * B(xs))) / r12pc ** 2)), float(np.log10(Mc * np.max(xs ** 2 / (math.pi * B(xs))) / r12pc ** 2))],
                        r0_at_min_pc=r12pc / 10 ** cB.x))
    DW[foot] = out
same = all(abs(a.get("lSmin", 0) - b.get("lSmin", 0)) < 1e-9 for a, b in zip(DW["canonical"], DW["alt"]))
TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv"); GR = []
for l in open(TIAN):
    if l.startswith("#"): continue
    t = l.rstrip("\n").split("\t")
    if len(t) < 13 or not t[0].strip().isdigit() or t[1].strip() != "Galaxy group": continue
    ls, els, lM, elM, Re = float(t[5]), float(t[6]), float(t[7]), float(t[8]), float(t[10])
    sig = 10 ** ls; r12 = 4 / 3 * Re * KPC; gobs = 3 * (sig * 1e3) ** 2 / r12; gN = GE * (10 ** lM / 2) * MSUN / r12 ** 2
    if (gobs - gN) / gN < 0.1:
        GR.append(dict(cls="group", name=t[2].strip(), detected=False, sig=sig)); continue
    Mc = (gobs - gN) * r12 ** 2 / GE / MSUN; r12pc = r12 / PC
    eM = math.hypot(gobs * 2 * math.log(10) * els, gN * math.log(10) * elM) * r12 ** 2 / GE / MSUN
    GR.append(dict(cls="group", name=t[2].strip(), detected=True, sig=sig, lMb=lM, lSmin=math.log10(CMIN["burkert"] * Mc / r12pc ** 2),
                   lSmin_iso=math.log10(CMIN["iso"] * Mc / r12pc ** 2), e=eM / Mc / math.log(10)))
P(f"dwarfs: {len(DW['canonical'])} per footing ({sum(d['detected'] for d in DW['canonical'])} with detected cold mass; footings identical: {same}); "
  f"groups: {len(GR)} ({sum(g['detected'] for g in GR)} detected)  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

# ------------------------------------------------------------------ eRASS1 KT terciles (X30 machinery read-only)
X30SRC = os.path.join(REB, "X30_sheet_cluster_profile", "x30_sheet_cluster_profile.py"); TX = open(X30SRC).read()
codeX = TX[:TX.index("# ============================================================== STEP 0")]
old = 'OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")'; assert codeX.count(old) == 1
codeX = codeX.replace(old, f'OUTF = open({os.path.join(HERE, "cs1_x30_machinery" + TAG + ".log")!r}, "w")')
NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(codeX, X30SRC, "exec"), NX)
sys.argv = argv0
HK, M_, DC, IX, TID, N, bsum, prep, RM, SIGKT = (NX[k] for k in ("HK", "M", "DC", "I", "TID", "N", "bsum", "prep", "RM", "SIG_KT"))
O_, P_, A_, DS_, KG, RF, SB, DAT, MPC = (NX[k] for k in ("offset_floor", "project_floor", "at_bins", "dsig_from_sig", "KG_PC2", "redfac", "sig_bins", "DAT", "MPC"))
check("K3", len(GR) == 63 and all(len(DW[f]) == 89 for f in FEET) and sum(c["primary"] for c in XC) == 7 and len(IX) == 106
      and abs(sref_chk - SREF) < 0.01, f"groups {len(GR)}, dwarfs {[len(DW[f]) for f in FEET]}, X-COP primary {sum(c['primary'] for c in XC)}, "
      f"KT clusters {len(IX)}, SPARC median sigma {sref_chk:.2f}")
def dvecN(i, foot, hk, Msrc):
    pp = prep(i, foot, hk); rho = np.gradient(Msrc, RM) / (4 * np.pi * RM ** 2)
    So = O_(P_(rho), pp["dmpc"]); Pp = A_(DS_(So)) / KG; fr, _ = RF(hk, i, SB(So)); return DAT[hk]["W"][i] * (Pp * fr)
def terc_pred(foot, hk, Mh_of):
    V = np.zeros((N, 8))
    for i in IX:
        pp = prep(int(i), foot, hk); V[i] = dvecN(int(i), foot, hk, pp["Mb"] + Mh_of(int(i), pp))
    vB = bsum(V)[IX]; vC = bsum(DC[(foot, hk)])[IX]
    return np.array([[vB[TID == t, b].sum() / vC[TID == t, b].sum() for b in range(3)] for t in range(3)])   # (tercile, band)
def meas(foot, hk):
    o = M_[f"{foot}|{hk}"]
    A = np.array([[o["KT_terc|INNER"][t]["A"], o["KT_terc|MID"][t]["A"], o["KT_terc|OUTER"][t]["A"]] for t in range(3)])
    S = np.array([[o["KT_terc|INNER"][t]["s_IN"], o["KT_terc|MID"][t]["s"], o["KT_terc|OUTER"][t]["s"]] for t in range(3)])
    return A, S
# K0c: X38's halos reproduce X38's cells
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
def solve_r0(Mtot, Rout, Sig):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    if lm(float(pk.x)) < math.log(Mtot): return math.exp(float(pk.x))
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), float(pk.x), xtol=1e-14))
SIGSI = A0["canonical"] / (2 * math.pi * GE)
def x38_halo(i, pp):
    r0 = solve_r0(pp["Mfair"], pp["rta"], SIGSI); return math.pi * SIGSI * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
A38 = terc_pred("canonical", "h0672", x38_halo); c38 = X38J["footings"]["canonical"]["clusters"]["cells"]["h0672"]
ref = np.array([[c38[f"G-MID-T{t+1}"]["pred"], c38[f"G-OUT-T{t+1}"]["pred"]] for t in range(3)])
dk0c = float(np.max(np.abs(A38[:, 1:] - ref)))
check("K0c", dk0c < 1e-6, f"X38 halos -> MID/OUTER tercile preds max |diff| {dk0c:.1e} vs x38_sd_halos_results.json")
LSE = np.round(np.arange(1.0, 4.5001, 0.1), 2); LXE = np.round(np.arange(-2.0, 0.6001, 0.1), 2)
ER = {}
CACHE = os.environ.get("CS1_ERASS_CACHE")          # optional cache of the eRASS1 chi2 grids (identical numbers; the normal run computed and saved them, MUTATE loaded them)
for foot in FEET:
    Am, Sm = meas(foot, "h0672"); chi = np.zeros((3, len(LSE), len(LXE)))
    cf = os.path.join(CACHE, f"erass_{foot}.npy") if CACHE else None
    for js, ls in enumerate(LSE if not (cf and os.path.exists(cf)) else []):
        S_ = 10 ** ls * SPC
        for jx, lx in enumerate(LXE):
            def mh(i, pp, S_=S_, lx=lx):
                r0 = 10 ** lx * pp["R500"] * MPC; return math.pi * S_ * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
            Ap = terc_pred(foot, "h0672", mh); chi[:, js, jx] = (((Am - Ap) / Sm) ** 2).sum(1)
        if js % 6 == 0: P(f"  eRASS1 [{foot}] grid row {js + 1}/{len(LSE)}  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    if cf:
        if os.path.exists(cf): chi = np.load(cf)
        else: np.save(cf, chi)
    res = []
    for t in range(3):
        pr = chi[t].min(1); cs = CubicSpline(LSE, pr); fine = np.round(np.arange(LSE[0], LSE[-1] + 1e-9, 0.01), 2); pf_ = cs(fine)
        jb = int(pf_.argmin()); scale = max(1.0, float(pf_[jb]) / 1); okk = np.where((pf_ - pf_[jb]) / scale <= 1)[0]
        lo, hi = int(okk.min()), int(okk.max()); jx = int(chi[t, int(np.argmin(np.abs(LSE - fine[jb])))].argmin())
        kind = ("unconstrained" if lo == 0 and hi == len(fine) - 1 else "lower" if hi == len(fine) - 1 else "upper" if lo == 0 else "two-sided")
        mem = TID == t; R500m = float(np.median([prep(int(i), foot, "h0672")["R500"] for i in IX[mem]]))
        Mb5 = float(np.median([np.interp(prep(int(i), foot, "h0672")["R500"] * MPC, RM, prep(int(i), foot, "h0672")["Mb"]) for i in IX[mem]])) / MSUN
        Mf = float(np.median([prep(int(i), foot, "h0672")["Mfair"] for i in IX[mem]])) / MSUN
        res.append(dict(cls="eRASS1", name=f"KT T{t + 1}", sig=float(np.median(SIGKT[mem])), lMb=math.log10(Mb5), lMfair=math.log10(Mf),
                        B=dict(lS=float(fine[jb]), lS_lo=float(fine[lo]), lS_hi=float(fine[hi]), kind=kind, e=float(0.5 * (fine[hi] - fine[lo])),
                               lr0=float(math.log10(10 ** LXE[jx] * R500m * 1e3)), lx0=float(LXE[jx]), chi2=float(pf_[jb]), dof=1)))
    ER[foot] = res
    # h 0.686 reported at the h 0.672 best point
    for t, e in enumerate(res):
        S_ = 10 ** e["B"]["lS"] * SPC; lx = e["B"]["lx0"]
        def mh(i, pp, S_=S_, lx=lx):
            r0 = 10 ** lx * pp["R500"] * MPC; return math.pi * S_ * r0 ** 2 * B(np.minimum(RM, pp["rta"]) / r0)
        A6, S6 = meas(foot, "h0686"); Ap6 = terc_pred(foot, "h0686", mh); e["chi2_h0686_at_best"] = float((((A6 - Ap6) / S6) ** 2)[t].sum())
        P(f"  eRASS1 [{foot}] {e['name']}: log Sigma0 {e['B']['lS']:.2f} [{e['B']['lS_lo']:.2f}, {e['B']['lS_hi']:.2f}] {e['B']['kind']}, x0 = r0/R500 10^{e['B']['lx0']:.1f}, "
          f"chi2 {e['B']['chi2']:.2f}/1 (h0.686 at same point {e['chi2_h0686_at_best']:.2f}); sigma {e['sig']:.0f}")
    NX["PREP"].clear()

# ------------------------------------------------------------------ the law
def model(m, p, x):
    if m == "M0": return np.full_like(x, p[0])
    if m == "M1": return p[0] + p[1] * x
    if m == "M2": return np.where(x < p[3], p[0] + p[1] * (x - p[3]), p[0] + p[2] * (x - p[3]))
    if m == "M3": return np.log10(10 ** p[0] + 10 ** (p[1] + p[2] * x))
KPAR = {"M0": 1, "M1": 2, "M2": 4, "M3": 3}
XB = (math.log10(15 / SREF), math.log10(600 / SREF))
def nll(m, p, ls, x, y, e, cx, cy, ce):
    s = math.exp(ls); mu = model(m, p, x); v = e ** 2 + s * s
    L = 0.5 * np.sum((y - mu) ** 2 / v + np.log(2 * math.pi * v))
    if len(cx):
        L -= np.sum(norm.logcdf((model(m, p, cx) - cy) / np.sqrt(ce ** 2 + s * s)))        # lower bounds: Sigma >= cy
    return float(L)
def fit_law(m, x, y, e, cx=np.array([]), cy=np.array([]), ce=np.array([])):
    best = None; a0, q0 = float(np.median(y)), 0.5
    starts = {"M0": [[a0]], "M1": [[a0, q] for q in (0.0, 0.5, 1.0)],
              "M2": [[a0, q1, q2, xb] for q1 in (0.0, 1.0) for q2 in (0.0, 1.0) for xb in (-0.5, 0.0, 0.5, 1.0)],
              "M3": [[f, a0 + d, q] for f in (1.5, 2.0, 2.5) for d in (-0.5, 0.0) for q in (0.5, 1.0, 2.0)]}[m]
    for st in starts:
        fun = lambda z: nll(m, z[:-1] if m != "M2" else np.r_[z[:3], np.clip(z[3], *XB)], z[-1], x, y, e, cx, cy, ce) + (0 if m != "M2" else 1e3 * max(0, abs(z[3] - np.clip(z[3], *XB))))
        r = minimize(fun, np.r_[st, math.log(0.2)], method="Nelder-Mead", options={"maxiter": 40000, "maxfev": 40000, "xatol": 1e-7, "fatol": 1e-9})
        if best is None or r.fun < best.fun: best = r
    p = best.x[:-1].copy()
    if m == "M2": p[3] = float(np.clip(p[3], *XB))
    n = len(x) + len(cx); k = KPAR[m] + 1
    return dict(model=m, p=[float(v) for v in p], s_int=float(math.exp(best.x[-1])), nll=float(best.fun), BIC=float(2 * best.fun + k * math.log(n)), k=k, n=n)
def qerr(x, y, e, s):
    w = 1 / (e ** 2 + s * s); A = np.vstack([np.ones_like(x), x]).T; C = np.linalg.inv(A.T @ (A * w[:, None])); return float(math.sqrt(C[1, 1]))
def select(fits_, xr):
    ok = {}
    for m, f in fits_.items():
        if m == "M2": ok[m] = xr[0] < f["p"][3] < xr[1] and XB[0] + 1e-3 < f["p"][3] < XB[1] - 1e-3
        elif m == "M3": ok[m] = f["p"][2] > 0 and xr[0] < (f["p"][0] - f["p"][1]) / f["p"][2] < xr[1]
        else: ok[m] = True
    cand = [m for m in fits_ if ok[m]]; mb = min(cand, key=lambda m: fits_[m]["BIC"])
    simp = [m for m in cand if fits_[m]["k"] < fits_[mb]["k"] and fits_[m]["BIC"] - fits_[mb]["BIC"] < 6]
    sel = min(simp, key=lambda m: fits_[m]["k"]) if simp else mb
    return sel, ok
CLASSNAME = {"M0": "FLAT FLOOR", "M1": "SINGLE POWER LAW", "M2": "BROKEN", "M3": "FLOOR + RISE"}
OS1Q = {"canonical": 0.892, "alt": 0.748}
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
X43T = sorted((math.log10(float(k)), math.log10(v[0]), v[1]) for k, v in X43J["sigma_coll_table"].items())
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]
def x43(foot, lM200):
    lsc = np.interp(lM200, [t[0] for t in X43T], [t[1] for t in X43T], left=None, right=None)
    if lM200 > X43T[-1][0] or lM200 < X43T[0][0]:
        sl = np.polyfit([t[0] for t in X43T], [t[1] for t in X43T], 1); lsc = np.polyval(sl, lM200)
    return math.log10(max(SIGA0[foot], 14.83 * 10 ** lsc))
def zf43(lM200): return float(np.interp(lM200, [t[0] for t in X43T], [t[2] for t in X43T]))
rng = np.random.default_rng(20261027)
RES = dict(frozen="6f303e256b", mutate=MUTATE, Sigma_a0=SIGA0, footings={}, checks={})
ATLAS = []
for foot in FEET:
    P(f"\n=== [{foot}] law fit (Sigma_a0 {SIGA0[foot]:.1f})")
    prim = [s for s in SP if s["B"]["kind"] == "two-sided"] + ([mw] if mw["B"]["kind"] == "two-sided" else []) \
        + [c for c in XC if c["primary"] and c["B"]["kind"] == "two-sided"] + [e for e in ER[foot] if e["B"]["kind"] == "two-sided"]
    x = np.log10(np.array([s["sig"] for s in prim]) / SREF); y = np.array([s["B"]["lS"] for s in prim]); e = np.array([max(s["B"]["e"], 0.005) for s in prim])
    cl = np.array([s["cls"] for s in prim])
    cens = [s for s in SP if s["B"]["kind"] == "lower"] + [c for c in XC if c["primary"] and c["B"]["kind"] == "lower"] \
        + [e_ for e_ in ER[foot] if e_["B"]["kind"] == "lower"] + ([mw] if mw["B"]["kind"] == "lower" else [])
    cx = np.log10(np.array([s["sig"] for s in cens]) / SREF) if cens else np.array([]); cy = np.array([s["B"]["lS_lo"] for s in cens]); ce = np.zeros(len(cens))
    dws = [d for d in DW[foot] if d["detected"]]; grs = [g for g in GR if g["detected"]]
    bx = np.log10(np.array([d["sig"] for d in dws + grs]) / SREF); by = np.array([d["lSmin"] for d in dws + grs]); be = np.array([d["e"] for d in dws + grs])
    if MUTATE:
        x = rng.permutation(x); allx = rng.permutation(np.r_[x, cx, bx]); cxm, bxm = allx[len(x):len(x) + len(cx)], allx[len(x) + len(cx):]
    else:
        cxm, bxm = cx, bx
    P(f"  PRIMARY: {len(prim)} two-sided ({', '.join(f'{k} {int((cl == k).sum())}' for k in ('SPARC', 'MW', 'XCOP', 'eRASS1'))}); sigma range "
      f"{SREF * 10 ** x.min():.0f}-{SREF * 10 ** x.max():.0f} km/s")
    F = {m: fit_law(m, x, y, e) for m in ("M0", "M1", "M2", "M3")}
    sel, okm = select(F, (x.min(), x.max()))
    for m, f in F.items():
        P(f"    {m} {CLASSNAME[m]:17s} p {[round(v, 3) for v in f['p']]}, s_int {f['s_int']:.3f}, BIC {f['BIC']:.1f} (dBIC {f['BIC'] - F[sel]['BIC']:+.1f})" + ("" if okm[m] else "  [break/floor outside range: not selectable]"))
    fs = F[sel]; res_ = y - model(sel, fs["p"], x); override = []
    if fs["s_int"] > 0.35: override.append(f"s_int {fs['s_int']:.2f} > 0.35")
    clres = {}
    for k in ("SPARC", "XCOP", "eRASS1", "MW"):
        mk = cl == k
        if not mk.any(): continue
        rr = res_[mk]; n = int(mk.sum())
        if n >= 3:
            se = float(rr.std(ddof=1) / math.sqrt(n)); clres[k] = dict(n=n, mean=float(rr.mean()), se=se)
            if abs(rr.mean()) > 3 * se and abs(rr.mean()) > 0.25: override.append(f"{k} mean residual {rr.mean():+.2f} ({rr.mean() / se:+.1f} se)")
        elif k == "MW":
            zz = float(rr[0] / math.hypot(e[mk][0], fs["s_int"])); clres[k] = dict(n=1, resid=float(rr[0]), z=zz)
            if abs(zz) > 3: override.append(f"MW residual z {zz:+.1f}")
        else:
            clres[k] = dict(n=n, mean=float(rr.mean()))
    cls_p = "NO SIMPLE LAW" if override else CLASSNAME[sel]
    qe = qerr(x, y, e, F["M1"]["s_int"]); qsig = F["M1"]["p"][1] / qe
    P(f"  PRIMARY selected {sel}; class residuals {json.dumps({k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in clres.items()})}")
    P(f"  PRIMARY CLASS [{foot}]: {cls_p}" + (f"  (override: {'; '.join(override)})" if override else "") + f"; M1 slope q = {F['M1']['p'][1]:.3f} +- {qe:.3f} ({qsig:.1f} sigma)")
    # whole range (Tobit)
    WX = np.r_[cxm, bxm]; WY = np.r_[cy, by]; WE = np.r_[ce, be]
    FW = {m: fit_law(m, x, y, e, WX, WY, WE) for m in ("M0", "M1", "M2", "M3")}
    selW, okW = select(FW, (min(x.min(), WX.min()), max(x.max(), WX.max())))
    for m, f in FW.items():
        P(f"    WHOLE {m} p {[round(v, 3) for v in f['p']]}, s_int {f['s_int']:.3f}, BIC {f['BIC']:.1f} (dBIC {f['BIC'] - FW[selW]['BIC']:+.1f})" + ("" if okW[m] else "  [not selectable]"))
    fw = FW[selW]; ovW = []
    if fw["s_int"] > 0.35: ovW.append(f"s_int {fw['s_int']:.2f} > 0.35")
    resW = y - model(selW, fw["p"], x)
    for k in ("SPARC", "XCOP", "eRASS1"):
        mk = cl == k
        if mk.sum() >= 3:
            rr = resW[mk]; se = float(rr.std(ddof=1) / math.sqrt(mk.sum()))
            if abs(rr.mean()) > 3 * se and abs(rr.mean()) > 0.25: ovW.append(f"{k} mean residual {rr.mean():+.2f}")
    if (cl == "MW").any():
        zz = float(resW[cl == "MW"][0] / math.hypot(e[cl == "MW"][0], fw["s_int"]))
        if abs(zz) > 3: ovW.append(f"MW residual z {zz:+.1f}")
    cls_w = "NO SIMPLE LAW" if ovW else CLASSNAME[selW]
    P(f"  WHOLE-RANGE CLASS [{foot}]: {cls_w} ({selW})" + (f"  (override: {'; '.join(ovW)})" if ovW else "") + f"; {len(cens)} SPARC/cluster bounds + {len(dws)} dwarf + {len(grs)} group bounds")
    # dwarf / group read-out against the PRIMARY law
    def bound_read(lst, xx):
        ex = [(d["lSmin"] - float(model(sel, fs["p"], np.array([xv]))[0])) / math.hypot(d["e"], fs["s_int"]) > 2 for d, xv in zip(lst, xx)]
        fr = float(np.mean(ex)) if ex else float("nan")
        return dict(n=len(ex), frac_exceed=fr, cls="ABOVE LAW" if fr >= 0.25 else "CONSISTENT" if fr < 0.05 else "PARTIAL",
                    median_lSmin=float(np.median([d["lSmin"] for d in lst])), median_sig=float(np.median([d["sig"] for d in lst])),
                    median_excess=float(np.median([d["lSmin"] - float(model(sel, fs["p"], np.array([xv]))[0]) for d, xv in zip(lst, xx)])))
    rd = bound_read(dws, bx[:len(dws)]); rg = bound_read(grs, bx[len(dws):])
    P(f"  dwarfs vs PRIMARY law: {rd['cls']} ({rd['frac_exceed']:.0%} of {rd['n']} exceed at 2 sigma); median Sigma_min 10^{rd['median_lSmin']:.2f} at sigma {rd['median_sig']:.1f}, "
      f"median (Sigma_min - law) {rd['median_excess']:+.2f} dex; vs Sigma_a0 {rd['median_lSmin'] - math.log10(SIGA0[foot]):+.2f} dex")
    P(f"  groups vs PRIMARY law: {rg['cls']} ({rg['frac_exceed']:.0%} of {rg['n']}); median Sigma_min 10^{rg['median_lSmin']:.2f} at sigma {rg['median_sig']:.0f}, median excess {rg['median_excess']:+.2f} dex")
    # candidates (reported)
    def cand(name, fn):
        pr = np.array([fn(s) for s in prim]); r = y - pr; o = dict(chi2_meas=float(np.sum(r ** 2 / e ** 2)), chi2_sint=float(np.sum(r ** 2 / (e ** 2 + fs["s_int"] ** 2))), by_class={})
        for k in ("SPARC", "MW", "XCOP", "eRASS1"):
            mk = cl == k
            if mk.any(): o["by_class"][k] = dict(median=float(np.median(r[mk])), rms=float(np.sqrt(np.mean(r[mk] ** 2))), n=int(mk.sum()))
        P(f"    {name:26s} chi2(meas) {o['chi2_meas']:9.0f}  chi2(+s_int) {o['chi2_sint']:7.1f}  " + "  ".join(f"{k} med {v['median']:+.2f} rms {v['rms']:.2f}" for k, v in o["by_class"].items()))
        return o
    def lM200(s):
        if s["cls"] in ("SPARC", "MW"): return EM1J["a"] + EM1J["b"] * (s["lMb"] - 10)
        if s["cls"] == "XCOP": return s["lM200"]
        return s["lMfair"]
    P("  candidates on the PRIMARY sample (residual = measured - candidate, dex):")
    CAND = {"X38 flat": cand("X38 flat Sigma_a0", lambda s: math.log10(SIGA0[foot])),
            "OS1": cand(f"OS1 q {OS1Q[foot]}", lambda s: math.log10(SIGA0[foot]) + OS1Q[foot] * math.log10(s["sig"] / SREF)),
            "X43": cand("X43 floor+collapse (own M)", lambda s: x43(foot, lM200(s))),
            "CS1 selected": cand(f"CS1 {sel}", lambda s: float(model(sel, fs["p"], np.array([math.log10(s['sig'] / SREF)]))[0]))}
    # correlations
    lr0 = np.array([s["B"]["lr0"] for s in prim]); lmb = np.array([s["lMb"] for s in prim]); zf = np.array([zf43(lM200(s)) for s in prim])
    COR = {k: dict(zip(("rho", "p"), [float(v) for v in spearmanr(y, v_)])) for k, v_ in (("sigma", x), ("M_b", lmb), ("r0", lr0), ("X43 z_f (non-native)", zf))}
    P("  Spearman (log Sigma0 vs): " + "; ".join(f"{k} {v['rho']:+.2f} (p {v['p']:.1e})" for k, v in COR.items()))
    sp_only = fit_law("M1", x[cl == "SPARC"], y[cl == "SPARC"], e[cl == "SPARC"])
    P(f"  reported: SPARC-only power law q {sp_only['p'][1]:.3f}, s_int {sp_only['s_int']:.3f}")
    # Milky Way read-out
    mwpred = float(model(sel, fs["p"], np.array([math.log10(mw["sig"] / SREF)]))[0])
    mwr = dict(lS=mw["B"]["lS"], lS_lo=mw["B"]["lS_lo"], lS_hi=mw["B"]["lS_hi"], kind=mw["B"]["kind"], over_Sigma_a0=10 ** (mw["B"]["lS"] - math.log10(SIGA0[foot])),
               law_pred=mwpred, resid=mw["B"]["lS"] - mwpred, s_band=mw["band"], os1_pred=math.log10(SIGA0[foot]) + OS1Q[foot] * math.log10(mw["sig"] / SREF),
               lr0=mw["B"]["lr0"], iso=mw["iso"]["lS"])
    P(f"  MW: Sigma0 = {mwr['over_Sigma_a0']:.2f} Sigma_a0 (log {mwr['lS']:.2f} [{mwr['lS_lo']:.2f}, {mwr['lS_hi']:.2f}]); law at its sigma {mwpred:.2f} (resid {mwr['resid']:+.2f}); "
      f"OS1 at sigma {mw['sig']:.0f}: {mwr['os1_pred']:.2f}; GD1's Eilers need ~3.5 Sigma_a0 = {math.log10(3.5 * SIGA0[foot]):.2f}; r0 10^{mwr['lr0']:.2f} kpc")
    # variants (reported)
    def vstat(get):
        vv = [get(s) for s in prim]; ok_ = [i for i, v in enumerate(vv) if v is not None]
        if len(ok_) < 5: return None
        xv, yv, ev = x[ok_], np.array([vv[i][0] for i in ok_]), np.array([max(vv[i][1], 0.005) for i in ok_])
        f1 = fit_law("M1", xv, yv, ev); f0 = fit_law("M0", xv, yv, ev); return dict(n=len(ok_), q=f1["p"][1], a=f1["p"][0], s_int=f1["s_int"], dBIC_M0_M1=f0["BIC"] - f1["BIC"])
    VAR = {"isothermal": vstat(lambda s: (s["iso"]["lS"], s["iso"]["e"]) if s.get("iso") and s["iso"]["kind"] == "two-sided" else None),
           "SPARC U=0.50": vstat(lambda s: (s["U05"]["lS"], s["U05"]["e"]) if s["cls"] == "SPARC" and s["U05"]["kind"] == "two-sided" else ((s["B"]["lS"], s["B"]["e"]) if s["cls"] != "SPARC" else None))}
    xa = [c for c in XC if c["B"]["kind"] == "two-sided"]
    VAR["X-COP all 12 (M*=0 for 5)"] = dict(n=len(xa), median_lS=float(np.median([c["B"]["lS"] for c in xa])) if xa else None,
                                           primary_median_lS=float(np.median([c["B"]["lS"] for c in XC if c["primary"] and c["B"]["kind"] == "two-sided"])) if any(c["primary"] and c["B"]["kind"] == "two-sided" for c in XC) else None)
    VAR["eRASS1 h0.686 chi2 at h0.672 best"] = [e_["chi2_h0686_at_best"] for e_ in ER[foot]]
    for k, v in VAR.items(): P(f"    variant {k}: {v}")
    RES["footings"][foot] = dict(n_primary=len(prim), fits=F, selected=sel, class_primary=cls_p, override=override, class_residuals=clres,
                                 M1_slope=dict(q=F["M1"]["p"][1], se=qe, nsig=qsig), whole=FW, selected_whole=selW, class_whole=cls_w, override_whole=ovW,
                                 dwarfs=rd, groups=rg, candidates=CAND, spearman=COR, sparc_only_M1=sp_only, MW=mwr, variants=VAR,
                                 dwarf_by_class={k: float(np.median([d["lSmin"] for d in dws if d["sub"] == k])) for k in sorted(set(d["sub"] for d in dws))})
    if MUTATE:
        bites = abs(qsig) < 2 and (F["M0"]["BIC"] - F["M1"]["BIC"]) < 6
        RES["footings"][foot]["mutate_bites"] = bool(bites)
        P(f"  MUTATE [{foot}]: shuffled-sigma M1 slope {F['M1']['p'][1]:.3f} ({qsig:.1f} sigma), dBIC(M0-M1) {F['M0']['BIC'] - F['M1']['BIC']:+.1f} -> {'control BITES (trend vanishes)' if bites else 'ALARM: trend survives the shuffle'}")
    if foot == "canonical" and not MUTATE:
        for s in SP + [mw] + XC:
            ATLAS.append(dict(cls=s["cls"], name=s["name"], footing="both", sigma=s["sig"], lMb=s["lMb"], lSigma0=s["B"]["lS"], lo=s["B"]["lS_lo"], hi=s["B"]["lS_hi"],
                              kind=s["B"]["kind"], lr0_kpc=s["B"]["lr0"], U=s["B"].get("U", ""), chi2=s["B"]["chi2"], dof=s["B"]["dof"],
                              lSigma0_iso=s["iso"]["lS"], kind_iso=s["iso"]["kind"]))
    if not MUTATE:
        for s in ER[foot]:
            ATLAS.append(dict(cls=s["cls"], name=s["name"], footing=foot, sigma=s["sig"], lMb=s["lMb"], lSigma0=s["B"]["lS"], lo=s["B"]["lS_lo"], hi=s["B"]["lS_hi"],
                              kind=s["B"]["kind"], lr0_kpc=s["B"]["lr0"], U="", chi2=s["B"]["chi2"], dof=1, lSigma0_iso="", kind_iso=""))
        for d in DW[foot] + (GR if foot == "canonical" else []):
            ATLAS.append(dict(cls=d["cls"], name=d["name"], footing=foot if d["cls"] == "dwarf" else "both", sigma=d["sig"], lMb=d.get("lMb", ""),
                              lSigma0=d.get("lSmin", ""), lo=d.get("lSmin", ""), hi="", kind="Burkert lower bound (two-point)" if d["detected"] else "no cold mass detected",
                              lr0_kpc=math.log10(d["r0_at_min_pc"] / 1e3) if d.get("r0_at_min_pc") else "", U="", chi2="", dof="", lSigma0_iso=d.get("lSmin_iso", ""), kind_iso=""))
    RES["footings"][foot]["_plot"] = dict(x=x.tolist(), y=y.tolist(), e=e.tolist(), cl=cl.tolist(), bx=bx.tolist(), by=by.tolist(),
                                          bcl=["dwarf"] * len(dws) + ["group"] * len(grs), cx=cx.tolist(), cy=cy.tolist())

V1 = {f: RES["footings"][f]["class_primary"] for f in FEET}; V2 = {f: RES["footings"][f]["class_whole"] for f in FEET}
RES["verdict_primary"] = V1["canonical"] if V1["canonical"] == V1["alt"] else f"UNDECIDED ({V1})"
RES["verdict_whole"] = V2["canonical"] if V2["canonical"] == V2["alt"] else f"UNDECIDED ({V2})"
P(f"\n=== VERDICT (both footings): PRIMARY {RES['verdict_primary']}; WHOLE-RANGE {RES['verdict_whole']}")
check("K4", rss() < 1.0, f"peak RSS {rss():.2f} GB, one thread")
RES["checks"] = {k: ok for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
open(os.path.join(HERE, f"cs1_atlas{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
json.dump(RES, open(os.path.join(HERE, f"cs1_atlas_results{TAG}.json"), "w"), indent=1, default=float)
if not MUTATE:
    with open(os.path.join(HERE, "cs1_atlas.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ATLAS[0])); w.writeheader(); [w.writerow(r) for r in ATLAS]
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
    for ax, foot in zip(axs, FEET):
        pd = RES["footings"][foot]["_plot"]; xx, yy, ee, cc = np.array(pd["x"]), np.array(pd["y"]), np.array(pd["e"]), np.array(pd["cl"])
        sty = {"SPARC": ("#8a8a8a", "o"), "MW": ("#d62728", "*"), "XCOP": ("#1f77b4", "s"), "eRASS1": ("#9467bd", "D")}
        for k, (col, mk) in sty.items():
            m_ = cc == k
            if m_.any(): ax.errorbar(SREF * 10 ** xx[m_], yy[m_], yerr=ee[m_], fmt=mk, color=col, ms=9 if k == "MW" else 4, lw=0.6, label=f"{k} ({m_.sum()})")
        bxx, byy, bcl = np.array(pd["bx"]), np.array(pd["by"]), np.array(pd["bcl"])
        for k, col in (("dwarf", "#2ca02c"), ("group", "#ff7f0e")):
            m_ = bcl == k
            if m_.any(): ax.scatter(SREF * 10 ** bxx[m_], byy[m_], marker="^", s=14, color=col, label=f"{k} lower bounds ({m_.sum()})")
        sg_ = np.logspace(0, 3.2, 200); lx_ = np.log10(sg_ / SREF); fsel = RES["footings"][foot]["fits"][RES["footings"][foot]["selected"]]
        ax.plot(sg_, model(RES["footings"][foot]["selected"], fsel["p"], lx_), "k-", lw=2, label=f"CS1 {RES['footings'][foot]['selected']} (s_int {fsel['s_int']:.2f})")
        ax.axhline(math.log10(SIGA0[foot]), color="c", ls="--", label="X38 flat Σ_a0")
        ax.plot(sg_, math.log10(SIGA0[foot]) + OS1Q[foot] * lx_, "m:", lw=2, label=f"OS1 σ^{OS1Q[foot]}")
        ax.set_xscale("log"); ax.set_xlabel("σ [km/s]"); ax.set_title(f"{foot} (a0 {A0[foot]:.4g})"); ax.set_ylim(-0.5, 4.8)
    axs[0].set_ylabel("log Σ0 = ρ0 r0 [M☉ pc⁻²] (Burkert, route E)"); axs[1].legend(fontsize=7, loc="upper left")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "cs1_atlas.png"), dpi=120)
if MUTATE:
    sys.exit(1 if all(RES["footings"][f]["mutate_bites"] for f in FEET) else 0)
sys.exit(0 if n == len(checks) else 1)
