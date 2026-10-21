"""Five-amplitude bulk spectrum of explicit alternative common matter action."""
from pathlib import Path
import json,math,sys,resource
import numpy as np
B=Path(__file__).resolve().parents[1]
par=json.loads((B/'run_001/results.json').read_text())['parameters']
co=json.loads((B/'run_003/results.json').read_text())['coexistence']
f=math.sqrt(co['I']);h=co['chi'];b=co['X'];om=co['omega'];a=par['a'];M=par['M_chi'];g=par['g'];lam=par['lambda'];MX2=par['MX2'];checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 assert v,n
D=MX2-4*om*om;Bh=M*M-.75*M*h+3*h*h;Aeff=lam-g*g/D
Vu=1-om*om+6*lam*f*f+a*h+2*g*b
Vv=1-om*om+2*lam*f*f+a*h-2*g*b
W0=np.diag([Vu,Vv,D,D,Bh]);W0[0,2]=W0[2,0]=2*g*f;W0[1,3]=W0[3,1]=2*g*f;W0[0,4]=W0[4,0]=math.sqrt(2)*a*f
Gy=np.zeros((5,5));Gy[0,1]=-2*om;Gy[1,0]=2*om;Gy[2,3]=-4*om;Gy[3,2]=4*om
phase=np.array([0,math.sqrt(2)*f,0,2*math.sqrt(2)*b,0])
ck('symmetric canonical stiffness',np.max(np.abs(W0-W0.T))==0)
ck('antisymmetric gyroscopic matrix',np.max(np.abs(Gy+Gy.T))==0)
ck('homogeneous Psi field equation',abs(1-om*om+2*lam*f*f+a*h+2*g*b)<1e-9)
ck('homogeneous X field equation',abs(D*b+g*f*f)<1e-10)
ck('homogeneous neutral field equation',abs(M*M*h-3*M*h*h/8+h**3+a*f*f)<1e-8)
ck('U1 phase vector null',np.linalg.norm(W0@phase)<1e-8*np.linalg.norm(phase))
ck('positive neutral and charged-X stiffness',Bh>0 and D>0)
Schur=2*f*f*(2*Aeff-a*a/Bh)
amp=W0[np.ix_([0,2,4],[0,2,4])]
phaseblock=W0[np.ix_([1,3],[1,3])]
ck('positive amplitude Schur complement',Schur>0)
ck('amplitude block positive',np.linalg.eigvalsh(amp)[0]>0)
ck('phase block neutral PSD',np.linalg.eigvalsh(phaseblock)[0]>-1e-10 and abs(np.linalg.det(phaseblock))<1e-9)
ck('Vu equals4lambdaI on stationary background',abs(Vu-4*lam*f*f)<1e-9)
ck('phase diagonal equalsminus4gb',abs(Vv+4*g*b)<1e-9)
rows=[]
for k in [0.,.001,.01,.1,1.,10.,100.]:
 W=W0+k*k*np.eye(5)
 lin=np.block([[np.zeros((5,5)),np.eye(5)],[-W,-Gy]])
 H=np.block([[W,np.zeros((5,5))],[np.zeros((5,5)),np.eye(5)]])
 hamres=np.linalg.norm(lin.T@H+H@lin,ord=np.inf)
 eig=np.linalg.eigvals(lin)
 idx=np.argsort(np.abs(eig));low=eig[idx[:2]]
 nonzero=eig[np.abs(eig)>2e-5]
 maxreal=float(max(abs(nonzero.real))) if len(nonzero) else 0.
 if k==0:
  ck('k0 two neutral numerical eigenvalues',len(eig[np.abs(eig)<=2e-5])==2)
 else:ck('positive W at k='+str(k),np.linalg.eigvalsh(W)[0]>0)
 ck('imaginary nonzero spectrum k='+str(k),maxreal<1e-8)
 ck('quadratic fluctuation energy identity k='+str(k),hamres<1e-10)
 record={'k':k,'W_eigenvalues':np.linalg.eigvalsh(W).tolist(),'firstorder_eigenvalues_real_imag':[[float(x.real),float(x.imag)] for x in sorted(eig,key=lambda z:(abs(z.imag),z.imag))],'max_abs_real_part_nonzero_spectrum':maxreal,'low_pair_real_imag':[[float(x.real),float(x.imag)] for x in low],'quadratic_energy_identity_infinity_norm':hamres}
 if k>0:
  record['Goldstone_frequency_squared_over_k_squared']=float(-np.real(low[0]*low[0])/(k*k))
 rows.append(record)
cs=rows[1]['Goldstone_frequency_squared_over_k_squared'];cs_therm=co['long_wavelength_adiabatic_cs2']
ck('Goldstone sound agrees corrected thermodynamics',abs(cs/cs_therm-1)<1e-4)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below200MB',rss<200000000)
result={'scope':'Finite homogeneous linear spectrum only; exact conditional energy argument is separate. No nonlinear/inhomogeneous/soliton stability or transport completion.','normalization':'canonical amplitudes sqrt2u,sqrt2v,sqrt2s,sqrt2t,xi','background':co,'parameters':par,'W0':W0.tolist(),'gyroscopic_matrix':Gy.tolist(),'phase_null_vector':phase.tolist(),'amplitude_Schur_complement':Schur,'amplitude_eigenvalues':np.linalg.eigvalsh(amp).tolist(),'phase_block_eigenvalues':np.linalg.eigvalsh(phaseblock).tolist(),'rows':rows,'Goldstone_cs2_finite_k':cs,'Goldstone_cs2_thermodynamic':cs_therm,'Goldstone_cs2_relative_difference':abs(cs/cs_therm-1),'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),'peak_rss_bytes_macos':rss,'zero_mode_scope':'At k0 the expected neutral zero pair is classified by the predeclared2e-5 cluster threshold; its printed tiny real splitting is not treated as an exponential instability. Exact phase residual and PSD algebra are separately checked.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'Schur':Schur,'cs2_mode':cs,'cs2_thermo':cs_therm,'relative':abs(cs/cs_therm-1),'RSS':rss,'max_real_nonzero':max(x['max_abs_real_part_nonzero_spectrum'] for x in rows),'k0_low':rows[0]['low_pair_real_imag']}))
