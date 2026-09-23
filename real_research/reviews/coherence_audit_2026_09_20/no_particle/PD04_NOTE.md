# PD04 under the explicit no-dark-matter-particle requirement

**Verdict: incomplete, with the missing correspondence identified.** PD04
does not add a particle-free closure equation or certificate. It assembles
four pairs of labels and proposes that they describe the same structure.
It expressly acknowledges that it does not derive charges from channels
(`deepseek_push/PD04_two_one_lock.py:57–64,228–241`). This does not rule out a
particle-free modified-gravity theory; it means that PD04 does not yet
establish that theory.

Reviewed at `d1ea3d4c347ca1df5e0d17db7f4972f95584a87c`. Read-only source
review; the only new artifact is this note. No original script was run or
edited. Stored output/results report 10/10 PASS. An independent AST read
finds one numerical comparison, `len(set([2, 2, 2, 2])) == 1` at line 114,
and nine checks whose condition is literally `True`. There is no new
action, field equation, current equation, perturbation equation, or Lean
certificate in PD04.

## What is and is not a particle assertion

- A classical metric or scalar field, its conserved Noether current, or a
  stress tensor obtained by varying its action does **not** by itself
  postulate a particle species. A gravitational contribution may be written
  as an effective stress tensor without changing this fact.
- PD04 explicitly imports a **cold species with mass 5.09 keV**, two
  particle phases, a decay line, and a warm-dust free-streaming scale
  (`PD04_two_one_lock.py:12–14,95–99,197–207`). These are actual particle
  interpretations, not consequences of merely using a scalar field.
- The source document is equally explicit:
  `deepseek_push/THE_COMPLETE_THEORY.md:38` calls the phantom a collisionless
  classical gas; lines 55–60 introduce a particle mass, decay flux and
  warm-dust transfer function; line 132 says “one cold species” and gives
  collisionless dust more than 98% of its cosmic dark budget. That package
  cannot be adopted unchanged under the user's constraint.
- A separately specified classical pressureless component is not
  automatically a particle species either. Nevertheless, an independently
  supplied density or integration constant is extra dynamical content or
  initial data. It must be stated explicitly and cannot be claimed to have
  been derived just by moving terms to the right side of Einstein's
  equation. Particle-free does not mean that a field has no degrees of
  freedom or no initial data.

## The precise implication PD04 lacks

The two static scalar metric potentials coexist in one static
configuration. Timelike and spacelike gradients are mutually exclusive
non-null cases of a scalar invariant at a point; the null case also needs
boundary treatment. Equality of the numbers of labels establishes no map
between these different mathematical objects. The missing result is a
derived map, from a specified action and its solutions, identifying the
relevant field response and conserved quantities while respecting their
equations and constraints. No such map is encoded in PD04.

Shift symmetry also does not imply a dust equation of state. For example,
define a classical scalar action with
\(X=-g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi/2\) and \(P(X)=X\).
For a timelike homogeneous gradient, variation gives
\(p=P=X\), \(\rho=2XP_X-P=X\), hence \(w=1\), while the shift current
is conserved. Thus a conserved shift charge can exist in a particle-free
classical field without pressureless dust. PD04's own cited stiff branch
is consistent with this distinction, not a derivation of dust from charge.
Likewise “one field” alone implies neither one physical particle mass nor
the absence of further response regimes.

The cited `gauss_map_charge` theorem is narrower and remains useful.
`deepseek_push/lean/G227_gauss_map_prototype.lean:41–61` defines
\(g=\sqrt{GM_ba_0}/r\) and proves
\[
\frac{4\pi r^2g}{4\pi G}=\frac{\sqrt{GM_ba_0}\,r}{G}.
\]
It certifies cancellation for an assumed radial field; it does not derive
a Noether current, particle spectrum, dust stress, or the radial field
itself. If \(g\) is the **total** gravitational acceleration, its flux
defines the total Newtonian-inferred mass \(M_{\rm dyn}=r^2g/G\).
The inferred excess is \(M_{\rm dyn}-M_b\), so it is not legitimate to
call the raw flux additional matter and then add the baryons again.

## Strongest surviving particle-free statement

The static field-response law and its spherical consequences can be
formulated entirely without dark-matter particles. Given a derived or
explicitly postulated gravitational response equation, its deep spherical
limit can imply \(g^2=a_0g_N\), and circular motion then gives
\(v^4=GM_ba_0\). An effective “phantom density” may describe the excess
response inferred by a Newtonian analysis; it need not be a material
substance. These implications can receive precise Lean certificates with
their field-law and boundary assumptions visible.

PD04 does not supply the missing covariant action, branch correspondence,
energy budget, or cosmological perturbation closure. The useful next
particle-free question is whether one specified gravitational action
produces the required static response and independently accounts for its
background and perturbations. The keV species, decay line and warm-particle
free-streaming claims are not premises for that program. No ΛCDM adoption
or particle hypothesis is required to pursue it.

