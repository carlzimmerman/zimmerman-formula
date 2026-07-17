#!/usr/bin/env python3
"""Independent cross-check of bulkflow.py: different transfer fn (Eisenstein-Hu
no-wiggle), independent sigma8 norm, independent g_pec, and SHAPE test."""
import numpy as np
from scipy.integrate import quad

h=0.70; Om=0.30; Ob=0.048; ns=0.96; s8=0.80
f_g=Om**0.55
H0_kms=100.0*h
Mpc_m=3.0856775814913673e22
H0_si=H0_kms*1e3/Mpc_m
A0=9.36e-11; A0alt=1.13e-10

# ---- Eisenstein-Hu no-wiggle transfer (independent of BBKS) ----
Theta=2.725/2.7
Omh2=Om*h*h; Obh2=Ob*h*h
s_drag=44.5*np.log(9.83/Omh2)/np.sqrt(1+10.0*Obh2**0.75)  # Mpc
alpha_g=1-0.328*np.log(431*Omh2)*Ob/Om+0.38*np.log(22.3*Omh2)*(Ob/Om)**2
def T_eh(k):  # k in h/Mpc -> convert to 1/Mpc
    kk=k*h
    ss=s_drag
    gamma_eff=Om*h*(alpha_g+(1-alpha_g)/(1+(0.43*kk*ss)**4))
    q=k*Theta**2/gamma_eff
    q=np.where(q<1e-9,1e-9,q)
    L=np.log(2*np.e+1.8*q)
    C=14.2+731.0/(1+62.5*q)
    return L/(L+C*q*q)
def Pk(k): return k**ns*T_eh(k)**2
def Wth(x):
    x=np.asarray(x,float); out=np.ones_like(x); m=x>1e-4; xm=x[m]
    out[m]=3.0*(np.sin(xm)-xm*np.cos(xm))/xm**3; return out
def sig2R(R,A):
    i=lambda k:A*Pk(k)*Wth(k*R)**2*k**2
    v,_=quad(i,1e-4,80.0,limit=400); return v/(2*np.pi**2)
A=s8**2/sig2R(8.0,1.0)
def sigmav(R):
    i=lambda k:A*Pk(k)*Wth(k*R)**2
    v,_=quad(i,1e-4,80.0,limit=400)
    return np.sqrt((H0_kms*f_g)**2/(2*np.pi**2)*v)
def gpec(R): return (3.0*H0_si*Om)/(2.0*f_g)*sigmav(R)*1e3
def nu(y): return np.sqrt(1+1/y)

print("EH transfer, sigma8=%.2f Om=%.2f f=%.3f"%(s8,Om,f_g))
print(f"{'R':>5} {'Vlcdm':>7} {'g_pec':>10} {'g/a0':>8} {'nu':>6} {'V_MI':>7}")
for R in [30,50,100,150,200,300]:
    V=sigmav(R); g=gpec(R)
    print(f"{R:5.0f} {V:7.1f} {g:10.3e} {g/A0:8.4f} {nu(g/A0):6.2f} {V*nu(g/A0):7.0f}")

# --- SHAPE test: how much does each reading flatten the fall R=30->200 ---
V30,V200=sigmav(30),sigmav(200)
g30,g200=gpec(30),gpec(200)
print("\nSHAPE (fall factor V(30)/V(200), smaller=flatter=more non-convergent):")
print(f"  LCDM              : {V30/V200:5.2f}")
print(f"  MI coherent-field : {(V30*nu(g30/A0))/(V200*nu(g200/A0)):5.2f}")
print(f"  MI env-a0 (const nu, cancels): {V30/V200:5.2f}")
# data fall factor CF4TF/H14(~30) vs D11/C11(~150-180)
print("  data (~260-380 @30 -> ~190-260 @150-180): ~1.3-1.5")

# --- benchmark: 1D rms bulk flow at R=50 (common literature quote) ---
print(f"\nBenchmark: 3D rms bulk flow @R=50 h/Mpc = {sigmav(50):.0f} km/s")
print(f"           1D component = {sigmav(50)/np.sqrt(3):.0f} km/s")
print(f"           @R=30 = {sigmav(30):.0f} (Qin pink ~300 => {sigmav(30)/300*100:.0f}% of pink)")
