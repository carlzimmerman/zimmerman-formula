"""Positive screened scalar Coulomb 2<->2 quadrature on physical number cells.

Exact two-body CM energies, derivative scalar current, three actual gauge colour
traces and separate isotropic Debye masses. Direct t-channel screened Born
kernel: controlled leading-log Coulomb physics, finite-log identical exchange
and contact terms remain excluded. Geometric quantum projection is supplied by
root's frozen BinaryEvents backend. Coefficients are physical dY/dtau units.
"""
import sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
G=math.sqrt(29/200)*.003
COLOUR=np.array([2/9,3/16,25/144]);SCREEN=np.array([2.,3.,5.])

def screening(q,W,f,T,m):
 q=np.asarray(q);en=np.sqrt(m*m+(T*q)**2)
 return G*G*SCREEN/(2*math.pi**2)*T*np.sum(W/(q*q)*f*(en+(T*q)**2/en))

def grid(edges,order=1,tail=True):
 edges=np.asarray(edges);z,w=np.polynomial.legendre.leggauss(order);q=[];W=[];cell=[]
 for k,(a,b) in enumerate(zip(edges[:-1],edges[1:])):
  if order==1:q.append(.75*(b**4-a**4)/(b**3-a**3));W.append((b**3-a**3)/3);cell.append(k)
  else:
   qq=(a+b)/2+(b-a)*z/2;q.extend(qq);W.extend((b-a)*w/2*qq*qq);cell.extend([k]*order)
 if tail:
  for a,b in ((edges[-1],1.5*edges[-1]),(1.5*edges[-1],2*edges[-1])):
   qq=(a+b)/2+(b-a)*z/2;q.extend(qq);W.extend((b-a)*w/2*qq*qq);cell.extend([-1]*order)
 return np.array(q),np.array(W),np.array(cell)

