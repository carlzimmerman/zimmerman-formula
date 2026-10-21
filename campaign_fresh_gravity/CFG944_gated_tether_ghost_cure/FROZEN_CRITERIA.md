# CFG944: curing the ghost of the turnaround-gated tether (frozen criteria, committed alone)

Block CFG940–949 (owner, 2026-10-20 ~23:45: "launch agents on option 1" = the collapse-gated tether, CFG941 R3θ; LEDGER row
CFG940–949). This file is written and committed **before** any derivation output, script or number of this lane. It fixes the
questions, the cures, the tests, the controls and the class rules. Any later change is a dated, labelled amendment in this
directory.

**Settings.** κ = ½ FITTED (never derived). Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), never pooled. The
extra mass is cold energy, never a dark-matter particle; no particle species is added. Framework-native inputs only; no ΛCDM or
standard-MOND yardstick in any verdict. Not "theory closed"; never "the data favour the framework". NO CURE is reported as plainly
as a cure.

**Inputs (read only).**
- CFG938: the parent P0, its reduced static Euler–Lagrange equation, its NGC 3198 number (2.2e-16), its slip definitions
  (s_∇, s_847) and worst s_847 = 1.5398e-5, its dispersion (S5a).
- CFG941: R3θ = P0 with the tether sector (W_full and the stiffness) multiplied by s(θ) = 1 − S5(θ/θ_s) on [0, θ_s], s = 1 for
  θ ≤ 0, s = 0 for θ ≥ θ_s, S5(x) = 6x⁵ − 15x⁴ + 10x³, θ_s = H₀, θ = ∇_μu^μ the medium's expansion; its k_g formula and nine values
  (`cfg941_results.json`); its growth machinery (n = 0.60954 / 0.69433 / 1) and c₂,max = 2.35e-3 (|n − 1| < 1e-3); its R3n numbers;
  theorem D-T; the hover lemma; its (g) definitions g1–g3.
- Class A: the CFG650/CFG654 engine code and READMEs (read with the Read tool only; never run, never imported).
- CFG654's native linear table `cfg654_ics_tables_cmb.npz` (addendum A1 primary: CAMB in the switch-off era, A_s from the CMB
  primary, H₀ from θ*). Used ONLY for the amplitude of linear perturbations in (c-amp). Its caveats are inherited (A_s from a
  base-ΛCDM fit of the CMB primary spectrum, massless ν).
- CFG847's five systems (slip line 1.9e-5); the record's SPARC file for NGC 3198 (Υ = 0.61, as CFG938/941); `CFG4_common.A0`;
  declared cosmology as CFG941 (Ω_b 0.0493, Ω_c/Ω_b 5.364, H₀ 67.4; matter era treated as EdS for z ≤ 1100).
- LEDGER and THEORY_CANONICAL were searched for a BBN bound on G_cosmo: none is on record (CFG172/195/897 discuss the aether
  Friedmann factor without a bound).
- Nothing is downloaded. CFG938/939/941/945 files, LEDGER and THEORY_CANONICAL are not edited.

## 1. Ghost re-derivation (each answered in DERIVATION.md with a sympy check)

- **G1.** Exact second variation of any θ-dependent medium term ∫√−g F(θ, u) in label coordinates, where θ = J̇/J (J the Jacobian
  of the map from labels to positions). Is it the rank-one form ½(F_θθ/J₀)(δJ̇ − θ₀δJ)²?
- **G2.** For one Fourier mode, is the second-order part of J a divergence, so that the longitudinal kinetic coefficient is exactly
  ρ₀ + F_θθk² (WKB, J₀ = 1)? For R3θ F_θθ = −s″(θ)W(u), so the ghost condition is s″Wk² > ρ₀.
- **G3.** Frozen-coefficient dispersion: (ρ₀ + F_θθk²)ω² = ρ₀Ω²_P0(k; s₀) − F_θθk²θ₀², with Ω²_P0 the CFG938 S5a form whose tether
  is multiplied by s₀ = s(θ₀). The k¹ gyroscopic terms from F_θu are subleading at large k and are stated, not dropped silently.
  Is ω² unbounded below near k_g (a degenerate kinetic surface)?
- **G4 (K).** CFG941's nine k_g R values.
- **G5.** Transition states reached from settled galaxies: k_g r at NGC 3198's 43 radii, with the medium density equal to the law's
  phantom density and W at the law's u, for perturbations that put θ in the convex half of the gate.

