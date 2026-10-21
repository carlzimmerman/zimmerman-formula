# Exact full-remainder shell result; warm target remains open

The full canonical remainder preserves the positive coherent radial-shell
energy. Direct separate Lagrangian displacements give

```
xi_t_ddot + kappa_t0^2 xi_t + G F'/r^2 (xi_t-xi_f)=0,
xi_f_ddot + kappa_f0^2 xi_f + G T'/r^2 (xi_f-xi_t)=0,

kappa_t0^2=G(B+F)/r^3+G B'/r^2+[2uR'-3R]/r,
kappa_f0^2=G(B+T+F)/r^3+G B'/r^2,
2uR'-3R=u^2(a0+u)/(a0-u)^2>=0.
```

The reciprocal quadratic is the two positive diagonal terms plus
`G T' F'(xi_t-xi_f)^2/r^2`. Finite smooth hollow supports with
`B>=B_*>0` and a uniform gap below saturation give a bounded positive
self-adjoint linear operator and conserved energy controlling weighted
radial displacement and velocity for all times in this coherent linear
system.

A new explicit finite smooth family carries the **exact full canonical
ordinary-tracer law** on any chosen compact annulus: taper the target
`C(r)=r^2 u_b(GB/r^2)/G` to a cumulative mass `M<=C`, retaining `M=C`
on the annulus, and set `T=fM`, `F=(1-f)M`, `0<f<1`. Monotonicity of C
when B'>=0 makes the taper positive. The full R supplies both a uniform
gap `u_t<f a0` and strictly positive circular angular momenta. All counted
cold energies are finite; there is no reflecting wall or infinite stock.

Two additional exact leaves make a future warm continuation more concrete:

- For `f<=(3-sqrt(5))/2`, circular angular momentum is strictly increasing
  and frozen-field circular radii are locally radially stable; the same
  bound gives a positive fixed-angular-momentum splitting second variation.
- For `f<1/sqrt(2)`, circular specific orbital energies are uniformly below
  escape. On support r<=R, `E_ct<=-G(1/2-f^2)B_*/R` and
  `E_cf<=-G B_*/(2R)`. The explicit f=1/64 satisfies both conditions.

These are analytic statements, with no scientific numerical run or sampled
theorem claim. The phase-space equilibria are singular circular measures:
zero radial dispersion, finite tangential kinetic support. No smooth warm
inverse construction, nonlinear all-time evolution, shell-crossing control,
nonspherical stability or original-theory closure is proved. The imposed
annulus normalization, fraction and finite support are not selected by
formation. Kappa, a0, physical abundance, finite stiffness and relativity
remain outside this result.

Full derivation: `FULL_REMAINDER_SHELL.md`. Exact source hashes and checkpoint:
`SOURCE_PINS.json`; author artifact hashes and source-change observations:
`PROVENANCE.json`. Independent actual-file review is recorded separately
by the capture_dynamics agent. The next step is a controlled positive smooth
phase-space continuation with finite radial width at fixed escape gap,
self-consistency and a stability argument. It has not been executed here.
