# Independent action-level review by the induced-quantum author

2026-10-20. Base `431f22bd6`; criteria-only `89bf113b0`.
This review was made from the raw matrix and flux packets before reading
the coordinator's combined RESULT/verdict. No script, scan, download,
build, Lean run or numerical parameter choice was used. No required
correction remains at the exact hashes below. The general microscopic
normalization and complete formal-bridge goal remains open.

## Artifacts and independence

| Reviewed artifact | SHA256 |
| --- | --- |
| `MATRIX_MODEL.md` | `49605568df5daba99f73b57c5a41a042d5567680a81150af2d2bf85a7fb0edf1` |
| `SOURCES_MATRIX.md` | `1a8620dd2374cface7943ee44ca4da98206a59e63da20b95d5dbe27539601a94` |
| `FLUX_GEOMETRY.md` | `1ef130e0479dff44f961f54a5b7aaadb92dfd13114f3a26babe759f5f588681f` |
| `SOURCES_FLUX.md` | `4c5d8e4c713f12165f6db33438990c9708668c3609c57436106088dd79173c85` |

I authored `INDUCED_QUANTUM.md` and `SOURCES_INDUCED.md`; this is not an
independent review of those files. Their frozen hashes are respectively
`2d3df2d6b09f1195b39d4ce195474406d988e8a7e4f5cb9f292e7c3984291026`
and `3b8767823d429b3a410d19d8e33722cc8d0fa075e0f54d28dc59a30ca4117689`.
The companion calculations below were reconstructed independently,
rather than accepted from a shared verdict. This report is bounded
analytic evidence, not a full microscopic or quantum-health theorem.

## Matrix functional, isolated vacuum variation and source law

I independently authenticated the primary HTML header for
Steinacker `2601.08031v1`, 12 January 2026, and read the actual displayed
equations 1.1,2.40,3.9,3.12--14,3.34--37 and 4.46 with their surrounding
scope. I also authenticated the header of `2303.08012v1`, 14 March 2023,
and read its one-loop/background discussion. I did not rederive the
full fuzzy-spectrum one-loop trace. The numerical spectral factors
remain primary calculations with the extraction pins in SOURCES_MATRIX.

For the isolated vacuum functional, write `q=sqrt|G|` and hold V0 and
the symplectic density fixed. Equations 2.40 and 3.12 give

    S_v=-integral rho_M^2 V0/q,
    delta q=-(q/2)G_mu nu delta G^{mu nu},
    delta S_v=-(1/2)integral q rho^-4 V0 G_mu nu delta G^{mu nu}.

With the actual matter convention in equation 3.9, this means
`T_v,mu nu=+rho^-4 V0 G_mu nu`, and therefore
`epsilon_v=-rho^-4 V0`. The determinant/frame variation also reproduces
equation 3.13. Reversing the trace of that frame source gives the same
plus sign on the Einstein right-hand side. The printed minus sign in
equation 3.14 consequently does not follow from that isolated action
and its declared stress convention. I verified the discrepancy directly
in the HTML; the source card separately records the coordinator's PDF
check. I have not independently repeated that PDF check.

The packet correctly keeps this statement conditional on fixed V0 and
rho_M. Restoring constrained frame variations, other background terms,
dilaton derivatives and the internal-radius equation is necessary for a
full cosmological solution. Neither a positive cosmological energy nor
a global negative-vacuum theorem follows merely from this isolated term.

The radial integration also reconstructs. For
`rho_eff=M delta3+M k^2 cos(kr)/(4pi r)`, the enclosed mass is
`M[cos(kr)+kr sin(kr)]`. The distributional identity for `cos(kr)/r`
gives the quoted potential and its inward-positive force coefficient.
Its first correction is a constant-in-radius acceleration proportional
to `M k^2/2`, and every term remains linear in M at fixed background
and fixed boundary/homogeneous sector. This decisively distinguishes
that linear branch from a deep-MOND square-root source law. It leaves
the nonlinear matrix/dilaton/higher-spin problem open.

For the scalar commuting-mode repair polynomial I independently obtain
the sum, product and discriminant. Strict positivity of its product for
all x>=0 requires `v00<-5u^2/4`; positivity of the root sum and the
discriminant at x=0 gives `v01>u+2sqrt(-v00)`. Under these conditions
the discriminant increases on x>=0, proving the stated sufficient
repair. This is a frequency calculation only. It neither fixes the
coefficients microscopically nor proves positive residues, all-component
health or nonlinear stability. The packet preserves that distinction.