## 2. Cures (declared now; at most one new constant each)

The object is R3θ:
  S = ∫√−g [c⁴R/16πG − mc²n − s(θ)(W_full(u) + (3γ/4K²)τ_μντ^μν) + λ(D_μD^μχ − Kmn)] + S_b,
with W_full = [−a₀u − a₀² ln(1 − u/a₀)]/K (defined for u < a₀), K = 4πG, γ = 2πGL*².

- **C1 (aether-like term, always on).** Add +(c_θ/2)θ² to the medium Lagrangian. New constant c_θ [kg m⁻¹].
  - Derive G_cosmo/G_N with a minisuperspace action including the lapse (sympy), and the static G_N.
  - Derive the extra inertia c_θk_phys² of linear perturbations.
  - Ghost bound: c_θ ≥ c_θ,g = s″_max × max W over each declared transition set (T1–T3, §3(d)).
  - Growth window c_θ ≤ c_θ,max from (c). Compare the two.
- **C2 (gate on a non-derivative variable).** Three variants, each with one constant (its threshold):
  - (i) ρ_c (= CFG941 R3n): state what differs from R3θ.
  - (ii) χ itself.
  - (iii) a label or latch field enforced by a multiplier. This includes the clock–density variable Y = Kρ_cT², with T the medium's
    proper time (u^μ∂_μT = 1, enforced by a multiplier); Y's cosmic-mean value is constant in EdS.
  - Graded analytically with sympy checks and CFG941's R3n numbers. R3n is not rerun.
- **C3 (gate profile alone).** Any s(θ), smooth, saturating or with bounded s″, in the R3θ structure.
  - Theorem to prove or refute: does any s give ρ₀ − s″Wk² > 0 for all k while keeping (a) and (c)?
  - Report the gate that minimizes max s″ (θ_s ≤ 3H₀) and its k_g. No new constant.
- **C4 (u-saturated gate + transition-localized convex θ-term).** Justification: W_full is unbounded as u → a₀, so any θ-only
  kinetic cure is overwhelmed at large u. The minimal remedy is to make the gate θ-independent where W is large and to add the
  smallest convex θ-term that dominates the residual s″W elsewhere.
  - Gate: s(θ, u) = ŝ(θ) + h(u)(1 − ŝ(θ)), with ŝ = R3θ's gate and h(u) = S5(2u/u_c − 1) on [u_c/2, u_c] (0 below, 1 above).
  - Convex term: L₀(θ) with L₀″ = W_g · 60x(1 − x)/θ_s² for x = θ/θ_s ∈ (0, 1); L₀ = 0 for θ ≥ θ_s; L₀ linear for θ ≤ 0.
  - W_g = max over 0 ≤ u ≤ u_c of (1 − h(u))W_full(u).
  - New constant: u_c only; W_g is fixed by it.
  - The stiffness is NOT gated in C4 (always on), so the ghost condition involves W only. Its sub-L* Jeans effect in the linear
    regime is reported, not graded (as CFG941 R1).
  - Bag: B₀ = L₀(0), a vacuum term (T_μν = B₀g_μν) in every region with θ ≤ 0.
- **Theorem G (declared statement; to be proven or refuted).** Take any local Lagrangian L(θ, u) of the medium's expansion and its
  tether invariant. Assume:
  - (a): L(0, u) = −W_full(u) + const on the static states of NGC 3198;
  - (c-amp): L(θ, u) = L(θ, 0) on the linear locus;
  - (d): L_θθ ≥ 0.
  Then every static region carries a vacuum offset B ≡ L(0, 0) − T(0) ≥ W_full(u*). Here T is the linear function equal to L(·, 0)
  on the cosmic range, and u* = min(max u on NGC 3198, U_max). With (e) bounding B ≤ B_e, the theorem is a no-go iff
  W_full(u*) > B_e.

## 3. Tests per cure

- **(a) Static law + deep BTFR.** As CFG941 (with its A1): max |g/g_law − 1| < 1e-6 at all 43 NGC 3198 radii on both footings, the
  symbolic limit lim V⁴/(GM_b a₀) = 1, and the numeric value at y = 1e-14 within 1e-6 of 1.
- **(b) FRW.**
  - Requirements: T^μ_ν diagonal and isotropic; the medium is dust (w = 0); the cure's added terms vanish on FRW.
  - For C1, the FRW effect is computed (G_cosmo/G_N) and stated as the cure's cost. CURED needs no FRW effect. CURED-WITH-COST allows
    a stated G_cosmo shift with its needed range.
  - The record has no BBN bound on G_cosmo, so a range is stated and not graded against literature.
