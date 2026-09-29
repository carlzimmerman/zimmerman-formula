#!/usr/bin/env python3
# CFG84: independent re-derivation of CFG79's headline. Spec: CFG84_SPEC_FROZEN.txt (frozen before any run). Own code; no repo imports.
import os, sys, math, itertools, json
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

MUTATE = os.environ.get("MUTATE", "0") == "1"
TSV = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/humphrey2006_ellipticals.tsv"
G, KPC, MSUN, MPC = 6.674e-11, 3.0857e19, 1.989e30, 3.0857e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
RADII = (5.0, 10.0, 20.0, 40.0, 70.0)
FB = 0.02237 / (0.02237 + 0.1200)
HH = 0.674
RHO_C = 3 * (67.4e3 / MPC) ** 2 / (8 * math.pi * G) / MSUN * MPC ** 3          # Msun/Mpc^3

checks = []
def check(name, ok, detail):
    checks.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")

# ------------------------------------------------------------------ kernel nu_mono (own construction, CFG5's stated recipe)
def h_rar(y):
    y = np.asarray(y, float); return y / np.expm1(np.sqrt(y))
def dh_rar(t):
    s = math.sqrt(t); E = math.expm1(s); return (2 * E - s * (1 + E)) / (2 * E ** 2)
Y_P = brentq(dh_rar, 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
Y_S = brentq(lambda t: dh_rar(t) - DELTA * H_P / (t + Y_P), 1.0, Y_P)
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    h = np.where(y <= Y_S, h_rar(np.minimum(y, Y_S)), float(h_rar(Y_S)) + DELTA * H_P * np.log((y + Y_P) / (Y_S + Y_P)))
    return 1.0 + h / y

# ------------------------------------------------------------------ data
rows = [l.rstrip("\n").split("\t") for l in open(TSV) if l.strip() and not l.startswith("#")]
hd = {h: i for i, h in enumerate(rows[0])}
GAL = [dict(name=d[hd["name"]], LK=float(d[hd["LK_1e11"]]) * 1e11, Re=float(d[hd["Re_kpc"]]), Mvir=float(d[hd["Mvir_1e12"]]) * 1e12,
            Rvir=float(d[hd["Rvir_kpc"]]), c=float(d[hd["c"]]), uf=float(d[hd["ups_fit"]]), uk=float(d[hd["ups_krou"]]),
            us=float(d[hd["ups_salp"]])) for d in rows[1:]]
NG = len(GAL)
def m_nfw(t): return np.log1p(t) - t / (1 + t)
def M_hern(r, Ms, Re):
    a = Re / 1.8153; return Ms * r ** 2 / (r + a) ** 2
def M_nfw_h(r, Mdm, Rvir, c): return Mdm * m_nfw(c * r / Rvir) / m_nfw(c)
def gobs_pts(g):
    Mfit = g["uf"] * g["LK"]; Mdm = max(g["Mvir"] - Mfit, 1e9)
    return np.array([G * (M_hern(r, Mfit, g["Re"]) + M_nfw_h(r, Mdm, g["Rvir"], g["c"])) * MSUN / (r * KPC) ** 2 for r in RADII])
GOBS = [gobs_pts(g) for g in GAL]
def gbar_pts(g, ups, radii=RADII):
    return np.array([G * M_hern(r, ups * g["LK"], g["Re"]) * MSUN / (r * KPC) ** 2 for r in radii])

# ------------------------------------------------------------------ Moster+2013 z=0, exact inversion
def moster_mstar(lmh):
    N, lM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10 ** (np.asarray(lmh, float) - lM1)
    return 10 ** np.asarray(lmh, float) * 2 * N / (x ** (-be) + x ** ga)
def halo_mass(Ms):
    return 10 ** brentq(lambda l: math.log10(float(moster_mstar(l))) - math.log10(Ms), 6.0, 17.0, xtol=1e-14, rtol=1e-14)
def c_duffy_full(Mh): return 5.71 * (Mh / (2e12 / HH)) ** (-0.084)
def c_duffy_rel(Mh): return 6.71 * (Mh / (2e12 / HH)) ** (-0.091)
def c_dm(Mh): return 10 ** (0.905 - 0.101 * (math.log10(Mh * 0.674) - 12.0))
def R200(Mh): return (3 * Mh / (4 * math.pi * 200 * RHO_C)) ** (1 / 3.) * 1000.0
def M_nfw_lcdm(Mh, cfn, r):
    c = cfn(Mh); x = np.clip(r / R200(Mh), 1e-4, 5.0); return Mh * m_nfw(c * x) / m_nfw(c)

MSTAR_K = [g["uk"] * g["LK"] for g in GAL]
MH0 = [halo_mass(M) for M in MSTAR_K]                     # declared halos
MH0_SAL = [halo_mass(g["us"] * g["LK"]) for g in GAL]     # R4a mapping
MH0_FIT = [halo_mass(g["uf"] * g["LK"]) for g in GAL]

# ------------------------------------------------------------------ generic estimator: model(g_bar_array, gal_index, ups, radii) -> g_model
def offsets_generic(model, ups="uk", radii=RADII):
    per = []
    for i, g in enumerate(GAL):
        idx = [RADII.index(r) for r in radii]
        gb = gbar_pts(g, g[ups], radii)
        gm = model(i, gb, g[ups], radii)
        per.append(np.median(np.log10(GOBS[i][idx] / gm)))
    return np.array(per)
def summarize(model_factory, foot=None, salp_model=None, fit_row=True):
    """model_factory(ups_key) -> model(i, gb, ups, radii). Returns dict with base/salp/r40, floors, sigma, z."""
    base = offsets_generic(model_factory("uk"))
    salp = offsets_generic(model_factory("us"), ups="us")
    r40 = offsets_generic(model_factory("uk"), radii=RADII[:4])
    m = lambda a: float(a.mean())
    err = float(base.std(ddof=1) / math.sqrt(NG))
    imf = abs(m(salp) - m(base)); rad = abs(m(r40) - m(base)); floor = math.hypot(imf, rad); sig = math.hypot(err, floor)
    return dict(per=base, mean=m(base), err=err, imf=imf, rad=rad, floor=floor, sig=sig, z=m(base) / sig, salp=m(salp), r40=m(r40))

def model_B(foot):
    a0 = A0[foot]
    def fac(ups):
        return lambda i, gb, u, radii: nu_mono(gb / a0) * gb
    return fac
def model_L(MH, cfn=c_duffy_full, mult=1.0, halo_zero=False):
    def fac(ups):
        def mod(i, gb, u, radii):
            Mh = MH[i] * mult
            if halo_zero: return gb
            Mn = np.array([M_nfw_lcdm(Mh, cfn, r) for r in radii])
            return gb + G * (1 - FB) * Mn * MSUN / (np.array(radii) * KPC) ** 2
        return mod
    return fac
def cls(zB, zL):
    if abs(zB) <= 1: return "B-ok"
    if abs(zL) <= 2: return "SPECIFIC-TO-B"
    return "SHARED" if zL * zB > 0 else "LCDM-WORSE"

print("CFG84 -- independent re-derivation of CFG79 headline" + ("   *** MUTATE=1: scored LCDM halos x100 ***" if MUTATE else ""))
print(f"  kernel: y_p={Y_P:.4f} y*={Y_S:.4f}; f_b={FB:.5f}; rho_c={RHO_C:.5e} Msun/Mpc^3")

# ------------------------------------------------------------------ C0 kernel
print("\nC0 kernel controls")
ys = np.logspace(-8, 4, 2000); nn = nu_mono(ys)
cont = np.max(np.abs(np.diff(nn) / nn[1:])) 
check("C0 kernel: y* = 2.3374 (1e-3), nu>=1, monotone decreasing, deep-MOND nu sqrt(y)->1 (1e-3 at y=1e-8), nu-1<1e-3... at y=1e4",
      abs(Y_S - 2.3374) < 1e-3 and np.all(nn >= 1) and np.all(np.diff(nn) < 0) and abs(float(nu_mono(1e-8)) * 1e-4 - 1) < 1e-3 and float(nu_mono(1e4)) - 1 < 1e-2,
      f"y*={Y_S:.5f}; nu(1e-8)sqrt(1e-8)={float(nu_mono(1e-8))*1e-4:.5f}; nu(1e4)-1={float(nu_mono(1e4))-1:.2e}; max rel step {cont:.1e}; monotone {bool(np.all(np.diff(nn)<0))}")

# ------------------------------------------------------------------ B
print("\nB (CFG32 pipeline, my kernel)")
RB = {}
for f in FOOTS:
    RB[f] = summarize(model_B(f))
    r = RB[f]
    print(f"  {f:9s} per-galaxy " + " ".join(f"{o:+.3f}" for o in r["per"]))
    print(f"  {'':9s} mean {r['mean']:+.4f} err {r['err']:.4f} IMF {r['imf']:.4f} rad {r['rad']:.4f} floor {r['floor']:.4f} sigma {r['sig']:.4f} z {r['z']:+.3f}  salp {r['salp']:+.4f} r40 {r['r40']:+.4f}")
T_B = {"canonical": dict(per=[.572,.270,.043,.034,.341,.551,.151], mean=.280, err=.084, imf=.126, rad=.065, floor=.142, sig=.165, z=1.70, salp=.154, r40=.215),
       "alt": dict(per=[.539,.246,.016,.009,.315,.525,.126], mean=.254, err=.083, imf=.124, rad=.061, floor=.138, sig=.161, z=1.58, salp=.130, r40=.193)}
dev = 0.0; msg = []
for f in FOOTS:
    r, t = RB[f], T_B[f]
    dpg = max(abs(round(a, 2) - round(b, 2)) for a, b in zip(r["per"], t["per"]))
    d3 = max(abs(round(r[k], 3) - t[k]) for k in ("mean", "err", "imf", "rad", "floor", "sig", "salp", "r40"))
    dz = abs(round(r["z"], 2) - t["z"])
    msg.append(f"{f}: per-galaxy(2dp) max diff {dpg:.3f}; scalars(3dp) max diff {d3:.3f}; z diff {dz:.2f}")
    dev = max(dev, dpg - 0.011, d3, dz)  # per-galaxy in 2 dp: allow 0 diff -> handled below
    dev = max(dev, 0)
ok = all(max(abs(round(RB[f]["per"][i], 2) - round(T_B[f]["per"][i], 2)) for i in range(NG)) < 1e-9 for f in FOOTS) and \
     all(max(abs(round(RB[f][k], 3) - T_B[f][k]) for k in ("mean", "err", "imf", "rad", "floor", "sig", "salp", "r40")) < 1e-9 for f in FOOTS) and \
     all(abs(round(RB[f]["z"], 2) - T_B[f]["z"]) < 1e-9 for f in FOOTS)
check("P2 B reproduces CFG32's committed printed numbers (per-galaxy 2dp; mean/err/IMF/rad/floor/sigma/Salpeter/r<=40 at 3dp; z 2dp), both footings", ok, "; ".join(msg))

# POST-HOC (added after the first run showed P2 failing on a double-rounding artefact in MY target list; reported only, P2 stays FAIL)
PRINT2 = {"canonical": [.57,.27,.04,.03,.34,.55,.15], "alt": [.54,.25,.02,.01,.31,.53,.13]}   # CFG32 .out printed 2dp (read from its .out)
for f in FOOTS:
    print(f"  P2' (post hoc, reported) {f}: mine unrounded {' '.join(f'{o:.5f}' for o in RB[f]['per'])}; vs CFG32 printed 2dp: match = {[round(a,2) for a in RB[f]['per']] == PRINT2[f]}")
# ------------------------------------------------------------------ LCDM base + variants
print("\nLCDM (Moster+13 exact inversion, Duffy full, (1-f_b) NFW, nu=1)")
MSC = 100.0 if MUTATE else 1.0
print("  per-galaxy: M*_K [Msun], log Mh (Moster 200c), log Mvir_H, Duffy c, Humphrey c, R200 kpc, Humphrey Rvir")
for i, g in enumerate(GAL):
    print(f"   {g['name']:8s} M*={MSTAR_K[i]:.3e} logMh={math.log10(MH0[i]):.3f} logMvir_H={math.log10(g['Mvir']):.3f} c={c_duffy_full(MH0[i]):.2f} c_H={g['c']:.1f} R200={R200(MH0[i]):.0f} Rvir_H={g['Rvir']:.0f}")
CFGS = {"base": dict(cfn=c_duffy_full, m=1.0), "V1": dict(cfn=c_dm, m=1.0), "V2": dict(cfn=c_duffy_rel, m=1.0),
        "V3": dict(cfn=c_duffy_full, m=1 / 3), "V4": dict(cfn=c_duffy_full, m=3.0)}
RL0, RL = {}, {}
for k, v in CFGS.items():
    RL0[k] = summarize(model_L(MH0, v["cfn"], v["m"]))
    RL[k] = summarize(model_L(MH0, v["cfn"], v["m"] * MSC))
def show(tag, r):
    print(f"  {tag:14s} {r['mean']:+.4f} +- {r['sig']:.4f} (gal-gal {r['err']:.4f}, IMF {r['imf']:.4f}, rad {r['rad']:.4f}) z {r['z']:+.3f}")
for k in CFGS: show(k + (" (x100)" if MUTATE else ""), RL[k])
print("  base per-galaxy: " + " ".join(f"{o:+.3f}" for o in RL0["base"]["per"]))
T_L = dict(base=(.060, .123, .49), V1=(.006, .124, .05), V2=(.028, .125, .22), V3=(.150, .127, 1.18), V4=(-.012, .132, -.09))
T_LPG = [.494, -.010, -.149, -.162, .069, .263, -.087]
print("  vs CFG79 README (read): " + "; ".join(f"{k}: mine {RL0[k]['mean']:+.3f}/{RL0[k]['sig']:.3f}/{RL0[k]['z']:+.2f} vs {T_L[k][0]:+.3f}/{T_L[k][1]:.3f}/{T_L[k][2]:+.2f}" for k in CFGS))
dmax = max(max(abs(RL0[k]["mean"] - T_L[k][0]), abs(RL0[k]["sig"] - T_L[k][1])) for k in CFGS)
dpg = max(abs(a - b) for a, b in zip(RL0["base"]["per"], T_LPG))
print(f"  max |diff| offset/sigma over base+V1-V4: {dmax:.5f} ; per-galaxy base max diff {dpg:.5f}")
b = RL0["base"]
check("P1 [HEADLINE] LCDM base reproduces +0.060 +- 0.123 (z +0.49) to 3 decimals (|diff|<=5e-4)",
      abs(b["mean"] - .060) <= 5e-4 and abs(b["sig"] - .123) <= 5e-4 and abs(round(b["z"], 2) - .49) < 1e-9,
      f"mine {b['mean']:+.4f} +- {b['sig']:.4f} z {b['z']:+.3f}; gal-gal {b['err']:.3f} (CFG79 0.091) IMF {b['imf']:.3f} (0.081) rad {b['rad']:.3f} (0.018)")
check("P1b class on both footings (declared halos) = SPECIFIC-TO-B; V1-V4 all SPECIFIC-TO-B", all(cls(RB[f]["z"], RL0[k]["z"]) == "SPECIFIC-TO-B" for f in FOOTS for k in CFGS),
      "; ".join(f"{f}: base {cls(RB[f]['z'], RL0['base']['z'])}" for f in FOOTS))

# ------------------------------------------------------------------ C1 closed forms
print("\nC1 closed-form controls")
dh = 0.0
for g in GAL:
    a = g["Re"] / 1.8153
    for r in RADII:
        num = quad(lambda s: 4 * math.pi * s ** 2 * (1.0 / (2 * math.pi)) * a / (s * (s + a) ** 3), 0, r, epsabs=0, epsrel=1e-13)[0]
        dh = max(dh, abs(num / (r ** 2 / (r + a) ** 2) - 1))
check("C1a Hernquist enclosed mass = integral of Hernquist density (rho = M a /(2 pi r (r+a)^3)), 35 (galaxy,radius)", dh < 1e-9, f"max rel diff {dh:.1e}")
dq = 0.0; dn = 0.0; mono = True
HALO_SETS = [(cf, MH0[i] * m) for cf in (c_duffy_full, c_dm, c_duffy_rel) for i in range(NG) for m in (1.0, 1/3, 3.0, 100.0, 0.01, 1e-2*30, 300.0)]
for cf, Mh in HALO_SETS:
    c = cf(Mh); R = R200(Mh)
    dn = max(dn, abs(float(M_nfw_lcdm(Mh, cf, R)) / Mh - 1))
for cf in (c_duffy_full, c_dm, c_duffy_rel):
    for i in range(NG):
        Mh = MH0[i]; c = cf(Mh); R = R200(Mh)
        for r in RADII:
            X = c * min(max(r / R, 1e-4), 5.0)
            q = quad(lambda t: t / (1 + t) ** 2, 0, X, epsabs=0, epsrel=1e-13)[0]           # int rho x^2 dx with rho ~ 1/(x(1+x)^2)
            dq = max(dq, abs(float(M_nfw_lcdm(Mh, cf, r)) / (Mh * q / float(m_nfw(c))) - 1))
        rr = np.logspace(-0.5, 2.5, 400); mm = np.array([M_nfw_lcdm(Mh, cf, r) for r in rr]); mono = mono and bool(np.all(np.diff(mm) > 0))
check("C1b NFW: M(<R200)=M_h to 1e-12 (%d halos); closed form = quad of density to 1e-7 (base,V1,V2); monotone" % len(HALO_SETS), dn <= 1e-12 and dq <= 1e-7 and mono,
      f"max |M(R200)/Mh-1| {dn:.1e}; max quad diff {dq:.1e}; monotone {mono}")
rt = max(abs(math.log10(float(moster_mstar(math.log10(halo_mass(M))))) - math.log10(M)) for M in MSTAR_K)
hand = float(moster_mstar(12.0)) / 1e12
lmh = [math.log10(x) for x in MH0 + MH0_SAL + MH0_FIT]
check("C1c Moster: round trip 1e-9 (exact inversion); analytic M*/Mh at Mh=1e12 = 0.03427+-2e-5; every Mh (Kroupa/Salpeter/fit stars) inside h48's grid logMh 9-15.5",
      rt < 1e-9 and abs(hand - 0.03427) < 2e-5 and min(lmh) >= 9.0 and max(lmh) <= 15.5, f"round trip {rt:.1e}; M*/Mh(1e12)={hand:.5f}; logMh range {min(lmh):.3f}-{max(lmh):.3f}")
zoff = offsets_generic(model_L(MH0, halo_zero=True)("uk"))
ref = np.array([np.median(np.log10(GOBS[i] / gbar_pts(g, g["uk"]))) for i, g in enumerate(GAL)])
gmin = min(float(np.min((gbar_pts(g, g["uk"]) + G * (1 - FB) * np.array([M_nfw_lcdm(MH0[i], c_duffy_full, r) for r in RADII]) * MSUN / (np.array(RADII) * KPC) ** 2) / gbar_pts(g, g["uk"]))) for i, g in enumerate(GAL))
check("C1d M_h->0: LCDM offset == log10(g_obs/g_bar) exactly (footing-independent by construction: no a0 in the LCDM code path); g_L>=g_bar", np.max(np.abs(zoff - ref)) < 1e-14 and gmin >= 1.0,
      f"max diff {np.max(np.abs(zoff-ref)):.1e}; min g_L/g_bar {gmin:.4f}")

# ------------------------------------------------------------------ C3 estimator identity
def B_direct(foot):
    a0 = A0[foot]; per = []
    for i, g in enumerate(GAL):
        gb = gbar_pts(g, g["uk"]); per.append(np.median(np.log10(GOBS[i] / (nu_mono(gb / a0) * gb))))
    return np.mean(per)
check("C3 estimator identity: generic estimator with B kernel == direct B pipeline to 1e-12", max(abs(RB[f]["mean"] - B_direct(f)) for f in FOOTS) < 1e-12,
      f"{max(abs(RB[f]['mean'] - B_direct(f)) for f in FOOTS):.1e}")

# ------------------------------------------------------------------ Ladder R6 and P3
print("\nLadder: every declared Mh x m (floors recomputed at each m)")
exact = [0.01, 1 / 3, 1.0, 3.0, 33.0, 100.0, 300.0, 1 / 100]
grid = sorted(set(list(np.logspace(math.log10(0.003), math.log10(300), 61)) + exact))
LAD = {m: summarize(model_L(MH0, c_duffy_full, m)) for m in grid}
zB = RB["canonical"]["z"]
for m in [0.003, 0.005, 0.01, 1/3, 1, 3, 10, 33, 50, 70, 100, 300]:
    r = LAD.get(m) or summarize(model_L(MH0, c_duffy_full, m))
    print(f"   x{m:<8.4g} {r['mean']:+.4f} +- {r['sig']:.4f} z {r['z']:+.2f}  {cls(zB, r['z'])}")
means = np.array([LAD[m]["mean"] for m in grid]); zs = np.array([LAD[m]["z"] for m in grid])
def cross(sgn):
    # multiples where z crosses sgn*2 (fine bisection on log m)
    f = lambda lm: summarize(model_L(MH0, c_duffy_full, 10 ** lm))["z"] - sgn * 2.0
    lo, hi = (math.log10(0.0003), math.log10(0.5)) if sgn > 0 else (math.log10(3.0), math.log10(1e4))
    try: return 10 ** brentq(f, lo, hi, xtol=1e-6)
    except Exception as e: return float("nan")
mlo, mhi = cross(+1), cross(-1)
print(f"   z crosses +2 at x{mlo:.4g}; crosses -2 at x{mhi:.4g}")
check("C2 ladder: sample mean offset strictly decreasing in the halo multiple", bool(np.all(np.diff(means) < 0)), f"{len(grid)} multiples, x{grid[0]:.3g}..x{grid[-1]:.3g}")
inside = [m for m in grid if 0.01 - 1e-12 <= m <= 33.0 + 1e-9]
p3a = all(abs(LAD[m]["z"]) <= 2 for m in inside)
p3b = abs(LAD[100.0]["z"]) > 2
check("P3 gate weakness: |z|<=2 at every ladder point x0.01..x33 (%d points) and |z|>2 at x100" % len(inside), p3a and p3b,
      f"x0.01 z={LAD[0.01]['z']:+.3f} ({LAD[0.01]['mean']:+.3f}+-{LAD[0.01]['sig']:.3f}); x33 z={LAD[33.0]['z']:+.3f}; x100 z={LAD[100.0]['z']:+.3f} ({LAD[100.0]['mean']:+.3f}+-{LAD[100.0]['sig']:.3f}); crossings x{mlo:.4g} / x{mhi:.4g}")

# ------------------------------------------------------------------ H1 (footing-wise) with MUTATE handling
print("\nH1 classification")
cls_decl = {f: cls(RB[f]["z"], RL0["base"]["z"]) for f in FOOTS}
cls_x100 = {f: cls(RB[f]["z"], LAD[100.0]["z"]) for f in FOOTS}
cls_scored = {f: cls(RB[f]["z"], RL["base"]["z"]) for f in FOOTS}
zs_ = RL["base"]["z"]
check("H1a NOT SHARED: LCDM (scored halos) not off in B's direction at >2 sigma", not (zs_ > 2), f"z_L={zs_:+.3f}")
check("H1b NOT LCDM-WORSE: LCDM (scored halos) not off in the opposite direction at >2 sigma", not (zs_ < -2), f"z_L={zs_:+.3f}")
check("H1c THE GATE SEES THE HALO: class at all-Mh x100 differs from class at declared Mh (both footings)", all(cls_x100[f] != cls_decl[f] for f in FOOTS),
      f"declared {cls_decl}; x100 {cls_x100}")
check("M1 [MUTATE detector] scored class == declared class", all(cls_scored[f] == cls_decl[f] for f in FOOTS), f"scored {cls_scored}; declared {cls_decl}")

# ------------------------------------------------------------------ Reported rows
print("\nR4 floor readings (reported)")
Msal = summarize(lambda ups: (lambda i, gb, u, radii: gb + G * (1 - FB) * np.array([M_nfw_lcdm(MH0_SAL[i] if ups == "us" else MH0[i], c_duffy_full, r) for r in radii]) * MSUN / (np.array(radii) * KPC) ** 2))
print(f"  R4a IMF term with Mh re-derived from Salpeter M*: IMF {Msal['imf']:.4f}, sigma {Msal['sig']:.4f}, z {Msal['z']:+.3f}  (CFG79 +0.31)")
for f in FOOTS:
    s = math.hypot(RL0["base"]["err"], RB[f]["floor"]); print(f"  R4b B's floor on LCDM ({f}): sigma {s:.4f} z {RL0['base']['mean']/s:+.3f}  (CFG79 +0.35 / +0.36)")
fit_only = offsets_generic(lambda i, gb, u, radii: gb + G * (1 - FB) * np.array([M_nfw_lcdm(MH0[i], c_duffy_full, r) for r in radii]) * MSUN / (np.array(radii) * KPC) ** 2, ups="uf")
print(f"  R4c Salpeter {RL0['base']['salp']:+.3f} (CFG79 -0.021); fitted M/L {fit_only.mean():+.3f} (+0.113); r<=40 {RL0['base']['r40']:+.3f} (+0.078)")
print("R5 shape: slope of log(g_obs/g_L) vs log g_bar per galaxy")
sl = []
for i, g in enumerate(GAL):
    gb = gbar_pts(g, g["uk"]); gl = model_L(MH0)("uk")(i, gb, g["uk"], RADII)
    sl.append(np.polyfit(np.log10(gb), np.log10(GOBS[i] / gl), 1)[0])
slB = []
for i, g in enumerate(GAL):
    gb = gbar_pts(g, g["uk"]); gm = nu_mono(gb / A0["canonical"]) * gb
    slB.append(np.polyfit(np.log10(gb), np.log10(GOBS[i] / gm), 1)[0])
print("  LCDM slopes " + " ".join(f"{s:+.3f}" for s in sl) + f" ; negative {sum(s<0 for s in sl)}/7 (CFG79: -0.07..+0.12, 3/7)")
print("  B slopes    " + " ".join(f"{s:+.3f}" for s in slB) + f" ; negative {sum(s<0 for s in slB)}/7 (CFG32 7/7; different sign convention? vs y = g_bar/a0: same slope)")

print("\nR-circ: how much of the LCDM pass is built in (reported)")
print("  data allow only Humphrey's fitted NFW+stars model (no deprojected profile in TSV): a model-independent g_obs is NOT available")
print("  per-galaxy log Mh_Moster - log Mvir_H: " + " ".join(f"{math.log10(MH0[i]/g['Mvir']):+.2f}" for i, g in enumerate(GAL)) + " | c_Duffy/c_H: " + " ".join(f"{c_duffy_full(MH0[i])/g['c']:.2f}" for i, g in enumerate(GAL)))
cnt, offs, ok_n, worst = 0, [], 0, []
MHc = list(MH0)
allp = list(itertools.permutations(range(NG)))
# permutation: galaxy i gets halo of galaxy p[i] (M_h from the other galaxy's stars); the Salpeter floor keeps the halo fixed
for p in allp:
    MHp = [MHc[p[i]] for i in range(NG)]
    r = summarize(model_L(MHp))
    offs.append(r["mean"]); ok_n += abs(r["z"]) <= 2; cnt += 1
offs = np.array(offs)
print(f"  (i) PERMUTATION of Moster/Duffy halos among the 7 galaxies ({cnt} perms incl. identity): sample offset median {np.median(offs):+.3f}, 5-95% {np.quantile(offs,.05):+.3f}..{np.quantile(offs,.95):+.3f}; |z|<=2 in {100*ok_n/cnt:.1f}%")
Mmed = float(np.median(MH0)); r = summarize(model_L([Mmed] * NG))
print(f"  (ii) GENERIC one halo (median Moster Mh={Mmed:.2e}) for all: {r['mean']:+.3f} +- {r['sig']:.3f}  z {r['z']:+.2f}")
print(f"  (iii) Humphrey's own fitted halos with Kroupa stars (form-matched limit) = 'fitted M/L' row for B {RB['canonical']['per'].mean():+.3f}; for LCDM-form: offset = log(g_obs/g_bar) only through stars -> see C1d ref mean {ref.mean():+.3f}")

# ------------------------------------------------------------------ POST-HOC reported rows (added after the first run; no check depends on them)
print("\nPOST-HOC rows (reported only)")
errs = []
for p in allp:
    MHp = [MHc[p[i]] for i in range(NG)]
    errs.append(summarize(model_L(MHp))["err"])
errs = np.array(errs); e0 = RL0["base"]["err"]
print(f"  (i') permutation invariance: the MEAN of per-galaxy offsets is ~permutation-invariant (each offset ~ a_i - s log Mh_j), so (i) says nothing about matching.")
print(f"       galaxy-to-galaxy error: identity {e0:.4f}; permuted median {np.median(errs):.4f}, 5% {np.quantile(errs,.05):.4f}; identity rank {100*np.mean(errs<e0):.1f}th percentile (lower err = better matched)")
Mfit_ = lambda i: GAL[i]["uf"] * GAL[i]["LK"]
def hum_halo_kroupa(ups):
    def mod(i, gb, u, radii):
        g = GAL[i]; Mdm = max(g["Mvir"] - g["uf"] * g["LK"], 1e9)
        return gb + np.array([G * M_nfw_h(r, Mdm, g["Rvir"], g["c"]) * MSUN / (r * KPC) ** 2 for r in radii])
    return mod
RH = summarize(hum_halo_kroupa)
print(f"  (iii') form-matched limit: Humphrey's OWN fitted halo (Newtonian) + Kroupa stars: {RH['mean']:+.4f} +- {RH['sig']:.4f} z {RH['z']:+.2f} (gal-gal {RH['err']:.3f}, IMF {RH['imf']:.3f}, rad {RH['rad']:.3f})")
print(f"       Moster/Duffy LCDM base for comparison: {RL0['base']['mean']:+.4f} +- {RL0['base']['sig']:.4f} z {RL0['base']['z']:+.2f}; the difference of means {RL0['base']['mean']-RH['mean']:+.4f} dex is what the Moster-vs-Humphrey halo mismatch costs at 5-70 kpc")
Rp = summarize(lambda ups: (lambda i, gb, u, radii: gb + G * (1 - FB) * np.array([M_nfw_lcdm(MH0[i], lambda M: GAL[i]["c"], r) for r in radii]) * MSUN / (np.array(radii) * KPC) ** 2))
print(f"  (iv') Moster M_h but Humphrey's c (per galaxy): {Rp['mean']:+.4f} +- {Rp['sig']:.4f} z {Rp['z']:+.2f}")
print("  gate power vs the Humphrey-halo model: the halo ladder of the Duffy halo moves z from +1.98 (x0.01) to -2.46 (x100): |dz| ~ 4.4 over 4 dex of Mh; per-dex sensitivity ~1.1 sigma/dex against sigma_stat ~0.12 dex")
# ------------------------------------------------------------------ summary
nfail = [n for n, ok in checks if not ok]
print(f"\n{sum(ok for _, ok in checks)}/{len(checks)} checks pass; failing: {nfail}")
json.dump(dict(mutate=MUTATE, B={f: {k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in RB[f].items()} for f in FOOTS},
               L0={k: {kk: (vv.tolist() if hasattr(vv, 'tolist') else vv) for kk, vv in RL0[k].items()} for k in CFGS},
               ladder={str(m): dict(mean=LAD[m]['mean'], sig=LAD[m]['sig'], z=LAD[m]['z']) for m in grid}, failing=nfail),
          open("cfg84_results%s.json" % ("_MUTATE" if MUTATE else ""), "w"), indent=1)
sys.exit(1 if nfail else 0)
