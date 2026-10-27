import json,sys
from pathlib import Path
import numpy as np
N=64;RMIN=2.;CORE=(np.sqrt(17)-1)/2;TOTAL=5.;DM=(TOTAL-CORE)/N
low=CORE+DM*np.arange(N);high=low+DM
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
def w(x):
 x=np.asarray(x)
 if np.any(x>=1):raise ValueError('full saturation wall')
 z=np.empty_like(x);sm=x<.05
 z[sm]=sum(x[sm]**i/i for i in range(3,25))
 z[~sm]=-x[~sm]**2/2-x[~sm]-np.log1p(-x[~sm]);return z
def force(r):
 order=np.argsort(r);rs=r[order]
 if np.any(rs<=RMIN):raise ValueError('prescribed core touched')
 ui=low/rs**2;uo=high/rs**2
 av=(w(uo)-w(ui))/(uo-ui);a=np.empty(N);a[order]=-1/rs**2+av
 return a
nodes,weights=np.polynomial.legendre.leggauss(96)
def energy(r,v):
 rs=np.sort(r);bounds=np.r_[0.,1/rs[::-1],1/RMIN];mass=np.r_[high[::-1],CORE]
 lo,hi=bounds[:-1],bounds[1:];q=(hi+lo)[:,None]/2+(hi-lo)[:,None]*nodes/2
 field=np.sum((hi-lo)/2*np.sum(weights*w(mass[:,None]*q*q)/q**4,axis=1))
 return float(DM*np.sum(v*v)/2-DM*np.sum(1/r)+field)
lo=np.sqrt(high)*(1+1e-12);hi=np.maximum(high+2,2*lo)
for _ in range(100):
 mid=(lo+hi)/2;ui=low/mid**2;uo=high/mid**2
 ff=-1/mid**2+(w(uo)-w(ui))/(uo-ui)
 lo=np.where(ff>0,mid,lo);hi=np.where(ff>=0,hi,mid)
eq=(lo+hi)/2
check('equilibrium full force',np.max(abs(force(eq))*eq**2)<1e-10,float(np.max(abs(force(eq))*eq**2)))
for i in [0,40,63]:
 hh=eq[i]*1e-5;p=eq.copy();p[i]+=hh;m=eq.copy();m[i]-=hh
 fd=-(energy(p,np.zeros(N))-energy(m,np.zeros(N)))/(2*hh*DM)
 check('full field derivative packet%d'%i,abs(fd-force(eq)[i])<1e-7,float(abs(fd-force(eq)[i])))
def run(dt,kick):
 r=eq.copy();v=np.zeros(N)
 if kick:v[40:48]=.8
 e0=energy(r,v);ground=energy(eq,np.zeros(N));injected=e0-ground
 a=force(r);maxde=0.;crossings=0;prev=np.argsort(r);samples=[]
 for it in range(round(200/dt)):
  v+=dt*a/2;r+=dt*v;a=force(r);v+=dt*a/2
  order=np.argsort(r)
  crossings+=int(np.count_nonzero(order!=prev));prev=order
  if it%round(1/dt)==0:
   ee=energy(r,v);maxde=max(maxde,abs(ee-e0))
   if it%round(20/dt)==0:samples.append(dict(t=(it+1)*dt,energy=ee,kinetic=DM*float(np.sum(v*v))/2,maxr=float(max(r))))
 ef=energy(r,v);maxde=max(maxde,abs(ef-e0))
 check('trajectory energy dt%g kick%s'%(dt,kick),maxde<1e-4*max(injected,1e-6),maxde)
 return dict(dt=dt,kick=kick,r=r.tolist(),v=v.tolist(),initial_energy=e0,initial_ground_energy=ground,
  injected_energy=injected,final_energy=ef,max_energy_error=maxde,
  total_kinetic=DM*float(np.sum(v*v))/2,ordering_change_count=crossings,
  far_outward_packet_count=int(np.count_nonzero((r>50)&(v>0))),samples=samples)
cold=run(.004,False);check('cold stays equilibrium',np.max(abs(np.array(cold['r'])/eq-1))<1e-8)
coarse=run(.004,True);fine=run(.002,True)
diff=float(np.max(abs(np.array(coarse['r'])-np.array(fine['r']))))
print(json.dumps(dict(label_radius_difference=diff,sorted_radius_difference=float(np.max(abs(np.sort(coarse['r'])-np.sort(fine['r'])))),coarse_summary={k:coarse[k] for k in ['max_energy_error','total_kinetic','far_outward_packet_count']},fine_summary={k:fine[k] for k in ['max_energy_error','total_kinetic','far_outward_packet_count']}),indent=2))
Path(sys.argv[1]).write_text(json.dumps(dict(cold=cold,coarse=coarse,fine=fine,label_radius_difference=diff),indent=2)+'\n')
check('trajectory resolution',diff<.01,diff)
check('far outward count resolution',coarse['far_outward_packet_count']==fine['far_outward_packet_count'])
out=dict(checks=checks,N=N,core=CORE,total_supply=TOTAL,packet_mass=DM,cold=cold,coarse=coarse,fine=fine,
 scope='Finite full-force shell experiment with fixed core, no removal/reflection; far-outward classification is not asymptotic escape or formation.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:fine[k] for k in ['injected_energy','max_energy_error','total_kinetic','ordering_change_count','far_outward_packet_count']},indent=2))
