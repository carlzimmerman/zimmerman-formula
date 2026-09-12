#!/usr/bin/env python3
"""GW/photon timing bookkeeping, NOT a fit or a full gravity certificate.

Published timing inputs: Abbott et al., ApJL 848 L13 (2017), sections 2.2/4.1.
The exact constant-speed model is Minkowski/low-redshift. The FLRW integral
is first order in the fractional speed difference, on a common background.
Source delays are unknowns, not quantities derived from the clock action.
"""
import argparse
import json
import platform
from pathlib import Path

import mpmath as mp
import sympy as sp


def symbolic_checks():
    checks = {}

    def check(name, condition):
        checks[name] = bool(condition)
        if not checks[name]:
            raise AssertionError(name)

    distance, c = sp.symbols("D c", positive=True)
    delta, source, lag = sp.symbols("delta source lag", real=True)
    # Arrival times constructed separately. delta=(c_GW-c_photon)/c_photon.
    t_gamma = source + distance / c
    t_gw = distance / (c * (1 + delta))
    arrival = sp.factor(t_gamma - t_gw)
    inferred = sp.solve(sp.Eq(arrival, lag), delta)[0]
    ratio = (lag - source) * c / distance
    check("arrival_sign_and_exact_rational_form",
          sp.simplify(arrival - source - distance / c * delta / (1 + delta)) == 0)
    check("exact_inversion", sp.simplify(inferred - ratio / (1 - ratio)) == 0)
    check("equal_speed_leaves_source_delay", sp.simplify(arrival.subs(delta, 0)-source) == 0)
    check("zero_source_delay_does_not_force_equal_speed", inferred.subs(source, 0) != 0)
    check("arrival_increases_with_delta",
          sp.simplify(sp.diff(arrival, delta)-distance/(c*(1+delta)**2)) == 0)

    # A common lapse changes both coordinate speeds, not their local ratio.
    lapse, scale = sp.symbols("N A", positive=True)
    omega, k = sp.symbols("omega k", real=True, nonzero=True)
    g = sp.diag(-lapse**2, scale**2)
    covector = sp.Matrix([-omega, k])
    cone = (covector.T * g.inv() * covector)[0]
    omega2 = sp.solve(cone, omega**2)[0]
    proper_speed2 = sp.factor(scale**2 / lapse**2 * omega2 / k**2)
    check("common_metric_local_null_speed", proper_speed2 == 1)

    # Control: an ACTUAL relative metric change, not relabeling time.
    conformal, disformal = sp.symbols("C B", real=True)
    g4 = sp.diag(-1, 1, 1, 1)
    normal_down = sp.Matrix([-1, 0, 0, 0])
    photon_metric = conformal*g4 + disformal*normal_down*normal_down.T
    photon_covector = sp.Matrix([-omega, k, 0, 0])
    photon_cone = (photon_covector.T*photon_metric.inv()*photon_covector)[0]
    photon_speed2 = sp.factor(sp.solve(photon_cone, omega**2)[0]/k**2)
    check("disformal_relative_cone_derived", sp.simplify(photon_speed2-(1-disformal/conformal)) == 0)
    check("conformal_control_same_cone", photon_speed2.subs(disformal, 0) == 1)
    check("changed_metric_negative_control", photon_speed2.subs({conformal:2, disformal:1}) != 1)

    # The unknown emission lag cancels from a two-image double difference.
    z, eg, ee, ga, gb, pa, pb = sp.symbols("z eg ee ga gb pa pb", real=True)
    tg_a, tg_b = (1+z)*eg+ga, (1+z)*eg+gb
    te_a, te_b = (1+z)*ee+pa, (1+z)*ee+pb
    double_difference = sp.expand((te_b-tg_b)-(te_a-tg_a))
    check("lensed_emission_cancellation", double_difference == -gb+ga+pb-pa)
    check("common_paths_null_test", sp.simplify(double_difference.subs({pa:ga,pb:gb})) == 0)
    check("differential_path_negative_control", double_difference.subs({pa:ga,pb:gb+1}) == 1)

    # A finite matrix witness of the general emission/speed degeneracy.
    # Compute its rank and nullspace: neither is inserted as a claimed output.
    eps = sp.Symbol("epsilon")
    source_lags = sp.symbols("e0:3")
    z_values = [sp.Rational(1,100), sp.Rational(1,10), sp.Rational(1,2)]
    path_integrals = [sp.Rational(4), sp.Rational(20), sp.Rational(80)]
    predictions = sp.Matrix([(1+zi)*si+eps*ii for zi,si,ii in zip(z_values, source_lags, path_integrals)])
    jacobian = predictions.jacobian([eps, *source_lags])
    nullspace = jacobian.nullspace()
    shift = sp.Symbol("shift")
    substituted = predictions.subs(dict([(eps, eps+shift)] +
        [(si, si-shift*ii/(1+zi)) for zi,si,ii in zip(z_values,source_lags,path_integrals)]), simultaneous=True)
    check("source_speed_reparametrization_invariance", sp.simplify(substituted-predictions) == sp.zeros(3,1))
    check("computed_nullspace_really_annihilated", all(jacobian*v == sp.zeros(3,1) for v in nullspace))
    check("unconstrained_sources_make_speed_unidentifiable", jacobian.rank() < jacobian.cols)
    # Even one free emission offset adds precisely the same ambiguity.
    single = predictions[:1, :].jacobian([eps, source_lags[0]])
    check("single_event_information_singular", sp.det(single.T*single) == 0)

    return {"checks": checks, "exact_arrival": str(arrival), "inferred_delta": str(inferred),
            "proper_speed_squared": str(proper_speed2), "disformal_photon_speed_squared":str(photon_speed2),
            "lensed_double_difference":str(double_difference), "finite_jacobian":str(jacobian),
            "computed_rank":jacobian.rank(), "computed_nullity":len(nullspace),
            "nullspace":[str(v) for v in nullspace]}


