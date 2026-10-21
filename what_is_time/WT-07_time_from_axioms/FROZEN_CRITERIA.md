# WT-07 FROZEN CRITERIA: what time structure ("now") do the framework's own axioms force?

Lane WT-07 of `what_is_time/`. Frozen 2026-10-21 and committed alone, before any script or number of this lane exists.
κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m s⁻² are used separately wherever a0 enters and are
never pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is added. Framework-native only. Not "theory
closed". Nothing here says the data favour the framework. Anything true by construction is marked as such and carries no weight.

## 0. Blindness disclosure (read first)

This lane is **not blind**. Before freezing I was told, and I read:
- WT-02's results (9b3d77382, criteria b85749d1c): CFG938's χ/λ pair is a forward/backward heat pair on FRW with
  Re σ = c²k²/3H (Hadamard ill-posed, also for H < 0); MU3 found that the intrinsic slice Laplacian removes the ill-posedness
  but then needs an explicit mean-density subtraction; the hidden cosmic clock χ̄(t); c_T ≠ c from the ττ term.
- The orchestrator's hint that the intrinsic Laplacian ³Δ plus a mean subtraction is the natural repair.
- CFG961's frozen criteria and its hand expectations (83b04219e).
- WT-08 builds a repaired parent and WT-09 classifies stiffness terms with c_T = c. This lane does not build their objects.

**Hand expectations written before any script** (they do not change the rules below):
1. L31's hypothesis (iii) "exactly two propagating gravitational modes" fails once the medium is dynamical (A3), so L31 alone
   does not force a foliation. What forces one is the χ constraint itself, if χ is non-propagating.
2. Any first-order normal derivative in the χ constraint makes the multiplier pair forward/backward parabolic for either
   sign of the expansion, because the adjoint flips the sign of a first-order operator.
3. On a compact leaf an elliptic leaf constraint is solvable only if its source has zero leaf average, so A7 (contrast
   sourcing) follows from A6 once χ is leaf-elliptic. The leaf mean can enter as an integration constant of a local
   leaf-gradient form of the constraint. That leaf constant ticks with leaf volume; a spacetime constant (unimodular Λ₀)
   is frozen.
4. The candidates I expect to survive are CMC/York leaves (no new mode) and a khronon (one new scalar mode). The medium rest
   frame fails wherever the medium has vorticity (Frobenius). Unimodular time is not a foliation.
5. Expected verdict: MENU {CMC, khronon} under the literal axioms, and CMC alone if new propagating modes are excluded.

## 1. The axioms, with sources (changes from the orchestrator's wording are flagged ⚑)

Record hashes are `git log -1 --format=%h -- <file>` at freezing.

- **A1 (one metric).** Matter, light and GWs couple to one metric g; c_T = c to GW170817 precision
  (−3e-15 < c_T/c − 1 < +7e-16). Sources: `CLOCK_WORK_ORDER.md` T1/CK01 (one-metric no-go, ≥ 7 orders);
  WT-01 §2 item 1 (1ce2b0dcc). This lane scores only the foliation-dependent part of c_T (the FRW cosmic-clock piece). The
  ττ stiffness piece belongs to WT-09 and is reported here as OPEN.
- **A2 (static law).** The static weak-field limit is canonical S2: ∇·P = δρ_c with W_full,
  a0 = κc√(Gρ_DE), κ = ½ FITTED. Covariantly u = K|P_L| is the medium-frame gradient of the medium's own potential χ, with
  ∇²χ = Kδρ_c on static slices (CFG938 §3.1–3.4, 92606e049).
- **A3 (cold energy).** Cold energy is real, conserved, gravitating mass: a comoving-label medium φ^I with conserved current
  J^μ and total label number N (topological, conserved identically). No particle species. ⚑ **Two readings, both scored:**
  - **A3-literal (primary):** no new particle species; extra gravitational-sector fields are allowed if they have no ghost
    (e.g. a khronon).
  - **A3-strict (secondary):** no new *propagating* degree of freedom beyond the medium (one longitudinal mode at c_s and two
    frozen vortical modes) and the graviton. Constraint fields (χ, λ, a CMC multiplier, a non-propagating cuscuton) are
    allowed, as in CFG938.
