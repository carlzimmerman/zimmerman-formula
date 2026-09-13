#!/usr/bin/env python3
"""Bounded PAPER25 audit; no full solar-system or gravitational solution.

Run with --output-dir below this audit directory. Original L216 runs in that
directory so its hardcoded result path cannot overwrite the shared result.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy

import sympy as S


def main(output):
    root = Path(__file__).resolve().parents[6]
    original = root / 'fable_independent_2026/L216_clock_alignment.py'
    assert original.is_file(), root
    before = hashlib.sha256(original.read_bytes()).hexdigest()
    output = output.resolve()
    assert Path(__file__).resolve().parent in output.parents
    output.mkdir(parents=True, exist_ok=True)
    (output / 'fable_independent_2026').mkdir(exist_ok=True)
    captured = io.StringIO()
    cwd = Path.cwd()
    try:
        os.chdir(output)
        with contextlib.redirect_stdout(captured):
            reproduction = runpy.run_path(str(original), run_name='__main__')
    finally:
        os.chdir(cwd)
    (output / 'L216.stdout.txt').write_text(captured.getvalue())
    assert hashlib.sha256(original.read_bytes()).hexdigest() == before
    old_results = json.loads((root / 'fable_independent_2026/L216_results.json').read_text())
    new_results = json.loads((output / 'fable_independent_2026/L216_results.json').read_text())
    checks = {}

    def eq(name, lhs, rhs=0):
        difference = S.simplify(lhs-rhs)
        checks[name] = difference == 0
        assert checks[name], (name, difference)

    eps = S.symbols('epsilon', real=True)
    s0, W, G, M, R, fs = S.symbols('s0 W G M R fs', positive=True)
    dt, z = S.symbols('dotpi z', real=True)
    # tau = s0*(t+pi); z = |grad pi| is physical tilt at first order.
    clock_norm = s0*S.sqrt((1+eps*dt)**2-eps**2*z**2)
    clock2 = S.diff(clock_norm, eps, 2).subs(eps, 0)/2
    eq('normalized_clock_quadratic', clock2, -s0*z**2/2)
    eq('normalized_clock_no_time_kinetic', S.diff(clock2, dt, 2))
    physical_stiffness = S.simplify(-S.diff(W*clock2, z, 2))
    eq('physical_tilt_stiffness_is_s0_W', physical_stiffness, s0*W)
    Wpaper = fs**2*G*M**2/(8*S.pi*s0*R**4)
    source = 4*(fs*G*M/R)*(3*M/(4*S.pi*R**3))
    corrected_gain = S.simplify(source/physical_stiffness.subs(W, Wpaper))
    eq('fixed_W_truncation_gain_has_no_s0', corrected_gain, 24/fs)

    # Exact projected invariant; spatial rotation sets background grad chi=(p,0,0).
    # This covers arbitrary tilt z by retaining all three independent components.
    q, p, zx, zy, zz = S.symbols('q p zx zy zz', real=True)
    W0, WY, WYY = S.symbols('W0 WY WYY', real=True)
    z2 = zx**2+zy**2+zz**2
    Q = (q-eps*p*zx)/S.sqrt(1-eps**2*z2)
    Y = Q**2-q**2+p**2
    dy = S.series(Y-p**2, eps, 0, 3).removeO().expand()
    eq('Y_linear', dy.coeff(eps, 1), -2*q*p*zx)
    eq('Y_quadratic', dy.coeff(eps, 2), q**2*z2+p**2*zx**2)
    L = s0*S.sqrt(1-eps**2*z2)*(W0+WY*dy+WYY*dy**2/2)
    L2 = S.diff(L, eps, 2).subs(eps, 0)/2
    L2expected = s0*((-W0/2+q**2*WY)*z2+(WY+2*q**2*WYY)*p**2*zx**2)
    eq('full_sW_quadratic_in_tilt', L2, L2expected)
    Kparallel = S.simplify(-S.diff(L2, zx, 2))
    Kperp = S.simplify(-S.diff(L2, zy, 2))
    eq('parallel_stiffness', Kparallel,
       s0*(W0-2*q**2*WY-2*p**2*(WY+2*q**2*WYY)))
    eq('perpendicular_stiffness', Kperp, s0*(W0-2*q**2*WY))
    eq('homogeneous_known_clock_stiffness', Kperp/s0**2, (W0-2*q**2*WY)/s0)
    B = 2*q*WY
    C = (W0-2*q**2*WY)/s0
    eq('W0_zero_clock_response_is_nonzero', (-B/C).subs(W0, 0), s0/q)

    # Exact first-order matter-metric term, expanded to velocity/tilt degree 2.
    rho, varphi, vel = S.symbols('rho varphi vel', real=True)
    Cmet, Dmet = 1-2*varphi, -4*varphi
    proper_time2 = Cmet*(1-eps**2*vel**2)-Dmet*(1+eps**2*z*vel)**2/(1-eps**2*z**2)
    matter_phi = S.diff(-rho*S.sqrt(proper_time2), varphi).subs(varphi, 0)*varphi
    matter2 = S.diff(matter_phi, eps, 2).subs(eps, 0)/2
    matter_tilt = S.expand(matter2-matter2.subs(z, 0))
    eq('matter_action_tilt_terms', matter_tilt, -2*rho*varphi*z**2-4*rho*varphi*z*vel)

    # PAPER25 roots are valid for its assumed scalar-weighted vacuum operator.
    n = (3-S.sqrt(17))/2
    eq('advertised_indicial_root', n**2-3*n-2)
    pp = 1-n
    reach = float((S.Rational(6957, 10000)/S.Rational(1496, 10))**pp)
    # Same R_sun/AU as PAPER25, in 1e9 m units.
    paper_reach = (6.957e8/1.496e11)**float(pp)
    assert abs(reach-paper_reach) < 1e-18
    eta = 1.25e-5
    exact_paper_rate = (1/eta-1)/(24*reach)
    # Even accepting a surface saturation law, propagating tilt and propagating
    # gain before saturation are different operations.
    surface_D = 48.0
    propagated_saturated_tilt = surface_D/(1+surface_D)*reach
    paper_saturated_propagated_gain = surface_D*reach/(1+surface_D*reach)
    assert abs(propagated_saturated_tilt-paper_saturated_propagated_gain) > 0.01
    checks['surface_saturation_and_exterior_propagation_do_not_commute'] = True

    # Re-run the independent action-derived photon-cone calculation.
    cone_path = root / ('qwen_claude_field_theory/closure_2026/clock_response_repair_2026/'
                        'closure_front_2026/disformal_cone/derive_cone.py')
    spec = importlib.util.spec_from_file_location('p25_cone', cone_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cone = module.derive()
    assert all(cone['checks'].values())
    checks['prior_cone_34_checks_reproduced'] = len(cone['checks']) == 34
    assert all(checks.values())
    result = {
        'scope': 'Exact local Taylor identities and algebraic surrogate checks; no full stellar BVP, PPN fit, or EFT cutoff',
        'checks': checks,
        'L216_reproduction': {'pass': reproduction['NP'], 'fail': reproduction['NF'],
                              'matches_committed_json': new_results == old_results,
                              'input_sha256': before,
                              'meaning': 'Reproduces arithmetic and assertions, not their field-theory interpretation'},
        'physical_tilt_normalization': {'stiffness': str(physical_stiffness), 'gain_in_fixed_W_truncation': str(corrected_gain)},
        'projected_Y_clock_hessian': {'L2': str(S.expand(L2)), 'parallel_stiffness': str(Kparallel),
                                     'perpendicular_stiffness': str(Kperp), 'matter_tilt_terms': str(matter_tilt)},
        'paper_arithmetic': {'falloff_exponent': float(pp), 'Rsun_over_AU_to_p': reach,
                            'rate_exact_within_paper_surrogate': exact_paper_rate,
                            'rate_approx_paper': 1/eta/(24*reach),
                            'surface_D_48_propagated_saturated_tilt': propagated_saturated_tilt,
                            'surface_D_48_paper_saturated_propagated_gain': paper_saturated_propagated_gain,
                            'fixed_W_corrected_gain_at_surface_fs1': 24,
                            'fixed_W_corrected_gain_times_reach': 24*reach},
        'cone': cone,
        'non_claims': ['No complete gravitational clock constraint or canonical-pair count',
                       'No observational bound on clock rate established',
                       'No alternate solar-system alignment prediction from the fixed-W check',
                       'No nonlinear or all-background tensor-cone theorem',
                       'No quantum strong-coupling scale']}
    (output / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    main(parser.parse_args().output_dir)
