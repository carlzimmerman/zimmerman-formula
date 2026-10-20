# W4-02: independent attempt at the coefficient 4

2026-10-20. The requested numerical derivation was **not achieved**.
`kappa=1/2` remains **FITTED**. The useful result is a precise nonselection
statement: **even after the background vacuum is fixed, the displayed effective
response laws permit a continuous coefficient**. Positive local kinetic
energy and subluminal linear response do not remove that freedom.

The inherited measurements are CFG493's `kappa_Lambda=0.417 +/- 0.095` and
`kappa_crit=0.345 +/- 0.078`, on separate footings. No measurements enter the
mathematics here, and no new observational or significance claim is made.

## Exact output

The three main derivations are in [PROOF.md](PROOF.md).

1. **A source-connected portal with a fixed zero mode.** For every `xi>0`,
   set `a=sqrt(xi G epsilon)` and

       W_xi(u;epsilon)=a^2/(4piG)[-u/a-log(1-u/a)-u^2/(2a^2)].

   Every member has `W_xi(0;epsilon)=0`, zero source variations at the
   unpolarized background, and a convex constitutive potential. The same
   algebraic spherical reduction gives `g_b=g^2/(g+a)`. The density history
   is the same, the zero mode is the same, and the dimensionless force law
   is the same, while `a^2/(G epsilon)=xi` changes. This makes the residual
   freedom explicit inside the recorded simple-mu constitutive structure.
   The exact algebraic reduction omits the stiffness contribution; a finite
   stiffness gradient changes that equation.

2. **An explicit positive, subluminal scalar toy.** In a specified preferred
   frame use

       L=dot(Phi)^2/(2Kc^2)-E_a(|grad Phi|)-rho_b Phi-epsilon,
       E_a(g)=[g^2/2-a g+a^2 log(1+g/a)]/K,  K=4piG.

   At every constant nonzero background gradient, its squared characteristic
   speeds are `v_T^2/c^2=mu`, `v_L^2/c^2=2mu-mu^2`, where `mu=g/(a+g)`.
   Both lie in `(0,1)` for every `a>0`. The vacuum parameter epsilon and the
   canonical time/source normalizations can be held fixed while a varies.
   A supplemental analytic member reproduces the **quadratic** branch
   `g^2=g_b^2+a g_b` and also has subluminal characteristic speeds for every
   a. Thus the conclusion is not conditional on choosing the simple-mu
   branch. These are effective local countermodels, not full gravitational
   theories: the zero-gradient spatial symbol is degenerate, and covariant
   clock dynamics, lensing and cosmological perturbations remain unspecified.

3. **The pi obstruction has a domain.** The safe statement excludes an exact
   half when `a0/(cH_Lambda)=R(pi)` for a rational function with algebraic
   coefficients. Horizon inputs alone do not establish that hypothesis.
   For example `a0=c^2/sqrt(A_dS)` gives `kappa^2=2/3`, a pi-free number.
   This is a counterexample to an unrestricted grammar claim, not a physical
   prescription selecting a coefficient. The proof uses the standard
   transcendence of pi.

None is a no-go for future physics. The required new input is one that
**breaks the multiplicative deformation** `xi -> s^2 xi` and fixes its
unique value to a quarter in physical source conventions. The usual
zero-mode normalization and density tracking do not do that.

## Other routes executed

**R1, symmetry/duality/BPS.** Canonical field normalization preserves the
physical ratio. Ordinary internal symmetries at fixed metric allow an
independent identity operator in the action. A Born-Infeld test yields

    xi_s=(alpha_c^2/G)(T/C),

where T is nonlinear tension, C absolute vacuum energy, and alpha_c a
physical canonical source coupling. Even granting C=T leaves alpha_c free.
Granting weak-field no-force gives `alpha_c^2=Omega_(d-2) G_d`, hence
`xi_s=4pi` in d=4 or `2pi^2` in d=5. This is not a derived MOND scale:
the square-root force is Newtonian at small field and saturates at large
field. Its threshold needs another bridge to a0. A vacuum-subtracted BPS
wall bound likewise does not determine the additive gravitational vacuum.
This closes these specific normalization mechanisms; transformations acting
on the metric or a fully specified microscopic theory were not exhausted.

