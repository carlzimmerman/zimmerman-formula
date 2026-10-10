"""Bounded arithmetic checks of the report's analytic transport identities.

No observations, fitted ages, halo evolution, or simulation outputs are used.
Units: G = V_f = alpha = r_in = M_b = r_M = 1 where applicable.
"""
import json
import math
import pathlib
import sys

checks = []
def check(name, passed, **details):
    checks.append(dict(name=name, passed=bool(passed), **details))

def derivative(fun, x):
    h = 1e-3*x
    return (fun(x-2*h)-8*fun(x-h)+8*fun(x+h)-fun(x+2*h))/(12*h)

def m0(r):
    return 1/math.expm1(1/r)

def m0_prime(r):
    q = 1/r
    return math.exp(q)/(r*r*math.expm1(q)**2)

edges = []
for supply in (5.364, 20.0, 50.0):
    row = dict(supply_over_mb=supply, edges={})
    for boost in (0.5, 1.0, 2.0, 3.0):
        edge = 1/math.log1p(boost/supply)
        row['edges'][str(boost)] = edge
        check('edge_mass_identity', math.isclose(boost*m0(edge), supply, rel_tol=2e-14), supply=supply, boost=boost)
    check('edge_decreases_at_fixed_settled_mass', row['edges']['2.0'] < row['edges']['1.0'], supply=supply)
    edges.append(row)

for r in (0.2, 0.5, 1.0, 3.0, 10.0, 100.0):
    check('mass_derivative', math.isclose(derivative(m0,r),m0_prime(r),rel_tol=1e-8), r=r)
    speed = -r*r*(-math.expm1(-1/r))  # dot(B)/B = 1
    check('source_free_enclosed_continuity', math.isclose(-speed*m0_prime(r),m0(r),rel_tol=3e-14), r=r)

flux_rows = []
for fill in (0.2, 0.5, 0.8):
    j0 = math.sqrt(fill)*(1-fill)
    def flux_from_fields(r):
        density = fill/(4*math.pi*r*r)
        tau = r/math.sqrt(fill)
        deficit_mass = (1-fill)*(r-1)
        drift = -tau*deficit_mass/(r*r)
        return -4*math.pi*r*r*density*drift
    for r in (2.0,5.0,10.0,50.0,100.0):
        growth = j0/(r*r)
        numeric = derivative(flux_from_fields,r)
        homogeneous = j0/r
        check('flux_from_poisson_and_continuity', math.isclose(numeric,growth,rel_tol=3e-8), fill=fill,r=r)
        check('finite_core_flux', math.isclose(flux_from_fields(r),j0*(1-1/r),rel_tol=2e-14), fill=fill,r=r)
        check('homogeneous_clock_negative_control', not math.isclose(numeric,homogeneous,rel_tol=.01), fill=fill,r=r)
        # Exact integral of the analytic growth across [1,r].
        check('annular_mass_balance', math.isclose(j0*(1-1/r),flux_from_fields(r)-flux_from_fields(1),rel_tol=2e-14), fill=fill,r=r)
        flux_rows.append(dict(fill=fill,r_over_core=r,flux=flux_from_fields(r),growth=growth,homogeneous_growth=homogeneous,suppression=growth/homogeneous))

result = dict(
    verdict='PASS' if all(c['passed'] for c in checks) else 'FAIL',
    check_count=len(checks), passed=sum(c['passed'] for c in checks),
    edge_examples=edges, flux_examples=flux_rows, checks=checks,
    limits=['Finite floating-point checks supplement analytic proofs.',
            'Not a halo evolution simulation, data fit, or universal physical theorem.',
            'The full-law core is idealized; fill is uniform only at the evaluated instant.'])
out = pathlib.Path(sys.argv[1])
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('verdict','check_count','passed')}))
sys.exit(0 if result['verdict']=='PASS' else 1)
