# FGF051 independent author comparison audit

**Primary verdict: proved as written.** This verdict applies to the bounded
local claim in the author's Section 1: actual coupled evolution on two
bounded-speed edge cones, its stated initial resonance coverage, regularity,
comparison-time local feedback bounds, and matching on an existing common
classical domain. It does not establish the full-cone compression objective.
No blocking mathematical finding or author correction is needed.

Author raw proof audited:
`deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-051/fgf051_run_001/DERIVATION.md`
SHA256 `37a88c86cd0ba56c1d30e10d79a68fda0dc2160313ae976712ab39f470418ac3`.
Author result SHA256 `68b14fe077402130b4e2de77ee32039198bbaee321b835191ed595648b0c9502`;
author freeze SHA256 `c81ae0add6c027ad3f54534199860bad23178815cfa139483b55983cbfadd50e`.

## 1. Independence and exact evidence chronology

The independent reviewer /root/fgf051_reviewer verified the task and all ten
ancestry pins before reading ancestry mathematical text. The framework and
result contract were read. The additional raw FGF047 construction was verified
against its pinned reconciliation hash before use. These sources supplied
only earlier accepted work, not any new FGF051 proof or verdict preview.

The reviewer then independently derived the local construction and froze
INDEPENDENT_DERIVATION.md with SHA256
`0579a7566496ef880822e2d0f1a4b00279494daf7a87e43a4124a55cc59a4d1c`,
independent_freeze.json with SHA256
`25637e3034ec0a62e8d411104f10df575cccad8d6da8118375e06f6f66610daa`,
and input_sha256.json with SHA256
`e942d9f02cda6f9bd423ec6992f1c17ed0763a53c77cd997fd502b95b5aac0a6`.
The parent received those pins before sending author proof pins.

After receiving the author's final pins, the reviewer verified all three
above and recorded AUTHOR_EXPOSURE.json BEFORE reading the raw proof.
The entire raw DERIVATION was read first and checked against the independent
construction; only afterward were result.json and FREEZE.json read. Failed
estimates and provenance were then read. The author verifier and reviewer
verifier were inspected as source before execution. Both perform reads,
hashing, comparisons and stdout output only; neither writes or refreshes pins.
The author verifier passed 13 source entries, ten ancestry pins and eight
frozen artifacts. The reviewer verifier passed 14 input entries, ten ancestry
pins and three independently frozen artifacts. No old freeze was edited.

No new FGF051 coordinator proof or other reviewer proof was consulted. There
were zero mathematical executable computations, numerical tests, literature
lookups, services, or agents spawned by this reviewer. Administrative SHA256
checks are not scientific experiments. Mathbox proof-audit governed the raw
review; proofread-math was used for self-review of these written artifacts.
No mathematical-token correction to the frozen independent proof was needed.

## 2. Normalized claim and dependencies

Fix positive physical coefficients and a smooth compatible background with
rho>0 and phi0_x>0. All coefficients and background choices are independent
of N. Use X=(x-x*)/L and theta=v0 t/L, P=N^(7/2). For every sufficiently
large integer N the original C1,1 packet, restricted to the two outer strips,
has actual coupled classical local solutions through k_edge/P. Fixed inner
strips persist; they contain all specified initial roots and the indicated
labeled paths. For each fixed B_*>0, theta_N=B_* N^-4 is included for all
sufficiently large N. The resulting local adverse integral is bounded by
an O(N^-4) background term plus O(N^-5) generated excess in fixed units.

Dependency chain checked directly:

1. Exact packet polynomial and fixed background speed bounds establish
   bounded local amplitude, first-gradient O(P), derivative-Lipschitz O(P^2),
   and the initial root inclusion.
2. Auxiliary data agree with original data on the entire outer strip and
   preserve compatibility; they have the bounded amplitudes needed for a
   fixed local speed. The actual physical coefficients remain fixed.
3. The full seven-coordinate characteristic system includes pressure, both
   Q modes, both scale modes and the chi equation. No speed separation is used.
4. The finite-N characteristic iteration constructs a C1/C1,1 start and any
   compatible restart. Block inequalities give strict uniform state and
   first-gradient bounds through k_edge/P.
5. Linear higher-norm propagation gives finite C1,1 endpoint traces for every
   fixed N; restart and uniqueness supply the actual asserted lifespan.
6. Constraints reconstruct C2 potentials and the actual dynamic MOND source.
7. Bounded local speeds and a genuine outer buffer yield the protected cones.
   Comparing along the constructed solution's characteristics establishes
   exterior independence and matching on existing common classical domains.
8. Higher field-gradient estimates integrated twice give the actual local
   feedback budget; complete energy and the hydrostatic control follow from
   the original compatible equations.

