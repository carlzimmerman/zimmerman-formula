# FGF050 full independent audit after author exposure

Normalized claim: for the exact fixed-coefficient Q/scale/isothermal system,
unchanged C1,1 compact velocity, either separately normalized compatible
background, and any putative positive classical solution covering the full
FGF049 cone to T_N=B*/omega, the author derives an exact weighted two-path
formula for signed g_x, integrates the density source using continuity while
retaining pressure and resonance terms, and identifies the additional traces
and state bounds that would suffice for the feedback budgets.

Primary verdict for the actual-family target: **incomplete, with the smallest
missing implication**. The exact identities, initial relative-speed crossings,
mass laws, conditional estimates and scoped failed-inference statements are
proved as written. The author does not prove, and correctly does not claim,
the actual full-interval force or adverse-gradient budgets. No correction to
the author proof is required.

## Source pins and independence

Raw author proof was verified then read before result metadata:

- DERIVATION.md: 9ba6685e50ef2b657c3740674b8ea8b921ced1f1c0d3527ce65df520e6490e18.
- result.json: f5bf4d4faf45e921e75b822b4d78a21eff96844acdf9d442a6bf8d6019994f5a.
- FREEZE.json: 8fe34b154cb7edac7196c8a0c05eeb5d326fd1bb4351968a32120a94433f5d10.

All are in deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/
FGF-050/fgf050_run_001/. The task and all nine ancestry pins matched before
ancestry use. The task text itself was read to discover pins before hashing;
that chronology is disclosed in INDEPENDENT_FREEZE.json. All input/artifact
hashes in author result and all artifacts in author FREEZE subsequently passed
a separate read-only Python standard-library check.

My independent derivation was frozen before ANY new FGF050 author/root/other
reviewer proof or preview, SHA256
080867663e7db3c6c7105449de4b178755fe53735715cc0c1539386bbf80de7c.
Its ancillary local display (3.4) contained a wrong sign and a missing term.
I detected this immediately by self-check, informed root, and saved
PRE_EXPOSURE_CORRECTION.md plus JSON before reading the root candidate.
The correct local display is

    (u^2-c^2)n_x=-u Dlambda n+n Dlambda u-nu lambda_x+n(g+D_v lambda).

The frozen primary integral/cutoff identities never depended on the erroneous
local display; they remain correct. Original bytes and correction are both
retained, and the original (3.4) is not accepted as evidence.

Next I read and audited ROOT_TRANSPORT_CHECK.md, SHA256
b3e6fe110362381bc010be422c36d3a36ba4d082c93cc766a1ac60836a2d52b3,
AFTER my freeze/correction but BEFORE author final-proof exposure. That root
source introduced an acoustic Riemann-invariant inversion and an initial
v-b=c crossing argument; my audit of those is post-exposure. Root separately
discloses that its own freeze followed an author identity preview. Hence this
report does not portray the root calculation as a third blind independent
identity proof. AUTHOR_EXPOSURE.json and ROOT_EXPOSURE.json retain the order.
No other new reviewer proof has been read. Model/agent agreement is not itself
proof; the algebraic checks below supply the actual evidence.

## Dependency graph and critical reconstruction

Dependencies terminate in the specified equations/data and verified FGF049
budget/cone definition. FGF047/048 supply only the existing local branch and
short-kappa estimates; neither is used to extend existence or bounds to B*.
There are no external literature or mathematical computation leaves.

1. Equations (3)-(6): reconstruct from g_t=p_x, tau p_t=B_g g_x+B_chi k-Cn,
H_g=b, H_chi as defined, and chi_t=w. With lambda_epsilon=-epsilon b,
D_epsilon(p+epsilon H)=B_chi k/tau+epsilon H_chi w-b H_chi k-(C/tau)n.
Differentiating the integrated equation in terminal x multiplies every initial
and source derivative by j=exp(-integral_s^t lambda_x), whose s derivative
is +lambda_x j. Thus both the sign and normalization j(t)=1 are correct.
Subtracting xi_plus-xi_minus=2b g_x+2H_chi k gives (6) with the adverse
source sign -(C/(2tau b))(I_plus-I_minus). Coefficients, paths, initial feet,
scale correction, F_x and Jacobian dependence all remain actual solution
quantities. C1 field state and smooth positive chart suffice; no f'' at a join
is required.

