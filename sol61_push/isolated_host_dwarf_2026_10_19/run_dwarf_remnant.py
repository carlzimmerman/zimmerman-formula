"""Diagnostic replay of run_dwarf.py; evolution unchanged.

Prepared daughter-carrier Boltzmann--Poisson dwarf; no target-profile force.

All evolving original dwarf particles remain in the ledger after stripping.
The host is an explicitly prescribed static source, not an evolved recipient.
"""
import os
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_key]='1'
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path
import numpy as np
from dynamics import gravity, host, scatter, G
from remnant import remnant_centre

MSTAR=574272.9377001019
MCOLD=53.64*MSTAR
RADII=np.array([50.,100.,150.,200.,300.,500.,1000.,2000.,4000.,10000.])


def vector_J(x,v,m):
    return np.sum(np.cross(x,m[:,None]*v),axis=0)


def centre(x,m,mask,eps=40.):
    # Only diagnostics change: no forces, initial state or RNG calls use this.
    return remnant_centre(x,m,~mask,eps=eps)


def ledger(x,v,m,cold,eps,has_host,U=None):
    M=float(m.sum()); X=np.average(x,axis=0,weights=m)
    V=np.average(v,axis=0,weights=m); q=x-X; w=v-V
    if U is None:
        _,U=gravity(x,m,eps)
    _,Uc=gravity(x[cold],m[cold],eps)
    _,Us=gravity(x[~cold],m[~cold],eps)
    Ucross=U-Uc-Us
    Kc=float(.5*np.sum(m[cold,None]*w[cold]**2))
    Ks=float(.5*np.sum(m[~cold,None]*w[~cold]**2))
    _,ph=host(x,enabled=has_host)
    UH=float(m@ph); Eorb=float(.5*M*(V@V))
    Jc=vector_J(q[cold],w[cold],m[cold]); Js=vector_J(q[~cold],w[~cold],m[~cold])
    Jint=Jc+Js; Jorb=np.cross(X,M*V); Jtotal=vector_J(x,v,m)
    cc=centre(x,m,~cold,eps); r=np.linalg.norm(x-cc,axis=1)
    order=np.argsort(r[cold]); rm=r[cold][order]
    cum=np.cumsum(m[cold][order]); rhalf=float(np.interp(.5*MCOLD,cum,rm))
    enclosed=np.array([float(m[cold & (r<=rr)].sum()) for rr in RADII])
    shellmass=np.diff(np.r_[0.,enclosed]); shellvolume=4*np.pi/3*np.diff(np.r_[0.,RADII**3])
    n300=int(np.count_nonzero(cold & (r<=300)))
    central_stars=(~cold)&(r<=300.)
    central_sigma=float(np.sqrt(np.mean(np.var(v[central_stars],axis=0)))/1.022712165045695) if central_stars.sum()>=8 else None
    return dict(Eint=Kc+Ks+U,Eorb=Eorb,Etotal=Kc+Ks+U+Eorb+UH,
                Ecold=Kc+Uc+.5*Ucross,Estars=Ks+Us+.5*Ucross,
                Kcold=Kc,Kstars=Ks,Uself=float(U),Ucc=float(Uc),Uss=float(Us),
                Ucross=float(Ucross),Uhost=UH,Jint=Jint.tolist(),Jorb=Jorb.tolist(),
                Jtotal=Jtotal.tolist(),Jcold=Jc.tolist(),Jstars=Js.tolist(),
                COM=X.tolist(),VCOM=V.tolist(),centre=cc.tolist(),
                centre_COM_offset_pc=float(np.linalg.norm(cc-X)),
                cold_enclosed_Msun=enclosed.tolist(),cold_shell_density_Msun_pc3=(shellmass/shellvolume).tolist(),
                M100=float(enclosed[1]),M300=float(enclosed[4]),M1000=float(enclosed[6]),
                cold_count300=n300,cold_rhalf_pc=rhalf,
                cold_beyond10kpc_Msun=float(m[cold & (r>10000)].sum()),
                central_star_count300=int(central_stars.sum()),central_sigma_star_1d_kms=central_sigma,
                global_sigma_star_1d_kms=float(np.sqrt(np.mean(np.var(v[~cold],axis=0)))/1.022712165045695))


