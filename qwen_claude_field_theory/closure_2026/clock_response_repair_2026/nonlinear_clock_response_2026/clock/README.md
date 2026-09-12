# Nonlinear clock response of the unchanged action

Verdict: the symbolic local elimination identities are checked exactly, and the
numerical consequences are verified only in the stated frozen-action range.
Clock elimination reverses the bare quartic sign at the actual first sourced
state. The resulting nonzero stationary gradient has zero transverse static
stiffness; retaining the cubic Einstein metric feedback gives a negative
transverse characteristic discriminant at an **affine** local jet. This is not
a solved nonlinear source or cosmology.

## Scope and physical input

Use `inhomogeneous_charge_2026/exterior/run_001/result.json`, row zero:
`tau=0`, `Q=0.9078321505772312`, `s0=1.0317810692809903`, and `gamma=1e-6`.
The same `nonlinear_evolution_2026/constitutive.py:Model` provides the action.
The constitutive reference `qbar=0.9090909090909091` remains in its defining
coefficient functions; it is never substituted for the physical scalar rate Q.

In a local Minkowski frame, with signature (-,+,+,+), restrict to
`chi=Q*t+f(x)`, `tau=s0*t+pi(x)`, `u=f'`, and `z=pi'/s0`. Freeze the metric and
all explicit tau-dependent coefficients. Then

```
X=Q²-u²,     s=s0 sqrt(1-z²),     Y=(u-Qz)²/(1-z²),
L(u,z)=P(Q²-u²)+s0 sqrt(1-z²) W(Y).
```

Frozen potentials and constants do not affect this derivative calculation.
The constant-gamma cubic is `gamma (Q²-u²)u'`, the x derivative of
`gamma (Q²u-u³/3)`, **after this flat, static, one-dimensional restriction**.
This boundary identity does not remove the cubic's metric variation.
Explicit tau variation, time dependence, curved-background terms, and the
Einstein constraints have not been solved.

Because `delta z=delta pi'/s0`, the frozen clock EL integrates to `L_z=J`.
We choose J=0. It is a spatial flux/boundary choice, not a theorem about the
global clock zero mode. The reduced action here is L evaluated on L_z=0.

## Variation before clock elimination

Write `p=P_X(Q²)`, `p2=P_XX(Q²)`, `w=W(0)`, `d=W_Y(0)`, `e=W_YY(0)`,
and `v=u-Qz`. To total degree four:

```
L2 = -p u²+s0[d v²-w z²/2],
L4 = p2 u⁴/2+s0[-w z⁴/8+d z²v²/2+e v⁴/2].
F=w-2Q²d,   A=-2Qd/F,   R=1-QA=w/F,
B=[-w A³/2+d(A R²-Q A²R)-2Q e R³]/F.
```

For F nonzero, the local zero-flux branch is
`z=A u+B u³+O(u⁵)`. The coefficient B follows from varying L2+L4 and setting
the cubic clock flux to zero. Substitution gives

```
L_eff=L0+c2 u²+c4 u⁴+O(u⁶),
c2=-p+s0 d w/F,
c4=p2/2+s0[-w A⁴/8+d A² R²/2+e R⁴/2].
```

B cancels from c4 because the quadratic action is stationary at z=A u.
The actual values are

| Quantity | Value |
|---|---:|
| F | 0.0008493856065188155 |
| A | -10.688103773007851 |
| B | 151356.08785840368 |
| c2 | 0.0016954346808089535 |
| c4 | -390.8075969398429 |
| Bare `P_XX+s0 W_YY` | +0.5677182360245643 |
| Bare quartic coefficient | +0.28385911801228214 |
| `L_zz(0)=-s0 F` | -0.000876379989325866 |
| `L_eff''(0)=2c2` | +0.003390869361617907 |

Thus the bare quartic cannot decide the clock-eliminated quartic sign.
The Schur complement is `L_eff''=L_uu-L_uz²/L_zz`. The spatial principal G
uses the opposite sign to this static action Hessian.

## Exact branch and its admissibility

The same W admits an independent radical representation. Set

```
C=U-2d ell-2gamma qbar² qbar_dot,   k=2d sqrt(ell),
T=ell(1-z²)+(u-Qz)².
sqrt(1-z²) W(Y)=C sqrt(1-z²)+k sqrt(T).
L_zz=s0[-C/(1-z²)^(3/2)+k ell (Q²-ell-u²)/T^(3/2)].
```

At this actual state C,d,ell,Q,s0 are positive, `a=Q²-ell>0`, and
`F=C-2d a>0`. For u nonnegative and -1<z<=0,
`T=ell+u²-2Quz+a z²>=ell`. If `a-u²>=0`, the formula implies
`L_zz<=s0(-C+2d a)=-s0 F<0`; if `a-u²<0`, the inequality is stronger.
For u>0 the clock flux is negative at z=0 and tends to positive infinity at
z=-1. Thus there is exactly one negative-z zero-flux root and its clock block
never degenerates on this branch. Reflection supplies `z(-u)=-z(u)`.
The P logarithm remains admissible as u grows because its positive numerator
at u=0 increases by `2d u²`. These are statements about this restricted action.

