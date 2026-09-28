# AS138.C01 — κ-closure attempt: total-stress conservation forcing Z/β² = 8 − 2b?

**Run:** `AS138.C01-20260928T1950Z-dsv4f-hermes`
**Task:** `deepseek_push/astra_spawn_ideas/branches/AS138/AS138.C01.md`
**task_sha256 (verified, computed at start):** `a1ebc02dbbfafc3459a5cc772881c097de582bddc4a33d9b11a77738a64d408c`
**Action pins (verified on disk):** `FINAL_ACTION.md` = `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`
(CA4-GNC / CA5-GNC-R); k04 four-form promotion = `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399`.
**Worker:** deepseek/deepseek-v4-flash-0731 (provider openrouter) via Hermes Agent focused subagent; identity taken from the executing system context.
**Started:** 2026-09-28T19:47:00Z · **Finished:** 2026-09-28T20:09:00Z
**Outcome:** **counterexample** to the closure hypothesis (conservation leaves a continuum);
the equivalence κ = 1/2 ⟺ Z/β² = 8 − 2b is reconfirmed exactly (60 dps), and the ratio is
fixed **by the framework input κ = 1/2 discharged through that equivalence**, not by
conservation. Publishable-incompleteness statement per the work order's refutation branch.

---

## 1. Framework cell, premises, conventions

**Mandatory framework inputs (adopted, not derived here):** a0 = κc√(Gρ_Λ), **κ = 1/2 adopted**
(AS651 proved that κ = 1/2 ⟺ Z/β² = 8−2b; whether the *adopted* κ is discharged onto the ratio
is exactly the present question). ρ_Λ = 4a0²/(Gc²); G = 6.67430e-11, c = 299792458 (SI);
G_N, G_bare, G_cosmo kept as separate constants (only G_N enters the footings). Both footings
kept distinct (they cannot share both fixed density and fixed κ): canonical a0 = 9.3619e-11 m/s²
(ρ_Λ = 5.844412454e-27 kg/m³, ε_Λ = 5.25269596e-10 J/m³, q_* = 1.145938e-05 at β = 1) and
alternative a0 = 1.1279e-10 m/s² (ρ_Λ = 8.48308962e-27 kg/m³, ε_Λ = 7.624220727e-10 J/m³,
q_* = 1.380600e-05); κ back-check = 0.5000000 exactly on both. Branches (Q, RAR, MU2, EXP, MONO):
none engaged — MONO enters only through the gate kernel's symbolic ν_mono as in the pinned action;
no branch translation; criterion B untouched. All results dimensionless ⇒ the theorems apply
identically to both footings (stated per footing where numerics appear). 1 thread everywhere;
CPU alarm `ulimit -t 120` (symbolic/numeric) and `ulimit -t 300` (Lean compile, a build step);
RSS measured (`/usr/bin/time -l`): symbolic 63.3 MB, numeric 19.3 MB, both ≪ 512 MB bound
(macOS RLIMIT_AS unavailable as in sibling runs — measured peak is the guarantee); Lean compile
2.95 GB RSS is the Mathlib build step, excluded from the research bound per house convention.

**The ten landed premises (used as premises; none re-derived here).** All hashes in
`result.json → input_sha256`:

| # | Premise (landed run) | Content used |
|---|---|---|
| 1 | AS137 (Tier-0) | ∇_μT_b^{μν} = E_b∇^νψ off shell, 0 on shell; S_b contains no a0/κ/G (vacuum-blind) |
| 2 | AS138 (Tier-0) | δ_ξS_heat = N[ΣE_Wk(ξ∂W_k)+ΣE_Lk(ξ∂L_k)+(R_W+L_b)ξ∂W_b+(λ0−L_0)ξ∂W_0+E_λ0ξ∂λ0+E_Uξ∂U]; endpoint multipliers load-bearing (omission leaves N·M ≠ 0) |
| 3 | AS147 (Tier-0) | div J_φ = +E_ex, div J_χ = −E_ex ⇒ div J_total = 0 on shell |
| 4 | AS651 (Tier-0) | ε_vac = (Z/2+bβ²)q² > 0, T_μν = −ε_vac g_μν; κ² = 2β²/(Z+2bβ²); κ=1/2 ⟺ Z/β² = 8−2b; flux EOM ⟹ ∂_μq = 0 (constancy) |
| 5 | AS652 | flux EOM spends its integration constant on environmental a0 (no ratio) |
| 6 | AS653 | homogeneity iff n = 2m (auxiliary) |
| 7 | AS658 | three-form has no propagating bulk modes (auxiliary) |
| 8 | AS669 | vacuum sector volume/amplitude-blind (auxiliary) |
| 9 | AS145 + AS132 | gate lapse source = C_N∫N√h φ[G(Y_h) − ℓΔ_hW_b]; compensator lapse source = −∫N√h φ Δ_NW_b — same Laplacian-of-W operator structure |
| 10 | AS133 + AS151 + AS156 | terminal BC L_b = −R_W, λ0 = L_0; 18 primaries static; spatial diffeo generator H_i exact |

