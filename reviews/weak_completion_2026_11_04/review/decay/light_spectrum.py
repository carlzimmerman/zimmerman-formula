"""Residual-representation check for all sub-parent-mass physical modes."""
import sys,os,json,math,time,resource
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/decay'))
import matching as a

def main(out):
    start=time.monotonic();data=a.model();d=data['d']
    Q=np.einsum('br,rIJ->bIJ',data['coeff'],data['RF'])
    C2=np.einsum('aij,ajk->ik',Q[8:11],Q[8:11]);C3=np.einsum('aij,ajk->ik',Q[:8],Q[:8])
    def scalar(C):
        C=C[:49,:49]
        return np.block([[C.real,-C.imag],[C.imag,C.real]])
    F2=np.einsum('ia,ij,ja->a',data['U'].conj(),C2,data['U']).real
    F3=np.einsum('ia,ij,ja->a',data['U'].conj(),C3,data['U']).real
    S2=np.einsum('ia,ij,ja->a',data['O'],scalar(C2),data['O']).real
    S3=np.einsum('ia,ij,ja->a',data['O'],scalar(C3),data['O']).real
    rows=[]
    for name in ('S8_0','S3_0'):
        p=a.parent(data,name);sectors=[]
        for tag,masses,cas2,cas3,physical in (('scalar',np.sqrt(np.maximum(d['mS2'],0)),S2,S3,~data['gold']),('Weyl',d['mF'],F2,F3,np.ones(73,bool))):
            ids=np.where(physical&(masses<p['mass']*(1-1e-9)))[0]
            for mass,I in a.grouped(ids,masses):
                sectors.append(dict(spin=tag,mass=mass,multiplicity=len(I),SU2_Casimir_mean=float(np.mean(cas2[I])),
                  SU2_Casimir_max=float(np.max(abs(cas2[I]))),SU3_Casimir_mean=float(np.mean(cas3[I]))))
        rows.append(dict(id=name,parent_mass=p['mass'],sub_parent_physical_modes=sectors))
    checks=dict(S8_only_massless_below_parent=all(s['mass']<1e-10 for s in rows[0]['sub_parent_physical_modes']),
      S3_all_massive_below_parent_SU2_singlets=all(s['SU2_Casimir_max']<1e-10 for s in rows[1]['sub_parent_physical_modes'] if s['mass']>1e-10))
    result=dict(states=rows,checks={k:bool(v) for k,v in checks.items()},
      interpretation='Other allowed massive channels are closed, but not every raw threshold is closed: octet modes below S3 are SU2 singlets and cannot form an initial triplet without additional final particles.',
      runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
