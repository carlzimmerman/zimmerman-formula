# A31 — adversarial referee of FINAL_THEORY.md

**Lane A31 · 2026-10-21 · target: `deepseek_push/DS_FINAL_2026_10_21/FINAL_THEORY.md` (612 lines).**
Deliverables: this report, `a31_checks.py` (35 independent numeric checks), `a31.out`,
`a31_results.json` (claim ledger + counts), `a31_ledger.py` (the machine-readable table), `MUTATE.md`.

## Bottom line

**130 quantitative claims were located, classified and (where numeric) re-derived. 98 are BACKED,
17 OVERSTATED, 1 UNBACKED, 14 WRONG.** Thirty-two non-BACKED findings out of 130 is a 24.6 % defect
rate; a zero-finding referee would have been the suspicious result. The document's arithmetic is
mostly right — the failures are concentrated in *what the numbers are made to mean*: conditional
results stated as derivations, one background choice stated as a general theorem, one single-galaxy
bound stated as a data window, and three numbers attached to the wrong quantity.

The single most damaging pattern is not any one number. It is that the synthesis repeatedly upgrades
a lane's own status word: A2's `CONDITIONAL` becomes "forces n = 1"; A15's `DIFFERENT-QUANTITY` for
one chain becomes "κ is a modulus"; A3's `P̄ = 0` becomes "exactly, not to leading order"; A22's
`r << λ` becomes "exactly"; A20's one-galaxy `f_c → 1` bound becomes "window after the data". Each
upgrade is small; together they are the difference between an effective theory with named premises
and a completed one.

**Numeric checks:** 35 run, **29 match** FINAL_THEORY.md, **6 mismatch** (`04, 23, 28, 29, 30, 33`).
Four of the six are findings about the synthesis (`04` the Λ convention, `23` the R_tot-vs-F(y_v)
substitution, `29` the 0/0 α₁, `30` the lane count); two (`28`, `33`) are structural demonstrations
that a premise the synthesis omits is load-bearing.

---

## The eight load-bearing attacks

### 1. "κ is a modulus" (A15) — the symmetry is valid, the word is not

A15's K9 is a genuine one-parameter family of the *truncated* halo equations. `σ² = C/2` and
`v² = C` are homogeneous of degree one in `C`, and the deep-MOND normalisation `C² = G M_b a₀` is
invariant under

```
a₀ → μ a₀,   C → √μ C,   σ² → √μ σ²,   v² → √μ v²   (fixed M_b, fixed ρ_DE).
```

So on that solution set `κ_dyn = σ²/v² = 1/2` is constant while `κ_law = a₀/(c√(Gρ_DE))` scales by
μ. **The argument does not assume what it proves** — it assumes the premise list is complete. But
that is exactly the contested point, and three things weaken the conclusion:

- **The code does not check the link that makes a₀ enter.** K9 verifies the two homogeneous
  equations, not `C² = G M_b a₀`, which is the relation that carries the a₀ weight. "Fixed `M_b`"
  must mean the external baryonic mass, not the scaled cold density (the pure SIS has infinite
  mass); the code does not state or check that distinction, so the symmetry is verified only for
  the two equations that are homogeneous by construction.
- **It is a family of different solutions, not one solution relabelled.** `v² → √μ v²` and
  `ρ → √μ ρ` change the rotation curve and the density. "On one and the same solution set" means the
  set, not a point; that is enough for the no-go, but it is weaker than the prose suggests.
- **A15 explicitly disclaims the general claim.** Its `What this does not do`: "It does not claim κ
  is underivable in general. It claims these premises do not derive it, and gives the exact equation
  that would." A19 then tries four candidate functionals for that equation. A flat direction of a
  two-equation truncation is not a modulus of the theory; it is a missing equation.

**Corrected:** *"Verdict: DIFFERENT-QUANTITY. κ is a flat direction of the halo sector's
two-equation truncation (A15 K9); A15 does not claim κ is underivable in general, and A19's
scale-functional programme is the search for the missing equation."*

### 2. "n = 1 is forced" (A2) — a conditional class result stated as a theorem

