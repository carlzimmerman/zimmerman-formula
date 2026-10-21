# WT-05 FROZEN CRITERIA: the arrow of time in the cold-energy dynamics

Committed alone, before any WT-05 script, sympy output or number. Folder `what_is_time/` (owner question 2026-10-21: "what is time,
based on the framework?"). κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², used separately and never
pooled. Z = 5.7888. Cold energy is real gravitating mass; no particle species is added. Framework-native inputs only. Nothing here can
say the theory is closed or that data favour the framework. Any change after this commit is a dated, labelled amendment appended below.

## 0. Question

Does the framework's own cold-energy dynamics contain an arrow of time, i.e. a functional that is monotone along every solution? Is
that functional a property of the medium alone, or only of the medium plus a reservoir (and is the reservoir the vacuum)? Is the
arrow's rate set locally (τ_ff, α) or by the vacuum time t_vac ≡ 1/√(Gρ_Λ)?

Record context (coordinator note from the WT-01 record map, received before this commit): on record the arrow is POSITED, not derived;
CFG938's ideal action has no settling drift, and the settling energy books do not close without a new reservoir (CFG932, CFG935,
CFG955). Those energy-book results are cited, not re-derived here. New pieces in this lane: the time-reversal parity of each settling
term, and whether a generalised second law (an H-functional with or without a named bath) holds for the committed relaxation and drift.

## 1. Inputs (read only; commit hashes)

| id | equation / input | file (commit) |
|---|---|---|
| E-OU | ∂ₜf + ∇ₓ·[(v + v_s)f] − ∇Φ·∇ᵥf = γ∇ᵥ·[(v − u)f + σ_J²∇ᵥf], γ = α/τ_ff, τ_ff = (4πGρ_m)^(−1/2), u = local mean velocity; v_s = −α 1_B 1_C τ_ff ∇ψ, ∇²ψ = 4πG(ρ_ph − ρ_c) (two-sided, FIX-1); ∇²Φ = 4πG(ρ_b + ρ_c) | CFG638 README + `cfg638.py` (28ce71974d); CFG541 EQUATIONS (a6c4c4e6f1); CFG550 VELOCITY_PART (ac69319c96); CFG554 v2 (f0e7065fff) |
| E-KT | ∂ₜf + v·∇f − ∇Φ·∂ᵥf = −(f − M[ρ, u, T_J])/τ inside a domain, τ = T1 = τ_ff/(2α); energy to a reservoir R, Q = (3/2)ρ(T_J − T)/τ | CFG955 FROZEN_CRITERIA (903cd8f1dc) §0, §3; AMENDMENT A1 (d11d477946) |
| E-Kρ | f_eq = ρ_eq M[u, T_J] (density target; mass not conserved) | CFG955 (903cd8f1dc) §0 |
| partner | the drift's energy goes to a coherent, zero-entropy dark-energy partner (GENERIC S = −F/Θ is formal) | CFG542 ACTION (92c45e9fcc) §1–2 |
| record Lyapunov | drift sub-flow: dF_ψ/dt ≤ 0 (CFG541 V3); dissipative sub-flow H-theorem S = −(F + F_v)/Θ (CFG550 §5); full-system Lyapunov NOT ESTABLISHED (CFG544 c2be5aa172, CFG550, CFG554, CFG558 415e3dc85c); E − TS rises under the drift on super-Jeans modes (CFG550 §5) | as listed |
| energy lanes | post hoc: drift → dynamical DE partner, bath → heat reservoir at σ_J²(x) (CFG935 1375588d0c); one-way cooling → gravothermal runaway (CFG935 R-c) | CFG935 README |
| systems | CFG847's five point masses (dwarf 1e7 M⊙ / 0.3 kpc, MW disc 6e10 / 10, MW outer 6e10 / 100, group 1e12 / 300, cluster 1.5e14 / 1000); simple law g = ½(g_N + √(g_N² + 4g_N a₀)) | `cfg847.py` (15c0894c1f) |
| NGC 3198 | record rotmod, Υ = 0.61, spherical-equivalent m_N = r²g_bar/G at the 43 radii | `real_research/data/sparc_data/NGC3198_rotmod.dat` (999f94dfee) |
| clock | CFG763's formation-clock window 0.72 / 0.83 – 3.47 Gyr (reported only) | CFG763 README (14e6a9c17d) |
| dS context | de Sitter entropy ceiling "forced but for constant Λ"; MUST NOT say the framework solves the arrow / Past Hypothesis | opus_48 review BEGINNING_OF_UNIVERSE (4a4cd211cd) |

