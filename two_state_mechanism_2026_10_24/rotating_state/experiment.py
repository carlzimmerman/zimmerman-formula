import argparse,json
import numpy as np

class Model:
    def __init__(self,N=32,L=16,h=.5,eps=1.):
        self.N=N;self.L=L;self.h=h;self.ms=np.array([1.,eps]);self.q=np.array([1.,-1.]);self.dv=(L/N)**3
        a=(np.arange(N)-N//2)*L/N
        self.xyz=np.array(np.meshgrid(a,a,a,indexing='ij'));self.r=np.sqrt(np.sum(self.xyz**2,axis=0))
        k=2*np.pi*np.fft.fftfreq(N,L/N);self.k=np.array(np.meshgrid(k,k,k,indexing='ij'));self.k2=np.sum(self.k**2,axis=0)
        self.inv=np.zeros_like(self.k2);np.divide(4*np.pi,self.k2,out=self.inv,where=self.k2>0)
        self.pb=-1/5.364/np.sqrt(self.r**2+1)
    def fields(self,p):
        d=abs(p)**2;rm=np.einsum('s,sijk->ijk',self.ms,d);rq=d[0]-d[1]
        pg=-np.fft.ifftn(np.fft.fftn(rm)*self.inv).real
        pe=np.fft.ifftn(np.fft.fftn(rq)*self.inv).real
        return d,rm,rq,pg,pe
    def potential(self,p):
        d,rm,rq,pg,pe=self.fields(p)
        return self.ms[:,None,None,None]*(pg+self.pb)+self.q[:,None,None,None]*pe
    def grad(self,a):return np.array([np.fft.ifftn(1j*k*np.fft.fftn(a)) for k in self.k])
    def initial(self,spin,offset=0):
        x,y,z=self.xyz;waves=[]
        for s,ms in enumerate(self.ms):
            wave=np.zeros_like(x,dtype=complex)
            for sign in [-1,1]:
                center=sign*1.6+(offset if s==1 else 0)
                g=np.exp(-((x-center)**2+y*y+z*z)/(4*.8**2))
                phase=ms/self.h*(-sign*.2*x+sign*spin*y)
                wave+=g*np.exp(1j*phase)
            wave*=np.sqrt((1/sum(self.ms))/(np.sum(abs(wave)**2)*self.dv));waves.append(wave)
        return np.array(waves)
    def measure(self,p):
        d,rm,rq,pg,pe=self.fields(p);kin=np.zeros_like(rm);Lz=0.
        for s in range(2):
            grad=self.grad(p[s]);kin+=self.h**2/(2*self.ms[s])*np.sum(abs(grad)**2,axis=0)
            Lz+=self.h*np.sum(np.imag(np.conj(p[s])*(self.xyz[0]*grad[1]-self.xyz[1]*grad[0])))*self.dv
        ed=kin+rm*self.pb+.5*rm*pg+.5*rq*pe;core=self.r<2.5
        ag=-self.grad(pg+self.pb).real;ae=-self.grad(pe).real
        g2=np.sum(ag*ag,axis=0);ratio=-np.sum(ae*ag,axis=0)/np.maximum(g2,1e-20)
        support=(ratio>.5)&(ratio<1.5)&(g2>1e-12)
        return dict(energy=float(np.sum(ed)*self.dv),kinetic=float(np.sum(kin)*self.dv),
            absolute_energy_scale=float(np.sum(kin+abs(rm*self.pb)+abs(.5*rm*pg)+abs(.5*rq*pe))*self.dv),
            core_energy=float(np.sum(ed*core)*self.dv),exterior_energy=float(np.sum(ed*~core)*self.dv),
            core_mass=float(np.sum(rm*core)*self.dv),exterior_mass=float(np.sum(rm*~core)*self.dv),
            outer_mass=float(np.sum(rm*(self.r>6.5))*self.dv),
            species_norms=(np.sum(d,axis=(1,2,3))*self.dv).tolist(),
            charge_separation_L1=float(np.sum(abs(rq))*self.dv),Lz=float(Lz),
            electric_support_fraction=float(np.sum(d[0]*support)/np.sum(d[0])))

def evolve(N,h,eps,spin,offset=0,dt=.01,duration=1.):
    model=Model(N=N,h=h,eps=eps);p=model.initial(spin,offset)
    first=model.measure(p);records=[first]
    phase=np.exp(-1j*dt*h/(2*model.ms[:,None,None,None])*model.k2)
    steps=round(duration/dt);assert abs(steps*dt-duration)<1e-12
    for j in range(steps):
        p*=np.exp(-.5j*dt/model.h*model.potential(p))
        p=np.fft.ifftn(np.fft.fftn(p,axes=(1,2,3))*phase,axes=(1,2,3))
        p*=np.exp(-.5j*dt/model.h*model.potential(p))
        if (j+1)%5==0:records.append(model.measure(p))
    final=records[-1]
    return dict(N=N,h=h,epsilon=eps,spin_speed=spin,offset=offset,dt=dt,duration=duration,
        initial=first,final=final,
        max_energy_error=max(abs(r['energy']-first['energy']) for r in records)/first['absolute_energy_scale'],
        max_number_error=max(np.max(abs(np.array(r['species_norms'])-first['species_norms'])) for r in records),
        max_partition_error=max(abs(r['energy']-r['core_energy']-r['exterior_energy']) for r in records),
        max_outer_mass=max(r['outer_mass'] for r in records),
        max_Lz_drift=max(abs(r['Lz']-first['Lz']) for r in records)),p

def mapping():
    G=6.67430e-11;HB=1.054571817e-34;C=299792458.;EV=1.7826619216279e-36;MS=1.98847e30;KP=3.085677581491367e19;eta=5.364
    profiles=[(3e5,.3),(1e8,1.),(6e10,3.),(1e14,300.)];rows=[]
    for eps in [.1,1.]:
        for m in np.geomspace(1e-27,1e-19,241):
            group=[]
            for Mb,b in profiles:
                Md=eta*Mb*MS;R=b*KP;mtot=(1+eta)*Mb*MS;h=HB/(m*EV*np.sqrt(G*Md*R));v=np.sqrt(G*mtot/R)
                group.append(dict(Mb=Mb,b=b,h=float(h),phase_resolved=bool(4*.5/h<32*np.pi/16),
                    nonrelativistic=bool(HB/(eps*m*EV*R*C)<.1),
                    coherent_dipole_loss_per_dynamical_time=float(4/3*eta/(1+eta)/(1+eps)**2*(v/C)**3)))
            rows.append(dict(m_eV=float(m),epsilon=eps,profiles=group,all_necessary_conditions=all(r['phase_resolved'] and r['nonrelativistic'] for r in group)))
    return rows

def main(output,refine=False):
    rows=[];states={}
    if not refine:
        for h in [.5,1.]:
            for eps,offset in [(1.,0.),(1.,.05),(.1,0.)]:
                for spin in [0.,.5]:
                    r,p=evolve(32,h,eps,spin,offset);rows.append(r)
    else:
        for N in [32,48]:
            for dt in [.01,.005,.0025]:
                r,p=evolve(N,.5,1.,.5,.05,dt);rows.append(r);states[N,dt]=p
    result=dict(runs=rows)
    if refine:
        result['time_refinement']=[dict(N=N,coarse_medium=float(np.linalg.norm(states[N,.01]-states[N,.005])/np.linalg.norm(states[N,.005])),medium_fine=float(np.linalg.norm(states[N,.005]-states[N,.0025])/np.linalg.norm(states[N,.0025]))) for N in [32,48]]
    else:result['physical_mapping']=mapping()
    with open(output,'w') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(runs=len(rows),max_energy=max(r['max_energy_error'] for r in rows),max_outer=max(r['max_outer_mass'] for r in rows))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--refine',action='store_true');a=p.parse_args();main(a.output,a.refine)
