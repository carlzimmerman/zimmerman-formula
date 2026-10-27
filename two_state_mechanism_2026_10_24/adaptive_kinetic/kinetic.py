import sys,json,argparse
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'field3d_capture'))
from run_exact_self import ExactSelfSimulation
from simulate import reaction_impulse,RESERVOIR,PROFILES
from octree import leaves,cell_pairs

class Kinetic(ExactSelfSimulation):
    def __init__(self,mass,b,nspace=32,nvel=2,max_width=2.,target=16,f=.95,flat=.25,seed=11,spacing=1.5):
        self.nspace=nspace;self.nvel=nvel;self.max_width=max_width;self.target=target
        super().__init__(mass,b,n=nspace,f=f,flat=flat,seed=seed,spacing=spacing)
        # Velocity quadrature samples share initial spatial nodes, then stream
        # independently. Fixed mass at each node preserves initial gravity.
        self.x=np.repeat(self.x,nvel,axis=0);self.m=np.repeat(self.m/nvel,nvel)
        self.n=nspace*nvel;self.state=np.zeros(2*self.n,dtype=bool)
        E,acc,_=self.energy_force(self.x,self.state)
        r=np.linalg.norm(self.x,axis=1);er=self.x/r[:,None]
        vc=np.sqrt(np.maximum(-np.sum(acc*er,axis=1)*r,1e-8))
        random=self.rng.normal(size=(2*self.n,3));random-=np.sum(random*er,axis=1)[:,None]*er
        random/=np.linalg.norm(random,axis=1)[:,None]
        az=np.column_stack([-self.x[:,1],self.x[:,0],np.zeros(2*self.n)]);az/=np.linalg.norm(az,axis=1)[:,None]
        tangent=random.copy();tangent[:self.n]=f*az[:self.n]+np.sqrt(1-f*f)*random[:self.n]
        tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        self.v=vc[:,None]*(np.sqrt(.7)*tangent-.3*er);self.v-=np.average(self.v,axis=0,weights=self.m)
        self.initialE=E+self.kinetic(self.v);self.norm=max(abs(E),abs(self.initialE))
        self.L0=np.sum(self.m[:,None]*np.cross(self.x,self.v),axis=0);self.P0=np.sum(self.m[:,None]*self.v,axis=0)
        self.Lscale=np.sum(self.m*np.linalg.norm(np.cross(self.x,self.v),axis=1));self.Pscale=np.sum(self.m*np.linalg.norm(self.v,axis=1))
        self.stats.update(expected_medium_proposals=0.,expected_cooling_proposals=0.,max_cell_width_over_mfp=0.,
                          max_molecular_range_over_cell=0.,max_macro_separation_kpc=0.)
        self.progress_path=None

    def energy_force(self,x,state):
        E,acc,meta=super().energy_force(x,state)
        # Constant full-density self contribution: no force or numerical repair.
        self_term=-.5*np.sum(self.m*self.m)/self.soft
        meta['phi']=meta['phi']-self.m/self.soft
        return E+self_term,acc,meta

    def partition(self,x):return leaves(x,self.max_width,self.target*self.nvel)

    def pairs(self,x,v):
        tree=self.partition(x)
        i,j,normal,speed,dist,volume=cell_pairs(x,v,self.n,tree,self.seed)
        keep=speed>0
        self._volumes=volume[keep]
        return i[keep],j[keep],normal[keep],self.cross_section*self.m[i[keep]]*speed[keep]/volume[keep],dist[keep]

    def swept_limit(self,old,new):
        width=np.empty(len(old))
        for ids,h,_ in self.partition(old):width[ids]=h
        return bool(np.any(np.linalg.norm(new-old,axis=1)>self.dt_motion*width))

    def collide(self,dt):
        i,j,normal,rates,dist=self.pairs(self.x,self.v)
        self.stats['eligible_pair_samples']+=len(i)
        volumes=self._volumes.copy()
        self.stats['expected_medium_proposals']+=float(np.sum(rates[j>=self.n])*dt)
        self.stats['expected_cooling_proposals']+=float(np.sum(rates[j<self.n])*dt)
        for p in self.rng.permutation(len(i)):
            a=int(i[p]);b=int(j[p]);nn=normal[p]
            # Recompute speed after previous impulses; radius remains unchanged.
            speed=-float((self.v[b]-self.v[a])@nn)
            if speed<=0:continue
            rate=self.cross_section*self.m[a]*speed/(volumes[p])
            self.stats['max_encounter_hazard_step']=max(self.stats['max_encounter_hazard_step'],rate*dt)
            if self.rng.random()>-np.expm1(-rate*dt):continue
            self.stats['max_macro_separation_kpc']=max(self.stats['max_macro_separation_kpc'],float(dist[p]*self.b))
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
        out=super().snapshot(t);tree=self.partition(self.x);occupied=[];widths=[];cover=0.;kninv=0.
        for ids,h,_ in tree:
            nb=int(sum(ids<self.n));nf=int(sum(ids>=self.n))
            if nf:
                occupied.append(nb);widths.append(h)
                if nb:cover+=sum(self.m[ids[ids>=self.n]])
            rho=sum(self.m[ids[ids<self.n]])/h**3
            kninv=max(kninv,h*self.cross_section*rho)
        out.update(kinetic_cells=len(tree),mixed_medium_mass_fraction=cover/RESERVOIR,
                   max_cell_width_over_mfp=kninv,median_medium_cell_width=float(np.median(widths)),
                   median_cell_baryon_samples=float(np.median(occupied)),max_width=self.max_width)
        if hasattr(self,'stats') and 'max_cell_width_over_mfp' in self.stats:
            self.stats['max_cell_width_over_mfp']=max(self.stats['max_cell_width_over_mfp'],kninv)
            self.stats['max_molecular_range_over_cell']=max(self.stats['max_molecular_range_over_cell'],max(self.capture_h/h for _,h,_ in tree))
        if self.progress_path:
            Path(self.progress_path).write_text(json.dumps(dict(t=t,q=out['q'],energy_error=out['energy_error'],stats=self.stats),indent=2)+'\n')
        return out

    def run(self,*args,**kwargs):
        row=super().run(*args,**kwargs);row.update(nspace=self.nspace,nvel=self.nvel,max_width=self.max_width,target=self.target)
        return row
