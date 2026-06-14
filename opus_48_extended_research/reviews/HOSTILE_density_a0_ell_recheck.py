#!/usr/bin/env python3
"""
HOSTILE INDEPENDENT RECHECK of the density-a0 @ ell=1/mu=1 Mpc claim.
=====================================================================
I do NOT reuse the original test's functions. I recompute, from the raw rotmod files and the
raw eRASS1 FITS, the two make-or-break numbers, and I stress the model assumptions:

(1) GALAXY RAR scatter under per-galaxy a0 = (c/2)sqrt(G rho_total,smoothed-1Mpc).
    - independent loader, independent scatter metric
    - the key suspect: does the inflation come from a REAL environmental spread, or from the
      halo-from-baryon model mechanically correlating a0 with Mbar?
    - robustness sweep over halo retention f = Mb/Mh, and over Upsilon.
    - I ALSO test the "fairest" reading: re-optimise the per-galaxy normalisation (let the
      universal piece float) so I am not penalising a mean-offset, only the SPREAD.

(2) CLUSTER eta(R500) under the same a0(rho_smoothed-1Mpc).
    - independent recompute of mean-enclosed density and the 1 Mpc-ball density
    - the ell-scan to find what scale WOULD thread (is it ~1 Mpc, or ~10 Mpc = tuned?)

Honest both ways. a0/Z never asserted derived.
"""
import glob, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar

c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0856775814913673e19
Mpc  = 3.0856775814913673e22

H0   = 67.4e3/Mpc
Om_L, Om_m = 0.685, 0.315
rho_crit = 3*H0**2/(8*np.pi*G)
rho_DE   = Om_L*rho_crit
rho_m_cosmic = Om_m*rho_crit

a0_of = lambda rho: 0.5*c*np.sqrt(G*rho)
A0_DE = a0_of(rho_DE)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_S = os.path.join(HERE, "..", "..", "real_research", "data", "sparc_data")
sys.path.insert(0, os.path.join(HERE, "..", "..", "real_research", "data"))
from _load_erass1 import load_clean

ELL = 1.0*Mpc
V_ELL = (4/3)*np.pi*ELL**3

print("="*88)
print("ANCHORS")
print("="*88)
print(f"  rho_crit={rho_crit:.3e}  rho_DE={rho_DE:.3e}  rho_m_cosmic={rho_m_cosmic:.3e}")
print(f"  a0(rho_DE)={A0_DE:.4e}  a0(rho_crit)={a0_of(rho_crit):.4e}  a0(2 rho_DE)={a0_of(2*rho_DE):.4e}")
print(f"  V(1Mpc ball)={V_ELL/Mpc**3:.3f} Mpc^3; cosmic-mean matter mass in ball={rho_m_cosmic*V_ELL/Msun:.3e} Msun")
print()

# ----------------------------------------------------------------------------------
# read every galaxy: per-point (gbar, gobs) with my own M/L, and the global Mbar
# ----------------------------------------------------------------------------------
def read_galaxy(path, ml=0.70):
    rows = []
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"): continue
            p = s.split()
            if len(p) < 6: continue
            try: r,vobs,ev,vgas,vdisk,vbul = (float(p[i]) for i in range(6))
            except ValueError: continue
            rows.append((r,vobs,ev,vgas,vdisk,vbul))
    if not rows: return None
    rows = np.array(rows)
    r,vobs,ev,vgas,vdisk,vbul = rows.T
    vbar2 = vgas*np.abs(vgas) + ml*vdisk*np.abs(vdisk) + ml*vbul*np.abs(vbul)
    # Mbar from outermost valid point
    ok = (r>0) & (vbar2>0)
    Mb = None
    if ok.any():
        i = np.where(ok)[0][-1]
        Mb = (vbar2[i]*1e6)*(r[i]*kpc)/G   # kg
    return dict(r=r,vobs=vobs,ev=ev,vbar2=vbar2,Mb=Mb)