## Source hashes (SHA-256)

| Source | Hash |
|---|---|
| `deepseek_push/PD04_two_one_lock.py` | `91c1114955de8d1eb0b4c471f029aa95156e977744437fef02174fb6185c62ba` |
| `deepseek_push/PD04_two_one_lock.out` | `b4ad3df1641a5b4f29e3b4ededb6ba45734c9c99bde5056740a0ee041278c5f1` |
| `deepseek_push/PD04_results.json` | `a9762664409322dab833f98f7a9818e6442ebffa7b8b60971ba98e1a8cc4b05a` |
| `deepseek_push/THE_COMPLETE_THEORY.md` | `9e63cff9d7c63372c2bbb63be37c424a1a26b9b82660122c2be76da968cc8422` |
| `deepseek_push/lean/G227_gauss_map_prototype.lean` | `83f2caa18e581288fd9188c5799a18f12599ca09434b474c15969e89e1536e25` |

## Addendum: PD05's limit theorem and its ontology claim

The new untracked `deepseek_push/lean/PD05_ontology_lock.lean` was reviewed
at observed HEAD `979c4d8557b3cf94eae8b8d2acacb6c465931172`; its SHA-256 is
`7ed22898705340fc433e7520c543250d8aa10b2e03281dd532e63611ad18872b`.
The unchanged file **compiles successfully** with
`lake env lean <repo>/deepseek_push/lean/PD05_ontology_lock.lean`
from `fable_independent_2026/lean_2026` (exit 0, no compiler output).

**Primary verdict for the claimed ontology implication: incomplete, with
the smallest missing implication identified.** The actual Lean mathematics
is correct. Lines 37–40 prove that \(kr\to0\) as \(r\to0\); lines 46–54
prove that \(C+kr\) cannot tend to zero if \(C\ne0\). Lines 60–64 merely
conjoin these facts. Their quantified objects are real constants and
functions on the real line. Neither a particle model nor a scalar action,
stress tensor, gravitational field equation, or source measure occurs in
the theorem statement.

The physical interpretation requires distinctions not present in the
certificate:

1. **Radial domain.** The assumed deep exterior law
   \(g=\sqrt{GM_ba_0}/r\) has \(g/a_0=r_M/r\), with
   \(r_M=\sqrt{GM_b/a_0}>0\). Its deep regime is \(r\gg r_M\), not
   \(r\to0\). An exterior profile cannot be extended to the origin by
   algebra alone. A baryonic point source also lies at that excluded
   origin. A valid core continuation and matching conditions are missing.
2. **Total versus excess.** When \(g\) is total acceleration, \(kr\) is
   the corresponding total inferred mass \(r^2g/G\), where
   \(k=\sqrt{M_ba_0/G}\). The excess above the baryons is
   \(kr-M_b\) in this exterior approximation, not \(kr\). Neither
   approximation has an established origin limit in the physical model.
3. **Central atom versus all particles.** If an enclosed-mass measure were
   defined near the origin, a positive point mass *at the chosen centre*
   would add a constant for all \(r>0\). An off-centre particle at radius
   \(r_*>0\) instead contributes \(m\mathbf1_{r\ge r_*}\), which
   tends to zero at the origin. A distributed particle population can
   likewise have vanishing enclosed mass there. The origin limit therefore
   excludes a central atom under appropriate positive-measure assumptions,
   not every possible particle source. Exact continuity of enclosed mass
   at every radius would be a stronger and different assertion; PD05 does
   not formalize it or a particle-source class.
4. **Vanishing mass does not imply smooth density.** Even the formal
   profile \(M(r)=kr\), for \(k>0,r>0\), has
   \(\rho(r)=M'(r)/(4\pi r^2)=k/(4\pi r^2)\): an integrable central
   cusp, not a density smooth at the origin. Thus “SMOOTH field stress” in
   lines 34–36 does not follow from this limit.
5. **No identification with Hilbert stress follows.** Excluding a central
   constant supplies no formula for
   \(T^\phi_{\mu\nu}=-(2/\sqrt{-g})\delta S_\phi/\delta g^{\mu\nu}\)
   and no solution of the associated equations. PD05 contains neither
   that variation nor a stress-tensor identity nor an existence theorem.
   Its theorem name does not strengthen its logical conclusion.

The strongest safe reading is: **a specified linear enclosed-mass profile
has no nonzero additive constant compatible with its stipulated zero
origin limit.** The user's no-dark-matter-particle requirement remains a
legitimate model choice. It should be imposed explicitly when specifying
the gravitational action, then supported by derived field-response and
observable predictions. This addendum neither introduces nor recommends a
dark particle. It separates a valid elementary limit certificate from the
much stronger physical assertion it currently labels.
