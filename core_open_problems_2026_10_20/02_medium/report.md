# Problem 2: a microscopic saturating medium and the n=1/n=2 choice

Checkpoint **MEDIUM-2026-10-20-A**, 20 October 2026 (America/New_York).
Base: `431f22bd6fe998759b843d13113762d73356aec6`. Owner: medium lane.

**The microscopic selection problem remains open.** Three explicit equilibrium
candidates were derived and tested: fixed-density orientational dipoles, a
Born–Infeld constitutive potential (also realized by a gapped two-level system),
and a finite-capacity binary lattice. None gives the specified remainder. A
vacancy-limited kinetic construction gives its stationary equation exactly,
but neither the coupling to gravitational force nor its coefficients follows
from a microscopic Hamiltonian. Positivity and saturation permit every real
`n>0`; they do not select either integer.

There is a precise distinction to test: with the same fixed `a0` and isolated
spherical baryonic source, the largest circular-speed ratio is
`v(n=1)/v(n=2)=sqrt(2/sqrt(3))=1.07456993` at `gbar=a0/2`.
The existing proposed surface-density test requires a geometry correction.

## 1. Target contract and exact source

The authoritative input is §S2 of
`campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md`, supported by
`argon_push/AG4_law_from_action/ag4_derive.py`. Their hashes, and those of nearby
read-only audits, are in `source_provenance.json`. No source document was edited.
The executable here is self-contained and imports no pre-existing repository
result or untracked file.

Write `K=4πG`, **u**`=K P`, `u=|u|`, **g**`=∇Φ`, and **A**`=g−u`.
The force variables below are magnitudes on the aligned, spherical, static
branch. Physical acceleration is `−∇Φ`; this sign convention does not change
the magnitude relations. The frozen action is

\[
\mathcal L=-\frac{|\nabla\Phi-K\mathbf P|^2}{2K}
 -\rho_b\Phi-W_{\rm rem}(K|\mathbf P|)
 -\frac\gamma2|\nabla\mathbf P|^2,\qquad
\gamma=\frac{K L_*^2}{2}.
\]

Its capacity family, an extension used for this comparison, is

\[
K W_{{\rm rem},n}'(u)=f_n(u):=\frac{u^2}{a_0-nu},\qquad
0\le u<b,\quad b=\frac{a_0}{n},\quad n>0.                 \tag{1}
\]

Here **n is a dimensionless capacity coefficient**. It is not a power in a
virial/snap fraction, a spacetime dimension, or a critical exponent. The
frozen action has `n=1`; the quadratic a0-line has `n=2`. With `W_rem(0)=0`,

\[
K W_{{\rm rem},n}=
\frac{a_0^2}{n^3}\left[-\log(1-nu/a_0)-\frac{nu}{a_0}
 -\frac12\left(\frac{nu}{a_0}\right)^2\right].             \tag{2}
\]

Variation gives `∇·A=Kρ_b` and
`A−f_n(u) P_hat+γ∇²P=0`. At `γ=0`, Gauss's law and alignment give

\[
\bar g=f_n(u),\qquad g=\bar g+u,\qquad
u_n=\frac{\sqrt{n^2\bar g^2+4a_0\bar g}-n\bar g}{2}.       \tag{3}
\]

Thus `n=1` implies `gbar=g²/(g+a0)`; `n=2` implies
`g²−gbar²=a0 gbar`. These are consequences **of the specified potential**,
not a microscopic derivation of it. This checkpoint does not replace S2.

A complete microscopic solution must supply a state, actual source operator,
partition function or dynamical reduction, and parameter selection yielding
(2), including its normalization and gravitational coupling. A bounded response
or a shared stationary root is partial progress. Relativistic completion,
formation, cosmological abundance and the value of `a0` are not supplied here.

## 2. The two endpoint requirements and the analytic-phase obstruction

The function a microscopic polarization model must reproduce is the **full**
polarization free energy,

\[
W_{\rm full}=\frac{u^2}{2K}+W_{\rm rem},\qquad
\mathcal L=-\frac{g^2}{2K}+\frac{\mathbf g\cdot\mathbf u}{K}
 -W_{\rm full}(u)-\rho_b\Phi\quad(\gamma=0).               \tag{4}
\]

Consequently `g=K W_full'(u)` and `gbar=g−u`. Confusing `W_full` with
`W_rem` would compare different constitutive laws.

For every `n>0`,

