import ctypes,json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent
lib=ctypes.CDLL(str((p/'collapse_force.dylib').resolve()))
lib.collapse_rhs.argtypes=[ctypes.c_int,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
lib.collapse_rhs.restype=None
source=(p/'reciprocal_collapse_v2.py').read_text()
body=source.split(' E0=')[0].split('for N,h in [(32,.000125),(64,.0000625)]:')[1]
records=[]
for row in json.loads((p/'collapse_core_run/results.json').read_text())['rows']:
    N=row['N'];ns={'N':N,'np':np}
    exec('\n'.join(line[1:] if line.startswith(' ') else line for line in body.splitlines()),ns)
    for epoch in [0,10,15,20,30]:
        s=min(row['samples'],key=lambda s:abs(s['t']-epoch))
        y=np.r_[s['radii'],s['B'],s['velocities'],0.]
        out=np.empty_like(y)
        lib.collapse_rhs(N,1e-8,y.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        a,ab=ns['forces'](y[:N],y[N]);reference=np.r_[y[N+1:],a,ab]
        error=float(np.max(abs(out-reference)/(1+abs(reference))))
        gradients=[]
        for j in [0,N//2,N-1,N]:
            delta=1e-5*(min(np.diff(np.r_[0,y[:N]])) if j<N else y[N])
            yp=y.copy();ym=y.copy();yp[j]+=delta;ym[j]-=delta
            E=lambda z:ns['energy'](z[:N],z[N+1:-1],z[N],z[-1])
            mass=ns['w'][j] if j<N else .6
            force=-(E(yp)-E(ym))/(2*delta*mass)
            actual=out[N+1+j]
            gradients.append(float(abs(force-actual)/(1+abs(actual))))
        records.append(dict(N=N,t=s['t'],compiled_vs_python=error,energy_gradient_errors=gradients))
checks=dict(force_identity=max(r['compiled_vs_python'] for r in records)<1e-8,
            energy_gradient=max(max(r['energy_gradient_errors']) for r in records)<1e-3)
out=dict(checks=checks,all_pass=all(checks.values()),records=records)
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
