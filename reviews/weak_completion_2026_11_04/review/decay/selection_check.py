"""Correct-coordinate C selection and active threshold audit, separate run."""
import sys,os,json,math,time,resource
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/decay'))
import matching as a

def min_den(t,s,xi,mv2):
    mt=xi*mv2 if t.get('goldt') else t['mt'];mb=xi*mv2 if t.get('goldb') else t['mb'];mr=xi*mv2 if t.get('goldr') else t['mr']
    # Hessian of -sxy has eigenvalues +/-s; no interior minimum for s>0.
    # The other two simplex edges are affine. Minimize the remaining edge.
    x=max(0.,min(1.,(s+mb-mt)/(2*s)))
    edge=mb+(mt-mb-s)*x+s*x*x
    return min(mt,mb,mr,edge),math.sqrt(mt)+math.sqrt(mb)-math.sqrt(s)

def main(out):
    start=time.monotonic();data=a.model();d=data['d'];T=a.T
    eta=np.array([1. if np.max(abs(t.T-t))<1e-14 else -1. for t in T])
    cc=np.r_[1.,eta,eta];cf=np.r_[cc,-eta];cs=np.r_[cc,cc]
    G=np.r_[d['F'].conj(),np.zeros(24)];G/=np.linalg.norm(G)
    sym=dict(Y=float(np.max(abs(d['Y']*(cc[:,None,None]*cc[None,:,None]*cc[None,None,:]-1)))),
        MF=float(np.max(abs(cf[:,None]*d['MF']*cf[None,:]-d['MF']))),
        H=float(np.max(abs(cs[:,None]*d['H']*cs[None,:]-d['H']))),
        background=float(np.max(abs(cc*d['z']-d['z']))),Goldstino=float(np.max(abs(cf*G-G))))
    rows=[]
    for name in ('S8_0','S3_0'):
        p=a.parent(data,name);old=data['O']@p['weights'];lam=data['ext'][:,p['b']]
        yp=np.einsum('IJs,s->IJ',data['dy'],p['weights'])
        # All these are in old-field coordinates. The previous run's
        # parent_C_parity diagnostic wrongly combined mass and old coordinates;
        # its two parent_C_parity numbers are invalid and superseded here.
        parent_C_error=float(np.max(abs(cs*old-old)))
        lambda_C_error=float(np.max(abs(cf*lam+lam)))
        target_C_error=float(np.max(abs(cf*data['ext'][:,11]+data['ext'][:,11])))
        threshold=[]
        for channel,aa,bb,charged in (('mixed',None,11,True),('pair',0,0,False)):
            if channel=='pair' and name!='S8_0':continue
            terms=a.coefficients(data,p,a=aa,b=bb,charged_only=charged)
            for xi in (.5,1.,2.):
                minima=[min_den(t,p['mass']**2,xi,max(d['mV2'])) for t in terms]
                threshold.append(dict(channel=channel,xi=xi,term_count=len(terms),
                  minimum_parameter_denominator=min(v[0] for v in minima),
                  minimum_parent_threshold_gap=min(v[1] for v in minima)))
        # Parent tree matrix with a fixed unbroken U1 endpoint is zero for
        # every possible other fermion, not merely after a Goldstino trace.
        rows.append(dict(id=name,parent_C_even_error=parent_C_error,lambda_C_odd_error=lambda_C_error,
          chi_C_odd_error=target_C_error,tree_chi_all_fermion_norm=float(np.linalg.norm(yp@data['ext'][:,11])),
          tree_Goldstino_vertex=float(abs(lam.T@yp@G)),thresholds=threshold))
    checks=dict(C_symmetry=max(sym.values())<1e-12,parent_parities=max(r['parent_C_even_error'] for r in rows)<1e-10,
      gaugino_parities=max(max(r['lambda_C_odd_error'],r['chi_C_odd_error']) for r in rows)<1e-12,
      no_active_internal_cut=min(t['minimum_parameter_denominator'] for r in rows for t in r['thresholds'])>=-1e-15)
    result=dict(symmetry=sym,states=rows,checks={k:bool(v) for k,v in checks.items()},
      superseded_diagnostics='run001/result.json actual.states[*].parent_C_parity used mass-basis coefficients with an old-field C diagonal; invalid diagnostic only, never an asserted check. This run explicitly transforms with O first.',
      scope='Fixed vacuum, tree action C invariance and analytic minimization of every retained triangle parameter denominator, xi=.5/1/2; not a gravity-sector symmetry audit.',
      runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