- **(c) Linear growth (literal).** As CFG941's frozen (c), from the quadratic action: |n − 1| < 1e-3 at every z ≤ 1100 and comoving
  k ∈ [0.01, 5] h/Mpc at super-L* scales.
  - For C1 the c_θ inertia is part of the quadratic action. Use two-component EdS growth with the medium's inertia ρ̄_c + c_θk_phys²
    and background G_cosmo, started in the dust growing mode at z = 1100; take the local exponent along the history.
- **(c-amp) Linear growth at the actual amplitude.** New in this lane; it applies to any cure whose switch reads an amplitude variable
  such as u.
  - PASS iff the effective tether coefficient at the 1σ linear medium field U(z) is ≤ c₂,max = 2.35e-3 at every z ≤ 1100, AND the
    tether's argument stays inside W_full's domain (u < a₀) wherever the tether is not exactly zero.
  - U(z) = f_c (3/2) H₀² Ω_m (1 + z)² [∫ P(k, z) dk/2π²]^{1/2}, with the integral over k ∈ [0.01, 5] h/Mpc and P from CFG654's native
    table scaled by the table's own D(a); parameters from the table.
  - The D5 χ̄ boost is omitted, which lowers U. f_c is the medium's share.
  - For θ-only gates (R3θ, C1, C3) (c-amp) ≡ (c), because the gate does not read u. The literal (c) is reported alongside.
- **(d) Well-posedness.**
  - PASS iff, at every k and every state in S = {θ ∈ ℝ} × {u ∈ [0, a₀)}, the kinetic matrix is positive definite and the
    frozen-coefficient ω² is real or bounded below independently of k.
  - A cure whose (d) holds only on a sub-region is reported with the exact region. Declared transition sets:
    - T1: CFG941's nine turnaround examples, u at R/2 (as CFG941);
    - T2: the same with the edge field u = Kρ₀R/3, capped at 0.999a₀;
    - T3: NGC 3198's 43 radii, as settled states perturbed into the transition.
  - CFG938's conditions (γ > 0, ρ_c c² > D(u)u/K) are inherited.
