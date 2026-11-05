"""Discrete sphere check of the local curved nodal-band heat coefficient."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as sy

ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True)
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
mp.mp.dps = 80
checks = {}

def check(name, condition):
    ok = bool(condition)
    checks[name] = ok
    print(('PASS ' if ok else 'FAIL ')+name, flush=True)

s, M, k, r = sy.symbols('s M k r', positive=True)
ell, lam = sy.symbols('ell lambda', real=True)
f = sy.exp(-s*(lam-k*k)**2/(4*M*M))
g = (2*ell+1)*f.subs(lam, ell*(ell+1)/r**2)
em_constant = sy.limit(g.subs(ell,0)/2-sy.diff(g,ell).subs(ell,0)/12,r,sy.oo)
check('Euler Maclaurin curvature constant', sy.simplify(em_constant-f.subs(lam,0)/3)==0)
B, z = sy.symbols('B z', positive=True)
J = (B+z)*sy.log(1+z/B)-z
check('curvature mass remainder has zero constant', J.subs(z,0)==0)
check('curvature mass remainder has zero quadratic mass coefficient',
      sy.diff(J,z).subs(z,0)==0)
check('curvature mass remainder is analytic with quartic leading mass',
      sy.simplify(sy.diff(J,z,2)-1/(B+z))==0)
check('curvature mass expansion',
      sy.simplify(sy.series(J,z,0,4).removeO()-z*z/(2*B)+z**3/(6*B*B))==0)
d,v,delta = sy.symbols('d v Delta',positive=True)
flat_nonanalytic = d*M/(2*v*(4*sy.pi)**sy.Rational(3,2))*sy.gamma(-sy.Rational(3,2))*delta**3
check('flat nodal cubic coefficient',sy.simplify(flat_nonanalytic-d*M*delta**3/(12*sy.pi*v))==0)

fixtures = []
for proper in [mp.mpf(1)/4,mp.mpf(1),mp.mpf(4)]:
    true_target = mp.exp(-proper/4)/3
    used_target = mp.mpf(1)/3 if args.mutate else true_target
    errors = []
    estimates = []
    all_tails = True
    all_monotone = True
    for radius in [20,40,80]:
        # q=(lambda-1)/2; ensure q^2*s exceeds 200 at truncation.
        lambda_cut = 1+2*mp.sqrt(200/proper)
        last = int(mp.ceil(radius*mp.sqrt(lambda_cut)))+5
        qlast = (mp.mpf(last)*(last+1)/radius**2-1)/2
        monotone = (2*last+1)**2*proper*qlast/radius**2 > 2
        all_monotone = all_monotone and monotone
        total = mp.fsum((2*j+1)*mp.exp(-proper*((mp.mpf(j)*(j+1)/radius**2-1)/2)**2)
                       for j in range(last+1))
        area = radius**2*mp.sqrt(mp.pi/proper)*(1+mp.erf(mp.sqrt(proper)/2))
        estimate = total-area
        # Since g is decreasing after last, sum_{j>last}g(j)<=integral_last^infinity g.
        tail = radius**2*mp.sqrt(mp.pi/proper)*mp.erfc(qlast*mp.sqrt(proper))
        all_tails = all_tails and tail < mp.mpf('1e-60')
        err = abs(estimate-true_target)
        errors.append(err)
        estimates.append(estimate)
        fixtures.append({'proper_time':str(proper),'radius':radius,'last_index':last,
                         'curvature_constant':mp.nstr(estimate,45),
                         'analytic_constant':mp.nstr(true_target,45),
                         'absolute_error':mp.nstr(err,20),'tail_bound':mp.nstr(tail,12),
                         'tail_monotonicity_verified':bool(monotone)})
    tag='s='+str(proper)
    check(tag+' controlled omitted tails',all_monotone and all_tails)
    ratios=[errors[j]/errors[j+1] for j in range(2)]
    check(tag+' radius convergence order',all(mp.mpf('3.5')<a<mp.mpf('4.5') for a in ratios))
    check(tag+' band endpoint curvature match',abs(estimates[-1]-used_target)/abs(used_target)<mp.mpf('1e-3'))

result={'passed':all(checks.values()),'checks':checks,
        'mode':'replace_band_endpoint_by_node' if args.mutate else 'main',
        'precision_decimal_digits':80,'fixtures':fixtures,
        'scope':'Large radius curvature coefficient for specified scalar-pseudospin '
                'band operator; not finite radius gapless matching or full gravitational dynamics.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True)
Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['passed'] else 1)
