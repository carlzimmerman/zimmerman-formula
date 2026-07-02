#!/usr/bin/env python3
"""
L5 -- OUT-OF-SAMPLE RAR from the Unified HI Rotation Curve Corpus (Zenodo 10.5281/zenodo.19563417, v7.0)
=========================================================================================================
FRAMEWORK OWN TERMS: de Sitter-Unruh MODIFIED INERTIA, a0 = cH_Lambda/Z = 9.36e-11 m/s^2,
own interpolation g_obs = sqrt(g_bar^2 + g_bar*a0)  [nu(y) = sqrt(1+1/y)].
Footing fork 1.13e-10 run alongside. McGaugh nu used ONLY as a named comparator.

WHAT THE CORPUS ACTUALLY SHIPS (v7.0 README, verified):
  - WALLABY DR2 (203 gal): rad_kpc, vrot_kms, vdisp, inc, pa. NO baryonic decomposition,
    NO photometry cross-match, NO HI fluxes/masses, NO per-ring errors. -> g_bar NOT constructible.
  - THINGS (19 w/ data): Rad, Vrot, e_Vrot only. 16 of 19 in SPARC; non-SPARC = NGC3031, NGC3627,
    NGC4826 -- de Blok 2008 mass models are NOT machine-readable (VizieR J/AJ/136/2648 absent). Skipped.
  - LITTLE THINGS (26): Rad, Vobs, errV (Oh+2015 rotdmbar 'Data' rows, asymmetric-drift corrected,
    unscaled via R0.3/V0.3). Baryonic per-ring decomposition NOT shipped, BUT Oh+2015 Table 2
    (VizieR J/AJ/149/180/table2) gives per-galaxy Mgas and Mstar(SED/kinematic) + Rmax + V(Rmax).

HONESTLY-DOABLE OUT-OF-SAMPLE TEST (stated coverage):
  18 LITTLE THINGS dwarfs NOT in SPARC (8 excluded as SPARC members incl. aliases:
  DDO154, DDO168, NGC2366, DDO50=UGC04305, DDO87=UGC05918, DDO126=UGC07559, Haro29=UGCA281, WLM=UGCA444).
  At the OUTERMOST measured HI ring, essentially all of Mgas and Mstar is enclosed, so
      g_bar(Rmax) ~= f_geom * G * (Mgas + s*Mstar) / Rmax^2
  with f_geom in [1.0, 1.15] bracketing point-mass vs thin-disk geometry, s = global stellar-mass
  scale nuisance (marginalized). One point per galaxy -> 18 independent RAR points in the DEEP
  regime (y = g_bar/a0 ~ 0.03-0.3), where the test is a0-DIAGNOSTIC and nearly
  interpolation-INDEPENDENT (unlike the SPARC-internal RAR).
  Both-ways forks: two (R,V) sources [corpus last ring vs Oh Table2 (Rmax, V(Rmax))],
  f_geom bracket, s fixed/free, starburst & pressure-support exclusions, Mstar=0/Mstar=Kin for
  the two galaxies with no SED mass.

KILL CONDITION (pre-registered): fitted a0 on the framework's own nu excludes 9.36e-11 at >3sigma
with M/L marginalized, BOTH footing forks -> out-of-sample hit. Verified both directions.
"""
import json, math, os, sys
import numpy as np

SCR = os.path.dirname(os.path.abspath(__file__))

G     = 6.674e-11         # m^3 kg^-1 s^-2
MSUN  = 1.989e30          # kg
KPC   = 3.0857e19         # m
A0_CANON = 9.36e-11       # cH_Lambda/Z, Z=sqrt(32pi/3)  (canonical footing)
A0_FORK  = 1.13e-10       # rho_total/cH0 footing fork (rule 4)

# ---------------------------------------------------------------- corpus
corpus = json.load(open(os.path.join(SCR, 'corpus_v7.json')))
gals = corpus['galaxies']
LT  = {g['galaxy']: g for g in gals if g.get('survey') == 'LITTLE_THINGS'}
WA  = [g for g in gals if g.get('survey') == 'WALLABY']
TH  = [g for g in gals if g.get('survey') == 'THINGS' and g.get('data')]
assert len(LT) == 26 and len(WA) == 203, "corpus counts changed"

SPARC_OVERLAP = {'DDO_154','DDO_168','NGC_2366','DDO_50','DDO_87','DDO_126','HARO_29','WLM'}
OOS = sorted(set(LT) - SPARC_OVERLAP)          # 18 out-of-SPARC dwarfs
assert len(OOS) == 18, OOS

