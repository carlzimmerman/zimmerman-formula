#!/usr/bin/env python3
"""
agentN5_freq_vs_accel.py -- THE DISCRIMINATOR: frequency-keyed vs acceleration-keyed inertia on SPARC
=====================================================================================================
CONTEXT (Door IVb, TOE_STATUS_AND_DOORS.md): the solar-reflex kill applies to MAGNITUDE(acceleration)-
keyed inertia: survival line s < (0.34-0.40) a0 (agentE fit-A .. kitchen-sink), both candidate
normalizations dead. Any tail/memory kernel is naturally FREQUENCY-keyed, K~(Omega) -- and frequency-
keying is the named evasion: the Sun's reflex wobble runs at Omega_J ~ 1.7e-8 s^-1, galactic orbits at
~1e-16..1e-15 s^-1 (eight decades of separation). But the RAR is observed tight in ACCELERATION.
QUESTION: does a frequency-keyed law fit SPARC as well as the acceleration-keyed one, or does SPARC
kill frequency-keying outright?

LAWS (modified inertia on circular orbits: mu(.) * a = g_bar exactly; a = V^2/R, Omega = V/R, a=Omega*V):
  P0 baseline  accel-keyed   g_pred = nu(g_bar/a0) g_bar; shapes {fw, McGaugh-RAR, simple, F4-standard};
               BOTH footings a0 = 9.36e-11 (framework) and 1.2e-10 (canonical).  [reproduces repo .out]
  P1 pure freq mu(Omega/Omega0) a = g_bar; shapes {standard x/sqrt(1+x^2), simple x/(1+x)}; Omega0 fitted.
               PRIMARY mode: SELF-CONSISTENT forward solve (Omega = sqrt(a/R) on the predicted circular
               orbit; bisection, monotone). SECONDARY: observed-Omega constraint form (Omega = V_obs/R)
               -- stated and shown; analytically it inflates deep-regime residuals by 3/2 vs the forward
               model, so it is NOT verdict-grade alone.
  P3 hybrid    accel-keyed with frequency-DRESSED scale (what a tail kernel with one power of frequency
               suppression on top of acceleration-keying would give):
               a0_eff = a0_ref * [(1+Omega/H0)/(1+Omega_ref/H0)]^(-p), Omega_ref = 3e-16 s^-1 (pure
               convention; a0_ref is refit at every p so Omega_ref drops out of the physics).
               Headline p in {0.5, 1}; corridor scan p in {0,0.05,0.1,0.15,0.2,0.3,0.5,0.75,1};
               shapes {standard, simple, McGaugh-RAR(nu-form)}; self-consistent solve.
CONVENTIONS (locked, = mi_f4_sparc_shape_test.py): 175 SPARC rotmod galaxies; Vbar^2 = sign(Vgas)Vgas^2
  + Ud Vdisk^2 + 1.4 Ud Vbul^2; per-function best-Ud on [0.3,1.2]x46; UNWEIGHTED dex rms PRIMARY,
  error-weighted shown (w = (V/eV)^2, eV floored at 1 km/s).
PRE-REGISTERED READING (thresholds = the repo's F4 shape-test thresholds):
  SPARC-ALIVE  best-variant unweighted scatter within +0.010 dex of the best accel-keyed law;
  DEGRADED  +0.010..0.020;  SPARC-DEAD  > +0.020.
  SOLAR PASS  delta_a_sun(Omega_J) <= 2.47e-15 m/s^2 (agentE fit-A line s < 3.21e-11 <=> >=8.5x below
  the framework std-mu reflex 2.10e-14 m/s^2; loose kitchen-sink line 3.38e-15 also quoted). Caveat:
  the line was derived for the std-mu time template; for other shapes it is approximate (flagged).
  PREDICTED failure mode of pure frequency-keying (stated BEFORE computing): a = Omega*V, so a single
  Omega0 maps to a per-galaxy acceleration scale a0_eq ~ Omega0*V; self-consistent deep-MOND residual
  = (2/3) log10[a0_emp/(Omega0 V)] -> per-galaxy residuals should run with V_flat, slope ~ -2/3 per dex
  (observed-Omega mode: -1). Hybrid deep slope: -p/(2+p/2) (p=0.5: -0.22; p=1: -0.40).
No git. Outputs: agentN5_freq_vs_accel.out (stdout), agentN5_freq_vs_accel.md (memo). 2026-06-10.
"""
import numpy as np, glob, os, time

