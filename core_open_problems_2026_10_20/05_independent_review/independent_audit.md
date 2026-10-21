# Independent audit of the covariant S2 candidate

**Primary verdict: correct only after the stated background and principal-symbol
restrictions.** The exact P=0 Minkowski scalar reduction, frozen-P tensor
principal block, and leading weak-static S2 recovery independently agree with
the candidate. This is not a proof of the full relativistic completion.

Base checkpoint: `431f22bd6fe998759b843d13113762d73356aec6`.
Reviewer: `/root/horizon_normalization`, separate from the author.
Scope: the action supplied directly by the coordinator, with K=4 pi G>0,
beta,eta,gamma>0 and a physical spatial **covector** P. Write scope is this
directory only. No external theorem or network source was needed.

## Independence and chronology

I first received only the candidate action and definitions. Before opening
`03_relativity/report.md` or `checks.py`, I derived the ADM identities, scalar
constraints and reduced action, pure TT block, and weak-static action. That
derivation was written to `raw_derivation.md`; a separately authored script
then executed 16 symbolic checks. Only afterwards did I read the candidate
report and checks for comparison. The equations agree. The initial input did
not include the author's proposed scalar reduction, so the key lapse/shift
elimination was independently reconstructed. This review does not independently
certify sections of the candidate outside the assigned scope.

## Decisive scalar calculation

Unitary clock gauge T=t gives exactly

    P_0=N^i P_i,
    E_i=N^(-1)[dot P_i - N^j partial_j P_i - P_j partial_i N^j].

Thus E has no hidden lapse or spatial-metric time derivative in these variables.
For `N=1+phi`, `N_i=partial_i B`, `h_ij=e^(2zeta)delta_ij`,
`P_i=partial_i sigma`, and k>0, write b=Delta B. The unreduced scalar action is

\[
L_g=\frac{-(6+9\beta)\dot\zeta^2+(4+6\beta)\dot\zeta b-\beta b^2
 +2k^2\zeta^2+4k^2\phi\zeta}{4K},
\]
\[
L_P=k^2\phi\sigma-\frac K2k^2\sigma^2
 +\frac\eta2k^2\dot\sigma^2-\frac\gamma2k^4\sigma^2.
\]

The lapse gives `zeta=-K sigma`, and the shift gives
`b=(2+3 beta) dot zeta/beta`. These cancel the k² scalar potential exactly:

\[
L_{\rm red}=\frac12(C+\eta k^2)\dot\sigma^2
 -\frac\gamma2 k^4\sigma^2,\qquad C=K(2+3\beta)/\beta,
\]
\[
\omega^2=\frac{\gamma k^4}{C+\eta k^2}>0.
\]

This is identical to the author's expression after `zeta=-K sigma`. There is
one scalar with positive quadratic kinetic coefficient for the specified
nonzero-k sector. The derivation divides by k² and beta: it says nothing about
the homogeneous or beta=0 constraint strata. It also leaves strong coupling
and nonlinear constraint propagation open.

**Additional check:** if `t=eta k²/C`, then

\[
v_g^2=\frac\gamma\eta\frac{t(t+2)^2}{(1+t)^3},\qquad
\max v_g^2=\frac{32\gamma}{27\eta}\quad(t=2).
\]

Thus `gamma<=eta` limits phase speed and the high-k limit, whereas bounding
every group velocity by the metric light speed requires `gamma/eta<=27/32`.
This does not by itself decide signal causality in the full constrained system.
The author calls its limit a front-speed limit and does not claim a group-speed
bound, so no correction to the displayed spectrum is needed.

## Tensor principal block

Freeze local coefficients at constant spatial P, with arbitrary orientation
relative to the wavevector. For transverse traceless h,

\[
\delta(D_iP^i)|_{\partial h}
 =-P_j\partial_i h_{ij}+\tfrac12P_i\partial_i h_{jj}=0.
\]

Exterior F has no connection term; E has no metric time derivative when P_i is
independent; the linear expansion is proportional to `dot tr(h)`. Therefore
the Hodge stiffness, electric term and beta term add no quadratic pure TT
derivative term. The potential is algebraic. The residual coupling
`h_ij P_j partial_i(delta N)` also vanishes for TT at principal order. Hence

\[
L_{TT,\rm principal}=
 [\dot h_{ij}\dot h_{ij}-\partial_lh_{ij}\partial_lh_{ij}]/(16K).
\]

An explicit connection calculation for a z-directed wave gives, for the
*different* rough-gradient operator,

\[
|\delta(D_iP_j)|^2=
\tfrac12k^2|P|^2(h_+^2+h_\times^2).
\]

This independently agrees with the author's adversarial control. The Hodge
choice genuinely matters. The result is a regular local geometric-optics
statement; it does not certify a singular constraint system, all mixed modes,
finite-frequency effects or stability of an actual polarized solution.

## Static lifting and limits

For static shift zero, E=theta=0. At leading weak-field order, variation of the
spatial metric gives zeta=-phi. The EH term becomes `-|grad phi|²/(2K)`, while
the polarization terms give `P dot grad phi-W_full`. The Fourier identity

    (k dot P)² + |k_i P_j-k_j P_i|²/2 = k²|P|²

establishes the flat-space Hodge/rough-gradient equality after integration,
with the appropriate boundary conditions. Thus the expanded S2 action is
recovered, or equivalently its completed square with W_rem. No immediate
algebraic obstruction to this restricted lifting was found. Equality of the
two derivative operators on arbitrary curved slices is not being asserted.

The comparison report correctly adds an important physical restriction:
Minkowski with finite a0 is an auxiliary family in which Lambda and a0 are
independent. If S1 fixes a0 from cosmological-constant dark energy, Lambda=0
also sets a0=0. Consequently the present flat calculation does not certify the
physical finite-a0 zero-acceleration endpoint. That endpoint requires the
de Sitter/clock/polarization calculation named in the author's open work.

## Obligation matrix and remaining gap

| Obligation | Independent outcome |
|---|---|
| ADM covector electric identity | Passed by direct constraint substitution |
| Minkowski scalar lapse and shift reduction, k>0 | Passed |
| Positive quadratic scalar spectrum, positive coefficients | Passed in that sector |
| Pure TT principal derivative block at frozen P | Passed |
| Leading static S2 recovery | Passed with weak-field and boundary hypotheses |
| Physical S1-linked de Sitter endpoint | Not addressed; smallest endpoint gap |
| Author's aligned polarized failure inequality | Outside assigned review; not independently certified here |
| General on-shell polarized solution and oblique reduced spectrum | Not addressed |
| PPN, preferred frame, S3 mass/current bridge, nonlinear well-posedness | Not addressed |

The strongest safe statement is that this is a concrete covariant candidate
with the checked static limit and selected healthy linear sectors, not a full
completion. The cheapest decisive next calculation is the de Sitter endpoint
with S1 enforced, or the complete constrained quadratic action on an actual
polarized static solution after imposing the author's necessary shift margin.
Passing the present checks does not replace either calculation.

## Reproduction

From repository root, Python 3.9+ and SymPy 1.14.0:

```sh
python3 core_open_problems_2026_10_20/05_independent_review/check_independent.py /tmp/covariant-independent-results.json
```

The script has no repository imports and writes only the requested JSON.
`results.json` preserves its initial 16-check output. `run_001/manifest.json`
records a bounded repeat with input hashes; `source_provenance.json` separately
pins the post-derivation author artifacts that were compared. The script
checks the algebra, not the physical applicability of every background.
