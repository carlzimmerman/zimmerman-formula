#!/usr/bin/env python3
"""
THE RIGOROUS EFE TEST (no dark matter): real per-galaxy external field from 2MRS, vs SPARC outer-RAR suppression.

For each SPARC galaxy I compute the ACTUAL external gravitational field -- the mass-weighted, distance-weighted
vector sum of accelerations from all 2MRS galaxies around it (K-band luminosity -> baryonic mass; redshift
distances; self/group excluded) -- NOT the overdensity scalar that gave the earlier null. e_N = g_ext/a0.

EFE PREDICTION (the one LambdaCDM cannot fake): galaxies in a STRONGER external field sit MORE BELOW the RAR at
low g_bar (internal MOND boost suppressed). So residual(low g_bar) vs e_N should be NEGATIVE, and the Newtonian
control (high g_bar) should be NULL. Warps/beam-smearing don't correlate with the cosmic web -> this isolates EFE.
C. Zimmerman, 2026-06-06. numpy + 2MRS + SPARC. No dark matter anywhere.
"""
import numpy as np, json, glob, os, csv
G=6.674e-11; Msun=1.989e30; Mpc=3.086e22; kpc=3.0857e19
H0=70.0; a0=1.2e-10; MLk=0.6; MKsun=3.27; MLd,MLb=0.5,0.7

# ---- 2MRS catalog -> 3D positions + baryonic masses ----
cra,cdec,cK,ccz=[],[],[],[]
with open(os.path.join(os.path.dirname(__file__),"data","2mrs_catalog.csv")) as f:
    for r in csv.DictReader(f):
        try:
            cz=float(r["cz"])
            if not (50<cz<15000): continue
            cra.append(float(r["RAJ2000"])); cdec.append(float(r["DEJ2000"])); cK.append(float(r["Ktmag"])); ccz.append(cz)
        except: pass
cra=np.radians(cra); cdec=np.radians(cdec); cK=np.array(cK); cd=np.array(ccz)/H0
MK=cK-5*np.log10(cd)-25; Mcat=MLk*10**(-0.4*(MK-MKsun))*Msun         # baryonic (~stellar) mass, kg
cx=cd*np.cos(cdec)*np.cos(cra); cy=cd*np.cos(cdec)*np.sin(cra); cz3=cd*np.sin(cdec)
print(f"2MRS contributors: {len(cd)}  (median logM*={np.median(np.log10(Mcat/Msun)):.1f})")

pos=json.load(open(os.path.join(os.path.dirname(__file__),"data","sparc_ned_positions.json")))
def g_RAR(gb): return np.sqrt(gb**2+gb*a0)
def resid(nm,lo,hi):
    f=os.path.join(os.path.dirname(__file__),"data","sparc_data",f"{nm}_rotmod.dat")
    if not os.path.exists(f): return np.nan
    d=np.genfromtxt(f,comments="#")
    if d.ndim!=2 or d.shape[1]<6: return np.nan
    R,Vobs,eV,Vgas,Vdisk,Vbul=(d[:,i] for i in range(6)); Rm=R*kpc
    Vbar2=np.sign(Vgas)*Vgas**2+MLd*Vdisk**2+MLb*Vbul**2
    gb=Vbar2*1e6/Rm; go=(Vobs*1e3)**2/Rm
    m=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(Vobs>0)&(gb>=lo)&(gb<hi)
    return np.mean(np.log10(go[m])-np.log10(g_RAR(gb[m]))) if m.sum() else np.nan
def gext(ra,dec,cz,dmin,dmax,mode="mondpc"):
    # external field models (the nonlinear MOND field of a distribution is genuinely ambiguous to approximate):
    #   newt   = Newtonian net (vector sum of GM/d^2)
    #   sqrtN  = single MOND-enhance of the Newtonian NET field: sqrt(g_newt*a0)  [same RANK as newt]
    #   mondpc = per-contributor MOND enhance then vector-sum  [over-weights distant deep-MOND structure]
    d=cz/H0; ra=np.radians(ra); dec=np.radians(dec)
    sx=d*np.cos(dec)*np.cos(ra); sy=d*np.cos(dec)*np.sin(ra); sz=d*np.sin(dec)
    dx=cx-sx; dy=cy-sy; dz=cz3-sz; r=np.sqrt(dx**2+dy**2+dz**2)
    s=(r>dmin)&(r<dmax)
    if s.sum()==0: return 0.0,0.0
    rm=r[s]*Mpc; M=Mcat[s]; ux=dx[s]*Mpc/rm; uy=dy[s]*Mpc/rm; uz=dz[s]*Mpc/rm
    gN=G*M/rm**2
    g=gN if mode in ("newt","sqrtN") else np.where(gN<a0,np.sqrt(gN*a0),gN)
    gxv=np.sum(g*ux); gyv=np.sum(g*uy); gzv=np.sum(g*uz); gnet=np.sqrt(gxv**2+gyv**2+gzv**2)
    if mode=="sqrtN": gnet=np.sqrt(gnet*a0) if gnet<a0 else gnet
    return gnet, np.sum(g)