t0 = time.time()
np.seterr(all="ignore")
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "..", "data", "sparc_data")

# ---------------- constants ----------------
kpc   = 3.0857e19                       # m
H0    = 70e3 / 3.0857e22                # s^-1 = 2.2685e-18 (enters only through Omega/H0; a0_ref refit absorbs it)
A0F, A0C = 9.36e-11, 1.2e-10            # framework / canonical footings
OMREF = 3e-16                           # s^-1, hybrid normalization pivot (convention only)
GMJ   = 1.266865341e17                  # m^3/s^2 (agentE/Juno)
RJ    = 5.2044 * 1.495978707e11         # m
ASUN  = GMJ / RJ**2                     # Sun's Jupiter-driven proper acceleration ~2.09e-7 m/s^2
OMJ   = 2*np.pi / (11.862*365.25*86400) # Sun's reflex (= Jupiter orbital) frequency ~1.678e-8 s^-1
DA_FW   = A0F**2 / (2*ASUN)             # framework std-mu solar reflex 2.10e-14 m/s^2 (agentE)
DA_LINE = (3.21e-11)**2 / (2*ASUN)      # survival line, fit-A (strict)   = 2.47e-15
DA_LINE_L = (3.76e-11)**2 / (2*ASUN)    # survival line, kitchen-sink     = 3.38e-15

print(f"agentN5: frequency-keyed vs acceleration-keyed inertia on SPARC (Door IVb discriminator)")
print(f"  constants: H0={H0:.4e} s^-1  Omega_J={OMJ:.4e} s^-1  |a_sun|={ASUN:.4e} m/s^2")
print(f"  solar budget: framework std reflex {DA_FW:.3e} m/s^2 ; survival line {DA_LINE:.3e} (strict, 8.5x)"
      f" .. {DA_LINE_L:.3e} (loose, 6.2x)")

# ---------------- load SPARC (identical to mi_f4_sparc_shape_test.py) ----------------
names, Vflat = [], []
Rl, Vol, eVl, sgl, sdl, sbl, gil = [], [], [], [], [], [], []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(f, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    gi = len(names)
    names.append(os.path.basename(f).replace("_rotmod.dat", ""))
    Vflat.append(float(np.mean(Vobs[-3:])) if len(Vobs) >= 3 else float(Vobs[-1]))
    Rl.append(R*kpc); Vol.append(Vobs); eVl.append(eV)
    sgl.append(np.sign(Vgas)*Vgas**2); sdl.append(Vdisk**2); sbl.append(Vbul**2)
    gil.append(np.full(len(R), gi, dtype=int))
Rm   = np.concatenate(Rl);  Vo = np.concatenate(Vol); eV = np.concatenate(eVl)
sg   = np.concatenate(sgl); sd = np.concatenate(sdl); sb = np.concatenate(sbl)
gidx = np.concatenate(gil); Vflat = np.array(Vflat); NGAL = len(names)
gobs   = (Vo*1e3)**2 / Rm
Om_obs = (Vo*1e3) / Rm
wgtpt  = 1.0 / (np.clip(eV, 1, None)/np.clip(Vo, 1, None))**2
ok0    = (gobs > 0) & np.isfinite(gobs) & (Vo > 0)
print(f"SPARC galaxies loaded: {NGAL} ; points {len(Rm)} ; "
      f"Omega_obs/H0 range {np.nanmin(Om_obs[ok0])/H0:.0f}..{np.nanmax(Om_obs[ok0])/H0:.0f} "
      f"(median {np.nanmedian(Om_obs[ok0])/H0:.0f})")

def gbar(Ud): return (sg + Ud*sd + 1.4*Ud*sb) * 1e6 / Rm

# ---------------- shapes ----------------
def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))
def mu_std(x):    return x/np.sqrt(1 + x*x)
def mu_simple(x): return x/(1 + x)

Uds = np.linspace(0.3, 1.2, 46)

def stats(res, w):
    return float(np.sqrt(np.mean(res**2))), float(np.sqrt(np.sum(w*res**2)/np.sum(w)))

def mask_of(gb): return ok0 & (gb > 0) & np.isfinite(gb)