\[
K W_{{\rm rem},n}=\frac{u^3}{3a_0}
 +\frac{n u^4}{4a_0^2}+O(u^5),\qquad
f_n'(u)=\frac{u(2a_0-nu)}{(a_0-nu)^2}>0\ (0<u<b).         \tag{5}
\]

The radial and transverse eigenvalues of `K Hessian_u(W_rem)` are respectively
`f_n'(u)` and `f_n(u)/u=u/(a0−nu)`, both positive away from zero.
At `u=0`, the remainder, force and remainder Hessian vanish continuously;
`A=0` has the unique rest value `u=0`. The full Hessian is `I/K` there.
At `u→b−`, the force has residue `b²/n`:
`f_n(u)~b²/[n(b−u)]`, and the energy diverges logarithmically.
The endpoint `u=b` is outside the finite-energy domain. Static convexity does
not prove dynamical stability, causality or absence of ghosts in an unspecified
time-dependent completion.

**Restricted obstruction.** Consider finite-temperature equilibrium dipoles
with a bounded vector observable, inversion symmetry, an isotropic zero-source
state, and nondegenerate covariance. The finite-volume partition function
`Z(h)=∫exp(β h·p)dμ(p)` is analytic near `h=0`; its even logarithm has
positive quadratic Hessian. The inverse-function theorem makes its local
Legendre transform analytic and even in the polarization components. Isotropy
therefore gives `c2 u²+c4 u⁴+…`, not `|u|³`. Even if the quadratic coefficient
is tuned to `1/(2K)` so the remainder starts beyond quadratic order, its
generic leading force is `u³`, giving `u∝gbar^(1/3)`, rather than the target
`u∝gbar^(1/2)`. Higher cancellations cannot produce a cubic from an analytic
even series.

This is not an exclusion of all media. It does not cover a singular
thermodynamic limit, a gapless or degenerate quantum state, a nonanalytic
constraint or spatial overlap, a broken-symmetry branch, or a driven system.
A finite gapped nondegenerate quantum system has an analogous analytic
small-source restriction; this does not apply to every quantum phase.
The target `|u|³` is rotationally invariant and C², so symmetry by itself
does not forbid it: **analyticity is the material assumption**.

## 3. Route D: a real saturating orientational dielectric

Use fixed local number density `N_d`, dipole moment `p`, and `T>0`, with
single-site Hamiltonian `−p h cosθ`. Direct integration gives

\[
z(x)=\frac12\int_{-1}^{1}e^{xt}dt=\frac{\sinh x}{x},\quad
m=\partial_x\log z=\coth x-\frac1x=\mathscr L(x),\quad
x=\beta p h.                                             \tag{6}
\]

