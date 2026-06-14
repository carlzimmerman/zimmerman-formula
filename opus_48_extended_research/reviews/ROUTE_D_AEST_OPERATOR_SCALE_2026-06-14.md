# ROUTE D — is there a DIFFERENT AeST/scalar operator whose natural scale lands at ~300-450 kpc (cluster cores) while staying OFF in galaxy disks? — VERDICT (2026-06-14)

**Grade: CLOSED-FALSIFIER (no framework-native operator delivers a DERIVED, density-localized, SPARC-safe,
right-signed 300-450 kpc scale). One genuinely new scale was surfaced and credited (r_C, the oscillatory-onset
radius) — but it is an ONSET radius not an amplitude, it rides the same free per-cluster boundary tune (Δ) as the
banked mass-term, and the one truly DIFFERENT operator (m_×) is spherically INERT.**

Companion scripts: `/tmp/route_d_rC.py`, `/tmp/route_d_signcheck.py`, `/tmp/route_d_mcross.py` (numbers reproduced
inline below). Quarantine held: a0/Z never asserted derived; every scale flagged derived-vs-tuned.

---

## The question (Route D, sharpened)
The banked closing-calc (`AEST_SINGLE_MU_GAUNTLET`, `DENSITY_A0_ELL_1MPC_VERDICT`) killed the scalar mass term's
Compton scale 1/μ ~ 1 Mpc (CMB-pinned) as the cluster smoothing scale: at 1 Mpc it breaks SPARC AND over-closes.
Route D asks whether a **DIFFERENT** framework-native operator carries an intrinsic scale in the **~300-450 kpc**
cluster-core window while staying OFF in galaxy disks — via (i) the K-essence kinetic-term scale vs the mass scale,
(ii) a density-dependent effective Compton wavelength 1/μ_eff(ρ), or (iii) a derived K(Q) free function.

## What the AeST literature actually contains (paper-sourced, two independent fetches agree)
The quasi-static weak-field AeST (Verwayen–Skordis–Złošnik 2024, MNRAS 531 272, arXiv:2304.05134; the m_× paper
arXiv:2305.07742; Skordis–Złošnik 2021) carries exactly these scales:

| object | formula | scale | ρ-dependent? | spherical effect? | sign vs MOND |
|---|---|---|---|---|---|
| **μ²Φ mass term** | μ = Q₀√(2K₂/(2−K_B)), 1/μ ≳ 1 Mpc (CMB-pinned) | ~1 Mpc | NO (global) | YES | banked: η~0.96, **no boost** |
| **r_C oscill. onset** | r_C≈⅓[18 r̂_M/(μ²(1+3\|Δ\|))]^{1/3}, r̂_M=r_M/(1+β₀) | 150–900 kpc | via M & **free Δ** | onset radius only | amplitude = mass-term (drain) |
| **m_× ("new scale")** | m_× = Q₀√((2−K_B)/(2K_B)) | ~Mpc (Q₀-set) | NO (global) | **ZERO (double-curl)** | ~1% wide-binary only |
| **K(Q) free function** | K = −2Λ + K₂(Q−Q₀)² + … | sets μ; 1/μ≳1 Mpc | NO (global) | sets μ only | not foundation-forced |

## (i) The kinetic-term scale vs the mass scale — they DIFFER, and a genuinely new in-window scale exists (r_C)
**This is the real, creditable finding.** The kinetic structure of the AeST scalar does NOT collapse to the single
1/μ scale. VSZ2024 identify **three regimes** with **distinct transition radii**, none equal to 1/μ:
`r_χ = r_M/(1+λ_s)`, `r̂_M ≈ r_M/(1+β₀)`, and the oscillatory-onset radius
**`r_C ≈ ⅓[18 r̂_M/(μ²(1+3|Δ|))]^{1/3}`** (Eq. 21). r_C is the geometric blend of the MOND radius and 1/μ²; it
scales as **`r_C ∝ M^{1/6} μ^{−2/3} a₀^{−1/6}`** — DIFFERENT from 1/μ, and it lands in the hundreds-of-kpc band:
- Validation: my Eq.-21 evaluation gives 203 kpc (paper's fiducial = 156 kpc; the ~1.3× gap is the paper's stated
  "factor ⅓ conservative" and exact λ_s/β₀ — order and scaling confirmed).