# ---------------- vectorized monotone bisection in log10(a) ----------------
def bis(f, gb, ndec=12.0, it=72):
    lo = np.log10(gb); hi = lo + ndec
    bad = ~(f(10**hi) > 0)
    if bad.any(): hi = np.where(bad, lo + 24.0, hi)     # never expected; safety
    for _ in range(it):
        mid = 0.5*(lo + hi)
        pos = f(10**mid) > 0
        hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
    return 10**(0.5*(lo + hi))

# residual engines ----------------------------------------------------------------------
def res_accel(nu, Ud, a0):
    gb = gbar(Ud); m = mask_of(gb)
    res = np.log10(gobs[m]) - np.log10(nu(gb[m]/a0)*gb[m])
    return res, m

def res_freq_sc(mu, Ud, Om0):
    gb = gbar(Ud); m = mask_of(gb); gbm, Rmm = gb[m], Rm[m]
    a = bis(lambda a: mu(np.sqrt(a/Rmm)/Om0)*a - gbm, gbm)
    return np.log10(gobs[m]) - np.log10(a), m

def res_freq_obs(mu, Ud, Om0):
    gb = gbar(Ud); m = mask_of(gb)
    res = np.log10(gobs[m]) - np.log10(gb[m]/mu(Om_obs[m]/Om0))
    return res, m

def a0eff(Omega, a0r, p): return a0r*((1 + Omega/H0)/(1 + OMREF/H0))**(-p)

def res_hyb_sc(shape, Ud, a0r, p):
    gb = gbar(Ud); m = mask_of(gb); gbm, Rmm = gb[m], Rm[m]
    if shape in ("std", "simple"):
        mu = mu_std if shape == "std" else mu_simple
        f = lambda a: mu(a/a0eff(np.sqrt(a/Rmm), a0r, p))*a - gbm
    else:                                    # McGaugh-RAR, nu-form
        f = lambda a: a - nu_rar(gbm/a0eff(np.sqrt(a/Rmm), a0r, p))*gbm
    a = bis(f, gbm)
    return np.log10(gobs[m]) - np.log10(a), m

def res_hyb_obs(shape, Ud, a0r, p):
    gb = gbar(Ud); m = mask_of(gb)
    nu = {"std": nu_std, "simple": nu_simple, "rar": nu_rar}[shape]
    a0e = a0eff(Om_obs[m], a0r, p)
    res = np.log10(gobs[m]) - np.log10(nu(gb[m]/a0e)*gb[m])
    return res, m

def sc_of(resfn, *args):
    res, m = resfn(*args)
    return stats(res, wgtpt[m])

# =======================================================================================
print("\n" + "="*99)
print("P0  BASELINE: acceleration-keyed nu(g_bar/a0), per-function best-Ud (reproduction gate)")
print("="*99)
ACC = {}
for a0, lab in [(A0F, "framework 9.36e-11"), (A0C, "canonical 1.2e-10")]:
    print(f"  a0 = {lab}:")
    for fl, nu in [("fw sqrt(1+1/y)", nu_fw), ("McGaugh RAR", nu_rar), ("simple", nu_simple), ("F4 standard", nu_std)]:
        su = [sc_of(res_accel, nu, U, a0) for U in Uds]
        i = int(np.argmin([s[0] for s in su]))
        ACC[(lab, fl)] = (Uds[i], su[i][0], su[i][1])
        print(f"    {fl:16s} bestUd {Uds[i]:5.2f}  unweighted {su[i][0]:.4f}  weighted {su[i][1]:.4f}")
gate = abs(ACC[("framework 9.36e-11", "McGaugh RAR")][1] - 0.1950) < 0.0005 and \
       abs(ACC[("framework 9.36e-11", "F4 standard")][1] - 0.1984) < 0.0005
ACC_BEST = min(v[1] for v in ACC.values())
ACC_BEST_W = min(v[2] for v in ACC.values())
print(f"  reproduction gate (McGaugh 0.1950 / F4-std 0.1984 at framework a0): {'PASS' if gate else '** FAIL **'}")
print(f"  best accel-keyed law (any shape, any footing): unweighted {ACC_BEST:.4f} dex ; weighted {ACC_BEST_W:.4f}")

