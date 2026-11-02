from lib import *
import sys
cos,s8=setc();print('base s8',s8)
Ms=np.logspace(10,15,11)
print('logM   c    g0     g(rs)   g(rmax) ')
hmf=lambda M,cs:MF.massFunction(M*cs.h,0,mdef='200c',model='tinker08',q_out='dndlnM')
def scales(cos,M,model='diemer19'):
    h=H(cos,M,model=model);rs=h.rs
    d=dict(g0=h.g0(),grs=h.g(rs),grmax=h.g(2.163*rs),g2=h.g(2*rs))
    return d
for M in Ms:
    d=scales(cos,M);print('%.1f %.1f '%(np.log10(M),H(cos,M).cv)+' '.join('%s=%.2e'%kv for kv in d.items()))
for mdl in ['duffy08','ludlow16','diemer19','ishiyama21','dutton14','prada12']:
  try:
    print(mdl,['%.2e'%H(cos,M,model=mdl).g0() for M in [1e11,1e12,1e13]])
  except Exception as e:print(mdl,e)
# M-slope of g0 (10.5..12.5)
gg=[H(cos,M).g0() for M in Ms];print('dlng0/dlnM 10.5-12.5',np.polyfit(np.log(Ms[1:6]),np.log(gg[1:6]),1)[0])
# weights
M=np.logspace(10.5,12.5,41)
w1=hmf(M,cos);w2=w1*smhm(M)
for nm,w in [('num',w1),('Mstar',w2)]:
  v=np.array([H(cos,m).g0() for m in M]);
  print(nm,'g0 logmean %.3e'%10**np.average(np.log10(v),weights=w), 'g(rs) %.3e'%10**np.average(np.log10(v*2*(np.log(2)-.5)),weights=w))
# slopes
def sl(case,fn):
    u,d,dl=cosmo_case(case);cu,_=setc(**u);a=fn(cu);cd,_=setc(**d);b=fn(cd);return np.log(a/b)/dl
def fixedM(c):return H(c,1e12).g0()
# abundance-matched: M at fixed n(>M) = base
Mg=np.logspace(9,15,60)
def nofM(c):
    w=MF.massFunction(Mg*c.h,0,mdef='200c',model='tinker08',q_out='dndlnM')*c.h**3
    return np.cumsum(w[::-1])[::-1]*np.log(Mg[1]/Mg[0])
cos,_=setc();n12=np.interp(np.log(1e12),np.log(Mg),np.log(nofM(cos)))
def am(c):
    logn=np.log(nofM(c));M=np.exp(np.interp(-n12,-logn,np.log(Mg)));return H(c,M).g0()
for case in ['rde','OL','H0']:
    print(case,'dlng0 fixed M=%.3f  AM=%.3f; law %.2f'%(sl(case,fixedM),sl(case,am),{'rde':.5,'OL':.5,'H0':1}[case]))
print('case rde: s8 changes:',setc(**cosmo_case('rde')[0])[1],setc(**cosmo_case('rde')[1])[1])
# z evol
cos,_=setc()
for z in [0,1,1.5,2.33]:
    h=H(cos,1e12,z);print('z',z,'g0(fixed M=1e12) ratio %.2f'%(h.g0()/H(cos,1e12,0).g0()))