**R2, a single Lorentz scalar.** For `L=-B Y^(p/2)` on a spacelike-gradient
background with metric signature `(-,+,...)`, the squared longitudinal
characteristic speed is `(p-1)c^2`. Deep MOND needs p=3 in this model,
giving `2c^2`, independently of B. Changing B cannot select a causal
normalization. A cone wider than the matter cone is not by itself a proof
of closed causal curves. The preferred-frame toys above show separately
that requiring a narrower cone also does not select the scale.

**R2b, published DBI bridge.** The source verification and normalization
translation are in [SOURCES.md](SOURCES.md). Its radius identification and
matter coupling remain free. The sign chosen for its dark-energy action
also gives a negative time kinetic Hessian. It is not a healthy completion
of the toy or an exact coefficient selection.

## Independent consequences and the missing step

All constant-xi density portals predict
`a0(t)/a0(t0)=sqrt(epsilon(t)/epsilon(t0))` at fixed G. The simple-mu toy
also predicts `v_L^2/c^2=2(v_T^2/c^2)-(v_T^2/c^2)^2`. These could test a
response model, but they hold for **all** xi and therefore cannot favor a
quarter within the family. They are not two successful predictions of a
coefficient derivation. No candidate reached that campaign gate.

An actual solution needs a specified cross-sector normalization principle
whose restriction to this family is not invariant under the deformation.
It must determine xi without using the measured a0, then survive a full
gravitational and independent-observable test. An explicit UV action with
fixed source couplings is the meaningful continuation; another vacuum
subtraction, field rescaling, or causal inequality repeats an obstruction.
No such action was constructed here. The original puzzle remains open.

## Checks, provenance and overlap

The base was `177591c05a384bc07c819e3fe0d5517aa8798cb4`. Criteria alone were
committed first as `72a3b470d`. Three read-only agents developed independent
symmetry, response and falsification routes. The coordinator reconstructed
the displayed countermodels and reconciled the results. A separate fresh
agent audits [PROOF.md](PROOF.md); see [REVIEW.md](REVIEW.md) for the exact
artifact and outcome.

The final symbolic run passes **34/34** exact checks. MUTATE changes the
constitutive normalization, cubic power and selected spatial dimension;
**C08, C20 and C28 fail as expected** with exit 1, while the other 31 pass.
No numerical parameter search was used. The supplemental quadratic formulas
are checked in C29-C34 and independently reviewed. The original 27-check
runs and original checker are retained as history; the timing and expanded
checks were disclosed in [SUPPLEMENT.md](SUPPLEMENT.md), committed alone
as `05b047a17` before the checker changed. PROOF.md's historical reference
to the checker at the time of writing refers to that original version.

The script/contract and bounded-run manifests record actual versions,
before/after hashes, logs, limits and exit statuses. Both final manifests
validate against current inputs: [normal](runs/final_normal/manifest.json)
is `completed`, [mutant](runs/final_mutate/manifest.json) is the expected
`failed` control. `nice` was requested but the sandbox did not permit changing
scheduling priority; each computation still used one Python process, one
library thread and under four seconds. Earlier runs refer to superseded
checker/dashboard hashes; use the final manifests for current evidence.

This is an independent extension and synthesis, **not a novelty claim**.
Nearest prior results: CFG911's free xi portal, K219's DBI pressure minimum,
K308's Lorentz response cone, K313's offset nonselection, K535's kernel
deformations, and K322's fixed-vacuum preferred-foliation family. Those
precedents are not relabeled as new derivations. This lane adds the explicit
source-zero constitutive family, globally bounded local scalar cones for
both interpolation branches, the screening-source translation, and a
qualified pi-grammar proof.

Reproduce from repository root:

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_02_independent_portal_audit/checks.py
    W4_02_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_02_independent_portal_audit/checks.py

The second command intentionally exits 1. Nothing was downloaded; no p63,
four-form, KAPPA_LOGIC or manuscript integration work was duplicated.
