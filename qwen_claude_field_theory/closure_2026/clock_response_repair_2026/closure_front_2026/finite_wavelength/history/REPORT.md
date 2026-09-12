# Future criticality on the fixed canonical history

Base `196f84653fec06a359314ec705d69647c5bd05a4`. The action, its reconstructed
coefficient functions, gamma=10^-6, M2=1, and the reference initial data
`a=1,m=1/10,v=1/2` are unchanged.

**Result:** throughout the maximal regular forward interval of this actual
reference history, the full FLRW principal gradient coefficient satisfies

    G > gamma H q/5 > 0.

Also `K>(1411/2500)B0>0` and the clock principal block is positive. Thus this
history cannot reach the proposed G=0 principal criticality at a finite regular
future epoch. This is a pointwise history theorem under the ODE invariant-region
argument below; it is not a finite-wavelength stability or nonlinear metric
response theorem. The bound tends with Hq and is not a uniform absolute gap
at an infinite-time endpoint. Past epochs a<1 are not covered.

## Exact action-to-history reduction

Write `j=1/(10a³)`, `q=1/(1+m)`, `R=-qdot`, and
`H²=(7/10+j)/3`. Directly from the existing canonical constitutive source,

    U=mqj, d=mj/2, Delta=U-2dq²=m²j/(m+1)²,
    B0=2P0_X+4q²P0_XX=j(m+1)(m+2)/m,
    lambda_X=3gamma qH, lambda_W=2gamma q²R,
    C=W(0)-2q²W_Y=q²(m²j+2gamma R).

After the same constrained clock and metric principal elimination as
`cubic_principal_audit/derive.py`, the **full FLRW** coefficients simplify to

    G=2gamma[2R-Hq+jR/(m²j+2gamma R)-gamma q⁴],
    K=B0-6gamma Hq+6gamma²q⁴.                         (1)

The script independently substitutes these identities into that earlier
action-derived `dust_restoring` and `kinetic` output, and checks equality
with the current canonical P/W jets. It does not infer the formula from
the old numerical scan. The affine coefficient differs:

    G_affine=G+8gamma Hq-4gamma R.

Dropping the nonzero H and qdot terms would change the question.

## Forward invariant region of the reference ODE

Use x=log(a), Omega=j/(3H²)=1/(1+7a³). The exact source ODE gives

    Omega'=-3Omega(1-Omega),
    m'/m=3Omega/2+3(m+1)v/(m+2),
    u:=R/(Hq)=m'/(m+1)
      =3mv/(m+2)+3m Omega/[2(m+1)].                  (2)

Primes here mean d/dx. The v equation is the existing rational polynomial
flow in `nonlinear_evolution_2026/constitutive.py`; no replacement evolution
is prescribed. Set w=Omega(m+2). The region

    m>0, 0<Omega<1, 1/2<=v<=1, w<=1/3

contains the initial point, where `Omega=1/8,w=21/80`. Its relevant boundary
derivatives are computed exactly:

    v'=0 at v=1;
    v' >= (m³+8m²+12m+4)/[4(m+1)(m+2)²] > 0
        at v=1/2 and w<=1/3;
    w'/w <= -5(3m+4)/[2(m+2)²] < 0
        at w=1/3 and v<=1.                          (3)

The first inequality follows because v' at v=1/2 decreases with Omega;
the second because w'/w increases with v. Equation (3), uniqueness, and
the multiplicative m and Omega equations give the usual first-exit proof
that the region is forward invariant on the regular interval. Independent
read-only review supplied and checked this coupled w barrier; bounding
Omega alone would not suffice for arbitrary large m.

For `I=j m⁴/(m+1)²`, (2) yields the exact identity

    I'/I = 6v-3+3Omega(m+2)/(m+1) >= 0,
    I(0)=1/121000.                                  (4)

