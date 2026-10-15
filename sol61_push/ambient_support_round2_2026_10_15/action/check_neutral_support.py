#!/usr/bin/env python3
"""Exact checks for NS-ACTION-001; analytic scope is in PROOF.md."""
import hashlib
import json
from pathlib import Path
import sys

import sympy as s

checks = []


def equal(name, left, right=0):
    difference = s.simplify(left - right)
    is_zero = all(entry == 0 for entry in difference) if isinstance(difference, s.MatrixBase) else difference == 0
    if not is_zero:
        raise AssertionError((name, difference))
    checks.append({"name": name, "passed": True, "arithmetic": "exact SymPy"})


def truth(name, assertion):
    if not bool(assertion):
        raise AssertionError(name)
    checks.append({"name": name, "passed": True, "arithmetic": "exact SymPy"})


project = Path(__file__).resolve().parents[3]
inputs = Path(__file__).resolve().parents[1] / "inputs"
source_manifest = json.loads((inputs / "source_manifest.json").read_text())
used_snapshots = {"RTM_REPORT.md", "MC_MODES_PROOF.md", "MC_BOUNDARY_PROOF.md", "CE053_FINITE_EDGE.txt"}
for record in source_manifest["sources"]:
    if Path(record["snapshot"]).name in used_snapshots:
        digest = hashlib.sha256((project / record["snapshot"]).read_bytes()).hexdigest()
        truth("immutable snapshot " + Path(record["snapshot"]).name, digest == record["sha256"])

ex, ey, ez, vx, vy, vz = s.symbols("ex ey ez vx vy vz", real=True)
metric = s.diag(-1, 1, 1, 1)
u = s.Matrix([1, 0, 0, 0])
ul = metric * u
e = s.Matrix([0, ex, ey, ez])
du = s.Matrix([0, vx, vy, vz])
fcov = ul * e.T - e * ul.T
esq = ex**2 + ey**2 + ez**2
equal("pure electric F U = E", fcov * u, e)
equal("E F is parallel to U covector", e.T * fcov, -esq * ul.T)
equal("projected first frame variation vanishes", (e.T * fcov * du)[0])
equal("current frame variation is tangent", (ul.T * du)[0])
q, beta0, beta1, b2 = s.symbols("q beta0 beta1 b2", real=True)
equal("first magnetic density/frame variation vanishes",
      s.diff(-(beta0 + q * beta1) * q**2 * b2 / 2, q).subs(q, 0))

rho, c, k, n = s.symbols("rho c K n", positive=True)
pressure = k * rho ** (1 + 1/n)
energy = rho * c**2 + n * pressure
enthalpy = energy + pressure
sound = s.diff(pressure, rho) / s.diff(energy, rho)
effective = enthalpy * (1 - sound)
equal("thermodynamic h = rho d epsilon/d rho", enthalpy,
      rho * s.diff(energy, rho))
equal("polytropic effective gate inertia", effective,
      rho * c**2 + (n + 1) * (n - 1) * pressure / n)
equal("chemical enthalpy per mass", s.diff(energy, rho),
      c**2 + (n + 1) * k * rho**(1/n))

r, gm, density_amplitude = s.symbols("r GM0 density_amplitude", positive=True)
rho_r = density_amplitude * r**(-n)
p_r = gm * density_amplitude * r**(-n - 1) / (n + 1)
equal("hydrostatic polytrope derivative", s.diff(p_r, r), -rho_r * gm / r**2)
equal("hydrostatic enthalpy derivative", s.diff(gm/r, r), -gm/r**2)

y, x, eta, b = s.symbols("y x eta b", positive=True)
sound_profile = eta*y / (n * (1 + eta*y))
equal("sound along profile", sound.subs(k, gm/(n+1)/r/rho**(1/n)),
      gm/(n*r*c**2)/(1 + gm/(r*c**2)))
equal("profile effective inertia", (1 + eta*y) * (1 - sound_profile),
      1 + (n - 1)/n * eta*y)

f = y**(n - 6) * (1 + b*y) * (1 - x*y**2)**2
hpoly = ((n - 6) + (n - 5)*b*y - (n - 2)*x*y**2
         - (n - 1)*b*x*y**3)
equal("log derivative cubic", s.diff(f, y) / f * y*(1+b*y)*(1-x*y**2), hpoly)
equal("cubic strict concavity formula", s.diff(hpoly, y, 2),
      -2*(n-2)*x - 6*(n-1)*b*x*y)
equal("n=6 endpoint derivative factor", hpoly.subs(n, 6),
      y*(b - 4*x*y - 5*b*x*y**2))
equal("n=6 infinity coefficient", s.limit(f.subs(n, 6), y, 0), 1)
equal("n=7 gate necessarily lost at infinity", s.limit(f.subs(n, 7), y, 0), 0)
truth("n=4 ratio diverges at infinity", s.limit(f.subs(n, 4), y, 0) == s.oo)

rho0, d0, r0 = s.symbols("rho0 D0 R0", positive=True)
heff = rho0*c**2*y**n*(1+b*y)
hcrit = d0**2*x**3*y**6/(1-x*y**2)**2
equal("direct gate ratio", heff/hcrit, rho0*c**2/(d0**2*x**3)*f)
equal("mass amplitude normalization", 4*s.pi*rho0*r0**3/(n-3)
      * (n-3)/(4*s.pi*r0**3), rho0)

for index in (4, 5, 6):
    mass_integral = s.integrate(y**(index-4), (y, 0, 1))
    pressure_integral = s.integrate(y**(index-3), (y, 0, 1))
    equal(f"rest mass n={index}", mass_integral, s.Rational(1, index-3))
    equal(f"material energy n={index}",
          mass_integral + s.Rational(index, index+1)*eta*pressure_integral,
          mass_integral*(1+s.Rational(index, index+1)*eta
                         *s.Rational(index-3, index-2)))
    equal(f"integrated enthalpy n={index}",
          mass_integral + eta*pressure_integral,
          mass_integral*(1+eta*s.Rational(index-3, index-2)))

index = s.Rational(5999, 1000)
eta_value = s.Rational(1, 100)
counter = {n: index, x: s.Rational(1, 1000000),
           b: (index - 1)/index * eta_value}
truth("weak-field interior-minimum control H(0)<0", hpoly.subs(counter).subs(y, 0) < 0)
truth("weak-field interior-minimum control H(1)>0", hpoly.subs(counter).subs(y, 1) > 0)

beta, p, t, e2, h = s.symbols("beta p t E2 h", positive=True)
schur = p - beta - e2*(t-beta)**2/(h + e2*(t-beta))
equal("single-current cone Schur derivative", s.diff(schur, beta),
      -h**2/(h+e2*(t-beta))**2)

result = {
    "claim_id": "NS-ACTION-001",
    "status": "all declared finite exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "countercontrol": {
        "n": str(index), "eta": str(eta_value), "x0": "1/1000000",
        "H_at_1": str(s.factor(hpoly.subs(counter).subs(y, 1))),
        "meaning": "Inner gate alone is insufficient for some 5<n<6; no numerical root approximation used."
    },
    "non_claims": [
        "The finite checks do not prove the universal analytic conclusions without PROOF.md.",
        "No self-gravitating or Einstein solution, microscopic species, boundary match or global stability is constructed.",
        "The Newtonian comparison with exact local EOS is not an exact covariant background."
    ]
}
output = Path(sys.argv[1])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2) + "\n")
print(f"{len(checks)} exact checks passed; results written to {output}")