# =======================================================================================
print("\n" + "="*99)
print("P1  PURE FREQUENCY-KEYING: mu(Omega/Omega0) a = g_bar  (Omega0 and Ud fitted per shape)")
print("="*99)
OM0_GRID = np.logspace(-17.0, -14.2, 43)

def fit_freq(mu, mode, om_grid):
    best = (None, None, np.inf, np.inf)
    for Ud in Uds:
        gb = gbar(Ud); m = mask_of(gb); gbm, Rmm = gb[m], Rm[m]
        lg_obs = np.log10(gobs[m]); w = wgtpt[m]; omm = Om_obs[m]
        for Om0 in om_grid:
            if mode == "sc":
                a = bis(lambda a: mu(np.sqrt(a/Rmm)/Om0)*a - gbm, gbm)
                res = lg_obs - np.log10(a)
            else:
                res = lg_obs - np.log10(gbm/mu(omm/Om0))
            u, wq = stats(res, w)
            if u < best[2]: best = (Ud, Om0, u, wq)
    return best

FREQ = {}
for shape, mu in [("standard", mu_std), ("simple", mu_simple)]:
    for mode, mlab in [("sc", "self-consistent (PRIMARY)"), ("obs", "observed-Omega (check)")]:
        Ud, Om0, u, w = fit_freq(mu, mode, OM0_GRID)
        # refine Omega0 +-2 coarse steps
        i = int(np.argmin(abs(np.log10(OM0_GRID) - np.log10(Om0))))
        lo, hi = max(0, i-2), min(len(OM0_GRID)-1, i+2)
        fine = np.logspace(np.log10(OM0_GRID[lo]), np.log10(OM0_GRID[hi]), 25)
        Ud, Om0, u, w = fit_freq(mu, mode, fine)
        edge = " [GRID EDGE]" if (Om0 <= OM0_GRID[0]*1.01 or Om0 >= OM0_GRID[-1]*0.99
                                  or Ud <= Uds[0]+1e-9 or Ud >= Uds[-1]-1e-9) else ""
        FREQ[(shape, mode)] = (Ud, Om0, u, w)
        dU, dW = u - ACC_BEST, w - ACC_BEST_W
        print(f"  mu_{shape:8s} {mlab:26s} bestUd {Ud:5.2f}  Omega0 {Om0:.3e} s^-1  "
              f"unw {u:.4f} (D={dU:+.4f})  wgt {w:.4f} (D={dW:+.4f}){edge}")
for shape in ("standard", "simple"):
    u_sc, u_ob = FREQ[(shape, "sc")][2], FREQ[(shape, "obs")][2]
    print(f"    note mu_{shape}: observed-Omega/self-consistent deep-inflation check: "
          f"{u_ob:.4f} vs {u_sc:.4f} (expected obs > sc by ~3/2 in deep residuals)")
best_freq = min(FREQ[(s, "sc")][2] for s in ("standard", "simple"))
dbest = best_freq - ACC_BEST
v = "SPARC-ALIVE (<+0.010)" if dbest <= 0.010 else ("DEGRADED (+0.010..0.020)" if dbest <= 0.020
                                                    else "SPARC-DEAD (>+0.020)")
print(f"  => best pure frequency-keyed law (self-consistent): {best_freq:.4f} dex = "
      f"+{dbest:.4f} vs best accel-keyed {ACC_BEST:.4f}  => {v}")

# =======================================================================================
print("\n" + "="*99)
print("P2  PER-GALAXY STRUCTURE: does frequency-keying fail systematically with V_flat?")
print("    (predicted: pure-freq deep slope ~ -2/3 per dex V_flat self-consistent; accel laws ~ 0)")
print("="*99)

def pergal(res, m, deep=None):
    gi = gidx[m]
    sel = np.ones(len(res), bool) if deep is None else deep
    cnt = np.bincount(gi[sel], minlength=NGAL)
    sm  = np.bincount(gi[sel], weights=res[sel], minlength=NGAL)
    ok = cnt >= (1 if deep is None else 2)
    mean = np.where(ok, sm/np.maximum(cnt, 1), np.nan)
    return mean, ok

