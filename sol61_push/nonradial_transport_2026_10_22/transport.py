import argparse,json,sys
from pathlib import Path
import numpy as np
MSTAR=.08408132497418408

def field(x,m,soft):
 d=x[:,None,:]-x[None,:,:];s=np.sqrt(np.sum(d*d,axis=2)+soft**2)
 kernel=(1-(1+s)*np.exp(-s))/s**3
 np.fill_diagonal(kernel,0)
 a=-m*np.einsum('ij,ijk->ik',kernel,d)
 f=-np.expm1(-s)/s;np.fill_diagonal(f,0)
 U=-.5*m*m*np.sum(f)
 return a,U

def run(n=96,spin=.02,b=1.,dt=.04,soft=.2,end=120):
 mass=4*MSTAR*b;m=mass/n
 i=np.arange(n);r=8*np.sqrt((i+.5)/n);theta=i*np.pi*(3-np.sqrt(5))
 x=np.array([1.08*r*np.cos(theta),.92*r*np.sin(theta)]).T;x-=x.mean(axis=0)
 a,U=field(x,m,soft);omega=np.sqrt(2*spin*abs(U)/(m*np.sum(x*x)))
 v=omega*np.array([-x[:,1],x[:,0]]).T
 dt=dt/np.sqrt(b);end=end/np.sqrt(b);steps=round(end/dt)
 L0=m*(x[:,0]*v[:,1]-x[:,1]*v[:,0]);E0=U+.5*m*np.sum(v*v)
 inner=np.argsort(np.sum(x*x,axis=1))[:n//4];rows=[]
 for step in range(steps+1):
  if step%25==0 or step==steps:
   L=m*(x[:,0]*v[:,1]-x[:,1]*v[:,0]);E=U+.5*m*np.sum(v*v)
   rows.append(dict(time=step*dt,energy_error=(E-E0)/abs(E0),L_error=(sum(L)-sum(L0))/sum(L0),momentum=float(np.linalg.norm(m*v.sum(axis=0))),inner_L_fraction=float(sum(L[inner])/sum(L0)),exchange=float(sum(abs(L-L0))/(2*abs(sum(L0)))),half_radius=float(np.median(np.linalg.norm(x,axis=1)))))
  if step==steps:break
  v+=a*dt/2;x+=v*dt;a,U=field(x,m,soft);v+=a*dt/2
 return dict(n=n,spin=spin,b=b,dt=dt,soft=soft,initial_energy=E0,initial_L=float(sum(L0)),max_energy_error=max(abs(z['energy_error']) for z in rows),max_L_error=max(abs(z['L_error']) for z in rows),rows=rows,final_x=x.tolist(),final_v=v.tolist())

p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args()
cases=[run(),run(spin=.05),run(dt=.02),run(n=192),run(soft=.1),run(b=.5),run(b=2)]
a=cases[0];checks=[]
def ck(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=value))
# Finite-difference gradient versus central force: independent implementation check.
x=np.array([[.1,.2],[1.,-.3],[-.7,.4]]);m=.1;acc,U=field(x,m,.2);h=1e-6;err=[]
for i in range(3):
 for j in range(2):
  xp=x.copy();xm=x.copy();xp[i,j]+=h;xm[i,j]-=h
  err.append(abs((field(xp,m,.2)[1]-field(xm,m,.2)[1])/(2*h)+m*acc[i,j]))
ck('force_is_energy_gradient',max(err)<1e-10,max(err))
ck('central_pair_torque',abs(np.sum(x[:,0]*acc[:,1]-x[:,1]*acc[:,0]))<1e-13,float(np.sum(x[:,0]*acc[:,1]-x[:,1]*acc[:,0])))
for c in cases:
 ck('energy_n%d_spin%.2f_b%.1f_soft%.1f_dt%.3f'%(c['n'],c['spin'],c['b'],c['soft'],c['dt']),c['max_energy_error']<1e-4,c['max_energy_error'])
 ck('L_n%d_b%.1f_soft%.1f'%(c['n'],c['b'],c['soft']),c['max_L_error']<1e-10,c['max_L_error'])
for c in cases[-2:]:
 err=float(np.max(abs(np.array(c['final_x'])-np.array(a['final_x']))))
 ck('mass_similarity_b'+str(c['b']),err<1e-8,err)
err=float(np.max(abs(np.array(cases[2]['final_x'])-np.array(a['final_x']))))
ck('time_refinement_positions',err<.01,err)
# Prior spherical seeds: conditional angular momentum inventory, not a no-go theorem.
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'radiating_collapse_2026_10_22'))
from model import Model
R=np.pi/np.sqrt((np.sqrt(5)-1)/2);budgets=[]
for b in [.5,1,2,4]:
 for spin in [.02,.05]:
  model=Model(n=256,ns=128,spin=spin,mass_ratio=b);M=sum(model.mi);L=sum(model.li)
  j=np.sqrt(M*R*(1-(1+R)*np.exp(-R)))
  budgets.append(dict(mass_ratio=b,spin=spin,L=float(L),optimistic_circular_radius=R,aligned_circular_fraction_limit=float(L/(M*j)),seed_r95=float(np.quantile(model.r0,.95))))
result=dict(checks=checks,cases=cases,budgets=budgets,refinement=dict(time_position_max=err,particle_inner_L_change=cases[3]['rows'][-1]['inner_L_fraction']-a['rows'][-1]['inner_L_fraction'],soft_inner_L_change=cases[4]['rows'][-1]['inner_L_fraction']-a['rows'][-1]['inner_L_fraction']))
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
