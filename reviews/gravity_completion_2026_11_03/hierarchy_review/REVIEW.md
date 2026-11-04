# Independent audit of the unequal-coupling hierarchy reduction

Normalized claim: on the real aligned canonical rigid SU(5) valley, with
positive h, lambda, f and the fixed ratio g/lambda=sqrt(29/200), the COMPLETE
one-loop CW potential has a universal shape after the stated rescaling. The
leading residual-U(1) gaugino self-energy has a universal charged-sector
coefficient at each fixed z. At the inherited rigid CW minimum, this implies
the stated mass-to-sqrt(F_eff) formula and a maximum at the two upper coupling
bounds. The numerical constant is the TP04 minimum coefficient, not a constant
for every background.

**Primary verdict: correct only after these stated restrictions.** There is
no missing power of lambda or factor of 31 in the proposed normalized mass.
Individual representation CW values have scale-log constants, although their
derivatives and their complete sum have the claimed scaling. Maximization is
of m_chi/sqrt(F_eff), or of m_chi at fixed F_eff; it is not maximization of the
unnormalized mass while holding f fixed. This is an audit of internal algebra
using the imported TP04 self-energy formula; its external derivation, gravity
completion and higher-order current/pole matching are outside this review.

## Claim card and dependency graph

The coefficient domain is real h>0, lambda>0, f>0, real X on the stated CP
slice; z=hX/sqrt(c), c=f lambda²h/Delta, Delta=30h²+lambda². The imported CW
prescription is exactly that of `pressure_scan.py`, including its vector
finite constant. Signed thresholds use TP04's auxiliary convention; a physical
mass is the absolute value. The final numerical coefficient is positive in
that convention at z0=7.367143721278508.

The dependency chain is:

1. TP01 valley and representation matrices -> common charged/nontrivial
   mass scale sqrt(c).
2. Exact block supertraces and exact neutral-singlet cancellation -> full
   CW=c² Phi(z) at the critical gauge ratio.
3. The universal derivative -> the inherited stationary z0, independent of
   h/lambda. This transports the existing minimum; it does not prove a new
   uniqueness or global-minimum theorem.
4. U(1) charge support, raw scalar/vector vertices and finite B0 formula ->
   m_chi=g²sqrt(c) H(z), with separate scalar/vector scale-log cancellation.
5. Imported TP04 numerical C_equal at z0 -> normalization of H(z0).
6. The full auxiliary norm and elementary positive derivatives -> the
   two-coupling maximum at fixed raw SUSY-breaking scale.

## 1. Mass matrices and complete CW scaling

Put kappa=g/lambda. Direct substitution gives

    hX=sqrt(c) z, lambda a=sqrt(2c),
    5ga=5kappa sqrt(2c), 5gb=5kappa sqrt(c) z.

For r=2,-3,-1/2, m/sqrt(c)=(1+r)z,
q/sqrt(c)=r sqrt(2), beta/c=1+r. Thus every entry of the two real
scalar 2x2 blocks is c times a dimensionless universal function of z and
kappa. In the broken block the D-term adds the outer product
(5kappa sqrt(2),-5kappa z) with itself. The real-rephased fermion matrix is

    M_F/sqrt(c) = [[(1+r)z, r sqrt(2), 5kappa sqrt(2)],
                  [r sqrt(2), 0, 5kappa z],
                  [5kappa sqrt(2), 5kappa z, 0]],  r=-1/2,

and m_V²/c=25kappa²(2+z²). The unbroken SU(3)/SU(2) blocks are the
upper-left 2x2 matrices. All eigenvalue multiplicities are retained: 8,3,12.

Per generator, exact trace algebra yields:

| Block | multiplicity | STr M²/c | STr M⁴/c² |
|---|---:|---:|---:|
| SU(3) | 8 | 0 | 18 |
| SU(2) | 3 | 0 | 8 |
| broken | 12 | 0 | 1/2-100kappa² |

Therefore the total STr M⁴/c²=174-1200kappa², identically independent of
z. At kappa²=29/200 it vanishes exactly. Applying
log(c u/Q²)=log(u)+log(c/Q²) proves V_CW=c² Phi(z) for the COMPLETE sum.
For an individual representation block the extra c²log(c/Q²) term is
generally nonzero but independent of z. Its z derivative still scales as
c². At other fixed kappa, the same derivative reduction holds with a
kappa-dependent shape and an additive z-independent scale-log term; the
specific z0 and C_equal used here are not transported to a different kappa.

The singlet sector cannot be included in the assertion that all mass
matrices scale with c. With normalized coordinates A_s, B_s along
D/sqrt(30), its superpotential is

    W_s=fX+(h/2)X A_s²-lambda A_s² B_s/(2sqrt(30)).

On the valley A_s=i sqrt(30)a, B_s=sqrt(30)b. Its only potentially
nonzero holomorphic scalar splitting is

    B_AA=h W_X-(lambda/sqrt(30))W_Bs
        =h f lambda²/Delta-(lambda/sqrt(30))sqrt(30)fh lambda/Delta=0.

