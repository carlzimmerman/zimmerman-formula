import numpy as np, math
from scipy.integrate import quad
OM_M=0.3153; OM_L=0.6847; H0=67.4
def Hz(z): return H0*math.sqrt(OM_M*(1+z)**3+OM_L)  # km/s/Mpc
# Madau-Dickinson 2014 SFRD (UNVERIFIED literature): M_sun/yr/Mpc^3
def sfrd(z):
    return 0.015*(1+z)**2.7/(1+((1+z)/2.9)**5.6)
def rho_star(z):
    # integral from z to inf: rho*(z) = int_z^inf SFRD(z') |dt/dz'| dz'
    # |dt/dz| = 1/((1+z) H(z)) in Gyr units: convert km/s/Mpc -> Gyr^-1: 1 km/s/Mpc = 1.0227e-3 Gyr^-1
    def integ(zp):
        return sfrd(zp)/( (1+zp)*Hz(zp)*1.0227e-3 )  # M_sun/yr/Mpc^3 * Gyr = M_sun/Mpc^3
    return quad(integ, z, 15.0, limit=200)[0]
r0=rho_star(0.0)
for z in (0.0,1.0,2.0,2.4262,3.0):
    print("rho*(z=%.3f)=%.4e  frac=%.3f"%(z,rho_star(z),rho_star(z)/r0))
# checks: converged at z=15? add tail
tail=quad(lambda zp: sfrd(zp)/((1+zp)*Hz(zp)*1.0227e-3), 15.0, 30.0, limit=200)[0]
print("tail 15-30: %.3e  (%.4f of rho*0)"%(tail, tail/r0))
# z_coll corrected
GN=6.674e-11; MSUN=1.98892e30; H100=0.6736; NS=0.9649; SIG8=0.811
def eh98_T(k):
    omc=OM_M-0.0493; ombom0=0.0493/OM_M; h2=H100**2; om0h2=OM_M*h2; ombh2=0.0493*h2
    th=2.725/2.7; th2,th4=th**2,th**4; kh=k*H100
    zeq=2.50e4*om0h2/th4; keq=7.46e-2*om0h2/th2
    b1d=0.313*om0h2**-0.419*(1.0+0.607*om0h2**0.674); b2d=0.238*om0h2**0.223
    zd=1291.0*om0h2**0.251/(1.0+0.659*om0h2**0.828)*(1.0+b1d*ombh2**b2d)
    Rd=31.5*ombh2/th4/(zd/1e3); Req=31.5*ombh2/th4/(zeq/1e3)
    s=2.0/3.0/keq*np.sqrt(6.0/Req)*np.log((np.sqrt(1.0+Rd)+np.sqrt(Rd+Req))/(1.0+np.sqrt(Req)))
    ksilk=1.6*ombh2**0.52*om0h2**0.73*(1.0+(10.4*om0h2)**-0.95)
    q=kh/13.41/keq
    a1=(46.9*om0h2)**0.670*(1.0+(32.1*om0h2)**-0.532); a2=(12.0*om0h2)**0.424*(1.0+(45.0*om0h2)**-0.582)
    ac=a1**(-ombom0)*a2**(-ombom0**3)
    b1=0.944/(1.0+(458.0*om0h2)**-0.708); b2=(0.395*om0h2)**-0.0266
    bc=1.0/(1.0+b1*((omc/OM_M)**b2-1.0))
    y=(1.0+zeq)/(1.0+zd)
    Gy=y*(-6.0*np.sqrt(1.0+y)+(2.0+3.0*y)*np.log((np.sqrt(1.0+y)+1.0)/(np.sqrt(1.0+y)-1.0)))
    ab=2.07*keq*s*(1.0+Rd)**(-3.0/4.0)*Gy
    f=1.0/(1.0+(kh*s/5.4)**4)
    C=14.2/ac+386.0/(1.0+69.9*q**1.08)
    T0t=np.log(np.e+1.8*bc*q)/(np.log(np.e+1.8*bc*q)+C*q*q)
    C1bc=14.2+386.0/(1.0+69.9*q**1.08)
    T0t1bc=np.log(np.e+1.8*bc*q)/(np.log(np.e+1.8*bc*q)+C1bc*q*q)
    Tc=f*T0t1bc+(1.0-f)*T0t
    bb=0.5+ombom0+(3.0-2.0*ombom0)*np.sqrt((17.2*om0h2)*(17.2*om0h2)+1.0)
    bnode=8.41*om0h2**0.435
    st=s/(1.0+(bnode/kh/s)**3)**(1.0/3.0)
    C11=14.2+386.0/(1.0+69.9*q**1.08)
    T0t11=np.log(np.e+1.8*q)/(np.log(np.e+1.8*q)+C11*q*q)
    Tb=(T0t11/(1.0+(kh*s/5.2)**2)+ab/(1.0+(bb/kh/s)**3)*np.exp(-(kh/ksilk)**1.4))*np.sin(kh*st)/(kh*st)
    return ombom0*Tb+omc/OM_M*Tc
KH=np.geomspace(1e-4,300.0,6000); TH=eh98_T(KH)
def sigma2_norm_A(A,R_h):
    x=np.clip(KH*R_h,1e-12,None); W=3.0*(np.sin(x)-x*np.cos(x))/x**3
    integ=A*KH**3*KH**NS*TH**2/(2.0*math.pi**2)*W**2
    return np.trapz(integ,np.log(KH))
A_norm=SIG8**2/sigma2_norm_A(1.0,8.0)
def sigma_M(M_h1):
    R=(3.0*M_h1/(4.0*math.pi*2.775e11*OM_M))**(1.0/3.0)
    return math.sqrt(sigma2_norm_A(A_norm,R))
def CPT_growth(z):
    E2=OM_M*(1+z)**3+OM_L; Omm=OM_M*(1+z)**3/E2; Oml=OM_L/E2
    return (5.0*Omm/2.0)/(Omm**(4.0/7.0)-Oml+(1.0+Omm/2.0)*(1.0+Oml/70.0))/(1.0+z)
g0=CPT_growth(0.0)
def z_coll(Mp):
    s0=sigma_M(Mp/H100)
    if s0<=1.686: return None
    tar=1.686/s0; lo,hi=0.0,400.0
    for _ in range(80):
        mid=(lo+hi)/2
        if CPT_growth(mid)/g0>tar: lo=mid
        else: hi=mid
    return lo
for Mp in (1e-1,1e2,1e4,1e6,1e8,1e10,1e12,1e13):
    zc=z_coll(Mp)
    print("z_coll(M=%.0e)=%s"%(Mp, "%.1f"%zc if zc is not None else "never(>today)"))
