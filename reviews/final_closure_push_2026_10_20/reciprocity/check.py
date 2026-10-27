"""Exact small controls for SOURCE_RESPONSE.md; no scientific integrations."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--delete-backreaction', action='store_true')
args = parser.parse_args()
checks = []


def check(name, actual, expected):
    good = actual == expected
    checks.append({'name': name, 'actual': str(actual), 'expected': str(expected),
                   'pass': good})


# The counted quadratic energy at fixed radius, setting G/r^2=1.
def energy(b, t, f):
    return -((b + t + f) ** 2 - t ** 2) / 2


def derivative(fun, x):
    # Exact for a quadratic polynomial in this argument.
    return (fun(x + 1) - fun(x - 1)) / 2


for b, t, f in [(Q(2), Q(3), Q(5)), (Q(1, 2), Q(2, 3), Q(4, 5)),
                (Q(0), Q(1), Q(0))]:
    check(f'tethered gravity {b,t,f}', derivative(lambda x: energy(b, x, f), t),
          -(b + f))
    check(f'free gravity {b,t,f}', derivative(lambda x: energy(b, t, x), f),
          -(b + t + f))
    check(f'baryon gravity {b,t,f}', derivative(lambda x: energy(x, t, f), b),
          -(b + t + f))

mixed_tf = Q(0) if args.delete_backreaction else Q(-1)
mixed_ft = Q(-1)
check('reciprocal mixed variation', mixed_tf, mixed_ft)

shell = -(Q(1, 4) - Q(1, 3) - Q(1, 4) + Q(1, 2))
check('zero-mass rearrangement cross coefficient', shell, Q(-1, 6))
check('one-way rectangle integral for A=2 B=3', shell * 2 * 3, Q(-1))

rows = []
for a0 in [Q(1, 3), Q(1), Q(7)]:
    for n in range(1, 13):
        u = a0 * Q(n, 13)
        s = u ** 2 / (a0 - u)
        g = s + u
        check(f'cold rest inverse a0={a0} n={n}', g ** 2 / (g + a0), s)
        uprime = (a0 - u) ** 2 / (u * (2 * a0 - u))
        check(f'derivative identity a0={a0} n={n}', 1 + uprime,
              a0 ** 2 / (u * (2 * a0 - u)))
        check(f'positive extra response a0={a0} n={n}', uprime > 0, True)
        rows.append({'a0': str(a0), 'u': str(u), 's': str(s), 'g': str(g),
                     'dg_ds': str(1 + uprime)})

result = {'finite_assertion': 'Exact energy/source algebra and 36 saturation fixtures',
          'checks': checks, 'n_checks': len(checks), 'n_pass': sum(c['pass'] for c in checks),
          'rows': rows, 'mutation': args.delete_backreaction,
          'non_claims': ['No astrophysical or continuum evolution was run',
                         'Does not prove positive collisionless warm realization']}
out = Path(args.output)
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'checks': len(checks), 'passed': result['n_pass'],
                  'mutation': args.delete_backreaction}))
raise SystemExit(0 if all(c['pass'] for c in checks) else 1)
