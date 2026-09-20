# Action, matching, and normalization route

Base revision: `928c61c79b4a74bd47ecf515be19da2342cde093`.
Review date: 2026-09-20. Scope: the specified four-form and fixed-shape scalar
constructions, with no inference of particles from field variables. Original
sources are unchanged. This is a bounded mathematical audit and constructive
counterfamily, not a statement about every possible action.

**Normalized target.** With the independently fixed acceleration
`s = c sqrt(G rho_Lambda)`, let `x = g/s` and
`mu(x) = 1 - (1-p(x))^2`. Derive `p(0)=0` and `p'(0)=1` from the
action without fixing a free dimensionless parameter by the desired answer.
For the deep-MOND convention `mu ~ g/a0`, the chain rule gives
`2 p'(0) = 1/kappa`, where `kappa=a0/s`, whenever `p(0)=0`.
Thus unit response is equivalent to `kappa=1/2` under that convention.

**Primary verdict: incomplete, with the smallest missing implication.**
The reviewed action and matching equations do not fix the invariant ratio
`Z/beta^2`; an additional physical principle must do so. The stronger assertion
that those equations alone force the half is refuted by the explicit family
below. The four-form source does not itself define the occupancy variable `p`,
so the last translation to its derivative remains conditional on the stated
static constitutive relation.

## Raw source anchors

- `kappa_closure/k04_four_form_promotion_consistency.py:44-52`:

  ```python
  P = Z*q**2/2 + b*beta**2*q**2
  eps = sp.simplify(q*sp.diff(P, q) - P)
  a0sq_over_G = beta**2*q**2
  kappa2 = sp.simplify(a0sq_over_G/eps)
  ratio_needed = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), Z)[0]/beta**2
  ```

  Lines 14-16 state the flux equation `d_mu(dL/dq)=0`; lines 12-13
  explicitly give `Z/beta^2 = 8 - 2b` as the half condition. The later
  shorthand `Z/beta^2=8` at lines 96 and 101 drops the primitive contribution;
  the exact condition used here retains it.

- `fable_independent_2026/L226_kappa_and_the_free_function.py:85-90`
  specifies `F(Z)=mu^4 f(Z/mu^4)`, `rho_fixed=f0*mu**4`,
  `beta_fixed=bb/mu**2`, and `a0_expr=lam**3/(12*pi*G*beta_fixed)`.
  Lines 163-166 require a principle fixing shape, locking the vacuum value
  to the branch coefficient, and fixing matter coupling independently.

- `fable_independent_2026/L229_the_principle.py:68-73` specifies the
  scalar action and derives `G_obs = G_b (1+2 xi/K)`. Lines 83-100 perform
  the deep-MOND matching. Lines 138-141 **insert** `b=K/3` in a scan;
  lines 199-204 claim saturation suffices for that relation.

- `kappa_closure/k02_global_constraint_average.py:8-13` assumes
  `rho_Lambda = eta <L_phi>` and defines the scalar density to be averaged.
  Lines 61-77 implement a particular Maxwellian cosmological model and
  finite-time averages. These are model inputs, not an action-derived
  Ward identity fixing unit susceptibility.

## 1. Flux variation and exact elimination

Write the vacuum part in the source's units as

`D = Z/2 + b beta^2 > 0`, `P(q)=D q^2`, `a0=beta sqrt(G)|q|`.

Here the energy density is `epsilon_Lambda=rho_Lambda c^2`, so the
independently fixed acceleration is exactly `s=sqrt(G epsilon_Lambda)`.
There is no missing factor of `c` in this convention.

For a four-form `F=dA=q volume`, variation of `A` gives
`d(P_q)=0`, hence `P_q=C` on a connected vacuum region. With fixed covariant
`F`, inverse-metric variation gives
`delta q=(q/2) g_mn delta g^mn`; consequently
`T_mn=(P-q P_q)g_mn` and `epsilon=qP_q-P`. Thus

