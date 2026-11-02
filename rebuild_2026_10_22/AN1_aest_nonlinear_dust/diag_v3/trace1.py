"""A3 audit: trace the first field shells on a disclosed side-test row. Diagnostics, no grade."""
import sys,os,numpy as np
args=sys.argv[1:]; sys.argv=[sys.argv[0],'x']
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import an1
G=an1.G
def setup(R):
    cum=np.cumsum(R.mb); lo=cum-R.mb
    ql=np.cbrt(lo); qh=np.cbrt(cum); qc=.5*(ql+qh)
    R.fr=(qc**3-ql**3)/(qh**3-ql**3)
def Mb(R,x):
    o=np.argsort(R.rb); c=np.cumsum(R.mb[o])-(1-R.fr[o])*R.mb[o]
    return np.interp(np.asarray(x)**3,np.concatenate([[0.],R.rb[o]**3]),np.concatenate([[0.],c]))
orig=an1.Run.forces
def forces(s,tol=1e-8):
    if s.rb is not None and not hasattr(s,'fr'): setup(s)
    orig(s,tol); f=1-s.KB/2; r=s.r
    g=np.zeros_like(r); g[1:]=f*G*(Mb(s,r[1:])+s.m[1:])/r[1:]**2
    F=-g+an1.SIGN*s.E+s.Lam*r; F[0]=0; F[s.pinf]=0
    s.g=g; s.F=F
    s.gb=f*G*(Mb(s,s.rb)+np.interp(s.rb**3,r**3,s.m))/s.rb**2-s.Lam*s.rb
    return F
an1.Run.forces=forces
key,mu,N=args[0],float(args[1]),int(args[2])
R=an1.build(key,mu,'canonical',N=N)
Cf=float(args[3]) if len(args)>3 else 1e-4
R.forces(); nx=0; n=0
tp=[R.t0*x for x in (.1,.2,.3,.4,.5,.6,.7,.8,.85,.9,.93,.95,.97,.98,.99,.995,.998,.999,1)]
ip=0
a0=R.a0
def show():
    a=R.aval();i=np.argmin(np.diff(R.r));C=np.diff(R.r)/(a*R.dq)
    print('z %.4f n %d imin %d Cmin %.2e | r'%(1/a-1,R.nstep,i,C[i]),np.array2string(R.r[1:6],precision=4),'v',np.array2string(R.v[1:6],precision=2),'E/a0',np.array2string(R.E[1:5]/a0,precision=2),'g/a0',np.array2string(R.g[1:5]/a0,precision=2),'Mb1 %.2e nsto %d rb0 %.3g'%(Mb(R,R.r[1:2])[0],R.pinb.sum(),R.rb[0]),flush=True)
while R.t<R.t0-1e-12:
    R.step(R.t0)
    if getattr(R,'crossed',False): print('crossed');break
    if ip<len(tp) and R.t>=tp[ip]: show(); ip+=1
    if R.fold(Cf,R.dq): print('FOLD');show();break
show()
