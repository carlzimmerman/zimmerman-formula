# Expansion limits coherent conversion: exact bound and resonance passage

The new exact result is a finite, uniform-in-wave-number energy-gain
bound for transverse carrier perturbations about the actual self-gravitating
homogeneous pump. The bounded calculation also finds that peak conversion
growth faster than Hubble expansion does not guarantee net physical energy
growth during resonance passage. Neither result establishes spatial clearing.
Work is frozen after the single completed run below, as requested.

## Exact same-action transverse subsystem

Use the PQ action and the expanding compact-flat-FLRW branch proved in
[HOMOGENEOUS_FRW.md](../../common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md).
Take `chi=s=0`, with the two-real-field pump `phi` evolving, `M,m,mu,V0>0`,
bare `Lambda=0`, and `gamma` finite. Write `Psi=(phi1+i phi2)/sqrt(2)`.
The background solves

```
phi''+3H phi'+M^2 phi=0,
E=(|phi'|^2+M^2|phi|^2)/2,
3 Mpl^2 H^2=E+V0,  H'=-|phi'|^2/(2 Mpl^2),  a'=Ha.
```

Because the background `chi,s` and their velocities vanish, transverse
`(chi,s)` perturbations have zero first-order stress, density and projected
auxiliary source. Setting the metric/auxiliary perturbations to zero is
therefore consistent at first order. It does not discard their second-order
backreaction. For comoving wave number `k`, `p=k/a`, the exact linear equations are

```
chi''+3H chi'+(p^2+m^2)chi+gamma m^2 s phi=0,
s''+3H s'+(p^2+mu^2+gamma^2 m^2|phi|^2)s+gamma m^2 phi·chi=0.
```

They are derived from the same positive-square potential, including its
quartic term. No dissipative conversion rate is inserted.

The final [CA5-GNC-R action](../vacuum/ACTION.md) has exactly this same
homogeneous pump and transverse linear subsystem. Its replacement vacuum
term is `-V0 F(t)`, with `F(1)=1`; the excitation coupling at `t=1` is
unchanged. First-order transverse stress and auxiliary-source variations
still vanish, so zero metric/auxiliary perturbations remain consistent.
Consequently the equations, analytic bounds and existing finite calculation
apply to this restricted CA5-GNC-R sector without rerunning an unchanged
ODE. This does not identify the two actions outside that sector.

## Uniform finite gain: analytic proof

For `y=(chi,s)`, define the positive physical mode energy

```
e=|y'|^2/2+p^2|y|^2/2+m^2|chi+gamma s phi|^2/2+mu^2 s^2/2.
```

Direct differentiation gives the exact identity

```
e'=-3H|y'|^2-Hp^2|y|^2
   +gamma m^2 s(chi+gamma s phi)·phi'.
```

For `q=chi+gamma s phi`, Young's inequality gives
`m mu |s||q| <= (m^2|q|^2+mu^2s^2)/2 <= e`. Consequently

```
e' <= (|gamma|m/mu)|phi'| e,
e(T) <= e(0) exp[(|gamma|m/mu) integral_0^T |phi'| d tau].
```

This bound is independent of `k`; it also applies after summing a
finite-energy Fourier expansion. It is generally a loose upper bound,
not a calibrated conversion efficiency.

The pump supplies a finite total logarithmic gain budget. Put
`Hmin=sqrt[V0/(3 Mpl^2)]`, `epsilon=min(Hmin,M/2)>0`, and

```
L=E+epsilon phi·phi'+(3epsilon/2)H|phi|^2,
Cminus=1-epsilon/M>0,
Cplus=1+epsilon/M+3epsilon H(0)/M^2.
```

Then `Cminus E <= L <= Cplus E`, and direct differentiation yields

```
L'=-(3H-epsilon)|phi'|^2
   -epsilon(M^2-3H'/2)|phi|^2 <= -2epsilon E.
```

Using `H>=Hmin`, `H'<=0` and `H<=H(0)` therefore gives, with
`beta=2epsilon/Cplus`,

```
E(tau) <= (Cplus/Cminus) E(0) exp(-beta tau),
integral_0^infinity |phi'| d tau
  <= (2/beta) sqrt[2 Cplus E(0)/Cminus] < infinity.
```

Thus the linear transverse energy gain is bounded for all future time
and all wave numbers on this branch. This excludes extrapolating an eternal
constant-amplitude-pump Floquet instability to this expanding solution.
It permits large but finite transient amplification. Positive `mu` is
needed in the work bound and positive `V0` in the strict Hubble floor;
the statement does not cover the earlier massless slow-wave witness.
It is not a nonlinear stability theorem for the full gravitational action.

## Resonance passage and its assumptions

The exact rescaling `X=a^(3/2)y` gives
`X''+[Kphysical-d I]X=0`, where `d=3H'/2+9H^2/4`. Its fundamental
matrix is symplectic. Only the following interpretation uses adiabatic
approximations: an underdamped rotating pump
`Psi approximately A0 a^(-3/2) exp(-i M tau)` with slowly varying frequencies,
weak mixing and `|omega'|/omega^2 << 1`. Put

```
h=gamma m^2 |Psi|,
omegaChi approximately sqrt(m^2+p^2),
omegaS approximately sqrt(mu^2+p^2+2h^2/m^2),
delta=M-omegaChi-omegaS,
sigma0=|h|/(2 sqrt(omegaChi omegaS)).
```

