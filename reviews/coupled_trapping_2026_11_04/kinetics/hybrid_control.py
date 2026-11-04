"""Endpointphase/angularrefinement of the completedlateBWcontinuation."""
import sys
sys.dont_write_bytecode=True
import json,time,resource
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from finite_bw import Finite
from accurate import LocalPotential
from two_species import ROOT,HERE

def main(out):
 start=time.monotonic();source=json.loads((HERE/'run_hybrid_bw_001/result.json').read_text());assert not source['partial'];old=source['case'];p=dict(json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1]);s=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0];packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];r=packet['global_profile'];p.update(grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'],mu_GeV=packet['mu_GeV']);m=Finite(p,s,bins=24,orbitn=16,absorbing=True,angular=12);m.v=LocalPotential(m.v,packet['local_profile']);m.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,180)]);m.setup();y=np.array(old['state']);N=old['final_N'];rows=[]
 for angular,phase in ((12,4),(24,4),(24,8)):
  m.angular=angular;m.rz,m.rw=leggauss(phase);B,d=m.rate(N,y);loss=-float(sum(B@y[:2*m.n]))/float(sum(y[:2*m.n]));rows.append(dict(angular_nodes=angular,phase_nodes_per_split=phase,numberloss_over_H=loss,dlogJ_dN=float(d[0]),radiation_comoving_derivative=float(d[1]),max_phase_nodes=m.max_phase_nodes))
 checks={'angular_endpoint_rate':abs(rows[0]['numberloss_over_H']/rows[1]['numberloss_over_H']-1)<.005,'phase_endpoint_rate':abs(rows[1]['numberloss_over_H']/rows[2]['numberloss_over_H']-1)<.01,'action_endpoint_derivative':abs(rows[1]['dlogJ_dN']-rows[2]['dlogJ_dN'])<.001};result=dict(claim_id='CT09_HYBRID_ENDPOINT_CONTROL',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Fixedcompletedhybridendpointstate; onlyangular/phaseconvergence ofinstantaneousstaticMarkovkernel. Notfullabundanceconvergence orphysicalmedium/memoryproof.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
