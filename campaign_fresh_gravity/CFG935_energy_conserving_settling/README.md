# CFG935: is there an energy-conserving form of cold-energy settling that keeps the law as the settled state?

**Bottom line: NO REPAIR (as frozen, with amendments A0–A5).**

The books can always be closed. The question is whether the law survives once they are.
- Every repair closes them: each derived energy equation books every source and sink, and the MUTATE runs show what is lost
  when the booking is switched off.
- But **no candidate that books the released settling energy inside the matter sector keeps ρ_c = ρ_ph as the end state**
  in the 1-D toy:
  - the heat, the cold energy's own motions, or the field energy pushes the halo off the law;
  - or (with one-way cooling) the halo runs away into gravothermal collapse.
- The one candidate whose books close outside matter, a dynamical dark-energy partner (R-d), needs very little exchange
  (Δρ_DE/ρ_DE ≈ 1e-6 since z = 1). But the record's own drift-plus-bath kinetics, implemented in this toy with orbits, do not
  hold the law either: D = −0.145 from the settled start. A post-hoc check with a stochastic, isotropising bath
  (PH-OU, below) does hold the law from both the settled and the infall start (D = +0.003 / +0.010; books closed to 7.9e-5 / 5.3e-4).
  So R-d's frozen failure belongs to my deterministic, trace-only bath, not to the record's kinetics. That bath is noisy,
  though: its energy partner must be a heat reservoir at the local Jeans temperature σ_J²(x). The record does not name one, and
  CFG542 requires the dark-energy partner to be coherent (zero entropy). **Read post hoc, the only working form needs new
  physics: a dynamical dark-energy partner for the drift plus a thermal reservoir for the bath.**

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled: the toy is scale-free (G = a₀ = 1), and the footing enters
only the physical tables, which are given per footing. "Cold energy" throughout; its mass is required; no particle species.
Not "theory closed". Nothing here says the data favour the framework. Framework-native inputs only.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (38f4b6f18).
- **Amendments:**
  - A0 `AMENDMENT_A0_pre_result.md` (e9a824153, pre-result): run lengths; "f_min" is really f_esc,max.
  - A1 `AMENDMENT_A1_s2_discretisation.md` (679994050): S2 midpoint-in-mass shells.
  - A2 `AMENDMENT_A2_softening.md` (407e7054b): N-type kernels softened; post-result for R-d.
  - A3–A5 and the post-hoc parts: below (dated 2026-10-20/21, this README).
- **Derivation:** `DERIVATION.md`.
- **Script:** `cfg935.py` with parts, run by `run_935.sh`.
  - Main: `cfg935.out`, `cfg935_results.json`, `parts/*.json`.
  - MUTATE: `cfg935_MUTATE.out`, `cfg935_results_MUTATE.json`. It exits 1 as designed: all three teeth bite.
  - Every run used one core, nice 10 and < 120 MB. Nothing was downloaded and no other lane was touched.

## The toy

1-D spherical shells (N = 10000).
- Units G = a₀ = 1; static Plummer baryons M_b = 1, a = 1.
- Simple law g_N = g²/(g + a₀); settled edge r_* = 10, so M_c = M_ph(<10) = 9.4453.
- Catchment R_C = 30; α = 1.
- Starts: IC-L, the settled law (N-type: isotropic Jeans Maxwellian; S2: cold static); IC-I, a cold uniform sphere of radius
  15 (infall / deficit fill); IC-S, a cold ×1.5 surplus core.