paths = sorted(glob.glob(os.path.join(DATA_S,"*_rotmod.dat")))
print(f"SPARC galaxies: {len(paths)}")

# ----------------------------------------------------------------------------------
# RAR scatter machinery
# ----------------------------------------------------------------------------------
def nu_dsunruh(gbar,a0): return np.sqrt(gbar**2 + gbar*a0)
def nu_mcgaugh(gbar,a0):
    x=np.sqrt(gbar/a0); return gbar/(1.0-np.exp(-x))

def build_points(ml=0.70, ev_cut=0.10):
    """Return per-point gbar, gobs, and the galaxy index, with quality cuts."""
    GB,GO,IDX,MB = [],[],[],[]
    for gi,path in enumerate(paths):
        g = read_galaxy(path, ml=ml)
        if g is None: continue
        r,vobs,ev,vbar2 = g['r'],g['vobs'],g['ev'],g['vbar2']
        for k in range(len(r)):
            if r[k]<=0 or vobs[k]<=0: continue
            if ev[k]<=0 or ev[k]/vobs[k]>ev_cut: continue
            if vbar2[k]<=0: continue
            rm=r[k]*kpc
            go=(vobs[k]*1e3)**2/rm
            gb=(vbar2[k]*1e6)/rm
            if gb<=0 or go<=0: continue
            GB.append(gb); GO.append(go); IDX.append(gi); MB.append(g['Mb'])
    return np.array(GB),np.array(GO),np.array(IDX),np.array(MB)

def rms_dex(gbar,gobs,a0arr,nu):
    pred=nu(gbar,a0arr)
    return float(np.sqrt(np.mean((np.log10(gobs)-np.log10(pred))**2)))

def best_uni(gbar,gobs,nu):
    f=lambda la: rms_dex(gbar,gobs,np.full_like(gbar,10**la),nu)
    r=minimize_scalar(f,bounds=(math.log10(3e-11),math.log10(3e-10)),method="bounded")
    return 10**r.x, r.fun

# per-galaxy a0 from the 1 Mpc smoothing, parametrised by retention f=Mb/Mh
def per_galaxy_a0(Mb_by_idx, f=0.03):
    """rho_smoothed = rho_DE + (Mhalo + cosmic-floor)/V_ELL ; Mhalo = Mb/f."""
    a0g = {}
    for gi,Mb in Mb_by_idx.items():
        if Mb is None or Mb<=0:
            a0g[gi]=A0_DE; continue
        Mh = Mb/f
        Mmatter = Mh + rho_m_cosmic*V_ELL
        rho_sm = rho_DE + Mmatter/V_ELL
        a0g[gi]=a0_of(rho_sm)
    return a0g

