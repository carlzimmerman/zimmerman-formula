import json,sys,time,resource,math
from pathlib import Path
import numpy as np
from model import build_model,component_data,graph_weights

def polynomial(Y,z,linear,R,g,mu=None):
    n=len(z)
    if mu is None:mu=np.zeros((n,n))
    ff=linear+mu@z+.5*np.einsum('ijk,j,k->i',Y,z,z)
    rz=np.einsum('aij,j->ai',R,z) if len(R) else np.zeros((0,n),complex)
    dd=g*np.einsum('i,ai->a',z.conj(),rz).real
    return float(np.vdot(ff,ff).real+.5*dd@dd)

def main(path):
    start=time.monotonic();e=.03;X=7.367143721278508*math.sqrt(e/31)/e;g=math.sqrt(29/200)*e
    d=build_model(X,e,e,g);w=graph_weights(d);Y=d['Y'];z=d['z'];linear=np.r_[1.+0j,np.zeros(48)]
    # Directional cubic/quartic contractions independently from polynomial values.
    v=np.cos(np.arange(98)+.31);v/=np.linalg.norm(v)
    direction=d['E']@d['O']@v
    cubic=float(np.einsum('abc,a,b,c',d['cubic'],v,v,v))
    # General quartic direction from original F/D homogeneous top coefficients.
    yf=np.einsum('ijk,j,k->i',Y,direction,direction)
    dq=g*np.einsum('i,aij,j->a',direction.conj(),d['R'],direction).real
    quartic=6*np.vdot(yf,yf).real+12*np.dot(dq,dq)
    poly=lambda t:polynomial(Y,z+t*direction,linear,d['R'],g)
    step=.02;vals={j:poly(j*step) for j in [-2,-1,0,1,2]}
    cubic_fd=(vals[2]-2*vals[1]+2*vals[-1]-vals[-2])/(2*step**3)
    quartic_fd=(vals[2]-4*vals[1]+6*vals[0]-4*vals[-1]+vals[-2])/step**4
    # Quartic_iijj uses an independent two-direction polynomial coefficient.
    i,j=7,41;u=d['E']@d['O'][:,i];v2=d['E']@d['O'][:,j]
    a=.1;b=.1
    cross=sum(sign*polynomial(Y,z+sx*a*u+sy*b*v2,linear,d['R'],g)
              for sx,sy,sign in [(1,1,1),(1,-1,1),(-1,1,1),(-1,-1,1)])
    cross-=2*(polynomial(Y,z+a*u,linear,d['R'],g)+polynomial(Y,z-a*u,linear,d['R'],g))
    cross-=2*(polynomial(Y,z+b*v2,linear,d['R'],g)+polynomial(Y,z-b*v2,linear,d['R'],g))
    cross+=4*polynomial(Y,z,linear,d['R'],g)
    quartic_pair_fd=cross/(a*a*b*b)
    # One-field WZ supersymmetric origin fixes all normalization factors by hand.
    toyY=np.ones((1,1,1),complex)*.7;toy=component_data(toyY,np.zeros(1,complex),np.zeros(1,complex),np.empty((0,1,1),complex),0.,mu=np.array([[1.3]]))
    tw=graph_weights(toy)
    expected={'SSS_total':.5*1.3**2*.7**2,'SS_total':.5*.7**2,'FFS_total':.5*.7**2,'barFFS_total':0.}
    actual={'SSS_total':float(np.sum(tw['SSS'])),'SS_total':float(np.sum(tw['SS'])),'FFS_total':float(np.sum(tw['FFS'])),'barFFS_total':float(np.sum(tw['barFFS']))}
    checks={k:val<1e-8 for k,val in d['controls'].items()}
    checks.update(cubic_permutation=max(float(np.max(abs(d['cubic']-d['cubic'].transpose(p)))) for p in [(1,0,2),(2,1,0)])<1e-10,
                  Yukawa_symmetric=float(np.max(abs(d['yukawa']-d['yukawa'].transpose(1,0,2))))<1e-12,
                  cubic_polynomial_derivative=abs(cubic-cubic_fd)<1e-7,
                  quartic_polynomial_derivative=abs(quartic-quartic_fd)<1e-6,
                  quartic_pair_derivative=abs(float(d['quartic_iijj'][i,j])-quartic_pair_fd)<1e-7,
                  WZ_graph_weights=all(abs(actual[k]-v)<1e-10 for k,v in expected.items()))
    checks={k:bool(v) for k,v in checks.items()}
    out={'claim_id':'FM_BUILDER','checks':checks,'spectrum_controls':d['controls'],
         'cubic_direction':{'analytic':cubic,'polynomial_fd':cubic_fd},'quartic_direction':{'analytic':float(quartic),'polynomial_fd':quartic_fd},
         'quartic_pair':{'indices':[i,j],'analytic':float(d['quartic_iijj'][i,j]),'polynomial_fd':quartic_pair_fd},
         'WZ_weights':{'actual':actual,'expected':expected},'scalar_groups':w['scalar_groups'],'fermion_groups':w['fermion_groups'],
         'runtime_seconds':time.monotonic()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'non_claims':['No two-loop numerical integral yet','Nonvector graph classes do not complete gauged potential']}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
