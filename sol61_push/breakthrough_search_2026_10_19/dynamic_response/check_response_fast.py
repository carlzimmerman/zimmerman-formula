"""Bounded independent checks of the analytic retarded response; not a proof."""
import json
import pathlib
import sys
import mpmath as m
import sympy as s
import scipy.integrate as si
import scipy.special as sp
import math

m.mp.dps = 35
checks = []

def check(name, error, tol=m.mpf('1e-28')):
    error = abs(error)
    assert error < tol, (name, error, tol)
    checks.append({'name': name, 'absolute_error': str(error), 'tolerance': str(tol)})

sx = s.Matrix([[0, 1], [1, 0]])
sy = s.Matrix([[0, -s.I], [s.I, 0]])
sz = s.diag(1, -1)
d, D, b = s.symbols('d D b', positive=True)
H, P = d * (D * sx - b * sz), d * sz
comm = P * (H * P - P * H) - (H * P - P * H) * P
assert comm == -4 * d**3 * D * sx
checks.append({'name': 'exact double commutator', 'passed': True})

# Dimensionless a=p_sat=gamma=1; physical units restored in derivation.
def w(x):
    return x / (1 + x*x)**m.mpf('1.5')

def response_direct(z, bias):
    return m.quad(lambda x: w(x)*x*x/(m.sqrt(x*x+bias*bias)*(x*x+bias*bias-z*z)), [0, 1, m.inf])

def loss(q, bias):
    if q <= bias:
        return m.mpf(0)
    return m.pi*(q*q-bias*bias)/(2*q*(1+q*q-bias*bias)**m.mpf('1.5'))

def chi_zero(x):
    return (1-x*m.asinh(x)/m.sqrt(1+x*x))/(1+x*x) + 1j*m.pi*x/(2*(1+x*x)**m.mpf('1.5'))

def kernel(t):
    return t*m.besselk(0,t)

for bias in map(m.mpf, ['0', '.3', '1', '3']):
    static = m.quad(lambda x: w(x)*x*x/(x*x+bias*bias)**m.mpf('1.5'), [0, 1, m.inf])
    check('static derivative bias '+str(bias), static-1/(1+bias)**2)
    kk = (2/m.pi)*m.quad(lambda q: loss(q,bias)/q, [bias, bias+1, m.inf])
    check('static KK bias '+str(bias), kk-1/(1+bias)**2)
    for nu in map(m.mpf, ['.2', '2']):
        z = 1j*nu
        spectral = (2/m.pi)*m.quad(lambda q: q*loss(q,bias)/(q*q-z*z), [bias,bias+1,m.inf])
        check('spectral reconstruction '+str((bias,nu)), spectral-response_direct(z,bias))

# Independent transform of the time-domain Bessel kernel, including phase.
for x in map(m.mpf, ['0', '.3', '1', '3']):
    xx=float(x)
    real=si.quad(lambda t:t*sp.k0(t)*math.cos(xx*t),0,100,epsabs=2e-12,epsrel=2e-12)[0]
    imag=si.quad(lambda t:t*sp.k0(t)*math.sin(xx*t),0,100,epsabs=2e-12,epsrel=2e-12)[0]
    check('Bessel Fourier boundary '+str(x), complex(real,imag)-complex(chi_zero(x)),m.mpf('1e-10'))

# Oscillatory transform directly from the positive reduced-gap density.
for t in map(m.mpf, ['.2', '1', '3']):
    tt=float(t)
    direct=si.quad(lambda x:x/(1+x*x)**1.5,0,math.inf,weight='sin',wvar=tt,epsabs=1e-12,limlst=200)[0]
    check('gap sine transform '+str(t),direct-float(kernel(t)),m.mpf('1e-10'))

# Two-level threshold normalization follows independently from changing r^2=D^2+b^2.
for bias, q in [('0.3','0.8'), ('1','2'), ('3','5')]:
    bias,q=m.mpf(bias),m.mpf(q)
    gap=m.sqrt(q*q-bias*bias)
    delta_change=m.pi*w(gap)*gap/(2*q)
    check('threshold delta Jacobian '+str((bias,q)),delta_change-loss(q,bias))

# Verify the isotropic low-frequency exponent and coefficient at nonzero bias.
def w_iso(x):
    return x*(4+x*x)/(1+x*x)**m.mpf('2.5')
def iso_loss(q,bias):
    upper=min(m.mpf(1),q/bias) if bias else m.mpf(1)
    return m.pi/2*m.quad(lambda c: c*c*w_iso(m.sqrt(max(m.mpf(0),q*q-c*c*bias*bias)))*m.sqrt(max(m.mpf(0),q*q-c*c*bias*bias))/q,[0,upper])
for bias in map(m.mpf,['.3','1','3']):
    q=m.mpf('1e-5')*bias
    ratio=iso_loss(q,bias)/(4*m.pi*q**4/(15*bias**3))
    check('isotropic biased omega^4 '+str(bias),ratio-1,m.mpf('2e-9'))

# Finite cutoffs discriminate the logarithmically divergent first spectral moment.
for cutoff in map(m.mpf,['10','100','1000']):
    moment=m.quad(lambda q: q*loss(q,0),[0,1,cutoff])
    exact=m.pi/2*(m.asinh(cutoff)-cutoff/m.sqrt(1+cutoff*cutoff))
    check('finite f-sum primitive '+str(cutoff),moment-exact)

# A static-preserving variable-dipole counterexample regularizes UV strength.
def variable_d(x):
    return (1+x*x)**(-m.mpf('0.25'))
site_density=m.quad(lambda x:w(x)/variable_d(x),[0,1,m.inf])
check('variable d finite number density',site_density-2,m.mpf('1e-16'))
osc_strength=4*m.quad(lambda x:w(x)*variable_d(x)**2*x,[0,1,m.inf])
check('variable d finite oscillator strength',osc_strength-m.pi)

out={'assertion_tested':'Exact matrix identity and deterministic high-precision transform, KK, threshold, finite-moment and asymptotic controls in declared dimensionless domains.', 'checks':checks,'count':len(checks),'precision_decimal_digits':m.mp.dps,'all_passed':True}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'count':len(checks),'all_passed':True}))