- At the CMB-pinned μ=1 Mpc⁻¹, Δ=0: L* disk r_C≈185 kpc, group (10¹³) r_C≈433 kpc (**in window**), fiducial cluster
  (5×10¹⁴) r_C≈832 kpc (**above window**). **r_C lands in 300-450 kpc only for group/small-cluster masses, not the
  fiducial cluster** — because the M^{1/6} scaling is too weak to track R500.

So (i) is honestly answered: a second, kinetic-origin scale **does** exist and **can** sit at a few×100 kpc. But:

## The two reasons r_C does NOT solve the cluster deficit (sign + tune)
**SIGN.** r_C is only the **onset radius** of the μ²Φ oscillatory regime — it says WHERE the bend begins, not that it
BOOSTS. The amplitude/sign at and beyond r_C is the exact physics the banked mass-term gauntlet already settled:
Durakovic–Skordis "a peak FOLLOWED BY A DEFICIT (negative phantom mass)"; `AEST_SINGLE_MU_GAUNTLET` natural-BC
**η(R500)=0.96**; `cluster_aest_massterm` natural-BC **g_AeST/g_MOND=0.21 at R500** — a **DRAIN, wrong sign**. A new
onset radius inherits the same amplitude verdict.

**TUNE.** r_C depends on **Δ**, the inner-boundary deviation — which is **exactly the free per-cluster boundary shift
χ_inf** the gauntlet identified as the tuning knob. r_C slides **832 → 268 kpc as Δ goes 0 → 30** (computed). So
"landing r_C at 300-450 kpc" is **achieved by choosing Δ** — the same per-cluster tune, re-expressed as a radius.
**Not a forced second scale.**

## (ii) Density-dependent effective Compton wavelength 1/μ_eff(ρ) — DOES NOT EXIST in AeST
μ² = 2K₂Q₀²/(2−K_B). Q₀ is the **cosmological** background temporal-scalar velocity ⟨A^μ∇_μφ⟩ in FLRW; K₂, K_B are
action constants. **None is a function of local ρ_b.** Both 2024 fetches state explicitly the transition scales
depend on (M, μ, inner BC) — **NOT on ρ_b**; "the parameters are genuinely cosmological constants, not screening
mechanisms responding to environmental conditions." In the quasi-static cluster limit Q→Q₀ as a boundary condition
and the local δQ the EOM solves for does **not** feed back into μ (μ is pinned at the K-expansion minimum Q₀). So
**1/μ_eff(ρ) is not a framework object** — AeST is NOT a chameleon/density-screened scalar; its scale is set
cosmologically, not locally. To introduce μ_eff(ρ) would be a NEW tuned Q-structure, not a derivation.

## (iii) A derived K(Q) that shrinks the scale in cores — NOT forced, and would have to break the CMB pin
K(Q) is the **cosmological (temporal-Q) sector** (CDM-mimic for the CMB). Banked `project02_aest_K_of_Q.py`: the
horizon foundation does **NOT** force K(Q) — it must carry a mass ~6500 H₀ to cluster by recombination, while the
dS horizon supplies only ~H₀ (dark *energy*). K(Q) sets Q₀, K₂ → hence μ; but the CMB acoustic fit **IS** what pins
1/μ ≳ 1 Mpc. A K(Q) that shrank the scalar's Compton wavelength to 300-450 kpc **in cluster cores** would need to be
Q-dependent in a way that (a) is not foundation-forced and (b) leaves the cosmological Q₀-minimum (hence the CMB)
untouched while changing μ locally — but μ is **evaluated at the Q₀ minimum, which is cosmological**. No derived K(Q)
delivers a density-localized in-window scale without a new tuned input.

