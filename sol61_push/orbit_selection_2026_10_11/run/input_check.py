"""Bounded tests of two inner kinetic routes; no halo formation simulation."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import beta

P = math.pi
checks = []


def check(name, ok, detail=None):
    checks.append(dict(name=name, passed=bool(ok), detail=detail))


def close(name, a, b, tol=1e-8):
    check(name, abs(a-b) <= tol*max(abs(b), 1e-300), dict(value=a, expected=b))


def hr(y):
    return y / math.expm1(math.sqrt(y))


def hp(y):
    q = math.sqrt(y)
    e = math.expm1(q)
    return (2*e-q*(1+e))/(2*e*e)


yp = brentq(hp, 1, 5)
b = .05*hr(yp)
ys = brentq(lambda y: hp(y)-b/(y+yp), 1, yp)


def repair(y):
    if y <= ys:
        return hr(y), hp(y)
    return hr(ys)+b*math.log((y+yp)/(ys+yp)), b/(y+yp)


def shell_scaled(r, energy, K, method):
    """rho exp(K/s), f=delta(E-energy) j^-8 exp(-K/j^2), mu=1."""
    s = 2*r + 2*energy*r*r
    k = K/s
    if method == 'angle':
        def integrand(theta):
            sn = math.sin(theta)
            if sn == 0:
                return 0.
            logval = -7*math.log(sn)-k*(1/sn**2-1)
            return math.exp(logval) if logval > -745 else 0.
        val = quad(integrand, 0, P/2, epsabs=1e-12, epsrel=1e-11)[0]
        return 4*P/r*s**(-3.5)*val
    val = quad(lambda z: (1+z*z/k)**2.5*math.exp(-z*z),
               0, 12, epsabs=1e-12, epsrel=1e-11)[0]
    return 4*P/r*s**(-3.5)/math.sqrt(k)*val


def main(output):
    close('splice_y', ys, 2.337412405, 1e-9)
    close('splice_slope', hp(ys), b/(ys+yp))
    repairs = []
    for y in [ys, 3., 10., 1e2, 1e4, 1e8, 1e12]:
        h, dh = repair(y)
        r = 1/math.sqrt(y)
        rho = (h-y*dh)/(2*P*r)
        step = 1e-5*r
        mass = lambda x: x*x*repair(1/x**2)[0]
        fd = (mass(r+step)-mass(r-step))/(2*step)/(4*P*r*r)
        close('repair_density_%g' % y, fd, rho, 2e-8)
        check('repair_positive_%g' % y, rho > 0 and dh > 0)
        repairs.append(dict(y=y, rho=rho, h=h, dh=dh))

    # Independent angular and Laplace-variable velocity integrals.
    shells = []
    for energy in [-1., -.5, 0.]:
        for q in [4., 16., 64., 256., 1024.]:
            r = 1/q
            K = 2.
            s = 2*r+2*energy*r*r
            a = shell_scaled(r, energy, K, 'angle')
            c = shell_scaled(r, energy, K, 'laplace')
            close('shell_quadrature_%g_%g' % (energy,q), a, c, 2e-10)
            # Analytic endpoint limit: rho~C r^-4 exp(-q), C contains exp(E).
            C = P**1.5/(4*math.sqrt(K))*math.exp(energy)
            ratio = c*r**4/C*math.exp(q-K/s)
            shells.append(dict(energy=energy, q=q, scaled_asymptotic_ratio=ratio))
        check('shell_asymptotic_%g' % energy, abs(ratio-1) < .006, ratio)

    # Polynomial low-j distributions give power laws. E=0 is a shell
    # integration benchmark, not a finite-mass bound halo.
    powers = []
    for n in [0., 1., 2., 4.]:
        angular = quad(lambda t: math.sin(t)**(2*n+1), 0, P/2)[0]
        close('polynomial_angular_%g' % n, angular, .5*beta(n+1,.5))
        r1, r2 = .02, .01
        rho = lambda r: 4*P/r*(2*r)**(n+.5)*angular
        slope = math.log(rho(r2)/rho(r1))/math.log(r2/r1)
        close('polynomial_slope_%g' % n, slope, n-.5)
        powers.append(dict(n=n, radial_power=slope))

    # A positive high-binding-energy isotropic DF realizes the repaired
    # cusp's leading terms in a prescribed Kepler field. Lower cutoff is
    # a declared construction, not a derived supply boundary.
    # rho=A Psi log(Psi)+B Psi; here G=Mb=a0=1, Psi=1/r.
    A = b/P
    B = (hr(ys)-b*math.log(ys+yp)-b)/(2*P)
    offset = 1+2*math.log(2)+B/A
    pref = A/(math.sqrt(8)*P**2)
    high_energy = []
    for psi in [10., 100., 1000., 10000.]:
        # E=psi sin^2 theta removes both endpoint square roots.
        lo = math.asin(1/math.sqrt(psi))
        fun = lambda t: (math.log(psi*math.sin(t)**2)+offset)*math.cos(t)**2
        rho = 8*P*math.sqrt(2)*pref*psi*quad(fun,lo,P/2,epsabs=1e-11)[0]
        leading = A*psi*math.log(psi)+B*psi
        # The omitted 0<E<1 integral is subleading O(sqrt(Psi)).
        remainder = (rho-leading)/math.sqrt(psi)
        high_energy.append(dict(psi=psi,rho=rho,leading=leading,remainder_scaled=remainder))
        check('positive_isotropic_%g' % psi, rho > 0)
    check('isotropic_relative_limit', abs(rho/leading-1) < .02, rho/leading)
    close('isotropic_subleading_limit', high_energy[-1]['remainder_scaled'],
          high_energy[-2]['remainder_scaled'], .001)
    check('positive_DF_above_cutoff', offset > 0, offset)

    # A regular imposed rotating quadrupole changes L; energy follows the
    # Jacobi relation. This is a transfer test, with external pattern work,
    # not a self-consistent bar, isolated-energy test or distribution selector.
    eps, a, soft, omega = .01, .3, .01, .7
    def field(t, pos):
        x,y = pos
        co,si = math.cos(omega*t),math.sin(omega*t)
        u,v = co*x+si*y,-si*x+co*y
        s = x*x+y*y+a*a
        amp = eps*a*a
        Q = amp*(u*u-v*v)*s**(-2.5)
        gu = amp*(2*u*s**(-2.5)-5*u*(u*u-v*v)*s**(-3.5))
        gv = amp*(-2*v*s**(-2.5)-5*v*(u*u-v*v)*s**(-3.5))
        rsoft = x*x+y*y+soft*soft
        grad = np.array([x,y])*rsoft**(-1.5)+np.array([co*gu-si*gv,si*gu+co*gv])
        return -rsoft**(-.5)+Q,grad
    def rhs(t,z):
        return np.r_[z[2:],-field(t,z[:2])[1]]
    sol = solve_ivp(rhs,(0,40),[1.,0.,0.,.6],method='DOP853',
                    rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,40,401))
    check('torque_integration_completed', sol.success)
    energy = np.array([.5*np.dot(z[2:],z[2:])+field(t,z[:2])[0]
                       for t,z in zip(sol.t,sol.y.T)])
    L = sol.y[0]*sol.y[3]-sol.y[1]*sol.y[2]
    jac = energy-omega*L
    residual = float(np.max(abs(jac-jac[0])))
    change = float(np.max(abs(L-L[0])))
    check('Jacobi_conserved', residual < 2e-8, residual)
    check('torque_changes_L', change > 1e-4, change)
    # Mutation controls: wrong pattern-work sign and wrong hollow exponent.
    wrong = energy+omega*L
    check('reject_wrong_Jacobi_sign', np.max(abs(wrong-wrong[0])) > 1e-4)
    r = .01
    correct = shell_scaled(r,-1.,2.,'laplace')*math.exp(-2/(2*r-2*r*r))
    wrong_shape = shell_scaled(r,-1.,1.,'laplace')*math.exp(-1/(2*r-2*r*r))
    check('reject_wrong_exponential_scale', wrong_shape/correct > 1e10)
    check('reject_exponential_density_as_repaired', abs(repair(100.)[0]-hr(100.)) > .5)

    result = dict(assertions=len(checks),passed=sum(x['passed'] for x in checks),
                  splice=dict(yp=yp,ys=ys,b=b),repair=repairs,shells=shells,
                  power_laws=powers,isotropic=high_energy,
                  torque=dict(jacobi_max_error=residual,L_max_change=change,nfev=sol.nfev),
                  checks=checks)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['assertions','passed','splice','torque']}))
    if result['passed'] != result['assertions']:
        print(json.dumps([x for x in checks if not x['passed']],indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    main(p.parse_args().output)
