import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from field import Field3D
from simulate import Simulation,reaction_impulse,RESERVOIR

def main():
    out={};x=np.array([[.2,.3,-.1],[1.7,-.6,.8]]);m=np.array([.21,.17]);k=.15
    f=Field3D(k,1,12,.75);E,g,meta=f.evaluate(x,m);errs=[]
    for i in range(2):
        for j in range(3):
            dx=np.zeros_like(x);dx[i,j]=1e-5
            fd=(f.evaluate(x+dx,m,False)[0]-f.evaluate(x-dx,m,False)[0])/2e-5
            errs.append(abs(fd-g[i,j])/max(abs(g[i,j]),1e-8))
    out['gradient_relative_error']=max(errs);assert max(errs)<1e-4
    fixtures=[]
    for spacing,extent in ((1.5,12),(.75,12),(.375,12),(.75,24)):
        ff=Field3D(k,1,extent,spacing);ee,gg,mm=ff.evaluate(x,m)
        fixtures.append(dict(spacing=spacing,extent=extent,energy=ee,gradient=gg.tolist(),**mm))
    out['mesh_fixtures']=fixtures
    out['fine_energy_relative_change']=abs(fixtures[1]['energy']/fixtures[2]['energy']-1)
    out['fine_force_relative_change']=float(np.linalg.norm(np.array(fixtures[1]['gradient'])-fixtures[2]['gradient'])/np.linalg.norm(fixtures[2]['gradient']))
    out['box_energy_relative_change']=abs(fixtures[1]['energy']/fixtures[3]['energy']-1)
    # Independent radial integral for one Gaussian, over all space.
    ff=Field3D(.2,1,12,.5);mm=np.array([.3]);xx=np.zeros((1,3));ee,gg,meta=ff.evaluate(xx,mm)
    def integrand(r):
        kernel=ff.kernel(np.array([[r,0,0]]))[0][0];z=mm[0]*r*kernel/.2
        return .2**2*r*r*(sum(z**j/j for j in range(2,14)) if z<.03 else -np.log1p(-z)-z)
    ref=quad(integrand,0,np.inf,epsabs=1e-11)[0]
    out['spherical_benchmark_relative_error']=abs(ee/ref-1)
    # Same radii and COM, different 3D geometry: square vs elongated rectangle.
    aa=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0.]])
    bb=np.array([[.98,.199,0],[-.98,-.199,0],[.98,-.199,0],[-.98,.199,0.]])
    bb/=np.linalg.norm(bb,axis=1)[:,None]
    out['same_radii_distinct_geometry_energies']=[f.evaluate(q,np.full(4,.07),False)[0] for q in (aa,bb)]
    # Mesh symmetry defects explicitly measured, not projected away.
    theta=.63;R=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    f=Field3D(k,1,12,.375);ee,gg,_=f.evaluate(x,m)
    out['translation_energy_relative_error']=abs(f.evaluate(x+[.37,.19,-.23],m,False)[0]/ee-1)
    out['rotation_energy_relative_error']=abs(f.evaluate(x@R.T,m,False)[0]/ee-1)
    out['net_force_over_individual_force']=float(np.linalg.norm(np.sum(gg,axis=0))/np.sum(np.linalg.norm(gg,axis=1)))
    # Finite field energy supplied in an actual close pair impulse.
    pos=np.array([[.04,0,0.]]);mass=np.array([.03]);delta=f.evaluate(pos,mass,False)[0]
    vi=np.array([-2.,.2,0]);vj=np.array([0.,-.3,0]);mi=.03;mj=.02;n=np.array([1.,0,0])
    proposal=reaction_impulse(vi,vj,mi,mj,n,delta);loss=.91*(proposal[2]-delta)
    a,b,_=reaction_impulse(vi,vj,mi,mj,n,delta+loss)
    out['radiative_energy_absolute_error']=abs(.5*mi*(a@a-vi@vi)+.5*mj*(b@b-vj@vj)+delta+loss)
    out['impulse_momentum_error']=float(np.linalg.norm(mi*(a-vi)+mj*(b-vj)))
    # Actual locality exclusion and swept-encounter detection.
    s=Simulation(1e8,1,n=16);s.x[:]=np.arange(32)[:,None]*np.array([3.,0,0]);s.v[:]=0
    s.x[16]=s.x[0]+[.099,0,0];s.v[16]=[-1,0,0]
    out['inside_pair_count']=len(s.pairs(s.x,s.v)[0]);assert out['inside_pair_count']==1
    s.x[16]=s.x[0]+[.101,0,0];out['outside_pair_count']=len(s.pairs(s.x,s.v)[0]);assert out['outside_pair_count']==0
    old=s.x.copy();new=s.x.copy();old[16]=[.3,0,0];new[16]=[-.3,0,0]
    out['crossing_detected']=s.swept_limit(old,new);assert out['crossing_detected']
    # Packet self-energy scaling is a real resolution cost, not removed by hand.
    out['packet_self_energy']=[dict(n=n,energy=Field3D(10,1,12,1).evaluate(np.zeros((1,3)),np.array([RESERVOIR/n]),False)[0]) for n in (32,64,128,256)]
    for key in ('fine_energy_relative_change','fine_force_relative_change','box_energy_relative_change','spherical_benchmark_relative_error'):
        assert out[key]<.05,(key,out[key])
    assert out['radiative_energy_absolute_error']<1e-12
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=main();Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
