import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,null_space,svdvals
import solve as m
HERE=Path(__file__).resolve().parent

def microscopic(z,Y,R,g,p,y):
 n=len(z);E=np.concatenate([np.eye(n),1j*np.eye(n)],axis=1)/math.sqrt(2);k=1/p**2
 linear=np.r_[1.+0j,np.zeros(n-1)];F=linear+.5*np.einsum('ijk,j,k->i',Y,z,z);M=np.einsum('ijk,k->ij',Y,z);W=p*y+z[0]+np.einsum('ijk,i,j,k',Y,z,z,z)/6;K=np.vdot(z,z).real;D=F+k*z.conj()*W
 W1=F@E;W2=E.T@M@E;D1=M@E+k*(W*E.conj()+np.outer(z.conj(),W1));D2=np.einsum('ijk,ja,kb->iab',Y,E,E,optimize=True)+k*(np.einsum('ia,b->iab',E.conj(),W1)+np.einsum('ib,a->iab',E.conj(),W1)+np.einsum('i,ab->iab',z.conj(),W2))
 P=np.vdot(D,D).real-3*k*abs(W)**2;P1=2*(D.conj()@D1).real-6*k*(W.conjugate()*W1).real;P2=2*(D1.conj().T@D1+np.einsum('i,iab->ab',D.conj(),D2)).real-6*k*(np.outer(W1.conj(),W1)+W.conjugate()*W2).real
 K1=2*(z.conj()@E).real;K2=np.eye(2*n);H=np.exp(k*K)*(P2+k*(np.outer(K1,P1)+np.outer(P1,K1)+K2*P)+k*k*np.outer(K1,K1)*P)
 rz=np.einsum('aij,j->ai',R,z);Lg=2*g*(E.conj().T@rz.T).real.T;H+=Lg.T@Lg
 mc=np.exp(k*K/2)*(M+k*(np.outer(z.conj(),F)+np.outer(F,z.conj()))+k*k*W*np.outer(z.conj(),z.conj()));mcU=mc-(2/3)*np.exp(k*K/2)*np.outer(D,D)/W
 J=math.sqrt(2)*g*np.einsum('i,aij->aj',z.conj(),R);MF=np.block([[mcU,J.T],[J,np.zeros((len(R),len(R)),complex)]])
 grad=np.exp(k*K)*(P1+k*K1*P)
 gi=np.exp(k*K)*( (M+k*(np.outer(z.conj(),F)+np.outer(F,z.conj()))+k*k*W*np.outer(z.conj(),z.conj()))@D.conj()-2*k*D*W.conjugate())
 ward=mcU@D.conj()-np.exp(-k*K/2)*(gi-(2/3)*D*np.exp(k*K)*P/W)
 return dict(H=H,MF=MF,D=D,W=W,V=np.exp(k*K)*P,gradient=grad,ward_residual=ward,mcU=mcU,gi=gi)

