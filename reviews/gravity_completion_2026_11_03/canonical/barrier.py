import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,time,resource
from pathlib import Path
import mpmath as mp
import nearfold as nf
m=nf.m;HERE=Path(__file__).resolve().parent

def main(path):
 start=time.monotonic();data=json.load(open(HERE/'run_nearfold/result.json'));tf=mp.mpf(str(data['folds'][-1]['t']));rows=[]
 for point in data['threshold_points'][5:]:
  t=mp.mpf(str(point['t']));r=nf.core(t,29);p=r['p'];y=r['y'];mu=r['mu'];u0=r['u'];v0=r['v'];s0=r['s'];delta=tf-t
  cache={}
  def normals(s):
   key=mp.nstr(s,110)
   if key not in cache:cache[key]=m.normals(s,p,y,29,(u0,v0))
   return cache[key]
  def red(s):u,v=normals(s);return m.potential(s,u,v,p,y,29)
  def slope(s):u,v=normals(s);return mp.diff(lambda ss:m.potential(ss,u,v,p,y,29),s)
  sb=mp.findroot(slope,(mp.log(tf+delta/2),mp.log(tf+2*delta)),tol=mp.mpf('1e-80'),maxsteps=30);tb=mp.exp(sb);assert m.DOMAIN[0]<sb<m.DOMAIN[1]
  barrier=(red(sb)-red(s0))*mu**4;equiv=mp.sqrt(2*barrier/r['m2']);R=mu*mp.sqrt(31)*r['x'];eps=mp.mpf('1e-5');curv=(slope(sb+eps)-slope(sb-eps))/(2*eps)
  rows.append(dict(m_sigma_over_photino=point['target_ratio'],t_min=float(t),t_barrier=float(tb),distance_barrier_over_radius=float(tb/t-1),barrier_GeV4=float(barrier),barrier_over_m2_R2=float(barrier/(r['m2']*R*R)),harmonic_energy_equivalent_amplitude_GeV=float(equiv),harmonic_energy_equivalent_amplitude_over_R=float(equiv/R),outer_log_curvature=float(curv),fitdomain_s=list(map(float,m.DOMAIN))))
 checks=dict(five_fixed_vacua=len(rows)==5,positive_barriers=all(r['barrier_GeV4']>0 for r in rows),outer_unstable=all(r['outer_log_curvature']<0 for r in rows),subpercent_harmonic_energy_equivalent=all(r['harmonic_energy_equivalent_amplitude_over_R']<.01 for r in rows))
 out=dict(claim_id='CANONICAL_FIXED_VACUUM_OUTER_BARRIER',checks=checks,points=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite local action barrier at fixedmu,W0 for each nearfoldvacuum. Harmonic-equivalent amplitude is an energy diagnostic, not a solution of largeamplitude dissipative cosmology.')
 Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
