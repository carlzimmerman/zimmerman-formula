# X1_seedfree_abundance — assumption ledger (committed with FROZEN_CRITERIA.md, before any lane number)

Classes: FRAMEWORK-NATIVE (from the record's carrier action), DECLARED-INPUT (not fixed by the action; varied, never
fitted), APPROXIMATION (a controlled or tested truncation; its test is named), CONVENTION, INHERITED (a number or code
from Codex's `sol61_push/mechanism_reassessment_2026_10_22/`, copied with sha256), CLOSURE (an untested physical rule
used only to bracket), GAP (known missing piece, stated), ΛCDM-PROCESSED (a number produced by a ΛCDM analysis),
STANDARD-COSMOLOGY (textbook constants/tables), STANDARD-MOND-MACHINERY (none in this lane).

The record's verdict being rebuilt: Codex's high-H branch ends with `cold_relic_yield: null` (no surviving abundance
computed; Gaussian/Hartree insufficient; a late kinetic start re-assumes matching; a correlation evolution needed).

| id | item | class | where / test |
|---|---|---|---|
| A1 | V = m²\|Φ\|² + M²\|X\|² + g(X*Φ² + XΦ*²) + λ\|Φ\|⁴; m = 1 MeV, M = 2m√(1+0.02²), g = 2.168e-6 GeV, λ = 0.00881292; charges 1, 2 | FRAMEWORK-NATIVE | Codex benchmark (QUANTUM_CONVERSION_RESULT.md); unchanged |
| A2 | canonical complex fields, Φ = (f₁+if₂)/√2 | CONVENTION | Codex's convention |
| A3 | H_inf = 1.3445177278709404e10 GeV primary | DECLARED-INPUT | Codex `production_scalings.py`: chosen so a free X condensate gives about the target → circular at the primary point; map over 1e8–1e13 GeV |
| A4 | N_e = 60 e-folds of noise from zero coarse field | DECLARED-INPUT | Codex; X variance ∝ N_e (M ≪ H, no equilibrium) |
| A5 | reheating: instant radiation era (a = 1 + H_inf η), visible g* = 106.75; T_rh variants with a w = 0 era | DECLARED-INPUT | the action has no inflaton or reheating |
| A6 | dark sector couples to the visible sector only through gravity | FRAMEWORK-NATIVE | no portal term in A1; makes the dark/visible entropy ratio a conserved input |
| A7 | ξ = 0 primary, 1/6 control | DECLARED-INPUT | EMPTY_STATE_OBSTRUCTION.md: the flat-space action does not fix ξ |
| A8 | ξ enters only via the inflationary state and non-radiation eras (a″ = 0 in radiation) | derived | conformal mode equation |
| A9 | stochastic light-field (Starobinsky–Yokoyama) coarse field | APPROXIMATION / INHERITED | R0 reproduces Codex; λ\|Φ\|²/H² ≈ 0.01 |
| A10 | box zero mode = Langevin with noise stopped N_box e-folds early, then drift only | APPROXIMATION | avoids double counting the in-box modes |
| A11 | zero-mode velocity = slow-roll attractor of the same drift | APPROXIMATION | decaying mode ∝ a⁻³ dropped; Codex shows ḟ/H² enters F_max at ~0.3 % |
| A12 | in-box modes = de Sitter BD Hankel modes with constant-background masses 3λf₀², λf₀², 0, 0 | APPROXIMATION / INHERITED | Codex's NONLINEAR_FRAGMENTATION prescription; now for every lattice mode, with half-quanta |
| A13 | truncated Wigner (classical evolution of the sampled Wigner function) | APPROXIMATION | V0–V3 give the validity occupation n* |
| A14 | visible g*(T), g*s(T): smoothed step table (SM thresholds, QCD at 150 MeV, e± at 0.2 MeV) | STANDARD-COSMOLOGY | ≲ 20 % in Y; immaterial to order-of-magnitude bracket ends |
| A15 | normal ordering with respect to the massless conformal lattice vacuum (Weyl counterterm −4λc\|φ\|²) | CONVENTION | same structure as Codex's normal-ordered Fock Hamiltonian; V0/V3 test it |
| A16 | periodic box L = 78.54 (k_min = 0.08), lattice cutoff; modes below k_min live in the zero mode | APPROXIMATION | N = 32/48/64 prototype, 128/256 queued |
| A17 | isotropic, charge-symmetric quasi-particle Boltzmann with Hartree mass, 2↔2 contact \|M\|² = (4λ)² | APPROXIMATION | K10, K11 overlap with TW |
| A18 | X is a homogeneous coherent zero mode through E2 | APPROXIMATION | cubic force ∝ ĝa² ≈ 1e-14 a² of the quartic; diagnostic printed |
| A19 | E3 closures L (prompt), K (kinetic), C (free ceiling) | CLOSURE | the X–bath dissipation at hierarchy ~1e5 is not computed; G1 reports a bracket |
| A20 | E4: kinetic equilibrium, MB forward rates + detailed-balance inverses, BE thermodynamics, Hartree Φ mass | APPROXIMATION | K12 |
| A21 | C = 1.0181045670e14 GeV⁻⁸ (4→2 threshold), σv(XX̄→ΦΦ̄) = √(1−m²/M²)g⁴/(2πM⁶), D(T) MB table and D₀ = 1767.578 GeV⁻⁵ | INHERITED | Codex runs neutral_four_to_two_v2, highH_annihilation_gate, bath_assisted_conversion |
| A22 | crossed channel XΦ̄Φ̄ → ΦΦ̄ (RIS-subtracted kernel) | GAP | uncomputed; ×0 primary, ×1 of D sensitivity |
| A23 | target Ω_c h² = 0.12 (Planck) | ΛCDM-PROCESSED | used only as a comparison line, never a fit |
| A24 | ρ_crit/h² = 1.0537e-5 GeV cm⁻³, s₀ = 2891.2 cm⁻³ | STANDARD-COSMOLOGY | Ω_c h² = 2.744e5·Y·(m/MeV) |
| A25 | β_iso < 0.038 (uncorrelated CDI), P_R = 2.1e-9 | ΛCDM-PROCESSED | Planck 2018 inflation analysis (Codex cites it) |
| A26 | r < 0.036 → H_inf ≲ 4.7e13 GeV | ΛCDM-PROCESSED | sets the top of the H_inf grid |
| A27 | our patch = one stochastic draw; N_pre for the isocurvature lever = the patch's own coarse amplitude | APPROXIMATION | median and 10–90 % patches reported |
| A28 | "cold abundance" = W = n_Φ + 2n_X of the scalar carrier after freeze-out | FRAMEWORK-NATIVE / GAP | the scalar → identified-medium bridge is unspecified in the record (QUANTUM_CONVERSION_RESULT.md); not used |

Rebuild-brief changes (BRIEF.md "what changed"): AQUAL vs QUMOND, screening L★, the record's native H₀, SPS/h-conventions —
none enters a formation-epoch calculation (Ω_c h² uses ρ_crit/h², no H₀). The covariant cold sector (BS dust) takes the
abundance as an initial condition; this lane computes that initial condition. No STANDARD-MOND-MACHINERY is used.