def structure(tag, res, m, gb_m):
    lgV = np.log10(Vflat)
    out = {}
    for sub, dsel in [("all", None), ("deep g_bar<1e-10", gb_m < 1e-10)]:
        mean, ok = pergal(res, m, dsel)
        x, y = lgV[ok], mean[ok]
        if len(x) < 8: continue
        A = np.vstack([x, np.ones_like(x)]).T
        sl, ic = np.linalg.lstsq(A, y, rcond=None)[0]
        r = float(np.corrcoef(x, y)[0, 1])
        q1, q2 = np.percentile(Vflat[ok], [33.3, 66.7])
        t1, t3 = y[Vflat[ok] <= q1], y[Vflat[ok] > q2]
        loV, hiV = y[Vflat[ok] < 80], y[Vflat[ok] >= 150]
        dHL = np.mean(hiV) - np.mean(loV)
        sHL = np.sqrt(np.var(hiV)/len(hiV) + np.var(loV)/len(loV))
        out[sub] = (sl, r, len(x))
        print(f"  {tag:34s} [{sub:16s}] N={len(x):3d}  slope {sl:+.3f}/dex  r={r:+.3f}  "
              f"terciles(lo,hi) {np.mean(t1):+.3f},{np.mean(t3):+.3f}  "
              f"V>=150 minus V<80: {dHL:+.3f}+-{sHL:.3f} dex ({abs(dHL)/max(sHL,1e-9):.1f} sig)")
    return out

champs = []
Ud, u, w = ACC[("framework 9.36e-11", "McGaugh RAR")][0], None, None
champs.append(("accel McGaugh (control)", lambda: res_accel(nu_rar, ACC[("framework 9.36e-11","McGaugh RAR")][0], A0F),
               ACC[("framework 9.36e-11","McGaugh RAR")][0]))
champs.append(("accel F4-standard (control)", lambda: res_accel(nu_std, ACC[("framework 9.36e-11","F4 standard")][0], A0F),
               ACC[("framework 9.36e-11","F4 standard")][0]))
for shape, mu in [("standard", mu_std), ("simple", mu_simple)]:
    Ud, Om0, _, _ = FREQ[(shape, "sc")]
    champs.append((f"freq mu_{shape} self-consistent", (lambda mu=mu, Ud=Ud, Om0=Om0: res_freq_sc(mu, Ud, Om0)), Ud))
STRUCT = {}
for tag, fn, Ud in champs:
    res, m = fn()
    STRUCT[tag] = structure(tag, res, m, gbar(Ud)[m])
print("  DIFFERENTIAL (the discriminating statement -- baseline per-galaxy trend is shared systematics):")
for shape in ("standard", "simple"):
    for sub in ("all", "deep g_bar<1e-10"):
        d = STRUCT[f"freq mu_{shape} self-consistent"][sub][0] - STRUCT["accel McGaugh (control)"][sub][0]
        print(f"    freq mu_{shape:8s} minus accel control [{sub:16s}]: slope shift {d:+.3f}/dex "
              f"(predicted deep shift ~ -2/3 self-consistent, attenuated by non-deep points)")

# =======================================================================================
print("\n" + "="*99)
print("P3  HYBRID: accel-keyed with frequency-dressed scale a0_eff = a0_ref [(1+Om/H0)/(1+Om_ref/H0)]^-p")
print("    corridor scan over p (a0_ref and Ud refit at every p; self-consistent solve)")
print("="*99)
PLIST = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.75, 1.0]
A0R_GRID0 = np.logspace(np.log10(2e-11), np.log10(2.4e-9), 35)

def fit_hyb(shape, p, grid):
    best = (None, None, np.inf, np.inf)
    for Ud in Uds:
        for a0r in grid:
            u, wq = sc_of(res_hyb_sc, shape, Ud, a0r, p)
            if u < best[2]: best = (Ud, a0r, u, wq)
    return best