The orientational trace and the distinction between density and orientation
appear explicitly in Abrashkin, Andelman and Orland,
[arXiv:0705.1269v1, Eqs. (4)–(5), (11)](https://arxiv.org/pdf/0705.1269v1).
Their unconstrained mobile-dipole density need not saturate; fixed density or
a packing constraint is essential. Here fixed density is an explicit input.

Set `u=bm` and `C=N_d k_B T`. The Legendre free-energy density is
`F_D=C[m x−log(sinh(x)/x)]`, where `x=L^{-1}(m)`.
The favorable susceptibility match `K F_D''(0)=1` requires `C=b²/(3K)`.
It is a tuning condition, not a prediction. Subtracting the quadratic in (4),

\[
K W_{{\rm rem},D}'=\frac b3\mathscr L^{-1}(u/b)-u
 =\frac{3u^3}{5b^2}+\frac{99u^5}{175b^4}+\cdots.           \tag{7}
\]

At saturation, `L^{-1}(m)~1/(1−m)`, so the remainder force has a
simple pole `b²/[3(b−u)]`. It gets the *kind* of saturation barrier right
but the small-field order wrong. Matching only this residue to (1) would
suggest `n=3`, not `1` or `2`, and would still fail (5). The full inverse
Langevin function is not a rational law. The finite numerical check uses
five independent orientation integrals and six inverse-function values.

Disposition: the stated independent, isotropic, thermal-dipole construction
fails. Collective critical or nonthermal variants remain open, with the
first required check being their actual small-source nonanalyticity and
physical gravitational source, not another saturation curve fit.

## 4. Route B: Born–Infeld and a quantum two-level realization

The electrostatic Born–Infeld variational density is proportional to
`1−sqrt(1−|E|²/b²)`; its derivative is `E/sqrt(1−|E|²/b²)`.
This functional is explicit in Haarala,
[arXiv:2006.08208v2, p. 1](https://arxiv.org/pdf/2006.08208v2).
We use the constitutive density, not his regularity theorem. The original
1934 paper's publisher endpoint was inaccessible, and the scanned mirror
did not provide an inspectable formula through the available browser; no
verification of its exact equation numbering is claimed.

Giving the analogy its most favorable dictionary, identify the bounded field
with `u` and the conjugate with `g`, and choose

\[
K F_{\rm BI}=b^2(1-\sqrt{1-u^2/b^2}),\quad
\bar g_{\rm BI}=\frac{u}{\sqrt{1-u^2/b^2}}-u
 =\frac{u^3}{2b^2}+O(u^5).                               \tag{8}
\]

Its force diverges as `(b−u)^(-1/2)`, while its full and remainder
energies remain finite at `u=b`. The target needs a pole of order one and
logarithmically infinite energy. Calling `u` the Born–Infeld displacement
instead would remove the upper bound, since that conjugate is unbounded.
An electromagnetic constitutive analogy does not derive a gravitational
polarization operator or its source term.

There is an actual microscopic control with the same shape. Take a two-level
Hamiltonian `H=−Δ σ_x−p h σ_z`, `Δ>0`, at zero temperature. Its ground-state
energy is `−sqrt(Δ²+p²h²)` and `m=p h/sqrt(Δ²+p²h²)`.
For independent sites, Legendre transformation gives
`F=N_d Δ[1−sqrt(1−m²)]`. Setting `u=bm` and `N_d Δ=b²/K` gives (8).
The spectrum therefore explains this candidate's saturation and also
demonstrates its mismatch. Five direct 2×2 eigensolves check the dictionary.

A logarithm alone does not repair it. The symmetric convex choice
`K F_log=−(b²/2)log(1−u²/b²)` gives
`gbar=u³/(b²−u²)`. It has a logarithmic barrier but still the wrong
small-field order. This is the pure-electric form of the explicitly posited
model in Gaete and Helayël-Neto,
[EPJC 74 (2014) 2816, Eqs. (3), (8)](https://doi.org/10.1140/epjc/s10052-014-2816-4),
after `b=sqrt(2)β`. Neither paper claims to derive the repository action.

Disposition: standard BI, its finite gapped two-level realization, and the
displayed symmetric logarithmic control fail. Different gapless spectra or
constraints are untested, rather than excluded by this calculation.

## 5. Route L: finite-capacity lattice statistics

For a site with states `s=±1`, energy `−ε s`, and `x=βε`,
`z=2cosh x`, `m=tanh x`. If a site instead has occupancy `0/1`, setting
`m=2θ−1` gives the same entropy after shifting the source reference.
The exact mixing free energy relative to its unpolarized minimum is

\[
F_L=C\left[\frac{1+m}{2}\log(1+m)
 +\frac{1-m}{2}\log(1-m)\right],\qquad m=u/b.              \tag{9}
\]

Excluded-volume lattice models genuinely produce finite occupancy: see the
mixing entropy and saturation formulas in Borukhov, Andelman and Orland,
[PRL 79 (1997) 435, Eqs. (2), (5)](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.79.435/fulltext).
This supplies a statistical mechanism for capacity; it does not identify
occupancy with the action's polarization.

Matching the zero-field susceptibility requires `C=b²/K`, giving

\[
K W_{{\rm rem},L}'=b\operatorname{artanh}(u/b)-u
 =\frac{u^3}{3b^2}+O(u^5).                                \tag{10}
\]

The force grows only logarithmically at the endpoint and the full energy
approaches `b² log(2)/K`, a finite value. Both endpoint and origin disagree
with (2). Mean-field interactions may cancel the quadratic term but leave
an even analytic expansion unless a separate singular limit is established.
Increasing the number of finite local states does not bypass §2's analytic
restriction at positive temperature.

Disposition: ordinary finite-state equilibrium packing fails as an exact
origin. A specifically derived singular collective limit remains a separate
open route. A count of available slots cannot by itself determine `a0/b`.

## 6. Constructive kinetic route: the correct root, but a missing force coupling

The following local rate equation does preserve finite capacity and produce
the exact stationary family:

\[
\dot u=\Gamma[\bar g(a_0-nu)-u^2],\qquad\Gamma>0.          \tag{11}
\]

Its units require `Γ` to have units `(acceleration×time)^(-1)`.
At `u=0`, the derivative is nonnegative; at `u=b`, it is negative. The closed
interval is forward invariant. For `gbar>0` there is one admissible stationary
root (3), with exponential linear relaxation rate

\[
\lambda_n=\Gamma(2u_n+n\bar g)
 =\Gamma\sqrt{n^2\bar g^2+4a_0\bar g}.                    \tag{12}
\]

At `gbar=0`, decay is instead algebraic,
`u(t)=u(0)/(1+Γu(0)t)`. With `u_±=(-n gbar±D)/2` and
`D=sqrt(n² gbar²+4a0 gbar)`, the exact positive-source trajectory obeys
`(u−u_+)/(u−u_−)=[(u(0)−u_+)/(u(0)−u_−)] exp(−ΓDt)`.
The implementation compares 18 trajectories, 41 times each, and two
zero-source controls to independent ODE integration.

For constant source, (11) is also a positive-mobility gradient flow:

\[
\dot u=-\Gamma K(a_0-nu)\partial_u
 \left[W_{{\rm rem},n}(u)-\frac{\bar g u}{K}\right].        \tag{13}
\]

This establishes consistency with an *assumed* potential and mobility. It
does not derive either from a conservative action, nor does it add a time
equation to the frozen S2 action.

There is a concrete mass-action resemblance. For `S ⇌ X+Y`, with
`[X]=[Y]=c`, `[S]+c=C`, equilibrium gives `c²/(C−c)=k_d/k_a`.
Put `u=ℓ c`, `b=ℓ C`. To identify this with (1), one needs
`ℓ k_d/k_a=n gbar` and `a0=nb`. Neither relation is fixed by the
stoichiometry. At finite-temperature detailed balance with a source that
couples linearly to an elementary reaction dipole, the equilibrium constant
has the form `K_d(gbar)=K_d(0)exp(β Δp gbar)`, rather than a quantity
proportional to `gbar`. Exactly linear activity would require an imposed
logarithmic source-dependent reaction free energy; exact `K_d(0)=0` is
also not a finite-gap finite-temperature equilibrium constant.

The ideal mixing chemical potential is proportional to
`log[c²/((C−c)K_d)]`. It has the same root if `K_d` is fitted appropriately,
but is not the mechanical force `f_n(u)−gbar`. The kinetic Lyapunov
potential can be manufactured from that root and a mobility; this does
not identify it with the thermodynamic energy. Two reactions or two slots
do not force `n=2`: `n=a0/b` still compares an independently normalized
weak-field scale with a capacity.

There is a conditional extra discriminator: if the two variants have the
same `Γ`, then at `gbar=a0/2`,
`λ2/λ1=2/sqrt(3)=1.15470` and `τ2/τ1=sqrt(3)/2=0.866025`.
The original static action predicts no value of `Γ`, so this is a prediction
of the declared kinetic completion only. Its detailed-balance source bridge
and stoichiometric normalization remain open.

## 7. A near-miss already in the repository: Gamma compression

The nearby read-only note
`sol61_push/nonlinear_origin_2026_10_19/canonical_response/CANONICAL_RESPONSE.md`
contains a useful positive construction. An isothermal harmonic cloud gives
a Gamma-distributed quadratic width `Q` and response
`p(E)=Q0 E/(a+E)`. Its one-sided Legendre transform can have the logarithmic
shape of `W_full,1`. This observation is retained as adjacent evidence,
not newly claimed here.

The acting source is a curvature increment and the responding observable is
a mass second moment, not the acceleration-coupled vector dipole in (4).
The width deficit is bounded above but unbounded below. Its odd vector
continuation and its susceptibility normalization do not follow. An
adiabatic receiver changes the response power. Thus this route avoids §2's
bounded-vector hypotheses for an identifiable reason, but that same reason
prevents promoting the scalar compression law into a solution. The local
note's hash is recorded; it is not needed to reproduce the present checks.

## 8. Quantitative n discriminator on a stated footing

Fix the same `a0`, baryon distribution, and isolated spherical `γ=0` branch.
Let `y=gbar/a0`. Then

\[
\frac{g_1}{a_0}=\frac{y+\sqrt{y^2+4y}}2,\qquad
\frac{g_2}{a_0}=\sqrt{y^2+y}.                             \tag{14}
\]

Both share the leading deep-field scale. Their distinction cannot be absorbed
by changing a0 while also preserving that common asymptote. For a circular
orbit at the same radius, `v1/v2=sqrt(g1/g2)`. With
`z=sqrt(1+4/y)>1`,

\[
\frac{g_1}{g_2}=\frac{z+1}{\sqrt{z^2+3}},\qquad
\frac{d}{dz}\frac{g_1}{g_2}=\frac{3-z}{(z^2+3)^{3/2}}.     \tag{15}
\]

Hence the global maximum for `y>0` is at `z=3`, or `y=1/2`:

\[
g_1=a_0,\quad g_2=\frac{\sqrt3}{2}a_0,\quad
\max\frac{g_1}{g_2}=\frac2{\sqrt3},\quad
\max\frac{v_1}{v_2}=\sqrt{\frac2{\sqrt3}}=1.0745699318.    \tag{16}
\]

For an illustrative `10^10 M_sun` point baryon source, `r=√2 r_M`,
`r_M=sqrt(GM_b/a0)`. The two frozen a0 footings are kept separate:

| a0 footing (m s⁻²) | r at maximum (kpc) | v1 (km s⁻¹) | v2 (km s⁻¹) |
|---|---:|---:|---:|
| canonical `9.3603×10⁻¹¹` | 5.45785 | 125.554 | 116.841 |
| alternative `1.1312×10⁻¹⁰` | 4.96474 | 131.642 | 122.506 |

This is a kinematic prediction from the two effective laws, not evidence
favoring one and not a microscopic prediction of n. A real measurement needs
an independently constrained baryonic acceleration, external-field and
noncircular-motion control, and a solution for non-spherical geometry.
No new dataset, stellar-mass fit, or lensing closure is used here.

Finite stiffness matters. For the point-source algebraic profile
`u/a0=q_n(x)=2/[n+sqrt(n²+4x²)]`, `x=r/r_M`, the omitted-force residual is

\[
\epsilon_n=\frac12\left(\frac{L_*}{r_M}\right)^2
 x^2\left|q_n''+\frac{2q_n'}x-\frac{2q_n}{x^2}\right|.     \tag{17}
\]

At `x=√2`, its coefficients multiplying `(L*/r_M)²` are `17/27`
for n=1 and `5/(6sqrt(3))` for n=2. The separate self-contained supplement
`run_stiffness/residuals.csv` evaluates the relevant lengths. All entries
below are fractional omitted-force residuals, not percentages:

| footing | n | L*=5.75 pc | L*=24 pc | L*=1 kpc |
|---|---:|---:|---:|---:|
| canonical | 1 | `1.398×10⁻⁶` | `2.435×10⁻⁵` | `0.04227` |
| canonical | 2 | `1.068×10⁻⁶` | `1.861×10⁻⁵` | `0.03230` |
| alternative | 1 | `1.689×10⁻⁶` | `2.943×10⁻⁵` | `0.05109` |
| alternative | 2 | `1.291×10⁻⁶` | `2.249×10⁻⁵` | `0.03904` |

The 5.75 pc column is the historical S2 lower scale, not the current primary
globular-sample bound. `CFG820_stiffness_from_globulars/README.md` reports
`L*≥24.0 pc` canonical and `24.7 pc` alternative (95%, sample dependent);
24 pc is used as a common arithmetic comparison here, not as an alternative
footing confidence limit. `PARAMRED_2026-10-16/C_LSTAR/README.md` explains
that 1 kpc was a grid edge and reports soft, approximation-conditional
upper edges of 2.04/2.14 kpc. These contextual results were read, not rerun.

These are residuals of the trial profile, **not a rigorous bound on the
finite-stiffness solution or its velocity error**. The exact comparison is
at `γ=0`; using it observationally at finite L* requires the regular,
weak-stiffness branch or an actual boundary-value solve. At 1 kpc the
residual is already several percent, so the lower-length examples cannot
certify the whole current parameter window.

## 9. Correction to the existing surface-density proposal

In a spherical geometry, `M_ph(<r)=u r²/G`. Therefore
`M_ph(<r)/(πr²)=u/(πG)<a0/(nπG)`. This is the mean **three-dimensional
enclosed mass divided by projected disk area**, not an integral through the
line of sight. It is also not the infinite-sheet surface density.

For a symmetric planar sheet, Gauss's law instead gives
`g_ph=2πG Σ_ph`; thus `Σ_ph<a0/(2πGn)`. At the canonical footing:

| Quantity | n=1 cap (M_sun pc⁻²) | n=2 cap (M_sun pc⁻²) |
|---|---:|---:|
| spherical `M_ph(<r)/(πr²)` | 213.716 | 106.858 |
| planar sheet `Σ_ph` | 106.858 | 53.429 |

Furthermore, in the `γ=0` spherical point-source control, saturation gives
`ρ_ph(r)~b/(2πG r)` as `r→0`. Its central projected column diverges
logarithmically: integrating only a fixed small-radius cusp already yields
`Σ(R)~b/(πG)log(const/R)` as `R→0`. A finite stiffness or source core changes
that center, but it does not turn the spherical enclosed-mass identity into
a general projected-density ceiling.

Accordingly, AG4's unqualified “lensing/edge-on sheet in (107,214] excludes
n=2” proposal does not follow from its spherical calculation. It needs a
specific geometry, deprojection and a lensing law. Equations (14)–(16) avoid
that particular ambiguity. No historical AG4 file or frozen criterion was
changed by this audit.

## 10. Evidence, review status, and continuation

The strongest result is a **restricted equilibrium obstruction plus an exact
conditional discriminator**, with a constructive but unclosed kinetic route.
The original microscopic selection claim is **incomplete**: the smallest
missing implication is a microscopic source/observable/ensemble that yields
`W_full=u²/(2K)+u³/(3Ka0)+…` and the exact simple pole, then fixes `a0/b`.

| Route | Executed decisive check | Current disposition |
|---|---|---|
| D: orientational dielectric | partition integral, Legendre derivative, both endpoints | specified independent thermal model fails; collective alternative open |
| B: BI / gapped two-level | constitutive derivative, exact 2×2 ground state, pole order | specified model fails; other quantum phases open |
| L: binary packing | exact finite trace and entropy derivative | specified equilibrium model fails; singular collective limit deferred |
| K: finite-capacity kinetics | invariant interval, exact stationary root, relaxation solution | conditional construction; source and rate selection unresolved |
| G: Gamma compression | nearest prior derivation and source dictionary examined | adjacent positive scalar result; vector/source bridge unresolved |

`run_002/manifest.json` is a validated v2 evidence record with status
`completed`; all **75** checks passed, including the exact identities,
10 force integrals, 5 orientation traces, 5 binary traces, 5 quantum controls,
6 Langevin inversions, 18 positive-source trajectories and 2 zero-source
trajectories. The finite assertion is in `contract.json`; runtime versions,
hashes, tolerances and exclusions are recorded. Numerical calculations use
double precision; they support only the listed controls. Uniform statements
above rest on the displayed derivations, not on sample counts.

`run_001` is a retained failed implementation check: SymPy did not automatically
replace `atanh(u/b)` by its real logarithmic form on `0<u<b`. The original
script is retained as `run_001/input_snapshot.py`; the fix expands that exact
identity on its declared domain. No physical formula changed. Its original
manifest's input path is now superseded by the revised script; use the
snapshot hash when inspecting that historical failure. It is not the current
passing evidence.

`run_stiffness/manifest.json` is separately validated with status `completed`:
12 arithmetic evaluations and eight length-squared scaling checks passed.
This supplement changes no result in the primary run and supplies no new
observational constraint.

Self-review using proof-audit reconstructed (1)–(5), the three independent
traces and Legendre dictionaries, the rate/source distinction, the global
maximum (15), and both density geometries. The dependency leaves are:
the frozen action and branch assumptions (inputs); partition traces and
algebra (internal derivations); external constitutive formulas (verified in
`sources.json`); numerical controls (`run_002`); physical realization of
the source and scale (open). Endpoint, sign, domain and units obligations
passed within the stated restrictions. A finite-stiffness global error bound,
relativistic lensing and formation dynamics were not addressed. This is
**self-review**, not an independent audit or a formal proof certificate.
Proofread-math self-review covered this complete new report; no unresolved
notation or cross-reference issue remains. No existing manuscript was edited.

Next executable work is to derive the **actual** source operator and
field-dependent reaction affinity for a proposed finite-capacity microscopic
Hamiltonian, including `gbar→0`, before fitting any n. If that construction
remains an analytic equilibrium phase, §2 rules out its exact target and
the route must supply a specified singular or driven limit. A gapless
collective candidate should first compute the sign and coefficient of
`|P|³`; generating that term would still leave the capacity pole and n
selection as separate obligations. A one-sided Gamma realization must first
solve its vector source bridge. These are deferred continuations, not proofs
that every remaining model is impossible.

Reproduction, from the repository root (choose a fresh output name):

```bash
python3 core_open_problems_2026_10_20/02_medium/check_medium.py /tmp/medium-check-output
```

For a new audited record, reuse `contract.json` and the documented
computation-audit runner with `check_medium.py` as its sole execution input;
the exact original argv is in `run_002/manifest.json`. No network, source
cache, observational dataset, or untracked repository file is required.
