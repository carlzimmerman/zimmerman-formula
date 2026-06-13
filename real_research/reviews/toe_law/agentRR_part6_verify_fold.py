"""
agentRR Part 6 -- VERIFY a genuine bounded fold at an in-window point, then quantify how fine-tuned
the window is (the central forced-vs-free question), and check edge-pinning (k* at b->c_chi).
"""
import numpy as np
import sympy as sp

def coeffs(A, Gam, k0, c=1.0):
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

def full_om2(u, A, Gam, k0, c=1.0):
    return c**2*u - A*Gam*(u - k0**2)/((u - k0**2)**2 + Gam**2)

# ---- (1) verify a genuine bounded fold on the FULL branch at an in-window point
Gam, c = 1.0, 1.0
x, y = 0.350, 0.678
k0 = np.sqrt(x*Gam); A = y*c**2*Gam
ceff2, s4, s6 = coeffs(A, Gam, k0, c)
ratio = s6/(s4**2/(4*ceff2))
print(f"IN-WINDOW point x={x} y={y}: c_eff^2={ceff2:.4f} s4={s4:.4f} s6={s6:.4f} ratio={ratio:.4f}")

# FULL branch v_g^2 over u
ug = np.linspace(1e-4, 2.0, 400000)
om2 = full_om2(ug, A, Gam, k0, c)
vg2 = np.gradient(om2, ug)
imin = np.argmin(vg2)
print(f"FULL branch: v_g^2 min = {vg2[imin]:.5f} at u={ug[imin]:.4f} (omega^2={om2[imin]:.5f})")
print(f"  v_g^2_min<0 AND omega^2>0 there => TRUE BOUNDED FOLD: "
      f"{vg2[imin]<0 and om2[imin]>0}")
# also confirm omega^2 stays >0 across the whole branch (no ghost)
print(f"  min omega^2 over branch = {om2.min():.5f} (>0 => no ghost): {om2.min()>0}")
# roton MINIMUM in omega(k): does omega^2 itself dip (d omega^2/du<0)?  v_g^2<0 IS that. report k of dip.
print(f"  roton dip at k={np.sqrt(ug[imin]):.4f}")

# ---- (2) HOW FINE-TUNED is the window? width in x at fixed-ish y, and in the (g0,kappa)/clamp sense.
print("\n--- fine-tuning of the bounded-fold window ---")
# For each x, find the y-range (if any) that lands ratio in (1,4/3) AND gives a true full-branch fold.
def true_fold(A,Gam,k0,c=1.0):
    ug=np.linspace(1e-4,2.0,40000); om2=full_om2(ug,A,Gam,k0,c); vg2=np.gradient(om2,ug)
    return (vg2.min()<0) and (om2.min()>0)
xgrid=np.linspace(0.20,0.60,81)
window_x=[]
for x in xgrid:
    k0=np.sqrt(x*Gam)
    ys=np.linspace(0.05,3.0,400)
    good=[]
    for y in ys:
        A=y*c**2*Gam
        ceff2,s4,s6=coeffs(A,Gam,k0,c)
        if ceff2<=0 or s4>=0 or s6<=0: continue
        r=s6/(s4**2/(4*ceff2))
        if 1<r<4/3 and true_fold(A,Gam,k0,c):
            good.append(y)
    if good:
        window_x.append((x,min(good),max(good)))
if window_x:
    xs_ok=[w[0] for w in window_x]
    print(f"x=k0^2/Gam giving a true bounded fold for some y: {min(xs_ok):.3f} .. {max(xs_ok):.3f}")
    print(f"  => fold exists only in a {(max(xs_ok)-min(xs_ok)):.3f}-wide band of x around ~{np.mean(xs_ok):.3f}")
    for w in window_x[::max(1,len(window_x)//8)]:
        print(f"    x={w[0]:.3f}: y in [{w[1]:.3f},{w[2]:.3f}] (width {w[2]-w[1]:.3f})")
else:
    print("  no true full-branch fold found in x in [0.2,0.6].")

# ---- (3) edge-pinning: at the in-window point, is the dip at the SONIC edge (omega^2(k*) small)?
# The "soft edge" of QQ is omega(k*)->0. Here omega^2 at the dip is O(0.05) not ->0 -- report honestly.
print(f"\nEDGE-PINNING: at the fold, omega^2={om2[imin]:.4f}; sonic-edge soft limit needs omega^2->0.")
print("  k* location is set by k0 (the gain center). Pinning k* AT b->c_chi requires k0 ~ sonic edge.")
