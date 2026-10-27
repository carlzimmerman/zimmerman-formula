"""Fixed-gate unit checks with an explicit single-thread native reference."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse,json,platform,time,unittest
import numpy as np
import scipy
import fast_gravity
import test_tile3_gravity as tests
from tile2_gravity import gravity as old
from tile3_gravity import gravity as candidate,backend_metadata


def main(output):
    tests.reference=lambda x,m,eps:fast_gravity.gravity(x,m,eps,threads=1)
    start=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    x=np.array([[80001.234,-30000.456,2000.567],[79996.876,-30002.345,2004.321]])
    m=np.array([1880.1269762105387,280.4067078613779]);pairs={}
    for name,operator in (('tile2',old),('tile3',candidate)):
        a,U,phi=operator(x,m,10.);f=m[:,None]*a
        pairs[name]=dict(normalized_P=float(np.linalg.norm(f.sum(0))/np.linalg.norm(f,axis=1).sum()),
            pairpotential_reciprocity_defect=float(abs(m[0]*phi[0]-m[1]*phi[1])/abs(m[0]*phi[0])))
    report=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),seconds=time.monotonic()-start,
        backend=backend_metadata(),unequal_mass_pair=pairs,CPU_reference_threads=1,
        software=dict(Python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    Path=None
    with open(output,'w') as target:json.dump(report,target,indent=2);target.write('\n')
    if not result.wasSuccessful():raise AssertionError('tile3 fixed-gate tests failed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