- **A4 (locality).** The non-locality the record already accepts:
  - (i) elliptic constraints solved on leaves, instantaneous on leaves (CFG938 S5d; CFG292's leaf-elliptic lapse factor;
    criterion B allows it);
  - (ii) leaf averages ⟨·⟩_h (CFG6 Branch B-leaf, 3409d12da, CONDITIONAL; L350's −c₂(K − ⟨K⟩)², a construction;
    XR30/FP14's −2μ(K − ⟨K⟩_h), 2a2d81f61);
  - (iii) global constants of motion: the HT pair (Λ₀, T) (XR20 T1, XR30, CFG6 Branch A, STANDING as a construction).

  Not accepted: time-non-local (retarded or advanced) kernels in an action. CFG947 (59da0f016) finds that a causal non-local
  parent comes from no action, and that the time-symmetric form is acausal.

  ⚑ **Two readings, both scored:**
  - **A4-record (primary):** (i)–(iii) are admitted.
  - **A4-strict (secondary):** the action must be a local functional; global quantities may appear only as integration
    constants or boundary conditions of local equations (as Λ₀ does in HT).
- **A5 (causality, criterion B; owner decision 2026-09-26).** There must be no backward signal in a global time function
  compatible with every characteristic cone. Instantaneous propagation within a leaf is allowed. Sources: CFG172 criteria:136
  (ac2d5a2be); CFG292 (918b33183).
- **A6 (well-posed IVP).** The linear IVP must be Hadamard well-posed on: expanding FRW (H > 0); contracting FRW (H < 0, a
  collapsing region); the turnaround instant (H = 0); and a static halo. ⚑ **Sharpening drawn from the record:** CFG678's
  one-action contract gate A1 is "no ghost; second-order field equations" (72577e919). The primary reading of A6 is
  Hadamard + no ghost. The **secondary reading, A6-Hadamard-only,** is also scored.
- **A7 (contrast).** The law is sourced by the density contrast, not the mean (S2: ∇·P = ρ_c − ρ̄_c). §4 tests whether A7
  is an independent axiom or follows from A6 plus a leaf-elliptic χ.

Settings: K = 4πG, signature (−+++), c explicit or c = 1 as stated per check.

## 2. The question, in parts (answers are produced in this order)

- **(a)** Do L31's hypotheses (i)–(iv) (and corollary (v)) hold under A1–A7? If one fails, does anything else force a
  foliation? The test is the principal-part trichotomy of §4 (S1).
- **(b)** Which foliation? Per candidate (§3), decide:
  - can the χ constraint be written with only intrinsic leaf derivatives in its principal part, i.e. elliptic on each leaf
    with no time derivative of χ or λ (gate G-INT);
  - is the source n_Σ − n̄_Σ with n̄_Σ well defined (G-NBAR);
  - the linear IVP on FRW and contracting FRW, and the Hadamard test (G-HAD).
- **(c)** The mean density n̄. Options N1–N5 (§5), scored against A4, A6 and ∇_μT^{μν} = 0. Does any option reproduce the
  record's two clocks (York time ticks; unimodular Λ₀ frozen) as "now" and "scale"?
- **(d)** Does criterion B hold for each surviving candidate? Does the surviving "now" coincide with the medium rest frame in
  static halos, so that the static law and WT-04's clocks are unchanged?
- **(e)** One paragraph, "From axioms A1–A7, time in this framework is …", with each clause marked FORCED / CHOSEN / OPEN.

## 3. Candidates (frozen list) and controls

The χ constraint for an intrinsic candidate with leaves T = const, unit normal n_μ = −N∂_μT and leaf expansion K_T = ∇·n is

  ³Δ_T χ ≡ h_T^{μν}∇_μ∇_νχ + K_T n·∂χ = Km (n_Σ − n̄_Σ),

with n_Σ = −n_μJ^μ the leaf-measured density (∫_Σ n_Σ√h = N exactly) and n̄_Σ the leaf mean. Elsewhere the action is CFG938's:
- u² = h_T^{μν}∂χ∂χ (leaf gradient), with K·W_full → u²/2 at quadratic order about u = 0;
- the stiffness −(3L*²/8)τ_T·τ_T (in units with the action multiplied by K), where τ_T is the traceless *intrinsic* leaf
  Hessian, = projected Hessian + (K_μν − ⅓h_μνK) n·∂χ;
- the rest-mass term −Km n√−g;
- a quasi-static Newtonian potential Φ = Ψ.

| id | foliation | how its leaves are fixed in the linear test |
|---|---|---|
| **F0** (control) | fixed cosmic time T = t, **not varied** (prior geometry) | δT ≡ 0 imposed, no δT equation |
| **F1** | medium rest frame (leaves ⟂ u; exists iff the flow is irrotational) | lock multiplier ℓ: ∂_xδT + a²ξ̇ = 0 (longitudinal sector only) |
| **F1′** | medium proper time (Brown–Kuchař-type clock carried by the medium, u·∂T = 1) | lock multiplier: δṪ − Φ = 0 |
| **F2** | CMC/York leaves, pure (no new mode; α_c = 0) | multiplier ν on δK_T (k ≠ 0 part of K − ⟨K⟩), as XR30/FP14's −2μ(K − ⟨K⟩_h) |
| **F3** | khronon (BPS, β = 0) at CFG292's window corners (α_c, c₂) = (9.62e-14, 7.29e-3) and (3.2e-9, 0.0667) | toy L_kh = (A/2)a(∂_x(Φ − δṪ))² − (A c_k²/2)(∂_x²δT)²/a, with A = α_c and c_k² = c₂(2 − α_c)/(α_c(2 + 3c₂)) (CFG292's c_S² at β = 0) |
| **F3b** | FP14's CMC-khronon (c₂ → ∞ multiplier plus the α_c regulator) | F2 plus the α_c term of F3, at α_c = 3.2e-9 and 8.2e-16 |
| **F4** | leaves of unimodular (HT) time | structural test only (§6, E7): is a level set of T⁰ gauge invariant? |