## The one genuinely DIFFERENT operator (m_×) — surfaced, and it is the WRONG TOOL
The m_× paper (arXiv:2305.07742, "A new scale in the quasi-static limit of AeST") is the literal "different
framework-native operator" Route D hypothesizes. Findings (paper-sourced):
- **m_× = Q₀√((2−K_B)/(2K_B))** — proportional to the **same Q₀** as μ; m_×/μ = √[(2−K_B)²/(4K_BK₂)] = O(1), so
  **1/m_× is also ~Mpc** unless (K_B,K₂) is tuned (computed: 1/m_× spans 0.1–6 Mpc across K_B∈[0.1,1], K₂∈[0.1,10];
  300-450 kpc needs deliberate tuning, and even then it is a **global constant**, identical in disk and cluster).
- **m_× has NO EFFECT IN SPHERICAL SYMMETRY (exact):** it multiplies only the double-curl ∇×∇×U⃗, which vanishes
  identically for spherical systems. **Cluster cores are modeled spherically → m_× is constitutionally inert there.**
- Where it acts (non-spherical), it is **~1% in wide binaries** and "does not affect the ability of AeST to reproduce
  MOND." Wrong amplitude (need ~2×, get ~1%), wrong geometry (off in spherical), wrong sign-story (untested boost).

So the most promising "different operator" is **spherically inert and percent-level** — it cannot supply the cluster
core's η~2.

## VERDICT: CLOSED-FALSIFIER (both ways)
**No framework-native AeST operator delivers a DERIVED, density-localized, SPARC-safe, right-signed scale in the
300-450 kpc cluster-core window.** The three sub-routes resolve:
- (i) A genuinely **new** kinetic-origin scale exists and CAN sit at a few×100 kpc — **r_C, credited as a real
  finding** — but it is an *onset radius not an amplitude* (inherits the mass-term's η~0.96/0.21 **drain**), it scales
  as M^{1/6} (too weak to track R500: in-window only for groups), and "landing it in 300-450 kpc" rides the **same
  free per-cluster Δ tune** the gauntlet already flagged. **Re-tuning under a new name, not a forced scale.**
- (ii) **1/μ_eff(ρ) does not exist** — AeST's scale is cosmological (Q₀), not density-screened. Manufacturing one is
  a new tuned input.
- (iii) **No derived K(Q)** shrinks the scale in cores without breaking the CMB pin (1/μ ≳ 1 Mpc) — and K(Q) is not
  foundation-forced.
- The one truly **different** operator, **m_×, is spherically INERT** (double-curl) and ~1% — wrong tool for spherical
  cluster cores.

**Both ways:** credited — r_C is a real, paper-sourced, framework-native scale distinct from 1/μ that does sit in the
right ballpark for groups (not manufactured-away); the regime structure is genuinely richer than a single Compton
wavelength. Failed on the merits — r_C is an onset not a boost, rides the Δ tune, and scales wrong in M; 1/μ_eff(ρ)
isn't an AeST object; m_× is spherically inert. This is **consistent with and converges on** the banked nulls
(`AEST_SINGLE_MU_GAUNTLET` FALSIFIED-AS-CLOSURE, `DENSITY_A0_ELL_1MPC` BREAKS+OVER-CLOSES,
`ELL_DESITTER_UNRUH_HORIZON` SCALE-IS-COSMOLOGICAL): every AeST/density route to a second in-window cluster scale
either reduces to 1/μ, requires a per-cluster tune, or is spherically inert. **The falsifier is closed; bank it.**

*Sources: Verwayen, Skordis & Złošnik 2024 MNRAS 531 272 (arXiv:2304.05134); "A new scale in the quasi-static limit
of AeST" arXiv:2305.07742; Durakovic & Skordis 2024 JCAP 04 040 (arXiv:2312.00889); Skordis & Złošnik 2021 PRL 127
161302 (arXiv:2007.00082); Mistele+2023 A&A 676 A100 (arXiv:2301.03499). Banked companions:
AEST_SINGLE_MU_GAUNTLET_2026-06-14.md, DENSITY_A0_ELL_1MPC_VERDICT_2026-06-14.md,
ELL_DESITTER_UNRUH_HORIZON_VERDICT_2026-06-14.md, project02_aest_K_of_Q.py.*
