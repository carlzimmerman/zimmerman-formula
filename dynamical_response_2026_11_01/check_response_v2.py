"""Independent finite DR01 controls. Import is passive; root runs the main."""
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp
from scipy.linalg import eigh


def fixed_system():
    nu = np.array([-1.4, -1.1, -.7, -.25, .35, .8, 1.15, 1.6])
    rr = np.arange(1, 4)[:, None]
    jj = np.arange(1, 9)[None, :]
    V = .065*(np.cos(rr*jj) + .7j*np.sin((rr+1)*jj))
    signs = np.array([-1., -1., 1.])
    b = (np.cos(np.arange(1, 9)) + .6j*np.sin(2*np.arange(1, 9)))/3
    return nu, V, signs, b


def matrix_control(original, response):
    nu, V, signs, b = fixed_system()
    zero_failure = None
    try:
        original.finite_hamiltonian(np.zeros_like(V), signs)
    except Exception as exc:
        zero_failure = type(exc).__name__ + ': ' + str(exc)
    ident = response.finite_hamiltonian(np.zeros_like(V), signs)
    eye = np.eye(len(nu))
    identity_error = max(float(np.max(abs(ident.sqrt(eye)-eye))),
                         float(np.max(abs(ident.invsqrt(eye)-eye))))
    H = eye + V.conj().T @ (signs[:, None]*V)
    ev, U = eigh(H)
    square = (U*np.sqrt(ev)) @ U.conj().T
    inverse = (U/np.sqrt(ev)) @ U.conj().T
    low = response.finite_hamiltonian(V, signs)
    errors = {'sqrt': float(np.max(abs(low.sqrt(eye)-square))),
              'invsqrt': float(np.max(abs(low.invsqrt(eye)-inverse))),
              'minimum': abs(low.minimum-float(ev[0])),
              'maximum': abs(low.maximum-float(ev[-1]))}
    return {'original_rank_zero_failure': zero_failure,
            'v2_rank_zero_identity_error': identity_error,
            'dense_comparison_errors': errors,
            'passed': bool(zero_failure is not None and identity_error < 2e-11
                           and max(errors.values()) < 2e-11 and ev[0] > 0)}


def pulse_control(response):
    T, omega = 7.3, .86
    lam = np.array([omega, omega-2*np.pi/T, omega+2*np.pi/T, 0., -.43, 1.91])
    times = np.linspace(0, T, 1201)
    def rhs(t, y):
        F = np.sin(np.pi*t/T)**2*np.exp(-1j*omega*t)
        return -1j*(lam*y+F)
    sol = solve_ivp(rhs, (0, T), np.zeros(len(lam), complex), t_eval=times,
                    method='DOP853', rtol=2e-12, atol=2e-14)
    exact = response.pulse_integral(lam, times, omega, T)
    error = float(np.max(abs(sol.y-exact))/max(1., np.max(abs(exact))))
    late = response.pulse_integral(lam, np.array([1.3*T, 2*T]), omega, T)
    late_direct = sol.y[:, -1, None]*np.exp(-1j*lam[:, None]*(np.array([1.3*T, 2*T])-T))
    late_error = float(np.max(abs(late-late_direct))/max(1., np.max(abs(late_direct))))
    return {'direct_ivp_success': sol.success, 'pulse_scaled_error': error,
            'post_pulse_scaled_error': late_error,
            'passed': bool(sol.success and max(error, late_error) < 2e-9)}


def finite_response_control(response, bare):
    nu, V, signs, b = fixed_system()
    if bare:
        V = np.zeros_like(V)
    H = np.eye(len(nu)) + V.conj().T @ (signs[:, None]*V)
    # This analytic background only supplies units and the optional radial
    # diagnostic. The independent eight-mode matrix is not a halo truncation.
    from orbits import HarmonicBackground
    bg = HarmonicBackground(omega=.7, energy=1.3)
    bg.omega_dyn = 1.3
    bg.original_psi = 10.
    bg.original_radius = bg.R
    data, series = response.solve_pulses(V, signs, nu, b, .37*b, bg, nkrylov=8, nt=4097)
    rows = []
    for row in data['cases']:
        T, amp, omega = row['pulse_duration'], row['amplitude'], row['forcing_omega']
        times = series[str(row['pattern_ratio'])][0]
        # Integrate z/amplitude and the three ledgers/amplitude**2.
        def rhs(t, state):
            z = state[:len(nu)]
            env = np.sin(np.pi*t/T)**2
            denv = np.pi/T*np.sin(2*np.pi*t/T)
            phase = np.exp(-1j*omega*t)
            F, Fe = env*phase, denv*phase
            Fdot = Fe-1j*omega*F
            obs = np.vdot(b, z)
            return np.r_[-1j*nu*(H@z+b*F),
                         .5*np.real(obs.conjugate()*Fdot),
                         np.imag(obs.conjugate()*F),
                         .5*np.real(obs.conjugate()*Fe)]
        sol = solve_ivp(rhs, (0, T), np.zeros(len(nu)+3, complex), t_eval=times,
                        method='DOP853', rtol=2e-13,
                        atol=np.r_[np.full(len(nu), 2e-18), np.full(3, 2e-20)],
                        max_step=T/4096)
        final = amp*sol.y[:len(nu), -1]
        energy = float(np.vdot(final, H@final).real/4)
        angular = float(.5*np.sum(abs(final)**2/nu))
        work, torque, envwork = amp**2*sol.y[-3:, -1].real
        obs = amp*(b.conj()@sol.y[:len(nu)])
        computed = series[str(row['pattern_ratio'])][3] + 1j*series[str(row['pattern_ratio'])][4]
        e_scale = max(energy, abs(work), 1e-13)
        j_scale = max(abs(angular), abs(torque), 1e-13)
        errors = {'response': float(np.max(abs(obs-computed))/max(np.max(abs(obs)), 1e-12)),
                  'energy': abs(row['final_energy']-energy)/e_scale,
                  'work': abs(row['work']-work)/e_scale,
                  'torque': abs(row['torque_integral']-torque)/j_scale,
                  'canonical_angular': abs(row['canonical_angular_momentum']-angular)/j_scale,
                  'direct_work_energy': abs(work-energy)/e_scale,
                  'direct_torque_angular': abs(torque-angular)/j_scale,
                  'direct_rotating_ledger': abs(work-omega/2*torque-envwork)/max(e_scale,abs(envwork))}
        rows.append({'pattern_ratio': row['pattern_ratio'], 'errors': errors,
                     'direct_energy': energy, 'direct_work': float(work),
                     'direct_torque': float(torque),
                     'passed': bool(sol.success and max(errors.values()) < 2e-6)})
    return {'bare': bare, 'cases': rows, 'passed': all(r['passed'] for r in rows)}


