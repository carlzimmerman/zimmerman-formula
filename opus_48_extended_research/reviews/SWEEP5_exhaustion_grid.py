#!/usr/bin/env python3
"""
SWEEP 5 — the exhaustion grid + falsifiable-corner map (Opus 4.8 [1m], 2026-06-15).

Quantify the JOINT viable region of the effective parameter box and its fine-tuning:
volume(viable)/volume(prior), and the sigma each front allows. Both ways — no manufactured
viable corner, no high-priest dismissal. Quarantine: a0/Z never asserted derived.

The effective box (the dark-sector / galactic part that the data actually pins):
  a0      [9.1e-11 .. 1.2e-10]   galactic best-fit band; framework value 9.36e-11
  Upsilon [0.4 .. 0.7]           3.6um stellar M/L (load-bearing nuisance)
  nu (IF) {dS-Unruh(FW), simple-mu, standard-mu, McGaugh}  the interpolation family

Fronts scored on the REAL data:
  Front 2 RAR  : SPARC-175 per-point scatter(a0,Upsilon,nu) on rotmod data
  Front 7 clus : eRASS1 eta(R500)(a0,Upsilon-irrelevant,nu) — the cluster magnitude
  (the cosmological params mu, I0, cs^2 are scored from the banked Mistele/sound-speed work,
   not gridded here — they are a SEPARATE squeezed sub-box, see verdict.)

A cell is "RAR-viable" if scatter <= 0.13 + tol (SPARC intrinsic ~0.11-0.13 dex).
"""
import numpy as np, glob, os
from astropy.io import fits

c=2.998e8; G=6.674e-11; kpc=3.0857e19; Msun=1.989e30
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.abspath(os.path.join(HERE,"..",".."))
SPARC=os.path.join(ROOT,"real_research","data","sparc_data")
ERASS=os.path.join(ROOT,"real_research","data","erass1cl_primary_v3.2.fits")

H0=2.184e-18; OmL=0.685; rho_crit=3*H0**2/(8*np.pi*G); rho_L=OmL*rho_crit
a0_fw=(c/2)*np.sqrt(G*rho_L)
print(f"framework a0 = {a0_fw:.4e} m/s^2\n")

# ---------- interpolation functions nu(y), y=g_bar/a0; g_obs = g_bar*nu(y) ----------
def nu_dsU(y):   return np.sqrt(0.5+0.5*np.sqrt(1+4/y))*0  + np.sqrt(1+1/y)  # dS-Unruh sqrt(1+1/y)
def nu_simple(y):return 0.5+np.sqrt(0.25+1/y)
def nu_std(y):   return np.sqrt(0.5+0.5*np.sqrt(1+4/y**2))
def nu_mcg(y):   return 1.0/(1.0-np.exp(-np.sqrt(y)))
IFS={"dsU(FW)":nu_dsU,"simple":nu_simple,"std":nu_std,"McGaugh":nu_mcg}

# ---------- Front 2: SPARC RAR per-point scatter ----------
def load_sparc():
    rows=[]
    for f in sorted(glob.glob(os.path.join(SPARC,"*_rotmod.dat"))):
        try: d=np.genfromtxt(f,comments="#")
        except: continue
        if d.ndim!=2 or d.shape[1]<6: continue
        R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6))
        rows.append((R*kpc,Vobs,eV,Vgas,Vdisk,Vbul))
    return rows
SP=load_sparc()
print(f"SPARC galaxies loaded: {len(SP)}")

def rar_scatter(Ud,a0,nu,Ub_fac=1.4):
    res,w=[],[]
    Ub=Ub_fac*Ud
    for Rm,Vobs,eV,Vgas,Vdisk,Vbul in SP:
        Vbar2=np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + Ub*Vbul**2
        gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
        ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)
        y=gb[ok]/a0
        r=np.log10(go[ok])-np.log10(gb[ok]*nu(y))
        fr=np.clip(eV[ok],1,None)/np.clip(Vobs[ok],1,None)
        res+=list(r); w+=list(1/fr**2)
    res,w=np.array(res),np.array(w)
    rms=np.sqrt(np.sum(w*res**2)/np.sum(w))
    return rms, np.average(res,weights=w)

# ---------- Front 7: eRASS1 cluster eta(R500) ----------
def load_erass(zmax=1.0,fstar=0.2):
    d=fits.open(ERASS)[1].data
    f=lambda c: np.array([float(x) if str(x).strip() not in("","--") else np.nan for x in d[c]],dtype=float)
    z=f("BEST_Z"); M500=f("M500"); Mgas=f("MGAS500"); fgas=f("FGAS500"); R500=f("R500")
    ok=((z>0)&(z<zmax)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>0.01)&(fgas<0.30))
    M500_kg=M500[ok]*1e13*Msun; Mbar_kg=(1+fstar)*Mgas[ok]*1e11*Msun; R_m=R500[ok]*kpc
    gobs=G*M500_kg/R_m**2; gbar=G*Mbar_kg/R_m**2
    return gobs,gbar,int(ok.sum()),np.median(z[ok])
