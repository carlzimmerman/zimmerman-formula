"""Test first: an outgoing circular boundary must carry positive K flux."""
import cmath

def outgoing_ratio(p,h):
    return 1.0  # Unimplemented boundary: no outgoing phase.

rho=outgoing_ratio(.6,.1)
assert abs(rho-cmath.exp(-.06j))<1e-13, 'Missing outgoing phase in the boundary ghost ratio'
assert rho.imag<0, 'An outgoing +iOmega t phasor must have positive outward K flux'
