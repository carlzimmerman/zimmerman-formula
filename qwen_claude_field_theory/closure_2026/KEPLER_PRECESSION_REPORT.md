# Kepler-like prediction from the exact exponential MOND law

For a spherical point source, define `x=g/a0` and
`r_M=sqrt(G M/a0)`.  The exact constitutive equation is

```text
x (1-exp(-x)) = (r_M/r)^2.
```

For a circular orbit `Omega^2=g/r`.  Differentiating the same force law,
without fitting a potential, gives

```text
A(x) = d ln(mu g)/d ln g = 1 + x/(exp(x)-1),
kappa^2/Omega^2 = 3 - 2/A(x),
Delta-varpi = 2 pi [1/sqrt(3-2/A(x)) - 1].
```

Thus the framework predicts a universal retrograde apsidal shift when plotted
against `r/r_M`: it tends to zero in the Newtonian limit and to
`2 pi (1/sqrt(2)-1) = -105.44 degrees` per radial cycle in the deep-MOND limit.  At
`r=r_M` the exact law predicts a finite transition value computed by the
script.  The period ratio at fixed `M,r` is independently
`P/P_Newton=sqrt(mu(x))`.

This is a new repository prediction, not a claim of global literature
priority.  It is distinct from the BTFR: it concerns orbital shape and
precession, and its mass dependence enters only through the derived
`r_M=sqrt(GM/a0)`.  A relativistic completion must reproduce this static
limit; any slip, preferred-frame correction, or clock-sector force would give
an additional deviation that must be derived rather than hidden.

Reproduction:

```bash
python3 kepler_precession_prediction_2026.py       # exit 0
python3 -m unittest -v test_kepler_precession_prediction_2026.py  # 1 test, exit 0
python3 run_kepler_transition_lean.py                 # exit 0 (warnings only)
```

`KeplerTransitionFormal.lean` certifies the circular-frequency ratio,
the period ratio, and the epicyclic-frequency identity from the spherical
field equation; it does not certify the existence of a relativistic completion.
