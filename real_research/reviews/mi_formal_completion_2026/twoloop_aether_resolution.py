#!/usr/bin/env python3
"""
RESOLUTION of the apparent two-loop transverse aether term. The finite/two-loop workflow's
SYNTHESIS agent reported that a 'matter bubble between two frame vertices' generates a
transverse (grad_perp du)^2 kinetic term (UV-growing). On scrutiny that is an ARTIFACT of
TWO setup errors; done correctly, no transverse term is generated, for a clean all-orders reason.
Framework: frame u is 0-dof (2nd-class, no propagator); K acts ONLY on u via Box_u=(u.grad)^2;
matter phi (proxy rho_m=m^2 phi^2) has a standard propagator; background frame is geodesic (dS comoving).
"""
import numpy as np, sympy as sp

def Kf(z):
    z=np.asarray(z,float); out=np.zeros_like(z); m=z>0
    out[m]=(np.sqrt(1+4*z[m])-1)/(2*np.sqrt(z[m])); return out

print("="*78); print("ERROR 1 — the synthesis put K on the LOOP (matter) momentum"); print("="*78)
def bub(direction, on_loop, N=6_000_000, L=8.0, seed=1):
    rng=np.random.default_rng(seed); ks=rng.uniform(-L,L,(N,4)); vol=(2*L)**4
    D=(ks**2).sum(1)+1.0; kd=ks[:,direction]; d2=(8*kd*kd)/D**3-2/D**2
    w=Kf(ks[:,0]**2)**2 if on_loop else np.ones_like(D)
    return (w/D*d2).mean()*vol
print(f"  K on loop k0 (WRONG): q0={bub(0,1):+.3e} qperp={bub(1,1):+.3e} split={bub(0,1)-bub(1,1):+.3e} -> fake asymmetry")
print(f"  plain scalar bubble  : q0={bub(0,0):+.3e} qperp={bub(1,0):+.3e} split={bub(0,0)-bub(1,0):+.3e} -> dS-symmetric (~MC noise)")
print("  Physically K rides the EXTERNAL frame leg (Box_u -> K(-q0^2), q0 only), never the loop.")
print("  The frame has NO propagator (0 dof) so delta_u is never an internal line -> no loop carries K.")

print("\n"+"="*78); print("ERROR 2 — the required delta_u-phi-phi bubble VERTEX is identically ZERO (F1)"); print("="*78)
# background frame geodesic: the linear-in-du coupling is m^2 phi^2 * du.[K(Box_ubar) ubar].
# On a geodesic comoving frame, (ubar.grad) ubar = 0  =>  Box_ubar ubar = (ubar.grad)^2 ubar = 0
# => K(Box_ubar) ubar = K(0) ubar = 0  (since K(0)=0). So the bubble vertex does not exist.
t,x,H=sp.symbols('t x H',positive=True); a=sp.exp(H*t); g=sp.diag(-1,a**2); gi=g.inv()
def Gamma(l,m,n): return sum(gi[l,r]*(sp.diff(g[r,m],[t,x][n])+sp.diff(g[r,n],[t,x][m])-sp.diff(g[m,n],[t,x][r]))/2 for r in range(2))
ub=sp.Matrix([1,0])                                   # comoving frame
acc=sp.Matrix([sp.diff(ub[l],t)+sum(Gamma(l,0,n)*ub[n] for n in range(2)) for l in range(2)])  # (ubar.grad)ubar
print(f"  background frame acceleration (ubar.grad)ubar = {sp.simplify(acc).T}  -> 0 (geodesic)")
print(f"  => Box_ubar ubar = (ubar.grad)^2 ubar = 0, and K(Box_ubar)ubar = K(0)ubar = 0 since K(0)=0.")
zK=sp.symbols('z',positive=True); Kz=(sp.sqrt(1+4*zK)-1)/(2*sp.sqrt(zK))
print(f"  K(0) = {sp.limit(Kz,zK,0,'+')}. So the delta_u-phi-phi (bubble) vertex VANISHES identically.")

print("\n"+"="*78); print("THE ALL-ORDERS REASON: delta_u has no transverse kinetic term at ANY loop order"); print("="*78)
print("  In S_matter, delta_u appears ONLY sandwiched with K(Box_u) [-> K(-q0^2), a function of the")
print("  frequency q0 ONLY] or with longitudinal factors (u.grad -> q0). The transverse aether kinetic")
print("  term is the coefficient of qperp^2 |du_perp|^2 at q0=0. EVERY contribution carries a factor")
print("  that vanishes at q0=0: either K(-q0^2)->K(0)=0, or (u.grad)->q0=0. Hence the coefficient is")
print("  0 to ALL loop orders. This is the SAME K(0)=0 fact that forbids the a0 tadpole.")
print("  (Caveat, unchanged: the GRAVITON-loop sector — the graviton IS dynamical — rests on the")
print("   TT x delta_u_perp vertex being zero, CAS-verified n=1,2; the regulated dS integral and")
print("   constraint-survival-under-loops remain the honest open items.)")
print("\nVERDICT: NO two-loop transverse aether kinetic term. The synthesis finding was an artifact")
print("(K mis-placed on the loop momentum + a bubble whose vertex is zero by F1). Aether-freedom UPHELD;")
print("structurally protected to all orders by F1 (linear vertex=0) + K(0)=0. NOT 'theory closed'.")
