from lib import *
cos,_=setc()
Ms=np.logspace(10,13,13)
print('Blum/none/Gnedin per-mass a_fit; K13 size')
for cm in ['blumenthal','none','gnedin']:
  for Rm in ['K13','MMW']:
    A=[]
    for M in Ms:
      r,gb,gt,h,Rd,ms=galaxy(cos,M,cmode=cm,Rmode=Rm);A.append(fit_a(gb,gt))
    A=np.array(A);print(cm,Rm,' '.join('%.2e'%x for x in A[::2]),' | median %.2e spread %.2f dex dlnA/dlnM %.2f'%(np.median(A),np.log10(A.max()/A.min()),np.polyfit(np.log(Ms),np.log(A),1)[0]))
# ensemble: stacked MC with scatter
rng=np.random.default_rng(1)
def mc(c,n=1200,cm='blumenthal',Rm='K13',sigs=(.11,.15,.2)):
    GB=[];GT=[];per=[]
    for lm in rng.uniform(10,12.7,n):
        M=10**lm;c0=H(c,M).cv*10**(rng.normal(0,sigs[0]))
        r,gb,gt,*_=galaxy(c,M,conc=c0,cmode=cm,Rmode=Rm,mscale=10**rng.normal(0,sigs[1]),dsize=10**rng.normal(0,sigs[2]))
        GB+=list(gb);GT+=list(gt);per.append(fit_a(gb,gt))
    GB,GT=np.array(GB),np.array(GT);a=fit_a(GB,GT)
    res=np.log10(GT)-np.log10(law_g(GB,a));
    return a,res.std(),np.log10(per).std(),GB,GT
for cm in ['blumenthal','none']:
  for Rm in ['K13','MMW']:
    a,s,sp,GB,GT=mc(cos,cm=cm,Rm=Rm);print('MC',cm,Rm,'a=%.2e rms=%.3f dex per-gal a scatter=%.2f dex'%(a,s,sp))
    # binned residual shape + low-end slope
    b=np.arange(-12.5,-8,.5);idx=np.digitize(np.log10(GB),b);print('  res bins',[round(float((np.log10(GT)-np.log10(law_g(GB,a)))[idx==i].mean()),2) if (idx==i).sum()>5 else None for i in range(1,len(b))])
# no-scatter version
a,s,sp,*_=mc(cos,sigs=(0,0,0));print('MC noscatter a=%.2e rms %.3f'%(a,s))
# slopes for ensemble a (common random numbers by reseeding)
def A(k):
    global rng;rng=np.random.default_rng(7);c,_=setc(**k);return mc(c,n=400)[0]
for case in ['rde','OL','H0']:
    u,d,dl=cosmo_case(case);print(case,'dln a_RAR slope %.3f'%(np.log(A(u)/A(d))/dl),'s8',setc(**u)[1],setc(**d)[1])
# a(z): halo c(M,z)+ SHMR fixed + size prop R200(z)
for z in [0,1,1.5,2.33]:
    GB=[];GT=[]
    for lm in np.linspace(10,12.7,60):
        r,gb,gt,*_=galaxy(cos,10**lm,z=z);GB+=list(gb);GT+=list(gt)
    print('z',z,'a %.2e'%fit_a(np.array(GB),np.array(GT)))
# large-radius lensing: ratio g_DM+bar to law at r=0.3,1 Mpc etc for 1e12 (M*~2e10)
print('Large radius: M200, r kpc, g_CDM(no 2-halo), g_law, log ratio')
for M in [3e11,1e12,3e12]:
    h=H(cos,M);Mb=smhm(M);Mb=(Mb+Mb*fgas(Mb))*Msun
    for R in [100,300,1000,3000]:
        r=R*kpc;gb=G*Mb/r**2;gc=(G*h.m(min(r,h.R))/r**2)
        print('%.0e %d %.2e %.2e %.2f R200=%d'%(M,R,gc,law_g(gb),np.log10(gc/law_g(gb)),h.R/kpc))
# clusters: X-COP-like M500; law's M vs CDM M: use beta gas, fgas(R500)=.13, BCG
print('Cluster ratio M_true/M_law at R500')
for M200 in [3e14,7e14,1.5e15]:
    h=H(cos,M200);R500=brentq(lambda r:h.m(r)/(4/3*np.pi*r**3*500*h.rc)-1,.1*h.R,h.R)
    M500=h.m(R500);Mb=.13*M500+smhm(M200)*Msun;gb=G*Mb/R500**2;gl=law_g(gb);print('M500 %.1e gb=%.2e g_cdm=%.2e M/M_law=%.2f'%(M500/Msun,gb,G*M500/R500**2,(G*M500/R500**2)/gl))
# IC 1613-like: M*=1e8; AM halo; 2 kpc
Ml=brentq(lambda lm:np.log10(smhm(10**lm)/1e8),9,12);print('M*=1e8 -> M200 %.2e'%10**Ml)
r,gb,gt,h,Rd,ms=galaxy(cos,10**Ml);i=6;print('at r=%.2f kpc gb %.2e gCDM %.2e glaw %.2e; V cdm %.1f law %.1f kms'%(r[i]/kpc,gb[i],gt[i],law_g(gb[i]),np.sqrt(gt[i]*r[i])/1e3,np.sqrt(law_g(gb[i])*r[i])/1e3),' a_fit %.2e'%fit_a(gb,gt))
# UFD: M*=3e3,r=30pc,M200=1e9
h=H(cos,1e9);r=30*3.0857e16;gc=G*h.m(r)/r**2;gb=G*3e3*Msun/r**2;gl=law_g(gb);print('UFD g_cdm %.2e g_law %.2e sigma cdm/ law %.2f'%(gc,gl,(gc/gl)**.5))
