# CFG781 FROZEN CRITERIA: phase-mixed free cold energy (Argon's rule). Free core mass = (Ω_c/Ω_b) × hot-gas mass

Committed alone, before any script or number. 2026-10-14. Block CFG780–789.

## Origin and record check
- Proposed by an external agent ("Argon"), relayed by the owner.
- Claude's chat review, before freezing:
  - The kernel (the tether acts only on the coherent displacement, so phase-mixed carrier is untethered) is sound only as a
    TWO-POPULATION postulate. CFG723's identity ∇·P = ρ − ρ̄ forbids a concentrated core with zero P in a single medium.
  - Hot gas cannot randomise a collisionless carrier by shocks; violent relaxation could.
  - UFDs have no hot gas, so this rule predicts no UFD fix.
- What is tested is the rule's sharp amount: **M_free = 5.364 × M_hot**, untethered and collisionless, alongside a tethered
  population on the condensed baryons.
- Seen before freezing: the CFG721/726/776 results, the eRASS1 core excess (CFG687), the KiDS early-type +0.280 ± 0.083
  (CFG669), and astra's warm-tether witnesses.

## Model (declared; no new constant)
- **Tethered population.**
  - Supply S_t = 5.364 × M_cond/0.10 (CFG652's progenitor-containment catchment for condensed baryons).
  - Profile = the law's phantom of the condensed baryons (kernel ν), cumulative m_t(r) = min(phantom_cond(<r), S_t),
    held constant beyond the supply edge, out to r_ta.
- **Free population.**
  - M_free = 5.364 × M_hot,tot (hot gas within the declared gas truncation, 2 R_X for clusters/groups; the declared halo for
    early types).
  - Placement: CFG637 Method B (`maxent_reservoir`, lowered isothermal, self-consistent with its own gravity) in the
    potential of baryons + tethered + free.
  - Energy target: E = −G (M_b + S_t + M_free)/r_ta × M_free, i.e. the free mass at rest at turnaround (cold collisionless
    infall conserves energy).
  - r_ta from `cfg637_lib.r_ta_single(M_ta, a_obs)` with M_ta = catchment/f_b.
- **Baryon placement:** as CFG652/CFG721 (half BCG Hernquist R_e = 15 kpc, half members Hernquist R_e = 0.5 R_X; hot gas as
  the CFG652/686/687 harness profiles).
- **Kernels:** ν_s (primary) and ν_mono. Both footings, never pooled.

## Targets and pass rules (CFG721/777 harness scoring, unchanged)
1. eRASS1 318: MID and OUTER band A within 2σ of 1.
2. ACCEPT 8: OUTER within 2σ.
3. eFEDS 131: χ² p ≥ 0.01.
4. KiDS early − late at matched baryonic mass (CFG721 T-K construction): early types carry a hot halo M_hot = h·M_b.
   - Primary h = 1 (CFG721's T-K construction).
   - Bracket h ∈ {0.25, 0.5, 2} (reported).
   - Late types h = 0.
   - Pass: within 2σ of +0.280 ± 0.083.
5. MW UFDs: M_hot = 0, so the rule predicts no change. Declared expected FAIL of the UFD problem (reported, not scored).
6. SPARC guard: discs M_hot = 0 ⇒ M_free = 0. Reported; the tethered construction must reproduce the law within supply
   (check at log M_b 9–11).

**Verdict:** PASS if 1–4 pass on at least one footing (ν_s); PARTIAL if 1–3 pass but 4 fails, or 4 passes but any of 1–3
fails; FAIL otherwise.

## Controls / MUTATE
- K1: M_hot = 0 ⇒ M_free = 0 and the model reduces to the tethered law within supply. Every disc case changes by ≤ 1e-6.
- K2: Method B returns a converged solution (flag True) for ≥ 95% of systems; failures are reported.
- **MUTATE M1:** M_free = 0 everywhere. The model must reproduce the condensed-source law with a supply cut, and the
  eRASS1 MID band must change from the primary by ≥ 0.1.
- **MUTATE M2:** M_free placed uniformly (∝ r³) inside r_ta instead of by Method B. The KiDS and eRASS1 MID predictions must
  change, i.e. placement matters.

## Hand estimate (before any script)
- Clusters: M_free ≈ 5.4 M_gas, comparable to CFG721 all-source overflow amounts. Concentrated by Method B, it likely
  overshoots the inner bands. Expected eRASS1 MID near or above the data.
- Early types (h = 1): M_free ≈ 5.4 M_b. Even partly inside 100 kpc it gives ≥ +0.3 dex, so a possible overshoot.
- **Expected: FAIL or PARTIAL by overshoot.**

## Machine
Run ONLY after the relaunched T1x has finished and been scored, serially after CFG780 and CFG777. 1 process, < 1.5 GB.

κ fitted; cold energy mass required; not theory closed.
