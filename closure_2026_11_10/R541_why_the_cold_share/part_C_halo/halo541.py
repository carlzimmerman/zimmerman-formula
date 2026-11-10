import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
G=6.67430e-11; c=2.99792458e8; Msun=1.98892e30; kpc=3.085677581e19; Mpc=1e3*kpc
R=5.41
# canonical footing (KD1 kd1.json)
h=0.6740779913310114; ob=0.02235817066393584; od=0.12094000633665247
H0=100*h*1e3/Mpc; rhoc=3*H0**2/(8*np.pi*G)
Ob=ob/h**2; Om=(ob+od)/h**2; OL=1-Om
rhoDE=OL*rhoc; rhob=Ob*rhoc
a0s={'canonical':9.3603e-11,'alt':1.1312e-10}
print('rho_DE=%.4e  (0.5 c sqrt(G rhoDE)=%.4e)  rho_b=%.4e Om=%.4f OL=%.4f Ob/Om->R=%.3f'%(rhoDE,0.5*c*np.sqrt(G*rhoDE),rhob,Om,OL,od/ob))
def law_g(gN,a0): return 0.5*gN+np.sqrt(0.25*gN**2+a0*gN)   # mu=x/(1+x), record mk2_lib.py:22
for fk,a0 in a0s.items():
  print('\n=== footing',fk,'a0=%.4e'%a0)
  # step 1 point mass
  x2=(1+R+0.5)**2-0.25-0.0  # X=sqrt(1/4+x^2)-1/2 -> x^2=(X+1/2)^2-1/4
  x2=(R+0.5)**2-0.25
  gN=a0/x2; g=gN*(1+R)
  print('STEP1 point mass: x_cap=r/r_M=%.4f  g_N=%.5f a0  g=%.5f a0 = %.4e m/s2 (deep estimate a0/6.41=%.5f a0)'%(np.sqrt(x2),gN/a0,g/a0,g,1/(1+R)))
  gcap=g
  Rta=lambda Mb: 190*kpc*(Mb/1e10/Msun)**(1/3)   # FLD1 RESULT.md table, R_ta ~ M^(1/3)
  Rfold=lambda Mb: 99*kpc*(Mb/1e10/Msun)**(1/3)*1.0
  print(' logM  r_M kpc  r_cap kpc  R200 kpc r_cap/R200  r_cap/R_ta  r_cap/R_fold  X(R_ta) g(R_ta)/gcap  g200/gcap  gDE(rcap)/gcap')
  for lm in [7,8,9,10,11,12,13,14,15]:
    Mb=10**lm*Msun; rM=np.sqrt(G*Mb/a0); rcap=np.sqrt(x2)*rM
    M200=(1+R)*Mb; R200=(3*M200/(4*np.pi*200*rhoc))**(1/3)
    rta=Rta(Mb); xta=rta/rM; Xta=np.sqrt(.25+xta**2)-.5
    gta=law_g(G*Mb/rta**2,a0); g200=G*M200/R200**2
    gde=8*np.pi*G*rhoDE/3*rcap
    print(' %4.1f %8.2f %9.1f %8.1f %8.3f %9.3f %9.3f %9.2f %8.3f %8.3f %9.2e'%(lm,rM/kpc,rcap/kpc,R200/kpc,rcap/R200,rcap/rta,rcap/Rfold(Mb),Xta,gta/gcap,g200/gcap,gde/gcap))
  # extended cluster: beta=2/3 gas, r_c = 0.1 r_t, truncated at r_t = 2 Mpc (Mb/1e14)^(1/3)
  print(' extended beta-model (beta 2/3, r_c=0.1 r_t, r_t=2 Mpc (M/1e14)^1/3):')
  for lm in [13,14,15]:
    Mt=10**lm*Msun; rt=2*Mpc*(10**lm/1e14)**(1/3); rc=0.1*rt
    f=lambda r: (min(r,rt)-rc*np.arctan(min(r,rt)/rc))/(rt-rc*np.arctan(rt/rc))
    Mbr=lambda r: Mt*f(r)
    Xr=lambda r: (r**2*law_g(G*Mbr(r)/r**2,a0)/G-Mbr(r))
    rr=np.geomspace(0.01*rt,1e3*rt,4000); q=np.array([Xr(r)/Mbr(r) for r in rr])
    i=np.argmin(q); idx=np.where(np.diff(np.sign(q-R)))[0]
    out=[]
    for j in idx:
      r1=brentq(lambda r: Xr(r)/Mbr(r)-R,rr[j],rr[j+1]); out.append('%.0f kpc (r/r_t %.2f, g %.4f a0)'%(r1/kpc,r1/rt,law_g(G*Mbr(r1)/r1**2,a0)/a0))
    print('  logM %d: min Mh/Mb(<r)=%.2f at r/r_t=%.2f ; crossings of 5.41: %s'%(lm,q[i],rr[i]/rt,'; '.join(out)))
  # STEP 2 candidates
  print('STEP2 candidate/gcap (gcap=%.4e):'%gcap)
  cand={'C1 a0':a0,'C2 c sqrt(G rhoDE)':c*np.sqrt(G*rhoDE),'C3 cH0':c*H0,'C4 cH0/2pi':c*H0/2/np.pi,'C5 cH0 sqrt(OL)':c*H0*np.sqrt(OL),
        'C6 OL cH0':OL*c*H0,'C7 a0/2pi':a0/2/np.pi,'C8 a0/4':a0/4,'C9 cH0 Om/2':c*H0*Om/2,'C10 (4pi/3)G rhoDE c/H0':4*np.pi/3*G*rhoDE*c/H0,
        'C11a 0.01 a0':0.01*a0,'C11b 0.03 a0':0.03*a0}
  for k,v in cand.items(): print('   %-26s %.4e  ratio %.3f'%(k,v,v/gcap))
  # STEP 3 rules
  print('STEP3 X = Mh/Mb at truncation radius:')
  print(' logM  (a) r0 kpc X0 | (b) d_L/2 kpc X | (b2) census-sep/2 X | (c) R_ta X')
  def Xat(r,Mb): x=r/np.sqrt(G*Mb/a0); return np.sqrt(.25+x*x)-.5
  res={}
  for lm in np.arange(7,15.01,1):
    Mb=10**lm*Msun
    r0=brentq(lambda r: law_g(G*Mb/r**2,a0)-8*np.pi*G*rhoDE/3*r,1e-3*kpc,1e5*Mpc)
    dL=(Mb/rhob)**(1/3)
    fcl=0.12 if lm<12.5 else 0.04   # Shull+2012: galaxies+CGM ~12%, ICM ~4%
    dC=(Mb/(fcl*rhob))**(1/3)
    rt=Rta(Mb)
    res[lm]=(Xat(r0,Mb),Xat(dL/2,Mb),Xat(dC/2,Mb),Xat(rt,Mb))
    print(' %4.1f  %8.0f %7.2f | %8.0f %7.2f | %8.0f %7.2f | %6.0f %6.2f'%(lm,r0/kpc,res[lm][0],dL/2/kpc,res[lm][1],dC/2/kpc,res[lm][2],rt/kpc,res[lm][3]))
  # census weighting: Shull, Smith & Danforth 2012 (ApJ 759, 23): galaxies 7%, CGM 5%, ICM 4%, rest diffuse
  # galaxies+CGM at log M_b 10.7 (12%), ICM at log M_b 13.5 (4%); diffuse 84% has no bound object
  def interp(lm,i): ks=sorted(res); return np.interp(lm,ks,[res[k][i] for k in ks])
  for i,name in enumerate(['(a) zero-gravity','(b) d_L/2','(b2) census sep/2','(c) R_ta']):
    Xg=interp(10.7,i); Xc=interp(13.5,i)
    print('  census mean %-18s bound only: %.2f   (galaxies X=%.2f, ICM X=%.2f)'%(name,(0.12*Xg+0.04*Xc)/0.16,Xg,Xc))
  # STEP 4 cosmic
  x2c=(R+.5)**2-.25
  r4=3*a0/(4*np.pi*G*rhob*x2c); r4deep=a0/(4*np.pi/3*G*rhob*R**2)
  print('STEP4: ratio=5.41 at r=%.1f Mpc (simple mu); deep formula gives %.1f Mpc'%(r4/Mpc,r4deep/Mpc))
  # native lengths
  RH=c/H0
  Orad=4.18e-5/h**2*(1+0.2271*3.046)/ (1+0.2271*3.046) # photons+nu approx below
  og=2.47e-5; Or=og*(1+0.2271*3.046)/h**2
  aeq=Or/Om
  eta=lambda a: quad(lambda aa: c/(aa**2*H0*np.sqrt(Om/aa**3+Or/aa**4+OL)),1e-12,a,limit=200)[0]
  print('   c/H0=%.0f Mpc ; comoving horizon at equality=%.1f Mpc ; sound horizon r_d~147 Mpc (Planck18, not recomputed); r/c/H0=%.3f r/eta_eq=%.2f r/147=%.2f'%(RH/Mpc,eta(aeq)/Mpc,r4/RH,r4/eta(aeq),r4/(147.1*Mpc)))
  print('   z_eq=%.0f'%(1/aeq-1))