Every load-bearing proof step is raw internal mathematics. The result does
not rest on a scientific computation or an external PDE theorem whose exact
hypotheses have not been checked. FGF047 supplies a corroborating pinned
construction, and the author reproduces the needed iteration in Section 4.

## 3. Decisive mathematical checks

### Profile and complete stated initial coverage

For inward u=P|X-X_e| on a packet half,

  v_N=u^2(2-u/sqrt(N))^2,
  |v_N,X|=4P u(2-u/sqrt(N))(1-u/sqrt(N)).

On u<=D with D<=sqrt(N), these imply v_N<=4D^2 and |v_N,X|<=8DP.
The exact f'' bound is 8 almost everywhere, so Lip(v_N,X)<=8P^2,
including the unchanged joins because f' is continuous and zero there.
The cutoff derivative constants C_v and C_h in (3.5) follow from the product
rule, with factors 2 in the mixed second-derivative term correctly retained.

The lower bound v_N>=u^2 on the entire half proves every root with positive
value at most b_bar+c has u<=sqrt(b_bar+c)=r_*. It applies to b0, b0+c,
and positive b0-c,c-b0 even when b0 varies spatially. The intermediate value
argument proves existence of the required first two types on each half.
Outside the support those two types cannot occur. The author correctly
excludes arbitrary exterior coincidences v=0,b0=c from its localization claim.
No nonsonicity assumption or finite number of crossings is silently added.

### Exact chart, starts, and bootstrap

The Q plus mode has speed -b, the minus mode +b. The R sources include both
B_chi k/tau and h_chi(w∓bk). The source depends on exp(q), so no static
source substitution is present. The field inverse needs b>0 and fixed c,d>0,
not pairwise distinct characteristic speeds. Equations (5.1) follow from
D_i z_i,X=-(Dlambda_i.z_X)z_i,X+H_i,q q_X+D_zH_i.z_X;
|q_X|<=A/c and |v_X|<=A are valid in the induced max norms.

In (5.3) all denominators are positive. Substituting A<=a1P and Bf<=beta
into their integrals at theta<=k/P gives exactly (5.4), since P>=1.
The material q estimate gives at most a1k<=1/2. The same-point field
estimate leaves delta/2. Fluid invariant amplitudes, including the actual
force source, give |v|<=V_e+cQ0+g_bar. The source/state/velocity cutoffs used
for starts are consequently inactive; they do not change the bootstrap PDE.

Section 4's derivative-Lipschitz bound is not used for a uniform starting
time: every finite N permits a sufficiently small positive time satisfying
its K,H and contraction gates. The finite-difference interpolation correctly
upgrades the uniform C0 limit to spatial C1; the PDE then supplies continuous
time derivatives. This is a real construction rather than an eigenvalue test.

### Higher norms and endpoint compatibility

The second fluid derivative equation contains -2v_X r_XX-v_XX r_X-g_XX,
so 3A Hf+G Hz+G2 Bf^2 is a valid bound. The field version gives exactly
(6.1), including Hf/c, L2 Bf^3, and the quadratic source term. The initial
H0 is O(P^2); the differential coefficient is O(P) and the inhomogeneous
term O(P^2). Thus (6.2) gives H<=C_H P^2 on k/P. The argument never
replaces the original C1,1 join by a C2 datum.

For each fixed N the a.e. formula (6.3) has bounded right side; distributional
integration gives a uniform-in-space time Lipschitz bound for U_X. The
endpoint has a genuine C1,1 trace, finite amplitude and strict state margins.
Restart need not have a uniform-in-N duration. Local uniqueness glues it,
so the no-finite-endpoint argument reaches k/P. The author correctly keeps
chi_X=k through the limit, derives g_theta=p_X before using the scale
constraint, and only then removes b h_chi(chi_X-k) from p_theta. Both C2
potentials and B_X=C exp(q)+tau phi_thetatheta follow.

### Fast exterior, local uniqueness and the true buffer

The bounds Sk<=(R_o-R_i)/2 and Sk<=(R_i-r_*)/2 preserve both the fixed
inner strip and every labeled characteristic launched from an initial root.
All backward paths used for the estimates stay in the shrinking outer cone.
The cones are disjoint and within the original background patch for large N.

The decisive comparison is (9.2): integrate the difference using U's local
characteristics, and bound the coefficient difference times the competitor's
finite first derivative. The competitor V need not have a speed bound
independent of N. For each common compact classical cone C_V is finite and
D(theta)<=C_V int D forces equality. This resolves the incoming fast-core
concern in the exact class stated. Using the global O(N) speed to choose the
cone slope would fail, but that is not the author's argument. The comparison
requires the competitor to exist and be classical on the whole common cone;
it does not construct a whole-packet branch after its possible breakdown.

### Feedback, signs, and units