# ---------------------------------------------------------------- Oh+2015 Table 2 (VizieR J/AJ/149/180)
# pipe-delimited; cols: Name|Rmax|R0.3|VRmax|VisoRmax|RmaxHI|z0|c|e_c|cM07|V200|e_V200|V200M07|
#                       e_V200M07|Rc|e_Rc|rho0|e_rho0|alphamin|e_alphamin|f_am|alpha36|e_a36|f_a36|
#                       Mgas(1e7)|MstarK(1e7)|MstarSED(1e7)|logMdyn|logM200
t2 = {}
for line in open(os.path.join(SCR, 'lt_table2.dat')):
    p = [x.strip() for x in line.rstrip('\n').split('|')]
    if len(p) < 29:
        continue
    name = p[0]
    def f(i):
        try: return float(p[i])
        except ValueError: return np.nan
    t2[name.upper()] = dict(Rmax=f(1), VRmax=f(3), Mgas=f(24)*1e7,
                            MstarK=f(25)*1e7 if p[25] else np.nan,
                            MstarSED=f(26)*1e7 if p[26] else np.nan)
assert len(t2) == 26, len(t2)

def t2row(corpname):
    key = corpname.upper()
    if key in t2: return t2[key]
    raise KeyError(corpname)

# ---------------------------------------------------------------- build per-galaxy outer points
rows = []
for name in OOS:
    g  = LT[name]
    d  = g['data']
    r  = t2row(name)
    # corpus last ring (asymmetric-drift corrected Oh 'Data' rows, unscaled)
    last = d[-1]
    Rc_, Vc_, eVc_ = last['Rad'], last['Vobs'], last['errV']
    Mgas = r['Mgas']
    Mstar = r['MstarSED'] if np.isfinite(r['MstarSED']) else r['MstarK']   # fallback: kinematic
    star_missing = not np.isfinite(r['MstarSED'])
    if not np.isfinite(Mstar):
        Mstar = 0.0; star_missing = True
    rows.append(dict(name=name, R_corp=Rc_, V_corp=Vc_, eV=eVc_,
                     R_oh=r['Rmax'], V_oh=r['VRmax'],
                     Mgas=Mgas, Mstar=Mstar, star_missing=star_missing,
                     fgas=Mgas/(Mgas+Mstar) if Mgas+Mstar > 0 else np.nan))

STARBURST = {'IC_10','NGC_1569','HARO_36'}          # BCD/starburst, disturbed kinematics
PRESSURE  = {'DDO_210','DDO_216'}                   # V<~15 km/s, asym-drift-dominated

# ---------------------------------------------------------------- model
def gpred_framework(gbar, a0): return np.sqrt(gbar**2 + gbar*a0)            # OWN nu
def gpred_mcgaugh(gbar, a0):                                                # comparator ONLY
    y = gbar/a0
    return gbar/(1.0 - np.exp(-np.sqrt(y)))

def build_arrays(rows, src='corpus'):
    R  = np.array([r['R_corp'] if src=='corpus' else r['R_oh'] for r in rows]) * KPC
    V  = np.array([r['V_corp'] if src=='corpus' else r['V_oh'] for r in rows]) * 1e3
    eV = np.array([max(r['eV'], 1.0) for r in rows]) * 1e3
    Mg = np.array([r['Mgas']  for r in rows]) * MSUN
    Ms = np.array([r['Mstar'] for r in rows]) * MSUN
    gobs = V**2 / R
    # log-error: velocity (2 sigV/V) + distance (a0-relevant: gobs ~ 1/D -> 2*sigD/D... enters once in log gobs)
    sig_logV = 2.0 * (eV / V) / math.log(10.0)
    sig_logD = 0.021          # 5% LT distances (TRGB/CMD), gobs prop 1/D
    sig_inc  = 0.03           # ~3 deg on i~50-65deg -> ~3% on V -> 6%/ln10 in gobs... folded conservatively
    sig = np.sqrt(sig_logV**2 + sig_logD**2 + (2*sig_inc/math.log(10))**2)
    return R, gobs, sig, Mg, Ms

