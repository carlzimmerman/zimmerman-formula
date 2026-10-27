"""Independent isotropic Burkert Eddington inversion; no repository imports."""
import json
import sys
from pathlib import Path
import mpmath as m

m.mp.dps = 35
p = m.pi
rho = lambda r: 1 / ((1+r)*(1+r*r))


def rp(r):
    return -rho(r)*(1/(1+r)+2*r/(1+r*r))


def rpp(r):
    a = 1/(1+r)+2*r/(1+r*r)
    ap = -1/(1+r)**2+2*(1-r*r)/(1+r*r)**2
    return rho(r)*(a*a-ap)


def mass(r):
    return p*(2*m.log1p(r)+m.log1p(r*r)-2*m.atan(r))


def delta_psi(r):
    return 2*p*((1+1/r)*(m.atan(r)-m.log1p(r))
                +(1-1/r)*m.log1p(r*r)/2)


def rho_psipsi(r):
    a = -mass(r)/r**2
    b = -4*p*rho(r)+2*mass(r)/r**3
    return (rpp(r)*a-rp(r)*b)/a**3


coef = m.sqrt(3)/(8*p**m.mpf('2.5'))
rows = []
for re in map(m.mpf, ['.01', '.001', '.0001']):
    eps = delta_psi(re)

    def integrand(s):
        if abs(s) < m.mpf('1e-11'):
            return rho_psipsi(re)*m.sqrt(2*mass(re)/re)
        r = re*m.cosh(s)
        return (rho_psipsi(r)*mass(r)/r**2*re*m.sinh(s)
                / m.sqrt(delta_psi(r)-eps))

    f = m.quad(integrand, [0, 1, 3, 6, 12, 24, 48])/(m.sqrt(8)*p*p)
    rows.append({"turning_radius": str(re), "f": str(f),
                 "epsilon": str(eps), "epsilon_f_over_coefficient": str(eps*f/coef)})

sigma2 = m.quad(lambda r: rho(r)*mass(r)/r**2,
                [m.mpf('1e-10'), 1, 10, 100, m.inf])
checks = {
    "leading_coefficient": all(abs(m.mpf(r['epsilon_f_over_coefficient'])-1) < m.mpf('.001')
                               for r in rows),
    "coefficient_convergence": all(abs(m.mpf(rows[i+1]['epsilon_f_over_coefficient'])-1)
                                   < abs(m.mpf(rows[i]['epsilon_f_over_coefficient'])-1)
                                   for i in range(2)),
    "finite_positive_second_moment": bool(m.isfinite(sigma2) and sigma2 > 0),
}
result = {"units": "G=rho0=r0=1", "decimal_precision": m.mp.dps,
          "asymptotic_coefficient": str(coef), "rows": rows,
          "sigma0_squared": str(sigma2), "central_Q": str(sigma2**m.mpf('-1.5')),
          "checks": checks,
          "non_claims": ["Three finite values are not the proof of divergence; the local asymptotic derivation supplies that",
                         "No distribution-function certificate for a hard-truncated halo",
                         "No cosmological assembly or full mixing-function calculation"]}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
assert all(checks.values())
