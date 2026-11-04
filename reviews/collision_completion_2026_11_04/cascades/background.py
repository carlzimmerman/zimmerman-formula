"""Dense actual-vertex data and positive threshold-preserving interpolation."""
import sys,json,time,resource,math,copy
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from network import ROOT,table
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/photino'))
from source import atx

def make(out):
 start=time.monotonic();rows=[]
 for x in np.linspace(.1,4.1,81):
  d=table(float(x));r=atx(float(x));d['current_source']={key:r[key] for key in ('gauginos_over_mu','widths_over_mu','reverse_lightest_scalar_widths_over_mu')};d.pop('singlet_channel_Gamma');d.pop('singlet_indices')
  for name,gid in (('U1','F1_1'),('SU2','F3_0'),('SU3','F8_0')):
   next(g for g in d['groups'] if g['id']==gid)['mass']=r['gauginos_over_mu'][name]
  rows.append(d)
  if len(rows)%10==0:print(len(rows),x,flush=True)
 result=dict(claim_id='CC10_EARLY_CASCADE_BACKGROUND',cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,checks=dict(all_group_ids_equal=all([g['id'] for g in r['groups']]==[g['id'] for g in rows[0]['groups']] for r in rows),all_upstream_controls=all(r['checks']['charged_real_scalars'] and r['checks']['charged_Weyls'] and r['checks']['excluded_Goldstones'] for r in rows)))
 Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(result['checks'].values())

class Background:
 def __init__(self,path,stride=1):
  self.rows=json.loads(Path(path).read_text())['cases'][::stride];self.xs=np.array([r['x'] for r in self.rows]);self.groups=self.rows[0]['groups'];self.by={g['id']:i for i,g in enumerate(self.groups)};self.mass2=CubicSpline(self.xs,[[g['mass']**2 for g in r['groups']] for r in self.rows],axis=0)
  keys=sorted({(c['parent'],*c['daughters'],c['kind']) for r in self.rows for c in r['channels']});self.keys=keys;self.coeff=np.zeros((len(self.rows),len(keys)));ki={k:i for i,k in enumerate(keys)}
  for i,r in enumerate(self.rows):
   by={g['id']:g for g in r['groups']}
   for c in r['channels']:
    p,j,k=c['parent'],*c['daughters'];M,m1,m2=[by[t]['mass'] for t in (p,j,k)];phase=math.sqrt(max(0,(1-(m1+m2)**2/M**2)*(1-(m1-m2)**2/M**2))) if M>m1+m2 else 0
    if phase>1e-15:self.coeff[i,ki[(p,j,k,c['kind'])]]=c['width']/phase*(M if c['kind']=='SS' else 1.)
 def at(self,x):
  if not self.xs[0]<=x<=self.xs[-1]:raise RuntimeError('x outside pinned cascade background: '+str(x))
  ii=min(max(0,int(np.searchsorted(self.xs,x)-1)),len(self.xs)-2);a=(x-self.xs[ii])/(self.xs[ii+1]-self.xs[ii]);m2=self.mass2(x);slope=self.mass2(x,1);groups=[dict(g,mass=math.sqrt(max(0,m2[i])),dm2_dx=float(slope[i])) for i,g in enumerate(self.groups)]
  coeff=(1-a)*self.coeff[ii]+a*self.coeff[ii+1];channels=[]
  for key,v in zip(self.keys,coeff):
   p,j,k,kind=key;M,m1,m2=[groups[self.by[t]]['mass'] for t in (p,j,k)]
   if M<=m1+m2 or v<=0:continue
   phase=math.sqrt(max(0,(1-(m1+m2)**2/M**2)*(1-(m1-m2)**2/M**2)));width=v*phase/(M if kind=='SS' else 1)
   channels.append(dict(parent=p,daughters=[j,k],width=float(width),kind=kind))
  source={key:{g:(1-a)*self.rows[ii]['current_source'][key][g]+a*self.rows[ii+1]['current_source'][key][g] for g in self.rows[ii]['current_source'][key]} for key in self.rows[ii]['current_source']}
  return dict(x=float(x),groups=groups,channels=channels,current_source=source)

if __name__=='__main__':make(sys.argv[1])