- **(e) Slip.** s_∇ and s_847 (CFG938's definitions) ≤ 1.9e-5 on CFG847's five systems, both footings, on the cure's own static
  states, with any vacuum (bag) term B added to p_r and p_t.
- **(g) Class-A limit, equation by equation.** The terms:
  - g1 universal coupling: every cold element feels −∇Φ with ∇²Φ = K(ρ_b + ρ_c [+ class A's src]);
  - g2 the settled phantom's input contains baryons only (no settled-medium term from neighbours or host);
  - g3 the linear regime is pure dust;
  - g4 the switch is class A's catchment rule (turnaround balls around resolved peaks);
  - g5 the source is zero-sum per catchment by instantaneous redistribution.
  PASS iff g1–g5 all hold. PASS ⇒ the T1x/T2x/NC1x shear passes transfer; otherwise they do not.
- **F2.** Studied in CFG945 and not duplicated here. Only what the cure implies for the settled sector is noted.

## 4. Classes (frozen)

Per cure:
- **CURED:** (a), (b), (c) [and (c-amp) where it applies], (d) globally and (e) all pass; (g) reported.
- **CURED-WITH-COST:** as CURED, but the new constant is confined to a stated, non-empty window and/or it shifts G_cosmo (stated).
- **REGIONAL:** (a)–(c) and (e) pass; (d) holds exactly only on a stated sub-region that contains T1–T3.
- **NOT CURABLE:** a theorem, or a computation over the cure's whole constant range, shows that no value passes (a)–(e)
  [with (c-amp)] together.

Overall:
- **GHOST CURED:** at least one cure is CURED or CURED-WITH-COST.
- **CONDITIONAL:** none is, but at least one is REGIONAL (region and conditions listed).
- **NO CURE:** every cure is NOT CURABLE AND Theorem G passes its checks (a no-go for local L(θ, u)).
- **NO CURE FOUND (no proof):** every cure is NOT CURABLE but Theorem G fails.

## 5. Controls

**K (must pass, else VOID until fixed and disclosed):**
- K1: NGC 3198 law from P0's reduced EL, < 1e-6 on both footings (CFG938: 2.2e-16).
- K2: BTFR symbolic limit 1; at y = 1e-14 the numeric value is 1 ± 1e-6 on both footings.
- K3: growth by CFG941's route: n(c₂ = 1, no χ̄ boost) = 0.60954 ± 1e-5; n(c₂ = 1, boost) = 0.69433 ± 1e-5; n(c₂ = 0) = 1 ± 1e-12
  (R3θ's linear regime); c₂,max reproduced to 1%.
- K4: CFG941's nine k_g R values to relative 1e-6; s″_max = 5.7735 to 1e-4.
- K5: CFG938's worst s_847 = 1.5398e-5 to 2%.
- K6: G1's identity reproduces CFG941's −½s″W(∇·v)² at θ₀ = 0 (sympy).

**MUTATE (separate `_MUTATE` outputs; exit 1 by design when every tooth bites, 2 if a tooth fails):**
- M1: remove C4's cure (W_g → 0, h ≡ 0) → R3θ's ghost returns (min F_θθ < 0; k_g finite on T1).
- M1b: C1 with c_θ = 0 → the same.
- M2: C1 with c_θ = ½c_θ,g(T1) → a ghost remains on T1.
- M3: C4 with W_g → ½W_g → F_θθ < 0 somewhere.
- M4: C4 without the u-saturation (h ≡ 0), at its own W_g → F_θθ < 0 at large u.
- M5 (amplitude tooth): U ≡ 0 → C4's window opens (some u_c passes (a)–(e)), which shows that (c-amp) is what does the work.
- M6 (Theorem G tooth): drop (a) at u > 0 (u* → 0) → B_min = 0 ≤ B_e, i.e. the bound bites only through the static law.

## 6. Hand expectations (design-stage mental estimates, no script run; disclosed, not results; may be wrong)

- **G1/G2/G3.** The rank-one form holds and the kinetic coefficient is ρ₀ − s″Wk². ω² is unbounded below near k_g.
- **G5.** In galaxy interiors k_g r ≪ 1, so the ghost band covers all galactic scales.
- **C1.**
  - For +(c_θ/2)θ², G_cosmo = G/(1 − 12πGc_θ/c²), i.e. Einstein-aether c₂ = −8πGc_θ/c² in G/(1 + 3c₂/2); and G_N = G.
  - The ghost bound on NGC 3198's interior (u ~ 0.8a₀) needs 12πGc_θ/c² ~ 0.3, which reaches 1 near u ~ 0.94a₀.
  - The extra inertia c_θk²/ρ̄ ~ 1e2–1e8 freezes growth. Expected NOT CURABLE.
- **C2.**
  - The density gate trades the θθ ghost for a ρρ gradient instability and fails (a), as R3n did.
  - The χ gate breaks χ's shift symmetry and cannot separate collapsed from linear regions (|δχ_lin| ≫ galactic well depths).
  - A latch either carries λ̄F_θθ ghost terms or reduces to a density/clock gate (Y = Kρ̄T² = 2/3 for the EdS mean).
  - Expected NOT CURABLE.
- **C3.** Ghost-free ⇔ s is concave wherever W > 0. A concave s with s(0) = 1 and |s(3H(z))| ≤ 2.35e-3 at z = 0 and z = 1100 is
  impossible. min max s″ = 2/θ_s², which raises k_g by ~5 at θ_s = 3H₀. Expected NOT CURABLE.
- **C4.**
  - (a), (b), (d) and the literal (c) pass; (e) caps u_c near 0.3a₀.
  - (c-amp) is expected to fail. Estimate from v_rms ~ 400 km/s: the 1σ linear medium field is ~0.01a₀ today and rises ∝ (1 + z)
    to ≳ a₀ by z ~ 100.
  - Expected NOT CURABLE.
- **Theorem G.** Expected to hold, with B_min ≥ W(u_N,max) ~ 0.5–1 a₀²/K against B_e ~ 0.05 a₀²/K.
- **Side flag (estimate, reported, not graded).** P0's always-on tether argument u is expected to leave W_full's domain (u ≥ a₀) at
  z ≳ 100 on typical points. CFG938/941 files are untouched.
- **Expected overall: NO CURE.** These expectations may be wrong; results are reported as they fall.

## 7. Compute

One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, an in-script RSS guard aborting above 1 GB, sympy + small
numpy/scipy, seconds. A live 1024³ job (NC2x) runs beside this lane; nothing touches it.
