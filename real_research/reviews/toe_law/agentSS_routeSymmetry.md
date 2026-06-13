# agentSS — ROUTE 1 (heat-kernel hidden symmetry): does a hidden symmetry of the dS static-patch QNM spectral function FORCE the gain line-shape moment ratio 4 j3/j2^2 onto the edge surface G_sat, or merely PERMIT it for tuned Delta/lambda? (2026-06-13)

## TASK
Build the dS static-patch QNM spectral function from the Gibbons-Hawking heat kernel (the GH
state's two-point function on the static patch). Test three candidate hidden symmetries for whether
they FORCE the moment ratio 4 j3/j2^2 onto the edge surface 4 j3/j2^2 = G_sat (agentRR), or merely
permit a range:
  (a) static-patch SL(2,R) — the QNM ladder is an SL(2,R) representation;
  (b) modular / Tomita-Takesaki flow of the GH thermal (KMS at T_dS=H/2pi) state;
  (c) dS isometry SO(4,1) descending to the spectral weights.

RUTHLESS RULE: a symmetry that PERMITS the edge coincidence is NOT one that FORCES it. "The ratio
lands on G_sat only for a tuned Delta" = PERMITS, not FORCES. Report 'permits not forces' if found —
the brief names this the honest likely outcome.

## INPUTS (banked)
- agentS_edge_qnm.md: dS static-patch scalar QNM ladder omega_N = -i H (Delta + N), purely imaginary,
  uniform spacing, offset = probe dimension Delta. Finite-lambda (DSSYK) form: pole widths
  Gamma_n = sinh((Delta+n) lambda), lambda = -ln q = H_eff; lambda->0 recovers the dS ladder.
  The GH state is thermal/KMS at T_dS = H/2pi (two-sided support at center).
- agentRR_saturated_fold.md: the roton-building active gain line of amplitude G with line-shape
  moments j2, j3 must satisfy the EDGE EQUATION  G_sat = 4 j3 / j2^2  (codim-1 surface) for the
  inflection (sonic-edge) coincidence sigma6 = sigma6* = sigma4^2/(4 c^2). With sigma4 = -G j2 c^2,
  sigma6 = +G j3 c^2, the no-fold->fold window is sigma6/sigma6* in (1, 4/3). agentRR verdict:
  the edge coincidence is TUNED (>=1 free line-shape ratio); the pump fixes only the k* SCALE.

## PROGRESS (incremental)

### Part 1 — setup (DONE)
- QNM ladder rates: finite-lambda Gamma_n = sinh((Delta+n)lambda); dS limit Gamma_n/lambda = Delta+n
  (uniform spacing 1, offset Delta).
- SL(2,R) discrete-series rep: Casimir C2 = Delta(Delta-1); L_0 spectrum Delta+n; ladder matrix
  elements |<Delta+n+1|L_+|Delta+n>|^2 = (n+1)(2Delta+n).
- The rep FIXES spacing (uniform) + offset (Delta) + ladder matrix elements. LOAD-BEARING question:
  do these fix the spectral RESIDUES a_n that set the moments j2, j3? -> Part 2.

### Part 2-4 — the decisive moment-ratio computation (DONE)
Built the GH heat-kernel spectral measure as the QNM tower with the two SL(2,R)-canonical residue
choices: (i) character/Plancherel weight a_n=(2Delta)_n/n!; (ii) normalized descendant a_n=1/[n!(2Delta)_n].
Computed the CENTRAL moments j2, j3 of the discrete line shape (the physically correct object for a
gain line) and the ratio R = 4 j3/j2^2.

FINDINGS:
- The character weights (2Delta)_n/n! GROW as n^(2Delta-1) -> moment sums DIVERGE -> NOT a normalizable
  line shape. Verified: sum_a*n^2 grows ~linearly/faster with cutoff at every Delta. Discarded.
- The normalized-descendant measure is the only normalizable canonical choice. Its ratio:
      Delta:   0.5     1.0     2.0     4.0     8.0    16.0    32.0
   4 j3/j2^2: 4.314   8.125  16.038  32.008  64.001 128.000 256.000
  i.e.  **R = 4 j3/j2^2 = 8 Delta + O(1/Delta)** EXACTLY (R/Delta -> 8.000, R-8Delta -> 0).
- Central moments are origin-independent, so the absolute-vs-detuning origin choice does NOT matter;
  the ONLY freedom is Delta (and the discarded residue choice).

VERDICT OF SL(2,R) TEST: **PERMITS, NOT FORCES.** The discrete-series rep fixes spacing + offset +
ladder matrix elements, but the resulting moment ratio R = 8 Delta is a SLIDING knob set by the FREE
probe dimension Delta. It can be tuned to ANY value >= ~4 (at Delta=1/2) by choosing Delta; landing on
a specific G_sat requires picking Delta = G_sat/8. That is tuning, not forcing. The rep does not single
out a Delta, so it does not single out a moment ratio.

### Part 5-6 — (b) MODULAR / TOMITA-TAKESAKI flow of the GH thermal (KMS) state (DONE)
The GH state on the static patch is KMS at T_dS=H/2pi; Tomita-Takesaki modular flow = static-patch
boost (the well-known fact that the GH modular Hamiltonian generates static-patch time translation).
Two ruthless tests:

- The FULL continuous thermal spectral weight rho(omega) ~ sinh(omega/2T)|Gamma(Delta+i omega/2piT)|^2
  GROWS at large |omega| -> its raw moments DIVERGE (Part 5 numerics: integral cutoff-dominated, no
  finite j2,j3). It is a broad spectral DENSITY, not a normalizable line shape. This independently
  reproduces agentRR/MM/NN's "smooth GH continuum is BROAD -> sigma6<0 (no fold)": the unmodified
  thermal continuum has no peaked structure to give a controlled fold.

- THE DECISIVE STRUCTURAL ARGUMENT (analytic, not numeric): modular flow acts as a DILATION on the
  spectral axis, s -> e^{alpha} s (boost = rapidity translation = dilation of frequencies). Under it the
  central moments scale j_n -> e^{n alpha} j_n, so
        4 j3 / j2^2  ->  e^{(3-4)alpha} (4 j3/j2^2) = e^{-alpha} (4 j3/j2^2).
  The ratio has modular-scaling weight -1 (DIMENSION of [frequency]^{-1} -- it is NOT dimensionless;
  G_sat carries the same [1/frequency], consistent). A symmetry that DILATES the spectral axis cannot
  pin a weight-(-1) quantity to a specific finite nonzero value -- its only scale-fixed points are 0 and
  infinity. So modular covariance MOVES 4 j3/j2^2; it cannot FORCE it onto G_sat.

- KMS detailed balance rho(-w)=e^{-w/T}rho(w) fixes the thermal IMAGE weight of a peak, NOT the peak's
  intrinsic skew. A single retarded QNM pole (center s_g, width Gamma) satisfies KMS for ANY (s_g,Gamma);
  those are set by (Delta, lambda) and remain free, so j2, j3 of the gain line are free.

VERDICT OF MODULAR/KMS TEST: **PERMITS, NOT FORCES.** Modular flow is a dilation; 4 j3/j2^2 is
modular-covariant of weight -1, hence rescalable to anything; KMS fixes only the image weight, not the
line skew. (This is also WHY the SL(2,R) discrete result R=8 Delta slid: Delta sets the dilation/scale
of the rep, and the ratio rides that scale linearly.)

### Part 7 — (c) SO(4,1) dS isometry + hostile rescues (DONE)
- SO(4,1) on the static patch breaks to [R_t (static time) x SO(3) (sphere) x boost(=modular)]. The
  spectral-data part is exactly the SL(2,R)~SO(2,1) of (a)/(b). The extra SO(4,1) generators leave the
  static patch (they relate DIFFERENT static patches / observers), so they do not constrain the in-patch
  spectral weights. SO(3) only fixes the l-multipole degeneracy (orthogonal to the moment ratio). =>
  SAME constraint as SL(2,R): organizes the tower into a principal/complementary-series rep labelled by
  Delta, but does NOT fix Delta. PERMITS.
- HOSTILE RESCUE H1 (could G_sat co-dilate, making the edge eq scale-covariant so a dilation can't break
  it?): NO. [G_sat]=[s]^{-1}, but G_sat is fixed by the dispersion geometry (c_chi^2, the sonic edge), and
  c_chi is an INDEPENDENT khronon datum with no scale-tie to H (agentRR CHECK 5: no c_chi<->H collapse).
  So the LHS (QNM moment ratio) dilates as e^{-alpha} while the RHS (G_sat) is held fixed by c_chi-physics
  -> the equation is NOT scale-covariant -> the modular dilation genuinely BREAKS any forced coincidence.
  Worse: it shows the match can be reached at exactly ONE rapidity frame = explicit TUNING. H1 fails.
- HOSTILE RESCUE H2 (is Delta forced anywhere, making R=8Delta a fixed number?): NO. The roton-probe /
  khronon dimension Delta is a FREE input (agentS scans Delta in {0.1,0.5,1.0}; dS conformal/massless
  values exist but the probe's Delta is not pinned by the banked machinery). Delta free => R free. H2 fails.

### Part 8 — does the ratio land on the edge surface? + the k-resolution requirement (DONE)
- Feeding the QNM line (4 j3/j2^2 = 8 Delta, gain amplitude G a separate knob) into agentRR's geometry:
  sigma6/sigma6* = 8 Delta / G. The bounded-fold (no-ghost, non-monotone) window 1 < sigma6/sigma6* < 4/3
  becomes 6 Delta < G < 8 Delta -- a NONEMPTY but narrow G-band (25% wide) for each Delta. So the fold is
  SATISFIABLE, but only by hand-placing G in (6Delta, 8Delta), which must ALSO equal the saturation value
  (gain=loss, kappa-set) AND the edge value -- three independent conditions on one knob, generically
  unequal (agentRR's measured 10-266x roam). The edge-exact G=8Delta sits at the sigma6/sigma6*=1 soft
  sonic-edge boundary of the window. => codim-1 PERMITS, reproduces agentRR exactly. No symmetry collapses
  the three conditions onto each other.
- K-RESOLUTION (the brief's 2nd load-bearing requirement; agentRR's 4th condition -- the non-Markovian,
  k-resolved clamp that scalar saturation cannot supply): the QNM ladder Gamma_n = sinh((Delta+n)lambda)
  is indexed by the DESCENDANT number n; SL(2,R)/modular acts on time/energy spectral data; SO(3) carries
  the horizon-sphere multipole l -- NONE of these is the khronon spatial wavenumber k in omega^2(k). The
  static-patch symmetry sector is DECOUPLED from the spatial-k sector the fold lives in. => the dS
  heat-kernel symmetry does NOT supply the k-resolved clamp either. THIS IS THE ANSWER TO k_resolves_clamp:
  NO -- the symmetry structure carries no intrinsic spatial-k label to k-resolve the clamp.

### Part 9 — independent verification of the load-bearing result (DONE)
R = 4 j3/j2^2 = 8 Delta confirmed by THREE independent methods:
  (i) direct summation of the discrete measure (Part 3-4);
  (ii) generating function Z(t)=0F1(;2Delta;t) with theta-derivative moments (Bessel-I closed form);
  (iii) analytic asymptotic: a_n -> (1/2Delta)^n/n! (Poisson, rate p=1/2Delta) => j2=j3=p => 4j3/j2^2=4/p=8Delta EXACT.
All agree to O(1/Delta). The result is METHOD-INDEPENDENT, not a numerical artifact.

---

## OVERALL VERDICT — PERMITS, NOT FORCES (the honest likely outcome the brief named)

**No hidden symmetry of the dS static-patch QNM spectral function / GH heat-kernel forces the gain
line-shape moment ratio 4 j3/j2^2 onto the edge surface G_sat.** All three candidate symmetries return
PERMITS:

- **(a) static-patch SL(2,R):** the discrete-series rep fixes spacing (uniform), offset (Delta), and the
  ladder matrix elements -- a genuine, real symmetry constraint -- but the only normalizable canonical
  spectral measure gives a moment ratio R = 8 Delta that SLIDES monotonically with the FREE probe
  dimension Delta. Landing on G_sat means choosing Delta = G_sat/8: tuning, not forcing.
- **(b) modular / Tomita-Takesaki (KMS at T_dS=H/2pi):** the modular flow IS the static-patch boost = a
  DILATION of the spectral axis; 4 j3/j2^2 is a modular-covariant quantity of weight -1, hence rescalable
  to any value (only scale-fixed points 0, infinity). KMS detailed balance fixes the thermal IMAGE weight,
  not the line skew. The dilation ACTIVELY OBSTRUCTS a forced match (the coincidence is hit at one
  rapidity frame). The smooth GH thermal continuum is moreover broad/non-normalizable (no finite moments)
  -- independently reproducing the banked "smooth GH continuum -> sigma6<0, no fold."
- **(c) SO(4,1) dS isometry:** descends to the same SL(2,R)~SO(2,1) on in-patch spectral data; extra
  generators leave the patch; SO(3) only sets l-multiplicities. Same constraint, Delta unfixed. PERMITS.

**THE HIDDEN SYMMETRY THAT WAS FOUND (named precisely):** there IS a real hidden symmetry -- the
**static-patch SL(2,R)~SO(2,1) conformal/modular structure of the GH state** (the QNM ladder is its
lowest-weight discrete-series representation, and modular flow is its boost generator). It is a genuine
constraint: it organizes the spectrum into a uniform-spacing, Delta-offset ladder with fixed matrix
elements. **But it constrains the WRONG invariant.** It fixes the ladder STRUCTURE up to the rep label
Delta and an overall spectral SCALE; the edge coincidence requires fixing a SCALE-COVARIANT (weight -1)
ratio against an externally-set scale G_sat (c_chi-physics, scale-decoupled from H). A symmetry that acts
as a dilation cannot pin a covariant quantity to an external scale. So the symmetry PERMITS the edge
coincidence (one equation Delta=G_sat/8 or G in (6Delta,8Delta)) but does NOT FORCE it.

**k-resolution of the clamp:** NO. The static-patch symmetry sector (descendant n, time/energy, horizon
multipole l) carries no intrinsic khronon spatial wavenumber k. It cannot supply the k-resolved,
non-Markovian clamp that agentRR's 4th condition needs -- that requirement is decoupled from and
untouched by the dS heat-kernel symmetry.

**WHY THIS WAS EXPECTED (brief's framing held):** agentPP already proved the passive dS QNM spectrum is
broad and cannot fold; agentQQ that the deliverer must be ACTIVE; agentRR that the edge coincidence is
codim-1 with N=4 free ratios. This route asked whether a HIDDEN symmetry rescues forcing where the
explicit moment-counting could not. It does not: the relevant symmetry is a dilation, and the target is a
covariant ratio against a scale-decoupled external constant -- structurally the one configuration a
dilation symmetry cannot force. Forcing the edge requires imposing structure by hand (pinning Delta, or
pinning the gain amplitude G into the narrow window) -- NOT read off any banked symmetry.

**OUTCOME: NEEDS-NEW-INPUT.** The forcing symmetry is NOT in the banked dS heat-kernel / GH-state
machinery. The dS static-patch structure carries a real SL(2,R)/modular symmetry, but it permits rather
than forces the gain-shape ratios onto the edge surface, and supplies no intrinsic spatial-k structure to
k-resolve the clamp.

## QUARANTINE
Held throughout. Only computed: SL(2,R) rep data (Casimir, spacing, matrix elements), the moment ratio
R=8 Delta (signs/scaling/value of a RATIO, not the coefficient), the modular scaling weight (-1), the
fold-window G-band (6Delta,8Delta), and the absence of a spatial-k label. q=1/4, zeta-tilde,
(16pi/3)^{1/4} NEVER asserted.

## FINAL HOSTILE CHECK (Part 10) — no weight-0 reinterpretation rescues forcing
A dilation fixes weight-0 ratios (skewness j3/j2^1.5, kurtosis...). Could the edge condition secretly
BE such an invariant? NO: (i) the edge ratio 4 j3/j2^2 = 4*skewness/width carries a DIMENSIONFUL 1/width
(lambda=H_eff-set) factor on top of the skewness, so it is weight -1, not 0; (ii) even the weight-0 part
the symmetry CAN fix -- the skewness -- is itself Delta-DEPENDENT (~sqrt(2Delta), verified: 0.77/1.25/
1.91/2.79/3.99 at Delta=0.5/1/2/4/8), so not a universal constant. The genuinely symmetry-fixed invariant
still slides with the free rep label. Forcing remains impossible. PERMITS-NOT-FORCES is robust to this
last rescue.

## METHOD-INDEPENDENCE / FILES
agentSS_part1.py (SL(2,R) setup), part2 (GH residue candidates), part3-4 (moment ratio direct + char
divergence), part5-6 (thermal continuum + modular scaling), part7 (SO(4,1) + hostile rescues), part8
(edge landing + k-resolution), part9 (generating-function + Poisson-asymptotic verification). All in
real_research/reviews/toe_law/. R=8 Delta verified by 3 independent methods.