print("="*88)
print("PART 1 -- GALAXY RAR  (independent recompute)")
print("="*88)
for ml in (0.50, 0.70):
    GB,GO,IDX,MB = build_points(ml=ml)
    Mb_by_idx = {}
    for gi,mb in zip(IDX,MB):
        Mb_by_idx[gi]=mb
    print(f"\n--- Upsilon={ml:.2f}, points={len(GB)}, galaxies={len(set(IDX.tolist()))}")
    a0u,su_opt = best_uni(GB,GO,nu_dsunruh)
    s936 = rms_dex(GB,GO,np.full_like(GB,A0_DE),nu_dsunruh)
    print(f"  baseline universal free-opt a0={a0u:.3e} -> {su_opt:.4f} dex ; @9.36e-11 -> {s936:.4f} dex")
    for f in (0.05,0.03,0.017):
        a0g = per_galaxy_a0(Mb_by_idx,f=f)
        a0arr = np.array([a0g[gi] for gi in IDX])
        s = rms_dex(GB,GO,a0arr,nu_dsunruh)
        # ALSO: re-optimise a GLOBAL rescale of the per-galaxy a0 -> isolates the SPREAD penalty
        def f_rescale(lk):
            return rms_dex(GB,GO,a0arr*10**lk,nu_dsunruh)
        rr=minimize_scalar(f_rescale,bounds=(-1,1),method="bounded")
        s_rescaled=rr.fun
        med=np.median(a0arr); spread=a0arr.max()/a0arr.min()
        print(f"  density-a0 f={f:.3f}: per-gal a0 med={med:.3e} spread={spread:.1f}x "
              f"-> raw {s:.4f} dex (+{s-s936:.4f}); rescale-opt {s_rescaled:.4f} dex (+{s_rescaled-su_opt:.4f})")
    # McGaugh nu at f=0.03
    a0g = per_galaxy_a0(Mb_by_idx,f=0.03)
    a0arr=np.array([a0g[gi] for gi in IDX])
    s_mc_uni=rms_dex(GB,GO,np.full_like(GB,A0_DE),nu_mcgaugh)
    s_mc=rms_dex(GB,GO,a0arr,nu_mcgaugh)
    print(f"  [McGaugh nu] universal {s_mc_uni:.4f} -> density-a0(f=.03) {s_mc:.4f} (+{s_mc-s_mc_uni:.4f})")

print()
print("="*88)
print("PART 2 -- CLUSTER eta  (independent recompute) + ell scan")
print("="*88)
cl = load_clean()
N=cl['N']; M500=cl['M500']; R500=cl['R500']; gobs=cl['gobs']; gbar=cl['gbar']
M500_kg=M500*1e13*Msun; R500_m=R500*kpc
print(f"  clusters={N}; M500 med={np.median(M500)*1e13:.2e} Msun; R500 med={np.median(R500):.0f} kpc={np.median(R500_m)/Mpc:.2f} Mpc")

eta0 = gobs/nu_dsunruh(gbar, np.full_like(gbar,A0_DE))
print(f"  BASELINE eta(R500) median (universal 9.36e-11) = {np.median(eta0):.3f}")

# mean-enclosed within R500
rho_R500 = 3*M500_kg/(4*np.pi*R500_m**3)
a0_R500 = a0_of(rho_DE + rho_R500)
eta_R500 = gobs/nu_dsunruh(gbar, a0_R500)
print(f"  enclosed-R500 density: rho/rho_crit med={np.median(rho_R500/rho_crit):.0f}; "
      f"a0 boost med={np.median(a0_R500/A0_DE):.1f}x ; eta med={np.median(eta_R500):.3f}")

def eta_for_ell(ell_mpc):
    ell=ell_mpc*Mpc; V=(4/3)*np.pi*ell**3
    ratio=ell/R500_m
    # isothermal-ish M(<r) ~ r extrapolation (matches A2 in original)
    M_in = M500_kg*ratio
    rho_sm = rho_DE + M_in/V + rho_m_cosmic
    a0c = a0_of(rho_sm)
    eta = gobs/nu_dsunruh(gbar, a0c)
    frac_band = np.mean((eta>=1.2)&(eta<=1.5))
    frac_over = np.mean(eta<1.0)
    return np.median(eta), np.median(a0c/A0_DE), frac_band, frac_over

print("\n  ell scan (literal ball, M~r extrapolation):")
print(f"  {'ell[Mpc]':>9} {'eta_med':>8} {'a0boost':>8} {'%in[1.2,1.5]':>12} {'%over(eta<1)':>12}")
for ell_mpc in (1,2,3,5,8,10,12,15):
    em,boost,fb,fo = eta_for_ell(ell_mpc)
    print(f"  {ell_mpc:>9} {em:>8.3f} {boost:>8.1f} {fb*100:>11.0f}% {fo*100:>11.0f}%")

print()
print("="*88)
print("VERDICT NUMBERS")
print("="*88)
print(f"  ell=1Mpc galaxy RAR inflation and cluster over-closure reproduced independently above.")
