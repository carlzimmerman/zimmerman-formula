# H3_jeans_control: FROZEN CRITERIA (committed alone, before any script or number)

## Question (hostile)

H1's theorem T1 (`rebuild_2026_10_22/H1_aest_F/README.md`): in a Jeans-swindle background of AeST dust,
E_J/Γ² = −8k²D²/(I Q̄³ N²) < 0. H1 reads C5's "negative-energy ω = 0 mode" (C5 H10, defect (a)) as the dust's Jeans
growth mode, not a ghost. If so, health criterion (i) was mis-specified and AeST + γ_L + C1's capped F (μ = x/(1+x))
would be healthy up to ordinary gravitational instability.

This lane tries to break that reading. It is good news if true, so it is held to a fail-as-hard-as-a-win standard.

## What was done before this file (disclosure)

The lane read H1 and C5 (READMEs, scripts, JSON) and SZ21's text (`../_external_data/aest_papers_2026_10_22/
src_2007.00082/newRMONDLett.tex`, eq. `Minkowski_action` and the paragraph after it, which says the linear-in-t mode's
Hamiltonian is negative below ~μ and calls it "likely akin to Jeans-type"). **No sympy or numeric computation of this
lane has been run.** Pen-and-paper expectation (not a score): for Newtonian dust in Clebsch form the ρ̄ → 0 Jordan mode
is a static density lump whose energy is its gravitational self-energy, −2πG|δρ|²/k² < 0.

## 1. Machinery (shared, read-only)

- C5's `quad_matrix` and `jordan_energy` and C5's `sz_lagrangian` (SZ eq. `Minkowski_action`), exec'd from C5's source
  read-only, exactly as H1 does. Units 16πG̃ = 1 (4πG̃ = 1/4). Newtonian gauge, h^{0i} = 0, h^{ij} = −2Φδ^{ij}.
- The dust term is H1's: 2I[√−g(Q − Q̄)]⁽²⁾, I = K′(Q̄) > 0, K(Q̄) = 0, plus the vacuum K″ term 2K₂(δQ⁽¹⁾)².
  ρ̄ = 2IQ̄ in these units, so 4πG̃ρ̄ = IQ̄/2.
- The O(I) growth rate Γ² is the leading root of det M in the scaling (ω², I) → s(ω², I), as in H1.

## 2. Tests and pass lines

### T0. Machinery sanity (must pass, else UNDECIDED)
`jordan_energy` on (a) L = ½q̇² gives E_J > 0; (b) L = −½q̇² (ghost) gives E_J < 0; (c) first-order
L = p q̇ − ½p² gives E_J > 0. Signs +, −, + exactly.

### T1. The control: does criterion (i) flag ordinary gravity?
- **T1a GR + k-essence dust.** C5's GR (Fierz–Pauli) operator, i.e. `sz_lagrangian`'s first four terms, plus the same
  K-sector as AeST but with Q = √(−g^{μν}∂_μχ∂_νχ) (no vector; purely kinetic k-essence, c_s² = K′/(QK″) → 0 dust).
  Fields (Ψ, Φ, χ). E_J at I = 0 (vacuum, Q̄ = Q₀); Γ² at O(I).
- **T1b Newtonian self-gravitating dust**, Clebsch form, same machinery:
  L = −δρ(θ̇ + Φ) − ½ρ̄|∇θ|² − |∇Φ|²/(8πG), 8πG = ½. E_J at ρ̄ = 0; Γ² at O(ρ̄).
- **PASS ("criterion (i) flags normal gravity")** iff, in BOTH T1a and T1b: E_J(k) < 0 for every k > 0 (symbolic
  sign), AND Γ²(k → 0) = 4πGρ̄ exactly (sanity of the control), AND E_J/Γ² < 0 (T1's sign structure).
- **FAIL** iff either control has E_J ≥ 0 at some k > 0 where AeST's E_J < 0. That would mean AeST's mode is NOT
  the mode ordinary gravity has, and pushes the verdict toward CLAIM FAILS.

### T2. Ghost or instability? (AeST, λ₀ = 0 i.e. capped F at Y = 0, with and without γ_L)
Normalisation-free grading, plus one physical normalisation:
- **T2a** At I = 0, the ω = 0 root of det M has multiplicity exactly 2 (one non-propagating dust DOF), and every root
  with ω² ≠ 0 has ω² > 0 and positive Krein signature ω·v†(∂M/∂ω)v, at k ∈ {1e-3, 1, 1e3, 1e6}μ.
- **T2b** Lump normalisation. Define δQ on the Jordan solution (the static part of φ̇ − Q₀Ψ, i.e. the K-sector charge
  perturbation; δρ = 2Q̄K″δQ = 4K₂Q₀δQ at I = 0). Write E_J = −2πG_eff(k)|δρ|²/k² (calibrated on T1b, i.e. the
  coefficient T1b returns defines G_eff = G for Newton in this machinery).
  - GRAVITATIONAL FORM iff in AeST: δQ ≠ 0 on the Jordan mode; G_eff(k → 0) is finite and > 0; and without γ_L,
    0 < G_eff(k) ≤ G_eff(0) for every k (the lump's binding is Newtonian or weaker at every k). With γ_L, G_eff may
    turn negative only above a finite k_c (stable side), never grow above G_eff(0).
  - GR control T1a is put through the same normalisation; reported: G_eff^{GR}(k)/G.
- **T2 PASS (instability, not ghost)** iff T2a AND GRAVITATIONAL FORM.
- **T2 FAIL (ghost/pathology)** iff a root with ω² > 0 has negative Krein, or G_eff(k) grows above G_eff(0) without
  bound in k, or δQ = 0 on the negative-energy mode.

### T3. The vacuum case
At I = 0 (C5's E = −2k²(K₂Q₀² + k²)/(K₂Q₀⁴)-type expression): ρ̄_dust = 2IQ̄ = 0 exactly.
- **"Zero-background Jeans mode"** iff the negative-energy Jordan mode carries a dust density perturbation (δQ ≠ 0,
  T2b) AND the GR + k-essence control (T1a) has a negative-energy Jordan mode at I = 0 of the same kind (δQ ≠ 0,
  G_eff^{GR}(0) > 0).
- **"Genuine vacuum negative-energy mode"** (CLAIM FAILS) iff the mode has δQ = 0 (no matter content), or the control
  has no negative-energy mode at I = 0 while AeST does.
- Reported, not graded: whether the linear-order dust can carry δρ < 0 about a zero background (K at its minimum), in
  the control and in AeST alike.

### T4. The rate (exact roots of det M at finite I; H1's Lagrangian L0 + ΔL, no O(I) truncation of roots)
Declared values (none scanned, none fitted): K_B = 0.05, Q₀ = 1, μ = 1 (μ⁻¹ = 1 Mpc), K₂ = μ²(2−K_B)/(2Q₀²),
λ₀ = 0, L★ = 24 pc = 2.4e-5 μ⁻¹ (with γ_L) or 0 (without). I ∈ {2e-7 (4πG̃ρ̄ = 1e-7 μ², ≈ H² at μ⁻¹ = 1 Mpc),
2e-3 (stress)}. k on a log grid of 400 points over [1e-3, 1e6] μ plus H1's k_c(γ_L) = (2μ²/L★²)^¼ × {0.99, 1.01}.
- **T4a** at every k, at most one pair of roots has ω² < 0 (one unstable mode).
- **T4b** max_k Γ²(k)/(IQ̄/2) ≤ 1 + 1e-6 (the rate never exceeds √(4πG̃ρ̄)).
- **T4c** with γ_L: Γ² ≤ 0 at every grid k ≥ 1.01 k_c (the band ends at a finite k).
- **T4 PASS** iff T4a AND T4b AND T4c at both I. Reported: whether the band ends without γ_L (dust pressure from I).
- **T4 FAIL (pathological)** iff Γ² exceeds 4πG̃ρ̄ by more than 1e-6 relative, or Γ² grows with k at large k, or
  more than one unstable pair.

## 3. Verdict rule

- **CLAIM HOLDS** iff T0, T1 PASS, T2 PASS, T3 "zero-background Jeans mode", T4 PASS. Then criterion (i) as used by C5
  (E_J ≥ 0 at every k / SZ's λ_s > 0 at λ_eff = 0) flags ordinary gravity and is mis-specified, and AeST + γ_L +
  capped F is healthy at linear order up to ordinary gravitational instability. The README must still list what
  remains open, including C5's defect (b) (γ_L gives no causal cone), which this lane does not test.
- **CLAIM FAILS** iff T1 FAIL, or T2 FAIL, or T3 "genuine vacuum negative-energy mode", or T4 FAIL. The README says
  which mode, where (k range, background) and why.
- **UNDECIDED** iff T0 fails, or the tests split without any FAIL line triggered.

## 4. Checks (`Kn PASS/FAIL value threshold`)

- **K1** C5/H1 reproduction: AeST E_J (without and with γ_L) equals C5's JSON strings (sympy difference 0), and the O(I)
  Γ² equals H1's JSON strings (difference 0).
- **K2** T0's three signs.
- **K3** The GR operator used in T1a equals `sz_lagrangian` with the vector/φ terms removed: sz_lagrangian(K_B, K₂, Q₀,
  λ) − [GR part] − [AeST extras written out] = 0 symbolically.
- **K4** T1b Clebsch: the hand Noether energy H = δρΦ + |∇Φ|²/(8πG) + ½ρ̄|∇θ|² on the Jordan solution equals
  `jordan_energy`'s value (same normalisation), and Γ² = 4πGρ̄ at every k (cold Newtonian dust).
- **K5** T4 root solver: at I = 2e-7, the exact smallest root at k = 1e-3 μ matches the O(I) closed form to 1e-4
  relative.

## 5. Mutation (`H3_MUTATE=1`, outputs `*_MUTATE.*`)

Gravity is made repulsive in T1b (|∇Φ|² term sign flipped) and the dust sign flipped (I → −I) in T1a and T4.
K4 and T1's sanity line (Γ²(0) = 4πGρ̄) must FAIL.

## 6. Assumption ledger

| ingredient | class | source |
|---|---|---|
| SZ21 Minkowski action, λ_s condition, "Jeans-type" remark | literature, on disk | `../_external_data/aest_papers_2026_10_22/src_2007.00082/newRMONDLett.tex` eq. `Minkowski_action` + following paragraph |
| C5 `quad_matrix`, `jordan_energy`, `sz_lagrangian` (incl. γ_L term) | FRAMEWORK-NATIVE, exec'd read-only | `covariant_push_2026_10_22/C5_health/c5_health.py` |
| H1 dust term 2I[√−g(Q−Q̄)]⁽²⁾ and its O(I) consistency (vacuum part read at Q₀ ≡ Q̄) | FRAMEWORK-NATIVE (H1) | `rebuild_2026_10_22/H1_aest_F/h1_aest_f.py` |
| Jeans swindle (Minkowski + dust density, K(Q̄) = 0, no Hubble friction, k ≫ aH) | approximation (same for AeST and controls) | H1 |
| Newtonian gauge fixed in the action (h^{0i} = 0, traceless h_ij = 0) | approximation: legitimate when the gauge condition fixes gauge functions algebraically; tested empirically by T1a's Γ² = 4πGρ̄ | this lane |
| k-essence dust control (purely kinetic, Q = |∂χ|) | standard GR + CDM proxy (zero sound speed at K′ = 0); no data | this lane |
| Newtonian Clebsch dust | textbook fluid Lagrangian | this lane |
| capped F ⇒ λ₀ = F_Y(0)/(2−K_B) = 0 at Y = 0 | FRAMEWORK-NATIVE (C1, H1 K3) | H1 |
| K_B = 0.05, μ⁻¹ = 1 Mpc, L★ = 24 pc | declared (K_B BBN-allowed; μ⁻¹ SZ floor; L★ FITTED D10) | C2, SZ, D10 |
| I values (≈ H² scale, and stress) | declared, not data | this lane |

No data enter. No ΛCDM-processed input enters a graded line. Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS,
minutes, no downloads (a 1024³ job is live).
κ = ½ FITTED. Footings never pooled (no footing enters). No dark-matter particle. Never "theory closed". Nothing here
says the data favour the framework.

## AMENDMENT A1 (post-result, 2026-10-22): code fixes and reported additions; no pass line or declared value changed

Run 1 (`*_RUN1.*`) is kept. A1-1: Q₀ > 0 in the k-essence norm (Run 1 left Abs(Q₀)). A1-2: K5's O(I) closed form kept I
symbolic (Run 1 substituted I = 0, rel = inf). A1-3: T3 coded to the frozen wording (Run 1 added "control E_J < 0 at
every k"). A1-4 (reported only): the lump's static potential G_pot, the GR + k-essence exact-root scan, Krein of every
ω² > 0 root at I > 0. A1-5: the verdict mapping coded to §3 (Run 1 sent any K failure to UNDECIDED). The frozen verdict
is printed first in the README; the post-result reading of each FAIL line is labelled as such.
