"""Full grouped invariant FFS/SSS vertices, including kinematically closed edges.

Interpolation acts on |y|², Re y² and cubic², then reconstructs phase space
at the current mass. A channel crossing a threshold is never interpolated as
a zero-width/positive-width mixture.
"""
import sys,json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from network import ROOT,state,E
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/photino'))
from source import atx

def vertex_table(x):
 d=state(x);groups=d['groups'];ss=[g for g in groups if g['kind']=='S'];ff=[g for g in groups if g['kind']=='F'];c3=d['c3'];y=d['yy'];vertices=[]
 for p in ss:
  aa=p['indices'];count=len(aa)
  for ii,j in enumerate(ss):
   for k in ss[ii:]:
    v=c3[np.ix_(aa,j['indices'],k['indices'])];C=float(np.sum(v*v))*(1 if j['id']==k['id'] else 2)/count
    if C>1e-30:vertices.append(dict(parent=p['id'],daughters=[j['id'],k['id']],kind='SS',C=C))
  for ii,j in enumerate(ff):
   for k in ff[ii:]:
    v=y[np.ix_(np.array(j['indices'])-98,np.array(k['indices'])-98,aa)];fac=(1 if j['id']==k['id'] else 2)/count;A=float(np.sum(abs(v)**2))*fac;B=float(np.sum((v*v).real))*fac
    if A>1e-25:vertices.append(dict(parent=p['id'],daughters=[j['id'],k['id']],kind='FF',A=A,B=B))
 for p in ff:
  aa=np.array(p['indices'])-98;count=len(aa)
  for j in ff:
   for k in ss:
    v=y[np.ix_(aa,np.array(j['indices'])-98,k['indices'])];A=float(np.sum(abs(v)**2))/count;B=float(np.sum((v*v).real))/count
    if A>1e-25:vertices.append(dict(parent=p['id'],daughters=[j['id'],k['id']],kind='FS',A=A,B=B))
 source=atx(float(x));src={key:source[key] for key in ('gauginos_over_mu','widths_over_mu','reverse_lightest_scalar_widths_over_mu')}
 for name,gid in (('U1','F1_1'),('SU2','F3_0'),('SU3','F8_0')):next(g for g in groups if g['id']==gid)['mass']=source['gauginos_over_mu'][name]
 return dict(x=float(x),e=E,groups=groups,vertices=vertices,current_source=src,m_vector=d['mV'],checks=d['checks'])

def channels(groups,vertices):
 by={g['id']:g for g in groups};result=[]
 for c in vertices:
  M,m1,m2=[by[n]['mass'] for n in [c['parent']]+c['daughters']]
  if M<=m1+m2+1e-14:continue
  z1,z2=m1/M,m2/M;phase=math.sqrt(max(0,(1-(z1+z2)**2)*(1-(z1-z2)**2)))
  if c['kind']=='SS':w=c['C']*phase/(32*math.pi*M)
  elif c['kind']=='FF':w=M/(16*math.pi)*phase*(c['A']*(1-z1*z1-z2*z2)-2*c['B']*z1*z2)
  else:w=M/(16*math.pi)*phase*(c['A']*(1+z1*z1-z2*z2)+2*c['B']*z1)
  if w>1e-25:result.append(dict(parent=c['parent'],daughters=c['daughters'],kind=c['kind'],width=float(w)))
 return result

def make(out):
 start=time.monotonic();xs=np.unique(np.r_[np.linspace(.1,4.1,81),np.arange(4.3,10,.2),np.arange(10.,30.1,.5),np.arange(31.,61.),np.arange(65.,201.,5.)]);rows=[]
 for x in xs:
  d=vertex_table(float(x));rows.append(d)
  if len(rows)%20==0:print(len(rows),x,len(d['vertices']),flush=True)
 result=dict(claim_id='CC10_FULL_CLOSED_OPEN_VERTEX_BACKGROUND',cases=rows,checks=dict(all_group_ids_equal=all([g['id'] for g in r['groups']]==[g['id'] for g in rows[0]['groups']] for r in rows),nonnegative_norms=all(v.get('C',v.get('A',0))>=0 and abs(v.get('B',0))<=v.get('A',0)+1e-20 for r in rows for v in r['vertices']),charge_counts=all(r['checks']['charged_real_scalars'] and r['checks']['charged_Weyls'] and r['checks']['excluded_Goldstones'] for r in rows)),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(result['checks'].values())

class VertexBackground:
 def __init__(self,path,stride=1):
  self.rows=json.loads(Path(path).read_text())['cases'][::stride];self.xs=np.array([r['x'] for r in self.rows]);self.groups=self.rows[0]['groups'];self.by={g['id']:i for i,g in enumerate(self.groups)};self.mass2=CubicSpline(self.xs,[[g['mass']**2 for g in r['groups']] for r in self.rows],axis=0)
  self.keys=sorted({(v['parent'],*v['daughters'],v['kind']) for r in self.rows for v in r['vertices']});ki={k:i for i,k in enumerate(self.keys)};self.coefficients=np.zeros((len(self.rows),len(self.keys),3))
  for i,r in enumerate(self.rows):
   for v in r['vertices']:self.coefficients[i,ki[(v['parent'],*v['daughters'],v['kind'])]]=[v.get('A',0.),v.get('B',0.),v.get('C',0.)]
 def at(self,x):
  if not self.xs[0]<=x<=self.xs[-1]:raise RuntimeError('x outside pinned vertex background: '+str(x))
  i=min(max(0,int(np.searchsorted(self.xs,x)-1)),len(self.xs)-2);a=(x-self.xs[i])/(self.xs[i+1]-self.xs[i]);m2=self.mass2(x);dm2=self.mass2(x,1);groups=[dict(g,mass=math.sqrt(max(0,m2[j])),dm2_dx=float(dm2[j]),dm_dx=float(dm2[j]/(2*math.sqrt(m2[j]))) if m2[j]>1e-24 else 0.) for j,g in enumerate(self.groups)];co=(1-a)*self.coefficients[i]+a*self.coefficients[i+1];vv=[dict(parent=p,daughters=[j,k],kind=kind,A=float(v[0]),B=float(v[1]),C=float(v[2])) for (p,j,k,kind),v in zip(self.keys,co)]
  src={key:{g:(1-a)*self.rows[i]['current_source'][key][g]+a*self.rows[i+1]['current_source'][key][g] for g in self.rows[i]['current_source'][key]} for key in self.rows[i]['current_source']};mv=(1-a)*self.rows[i]['m_vector']+a*self.rows[i+1]['m_vector']
  return dict(x=float(x),e=E,groups=groups,vertices=vv,channels=channels(groups,vv),current_source=src,m_vector=float(mv))

if __name__=='__main__':make(sys.argv[1])