## 2. Assembly of Q_total (work-order step 1)

On the shared compact closed C² leaf at the pin b8c04d4e…, with all fields on shell where the
premises allow, assemble the total current from the four Ward sectors plus the lapse-channel
sources (the spec's component list):

```text
Q_total = Q_b + Q_heat + Q_U1 + Q_vac + [gate/compensator lapse-source]

Q_b    = E_b (ξ∂ψ)                       # AS137 [2]: matter Ward contraction
Q_heat = N [ Σ_k E_Wk(ξ∂W)_k + Σ_k E_Lk(ξ∂L)_k + (R_W+L_b)(ξ∂W)_b
             + (λ0−L_0)(ξ∂W)_0 + E_λ0 ξ∂λ0 + E_U ξ∂U ]     # AS138 CHK-3 display
Q_U1   = div J_φ + div J_χ = E_ex + (−E_ex)               # AS147
Q_vac  = −(Z + 2bβ²) q (g^{μν}∂_μq)      # AS651: div T_vac, metric-proportional
gate   = C_N N√h [G(Y_h) − ℓΔ_hW_b]      # AS145 (5) — pin's eq-(13) lapse source
comp   = − N√h Δ_NW_b                    # AS132 S3 (reduced) — same W-operator family
```

On-shell substitution set (premises 1, 2, 4, 10): E_b = E_Wk = E_Lk = E_λ0 = E_U = 0;
λ0 = L_0, L_b = −R_W (AS133 terminal BC); ∂_μq = 0 (flux constancy, AS651 step 3).

## 3. Impose ∇·Q_total = 0; symbolic reduction (work-order steps 2–3)

The reduction is a pure polynomial computation with all couplings symbolic (Z, b, β, q, ℓ, θ, N, C_N)
and generic jet data (sympy, exact); on the compact closed leaf the integrated Ward is the
divergence-theorem integral ∫∇·Q_total = 0 (verified exactly on a rational 4-node periodic cell,
residual 0). Result (`raw_output_assemble.txt`):

- **[K1]** On-shell reduction of the assembled total Ward: **R_total = 0 exactly** — the total
  current closes *without any hypothesis on* (Z, b, β, q₀).
- **[K2]** The reduced closure condition is the **zero polynomial in r := Z/β²**:
  `Poly(0, r)`. Hence the solution set of ∇·Q_total = 0 in the ratio is **the full continuum
  r ∈ (0, ∞)** — every ratio conserves; the unique candidate r* = 8 − 2b is one point of it.
- **[K3]** The *only* (Z, b, β) relation in the whole landing is the AS651 framework identity
  κ² = 2/(r + 2b); κ = 1/2 ⟹ r* = 8 − 2b (exact symbolic solve, `8 - 2*b`).

**Why the reduction is an identity and cannot force the ratio (structure theorem).** Each
sector's Ward charge vanishes *by its own premised identity* once its field equation holds:
matter (P1), heat with the endpoint display + terminal BC (P2 + P10; the display closes the
r-IBP leftover term by term), U(1) (P3: div J_φ + div J_χ = E_ex + (−E_ex) = 0), vacuum
(P4: the three-form EOM fixes ∂q = 0, so the metric-proportional stress is divergence-free).
Diffeomorphism Ward identities are identities in the couplings — they constrain fields, never
ratios. The gate/compensator pair is not a Ward divergence but the pinned lapse equation's
source (FINAL_ACTION eq. (13) balances it against geometry + ρ_b + ρ_d), which likewise contains
no (Z, β, b)-relation. The household conclusion (Lean-certified below, theorem
`total_ward_closes`): **on-shell total-stress conservation is satisfied for every coupling cell
(Z, b, β, q₀)** — conservation does not select κ.

## 4. Negative controls (work-order step 4) — all capable of failing, residuals actual

- **[K4] NC-a: drop the vacuum term (no AS651) → continuum.** Without Q_vac the reduced
  condition is again the zero polynomial; moreover the couplings (Z, b, β) then do not appear in
  the system at all — a 3-continuum. **With the vacuum term the continuum also survives (K2).**
  The conditional that the work order keyed NC-a to ("vacuum present ⇒ unique") is thereby
  **refuted**: the vacuum term carries the ratio into the system only through the framework
  identity of K3, never through a conservation equation.
- **[K5] NC-b: drop the heat endpoint multipliers → N·M ≠ 0.** Omitting the display
  (R_W+L_b)(ξ∂W)_b + (λ0−L_0)(ξ∂W)_0 from the canonical (r-IBP'd) heat Ward leaves exactly
  N·M with M = L_b(ξ∂W)_b − L_0(ξ∂W)_0; on shell M = −R_W(ξ∂W)_b − λ0(ξ∂W)_0, and at the
  rational witness (R_W, (ξ∂W)_b, λ0, (ξ∂W)_0, N) = (7/20, 21/50, 3/20, −11/50, 10):
  **N·M = −57/50 ≠ 0**, while the display itself closes to 0 (exact). The multipliers are
  load-bearing exactly as AS138 CHK-2 reported (their 5.704e-2 witness is a different jet;
  ours is reproduced independently). The endpoint structure makes the heat Ward *close*; it
  adds no coupling equation.
- **[K6] NC-c: unique vs continuum judge → CONTINUUM.** The reduced closure condition is
  r-free (zero polynomial). Witness family (K_B = 0, b₀ = 0.01800539354…): r ∈ {1, 2, 4, 7.9639892129, 8, 16, 64}
  ↦ κ(r) ∈ {1.38941780248, 0.99111708019, 0.70394517849, **0.50000000000**, 0.49887844786,
  0.35315619419, 0.17672698293} — all distinct, **all satisfying on-shell conservation
  identically** (K1). In particular r = 8 (κ = 0.498878447859 ≠ 1/2) is a full counterexample
  member: conservation holds there, κ does not.

## 5. The b read-off and the exact tuned ratio (work-order step 5)

Pinned k04 flux coefficient: P(q) = (Z/2 + bβ²)q² with **b = (2 − K_B)·I/(16π)**,
I = jsat = 2(s_satΔ_sat − ∫₀^{s_sat}Δ ds), Δ(s) = s/(e^{√s} − 1) truncated at its peak
(mpmath, 60 dps — `raw_output_numeric.txt`):

```text
s_sat = 2.539638282188165325      Δ_sat = 0.64761023789191486
∫₀^{s_sat}Δ = 1.4184333037497265  jsat  = 0.4525248966751305416   (AS651 landed 0.45252490; Δ = 3.3e-9)
K_B = 0   : b  = 0.018005393544499054547       8 − 2b = 7.9639892129110018909
K_B = 1/4 : b  = 0.015754719351436672729       8 − 2b = 7.9684905612971266545
consistency b = (8 − (8−2b))/2: |b − b_check| < 2e-61 both K_B
```

The spec's 7.96398921 is reproduced to 2.9e-9. The value "(0.0180107905?)" guessed in the work
order is **not** the pinned coefficient: the pinned b (K_B = 0) is **0.0180053935445**, and
8 − 2·0.0180053935445 = 7.9639892129. (K_B = 1/4 gives r* = 7.9684905613.) Hence the reading
`b = (r* − 8)/(−2)` is consistent with the pinned flux coefficient to 61 digits (it is the
definitional inverse); the ratio and the coefficient stand together — neither forces the other.

**Exact chain that IS true** (the closest-to-closure statement, each step certified or landed):

```text
total Ward on shell  ⟹  ∇·Q_total ≡ 0 for all r          (this run, K1–K2; Lean total_ward_closes)
κ² = 2β²/(Z+2bβ²)                                        (AS651, Lean kappa2_q_independent)
κ = 1/2  ⟺  Z/β² = 8 − 2b = 7.9639892129…               (AS651, Lean kappa_half_iff_ratio; 60-dps here)
κ(8) = 0.49888… ≠ 1/2  ∧  ∇·Q_total|₈ ≡ 0               (this run: continuum witness, Lean kappa_eight_neq_half)
```

The step "total Ward ⟹ Z/β² = 8 − 2b" is **false**; the step that pins the ratio is
"κ = 1/2 (framework, adopted) ⟹ Z/β² = 8 − 2b (AS651 equivalence)". The closure attempt
therefore **discharges the framework input κ = 1/2 onto the four-form coupling ratio** instead
of deriving it.

## 6. Footing and branch discipline

All statements dimensionless; numerically re-anchored on both footings (canonical 9.3619e-11 and
alternative 1.1279e-10 m/s²; ρ_Λ = 5.844412454e-27 / 8.48308962e-27 kg/m³; q_* = a0/√G = 1.145938e-05
/ 1.380600e-05; κ back-check 0.5000000 on both). κ_eff at fixed canonical density (relabel
diagnostic) = 0.602388 — the two footings never share fixed density and fixed κ. G_N/G_bare/
G_cosmo kept separate; only G_N = 6.67430e-11 enters numerics. Branches Q/RAR/MU2/EXP/MONO:
not engaged (MONO appears only as the gate kernel symbol ν_mono of the pinned action).

## 7. Lean 4 certificate (hard bar met)

`AS138C01_total_ward.lean` (+ `AS138C01_axioms_probe.lean`), compiled on the compile host
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean` — **exit 0, zero sorry**.
Unfiltered `#print axioms` for all nine theorems: **exactly {propext, Classical.choice, Quot.sound}**
(`lean_axioms_output.txt`). Theorems: `heat_endpoint_bracket_zero` (AS133 bracket closes),
`u1_exchange_zero`, `vacuum_div_zero_on_shell` (dq = 0 closes the vacuum divergence),
`total_ward_closes` (the continuum theorem: on-shell total Ward = 0 with no coupling hypotheses),
`bracket_nonzero_witness` (NC-b: −57/50 ≠ 0), `kappa2_eight_lt_quarter` (1/(4+b) < 1/4),
`kappa_eight_neq_half` (κ(8) ≠ 1/2, via sqrt squaring with Real.mul_self_sqrt + transitivity),
`kappa2_at_tuned_ratio` (κ²(r*) = 1/4), `tuned_point_in_domain` (0 < r* < 8 for the pinned cell
0 < b < 4). House-traps encountered and resolved in this build: two **adjacent** doc comments
break the parser ("expected 'lemma'"; merge comments); numerals inside `norm_num`/`rw` are typed
ℕ by default (`(1/2)` becomes ℕ-division = 0!) — annotate `(1 : ℝ) / 2` explicitly; use
`Real.mul_self_sqrt` + `.trans` rather than `rw` on numeral products.

## 8. Bounds actually enforced

CPU: `ulimit -t 120` (soft RLIMIT_CPU, shell-enforced) on both research scripts; `ulimit -t 300`
on Lean compiles. Wall (measured): symbolic assembly 0.37 s, numeric k04 0.07 s, Lean 3.29 s
(compile ~= 3.3 s). RSS (measured `/usr/bin/time -l`): symbolic 63.3 MB, numeric 19.3 MB
(both ≪ 512 MB; macOS has no RLIMIT_AS — the measured peak is the guarantee, as in sibling runs);
Lean 2.95 GB (Mathlib load, build step, excluded per house convention). Threads: 1
(OMP/OPENBLAS/MKL/NUMEXPR = 1); pure-single-threaded mpmath/sympy computations.

## 9. What this does NOT establish / next step

- Does **not** show that any Ward identity of the pinned action class can force Z/β²: the
  counterexample family is a certified continuum of conservative configurations.
- Does **not** touch propagation/PPN/criterion B, the metric-sector Ward (AS138 §7's open gate),
  or the carrier/Z-source dynamics (FINAL_ACTION eq. (6): 4Δ_NZ = −S_N†R_W determines Z from heat
  data; its mean is a normalization).
- Next unresolved bridge: an equation of the pinned action linking the four-form coefficient Z
  to the Z-source dynamics or to ρ_Λ (e.g., the identification ⟨Z⟩_h ↔ (8−2b)β²), i.e., the
  *derivation* of κ = 1/2 itself. Until then κ = 1/2 is exactly as strong as the ratio — the
  framework input and the ratio stand and fall together (AS651 equivalence, exact).

**Verdict (per work order's refutation branch):** the closure hypothesis is **refuted as a
forcing statement** — total-stress conservation leaves a continuum of ratios; the numerical
ratio 7.9639892129 = 8 − 2·0.0180053935445 and the equivalence κ = 1/2 ⟺ Z/β² = 8 − 2b are
reconfirmed exactly; κ = 1/2 remains **adopted**. Publishable-incompleteness: *"total-stress
(Ward) conservation at pin b8c04d4e is realized identically for every coupling ratio; the ratio
Z/β² = 8 − 2b is fixed only by the adopted framework input κ = 1/2, discharged through the AS651
equivalence."*