import numpy as np, importlib.util
from scipy.interpolate import CubicSpline
spec=importlib.util.spec_from_file_location('m','methodA_ode.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
G=6.674e-11; Msun=1.989e30; AU=1.496e11
a0=9.36e-11; Z=np.sqrt(32*np.pi/3); a0V=Z*a0; r_t=np.sqrt(2*G*Msun/a0V)
print("r_t = %.0f AU"%(r_t/AU))

# ---- 1. where does the scalar phantom l=2 moment integrand live? ----
gx=2.2
r=np.logspace(np.log10(5*AU),np.log10(5e5*AU),4000)
Ar2,Ath2=m.extra_field_l2(a0,gx,r)
rho2=m.div_l2(r,Ar2,Ath2)
# moment integrand per dln r : rho2 * P2-weight... project_l2 integrand ~ rho2 * r^2/r^3 * r (dlnr) = rho2/1 * dr; per dlnr ~ rho2*r
# actual project weight: 2pi R^2 ST dr dth * P2^2/R^3 ; radial part ~ rho2 * r^2 * dr / r^3 = rho2 dr/r ; per dlnr = rho2
integrand = rho2.copy()  # d(moment)/dln r proportional to rho2 * (angular const)
cum = np.cumsum(np.abs(integrand))*np.gradient(np.log(r))
cum/=cum[-1]
for frac,label in [(0.25,'25%'),(0.5,'50%'),(0.75,'75%'),(0.9,'90%')]:
    idx=np.searchsorted(cum,frac); print(f"  {label} of |moment| accumulated by r = {r[idx]/AU:8.0f} AU  (r/r_t={r[idx]/r_t:.3f})")

# ---- 2. w three ways at beta=0.95, K0hat=0.5 and 1.0 ----
def S_floor(K0hat,beta): return K0hat/(K0hat+4*beta)
for K0hat in [0.5,1.0]:
    rho_=r/r_t; kt=K0hat*np.maximum(1.0,rho_); 
    for beta in [0.95]:
        Ssup=kt/(kt+4*beta)
        # method A: div(S*A)
        wA = m.project_l2(r,m.div_l2(r,Ssup*Ar2,Ssup*Ath2))/m.project_l2(r,m.div_l2(r,Ar2,Ath2))
        # suppress density: S*rho2
        wD = m.project_l2(r,Ssup*rho2)/m.project_l2(r,rho2)
        # suppress bulk strain l=2 (J ~ |g_N| l=2): build Jt2 radial then suppress
        S=m.setup(a0,gx,K0hat); Jt2=S['Jt2_of'](r)
        wJ = m.project_l2(r,Ssup*Jt2)/m.project_l2(r,Jt2)  # note: project of Jt2 as density-like
        print(f"K0hat={K0hat} beta={beta}: S_floor={S_floor(K0hat,beta):.3f}  wA(div S*A)={wA:.3f}  wD(S*rho)={wD:.3f}  wJ(S*Jstrain)={wJ:.3f}")

# ---- 3. mask sensitivity of wA ----
print("\nmask sensitivity (K0hat=0.5, beta=0.95):")
for rmin in [5,20,50,200,1000]:
    rr=np.logspace(np.log10(rmin*AU),np.log10(5e5*AU),4000)
    A2,At2=m.extra_field_l2(a0,gx,rr); 
    rho_=rr/r_t; kt=0.5*np.maximum(1.0,rho_); Ssup=kt/(kt+4*0.95)
    wA=m.project_l2(rr,m.div_l2(rr,Ssup*A2,Ssup*At2))/m.project_l2(rr,m.div_l2(rr,A2,At2))
    print(f"  rmin={rmin:5d} AU:  wA={wA:.3f}")