def event_arrays(q,W,T,m,md2,incoming_angles=4,azimuth=2,log_order=2,max_log_span=3.,diagnostic_f=None,pair_slice=None):
 q=np.asarray(q,float);W=np.asarray(W,float);n=len(q);measure=12*W/(2*math.pi**2);p=T*q;E=np.sqrt(m*m+p*p);K=p*p/(E+m);ii,jj=np.triu_indices(n)
 if pair_slice is not None:ii=ii[pair_slice[0]:pair_slice[1]];jj=jj[pair_slice[0]:pair_slice[1]]
 z,zw=np.polynomial.legendre.leggauss(incoming_angles);cp=np.cos((np.arange(azimuth)+.5)*math.pi/azimuth);i=np.repeat(ii,incoming_angles*azimuth);j=np.repeat(jj,incoming_angles*azimuth);zz=np.tile(np.repeat(z,azimuth),len(ii));cw=np.tile(np.repeat(zw/2,azimuth),len(ii))/azimuth;cosphi=np.tile(cp,len(ii)*incoming_angles);p1,p2=p[i],p[j];k1,k2=K[i],K[j];ds=2*(m*(k1+k2)+k1*k2-p1*p2*zz);s=4*m*m+ds;B=.5*np.sqrt(np.maximum(0,(p1*p1+p2*p2+2*p1*p2*zz)/s*ds));ksum=k1+k2;half=ksum/2;c0=(k1-k2)/(2*B);c0=np.clip(c0,-1,1);s0=np.sqrt(np.maximum(0,1-c0*c0));rr=np.sqrt(c0*c0+s0*s0*cosphi*cosphi);delta=np.arctan2(s0*cosphi,c0);D=float(min(md2));logD=math.log(D);end=np.log(D+ds);candidates=[]
 with np.errstate(divide='ignore',invalid='ignore'):
  target=(K[None,:]-half[:,None])/B[:,None];target=np.c_[target,-target];u=target/rr[:,None];valid=abs(u)<1;angle=np.arccos(np.clip(u,-1,1))
 for sign in (1,-1):
  th=np.mod(delta[:,None]+sign*angle,2*math.pi);validroot=valid&(th>1e-12)&(th<math.pi-1e-12);y=ds[:,None]/2*(1-np.cos(th));lg=np.log(D+y);candidates.append(np.where(validroot,lg,np.inf))
 maxint=int(math.ceil(float(max(end-logD))/max_log_span));uniform=logD+max_log_span*np.arange(1,maxint+1);unif=np.broadcast_to(uniform,(len(i),len(uniform)));unif=np.where(unif<end[:,None],unif,np.inf);cuts=np.sort(np.concatenate([np.full((len(i),1),logD),end[:,None],unif]+candidates,axis=1),axis=1);left,right=cuts[:,:-1],cuts[:,1:];rows,cols=np.where(np.isfinite(right)&(right-left>1e-12));lo,hi=left[rows,cols],right[rows,cols];zg,wg=np.polynomial.legendre.leggauss(log_order);row=np.repeat(rows,log_order);lg=((lo+hi)[:,None]/2+(hi-lo)[:,None]/2*zg).ravel();dy=((hi-lo)[:,None]/2*wg).ravel();y=D*np.expm1(lg-logD);ct=1-2*y/ds[row];st=2*np.sqrt(np.maximum(0,y/ds[row]*(1-y/ds[row])));K3=half[row]+B[row]*(c0[row]*ct+s0[row]*cosphi[row]*st);K3=np.clip(K3,0,ksum[row]);K4=ksum[row]-K3
 dsdq=G**4/(16*math.pi*s[row]*ds[row])*(2*(2*m*m+ds[row])-y)**2*np.sum(COLOUR[:,None]/(y[None,:]+np.asarray(md2)[:,None])**2,axis=0);vM=.5*np.sqrt(s[row]*ds[row])/(E[i[row]]*E[j[row]]);coef=T**3*measure[i[row]]*measure[j[row]]*np.where(i[row]==j[row],.25,.5)*cw[row]*vM*dsdq*(y+D)*dy
 diagnostics={}
 if diagnostic_f is not None:
  ff=np.asarray(diagnostic_f);ffpair=ff[i[row]]*ff[j[row]];norm=float(measure@ff);de=K3-K[i[row]];qkick=y+de*de;rad1=(E[i[row]]*de-y/2)/p[i[row]];rad2=(E[j[row]]*de+y/2)/p[j[row]];diagnostics=dict(transport_rate=float(8*np.sum(coef*ffpair*y/ds[row])/norm),dp2_rate=float(4*np.sum(coef*ffpair*qkick)/norm),radial_dp2_rate=float(2*np.sum(coef*ffpair*(rad1*rad1+rad2*rad2))/norm))
 support=(K3>=K[0])&(K3<=K[-1])&(K4>=K[0])&(K4<=K[-1]);
 if diagnostic_f is not None:diagnostics['dropped_dp2_fraction']=float(np.sum((coef*ffpair*qkick)[~support])/np.sum(coef*ffpair*qkick))
 oi=i[row[~support]];oj=j[row[~support]];oc=coef[~support];row=row[support];K3=K3[support];K4=K4[support];coef=coef[support]
 def bracket(target):
  l=np.clip(np.searchsorted(K,target)-1,0,n-2);h=l+1;u=(target-K[l])/(K[h]-K[l]);return l,h,np.clip(u,0,1)
 a,b,u=bracket(K3);c,d,v=bracket(K4);index=np.c_[i[row],j[row],a,b,c,d];weights=np.c_[np.ones(len(row)),np.ones(len(row)),1-u,u,1-v,v];sg=np.array([-1,-1,1,1,1,1]);residual=np.sum(weights*sg*K[index],axis=1)
 return dict(diagnostics=diagnostics,index=index,weights=weights,coefficient=coef,measure=measure,energy=K,eta=np.ones(n),groups=[dict(id='Sc_0',kind='S',degeneracy=12,charged=True)],kinetic_energy=K,full_energy=E,q=q,W=W,T=T,m=m,md2=np.asarray(md2),omitted_incoming_i=oi,omitted_incoming_j=oj,omitted_coefficient=oc,energy_residual=float(np.max(abs(residual),initial=0.)),incoming_angles=incoming_angles,azimuth=azimuth,log_order=log_order,max_log_span=max_log_span)

def make_events(arrays):
 sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
 from binary_events import BinaryEvents
 ev=BinaryEvents(arrays['index'],arrays['weights'],arrays['coefficient'],arrays['measure'],arrays['energy'],arrays['eta'],arrays['groups']);ev.physical_inputs=arrays;return ev


def event_arrays_chunked(q,W,T,m,md2,pair_chunk=128,**kwargs):
 count=len(q)*(len(q)+1)//2;parts=[];diagnostics=[];energy_error=0.
 for first in range(0,count,pair_chunk):
  a=event_arrays(q,W,T,m,md2,pair_slice=(first,min(count,first+pair_chunk)),**kwargs);parts.append(a);diagnostics.append(a['diagnostics']);energy_error=max(energy_error,a['energy_residual'])
 out=dict(parts[0])
 for k in ('index','weights','coefficient','omitted_incoming_i','omitted_incoming_j','omitted_coefficient'):out[k]=np.concatenate([a[k] for a in parts])
 out['energy_residual']=energy_error;out['pair_chunk']=pair_chunk
 if diagnostics and diagnostics[0]:
  out['diagnostics']={k:sum(a[k] for a in diagnostics) for k in ('transport_rate','dp2_rate','radial_dp2_rate')};out['diagnostics']['dropped_dp2_fraction']=sum(a['dp2_rate']*a['dropped_dp2_fraction'] for a in diagnostics)/sum(a['dp2_rate'] for a in diagnostics)
 return out
