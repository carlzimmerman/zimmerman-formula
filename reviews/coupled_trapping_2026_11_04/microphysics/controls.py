"""Independent algebraic controls: group coefficient, pole covariance and e scaling."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import json,math,time,resource
import numpy as np
from pole_network import one
BASE=Path(__file__).resolve().parent
def main(out):
 start=time.monotonic();q=json.loads((BASE/'run_pole002/result.json').read_text());W=np.array(q['Gamma_other_matrix_mu']);G=np.array(q['production_Gram_mu2']);m=q['mC'];M=q['Mpole']
 R=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
 ref=q['sigma_pair_v_at_rest_mu_minus2'];rot=2/(m*M*M)*np.trace((R.T@G@R)@np.linalg.inv(R.T@W@R))
 terms=dict(SU3=F(7,54),SU2=F(1,32),U1=F(25,864),SU3_SU2=F(1,3),SU3_U1=F(5,27),SU2_U1=F(5,48))
 rows=[]
 for e in (.001,.003,.01):
  xp=math.sqrt(60/(31*e));r=one(xp,e);pp=[p for p in r['neutral_parents'] if abs(p['mass']-math.sqrt(2*e))<1e-8];width=sum(p['width'] for p in pp)
  rows.append(dict(e=e,xpole=xp,m_light_S=r['m_light_S'],width_trace=width,scaled_mass=r['m_light_S']/math.sqrt(e),scaled_width=width/e**2.5))
 checks=dict(exact_gauge_coefficient=sum(terms.values())==F(13,16),pole_basis_covariance=bool(abs(rot/ref-1)<1e-12),tree_mass_scaling=max(r['scaled_mass'] for r in rows)-min(r['scaled_mass'] for r in rows)<1e-9,tree_width_scaling=max(r['scaled_width'] for r in rows)/min(r['scaled_width'] for r in rows)-1<1e-8)
 result=dict(claim_id='CT09_MICROPHYSICS_CONTROLS',checks={k:bool(v) for k,v in checks.items()},group_trace_terms={k:str(v) for k,v in terms.items()},sum_trace=str(sum(terms.values())),pole_cross_section_reference=ref,pole_cross_section_rotated=float(rot),coupling_cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite independent representation normalization, fixed orthogonal basis covariance, and three e scaling controls. Not an allchannel cosmological bound.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
