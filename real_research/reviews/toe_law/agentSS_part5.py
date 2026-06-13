"""
agentSS Part 5 — (b) MODULAR / TOMITA-TAKESAKI flow of the GH thermal (KMS) state.

The GH state on the dS static patch is KMS at T_dS=H/2pi. Tomita-Takesaki: the modular flow is
sigma_t = e^{i H_mod t} with H_mod the modular Hamiltonian; for the GH/static-patch state the modular
flow IS the static-patch time translation (boost), beta = 2pi/H. KMS condition:
   G(t) = G(-t - i beta)   <=>   rho(-omega) = e^{-beta omega} rho(omega)   (detailed balance)
on the spectral function rho(omega) of the GH 2-pt function.

KEY: KMS / modular covariance is a SYMMETRY of the FULL thermal 2-pt function. It constrains the
NEGATIVE-frequency weight relative to the positive (detailed balance). Question: does this FORCE the
moment ratio 4 j3/j2^2 of the relevant gain line?

The full GH thermal spectral function for a dimension-Delta operator on the static patch is the
SL(2,R)/AdS2-thermal weight (continuous principal-series-like):
   rho(omega) = (1/Gamma(2Delta)) * |Gamma(Delta + i omega/(2pi T))|^2 * sinh(omega/(2T)) * (2pi T)^{2Delta-1}
(up to convention). I COMPUTE its moments directly via numerical integration and check:
  - does KMS (detailed balance) fix the ratio? It fixes rho(-w)/rho(w)=e^{-w/T}; the *positive*-w
    line shape still has a free Delta and a free T (=H/2pi). So the ratio depends on Delta -> permits.
  - compute 4 j3 / j2^2 of the thermal line and confirm Delta/T-dependence.
"""
import mpmath as mp
mp.mp.dps = 30

def rho_thermal(omega, Delta, T):
    # thermal SL(2,R) weight; T in same units as omega. Use beta=1/T.
    b = mp.mpf(1)/T
    z = Delta + 1j*omega/(2*mp.pi*T)
    g = mp.gamma(z)
    return mp.sinh(omega/(2*T)) * (abs(g)**2)

def central_moments_thermal(Delta, T, W=60.0, Npts=4000):
    D=mp.mpf(Delta); T=mp.mpf(T)
    # integrate over omega in [-W*T, W*T]
    a=-W*T; b=W*T
    h=(b-a)/Npts
    M0=mp.mpf(0);M1=mp.mpf(0)
    xs=[];ws=[]
    for i in range(Npts+1):
        w=a+i*h
        r=rho_thermal(w,D,T)
        wt=(0.5 if (i==0 or i==Npts) else 1.0)*h
        xs.append(w);ws.append(r*wt)
        M0+=r*wt;M1+=w*r*wt
    mean=M1/M0
    j2=mp.mpf(0);j3=mp.mpf(0)
    for w,wt in zip(xs,ws):
        d=w-mean; j2+=d*d*wt; j3+=d*d*d*wt
    j2/=M0;j3/=M0
    return mean,j2,j3

print("=== (b) Full GH thermal spectral function: central moments & ratio ===")
print("    (the genuinely thermal/KMS two-sided line; T=H/2pi=1 in these units)")
print(f"{'Delta':>8} {'mean':>10} {'j2':>12} {'j3':>14} {'4j3/j2^2':>12}")
T=1.0/(2*mp.pi)  # T_dS with H=1
for Dv in [0.5,1.0,1.5,2.0,3.0]:
    mean,j2,j3=central_moments_thermal(Dv,T,W=80,Npts=6000)
    R=4*j3/j2**2
    print(f"{Dv:>8} {float(mean):>10.5f} {float(j2):>12.5e} {float(j3):>14.5e} {float(R):>12.6f}")
print()
print(">>> The thermal line is SYMMETRIC about omega=0? Check j3 (3rd central moment).")
print(">>> KMS forces rho(-w)=e^{-w/T}rho(w): an ASYMMETRY, so j3 != 0. But does it FIX 4j3/j2^2?")