## Flux reduction, canonical source and exact hierarchy

I independently authenticated Seo `2312.03184v2`, 2 May 2024, and
Brown--Dahlen `1310.6360v2`, 23 December 2014. The declared flux/action
normalizations were checked against their primary HTML. In addition to
the source cards, I directly read Seo's radion/KK equations 16--17,
Brown--Dahlen's special scalar equations 142--145 and vector block
immediately before equation 226 with printed roots 228. HTML/PDF label
differences remain as documented by SOURCES_FLUX; I did not independently
read every PDF block or redo every six-dimensional linear Euler equation.

Starting from the declared six-dimensional action, its measure,
curvature and flux norm reproduce
`V=A exp(-psi)-B exp(-2psi)+C exp(-3psi)` and
`chi=M4 psi`. Fixed flux is retained while varying the radion. The two
extrema, their canonical masses, the positive minimum condition
`0<Delta<B/2` and the physical vacuum stress all reconstruct. Normalizing
the reference radius at the minimum gives exactly

    M4^2 m_rad^2=-2B+6C,
    3M4^2 H^2=B-2C,
    m_rad^2+9H^2=R^-2.

The first spin-two sphere harmonic has squared mass `2/R^2`; it must
not be confused with the conventionally named inverse-radius KK scale.
The resulting hierarchy bound
`min(m_rad^-1,H^-1)<=sqrt(10)R` follows directly. More precisely,
`r/R>=L` and `Hr<=eps` imply
`m_rad r>=sqrt(L^2-9eps^2)` when `L>3eps`. Monotonicity of
`(1+x)exp(-x)` gives the packet's sourced Yukawa bound. No parametrically
wide unscreened, subcurvature, four-dimensional force window is inferred
from merely making the radion light.

The specified neutral zero-internal-momentum particle has
`A_m=exp[-chi/(2M4)]`. Its derived charge is
`alpha=-1/(2M4)`. The canonical scalar Green function and conformal
metric map give `G_S=G_T/2`, the attractive Yukawa potential and the
quoted force factor `1+m_rad r`. The on-shell source energy has the
negative nonlocal Green-kernel sign given in the packet; it is not a
positive local gradient cubic. Its nominal unscreened potential ratio
and force coefficient remain conditional on an actual compatible
radius/curvature window, not an already measured ultraviolet G.

At the merged endpoint I recover `V_chi chi=0` but
`V_chi chi chi=-6V0/M4^3`. The retained canonical field sits at a
stationary inflection and cannot be treated as a stable algebraic
auxiliary. This conclusion is action-level, independent of a root label
or a proposed spinodal exponent.

## Flux harmonic spectrum and source discrepancy

For the stated q=2,p=4 specialization, the scalar eigenvalues have
trace `2k_l^2+m_rad^2` and determinant
`k_l^2(k_l^2-2/R^2)`. I recover their displayed discriminant and positive
roots for l>=2, the single physical l=1 scalar, and the fixed-flux l=0
radion. The ordinary kinetic/gauge-constraint hypotheses are essential
to interpreting these as physical stable bosonic modes.

The source's displayed vector matrix has trace `2k_l^2-6H^2`.
Diagonalizing it gives roots centered on `k_l^2-3H^2`, not the printed
`k_l^2+3H^2`. Its determinant reduces to
`k_l^2(k_l^2-2/R^2)` using the background equation. The corrected matrix
roots contain the required massless Killing vector at l=1; the printed
plus-centered roots do not. This narrow source discrepancy is real in
the freshly read HTML. The packet uses the block, explicitly derives
the roots, and does not silently repair an unrelated equation. Its
reported PDF cross-check remains the source-card author's provenance.

The spin-two tower's l>=1 masses exceed the de Sitter Higuchi threshold
in the stated stable range. Within the inherited harmonic decomposition
and ordinary Einstein--Maxwell kinetic signs, the scalar/vector/tensor
specialization is consistent with classical bosonic linear stability.
I have not certified all-matter, nonlinear, quantum or cutoff health.

## Scope verdict

The two models are substantive common-action constructions. The matrix
packet's displayed linear source response does not supply the MOND mass
law, while the retained flux radion supplies a Yukawa field and an exact
scale identity obstructing the required parametric force window. Their
vacuum treatments are varied rather than read from unvaried constants.
Neither packet claims an operational positive C3 or a selected R.
These scoped conclusions pass the present independent audit. No global
no-go, target normalization or complete Lean bridge is established.
