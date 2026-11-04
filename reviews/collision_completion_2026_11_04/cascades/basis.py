"""Map CC10 per-daughter singlet widths back to CT09 pole basis."""
import sys,json,math,time,resource
from pathlib import Path
import numpy as np
from network import ROOT,E,build_model,DCOEF,T,adapt

def main(out):
 start=time.monotonic();source=ROOT/'reviews/collision_completion_2026_11_04/cascades/run_network001/result.json'
 data=json.loads(source.read_text())['cases'][-2];x=data['x'];d=build_model(x,E,E,math.sqrt(29/200)*E,vertices=False);R=d['R']
 ry=np.einsum('a,aij->ij',DCOEF/math.sqrt(30),R);q=ry@ry;qs=np.block([[q.real,-q.imag],[q.imag,q.real]])
 un=[a for a,t in enumerate(T) if np.max(abs(t@np.diag([2,2,2,-3,-3])-np.diag([2,2,2,-3,-3])@t))<1e-12]
 c=np.einsum('aij,ajk->ik',R[un],R[un]);cs=np.block([[c.real,-c.imag],[c.imag,c.real]])
 old=adapt(d['O'],d['mS2'],qs);new=adapt(old,d['mS2']+np.einsum('ia,ia->a',old,qs@old).real,cs);P=data['singlet_indices'];U=old[:,P].T@new[:,P]
 matrices={k:(U@np.array(v)@U.T).tolist() for k,v in data['singlet_channel_Gamma'].items()};total=sum(np.array(v) for v in matrices.values());ref=np.array(json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text())['Gamma_other_matrix_mu'])
 checks=dict(orthogonality=float(np.max(abs(U.T@U-np.eye(4))))<1e-12,reference_matrix=float(np.max(abs(total-ref)))<1e-19,all_channel_PSD=min(np.linalg.eigvalsh(np.array(v)).min() for v in matrices.values())>-1e-20)
 result=dict(claim_id='CC10_SINGLET_CHANNEL_BASIS',x=x,CT09_parent_indices=P,CC10_to_CT09_parent_coordinates=U.tolist(),Gamma_by_daughter_pair_CT09_mu=matrices,Gamma_total_CT09_mu=total.tolist(),reference_max_error=float(np.max(abs(total-ref))),checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,result['reference_max_error']);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