Hence `j >= (m+1)²/(121000m⁴)`. Also a>=1 gives
`2/5 < H < 3/5`. The ODE stays locally smooth on the region. On any bounded
forward x interval, `m'/m<4` and v remains bounded, so m cannot blow up or
reach zero there. Likewise `a_dot=aH` prevents finite proper-time a blowup.
These are the elementary continuation controls behind the regular-interval
qualification; no interval-certified ODE integration or formal ODE theorem
is supplied by the code or Lean file.

## Positive rational bound for G

Normalize (1) using

    beta=2gamma Hq/j, eps=gamma q³/H,
    G/(2gamma Hq)=2u-1+u/(m²+beta u)-eps.

Equations (2)-(4), gamma=10^-6 and the H bounds imply

    u >= u0:=3m/[2(m+2)] > 0,
    0<beta <= (363/2500)m⁴/(m+1)³
             < B:=3m⁴/[20(m+1)³],
    0<eps < 1/100000.                               (5)

For positive denominators the fraction `u/(m²+beta u)` increases with u
and decreases with beta. Its comparison can also be proved by cross
multiplication: the numerator of the difference is
`m²(u-u0)+u u0(B-beta)`, which is nonnegative. Therefore

    G/(2gamma Hq) >= L(m):=2u0-1+u0/(m²+B u0)-1/100000.

There is an exact positive-coefficient identity

    L(m)-1/10 = 3 P(m)/D(m),
    P(m)=2533320m⁶+10303237m⁵+9473074m⁴+1333000m³
         +2533120m²+8133280m+4000000,
    D(m)=100000m(m+2)(40m⁴+209m³+360m²+280m+80).

Every displayed coefficient is positive and m>0, so `L(m)>1/10`. This
establishes the stated `G>gamma Hq/5`. It is an analytic sufficient bound,
not a scan or a fitted approximation.

For K, (4) and H<3/5 give

    6gamma Hq/B0
      < (1089/2500)m⁵/[(m+1)⁴(m+2)] <1089/2500.

The last denominator minus m⁵ is a polynomial with strictly positive
coefficients. Equation (1) now gives `K>(1411/2500)B0>0`. Since R>0 follows
from (2), C>0 follows immediately as well. These are the actual local
principal coefficients; lower-derivative constraints and finite wavelengths
remain outside this proof.

## Verification, evidence scope, and reproduction

`derive_history.py` checks the action/history identities, boundary and
invariant polynomials, positive numerator, and the exact definitions compiled
in `HistorySigns.lean`. It imports the earlier principal derivation, whose
26 checks must also pass. Three existing Model evaluations at t=0,0.1,1
are consistency controls only; the no-crossing result uses (2)-(5).
At t=0 the direct and reduced evaluations give
`G=7.533412027e-6` and `7.533412026972e-6`, respectively.

The four Lean theorems prove the rational identity, its strict bound, the
fraction comparison, and the resulting normalized bound under the explicit
pointwise assumptions (5). All compile with only
`[propext, Classical.choice, Quot.sound]`; there is no sorry or theory axiom.
The action variation, ODE invariant-region argument, and source-to-Lean
symbolic bridge are outside the formal proof. An initial aggregate tactic
import encountered a missing unused cached module; using the required
individual tactic imports compiled successfully without installing anything.

The bounded execution record is `run_001/manifest.json`; actual results and
Lean output are stored alongside it. The final run passed 27 new exact checks,
all 26 imported principal checks, three canonical Model consistency controls
and four Lean theorems, with exit zero. The manifest validated against the
workspace inputs and result hashes. Reproduce the Python calculation from
the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/history/derive_history.py
```

Compile the Lean file with `lake env lean` in the existing pinned environment
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.
`run_checks.py` runs both with their actual output retained by the bounded
runner. The contract declares versions, inputs, resource limits and exclusions.

Computation-audit guided the exact contract and provenance; proofread-math
self-review was limited to these new statements and notation. No action edit,
parameter change, global nonlinear theorem, CMB result or physical MOND
response follows from this package.
