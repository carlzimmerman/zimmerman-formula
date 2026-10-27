"""Independent radial retarded-source prediction of the unseeded pulse."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from dynamics import model,load
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();root=Path('infall_pump_2026_10_25/run_smooth_infall');z=load(root/'state.npz');hist=np.load(root/'history.npz');hh=hist['history'];rr=hist['r_kpc']/m.rm;n=len(rr);tt=hh[:,0];S=hh[:,1+2*n:1+3*n];spline=CubicSpline(tt,S,axis=0);I=np.sum(S,axis=1);Is=CubicSpline(tt,I);t=5.7
mask=(m.wr>=500/m.rm)&(m.wr<=(m.c/m.tdyn*t+500/m.rm));r=m.wr[mask];c=z[3][mask];v=z[4][mask];h=float(np.mean(np.diff(r)));re=(r[1:]+r[:-1])/2;ret=t-re/m.c*m.tdyn;actual=((r*v)[1:]+(r*v)[:-1])/4-m.c*np.diff(r*c)/(2*h)
# Time interpolation per material source cell; no fitted normalization.
pred=np.zeros_like(ret)
for i,ri in enumerate(rr):
 lag=ri/m.c*m.tdyn;plus=ret+lag;minus=ret-lag
 def ev(tq):
  val=spline(tq)[:,i];return np.where((tq>=tt[0])&(tq<=tt[-1]),val,0.)
 pred-=(ev(plus)-ev(minus))/(2*m.c*ri)
mono=-m.tdyn*np.where((ret>=tt[0])&(ret<=tt[-1]),Is(ret,1),0.)/m.c**2
# Source radius omitted beyond80 kpc has negligible T in this benchmark.
Q=[];mt=hh[:,1:1+n]*m.vol[:n][None,:]
for row in mt:Q.append(float(m.g*np.sum(row)+m.g2*np.sum(row*row/m.vol[:n])))
Q=np.array(Q);dq=CubicSpline(tt,Q)(tt,1)*m.tdyn;inorm=float(np.linalg.norm(dq[2:-2]-I[2:-2])/max(np.linalg.norm(I[2:-2]),1e-100))
valid=(ret>=.1)&(ret<=4.);norm=np.linalg.norm(actual[valid]);res={'physical_time_Myr':t,'history_step_Myr_max':float(np.max(np.diff(tt))),'source_cells_inside_kpc':80,'source_charge_identity_relative_L2':inorm,'retarded_source_prediction_relative_L2':float(np.linalg.norm(pred[valid]-actual[valid])/norm),'compact_monopole_prediction_relative_L2':float(np.linalg.norm(mono[valid]-actual[valid])/norm),'actual_outgoing_energy_annulus':float(h*np.sum(actual**2)),'retarded_prediction_energy_annulus':float(h*np.sum(pred**2)),'compact_prediction_energy_annulus':float(h*np.sum(mono**2)),'comparison_retarded_interval_Myr':[.1,4.],'non_claim':'Finite radial source-history retrodiction, not a universal radiation efficiency or proof of sustained emission.'}
np.savez_compressed(Path(args.output).with_name('waveform.npz'),retarded_time_Myr=ret,actual=actual,retarded_prediction=pred,compact_prediction=mono,source_time_Myr=tt,source_monopole=I,material_charge_inner80=Q)
Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(res)

assert inorm<.01
assert res["retarded_source_prediction_relative_L2"]<.01
