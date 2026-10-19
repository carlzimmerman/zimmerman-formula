#!/usr/bin/env python3
"""Posttarget coordinate-moment and remainder-bound companion checks."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
from check_photon_mass_clean import ordinary_polynomial, value


def main(out):
    # Htrace/(4pi): diagonal quadratic coefficients for a,b separately.
    basis = {"a": [F(3),F(1),F(1),F(1)],
             "b": [F(0),F(-2),F(-2),F(-2)]}
    laplacians = {k: 2*sum(v) for k,v in basis.items()}
    assert laplacians == {"a":F(12),"b":F(-12)}
    # Moment=-4pi*laplacian; C=-moment/(512pi^2 M).
    c_times_pi_M = {k:4*v/512 for k,v in laplacians.items()}
    assert c_times_pi_M == {"a":F(3,32),"b":F(-3,32)}

    # K2(z)=2/z^2+c0+..., its Bessel ODE constant is -2-4c0.
    c0 = F(-1,2)
    assert -2-4*c0 == 0
    # G3 coordinate weight /(2M) is r^2 K2/(256pi^2 M).
    assert c0/F(256) == F(-1,512)

    # h(y)=(4y-1)(4y-3), y in [0,1]. Identities establish
    # -1<=h<=3, hence abs((5/3)h)<=5 over the complete interval.
    count = 0
    for j in range(65):
        y = F(j,64)
        h = (4*y-1)*(4*y-3)
        assert h == 16*(y-F(1,2))**2-1
        assert 3-h == 16*y*(1-y)
        assert -1 <= h <= 3
        assert abs(F(5,3)*h) <= 5
        count += 1
    # Exact integrated local fifth-filter polynomial.
    primitive = [F(0),F(0),F(0),F(5),F(-20),F(16)]
    derivative = [(j+1)*primitive[j+1] for j in range(5)]
    assert derivative == [F(0),F(0),F(15),F(-80),F(80)]
    # Positive remainder integral primitive derivative identity.
    p, q = [F(1),F(-1)], [F(1),F(1),F(1)]
    product = [sum((a*b for i,a in enumerate(p) for j,b in enumerate(q)
                    if i+j == degree),F(0)) for degree in range(4)]
    assert product == [F(1),F(0),F(0),F(-1)]

    # A finite-volume charged zero mode s^-1 is not removed.
    p = ordinary_polynomial([F(0),F(1,2),F(1),F(3,2),F(2)])
    inverse_power = value(p,F(-1))
    assert inverse_power == F(-45,2)
    assert F(2,3)*inverse_power == -15

    result = {"status":"exact bounded companion assertions passed",
              "coordinate_moment_over_pi": {k:str(-4*v) for k,v in laplacians.items()},
              "C_from_moment_denominator":"512*pi^2*M",
              "C_times_pi_M":{k:str(v) for k,v in c_times_pi_M.items()},
              "K2_constant_term":str(c0),
              "normalized_P5_absolute_kernel_bound_times_G3":5,
              "rational_kernel_ratio_diagnostic_points":count,
              "finite_volume_inverse_s_Euler_coefficient":str(inverse_power),
              "non_claims":["No QCD moment integrability or contact renormalization proved",
                            "No full-current numerical data", "No physical remainder bound"]}
    Path(out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"passed":True,"coordinate_factor":512,"remainder_bound_factor":5}))


if __name__ == "__main__":
    main(sys.argv[1])