- Law gate (the record's CFG544 density part): D = the median over 16 bins in r = 1–9 of log10(ρ̄_c/ρ_ph). ON THE LAW iff
  |D| ≤ 0.1 and |ΔD| ≤ 0.05 between windows.
- Also reported: X_m = max |log10 m̄(<r)/M_ph(<r)| at r = 2, 5, 8 (the rotation-curve scale), and f_esc = the fraction beyond R_C.

## Controls

| control | result |
|---|---|
| **K0** | CFG932's drift test, reproduced through a copy of its routine: ΔW/\|W₀\| = 0.5926642444000018, identity 1.8633e-3, both **exact**. **PASS** |
| **K0b** | The same run with exact discrete-gradient bookkeeping (the partner takes Σ dm(Φ̄_{i+1} − Φ̄_i), Φ̄ the step-mean potential) closes W + E_X to **5.0e-16 \|W₀\|**; the record's explicit accounting leaves 1.10e-3 \|W₀\|. **PASS** |
| **K1** | S2 discrete static law (A1): force residual 1.5e-15. **PASS** (the IC-L gates are criterion (b)) |
| **K2** | Pure N-type Vlasov on IC-I: ε_E = 6.5e-5 at t = 200 with the A2 kernels (1.5e-4 with the frozen kernels). **PASS** |
| **MUTATE** | M1 R-d with the partner booking off: ε_E 0.63. M2 R-b with the heat booking off: 3.8. M3 S2 with the tether energy left out: 0.14. **All bite; exit 1** |

## The energy theorem (DERIVATION §4, §7), in the toy's discretisation

Excess = E_init − E_law(M_c), as a fraction of |E_law(M_c)|. f_esc,max is the largest escaped fraction compatible with a law
remnant (zero-energy escapers; A0.2).

| start | N-type (Jeans-supported law, −5.382) | S2 (cold ground state, −1.888) | R-a(i) λ = 10 |
|---|---|---|---|
| IC-L | −0.012 (sampling) | 0 (exact) | −0.004 |
| IC-I (infall) | **+0.165**, f_esc,max 0.18 | **+0.532**, f_esc,max 0.81 | +1.76, f_esc,max 0.49 |
| IC-S (cold surplus) | **−1.60: energy deficit**, so the law is unreachable without an input | +0.271, f_esc,max 0.56 | −0.155 (deficit) |

- An infall start carries more energy than the settled law. It must lose 16.5% (N-type) or 53% (S2) of the law's binding
  energy, or keep it as motions that are not the law.
- A cold surplus start carries less energy than the Jeans-supported law, so it must gain energy (R-d's partner supplies it).
- The S2 law is the strict minimum of V_S2 at fixed mass (pointwise convexity, §3.2), so every S2 start has an excess.

## Runs (A1/A2 code; windows W1/W2 = [0.5, 0.75] and [0.75, 1] of t_end, or of the reached time if capped, A5)

| run | ε_E | D(W2) | ON THE LAW | X_m | f_esc | notes |
|---|---|---|---|---|---|---|
| Ra1_L (λF, λ 10) | 5.7e-6 | +0.012 | **yes** | 0.011 | 0 | baryon reaction already 0.45 g_law (from a 2.5% offset × λ ∂M_ph/∂M_b) |
| Ra1_I | 2.7e-5 | −0.216 | no | 0.232 | 0.214 | hot remnant (X = 4.6); baryon reaction 0.12 / 4.9 / 13 g_law at r = 2 / 5 / 8 |
| Ra1_S | 8.3e-6 | +0.051 | (yes) | 0.067 | 0.004 | baryon reaction 0.83 / 2.3 / 0.84 g_law |
| Ra1x100_I (λ 100) | 7.2e-5 | −0.126 | no | 0.219 | 0.345 | capped at t = 362 (A5); X = 24; baryon reaction 0.67 / 38 / 125 g_law (×10 the λ 10 run) |
| Ra2_L (S2) | 0 | +0.000 | **yes** | 0.000 | 0 | exact static ground state |
| Ra2_I | 1.6e-3 | −0.271 | no | 0.334 | **0.406** | inner bins −0.06 dex (r ≈ 1), outer −0.65 dex (r ≈ 8.5); warm remnant |
| Ra2_S | 6.1e-3 | −0.155 | no | 0.218 | 0.234 | surplus expelled, overshoots to a deficit (as CFG776) |
| Rb_L (one-sided + heat) | 2.4e-5 | −0.102 | no | 0.107 | 0 | heat booked 58.8 (\|E\| = 5.4): circulation |
| Rb_I | 2.6e-4 | −0.355 | no | 0.597 | 0 | heat booked 346.5; ragged profile |
| Rb_S | unmeasured | — | — | — | — | stopped by hand before t = 50 (A4) |
| Rc_L (one-sided + heat + cooling) | 1.6e-3 | −0.017 | (gate yes) | **0.311** | 0 | capped at t = 43.6 (A5); E_rad 12.9; 1372 shells inside r < 0.1 against 2.8 for the law: **central collapse** |
| Rc_I | 7.7e-2 | −0.170 | no | 0.749 | 0 | capped at t = 14.9; E_rad 99.0 (18 \|E_law\|); m(<2) = 7.70 of 9.45: **runaway collapse** |
| Rc_S | 1.2e-3 | — | — | — | — | A3 stop at t = 5; collapsing (1643 shells inside 0.1) |
| Rd_L (FIX-1 + FIX-2 + E_DE) | 2.2e-5 | −0.145 | no | 0.268 | 0 | E_DE −2.48 (drift +2.68 net to partner, bath −5.16 net from it) |
| Rd_I | 3.4e-4 | −0.215 | no | 0.467 | 0 | E_DE −3.33; reaches about the law at t ≈ 50, then puffs up |
| Rd_S | 1.8e-3 | — | — | — | — | stopped by hand at t ≈ 100–150 (A3) |

## Classes (FROZEN_CRITERIA §4)

| repair | (a) conserves | (b) IC-L on the law | (c) IC-I on the law + baryons | class | why |
|---|---|---|---|---|---|
| **R-a(i)** Hamiltonian FIX-1 (λF) | yes (≤ 7.2e-5) | yes | **no** (D −0.216; baryon reaction 13 g_law, 125 at λ 100) | **NOT VIABLE** | heat ∝ λ; the reaction on baryons grows with λ; needs a new constant and a +F mediator |
| **R-a(ii)** canonical S2 tether | **no** numerically (1.6e-3, 6.1e-3: near-barrier integration; the S2 action conserves exactly) | yes (exact) | **no** (D −0.271; 41% unbound) | **NOT VIABLE** | the excess (53% of \|V_min\|) is shed only by unbinding supply; the warm remnant falls below the law |
| **R-b** one-sided + booked heat | yes (≤ 2.6e-4; IC-S unmeasured) | **no** (−0.102) | **no** (−0.355) | **NOT VIABLE** | the one-sided drift rectifies orbital fluctuations into a heat-driven circulation |
| **R-c** radiation channel | **no** (1.6e-3, 7.7e-2, 1.2e-3) | gate yes (−0.017), but the centre collapses | **no** (−0.170; runaway collapse) | **NOT VIABLE** | one-way cooling to a local virial target is a gravothermal runaway; also needs a new gapless field (P is gapped) |
| **R-d** dark-energy partner (record dynamics, books closed) | **no** (Rd_S 1.8e-3) | **no** (−0.145) | **no** (−0.215) | **NOT VIABLE** as frozen | books exact, but the frozen deterministic bath does not hold the law; post hoc, the isotropising bath does (below) |

**Overall: NO REPAIR (frozen rule, amendments A0–A5). Post-hoc reading (no verdict weight): REPAIR NEEDS NEW PHYSICS, via R-d with the record's isotropising bath, whose books need a dynamical dark-energy partner and a thermal reservoir.**

## Physical tables (both footings; CFG932 central corner EPS 0.05, L = 1; CFG630 brackets)

Excess energy that each system's settling must dispose of: E_x = −ΔE_a,tot (primordial NFW debris → Jeans-supported law,
whole catchment).

| system | E_x can (erg) | E_x alt (erg) | E_x/(M_cat\|Φ(r_*)\|) can / alt | E_x/(M_cat c²) can / alt |
|---|---|---|---|---|
| UFD-c | 1.63e49 | 1.78e49 | 0.396 / 0.393 | 3.4e-11 / 3.7e-11 |
| UFD-e | 1.60e50 | 1.71e50 | 0.311 / 0.310 | 5.6e-11 / 5.9e-11 |
| Draco-like | 1.57e52 | 1.73e52 | 0.376 / 0.378 | 3.3e-10 / 3.6e-10 |
| Fornax-like | 1.06e55 | 1.20e55 | 0.351 / 0.361 | 2.8e-9 / 3.1e-9 |
| SPARC-like dwarf | 2.82e56 | 3.24e56 | 0.302 / 0.317 | 7.5e-9 / 8.6e-9 |
| MW-like | 2.38e59 | 3.26e59 | 0.136 / 0.169 | 4.1e-8 / 5.7e-8 |
| cluster core | 7.34e63 | 9.15e63 | 0.145 / 0.164 | 3.0e-6 / 3.7e-6 |

- **Matter-sector repairs (R-a, R-b).** If the excess stays in the cold energy and the remnant is to be the law, an
  escape-from-the-edge estimate (the zero-energy-escaper, upper-type figure of A0.2) unbinds **14–40% of each catchment** on
  both footings. The toy's S2 infall unbound 41%.
- **R-d (dark-energy partner).** CFG630's settling trickle is Δρ_DE/ρ_DE = 0.80–1.10e-6 (can) / 0.92–1.25e-6 (alt) since z = 1,
  shifting a₀ by 1.7–2.4e-7 / 2.0–2.7e-7 dex through a₀ ∝ √ρ_DE. CFG689 (LEDGER) did not reject constant dark energy (1.97σ;
  native a₀(z = 1)/a₀(0) = 0.91 [0.76, 1.03]). The exchange R-d needs is four to five orders of magnitude below that resolution:
  allowed, and unmeasurable. It needs ρ_DE to be dynamical (exact Λ cannot exchange), and a canonical partner is singular at
  w = −1.
- **R-c (radiation).** Exporting the same energy into a new massless field gives Ω_rad,new ≤ 5.5–7.5e-7 (can) / 6.3–8.5e-7
  (alt), 1.0–1.4% / 1.2–1.6% of the CMB photons'. The record's own field P is gapped (CFG760–762), so this would be a new field.

## What it means for "the law is the settled state"

1. **The settled law survives as a near-stationary state under R-a(i), R-a(ii) (exactly, as its ground state) and R-c (in
   r = 1–9).** R-b (D −0.102) and frozen R-d (−0.145) move off it.
   - **No repair that keeps the released energy in matter brings an infall start onto the law** (Ra1_I −0.216, Ra2_I −0.271,
     Rb_I −0.355, Rc_I collapse).
   - Only the post-hoc R-d with the isotropising bath does (+0.010), by sending the energy out of matter.
2. **Settling releases energy, and the release is the problem.**
   - From an infall start, the law sits 16.5% (N-type) to 53% (S2) of its binding energy below the start.
   - Booked as cold-energy heat or motion, that energy keeps the halo off the law:
     - S2: a warm tethered halo falls short by δm/m ≈ −σ²|dln p/dln r|/(2V_N²) (DERIVATION §3.2), and 41% of the supply is
       unbound;
     - λF: the heat scales with λ, and the reaction on the baryons reaches 13 g_law;
     - one-sided: the drift rectifies orbital fluctuations into a heat-driven circulation (59–347 energy units booked).
   - Exported one way (R-c), it runs away into gravothermal collapse.
3. **The record's settled state needs an energy sink outside matter.** "The law is the settled state" holds in the record only
   because its drift dumps the released energy into an unbooked sink (CFG932). Close that sink inside matter and the statement
   fails. Close it with a dynamical dark-energy partner and the books balance at a level no observation can see (≈1e-6).
   - As frozen (deterministic bath), the record's drift-plus-bath kinetics with orbits did not hold the law even with exact
     books.
   - Post hoc, with FIX-2's isotropising stochastic bath, they do (PH-OU).
   - The price is two new reservoirs: a dynamical dark-energy field for the drift, and a heat bath at the local Jeans
     temperature for the bath's noise.
   - So the settled law is kept only by new physics outside the matter sector, not by a repair of the equations inside it.
4. **The canonical S2 dynamics (THEORY_CANONICAL S2/S3) conserves energy and has the law as its unique ground state.** A real
   halo reaches the ground state only to the extent that it sheds the infall energy. In the toy that took 41% of the supply,
   and the warm remnant sits −0.06 dex at r ≈ 1 but −0.65 dex at r ≈ 8.5. The law in rotators needs tethered cold energy much
   colder than V_N² (the baryons' own Newtonian circular speed squared), and nothing in S2 supplies that cooling.

## Post hoc (no verdict weight; dated 2026-10-21)

- **P0_L (control: pure N-type Vlasov on IC-L, no settling term):** ε_E 9.4e-7; D +0.048, ON THE LAW; X_m 0.074; f_esc 0.025.
  The settled start is close to steady by itself. Criterion (b) therefore tests mainly whether a repair *destroys* a settled
  galaxy: R-b and frozen R-d do; R-a(i), R-a(ii) and R-c (inside r = 1–9) do not.
- **PH-OU (R-d with a per-shell stochastic Ornstein–Uhlenbeck bath on all three velocity components, FIX-2's isotropising
  form; drift and books as R-d):**

  | run | ε_E | D(W2) | ΔD | ON THE LAW | X_m | m(<2, 5, 8) | E_DE (net) |
  |---|---|---|---|---|---|---|---|
  | PHou_L | 7.9e-5 | +0.003 | −0.001 | yes | 0.092 | 1.69, 4.61, 6.71 | −0.35 |
  | PHou_I | 5.3e-4 | +0.010 | +0.009 | yes | 0.103 | 1.74, 4.70, 6.81 | +0.56 |

  - With the record's own bath form, R-d keeps the law from both starts and fills deficits on infall, with exact books. The
    frozen R-d failure (D −0.145 / −0.215) is my deterministic bath, which rescales the dispersion trace and keeps the
    anisotropy that the drift and infall build up. It is not the record's kinetics.
  - The cost is two reservoirs, not one:
    - (i) the drift's work Q = −ρ_c v_s·∇Φ goes to a dynamical dark-energy partner (exact Λ cannot take it; a canonical partner
      is singular at w = −1);
    - (ii) the bath exchanges energy both ways at a large gross rate (PHou_L: 228 in / 240 out over t = 350, net 11.7), as a heat
      bath at the local temperature σ_J²(x).
  - CFG542 Pb requires the dark-energy partner to be coherent (zero entropy), and a thermal partner shifts the stationary state
    (CFG542 M3). CFG544 found no named partner for P_bath. So reservoir (ii) is a second new ingredient, and a position-dependent
    temperature has no single thermodynamic owner.
  - Net exchange is small: on infall the partner kept +0.56 of the toy's 0.89 excess.
  - IC-S was not run with this bath, so (a) on IC-S is open.
- **Pre-A2 records (frozen thin-shell kernels):** Rd_L D −0.151 (NOT ON THE LAW, ε_E 6.2e-4); Rd_I the same puffed state, with
  integration bursts to 4.0e-3.

## Amendments and disclosures (the frozen text is not edited)

1. **A0 (pre-result, e9a824153).** t_end scaled to each gravity type's edge period (N-type 650 / 350, S2 2000 / 1000). The
   frozen "f_min" is the largest escaped fraction compatible with a law remnant (zero-energy escapers) and is reported as
   f_esc,max.
2. **Numerical knobs (set on K2 only).** Reflecting inner boundary r_min 0.05 → 1e-3: at 0.05 the reflections pumped energy
   (K2 ε_E 8.9e-3). Also CA 0.03, DTMAX 0.02, CS 0.05, checked to t = 650 (2.1e-4).
3. **A1 (679994050).** The frozen S2 step rule had a finite thin-shell barrier. The first S2 runs (MUTATE M3, Ra2_I, Ra2_S)
   reached u = a₀ and returned NaN; they are kept as `parts/preA1_*` and `parts/preA1A2_MUTATE_*`. Replaced by the midpoint-in-mass
   rule (same continuum functional, infinite barrier), plus a step limit of 10% of the gap to each shell's barrier. The first ETH
   part crashed on a `brentq` tolerance; the runner's logged rc was wrong ($(date) resets $?; fixed).
4. **A2 (407e7054b; post-result for R-d).** The frozen N-type thin-shell kernels let a shell whose L the bath had scaled to zero
   fall into the singular self-energy. Frozen Rd_I's energy then failed in bursts (1.6e-3 at t = 400, 4.0e-3 at t = 550).
   - All N-type 1/r² kernels are softened with ε = 0.02.
   - Frozen-code records: `parts/preA2_Rd_L.json` (D −0.151, NOT ON THE LAW, ε_E 6.2e-4) and `parts/preA2_Rd_I.json`
     (progress lines; the same puffed state).
   - The A2 R-d results reproduce the frozen-code failure (D −0.145 / −0.215).
5. **A3 (post-result, compute only).** An IC-S run stops once its running ε_E exceeds 1e-3; (a) has then failed for good.
6. **A4 / A5 (post-result, compute only).** IC-S runs are capped at 30 min of wall clock, the others at 45 min. A capped run is
   scored on windows relative to the time reached and labelled (Rc_L at t = 43.6, Rc_I at t = 14.9, Ra1x100_I at t = 362). Both R-c runs
   were collapsing when capped.
7. **Own processes stopped by hand** (by verified PID; no other process touched): frozen-code Rd_I (stalled after its energy
   bursts), A2 Rd_S (ε_E 1.8e-3 at t = 100, (a) already failed), A2 Rb_S (32 min without reaching t = 50; R-b already failed (b)
   and (c)), and the first A2 Rc_L (stalled in collapse; rerun under A5). Their records are the part JSONs and progress lines
   named above.
8. **Frozen-gate caveat.** Rc_L passes the frozen density gate (D = −0.017 over r = 1–9) while its centre collapses (+2.7 dex
   inside r = 0.1; m(<2) doubled, X_m 0.31). R-c fails (a) anyway. The frozen D measure cannot see a collapse inside r = 1;
   X_m and the core count are reported for that reason.
9. **Bath form.** The frozen R-d / R-c bath rescales each bin's 3-D dispersion deterministically, keeping its anisotropy. The
   record's FIX-2 relaxes the full pressure tensor (isotropising). The PH-OU parts test this.
10. **Logs.** `parts/run_935*.log` contain local paths in tracebacks and are not committed. Every quoted number is in a JSON.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A0_pre_result.md`, `AMENDMENT_A1_s2_discretisation.md`, `AMENDMENT_A2_softening.md`,
`DERIVATION.md`, `cfg935.py`, `run_935.sh`, `cfg935.out`, `cfg935_results.json`, `cfg935_MUTATE.out`,
`cfg935_results_MUTATE.json`, `parts/*.json` (including the pre-A1/pre-A2 records).

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
