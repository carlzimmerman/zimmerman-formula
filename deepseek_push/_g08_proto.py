import numpy as np, math
GN=6.674e-11; MSUN=1.98892e30; PC=3.0856775814913673e16; KPC=1e3*PC
OM_DM=0.264; OM_M=0.3153; OM_B=0.0493; H100=0.6736; NS=0.9649; SIG8=0.811; OM_L=1.0-OM_M
RHO_CRIT_H=2.775e11  # h^-1 Msun per (h^-1 Mpc)^3
def eh98_T(k):
    omc=OM_M-OM_B; ombom0=OM_B/OM_M; h2=H100**2; om0h2=OM_M*h2; ombh2=OM_B*h2
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
print("sigma8", math.sqrt(sigma2_norm_A(A_norm,8.0)))
def sigma_M(M_h1):
    R=(3.0*M_h1/(4.0*math.pi*2.775e11*OM_M))**(1.0/3.0)
    return math.sqrt(sigma2_norm_A(A_norm,R))
def CPT_growth(z):
    E2=OM_M*(1+z)**3+OM_L; Omm=OM_M*(1+z)**3/E2; Oml=OM_L/E2
    return (5.0*Omm/2.0)/(Omm**(4.0/7.0)-Oml+(1.0+Omm/2.0)*(1.0+Oml/70.0))/(1.0+z)
g0=CPT_growth(0.0)
print("g0",g0)
for z in (0.5,1.0,2.4,2.4262,5.0,14.0,30.0,100.0):
    print("g(%g)=%.4f"%(z, CPT_growth(z)/g0))
# sigma table
for Mp in (1e-1,1e2,1e4,1e6,1e8,1e10,1e12,3.09e14):
    Mh=Mp/H100
    print("sigma(M=%.3g)=%.3f"%(Mp,sigma_M(Mh)))
# n(>M,z): Tinker cumulative via dn/dlnM
def f_sigma(s):
    A_t,a_t,b_t,c_t=0.186,1.47,2.57,1.19
    s=np.asarray(s,float)
    return A_t*((s/b_t)**(-a_t)+1.0)*np.exp(-c_t/s**2)
RHO_M=2.775e11*OM_M
m_grid=np.geomspace(1e2, 3e15/H100, 4000)  # h^-1 Msun
sig_grid=np.array([sigma_M(m) for m in m_grid])
dsig_dlnM=np.gradient(np.log(sig_grid), np.log(m_grid))
def n_above(Mp, z):
    Mh=Mp/H100
    gz=CPT_growth(z)/g0
    sigz=sig_grid*gz
    sel=m_grid>=Mh
    dn=f_sigma(sigz[sel])*RHO_M/m_grid[sel]*np.abs(dsig_dlnM[sel])
    return np.trapz(dn, np.log(m_grid[sel]))  # h^3 Mpc^-3
def n_phys(Mp,z):
    return n_above(Mp,z)*H100**3
print("n(>3.09e14,0) h3:", n_above(3.09e14,0.0), "phys:", n_phys(3.09e14,0.0))
print("n(>2.5e14,0):", n_phys(2.5e14,0.0))
print("n(>3.09e14,2.4):", n_phys(3.09e14,2.4262))
print("n(>1.8e14,2.4):", n_phys(1.8e14,2.4262))
print("n(>3.5e14,2.4):", n_phys(3.5e14,2.4262))
# progenitor mass: n(>Mp,2.4)=n(>3.09e14,0)
target=n_above(3.09e14,0.0)
lo,hi=1e12,3.09e14
for _ in range(60):
    mid=math.sqrt(lo*hi)
    if n_above(mid,2.4262)>target: lo=mid
    else: hi=mid
print("M_prog(2.4) phys: %.3e  (f_b*M_prog=%.3e)"%(math.sqrt(lo*hi), 0.1564*math.sqrt(lo*hi)))
print("n(>4.48e11,2.4) phys:", n_phys(4.48e11,2.4262))
# F_above cross-check vs G079
def F_above(Mh):
    smax=sigma_M(Mh); u=np.linspace(-8.0,math.log10(smax),6000); s=10**u
    return float(np.trapz(f_sigma(s)*math.log(10.0),u))
print("F(>1e14)=%.3f F(>1e13)=%.3f (G079: 0.079 / 0.222)"%(F_above(1e14),F_above(1e13)))
# WDM T2 at 5.09
MU=1.12
def alpha_wdm(m): return 0.049*m**-1.11*(OM_M/0.25)**0.11*(H100/0.7)**1.22
def T2(k,m):
    x=(alpha_wdm(m)*k)**(2*MU); return (1+x)**(-10/MU)
print("T2(30,5.09)=%.4f T2(100,5.09)=%.4f (S07: 0.7074/0.0162)"%(T2(30,5.09),T2(100,5.09)))
print("Rcomp(30,0.98)=%.4f (S07 0.7132)"%((1-0.98)+0.98*T2(30,5.09)))
# z_coll map
def z_coll(Mp):
    s0=sigma_M(Mp/H100)
    if s0*g0 >= 1.686 and s0>1.686:
        return 0.0  # collapsed already by z=0 (ill-defined)
    # find z: CPT(z)/g0 = 1.686/s0
    tar=1.686/s0
    lo,hi=0.0,400.0
    for _ in range(80):
        mid=(lo+hi)/2
        if CPT_growth(mid)/g0>tar: lo=mid
        else: hi=mid
    return lo
for Mp in (1e-1,1e2,1e4,1e6,1e8,1e10,1e12):
    print("z_coll(M=%.0e)=%.1f"%(Mp,z_coll(Mp)))