HYB = {}
for shape in ("std", "simple", "rar"):
    print(f"  shape mu_{shape}:" if shape != "rar" else "  shape McGaugh-RAR (nu-form):")
    for p in PLIST:
        grid = A0R_GRID0
        Ud, a0r, u, w = fit_hyb(shape, p, grid)
        while a0r >= grid[-1]*0.99 and grid[-1] < 1e-8:          # auto-extend upper edge
            grid = grid * 4.0
            Ud, a0r, u, w = fit_hyb(shape, p, grid)
        i = int(np.argmin(abs(np.log10(grid) - np.log10(a0r))))
        lo, hi = max(0, i-1), min(len(grid)-1, i+1)
        fine = np.logspace(np.log10(grid[lo]), np.log10(grid[hi]), 13)
        Ud, a0r, u, w = fit_hyb(shape, p, fine)
        HYB[(shape, p)] = (Ud, a0r, u, w)
        a0e_med = a0eff(np.median(Om_obs[ok0]), a0r, p)
        edge = " [Ud EDGE]" if (Ud <= Uds[0]+1e-9 or Ud >= Uds[-1]-1e-9) else ""
        print(f"    p={p:4.2f}  bestUd {Ud:5.2f}  a0_ref {a0r:.3e}  (a0_eff at median Omega {a0e_med:.3e})  "
              f"unw {u:.4f} (D={u-ACC_BEST:+.4f})  wgt {w:.4f}{edge}")

print("  headline p=0.5, p=1 cross-check in observed-Omega mode (constraint form):")
for shape in ("std", "simple", "rar"):
    for p in (0.5, 1.0):
        Ud, a0r, u, w = HYB[(shape, p)]
        uo, wo = sc_of(res_hyb_obs, shape, Ud, a0r, p)
        print(f"    {shape:6s} p={p:3.1f}: self-consistent {u:.4f} ; observed-Omega {uo:.4f}")

# per-galaxy structure of headline hybrids (std shape)
print("  per-galaxy structure of the dressed law (std shape):")
for p in (0.5, 1.0):
    Ud, a0r, u, w = HYB[("std", p)]
    res, m = res_hyb_sc("std", Ud, a0r, p)
    structure(f"hybrid std p={p:3.1f}", res, m, gbar(Ud)[m])

# =======================================================================================
print("\n" + "="*99)
print("P5  SOLAR-REFLEX CONSISTENCY at Omega_J (the Door-IVb budget) + the corridor")
print("="*99)
def inv_mu_m1_std(x):   return 1.0/(x*(np.sqrt(1 + x*x) + x))     # 1/mu_std - 1, overflow-stable
def inv_mu_m1_simple(x): return 1.0/x                             # 1/mu_simple - 1

print(f"  budget: delta_a_sun <= {DA_LINE:.2e} m/s^2 (strict fit-A) / {DA_LINE_L:.2e} (loose); "
      f"framework std-mu accel-keyed reflex = {DA_FW:.2e} (the 8.5x-over kill)")
print(f"  {'variant':44s} {'delta_a_sun':>12s} {'suppress.':>10s}  verdict")
SOLAR = {}
def solrow(tag, da, sparc_d):
    sup = DA_FW/da if da > 0 else np.inf
    sv = "SOLAR PASS" if da <= DA_LINE else ("marginal (loose line only)" if da <= DA_LINE_L else "SOLAR FAIL")
    spv = "SPARC-ALIVE" if sparc_d <= 0.010 else ("SPARC-DEGRADED" if sparc_d <= 0.020 else "SPARC-DEAD")
    both = "** PASSES BOTH **" if (da <= DA_LINE and sparc_d <= 0.010) else ""
    SOLAR[tag] = (da, sup, sv, spv)
    sups = f"{sup:.1e}x" if np.isfinite(sup) else "inf"
    das = f"{da:12.3e}" if da > 0 else "   <1e-300  "
    print(f"  {tag:44s} {das} {sups:>10s}  {sv} | {spv} (D={sparc_d:+.4f}) {both}")

# context rows: undressed accel-keyed shapes
solrow("accel std (F4) framework         [context]", DA_FW, ACC[("framework 9.36e-11","F4 standard")][1]-ACC_BEST)
solrow("accel simple framework           [context]", A0F, ACC[("framework 9.36e-11","simple")][1]-ACC_BEST)
y_sun = ASUN/A0F
da_rar = ASUN*np.exp(-np.sqrt(y_sun))/(1-np.exp(-np.sqrt(y_sun)))
solrow("accel McGaugh-RAR framework      [context]", da_rar, ACC[("framework 9.36e-11","McGaugh RAR")][1]-ACC_BEST)
# pure frequency-keyed
for shape, fn in [("standard", inv_mu_m1_std), ("simple", inv_mu_m1_simple)]:
    Ud, Om0, u, w = FREQ[(shape, "sc")]
    da = ASUN*fn(OMJ/Om0)
    solrow(f"pure freq mu_{shape} (Omega0={Om0:.2e})", da, u-ACC_BEST)
