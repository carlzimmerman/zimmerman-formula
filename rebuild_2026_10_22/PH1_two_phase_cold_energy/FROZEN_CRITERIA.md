# PH1_two_phase_cold_energy — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, before any script or number)

κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), scored separately, never pooled. No
dark-matter particle: the cold sector is "cold energy", a classical field / medium (a classical field condensate is allowed by
the owner). Not "theory closed". Nothing here says the data favour the framework. Compute: one thread, `nice -n 15`,
< 1 GB RSS, minutes. No downloads. All other lanes read-only.

## 0. The question

O1 proved no local single-phase held-dust action in the v3s family lets a satellite keep cold mass (ε = 1). Hypothesis:
**two-phase cold energy** — a CONDENSED phase (held; it sources the law exactly as v3's khronon dust) where the medium is
dynamically cold, and a NORMAL phase (self-gravitating, dust-like, Ξ-neutral) where it is hot, with the phase set by a
DERIVED criterion. Verdict classes for the hypothesis as a whole:

- **VIABLE**: an action is written, the criterion is derived with no new constant, and every scored row below passes;
- **CONDITIONAL**: as VIABLE but one named row fails or one named non-derived ingredient remains;
- **NO-GO (owner rule)**: a new constant is unavoidable, or the criterion cannot assign every class its required phase
  from the allowed constants {κ, a₀, G, c, Λ, L★};
- **NO-GO (data)**: the best-allowed construction fails ≥ 2 scored rows.

## 1. Action family (T1; written and derived in `ph1_two_phase.py`, sympy)

One complex classical scalar ψ = √(ρ/m̂) e^{iθ} (m̂ a units placeholder; the eikonal limit is taken unless a row needs the
wave scale, in which case the wave scale is COUNTED as a constant). The coherent part ⟨ψ⟩ defines the khronon:
u_μ ∝ ∂_μθ (condensed phase = BS khronon dust, held, carrying v3s's J_x law sector and γ_L / switched stiffness unchanged).
The incoherent part δψ (⟨δψ⟩ = 0) is the normal phase: its coarse-grained stress is pressureless multi-stream dust
(Wigner / Vlasov limit), Ξ-neutral, minimally coupled. Derive with sympy:

- **D1 condensed static limit**: dust = AQUAL phantom of every non-held source, Ξ = Φ + C (U1 D2 reproduced, residual 0);
- **D2 normal static limit**: Jeans equilibrium in Φ, with Φ sourced by ρ_b + ρ_s + ρ_n; the law's phantom is sourced by
  ρ_b + ρ_n (normal sources the law like baryons; X6 C1b) — residual 0;
- **D3 composite weight (O1 W) with a normal share**: net force on a satellite = (M_b + M_n + M_s) g_host − M_s |∇Ξ_amb|,
  so ε_n = 0 for the normal share (residual 0);
- **D4 Landau criterion** from the condensed phase's linear dispersion: ω² = c_s²k² with c_s = L★√(2πGρ̄) (O1 §3's number)
  ⇒ v_c = c_s; a bound system moving at V_rel > v_c relative to the local khronon cannot keep superflow;
- **D5 Liouville / unfolding lemma**: a multi-stream (normal) state cannot evolve into a single-stream (condensed) state
  under the field's Hamiltonian flow (fine-grained sheet folds are not undone except on a measure-zero set).

Constant count (C-count): every continuous constant entering the criterion and the two phases, classed DERIVED (from
κ, a₀, G, c, Λ, L★), FITTED, IC (initial condition), or NEW. Any NEW ⇒ NO-GO (owner rule).

## 2. Criterion menu (T2) — each assigns a phase per class from the classes' state variables

Candidates (each with its constant count): **C-g** local acceleration |∇Φ| vs a₀; **C-ρ** density vs ρ_Λ (a₀ = κc√(Gρ_Λ));
**C-σ** dispersion vs σ_c with σ_c⁴ = G M a₀; **C-V** Landau: V_rel vs c_s(L★, ρ̄); **C-SX** shell crossing (single- vs
multi-stream); **C-λ** coherence λ = c/(μσ) vs system size (needs the wave scale μ: COUNTED).
Classes and REQUIRED phase: isolated discs CONDENSED (RAR); satellites NORMAL (or a bound normal share); cluster cores
partly NORMAL (×1.7); early linear universe NORMAL (dust growth); TDGs no cold energy; Solar System / globulars no phantom.
A criterion is **ADMISSIBLE** iff it assigns every class its required phase with no NEW constant. State variables are
taken from the record (numbers cited in the script with file pointers).

## 3. Scored rows (T4)

**G (growth, F3 ODE re-implemented).** Three components (baryons, normal s = 1, condensed held s = 0 — no self-force,
X6/U1), sub-horizon, radiation on, a_i = 1e-3, backgrounds A (C2 c2b refit: ω_b 0.022308, ω_c 0.120573, H₀ 67.578) and
B (CFG886: Ω_m 0.2976, h 0.68564, ω_b as A). Output δ_m(a=1)/δ_dust. **Line (F3's): ratio ≥ 0.95.** f_n,min = the smallest
normal fraction meeting the line (bisection; a requirement, not a fit). Branch EC (early condensed, f_n = 0) and branch EN
(early normal, f_n = f_n,min) both reported. Reproduction KG: F3's `growth_ratio` (imported read-only) at μ → ∞ equals my
f_n = 1 run to 1e-4, and my f_n = 0 ratio vs F3/X4's held-limit statement (< 0.05) checked.

**P4 (isolated RAR, double counting).** SPARC 175 galaxies; isolated spherical AQUAL law g = a₀ ν(g_N/a₀),
ν from μ = x/(1+x); per-galaxy Υ on [0.30, 1.20] step 0.01 by P4's weighted rms; P4's statistic and line:
**weighted rms ≤ 0.110 dex AND median Υ ∈ [0.50, 0.80], each footing.** EFE omitted (P4: < 0.001 dex; disclosed).
Reproduction KP: with no normal component, rms and median Υ equal P4's `iso_perUps` (0.054087 / 0.52 canonical; alt
from its JSON) to 1e-4 / exactly. Normal components (both enter g_N, i.e. they source the law like baryons):
- **EN**: isothermal ρ_n ∝ r⁻², M_n(<r) = v_n² r/G, v_n³ = 10 G H₀ M_n,tot, M_n,tot = f_n,min (ω_c/ω_b) M_b,gal with
  M_b,gal the galaxy's baryonic mass at its last point (present baryons: a LOWER bound on the cold supply), at h of
  backgrounds A and B. Scored: PASS iff the line holds both footings, both h.
- **EC**: merger-released normal debris, M_n(<r) = λ M_ph(<r), M_ph the galaxy's own isolated phantom of its baryons.
  Reported diagnostic: λ_max per footing (largest λ on the grid 0, 0.05, …, 2 keeping the line). Not a class.
- Diagnostic m_max: largest multiplier on the EN normal mass keeping the line.
**Double-counting number (headline):** Δrms and Δ median Υ of EN relative to the reproduction, each footing.

**Z2 (satellites).** Data: Z2's committed per-system file `z2_per_system.csv` (read-only), Z2's C2–C4 subset
(ell_flag False, grad_flag False, N_q ≥ 10; must give N = 19 per footing) and the MW+M31 systems; per-system central
Δ_ISO. Reproduction KZ: median Δ_ISO over C2–C4 within 0.05 dex of Z2's bootstrap +0.450 / +0.409.
Predictions:
- **EC freeze-out** (Landau release at Δv = v_c ≪ σ_sat, so the released medium is bound): the satellite's isolated
  phantom becomes normal at rest and irrotational (j = 0, derived: the held flow is curl-free and static). Lower bound:
  no collapse (prediction = ISO). **Primary: radial cold collapse** of the released phantom with the stars on circular
  shells (1D spherical shell code, Newtonian, phantom truncated at the Jacobi radius r_J = D (M(<r_J)/2M_eff)^{1/3},
  M_eff = x_e a₀ D²/G, present D_host; pericentre variant reported). Output boost B at the final stellar r₁₂;
  Δ_FO = Δ_ISO − log₁₀B.
- **EN normal subhalo**: Newtonian g = g_N,b + g_N,n(r₁₂), EN isothermal on the present stellar mass (Z2's Υ★ = 2
  convention), truncated at r_J; condensate share lost by O1's hover.
Statistic: median residual over C2–C4 (bootstrap over systems, 4000, seed 20261024) and its sd. **Classes:** CONSISTENT
iff |median| ≤ 2 sd; ABOVE (data above the prediction) / BELOW otherwise. EC row: **PASS** iff the primary is CONSISTENT
on both footings **and** the fixed-M_V host-field slope of the residual (OLS on [1, log x_e, M_V], bootstrap se) is within
2 se of 0 — the data's −0.05 ± 0.19 must be met by the prediction, not refitted; **FAIL** iff ABOVE on both footings.
Shell-code checks KS: energy conservation of a cold uniform-sphere collapse to < 1 % before shell crossing; B converged to
≤ 0.02 dex when N and the softening are both halved/doubled.

**F1 (cluster cores).** Not recomputed: the phase each branch assigns to cluster cold mass is mapped to X2's committed
readings (debris REPLACING the law: X2 V2 passes; debris ADDED to the law: fails) and F1/X2 tercile numbers (MID 1.12 /
1.88 / 1.89 canonical) are compared for sign. Verdict per branch from that mapping; labelled REUSED.

**U1 (TDGs, DF2/DF4), Solar System / globulars.** Reused: U1 B0 +0.055 ± 0.114 dex; O1 §3 VS numbers. Scored only as
"the criterion assigns them no condensate" (PASS) or not.

**O1 / CFG946 check (T3).** D3 must give ε_n = 0 exactly. CFG946's premises are listed and each is marked held / evaded
by the two-phase construction; the "particle in disguise" label is stated per the owner's field rule.

## 4. Checks and `--mutate`

Script `ph1_two_phase.py`: one line per check `K* PASS/FAIL`; exit 0 iff all pass (D1–D5 residuals, KG, KP, KZ, KS, RSS
< 1 GB). `--mutate`: the normal phase is given Ξ-charge (held like the condensate, α = 1) — D3 must then give ε = 1 and
KG's f_n = 1 run must fail the growth line, so D3 and KG FAIL (exit 1). Outputs `ph1_two_phase{,_MUTATE}.out`,
`ph1_two_phase_results{,_MUTATE}.json`.

## 5. Stop rule

No knob scans to make a row pass. f_n,min, λ_max and m_max are requirements / tolerances, reported as such. Fix-forward:
post-result changes go in a dated AMENDMENT, never by editing this file.
