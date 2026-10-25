"""Independent T/F transport, local finite-rate capture, and live 3D gravity."""
import sys,json,argparse
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'local_capture'))
from capture_v4 import Capture, reaction_impulse, G,A0,RESERVOIR,PROFILES
from field import Field3D

class Simulation(Capture):
    def __init__(self,mass,b,n=64,f=.95,flat=.25,seed=11,sigma=1.,spacing=1.,extent=24.,capture_kpc=.1,dt_motion=.2):
        self.field3d=Field3D(A0*b*b/(G*mass),sigma,extent,spacing)
        self.mass=mass;self.b=b;self.capture_h=capture_kpc/b
        # 1 cm²/g = 2.0884e-10 kpc²/Msun.
        self.cross_section=2.0884e-10*mass/b**2
        self.dt_motion=dt_motion
        super().__init__(mass,b,n=n,f=f,flat=flat,seed=seed,beta=0,cooling=True)
        self.stats.update(capture_radiation=0.,eligible_pair_samples=0,locality_subdivisions=0,
                          hazard_subdivisions=0,max_encounter_distance_kpc=0.,max_encounter_hazard_step=0.)

    def energy_force(self,x,state):
        d=x[:,None,:]-x[None,:,:];r2=np.sum(d*d,axis=-1)+self.soft**2
        inv=1/np.sqrt(r2);np.fill_diagonal(inv,0.)
        phi=-inv@self.m;ug=.5*float(self.m@phi)
        acc=-np.sum((inv**3*self.m[None,:])[:,:,None]*d,axis=1)
        ids=np.flatnonzero(state)
        ut,grad,meta=self.field3d.evaluate(x[ids],self.m[ids])
        acc[ids]-=grad/self.m[ids,None]
        return ug+ut,acc,dict(phi=phi,ut=ut,**meta)

    def pairs(self,x,v):
        # Medium-baryon and unique baryon-baryon pairs, actual fixed spatial support.
        i,j=np.triu_indices(2*self.n,1);keep=(i<self.n)
        i=i[keep];j=j[keep]
        d=x[j]-x[i];dist=np.linalg.norm(d,axis=1)
        keep=(dist<self.capture_h)&(dist>1e-12)
        i=i[keep];j=j[keep];d=d[keep];dist=dist[keep]
        normal=d/dist[:,None];speed=-np.sum((v[j]-v[i])*normal,axis=1)
        keep=speed>0;i=i[keep];j=j[keep];normal=normal[keep];speed=speed[keep];dist=dist[keep]
        rate=self.cross_section*self.m[i]*speed/(4*np.pi*self.capture_h**3/3)
        return i,j,normal,rate,dist

    def swept_limit(self,old,new):
        # Conservative straight-segment encounter audit; trajectory-curvature
        # error is independently controlled by the gravity integrator and dt test.
        d0=old[self.n:,None,:]-old[None,:self.n,:]
        dd=(new[self.n:,None,:]-new[None,:self.n,:])-d0
        b0=old[:self.n,None,:]-old[None,:self.n,:]
        bd=(new[:self.n,None,:]-new[None,:self.n,:])-b0
        ii,jj=np.triu_indices(self.n,1)
        d0=np.concatenate([d0.reshape(-1,3),b0[ii,jj]])
        dd=np.concatenate([dd.reshape(-1,3),bd[ii,jj]])
        l2=np.sum(dd*dd,axis=1)
        t=np.clip(-np.sum(d0*dd,axis=1)/np.maximum(l2,1e-30),0,1)
        close=np.linalg.norm(d0+t[:,None]*dd,axis=1)<1.2*self.capture_h
        return bool(np.any(close&(l2>(self.dt_motion*self.capture_h)**2)))

    def collide(self,dt):
        i,j,normal,rates,dist=self.pairs(self.x,self.v)
        self.stats['eligible_pair_samples']+=len(i)
        for p in self.rng.permutation(len(i)):
            a=int(i[p]);b=int(j[p]);nn=normal[p]
            # Recompute speed after previous impulses; radius remains unchanged.
            speed=-float((self.v[b]-self.v[a])@nn)
            if speed<=0:continue
            rate=self.cross_section*self.m[a]*speed/(4*np.pi*self.capture_h**3/3)
            self.stats['max_encounter_hazard_step']=max(self.stats['max_encounter_hazard_step'],rate*dt)
            if self.rng.random()>-np.expm1(-rate*dt):continue
            self.stats['max_encounter_distance_kpc']=max(self.stats['max_encounter_distance_kpc'],float(dist[p]*self.b))
            oldk=.5*(self.m[a]*np.dot(self.v[a],self.v[a])+self.m[b]*np.dot(self.v[b],self.v[b]))
            if b<self.n:
                mu=self.m[a]*self.m[b]/(self.m[a]+self.m[b]);radiation=.75*.5*mu*speed*speed
                proposal=reaction_impulse(self.v[b],self.v[a],self.m[b],self.m[a],nn,radiation)
                delta=0.;self.stats['cooling_events']+=1
            else:
                self.stats['attempts']+=1
                ids=np.flatnonzero(self.state)
                oldfield=self.field3d.evaluate(self.x[ids],self.m[ids],False)[0]
                candidate=self.state.copy();candidate[b]=not candidate[b];ids=np.flatnonzero(candidate)
                try:newfield=self.field3d.evaluate(self.x[ids],self.m[ids],False)[0]
                except ValueError:self.stats['saturation_rejections']+=1;continue
                delta=newfield-oldfield
                proposal=reaction_impulse(self.v[b],self.v[a],self.m[b],self.m[a],nn,delta)
                if proposal is None:self.stats['energy_rejections']+=1;continue
                radiation=0. if self.state[b] else .91*max(proposal[2]-delta,0.)
                proposal=reaction_impulse(self.v[b],self.v[a],self.m[b],self.m[a],nn,delta+radiation)
                self.stats['releases' if self.state[b] else 'captures']+=1
                self.stats['capture_radiation']+=radiation;self.state=candidate
            vb,va,_=proposal
            newk=.5*(self.m[a]*np.dot(va,va)+self.m[b]*np.dot(vb,vb))
            dp=self.m[a]*(va-self.v[a])+self.m[b]*(vb-self.v[b])
            dl=self.m[a]*np.cross(self.x[a],va-self.v[a])+self.m[b]*np.cross(self.x[b],vb-self.v[b])
            self.stats['event_energy_error']=max(self.stats['event_energy_error'],abs(newk-oldk+delta+radiation)/self.norm)
            self.stats['event_p_error']=max(self.stats['event_p_error'],float(np.linalg.norm(dp))/self.Pscale)
            self.stats['event_l_error']=max(self.stats['event_l_error'],float(np.linalg.norm(dl))/self.Lscale)
            self.v[a]=va;self.v[b]=vb;self.Q+=radiation

    def snapshot(self,t):
        E,acc,meta=self.energy_force(self.x,self.state);K=self.kinetic(self.v)
        center=np.average(self.x[:self.n],axis=0,weights=self.m[:self.n]);r=np.linalg.norm(self.x-center,axis=1)
        half=float(np.median(r[:self.n]));bary=self.x[:self.n]-center
        eig=np.linalg.eigvalsh((bary.T*self.m[:self.n])@bary)
        bound=.5*np.sum(self.v*self.v,axis=1)+meta['phi']<0
        free=(~self.state).astype(float)*self.m;free[:self.n]=0
        angle=np.arange(24)*2*np.pi/24;radius=np.geomspace(.5*half,5*half,12)
        er=np.column_stack([np.cos(angle),np.sin(angle),np.zeros(24)])
        pts=(center+radius[:,None,None]*er[None,:,:]).reshape(-1,3);directions=np.tile(er,(len(radius),1))
        d=pts[:,None,:]-self.x[None,:,:];inv=(np.sum(d*d,axis=-1)+self.soft**2)**-1.5
        ai=-d*inv[:,:,None]*self.m[None,:,None]
        gb=-np.sum(np.sum(ai[:,:self.n],axis=1)*directions,axis=1)
        gt=-np.sum(np.sum(ai,axis=1)*directions,axis=1)
        mask=(gb>0)&(gt>0);expected=.5*(gb[mask]+np.sqrt(gb[mask]**2+4*self.kappa*gb[mask]))
        residual=np.log10(gt[mask]/expected)
        counts=np.sum(np.linalg.norm(self.x[self.n:,None,:]-self.x[None,:self.n,:],axis=-1)<self.capture_h,axis=1)
        L=np.sum(self.m[:,None]*np.cross(self.x,self.v),axis=0);P=np.sum(self.m[:,None]*self.v,axis=0)
        inner=(r<half)&(np.arange(2*self.n)>=self.n)
        return dict(t=float(t),q=float(self.m@self.state/RESERVOIR),
            inner_q=float(self.m[inner]@self.state[inner]/sum(self.m[inner])) if np.any(inner) else None,
            bound_free_fraction=float(free@bound/RESERVOIR),energy_error=abs(E+K+self.Q-self.initialE)/self.norm,
            receiver=self.Q,field_energy=meta['ut'],max_z=meta['max_z'],
            rar_max_dex=float(np.max(abs(residual))),rar_rms_dex=float(np.sqrt(np.mean(residual**2))),
            rar_valid_samples=int(sum(mask)),rar_total_samples=len(mask),
            shape_axis_ratio=float(np.sqrt(eig[0]/eig[-1])),
            momentum_error=float(np.linalg.norm(P-self.P0)/self.Pscale),angular_momentum_error=float(np.linalg.norm(L-self.L0)/self.Lscale),
            local_neighbor_mean=float(np.mean(counts)),local_neighbor_max=int(max(counts)),
            local_empty_fraction=float(np.mean(counts==0)),capture_radius_over_half=self.capture_h/half)

    def run(self,duration=2,dt=.02):
        history=[self.snapshot(0)];t=0.;next_output=duration/20;status='completed';reason=None;count=0
        while t<duration-1e-12:
            h=min(dt,duration-t)*self.tdyn
            try:
                for attempt in range(30):
                    xn,vn=self.advance(self.x,self.v,self.state,h)
                    if self.swept_limit(self.x,xn):
                        h/=2;self.stats['locality_subdivisions']+=1;continue
                    i,j,_,rate,_=self.pairs(xn,vn)
                    sums=np.bincount(np.r_[i,j],weights=np.r_[rate,rate],minlength=2*self.n)
                    if max(sums)*h>.1:
                        h/=2;self.stats['hazard_subdivisions']+=1;continue
                    break
                else:raise RuntimeError('encounter timestep unresolved')
                self.x=xn;self.v=vn;self.collide(h);t+=h/self.tdyn;count+=1
                if np.any(self.state) and np.max(np.abs(self.x[self.state]))>self.field3d.extent-3*self.field3d.sigma:
                    raise RuntimeError('T source approaches nonlinear quadrature boundary')
                if count>20000:raise RuntimeError('step resource bound')
                if t>=next_output-1e-12 or t>=duration-1e-12:
                    history.append(self.snapshot(t));next_output+=duration/20
            except (ValueError,RuntimeError) as exc:status='incomplete';reason=str(exc);break
        if abs(history[-1]['t']-t)>1e-12:history.append(self.snapshot(t))
        return dict(status=status,reason=reason,n=self.n,f=self.f,flat=self.flat,seed=self.seed,mass_msun=self.mass,b_kpc=self.b,
            dt=dt,duration=duration,steps=count,capture_kpc=self.capture_h*self.b,sigma=self.field3d.sigma,
            spacing=self.field3d.spacing,extent=self.field3d.extent,dt_motion=self.dt_motion,
            history=history,final=history[-1],stats=self.stats,
            max_energy_error=max(r['energy_error'] for r in history),
            max_momentum_error=max(r['momentum_error'] for r in history),
            max_angular_momentum_error=max(r['angular_momentum_error'] for r in history),
            final_positions=self.x.tolist(),final_velocities=self.v.tolist(),final_states=self.state.tolist())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=64)
    ap.add_argument('--duration',type=float,default=2);ap.add_argument('--dt',type=float,default=.02)
    ap.add_argument('--profiles',default='0,1,2,3');ap.add_argument('--fs',default='0,.95');ap.add_argument('--flats',default='1,.25')
    ap.add_argument('--seed',type=int,default=11);ap.add_argument('--sigma',type=float,default=1.)
    ap.add_argument('--spacing',type=float,default=1.);ap.add_argument('--motion',type=float,default=.2)
    args=ap.parse_args();out=dict(runs=[])
    for p in map(int,args.profiles.split(',')):
        _,mass,b,_=PROFILES[p]
        for f in map(float,args.fs.split(',')):
            for flat in map(float,args.flats.split(',')):
                sim=Simulation(mass,b,n=args.n,f=f,flat=flat,seed=args.seed,sigma=args.sigma,spacing=args.spacing,dt_motion=args.motion)
                row=sim.run(args.duration,args.dt);row['profile_index']=p;out['runs'].append(row)
                print(json.dumps({k:row[k] for k in ('profile_index','f','flat','status','final','stats')}),flush=True)
                Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
