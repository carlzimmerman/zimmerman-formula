"""Finite, declared checks of the complete leading quartic vacuum diagram.

No target alpha, fitted parameters, parent implementation imports or samples
selected by their answers. Analytic proof and scope are in the frozen raw note.
"""
import argparse
import json
import pathlib
import sympy as s
import mpmath as mp


def symbolic_checks():
    J, G, F, lam, V, kappa = s.symbols('J G F lambda V kappa')
    m, R, L, a, T = s.symbols('m R L a T', positive=True)
    pi = s.pi
    checks = []

    def equal(name, left, right):
        residual = s.factor(left-right)
        assert residual == 0, (name, residual)
        checks.append(name)

    equal('four_field_Wick_contractions', s.diff(s.exp(G*J**2/2), J, 4).subs(J, 0), 3*G**2)
    equal('quartic_figure_eight', (lam/s.factorial(4))*3*G**2, lam*G**2/8)
    delta = -lam*F/2
    equal('pole_mass_retuning_square', lam*(G**2-F**2)/8+delta*(G-F)/2, lam*(G-F)**2/8)
    equal('cosine_quartic', s.diff(-m**2*kappa*s.cos(J/s.sqrt(kappa)),J,4).subs(J,0), -m**2/kappa)
    equal('zero_mode_Bessel_correction', (-m**2/kappa)*V*(1/(V*m**2))**2/8, -1/(8*kappa*m**2*V))
    equal('mass_derivative_normalization', (-pi*a**2*T/2)*R**2/(2*a), (2*pi**2*R**3)*(-a*T/(4*pi*R))/2)

    def D(expr):
        return R*s.diff(expr,R)+(m*m*R*R/a)*s.diff(expr,a)-pi*(T*T-1)*(m*m*R*R/a)*s.diff(expr,T)

    def equal_on_spectrum(name, left, right):
        num = s.together(left-right).as_numer_denom()[0]
        rem = s.rem(s.expand(num), a*a-m*m*R*R+1, a)
        assert s.factor(rem) == 0, (name, s.factor(rem))
        checks.append(name)

    pref = lam/(128*pi*pi)
    q = a/R
    fA = pref*(q*q*T*T-m*m)
    tauA = pref*((m*m-1/(3*R*R))*T*T-m*m-(2*pi/3)*a*m*m*T*(T*T-1))
    equal_on_spectrum('exact_metric_derivative_path_A', fA+D(fA)/3, tauA)
    dqT = T/(q*R*R)-pi*m*m*R*(T*T-1)
    equal_on_spectrum('exact_q_coth_radial_derivative', D(q*T), dqT)
    X = q*T-m
    fB = pref*X*X
    equal_on_spectrum('exact_metric_derivative_path_B', fB+D(fB)/3, pref*(X*X+2*X*dqT/3))

    z = s.Symbol('z')
    alg_A = -pref*m*m*z
    alg_B = pref*m*m*(s.sqrt(1-z)-1)**2
    series_B = s.series(alg_B,z,0,5).removeO().expand()
    tau_B = s.series(alg_B-2*z*s.diff(alg_B,z)/3,z,0,5).removeO().expand()
    equal('path_A_only_R_minus_2', alg_A-2*z*s.diff(alg_A,z)/3, -lam*m*m*z/(384*pi*pi))
    equal('path_B_f_R_minus_4', series_B.coeff(z,2), lam*m*m/(512*pi*pi))
    equal('path_B_tau_R_minus_4', tau_B.coeff(z,2), -lam*m*m/(1536*pi*pi))
    equal('path_B_no_R_minus_2', series_B.coeff(z,1), 0)
    equal('path_B_f_R_minus_6', series_B.coeff(z,3), lam*m*m/(1024*pi*pi))
    equal('path_B_tau_R_minus_6', tau_B.coeff(z,3), -lam*m*m/(1024*pi*pi))
    equal('cosine_fixed_pole_tau_coefficient', (-lam/(1536*pi*pi*m*m*L)).subs(lam,-m*m/kappa), 1/(1536*pi*pi*kappa*L))
    return {'count':len(checks),'passed':checks,'fB_series_in_z':str(series_B),'tauB_series_in_z':str(tau_B)}