The singlet chiral matrix has off-diagonal entries
i sqrt(30)ha and -i lambda a, no X-dependent diagonal, and squared
singular values (0,2fh,2fh). Each is duplicated in the real-scalar Hessian.
The resulting real scalar masses squared are (0,0,2fh,2fh,2fh,2fh),
while the Weyl squared masses are (0,2fh,2fh). These cancel term by term
in CW for every h/lambda, including all finite constants. The unbroken
gauge sector is massless and contributes zero to this potential.

Consequently every stationary z and its derivative-sign pattern in the
imported complete one-loop potential are independent of h/lambda at fixed
kappa. The source's z0 minimum is transported by
X0=z0 sqrt(c)/h. The statement concerns this rigid one-loop prescription.

## 2. All residual-U(1) vertices and absence of hidden Yukawa factors

In the source normalization Tr(T_a T_b)=delta_ab, T_D=D/sqrt(30) and the
adjoint representation is [T_D, .]/sqrt(2). A broken root E_ij has
q=(D_i-D_j)/sqrt(60)=+/-5/sqrt(60), so q²=5/12. Each adjoint contains
six roots of either sign, twelve neutral generators and Tr_adj q²=5.
The two chiral adjoints provide 24 charged complex chiral components;
the broken gauge block provides 12 gauge Weyls and 12 massive vectors.
Neutral SU(3), SU(2), X and D-singlet components have zero U(1) charge.

Let E=(I,iI)/sqrt(2), O be the real scalar rotation and U the Takagi
matrix with U^T M_F U=diag(m_I)>=0. For a pure raw U(1) gaugino external
leg the scalar vertex is exactly the gauge derivative

    y_Ia = sqrt(2)g sum_ki (R_D)_ki (EO)_ka* U_iI.

The superpotential Yukawa tensor has two chiral external rows and hence
does not enter this pure gauge external row. R_D annihilates every neutral
component. Thus no h or lambda vertex factor is hidden in the scalar
diagram; its only explicit coupling is g, twice in the self-energy.

The vector vertex is

    G_aI = g sum_bJK Ov_ba (e_D)_J* (R_F^b)_JK U_KI.

Since the external state is a gaugino, R_F acts on the gauge-adjoint
block. A generator has a nonzero commutator with D only in the broken
sector. These vector/Weyl internal states also lie entirely in the
universal charged blocks. Gauge/Goldstone shifts at fixed xi scale with
c as well. Unbroken massless vectors have zero such vertex. This covers
both scalar/Weyl and vector/Weyl terms retained by the source formula.

At fixed z,kappa, charged O,U,Ov can be chosen independently of h/lambda
(basis freedom inside exact degeneracies cancels in the complete sums).
All internal nonzero masses scale as sqrt(c), and y,G scale as g. The
finite B0 function obeys

    B0(cu,cv;Q²)=B0(u,v;1)-log(c/Q²).

Its apparent residual logarithm vanishes separately in the two diagram
classes. For the scalar term, completeness gives
sum_a (EO)_ka* (EO)_la*=(E* E*^T)_kl=0. Combining this with
sum_I U_iI U_jI m_I=(M_F*)_ij annihilates the coefficient
sum_Ia y_Ia y_Ia m_I of the common scale logarithm. For the vector
term the same Takagi identity reduces its log coefficient to the raw
gaugino-gaugino block of M_F*, which is identically zero. Gauge generators
acting on the pure gauge external leg cannot select its chiral/gaugino
off-diagonal block. Neither argument uses a small-splitting expansion.

It follows that the signed projected self-energy is

    m_chi(z)=g²sqrt(c) H(z;kappa)
            =lambda²sqrt(c) K_chi(z),  K_chi=kappa² H,

at every fixed real aligned background where the imported self-energy is
used. A generic off-shell background self-energy is not an occupied-state
quasiparticle pole. At the rigid loop minimum this is the source's leading
vacuum pole threshold. The photino does not mix with the neutral chiral
singlets on this slice: the action and diagonal background preserve the
linear transpose charge conjugation A,B -> A^T,B^T, V -> -V^T. All the
diagonal chiral singlets are even and the D gaugino is odd. A mixed mass
is forbidden. This argument holds for unequal h/lambda, while the source's
equal-coupling null-space controls provide an implementation check.

## 3. Physical normalization and the maximum

At h=lambda=e, c=fe/31, so comparison with the imported TP04 result
m_chi=sqrt(f) C_equal e^(5/2) fixes

    K_chi(z0)=sqrt(31) C_equal,
    C_equal=0.00011164161505832252 approximately.

The full rigid auxiliary norm is

    F_eff=sqrt(sum_i |W_i|²)=f lambda/sqrt(Delta).

In particular F_eff is a mass-squared quantity; sqrt(F_eff) is a mass.
Restoring f gives, with no omitted lambda,

    m_chi/sqrt(F_eff)
      =sqrt(31) C_equal lambda^(5/2) sqrt(h)/Delta^(1/4).

As a normalization cross-check, at equal e this reduces to
31^(1/4) C_equal e^(5/2), as required because
sqrt(F_eff)=sqrt(f)/31^(1/4).

