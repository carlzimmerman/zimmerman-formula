#!/usr/bin/env python3
"""
L5 CONTROL -- calibrate the outer-point/total-mass estimator on the 8 LT galaxies that ARE in SPARC
====================================================================================================
Question: is the ~2e-10 preferred a0 from the 18 out-of-sample LT dwarfs a real out-of-sample pull,
or a bias/noise floor of the METHOD (outermost ring + Oh Table-2 total masses + point-mass g_bar)?

Control: the 8 overlap galaxies (DDO154, DDO168, NGC2366, DDO50=UGC04305, DDO87=UGC05918,
DDO126=UGC07559, Haro29=UGCA281, WLM=UGCA444) have BOTH:
  (a) the LT outer-point estimate (same method as the 18), and
  (b) full SPARC per-ring baryonic decompositions (rotmod) -> 'truth-grade' g_bar at the same radius.
Compare implied a0 from (a) vs (b) galaxy by galaxy. If (a) scatters wildly / biases high while (b)
is tame, the 18-galaxy 'exclusion' is a method artifact, not framework physics. Both-ways: if (a)
tracks (b), the out-of-sample pull stands.

Also: robust statistics for the 18 (fitted intrinsic scatter by ML, median/bootstrap), and the
DDO_101 distance systematic (known literature issue: D=6.4 vs ~12-16 Mpc).
"""
import json, math, os, glob
import numpy as np

SCR  = os.path.dirname(os.path.abspath(__file__))
SPD  = '/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data'
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0_CANON, A0_FORK = 9.36e-11, 1.13e-10

corpus = json.load(open(os.path.join(SCR,'corpus_v7.json')))
LT = {g['galaxy']: g for g in corpus['galaxies'] if g.get('survey')=='LITTLE_THINGS'}

t2 = {}
for line in open(os.path.join(SCR,'lt_table2.dat')):
    p=[x.strip() for x in line.rstrip('\n').split('|')]
    if len(p)<29: continue
    def f(i):
        try: return float(p[i])
        except ValueError: return np.nan
    t2[p[0].upper()] = dict(Rmax=f(1), VRmax=f(3), Mgas=f(24)*1e7,
                            MstarK=f(25)*1e7 if p[25] else np.nan,
                            MstarSED=f(26)*1e7 if p[26] else np.nan)

OVERLAP = {'DDO_154':'DDO154','DDO_168':'DDO168','NGC_2366':'NGC2366','DDO_50':'UGC04305',
           'DDO_87':'UGC05918','DDO_126':'UGC07559','HARO_29':'UGCA281','WLM':'UGCA444'}

def lt_outer(name, src='corpus'):
    g = LT[name]; r = t2[name.upper()]
    if src=='corpus':
        last = g['data'][-1]; R,V = last['Rad'], last['Vobs']
    else:
        R,V = r['Rmax'], r['VRmax']
    Ms = r['MstarSED'] if np.isfinite(r['MstarSED']) else (r['MstarK'] if np.isfinite(r['MstarK']) else 0.0)
    Mb = (r['Mgas']+Ms)*MSUN
    gobs = (V*1e3)**2/(R*KPC)
    gbar = G*Mb/(R*KPC)**2
    return R, V, gobs, gbar, (gobs**2-gbar**2)/gbar

def sparc_at(name, R_kpc, UPS=0.5):
    """SPARC rotmod: interpolate gbar (own decomposition, Ups_disk=UPS, Ups_bul=0.7) and gobs at R."""
    fp = os.path.join(SPD, f'{name}_rotmod.dat')
    d = np.loadtxt(fp)
    R, Vobs, eV, Vg, Vd, Vb = d[:,0], d[:,1], d[:,2], d[:,3], d[:,4], d[:,5]
    gobs = (Vobs*1e3)**2/(R*KPC)
    gbar = (np.sign(Vg)*Vg**2 + UPS*Vd**2 + 0.7*Vb**2)*1e6/(R*KPC)
    j = np.argmin(np.abs(R - R_kpc))
    return R[j], Vobs[j], gobs[j], gbar[j], (gobs[j]**2-gbar[j]**2)/gbar[j], R.max()

print('='*104)
print('CONTROL: 8 LT-SPARC overlap galaxies -- outer-point/total-mass method vs SPARC decomposition')
print('='*104)
print(f"{'LT name':9s}{'SPARC':10s}{'R_LT':>6s}{'V_LT':>7s}{'R_SP@':>6s}{'V_SP':>7s}"
      f"{'a0impl_LTmeth':>14s}{'a0impl_SPARC':>13s}{'dlog(LT-SP)':>12s}")
dl, a0_lt, a0_sp = [], [], []
for lt_n, sp_n in OVERLAP.items():
    R,V,gobs,gbar,a0i = lt_outer(lt_n)
    Rs,Vs,gobss,gbars,a0s,Rmax_sp = sparc_at(sp_n, R)
    d_ = math.log10(a0i/a0s) if (a0i>0 and a0s>0) else np.nan
    dl.append(d_); a0_lt.append(a0i); a0_sp.append(a0s)
    print(f"{lt_n:9s}{sp_n:10s}{R:6.2f}{V:7.1f}{Rs:6.2f}{Vs:7.1f}{a0i:14.2e}{a0s:13.2e}{d_:12.2f}")