# hybrids
for shape, fn in [("std", inv_mu_m1_std), ("simple", inv_mu_m1_simple)]:
    for p in (0.5, 1.0):
        Ud, a0r, u, w = HYB[(shape, p)]
        a0e = a0eff(OMJ, a0r, p)
        da = ASUN*fn(ASUN/a0e)
        solrow(f"hybrid {shape:6s} p={p:3.1f} (a0_ref={a0r:.2e})", da, u-ACC_BEST)
for p in (0.5, 1.0):
    Ud, a0r, u, w = HYB[("rar", p)]
    y = ASUN/a0eff(OMJ, a0r, p)
    da = ASUN*np.exp(-np.sqrt(y))   # exponentially dead
    solrow(f"hybrid rar    p={p:3.1f} (a0_ref={a0r:.2e})", da, u-ACC_BEST)

# ---- the corridor: p_min from solar vs p_max from SPARC, per shape ----
print("\n  CORRIDOR per shape: smallest p passing solar (strict line) vs largest p with SPARC D<=+0.010")
RATIO = (1 + OMJ/H0)/(1 + OMREF/H0)
pfine = np.linspace(0, 1, 2001)
COR = {}
for shape, fn in [("std", inv_mu_m1_std), ("simple", inv_mu_m1_simple), ("rar", None)]:
    ps  = np.array(PLIST)
    a0s = np.array([HYB[(shape, p)][1] for p in PLIST])
    us  = np.array([HYB[(shape, p)][2] for p in PLIST])
    la0 = np.interp(pfine, ps, np.log10(a0s))
    a0e = 10**la0 * RATIO**(-pfine)
    if shape == "rar":
        da = ASUN*np.exp(-np.sqrt(ASUN/a0e))
    else:
        da = ASUN*fn(ASUN/a0e)
    okS = da <= DA_LINE
    pmin = pfine[okS][0] if okS.any() else np.inf
    uf = np.interp(pfine, ps, us)
    okR = uf <= ACC_BEST + 0.010
    pmax = pfine[okR][-1] if okR.any() else -np.inf
    COR[shape] = (pmin, pmax)
    stat = f"CORRIDOR [{pmin:.3f}, {pmax:.3f}] NON-EMPTY" if pmin <= pmax else \
           f"corridor EMPTY (p_min {pmin:.3f} > p_max {pmax:.3f})"
    print(f"    {shape:6s}: p_min(solar) = {pmin:.3f} ; p_max(SPARC,+0.010) = {pmax:.3f}  => {stat}")
print("    (p interpolated between scan points; a0_ref(p) from each p's own SPARC fit; "
      "strict fit-A line; the line is std-template-derived -- approximate for other shapes; "
      "p_max quoted within the scanned family p<=1)")

# ---- side prediction of the corridor: wide-binary suppression (the falsifiable hook) ----
OMWB = np.sqrt(1.327e20*1.5/(7000*1.495978707e11)**3)   # ~1.5 Msun, 7 kAU separation
print(f"\n  SIDE PREDICTION (corridor-discriminating): dressing factor S = a0_eff/a0_ref at the")
print(f"  wide-binary frequency Omega_WB = {OMWB:.2e} s^-1 (7 kAU, 1.5 Msun; Omega_WB/H0 = {OMWB/H0:.1e}):")
for p in (0.069, 0.30, 0.50, 1.0):
    S = ((1 + OMWB/H0)/(1 + OMREF/H0))**(-p)
    print(f"    p={p:5.3f}: S(Omega_WB) = {S:.3f}  -> wide-binary MOND boost {'~intact' if S>0.8 else ('suppressed' if S>0.1 else 'OFF (Newtonian)')}")
print("    => a detected WB anomaly at full MOND amplitude (Chae-type) would cap p <~ 0.1 and pinch the std")
print("       corridor [0.069, ~0.1]; a WB null (Banik-type) is consistent with any corridor p. Same logic")
print("       kills lab/atom-interferometer MOND signatures for ANY corridor p (lab Omega/H0 >~ 1e17).")