For R=lambda^(5/2)sqrt(h)/Delta^(1/4), exact logarithmic derivatives are

    d log R/d log h = lambda²/(2Delta)>0,
    d log R/d log lambda = (75h²+2lambda²)/Delta>0.

Thus on 0<h,lambda<=L the ratio is maximized at h=lambda=L. If the raw
source condition fixes F_eff²=rho_DE, this yields

    m_chi <= C_equal (31rho_DE)^(1/4) L^(5/2).

The same monotonicity does NOT hold for the fixed-f unnormalized mass:
m_chi is proportional to lambda³ sqrt(h/Delta), and its derivative in h
changes sign at h=lambda/sqrt(30). Any statement of the maximum must retain
the physical normalization or explicitly fix F_eff. Likewise C_equal must
be replaced by K_chi(z)/sqrt(31) at a different background. Gravity can
move the background and add masses; such a problem is outside this result.

## Obligation matrix and remaining scope

| Obligation | Status | Evidence or limit |
|---|---|---|
| Scalar, fermion, vector powers | passed | Exact dimensionless matrices above |
| Individual versus total CW scaling | passed after restriction | Individual constant scale logs retained; total exact critical cancellation |
| Singlet effect on potential/derivative | passed | B=0 and exact singlet spectrum |
| U(1) charge normalization/support | passed | q²=5/12, trace 5 per adjoint |
| Scalar and vector vertices | passed | Raw external gauge projection removes Y; both vertices proportional to g |
| Scale-log cancellation | passed | Scalar completeness and zero raw gauge Majorana block |
| U(1)/neutral-singlet mixing | passed on aligned slice | Preserved transpose charge conjugation |
| Auxiliary norm, powers and 31 factors | passed | Direct substitution and equal-coupling limit |
| Monotonicity/maximum | passed for normalized ratio | Exact positive derivatives |
| Numerical z0 and C_equal | imported numerical input | Existing TP01/TP04 result; no new uniqueness certificate |
| External self-energy formula | not re-audited | TP04 formula taken as named input; no new literature check |
| Arbitrary gauge ratio, all backgrounds, SUGRA, all-loop/no-SUSY theorem | out of scope | Each changes a premise |

No missing internal algebraic implication remains for the restricted
one-loop claim. A claim about a physical spectrum in a gravity-shifted or
rotating state needs the corresponding background and full mass/current
matching. The result is not uniform control of higher-loop corrections
at exponentially extreme h/lambda; large threshold logarithms must remain
within a controlled expansion or be resummed. This does not change the
exact stated one-loop reduction.

## Independent exact control and provenance

The fresh isolated audit was assigned the raw TP01/TP04 artifacts and the
proposed claim. Critical block traces, the normalized auxiliary powers,
the charge normalization and vertex/log argument were reconstructed here;
the original author's derivation was read only afterwards for wording review.
The symbolic script is independent of the source mass-assembly implementation.
The numerical constant and external formula remain shared inputs, not
independent external verifications.

`control_contract.json` preceded execution. `run_exact_001/manifest.json` is
a validated v2 evidence record with status `completed`; the run used exact
SymPy 1.14.0 arithmetic under a 60-second wall/55-second CPU cap and one
numerical thread. Observed RSS was 52,412,416 bytes. Input hashes before/after
pin the exact raw source files audited; they were unchanged during the run.
The observed repository commit was `56749af4221bdba5a92f76535fdb1f3bf9eaa291`,
with dirty state true; the individual source hashes, rather than that commit
alone, identify the artifacts reviewed.
Read-only Git provenance was permitted by the coordinator's clarification;
no Git mutation, package installation or queue access occurred.

The exact result establishes STr M⁴/c²=-6(200kappa²-29), all three
STr M²=0, the singlet characteristic polynomial t(t-2h)², the root charge
normalization, the scalar completeness identity and both logarithmic
monotonicity identities. It does not rerun the coordinator's independent
27-point full-component controls.

Reproduction uses the installed mathbox `run_experiment.py` with the
contract's six `execution_artifacts` supplied as matching `--input` arguments,
a fresh output directory, `--timeout 60 --max-cpu-seconds 55 --max-threads 1`,
and child command `python3 reviews/gravity_completion_2026_11_03/hierarchy_review/control.py NEW_RESULT_PATH`.
The manifest records the exact executable argv and resulting hashes. Validation
command:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/gravity_completion_2026_11_03/hierarchy_review/run_exact_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Audited source locators: TP01 `pressure_scan.py` lines 11-42;
`block_spectrum.py` singlet definition; `spectrum.py` generators, tensor and
adjoint representation; TP03 `two_loop/model.py` component_data/build_model;
TP04 `gaugino_threshold.py` lines 17-62 and `run_003/result.json` first case.
The latter supplies the decimal C_equal value; its number is not claimed exact.

Final mathematical proofreading covered this entire new review. Routine edits:
none required after rereading. Mathematical-token changes: none. Unresolved
issues: only the explicitly stated scope and imported numerical/external inputs.
The v2 manifest validation passed after the exact run; no document build is
specified or needed for this plain Markdown audit.