def main(path):
 start=time.monotonic();d=json.load(open(HERE/'run_highprecision/result.json'));p=d['export']['parameters'];e=float(p['e']);t=float(p['t']);X=float(m.X0)*t;mu=float(p['mu']);P=float(p['p']);y=float(p['y']);u=float(p['u']);v=float(p['v']);g=math.sqrt(29/200)*e
 base=m.build_model(X,e,e,g,vertices=False);Y=base['Y'];R=base['R'];z=base['z'].copy();z[1:25]*=1+u/float(m.A0);z[25:]*=1+v/X
 sg=microscopic(z,Y,R,g,P,y);ev,O=eigh(base['H']);massscale=max(ev);null=abs(ev)<1e-10*massscale;B=O[:,~null];scalarheavy=eigh(B.T@sg['H']@B,eigvals_only=True)
 Gold=np.r_[sg['D'],np.zeros(24)];Q=null_space(Gold[None,:]);MFred=Q.T@sg['MF']@Q;ferm=svdvals(MFred);fs=ferm[ferm>1e-9*max(ferm)];fv=np.sqrt(base['mV2'][base['mV2']>0]);nullf=int(sum(ferm<=1e-9*max(ferm)))
 # Independent directional check of the exact canonical tree Hessian using
 # high precision D-flat microscopic variables, not the tensor implementation.
 # r_a=sqrt60 deltaa, r_b=sqrt60 deltab, r_X=sqrt2 deltaX.
 b0=X;aa=float(m.A0)+u;bb=X+v
 va=np.r_[np.zeros(1),-base['z'][1:25].imag/float(m.A0)/math.sqrt(30),np.zeros(24),np.zeros(49)] # ReA not a; use direct real embedding below
 avec=np.r_[np.zeros(49),np.r_[0.,base['z'][1:25].imag/float(m.A0),np.zeros(24)]]/math.sqrt(30)
 bvec=np.r_[np.r_[0.,np.zeros(24),base['z'][25:].real/X],np.zeros(49)]/math.sqrt(30)
 import mpmath as mp
 mp.mp.dps=80;s=mp.log(mp.mpf(p['t']));uu=mp.mpf(p['u']);vv=mp.mpf(p['v']);pp=mp.mpf(p['p']);yy=mp.mpf(p['y'])
 Ha=mp.diff(lambda q:m.sg(s,q,vv,pp,yy),uu,2)/60;Hb=mp.diff(lambda q:m.sg(s,uu,q,pp,yy),vv,2)/60
 herrors=[abs(float(Ha)-float(avec@sg['H']@avec)),abs(float(Hb)-float(bvec@sg['H']@bvec))]
 # Explicit anomaly terms are quoted only as a specified UV counterterm.
 # Their matching to a complete IR 1PI mass is a separate obligation.
 m32=d['candidate']['m32_GeV'];KiFi=-mu*np.exp(np.vdot(z,z).real/(2*P*P))*np.dot(z.conj(),sg['D'].conj())/(P*P);ct=-g*g/(16*math.pi**2)*(5*m32-5*KiFi.real)
 envelope=100*g*g*m32/(16*math.pi**2)
 checks=dict(scalar_heavy_count_84=len(scalarheavy)==84,heavy_scalar_positive=min(scalarheavy)>0,fermion_heavy_count_60=len(fs)==60,unbroken_gaugino_count12=nullf==12,scalar_tensor_vs_microscopic=max(herrors)<1e-12,tree_Ward_algebra=np.max(abs(sg['ward_residual']))<1e-14)
 checks={key:bool(value) for key,value in checks.items()}
 out=dict(claim_id='CANONICAL_TREE_TRANSVERSE_AND_SUPERHIGGS_DIAGNOSTIC',checks=checks,heavy_scalar_masses_GeV=list(map(float,np.sqrt(scalarheavy)*mu)),heavy_fermion_masses_GeV=list(map(float,sorted(fs*mu))),massive_vector_masses_GeV=list(map(float,fv*mu)),heavy_scalar_min_GeV=float(np.sqrt(min(scalarheavy))*mu),heavy_fermion_min_GeV=float(min(fs)*mu),raw_tree_light_and_gauge_eigenvalues_GeV2=list(map(float,eigh(sg['H'],eigvals_only=True)[:14]*mu*mu)),tree_gradient_norm_dimensionless=float(np.linalg.norm(sg['gradient'])),tree_projected_Goldstino_mass_residual_dimensionless=float(np.linalg.norm(sg['mcU']@sg['D'].conj())/np.linalg.norm(sg['D'])),tree_Ward_algebra_residual=float(np.max(abs(sg['ward_residual']))),Hessian_normal_check_absolute_errors=herrors,UV_SU5_anomaly_counterterm_GeV=float(ct),UV_counterterm_relative_photino=float(ct/d['candidate']['gauginos_GeV']['U1']),coefficient100_gravity_matching_scale_GeV=envelope,coefficient100_relative_photino=envelope/d['candidate']['gauginos_GeV']['U1'],runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['84 heavy scalar positivity is the microscopic TREE SUGRA transverse diagnostic; full transverse CW/V2 self-energies are not computed here.','The12 raw gauge/2 retained eigenvalues of the tree-offshell Hessian are not physical light poles.','Projection orthogonal to tree D_iW is a tree diagnostic at this loop-stationary point, not a loop-consistent super-Higgs certificate.','Coefficient100 is an explicit sensitivity scale, not a rigorous bound on uncomputed gravitational matching.','The quoted UV anomaly counterterm is not by itself the full finite IR threshold-corrected photino pole mass.'])
 Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('checks','heavy_scalar_min_GeV','heavy_fermion_min_GeV','tree_projected_Goldstino_mass_residual_dimensionless','UV_SU5_anomaly_counterterm_GeV','coefficient100_relative_photino','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