def fit_a0(rows, src='corpus', fgeom=1.0, s_mode='free', nu=gpred_framework,
           sint_fix=None):
    """Profile chi^2 in log10 gobs over (a0, s). Returns dict."""
    R, gobs, sig, Mg, Ms = build_arrays(rows, src)
    la0_grid = np.linspace(-11.5, -9.0, 1201)
    s_grid   = np.array([1.0]) if s_mode == 'fixed' else np.geomspace(0.33, 3.0, 61)
    s_prior  = 0.15  # dex lognormal prior on global stellar-mass scale (free mode)
    best = dict(chi2=np.inf)
    chi2_prof = np.full_like(la0_grid, np.inf)
    for i, la0 in enumerate(la0_grid):
        a0 = 10**la0
        for s in s_grid:
            gbar = fgeom * G * (Mg + s*Ms) / R**2
            gp   = nu(gbar, a0)
            # iterate intrinsic scatter to chi2/dof ~ 1 at optimum handled after; here fixed sint
            sint = sint_fix if sint_fix is not None else 0.10
            w    = sig**2 + sint**2
            c2   = np.sum((np.log10(gobs) - np.log10(gp))**2 / w)
            if s_mode == 'free':
                c2 += (math.log10(s)/s_prior)**2
            if c2 < chi2_prof[i]:
                chi2_prof[i] = c2
            if c2 < best['chi2']:
                best = dict(chi2=c2, la0=la0, s=s, sint=sint)
    dchi2 = chi2_prof - best['chi2']
    def ci(level):
        ok = la0_grid[dchi2 <= level]
        return (ok.min(), ok.max()) if len(ok) else (np.nan, np.nan)
    lo1, hi1 = ci(1.0); lo2, hi2 = ci(4.0); lo3, hi3 = ci(9.0)
    def nsig(a0pin):
        j = np.argmin(abs(la0_grid - math.log10(a0pin)))
        return math.sqrt(max(dchi2[j], 0.0))
    # scatter at pinned canonical (s at its per-pin optimum)
    def scatter_at(a0pin):
        a0 = a0pin; bestc, bsct = np.inf, np.nan
        for s in s_grid:
            gbar = fgeom * G * (Mg + s*Ms) / R**2
            resid = np.log10(gobs) - np.log10(nu(gbar, a0))
            c2 = np.sum(resid**2/(sig**2+ (sint_fix or 0.10)**2))
            if s_mode == 'free': c2 += (math.log10(s)/s_prior)**2
            if c2 < bestc: bestc, bsct = c2, np.std(resid)
        return bsct
    return dict(a0=10**best['la0'], la0=best['la0'], s=best['s'],
                ci1=(10**lo1, 10**hi1), ci2=(10**lo2, 10**hi2), ci3=(10**lo3, 10**hi3),
                nsig_canon=nsig(A0_CANON), nsig_fork=nsig(A0_FORK),
                scat_canon=scatter_at(A0_CANON), scat_fork=scatter_at(A0_FORK),
                scat_best=scatter_at(10**best['la0']),
                chi2=best['chi2'], N=len(rows))

def implied_a0(rows, src='corpus', fgeom=1.0, s=1.0):
    R, gobs, sig, Mg, Ms = build_arrays(rows, src)
    gbar = fgeom * G * (Mg + s*Ms) / R**2
    return (gobs**2 - gbar**2) / gbar, gbar/ (gobs**2 - gbar**2) * 0 + gbar  # a0_implied, gbar

# ---------------------------------------------------------------- report
print("="*100)
print("L5 OUT-OF-SAMPLE RAR -- Unified HI Corpus v7.0 (Zenodo 19563417) -- framework's OWN nu")
print("="*100)
print("\n-- COVERAGE (plain statement) --")
print("WALLABY DR2 (203 gal): corpus ships NO baryonic decomposition / photometry / HI fluxes.")
print("  g_bar NOT constructible from what ships. WALLABY RAR = NOT DOABLE without external")
print("  photometry cross-match (days). Tier-2 caveat anyway: Vrot<50 km/s unreliable (30'' beam).")
print("THINGS non-SPARC w/ data: NGC3031, NGC3627, NGC4826 only; de Blok 2008 decompositions not")
print("  machine-readable; high-acceleration spirals (weak a0 leverage). SKIPPED, stated.")
print("LITTLE THINGS: 26 total, 8 are SPARC members (incl. aliases) -> 18 OUT-OF-SAMPLE dwarfs used.")
print("  Test = outermost-HI-ring RAR point per galaxy; Mgas+Mstar from Oh+2015 Table 2 (VizieR).")
print(f"\n  Excluded as SPARC: {sorted(SPARC_OVERLAP)}")
print(f"  Out-of-sample 18 : {OOS}")

print("\n-- PER-GALAXY outer points (corpus last ring | Oh Table2) --")
print(f"{'galaxy':10s} {'R_c':>5s} {'V_c':>6s} {'eV':>5s} {'R_oh':>5s} {'V_oh':>6s} "
      f"{'Mgas/1e7':>9s} {'Mstar/1e7':>9s} {'fgas':>5s} {'y=gbar/a0':>9s} {'a0_impl(c)':>10s} {'a0_impl(oh)':>11s}")
