import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from vertex import vertex,equal_resonance
from fine_material import PhysicalFull
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=PhysicalFull();a=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz')['a'];idx=np.argmin(abs(m.r*m.rm-30));rho=abs(a[0,idx])**2/m.vol[idx];u=m.enclosed(abs(a[0])**2)[idx];c=m.c;g=1716.802731965808;rows=[]
# On-shell cancellation benchmark of the exactly free Schrodinger field.
z=vertex([3.,0.,0.],[0.,4.,0.],rho,0.,m.k,1.);free_error=abs(z['V'])/max(abs(z['V_velocity']),1e-30);assert free_error<1e-12
for q in [3.,10.,20.,80.]:
 R=4*np.pi/q;vol=R**3/3;k1,k2=equal_resonance(q,rho,u,m.k);v=vertex(k1,k2,rho,u,m.k,vol);om=v['omega'];A=v['A'];gap=rho*(1/(1-u)-1);d=np.sqrt(1+3*gap/(m.k*q**4));stable=q*q*np.sqrt(d)*(d+1)/(4*A[0]*np.sqrt(vol))*gap/om[0]**2;assert abs(stable-v['V'].real)/stable<1e-8
 N=.1**2*rho**2*vol/(64*A[0]**2);tau=1/(stable*np.sqrt(N));D=1.2/R;group=[np.array([0,1]),np.array([2])];alphas=[];gammas=[]
 for ids in group:
  w=om[ids[0]];x=2*w*R/c;F=3*(np.sin(x)-x*np.cos(x))/x**3;alphas.append(16*g*g*w*w*D/c**2*N*tau);gammas.append(32*g*g*w**3/c**3*F*F*N*tau)
 def rhs(t,y):
  z=(y[:6]+1j*y[6:12]).reshape(2,3);dz=np.zeros((2,3),complex)
  for sign in range(2):
   b=z[sign];dz[sign]=[-1j*np.conj(b[1])*b[2],-1j*np.conj(b[0])*b[2],-1j*b[0]*b[1]]
  loss=0.
  for ids,alpha,gamma in zip(group,alphas,gammas):
   O=np.sum(A[ids]**2*z[0,ids]*z[1,ids]);loss+=4*om[ids[0]]*gamma*abs(O)**2
   for sign in range(2):dz[sign,ids]+=(1j*alpha-gamma)*A[ids]**2*np.conj(z[1-sign,ids])*O
  return np.r_[dz.ravel().real,dz.ravel().imag,loss]
 z0=np.array([[1.,1.,0.],[1.,1.,0.]],complex);y0=np.r_[z0.ravel().real,z0.ravel().imag,0.];sol=solve_ivp(rhs,[0,5],y0,method='BDF',rtol=2e-8,atol=2e-10);zz=(sol.y[:6]+1j*sol.y[6:12]).reshape(2,3,-1);en=np.sum(om[None,:,None]*abs(zz)**2,axis=(0,1));E0=en[0];error=float(np.max(abs(en+sol.y[12]-E0))/E0);assert sol.success and error<2e-4
 rows.append({'q':q,'local_radius_kpc':float(m.r[idx]*m.rm),'patch_radius_kpc':R*m.rm,'angle_degrees':float(np.degrees(np.arccos(k1@k2/q**2))),'parent_angular_frequency_per_Myr':float(om[0]/m.tdyn),'vertex':stable,'uncancelled_velocity_vertex':float(v['V_velocity']),'cancellation_factor':float(gap/om[0]**2),'pump_amplitude_density_fraction_bound':.1,'coherent_transfer_time_Myr':tau*m.tdyn,'elapsed_Myr':5*tau*m.tdyn,'max_daughter_energy_fraction':float(np.max(om[2]*np.sum(abs(zz[:,2])**2,axis=0))/E0),'escaped_fraction':float(sol.y[12,-1]/E0),'secular_energy_relative_error':error,'max_reactive_frequency_shift_over_parent':float(2*alphas[0]*A[0]**4/(tau*om[0])),'daughter_compactness':float(2*om[2]*R/c),'steps':len(sol.t)})
out={'rhoT':float(rho),'uT':float(u),'free_Schrodinger_on_shell_vertex_relative_error':float(free_error),'rows':rows,'scope':'Local specified3D WKB pure-T continuation, weak resonant triads with depleted pumps and compact reciprocal scalar reaction/loss. Initial weak modes are not derived infall occupations. No interface, outer phase or galaxy formation test; long calculated times are not universal bounds.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