def initial_conditions(ncold,nstar,seed,eps):
    if ncold%2 or nstar%2:
        raise ValueError('Antithetic samples require even counts')
    rng=np.random.default_rng(seed)
    direction=rng.normal(size=(ncold//2,3)); direction/=np.linalg.norm(direction,axis=1)[:,None]
    xc=direction*rng.random(ncold//2)[:,None]**(1/3)*np.array([2000.,1600.,1200.])
    angle=np.deg2rad(37.); rot=np.array([[np.cos(angle),-np.sin(angle),0.],[np.sin(angle),np.cos(angle),0.],[0.,0.,1.]])
    xc=xc@rot.T; xc=np.r_[xc,-xc]
    direction=rng.normal(size=(nstar//2,3)); direction/=np.linalg.norm(direction,axis=1)[:,None]
    fmax=(1500./np.sqrt(1500.**2+193.22**2))**3
    u=rng.uniform(0.,fmax,size=nstar//2)
    rs=193.22/np.sqrt(u**(-2/3)-1.)
    xs=direction*rs[:,None]; xs=np.r_[xs,-xs]
    x=np.r_[xc,xs]; m=np.r_[np.full(ncold,MCOLD/ncold),np.full(nstar,MSTAR/nstar)]
    cold=np.arange(ncold+nstar)<ncold; a,U=gravity(x,m,eps)
    v=np.zeros_like(x); axis=np.array([1.,1.,2.])/np.sqrt(6.)
    details={}
    for label,mask,ratio in [('cold',cold,.2),('stars',~cold,1.)]:
        xx=x[mask]; mm=m[mask]; nn=len(xx)
        w=rng.normal(size=(nn//2,3)); w=np.r_[w,-w]
        I=np.eye(3)*np.sum(mm*np.sum(xx*xx,axis=1))-(xx*mm[:,None]).T@xx
        w-=np.cross(np.linalg.solve(I,vector_J(xx,w,mm)),xx)
        vir=float(np.sum(mm[:,None]*xx*a[mask])); target=.5*ratio*abs(vir)
        frot=.1 if label=='cold' else 0.
        w*=np.sqrt((1-frot)*target/(.5*np.sum(mm[:,None]*w*w)))
        rotation=np.cross(axis,xx)
        if frot:
            rotation*=np.sqrt(frot*target/(.5*np.sum(mm[:,None]*rotation*rotation)))
            w+=rotation
        v[mask]=w
        details[label]=dict(virial_W=vir,kinetic=float(.5*np.sum(mm[:,None]*w*w)),virial_ratio=ratio,ordered_fraction=frot)
    details.update(total_self_potential=U,cold_mass=MCOLD,stellar_mass=MSTAR,
                   cold_axes_pc=[2000,1600,1200],star_scale_pc=193.22,
                   relative_state_sha256=hashlib.sha256(x.tobytes()+v.tobytes()+m.tobytes()).hexdigest())
    return x,v,m,cold,details


def per_particle_EJ(x,v,m,eps):
    X=np.average(x,axis=0,weights=m); V=np.average(v,axis=0,weights=m)
    phi=np.zeros(len(m))
    for first in range(0,len(m),128):
        last=min(first+128,len(m)); d=x[first:last,None,:]-x[None,:,:]
        den=np.sqrt(np.sum(d*d,axis=2)+eps*eps)
        pp=-G*(1./den)@m
        pp+=G*m[first:last]/eps
        phi[first:last]=pp
    ep=.5*m*np.sum((v-V)**2,axis=1)+.5*m*phi
    jp=np.cross(x-X,m[:,None]*(v-V))
    instant_self_unbound=.5*np.sum((v-V)**2,axis=1)+phi>0
    return ep,jp,instant_self_unbound


def simulate(args):
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    x,v,m,cold,initial=initial_conditions(args.ncold,args.nstar,args.seed,args.eps)
    if args.host:
        X0=np.array([80000.,0.,0.]); ah,_=host(X0[None,:],enabled=True)
        vcirc=np.sqrt(-80000.*ah[0,0])
        x+=X0; v+=np.array([0.,.65*vcirc,0.])
    xinitial=x.copy(); vinitial=v.copy()
    np.savez_compressed(out/'initial.npz',x=x,v=v,m=m,cold=cold)
    rng=np.random.default_rng(args.seed+1000000)
    ai,U=gravity(x,m,args.eps); ah,phh=host(x,enabled=args.host); acc=ai+ah
    state0=ledger(x,v,m,cold,args.eps,args.host,U)
    Escale=abs(state0['Eint'])
    Jscale=float(m.sum()*2000*np.sqrt(2*(state0['Kcold']+state0['Kstars'])/m.sum()))
    cumulative=dict(W_host=0.,W_host_int=0.,W_host_orb=0.,W_host_cold=0.,W_host_stars=0.,
                    tau_host_int=np.zeros(3),tau_host_orb=np.zeros(3),tau_host_total=np.zeros(3),
                    collision_dE=0.,collision_dJ=np.zeros(3),collisions=0,max_probability=0.,max_resonance_x=0.)
    host_work_particle=np.zeros(len(m)); host_torque_particle=np.zeros((len(m),3))
    allstep_max=dict(energy=0.,internal_work=0.,host_work=0.,Jint=0.,Jorb=0.,Jtotal=0.)
    minimum_host_COM_radius=float(np.linalg.norm(np.average(x,axis=0,weights=m)))
    trajectory_x=[]; trajectory_v=[]; trajectory_times=[]
    rows=[]; beginning=time.monotonic(); steps=int(round(args.duration/args.dt))
    if abs(steps*args.dt-args.duration)>1e-8:
        raise ValueError('duration must be an integer multiple of dt')
    save_every=max(1,int(round(100./args.dt)))
    def record(t):
        trajectory_x.append(x.copy()); trajectory_v.append(v.copy()); trajectory_times.append(t)
        s=ledger(x,v,m,cold,args.eps,args.host,U); s['time_Myr']=t
        s['cumulative']={k:(z.tolist() if isinstance(z,np.ndarray) else z) for k,z in cumulative.items()}
        s['energy_total_error_scaled']=(s['Etotal']-state0['Etotal'])/Escale
        s['energy_internal_work_residual_scaled']=(s['Eint']-state0['Eint']-cumulative['W_host_int']-cumulative['collision_dE'])/Escale
        s['energy_host_work_residual_scaled']=(s['Uhost']-state0['Uhost']+cumulative['W_host'])/Escale
        for part in ('int','orb','total'):
            resid=np.array(s['J'+part])-state0['J'+part]-cumulative['tau_host_'+part]-cumulative['collision_dJ']*(part!='orb')
            s['J_'+part+'_closure_scaled']=float(np.linalg.norm(resid)/Jscale)
        rows.append(s)
    record(0.)
    for step in range(1,steps+1):
        oldx=x.copy(); oldv=v.copy(); oldah=ah
        Xold=np.average(oldx,axis=0,weights=m)
        tauint0=vector_J(oldx-Xold,oldah,m); tautotal0=vector_J(oldx,oldah,m)
        v+=.5*args.dt*acc
        kick1mid=.5*(oldv+v); kick1dvh=.5*args.dt*oldah
        vhalf=v.copy(); x+=args.dt*v
        ai,U=gravity(x,m,args.eps); ah,phh=host(x,enabled=args.host); acc=ai+ah
        v+=.5*args.dt*acc
        for vmid,dvh in [(kick1mid,kick1dvh),(.5*(vhalf+v),.5*args.dt*ah)]:
            Vmid=np.average(vmid,axis=0,weights=m); dVh=np.average(dvh,axis=0,weights=m)
            wmid=vmid-Vmid
            cumulative['W_host']+=float(np.sum(m[:,None]*vmid*dvh))
            cumulative['W_host_int']+=float(np.sum(m[:,None]*wmid*dvh))
            cumulative['W_host_orb']+=float(np.sum(m[:,None]*Vmid*dvh))
            for label,mask in [('cold',cold),('stars',~cold)]:
                cumulative['W_host_'+label]+=float(np.sum(m[mask,None]*wmid[mask]*(dvh[mask]-dVh)))
            host_work_particle+=np.sum(m[:,None]*wmid*(dvh-dVh),axis=1)
        Xnew=np.average(x,axis=0,weights=m)
        Aold=np.average(oldah,axis=0,weights=m); Anew=np.average(ah,axis=0,weights=m)
        host_torque_particle+=.5*args.dt*(np.cross(oldx-Xold,m[:,None]*(oldah-Aold))
                                          +np.cross(x-Xnew,m[:,None]*(ah-Anew)))
        tint=.5*args.dt*(tauint0+vector_J(x-Xnew,ah,m))
        ttotal=.5*args.dt*(tautotal0+vector_J(x,ah,m))
        cumulative['tau_host_int']+=tint; cumulative['tau_host_total']+=ttotal
        cumulative['tau_host_orb']+=ttotal-tint
        if not args.collisionless:
            report=scatter(x,v,m,cold,args.dt,args.h,rng,sigma_cm2_g=.3)
            cumulative['collisions']+=report['n']
            cumulative['collision_dE']+=report['delta_energy']
            cumulative['collision_dJ']+=np.asarray(report['delta_J'])
            cumulative['max_probability']=max(cumulative['max_probability'],report['max_prob'])
            cumulative['max_resonance_x']=max(cumulative['max_resonance_x'],report['max_x_resonance'])
        vv=np.average(v,axis=0,weights=m); xx=np.average(x,axis=0,weights=m)
        eint=float(.5*np.sum(m[:,None]*(v-vv)**2)+U)
        etotal=float(.5*np.sum(m[:,None]*v*v)+U+m@phh)
        allstep_max['energy']=max(allstep_max['energy'],abs(etotal-state0['Etotal'])/Escale)
        allstep_max['internal_work']=max(allstep_max['internal_work'],abs(eint-state0['Eint']-cumulative['W_host_int']-cumulative['collision_dE'])/Escale)
        allstep_max['host_work']=max(allstep_max['host_work'],abs(float(m@phh)-state0['Uhost']+cumulative['W_host'])/Escale)
        current_J={'int':vector_J(x-xx,v-vv,m),'orb':np.cross(xx,m.sum()*vv),'total':vector_J(x,v,m)}
        for part in ('int','orb','total'):
            residual=current_J[part]-state0['J'+part]-cumulative['tau_host_'+part]-cumulative['collision_dJ']*(part!='orb')
            allstep_max['J'+part]=max(allstep_max['J'+part],float(np.linalg.norm(residual)/Jscale))
        minimum_host_COM_radius=min(minimum_host_COM_radius,float(np.linalg.norm(xx)))
        if step%save_every==0 or step==steps:
            record(step*args.dt)
        if step%max(1,steps//10)==0:
            print(json.dumps(dict(time_Myr=step*args.dt,seconds=round(time.monotonic()-beginning,2),
                host=args.host,ncold=args.ncold,collisions=cumulative['collisions'],
                M300=rows[-1]['M300'],energy_error=rows[-1]['energy_total_error_scaled'])),flush=True)
    np.savez_compressed(out/'final.npz',x=x,v=v,m=m,cold=cold,host_work_particle=host_work_particle,host_torque_particle=host_torque_particle)
    np.savez_compressed(out/'trajectory.npz',x=np.array(trajectory_x),v=np.array(trajectory_v),time_Myr=np.array(trajectory_times),m=m,cold=cold)
    finalcentre=centre(x,m,~cold,args.eps); r=np.linalg.norm(x-finalcentre,axis=1)
    core=cold & (r<=300.); groups={'final_core_material':core,'other_cold_material':cold & ~core,'stars':~cold}
    ep0,jp0,_=per_particle_EJ(xinitial,vinitial,m,args.eps)
    ep1,jp1,unbound=per_particle_EJ(x,v,m,args.eps)
    def account(mask):
        return dict(count=int(mask.sum()),mass_Msun=float(m[mask].sum()),
            E_initial=float(ep0[mask].sum()),E_final=float(ep1[mask].sum()),
            delta_E=float(ep1[mask].sum()-ep0[mask].sum()),
            host_internal_work=float(host_work_particle[mask].sum()),
            inferred_internal_energy_transfer=float(ep1[mask].sum()-ep0[mask].sum()-host_work_particle[mask].sum()),
            J_initial=jp0[mask].sum(axis=0).tolist(),J_final=jp1[mask].sum(axis=0).tolist(),
            delta_J=(jp1[mask].sum(axis=0)-jp0[mask].sum(axis=0)).tolist(),
            host_internal_torque=host_torque_particle[mask].sum(axis=0).tolist(),
            inferred_internal_J_transfer=(jp1[mask].sum(axis=0)-jp0[mask].sum(axis=0)-host_torque_particle[mask].sum(axis=0)).tolist())
    groups_out={name:account(mask) for name,mask in groups.items()}
    initial_centre=centre(xinitial,m,~cold,args.eps)
    initial_core_account=account(cold & (np.linalg.norm(xinitial-initial_centre,axis=1)<=300.))
    last=[z for z in rows if z['time_Myr']>=args.duration-1000.]
    concentrated=args.duration>=1000. and len(last)>=11 and all(z['cold_count300']>=64 and z['M300']/MCOLD>=.1 for z in last)
    peakRSS=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    summary=dict(cold_mass_Msun=MCOLD,stellar_mass_Msun=MSTAR,
       max_energy_total_error_scaled=allstep_max['energy'],
       max_internal_work_residual_scaled=allstep_max['internal_work'],
       max_host_work_residual_scaled=allstep_max['host_work'],
       max_J_int_closure_scaled=allstep_max['Jint'],
       max_J_orb_closure_scaled=allstep_max['Jorb'],
       max_J_total_closure_scaled=allstep_max['Jtotal'],
       minimum_host_COM_radius_pc=minimum_host_COM_radius,
       collision_energy_error_scaled=cumulative['collision_dE']/Escale,
       collision_J_error_scaled=float(np.linalg.norm(cumulative['collision_dJ'])/Jscale),
       collisions=cumulative['collisions'],mean_collisions_per_cold_particle=2*cumulative['collisions']/args.ncold,
       final_M100=rows[-1]['M100'],final_M300=rows[-1]['M300'],final_M1000=rows[-1]['M1000'],
       final_cold_rhalf_pc=rows[-1]['cold_rhalf_pc'],
       persistent_resolved_300pc_concentration_candidate=concentrated,
       formed_100pc_core='NOT ESTABLISHED: needs radial shape and refinement checks',
       cold_instantaneously_self_unbound_mass=float(m[cold & unbound].sum()),
       fixed_membership_groups=groups_out,
       initially_selected_core_material=initial_core_account,
       energy_group_sum_residual=float(sum(g['E_final'] for g in groups_out.values())-rows[-1]['Eint']),
       host_work_particle_sum_residual=float(host_work_particle.sum()-cumulative['W_host_int']),
       host_torque_particle_sum_residual=(host_torque_particle.sum(axis=0)-cumulative['tau_host_int']).tolist(),
       energy_scale=Escale,J_scale=Jscale,wall_seconds=time.monotonic()-beginning,
       observed_peak_RSS_native_units=int(peakRSS),RSS_units='bytes on Darwin, KiB on Linux')
    result=dict(diagnostic_revision='potential-minimum remnant centre; full snapshots and per-particle host receipts',model='prepared dilute Phi/X daughter-carrier Newtonian Boltzmann-Poisson',
         args=vars(args),initial_conditions=initial,radii_pc=RADII.tolist(),summary=summary,snapshots=rows,
         nonclaims=['Not full canonical polarization action','Initial state is not production-derived',
                    'Static host response not evolved','No radiation/inelastic channel',
                    'No universal formation or exclusion result','Finite-N and kernel convergence required'])
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'summary':summary}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--host',action='store_true')
    parser.add_argument('--collisionless',action='store_true')
    parser.add_argument('--ncold',type=int,default=2048)
    parser.add_argument('--nstar',type=int,default=256)
    parser.add_argument('--duration',type=float,default=10000.)
    parser.add_argument('--dt',type=float,default=2.)
    parser.add_argument('--eps',type=float,default=40.)
    parser.add_argument('--h',type=float,default=200.)
    parser.add_argument('--seed',type=int,default=87319)
    simulate(parser.parse_args())