Under those derivative assumptions, `p'=-Hp`, `h' approximately -3Hh/2`
imply

```
delta' approximately H[p^2(1/omegaChi+1/omegaS)+3h^2/(m^2 omegaS)] > 0.
```

For a locally linear detuning sweep with nearly constant coupling, the
integrated unstable-amplitude exponent is

```
S = integral sqrt(sigma0^2-delta^2/4)_+ d tau
  approximately pi sigma0^2/|delta'|.
```

The last integral follows by the elementary semicircle area, not by assuming
a stochastic decay law. `S` is not exactly the coherent transfer-matrix
norm: matching across the band and the input phase also matter. In
particular `sigma0/H>1` alone does not fix passage gain. Failure of the
adiabatic assumptions invalidates these estimates, but not the exact
mode equations or energy identity above.

## Discriminating completed calculation

[check.py](check.py), under [contract.json](contract.json), evolves the
nonlinear Einstein pump and two exact transverse propagators simultaneously:
the given coupling and a zero-coupling control. It does not evolve finite
amplitude pump depletion. Parameters are
`M=3,m=1,mu=.5,gamma=.2,V0=.01,|Psi(0)|=1,k=1.6,a:1->2`.
The two choices `Mpl=100,1000` change expansion relative to the field masses;
neither is an observational fit. The initial radial pump velocity is
`-3H phi/2`, and its initial Friedmann constraint is solved exactly.

| Quantity | Mpl=100 | Mpl=1000 |
| --- | ---: | ---: |
| Initial H | .0245026 | .00245017 |
| Time to a=2 | 49.7084 | 497.091 |
| Peak sigma0/H at crossing | 2.72860 | 27.2865 |
| Integrated adiabatic-band exponent S | .183417 | 1.83420 |
| Maximum exact physical energy ratio e_final/e_initial | .298625 | 14.7429 |
| Maximum specified rescaled action-norm ratio | 3.86888 | 184.273 |
| Uncoupled action-norm ratio | 1.00601 | 1.00042 |

The action norm is explicitly
`I=(sum omega_i X_i^2+X_i'^2/omega_i)/2`, with uncoupled
`omega=(sqrt(m^2+p^2),sqrt(m^2+p^2),sqrt(mu^2+p^2))` at each endpoint.
Its maximum ratio is the largest eigenvalue of the weighted exact propagator;
it is not a physical clearing fraction. The physical energy ratio instead
uses the full positive energy `e`, including mixing and the Hubble cross
term from rescaling. The faster-expanding test has net physical-energy
decrease for every transverse initial vector over this tested interval,
despite peak growth exceeding `H`. Slower expansion permits substantial
linear gain. Neither conclusion extrapolates to arbitrary parameters.

The maximum background Friedmann error relative to initial density is
`7.59e-9`, comoving pump-charge error `2.65e-8`, and transverse symplectic
error `5.69e-9`. Zero coupling produces exactly no light-field charge from
a neutral seed. Charge gained by `chi` in the coupled linear calculation
is a quadratic response coefficient; an actual seed multiplies it by its
squared amplitude. Conservation requires the corresponding second-order
pump depletion, which is not simulated here.

## Dilution, flux and the remaining clearing question

The full simultaneous U(1) current obeys, in this FLRW chart,
`partial_tau(a^3 j^0)+a^2 partial_i jhat^i=0`. Thus a fixed comoving
region changes total charge only through boundary flux. Homogeneous
physical density dilution does not clear comoving charge.

The exact characteristic speed on the homogeneous branch is one, giving
the causal comoving travel bound
`Delta x <= integral d tau/a <= 1/[a(t0)Hmin]`. A narrower, conditional
bound for a freely propagating adiabatic massive wave-packet center is

```
a(t0) Delta x <= [sqrt(m^2+p0^2)-m]/(Hmin p0)
              = p0/[Hmin(sqrt(m^2+p0^2)+m)].
```

It follows from `H>=Hmin`, conserved comoving momentum and
`v_group=p/sqrt(m^2+p^2)`. For slow packets it is approximately
`v0/(2Hmin)`. This is a group-ray statement, not an exact bound on arbitrary
field tails, and assumes no later interaction changes the momentum or
dispersion. No spatial packet or outward flux is computed in this checkpoint.

## Evidence and limitations

[run_001/manifest.json](run_001/manifest.json) validates with `--root`:
26 exact/finite checks, exit zero, runtime 2.071341 seconds, 120-second wall
and 110-second per-process CPU limits, cooperative thread cap one. No
memory/affinity limit is claimed. There were no failed runs in this new lane.
The shared dirty checkout was at `fef4cfd8b49fdd8617b7efb15bf960140bff1891`.

- Source SHA-256: `c15a5aa585d32c42992f77c48f81330e571c5d1624e52d4ffaaf693ad8585393`.
- Result SHA-256: `f964f0a1a84cd3e406a38841ded4fcd5180546b00e0b5544645faa888878fa44`.

The infinite-time energy bound is the analytic argument above, not a
conclusion inferred from a finite integration. It is not Lean-formalized.
No empirical transport efficiency, new particle population, cosmological
abundance, nonlinear depletion, host-mode health, or spatial evacuation
is established. The constructive result is a precise restricted gain bound
and a demonstrated dependence of conversion on the duration of resonance
passage.