`q=C/(2D)`, `epsilon=C^2/(4D)`, `kappa^2=beta^2/D`.

Equivalently, in the fixed-conjugate-flux ensemble, stationarity of
`P(q)-Cq` gives the same `q`; eliminating it gives
`P-Cq=-C^2/(4D)`. Eliminating a variable does not supply a new equation
for the constant couplings. Fixing `epsilon` determines an appropriate
`C` for each `D`, and does not determine `beta^2/D`.

This derivation uses the action's explicit algebra, not the historical
four-form citations named in its docstring. Global topology, quantum flux
quantization, and membrane charge spectra are not inputs to this local result.

## 2. Counterfamily preserving vacuum matching and flux stationarity

An especially strong test holds `D`, `C`, `q`, and `b` all fixed. Set

`beta=t>0`, `Z(t)=2D-2b t^2`.

On the open interval where `Z(t)>0`, all members have precisely the same
vacuum `P(q)=Dq^2`, stress tensor, conserved conjugate flux, and flux
stiffness `P_qq=2D>0`. They nevertheless have

`a0(t)=t sqrt(G)|q|`, `kappa(t)=t/sqrt(D)`.

For example, for any fixed `0<=b<1` and `D=4`:

| beta | Z | D | kappa |
| --- | --- | --- | --- |
| 1 | `8-2b` | 4 | 1/2 |
| 2 | `8-8b` | 4 | 1 |

Both have positive bare `Z` and equal positive total flux stiffness.
The family is a variation of actions' couplings, not a claim that a fixed
action has multiple values of a constant. It establishes nonuniqueness
under the listed requirements. The galaxy sector changes through `a0(q)`,
which is precisely the response that vacuum matching failed to determine.
The report does not claim both parameter points fit galaxy or Solar-System
data, nor that both give identical perturbations on a nonzero-gradient
cosmological solution. Its vacuum background is the zero-gradient vacuum
used to derive the source's coefficient relation.

If the stipulated `p` dictionary applies, the two members would have
`p'(0)=1` and `p'(0)=1/2`, respectively. The action source alone does not
provide a globally defined `p` or establish its probability interpretation.

## 3. Field redefinition and Ward identities

For `q_tilde=alpha q` with `alpha>0`, rewriting the **same** action gives

`Z_tilde=Z/alpha^2`, `beta_tilde=beta/alpha`,
`D_tilde=D/alpha^2`.

Therefore `Z_tilde/beta_tilde^2=Z/beta^2` and
`beta_tilde^2/D_tilde=beta^2/D`. Setting the quadratic term to a canonical
coefficient merely moves the surviving number into the response coupling.
It cannot change a dimensionless observable.

Gauge symmetry `A -> A+dB` leaves `F` unchanged for every value of these
couplings. Its variational identity and flux conservation hold throughout
the counterfamily. Diffeomorphism covariance likewise holds for each scalar
term separately. These symmetries supply no identity relating their independent
coefficients. A new symmetry mixing the vacuum and response operators could
in principle restrict the ratio, but no such transformation or Ward identity
is exhibited in the reviewed sources.

The parallel scalar check is equally direct: under `phi_tilde=alpha phi`,
the matter coupling transforms as `lambda_tilde=lambda/alpha`, and a
`|grad phi|^3` coefficient as `b_tilde=b/alpha^3` in fixed vacuum units.
Thus `lambda^3/b`, the combination in deep-MOND matching, is invariant.
The high-gradient coefficient transforms as `K_tilde=K/alpha^2`, so
`lambda^2/K` and the Newton-constant renormalization are invariant too.

## 4. Stationarity and saturation do not fix the branch coefficient

L229 correctly observes that `f(u)=-1+b|u|^(3/2)+...` has zero first
derivative at the origin for every finite `b`. Stationarity therefore
does not select `b`. More strongly, fixing the vacuum value **and** the
high-gradient slope still leaves it free.

For `K,h>0` and `u>=0`, define the explicit family