2. Equation (7): directly differentiate jn/r with r=v-lambda:
Dlambda(jn/r)=-j n_x-jn D_v r/r^2. This proves the displayed integration
by parts including both endpoint terms and sign. Substitution of the full
momentum equation gives the author's (8)-(9); D_v lambda uses
lambda_g(p_x+v g_x)+lambda_chi(w+v k), correctly retaining dynamical scale.
The pressure coefficient remains inside the integral. No variable factor
1-c^2/r^2 is pulled outside. The nonzero-r segment qualification is explicit.

3. Equation (10): subtract terminal pieces -n/(v+b) and -n/(v-b). Their
difference is +2bn/(v^2-b^2), and multiplication by -(C/(2tau b)) gives
-Cn/[tau(v^2-b^2)]. This is adverse for |v|>b, favorable for |v|<b, with
neither conclusion applying to total g_x or at the singular denominator.
Initial endpoints and both acceleration integrals remain.

4. Equation (11): start from the independently derived smooth-cutoff identity
I=integral j(1-theta)n_x-[j theta n/r]+integral jn Dlambda theta/r
-integral jn theta D_v r/r^2. Substitution of full momentum produces exactly
J+P+L. Expanding Dlambda theta=theta'(r)Dlambda r using (12) contributes
-c^2 theta' n_x/r, so the combined n_x weight is
1-theta+c^2(theta/r^2-theta'/r), as stated. The cutoff is identically zero
near r=0, making the quotients smooth; there is no finite-crossing-count
assumption. delta is dimensionless, threshold delta V has velocity units,
and this is a partition of an identity, not retuning the physical model.

5. Initial relative-speed obstruction: actual smooth b0(x)>0 and the unchanged
velocity imply v-b0<0 at both joins and >0 at center for sufficiently large
N. The intermediate value theorem supplies an interior zero in each half.
The positive branch v+b0 has only order-one gaps at the joins. The argument
proves initial global separation false and proves no later singularity.
The separately audited root acoustic v-b=c crossing is stronger in a different
direction but is not silently attributed to the author as a blind derivation.

6. Material mass identities (13)-(14): inverse label satisfies D_v A_m=0,
n=rho(A_m) A_m,x; thus Dlambda M0(A_m)=-rn. On fixed-sign segments,
absolute endpoint mass change equals integral n|r|. The material-domain gate
is explicit. Changing signs requires variation with multiplicity; it is not
bounded by range alone. For (15), backward plus path is to the right of the
minus path. To check ordering, in reverse time their vector fields are +b
and -b: at any attempted contact their separation derivative is +2b>0, so
ordering cannot first fail. Reynolds transport then gives
M'=-r_plus n_plus+r_minus n_minus and M(t)=0, proving the author's sign
and initial-wedge-mass endpoint. These are flux identities, not derivative
trace estimates. Differentiation in terminal x necessarily introduces traces
and derivatives of r.

7. Sufficient budget accounting: with Ecal as defined,
(-g_x)_+ <= (-Ecal)_+ +C(|I_plus|+|I_minus|)/(2tau bmin).
Integrating and using I=J+P+L proves (16). The two proposed halves each
consume at most eta omega/2; their constants are correct. Compact |g|<=gmax
implies force impulse <=gmax B*/omega, below Gamma V for sufficiently large
N because omega V grows as N^5 with fixed parameters. These gates are not
proved for the actual data and the author explicitly says so.

8. N dependence in (17): on the support of theta, |r|>=delta V. Then each
|P_epsilon(t,x)|<=jmax c^2/(delta^2 V^2) integral_0^t Mx(s)ds by field-path
containment. Sum two families and integrate t; Tonelli on the nonnegative
bound gives the weight T_N-s and exactly factor 2. Hence the sufficient
little-o condition is weighted integral=o(omega V^2)=o(N^6), with fixed
physical units and coefficients. This is a named sufficient input, not a
deduced asymptotic. The paired terminal O(V^-2) gain also requires the fast
region and bounded b (available under the stated compact chart), and does
not bound density traces. A compact state alone supplies no jmax because
j depends on lambda_x. No short-kappa estimate is reused through B*.

## Separate reviewer lemma: continuity-only signed-trace failure

My frozen Section 4 goes beyond the author's static fixed-mass bump example
by constructing a continuity-only moving bump. For constants U>b>0,
n_epsilon=nbar+(M/epsilon)psi((x-Ut)/epsilon), v=U, lambda_plus=-b,
lambda_minus=b, j=1, it satisfies continuity, has constant excess mass M,
and both relative speeds are bounded away from zero. It yields

    I_plus=[n_epsilon(0,x+bt)-n_epsilon(t,x)]/(U+b),
    I_minus=[n_epsilon(0,x-bt)-n_epsilon(t,x)]/(U-b).

Take any fixed [t0,t1] with t0>0 and a finite cone containing x=Ut in its
interior. For epsilon smaller than the distance (U-b)t0 divided by the
fixed bump support radius, both initial feet miss the bump at x=Ut, while
the terminal point is its peak. Then

    (I_plus-I_minus)(t,Ut)=2b M psi(0)/[(U^2-b^2)epsilon].

Consequently its time-integrated spatial supremum diverges as epsilon tends
to zero at fixed mass, time interval and relative-speed separation. Background
nbar cancels exactly in the source integrals and gives positive density on a
finite domain. This adjudicates the lemma as a valid analytic counterexample
to a UNIVERSAL continuity-plus-mass-plus-separation signed-source estimate.
It is not a finite experiment and has no asserted actual-N asymptotic.

Crucial restriction: it does not satisfy the full momentum/Q/scale equations
or the prescribed initial rho/velocity. Its constants are an auxiliary
functional-inequality class, not replacement coefficients in the author proof.
It therefore CANNOT be promoted as an actual coupled-family counterexample,
a compression counterexample, a prediction of adverse feedback, or a physical
law test. Author's narrower static mass-to-trace obstruction is also correct.
This is the reviewer's own independently derived lemma, algebraically checked
in this audit; a separately named agent's acceptance must not be fabricated.

## Controls, scope and obligation matrix

Exact hydrostatic zero velocity: all four equations hold, p=w=v=0, r=-lambda,
D_v r=0, and the IBP gives its boundary-only source integral. Full field
initial/source/scale terms reconstruct g0_x, rather than incorrectly making
the density contribution vanish by itself. At t=0 j=1 and I=0 check (6).
Favorable g_x>=0 contributes zero adverse budget; the fluid weighted-gradient
force is -h g_x, confirming that charging only negative g_x has the right sign.

Energy: W_t=Bp_x-Tw gives matter +np, Q -np-Tw/C, and scale +Tw/C;
both -(pB+Jwk)/C fluxes survive. Reynolds terms are correct for arbitrary
moving endpoints and for the shrinking cone. The excess O(V^2 ell)=O(N^-1)
energy is not promoted to a gradient norm. For an explicitly evolving a_ref,
W's extra derivative is W_loga alpha_ref=-T alpha_ref, agreeing with the
separately stated protocol work; fixed-reference field formulas are not
silently transferred to that history.

Passed: actual equations/regularity; signs/Jacobians; two different paths;
initial/terminal/transition terms; pressure; full dynamical scale; resonance
partitions; material and wedge mass laws; N-dependent sufficient estimates;
hydrostatic and favorable-sign controls; energy and moving boundaries;
both dimensional normalizations and constant/frozen/evolving histories;
Q/RAR/registered-M/filtered-MONO separation; no physical closure inflation.
Failed inequality: mass-only trace inference, scoped to the stated broad
functional/continuity classes. Not established: actual-family full-horizon
chart, Jacobian, force and signed two-path feedback estimates. Out of scope:
actual maximal-endpoint classification, completion and observational claims.

## Metadata, limitations and smallest missing implication

The author's verify_metadata.py writes a newly timestamped VALIDATION.json,
whose final bytes FREEZE.json pins. Re-running that script in place would
invalidate the freeze. I did not run it. Independent read-only JSON/hash
checks confirm the current bytes instead. This is an administrative
reproducibility limitation, not a mathematical defect or an experiment.
Zero mathematical executable computations, no external literature, services,
new agents, or changes outside the assigned reviewer directory were used.

The smallest remaining implication is a non-circular estimate, from the actual
initial data and full coupled dynamics, of the signed combination
[-Ecal+(C/(2tau b))(I_plus-I_minus)]_+ integrated over the full cone, together
with the force impulse. The exact remainder is (11): low-speed L, cutoff
transition/endpoint and acceleration content of J, pressure P, and all
field/scale/Jacobian terms. Quantitative compact-chart control is an unproved
sufficient gate. Establishing fast-core separation alone leaves these terms
and the initial resonance regions uncontrolled.

Strongest safe acceptance: exact transport/mass identities and precise failed
mass-only inference, plus explicitly conditional sufficient feedback bounds.
Actual feedback remains open. A next useful check must bound these signed
traces or show a specific proposed bound fails in the actual initial family;
repeating FGF049's Riccati theorem or an unchanged short-time bootstrap would
not address that implication. Entire audit self-proofread; no author edits
or post-freeze revisions to the original independent derivation were made.
