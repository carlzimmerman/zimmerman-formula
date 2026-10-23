"""Audit omitted reaction on OLD conditional trajectory; no new matching epoch."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import trapezoid
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
# Reuse audited moment definitions, not the script's run loop.
ns={'__file__':str(P/'thermal_recycling_evolution.py'),'__name__':'definitions'}
exec(compile((P/'thermal_recycling_evolution.py').read_text().split('\ncases={}')[0],'thermal_recycling_evolution.py','exec'),ns)
r=json.loads((P/'bath_assisted_conversion_run/results.json').read_text());rows=r['rates'];theta=np.array([x['T_over_m'] for x in rows]);D0=r['threshold']['D_GeV_minus5'];interp=PchipInterpolator(np.log(theta),np.log([x['D_MB_GeV_minus5'] for x in rows]))
def D(T):
 t=np.asarray(T)/.001
 return np.where(t<theta[0],D0*np.exp(np.log(rows[0]['D_MB_GeV_minus5']/D0)*t/theta[0]),np.exp(interp(np.log(np.maximum(t,theta[0])))))
a=np.genfromtxt(P/'thermal_recycling_dense_run/full.csv',delimiter=',',names=True)
N=a['N'];T=a['T'];eta=a['eta'];n=a['nPhi'];nx=a['nX'];W=n+2*nx;H=ns['Hs']*np.exp(-2*N);alpha=eta+.001/T
pref=D(T)*nx*n*n;loss=pref*(-np.expm1(-2*alpha));omittedY=trapezoid(loss/H*np.exp(3*N)/ns['svis'],N)
C,sv=ns['rate'](.0005);n0,nx0,W0,U0,P0,J=ns['state'](.0005,-2.)
# At fixed rho, transform a unit dW into (dlogT,deta), then d alpha.
dy=np.linalg.solve(J,np.array([1.,-.001]));dalpha=np.dot(np.array([-2.,1.]),dy)
p0=float(D(.0005)*nx0*n0*n0);old=.5*sv*nx0**2+C*n0**4
# Species order Phi+,Phi-,X+,X-; rows reactions' net number changes.
S=np.array([[2,0,-1,0],[0,2,0,-1],[1,-1,-1,0],[-1,1,0,-1]])
Q=np.array([1,-1,2,-2]);weight=np.array([1,1,2,2])
flux=[]
for folder,name in [('coupled_fragmentation_96_run','fine96'),('late_conversion_96_run','space96')]:
 header=np.fromfile(P/folder/(name+'_initial.bin'),dtype='<f8',count=9);size=int(header[0]);L,dt,z,b,mp,mx,c,quart=header[1:]
 q,v=np.fromfile(P/folder/(name+'_final.bin'),dtype='<f8').reshape(2,4,size,size,size);scale=1+b*z
 # Physical kinetic uses v - (a'/a)q. Flip that, holding q fixed.
 w=v-b/scale*q;vp=2*b/scale*q-v;wp=vp-b/scale*q
 F=q[0]**2-q[1]**2;G=2*q[0]*q[1]
 transfer=-c*scale*np.mean(w[2]*F+w[3]*G)
 reverse=-c*scale*np.mean(wp[2]*F+wp[3]*G)
 kin=.5*np.mean(np.sum(w*w,axis=0));kinrev=.5*np.mean(np.sum(wp*wp,axis=0))
 charge=np.mean(q[0]*w[1]-q[1]*w[0]+2*(q[2]*w[3]-q[3]*w[2]))
 # Hartree/free-field closure not used to infer temperature from these states.
 flux.append(dict(run=folder,interaction_source_conformal_units=float(transfer),time_reversed_source=float(reverse),kinetic_energy_relative_difference=float(abs(kinrev-kin)/kin),charge_conformal=float(charge),source_reversal_relative_error=float(abs(reverse+transfer)/max(abs(transfer),1e-100))))
checks=dict(stoichiometry_rank_three=np.linalg.matrix_rank(S)==3,charge_conserved=np.all(S@Q==0),weighted_number_broken=np.array_equal(S@weight,[0,0,-2,-2]),time_reversal_energy=all(x['kinetic_energy_relative_difference']<1e-12 for x in flux),time_reversal_flux=all(x['source_reversal_relative_error']<1e-8 for x in flux),chemical_relaxation_positive=dalpha>0)
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),old_conditional_trajectory_diagnostic=dict(start_new_to_old_forward_loss_prefactor=p0/old,start_new_chemical_relaxation_over_H=2*p0*dalpha/ns['Hs'],start_old_chemical_relaxation_over_H=2*old*dalpha/ns['Hs'],integrated_omitted_loss_Y_on_UNCHANGED_old_path=float(omittedY),omitted_loss_over_old_final_Y=float(omittedY/a['Yweighted'][-1]),warning='Perturbation diagnostic only. Do not subtract this number to claim a corrected yield: populations and temperature must respond.'),saved_state_phase_audit=flux,scope='Kernel and state-information audit. No inferred thermalization epoch, seed, quantum cumulant propagation, or final surviving abundance.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
