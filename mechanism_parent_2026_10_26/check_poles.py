"""Self-consistent linear collective-mode poles; illustrative dimensionless input."""
import argparse,json
from pathlib import Path
import mpmath as mp
mp.mp.dps=60

def green(A,om):
    x=mp.sqrt(A)*om
    a=3/x**2*(1j*om-1)/(x*mp.cos(x)-1j*om*mp.sin(x))
    return 3/x**2+3*a*(mp.sin(x)-x*mp.cos(x))/x**2

def pole(A,target):
    # Track from the bare mechanical mode along coupling; do not select the
    # most strongly damped root after seeing the answer.
    om=mp.mpf('.1')
    maxres=mp.mpf(0)
    for j in range(1,41):
        C=mp.mpf(target)*j/40
        fun=lambda z:mp.mpf('.01')-z*z+z*z*C*C*green(A,z)
        om=mp.findroot(fun,(om,om*(1+mp.mpf('1e-5'))-1j*mp.mpf('1e-8')),tol=mp.mpf('1e-48'),maxsteps=60)
        maxres=max(maxres,abs(fun(om)))
        assert om.real>0 and om.imag<0
    assert maxres<mp.mpf('1e-45')
    return {'A':A,'C':float(mp.mpf(target)),'omega_real':float(om.real),
            'amplitude_decay_rate':float(-om.imag),'energy_efold_time':float(-1/(2*om.imag)),
            'max_root_residual':str(maxres),'coupling_continuation_steps':40}

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
rows=[pole(A,'.2') for A in [1,10,100,250,1000]]
weak=pole(1,'.002');C=mp.mpf('.002');meff=1+mp.mpf('1.2')*C*C
expected=C*C*mp.mpf('.01')/(2*meff*meff)
# finite omegaR~.1 leaves an O(omega^2) correction, not a precision error.
assert abs(mp.mpf(weak['amplitude_decay_rate'])/expected-1)<mp.mpf('.02')
out={'inputs':{'R':1,'mechanical_inertia':1,'spring_constant':.01,'coupling_C':.2},
     'rows':rows,'weak_coupling_control':weak,'weak_compact_prediction':float(expected),
     'non_claim':'Selected linear outgoing poles of a one-mode uniform-sphere model; no exhaustive pole count, no nonlinear fluid matching, no derived galaxy times.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
