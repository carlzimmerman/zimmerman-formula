"""Exploratory spherical-gravity, 3D DSMC halo formation; target used only in diagnostics."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[key]='1'
import ast,json,math,time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid
p=Path(__file__).parent;root=p.parents[1]
p626=root/'campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target'
c=json.loads((p626/'cfg626_results_mono.json').read_text())['cells']['MW_can']
# Read-only extraction of target functions. They never enter forces or collisions.
ns={'np':np}
def selected(path,names):
    nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
selected(p626/'cfg626.py',['h_rar','dh_rar','nu_m1_mono'])
y=10**np.linspace(-12,12,240001);yp=brentq(lambda t:float(ns['dh_rar'](t)),1,5);hp=float(ns['h_rar'](yp))
dh=np.maximum(ns['dh_rar'](y),.05*hp/(y+yp));hm=float(ns['h_rar'](y[0]))+np.r_[0,np.cumsum(.5*(dh[1:]+dh[:-1])*np.diff(y))]
ns.update(LYG=np.log10(y),H_MONO=hm,nu_m1=ns['nu_m1_mono'])
selected(root/'campaign_fresh_gravity/CFG544_settling_kinetic_consistency/cfg544.py',['Mb_enc','Mph_enc'])
M=c['Mcat'];eps=.01;Gsi=6.67430e-11;Rsi=c['rstar_kpc']*3.085677581491367e19;Vsi=c['Vf_kms']*1000
sigma_unit=.4*Vsi**2/(Gsi*Rsi) # 4 cm²/g = .4 m²/kg.
rg=np.geomspace(1e-7,1e5,50000);gb=ns['Mb_enc'](c,rg)*rg/(rg*rg+eps*eps)**1.5
integ=cumulative_trapezoid(gb,rg,initial=0);phib=integ-integ[-1]-c['Mb']/rg[-1]
rrscore=np.geomspace(.03,1,60);target=np.asarray(ns['Mph_enc'](c,rrscore));target=np.minimum(target,M)
checks=[]
def ck(name,b):checks.append(dict(name=name,passed=bool(b)))
def force(pos,mp):
    r=np.linalg.norm(pos,axis=1);order=np.argsort(r);rank=np.empty(len(r));rank[order]=np.arange(len(r))
    enc=mp*rank+ns['Mb_enc'](c,r)
    return -pos*(enc/(r*r+eps*eps)**1.5)[:,None]
def energy(pos,vel,mp):
    r=np.sort(np.linalg.norm(pos,axis=1));K=.5*mp*np.sum(vel*vel)
    Wc=-mp*mp*np.sum(np.arange(len(r))/np.sqrt(r*r+eps*eps))
    Wb=mp*np.sum(np.interp(np.log(r),np.log(rg),phib))
    return float(K+Wc+Wb),float(K),float(Wc),float(Wb)
def collide(pos,vel,mp,dt,h,rng):
    # Randomly shifted Cartesian cells; random disjoint pairs, unbiased Ncell-1 multiplicity.
    cell=np.floor(pos/h+rng.random(3)).astype(np.int64)
    _,inv,count=np.unique(cell,axis=0,return_inverse=True,return_counts=True)
    order=np.lexsort((rng.random(len(pos)),inv));ids=inv[order]
    starts=np.r_[0,np.where(np.diff(ids))[0]+1];ends=np.r_[starts[1:],len(order)]
    aa=[];bb=[];mult=[]
    for start,end in zip(starts,ends):
        n=end-start
        if n<2:continue
        z=order[start:end];pairs=n//2
        aa.extend(z[:2*pairs:2]);bb.extend(z[1:2*pairs:2]);mult.extend([n if n%2 else n-1]*pairs)
    if not aa:return 0,0.,0.,0.
    aa=np.asarray(aa);bb=np.asarray(bb);w=vel[aa]-vel[bb];speed=np.linalg.norm(w,axis=1)
    x=(speed*Vsi/(2*299792458.*.01))**2
    if np.any(x>=.5):raise RuntimeError('sampled relative speeds leave declared below-resonance domain')
    ratio=((2-x/(1-x))/2)**2/(1+.01**2*x)
    prob=mp*sigma_unit*ratio*speed*dt*np.asarray(mult)/h**3
    if prob.max()>.1:
        substeps=int(math.ceil(float(prob.max())/.05))
        reports=[collide(pos,vel,mp,dt/substeps,h,rng) for _ in range(substeps)]
        return sum(z[0] for z in reports),max(z[1] for z in reports),max(z[2] for z in reports),max(z[3] for z in reports)
    hit=rng.random(len(aa))<prob;aa=aa[hit];bb=bb[hit];w=w[hit];speed=speed[hit]
    if not len(aa):return 0,float(prob.max()),0.,float(x.max())
    before=float(np.sum(vel[aa]**2)+np.sum(vel[bb]**2));mom=vel[aa]+vel[bb]
    direction=rng.normal(size=(len(aa),3));direction/=np.linalg.norm(direction,axis=1)[:,None]
    vel[aa]=mom/2+speed[:,None]*direction/2;vel[bb]=mom/2-speed[:,None]*direction/2
    err=abs(float(np.sum(vel[aa]**2)+np.sum(vel[bb]**2))-before)
    return len(aa),float(prob.max()),err,float(x.max())
# A finite-difference Hamiltonian force check away from shell crossings.
rng=np.random.default_rng(11);z=rng.normal(size=(32,3));v=np.zeros_like(z);mp=M/32
f=force(z,mp);step=1e-5;zp=z.copy();zm=z.copy();zp[5,0]+=step;zm[5,0]-=step
num=-(energy(zp,v,mp)[0]-energy(zm,v,mp)[0])/(2*step*mp)
ck('force matches shell Hamiltonian',abs(num-f[5,0])<1e-5)

def run(name,N,dt,h,Rinitial,scatter,seed=123):
    start=time.monotonic();rng=np.random.default_rng(seed);mp=M/N
    direction=rng.normal(size=(N,3));direction/=np.linalg.norm(direction,axis=1)[:,None]
    pos=direction*(Rinitial*rng.random(N)**(1/3))[:,None]
    vel=.05*rng.normal(size=(N,3));vel-=vel.mean(axis=0)
    E0=energy(pos,vel,mp)[0];acc=force(pos,mp)
    snaps=[];collisions=0;pmax=0.;collision_error=0.;xmax=0.;maxedrift=0
    saves={int(round(t/dt)):t for t in [0,1,2,4,4.5,6,8]}
    for it in range(int(round(8/dt))+1):
        if it in saves:
            rad=np.linalg.norm(pos,axis=1);cum=mp*np.searchsorted(np.sort(rad),rrscore,side='right')
            E,K,Wc,Wb=energy(pos,vel,mp);drift=abs((E-E0)/E0);maxedrift=max(maxedrift,drift)
            snaps.append(dict(t_code=saves[it],elapsed_Gyr=saves[it]*c['tu_Gyr'],mass_within_target_radius=float(mp*np.sum(rad<=1)),target_mass=M,r50=float(np.median(rad)),r90=float(np.quantile(rad,.9)),max_enclosed_mass_error_over_target_mass=float(np.max(abs(cum-target))/M),rms_acceleration_log10_error=float(np.sqrt(np.mean(np.log10((ns['Mb_enc'](c,rrscore)+cum)/(ns['Mb_enc'](c,rrscore)+target))**2))),energy=E,relative_energy_drift=drift,virial_2K_over_absW=2*K/abs(Wc+Wb),cumulative_mass=cum.tolist()))
        if it==int(round(8/dt)):break
        vel+=.5*dt*acc;pos+=dt*vel;acc=force(pos,mp);vel+=.5*dt*acc
        if scatter:
            nc,pr,er,x=collide(pos,vel,mp,dt,h,rng);collisions+=nc;pmax=max(pmax,pr);collision_error=max(collision_error,er);xmax=max(xmax,x)
    return dict(name=name,N=N,dt=dt,cell_width=h,Rinitial=Rinitial,scatter=scatter,seed=seed,collisions=collisions,mean_collisions_per_particle=2*collisions/N,max_collision_probability=pmax,max_pair_energy_roundoff=collision_error,max_resonance_x=xmax,max_sampled_energy_drift=maxedrift,seconds=time.monotonic()-start,snapshots=snaps)
configs=[('base',2048,.001,.05,c['rta'],True),('collisionless',2048,.001,.05,c['rta'],False),('refined',4096,.0005,.05,c['rta'],True),('smaller_cells',4096,.0005,.025,c['rta'],True),('compact_initial',2048,.001,.05,1.2,True),('compact_refined',4096,.0005,.025,1.2,True)]
rows=json.loads((p/'halo_formation_probe_run/results.json').read_text())['rows']
configs=configs[4:]
for conf in configs:
    row=run(*conf);rows.append(row);print(json.dumps({k:row[k] for k in ['name','seconds','collisions','max_sampled_energy_drift']}),flush=True)
    # Persist after every completed run so an interrupted experiment is recoverable.
    out=dict(cell=c,sigma_over_mass_cm2_g=4.,sigma_code=sigma_unit,score_radii=rrscore.tolist(),target_enclosed_mass=target.tolist(),rows=rows,checks=checks,scope='Exploratory spherical monopole gravity with 3D cell DSMC; static softened baryons; all particles retained including escaping ones; no target force or thermostat')
    (p/'halo_formation_probe_v2_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
for row in rows:
    ck(row['name']+' energy accuracy',row['max_sampled_energy_drift']<.02)
    ck(row['name']+' collision energy',row['max_pair_energy_roundoff']<1e-9)
out['checks']=checks;out['all_numerical_checks_pass']=all(x['passed'] for x in checks)
(p/'halo_formation_probe_v2_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Numerical checks',out['all_numerical_checks_pass'],flush=True)