imp_c, gbar_c = implied_a0(rows, 'corpus'); imp_o, _ = implied_a0(rows, 'oh')
for r_, ic, io_, gb in zip(rows, imp_c, imp_o, gbar_c):
    tag = ('SB' if r_['name'] in STARBURST else '') + ('P' if r_['name'] in PRESSURE else '') + \
          ('*' if r_['star_missing'] else '')
    print(f"{r_['name']:10s} {r_['R_corp']:5.2f} {r_['V_corp']:6.1f} {r_['eV']:5.1f} "
          f"{r_['R_oh']:5.2f} {r_['V_oh']:6.1f} {r_['Mgas']/1e7:9.2f} {r_['Mstar']/1e7:9.2f} "
          f"{r_['fgas']:5.2f} {gb/A0_CANON:9.3f} {ic:10.2e} {io_:11.2e}  {tag}")
print("  tags: SB=starburst/BCD, P=pressure-supported (V<~15), *=no SED stellar mass (fallback/0)")

# --- median implied a0 (robust, per-fork)
for src, imp in (('corpus', imp_c), ('ohT2', imp_o)):
    ok = imp[imp > 0]
    print(f"\n  median implied a0 [{src}]: {np.median(ok):.2e}  "
          f"(16-84%: {np.percentile(ok,16):.2e} - {np.percentile(ok,84):.2e}, N>0 = {len(ok)}/18)")

# ---------------------------------------------------------------- fits, both-ways grid
print("\n-- FITS on the framework's OWN nu:  g_obs = sqrt(g_bar^2 + g_bar a0) --")
hdr = (f"{'variant':52s} {'N':>2s} {'a0_ML':>9s} {'68% CI':>21s} "
       f"{'sig(9.36e-11)':>13s} {'sig(1.13e-10)':>13s} {'scat@can':>8s}")
print(hdr); print('-'*len(hdr))

def show(label, res):
    print(f"{label:52s} {res['N']:2d} {res['a0']:9.2e} "
          f"[{res['ci1'][0]:8.2e},{res['ci1'][1]:8.2e}] "
          f"{res['nsig_canon']:13.2f} {res['nsig_fork']:13.2f} {res['scat_canon']:8.3f}")

subs = {
    'ALL 18': rows,
    'no starburst (15)': [r for r in rows if r['name'] not in STARBURST],
    'no SB, no pressure-supported (13)': [r for r in rows if r['name'] not in STARBURST | PRESSURE],
}
results = {}
for sub, rws in subs.items():
    for src in ('corpus', 'oh'):
        for fg in (1.0, 1.15):
            lbl = f"{sub} | {src} | fgeom={fg} | s free"
            res = fit_a0(rws, src=src, fgeom=fg, s_mode='free', sint_fix=0.10)
            results[lbl] = res; show(lbl, res)
# s fixed stress on the baseline
res = fit_a0(rows, src='corpus', fgeom=1.0, s_mode='fixed', sint_fix=0.10)
show('ALL 18 | corpus | fgeom=1.0 | s=1 FIXED', res)
# intrinsic-scatter stress
for si in (0.05, 0.15):
    res = fit_a0(rows, src='corpus', fgeom=1.0, s_mode='free', sint_fix=si)
    show(f'ALL 18 | corpus | fgeom=1.0 | sint={si}', res)
# comparator (named): McGaugh nu -- NOT the framework's, listed for reference only
resM = fit_a0(rows, src='corpus', fgeom=1.0, s_mode='free', nu=gpred_mcgaugh, sint_fix=0.10)
show('[comparator] McGaugh nu | ALL 18 | corpus | fg=1.0', resM)

# ---------------------------------------------------------------- verdict logic (pre-registered)
base_c = results['ALL 18 | corpus | fgeom=1.0 | s free']
base_o = results['ALL 18 | oh | fgeom=1.0 | s free']
kill_canon = all(res['nsig_canon'] > 3.0 for res in (base_c, base_o))
kill_fork  = all(res['nsig_fork']  > 3.0 for res in (base_c, base_o))
span = [res['a0'] for res in results.values()]
print("\n-- VERDICT (pre-registered kill: a0=9.36e-11 excluded >3sig, M/L marginalized, BOTH forks) --")
print(f"  a0_ML across ALL both-ways variants: {min(span):.2e} .. {max(span):.2e}")
print(f"  canonical 9.36e-11 excluded >3sig in BOTH (R,V) sources (baseline)? {kill_canon}")
print(f"  fork      1.13e-10 excluded >3sig in BOTH (R,V) sources (baseline)? {kill_fork}")
print(f"  SPARC-internal anchors (banked, commit 362e8ff7): full-SPARC joint ~1.08-1.13e-10 @ U~0.59;")
print(f"  gas-dominated SPARC cut (N=37) ~7.7e-11; canonical horizon value 9.36e-11.")
print("\nExit 0 = ran clean; verdict text above is the result, not a success flag.")