def numerical_checks():
    rows = []
    previous = None
    for precision in (50, 90):
        with mp.workdps(precision):
            c = mp.mpf("299792458")
            # SI conversion; extra printed digits serve arithmetic, not distance precision.
            mpc = mp.mpf("3.0856775814913673e22")
            lag = mp.mpf("1.74")
            sigma = mp.mpf("0.05")
            flight40 = 40*mpc/c
            flight26 = 26*mpc/c
            def infer(flight, observed, emission_observer):
                r = (observed-emission_observer)/flight
                return r/(1-r)
            central_bounds = [infer(flight26,lag,mp.mpf(10)), infer(flight26,lag,mp.mpf(0))]
            expanded = [infer(flight26,lag-sigma,mp.mpf(10)), infer(flight26,lag+sigma,mp.mpf(0))]
            # Verify at high precision using separately constructed arrival times.
            solutions = []
            for emission in map(mp.mpf, (0, 1, 2, 10)):
                eps = infer(flight40,lag,emission)
                reconstructed = (emission+flight40)-flight40/(1+eps)
                if abs(reconstructed-lag) > mp.mpf("1e-30"):
                    raise AssertionError("separate-arrival reconstruction")
                solutions.append({"observer_emission_delay_s":str(emission), "delta":mp.nstr(eps,20)})
            numeric_vector = [flight40, *central_bounds, *expanded]
            if previous is not None:
                for x,y in zip(previous,numeric_vector):
                    if not mp.almosteq(mp.mpf(x),y, rel_eps=mp.mpf("1e-35")):
                        raise AssertionError("precision refinement")
            previous = [mp.nstr(v,42) for v in numeric_vector]
            # FLRW illustration, NOT inference of the cosmology of this action.
            H0 = mp.mpf("70")*1000/mpc
            hubble = lambda zz: H0*mp.sqrt(mp.mpf("0.3")*(1+zz)**3+mp.mpf("0.7"))
            flrw = []
            for redshift in map(mp.mpf, ("0.01", "0.1", "1")):
                path_time = mp.quad(lambda zz: 1/hubble(zz), [0,redshift])
                lookback_time = mp.quad(lambda zz: 1/((1+zz)*hubble(zz)), [0,redshift])
                if not path_time > lookback_time > 0:
                    raise AssertionError("FLRW conformal weighting")
                flrw.append({"z":str(redshift), "path_integral_s":mp.nstr(path_time,16),
                             "lookback_s":mp.nstr(lookback_time,16),
                             "propagation_lag_for_delta_1e_minus15_s":mp.nstr(path_time*mp.mpf("1e-15"),16)})
            # An existence example of source kinematics, NOT a fit to this event:
            # emitting ejecta at radius R, speed beta*c, angle theta, launch delay tL.
            Gamma, radius, theta, launch = mp.mpf(10), mp.mpf("1e11"), mp.mpf("0.08"), mp.mpf("0.4")
            beta = mp.sqrt(1-Gamma**-2)
            source_kinematic_lag = launch+radius/c*(1/beta-mp.cos(theta))
            if source_kinematic_lag <= 0:
                raise AssertionError("subluminal source kinematics")
            a0 = mp.mpf("9.36e-11")  # Carl's GLOBAL empirical input, not fitted here.
            year = mp.mpf("365.25")*86400
            rows.append({"precision_digits":precision,"flight40_s":mp.nstr(flight40,20),
                         "flight40_years":mp.nstr(flight40/year,16),
                         "central_delta_bounds_26Mpc_0to10s":[mp.nstr(v,20) for v in central_bounds],
                         "bounds_with_plus_minus_0point05s":[mp.nstr(v,20) for v in expanded],
                         "source_delay_degeneracy":solutions,"FLRW_illustration":flrw,
                         "kinematic_example_lag_s":mp.nstr(source_kinematic_lag,16),
                         "kinematic_example_not_a_fit":{"Gamma":10,"R_m":"1e11","theta_rad":"0.08","launch_s":"0.4"},
                         "a0_input_m_s2":str(a0), "c_over_a0_years":mp.nstr(c/a0/year,16)})
    return {"precision_refinement":"50 and 90 digits agree to relative 1e-35 on declared vector",
            "source_reconstruction_absolute_tolerance_s":"1e-30", "rows":rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    result = {"scope":"conditional timing identities and published-input arithmetic; no new observation or gravity closure",
              "software":{"Python":platform.python_version(),"SymPy":sp.__version__,"mpmath":mp.__version__},
              "symbolic":symbolic_checks(),"numerical":numerical_checks()}
    payload = json.dumps(result, indent=2)
    if args.output:
        # Scientific result output only; refuse to overwrite prior evidence.
        with args.output.open("x") as target:
            target.write(payload+"\n")
    print(payload)


if __name__ == "__main__":
    main()
