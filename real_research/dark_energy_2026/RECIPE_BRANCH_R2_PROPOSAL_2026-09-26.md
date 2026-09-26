# Proposed ingredient adjustments for the crispy fried chicken recipe — Branch R2 (2026-09-26)

**Status.** A proposal for whoever owns the next edit of
[`CRISPY_FRIED_CHICKEN_RECIPE.md`](../../qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md). It does
not edit the recipe. On 2026-09-26 the lead track added its own dated amendment to the recipe ("ingredient and evidence
reconciliation", with audits in `real_research/closure_resume_2026_09_26/`; both uncommitted at the time of writing),
keeping the thirteen-requirement spec as the success contract and the exact exponential law as its target. This proposal is
consistent with that amendment. It lists what the calculations since the recipe's last edit (09-09) force on the
**alternative filtered branch** the record has actually built (C-H/K), labelled Branch R2 as the recipe's §1 requires
("changing μ = a different recipe, branched explicitly, never silently substituted"). Every row cites the committed
lane; labels follow the lead track's stricter scoping.

**Update, same day:** the author decided three of this proposal's open items, recorded in the recipe and spec by
commit 9092fc0fd — the kernel is ν_mono, causality is criterion B, and the Z line is corrected. The remaining items below
(I6 the vacuum gate, I7 the dark mass, G13–G21, P8–P16, §9 and §12.6) are still proposals. One consequence recorded both
ways: under criterion B the signalling theorem no longer closes the strict two-DOF constraint branch (CDE-L4C is open
again).

## 1. One factual error in the recipe as it stands (fixed in 9092fc0fd)

§1's Numbers line says "Z~21 FITTED". On the record's definition Z ≡ cH_Λ/a₀, with a₀ = κc√(Gρ_Λ) and the vacuum
Friedmann normalization H_Λ² = Λc²/3, one has **Z² = 8π/(3κ²)**, so Z is κ restated, not a second fitted number; at
κ = ½, **Z = √(32π/3) = 5.7888**. The "~21" was an error corrected on the record on 09-16. Lean:
`Z_is_kappa`, `Z_at_half` in [`DE_vacuum_gate_certificates.lean`](../../fable_independent_2026/lean_2026/DE_vacuum_gate_certificates.lean).

## 2. Ingredients of Branch R2

| ingredient | recipe (09-09) | Branch R2 | status / forced by |
|---|---|---|---|
| a₀ normalization | κ = ½ fitted | κ measured 0.465 ± 0.076 (BTFR), 0.55 ± 0.17 (distance-free), consistent with ½; not derivable in the present action class | `kappa_closure/k01–k03`; the four-form promotion (k04) is a distinct action proposal that moves the question to one free ratio, κ = ½ ⟺ Z_q/β² = 7.96 (Z_q = the four-form's stiffness, k04's P(q) = Z_q q²/2 — not the framework's Z = 5.7888) |
| a₀(z) | "a₀(z) ∝ √ρ_DE(z) = TARGET" | the stage-17 promotion a₀² = κ²G(−p_vac) (a postulate); for a w = −1 vacuum it gives a **flat** a₀(z) (< 1% to z = 5). √ρ_DE(z) for an evolving dark energy is the naive promotion the record rejects | L37, L273–L275 |
| I1 kernel | exact μ(y) = 1 − e^{−y} | **Branch R2 uses ν_mono** (ν_RAR = 1/(1−e^{−√y}) below its phantom peak y_p = 2.54, a monotone phantom above; ≤ 0.01 dex from ν_RAR on SPARC). This is a different constitutive law and does **not** meet spec requirements 1/12. Reason for the branch: the exact law's longitudinal coefficient C_L = (1−x)/(eˣ+x−1) is negative for x > 1 (exact), and L340's tested momentum channels need C_L > 0 (243/243 negative cells unhealthy — a bounded scan of the families tried, not a theorem for every channel). Whether another constrained action can carry the exact law is open — the lead track's named next construction check | L340 H2/H3/A1; lead-track recipe audit; hunt_2026 f23; G01 (strict μ_exp AQUAL fails Cassini 3.8–5.5×) |
| I5 Newtonian recovery | exponentially small kernel corrections | in Branch R2 GR returns through the heat filter S = exp((ξ²/2)∇²), floors 0.031/0.045 pc: a monotone phantom's tail alone is ephemeris-excluded by > 10⁴ | L340 S1; G02 |
| I3a mode count | N_grav = 2 exactly | Branch R2 has 2 tensors + 1 extra scalar (the khronon). Whether it qualifies as the spec's separately counted "genuine clock" needs the full canonical classification of the assembled action (open). Motivation: strict 2-DOF MOND with an external-field effect can signal (conditional theorem), and a moving source's phantom needs a momentum channel | `qwen_claude_field_theory/theory_2026/york/elliptic_channel_signaling_theorem_2026.py`; L330; L340; L333/KM1 |
| clock couplings | — | c₂ below the Planck-era Hořava cap 0.6–2.9×10⁻³ via the leaf-average λ-term −c₂(K−⟨K⟩_Σ)²; static β = γ = 1 derived in the reduced khronometric sector (other PPN terms and the filtered remainder documentary); c_T = 1 in the tested TT sector | L350; KM3; L351 W5 |
| I4 screening | a local dynamical quantity | still local, plus: the kernel must be blind to the large-scale web's Newtonian field (KiDS bounds an external field in the kernel at ~7×10⁻⁵ a₀) while the Sun keeps the Galaxy's field — the bound-region kernel (nonrelativistic, gate prescribed; relativistic embedding open) | BS2/BS3/L355; L361 |
| **I6 (new) the vacuum gate** | — | MOND acts in bound regions where u = x̃[Ω_Λ(z)/Ω_Λ,0]^p ≥ x_c0, x̃ = 9(R⁽³⁾+σ²)/(4K²) (shear-completed), Ω_Λ = 3Λc²/K² (for p = 1: x̃Ω_Λ = 27Λc²(R⁽³⁾+σ²)/(4K⁴)). A constant threshold is closed (KiDS ≲ 3.86 at z = 0.25 vs the forest ≳ 5.43 at z = 2). DE1: the flagship caps the exponent (p ≤ 1.97 at x_c0 = 2, canonical); the p = 2, x_c0 = 2 cell fails it at 10¹¹ M☉. DE2: a joint window exists (KiDS cap x_c,eff(0.25) ≤ 3.867, cosmic-shear floor x_c,eff(0.5) ≥ 3.50/2.93/2.49 at 600/650/700 km/s, flagship cap x_c,eff(2.5) ≤ 364.5, forest by dominance): p ∈ [0.5, 2.07], containing the **linear gate p = 1, x_c0 ∈ [2.005, 2.975]** — proposed R2 gate: p = 1, x_c0 = 2.5 (L359's own cell; passes all four; the PM gates of L380/L381 must be re-run there). **A prescribed mask, not yet varied in an action**: W(U)L_M adds L_M W′(U)δU to the clock and metric equations | L352/L358/L362; L359; L351; DE1; DE2; lead-track dark-energy audit §4 |
| **I7 (new) the dark mass** | — | required (CMB, clusters); no particle species added. Must be kernel-invisible (reciprocity ⇒ Newtonian force only), cold in the IGM at z = 2–3, out of galaxy halos by z ≈ 2.5, ~half retained in clusters (two-sided X-COP), ≳ 5× baryons in group cores (Harvey), and must not double the phantom's lensing (cosmic shear). Best realization so far: the virialization-triggered kicked carrier (v_k ≈ 600–675 km/s, pooled on fixed-cell clearing; Harvey cusp-kept only) — trigger posited, no action. The minimal field version (ghost-condensate dust) fails the tested shell-crossing setup; a linear wave field passes it (quanta: light bosons, m ≳ 2–5×10⁻¹⁹ eV); a wave field is extra field content unless derived from the clock. Its amplitude is initial data (homogeneous charge I) | two-sector door; L353; L357/L365–L381; L370–L372; L363/GP3/L364; GP5/L356; L374/L382/L383; lead-track homogeneous check |

## 3. Proof obligations to add to §5

G13 moving source (L330/L340) · G14 KiDS-1000 isolated lensing with Gauss-compensated, action-realizable profiles against
the realizable floor (L352, GP2) · G15 the Lyman-α forest observable, FGPA 1D flux power within 10% at z = 2–3, both boxes
(L347/L358/L362) · G16 cosmic shear, R ≤ 1.2 on k = 0.1–1 h/Mpc (GP3/L363) · G17 the flagship: deep-MOND Tully–Fisher
zero point within 0.10 dex at z = 2.5, M_b = 10¹⁰–10¹¹ (L356/GP5/DE1) · G18 X-COP two-sided (L366) · G19 Harvey+2015
merger offsets (L370–L372/L381) · G20 growth σ₈ within 2% (L341/L342) · G21 RC100 only in its calibration-conditional
wording (L331/L332). For G8, the first computations on the live candidate (`real_research/extra_crispy_2026/`, peer lanes): a
bounded pass at frozen-background, decoupling-limit scope, including the filter/foliation interaction — XC1
(strong-coupling momentum ≥ 8.5×10⁸ GeV over L340's window; α_c = 0 collapses it, so α_c > 0 is load-bearing) and XC3
(the filter's own foliation vertices enter only at O(π²) with two background powers; induced terms ≤ 3.5×10⁻⁷ of the
khronon's gradient term, in a cluster core); conditional at full-action scope (curved-background mixing, the assembled
action, loops). XC1
also reports the UV khronon superluminal on the metric cone (4.4×10²–7.9×10⁵ c): requirement 7 must be resolved
explicitly. **Proposed reading of requirement 7 (the user's call):** under the metric-cone criterion (A) every scalar MOND
realization on the record fails by construction — a propagating AQUAL scalar is superluminal along its gradient in the
whole MOND regime, and an elliptic/QUMOND field is instantaneous (L318 K3/K4) — so the spec as written is unsatisfiable
for any scalar MOND. The satisfiable reading is criterion B: no signal backward in a global time function compatible with
every characteristic cone (Bruneton 2007; Babichev, Mukhanov & Vikman 2008). C-H/K meets B at the linear,
frozen-coefficient level with the preferred foliation as that time (XC1 A9, XC2 B6). For G4/G5/G7, XC2 (f3b848273) scopes nonlinear
well-posedness, but the lead track's peer review (`real_research/peer_review_2026_09_26/`, uncommitted) finds its
all-kernel convexity step uses an unweighted heat contraction on a lapse-weighted norm (sound for genuinely monotone
kernels only), its zero-field modulus fails at a homogeneous U = 0 leaf, and mixed heat-operator variations escape the
per-leg suppression that XC1/XC3 rely on: G4/G7/G8 stay conditional. The same review finds both exact laws need
α_c > 0.06 (RAR) / 0.27 (exponential) in the reduced C-H/K block, against the candidate's ceiling 3.2×10⁻⁹, and that
L381's Harvey check mixes gate cells (p = 1, x_c0 = 1.5 merger gate; p = 2, x_c0 = 2 retentions).

## 4. Construction warnings to add to §2

P8 hand-truncated phantom profiles (Gauss: a switched divergence-form flux cancels the phantom beyond the edge, L352) ·
P9 force laws with no action for an extra species (reciprocity, L353 N2) · P10 switches built from R⁽³⁾ without the
shear completion (c_T, L351) · P11 clock couplings above the Planck-era cap (L350) · P12 the condensate's k⁴ term as a
caustic quencher (L374) · P13 a formal-order "negligible" not evaluated at the parameters another check fixes (PAPER33
v1 → v2) · P14 a clearing statistic on each run's own selected cells (L379, Lean I28) · P15 a gate scored against a
self-built benchmark never checked against published fits (GP2's withdrawn W4) · P16 pooling passes from different gate
cells or action revisions (lead-track audit).

## 5. §9 and §12.6

§9 is historical and says so; its "current best candidate" (the self-screened khronometric theory) died of a radial
gradient instability (FC-KH, 09-01) and should not be reused as a current label. §12.6's "Neither `lean` nor `lake` was
found" is out of date: Lean 4 + Mathlib (v4.34.0-rc2) are installed in `fable_independent_2026/lean_2026` with many
checked algebraic certificates; they certify algebra only.