`f_h(u) = -1 + K[u/2 - h sqrt(u) + h^2 log(1+sqrt(u)/h)]`.

Direct differentiation gives

`f_h'(u) = (K/2) sqrt(u)/(h+sqrt(u))`.

For every `h`, this has `f_h(0)=-1`, `f_h'(0)=0`,
`f_h'(infinity)=K/2`, and

`f_h(u) = -1 + [K/(3h)] u^(3/2) + O(u^2)`.

Moreover, for `u>0`,
`f_h''(u)=K h/[4 sqrt(u)(h+sqrt(u))^2]>0`; the static flux derivative
`f_h'+2u f_h''` is positive. Thus the freedom does not depend on losing
these elementary static ellipticity conditions. No claim about full
relativistic stability follows from this check.

Consequently `b=K/3` is the special choice `h=1`; saturation alone does
not imply it. Holding the vacuum scale, `lambda`, `K`, and `G_b` fixed
also holds `G_obs` fixed. The L229 matching equation then yields

`kappa_h = lambda^3/[12 pi b_h G_obs^(3/2)]`
`= lambda^3 h/[4 pi K G_obs^(3/2)]`.

Hence different `h` change the predicted coefficient while preserving all
the just-listed background and asymptotic data. This is a construction on
the spacelike/static branch, not a complete timelike cosmological theory.

## 5. Global averaging route: what was and was not established

The k02 model assigns a dimensionless average of a selected density to
vacuum energy, with an assumed coefficient `eta`. Its finite quadratures
do not amount to a variational mechanism fixing either `eta` or the local
response slope. A global constraint could remove some freedoms in a new
action, but it would have to be specified and varied with the local sector;
no such completed action is supplied in this script.

The present report does not rerun its costly quadratures or elevate the
script's finite-time diagnostics to a proof about every asymptotic future.
It also does not adopt the broad claim at k02 lines 91-92 that those routes
exhaust all possible principles.

## Dependency and obligation record

`specified P(q)` -> `flux equation and stress tensor` ->
`kappa^2=beta^2/D` -> **missing physical constraint on beta^2/D** ->
`kappa=1/2` -> (given constitutive dictionary) `p'(0)=1`.

| Obligation | Result |
| --- | --- |
| Correct energy-density and acceleration units | Passed, epsilon=rho c^2 |
| Exact flux elimination | Passed by explicit variation and algebra |
| Vacuum matching removes coupling freedom | Failed, fixed-D counterfamily |
| Canonical normalization removes coupling freedom | Failed, invariant ratios |
| Existing gauge/diffeomorphism identities select half | Failed within this family |
| Stationarity plus high-gradient saturation selects branch coefficient | Failed, f_h family |
| Global constraint derives unit local susceptibility | Not addressed by the source's averaging model |
| Full relativistic stability and observational viability of counterfamilies | Out of scope |
| Complete action-to-p dictionary | Conditional on separately supplied reduction |

## Verification and exact remaining gap

An independent `python3`/SymPy calculation at this revision verified exactly:
the fixed-D substitution, Legendre elimination, invariant flux ratio, all
three limits of `f_h`, its branch coefficient, and invariance of
`lambda^3/b` under field rescaling. It printed:

```text
PASS: exact flux family, fixed-flux Legendre elimination, invariant normalization ratio, stationary saturated shape family, scalar coupling/branch rescaling invariance.
```

These are symbolic checks of displayed identities, not observational tests.
The proof itself is the explicit formulas above. No external theorem is
needed for the nonuniqueness implication.

The strongest safe conclusion is that the reviewed particle-free field
actions can link the **scale** of local response to vacuum energy, but the
stated stationarity, matching, and normalization conditions do not select
unit dimensionless response. A useful next principle would derive a relation
between the two operators' coefficients from specified dynamics or a symmetry
that forbids the counterfamily. For the four-form example the necessary
relation is exactly `Z/beta^2=8-2b`; imposing this equality with a multiplier
would encode the desired answer unless the multiplier's physical origin
independently requires that numerical relation.