**Controls and alternatives scored with the same gates:**
- **C938:** CFG938 as written. Medium-frame D² = h∇∇χ (= ³Δ − θu·∂χ), no subtraction, and χ̄(t) with χ̄̇ = −Km n̄/(3H)
  (S1d). This is K1.
- **P1 (propagating χ, no foliation):** λ(□χ − Km n), Lorentz-invariant □ of g.

F1 and F1′ are tested in the longitudinal sector, since F1 does not exist with transverse velocity. All the others carry the
transverse (vortical) displacement η as well.

## 4. Structural theorems to derive (sympy), each with a check that can fail

- **S1 (principal-part trichotomy).** For L[χ] = h∇∇χ + a n·∂χ + b (n·∂)²χ with a multiplier λ:
  - if b = 0 and a ≠ a_θ (a first-order normal derivative survives), the χ and λ equations carry opposite-sign first-order
    time derivatives (one backward-parabolic), for either sign of θ;
  - if b ≠ 0, χ propagates and the (χ, λ) kinetic form is indefinite (ghost);
  - only b = 0 with the normal derivative removed is leaf-elliptic.

  Checks: the signs of the σ coefficients in the χ and λ rows on FRW with H = ±1 (C938 vs intrinsic); and the (χ̇, λ̇)
  kinetic matrix eigenvalues for P1.
- **S2 (leaf-constant lemma).** The operator h∇∇ + a n·∂ + b(n·∂)² annihilates every leaf-constant f(T) iff a = K_T
  (= θ for the medium frame) and b = 0. That operator is the intrinsic Laplacian. Checks:
  - the identity ³Δχ = h∇∇χ + K_T n·∂χ is verified against the Laplacian of the induced metric on three geometries: Milne
    (exact, hyperbolic leaves), Bianchi I (exact, anisotropic) and perturbed FRW with a tilted leaf and Φ (O(ε), χ̄ ≠ 0, so
    the tilt matters);
  - the residual (a − K_T)f′/N is checked on perturbed FRW.
