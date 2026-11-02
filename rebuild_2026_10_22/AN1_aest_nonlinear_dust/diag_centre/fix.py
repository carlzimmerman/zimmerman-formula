import sys,os,json,numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
import an1
G=an1.G
def setup(R):
    cum=np.cumsum(R.mb); lo=cum-R.mb
    q3lo=lo; q3hi=cum
    R.fr=0.5**3*np.ones_like(R.mb)
    # mass fraction of each shell inside its mid-q surface
    ql=np.cbrt(lo); qh=np.cbrt(cum); qc=.5*(ql+qh)
    R.fr=(qc**3-ql**3)/(qh**3-ql**3)
def Mb(R,x):
    o=np.argsort(R.rb); c=np.cumsum(R.mb[o])-(1-R.fr[o])*R.mb[o]
    return np.interp(np.asarray(x)**3,np.concatenate([[0.],R.rb[o]**3]),np.concatenate([[0.],c]))
orig=an1.Run.forces
def forces(s,tol=1e-8):
    if s.rb is not None and not hasattr(s,'fr'): setup(s)
    F=orig(s,tol)
    f=1-s.KB/2
    r=s.r
    g=np.zeros_like(r); g[1:]=f*G*(Mb(s,r[1:])+s.m[1:])/r[1:]**2
    F=-g+an1.SIGN*s.E+s.Lam*r; F[0]=0; F[s.pinf]=0
    s.g=g; s.F=F
    s.gb=f*G*(Mb(s,s.rb)+np.interp(s.rb**3,r**3,s.m))/s.rb**2-s.Lam*s.rb
    return F
an1.Run.forces=forces
N=int(sys.argv[1]); wall=float(sys.argv[2]); out=open(sys.argv[3],'a')
for key in ['1e12','1e15']:
  for mu in [1.24e8,2.04e4,56.6,10,1,0.1,0.0156]:
    R=an1.build(key,mu,'canonical',N=N)
    st=an1.integrate(R,R.t0,Cf=1e-4,wall=wall)
    dr=np.diff(R.r);i=int(np.argmin(dr));a=R.aval()
    Rt={'1e12':None,'1e15':1350.}[key]
    d=dict(key=key,mu=mu,N=N,status=st['status'],z=float(1/a-1),t=float(R.t),cell=i,Cmin=float(dr[i]/(a*R.dq)),r_fold=float(R.r[i]),nbelow=int(np.sum(dr/(a*R.dq)<0.05)),turned=bool(R.turned),nstep=st.get('nstep'))
    out.write(json.dumps(d)+'\n');out.flush()
