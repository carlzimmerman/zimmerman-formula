"""Full two-field classical evolution in 1D periodic box, per transverse area.
Tests nonlinear growth and internal energy/charge accounting, not 3D Q-balls.
"""
import sys,json,math,time
from pathlib import Path
import numpy as np
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
parent=json.loads((base/'four_gap_audit_run_003/results.json').read_text())
med=json.loads((base/'mediator_phase_matching_run_002/results.json').read_text())
phase=next(x for x in med['rows'] if x['M_over_m']==10)
M=10.;L=1.9;a=20.;mu=-3.75;I0=.5*phase['phase_I_exact'];omega=next(x['omega'] for x in parent['formation_rows'] if x['M_over_m']==M and x['I_fraction_of_coexistence']==.5)
# Solve mediator stationarity with NumPy's polynomial roots.
chi0=float([z.real for z in np.roots([1,mu,M*M,a*I0]) if abs(z.imag)<1e-10][0])
box=64*math.pi;mode=10;k=2*math.pi*mode/box;delta=1e-4;end=220.
checks=[];runs=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
for nodes,dt in ((256,.01),(256,.005),(512,.005)):
 dx=box/nodes;x=np.arange(nodes)*dx;cos=np.cos(k*x)
 kd=2*math.sin(k*dx/2)/dx;Ar=4*L*I0;Bh=M*M+2*mu*chi0+3*chi0*chi0;h=a*math.sqrt(2*I0)
 K=np.array([[kd*kd+Ar,0,h],[0,kd*kd,0],[h,0,kd*kd+Bh]])
 gyro=np.array([[0,-2*omega,0],[2*omega,0,0],[0,0,0]])
 generator=np.block([[np.zeros((3,3)),np.eye(3)],[-K,-gyro]])
 eig,vec=np.linalg.eig(generator);which=int(np.argmax(eig.real));growth=float(eig[which].real);v=vec[:,which].real;v*=math.sqrt(2*I0)/v[0]
 psi=math.sqrt(I0)+delta*(v[0]+1j*v[1])/math.sqrt(2)*cos
 vel=1j*omega*psi+delta*(v[3]+1j*v[4])/math.sqrt(2)*cos
 chi=chi0+delta*v[2]*cos;chivel=delta*v[5]*cos
 def lap(q):return (np.roll(q,1)-2*q+np.roll(q,-1))/(dx*dx)
 def acceleration(pp,cc):
  ii=abs(pp)**2
  return lap(pp)-(1+2*L*ii+a*cc)*pp,lap(cc)-(M*M*cc+mu*cc*cc+cc**3+a*ii)
 def observe(t):
  ii=abs(psi)**2;potential=ii+L*ii*ii+a*chi*ii+.5*M*M*chi*chi+mu*chi**3/3+chi**4/4
  kinetic=float(dx*np.sum(abs(vel)**2+.5*chivel**2))
  gradient=float(dx*np.sum(abs(np.roll(psi,-1)-psi)**2+.5*(np.roll(chi,-1)-chi)**2)/(dx*dx))
  pot=float(dx*np.sum(potential));energy=kinetic+gradient+pot
  number=float(dx*np.sum(2*np.imag(np.conj(psi)*vel)))
  mode_amp=float(abs(np.fft.rfft(ii)[mode])*2/nodes/I0)
  return {'t':t,'energy':energy,'charge':number,'kinetic':kinetic,'gradient':gradient,'potential':pot,
   'peak_I_over_initial':float(np.max(ii)/I0),'min_I_over_initial':float(np.min(ii)/I0),'density_relative_std':float(np.std(ii)/np.mean(ii)),
   'density_mode_fraction':mode_amp,'mediator_kinetic':float(dx*np.sum(.5*chivel**2))}
 samples=[observe(0.)];acc,chiacc=acceleration(psi,chi);steps=round(end/dt);stride=round(1/dt)
 for step in range(steps):
  vel+=.5*dt*acc;chivel+=.5*dt*chiacc
  psi+=dt*vel;chi+=dt*chivel
  acc,chiacc=acceleration(psi,chi)
  vel+=.5*dt*acc;chivel+=.5*dt*chiacc
  if (step+1)%stride==0:samples.append(observe((step+1)*dt))
 early=[r for r in samples if 10<=r['t']<=70]
 fitted=float(np.polyfit([r['t'] for r in early],np.log([r['density_mode_fraction'] for r in early]),1)[0])
 E0=samples[0]['energy'];N0=samples[0]['charge']
 Eerr=max(abs(r['energy']/E0-1) for r in samples);Nerr=max(abs(r['charge']/N0-1) for r in samples)
 check('energy conservation '+str((nodes,dt)),Eerr<.002)
 check('charge conservation '+str((nodes,dt)),Nerr<1e-10)
 check('linear eigenmode growth '+str((nodes,dt)),abs(fitted/growth-1)<.03)
 # Nonlinearity and clumping are results, not forced physical success flags.
 row={'nodes':nodes,'dt':dt,'box_length':box,'end_time':end,'mass':M,'initial_I':I0,'omega':omega,'chi0':chi0,
  'seed_relative_amplitude':delta,'seed_mode':mode,'wave_number':k,'lattice_wave_number':kd,'predicted_lattice_growth':growth,'fitted_early_growth':fitted,
  'max_energy_relative_error':Eerr,'max_charge_relative_error':Nerr,'max_peak_I_over_initial':max(r['peak_I_over_initial'] for r in samples),
  'max_density_relative_std':max(r['density_relative_std'] for r in samples),'nonlinear_contrast_exceeds_one':bool(max(r['density_relative_std'] for r in samples)>1),
  'samples':samples}
 runs.append(row)
 np.savez_compressed(out/('final_N'+str(nodes)+'_dt'+str(dt)+'.npz'),x=x,psi=psi,psi_dot=vel,chi=chi,chi_dot=chivel)
result={'checks':checks,'runs':runs,'weak_scaling':'Same classical rescaled dynamics for epsilon version; charge/energy multiply1/epsilon, not derived abundance',
 'non_claims':['1D periodic box per transverse area; no isolated 3D body, interface completion, outgoing-boundary radiation or final Q-ball classification','Specified initial coherent charge and seed; not neutral thermal production or actual cosmological formation','No physical gravity response or quantum loops evolved','Late profile convergence not implied by early growth/budget checks; emitted waves remain in box']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'controls':len(checks),'summaries':[{k:v for k,v in r.items() if k!='samples'} for r in runs]},indent=2))