- **S3 (solvability ⇒ A7).**
  - On a compact leaf, ∫√h ³Δχ = 0, so ³Δχ = Km n_Σ − s is solvable iff s = Km N/V(Σ). Checks: symbolic divergence on a
    conformally curved periodic 3-torus, and numeric 32³ FFT (exact n̄: residual ≤ 1e-10; n̄ × 1.01: the k = 0 equation
    fails by Km·0.01·n̄).
  - On an infinite FRW leaf, with no subtraction, u grows linearly from an arbitrary centre and reaches the W_full wall
    u = a0 at r_wall = 3a0/(Km n̄). This is computed on both footings.
- **S4 (local form; n̄ as an integration constant).** The leaf-gradient form μ^i D_i(³Δχ − Km n_Σ) = 0 is local (A4-strict)
  and implies ³Δχ − Km n_Σ = c(T) on each leaf. Solvability (compact) or finite W energy (infinite: the wall) fixes
  c(T) = −Km n̄_Σ. Checks:
  - D_i f(T) = 0 while ∂_μ f(T) ≠ 0 (the leaf-gradient condition admits a function of T; the 4-gradient admits only a
    constant, as HT's Λ₀);
  - the linear dispersion determinant in this form equals the λ form's up to a nonzero factor.
- **S5 (AS206 cross-check, light).** The conformal specialization δΔ = −2σΔ + ∇σ·∇ in 3D is recomputed independently.
  This is used only to state that the λ³Δχ term's metric variation carries leaf derivatives only (astra's identity;
  astra's files are cited, never edited).

## 5. The mean density n̄: options

| id | option | scored on |
|---|---|---|
| N1 | leaf average n̄_Σ = N/V(Σ) (compact) or its Følner limit (infinite) | A4-record, A6, ∇T = 0 |
| N1′ | the same, entering only as the integration constant c(T) of S4 | A4-strict, A6, ∇T = 0 |
| N2 | a Λ₀-type global constant n̄₀ (∂_μn̄ = 0 via an HT-type pair) | solvability on FRW at z = 0, 1, 10 with n̄₀ = n̄(z = 0); r_wall on both footings |
| N3 | the medium's own local fields: (a) n̄ := n; (b) a K-proxy from the Hamiltonian constraint on CMC leaves | A2 (law kept?) and exactness (residual mean = 0?) |
| N4 | absorbed by a first-order normal derivative (C938) | A6 (Hadamard) |
| N5 | absorbed by a second-order normal derivative (P1) | A6 (no ghost) |

∇_μT^{μν} = 0 test (G-T): the foliation must be varied in the action, or be a functional of varied fields, and n̄ must be a
diff-invariant functional or an integration constant. Check: the foliation force E_T = ∂L₂/∂δT on the linear FRW system. For F0
(not varied) a nonzero E_T means ∇_μT^{μ0} = −E_T ≠ 0. FAIL iff E_T ≢ 0 for a non-varied foliation.

Two clocks (part c): reported YES iff
- on the surviving leaves, n̄_Σ is a strictly monotone function of the leaf label on FRW for H > 0 ("now" ticks), and
- the a0 constant is a spacetime constant (HT Λ₀; Branch A), not a leaf function ("scale" frozen).

## 6. Gates per candidate (all frozen here)

- **G-EX (existence).** Leaves exist and are spacelike on each background:
  - E1 expanding FRW; E2 contracting FRW; E3 turnaround (H = 0, compact leaf);
  - E4 static halo (NGC 3198's law state, medium at rest; CMC tilt H₀r/c computed);
  - E5 a medium with vorticity, both rigid rotation and WT-02's forced ε_ω (Frobenius: u∧du = 0 required for F1);
  - E6 a bound region over the medium's age: leaf slope c|∇t_leaf| = g t/c must be < 1 for F1′, evaluated with t = 13.8 Gyr
    and 1 Gyr at the Sun (1 AU) and at NGC 3198's radii;
  - E7 F4: does an HT gauge transformation T^μ → T^μ + ε^{μνρσ}∂_νω_ρσ change T⁰'s level sets while preserving
    ∂_μT^μ (symbolic)?

  PASS iff every applicable item passes. For F2, E1–E5 include the CMC lapse equation's potential
  V = K_ijK^ij + R_nn ≥ K²/3 − Λ + 4πGρ (> 0 required). Checked symbolically on FRW.
- **G-INT.** The linearised χ row (λ's Euler–Lagrange equation) and λ row (χ's) contain no σ at any power, on FRW with H = +1
  and −1 (symbolic).
- **G-NBAR.** The FRW background solves with χ̄ constant on leaves (no χ̄(t) needed), and S3 passes.
- **G-HAD (Hadamard).** Frozen-coefficient WKB on FRW. Units: time 1/|H|, length c/|H|, a = 1, ȧ = ±1, Ḣ kept as
  −(3/2)Ω_m(z)H² in matter + Λ. Grid:
  - Km = (3/2)Ω_c(z) with Ω_b = 0.0493, Ω_c/Ω_b = 5.364, Ω_Λ = 1 − Ω_m (flat, no radiation; CFG938's inputs);
  - z = 0 and 10; L* = 24 pc and 1 kpc; H > 0 and H < 0; gravity on (Φ = Ψ) and off;
  - k ∈ {1e2, …, 1e10} c/H (one value per decade), roots of det M(σ, k) = 0 by mpmath at 80+ digits.

  Labels:
  - **ILL-POSED** iff max Re σ ≥ 1e3|H| at the top k and the log slope over the top decade is ≥ 0.9;
  - **WELL-POSED** iff max Re σ ≤ 10|H| at every k and every background;
  - **UNRESOLVED** otherwise.

  Gravity-on and gravity-off must give the same label (K4).
- **G-T.** As in §5.
- **G-B (criterion B).**
  - The λ row has no σ, so no field needs final data.
  - Every finite cone lies inside the leaves' future: v_rel + c_s < c with the record's largest medium speed 4700 km/s
    (Bullet; ARGON10 G2, 3839aa9b0) and c_s ≤ 104 km/s (WT-02, L* = 1 kpc). The khronon cone shares the leaf normal
    (CFG292 T7).
  - PASS iff all hold.
- **G-NOGHOST.** The kinetic Hessian ∂²L₂/∂ḟ_i∂ḟ_j over the fields that appear with time derivatives (terms linear in ḟ
  excluded) is positive semi-definite. Lock and constraint multipliers carry no kinetic term. Primary A6 only.
- **G-STAT (static halo).** On NGC 3198's 43 radii (Υ = 0.61, `real_research/data/sparc_data/NGC3198_rotmod.dat`, both
  footings), the relative change of u from the leaf choice must be ≤ 1e-3:
  - for a halo at rest in the cosmic frame (CMC tilt H₀r/c, F2/F3);
  - for a halo moving at 370 km/s (boosted leaf: the induced metric δ_ij − v_iv_j/c²; sympy anisotropic Poisson for a point
    source, angle-maximized).

  F1 is exact by construction. Reported per candidate.
- **G-A3s (secondary).** The candidate adds no propagating mode (A3-strict).

Out of scope for every candidate (reported OPEN, not scored): nonlinear well-posedness; CMC existence theorems for the
non-compact inhomogeneous universe; khronon caustics in collapse; black-hole universal horizons (XR25: c₂ → ∞ singular at
O(α_c)); the ττ contribution to c_T (WT-09).

## 7. Verdict rules (frozen)

Scored over the candidate list of §3 (P1 and C938 included as candidates).
- **Primary reading** (A3-literal, A4-record, A6 = Hadamard + no ghost). A candidate SURVIVES iff it passes G-EX, G-INT,
  G-NBAR, G-HAD (WELL-POSED), G-T, G-B, G-NOGHOST and G-STAT. P1 is scored on G-HAD, G-NOGHOST and G-T only (it has no
  leaves).
  - **FORCED** iff exactly one candidate survives.
  - **MENU** iff two or more survive; give the discriminating test.
  - **NO-GO** iff none survives; give the minimal inconsistent subset of axioms with proof.
  - **UNDERDETERMINED** iff a gate is UNRESOLVED for a candidate that passes every other gate, or a K control fails (unless
    fixed by a disclosed amendment before the verdict is written).
- **Secondary readings**, each verdict reported by the same rule: (A3-strict: add G-A3s); (A6-Hadamard-only: drop
  G-NOGHOST); (A4-strict: N1 replaced by N1′; a candidate needs its n̄ in the N1′ form).
- **Part (a) label:**
  - L31 APPLIES iff its (iii) holds under A3;
  - otherwise, FOLIATION FORCED BY χ iff under the primary reading no surviving member is foliation-free (P1 fails);
  - else FOLIATION NOT FORCED.
- **Part (c) label:**
  - per option N1–N5: PASS / FAIL on A4 (each reading), A6, ∇T = 0;
  - TWO CLOCKS REPRODUCED iff §5's rule holds on a surviving candidate.
- **Part (d):** criterion B PASS/FAIL per survivor; static coincidence EXACT / ≤ ε (number) / FAIL.

## 8. Controls (each must pass; a failure makes the verdict UNDERDETERMINED unless fixed by a disclosed amendment)

- **K1 (WT-02 reproduced).** C938 on FRW:
  - χ row −k² − 3Hσ (forward-parabolic for H > 0), λ row −k² + 3Hσ (backward);
  - max Re σ/(c²k²/3|H|) = 1 within 1% at the top k on all 16 C938 backgrounds; slope 2.00 ± 0.02;
  - G-HAD reads ILL-POSED;
  - the χ̄̇ coefficient carries 1/H (no background at H = 0).
- **K2 (static reduction).**
  - (a) On any static slice of a general static weak-field metric (Φ(x), Ψ(x) symbolic), ³Δχ = h∇∇χ identically (θ = 0),
    so every intrinsic candidate's static law is CFG938's.
  - (b) The NGC 3198 law reduction from E[M_c] (own sympy Euler–Lagrange) gives max |g/g_law − 1| ≤ 1e-12 on both footings
    (CFG938: 2.2e-16).
- **K3 (lemma).** S2's identity holds with zero residual on Milne, Bianchi I and perturbed FRW.
- **K4.** Gravity-on and gravity-off G-HAD labels agree for every candidate.
- **K5 (khronon toy).** In the decoupled limit (Km = 0, Φ = 0, H → 0) the toy gives σ² = −c_k²k² exactly; with A < 0 it
  gives real σ ∝ k.
- **K6 (torus).** S3's FFT check as stated.
- **K7.** S4's determinant equivalence (λ form vs leaf-gradient form) holds up to a nonzero factor.

## 9. MUTATE (`WT07_MUTATE=1`; separate outputs `wt07_MUTATE.out`, `wt07_results_MUTATE.json`; exit 1 by design if every tooth bites)

- **MU1 (drop A7).** Intrinsic candidates without the subtraction. Bites iff G-NBAR flips to FAIL (no leaf-constant FRW
  background; torus k = 0 equation inconsistent).
- **MU2 (restore θu·∂).** Use CFG938's projected D² with χ̄(t) in F1, F2, F3. Bites iff G-HAD flips to ILL-POSED for each.
- **MU3 (khronon wrong sign).** A = −α_c. Bites iff F3's G-HAD flips to ILL-POSED (or G-NOGHOST flips).
- **MU4 (no vorticity).** Ω = ε_ω = 0. Bites iff F1's E5 flips to PASS. This shows that F1's failure is the vorticity.
- **MU5 (no potential gradient).** g = 0 in E6. Bites iff F1′'s E6 flips to PASS.
- **MU6 (vary the frozen foliation).** F0 with δT varied (it becomes F2-like or F1-like). Bites iff G-T flips to PASS.

## 10. Compute and hygiene

- One process, `OMP_NUM_THREADS=1 nice -n 10`, sympy + numpy + scipy + mpmath.
- In-script guard: exit 75 if RSS > 0.9 GB, if swap used grows > 1 GB above its start, or if free + inactive memory
  (`vm_stat`) drops below 8 GB.
- Before each run: check `ps -axo command=` for a live 1024³ `*_pm.py` job and for two other `wt0*.py` processes; if either,
  wait and say so. Peak RSS is measured with `/usr/bin/time -l`.
- No downloads. No other lane's files edited, staged or run (CFG960, CFG961, WT-06, WT-08, WT-09). Astra's files are cited,
  never edited.
- No personal names or home paths in repo files.
- Outputs: `DERIVATION.md`, `wt07.py`, `wt07.out`, `wt07_results.json` (+ `_MUTATE`), `README.md`. They are left
  uncommitted for orchestrator review. Changes after freezing go in appended amendments only.
