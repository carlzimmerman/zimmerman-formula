import json,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).resolve().parent
s=json.loads((p/'sheet_run/result.json').read_text());d=json.loads((p/'transport_run/result.json').read_text());checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=v))
# Axisymmetric local ODE eigenvalues reproduce epicyclic subtraction.
k=.8;Om=.03;A=.01
mat=np.array([[0,-k,0],[-A/k,0,2*Om],[0,-Om,0]])
ev=np.sort(np.linalg.eigvals(mat));expected=np.array([-np.sqrt(A-2*Om**2),0,np.sqrt(A-2*Om**2)])
ck('axisymmetric_eigenvalues',np.max(abs(ev-expected))<1e-12,float(np.max(abs(ev-expected))))
# Selected stable and unstable shearing-wave repeats, tighter tolerance and denser sampling.
repeats=[]
for H,margin,kyfac in [(0,.3,.5),(0,1.2,.5),(1,.9,1)]:
 row=next(r for r in s['thickness'] if r['H']==H);Om=np.sqrt(margin*s['sigma_star']*row['F_peak']/4);ky=kyfac*row['k_peak'];end=8/Om
 def T(a):return (2+a)/(2*(1+a)**2)
 def rhs(t,Y):
  kx=ky*(-4+Om*t);kk=np.hypot(kx,ky);q=np.sqrt(1+kk*kk);A=s['sigma_star']/2*(kk*T(kk*H)-kk*kk/q*T(q*H))
  return [-kx*Y[1]-ky*Y[2],2*Om*Y[2]-A*kx/kk**2*Y[0],-Om*Y[1]-A*ky/kk**2*Y[0]]
 def stop(t,Y):return .1-abs(Y[0])
 stop.terminal=True;stop.direction=-1
 sol=solve_ivp(rhs,(0,end),[1e-5,0,0],rtol=2e-11,atol=1e-14,max_step=end/2000,events=stop,dense_output=True)
 amp=float(max(abs(sol.sol(np.linspace(0,sol.t[-1],8001))[0]))/1e-5)
 old=next(r for r in s['swing'] if r['H']==H and r['margin']==margin and r['ky_over_peak']==kyfac)
 err=abs(amp/old['max_amplification']-1);ck('swing_repeat_%g_%g_%g'%(H,margin,kyfac),sol.success and err<1e-4,err)
 repeats.append(dict(H=H,margin=margin,kyfac=kyfac,amplification=amp))
G=6.67430e-11;pc=3.085677581491367e16;msun=1.98847e30;a0=9.3603e-11;ell=.4404221297174536*1000*pc
M0=a0*ell*ell/G/msun;time=np.sqrt(ell/a0)/(365.25*86400*1e6);Sigma=s['sigma_star']*a0/(4*np.pi*G)*pc*pc/msun
units=dict(M0_Msun=M0,canonical_Msun=.08408132497418408*M0,sigma_star_Msun_pc2=Sigma,time_Myr=time,thin_efold_Myr=time/s['thickness'][0]['critical_kappa'])
a=d['cases'][0];n=d['cases'][3];soft=d['cases'][4]
gates=[dict(name='qualitative_torque_repeats',passed=all(abs(c['rows'][-1]['inner_L_fraction']-c['rows'][0]['inner_L_fraction'])>.1 for c in [a,n,soft])),dict(name='inner_L_distribution_one_percent_absolute',passed=abs(n['rows'][-1]['inner_L_fraction']-a['rows'][-1]['inner_L_fraction'])<.01 and abs(soft['rows'][-1]['inner_L_fraction']-a['rows'][-1]['inner_L_fraction'])<.01),dict(name='absolute_mass_selection_in_quadratic_limit',passed=False),dict(name='full_nonlinear_dwarf_rotation_growth_joint_test',passed=False)]
# Spatially compensated redistribution keeps mass and centroid: Fourier difference starts at k^2.
x=np.array(a['final_x']);x-=x.mean(axis=0);ks=[.1,1.];comp=[]
for kval in ks:
 kd=kval*.4404221297174536/1000
 u=np.exp(1j*kd*x[:,0]).mean();bound=.5*kd*kd*np.mean(x[:,0]**2)
 ck('compensated_fourier_bound_'+str(kval),abs(u-1)<=bound*(1+1e-8),dict(difference=float(abs(u-1)),bound=float(bound)))
 comp.append(dict(k_Mpc_inverse=kval,difference=float(abs(u-1)),bound=float(bound)))
result=dict(checks=checks,interpretation_gates=gates,units=units,swing_repeats=repeats,compensated_final_cloud=comp)
Path(argparse.ArgumentParser().parse_args().output if False else __import__('sys').argv[2]).write_text(json.dumps(result,indent=2)+'\n')