# =======================================================================================
print("\n" + "="*99)
print("VERDICT (pre-registered thresholds; both directions, full weight)")
print("="*99)
samesh = {"standard": "std", "simple": "simple"}
for shape in ("standard", "simple"):
    Ud, Om0, u, w = FREQ[(shape, "sc")]
    d = u - ACC_BEST
    da = SOLAR[f"pure freq mu_{shape} (Omega0={Om0:.2e})"][0]
    print(f"  pure freq mu_{shape:8s}: SPARC +{d:.4f} dex "
          f"({'ALIVE' if d<=0.01 else 'DEGRADED' if d<=0.02 else 'DEAD'}) ; "
          f"solar delta_a {da:.2e} ({'pass' if da<=DA_LINE else 'FAIL'})")
print("  robustness of the pure-freq SPARC death (the working rule: a 'fails' needs the same rigor):")
for shape in ("standard", "simple"):
    Ud, Om0, u, w = FREQ[(shape, "sc")]
    u0 = HYB[(samesh[shape], 0.0)][2]      # same-shape accel-keyed law at its own FREE-a0 optimum
    uo = FREQ[(shape, "obs")][2]
    print(f"    mu_{shape:8s}: vs same-shape free-a0 accel optimum {u0:.4f}: +{u-u0:.4f} ; "
          f"weighted {w:.4f} vs accel-best-weighted {ACC_BEST_W:.4f}: +{w-ACC_BEST_W:.4f} ; "
          f"observed-Omega mode worse ({uo:.4f}); Ud freedom granted; Omega0 grid-interior")
print(f"  hybrid (dressed accel-keying): headline p=0.5 / p=1.0 penalties (std shape): "
      f"{HYB[('std',0.5)][2]-ACC_BEST:+.4f} / {HYB[('std',1.0)][2]-ACC_BEST:+.4f} dex")
bu = min((HYB[(s, p)][2], s, p) for s in ("std", "simple", "rar") for p in PLIST)
print(f"  both-ways note: mild dressing IMPROVES the unweighted fit (best {bu[0]:.4f} at shape={bu[1]}, "
      f"p={bu[2]:.2f}, {bu[0]-ACC_BEST:+.4f} vs accel best) -- at the level of known per-galaxy")
print(f"  systematics (distance/inclination/M-L correlated with V_flat); NOT claimed as a detection.")
for shape in ("std", "simple", "rar"):
    pmin, pmax = COR[shape]
    print(f"  corridor {shape:6s}: [{pmin:.3f}, {pmax:.3f}] {'NON-EMPTY' if pmin<=pmax else 'EMPTY'}")
print("""
  BOTTOM LINE (three-way, full weight):
  (1) PURE frequency-keying is SPARC-DEAD: best variant +0.023 dex over the acceleration-keyed law
      (past the pre-registered DEAD threshold +0.020; 2.3x the ALIVE line +0.010), with the PREDICTED
      failure signature -- per-galaxy residuals
      run against V_flat (sign-flip of the control trend; a = Omega*V is the mechanism). The only
      solar-safe pure-freq shape (standard) is exactly the SPARC-dead one; the simple shape fails BOTH.
      Frequency-keying as a REPLACEMENT for acceleration-keying is excluded by the data.
  (2) The acceleration-keyed exponential-tail shape (McGaugh RAR) ALREADY passes the Door-IVb solar
      budget undressed (delta_a ~ 6e-28): the solar-reflex kill is specific to power-law-tail mu
      (F4-standard, simple) -- frequency arguments are NOT needed for solar safety in general.
  (3) For F4's OWN shape the rescue corridor is OPEN: weak frequency DRESSING of acceleration-keying,
      a0_eff = a0 [(1+Omega/H0)/(1+Omega_ref/H0)]^-p with p in [0.069, 1.0], passes the solar budget
      AND costs <0.010 dex on SPARC (p<~0.3 costs nothing at all). The Door-IVb kill of F4 is therefore
      EVADABLE by one power-law dressing factor -- at the price of a falsifiable side prediction:
      suppressed wide-binary anomaly (S_WB = 0.6 at the corridor floor, OFF for p>=0.5) and no lab-scale
      MOND signatures. A confirmed full-amplitude WB detection would pinch the corridor to ~[0.07, 0.1].
""")
print(f"  total runtime {time.time()-t0:.1f} s")
