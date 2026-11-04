"""Generic symmetric-coupling normalization and covariance fixture, not a model."""
import sys, os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import json, math, time, resource
from pathlib import Path
import numpy as np
from probe import vv_width

def main(out):
    start = time.monotonic()
    rng = np.random.default_rng(20261104)
    raw = rng.normal(size=(4, 5, 5))
    K = .003*(raw+raw.transpose(0,2,1))/2
    RP = np.linalg.qr(rng.normal(size=(4,4)))[0]
    RV = np.linalg.qr(rng.normal(size=(5,5)))[0]
    transformed = np.einsum('ab,aij->bij', RP, K)
    transformed = np.einsum('ik,akl,lj->aij', RV.T, transformed, RV)
    rows = []
    for mass in (.02,.2,.49):
        M = 1.
        beta = math.sqrt(1-4*mass**2)
        polar = 2+(M*M-2*mass**2)**2/(4*mass**4)
        # The full ordered real-vector sum has one global factor1/2.
        # This is independent of the unordered i<=j implementation.
        ordered = beta*polar/(32*math.pi*M)*np.einsum('aij,bij->ab',K,K)
        unordered, pairs = vv_width(K,np.full(5,mass),M)
        rotated,_ = vv_width(transformed,np.full(5,mass),M)
        rows.append(dict(m_vector=mass, unordered_pair_count=len(pairs),
            ordered_unordered_relative=float(np.linalg.norm(ordered-unordered)/np.linalg.norm(ordered)),
            nontrivial_covariance_relative=float(np.linalg.norm(rotated-RP.T@ordered@RP)/np.linalg.norm(ordered)),
            eigenvalues=np.linalg.eigvalsh(unordered).tolist()))
    checks = dict(all_fifteen_pairs=all(r['unordered_pair_count']==15 for r in rows),
        ordered_unordered_normalization=all(r['ordered_unordered_relative']<1e-12 for r in rows),
        nontrivial_vector_parent_covariance=all(r['nontrivial_covariance_relative']<1e-12 for r in rows),
        positive_gram_width=all(min(r['eigenvalues'])>0 for r in rows))
    result = dict(claim_id='CC10_GENERIC_REAL_VECTOR_NORMALIZATION',checks=checks,
        rows=rows,seed=20261104,scope='Generic symmetric K fixture only; actual model inputs are unchanged.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    assert all(checks.values()),checks

if __name__=='__main__': main(sys.argv[1])
