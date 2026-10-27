"""Reconstruct mixed responses from energy and a deleted-force control."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
a = p.parse_args()


def energy(b, t, f):
    return -((b+t+f)**2-t*t)/2


def derivative(fun, x):
    # All differentiated functions here are at most quadratic.
    return (fun(x+1)-fun(x-1))/2


def force_t(b, t, f, delete=False):
    # The control removes only the f -> t contribution, directly in its force.
    return derivative(lambda u: energy(b, u, F(0) if delete else f), t)


def force_f(b, t, f):
    return derivative(lambda u: energy(b, t, u), f)


rows = []
for b, t, f in [(F(2),F(3),F(5)),(F(1,2),F(2,3),F(4,5)),(F(0),F(1),F(0))]:
    forward = derivative(lambda v: force_t(b,t,v), f)
    reverse = derivative(lambda u: force_f(b,u,f), t)
    deleted = derivative(lambda v: force_t(b,t,v,True), f)
    assert forward == reverse == -1
    assert deleted == 0 and deleted != reverse
    rows.append({'point':list(map(str,(b,t,f))), 'mixed_t_f':str(forward),
                 'mixed_f_t':str(reverse),'deleted_f_to_t':str(deleted)})

def kernel(r, s):
    return -F(1,max(r,s))

# Independent four-corner pair energy of two zero-mass shell displacements.
coefficient = sum((qt*qf*kernel(rt,rf)
                   for rt,qt in [(1,F(-1)),(3,F(1))]
                   for rf,qf in [(2,F(-1)),(4,F(1))]), F(0))
assert coefficient == -F(1,6)

result = {'status':'completed','assertion_tested':
          'Mixed derivatives independently reconstructed from quadratic energy; '
          'one-way force deletion fails reciprocity at all 3 rational fixtures; '
          'zero-mass shell pair energy independently reconstructed.',
          'rows':rows,'shell_cross_coefficient':str(coefficient),
          'non_claims':['No physical or finite-halo construction is tested']}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
print('3 derived mixed-variation controls and 1 shell pair-energy control pass')