G_OBS,G_BAR,NCL,ZMED=load_erass()
print(f"eRASS1 clusters (clean): N={NCL}, z_med={ZMED:.2f}\n")

def cluster_eta(a0,nu):
    y=G_BAR/a0
    gpred=G_BAR*nu(y)
    eta=G_OBS/gpred       # >1 means residual missing-mass at R500
    return np.median(eta)

# ============================================================
# THE GRID over the effective box
# ============================================================
A0  = np.linspace(9.1e-11,1.2e-10,12)     # galactic band
UPS = np.linspace(0.40,0.70,7)            # stellar M/L
print("="*78)
print("FRONT 2 (RAR) scatter[dex] over (a0,Upsilon,IF) — viable if <=0.13 dex")
print("="*78)
RAR_VIABLE_TOL=0.13
grid_viable={}   # IF -> boolean array (a0 x Upsilon)
for name,nu in IFS.items():
    arr=np.zeros((len(A0),len(UPS)))
    for i,a0 in enumerate(A0):
        for j,U in enumerate(UPS):
            arr[i,j],_=rar_scatter(U,a0,nu)
    grid_viable[name]=arr<=RAR_VIABLE_TOL
    fmin=arr.min(); amin=A0[np.argmin(arr)//len(UPS)]; umin=UPS[np.argmin(arr)%len(UPS)]
    nviab=grid_viable[name].sum(); ntot=arr.size
    # scatter at the FRAMEWORK point a0=9.36, Upsilon=0.5 and 0.7
    s_fw50,_=rar_scatter(0.5,a0_fw,nu); s_fw70,_=rar_scatter(0.7,a0_fw,nu)
    print(f"  {name:9s}: min={fmin:.4f} dex @(a0={amin:.2e},U={umin:.2f}); "
          f"viable cells {nviab}/{ntot} ({100*nviab/ntot:.0f}%); "
          f"FW@U=0.5:{s_fw50:.4f} U=0.7:{s_fw70:.4f}")

# Joint RAR viable fraction (cell viable under the FRAMEWORK's OWN IF dS-Unruh)
fw_viab=grid_viable["dsU(FW)"]
print(f"\n  Framework-IF (dS-Unruh) viable fraction of the (a0,Upsilon) box: "
      f"{100*fw_viab.sum()/fw_viab.size:.0f}%")

print("\n"+"="*78)
print("FRONT 7 (clusters) median eta(R500) over (a0,IF) — Upsilon-independent (gas+remnant)")
print("="*78)
for name,nu in IFS.items():
    etas=[cluster_eta(a0,nu) for a0 in [9.1e-11,a0_fw,1.05e-10,1.2e-10]]
    print(f"  {name:9s}: eta @a0=[9.1e-11,9.36e-11,1.05e-10,1.20e-10] = "
          f"{etas[0]:.2f},{etas[1]:.2f},{etas[2]:.2f},{etas[3]:.2f}")
print("  (eta=1 = no residual; the cluster front needs the SEPARATE mu/I0 channel for closure)")

# ============================================================
# FINE-TUNING METRIC: volume of jointly-viable region / prior box
# Joint = RAR-viable (framework IF) AND a0 within the Lambda-tied band [9.1,9.6]e-11
# (the framework does NOT get to slide a0 freely; it is tied to Lambda)
# ============================================================
print("\n"+"="*78)
print("FINE-TUNING — viable VOLUME vs prior box (the exhaustion metric)")
print("="*78)
# (a0,Upsilon) galactic sub-box volume
prior_cells=fw_viab.size
viab_cells=fw_viab.sum()
print(f"  Galactic (a0,Upsilon) sub-box, framework IF:")
print(f"    prior box   : a0 in [9.1e-11,1.2e-10] x Upsilon in [0.40,0.70]")
print(f"    viable      : {viab_cells}/{prior_cells} cells = {100*viab_cells/prior_cells:.0f}% of the box")
# a0 tied to Lambda: the framework lives at a SINGLE a0=9.36e-11 (a line, not a slab)
# the only real freedom is Upsilon -> count viable Upsilon at a0_fw
j_fw=np.argmin(np.abs(A0-a0_fw))
ups_viab_fw=grid_viable["dsU(FW)"][j_fw].sum()
print(f"    a0 TIED to Lambda (single value 9.36e-11): viable Upsilon range = "
      f"{ups_viab_fw}/{len(UPS)} = {100*ups_viab_fw/len(UPS):.0f}% of [0.40,0.70]")

print("\nDONE — see SWEEP5 verdict memo for the fine-tuning interpretation.")
