# Natural second-harmonic energy loss at zero net intrinsic spin

**The same finite-fragment action has a natural scalar outlet for a standing
quadrupole's energy with zero net intrinsic angular momentum.** On the
finest tested grid the leading coefficients are
`gamma=1.83105331454e-5` at Q=80000 and `1.44104501034e-5` at Q=160000.
The Q=160000 coefficient is about 85.9 times the pure-chiral coefficient,
because a large monopole second harmonic is now present. This is a
specified weak-mode radiation calculation, not a merger capture or
excitation measurement.

`standing_run_001/manifest.json` is **completed** and validates against
current inputs. All 172 checks pass. Numerical runtime was 0.218 seconds;
runner wall time was 1.203 seconds and measured RSS was 84,066,304 bytes.
The runner requested one numerical thread, a 90-second CPU cap and a
120-second wall cap. The `nice -n 10` wrapper reported that it could not
adjust priority; execution nevertheless completed and passed the resource
gate. No hard virtual-address-space cap is claimed.

## Angular source and mode normalization

Use the exact cached normalized radial mode Z and the no-half convention

```
z1 = A [Z H exp(+iOmega t) + c.c.]/r,
H = (Y22+Y2,-2)/sqrt(2),
integral |H|^2 dOmega = 1.
```

The real standing H has zero integrated intrinsic-J factor. Its exact square
is

```
H^2 = (C44/2)(Y44+Y4,-4) + C0 Y00 + C2 Y20 + C4 Y40,
C44 = sqrt(5/(14pi)),
C0  = 1/sqrt(4pi),
C2  = -sqrt(5)/(7sqrt(pi)),
C4  = 1/(14sqrt(pi)).
```

The coefficients were checked independently with deterministic 64-by-64
angular quadrature and pointwise reconstruction; changing the sign of C2 is
a detected negative control. Each second-harmonic radial force is
`-C_lm r N2(Z/r)` using the same action-derived five-component quadratic
polynomial as the chiral calculation, without conjugating its quadratic
products. The zero-frequency deformation is not part of this outgoing
coefficient.

The standing mode has the same `K=A^2` normalization as the chiral mode:
its apparent oscillating cross-energy term is proportional to

```
Z^T (W-Omega^2 I) Z = -iOmega Z^T G Z = 0
```

because G is skew. The finite eigenvector control checks this identity as
well as unit K, matching background fields and the recomputed quadratic
source. There is no extra factor of two from using a real angular pattern.

## New computation and reuse of existing evidence

The contract declares Q=80000/160000 and grids
`(L,N)=(40,399),(60,599),(60,1199)`. Only the newly needed ell=0 and ell=2
responses were solved, along with their half-parent-amplitude controls.
The exact matched ell=4 result from `radiation_run_002` was reused by linear
source scaling; its original source/work and normalization controls remain
pinned inputs. No prior outgoing experiment was duplicated.

For each row, the two ell=4 chiral forces are one half the old force, so
their powers are one quarter each and their J fluxes cancel. The ell=4,m=0
force has factor `C4/C44`, hence power `gamma4/70`. Thus the reused ell=4
total is `(18/35) gamma4`. The ell=0 and ell=2 coefficients must be computed
with their own radial operators; angular weights alone do not determine
their powers. Spherical-harmonic orthogonality removes interference between
the distinct outgoing angular sectors in integrated fluxes.

| Q | Finest total gamma | / pure-chiral gamma | ell=0 share | ell=2 share | ell=4 share | Unit-K half-time, 1/m |
|---:|---:|---:|---:|---:|---:|---:|
| 80000 | 1.83105331454e-5 | 4.81812345 | 88.9351% | 0.39094% | 10.67398% | 54613.3743 |
| 160000 | 1.44104501034e-5 | 85.91282043 | 99.32735% | 0.07403% | 0.59861% | 69394.0850 |

Only the positive-Psi vacuum sideband is open. The summed edge power agrees
with source work; the new responses also pass the linear residual and
fourth-power amplitude controls. Net outgoing intrinsic J is zero, whereas
positive charge and laboratory energy leave. The same ledger as in
`MERGER_LEDGER.md` remains mandatory:

```
Eout/Qout = omega+2Omega,
Kout/Qout = 2Omega,
Qremdot = -Qoutdot.
```

Finite box changes in total gamma are 0.3552% (Q80000) and 0.00270%
(Q160000); mesh changes are 0.0592% and 0.0402%, below the declared 5%
gate. These tests are not an interval-certified continuum error bound or a
search for every resonance.

## Consequence for the merger ledger and remaining limits

This closes one kinematic restriction of a sole fully chiral outlet:
the action's quadratic self-source can emit excitation energy at zero net
spin. A low-spin encounter therefore need not export the large intrinsic J
that would accompany putting its entire energy into one m=+2 mode. The
standing pattern carries no initial net spin, and its m=+4/-4 outgoing
components cancel rather than borrowing angular momentum from nowhere.
An actual nonzero merger orbital J still requires a chiral or other torque
outlet; this standing result does not export it by itself.

The leading weak adiabatic law is `dK/dt=-gamma K^2` for the specified
standing pattern. At unit K the slow-rate ratios `gamma K/Omega` are
0.00024263 and 0.00025740. At Q160000, a conditional occupation of 1000 mode
quanta means K=55.9848, expected total outgoing charge 500, and rate ratio
0.01441. Its field-amplitude validity still needs a nonlinear check.
Putting the whole earlier 2978.72488 gap into this frozen standing mode
would give a rate ratio about 0.767 at Q160000, which is not a controlled
slow-damping extrapolation. No full-gap cooling time is inferred.

The computation does not show that a merger excites this angular pattern,
that it remains a closed standing subspace under nonlinear evolution, or
that a remnant captures and survives while its charge changes. It does not
determine a physical mass scale or a galaxy-scale transfer rate. Coupling
the fragment's internal E/Q/J fluxes to an outer receiver and to the
Draco/Sextans/Fornax/Leo I budgets remains unresolved.
