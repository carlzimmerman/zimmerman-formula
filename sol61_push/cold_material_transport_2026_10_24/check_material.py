import pathlib,json,numpy as np
from scipy.special import sph_harm
from material import Wave
from angular_half import SHT,Angular
P=pathlib.Path(__file__).resolve().parent;r=np.linspace(.0001,12,768);w=np.gradient(r);eta=.5;boost=.3;field=SHT(16,0,40,2);mu=field.mu;lm=field.lm;rng=np.random.default_rng(11011);x0=rng.normal(size=(64,3))*.6;xx=x0.copy();ds=.02;maxvel=0.
def wave(t):
 ss=1+1j*eta*t;zz=r[:,None,None]*mu[None,:,None];rr2=r[:,None,None]**2+(.2+boost*t)**2-2*zz*(.2+boost*t);psi=ss**(-1.5)*np.exp(-rr2/(2*ss)+1j*(boost*zz-boost*boost*t/2)/eta);psi=np.broadcast_to(psi,(len(r),len(mu),field.nphi));coeff=field.back(psi)*(np.sqrt(w)*r)[:,None];return Wave(coeff,r,w,lm,eta)
for k in range(100):
 t=k*ds;a=wave(t);ps,g=a.values(xx);vel=eta*np.imag(ps.conj()[:,None]*g)/abs(ps)[:,None]**2;mid=xx+.5*ds*vel;b=wave(t+ds/2);ps,g=b.values(mid);vm=eta*np.imag(ps.conj()[:,None]*g)/abs(ps)[:,None]**2;analytic=np.array([0,0,boost])+eta*eta*(t+ds/2)/(1+eta*eta*(t+ds/2)**2)*(mid-np.array([0,0,.2+boost*(t+ds/2)]));maxvel=max(maxvel,float(np.max(abs(vm-analytic))));xx+=ds*vm
ex=np.array([0,0,.2+boost*2])+(x0-np.array([0,0,.2]))*np.sqrt(1+(eta*2)**2);traj=float(np.max(abs(xx-ex)));assert maxvel<1e-4 and traj<1e-4,(maxvel,traj)
# Pointwise potential derivative: small projection versus product-complete projection.
a=Angular(4,4,np.geomspace(.02,10,40),np.ones(40)*.1);v=rng.normal(size=(40,a.field.nm))+1j*rng.normal(size=(40,a.field.nm));v/=np.linalg.norm(v);F=SHT(4,4,30,30);D=SHT(8,8,30,30);full=SHT(12,12,30,30);va=F.forward(v);rho=D.back(abs(va)**2/(a.w*a.r*a.r)[:,None,None]);co=a.green(rho);pa=D.forward(co).real;force=pa*va;pv=F.forward(F.back(force));S=2/eta*np.imag(va.conj()*pv);h=1e-6;fd=(abs(va-1j*h*pv/eta)**2-abs(va+1j*h*pv/eta)**2)/(2*h);derr=float(np.max(abs(fd-S)));globalS=float(abs(np.sum(F.integral(S))));expanded=full.forward(full.back(force));Sfull=2/eta*np.imag(va.conj()*expanded);fullerr=float(np.max(abs(Sfull)));assert derr<1e-8 and globalS<1e-12 and fullerr<1e-12
out=dict(free_Gaussian_max_velocity_error=maxvel,free_Gaussian_trajectory_max_error=traj,projected_density_derivative_error=derr,projected_global_mass_source=globalS,product_complete_projection_local_source_max=fullerr,small_projection_local_source_max=float(np.max(abs(S))),scope='finite benchmarks, not nonlinear material survival or a four-dwarf closure');(P/'material_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