The author proves Hz(theta)<=(Hz0+D_z P^2 theta)exp(E_z theta). Integrating
Lip(p_X)<=Hz in g-g0=int p_X gives (8.4). At theta_N=B_*N^-4,
P^2 theta_N^2=B_*^2N^-1 and n_X=O(N^3). Integrating the positive-part
bound gives the exact denominators 1/2 and 1/6 in (8.6):

  int_0^theta_N sup_edge(-g_X)_+
   <= M_- B_* N^-4
      +exp(E_z k)[Hz0 B_*^2 N^-8/2+D_z B_*^3 N^-5/6].

The O(N^-4) term cannot be dropped without a favorable background-gradient
assumption. Favorable actual gradients are uncharged; the sufficient absolute
increment bound can overestimate their contribution. The full edge-time
increment is only O(1), and the author explicitly distinguishes it from the
O(N^-1) comparison-time increment. Multiplying the integral by v0/L and
the force impulse by v0 correctly restores physical units. The comparison
condition sqrt(N)>=B_*/k_edge is exact and does not replace an old kappa by B_*.

### Energy, hydrostatic control, normalizations and histories

The energy exchanges are +np for matter plus interaction, -np-Tw/C for Q,
and +Tw/C for scale. Both fluxes -pB/C and -Jwk/C remain. The moving-boundary
term is -v0 S[E(beta)+E(alpha)] for these cones; no conserved shrinking-domain
energy is inferred. The exact zero-velocity background solves all equations,
including pressure and the full scale balance. Its flux is zero, and uniqueness
identifies the constructed restriction with it.

Both a0 values are treated separately with their own compatible backgrounds.
Constant vacuum and each separately frozen a0 E(z) are distinct fixed cases;
there is no unproved uniformity over all z. The evolving-reference protocol
work and chart-time terms are explicitly excluded from the autonomous result.
The Q/RAR/M/MONO and physical-completion exclusions remain intact.

## 4. Obligation matrix and exact remaining gap

| Obligation | Status | Evidence |
|---|---|---|
| Task, ten ancestry, raw author and result pins | passed | pre-use hash checks and both read-only verifiers |
| Unchanged C1,1 joins and exact edge scaling | passed | (3.1)-(3.5) |
| Required roots and all stated positive-velocity packet intersections | passed | (3.3), variable b0 allowed |
| Exterior b0=c exception and future-zero-set qualification | passed | Sections 1,3,9 |
| Full momentum/Q/scale dynamics with fixed coefficients | passed | (2.1)-(2.4), (7.2) |
| Actual finite-N construction and C1 limit | passed | Section 4 |
| Uniform N^-7/2 block bootstrap | passed | (5.1)-(5.5) |
| Full C1,1 endpoint/restart and constraints | passed | Sections 6-7 |
| Derived local speed, buffers, and labeled-path persistence | passed | (5.3),(5.5),(9.1) |
| Exterior independence and matching to an existing branch | passed | (9.2), competitor existence condition retained |
| Comparison-time density, field and adverse bounds | passed | (8.1)-(8.7) |
| Complete energy, moving boundary and zero-velocity control | passed | Section 10 |
| Both normalizations and fixed/evolving-history distinction | passed | Section 11 |
| Fast-core/future-resonance/interface control | not addressed | deliberately remaining |
| Full-cone feedback and actual compression endpoint | not addressed | edge suprema do not bound uncovered points |
| Physical completion, observations, cosmology, novelty, closure | out of scope | no promotion |

The strongest safe accepted statement is the author's bounded local theorem
and its quantitative comparison-time edge budgets. The exact remaining
implication for the broader program is complementary actual control of the
uncovered core and evolving interfaces/resonances sufficient to bound the
full FGF049 cone supremum through B_* (L/v0)N^-4. Existence of the edge
solutions alone does not even assert that the whole branch survives that time.

The failed routes in FAILED_ESTIMATES.md are correctly classified as failed
bounds or forbidden extrapolations, not as counterexamples to compression.
No manuscript correction is requested. The cheapest next mathematical check
is a complementary core-to-edge estimate with explicit causal coverage and
matching hypotheses, preserving the possibility of newly created resonance
regions. No full-cone or physical claim is accepted by this audit.

## 5. Verification scope

Executed administrative commands after inspecting their source:

    python3 deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-051/fgf051_run_001/verify_metadata.py
    python3 campaign_fresh_gravity_astra/stage_38/independent_audit/verify_metadata.py

Both passed and performed no writes. Their output confirms metadata, not
mathematical correctness; the raw-proof checks above provide the latter.
Proofreading covered the independent derivation and this audit, with no
routine edits or mathematical-token changes to any frozen source. The present
report is the complete independent audit, not an author self-review.