dl = np.array(dl); ok = np.isfinite(dl)
print(f"\n  method-vs-SPARC offset: median {np.median(dl[ok]):+.2f} dex, "
      f"mean {np.mean(dl[ok]):+.2f} dex, rms {np.std(dl[ok]):.2f} dex  (N={ok.sum()})")
print(f"  SPARC-decomp implied a0 (these 8, at LT outer radius): median {np.median(a0_sp):.2e}")
print(f"  LT-method   implied a0 (same 8):                        median {np.median(a0_lt):.2e}")
print("  NOTE: same PHYSICAL galaxies -- any offset/scatter here is pure METHOD+DATA systematics,")
print("        the framework cannot cause it.")

# per-point V comparison at matched radii (data quality check LT vs SPARC)
print(f"\n{'LT name':9s}{'SPARC':10s}{'V_LT(Rout)':>11s}{'V_SPARC(Rout)':>14s}{'dV/V':>7s}")
for lt_n, sp_n in OVERLAP.items():
    R,V,_,_,_ = lt_outer(lt_n)
    Rs,Vs,_,_,_,_ = sparc_at(sp_n, R)
    print(f"{lt_n:9s}{sp_n:10s}{V:11.1f}{Vs:14.1f}{(V-Vs)/Vs:7.1%}")

# ------------------------------------------------------------------ robust stats for the 18 OOS
print('\n' + '='*104)
print('ROBUST re-assessment of the 18 out-of-sample dwarfs (a0 implied per galaxy, corpus outer ring)')
print('='*104)
SPARC_OVERLAP = set(OVERLAP)
OOS = sorted(set(LT) - SPARC_OVERLAP)
imp, names = [], []
for n in OOS:
    _,_,_,_,a0i = lt_outer(n)
    imp.append(a0i); names.append(n)
imp = np.array(imp)
la = np.log10(imp[imp>0])
print(f"  N={len(la)}, log10 a0: median {np.median(la):.2f}, MAD-sigma {1.4826*np.median(abs(la-np.median(la))):.2f} dex")
mad = 1.4826*np.median(abs(la-np.median(la)))
se  = mad/math.sqrt(len(la))
for a0pin, tag in ((A0_CANON,'canonical 9.36e-11'), (A0_FORK,'fork 1.13e-10')):
    z = (np.median(la)-math.log10(a0pin))/ (se*1.2533)   # median SE = 1.2533 sigma/sqrt(N)
    print(f"  median-based tension vs {tag}: {z:+.1f} sigma  (SE_median={se*1.2533:.3f} dex)")
# bootstrap of the median
rng = np.random.default_rng(42)
boots = np.array([np.median(rng.choice(la, len(la), replace=True)) for _ in range(20000)])
for a0pin, tag in ((A0_CANON,'canonical'), (A0_FORK,'fork')):
    p = (boots <= math.log10(a0pin)).mean()
    print(f"  bootstrap P(median <= {tag}) = {p:.4f}  -> {abs(np.median(boots)-math.log10(a0pin))/np.std(boots):.1f} sigma-equiv")

# ML with intrinsic scatter FITTED (profile likelihood over a0, sint; s nuisance on stars)
def mlfit(la_arr):
    la0g = np.linspace(-11.5,-8.5,601); sig = np.geomspace(0.05,1.0,60)
    best=(np.inf,None,None); prof=np.full(len(la0g),np.inf)
    for i,l0 in enumerate(la0g):
        for st in sig:
            nll = np.sum(0.5*((la_arr-l0)/st)**2 + np.log(st))
            if nll<prof[i]: prof[i]=nll
            if nll<best[0]: best=(nll,l0,st)
    d2 = 2*(prof-best[0])
    def ns(a0pin):
        j=np.argmin(abs(la0g-math.log10(a0pin))); return math.sqrt(max(d2[j],0))
    return best[1],best[2],ns(A0_CANON),ns(A0_FORK)
l0,st,nsc,nsf = mlfit(la)
print(f"\n  ML (Gaussian, sint FITTED): a0={10**l0:.2e}, sint={st:.2f} dex, "
      f"sig vs canonical={nsc:.1f}, vs fork={nsf:.1f}")

# DDO_101 distance systematic (Read+2016: D may be ~2x Oh's 6.4 Mpc)
print("\n  DDO_101 (known distance controversy, Read et al. 2016 'curious case'):")
_,_,gobs,gbar,a0i = lt_outer('DDO_101')
for fD in (1.0, 1.9):   # 6.4 -> ~12.9 Mpc
    # M ~ D^2, R ~ D, V fixed: gobs ~ 1/D, gbar ~ 1
    a0d = ((gobs/fD)**2 - gbar**2)/gbar
    print(f"    D scale x{fD:.1f}: implied a0 = {a0d:.2e}")

print("\nBOTH-WAYS BOTTOM LINE printed above; exit 0 = ran clean.")
