"""Spin-uniform Yang-Mills diagram-norm bound for warm V+V- gauge annihilation."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));import numpy as np
from common import CommonBackground

def dot(a,b):return a[...,0]*b[...,0]-np.sum(a[...,1:]*b[...,1:],axis=-1)
def current(e1,e2,k1,k2,k3):return dot(e1,e2)[...,None]*(k1-k2)+e2*dot(e1,k2-k3)[...,None]+e1*dot(e2,k3-k1)[...,None]

def bound(beta,order):
 z,w=np.polynomial.legendre.leggauss(order);ss=np.sqrt(1-z*z);E=1/math.sqrt(1-beta*beta);p=E*beta;P1=np.array([E,0,0,p]);P2=np.array([E,0,0,-p]);k1=np.c_[np.full(order,E),E*ss,np.zeros(order),E*z];k2=np.c_[np.full(order,E),-E*ss,np.zeros(order),-E*z];e1=[np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.]),np.array([p,0,0,E])];e2=[np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.]),np.array([p,0,0,-E])];ef=[np.c_[np.zeros(order),z,np.zeros(order),-ss],np.tile([0.,0.,1.,0.],(order,1))];value=np.zeros(order)
 for a in e1:
  for b in e2:
   for c in ef:
    for d in ef:
     qt=k1-P1;qu=k2-P1;J1=current(a,c,P1,-k1,qt);J2=current(b,d,P2,-k2,-qt);Lt=(-dot(J1,J2)+dot(J1,qt)*dot(J2,qt))/(dot(qt,qt)-1);J1=current(a,d,P1,-k2,qu);J2=current(b,c,P2,-k1,-qu);Lu=(-dot(J1,J2)+dot(J1,qu)*dot(J2,qu))/(dot(qu,qu)-1);J1=current(a,b,P1,P2,-P1-P2);J2=current(c,d,-k1,-k2,P1+P2);Ls=-dot(J1,J2)/(4*E*E);L4s=dot(a,c)*dot(b,d)-dot(a,d)*dot(b,c);L4t=dot(a,b)*dot(c,d)-dot(a,d)*dot(b,c);L4u=dot(a,b)*dot(d,c)-dot(a,c)*dot(b,d);value+=3*((25/24)*(Lt*Lt+Lu*Lu+L4t*L4t+L4u*L4u)+(11/12)*(Ls*Ls+L4s*L4s))
 # Full initial3x3 sum bounds any L/T mixture, including its boosted Wigner rotation.
 return float(w@value/(64*math.pi*E*E))

def main(out):
 start=time.monotonic();warm=json.loads((HERE.parent/'run_population002/result.json').read_text());sf=json.loads((HERE.parent/'run_warm_ann002/result.json').read_text());q=np.array(warm['q']);T=warm['Tc'];x=warm['x'];data=CommonBackground().at(x);Y=np.array(warm['endpoints']['full']['Y']).reshape(30,len(q));m=data['groups'][25]['mass'];H=sf['H_mu'];g=math.sqrt(29/200)*.003;betas=np.unique(np.r_[np.linspace(0,.9,17),1-np.geomspace(.1,1e-5,91)]);tab=[]
 for order in (96,192):tab.append(np.array([bound(b,order) for b in betas]))
 E=np.sqrt(m*m+(T*q)**2);z,w=np.polynomial.legendre.leggauss(20);s=2*m*m+2*(E[:,None,None]*E[None,:,None]-(T*q)[:,None,None]*(T*q)[None,:,None]*z);b=np.sqrt(np.maximum(0,1-4*m*m/s));boost=s/(4*E[:,None,None]*E[None,:,None]);n=T**3*(Y[25]+Y[26]);total=T**3*float(sum(Y[i].sum() for i,G in enumerate(data['groups']) if G['charged']));vals=[]
 for v in tab:
  sig=g**4/m**2*np.interp(b,betas,v)*boost;vals.append(.5*float(np.sum(n[:,None,None]*n[None,:,None]*sig*w[None,None,:]/2))/max(float(n.sum()),1e-300))
 loss=1.1*vals[-1];relative=abs(vals[0]/vals[1]-1);allloss=loss*float(n.sum())/(H*total);checks=dict(finite=bool(np.isfinite(allloss)),angular_refinement=bool(relative<.02));discriminator=dict(V_gauge_ann_subpercent=bool(allloss<.01),all_SFV_gauge_ann_subpercent=bool(allloss+sf['all_charged_scalar_gauge_ann_loss_over_H_bound']+sf['all_charged_fermion_gauge_ann_loss_over_H_bound']<.01))
 Path(out).write_text(json.dumps(dict(vector_physical_number_mu3=float(n.sum()),vector_fraction=float(n.sum())/total,vector_mass_mu=m,per_vector_annihilation_loss_over_H_bound=loss/H,all_charged_V_annihilation_loss_over_H_bound=allloss,all_charged_SFV_annihilation_loss_over_H_bound=allloss+sf['all_charged_scalar_gauge_ann_loss_over_H_bound']+sf['all_charged_fermion_gauge_ann_loss_over_H_bound'],angular_refinement_relative=relative,checks=checks,discriminator=discriminator,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualconditionalwarmmassiveVpopulation; pureYang-MillsV+V-→unbrokengaugepairs bounded bysix-componenttriangleinequality(t/u/s exchange+threequarticcolourterms), canonicalr6colourtraces andunitary-gaugemassivepropagator. Fullinitialspin sum bounds anyL/Tmixturewithoutspinclosureassumption; positiveCManglequadrature+10%inflation. Noexactinterferencecrosssectionclaim. Resonantscalar1↔2inversepathsarealreadyseparateandmustnotbedoublecounted; finalgaugepopulationsinthispacketempty. Boundappliesonlytestedwarmpacket.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