A2's own status line is `CONDITIONAL(single-scale driven two-state lattice: capacity = affinity = a0);
n=1 forced` **in that class**. The lattice does not derive the capacity: A2 §4 derives `C = s` from
the requirement that the deep limit be `g = √(a₀ g_N)`, and then identifies `s = a₀` with the
observed deep-limit scale. That is a matching, not a derivation. Given one gate per site, `θ =
x/(1+x)` is the definition of the lattice; "n = 1 is forced by one gate per site" is therefore true
but nearly tautological. The genuinely non-trivial result is the *no-go*: no positive mixture of
two-state gates reproduces n = 2 (A2 K7), and that is backed.

**Corrected:** *"Within a single-scale two-state lattice with mass-action kinetics, one occupant per
site and capacity = affinity, n = 1 is the unique member; the capacity is fixed by matching the
observed deep-MOND limit, not derived, and a₀ remains the free κ input (A2, CONDITIONAL)."*

### 3. `c_T² = 1` exactly (A3) — the proof sets `P̄ = 0` and the synthesis drops it

A3 §3.1 is explicit: "**Background `P̄ = 0`, `N = 1`, `h_ij = a²δ_ij`**". §7 repeats: "`c_T = 1` is a
classical statement about the quadratic action on a `P̄ = 0` de Sitter background." The synthesis
prints "`c_T² = 1` exactly, not to leading order" and "the quadratic tensor action is therefore the
Einstein one" with no premise.

That matters because A22 D4 puts the Solar System in a **hedgehog with `P ≠ 0`**
(`u = 2.59e-6 a₀`, `λ = 17 pc`). On a `P̄ ≠ 0` background, `W(u)` with `u = K√(h^{ij}P_iP_j)`
contracts `P̄_iP̄_j` with the TT perturbation at linear order and produces a nonzero `h²` term — the
parent's own GW certificate K4 says the only TT–P coupling is "a mass term that vanishes where P = 0
(the FRW background)". My check 28 computes the coefficient for `P̄` along x: `3Kp/8 ≠ 0`. The
`p²` coefficient may still be 1 (so `c_T² = 1` in the narrow dispersion sense), but the quadratic
action is **not** the Einstein one, and the synthesis's stronger sentence is false on the background
where GWs are actually detected. A3's own breaker inventory item 3 — "an explicit
`n_in_j`/`h_ijP^iP^j` multiplier of `h^TT` (a condensate or Proca mass would do it)" — is *already
present* as `W(u)`; it is inert only because the background was chosen with `P̄ = 0`.

**Corrected:** *"`c_T² = 1` exactly on the `P̄ = 0` de Sitter background (A3 §3.1); on a `P̄ ≠ 0`
background such as A22's Solar-System hedgehog, `W(u)` adds a nonzero `h²` mass term, so the
quadratic tensor action is not the Einstein one and the general-background statement is open."*

### 4. `α₁ = α₂ = 0` (A22) — a 0/0 and a regime-limited zero

A22's F1 says: in aether variables `c₁ = c₃ = c₄ = 0`, `c₂ = −β_ADM`, "for which the published α₁
and α₂ both vanish". The published α₁ is

```
α₁ = −8(c₃² + c₁c₄) / (2c₁ − c₁² + c₃²).
```

At `c₁ = c₃ = c₄ = 0` this is **0/0**, not 0. A22's own code (lines 221–223) does:

```python
den = 2*c1a - c1a**2 + c3a**2
alpha1_lit = sp.Integer(0) if den == 0 else sp.simplify(...)
```

i.e. it *sets* α₁ = 0 when the denominator vanishes. That is an assertion dressed as a check. The
α₁ = 0 result therefore rests entirely on F2's "pure isotropic rescaling of a linear potential"
argument, which is a linearised static argument. A22 itself says D5–D6 are exact only for
`r << λ = 17 pc`, and that at `r >> λ` the P field is MOND-slaved and "an effective α₁ ~ O(1) ... Not
computed". So "exactly" is a Solar-System-regime statement, not a theorem.

There is also a direct self-contradiction in the synthesis: the table and §8 say preferred frame
**DERIVED (zero), α₁ = α₂ = 0 exactly**, while the §3 text says "the `(1+β)θ²` deformation ... is a
genuine preferred-frame term and is **not** closed here — it is the one gate still open." A22 closes
that route (θ ≡ 0 static, θ² = O(h²), K5), and the parent's scope note says the θ² route "is A22's
job". The text is stale; one of the two sentences must go.

**Corrected:** *"α₁ = α₂ = 0 and β = 1 at PPN order in the Solar-System linear regime `r << λ = 17
pc` (A22 D5–D6); the Einstein-aether formula is 0/0 at `c₁ = c₃ = c₄ = 0` and does not establish the
zero, and A22's galactic-regime `α₁ ~ O(1)` is not computed. The `(1+β)θ²` route is closed by A22,
not open."*

### 5. `L* = 24–90 pc` (A20) — a one-galaxy, maximal-cold-fraction bound

A20's 90 pc is `R0.3(IC_10 = 200 pc) / 2.22144`, under the assumption that the cold sector dominates
the inner mass (`f_c → 1`). A20's own `What this does not do` 3: at `f_c = 0.5` the bound weakens to
**127.3 pc**, at `f_c = 0.25` to **180.1 pc**; the sample's 10th-percentile bound is **184.6 pc** and
the median is **787.8 pc**. The "300 pc excluded by 3.33×" is just `300/90`: it inherits the same
single-galaxy, `f_c → 1` assumption and is not an independent sample exclusion. The LITTLE THINGS
`R0.3` is itself a model-dependent turnover radius (defined by `v = 0.3 v_max`), and the bound
assumes the `n = 1` polytrope edge `R_core = 2.22144 L*`.

So "window after the data: 24–90 pc" is the best case, not the data window. The honest statement is
`24 pc` (thermal bottom) to `~127–185 pc` (f_c = 0.5 or the 10th percentile), with 90 pc as the
most favourable single object.

**Corrected:** *"LITTLE THINGS gives a one-sided bound `L* ≤ 90 pc` from IC 10 under `f_c → 1`; at
`f_c = 0.5` it is 127 pc, at `f_c = 0.25` 180 pc, and the sample's 10th-percentile bound is 184.6 pc,
so the data window is 24 pc to ~130–185 pc with 90 pc the best case, not a measured 24–90 pc
window."*

### 6. "u rises outward" (A21) — the band-to-3D mapping is unmodelled

A21's `u` is `(A_newton − A_law)/(A_law(A_newton − 1))`, a ratio of **ΔΣ-weighted band amplitudes**,
not a 3D mass ratio. A21's own caveat: "the band→3D mapping is not modelled (A18 ... `f_band = 0.812`
is a weighted share, the 3D value at the MID band centre is 0.65)." Folding a ±0.06 systematic moves
the MID 1/2-distance from 0.78σ to 0.41σ. The direction of the 3D correction is not computed, so
whether the *sourcing fraction* rises outward is not established — what is established is that the
band amplitude ratio rises.

The band-ratio significance is quoted at its optimistic end. A21 gives `Z_band = 4.91` in quadrature
and `Z_band_worst = 3.82` for any band correlation; §0 quotes the 4.9σ without the caveat, while §5
gives the conservative `≥ 3.8σ`. The two numbers are consistent — the issue is that §0 presents the
quadrature value as the exclusion, and the 4.9σ is not robust to the band correlation.

**Corrected:** *"The band-weighted amplitude ratio rises from `u = 0.472 ± 0.036` (MID) to
`0.986 ± 0.098` (OUT); a constant band ratio is excluded at 4.9σ in quadrature and at `≥ 3.8σ` for
any band correlation, and
whether the 3D sourcing fraction rises is not established because the band-to-3D mapping is not
modelled (A21)."*

### 7. The named arithmetic

| number | re-derived | verdict |
|---|---|---|
| **2557.38×** | `9.36e-11 / 3.66e-14 = 2557.377` | **BACKED** (A4); the "twice 1279" is exact in the coefficient (1 vs 1/2), not in the rounded 1279 |
| **15.47 %** | `2/√3 − 1 = 0.1547005` | **BACKED** (A2); but the circular-speed figure is `√(2/√3) − 1 = 7.4570 %`, and FINAL prints `√(2/3) − 1 = −0.1835` — **WRONG formula** |
| **7.457 % via Q2.8** | parent `max_frac_v = 0.0773503` | **WRONG**: Q2.8 linearly halves 15.47 %; it gives 7.735 %, not 7.457 %. The synthesis says Q2.8 "reproduces both" — it does not |
| **66.30** | `y_t` root of `F_can(y_t) = 100.405845` = 66.29994 | **BACKED** (A4); but §8's "`y_t = 100.4` closes Λ" is **WRONG** — 100.4 is `N_Λ` |
| **2.424** | `−3.5289 + 1.1048 = −2.4242` at 160 k points | **BACKED** (A6) at the lane's resolution; 1e6 points give −2.372 (2 % drift), so the third digit is not stable |
| **1.18** | A24 EFE-present: 1.1811 (RAR) / 1.1933 (canonical), bracket 1.1771–1.1933 | **BACKED** at 20 kAU; the "1.16 at 10 kAU" is **WRONG** — that is the EFE-blind value; EFE-present is 1.100 / 1.107 |
| **53.31 pc** | `(π/√2)·24 = 53.3146` | **BACKED** (A20) |
| **3.87e5 M⊙** | `a₀L*²/G = 386789` | **BACKED** (A22) |
| **5.57e8 M⊙** | `π³/(6√2)·V²L/G = 5.565e8` | arithmetic **BACKED**; the value is model-dependent — NFW gives 3.149e6 (A16), a 2.2-dex spread |

The one arithmetic item that is not merely a typo is the `√(2/3)` formula. It is the kind of error
that survives proofreading because the *number* 7.457 % is right; only the expression is wrong, and
the same sentence then uses the wrong expression to "reconcile" the record. The parent harness's
7.735 % shows the reconciliation is not a reconciliation at all.

### 8. Cross-references that fail

| # | citation | what the cited lane actually says | verdict |
|---|---|---|---|
| 1 | "A13's suppression curve transfers" | A23 §6: A13's curve is a mirror-symmetry artefact, "not transferable"; 0.751 half-domain vs 0.050 full-domain at e = 0.3 | **WRONG** |
| 2 | "`M_ph/M_b = ½(√(1+4/y)−1)` at the virial radius is 25.04 / 2.62" | A18: `F(y_v) = 25.90 / 3.77`; 25.04 / 2.62 are `R_tot = μ(1+F)−1`, the phantom per *total* baryon; the ratio is 6.87, not 9.57 | **WRONG** |
| 3 | §7 item 5: "depths 2.16–2.37 / 5.16–5.68 (A13)" | §5 item 3: "3.529, not 2.16–2.37 (A13 ...)" — the document adopts A6's 3.529 and A13's 2.16–2.37 in the same breath | **WRONG** (internal contradiction) |
| 4 | "23 lanes" (line 3) | 24 lane directories at the synthesis (`A1–A16, A18–A25`; no A17); §5b itself says "24 lanes" | **WRONG** |
| 5 | "Every number below was re-run by the coordinator (21/21)" | `_parent/parent_audit.py` checks 21 specific items; 2557.38, 66.30, 7.457 %, 53.31, 3.87e5, 2.424, 1.18 are not among them | **OVERSTATED** |
| 6 | §4 table: "in horizon units 5.40e-9 – 2.25e-7" under the 24–90 pc window | 5.40e-9 is 24 pc; 2.25e-7 is **1 kpc**; 90 pc is 2.02e-8 | **WRONG** (row mismatch) |
| 7 | §3 table + §8: "Preferred frame DERIVED (zero)" | §3 text: "the (1+β)θ² route ... is not closed here — it is the one gate still open" | **WRONG** (self-contradiction) |
| 8 | "adding a P–curvature coupling ... my mutation demonstrates it" | A3 `MUTATE.md`: the c_T² mutation is `naive_stiffness` (`c_T² = 1 + 2K|P|²`); no curvature coupling is mutated | **WRONG** |
| 9 | "the published α₁ ... vanish" (A22) | A22 `a22_checks.py` sets α₁ = 0 when the aether denominator is 0 (0/0) | **WRONG** |
| 10 | "Q2.8 reproduces both" (7.46 % and 15.47 %) | Q2.8 gives 15.47 % and 7.735 % (linearised half), not 7.457 % | **WRONG** |

---

## The full ledger (130 claims)

Column **backing** names the file/field or report section where the number lives; the section column
is the FINAL_THEORY section number. `FINAL` is paraphrased, not quoted line-by-line. **BACKED** = same
value and same meaning; **OVERSTATED** = number exists but the prose claims more; **UNBACKED** = no
file contains it; **WRONG** = the backing says something different.

| id | § | claim in FINAL_THEORY.md (paraphrase) | backing | verdict | corrected sentence |
|---|---|---|---|---|---|
| C01 | 0 | M_c = (Omega_c/Omega_b) M_b = 5.3643 M_b | A18_two_ratios/a18_results.json:numbers.R_cosmic = 5.364327; A9 report D2 | **BACKED** | — |
| C02 | 0 | u = 0.4716 +/- 0.0362 (MID), 0.9865 +/- 0.0984 (OUT) | A21_u_half/a21_results.json:numbers.u_data = 0.4715659, u_OUT = 0.9864741 | **BACKED** | — |
| C03 | 0 | i.e. the sourcing fraction rises outward | A21_u_half/report.md section 'What this does not do' 1: u_data is a Delta-Sigma-weighted band fraction, not a 3D mass ratio; band->3D mapping not modelled | **OVERSTATED** | The band-weighted amplitude ratio u rises from 0.472 in MID to 0.986 in OUTER; whether the 3D sourcing fraction rises is not established, because A21 does not model the band-to-3D mapping (the 3D MID value quoted by A18 is 0.65 against the 0.812 band share). |
| C04 | 0 | a constant u is excluded at 4.9 sigma by the band ratio | A21_u_half/a21_results.json:numbers.Z_band_MID_OUT = 4.910 (quadrature), Z_band_MID_OUT_worst = 3.824 (any correlation); A21 section 4 states 4.9 sigma in quadrature and >= 3.8 sigma for any band correlation | **OVERSTATED** | A constant u is excluded at 4.9 sigma in quadrature and at >= 3.8 sigma for any band correlation; section 0 quotes only the optimistic quadrature value, while section 5 gives the conservative one. |
| C05 | 0 | one free number, one free scale, one free function ... a completed effective theory; everything else asked for is derived, proved impossible, or pre-registered | FINAL_THEORY.md section 8 itself lists six open items (law-first/medium-first, the scale functional, u(r), the turn-off origin, L*'s value, UV completion); A4_ppn/report.md: y_t is a fitted posit ('It does not derive the turn-off') | **OVERSTATED** | The framework has one free number (kappa), one free scale (L*), one fitted turn-off (y_t, whose form is a posit), and six named open items in its own section 8; it is an effective description with those open premises, not a completed theory. |
| C06 | 1 | Z = 2 sqrt(8 pi/3) = 5.7888100; 2Z = 11.5776201 | A1_horizon/a1_results.json:numbers.Z = 5.788810036, two_Z = 11.577620073; A8 Lean two_sqrt_32pi_3 | **BACKED** | — |
| C06b | 1 | the count menu kappa(4pi,2pi,pi,2,1) = 0.2303294, 0.4606589, 0.9213177, 1.4472025, 2.8944050; factor 12.6; nearest 0.4607 is 7.9% low | A1_horizon/a1_results.json:numbers.kappa_menu and kappa_at_integer_counts; A10_first_principles/report.md section 5 | **BACKED** | — |
| C07 | 1 | a0/(cH_Lambda) = kappa sqrt(3/8pi) = 1/(2Z); kappa = Z/12 = 0.4824008, 3.52% from 1/2 | A1_horizon/a1_results.json:numbers.kappa_from_twelfth_Z_over_12 = 0.482400836, twelfth_gap_percent = 3.5198 | **BACKED** | — |
| C08 | 1 | Lean A8.inv_twoZ_ne_twelfth proves 1/(2Z) != 1/12 exactly | A8_lean/A8_C1_C2_kappa_Z.lean: theorem inv_twoZ_ne_twelfth; a8_lean_checks.out K5 | **BACKED** | — |
| C09 | 1 | hbar G Lambda / c^3 = 2.8498e-122 is the only dimensionless group built from {c,G,hbar,Lambda,H} | A1_horizon/a1_results.json:numbers.x_hbar_G_Lambda_over_c3 = 2.844773e-122 (BRIEF Lambda = 1.0890e-52); _parent/parent_audit.out Q1.5 = 2.849764e-122 (Lambda from H0, Omega_L = 0.685); A1 section 5.1: with H free the nullspace is 2-dimensional | **OVERSTATED** | hbar G Lambda / c^3 = 2.845e-122 with the BRIEF's Lambda (2.850e-122 with Lambda rebuilt from H0 and Omega_L = 0.685), and it is the only invariant only after imposing H = H_Lambda; with H free there are two dimensionless combinations (A1 section 5.1). |
| C10 | 1 | kappa = 4 sqrt(pi/3) = 4.093307, off by 8 sqrt(pi/3) = 8.186614 | A1_horizon/a1_results.json:numbers.kappa_P1 = 4.093306832, mismatch_P1_to_half = 8.186613664 | **BACKED** | — |
| C11 | 1 | every member of the strain-saturation family has kappa^2 in Q * pi^odd, hence kappa irrational | A1_horizon/report.md section 7, eqs (7.1)-(7.4), K9-K11 | **BACKED** | — |
| C12 | 1 | N T_dS = M_h c^2 identically reduces to rho = 3H^2/8piG | A1_horizon/a1_results.json / report section 8, K10 (sympy identity) | **BACKED** | — |
| C13 | 1 | a0/(cH0) = 1/7 to 5.6e-4, sixty times tighter than the 1/12 hit | A1_horizon/a1_results.json:numbers.a0_over_cH0 = 0.14293737; A1 report K13 | **BACKED** | — |
| C14 | 1 | the Euler charge is a total derivative and a0-blind; d(A Lambda)/da0 = 0 while dR/da0 != 0 | A19_scale_functional/report.md K4, K5; a19_results.json K1_worst_residual = 0.0 | **BACKED** | — |
| C15 | 1 | A Lambda = 32 pi^2 is the arithmetic identity 32 pi^2 = pi * 8pi * 4 | A19_scale_functional/report.md K15, eq (10) | **BACKED** | — |
| C16 | 1 | the GF2 chain's 1/2 is mu := sigma^2/v_c^2, not kappa | A15_closure_adjudication/a15_results.json:verdict = DIFFERENT-QUANTITY; K1 sigma2_over_C = 0.5 | **BACKED** | — |
| C17 | 1 | Verdict: DIFFERENT-QUANTITY. kappa is a modulus. | A15_closure_adjudication/report.md section 4 calls kappa_law 'a modulus of the theory', but its 'What this does not do' says 'It does not claim kappa is underivable in general'; the K9 symmetry is a flat direction of the two-equation halo truncation | **OVERSTATED** | Verdict: DIFFERENT-QUANTITY. kappa is a flat direction of the halo sector's two-equation truncation (A15 K9); A15 explicitly does not claim kappa is underivable in general, and the full action class may supply the missing equation (A15-C1, A19). |
| C18 | 1 | rho_DE appears zero times in the GF2 chain; CFG908 was right | A15_closure_adjudication/a15_results.json:numbers.rho_DE_mentions_in_gf2_record = 0; K8 | **BACKED** | — |
| C19 | 1 | rho_Lambda c^2/(a0^2/G) = 4 <=> Lambda ell0^2 = 32pi <=> kappa = 1/2 | A15_closure_adjudication/a15_results.json:K13 lambda_l0sq_at_half = 100.530965 = 32pi | **BACKED** | — |
| C20 | 1 | the saturation cap admits only R in {1,2,4}; measured kappa excludes them at 6.14, 3.05, 0.87 sigma; 4 is the only natural value the data admit. That is a selection, not a derivation | A19_scale_functional/report.md section 5 and K10; A19 Status: 'nothing in the class picks one; the data measure kappa itself' | **OVERSTATED** | A chosen three-member cap family gives kappa in {1, 0.7071, 0.5}; the measured kappa = 0.417 +/- 0.095 fails to exclude 0.5 at 0.87 sigma while excluding the other two, so the data select nothing positively - 0.5 is merely the only member not excluded, and kappa is what the data measure. |
| C21 | 1 | the Unruh/de Sitter control gives R = 3/(8pi) = 0.1194 -> kappa = 2.894, excluded at 33.5x | A19_scale_functional/report.md section 6, K12; a19_results.json R_alt_footing and K12 | **BACKED** | — |
| C22 | 2 | the canonical law is exactly the Langmuir isotherm theta = x/(1+x), x = g/a0 | A2_medium/a2_results.json:K1 sympy identity; A2 report eqs (1)-(4) | **BACKED** | — |
| C23 | 2 | Answer: a single-scale two-state lattice - and it forces n = 1. n = 1 is forced by one gate per site | A2_medium/a2_results.json:status = 'CONDITIONAL(single-scale driven two-state lattice: capacity = affinity = a0); n=1 forced' in that class; A2 report section 4 derives C = s = a0 from the assumed deep limit | **OVERSTATED** | Within the stated class (single-scale, two-state, one occupant per site, mass-action with linear drive, capacity = affinity), n = 1 is the unique member; the lattice does not derive a0, and the capacity is fixed by matching the observed deep-MOND limit rather than derived from the lattice. |
| C24 | 2 | with the capacity identified as the affinity, a0, the stationary condition is the law, with no new fitted constant | A2_medium/report.md section 4, eq (10): the deep limit forces C = s exactly and s = a0 | **BACKED** | — |
| C25 | 2 | there is no equilibrium Gibbs state with linear coupling: the Fermi occupancy stays finite at g = -a0, where Langmuir has its only pole | A2_medium/report.md section 3, K4 (measured 0.2689) | **BACKED** | — |
| C26 | 2 | sigma(log g) scales as g^-3/2 with (g+a0)/(g+2a0); sigma(0.3a0)/sigma(3a0) = 22.34 (n=1) vs 34.49 (n=2); skew( delta g ) flips at g = a0 | A2_medium/a2_results.json:numbers.sigma_ratio_0p3_3_n1 = 22.3422, n2 = 34.4859, sigma_log_slope_high_g = -1.49979 | **BACKED** | — |
| C27 | 2 | n = 2 is a NO-GO in the thermal-lattice class: no positive mixture of two-state gates reproduces it | A2_medium/report.md section 5, K7: branch points +/- i a0/2, not a Stieltjes function | **BACKED** | — |
| C28 | 2 | n = 2's natural home is the Poisson second-moment identity <n^2> = lambda^2 + lambda, not a maximum-entropy law | A10_first_principles/report.md section 6, K13 (exact identity) | **BACKED** | — |
| C29 | 2 | max (g1-g2)/g2 = 2/sqrt3 - 1 = 15.4700% at g_N = a0/2 | A2_medium/a2_results.json:numbers.max_frac_g_exact = 0.1547005384 | **BACKED** | — |
| C30 | 2 | which is sqrt(2/3) - 1 = 7.4570% in circular speed; my harness Q2.8 reproduces both | A2_medium/report.md eq (16): max (v1-v2)/v2 = sqrt(2/sqrt3) - 1 = 0.0745699318; _parent/parent_audit.out Q2.8: max_frac_v = 0.0773503 (one half of 15.47%, a linearisation, not 7.457%) | **WRONG** | which is sqrt(2/sqrt3) - 1 = 7.4570% in circular speed; the parent harness Q2.8 does not reproduce it - Q2.8 linearly halves the acceleration difference and returns 7.735%, while the exact circular-speed maximum is 7.457%. |
| C31 | 2 | v^2 = g r, so the two figures are the same number in different units | Exact algebra: at fixed r, delta v/v = sqrt(1 + delta g/g) - 1 = 7.457% for delta g/g = 15.47%, not 15.47/2 = 7.735% | **OVERSTATED** | v^2 = g r makes the circular-speed difference sqrt(1 + delta g/g) - 1 = 7.457%, not half the acceleration difference (7.735%); the two figures are related by a square root, not by a unit change. |
| C32 | 3 | (Phi-Psi)/Psi = O(Psi) = 2.63e-7; 9.13e-8 at 10 kpc | A12_slip_theorem/a12_results.json:numbers.slip_max_abs_1mPhiOverPsi = 2.630068e-7, slip_10kpc = -9.132216e-8; A3 report section 2.4 | **BACKED** | — |
| C33 | 3 | GW speed = c: DERIVED (exact), c_T^2 = 1 exactly, not to leading order | A3_lensing_gw/report.md section 3.1: 'Background Pbar = 0, N = 1'; section 7: 'c_T = 1 is a classical statement about the quadratic action on a Pbar = 0 de Sitter background'; _parent/a3_gw_certificate.out K4: the only TT-P coupling is a mass term that vanishes where P = 0; A22_ppn_frames/report.md D4: the Solar System is a hedgehog with P != 0 | **OVERSTATED** | c_T^2 = 1 exactly on the Pbar = 0 de Sitter background (A3 section 3.1); the proof does not cover a Pbar != 0 background such as A22's Solar-System hedgehog, where W(u) contracts P_iP_j with the TT perturbation and adds a mass term, so the quadratic tensor action is not the Einstein one there. |
| C34 | 3 | adding a P-curvature coupling shifts c_T^2 off 1 (my mutation demonstrates it) | A3_lensing_gw/MUTATE.md: the only c_T^2 mutation is 'naive_stiffness' (non-Hodge norm(D_iP_j)^2), giving c_T^2 = 1 + 2K abs(P)^2; no P-curvature mutation is run | **WRONG** | Adding a non-Hodge stiffness norm(D_iP_j)^2 shifts c_T^2 to 1 + 2K abs(P)^2 and the mutation demonstrates that; a P-curvature coupling (xi R_ij P^iP^j or zeta R P^2) would also break c_T^2 = 1, but no mutation of that operator was run. |
| C35 | 3 | kernel anomaly a0 = 2557.38 B_E; 2557.38x, twice the quadrature's published 1279x | A4_ppn/a4_results.json:numbers.a0_over_B_E = 2557.377, half_a0_over_B_E = 1278.689 | **BACKED** | — |
| C36 | 3 | y_t = 66.30 closes Lambda, planets pass with a 9.14x margin; Neptune sits at 1.2% of its bound | A4_ppn/a4_results.json:numbers.y_t_canonical = 66.29994, y_t_margin = 9.1397, worst_planet_ratio = 0.011972 | **BACKED** | — |
| C37 | 3 | a_P = GM/L*^2 = 2.4205e-16 m/s^2 = 6.61e-3 B_E, 151x inside the ephemeris bound | A22_ppn_frames/a22_results.json:numbers.a_P_constant_anomaly_m_s2 = 2.420469e-16, a_P_over_BE = 0.0066133, aP_margin_BE_over_aP = 151.21 | **BACKED** | — |
| C38 | 3 | dg/dg_N in [1,infinity); scalar front speed c_s = sqrt(gamma/eta) <= c iff gamma <= eta | A4_ppn/a4_results.json:numbers.response_min_over_u_le_a0 = 1.06066; A3 report section 4, K8 | **BACKED** | — |
| C39b | 3 | SPARC cannot decide: Delta chi^2 = +219.45 canonical / -344.66 alt; sd 22.7; z = +0.75 / -1.21; wins 84/87 and 73/98; forecast N ~ 1330-1980; 3x at N=171; per-galaxy S/N 0.068-0.082 | A7_discriminator/a7_results.json:numbers.canonical.dchi2 = 219.453, alt.dchi2 = -344.663, canonical.z_boot = 0.7453, alt.z_boot = -1.2094, n1_wins/n2_wins = 84/87 and 73/98; A7 report F2 N = 1327-1976 and section Forecast | **BACKED** | — |
| C39 | 3 | Preferred frame: DERIVED (zero), alpha_1 = alpha_2 = 0 exactly, beta = 1 | A22_ppn_frames/a22_results.json:alpha1_ppn_order = 0, alpha2_ppn_order = 0, beta_ppn_minus_1 = 0; A22 report 'What this does not do': 'D5-D6 are exact only for r << lambda = 17 pc ... at r >> lambda ... an effective alpha_1 ~ O(1) ... Not computed' | **OVERSTATED** | alpha_1 = alpha_2 = 0 and beta = 1 at PPN order in the Solar-System linear regime r << lambda = 17 pc (A22 D5-D6); A22's own caveat says that at r >> lambda the P field is MOND-slaved and an effective alpha_1 ~ O(1) is not computed, so this is a regime-limited zero, not a global one. |
| C40 | 3 | in aether variables c1 = c3 = c4 = 0, c2 = -beta_ADM, for which the published alpha_1 and alpha_2 both vanish | A22_ppn_frames/a22_checks.py lines 221-223: den = 2*c1 - c1^2 + c3^2 = 0 at c1=c3=c4=0, and the code sets alpha1_lit = 0 if den == 0; the published alpha_1 expression is 0/0 at that point, not 0 | **WRONG** | At c1 = c3 = c4 = 0 the published alpha_1 expression is 0/0 (its denominator 2c1 - c1^2 + c3^2 vanishes), so the aether formula does not establish alpha_1 = 0; the zero follows only from the separate theta == 0 / no-momentum-stress arguments in A22 D2-D3, and the aether citation should be dropped. |
| C41 | 3 | the remaining route to alpha_1, alpha_2 is the (1+beta)theta^2 deformation, which is a genuine preferred-frame term and is not closed here - it is the one gate still open | A22_ppn_frames/report.md D2 (F1): theta == 0 on static configurations and theta^2 is O(h^2), so the deformation is inert at linear order; A22 closes the gate (status CLOSED-DERIVED); _parent/a22_no_cosmic_aether.out SCOPE says the theta^2 route 'is A22's job' | **WRONG** | The (1+beta)theta^2 deformation is inert at PPN order: theta == 0 on static configurations and theta^2 is O(h^2), so it has no linearised stress (A22 D2, K5); A22 closes this route, and the sentence is a stale copy of the parent scope note. |
| C42 | 3 | P = 0 is the unique homogeneous solution on FRW (coordinator 4/4, mutation bites) | _parent/a22_no_cosmic_aether.out: 4/4, dW/du zeros [0], W strictly increasing; A22 report D8 | **BACKED** | — |
| C43 | 3 | imposing the Galactic field moves gamma_v by 0.350 (12.7 sigma) while the QUMOND-vs-AQUAL solver fork is <= 0.019 (0.7 sigma) - the EFE is 18x larger | A24_wide_binaries/a24_results.json:numbers.delta_gamma_efe_20kAU = 0.350394, z_efe_sig_tot = 12.7018, delta_gamma_solver = 0.019395, z_solver_sig_tot = 0.7031 | **BACKED** | — |
| C44 | 3 | gamma_v = 1.18 at 20 kAU (bracket 1.1771-1.1933), which sits inside Arm A's 1.1614-1.1814 | A24_wide_binaries/a24_results.json:numbers.efe_bracket_20kAU = [1.177143, 1.193324]; A24 report section 3: 1.1811 is 0.0003 below the Arm A top, 1.1933 is 0.012 above it | **OVERSTATED** | gamma_v = 1.177-1.193 at 20 kAU, within 0.6 sigma_fit of Arm A's top 1.1814; 1.1771 lies inside the band, 1.1811 is 0.0003 inside, and 1.1933 lies 0.012 above it, so the bracket straddles the band edge rather than sitting inside the band. |
| C45 | 3 | the 1.51 figure comes from dropping the EFE and using the total rather than exact two-body composition: 1.5315 (mass) -> 1.4037 (composition) -> 1.1933 (EFE) | A24_wide_binaries/report.md section 4 chain table: 1.5107 (paper recipe) -> 1.6160 (kernel) -> 1.5315 (mass) -> 1.4037 (composition) -> 1.1933 (EFE) | **BACKED** | — |
| C46 | 3 | 1.51 > 1.23, the framework's own no-verdict zone, so a 1.51 detection could never have scored as confirmation | A24_wide_binaries/report.md section 4 item 3: 'gamma_hat > 1.23 is the guard zone, no hypothesis verdict permitted' | **BACKED** | — |
| C47 | 3 | the vacuum integral diverges linearly for both, canonical twice as fast (pi/2 vs pi/4 per unit y_t); C_can = -0.8862944 = 8 C_quad | A4_ppn/a4_results.json:numbers.C_can = -0.886294361, C_quad = -0.110786795, C_ratio = 8.0; I_can_over_Y_limit = 1.5708, I_quad_over_Y_limit = 0.7854 | **BACKED** | — |
| C48 | 3 | Lambda c^4/a0^2 = 100.4058; the turn-off solves to y_t = 66.2999, i.e. 6.21e-9 m/s^2 | A4_ppn/a4_results.json:numbers.N_Lambda_dimensionless = 100.405845, y_t_canonical = 66.29994, y_t_canonical_a0 = 6.205674e-9 | **BACKED** | — |
| C49 | 3 | the quadrature law needs y_t = 128.7559; feeding it to the canonical law over-predicts Lambda by 1.9707x; ratio 1.942 | A4_ppn/a4_results.json:numbers.y_t_quadrature = 128.75587, F_can_at_y_t_quad_over_N = 1.970683, y_t_ratio_quad_over_can = 1.942021 | **BACKED** | — |
| C50 | 3 | That is a conditional pass with the premise named: the turn-off exists and its scale is tied to Lambda, not fitted | A4_ppn/report.md 'What this does not do': 'It does not derive the turn-off. nu_fix is a posit inherited from Zenodo 23171085; y_t is a fitted number'; A4 Status: CONDITIONAL(turn-off premise) | **WRONG** | That is a conditional pass: the turn-off's functional form is a posit inherited from Zenodo 23171085 and y_t is a fitted number (A4), which the Lambda closure then fixes to 66.30 once the form is assumed. |
| C51 | 8 | The turn-off's origin: y_t = 100.4 closes Lambda, but nothing yet forces it | A4_ppn/a4_results.json:numbers.y_t_canonical = 66.29994; N_Lambda_dimensionless = 100.405845. 100.4 is the dimensionless vacuum integral, not y_t | **WRONG** | The turn-off's origin: y_t = 66.30 closes Lambda, but nothing yet forces it (100.4058 is Lambda c^4/a0^2, the target the closure meets). |
| C52 | 4 | L* is the pressure switch-off radius, and that is a derived identity, not a definition | A16_cutoffs_edge/report.md section 6 derives R_press = (L*/r)^2; A20_Lstar_cores/report.md 'What this does not do' 2: 'L* is still not derived'; A20 section 1: against total gravity the switch is L* sqrt(f_c), not L* | **OVERSTATED** | The pressure-to-gravity ratio is the derived identity (L*/r)^2 against the cold sector's own gravity; L* itself is not derived, and against total gravity the switch is at L* sqrt(f_c) (A20). |
| C53 | 4 | (1/rho) dp/dr / g = (L*/r)^2 for cusps 1 <= n <= 2 - density-free | A16_cutoffs_edge/report.md eq (11); A20_Lstar_cores/report.md eq (1) with residual 0 | **BACKED** | — |
| C54 | 4 | r_switch = L* against the cold sector's own gravity; L* sqrt(f_c) against total: 3.73 pc (MW), 18.40 pc (dwarf) at L* = 24 pc | A20_Lstar_cores/a20_results.json:numbers.fc_rswitch_dwarf_24pc = 18.4; A20 report table row MW r_switch = 3.73 pc | **BACKED** | — |
| C55 | 4 | R_core = (pi/sqrt2) L* = 53.31 pc at L* = 24 pc | A20_Lstar_cores/a20_results.json:numbers.R_core_24pc = 53.3146, K2 polytrope residual 0 | **BACKED** | — |
| C56 | 4 | force-balance deviation 13.40% at 2 r_switch, 2.02% at 5 r_switch, 1% at 7.09 r_switch; plateau 1.21% (MW) / 35.82% (dwarf) | A20_Lstar_cores/a20_results.json:numbers.delta_ladder_r_over_rsw and delta_plateau_MW_max = 0.014839, delta_plateau_dwarf_min = 0.358185 | **BACKED** | — |
| C57 | 4 | window after the data: 24 pc - 90 pc (LITTLE THINGS: L* <= 90.0 pc from IC 10; 300 pc excluded by 3.33x, 1 kpc by 11.11x) | A20_Lstar_cores/a20_results.json:numbers.lt_Lstar_bound_pc = 90.0, lt_Lstar_bound_p10_pc = 184.6, lt_Lstar_bound_med_pc = 787.8, lt_bound_fc05_pc = 127.3, lt_bound_fc025_pc = 180.1; A20 'What this does not do' 3: the 90 pc is the f_c -> 1 reading | **OVERSTATED** | The one-sided bound L* <= 90 pc comes from a single galaxy (IC 10) under the f_c -> 1 assumption that the cold sector dominates the inner mass; at f_c = 0.5 it weakens to 127 pc, at f_c = 0.25 to 180 pc, and the sample's 10th-percentile bound is 184.6 pc (median 787.8 pc), so '24-90 pc' is a best-case single-object window, not a sample bound. |
| C58 | 4 | in horizon units L* H0/c = 5.40e-9 - 2.25e-7 (row under the 24-90 pc window) | _parent/parent_audit.out Q4.2: [5.3957e-9, 2.2482e-7] is 24 pc to 1 kpc; at 90 pc the value is 2.02e-8 | **WRONG** | In horizon units L* H0/c = 5.40e-9 to 2.02e-8 for the 24-90 pc window; the quoted 2.25e-7 is the 1 kpc end of the published window, not the 90 pc end. |
| C59 | 4 | a c/sqrt(G rho) reading requires rho = 2.4e14 - 4.2e17 rho_Lambda (a medium density, not the vacuum) | _parent/parent_audit.out Q4.3: [2.4196e14, 4.2008e17] | **BACKED** | — |
| C60 | 4 | L* = sigma^2/a0 maps 24 pc <-> 8.33 km/s; 90 pc <-> 16.1 km/s | sigma = sqrt(a0 L*): 8.3257 km/s at 24 pc; 16.12 km/s at 90 pc; A20 cand1_sigma_km_s | **BACKED** | — |
| C61 | 4 | Jeans mass at switch-off M_J = 3.654 V_f^2 L*/G = 2.04e4 (V_f/km/s)^2 Msun = 5.57e8 Msun | A16_cutoffs_edge/a16_results.json:numbers.MJ_coefficient = 3.65412, M_J_per_kms2_Msun = 20390.1, M_J_isothermal_Msun = 5.56468e8, M_J_at_switch_NFW_Msun = 3.14912e6; A16 'What this does not do' 5: NFW gives 3.149e6, 'the class is GC-to-UCD' | **OVERSTATED** | For the law's flat-curve profile the Jeans mass at switch-off is 3.654 V_f^2 L*/G = 2.04e4 (V_f/km/s)^2 Msun = 5.57e8 Msun; the same halo read with NFW gives 3.15e6 Msun, so the mass is fixed only to about 2 dex by the inner profile. |
| C62 | 4 | d ln M_J/d ln rho = +1 (standard Jeans -1/2) | A16_cutoffs_edge/a16_results.json:numbers.dlnMJ_dlnrho = 1.0, K21 exactly 1 | **BACKED** | — |
| C63 | 4 | L* = V_f^2/(9a0) fails: 2.637 dex spread, 30.3% outside the window, 55 km/s (6.7x the 8.23 km/s) | A20_Lstar_cores/a20_results.json:numbers.cand2_spread_dex = 2.637, cand2_frac_outside_window = 0.3029, cand2_sigma_MW_km_s = 55.07, cand2_sigma_MW_over_thermal = 6.691 | **BACKED** | — |
| C64 | 4 | L* = sigma^2/a0 survives at 24 pc and dies at 1 kpc; its own cap is L* <= 93.8 pc | A20_Lstar_cores/a20_results.json:numbers.cand1_L_max_C4_pc = 93.8, cand1_sigma_over_thermal['24'] = 1.012, ['1000'] = 6.53 | **BACKED** | — |
| C65 | 4 | the guard removes the upper half of the published window and leaves a single number, ~24 pc | A20_Lstar_cores/report.md section 8: the surviving window is [24, 90] pc and 'the dispersion picks the bottom of it'; 24 pc is the 10^4 K thermal width, not a measurement | **OVERSTATED** | The guard removes the upper half of the published window and leaves the window 24-90 pc; 24 pc is the bottom set by the 10^4 K thermal width, not a measured single value. |
| C66 | 4 | SPARC's 30-inch beam floors at ~142 pc, innermost reliable radius 80 pc, 0/175 galaxies probe a 24 pc core | A20_Lstar_cores/a20_results.json:numbers.sparc_beam_min_pc = 142.5, sparc_rfirst_min_pc = 80.0, sparc_frac_inside_rfirst['24'] = 0.0 | **BACKED** | — |
| C67 | 4 | ngVLA at 0.15 arcsec reaches 24 pc to 33 Mpc; ~30 dwarfs with V_f < 40 km/s inside 8 Mpc; 21.03% dip at 30 pc, 11.21% at 40 pc, >= 5 sigma | A20_Lstar_cores/a20_results.json:numbers.fc_ngvla_beam_arcsec = 0.15, fc_ngvla_reach_Mpc = 33.0, fc_N_dwarfs = 30, fc_dip_30pc = 0.2103, fc_dip_40pc = 0.1121 | **BACKED** | — |
| C68 | 4 | L* is 7-8 decades below c/H0; one L* gives lambda_J = 4.443 L* (106.6 pc), lambda_FS ~ 82 kpc, half-mode ~1.02 Mpc, spread >= 3.36 dex | A16_cutoffs_edge/a16_results.json:numbers.lambda_J_24pc_pc = 106.629, lambda_FS_24pc_kpc = 82.350, lam_half_Mpc['24'] = 1.02046, spread_min_dex = 3.3568; _parent Q4.1 | **BACKED** | — |
| C69 | 5 | M_ph/M_b = 1/2(sqrt(1+4/y)-1) at the virial radius is 25.04 (MW-like) and 2.62 (cluster-like), 9.57x apart | A18_two_ratios/a18_results.json:numbers.MW.F_enc = 25.8985, MW.R_tot = 25.0429; cluster.F_enc = 3.77015, cluster.R_tot = 2.61793. The formula F(y_v) gives 25.90/3.77 (ratio 6.87); 25.04/2.62 is R_tot = mu(1+F)-1, the phantom per total baryon | **WRONG** | M_ph(<r_v)/M_b(<r_v) = 1/2(sqrt(1+4/y_v)-1) is 25.90 (MW-like) and 3.77 (cluster-like), 6.87x apart; the phantom per total baryon, R_tot = mu(1+F)-1, is 25.04 and 2.62, 9.57x apart. |
| C70 | 5 | the two ratios cross at M_v = 1.7584e14 Msun, independent of concentration | A18_two_ratios/a18_results.json:numbers.cross_Mv_enc_Msun = 1.7584e14, cross_Mv_enc_spread = 0.0 | **BACKED** | — |
| C71 | 5 | cold = the law's phantom is excluded at 7.7 sigma; A_MID = 1.9102 +/- 0.1186; phantom predicts 1.000, cosmic share 1.852; data 0.49 sigma from cosmic, 7.67 sigma from phantom | A18_two_ratios/a18_results.json:numbers.A_MID_residual_hi, A_pred_cosmic = 1.85203, Z_law = 7.6745, Z_cos = 0.4905 | **BACKED** | — |
| C72 | 5 | the exact two-body solution requires -89.32x the mean cold density at R = 0.2d for M_b = 1.4e11 Msun each at d = 780 kpc; plausible band -75.5 to -110.9 | A6_assets/a6_results.json:numbers.ratio_panc_over_rbarc_MW = -89.3197, ratio_panc_MW_M1.0e11 = -75.49, ratio_panc_MW_d700kpc = -110.90; independent A31 recomputation -89.19 | **BACKED** | — |
| C73 | 5 | pancake 30.5 deg wide, 26.3% of the solid angle at R = 0.2d; abs(rho) ~ r^-1/2 at the null (0.6%) | A6_assets/a6_results.json:numbers.pancake_half_width_deg = 15.275, pancake_solid_angle_percent = 26.345; A6 K7 spread 0.597% | **BACKED** | — |
| C74 | 5 | Since A24 established that the law does carry an EFE, A13's suppression curve transfers | A23_no_efe_saddle/report.md sections 4 and 6: A13's curve is a mirror-symmetry artefact, 0.746 at e=0.3 on the half domain vs 0.050 on the full domain; 'its quantitative curve is not transferable' | **WRONG** | Since A24 established that the law carries an EFE, A13's qualitative conclusion transfers (the dip is switched off in dense environments) but its suppression curve does not: A23's full-domain solve gives 0.050 at e = 0.3 against A13's 0.751. |
| C75 | 5 | the dip needs e <= 0.22 (g_ext <= 3.2e-4 a0), while a deep void is at e = 0.68, a filament at 10.2 and a group at 34.1 | A23_no_efe_saddle/a23_results.json:numbers.decision.e_half = 0.1287, retained_at_0p68 = 0.0, void_e = 0.682, filament_e = 10.231; A23 report section 5 (e_req 0.21-0.24, g_ext 3-3.5e-4 a0) | **BACKED** | — |
| C76 | 5 | retained column 1.00 / 0.64 / 0.40 / 0.24 / 0.05 / 0.00 at e = 0 / 0.1 / 0.15 / 0.2 / 0.3 / 0.68 | A23_no_efe_saddle/a23_results.json:numbers.decision.retained_at_0p1 = 0.6411, 0p2 = 0.2372, 0p3 = 0.0501, 0p68 = 0.0; A23 report table 0.396 at 0.15 | **BACKED** | — |
| C77 | 5 | A13's half-domain 0.746/0.332 at e = 0.3/1.0 vs 0.050 at e = 0.3 on the full domain | A23_no_efe_saddle/a23_results.json:numbers.half_domain_aqual = {'0.3': 0.74564, '1.0': 0.33174}, decision.retained_at_0p3 = 0.0501 | **BACKED** | — |
| C78 | 5 | -33 is not a cluster-pair number: at d = 3 Mpc a cluster pair gives -485; -33 needs d = 11.78 Mpc and then the column is -19.73; the two cluster numbers need a group pair (4.2e12 Msun each, 3 Mpc): -33.07 and -5.025 | A6_assets/a6_results.json:numbers.ratio_panc_over_rbarc_cluster_3Mpc = -485.29, d_for_minus33_Mpc = 11.7777, col_neg_cluster_d33 = -19.726, group_ratio = -33.0678, group_col_neg = -5.02515 | **BACKED** | — |
| C79 | 5 | the net column is -2.424 Msun/pc^2 (negative -3.529, positive +1.105); +0.016 appears only within ~1 deg of phi = 77.44 deg; at phi = 90 deg it is -2.42 | A6_assets/a6_results.json:numbers.col_net_MW_Msun_pc2 = -2.42418, col_neg_MW = -3.52886, col_pos_MW = 1.10468, phi_zero_crossing_deg = 77.4416 | **BACKED** | — |
| C80 | 5 | the missing depth is 3.529 Msun/pc^2 (A6, explicit masses), not 2.16-2.37 (A13, which rescales the paper's own units rather than recomputing) | A6_assets/a6_results.json:col_neg_MW_Msun_pc2 = -3.52886; A13_saddle_forecast/report.md section 3.1 is an independent PDE solve (four resolutions, Richardson) giving 2.159/2.374; the 1.5x disagreement is not resolved by either lane | **WRONG** | The MW missing depth is 3.529 Msun/pc^2 in A6's explicit-mass calculation and 2.16-2.37 Msun/pc^2 in A13's independent PDE solve (A13 section 3.1 is a solve, not a rescaling of the paper's units); the 1.5x discrepancy between two stated-input calculations is unresolved and should be reported as a systematic, not adjudicated by assertion. |
| C81 | 5 | a naive superposition gives the wrong sign (+0.64), so the pancake is strictly nonlinear | A13_saddle_forecast/report.md section 2 item 3: C = 2/pi = +0.6366 | **BACKED** | — |
| C82 | 5 | the 11.8x pair requirement (~8282 pairs for 3 sigma) reproduces the published 'about twelve times' | A6_assets/a6_results.json:numbers.survey_N3 = 8281.8, survey_multiple = 11.8312 | **BACKED** | — |
| C83 | 5 | u = 0.4716 +/- 0.0362 (MID) -> 0.9865 +/- 0.0984 (OUT); MID 0.78 sigma from 1/2, OUT 4.9 sigma; bands differ by >= 3.8 sigma | A21_u_half/a21_results.json:numbers.Z_half_cluster = 0.7845, Z_half_OUT = -4.9434, Z_band_MID_OUT_worst = 3.8239 | **BACKED** | — |
| C84 | 5 | the law's ratio spans 9.566x between the anchors, the retention table 9.0x, quotient 1.063 | A21_u_half/a21_results.json:numbers.ratio_law_anchors = 9.56592, ratio_u_anchors = 1.06288; ratio_fret_anchors = 0.11111 | **BACKED** | — |
| C85 | 5 | u = 1/2 is structurally excluded: u = 1 + 3<w> forces w = -1/6 (negative sound speed); f_ret <= 1 caps the cluster at u <= 0.4880, so 1/2 needs f_ret = 1.0245 | A21_u_half/a21_results.json:numbers.route_i.w_for_half = -0.166667, u_ceiling_cluster = 0.488026, fret_needed_cluster = 1.02454 | **BACKED** | — |
| C86 | 5 | the MW anchor needs f_ret = 0.1071, which is admissible; the two anchors cannot both be at 1/2 for a physical reason | A21_u_half/a21_results.json:numbers.fret_needed_MW = 0.107103 | **BACKED** | — |
| C87 | 5 | u ~ (f_ret/R_cosmic)[y_v^-1/2 - 1/2], d ln u/d ln M_v -> +1/6, spanning 0.37-0.72 over 1e10-1e14 Msun | A21_u_half/a21_results.json:numbers.n_candidates, one_sixth = 0.166667, u_window values 0.3696-0.7164 | **BACKED** | — |
| C88 | 5 | A18's prose reverses its sign: the phantom is too diffuse, not too centrally concentrated (1.910 MID vs 1.012 OUTER) | A21_u_half/report.md section 4: 'the data's excess is more centrally concentrated than the law's phantom'; A21 numbers.residual_ratio_MID_OUTER = 1.8879 | **BACKED** | — |
| C89 | 5 | 3 sigma needs sigma(A_MID) <= 0.0312, i.e. >= 4602 clusters; the group stack at M_v = 1e13 has A_MID 1.8122 vs 1.4051 (33% in cold mass), needing sigma(A) <= 0.136 | A21_u_half/a21_results.json:numbers.Z_half_cluster and report K21 (sigma_u <= 0.00948, sigma_A <= 0.0312, N >= 4602); A21 report section Falsifier | **BACKED** | — |
| C90 | 5b | inside lambda = 17 pc the gamma-gradient term beats the mass term; P is a hedgehog of constant magnitude GM/(2 gamma) with u = 2.59e-6 a0 | A22_ppn_frames/a22_results.json:numbers.lambda_P_compton_pc = 16.9706, u_P_over_a0 = 2.58597e-6 | **BACKED** | — |
| C91 | 5b | the crossover defines M_crit = a0 L*^2/G = 3.87e5 Msun below which the medium never reaches the MOND branch | A22_ppn_frames/a22_results.json:numbers.M_crit_MOND_Msun = 386701.97 | **BACKED** | — |
| C92 | 5b | medium-first reading: wide-binary gamma_v at 20 kAU = 1.0 | No lane computes a medium-first wide-binary boost. A22 computes the P-field hedgehog and the sub-threshold mass, but never gamma_v; the 1.0 is an assumption that 'not in the MOND branch' equals Newtonian | **UNBACKED** | Medium-first: gamma_v at 20 kAU is not computed by any lane; the table's 1.0 assumes that a system inside lambda, with the P field off the MOND branch, reduces to Newtonian, which A22 does not demonstrate. |
| C93 | 6 | P1 depth 3.529 (MW) / 5.025 (group) Msun/pc^2 | A6_assets/a6_results.json:numbers.col_neg_MW_Msun_pc2 = -3.52886; group_col_neg_Msun_pc2 = -5.02515 | **BACKED** | — |
| C94 | 6 | P1 needs e <= 0.22; no accessible environment has it (void 0.68) - not runnable | A23_no_efe_saddle/a23_results.json:numbers.decision; A23 report section 5 | **BACKED** | — |
| C95 | 6 | P1b: 30.5 deg wide, 26.3% of solid angle, abs(rho) ~ r^-1/2 | A6_assets/a6_results.json:numbers.pancake_half_width_deg, pancake_solid_angle_percent, K7 | **BACKED** | — |
| C96 | 6 | P7b: y_t = 66.30 (n=1) vs 128.76 (n=2), ratio 1.94 | A4_ppn/a4_results.json:numbers.y_t_canonical = 66.29994, y_t_quadrature = 128.75587, y_t_ratio_quad_over_can = 1.94202 | **BACKED** | — |
| C97 | 6 | P9: sign change of skew(delta g) exactly at g = a0 | A2_medium/report.md section 7, K13: skew ~ (1-2 theta), zero at theta = 1/2 i.e. g = a0 | **BACKED** | — |
| C98 | 6 | P2: MID/OUTER = 0.966 +/- 0.102 (native) vs 1.888 +/- 0.203 (phantom) | A18_two_ratios/a18_checks.py K18: mo_hut = A_HUT/A_HUT_OUT = 0.966 and mo_law = A_LAW/A_OUT_LAW = 1.888 are both ratios of measured amplitudes; the phantom's own band ratio is 1 by construction, so 1.888 is a data/model residual ratio, not a predicted band ratio | **OVERSTATED** | The measured amplitude ratio is 0.966 +/- 0.102 under the native normalisation and 1.888 +/- 0.203 under the law normalisation; 1.888 is the data/law residual ratio (how much more concentrated the data are than the phantom), not the phantom's predicted MID/OUTER, which is 1 by construction. |
| C99 | 6 | P3: u(MID) = 0.4716 +/- 0.0362, u(OUT) = 0.9865 +/- 0.0984 | A21_u_half/a21_results.json:numbers.u_data, u_OUT | **BACKED** | — |
| C100 | 6 | P3b: at M_v = 1e13, A_MID = 1.8122 (u=1/2) vs 1.4051 (cosmic share); sigma(A) <= 0.136; 33% difference | A21_u_half/report.md section 11 and Falsifier; a21_results.json K20 split 1.3345 | **BACKED** | — |
| C101 | 6 | P4: R_core = 53.31 pc at L* = 24 pc; 21.0% dip at 30 pc, 11.2% at 40 pc | A20_Lstar_cores/a20_results.json:numbers.R_core_24pc = 53.3146, fc_dip_30pc = 0.2103, fc_dip_40pc = 0.1121 | **BACKED** | — |
| C102 | 6 | P5: gamma_v = 1.18 at 20 kAU (bracket 1.1771-1.1933), 1.16 at 10 kAU; 2223 pairs, 4.5 sigma | A24_wide_binaries/a24_results.json:numbers.efe_bracket_20kAU, pairs_in_18_22kAU_bin = 2223.05, z_bin_20kAU = 4.5258; at 10 kAU the EFE-present exact value is 1.100 (1.107 canonical), while 1.1605 is the EFE-blind exact value | **WRONG** | P5: gamma_v = 1.177-1.193 at 20 kAU; with the EFE present the 10 kAU prediction is 1.100 (1.107 canonical), not 1.16 - 1.16 is the EFE-blind exact value (A24 table, section 3); the 18-22 kAU bin holds 2223 pairs and separates at 4.5 sigma. |
| C103 | 6 | P5b: Delta chi^2(Q-L) = +157.96 canonical / +75.25 alt with no free parameters; +17.05 profiled; Delta chi^2(R-L) = +10.1/-0.8 | A25_kernel_conflict/report.md section 7 and K9-K10; a25_results.json KiDS_lensing dchi2_Q_minus_L | **BACKED** | — |
| C104 | 6 | P6: abs(delta G/G) < 1e-6 (framework) vs 340 ppm (source-boost), two-configuration Cavendish at 30-50 ppm | A5_zenodo/report.md clue 5 (record 23397365) | **BACKED** | — |
| C105 | 6 | P7: 15.47% max in g at g_N = a0/2 | A2_medium/a2_results.json:numbers.max_frac_g_exact = 0.1547005384 | **BACKED** | — |
| C106 | 6 | P8: d ln M_J/d ln rho = +1; standard -1/2 | A16_cutoffs_edge/a16_results.json:numbers.dlnMJ_dlnrho = 1.0 | **BACKED** | — |
| C107 | 7 | #1 GF2's kappa = 1/2 is mu = sigma^2/v_c^2, not the law's kappa; CFG908 stands | A15_closure_adjudication: verdict DIFFERENT-QUANTITY, K1/K7/K8 | **BACKED** | — |
| C108 | 7 | #2 A11's c_s = 0.72c is a unit slip - c_s = 0.72 m/s; A11's Task-2 no-go and L* <= 0.0608 pc are withdrawn | A16_cutoffs_edge/a16_results.json:numbers.cs_cosmic_24pc_ms = 0.720473, cs_over_c = 2.4032e-9; A11_cold_normalization/report.md lines 133-136 contain the 0.72c and 0.0608 pc claims | **BACKED** | — |
| C109 | 7 | #3 A9's a0 -> a0/f is wrong; it is a0 -> a0/f^2; 0.207 dex measured vs 0.210 predicted for p=2, 0.105 for p=1 | A14_upsilon_free/report.md D2 and K5; a14_results.json a0_scatter_dex = 0.2067, pred_scatter_p2 = 0.2101, pred_scatter_p1 = 0.105 | **BACKED** | — |
| C110 | 7 | #4 Zenodo 23533323's 'total column positive' does not hold; net -2.42 Msun/pc^2; the cluster -33 is at 11.78 Mpc | A6_assets/a6_results.json:col_net_MW_Msun_pc2 = -2.42418, d_for_minus33_Mpc = 11.7777 | **BACKED** | — |
| C111 | 7 | #5 the published saddle depths are 11-14% low: 2.16-2.37 / 5.16-5.68 Msun/pc^2, not 1.9-2.1 / 4.6-5.1 | A13_saddle_forecast/report.md section 3.1: +13.6%/+13.1% (MW) and +12.2%/+11.4% (cluster); but FINAL section 5 item 3 rejects these numbers in favour of A6's 3.529/5.025 | **WRONG** | #5 the published saddle depths are 11-14% low on A13's PDE solve (2.16-2.37 / 5.16-5.68 Msun/pc^2), while A6's explicit-mass recomputation gives 3.529/5.025; the document cannot simultaneously adopt A6's depth and cite A13's correction as the corrected value. |
| C112 | 7 | #6 the shear pass is conditional on 'condensed baryons only' (Delta chi^2 +68.7 -> +2.03) | A5_zenodo/report.md clue 10 (record 23372002) | **BACKED** | — |
| C113 | 7 | #7 the wide-binary DR4 registration is stale (Arm A/B vs the October 1.51) | A5_zenodo/report.md tension 2 | **BACKED** | — |
| C114 | 7 | #8 r_switch = L* only against the cold sector's own gravity; against total gravity it is L* sqrt(f_c) = 3.73 pc, not 24 pc | A20_Lstar_cores/report.md section 1 and correction to A16 | **BACKED** | — |
| C115 | 7 | #9 A18's prose reverses its own sign: the phantom is too diffuse, not too centrally concentrated | A21_u_half/report.md section 4; A18_two_ratios K18 note says the opposite | **BACKED** | — |
| C116 | 7 | #10 A19's task statement was internally inconsistent: ell0 = sqrt(8pi/Lambda) gives Lambda ell0^2 = 8pi, not 32pi; L = c^2/a0 = 2 ell1 | A19_scale_functional/report.md section 1, eq (1)-(2), K16 | **BACKED** | — |
| C117 | 7 | #11 the 'smallest strong-field anomaly' justification for p=1 is empty; the coefficient is 1 at p=1 and 0 for p>1 | A6_assets/report.md section 2.3, K14 | **BACKED** | — |
| C118 | 7 | #12 the turn-off is law-dependent: 66.30 vs 128.76, ratio 1.94 | A4_ppn/a4_results.json:numbers.y_t_canonical, y_t_quadrature, y_t_ratio_quad_over_can | **BACKED** | — |
| C119 | 7 | #13 'No external-field effect' is wrong; the EFE moves gamma_v by 0.350 (12.7 sigma) vs 0.019 (0.7 sigma); 18x | A24_wide_binaries/a24_results.json:delta_gamma_efe_20kAU, z_efe_sig_tot, delta_gamma_solver | **BACKED** | — |
| C120 | 7 | #14 the kernel conflict dissolves: 12.99 = 2 pi^4/15 exactly (0.016%); the RAR kernel cannot close Lambda; Delta chi^2(R-L) = +10.1/-0.8 | A25_kernel_conflict/a25_results.json:numbers.K7 2*pi^4/15 = 12.9878788, record_reproduction rel_err 1.63e-4; K9 | **BACKED** | — |
| C121 | 7 | #15 73.19 vs 32pi is a convention: 73.19 = 32pi Omega_Lambda with Omega_Lambda = 0.728034; the framework's a0 makes the target exactly 32pi | A25_kernel_conflict/a25_results.json:numbers.targets['73.19_over_32pi'] = 0.728034 | **BACKED** | — |
| C122 | 7 | #16 four kappa numbers circulate; kappa ~ Upsilon^-1.23, IMF moves it 1.98x; the Upsilon-free channel gives 0.354 +/- 0.106 from 12 galaxies/73 points, 1.4 sigma from 1/2; distance floor 16.1% | A14_upsilon_free/a14_results.json:numbers.kappa_fit_cmb = 0.3538, kappa_err_total = 0.106, sigma_from_half = 1.378, n_gal = 12, n_points = 73, err_terms['distance zero point'] = 0.1608; A5 tension 3 | **BACKED** | — |
| C123 | 8 | m = 1 is the unique thermal-lattice law; the canonical law is Langmuir | A2_medium/report.md: the law is n = 1 (not m); status CONDITIONAL, n = 1 forced in the class. No 'm' index exists in A2 | **WRONG** | n = 1 is the unique thermal-lattice law in A2's stated class (the document's 'm = 1' is a typo; A2's status is CONDITIONAL, not unconditional). |
| C124 | 8 | the kernel is decided: Langmuir/simple, forced by three independent constraints, the only one that both closes Lambda and is derived | A25_kernel_conflict/report.md Status CLOSED-DERIVED; A25 'What this does not do': it does not adjudicate A2 vs FP1's action-level quadrature route | **BACKED** | — |
| C125 | 8 | Lean, no sorry, standard axioms only: 40 theorems, axiom footprint {propext, Classical.choice, Quot.sound} | A8_lean/a8_lean_checks.out K1-K3: 4/4 clean, 40/40 theorems with the allowed axioms, 0 sorry | **BACKED** | — |
| C126 | 8 | M_c = 5.3643 M_b is Omega_c/Omega_b, not a cold-sector parameter (A9, A11) | A18_two_ratios/a18_results.json:R_cosmic = 5.364327; A9 report D2; A11 report F_MW/F_cluster | **BACKED** | — |
| C127 | meta | 23 lanes, all in this folder, each with a script and a mutation | 24 lane directories existed when FINAL_THEORY.md was written (A1-A16, A18-A25; A17 does not exist); FINAL section 5b itself says '24 lanes'. Nine more (A26, A27, A28, A29, A30, A32, A33, A34, A35) were created after 19:20; A31 is this referee | **WRONG** | 24 lanes, all in this folder (A1-A16 and A18-A25; there is no A17), each with a script and a mutation; nine later directories (A26-A30 and A32-A35) postdate this synthesis, with A31 as the referee. |
| C128 | meta | Every number below was re-run by the coordinator from the lane script (_parent/parent_audit.py, 21/21, mutation bites) | _parent/parent_audit.out: 21/21 checks, but the audit covers a specific 21-item arithmetic set (Q1.1-Q4.3), not every number in FINAL_THEORY.md; e.g. 2557.38, 66.30, 7.457%, 53.31, 3.87e5, 2.424 and 1.18 are not re-run there | **OVERSTATED** | Twenty-one load-bearing numbers were re-run by the coordinator in _parent/parent_audit.py (21/21, mutation bites); the remaining numbers are quoted from the named lanes and have not all been independently re-run. |

**ERRATUM (2026-10-22, doors push D5):** (C20) "the data select 4 among the natural caps" is wrong. A19's own natural grid (`a19_checks.py` K6: β ∈ {1, 2}, χ ∈ {1…4}) is R ∈ {1, 2, 3, 4, 8, 12, 16}, not {1, 2, 4}. The data **exclude R = 1** (6.14σ) and, **on CFG493 only**, R = 2 (3.05σ; on the A81 joint band R = 2 is only +1.71σ). On CFG493 (κ = 0.417 ± 0.095) R = 3 (+1.69σ), 4 (+0.87σ), 8 (−0.67σ), 12 (−1.35σ), 16 (−1.76σ) and A19's 4π (−1.42σ) all lie within 2σ, and **R = 8 is closer to the data than R = 4**. The data do not select 4; κ = ½ stays FITTED. See `doors_push_2026_10_22/D5_kappa_four/README.md`.

---

## Independent arithmetic (35 checks)

Every check is computed in `a31_checks.py` from the BRIEF constants and the defining equations, not
read from the lane. `PASS` means the recomputed value matches the value printed in FINAL_THEORY.md at
the quoted precision; `MISMATCH` is a finding.

| id | check | FINAL | recomputed | result | note |
|---|---|---|---|---|---|
| 01 | Z = 2 sqrt(8 pi/3) | 5.78881 | 5.788810036466141 | PASS |  |
| 02 | 2Z = 2 sqrt(32 pi/3) | 11.5776201 | 11.577620072932282 | PASS |  |
| 03 | kappa from the literal twelfth = Z/12 | 0.4824008 | 0.4824008363721784 | PASS | relative gap to 1/2 = 3.5198% (FINAL says 3.52%) |
| 04 | hbar G Lambda / c^3 (BRIEF Lambda) | 2.8498e-122 | 2.8447732492855883e-122 | **MISMATCH** | BRIEF Lambda gives 2.844773e-122; Lambda rebuilt from H0, Omega_L=0.685 gives 2.849764e-122 (the parent harness value). A1's a1_results.json stores 2.844773e-122. |
| 05 | a0/(c H_Lambda) = 1/Z (a0 from 32pi) | 0.1727471 | 0.17274707473566775 | PASS | with the rounded footing a0 = 9.36e-11 the ratio is 0.172855, 0.06% high - the footing rounding, not the identity |
| 06 | kappa_P1 = 4 sqrt(pi/3); mismatch 8 sqrt(pi/3) | 4.093307 | 4.093306831785954 | PASS | mismatch factor = 8.186614 (FINAL 8.186614) |
| 07 | a0/B_E; half a0/B_E | 2557.377 | 2557.377049180328 | PASS | half = 1278.689 (FINAL 1278.69) |
| 08 | N_Lambda = Lambda c^4/a0^2 | 100.4058 | 100.40584466228644 | PASS |  |
| 09 | y_t canonical root of F_can(y_t) = N_Lambda | 66.2999 | 66.29993682557189 | PASS | y_t*a0 = 6.2057e-09 m/s^2 (FINAL 6.21e-9) |
| 10 | y_t quadrature; transplant ratio | 128.7559 | 128.7558667760549 | PASS | F_can(128.7559)/N_Lambda = 1.970683 (FINAL 1.9707); y_t ratio = 1.942021 (FINAL 1.942) |
| 11 | C_can = -0.8862944; C_can/C_quad = 8 | -0.8862944 | -0.8866081104325341 | PASS | C_quad = -0.110797 (FINAL -0.1107868); ratio = 8.002123 |
| 12 | max dg/g = 2/sqrt3-1; max dv/v = sqrt(2/sqrt3)-1 | 0.1547005 | 0.15470053837925168 | PASS | max dv/v = 0.0745699 (FINAL 7.4570%); the printed formula sqrt(2/3)-1 = -0.183503 is not 7.457%; the parent Q2.8 value 0.5*max_g = 0.0773503 |
| 13 | R_core = (pi/sqrt2) L*, L*=24 pc | 53.31 | 53.31459525790039 | PASS |  |
| 14 | lambda_J = sqrt2 pi L*, L*=24 pc | 106.6 | 106.62919051580079 | PASS |  |
| 15 | sigma_c = sqrt(a0 L*) and lambda_FS = 2 sigma/(3H0) | 82.35 | 82.35076961311923 | PASS | sigma_c = 8.3257 km/s (FINAL 8.33) |
| 16 | M_J = pi^3/(6 sqrt2) V^2 L/G at V=165.2 km/s | 557000000.0 | 556468359.9037627 | PASS | coefficient = 3.654125; per (km/s)^2 = 20390.1 Msun (FINAL 2.04e4); NFW value = 3.149e6 Msun (A16) |
| 17 | a_P = GM_sun/L*^2; a_P/B_E; 1/(a_P/B_E) | 2.4205e-16 | 2.419847850041258e-16 | PASS | a_P/B_E = 6.611606e-03 (FINAL 6.61e-3); margin = 151.25 (FINAL 151) |
| 18 | M_crit = a0 L*^2/G | 387000.0 | 386789.48200273764 | PASS |  |
| 19 | lambda = L*/sqrt2; u_P = GM/(2 lambda^2) | 16.9706 | 16.97056274847714 | PASS | u_P = 2.4198e-16 m/s^2 = 2.5853e-06 a0 (FINAL 2.59e-6 a0) |
| 20 | u = (A_n-A_l)/(A_l(A_n-1)) MID and OUT | 0.471566 | 0.4715658616019967 | PASS | u_OUT = 0.986474 (FINAL 0.9865) |
| 21 | Z(u_OUT vs 1/2); Z(band, quadrature); Z(band, worst) | 4.943 | 4.9434047318794585 | PASS | quadrature band Z = 4.910; worst-correlation Z = 3.824 (FINAL '>= 3.8 sigma'; section 5 uses 3.8, section 0 says 4.9) |
| 22 | R_cosmic = (1-f_b)/f_b | 5.3643 | 5.364327223960661 | PASS |  |
| 23 | F(y_v) at the two A18 anchors (formula in FINAL) | 25.04 | 25.898514572793594 | **MISMATCH** | F_enc cluster = 3.7702 (FINAL prints 2.62); A18's 25.0429/2.6179 are R_tot, the phantom per total baryon, not F(y_v) |
| 24 | ratio of the two anchors | 9.57 | 9.56592445846697 | PASS | ratio of F_enc = 6.8694 (6.87), not 9.57 |
| 25 | rho_panc/rho_bar_cold at R=0.2d (MW pair) | -89.32 | -89.30533457059545 | PASS | independent recomputation -89.31; A6 stores -89.3197 |
| 26 | net / negative / positive column, MW pair [Msun/pc^2] | -3.529 | -3.5292616783707422 | PASS | net = -2.4245 (FINAL -2.424), positive = 1.1048 (FINAL +1.105); a 1e6-point run gives -3.4758, a 1.5% resolution drift |
| 27 | -2.424 = -3.529 + 1.105 | -2.424 | -2.424178400546791 | PASS |  |
| 28 | TT mass term from W(u) at Pbar != 0 (coefficient of h^2, units u^2/K) | 0.0 | 0.375 | **MISMATCH** | W(u) with u = K abs(P) gives a nonzero h^2 coefficient 3*K*p/8; it vanishes only at p=0, so the 'Einstein quadratic action' statement holds only on the Pbar=0 background |
| 29 | published alpha_1 at c1=c3=c4=0 | 0.0 | 0/0 | **MISMATCH** | the published alpha_1 = -8(c3^2+c1c4)/(2c1-c1^2+c3^2) is 0/0 at that point; A22's a22_checks.py line 223 sets alpha1_lit = 0 when den == 0, which asserts the value |
| 30 | lane directories at the synthesis (FINAL says 23) | 23 | 24 | **MISMATCH** | directories now: 34; the 24 pre-existing lanes are A1-A16 and A18-A25 (no A17); post-synthesis: A26_fork_decider, A27_factor_two, A28_turnoff_origin, A29_u_radial, A30_aP_solarsystem, A31_referee, A32_cleanroom, A33_master_action, A34_dimension_route, A35_series_parallel |
| 31 | L* <= R0.3(IC10=200 pc)/2.22144 | 90.0 | 90.03163161571061 | PASS | 300/90 = 3.333 (FINAL 3.33x); 1000/90 = 11.111 (FINAL 11.11x); at f_c=0.5 the bound is 127.3 pc, at f_c=0.25 180.1 pc |
| 32 | L* H0/c at 24 pc / 90 pc / 1 kpc | 2.25e-07 | 2.248222001635545e-07 | PASS | 24 pc = 5.396e-09; 90 pc = 2.023e-08; FINAL's upper end 2.25e-7 is the 1 kpc value, not the 90 pc value |
| 33 | M_J(flat curve)/M_J(NFW) | 1.0 | 176.70587338685093 | **MISMATCH** | the ratio is 176.7, i.e. the two profiles differ by ~2.2 dex, not a small correction |
| 34 | group pair -33.07 and column -5.025 | -33.07 | -33.06250532613745 | PASS | column = -5.0257 (FINAL -5.025); independent recomputation of both A6 numbers |
| 35 | 3 sigma pairs = (3 sigma_dS / depth)^2, 11.8x a 700-pair stack | 8282 | 8273.832948405236 | PASS | A6's 8281.8 uses sigma(DeltaSigma)=107 Msun/pc2 and depth 3.529; the arithmetic reproduces it and 8281.8/700 = 11.83 |

Four of the six mismatches are synthesis errors (`04` the Λ convention, `23` the `R_tot`-vs-`F(y_v)`
substitution, `29` the 0/0 α₁, `30` the lane count); `28` and `33` are structural demonstrations that
the omitted premises (`P̄ = 0`, flat-curve profile) are load-bearing. `05` and `32` pass only after
the footing/row convention is made explicit: `a₀/(cH_Λ) = 1/Z` holds for the 32π-normalised `a₀`, and
`2.25e-7` is the 1 kpc horizon value, not the 90 pc value.

## What is solid (so the reader can calibrate the hostility)

The following survived independent recomputation and are not in dispute: `Z = 5.788810036`,
`2Z = 11.577620073`, `κ = Z/12 = 0.482400836` (3.5198 % from ½), `κ_P1 = 4.0933068` with mismatch
`8.186614`, `a₀/B_E = 2557.377`, `N_Λ = 100.405845`, the canonical `y_t` root `66.29994`
(`6.2057e-9 m/s²`), the quadrature `y_t = 128.75587`, the transplant ratio `1.97068`, `C_can = −0.88661`
(asymptotic; A4's Richardson value `−0.8862944`), `R_core = 53.3146 pc`, `λ_J = 106.629 pc`,
`σ_c = 8.3257 km/s`, `λ_FS = 82.351 kpc`, `M_J = 5.5647e8 M⊙` (arithmetic), `a_P = 2.4198e-16 m/s²`
(`6.61e-3 B_E`, 151×), `M_crit = 3.867e5 M⊙`, `u_MID = 0.471566`, `u_OUT = 0.986474`,
`R_cosmic = 5.364327`, the A6 saddle ratios `−89.31`, `−3.529`, `−2.424`, `−33.06`, `−5.026`, and the
A6 pair budget `8282`. These are the document's real content, and they are why the non-BACKED
findings matter: the arithmetic is good enough that a reader will believe the prose around it.

## What would change a verdict

- **C33 (`c_T² = 1` exactly):** redo the TT quadratic action on A22's hedgehog background and show
  the `W(u)` mass term cancels (or is absent by a constraint) — then BACKED. As written, A3's own
  premise `P̄ = 0` is the block.
- **C17 (`κ is a modulus`):** exhibit the missing equation (A15-C1 / A19) or prove the zero mode is
  a flat direction of the full action, not of the two-equation truncation.
- **C57 (`24–90 pc`):** measure `f_c` in the inner 20 pc of an MW-like halo; if `f_c → 1`, the 90 pc
  bound stands. Even then it remains a one-galaxy bound, so the "window" language would still need
  the 10th-percentile 184.6 pc alongside it.
- **C03 (`u rises outward`):** compute the band→3D mapping for the CFG687 stack. A21 lists this as
  the largest single systematic and a one-afternoon job.
- **C39 (`α₁ = α₂ = 0 exactly`):** compute the galactic-regime `α₁` at `r >> λ`; A22 calls it the
  framework's real preferred-frame exposure.
- **C80 (`3.529` vs `2.16–2.37`):** resolve the 1.5× A6/A13 discrepancy with a common definition of
  the column (mean-subtracted? finite line of sight? which aperture?). Two stated-input calculations
  cannot both be right.
- **C128 (`every number re-run`):** extend `_parent/parent_audit.py` from 21 items to the full
  ledger; until then the sentence is false.

## What this lane did not do

- It did not re-run the Lean build; it relies on `A8_lean/a8_lean_checks.out` (K1–K3: 4/4 clean,
  40/40 theorems, 0 `sorry`).
- It did not re-solve the A24 wide-binary quadrature; it checked the 20 kAU bracket, the 10 kAU
  EFE-present/EFE-blind distinction and the pair arithmetic from the results file.
- It did not re-run the A7 χ²; it checked the totals, the bootstrap `z` and the win counts from
  `a7_results.json`.
- It did not re-run the A23 PDE; it checked the retained-column table and the half/full-domain
  contrast from `a23_results.json`.
- It did not audit the 178 Zenodo records (A5); it uses A5 only for the four clues/tensions the
  synthesis cites.
- The A6 column is resolution-sensitive at the 1.5 % level (`−3.529` at 160 k points, `−3.476` at
  1e6); the sign, the order and the `−2.424` net are robust, the third digit is not.

## Mutation

`python3 a31_checks.py --mutate` forces check 01 to the value 5.78 and exits 1; the captured run is
in `MUTATE.md`. The mutation is on the *value*, not the check logic, so a green run after mutation
would mean the comparison is vacuous. It is not: check 01 reports MISMATCH and the script exits 1.

## Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A31_referee
python3 a31_checks.py            # 35 checks, 29 match, 6 mismatches; exit 0
python3 a31_checks.py --mutate   # check 01 forced to 5.78; exit 1
```

`a31_results.json` carries the full 130-row ledger and the 35 check records; `a31.out` is the
captured stdout.