T_J (= σ_J²) is the isotropic Jeans temperature of the phantom in the law field (CFG955 §0; CFG550's untruncated T_ph where no edge is
defined). α = 1 (record convention; causality bound α ≤ 1.186).

## 2. Readings evaluated

- **R1** E-OU with the drift OFF (the velocity relaxation alone; CFG638 / CFG554 FIX-2).
- **R2** E-KT (CFG955's primary reading; BGK to the local Maxwellian at T_J).
- **R3** E-OU in full (drift ON + velocity relaxation): the record's kinetic/fluid form (THEORY_CANONICAL 2026-10-18 row "Kinetic /
  fluid form", CFG638). **R3 is the headline reading.**
- **R4** E-Kρ: analytic note only (mass is not conserved; no mass reservoir is defined in the record) → NOT CLASSIFIED.
- The class-A engine (E6–E8 instant relocation) has no kinetic f: one-sentence note (a many-to-one map), NOT CLASSIFIED.

## 3. Part (a): what each reading conserves and what breaks time reversal

Tabulated from the inputs (mass, momentum, energy; relaxation target; where it acts). **T-parity (sympy, S4):** under T: t → −t,
v → −v, f(x, v, t) → f(x, −v, −t), each term of R1–R3 is classified T-even or T-odd. Expected (stated, not yet computed): Vlasov and
Poisson T-even; the relaxation (OU or BGK) and the drift v_s T-odd. The vacuum dependence of each T-odd term is listed: its rate, its
target (T_J, ρ_ph through a₀ = κc√(Gρ_Λ)) and its switch (domains / bound regions born at turnaround).

## 4. Candidate functionals

**Medium-alone (M):** no reservoir is booked.
- M1 Boltzmann entropy S[f] = −∫f ln f (≡ total entropy with a coherent partner, B-COH).
- M2 Casimir entropy S₂ = −∫f² (with the general statement for every concave C: the majorization order of Maxwellians, sympy S5).
- M3 relative entropy to the local target, D = ∫ f ln(f/M[ρ, u, T_J]) (non-increasing expected).
- M4 the drift functional F_ψ = (1/8πG)∫|∇ψ|² (CFG541 V3; non-increasing expected).
- M5 CFG550/554's GENERIC functional F_ψ + F_v, F_v = ∫T_J D_x(f ‖ M[ρ, u, T_J]) dx (non-increasing expected).

**Medium + reservoir (B):** S_tot = S[f] + S_R, with q_r(x), q_d(x) the energy delivered to matter by the relaxation and by the drift
(q_d = ρ_c v_s·∇Φ, the CFG638 energy-equation source; Φ total).
- B-TJ: local heat reservoirs at T_J(x) for both channels: Ṡ_R = −∫(q_r + q_d)/T_J.
- B-COH: coherent zero-entropy partner for both (CFG542): Ṡ_R = 0 (identical to M1).
- B-REC: the record's post-hoc pairing (CFG935): drift → coherent partner, relaxation → reservoir at T_J: Ṡ_R = −∫q_r/T_J.
- B-dS: the de Sitter horizon at T_dS = ħH_Λ/(2πk_B) for both channels, both directions, in the limit k_B T_dS/m → 0 relative to T_J
  (m the carrier mass; the ratio is reported in §8). Monotone iff the net energy into matter is never positive.
- B-SPLIT: releases (q < 0, per channel, per point) go to the horizon (T_dS → 0); draws (q > 0) are coherent work (Ṡ_R = 0). Monotone
  iff no finite interval exists with zero release everywhere during which S[f] falls. **Disclosed in advance: B-SPLIT is
  near-tautological** (any release into a ~0 K sink carries unbounded entropy); it is reported with that flag.
- F_T = K + W − T S[f] (free-energy form of B-TJ when T_J ≡ T is uniform): its boundedness below is reported (sympy S8: 1-D sheet
  bounded; 3-D sphere unbounded).

## 5. Analytic checks (sympy; each is a PASS/FAIL identity)

- S1 Liouville: Vlasov conserves ∫C(f) for every C and every Φ(x, t) (by-parts identity, 1-D).
- S2 BGK Clausius: with matched ρ, u, ∫(f − M) ln M = −(1/T_J)∫(f − M)v²/2, hence ṡ − q_r/T_J = (1/τ)∫(f − M)(ln f − ln M) ≥ 0.
- S3 OU Clausius: ṡ − q_r/T_J = (γ/T_J)∫|T_J∂ᵥf + (v − u)f|²/f ≥ 0 up to total v-derivatives (pointwise identity).
- S4 T-parity of each term (§3).
- S5 cooling counterexample: S per unit mass of a Maxwellian rises with T; −∫M_T^q (q > 1) rises with T; so relaxation from T > T_J
  lowers M1 and M2.
- S6 drift identity: Ṡ_drift − ∫q_d/T = −∫ρ_c v_s·∇(ln ρ_c + Φ/T) (uniform T); for ρ_c = (1 − ε)ρ_ph with ρ_ph isothermal at T it
  equals −ατ∫ρ_c|∇δΦ|²/T < 0; and the CFG550 super-Jeans mode sign ∝ (1 − k_J²/k²).
- S7 fluctuation–dissipation temperatures: the OU noise/mobility ratio is T_J; the drift has mobility and no noise (temperature 0).
- S8 F_T bounded below for a 1-D sheet, unbounded below (→ −∞) for a 3-D uniform sphere as R → 0.
- S9 rate elasticity e_Λ = ∂ln τ_ff/∂ln ρ_Λ at fixed baryons: deep-law SIS −1/8, Newtonian point mass −1/4, and |e_Λ| ≤ ¼ whenever the
  phantom's a₀-elasticity lies in [½, 1].

## 6. Toy (part d; code units G = 1; footing-free)

- **N-variant:** static Gaussian baryon slab Σ_b = 1, width 0.5. Target ("phantom stand-in", declared): ρ_ph = (Σ_ph/2H) sech²(x/H),
  Σ_ph = 5.364, H = 2, untruncated; T_J(x) = (1/ρ_ph)∫_{|x|}^∞ ρ_ph |g_t| dx′ with g_t the 1-D field of baryons + ρ_ph.
  **U-variant** (the deep-law isothermal region's analogue): no baryons, the same sech² target, T_J ≡ T = πGΣ_ph H exactly.
- Grid x ∈ [−32, 32], N_x = 512; v ∈ [−V, V], V = 7√(2 max T_J), N_v = 512. Planar self-gravity from cumulative mass.
- Vlasov: Strang splitting (half stream, kick, half stream); conservative, positivity-preserving flux-form semi-Lagrangian shifts with
  van Leer slopes. Relaxation: R2 exact BGK step f ← M + (f − M)e^{−dt/τ}, M with mass and momentum matched exactly; R1/R3 OU by an
  implicit Scharfetter–Gummel (Chang–Cooper) step (exact discrete Maxwellian equilibrium). Drift (R3): conservative MUSCL flux form,
  CFL ≤ 0.5 by substeps. Relaxation region |x| < 12; drift bound region |x| < 8; τ_ff from the actual local ρ_b + ρ_c.
- dt = 0.02 τ_ff0, τ_ff0 = (4πG ρ_m(0))^(−1/2) of the target state. Forward leg t₁ = 10 τ_ff0. **Reversed leg:** f(x, v) ← f(x, −v, t₁),
  evolved t₁ more with the same equations. NESS run (R2, IC-E) 80 τ_ff0.
- ICs (all at u = 0 unless stated): IC-H ρ_ph at T = 2T_J (cooling branch); IC-C ρ_ph at 0.25 T_J (heating); IC-E ρ_ph at T_J;
  IC-U ρ_ph at T_J with u = 0.5√T_J(0) sin(πx/2H) e^{−x²/8H²}; IC-D 0.7ρ_ph at T_J (deficit); IC-O 1.3ρ_ph at T_J (overfill).
- Runs: R2 {IC-H fwd+rev, IC-C, IC-U, IC-E NESS; U: IC-H fwd+rev}; R1 {IC-H fwd+rev, IC-C, IC-U}; R3 {IC-D fwd+rev, IC-O, IC-U, IC-H;
  U: IC-D}; controls (Vlasov only, same ICs and legs) for every IC used.
- **Numerical floor:** ε_num(IC) = max_t |S(t) − S(0)| in the paired Vlasov-only control (both legs), plus 1e-10 M.
- **Monotone PASS** (entropy-type): the largest drop max_{t<t′}[L(t) − L(t′)] ≤ ε_num in every run of the reading. **Verified violation:**
  a drop ≥ 10 ε_num + 1e-8 M in at least one run, with the matching analytic sign statement (S5/S6/record). Non-increasing candidates
  (M3–M5, F_T) mirror this with rises; for M3–M5 starting at L = 0 (IC-U) a verified rise is max L ≥ 1e-4 M (M3, M5 in KL units) or
  F_ψ ≥ 1e-4 |W(0)| (M4). B-dS: verified violation iff the cumulative net energy into matter over some interval exceeds 10× the
  control's max |E(t) − E(0)|. B-SPLIT: verified violation iff some interval of ≥ 5 steps has zero release (every q < −1e-12 E_scale
  per cell absent) and a drop of S ≥ 10 ε_num; the instantaneous search below is reported only.
- **B-SPLIT search (R3, reported):** 4000 random smooth states ρ_c = ρ_ph exp(Σ_{k≤6} a_k cos(kπx/16)) (and 1000 with odd terms) at
  T = T_J, a_k ~ N(0, 0.5²), plus Nelder–Mead from the 20 best: minimise Ṡ_drift subject to q_d ≥ 0 everywhere in |x| < 8.
- Reported, no class weight: the reversed-leg echo ‖f_rev(t₁)(x, −v) − f(0)‖₁/M (control vs relaxation runs); the NESS slope of S_tot.
- Compute: one process, OMP_NUM_THREADS=1, nice -n 10, in-script RSS guard 1 GB, 300 s wall cap per run, 45 min total; a capped run is
  labelled and graded on the time reached.

## 7. Verdict classes (per reading; R3 is the headline, R1/R2 stated beside it)

- **INTRINSIC ARROW:** some M-candidate has an analytic proof of monotonicity for all states of the reading and is Monotone PASS in every
  run of the reading.
- **BATH ARROW:** no M-candidate qualifies, every M-candidate has a verified violation, and some B-candidate has an analytic proof for
  all states and is Monotone PASS in every run. Qualifier **[finite-T bath]** if B-TJ or B-REC qualifies; **[T→0 sink only]** if only
  B-dS or B-SPLIT qualifies.
- **NO ARROW:** every M- and B-candidate has a verified violation in the reading's runs.
- **UNDERDETERMINED:** otherwise.
- **Bath identity:** VACUUM if every qualifying bath is a vacuum one (B-COH, B-dS, B-SPLIT); NOT VACUUM if only B-TJ qualifies; EITHER
  if B-TJ and a vacuum bath both qualify; B-REC is reported as "record pairing (mixed)". The record's coherent partner is SUFFICIENT
  iff B-COH (R1, R2) or B-REC (R3) qualifies.

## 8. Rate (part e), both footings, simple kernel (ν_mono reported)

Systems: CFG847's five (at their radii) and NGC 3198 (all 43 radii). Settled state ρ_c = ρ_ph; ρ_m = ρ_b + ρ_ph (point masses: ρ_b = 0).
- t_S = τ_π = τ_ff/(2α) (the e-folding time of a temperature deviation; σ e-folds at t_S/2), α = 1 (and 1.186 reported);
  t_D = 1/Γ = 1/[α(ρ_c/ρ_m)√(4πGρ_m)] (drift, CFG541); t_vac = 1/√(Gρ_Λ) ≡ κc/a₀ per footing (identity, flagged).
- e_Λ = ∂ln t_S/∂ln ρ_Λ at fixed baryons (a₀ ∝ ρ_Λ^½, central difference 1e-4); e_T = ∂ln T_J/∂ln ρ_Λ (destination, reported).
- **RATE LOCAL** iff for every system, radius and footing |e_Λ| ≤ 0.30 and t_S/t_vac ≤ 0.1. **RATE VACUUM-SET** iff every
  |e_Λ + ½| ≤ 0.1. **MIXED** otherwise. **Disclosed:** RATE LOCAL is expected by construction (CFG541 D1 builds τ from {G, ρ_m};
  S9 bounds |e_Λ| ≤ ¼); the test measures how much of ρ_m is phantom. The same rule is applied to t_D.
- Reported: CFG763's 0.72 / 0.83 – 3.47 Gyr against t_vac; k_B T_dS/m against T_J and the carrier mass m* below which the horizon is
  not effectively at zero temperature.

## 9. Controls (any K failure ⇒ classes VOID, reported)

| id | target | line |
|---|---|---|
| K1 | plain homogeneous BGK and OU without gravity (closed: target = own T; thermostat: fixed T) from a bimodal f | S (closed) and S_tot (thermostat) never drop by more than 1e-12 M per step (OU 1e-10 M); final KL ≤ 1e-6 |
| K2 | CFG638 K7 in an SIS: τ_ff = r/V, τ_π = r/(2αV), Kn = √2/(4α), Re = 4α | sympy exact |
| K3 | isothermal sphere in a box: canonical critical density contrast 32.1, microcanonical 709 (Emden equation) | each within 1% |
| K4 | Vlasov-only controls: mass, energy, entropy | mass ≤ 1e-12 relative (box-edge mass ≤ 1e-10); \|ΔE\|/\|E₀\| ≤ 5e-3; \|ΔS\|/M ≤ 0.02 |
| K5 | discrete BGK Clausius per relaxation step in every R2 run | ΔS − Σq_r dt/T_J ≥ −1e-11 M |
| K6 | CFG847's v_c: dwarf 21 km/s, cluster 1314 km/s (canonical) | within 1 km/s |

## 10. MUTATE (`WT05_MUTATE=1`, separate outputs `*_MUTATE`; exit 1 iff every tooth bites, 2 otherwise)

| tooth | change | bites if |
|---|---|---|
| Mu1 | anti-relaxation BGK, f ← M + (f − M)e^{+dt/τ}, R2 IC-H, 2 τ_ff0 (stop if negative mass > 1e-3 M) | B-TJ verified drop |
| Mu2 | fluctuation–dissipation mismatch: OU diffusion at 2T_J, bath booked at T_J, R1 IC-E | B-TJ verified drop |
| Mu3 | drift sign flipped (v_s → −v_s), R3 IC-D | F_ψ(τ_ff0)/F_ψ(0) > 1 while the unmutated R3 IC-D run has < 1 |

## 11. Discussion items (no class weight)

- Self-gravity: what an unbounded F_T (3-D) does to any H-theorem (an arrow with no floor), and whether CFG955's reported central collapse
  (A1: present under K-T, absent with relaxation off) is consistent with K3's canonical (thermostatted) vs microcanonical thresholds.
  Discussion only; CFG955's scripts and outputs are not run, edited, staged or copied.
- What the result means for CFG958's frozen T-S items (S5: "the drift's work to a coherent partner is admissible").

## 12. Design-stage disclosures (not blind)

Read before freezing: CFG638 README and script; CFG955 FROZEN_CRITERIA and AMENDMENT A1 only (its DERIVATION, scripts and outputs not
read); CFG955's result commit message (1150546489) was visible in the git log, including its post hoc PH4 statement (thermostatted SIS
Bonnor–Ebert instability) and L7 (coherent partner cannot take the cooling branch); CFG541 EQUATIONS §0–4; CFG542 ACTION §1–2; CFG544
README (K3); CFG550 VELOCITY_PART; CFG554 v2 §4; CFG558 v3 §4; CFG935 README (grep of reservoir lines); CFG847 README and script
lines; CFG763 README head; THEORY_CANONICAL 2026-10-18 notes; the opus_48 dS review; CFG958's frozen criteria T-S lines (8d7764d743),
seen after it landed during this lane's design.

Expectations formed (hand reasoning, no script run):
1. Vlasov–Poisson T-even; relaxation and drift T-odd.
2. M1–M5 all violated (cooling branch; Vlasov from a local-equilibrium start); no INTRINSIC ARROW in any reading.
3. R1, R2: B-TJ and B-SPLIT qualify (Clausius theorem, self-gravity included because Vlasov conserves S and E); B-COH and B-dS fail.
   Expected BATH ARROW [finite-T bath], bath identity EITHER, record's coherent partner NOT sufficient.
4. R3: B-TJ fails (S6 deficit state; CFG550's super-Jeans sign), B-REC and B-COH fail (deficit filling compresses phase space), B-dS
   fails on draws; B-SPLIT probably survives. Expected BATH ARROW [T→0 sink only], bath identity VACUUM (near-tautological).
5. Rate LOCAL (by construction); destination T_J vacuum-dependent (e_T up to ¼ in the deep regime).
6. CFG955's collapse is consistent with a thermostat turning the problem canonical.
