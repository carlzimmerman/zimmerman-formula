# Bounded audit of the L123 universal claims

2026-09-10. Audited revision: `293b4e70a167e6845e544b42671f7c24994c80a4`.
This directory is independent of the active nonaffine inverse and does not
change any Fable inputs. Verdict: the universal stiff-density assertion is
refuted; the purported universal CMB no-go and ghost-free hybrid conclusion
are not established by the implemented checks.

## Exact counterexample family

Use signature (-+++), homogeneous X=phidot^2/2>0 and the shift-symmetric scalar
Lagrangian P(X)=X^N, with fixed real N>=2 (in particular, integer N>=2).
This power-law family is a standard counterexample, not a proposed novel theory.
Let n=P_X sqrt(2X) be the physical shift-charge density and C=a^3 n the
conserved comoving charge. The ordinary homogeneous shift equation gives

\[
 n=\sqrt2 N X^{N-1/2},\qquad
 \rho=2XP_X-P=(2N-1)X^N,\qquad
 D=P_X+2XP_{XX}=N(2N-1)X^{N-1}>0.
\]

These density and current expressions are also derived in the executable
certificate by varying the homogeneous action before fixing its lapse:

\[
 L_{\rm hom}=\mathcal N a^3
       \left(\frac{v^2}{2\mathcal N^2}\right)^N,\qquad
 \rho=-\left.\frac1{a^3}\frac{\partial L_{\rm hom}}{\partial\mathcal N}
       \right|_{\mathcal N=1},\qquad
 n=\left.\frac1{a^3}\frac{\partial L_{\rm hom}}{\partial v}
       \right|_{\mathcal N=1},\qquad v=\dot\phi>0.
\]

The shift equation is d(a^3 n)/dt=0 because this action has no explicit phi.

For X>0 the inversion of n is unique. Hence

\[
 \rho=(2N-1)\left(\frac{n}{\sqrt2 N}\right)^{2N/(2N-1)},
 \qquad \rho\propto a^{-p_N},\qquad p_N=\frac{6N}{2N-1}.
\]

The standard minimally coupled k-essence coefficients obey P_X>0 and D>0,
and their ratio is c_s^2=P_X/D=1/(2N-1). Direct algebra gives

\[
 p_N=3+3c_s^2,\qquad 3<p_N\le4<6\quad(N\ge2).
\]

N=2 supplies the smallest integer counterexample: rho=3X^2=(3/4)n^(4/3),
rho proportional to a^(-4), and c_s^2=1/3. There is no a^(-6) density component
in this exact homogeneous solution. N=1 recovers the canonical stiff control.
Given delta>0, any N>=2+1/(2 delta) has 0<c_s^2<delta; arbitrarily large
integers satisfy that bound. Every finite N still has p_N>3 and positive
pressure, so this is not exact pressureless dust.

For general regular P(X), the same charge convention instead gives

\[
 \frac{d\rho}{dn}=\sqrt{2X},\qquad
 \frac{d^2\rho}{dn^2}=\frac1{P_X+2XP_{XX}}.
\]

A nonzero second derivative does not make rho globally quadratic in n. It
also does not identify a separate a^(-6) component: a Taylor term about a
nonzero reference n is not a global density component. The factor 2 in the
L123 derivative formula is absent under the explicit n convention above.

## What L123 actually checks

All line citations below refer to the pinned revision, not a moving dashboard.

| Artifact and lines | Implemented assertion | Missing implication |
|---|---|---|
| `fable_independent_2026/L123_cmb_pincer_tightness.py:57-63` | Q(0)=0 for one displayed Q | A complete homogeneous stress tensor and exclusion of other clock/curvature contributions are not calculated there. |
| Same script, `64-68` | NOGO-2 passes literal `True` | No perturbation equations, elliptic response operator, source/boundary hypotheses, or third-peak exclusion theorem is supplied. |
| Same script, `73-80` | Substitute eta=0 into -2 M2 k^2 eta | No complete enlarged constraint matrix or reduced kinetic energy is evaluated. |
| Same script, `89-107` | Canonical P=X and cuscuton P=sqrt(2X) arithmetic | Two examples do not classify all P(X); the N>=2 family above contradicts universal a^(-6) scaling. |
| Same script, `136-144` | VERDICT-1 and SCOPE-1 pass literal `True` | These checks cannot certify their CMB, ghost-free, or all-gates prose. |
| `fable_independent_2026/lean_2026/Mondlean.lean:342-352` | For M2!=0, k!=0, (-2 M2 k^2 eta=0 iff eta=0) | `dust_ghost_separable` has no action, dust, constraint-completeness, coupling or energy-positivity hypotheses. Its docstring's physical conclusion is stronger than its theorem. |

An elliptic field has no freely evolving homogeneous wave solution under
specified invertible boundary conditions. That observation alone does not
fix the coupled gravity-matter-radiation transfer functions or quantify the
third CMB peak. The script provides neither the proposed general reduction
nor a spectrum calculation. The fixed-Q background identity remains valid
as an identity, without becoming a universal MOND no-go theorem.

Likewise, zero contribution to one previously identified bracket is a useful
limited statement, not proof that a newly coupled sector has no other ghost.
The k=0 case is explicitly excluded by the Lean theorem's hypotheses.

## Scope and reproduction

This certificate rejects the claimed exhaustive route from finite k-essence
derivatives to unavoidable stiff density and thence to particle-only dark
matter. It does not prove an exactly pressureless, stiff-free regular P(X)
fluid; nor does it establish clustering, a BBN bound, a CMB fit, absence of
strong coupling, or a healthy complete MOND action. Positive local k-essence
coefficients and arbitrarily small positive c_s^2 do not supply those results.

Run from the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/l123_review/test_power_law_counterclaim.py
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/l123_review/PowerLawCounterclaim.lean
```

The SymPy suite has nine exact tests, including homogeneous action variation,
symbolic family identities, positive-factor range certificates, and canonical/N=2 controls. The three Lean
lemmas prove conditional rational inequalities and an identity after the
displayed density and sound-speed formulae have been derived; they do not
formalize the field equations. Python/Lean output and input hashes belong in
the parent bounded-run provenance. No network or new dependency is required.

Validation on 2026-09-10: all nine tests passed under Python 3.9.6 / SymPy
1.14.0, and all three Lean lemmas compiled under Lean 4.34.0-rc2. Each printed
axiom set is exactly [propext, Classical.choice, Quot.sound]; no sorry axiom.
The initial broad tactic import met an absent cached optional module; the
final file uses only the installed, required tactic imports. Final mathematical
self-review covered this report and both new certificate files.
