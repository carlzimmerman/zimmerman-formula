# Exact-exponential scale lock

Assume one acceleration scale, the dark-energy acceleration
`a_Lambda = c sqrt(G rho_DE)`, and the exact required constitutive law

```text
mu(u) = 1 - exp(-u),   u = g/a_Lambda.
```

Its deep-MOND slope is exactly one.  Rewriting the same law as a target
function of `g/a0` gives the physical slope `1/a0`; equality of the two laws
near the origin therefore forces `a0=a_Lambda` and

```text
kappa = a0/a_Lambda = 1.
```

The desired `kappa=1/2` requires a slope ratio two, equivalently
`mu(u)=1-exp(-2u)` or an inserted factor of two in the argument.  That is a
different kernel/normalisation and does not preserve the exact target
`mu(y)=1-exp(-y)` with `y=g/a0`.

The L231 alternative `mu=1-(1+u)^(-2)` also has slope two and is a viable
curve-level consistency check, but it is not the required exponential and its
integer choice is not derived.  It cannot close the original action problem.

This closes the exact-exponential coefficient loophole under the stated
one-scale, exact-law assumptions.  It does not close the separate relativistic
DOF, lensing, PPN, matter-Ward, FLRW, and stability gates.

## Reproduction

```bash
python3 exact_exponential_scale_lock.py
python3 -m unittest discover -s . -p 'test_*.py'
python3 run_exact_exponential_scale_lock_lean.py
```
