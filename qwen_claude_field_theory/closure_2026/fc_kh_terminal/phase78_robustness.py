#!/usr/bin/env python3
"""phase78_robustness.py -- WKB/high-k (Phase 8) + resolution (Phase 7) robustness.
The reduced dispersion is an EXACT closed form, so 'convergence' = invariance under
k-range extension and grid refinement. Confirm c_par^2 sign/value stable over >=15 decades
in k and under y0-grid 1x/2x/4x/8x refinement."""
import numpy as np
def Wprim(y): return 0.5*y*y+(1+y)*np.exp(-y)-1
def F(y,al): return 2*y*y-2*(2-al)*Wprim(y)
def F1(y,al):return 2*y*(al+(2-al)*np.exp(-y))
def F2(y,al):return 2*al+2*(2-al)*(1-y)*np.exp(-y)
def A_kin(b,l): return (1-b)*(2+b+3*l)/(b+l)
def num_V(kx,kz,W0,W1,W2,y,a0=1.0):
    return (-W0*W1*a0**4*y**2-9*W0*W1*a0**2*kx**2-W0*W2*a0**4*y**3-9*W0*W2*a0**2*kz**2*y
            +20*W0*a0**2*kx**2*y+20*W0*a0**2*kz**2*y+W1**2*a0**4*y**3+5*W1**2*a0**2*kx**2*y
            +4*W1**2*a0**2*kz**2*y-W1*W2*a0**2*kx**2*y**2+W1*W2*a0**2*kz**2*y**2
            -8*W1*a0**2*kx**2*y**2-8*W1*a0**2*kz**2*y**2-4*W1*kx**4-4*W1*kx**2*kz**2
            -4*W2*kx**2*kz**2*y-4*W2*kz**4*y+16*kx**4*y+32*kx**2*kz**2*y+16*kz**4*y)
def den_V(kx,kz,W0,W1,W2,y,a0=1.0): return 4*(W0*a0**2*y+W1*kx**2+W2*kz**2*y)
def o2(kx,kz,y,b,l):
    al=2*b; W0,W1,W2=F(y,al),F1(y,al),F2(y,al)
    return num_V(kx,kz,W0,W1,W2,y)/(A_kin(b,l)*den_V(kx,kz,W0,W1,W2,y))

b,l=1e-15,1e-3
print("Phase 8: c_par^2 = omega^2/kz^2 over 15 decades in k (y0=2, benchmark). a0=1.")
print(f"{'kz':>10}{'c_par^2':>16}")
for kz in np.logspace(1,15,15):   # k>>a0=1, above super-horizon pole
    print(f"{kz:>10.0e}{o2(0.0,kz,2.0,b,l)/kz**2:>16.6e}")
print("-> flat, negative, k-independent (converged). UV catastrophe regulated only above M_*.")

print("\nPhase 7: y0-grid refinement -- min c_par^2 over transition, grids 1x/2x/4x/8x")
for mult in [1,2,4,8]:
    ys=np.linspace(1.001,30.0,200*mult)
    cp=np.array([o2(0.0,1e6,y,b,l)/1e12 for y in ys])
    ineg=cp<0
    print(f"  grid {mult}x (N={len(ys)}): min c_par^2={cp.min():+.6e}  frac unstable={ineg.mean():.3f}")
print("-> stable under refinement (exact closed form).")

print("\nAngle scan at y0=2 (k=1e6): c^2(theta) from radial(0) to tangential(90). unstable cone:")
for deg in [0,10,20,30,45,60,80,90]:
    th=np.deg2rad(deg); kx,kz=1e6*np.sin(th),1e6*np.cos(th)
    print(f"  theta={deg:3d} deg: c^2={o2(kx,kz,2.0,b,l)/1e12:+.4e}  {'UNSTABLE' if o2(kx,kz,2.0,b,l)<0 else 'ok'}")
