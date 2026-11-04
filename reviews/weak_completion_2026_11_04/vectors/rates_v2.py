"""Canonical-current invariant tables and covariant spin-resolved matrix elements."""
import math
import numpy as np

def channels(record,groups):
 by={g['id']:i for i,g in enumerate(groups)};m=np.array([g['mass'] for g in groups]);out=[]
 def put(p,j,k,kind,A=0.,B=0.,K=0.):
  p,j,k=[by[t] for t in (p,j,k)]
  if m[p]>m[j]+m[k]+1e-13:out.append(dict(p=p,j=j,k=k,kind=kind,A=A,B=B,K=K,parent=groups[p]['id'],daughters=[groups[j]['id'],groups[k]['id']]))
 for r in record['invariants']:
  if r['vector']!='Vc':continue # residual currents commute their masses: all 1->2 cuts closed
  i=r['i'];j=r.get('j');typ=r['kind']
  if typ in ('VSS','VFF'):
   for v in ('Vc_L','Vc_T'):
    # Both orientations exist in the invariant records; choose the heavier one.
    put(i,j,v,'S_SV' if typ=='VSS' else 'F_FV',r['A']/r['n_i'],r['B']/r['n_i'])
    if by[i]<=by[j]:put(v,i,j,'V_SS' if typ=='VSS' else 'V_FF',r['A']/r['n_v']/(2 if i==j else 1),r['B']/r['n_v']/(2 if i==j else 1))
  else:
   put(i,'Vc_L','Vc_L','S_VV',K=r['K2']/r['n_i']/2)
   put(i,'Vc_L','Vc_T','S_VV',K=r['K2']/r['n_i'])
   put(i,'Vc_T','Vc_T','S_VV',K=r['K2']/r['n_i']/2)
 return out

def dot(a,b):return a[...,0]*b[...,0]-np.sum(a[...,1:]*b[...,1:],axis=-1)

def polarization(k,m):
 p=np.linalg.norm(k[...,1:],axis=-1);n=np.divide(k[...,1:],p[...,None],out=np.zeros_like(k[...,1:]),where=p[...,None]>1e-280);n=np.where((p<1e-280)[...,None],np.array([0.,0.,1.]),n)
 L=np.concatenate([(p/m)[...,None],k[...,0,None]/m*n],axis=-1)
 return L,n

def proj_T(a,n):return np.maximum(0,np.sum(a[...,1:]**2,axis=-1)-np.sum(a[...,1:]*n,axis=-1)**2)

def matrix_element(c,M,m1,m2,P,z,groups):
 """Spin sum over daughters, average only the specified initial polarization.

 T denotes two equal circular helicities. For a T parent average over two;
 for a T daughter sum over two. Matter fermions are unpolarized. Majorana
 V=i Im(Q), A=-Re(Q), so Re(V A*)=0 and no parity-odd helicity source exists.
 """
 P,z=np.broadcast_arrays(P,z);Ep=np.sqrt(M*M+P*P);star=(M*M+m1*m1-m2*m2)/(2*M);p=math.sqrt(max(0,(M-m1-m2)*(M+m1+m2)*(M-m1+m2)*(M+m1-m2)))/(2*M)
 k1=np.stack([Ep/M*star+P/M*p*z,p*np.sqrt(np.maximum(0,1-z*z)),np.zeros_like(z),Ep/M*p*z+P/M*star],axis=-1);parent=np.stack([Ep,np.zeros_like(P),np.zeros_like(P),P],axis=-1);k2=parent-k1;A=c['A'];B=c['B'];typ=c['kind'];pt=groups[c['p']]['id'].endswith('_T');jt=groups[c['j']]['id'].endswith('_T');kt=groups[c['k']]['id'].endswith('_T')
 if typ=='V_SS':
  value=A*(2*p)**2*((1-z*z)/2 if pt else z*z)
 elif typ=='V_FF':
  kd=(M*M-m1*m1-m2*m2)/2;eps=(p*p*(1-z*z)/2 if pt else p*p*z*z);value=4*(A*(kd-2*eps)-B*m1*m2)
 elif typ in ('S_SV','F_FV'):
  L,n=polarization(k2,m2);peT=P*P*(k2[...,1]**2+k2[...,2]**2)/np.maximum(np.sum(k2[...,1:]**2,axis=-1),1e-280);pe=peT if kt else np.maximum(0,M*M*p*p/(m2*m2)-peT)
  if typ=='S_SV':value=4*A*pe
  else:
   kp=(M*M+m1*m1-m2*m2)/2;mult=2 if kt else 1;value=2*(A*(2*pe+mult*kp)+mult*B*M*m1)
 elif typ=='S_VV':
  L1,n1=polarization(k1,m1);L2,n2=polarization(k2,m2)
  if jt and kt:value=c['K']*(1+np.sum(n1*n2,axis=-1)**2)
  elif jt:value=c['K']*proj_T(L2,n1)
  elif kt:value=c['K']*proj_T(L1,n2)
  else:value=c['K']*dot(L1,L2)**2
 else:raise ValueError(typ)
 if np.min(value,initial=0)<-1e-14*max(float(np.max(abs(value),initial=0)),1e-100):raise ValueError(('negative spin rate',c,float(np.min(value))))
 return np.maximum(value,0)

class VertexTable:
 def __init__(self,records):
  self.records=records;self.x=np.array([r['x'] for r in records]);keys=[]
  for r in records:
   for a in r['invariants']:
    key=(a['kind'],a['vector'],a['i'],a.get('j',''))
    if key not in keys:keys.append(key)
  self.templates={};self.values=np.zeros((len(records),len(keys),3));self.keys=keys
  for l,r in enumerate(records):
   for a in r['invariants']:
    key=(a['kind'],a['vector'],a['i'],a.get('j',''));k=keys.index(key);self.templates[key]=a
    self.values[l,k]=[a.get('A',0),a.get('B',0),a.get('K2',0)]
 def at(self,x):
  if x<self.x[0]-1e-12 or x>self.x[-1]+1e-12:raise ValueError(('vector vertex table support',x,self.x[[0,-1]]))
  k=int(np.clip(np.searchsorted(self.x,x)-1,0,len(self.x)-2));u=(x-self.x[k])/(self.x[k+1]-self.x[k]);v=(1-u)*self.values[k]+u*self.values[k+1];inv=[]
  for key,vals in zip(self.keys,v):
   a=dict(self.templates[key]);a.update(A=float(vals[0]),B=float(vals[1]),K2=float(vals[2]));inv.append(a)
  return dict(x=float(x),invariants=inv)