The recorded computation samples 2001 u values in [0,0.01], solves the exact
radical flux by bracketed roots, and independently recomputes derivatives from
the invariant action and Model jets. The sampled minimum clock timelike margin
is 0.9955443741, maximum |z| is 0.0667504747, minimum |L_zz| is
0.0008763799893, and minimum logarithm numerator is 0.0008493169547.
The maximum clock residual is 5.6e-19 and the two L_zz computations disagree by
less than 9e-18.

| Located event | u | z | Longitudinal L_zz |
|---|---:|---:|---:|
| `L_eff''=0` | 0.00087170339718875 | -0.0092195598810167 | -0.0009014813367401 |
| Nonzero `L_eff'=0` | 0.00153986429484595 | -0.0159526364648081 | -0.0009514737045390 |

The quartic predictions are respectively 0.00085032198407130 and
0.00147280087920427. Direct 80-digit differentiation of radicals and simultaneous
root finding reproduces the events. It uses the decimal representations of
rounded primitive Model data, not interval-certified coefficients. At u=.001
the quartic action increment error is about 1.01e-11; at u=.0015 it is 1.10e-10.
At u=.01 the cubic approximation even gives the wrong sign for z: this expansion
is local and is not used to solve the wider branch.

## Transverse and metric gate

Let `r=sqrt(1-z²)`, `Qc=(Q-uz)/r`, and `sc=s0*r`. Spatial rotation invariance
gives transverse static stiffness `h_perp=L_eff'(u)/u` on the eliminated
branch. Independent invariant differentiation gives

```
F_perp=W-2Qc² W_Y,
h_perp=-2P_X+2sc W_Y W/F_perp.
```

At the nonzero stationary point it vanishes, with a nonzero transverse clock
block. The longitudinal static Schur there is -0.00621946148. A longitudinal
sign improvement alone therefore does not establish strict positivity of the
static energy Hessian in all directions, let alone nonlinear stability.

The existing `finite_gradient_metric_2026/cubic/cubic_debraiding.py` supplies
the independent covariant Einstein elimination. Its exact symbolic checks are
rerun and its unchanged `corrected` function is evaluated at the clock-rest
jet, with chi covariant Hessian **assumed zero** and a transverse wavevector.
The high-precision stationary point gives

```
Qc=0.9079722562147027270,  sc=1.031649773693832815,
X=0.8241568424396340416,   Y=0.0002567756159837333,
G0=1.58e-81 (evaluated; not assigned zero),
K0=2.1849089455352200963,
delta G=-2gamma² X²/M2=-1.35846900188013554e-12,
delta K=+4.07709999268748e-12,
K G=-2.96813107444574849e-12,
c_perp²=-6.21750853578398e-13.
```

The binary64 existing helper differs in G by 1.67e-16 and has the same negative
sign. Its gamma=0 control switches off metric feedback at the **same finite-gamma
constitutive jets**; it is not a refitted action or a new gamma=0 model.

For a non-affine local chi Hessian H in this clock-rest frame, with the spatial
chi gradient along x, the exact next diagonal-gradient condition is

```
y-directed wave: B_H=-H_00+H_xx+H_zz,
z-directed wave: B_H=-H_00+H_xx+H_yy,
G_perp=4gamma B_H-2gamma² X²/M2.
```

For gamma>0, positive G requires `2 M2 B_H>gamma X²`, hence at M2=1 each
combination must exceed about `3.39617250470034e-7`. This is a condition on an
unsolved Hessian, not a value assigned to it. Both transverse directions,
kinetic and mixed terms, and the coupled constraints still require calculation.
The non-affine sourced background is not tested by the affine result.

## Reproduction and provenance

From the repository root:

```
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/clock/test_clock_response.py
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/clock/clock_response.py --run-tests --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/clock/reproduction/result.json
```

The eight tests cover invariant expansion, exact stationary elimination,
archived input identity, two derivative routes, finite-difference Schur,
branch admissibility, the transverse identity, and the high-precision affine
Einstein gate including the older covariant symbolic identities.
`run_002/result.json` is the canonical scientific result. `contract.json`
declares the executable inputs, actual software versions, and bounds. Its v2
manifest is produced by the installed computation-audit bounded runner, which
records the command, immutable input/output hashes, actual revision and dirty
state, logs and enforced limits. Earlier `exploratory_*` and `run_001/result.json`
are development outputs; the provisional custom v1 manifest was removed.
The canonical run enforces a 120-second wall limit, 60-second per-process CPU
limit, 1 MiB combined log limit, and a cooperative one-thread numerical-library
limit. No memory/affinity cap is claimed. No coefficient refit or git mutation
was performed.