def angular_control():
    mu, w = leggauss(32)
    C = math.sqrt(15/(32*math.pi))
    norm = float(2*np.pi*np.dot(w, C*C*(1-mu*mu)**2))
    gradient = float(2*np.pi*np.dot(w, 4*C*C*(1-mu*mu)*(1+mu*mu)))
    planar = (2*C*C+5/(16*np.pi))/5
    errors = {'complex_Y22_norm': abs(norm-1), 'real_Y22_norm': abs(norm/2-.5),
              'angular_gradient': abs(gradient-6), 'orientation': abs(planar-1/(4*np.pi))}
    return {'errors': errors, 'passed': max(errors.values()) < 2e-12}


def harmonic_shell_control():
    from orbits import HarmonicBackground, OrbitFamily
    bg = HarmonicBackground(omega=.7, energy=1.3)
    family = OrbitFamily(bg)
    xx, ww = leggauss(32)
    Ls, weights = (xx+1)*family.Lmax/2, ww*family.Lmax/2
    accumulated = np.zeros((3, 3), complex)
    moment = 0.
    fstar = 3/(4*np.pi*2**1.5)
    nphase = 512
    modes = np.fft.fftfreq(nphase, 1/nphase)
    for L, weight in zip(Ls, weights):
        orbit = family.orbit(float(L), nphase=nphase)
        r, pr, pt = orbit['r'], orbit['pr'], orbit['pphi']
        mw = fstar*(2*np.pi)**3*2*L*weight/orbit['Omega_r']/5
        for k in (-2, 0, 2):
            Y = -math.sqrt(5/(16*np.pi)) if k == 0 else math.sqrt(15/(32*np.pi))
            angular = Y*np.exp(1j*k*orbit['dphi'])
            current = pr*2*r/bg.R**2+1j*k*pt*r/bg.R**2
            values = np.vstack(((r/bg.R)**2, (r/bg.R)**4, current))*angular
            coeff = np.fft.fft(values, axis=1)/nphase
            accumulated += mw*(coeff.conj()@coeff.T)
            frequency = modes*orbit['Omega_r']+k*orbit['Omega_phi']
            moment += mw*float(np.sum(frequency**2*abs(coeff[0])**2))
    def beta(a, b):
        return math.gamma(a)*math.gamma(b)/math.gamma(a+b)
    direct = np.zeros((3, 3))
    for i, pi in enumerate((2, 4)):
        for j, pj in enumerate((2, 4)):
            direct[i, j] = .75*math.sqrt(bg.energy)*bg.R**3*beta((3+pi+pj)/2, 1.5)
    direct[2, 2] = 5*bg.energy**1.5*bg.R*beta(2.5, 2.5)
    scales = np.sqrt(np.diag(direct))
    error = float(np.max(abs(accumulated-direct)/np.outer(scales, scales)))
    fsum_error = abs(moment/direct[2, 2]-1)
    return {'spectral_gram_real': accumulated.real.tolist(), 'spectral_gram_imag': accumulated.imag.tolist(),
            'analytic_radial_gram': direct.tolist(), 'gram_scaled_error': error,
            'bare_frequency_second_moment': moment, 'analytic_force_sum': direct[2, 2],
            'force_sum_relative_error': fsum_error,
            'passed': bool(error < 3e-5 and fsum_error < 3e-5)}


def main():
    import response as original
    import response_v2 as response
    result = {'scope': 'Independent finite controls; not halo response evidence', 'checks': {}}
    try:
        result['matrix'] = matrix_control(original, response)
        result['pulse'] = pulse_control(response)
        result['angular'] = angular_control()
        result['bare_response'] = finite_response_control(response, True)
        result['dressed_response'] = finite_response_control(response, False)
        result['harmonic_shell'] = harmonic_shell_control()
        result['checks'] = {key: result[key]['passed'] for key in
                            ('matrix', 'pulse', 'angular', 'bare_response', 'dressed_response', 'harmonic_shell')}
        result['all_controls_pass'] = all(result['checks'].values())
    except Exception as exc:
        import traceback
        result['exception'] = repr(exc)
        result['traceback'] = traceback.format_exc()
        result['all_controls_pass'] = False
    output = Path(sys.argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'checks': result['checks'], 'passed': result['all_controls_pass']}))
    return 0 if result['all_controls_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
