#!/usr/bin/env python3
"""Independent turning-point quadrature, finite differences, and power integrals."""
import json, math, sys
from pathlib import Path
from scipy.integrate import quad

checks = []
rows = []
def check(name, actual, expected, rtol=2e-7):
    error = abs(actual-expected)/max(abs(expected), 1e-12)
    checks.append(dict(name=name, actual=actual, expected=expected,
                       relative_error=error, tolerance=rtol, passed=error <= rtol))

# V=x^2/2+lam*x^4/4. x=a*sin(theta) removes turning-point singularity.
# E-V = cos(theta)^2 [a^2/2 + lam*a^4*(1+sin(theta)^2)/4].
def orbit(E, lam):
    a2 = 2*E if lam == 0 else 4*E/(1+math.sqrt(1+4*lam*E))
    a = math.sqrt(a2)
    def xp(th):
        s, c = math.sin(th), math.cos(th)
        speed_factor = math.sqrt(a2 + lam*a2*a2*(1+s*s)/2)
        return a / speed_factor, a*speed_factor*c*c
    T = 4*quad(lambda th: xp(th)[0], 0, math.pi/2, epsabs=1e-11, epsrel=1e-11)[0]
    I = 4*quad(lambda th: xp(th)[1], 0, math.pi/2, epsabs=1e-11, epsrel=1e-11)[0]
    return T, I, I/T

for lam in [0., .1, 1., 10.]:
    for E in [.01, .1, 1., 10.]:
        T, I, D = orbit(E, lam) # k=1
        h = E*1e-4
        tm, im, dm = orbit(E-h, lam)
        tp, ip, dp = orbit(E+h, lam)
        check(f'action derivative lam={lam} E={E}', (ip-im)/(2*h), T)
        # q=ER-E. A_q = -1, even when T(E) varies.
        predicted_Aq = -(dp-dm)/(2*h) - D*(tp-tm)/(2*h*T)
        check(f'drift identity lam={lam} E={E}', predicted_Aq, -1.)
        rows.append(dict(lam=lam, E=E, period=T, diffusion=D, gap_drift=-1.,
                         reconstructed_gap_drift=predicted_Aq))
        if lam == 0:
            check(f'harmonic diffusion E={E}', D, E, 1e-10)
            check(f'harmonic period E={E}', T, 2*math.pi, 1e-10)

# Constant D=Q=1 regularized target. Integrate with y=sqrt(q+epsilon)
# and then z=y/sqrt(epsilon), independently of the closed mean-power formula.
powers=[]
for eps in [1., .1, .01, 1e-4, 1e-6]:
    a,b=math.sqrt(eps),math.sqrt(1+eps)
    Z=quad(lambda y: 2., a,b,epsabs=1e-12)[0]
    gain=quad(lambda z: 1/(a*z*z),1,b/a,epsabs=1e-10,epsrel=1e-11)[0]/Z
    predicted=1/(2*a*b)
    check(f'power epsilon={eps}',gain,predicted,1e-10)
    powers.append(dict(epsilon=eps, mean_extra_power=gain))

# Mutated physical coefficient must leave a nonzero target current.
# D=T=f=q=1, target f'=-1/2, missing b gives J=1/2.
check('missing extra drift exposes residual current', 0.-1.*(-.5), .5, 1e-12)
result=dict(all_passed=all(c['passed'] for c in checks), checks=checks,
            check_count=len(checks), orbit_grid=rows, power_grid=powers,
            scope='Finite quadrature checks of an analytically derived external momentum-kick model. No empirical data or complete gravity mechanism.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(all_passed=result['all_passed'],checks=len(checks),powers=powers),indent=2))
sys.exit(0 if result['all_passed'] else 1)
