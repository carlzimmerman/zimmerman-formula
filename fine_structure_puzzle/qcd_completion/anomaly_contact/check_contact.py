"""Bounded independent representations of the specified compact contact model."""
import argparse
import json
import platform
from pathlib import Path
import mpmath as mp
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    checks = []
    rows = []

    def check(name, condition, detail):
        checks.append({'name': name, 'passed': bool(condition), 'detail': detail})
        if not condition:
            raise AssertionError(name + ': ' + str(detail))

    # Full nonzero p-form determinant exponents, then Hodge pairing C3=C0,C2=C1.
    full = {j: sp.Rational((-1) ** (4-j) * (4-j), 2) for j in range(4)}
    coexact = {j: full[j] + full.get(j+1, 0) for j in range(4)}
    check('coexact spectral cancellation',
          coexact[0]+coexact[3] == 0 and coexact[1]+coexact[2] == 0,
          {str(k): str(v) for k, v in coexact.items()})

    # Gaussian moments after y=sqrt(a V)*x; an independent algebraic Laplace expansion.
    B, a, eps, y = sp.symbols('B a eps y', positive=True)
    polynomial = 1 + B*y**4*eps/(24*a**2) + eps**2*(B**2*y**8/(1152*a**4)-B*y**6/(720*a**3))
    def gaussian_moment(poly):
        answer = 0
        for (n,), coeff in sp.Poly(poly, y).terms():
            answer += coeff * (sp.factorial2(n-1) if n else 1)
        return sp.expand(answer)
    expansion = gaussian_moment(polynomial)
    expected = 1+B*eps/(8*a**2)+(35*B**2/(384*a**4)-B/(48*a**3))*eps**2
    check('Laplace Z coefficients', sp.simplify(expansion-expected) == 0, str(expansion))
    log_series = sp.series(sp.log(expansion), eps, 0, 3).removeO()
    check('Laplace log coefficients', sp.simplify(log_series-(B*eps/(8*a**2)+(B**2/(12*a**4)-B/(48*a**3))*eps**2)) == 0, str(log_series))
    phi, theta, chi = sp.symbols('phi theta chi', real=True)
    quadratic = B*phi**2/2+chi*(theta+phi)**2/2
    minimized = sp.simplify(quadratic.subs(phi, -chi*theta/(chi+B)))
    check('screened susceptibility', sp.simplify(sp.diff(minimized, theta, 2)-chi*B/(chi+B)) == 0, str(minimized))

    for dps in (55, 80):
        mp.mp.dps = dps
        tol = mp.mpf('1e-35')
        # Unit chi_g=mu=f_s=1, t=chi_g V and b=B/chi_g. No physics constants are fit.
        for t0 in ('0.02', '0.2', '1', '3'):
            t = mp.mpf(t0)
            for theta0 in ('0', '0.7', 'pi'):
                th = mp.pi if theta0 == 'pi' else mp.mpf(theta0)
                flux = mp.fsum(mp.exp(-q*q/(2*t))*mp.cos(q*th) for q in range(-160, 161))/mp.sqrt(2*mp.pi*t)
                branch = mp.fsum(mp.exp(-t*(th+2*mp.pi*k)**2/2) for k in range(-40, 41))
                rel = abs(flux-branch)/branch
                check('flux Poisson dps%d t%s theta%s' % (dps,t0,theta0), rel < tol, mp.nstr(rel, 9))
        for t0 in ('0.5','2','8'):
            t = mp.mpf(t0)
            for b0 in ('0','0.5','2'):
                b = mp.mpf(b0)
                for theta0 in ('0','0.7'):
                    th = mp.mpf(theta0)
                    # Direct unfolded integral, Gaussian coordinate y. Bound omitted tails
                    # by exp(-y^2/2); |y|>22 gives <1e-106 before normalization.
                    def density(yv):
                        xv = yv/mp.sqrt(t)-th
                        return mp.exp(-yv*yv/2-t*b*(1-mp.cos(xv)))
                    grid = list(range(-22,23,2))
                    den = mp.quad(density, grid)
                    direct = den/mp.sqrt(2*mp.pi)
                    terms = [mp.besseli(n,t*b)*mp.exp(-n*n/(2*t)) for n in range(81)]
                    fourier = mp.exp(-t*b)*(terms[0]+2*mp.fsum(terms[n]*mp.cos(n*th) for n in range(1,81)))
                    rel = abs(direct-fourier)/direct
                    check('compact Fourier dps%d t%s b%s theta%s' % (dps,t0,b0,theta0), rel < tol, mp.nstr(rel, 9))
                    if th == 0:
                        # Orthogonal susceptibility implementations: integral moments vs Fourier charge moments.
                        x2 = mp.quad(lambda yv:(yv*yv/t)*density(yv),grid)/den
                        susc_direct = 1-t*x2
                        susc_fourier = (2*mp.fsum(n*n*terms[n] for n in range(1,81)))/(t*(terms[0]+2*mp.fsum(terms[1:])))
                        err = abs(susc_direct-susc_fourier)
                        check('screening dps%d t%s b%s' % (dps,t0,b0), err < tol, mp.nstr(err, 9))
                    rows.append({'dps':dps,'t':t0,'b':b0,'theta':theta0,'Z0':mp.nstr(direct,35),'relative_representation_error':mp.nstr(rel,9)})
        # Large-volume stress from actual quadrature, independently of asserted series.
        for b0 in ('0.5','2'):
            b = mp.mpf(b0)
            a_num = 1+b
            for t0 in (40,80,160):
                t = mp.mpf(t0)
                def den_large(yv):
                    x = yv/mp.sqrt(a_num*t)
                    return mp.exp(-t*(x*x/2+b*(1-mp.cos(x))))
                grid = list(range(-22,23,2))
                den = mp.quad(den_large,grid)
                energy = mp.quad(lambda yv:((yv/mp.sqrt(a_num*t))**2/2+b*(1-mp.cos(yv/mp.sqrt(a_num*t))))*den_large(yv),grid)/den
                rho = energy-1/(2*t)
                first = b/(8*a_num**2*t*t)
                second = 2*(b*b/(12*a_num**4)-b/(48*a_num**3))/t**3
                error_scaled = abs((rho-first-second)*t**4)
                # Conservative finite-range O(t^-4) check; not a certified universal remainder bound.
                check('stress asymptotic dps%d b%s t%s' % (dps,b0,t0), error_scaled < mp.mpf('0.01'), mp.nstr(error_scaled,9))
                rows.append({'dps':dps,'b':b0,'t':t0,'rho0_over_chi':mp.nstr(rho,35),'predicted_through_t^-3':mp.nstr(first+second,35),'scaled_error':mp.nstr(error_scaled,9)})
    result = {'claim_id':'FSP-004-CONTACT','assertion_tested':'Exact compact-model representation identities, canonical spectral and zero-mode cancellation, screening and finite-range large-volume stress coefficients; not full QCD','software':{'Python':platform.python_version(),'sympy':sp.__version__,'mpmath':mp.__version__},'passed':all(c['passed'] for c in checks),'check_count':len(checks),'checks':checks,'rows':rows,'limits':{'direct_gaussian_abs_tail':'less than 1e-106 before normalization','Fourier_terms':'n=-80..80; I_n(z)<=exp(z) bounds omitted tail by Gaussian with t<=8','pure_flux_terms':'Q=-160..160 and k=-40..40, t<=3','numerics':'high precision floating, not interval certificates'}}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'checks':len(checks)}))


if __name__ == '__main__':
    main()
