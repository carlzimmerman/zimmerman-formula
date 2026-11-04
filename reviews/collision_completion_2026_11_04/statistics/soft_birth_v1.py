"""FD-weighted exact two-body birth measures, including threshold soft tail."""
import sys,json,time,resource,math
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from quantum import background,ROOT,NAMES,DEGENERACIES

def run(out):
 start=time.monotonic();old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/photino/run_source004/result.json').read_text());cross=old['threshold_x'];hist=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_leading_fine_001/result.json').read_text())['case']['history'];first=next(h for h in hist if h['x_outer']>cross)
 t=first['Tc_over_mu'];H=math.sqrt(math.pi**2*106.75/90)*2e6*t*t/(2.435e18*.02**2);omega=H/first['H_over_oscillation'];gx,gw=leggauss(160);q=(gx+1)*30;W=gw*30*q*q/(np.exp(q)+1);norm=float(sum(W));az,aw=leggauss(96);bins=np.geomspace(1e-12,100.,200);rows=[]
 xs=sorted(set([cross+dx for dx in [0.,1e-10,1e-8,1e-6,1e-4,.001,.01,.1]]+[5.,25.4000254000381]))
 for x in xs:
  row=background(x);ma=row['light_fermion_over_mu'];mb=row['lightest_scalar_over_mu'];EA=np.sqrt(ma*ma+(t*q)**2);dil=ma/EA;groups=[]
  for k,name in enumerate(NAMES[2:],2):
   mc=row['gauginos_over_mu'][name];width=row['widths_over_mu'][name]
   if width<=0 or ma<=mb+mc:continue
   pstar=math.sqrt(max(0,(ma-mb-mc)*(ma+mb+mc)*(ma-mb+mc)*(ma+mb-mc)))/(2*ma);elstar=(ma*ma+mc*mc-mb*mb)/(2*ma)
   EL=(EA[:,None]*elstar-(t*q[:,None])*pstar*az[None,:])/ma
   ql=np.sqrt(np.maximum(0,(EL-mc)*(EL+mc)))/t
   prob=(W*dil)[:,None]*aw[None,:]/2;weight=prob*width/norm
   rate=float(sum(weight.ravel()));soft={str(cut):float(sum(weight[ql<cut])) for cut in [1e-4,1e-6,1e-8]}
   histogram,_=np.histogram(ql,bins,weights=(24/(2*math.pi**2)*norm*weight));volume=DEGENERACIES[k]*(bins[1:]**3-bins[:-1]**3)/(6*math.pi**2);df=histogram/volume
   groups.append(dict(group=name,width_over_mu=width,pstar_over_mu=pstar,FD_mean_rate_per_carrier=rate,FD_mean_rate_over_H=rate/H,FD_mean_events_per_orbit=2*math.pi*rate/omega,soft_birth_rate_per_carrier=soft,soft_birth_rate_over_H={a:b/H for a,b in soft.items()},birth_mean_q=float(np.sum(weight*ql)/max(rate,1e-300)),histogram_peak_df_dtau=float(max(df)),histogram_peak_df_over_omega=float(max(df)/omega),histogram_fraction_covered=float(sum(histogram)/(24/(2*math.pi**2)*norm*rate))))
  rows.append(dict(x=x,mass_gap=ma-mb,groups=groups));print(x,[(r['group'],r['FD_mean_rate_over_H'],r['soft_birth_rate_over_H']['0.0001'],r['histogram_peak_df_over_omega']) for r in groups],flush=True)
 result=dict(claim_id='CC10_SOFT_BIRTH_RATE_V1',checks=dict(nonnegative=all(g['FD_mean_rate_per_carrier']>=0 for r in rows for g in r['groups']),histogram_coverage=all(g['histogram_fraction_covered']>.999999 for r in rows for g in r['groups'])),Tc=t,H_over_mu=H,omega_over_mu=omega,reference_first_crossing_history=first,threshold_x=cross,rows=rows,initial_scope='Frozen original FD F occupation, empty C and gauginos, at recorded first-crossing Tc and omega. Does not reconstruct the earlier absorbing-run deformed F distribution. Histogram maxima are resolution-dependent rate diagnostics; FD weighted integrated birth measures are the load-bearing estimates.',parent_radial_nodes=160,parent_qmax=60,angular_nodes=96,lambda_q_histogram_edges=bins.tolist(),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result['checks']),flush=True);assert all(result['checks'].values())
if __name__=='__main__':run(sys.argv[1])
