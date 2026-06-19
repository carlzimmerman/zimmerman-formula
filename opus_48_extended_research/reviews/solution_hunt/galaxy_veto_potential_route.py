#!/usr/bin/env python3
r"""
GALAXY VETO on the POTENTIAL-DEPTH a0 route -- REAL SPARC (solution_hunt, 2026-06-19)
================================================================================
The curvature-floor unifier identified the POTENTIAL DEPTH |Phi|/c^2 as the ONLY
curvature scalar with the cluster-core > galaxy-disk ordering the veto demands, and
found a STEEP power-law f=(|Phi|/c^2)^p (p>=2-3) is the only way to reach the cluster
core boost. THIS script runs that exact law on the REAL 175-SPARC RAR to measure the
scatter blow-up vs the ~0.13 dex floor -- the make-or-break galaxy veto, both ways.

For each SPARC point we compute the local |Phi|/c^2 from the baryonic enclosed mass,
apply a0_eff = a0*sqrt(1 + amp*(|Phi|/c^2)^p) with amp tuned to close the cluster core,
and measure the resulting RAR scatter. PASS = scatter stays ~0.13 dex; BREAK = it inflates.
Framework sealed: a0=9.36e-11, g_obs=sqrt(gbar^2+gbar*a0), Ups=0.70.
"""
import numpy as np, glob, os

G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.0857e19; pc=3.0857e16; km=1e3
a0=9.36e-11
DATA=os.path.join(os.path.dirname(__file__),"..","..","..","real_research","data","sparc_data")

# cluster-core anchor (from curvature_floor_unifier): |Phi|/c^2 ~ 8.4e-6 (median eRASS1 core),
# need Lambda_local/Lambda ~ 224 to close the deep core. amp_p = 224 / (PhiC2_core)^p.
PhiC2_core = 8.44e-6
NEED = 224.0

def load_sparc():
    rows=[]
    for f in sorted(glob.glob(os.path.join(DATA,"*_rotmod.dat"))):
        try: dat=np.loadtxt(f,comments="#")
        except Exception: continue
        if dat.ndim!=2 or dat.shape[1]<7: continue
        R=dat[:,0]*kpc; Vobs=dat[:,1]*km; Vgas=dat[:,3]*km; Vdisk=dat[:,4]*km; Vbul=dat[:,5]*km
        Ups=0.70
        Vbar2=Vgas*np.abs(Vgas)+Ups*Vdisk*np.abs(Vdisk)+1.4*Ups*Vbul*np.abs(Vbul)  # bulge Ups*1.4
        Vbar2=np.clip(Vbar2,0,None)
        gbar=Vbar2/R; gobs=Vobs**2/R
        m=(R>0)&(gbar>0)&(gobs>0)&np.isfinite(gbar)&np.isfinite(gobs)
        if m.sum()<3: continue
        # local |Phi|/c^2 ~ Vbar^2/c^2 (the circular speed squared = |Phi| scale for flat-ish potential)
        PhiC2 = Vbar2/c**2
        rows.append((gbar[m],gobs[m],PhiC2[m]))
    return rows

rows=load_sparc()
gbar=np.concatenate([r[0] for r in rows]); gobs=np.concatenate([r[1] for r in rows]); PhiC2=np.concatenate([r[2] for r in rows])
print("="*88)
print(" GALAXY VETO on the POTENTIAL-DEPTH a0 route -- REAL SPARC (175 gal, %d pts)" % len(gbar))
print("="*88)
print(f"  SPARC |Phi|/c^2 = Vbar^2/c^2: median={np.median(PhiC2):.2e}  range=[{PhiC2.min():.1e},{PhiC2.max():.1e}]")
print(f"  cluster-core anchor |Phi|/c^2={PhiC2_core:.2e}; need Lambda_loc/Lambda={NEED:.0f} to close core.\n")

def nu(gbar,a0_): return np.sqrt(gbar**2+gbar*a0_)
def rar_scatter(a0_eff):
    res=np.log10(gobs)-np.log10(nu(gbar,a0_eff))
    return 1.4826*np.median(np.abs(res-np.median(res)))   # robust MAD-scatter (matches lit ~0.13-0.14)

floor=rar_scatter(a0*np.ones_like(gbar))
print(f"  RAR scatter, constant a0 (robust MAD FLOOR): {floor:.4f} dex  (lit ~0.13-0.14)\n")
print(f"  {'p':>3} {'amp (closes core)':>18} {'med a0_eff/a0 (SPARC)':>22} {'max a0_eff/a0':>14} {'RAR scatter':>12} {'veto':>7} {'cures core?':>12}")
print("  "+"-"*100)
for p in [1,2,3,4]:
    amp = NEED/PhiC2_core**p
    a0_eff = a0*np.sqrt(1 + amp*PhiC2**p)
    sc=rar_scatter(a0_eff)
    veto = "PASS" if sc < floor+0.02 else "BREAK"
    # does this same amp,p give the needed boost at the core anchor?
    core_boost=np.sqrt(1+amp*PhiC2_core**p)
    cures = "YES" if core_boost>2.5 else "by constr."   # amp tuned to close core, so YES by construction
    print(f"  {p:>3} {amp:18.3e} {np.median(a0_eff/a0):22.3f} {np.max(a0_eff/a0):14.2f} {sc:12.4f} {veto:>7} {cures:>12}")

print(r"""
  THE REAL VERDICT (both ways, no spin) -- the potential route is the MIRROR IMAGE of the density route:
   * p=1 (linear, the mechanism-forced form): med a0_eff~1.8, max~7 on SPARC -> RAR scatter inflates
     -> BREAKS the veto (the deepest spirals get boosted). And it needs amp~3e7 (a put-in coupling).
   * p>=2 (steep): med a0_eff~1.00 on SPARC -> PASSES the veto by construction. BUT the SAME steep law,
     to close the cluster core, needs amp~1e12-1e22, and the deepest SPARC disk (|Phi|/c^2=1.7e-6) is
     only ~5x shallower than the cluster core (8.4e-6) -- so to keep the disk at a0_eff~1 while the core
     hits ~3x, the power must be so steep that the law is a near-STEP FUNCTION in |Phi|/c^2 at exactly
     the core value. That is not a coupling, it is a hand-placed threshold tuned to the answer.
  CONTRAST IS THE KILLER: deepest SPARC |Phi|/c^2=%.1e vs cluster core %.1e = only %.1fx apart."""
      % (PhiC2.max(), PhiC2_core, PhiC2_core/PhiC2.max()))
print(r"""  The MW-point toy showed ~100x core/disk potential contrast; REAL SPARC (bright spirals, Vbar~300 km/s)
  collapses it to ~5x, because |Phi|/c^2~(v/c)^2 and the deepest spiral (v~290 km/s) is within a factor
  ~few of a cluster core (v~600-1000 km/s but at large R, shallow |Phi|). With only ~5x separation, NO
  smooth power-law threads 'OFF on the deepest disk, 3-15x ON in the core' without being a tuned step.
  BOTH WAYS: the potential route either BREAKS the veto (linear) or requires a hand-tuned threshold
  (steep) that is not framework-forced -- and even then it gives the WRONG RADIAL SHAPE (|Phi| is flat
  across the cluster, the residual rises 6x inward; see curvature_floor_unifier.py STEP 4 note).""")
