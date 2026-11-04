"""Conservative diagram-norm gauge-annihilation bounds at actual warm population."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'));import numpy as np
from common import CommonBackground

def gammas():
 I=np.eye(2);Z=np.zeros((2,2));s=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];return np.array([np.block([[I,Z],[Z,-I]])]+[np.block([[Z,a],[-a,Z]]) for a in s])
GG=gammas()
def sl(p):return np.einsum('...i,ijk->...jk',p*np.array([1,-1,-1,-1]),GG)

def fermion_bound(beta,order):
 z,w=np.polynomial.legendre.leggauss(order);sn=np.sqrt(1-z*z);E=1/math.sqrt(1-beta*beta);p=E*beta;P1=np.array([E,0,0,p]);P2=np.array([E,0,0,-p]);k1=np.c_[np.full(order,E),E*sn,np.zeros(order),E*z];k2=np.c_[np.full(order,E),-E*sn,np.zeros(order),-E*z];eps=[np.c_[np.zeros(order),z,np.zeros(order),-sn],np.tile([0.,0.,1.,0.],(order,1))];U=sl(P1)+np.eye(4);V=sl(P2)-np.eye(4);nt=nu=ns=0*sn
 for ea in eps:
  for eb in eps:
   At=sl(eb)@(sl(P1-k1)+np.eye(4))@sl(ea)/(-2*E*E*(1-beta*z))[:,None,None];Au=sl(ea)@(sl(P1-k2)+np.eye(4))@sl(eb)/(-2*E*E*(1+beta*z))[:,None,None];dot=ea[:,0]*eb[:,0]-np.sum(ea[:,1:]*eb[:,1:],axis=1);As=sl(k1-k2)*dot[:,None,None]/(4*E*E)
   def norm(A):
    bar=GG[0]@A.conj().transpose(0,2,1)@GG[0];return np.maximum(0,np.trace(V@A@U@bar,axis1=1,axis2=2).real/4)
   nt=nt+norm(At);nu=nu+norm(Au);ns=ns+norm(As)
 bound=1.5*((25/24)*(nt+nu)+(11/12)*ns);return float(w@bound/(64*math.pi*E*E))

def main(out):
 start=time.monotonic();warm=json.loads((HERE.parent/'run_population002/result.json').read_text());q=np.array(warm['q']);T=warm['Tc'];x=warm['x'];data=CommonBackground().at(x);Y=np.array(warm['endpoints']['full']['Y']).reshape(30,len(q));g=math.sqrt(29/200)*.003;H=math.sqrt(math.pi**2*106.75/90)*T*T*2e6/(2.435e18*.02**2);betas=np.unique(np.r_[np.linspace(0,.9,17),1-np.geomspace(.1,1e-5,91)]);tab=[]
 for order in (128,256):tab.append(np.array([fermion_bound(b,order) for b in betas]))
 z,w=np.polynomial.legendre.leggauss(16);rows=[];total=float(T**3*sum(Y[i].sum() for i,G in enumerate(data['groups']) if G['charged']));Ctotal=Ftotal=0
 for i,G in enumerate(data['groups']):
  if not G['charged'] or G['kind'] not in ('S','F'):continue
  m=G['mass'];en=np.sqrt(m*m+(T*q)**2);n=T**3*Y[i];nn=float(n.sum())
  if G['kind']=='S':loss=(300*g**4/(32*math.pi))*float((n/en).sum())**2/(2*max(nn,1e-300));relquad=0.;Ctotal+=loss*nn
  else:
   s=2*m*m+2*(en[:,None,None]*en[None,:,None]-(T*q)[:,None,None]*(T*q)[None,:,None]*z);b=np.sqrt(np.maximum(0,1-4*m*m/s));boost=s/(4*en[:,None,None]*en[None,:,None]);vals=[]
   for v in tab:
    sigma=g**4/m**2*np.interp(b,betas,v)*boost;rate=.5*float(np.sum(n[:,None,None]*n[None,:,None]*sigma*w[None,None,:]/2))/max(nn,1e-300);vals.append(rate)
   loss=1.05*vals[1];relquad=abs(vals[0]/vals[1]-1);Ftotal+=loss*nn
  rows.append(dict(group=G['id'],mass_mu=m,physical_number_mu3=nn,chemical_fractional_loss_over_H_bound=loss/H,contribution_to_all_charged_loss_over_H_bound=loss*nn/(H*total),fermion_angular_refinement_relative=relquad))
 vecnums={G['id']:float(T**3*Y[i].sum()) for i,G in enumerate(data['groups']) if G['kind']=='V'};checks=dict(finite=bool(all(np.isfinite(r['chemical_fractional_loss_over_H_bound']) for r in rows)),fermion_angle_refine=bool(max(r['fermion_angular_refinement_relative'] for r in rows)<.01),small_sum=bool((Ctotal+Ftotal)/(H*total)<.01))
 Path(out).write_text(json.dumps(dict(Tc=T,x=x,H_mu=H,rows=rows,all_charged_scalar_gauge_ann_loss_over_H_bound=Ctotal/(H*total),all_charged_fermion_gauge_ann_loss_over_H_bound=Ftotal/(H*total),vector_physical_numbers=vecnums,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actualconditionalwarmfull30population atfixedx after3Vlifetimes. Bounds coverC-Cstar andF-Fbar→allunbrokengaugepairs: scalarpointwise4-diagramnormbound300; fermion3-diagramtriangleboundwithactualDiracspintraces andpositiveangularquadrature,5%inflationplusrefinement. Noexactcrosssectionassertion. Vector-pairannihilationnotboundedbytheseS/Fdiagrams; physicalVdensitiesreported. Newfreshhistoryandoccupiedloopgaugefinalbathsnotimplicitlycovered.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
