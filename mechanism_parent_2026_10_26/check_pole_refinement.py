"""Alternative matching-based G and twice as fine coupling continuation."""
import argparse,json
from pathlib import Path
import mpmath as mp
mp.mp.dps=60
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
base=json.loads(Path('mechanism_parent_2026_10_26/run_poles/result.json').read_text())
rows=[]
for old in base['rows']:
    A=old['A'];om=mp.mpf('.1')
    def G(z):
        x=mp.sqrt(A)*z
        a,b=mp.lu_solve(mp.matrix([[mp.sin(x),-mp.exp(1j*z)],
                                  [x*mp.cos(x),-1j*z*mp.exp(1j*z)]]),mp.matrix([-3/x**2,-3/x**2]))
        return 3/x**2+3*a*(mp.sin(x)-x*mp.cos(x))/x**2
    for j in range(1,81):
        C=mp.mpf('.2')*j/80
        fun=lambda z:mp.mpf('.01')-z*z+z*z*C*C*G(z)
        om=mp.findroot(fun,(om,om*(1+mp.mpf('1e-5'))-1j*mp.mpf('1e-8')),tol=mp.mpf('1e-48'),maxsteps=60)
        assert om.real>0 and om.imag<0
    target=mp.mpc(old['omega_real'],-old['amplitude_decay_rate'])
    error=float(abs(om-target)/abs(om));assert error<1e-12
    rows.append({'A':A,'relative_pole_difference':error,'steps':80})
Path(args.output).write_text(json.dumps({'rows':rows,'outcome':'finite branch continuations agree; not an exhaustive pole search'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