def spear(x,y):
    x,y=np.array(x),np.array(y); ok=np.isfinite(x)&np.isfinite(y); x,y=x[ok],y[ok]; n=len(x)
    rx=np.argsort(np.argsort(x)).astype(float); ry=np.argsort(np.argsort(y)).astype(float)
    rs=np.corrcoef(rx,ry)[0,1]; t=rs*np.sqrt((n-2)/max(1-rs**2,1e-9)); from math import erf
    return n,rs,2*(1-0.5*(1+erf(abs(t)/np.sqrt(2))))

def goodcz(nm):
    c=pos[nm].get("cz"); return c is not None and c>50
names=[nm for nm in pos if pos[nm].get("ra") is not None and goodcz(nm)
       and os.path.exists(os.path.join(os.path.dirname(__file__),"data","sparc_data",f"{nm}_rotmod.dat"))]
# compute e_N (vector field) per galaxy at fiducial dmin=1, dmax=40
eN={}; eNs={}
for nm in names:
    gv,gs=gext(pos[nm]["ra"],pos[nm]["dec"],pos[nm]["cz"],1.0,40.0); eN[nm]=gv/a0; eNs[nm]=gs/a0
eNarr=np.array([eN[nm] for nm in names])
print(f"SPARC galaxies with field computed: {len(names)}")
print(f"e_N (vector) distribution: median={np.median(eNarr):.3f}, 10-90pct={np.percentile(eNarr,10):.3f}-{np.percentile(eNarr,90):.3f}, max={eNarr.max():.2f}")
print("  (Chae+2020 find SPARC e_N ~ 0.01-0.1 typically; sanity check)")

print("\n"+"="*90); print("EFE CORRELATION: outer-RAR residual vs REAL external field e_N=g_ext/a0"); print("="*90)
for label,(lo,hi),efe in [("EFE-sensitive g_bar<3e-11 (deep-MOND)",(0,3e-11),True),
                          ("transition 3e-11..3e-10",(3e-11,3e-10),False),
                          ("Newtonian g_bar>3e-10 (CONTROL)",(3e-10,1e-7),False)]:
    R=[resid(nm,lo,hi) for nm in names]; E=[np.log10(max(eN[nm],1e-4)) for nm in names]
    n,rs,p=spear(E,R)
    pred="predict NEGATIVE" if efe else "predict ~0"
    flag=("<== EFE SIGNAL" if efe and rs<0 and p<0.05 else ("control OK" if not efe and p>0.05 else ""))
    print(f"  [{label:38}] N={n:3d}  Spearman r={rs:+.3f}  p={p:.3f}   [{pred}] {flag}")

print("\n"+"="*90); print("ROBUSTNESS (EFE-sensitive regime; vary group-exclusion dmin & radius dmax; vector vs scalar field)"); print("="*90)
RL=[resid(nm,0,3e-11) for nm in names]
for dmin,dmax in [(0.5,40),(1.0,40),(2.0,40),(1.0,30),(1.0,60)]:
    E=[np.log10(max(gext(pos[nm]["ra"],pos[nm]["dec"],pos[nm]["cz"],dmin,dmax)[0]/a0,1e-4)) for nm in names]
    n,rs,p=spear(E,RL); print(f"  dmin={dmin} dmax={dmax} Mpc (vector): N={n} r={rs:+.3f} p={p:.3f}")
Es=[np.log10(max(eNs[nm],1e-4)) for nm in names]; n,rs,p=spear(Es,RL)
print(f"  scalar field Sum(GM/d^2):           N={n} r={rs:+.3f} p={p:.3f}")

print("\n"+"="*90); print("FIELD-MODEL DEPENDENCE (the honest caveat: the nonlinear MOND field is ambiguous to approximate)"); print("="*90)
for mode,desc in [("newt","Newtonian net (vector sum GM/d^2)"),("sqrtN","single sqrt-enhance of Newtonian net"),
                  ("mondpc","per-contributor MOND enhance (used above)")]:
    E=[np.log10(max(gext(pos[nm]["ra"],pos[nm]["dec"],pos[nm]["cz"],1.0,40.0,mode)[0]/a0,1e-6)) for nm in names]
    n,rs,p=spear(E,RL); print(f"  {desc:42s}: N={n} r={rs:+.3f} p={p:.3f}")
print("""  => IF the EFE-sensitive sign FLIPS between field models, the ~1-sigma hint is NOT robust to the field
     approximation -- it is approximation-dependent, not an in-house detection. The proper external field is
     the nonlinear MOND solution for the whole mass distribution (or Chae's exact e_N); neither simple sum is it.""")
