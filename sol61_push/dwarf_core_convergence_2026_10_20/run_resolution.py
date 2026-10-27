"""Matched full3D resolution extension; no imposed cold density or cooling."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
import numpy as np
from scipy.optimize import minimize

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'isolated_host_dwarf_2026_10_19'
sys.path.insert(0,str(OLD))
from dynamics import host,scatter,G
from remnant import _candidate_centres
from evolution import initial_conditions,h4_step,vector_J,MCOLD
from fast_gravity import gravity as cpu_gravity,backend_metadata
from profile_diagnostics import shell_profile,relaxation_screen,fit_powerlaw

EDGES=np.array([5.,7.,10.,15.,20.,25.,30.,40.,50.,60.,75.,100.,125.,150.,200.,250.,300.,400.,500.,750.,1000.,1500.,2000.])


def choose_centre(x,m,cold,eps,previous=None,full_search=True):
    candidates,_=_candidate_centres(x,m,cold,eps) if full_search or previous is None else ([],None)
    if previous is not None:
        pred=np.asarray(previous)
        def objective(offset):
            d=pred+offset-x;inv=1./np.sqrt(np.sum(d*d,axis=1)+eps*eps)
            return -G*np.sum(m*inv),G*np.sum((m*inv**3)[:,None]*d,axis=0)
        f=minimize(objective,np.zeros(3),jac=True,method='L-BFGS-B',bounds=[(-2000.,2000.)]*3,
                   options=dict(ftol=1e-13,gtol=1e-10,maxiter=100))
        candidates.append(dict(centre=pred+f.x,potential=float(f.fun),seed_label='tracked_prediction',optimizer_success=bool(f.success),refinement_hit_boundary=bool(np.any(abs(f.x)>1999.))))
    candidates.sort(key=lambda z:z['potential'])
    best=candidates[0]
    return np.asarray(best['centre']),[dict(centre=np.asarray(z['centre']).tolist(),potential=z['potential'],seed=z['seed_label'],success=z['optimizer_success']) for z in candidates]


def unbind(x,v,m,cc,eps,radius,gravity):
    r=np.linalg.norm(x-cc,axis=1);ids=np.flatnonzero(r<=radius)
    inner=np.flatnonzero(r<=min(300.,radius))
    if not len(ids):return np.array([],dtype=int),np.zeros(3),0
    bulk=np.median(v[inner if len(inner) else ids],axis=0)
    for it in range(1,51):
        _,_,phi=gravity(x[ids],m[ids],eps)
        kept=ids[.5*np.sum((v[ids]-bulk)**2,axis=1)+phi<0.]
        if not len(kept):return kept,bulk,it
        newbulk=np.average(v[kept],axis=0,weights=m[kept])
        stable=len(kept)==len(ids) and np.linalg.norm(newbulk-bulk)<1e-9
        ids,bulk=kept,newbulk
        if stable:break
    return ids,bulk,it


def conservation(x,v,m,state):
    X=np.average(x,axis=0,weights=m);V=np.average(v,axis=0,weights=m)
    K=float(.5*np.sum(m[:,None]*(v-V)**2));Eorb=float(.5*m.sum()*(V@V))
    return dict(Eint=K+state[1],Eorb=Eorb,Uhost=float(m@state[4]),Etotal=K+state[1]+Eorb+float(m@state[4]),
        Jint=vector_J(x-X,v-V,m),Jorb=np.cross(X,m.sum()*V),Jtotal=vector_J(x,v,m),
        P=np.sum(m[:,None]*v,axis=0),COM=X,VCOM=V)


def simulate(args):
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    if args.backend=='metal':
        from metal_gravity import gravity as metal_gravity
        gravity=lambda x,m,eps:metal_gravity(x,m,eps)
        backend=dict(name='metal declared high-precision expansion direct gravity')
    else:
        gravity=lambda x,m,eps:cpu_gravity(x,m,eps,threads=args.threads)
        backend=backend_metadata()
    x,v,m,cold,ic=initial_conditions(args.ncold,args.ncold//8,args.seed,args.eps,gravity)
    ic['relative_state_sha256']=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest()
    if args.host:
        a,_=host(np.array([[80000.,0.,0.]]));vc=np.sqrt(-80000.*a[0,0])
        x+=np.array([80000.,0.,0.]);v+=np.array([0.,.65*vc,0.])
    x0,v0=x.copy(),v.copy()
    def force(xx):
        aa,U,phi=gravity(xx,m,args.eps);ah,ph=host(xx,enabled=args.host)
        return aa+ah,U,phi,ah,ph
    state=force(x);initial=conservation(x,v,m,state);phi0=state[2].copy()
    Escale=abs(initial['Eint']);Jscale=float(m.sum()*2000*np.sqrt(2*(initial['Eint']-state[1])/m.sum()))
    Pscale=Jscale/2000.
    np.savez_compressed(out/'initial.npz',x=x,v=v,m=m,cold=cold,phi=phi0)
    work_particle=np.zeros(len(m));torque_particle=np.zeros((len(m),3))
    Wint=0.;Worb=0.;torque_int=np.zeros(3);torque_orb=np.zeros(3);Phost=np.zeros(3)
    collisionE=0.;collisionJ=np.zeros(3);events=0;maxprob=0.;maxz=0.
    maxima=dict(E=0.,internal_work=0.,host_work=0.,Jint=0.,Jorb=0.,Jtotal=0.,P=0.)
    rng=np.random.default_rng(args.collision_seed if args.collision_seed is not None else args.seed+1000000)
    trajectory_x=[];trajectory_v=[];trajectory_t=[];rows=[];prev=None;prevV=None
    def receipt(xx,before,after,st,delta):
        nonlocal Wint,Worb
        dvh=delta*st[3];mid=.5*(before+after);Vmid=np.average(mid,axis=0,weights=m)
        X=np.average(xx,axis=0,weights=m);dV=np.average(dvh,axis=0,weights=m);wmid=mid-Vmid
        ww=np.sum(m[:,None]*wmid*(dvh-dV),axis=1)
        tt=np.cross(xx-X,m[:,None]*(dvh-dV))
        work_particle[:]+=ww;torque_particle[:]+=tt
        Wint+=float(ww.sum());Worb+=float(m.sum()*(Vmid@dV))
        torque_int[:]+=tt.sum(axis=0);torque_orb[:]+=np.cross(X,m.sum()*dV)
        Phost[:]+=m.sum()*dV
    def record(t):
        nonlocal prev,prevV
        prediction=None if prev is None else prev+prevV*(t-rows[-1]['time_Myr'])
        full_search=t==0. or t==args.duration or abs(t/100-round(t/100))<1e-7
        cc,candidates=choose_centre(x,m,cold,args.eps,prediction,full_search)
        if prediction is not None and not full_search and np.linalg.norm(cc-prediction)>1500.:
            cc,candidates=choose_centre(x,m,cold,args.eps,prediction,True)
        r=np.linalg.norm(x-cc,axis=1);central=r<=300.
        bulk=np.median(v[central],axis=0) if np.any(central) else np.average(v,axis=0,weights=m)
        offset=None if prediction is None else float(np.linalg.norm(cc-prediction))
        prev,prevV=cc.copy(),bulk.copy()
        prof=shell_profile(x,m,cc,EDGES,cold)
        fits={}
        for lo,hi in [(10,30),(20,60),(25,75),(30,100),(50,150),(75,250),(100,300)]:
            fits[str(lo)+'_'+str(hi)]=fit_powerlaw(prof,lo,hi)
        c=conservation(x,v,m,state)
        row=dict(time_Myr=t,centre=cc.tolist(),bulk=bulk.tolist(),host_radius_pc=float(np.linalg.norm(cc)),
            prediction_offset_pc=offset,candidates=candidates,profile=prof,relaxation=relaxation_screen(prof,args.eps),fits=fits,
            M100=float(m[cold&(r<=100)].sum()),M300=float(m[cold&central].sum()),
            cold_count100=int(np.sum(cold&(r<=100))),cold_count300=int(np.sum(cold&central)),
            star_count300=int(np.sum(~cold&central)),collisions=events,
            conservation={k:(z.tolist() if isinstance(z,np.ndarray) else z) for k,z in c.items()},
            host_work_internal=Wint,host_work_orbital=Worb,host_torque_internal=torque_int.tolist(),host_torque_orbital=torque_orb.tolist())
        if t>=args.duration-2000 and abs(t/100-round(t/100))<1e-7 or t==args.duration:
            bounds={}
            for radius in (500.,1000.,2000.):
                ids,bv,it=unbind(x,v,m,cc,args.eps,radius,gravity)
                bounds[str(int(radius))]=dict(total_mass=float(m[ids].sum()),cold_mass=float(m[ids[cold[ids]]].sum()),
                    cold_M300=float(m[ids[cold[ids]&(r[ids]<=300)]].sum()),count=int(len(ids)),bulk=bv.tolist(),iterations=it)
            row['instantaneous_bound_cuts']=bounds
        rows.append(row)
        if t in (0.,100.,200.,500.,1000.,2000.,4000.,6000.) or t>=args.duration-2000 and abs(t/100-round(t/100))<1e-7 or t==args.duration:
            trajectory_x.append(x.copy());trajectory_v.append(v.copy());trajectory_t.append(t)
        print(json.dumps(dict(time_Myr=t,seconds=round(time.monotonic()-start,3),M300=row['M300'],M100=row['M100'],collisions=events,maxE=maxima['E'])),flush=True)
        (out/'progress.json').write_text(json.dumps(dict(last_time_Myr=t,wall_seconds=time.monotonic()-start,maxima=maxima,latest_M300=row['M300']))+'\n')
    record(0.)
    steps=round(args.duration/args.dt)
    if abs(steps*args.dt-args.duration)>1e-9:raise ValueError('duration must be integer multiple of dt')
    save_every=round(args.record_interval/args.dt)
    if abs(save_every*args.dt-args.record_interval)>1e-9:raise ValueError('record interval must be integer multiple of dt')
    for step in range(1,steps+1):
        state=h4_step(x,v,args.dt,force,state,receipt if args.host else None)
        if not args.collisionless:
            sc=scatter(x,v,m,cold,args.dt,args.h,rng,sigma_cm2_g=.3)
            events+=sc['n'];collisionE+=sc['delta_energy'];collisionJ+=sc['delta_J']
            maxprob=max(maxprob,sc['max_prob']);maxz=max(maxz,sc['max_x_resonance'])
        c=conservation(x,v,m,state)
        maxima['E']=max(maxima['E'],abs(c['Etotal']-initial['Etotal'])/Escale)
        maxima['internal_work']=max(maxima['internal_work'],abs(c['Eint']-initial['Eint']-Wint-collisionE)/Escale)
        maxima['host_work']=max(maxima['host_work'],abs(c['Uhost']-initial['Uhost']+Wint+Worb)/Escale)
        for key,torque in [('Jint',torque_int),('Jorb',torque_orb),('Jtotal',torque_int+torque_orb)]:
            defect=c[key]-initial[key]-torque-(collisionJ if key!='Jorb' else 0.)
            maxima[key]=max(maxima[key],float(np.linalg.norm(defect)/Jscale))
        maxima['P']=max(maxima['P'],float(np.linalg.norm(c['P']-initial['P']-Phost)/Pscale))
        if not np.isfinite(c['Etotal']):raise FloatingPointError('nonfinite phase space')
        if step%save_every==0 or step==steps:record(step*args.dt)
    np.savez_compressed(out/'final.npz',x=x,v=v,m=m,cold=cold,phi=state[2],host_work_particle=work_particle,host_torque_particle=torque_particle)
    np.savez_compressed(out/'trajectory.npz',x=np.array(trajectory_x),v=np.array(trajectory_v),time_Myr=trajectory_t,m=m,cold=cold)
    cc=np.array(rows[-1]['centre']);core=cold&(np.linalg.norm(x-cc,axis=1)<=300.)
    X0=np.average(x0,axis=0,weights=m);V0=np.average(v0,axis=0,weights=m)
    X1=np.average(x,axis=0,weights=m);V1=np.average(v,axis=0,weights=m)
    ep0=.5*m*(np.sum((v0-V0)**2,axis=1)+phi0);ep1=.5*m*(np.sum((v-V1)**2,axis=1)+state[2])
    jp0=np.cross(x0-X0,m[:,None]*(v0-V0));jp1=np.cross(x-X1,m[:,None]*(v-V1))
    groups={}
    for label,mask in [('final_core',core),('other_cold',cold&~core),('stars',~cold)]:
        groups[label]=dict(mass=float(m[mask].sum()),delta_E=float((ep1-ep0)[mask].sum()),host_work=float(work_particle[mask].sum()),
            delta_J=(jp1-jp0)[mask].sum(axis=0).tolist(),host_torque=torque_particle[mask].sum(axis=0).tolist())
    result=dict(args=vars(args),model='prepared Newtonian dilute carrier Boltzmann-Poisson',initial_conditions=ic,
        backend=backend,integrator='H4 Hamiltonian composition; positive-time end-of-step elastic operator',
        maxima=maxima,energy_scale=Escale,J_scale=Jscale,collision_energy_defect=collisionE,collision_J_defect=collisionJ.tolist(),
        collisions=events,mean_collisions_per_cold_particle=2*events/args.ncold,max_collision_probability=maxprob,max_resonance_z=maxz,
        host_work_particle_sum_residual=float(work_particle.sum()-Wint),host_torque_particle_sum_residual=(torque_particle.sum(axis=0)-torque_int).tolist(),
        fixed_membership_groups=groups,snapshots=rows,runtime_seconds=time.monotonic()-start,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        status='finite numerical experiment; physical convergence decided by independent controls')
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(completed=True,runtime=result['runtime_seconds'],maxima=maxima,events=events)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--ncold',type=int,default=4096);p.add_argument('--seed',type=int,default=87319)
    p.add_argument('--collision-seed',type=int);p.add_argument('--eps',type=float,default=20.)
    p.add_argument('--h',type=float,default=100.);p.add_argument('--dt',type=float,default=1.)
    p.add_argument('--duration',type=float,default=10000.);p.add_argument('--record-interval',type=float,default=10.)
    p.add_argument('--host',action='store_true');p.add_argument('--collisionless',action='store_true')
    p.add_argument('--threads',type=int,default=4);p.add_argument('--backend',choices=('cpu','metal'),default='cpu')
    simulate(p.parse_args())
