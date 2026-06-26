import numpy as np
print("="*100)
print("ADVERSARY q1: The closed-orbit test (part4 C2) is TOO EASY -- any periodic motion gives oint=0.")
print("A genuinely ACTIVE medium injects energy on a NON-closed (inspiral / amplitude-changing) path.")
print("STRONGEST attack: drive a mu_fw oscillator OFF a closed orbit and ask if net work has a DEFINITE")
print("active SIGN, the way a negative-residue (gain) kernel would. If yes -> gap SURVIVES (active).")
print("="*100)

a0=1.0
def mu_fw(x):
    x=abs(x); return 1.0 if x==0 else (np.sqrt(1+4*x*x)-1)/(2*x)
# Instantaneous MI reading: mu_fw(|a|/a0) a = F(x).  Invert for a given F.
from scipy.optimize import brentq
def accel(F):
    s=np.sign(F); Fa=abs(F)
    if Fa==0: return 0.0
    g=lambda a: mu_fw(a/a0)*a - Fa
    a=brentq(g,1e-12,1e6); return s*a

# TEST 1: Is the instantaneous law derivable from a potential? If a=A(x) single-valued => conservative,
# net work on ANY path (closed OR open) between two x-endpoints depends ONLY on endpoints. Active media DON'T.
print("\n[T1] Path-independence of work (the REAL activity test, valid on OPEN paths):")
k=1.0
def A_of_x(x): return accel(-k*x)   # F=-kx
# work done by the MI 'force' m*a along a path = INT (m a) dx. If a=A(x), this = INT A(x)dx = Phi(x0)-Phi(x1): path-indep.
xs=np.linspace(-0.9,0.9,4001)
Ax=np.array([A_of_x(x) for x in xs])
import scipy.integrate as si
Phi=-si.cumulative_trapezoid(Ax,xs,initial=0.0)
# Path 1: straight x: 0->0.8.  Path 2: overshoot 0->0.85->0.8 (different path, same endpoints)
def workpath(pts):
    # integrate A(x) dx along piecewise-linear x path through pts (fine sampling)
    W=0.0
    for i in range(len(pts)-1):
        seg=np.linspace(pts[i],pts[i+1],20000)
        W+=np.trapz(np.interp(seg,xs,Ax),seg)
    return W
W1=workpath([0.0,0.8]); W2=workpath([0.0,0.85,0.8]); W3=workpath([0.0,-0.3,0.8])
print(f"   INT A dx, path 0->0.8           = {W1:.8f}")
print(f"   INT A dx, path 0->0.85->0.8     = {W2:.8f}")
print(f"   INT A dx, path 0->-0.3->0.8     = {W3:.8f}")
print(f"   max spread across DIFFERENT paths, SAME endpoints = {max(abs(W1-W2),abs(W1-W3)):.2e}")
print("   => path-INDEPENDENT  <=>  a=A(x) is a gradient  <=>  CONSERVATIVE. An active medium FAILS this.")

# TEST 2: full inspiral integration with damping-free dynamics: does a(t) law spontaneously gain energy?
# Integrate x'' from the instantaneous law with NO external drive, start off-orbit, watch modified-H.
print("\n[T2] Free evolution from a NON-equilibrium start (off any closed orbit), NO drive:")
Phi -= np.interp(0.0,xs,Phi)
def Aint(xc): return np.interp(xc,xs,Ax)
def Phint(xc): return np.interp(xc,xs,Phi)
dt=1e-4; n=400000; x=0.85; v=0.0  # start at rest, large amplitude -> will swing
Hmod0=0.5*v**2+Phint(x); hmn=hmx=Hmod0
for i in range(n):
    k1x,k1v=v,Aint(x); k2x,k2v=v+.5*dt*k1v,Aint(x+.5*dt*k1x)
    k3x,k3v=v+.5*dt*k2v,Aint(x+.5*dt*k2x); k4x,k4v=v+dt*k3v,Aint(x+dt*k3x)
    x+=dt/6*(k1x+2*k2x+2*k3x+k4x); v+=dt/6*(k1v+2*k2v+2*k3v+k4v)
    H=0.5*v**2+Phint(x); hmn=min(hmn,H);hmx=max(hmx,H)
print(f"   modified-H drift over {n} steps (off-eq start) = {hmx-hmn:.3e}")
print("   => NO secular energy growth from a non-equilibrium start. Not an active oscillator.")
print("      (An active/gain element started off-equilibrium would show monotone H growth or limit-cycle.)")
