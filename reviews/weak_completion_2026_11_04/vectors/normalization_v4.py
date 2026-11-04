import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
import numpy as np
from common import CommonBackground
from gauge_basis_v1 import build
from rates_v2 import channels,matrix_element
from network import signed_lift

def gamma_matrices():
 I=np.eye(2);Z=np.zeros((2,2));pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];g=[np.block([[I,Z],[Z,-I]])]+[np.block([[Z,s],[-s,Z]]) for s in pauli];g5=1j*g[0]@g[1]@g[2]@g[3];return g,g5

def main(out):
 start=time.monotonic();g,g5=gamma_matrices();PL=(np.eye(4)-g5)/2;PR=(np.eye(4)+g5)/2;I=np.eye(4);zz,wz=np.polynomial.legendre.leggauss(96);groups=[dict(id='F',kind='F'),dict(id='f',kind='F'),dict(id='Vc_L',kind='V'),dict(id='Vc_T',kind='V')];q=.3+.4j;A=abs(q)**2;B=(q*q).real;tracecontrols=[]
 def slash(k):return k[0]*g[0]-sum(k[i]*g[i] for i in range(1,4))
 def vertex(e):return (e[0]*g[0]-sum(e[i]*g[i] for i in range(1,4)))@(q*PL-q.conjugate()*PR)
 # Independent Dirac spin traces for F->FV and V->FF.
 M,m,mv=.2,.031,.074;p=math.sqrt((M-m-mv)*(M+m+mv)*(M-m+mv)*(M+m-mv))/(2*M);E1=(M*M+m*m-mv*mv)/(2*M);E2=M-E1;P=np.array([M,0,0,0]);k=np.array([E1,0,0,p]);ee=[np.array([p/mv,0,0,-E2/mv]),np.array([0,1,0,0]),np.array([0,0,1,0])]
 for h,e in enumerate(ee):
  V=vertex(e);bar=g[0]@V.conj().T@g[0];direct=float((np.trace((slash(k)+m*I)@V@(slash(P)+M*I)@bar)/2).real);c=dict(p=0,j=1,k=2 if h==0 else 3,kind='F_FV',A=A,B=B,K=0);formula=float(matrix_element(c,M,m,mv,np.array([0.]),np.array([1.]),groups)[0])/(2 if h>0 else 1);tracecontrols.append(dict(kind='F_FV',polarization=h,trace=direct,formula=formula,relative_error=abs(direct/formula-1)))
 M,m1,m2=.2,.031,.047;p=math.sqrt((M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2))/(2*M);z=.37;E1=(M*M+m1*m1-m2*m2)/(2*M);k1=np.array([E1,p*math.sqrt(1-z*z),0,p*z]);k2=np.array([M-E1,-k1[1],0,-k1[3]])
 for h,e in enumerate([np.array([0,0,0,1]),np.array([0,1,1j,0])/math.sqrt(2),np.array([0,1,-1j,0])/math.sqrt(2)]):
  V=vertex(e);bar=g[0]@V.conj().T@g[0];direct=float(np.trace((slash(k1)+m1*I)@V@(slash(k2)-m2*I)@bar).real);c=dict(p=2 if h==0 else 3,j=0,k=1,kind='V_FF',A=A,B=B,K=0);formula=float(matrix_element(c,M,m1,m2,np.array([0.]),np.array([z]),groups)[0]);tracecontrols.append(dict(kind='V_FF',polarization=h,trace=direct,formula=formula,relative_error=abs(direct/formula-1)))
 # Absolute normalizations: one complex scalar, one Weyl, one Dirac pair.
 normal=[];M=.2;coup=.003
 for kind,fac,expected in [('V_SS',1,coup*coup*M/(48*math.pi)),('V_FF',.5,coup*coup*M/(24*math.pi)),('V_FF',1,coup*coup*M/(12*math.pi))]:
  c=dict(p=2,j=0,k=1,kind=kind,A=fac*coup*coup,B=fac*coup*coup,K=0);calc=float(wz@matrix_element(c,M,0,0,0*zz,zz,groups))/(32*math.pi*M);normal.append(dict(kind=kind,coupling_factor=fac,width=calc,expected=expected,relative_error=abs(calc/expected-1)))
 bg=CommonBackground();rows=[];Pmats=[]
 for x in (3.8632233,5.,25.4000254000381):
  b=build(x);actual={a['id']:a for a in b['s']['groups']};gr=bg.at(x)['groups'];by={g['id']:i for i,g in enumerate(gr)};masses=np.array([g['mass'] for g in gr]);ids=b['vgroups']['Vc'];nv=len(ids);mv=masses[25];Gamma=np.zeros((nv,nv));vchannels=[];P=np.array(next(g['indices'] for g in b['s']['groups'] if g['id']=='S1_1'));M=masses[by['S1_1']];pm=[]
  for ia,Ia in enumerate(gr[:25]):
   kind=Ia['kind'];ii=np.array(actual[Ia['id']]['indices'])-(98 if kind=='F' else 0)
   for jb,Jb in enumerate(gr[:25]):
    if Jb['kind']!=kind or jb<ia:continue
    jj=np.array(actual[Jb['id']]['indices'])-(98 if kind=='F' else 0);m1,m2=masses[[ia,jb]]
    if mv<=m1+m2:continue
    cur=b['qs' if kind=='S' else 'qf'][np.ix_(ids,ii,jj)];f=b['d']['g']**2/(2 if ia==jb else 1);aa=f*np.einsum('iab,jab->ij',cur,cur.conj()).real;bb=f*np.einsum('iab,jab->ij',cur,cur).real;ps=math.sqrt((mv-m1-m2)*(mv+m1+m2)*(mv-m1+m2)*(mv+m1-m2))/(2*mv);beta=2*ps/mv
    mat=beta/(16*math.pi*mv)*((4/3)*aa*ps*ps if kind=='S' else 4*(aa*((mv*mv-m1*m1-m2*m2)/2-2*ps*ps/3)-bb*m1*m2));Gamma+=mat;
    if float(np.trace(mat)/nv)>1e-25:vchannels.append(dict(parent='Vc_L',daughters=[Ia['id'],Jb['id']],width=float(np.trace(mat)/nv)))
  for J in gr[:25]:
   if J['kind']!='S' or M<=J['mass']+mv:continue
   jj=np.array(actual[J['id']]['indices']);cur=b['qs'][np.ix_(ids,P,jj)];am=b['d']['g']**2*np.einsum('iaj,ibj->ab',cur,cur.conj()).real;ps=math.sqrt((M-J['mass']-mv)*(M+J['mass']+mv)*(M-J['mass']+mv)*(M+J['mass']-mv))/(2*M);mat=ps/(8*math.pi*M*M)*(4*M*M*ps*ps/(mv*mv))*am
   if np.linalg.norm(mat)>1e-25:pm.append(dict(daughters=[J['id'],'Vc'],Gamma=mat.tolist(),current_Gram=am.tolist(),width_average=float(np.trace(mat)/4)))
  if M>2*mv:
   K=b['K'][np.ix_(P,ids,ids)];gram=np.einsum('aij,bij->ab',K,K)/2;beta=math.sqrt(1-4*mv*mv/(M*M));polar=2+(M*M-2*mv*mv)**2/(4*mv**4);mat=beta*polar/(16*math.pi*M)*gram;pm.append(dict(daughters=['Vc','Vc'],Gamma=mat.tolist(),K_Gram_half=gram.tolist(),width_average=float(np.trace(mat)/4)))
  actualchannels=next(r['channels'] for r in json.loads((HERE/'run_transport003/result.json').read_text())['rows'] if abs(r['x']-x)<1e-8);species,lift=signed_lift(dict(groups=gr,channels=actualchannels));Q={a['id']:a['charge'] for a in species};chargeerr=max([abs(Q[c['parent']]-sum(Q[a] for a in c['daughters'])) for c in lift]+[0]);cl=b['vgroups'];vvvforbidden=float(np.max(abs(b['qv'][np.ix_(ids,np.r_[cl['V8'],cl['V3'],cl['V1']],np.r_[cl['V8'],cl['V3'],cl['V1']])])));Pmats.append(dict(x=x,parent_indices=P.tolist(),canonical_O_columns=b['O'][:,P].tolist(),channels=pm,total_width_average=float(sum(a['width_average'] for a in pm))))
  rows.append(dict(x=x,vector_width=float(np.trace(Gamma)/nv),irrep_width_matrix_relative=float(np.linalg.norm(Gamma-np.trace(Gamma)/nv*np.eye(nv))/max(np.linalg.norm(Gamma),1e-100)),positive_eigenvalues=np.linalg.eigvalsh(Gamma).tolist(),signed_charge_error=chargeerr,forbidden_one_broken_two_unbroken_VVV=vvvforbidden,controls=b['controls']))
 checks=dict(Dirac_trace=bool(max(c['relative_error'] for c in tracecontrols)<1e-12),absolute_normalizations=bool(max(c['relative_error'] for c in normal)<1e-12),vector_irrep_degeneracy=bool(max(r['irrep_width_matrix_relative'] for r in rows)<1e-10),charge=bool(all(r['signed_charge_error']==0 for r in rows)),VVV_closed=bool(max(r['forbidden_one_broken_two_unbroken_VVV'] for r in rows)<1e-10),Majorana_parity=bool(all(r['controls']['Majorana_parity_asymmetry']==0 for r in rows)))
 Path(out).write_text(json.dumps(dict(trace_controls=tracecontrols,absolute_normalizations=normal,cases=rows,singlet_absorptive_matrices=Pmats,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Independent spin traces and raw-color width matrices; actual signed charge lift; actual four-parent vector absorptive Gram matrices with canonical frame columns. P matrices are rest-polarization summed, no P decoherence assertion.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
