"""IC46 conditioning experiment; unchanged action, boundaries and tolerances.

Run: python3 ic47_jacobian_evolution.py
Exit 0 means the bounded numerical runs completed, never theory closure.
The existing centered-evolution regression remains an independent requirement.
"""
import contextlib
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.optimize import root
import ic46_centered_evolution as centered


@contextlib.contextmanager
def fixed_jacobian(step):
    previous = centered.root
    def solve(fun, x, **kwargs):
        directions = np.eye(len(x)) * step
        def jacobian(at):
            return np.column_stack([(fun(at+d)-fun(at-d))/(2*step)
                                    for d in directions])
        return root(fun, x, jac=jacobian, method='hybr',
                    options={'xtol': 1e-10, 'maxfev': 300})
    centered.root = solve
    try:
        yield
    finally:
        centered.root = previous


def main():
    runs=[]
    for nodes, dt, steps, difference in [(7,1e-8,20,1e-8),
                                       (7,5e-9,40,1e-8),
                                       (9,5e-9,40,1e-8),
                                       (7,1e-8,20,5e-9)]:
        with fixed_jacobian(difference):
            result=centered.experiment(nodes=nodes,dt=dt,steps=steps)
        result.pop('final_state',None)
        result['jacobian_step']=difference
        runs.append(result)
    paths=[Path(__file__),Path(centered.__file__),Path(centered.original.__file__)]
    report=dict(full_theory='OPEN',python=platform.python_version(),
                numpy=np.__version__,scipy=scipy.__version__,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                runs=runs,
                limitation='Hashes cover the numerical wrappers only; inherited IC46 symbolic and initial-data dependencies remain required.')
    print(json.dumps(report,indent=2))
    return 0 if all(r['completed'] for r in runs) else 1


if __name__=='__main__':
    raise SystemExit(main())
