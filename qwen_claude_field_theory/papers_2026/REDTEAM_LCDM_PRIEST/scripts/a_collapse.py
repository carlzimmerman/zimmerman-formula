# Model A: spherical top-hat with Lambda, numeric. All SI. HYPOTHETICAL RIVAL.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
G=6.674e-11;c=2.998e8;Mpc=3.0857e22;Msun=1.989e30
def bg(OL,H0,):
    H=H0*1e3/Mpc; Om=1-OL; return H,Om
def law(OL,H0):
    H,_=bg(OL,H0); rde=OL*3*H**2/(8*np.pi*G); return .5*c*np.sqrt(G*rde),rde
def collapse(OL,H0=67.4):
    # dimensionless: t in 1/H0, a(t). shell x=r/(a_i-comoving) ; x''=-Om/(2x^2)*(1+d)/.. 
    H,Om=bg(OL,H0)
    # age
    from scipy.integrate import quad
    age=quad(lambda a:1/(a*np.sqrt(Om/a**3+OL)),1e-8,1)[0]
    ai=1e-4
    ti=quad(lambda a:1/(a*np.sqrt(Om/a**3+OL)),1e-8,ai)[0]
    # shell: r'' = -Om*(1+di)*ai^3... r_i=ai (unit comoving); M-term: Omega_m(1+di)/(2 r^2)
    def run(di):
        K=Om*(1+di)
        f=lambda t,y:[y[1],-K/(2*y[0]**2)+OL*y[0]]
        vi=np.sqrt(Om/ai**3+OL)*ai*(1-di/3)  # growing mode
        ev=lambda t,y:y[0]-1e-3*ai;ev.terminal=True;ev.direction=-1
        s=solve_ivp(f,[ti,3*age+3],[ai,vi],events=ev,rtol=1e-9,atol=1e-12,dense_output=True)
        return s,K
    def tc(di):
        s,K=run(di);return (s.t[-1] if s.t_events[0].size else 99)-age
    di=brentq(tc,1e-4*1.0,2e-2,xtol=1e-9)
    s,K=run(di)
    tt=np.linspace(ti,s.t[-1],40001);r=s.sol(tt)[0];k=r.argmax();rta=r[k];tta=tt[k]
    # virial: energy cons, Lahav91: eta=Lambda term ; E=-K/(2 r_ta)-OL r_ta^2/2 ; virial 
    # U_G=-(3/5)K/(2r)*2... use uniform sphere: Ug=-(3/5)K/r *(1/1), UL=-(1/5)... ratio rvir/rta solves (Lahav) 
    eta=2*OL/K*rta**3   # Lambda/gravity ratio at ta (Lambda force OL r / (K/2r^2))
    n=brentq(lambda n:4*eta*n**3-2*(2+eta)*n+2,0.2,0.75)  # Lahav+91: 2 eta n^3-(2+eta)n+1=0 form
    rv=n*rta
    Dc=K/rv**3      # rho_vir/rho_c0 at z=0 (rho_m(r)=K/r^3 in crit units)
    Dta=K/rta**3
    return dict(di=di,Rta_over_Rv=1/n,Dvir_c=Dc,Dta_c=Dta,Om=Om,age=age,tta=tta)
def gs(OL,H0,M):
    H,Om=bg(OL,H0);d=collapse(OL,H0);rc=3*H**2/(8*np.pi*G);m=M*Msun
    out={}
    for nm,D in [('vir',d['Dvir_c']),('ta',d['Dta_c']),('200c',200.)]:
        R=(3*m/(4*np.pi*D*rc))**(1/3);out[nm]=G*m/R**2
    # splashback ~ 1.2 R200m (More+15 at Gamma~2, memory, UNVERIFIED coefficient)
    R200m=(3*m/(4*np.pi*200*Om*rc))**(1/3);Rs=1.2*R200m;out['sp']=G*m/Rs**2
    rmax=(3*G*m/(OL*3*H**2))**(1/3);out['rmax_Lambda']=G*m/rmax**2
    return out,d
print('law',law(.685,67.4)[0],'cH0',c*67.4e3/Mpc)
print(collapse(.685,67.4))
for M in [1e10,1e11,1e12,1e13,1e14,1e15]:
    print(M,{k:'%.2e'%v for k,v in gs(.685,67.4,M)[0].items()})
# mass where g=a0 and M-slope
a0=law(.685,67.4)[0]
for k in ['vir','ta','200c','sp','rmax_Lambda']:
    M=brentq(lambda lm:np.log(gs(.685,67.4,10**lm)[0][k]/a0),6,26); print(k,'M(g=a0)=%.2e'%10**M)
# log slopes at fixed M: (i) fixed omega_m (rho_DE alone) (ii) Omega_L at fixed H0 (iii) H0 at fixed OL
def slope(k,M=1e12):
    om=0.315*67.4**2
    def A(rde_f):
        rde0=.685*67.4**2; H2=om+rde0*rde_f;H0=np.sqrt(H2);return gs(rde0*rde_f/H2,H0,M)[0][k]
    s1=np.log(A(1.1)/A(.9))/np.log(1.1/.9)
    s2=np.log(gs(.70,67.4,M)[0][k]/gs(.67,67.4,M)[0][k])/np.log(.70/.67)
    s3=np.log(gs(.685,70,M)[0][k]/gs(.685,65,M)[0][k])/np.log(70/65)
    return s1,s2,s3
def lawsl():
    om=0.315*67.4**2;rde0=.685*67.4**2
    return .5,.5,1.
print('law slopes (rho_DE|omega_m, OL|H0, H0|OL)',lawsl())
for k in ['vir','ta','200c','sp','rmax_Lambda']:
    print(k,'slopes %.3f %.3f %.3f'%slope(k))
# required mass drift with OL
