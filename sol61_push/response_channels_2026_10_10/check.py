"""Finite-displacement check of instantaneous drift response; no time evolution."""
import json
import math
import pathlib
import sys

# Units: 4*pi*G = rho_center = R = alpha = 1; cold-dominated tau.
PI = math.pi
MASS = (2 * PI) ** 1.5
I0 = 3 * MASS


def integral(fn, a, b, n):
    h = (b - a) / n
    return h / 3 * (fn(a) + fn(b) + sum(
        (4 if k % 2 else 2) * fn(a + k * h) for k in range(1, n)))


def gravity(r):
    if r < .01:
        return r / 3 - r**3 / 10 + r**5 / 56 - r**7 / 432
    return (math.sqrt(PI / 2) * math.erf(r / math.sqrt(2))
            - r * math.exp(-r*r / 2)) / r**2


def dipole_rate(h, nr):
    # Integrate in coordinates centered on the displaced cold density.
    # Its actual mobility rho*tau = sqrt(rho), not a fitted constant.
    def radial(r):
        def angular(mu):
            z = r * mu + h
            s = math.sqrt(r*r + h*h + 2*r*h*mu)
            gz = gravity(s) * z / s if s else 0.
            return gz - gravity(r) * mu
        return r*r * math.exp(-r*r / 4) * integral(angular, -1, 1, 80)
    return 2 * PI / MASS / h * integral(radial, 0, 12, nr)


def size_flux(scale, nr):
    # Exact finite dilation; target potential stays fixed.
    return integral(lambda r: r**3 * scale**(-1.5)
                    * math.exp(-r*r / (4*scale*scale))
                    * (gravity(r) - gravity(r / scale) / scale**2),
                    0, 12, nr)


expected_d = (2/3)**1.5 / 3
expected_s = (2/3)**2.5
rows = []
checks = []
for nr in (400, 800):
    for h in (.02, .01, .005):
        d = dipole_rate(h, nr)
        s = 8 * PI * (size_flux(1+h, nr) - size_flux(1-h, nr)) / (
            I0 * ((1+h)**2 - (1-h)**2))
        rows.append(dict(radial_intervals=nr, perturbation=h,
                         dipole=d, size=s, ratio=s/d))
        checks.append(abs(d / expected_d - 1) < .001)
        checks.append(abs(s / expected_s - 1) < .001)
# Orthogonal mass/second-moment checks of the unperturbed Gaussian.
checks.append(abs(4*PI*integral(lambda r: r*r*math.exp(-r*r/2), 0, 12, 800)/MASS-1)<1e-10)
checks.append(abs(4*PI*integral(lambda r: r**4*math.exp(-r*r/2), 0, 12, 800)/I0-1)<1e-10)
# Dilation perturbation has zero total mass; no hidden source feeds assembly.
checks.append(abs(integral(lambda r: r*r*(3-r*r)*math.exp(-r*r/2), 0, 12, 800))<1e-10)
checks.append(abs(rows[2]['ratio']-rows[5]['ratio'])<1e-6)
# A shared scalar response rate is a negative control.
checks.append(abs(rows[-1]['size']/rows[-1]['dipole']-1)>.9)
out = dict(expected=dict(dipole=expected_d, size=expected_s, ratio=2),
           rows=rows, passed=sum(checks), count=len(checks),
           scope='Gaussian, two-sided drift only, instantaneous moment response; not halo evolution or a merger fit.')
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
sys.exit(0 if all(checks) else 1)
