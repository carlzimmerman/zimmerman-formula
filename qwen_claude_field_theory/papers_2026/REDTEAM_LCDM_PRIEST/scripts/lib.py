import numpy as np, warnings; warnings.filterwarnings('ignore')
from scipy.special import i0,i1,k0,k1
from scipy.optimize import brentq,minimize_scalar
from colossus.cosmology import cosmology as cc
from colossus.cosmology import power_spectrum as ps
from colossus.halo import concentration as CM
from colossus.lss import mass_function as MF
G=6.674e-11;c=2.998e8;Mpc=3.0857e22;kpc=Mpc/1e3;Msun=1.989e30
A0=9.3625e-11
BASE=dict(H0=67.4,Om0=.315,Ob0=.0493,sigma8=.811,ns=.965)
cnt=[0]
def sig_unnorm(H0,Om0,Ob0,ns):
    h=H0/100; c0=cc.setCosmology('t%d'%cnt[0],dict(flat=True,H0=H0,Om0=Om0,Ob0=Ob0,sigma8=.8,ns=ns,relspecies=False)); cnt[0]+=1
    k=np.logspace(-4,2,1500) # h/Mpc
    T=ps.transferFunction(k,h,Om0,Ob0,c0.Tcmb0,model='eisenstein98')
    R=8.;x=k*R;W=3*(np.sin(x)-x*np.cos(x))/x**3
    D=c0.growthFactorUnnormalized(0.)
    # Delta^2 ∝ A_s (k_phys)^(ns+3) T^2 *(stuff indep of h at fixed... )/(Om h^2)^2 D^2
    D2=(k*h)**(ns+3)*T**2/(Om0*h**2)**2*D**2
    return np.sqrt(np.trapz(D2*W**2,np.log(k)))
_ref=sig_unnorm(BASE['H0'],BASE['Om0'],BASE['Ob0'],BASE['ns'])
def setc(H0=67.4,OL=.685,wb=.0493*.674**2,As_fixed=True):
    Om=1-OL;h=H0/100;Ob=wb/h**2
    s8=.811*sig_unnorm(H0,Om,Ob,.965)/_ref
    nm='c%d'%cnt[0];cnt[0]+=1
    return cc.setCosmology(nm,dict(flat=True,H0=H0,Om0=Om,Ob0=Ob,sigma8=s8,ns=.965,relspecies=False)),s8
def cosmo_case(case,f=.1):
    om=.315*67.4**2;rd=.685*67.4**2;wb=.0493*.674**2
    # returns kwargs pairs up/down, dlnx
    if case=='rde': 
        r=lambda u:dict(H0=np.sqrt(om+rd*u),OL=rd*u/(om+rd*u),wb=wb);return r(1+f),r(1-f),np.log((1+f)/(1-f))
    if case=='OL': return dict(H0=67.4,OL=.70,wb=wb),dict(H0=67.4,OL=.67,wb=wb),np.log(.70/.67)
    if case=='H0': return dict(H0=70.,OL=.685,wb=wb),dict(H0=65.,OL=.685,wb=wb),np.log(70/65)
def smhm(M,N=.0351,lM1=11.59,b=1.376,g=.608):
    x=M/10**lM1;return 2*N*M/(x**-b+x**g)
def mu(x):return np.log(1+x)-x/(1+x)
class H:
    def __init__(s,cos,M,z=0,conc=None,model='diemer19',mdef='200c'):
        s.cos=cos;s.M=M;s.z=z;h=cos.h
        s.cv=conc if conc is not None else float(CM.concentration(M*h,mdef,z,model=model)) if mdef=='200c' else None
        rc=cos.rho_c(z)*(h**2)*Msun/kpc**3*1 # colossus Msun h^2/kpc^3
        s.rc=rc;s.R=(3*M*Msun/(4*np.pi*200*rc))**(1/3);s.rs=s.R/s.cv
        s.rhos=M*Msun/(4*np.pi*s.rs**3*mu(s.cv))
    def m(s,r):return 4*np.pi*s.rhos*s.rs**3*mu(r/s.rs)
    def g(s,r):return G*s.m(r)/r**2
    def g0(s):return 2*np.pi*G*s.rhos*s.rs
def fgas(Ms): # gas-to-star calibration, adopted (assumption): Mg/M*=10^(-0.55(logM*-9.5)) 
    return 10**(-0.55*(np.log10(Ms)-9.5))
def disc_v2(r,Md,Rd):
    y=np.clip(r/(2*Rd),1e-4,300)
    return 2*G*Md/Rd*y**2*(i0(y)*k0(y)-i1(y)*k1(y))
def Menc_disc(r,Md,Rd):
    x=r/Rd;return Md*(1-(1+x)*np.exp(-x))
def contract(h,Mb,Rd,mode='blumenthal',fb=None):
    """ final DM m(r) on grid r with baryons Mb(disc). returns r,mdm. mode none/blum/gnedin(A=.5 approximated)"""
    r=np.logspace(np.log10(h.R*1e-4),np.log10(h.R*1.2),300)
    fi=fb
    if mode=='none':return r,(1-fi)*h.m(r)
    ri=r.copy()
    for it in range(40):
        ave=(lambda x:x) if mode=='blumenthal' else (lambda x:0.85*h.R*(x/(.85*h.R))**.8)
        mi=h.m(ave(ri));mb=Menc_disc(ave(r),Mb,Rd)
        new=r*(mb+(1-fi)*mi)/mi*(ave(r)/ave(ri)*ri/r if False else 1)
        ri=.5*ri+.5*np.maximum(new,1e-3*r)
    return r,(1-fi)*h.m(ri)
def law_g(gb,a=A0):return .5*(gb+np.sqrt(gb**2+4*gb*a))
def galaxy(cos,M,conc=None,Rmode='K13',cmode='blumenthal',mscale=1.,dsize=1.,model='diemer19',z=0,extra=False):
    h=H(cos,M,z,conc,model)
    Ms=smhm(M)*mscale;Mg=Ms*fgas(Ms);Mb=(Ms+Mg)*Msun
    fb=(Ms+Mg)/M
    Rd=(.0089*h.R if Rmode=='K13' else .035/np.sqrt(2)*h.R)*dsize
    rd,mdm=contract(h,Mb,Rd,cmode,fb)
    r=np.logspace(np.log10(.5*Rd),np.log10(5*Rd),12)
    gb=np.maximum(disc_v2(r,Mb,Rd),1e-30)/r
    gt=gb+G*np.interp(r,rd,mdm)/r**2
    return r,gb,gt,h,Rd,Ms
def fit_a(gb,gt):
    f=lambda la:np.sum((np.log10(law_g(gb,10**la))-np.log10(gt))**2)
    return 10**minimize_scalar(f,bounds=(-13,-7),method='bounded').x
