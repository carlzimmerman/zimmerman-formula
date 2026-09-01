# FRIED CHICKEN — consolidated verdict, 2026-09-01

**Synthesis of three independent agent programs (Claude closure workflows 08-30/31; Codex sf54–sf62 +
one-shot 08-31/09-01; Qwen nonlocal/elliptic gates) against `FRIED_CHICKEN_SPEC.md`. Every script named
below was RE-RUN in the current checkout on 2026-09-01 and exits 0 (one_shot_final 10/10; sf61, sf62;
elliptic_phantom 7/7; nonlocal_door 5 test files + 2 gates). Nothing here is accepted from narrative.**

## Headline

**Outcome A (a fried-chicken theory): NOT achieved. No explicit action passes.**
**Outcome B (a no-go theorem): ACHIEVED for LOCAL actions** — a case-exhaustion theorem, each case
killed by a committed, re-run computation. The single un-excluded escape is a genuinely NONLOCAL,
field-dependent tensorial action that no one has written down (Codex's named residual), and it faces
two known obstructions of its own. **The existential target is therefore OPEN only through the
nonlocal door; every local route is closed.**

---

## THEOREM (fried-chicken local no-go)

**Assumptions.**
- **A1** One physical metric g; ordinary matter minimally coupled to g (spec reqs 5, 11).
- **A2** LOCAL action: finitely many derivatives; no □⁻¹, no form factors (this is the assumption the
  theorem cannot drop).
- **A3** N_grav = 2 (only the two tensor polarizations propagate) plus AT MOST ONE additional healthy
  clock/matter scalar T (spec req 2).
- **A4** Exact MOND μ(y)=1−e^{−y} quasistatic law sourced by baryons, with Φ=Ψ (1/r lensing) (reqs 1, 3).
- **A5** c_T = c to GW170817 precision (|c_T/c−1|<7e-16) along paths crossing galactic MOND zones (req 6).
- **A6** No instantaneous physical channel — well-posed causal Cauchy problem — and α₃≈0 (reqs 4, 7).
- **A7** Expanding FLRW, H≠0, not obtained by freezing the conformal mode (req 8).

**Statement.** No action satisfying A1–A3 realizes A4–A7 simultaneously.

**Proof — exhaustion over what carries the MOND force beyond the two tensor modes.**

| Case | Carrier | Why it dies | Committed evidence (re-run 09-01) |
|---|---|---|---|
| 1 | No extra field; MOND via algebraic/elliptic constraint on the metric scalars | **sf62 trilemma**: a 2nd no-slip constraint freezes the conformal momentum (kills H≠0, A7); a single constraint lacks GR's lapse-curvature relation (slip, A4). Independently **DC-019**: elliptic C_M ⇒ α₃=O(1) (A6). Independently **York/CMC**: the elliptic MOND Φ becomes a physical instantaneous observable via the EFE (A6). | `sf62_lapse_curvature_trilemma_proof.py`; `sf61_…`; `ppn_mmg_gate_2026`, DC-019; `theory_2026/york/YORK_CAUSAL_GATE_VERDICT.md`; Candidate A `elliptic_phantom_action_gate_2026.py` (3 DOF at k≠0 + FLRW zero-mode inconsistency + Ward conflict) |
| 2 | One frame-free propagating scalar φ, F(X) (the one scalar A3 allows) | Its anisotropic stress ∂ᵢφ∂ⱼφ (∝F_X, never zero when it carries a force) sources ∇²(Φ−Ψ)≠0 at O(1) in the MOND regime ⇒ **Φ≠Ψ** (A4). Fixing it needs a vector (Case 5) or a disformal coupling (A1). This is the Bekenstein–Sanders result that forced TeVeS's vector. **DC-013** slip-lock is the R-coupled version. | `closure_2026/` DC-013 scripts; DC-017 (DHOST subclass) |
| 3a | Clock scalar T (n∝∇T) coupled to n-projected curvature: R_nn, K_ijK^ij, K² | These enter the TT kinetic term: c_T² = 1/(1−2λ). Exact MOND forces λ_r = −a₀ y e^{−y} ≠ 0 ⇒ **λ ≈ −v_flat²/c² ≈ −2e-7** across every MOND zone ⇒ **A5 violated by 1e7–1e9× (c_T) / 1e5× (delay)**. Does NOT need exact luminality. Also: hidden c_s²=1/3 scalar (A3) and coasting-only ä=0 (A7). | `one_shot_final/curvature_qumond_luminality_no_go_2026.py` (6/6) + **`luminality_no_go_observational_strengthening_2026.py`** (11/11, this session; mutation control GR ⇒ no violation) + `…adm_dirac_gate` (hidden scalar) |
| 3b | Clock scalar coupled to its acceleration a_μ = D_μ ln N only (khronometric f(a)) | c_T=1 fine, but **radial khronon gradient instability** c²_∥ ∝ f''<0 on a₀<a<38a₀, growth 5e3–5e4 yr, β,λ-uncurable; **analytic no-go**: acceleration-only khronometric MOND + exact-GR-UV + radial stability ⇒ μ≡1. (A7-type stability, req 7) | `fc_kh_terminal/FC_KH_PAPER_vNEXT.md` + phase scripts; the (yq)' theorem |
| 3c | Clock scalar coupled to R^(3) or other spatial-curvature functions | Enters the TT gradient term ⇒ c_T≠c (A5), same fate as 3a; the Hořava-class UV terms are 4-derivative spatial and cannot carry a 2-derivative MOND force (Flanagan Eq 38). | FC-KH ADM reductions (β,λ backbone) |
| 3d | Clock T alone via its own gradient Y = h^{μν}∇T∇T | **Identically zero** — a clock is orthogonal to its own slices. Cannot carry a spatial MOND gradient. | trivial identity |
| 3e | Clock + DBI/k-essence clock dynamics + rotated-MMG constraints (sf60) | **sf61**: the DBI clock momentum is nonzero, so the advertised p_φ=0 primary is inconsistent; two scalar constraints freeze H (A7); the surviving single-constraint branch is 2+1 but then Φ=Ψ is not dynamical (Case 1). | `sf61_honest_canonical_adm_closure.py`, `sf60_…master.py` |
| 3f | Degenerate higher-derivative (DHOST/beyond-Horndeski) scalar | **DC-017**: under-lenses (MOND vacuum-exterior gate fails; 1/r³ slip) + pulsar bound; degeneracy fixes Ostrogradsky, not lensing. | DC-017 scripts |
| 4 | Clock T + a SECOND scalar χ carrying MOND (the "A/C hybrid") | χ is a scalar graviton ⇒ **A3** (N=2+2). If χ is made non-propagating ⇒ Case 1. | count |
| 5 | Preferred-frame VECTOR (AeST-class) | Extra gravitational DOF (A3); and **PPN KILLED**: α₁=−2(K_B+2)≈−4.2 un-tunable (4.4e4×), α₂ novel channel 1e4–1e5× (A6/req 4). | `V9_PPN_KILL_VERDICT.md`; 8b94872da, 0925e49f3, e95062743, 2fbbc873d |
| 6 | Second dynamical metric | N_grav = 7 (2+5) — **excluded by A3 outright**; Hassan–Rosen's own count. | `ONE_SHOT_FAILURE_LEDGER.md` (khronon-split bimetric host, 7=2+5) |

**Exhaustion.** Under A2, the local operator basis for {g, T, minimally-coupled matter} at ≤2 derivatives
(or degenerate higher) is: V(T), F(X) with X=(∇T)², and functions of the n-projected geometry
{R_nn, K_ijK^ij, K², R^(3), a_μa^μ, Y}, plus the DHOST degenerate class. Cases 1–3f cover every element; a
second field is Cases 4–6. Non-minimal matter coupling is excluded by A1. ∎

**Scope, stated honestly.** (i) Case 2's kill is the classic anisotropic-stress slip argument — solid at
the structural level but the sharpest committed form here is the R-coupled DC-013; a fully general
F(X) slip script is a worthwhile hardening. (ii) Case 3a's c_T argument is specific to couplings that
touch the TT kinetic/gradient coefficient; the strengthening shows the required λ is O(Φ_N/c²), so no
small-coupling escape exists. (iii) A2 is the load-bearing assumption. (iv) This is a theorem about the
FRIED-CHICKEN combination, not about MOND phenomenology or the a₀ reframing — see below.

---

## The one door left, named exactly (Codex's residual, unchanged by this synthesis)
Drop A2. A **field-DEPENDENT nonlocal spin-2 form factor** (the field-INDEPENDENT universal class is
already dead: "too linear in baryonic mass to produce exact MOND", `spin2_no_slip_linearity_gate`).
No such action exists in the repository or the literature we have. Two known obstructions it must
clear, neither yet proven fatal for the field-dependent case:
- **Localization adds DOF.** In-in/CTP localization of a causal nonlocal kernel introduces auxiliary
  fields (Leg-B trichotomy result; Codex `ctp_auxiliary_dirac_gate`: TT ghost-sign block; direct
  multiplier repair DEAD, `ctp_matching_multiplier_no_go`). If they propagate ⇒ A3; if elliptic ⇒ Case 1.
- **Conservation.** A retarded □⁻¹ imposed by hand is not Euler–Lagrange (□⁻¹_ret is not self-adjoint),
  so ∇_μT^{μν}=0 (req 5) is NOT automatic — Deffayet–Woodard's ∇^μE=0 is NOT-COMPUTED; their mimetic
  clock also ratio-locks a dark charge to ρ (dark field, not dark-field-free).

---

## What this does NOT touch
Layer A of the framework is untouched by every line above: a₀ = ½c√(Gρ_Λ) = c²√(Λ/32π) = 9.36×10⁻¹¹,
the a₀-coefficient phenomenology (RAR 0.108 dex, BTFR as a theorem of the a₀-line, weak-lensing RAR),
and the falsifiable a₀ ∝ H(z). Spec req 13 is honored as stated: **the a₀–Λ relation is external input
in every candidate examined; no derivation is claimed or faked.** What is closed is the *field-theory
embedding* of the reframing under the fried-chicken constraints with a local action.

## Reconciliation note (my session vs Codex ledger)
Codex's ledger records AeST as "α₁=−4K_B at the Maxwell locus." That is the BASE value (J_Y→∞). The
Claude workflow (8b94872da, 0925e49f3, two skeptic lenses) found the sharper physical result: the AeST
scalar drag renormalizes η_K=(K_B J_Y+2)/(J_Y+1), giving α₁=−2(K_B+2) at the deep field — which closes
the K_B<2.5e-5 escape that −4K_B alone would leave open. Both agree AeST is dead; the Claude number is
the one to quote.

## Reproduce
```bash
cd qwen_claude_field_theory/closure_2026
python3 one_shot_final/curvature_qumond_luminality_no_go_2026.py
python3 one_shot_final/luminality_no_go_observational_strengthening_2026.py
python3 sf62_lapse_curvature_trilemma_proof.py
python3 elliptic_phantom_action_gate_2026/elliptic_phantom_action_gate_2026.py
python3 nonlocal_door/spin2_no_slip_linearity_gate_2026.py
```
All exit 0. An exit status of zero certifies reproduction of the stated computation; it does not by
itself promote any result — see each script's own scope statement.