def numeric_checks(dps):
    mp.mp.dps = dps
    eps = mp.mpf('1e-50')
    names = []
    largest = mp.mpf(0)
    spectral_rows = []

    def close(name, x, y, extra=None):
        nonlocal largest
        err = abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
        largest = max(largest,err)
        assert err < eps, (name,str(err))
        if extra is not None:
            assert abs(x-y) <= extra+mp.mpf('1e-65'), (name,'tail bound',str(abs(x-y)),str(extra))
        names.append(name)

    def propagator(m,R):
        a = mp.sqrt((m*R)**2-1)
        return -a*mp.coth(mp.pi*a)/(4*mp.pi*R)

    def spectral(m,R):
        a = mp.sqrt((m*R)**2-1); N=256; K=40
        Q=mp.mpf(N+1)
        # Direct positive-scale Euler--Maclaurin evaluation avoids mpmath's
        # absolute stopping criterion on extremely small Hurwitz tails.
        def hurwitz_em(power):
            terms=[Q**(1-power)/(power-1),Q**(-power)/2]
            for j in range(1,51):
                terms.append(mp.bernoulli(2*j)/mp.factorial(2*j)
                             *mp.rf(power,2*j-1)*Q**(-power-2*j+1))
            return mp.fsum(terms),abs(terms[-1])
        total = mp.fsum(1/(n*n+a*a) for n in range(1,N+1))
        tail_terms=[];em_errors=[]
        for k in range(K+1):
            hk,err=hurwitz_em(2*k+2)
            tail_terms.append((-a*a)**k*hk)
            em_errors.append(a**(2*k)*err)
        total += mp.fsum(tail_terms)
        fp = -mp.mpf('0.5')-a*a*total
        power=2*K+4
        zeta_upper=Q**(1-power)/(power-1)+Q**(-power)
        geometric_bound=a**(2*K+4)*zeta_upper
        em_bound=a*a*mp.fsum(em_errors)
        bound=(geometric_bound+em_bound)/(2*mp.pi**2*R)
        return fp/(2*mp.pi**2*R),bound

    xs = list(map(mp.mpf,['1.05','1.25','2','3','5','10','20','30']))
    for x in xs:
        m=mp.mpf(1);R=x
        got,bound=spectral(m,R);exact=propagator(m,R)
        close('spectral_x_'+str(x),got,exact,extra=bound)
        spectral_rows.append({'mR':str(x),'tail_bound':str(bound),'absolute_error':str(abs(got-exact))})

    for m in map(mp.mpf,['0.5','1','2.5']):
        kappa=30*m; lam=-m*m/kappa;L=mp.mpf('0.7')
        for x in xs:
            R=x/m;a=mp.sqrt(x*x-1);q=a/R;ct=mp.coth(mp.pi*a);cs=1/mp.sinh(mp.pi*a)**2
            G=propagator(m,R);F=-m/(4*mp.pi);vol=2*mp.pi**2*R**3
            fA=lambda r:lam*(propagator(m,r)**2-F**2)/8
            fB=lambda r:lam*(propagator(m,r)-F)**2/8
            close('retuning_m_'+str(m)+'_x_'+str(x),fB(R),fA(R)-lam*F*(G-F)/4)
            tauA=lam/(128*mp.pi**2*L)*((m*m-1/(3*R*R))*ct*ct-m*m-(2*mp.pi/3)*a*m*m*ct*cs)
            tauB=lam/(128*mp.pi**2*L)*((q*ct-m)**2+mp.mpf(2)/3*(q*ct-m)*(ct/(q*R*R)-mp.pi*m*m*R*cs))
            close('stress_A_m_'+str(m)+'_x_'+str(x),(fA(R)+R*mp.diff(fA,R)/3)/L,tauA)
            close('stress_B_m_'+str(m)+'_x_'+str(x),(fB(R)+R*mp.diff(fB,R)/3)/L,tauB)
            # Differentiate the exact integrated determinant via its independently
            # defined derivative with respect to a; no copied tadpole sum.
            dW_da=-mp.pi*a*a*ct/2
            close('det_mass_derivative_m_'+str(m)+'_x_'+str(x),dW_da*R*R/(2*a),vol*G/2)

    heat_rows=[]
    for q0,R0,k in [('0.4','1',1),('0.7','1.3',1),('1.2','0.8',2),('2','1',1)]:
        q=mp.mpf(q0);R=mp.mpf(R0);c=(mp.pi*k*R)**2
        fun=lambda t:2*(4*mp.pi*t)**(-mp.mpf('1.5'))*(1-2*c/t)*mp.exp(-q*q*t-c/t)
        got=mp.quad(fun,[0,mp.sqrt(c)/q,mp.inf]);exact=-q/(2*mp.pi)*mp.exp(-2*mp.sqrt(c)*q)
        close('Poisson_heat_'+q0+'_'+R0+'_'+str(k),got,exact)
        heat_rows.append({'q':q0,'R':R0,'k':k,'absolute_error':str(abs(got-exact))})
    return {'dps':dps,'checks':len(names),'max_scaled_error':str(largest),'spectral_subtractions':spectral_rows,'winding_heat_integrals':heat_rows}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True)
    symbolic=symbolic_checks()
    numeric=[numeric_checks(dps) for dps in [70,95]]
    result={'status':'passed','symbolic':symbolic,'numeric':numeric,'non_claim':'Finite identities only. Loop completeness, tail proof, matching and physical scope are separately stated in RAW_DERIVATION_v1.md.'}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','symbolic_checks':symbolic['count'],'numeric_checks':[r['checks'] for r in numeric],'max_scaled_errors':[r['max_scaled_error'] for r in numeric]}))


if __name__=='__main__':main()
