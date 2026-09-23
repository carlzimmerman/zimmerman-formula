"""Exact angular audit; does not numerically test the stopped transport process."""
import json
from pathlib import Path
import sympy as s

mu, phi, r2, z = s.symbols('mu phi r2 z', real=True)
q = s.Rational
thomson = q(3, 8) * (1 + mu**2)  # density with respect to dmu
isotropic = q(1, 2)
# Azimuthal average of [sqrt(r2-z^2)*sqrt(1-mu^2)*cos(phi)+z*(mu-1)]^2.
# E_phi cos(phi)=0, E_phi cos(phi)^2=1/2.
cos1 = s.integrate(s.cos(phi), (phi, 0, 2*s.pi))/(2*s.pi)
cos2 = s.integrate(s.cos(phi)**2, (phi, 0, 2*s.pi))/(2*s.pi)
jump_phi = (r2-z**2)*(1-mu**2)*cos2 + z**2*(mu-1)**2

def angular(p):
    return s.expand(s.integrate(p*jump_phi, (mu, -1, 1)))

derived = angular(thomson)
iso = angular(isotropic)
claimed = q(3, 8)*(r2+z**2)
# Independent orientations integrate the original angular expression over phi,mu.
perp = s.integrate(q(3,16)/s.pi*(1+mu**2)*(1-mu**2)*s.cos(phi)**2,
                   (phi,0,2*s.pi),(mu,-1,1))
parallel = s.integrate(thomson*(mu-1)**2,(mu,-1,1))
checks = {
    'azimuth_cross_term_zero': cos1 == 0,
    'thomson_normalized': s.integrate(thomson,(mu,-1,1)) == 1,
    'isotropic_normalized': s.integrate(isotropic,(mu,-1,1)) == 1,
    'mean_outgoing_longitudinal_zero': s.integrate(mu*thomson,(mu,-1,1)) == 0,
    'thomson_second_moment': s.integrate(mu**2*thomson,(mu,-1,1)) == q(2,5),
    'thomson_polynomial': s.expand(derived-q(3,10)*r2-q(11,10)*z**2) == 0,
    'perpendicular_orientation': perp == derived.subs({r2:1,z:0}),
    'parallel_orientation': parallel == derived.subs({r2:1,z:1}),
    'isotropic_polynomial': s.expand(iso-r2/3-z**2) == 0,
    'same_thomson_residual_fails_isotropic': s.expand(iso-derived) != 0,
    'qwen_claim_fails_perpendicular': (derived-claimed).subs({r2:1,z:0}) != 0,
    'qwen_claim_fails_parallel': (derived-claimed).subs({r2:1,z:1}) != 0,
}
result = {
    'claim': 'Exact angular integral refutes a=b=3/8; no transport or novelty claim',
    'thomson_jump_square': str(derived),
    'martingale_bracket_integrand_divided_by_kappa': str(4*derived),
    'isotropic_jump_square': str(iso),
    'qwen_residual_perpendicular': str((derived-claimed).subs({r2:1,z:0})),
    'qwen_residual_parallel': str((derived-claimed).subs({r2:1,z:1})),
    'checks': {key: bool(value) for key,value in checks.items()},
}
Path('real_research/reviews/jwst_martingale_audit_2026_09_22/certified_v2/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
