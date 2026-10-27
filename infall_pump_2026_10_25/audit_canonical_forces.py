"""Independent energy differences at fixed canonical Pi audit all new forces."""
import argparse,json
from pathlib import Path
import numpy as np
from central_collocated import Collocated
from live_collocated import Collocated as Old
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');r=m.r;rr=m.wr
a*=np.exp(1j*np.array([.03*np.sin(r),.02*np.cos(r)]));c=1e-5*np.exp(-(rr/6)**2);v=1e-3*np.exp(-(rr/6)**2);p=m.Z(a)*.01*np.sin(r)
def deposit(q):return np.bincount(m.ids,weights=(1-m.frac)*q,minlength=len(c))+np.bincount(m.ids+1,weights=m.frac*q,minlength=len(c))
def charge_density(a):
 mt=abs(a[0])**2
 return m.g*mt+m.g2*mt*mt/m.vol
Pi=m.wvol*v+deposit(charge_density(a))
def energy(aa,xx,pp,cc,PP):
 vv=(PP-deposit(charge_density(aa)))/m.wvol
 return m.full_energy(aa,xx,pp,cc,vv)
mu=m.pot(a,x,True)[1];u=m.enclosed(abs(a[0])**2);omega=p/m.Z(a);mu[0]-=(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*omega**2*m.f(u)[3]);extra,source,bulk,conv,U,rate=m.transfer(a,x,c);mu[0]+=extra-(m.g+2*m.g2*abs(a[0])**2/m.vol)*m.true_chi_m(v)
Ha=(m.kd+mu)*a+m.J*m.alignment(a,x,c);Ha[0,:-1]+=m.ko*U*a[0,1:];Ha[0,1:]+=m.ko*np.conj(U)*a[0,:-1];Ha[1,:-1]+=m.ko*a[1,1:];Ha[1,1:]+=m.ko*a[1,:-1]
gradx=m.carrier_force(x,m.vacuum_parts(a,c))[0];gradp=p/m.Z(a)
psi=a[0]/np.sqrt(m.vol);D=m.k*m.w*np.imag(np.conj(psi[:-1])*U*psi[1:]);rho=abs(a[0])**2/m.vol;hh=m.g+m.g2*.5*(rho[:-1]+rho[1:]);gc=np.zeros(m.n);gc[:-1]+=hh*D/m.sigma;gc[1:]-=hh*D/m.sigma
wavegrad=m.c**2*m.wdiag*c;wavegrad[:-1]-=m.c**2*m.ww*c[1:];wavegrad[1:]-=m.c**2*m.ww*c[:-1];gradc=wavegrad+deposit(gc)
ascale=np.sqrt(np.sum(abs(a)**2,axis=0));da=ascale*np.array([np.sin(.31+2*r)+1j*np.cos(r),np.cos(.51+r)+1j*np.sin(2*r)])
dx=.01*np.sin(r)*np.exp(-(r/10)**2);dp=m.Z(a)*.01*np.cos(r);dc=1e-6*np.sin(rr)*np.exp(-(rr/10)**2);dP=m.wvol*1e-4*np.cos(rr)*np.exp(-(rr/10)**2)
directions=[('material',da,np.zeros_like(x),np.zeros_like(p),np.zeros_like(c),np.zeros_like(Pi),float(2*np.real(np.vdot(Ha,da)))),('carrier',np.zeros_like(a),dx,dp,np.zeros_like(c),np.zeros_like(Pi),float(gradx@dx+gradp@dp)),('scalar',np.zeros_like(a),np.zeros_like(x),np.zeros_like(p),dc,dP,float(gradc@dc+v@dP))]
rows=[]
for name,aa,xx,pp,cc,PP,expected in directions:
 errs=[]
 for eps in [1e-5,1e-6,1e-7]:
  actual=(energy(a+eps*aa,x+eps*xx,p+eps*pp,c+eps*cc,Pi+eps*PP)-energy(a-eps*aa,x-eps*xx,p-eps*pp,c-eps*cc,Pi-eps*PP))/(2*eps)
  errs.append({'epsilon':eps,'finite_difference':actual,'scaled_error':abs(actual-expected)/max(1.,abs(expected))})
 rows.append({'direction':name,'analytic':expected,'checks':errs})
old=Old(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);phi=a.copy();phi[0]*=np.exp(-1j*(m.g+2*m.g2*rho)*m.true_chi_m(c)/m.sigma);Enew=m.full_energy(a,x,p,c,v);Eold=old.full_energy(phi,x,p,c,v)
out={'checks':rows,'old_new_Hamiltonian_difference':Enew-Eold,'shift_invariance_difference':m.full_energy(a,x,p,c+1e-6,v)-Enew,'interpretation':'Artificial nonzero field and material phases are derivative-audit inputs, not infall initial seeds.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert abs(Enew-Eold)<1e-10
assert all(min(r['scaled_error'] for r in row['checks'])<1e-6 for row in rows)
