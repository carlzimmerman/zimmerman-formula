from lib import *
import itertools
cos,_=setc();hmf=lambda M:MF.massFunction(M*cos.h,0,mdef='200c',model='tinker08',q_out='dndlnM')
# SELECTION: enumerate plausible definitions. dimension: (radius rule)x(stat)x(c-M relation)x(mass rule)x(baryon)
Mset={'1e12':1e12,'MW 1.3e12':1.3e12,'SHMR-peak':None,'1e11.5':10**11.5,'L* 2e12':2e12}
# SHMR peak
Mg=np.logspace(10,14,400);Mpk=Mg[np.argmax(smhm(Mg)/Mg)];Mset['SHMR-peak']=Mpk;print('SHMR peak',Mpk)
Mw=np.logspace(10.5,12.5,21);w=hmf(Mw)
wst=w*smhm(Mw)
rad=lambda h:{'g0':h.g0(),'rs':h.g(h.rs),'rmax':h.g(2.163*h.rs),'2rs':h.g(2*h.rs),'.5rs':h.g(.5*h.rs),'.1R200':h.g(.1*h.R),'.05R200':h.g(.05*h.R),'.01R200':h.g(.01*h.R),'Rd(K13)':h.g(.0089*h.R),'2.2Rd(K13)':h.g(.0196*h.R),'R200':h.g(h.R),'1.2R200':h.g(1.2*h.R),'R500':h.g(.65*h.R),'V2/rmax*2':2*h.g(2.163*h.rs),'4piGrs':4*np.pi*G*h.rhos*h.rs,'piGrs':np.pi*G*h.rhos*h.rs,'surfdens Grhos rs':G*h.rhos*h.rs}
models=['duffy08','ludlow16','diemer19','ishiyama21','dutton14','prada12']
vals=[];names=[]
for mdl in models:
    for mn,M in Mset.items():
        for k,v in rad(H(cos,M,model=mdl)).items(): vals.append(v);names.append((mdl,mn,k,'single'))
    for wn,wt in [('num',w),('mstar',wst)]:
        G_={}
        for m in Mw:
            for k,v in rad(H(cos,m,model=mdl)).items():G_.setdefault(k,[]).append(v)
        for k,v in G_.items():
            vals.append(10**np.average(np.log10(v),weights=wt));names.append((mdl,wn,k,'wlogmean'))
vals=np.array(vals);print('N defs',len(vals),'log10 range %.2f..%.2f'%(np.log10(vals.min()),np.log10(vals.max())))
hit=np.abs(vals/A0-1)<.10
print('within 10%% of 9.36e-11: %d (%.1f%%)'%(hit.sum(),100*hit.mean()))
hit5=np.abs(vals/A0-1)<.05;print('within 5%%: %d'%hit5.sum())
from collections import Counter
print('hits by radius rule',Counter(n[2] for n,h in zip(names,hit) if h))
print('hits by mass rule',Counter(n[1] for n,h in zip(names,hit) if h))
# look-elsewhere: same window at other targets log spaced
T=10**np.arange(-12,-9.0,.05)
cnt=[(np.abs(vals/t-1)<.1).sum() for t in T];print('hits for arbitrary targets: median %d, max %d; windows at a0: %d; target frac with>=hit %.2f'%(np.median(cnt),max(cnt),hit.sum(),np.mean(np.array(cnt)>=hit.sum())))
for t in [1.2e-10,1.0766e-10,1.04e-10,3e-10,1e-11]:print('target %.2e hits %d'%(t,(np.abs(vals/t-1)<.1).sum()))
# best-case hits slopes
def sl(k,M,mdl='diemer19'):
    u,d,dl=cosmo_case('rde');a=rad(H(setc(**u)[0],M,model=mdl))[k];b=rad(H(setc(**d)[0],M,model=mdl))[k];return np.log(a/b)/dl
for k,M in [('g0',2e12),('g0',Mpk),('2.2Rd(K13)',1e12),('rs',10**14.8),('4piGrs',10**11),('V2/rmax*2',10**13.8)]:
    print(k,'%.2e'%M,'g=%.2e'%rad(H(setc()[0],M))[k],'dln/dlnrho_DE %.3f'%sl(k,M), 'dln/dlnM %.2f'%(np.log(rad(H(setc()[0],M*1.5))[k]/rad(H(setc()[0],M/1.5))[k])/np.log(2.25)))
# closed-form kappa grid: a=(p/q) pi^k c sqrt(G rho), plus Lambda
ks=[(p,q,e) for p in range(1,7) for q in range(1,7) for e in [-1,-.5,0,.5,1] if np.gcd(p,q)==1]
kv=np.array([p/q*np.pi**e for p,q,e in ks]);print('closed-form N',len(kv),'range',kv.min(),kv.max(),'within 10%% of .5: %d'%(np.abs(kv/.5-1)<.1).sum(),'exact: %d'%np.isclose(kv,.5).sum())
print('law kappa free-fit SPARC 1.0766e-10 -> kappa %.3f; cH0/2pi -> %.3f'%(1.0766e-10/(A0/.5),6.548e-10/(2*np.pi)/(A0/.5)))
# kappa_hat for main models
print('kappa_hat=a/(c sqrt(G rde)):','unit',A0/.5)
# Model D Lambda
hbar=1.0546e-34;eV=1.602e-19;Mpl=2.435e27  # eV reduced
rde=(.685*3*(67.4e3/Mpc)**2/(8*np.pi*G))*c**2  # J/m3
Lde=(rde*(hbar*c)**3/eV**3/eV)**.25 if False else (rde/eV*(hbar*c/eV)**3)**.25
print('rho_DE^(1/4)=%.3e eV'%Lde)
conv=eV/hbar*c
for nm,al,L in [('BFK18',5.7,.05e-3),('Lambda^4=rho_DE alpha=1',1,Lde)]:
    print(nm,'a0=%.3e reduced; %.3e nonreduced'%(al**3*L**2/Mpl*conv,al**3*L**2/(Mpl*np.sqrt(8*np.pi))*conv))
for mp,nm in [(Mpl,'red'),(Mpl*np.sqrt(8*np.pi),'nonred')]:
    print('alpha^3 to give a0 with Lambda^4=rho_DE,',nm,A0/(Lde**2/mp*conv),'alpha=',(A0/(Lde**2/mp*conv))**(1/3),'analytic kappa/sqrt8pi or kappa',.5/np.sqrt(8*np.pi),.5)
