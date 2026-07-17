# VERIFY — kernel-argument workflow (independent adversarial re-derivation)

**Date:** 2026-07-17. **Verifier scripts (all exit 0):**
`kernel_argument.py` (banked, re-run), `growth_derived.py` (banked, re-run), and
**`verify_independent.py` (NEW, 22/22 checks, nothing imported from the banked script —
every load-bearing object rebuilt from the action)**, out `verify_independent.out`.
Both a₀ footings throughout: canonical ρ_DE **9.36×10⁻¹¹**, alt ρ_tot/cH₀ **1.13×10⁻¹⁰**;
Z = √(32π/3) = 5.78881 (geometric, footing-independent), cH_Λ = Z·a₀ = 5.789 a₀.

## Re-run status

Both banked scripts reproduce their reported numbers exactly, exit 0:
- `kernel_argument.py`: all checks PASS.
- `growth_derived.py`: BARE σ₈ = 6.90/8.00 (canon/alt); FLOOR_const_allz = 1.02/1.02;
  FLOOR_const_gate (r_gate=3) = 4.84/5.56; FLOOR_rise = 0.83/0.83. Matches the feed.

## The six questions, adjudicated independently

**(1) Is the horizon floor GENUINELY the dS-Unruh pole, or smuggled to fix σ₈?**
Split into value vs application:
- **The floor VALUE is genuine, not smuggled.** I re-derived the first-moment identity
  `u·□_u u = −|a|²` from scratch on a general flat worldline (algebraic identity
  `u·jerk + |a|² − d/dτ(u·a) = 0`, on-shell `u·a=0`), so the RAR-producing reduction gives the
  **bare** `|a|²/a₀²`. Separately I re-derived the dS-Unruh pole from the static-patch
  **embedding**: `κ_eff² = H² + a_proper²` exactly (Pythagorean), giving in argument units
  `X_pole = Z² + (|a|/a₀)² = 33.50 + (|a|/a₀)²`. The floor Z² **is** `(cH_Λ/a₀)²` — the same
  horizon scale that *defines* a₀ (a₀ := cH_Λ/Z). It is not a number fitted to σ₈.
- **But its cosmological APPLICATION is not derived** (see #4). The first moment — the SAME
  closure that yields the galactic RAR — floors **neither** case: on FLRW the comoving element
  is a geodesic (`|a|²=0`, re-derived symbolically) and a peculiar-velocity element has
  `|a|² = H²γ²V²` (Hubble drag, re-derived), numerically H₀V ≈ 0.006–0.007 a₀, **~800–960× below**
  the cH_Λ floor. So the σ₈-curing floor requires the growing mode to couple to the **pole**, not
  the first moment — a coupling the pullback provably does **not** pin (PULLBACK PB-D4).

**(2) HARD CONSTRAINT — is the galactic deep-MOND RAR preserved (0.01–1 a₀ reached, not floored)?**
Yes under the bare first moment; broken under the floor. Mapped the deep-MOND band independently:
`ν_bare(y=0.01)=100`, `ν_bare(0.1)=10` (RAR preserved), whereas `ν_floored = 1/K(Z²+y²) ≈ 1.09`
at **every** y (kills the boost ×92 at y=0.01, ×9 at y=0.1). **A cH_Λ floor applied to galaxies
destroys deep-MOND.** The prescription is self-consistent only because the floor is never applied
to the fast bound orbits. Both footings identical (Z cancels a₀). This is the manufactured-save
tripwire, and it does **not** fire: the derived galactic prescription is bare, so the RAR survives.

**(3) Is the local-vs-cosmological split real, or hand-waved?** Real, computed non-arbitrarily.
The de Sitter tide on a star is `a_tidal = H_Λ² r`; for a flat rotation curve `g_obs = V²/r`, so
`tide/g_obs = (r/r_eq)²` with `r_eq = V_flat/H_Λ = 2.7–3.2 Mpc`. Within a galaxy: **9.6×10⁻⁶ at
10 kpc, ~1×10⁻³ at the 100 kpc HI edge** — a few 0.1% at the very outermost radius, negligible
against the ~10× deep-MOND boost. r_eq (~3 Mpc) is 27–32× the HI edge → the galaxy fits in one
local inertial frame and the equivalence principle removes H cleanly. **Correction surfaced by my
independent check:** the banked `kernel_argument.py` §3 sampled only y=0.1 and reported tide/orbit
~1e-4; the deepest edge (y~0.01 / 100 kpc) is ~10× closer to the tide (~1e-3). Still far from
breaking the RAR, but the "1e-4 clean" claim is edge-optimistic — honest value is **≲1e-3 at the
galaxy edge**. Split stands.

**(4) Is the dS-worldline pole legitimately applied to an FLRW growing mode? — THE CRUX WEAKNESS.**
**No, not across cosmic history.** The pole uses the de Sitter **event-horizon** rate H_Λ (constant);
the growing mode lives on FLRW where H = H(z) is time-dependent and the background is
**matter-dominated** at the epochs where most σ₈ growth accrues. Computed H(z)/H_Λ:
1.21 (z=0, Λ-dominated, dS-like — transplant defensible), 1.60 (z=0.5), 2.16 (z=1), 5.52 (z=3)
— matter-dominated, **NOT** de Sitter. There the mode's own rate ω~H(z) ≫ H_Λ is *fast* relative
to the dS memory, so by the framework's own frequency argument it takes the **first moment (bare)**,
not the pole. **Consequence:** the σ₈≈1.02 cure comes *only* from `FLOOR_const_allz` — applying the
z≈0 dS pole at **all** z, which is exactly where the transplant is illegitimate. The
frequency-honest gated fork (floor only where H(z)~H_Λ) **still overshoots** (σ₈ = 4.84/5.56,
3.8–7.3× Planck across the entire free r_gate gap) because the high-z runaway is bare and the
late-time floor cannot undo it. The rising c·H(z) floor is always-on but equals cH₀E(z), switching
MI off (ν→1) → σ₈ = 0.83, **LCDM-degenerate** (V35=350 vs LCDM 333, no lift toward Qin).

**(5) Both footings:** carried everywhere; agree to ≤15% on σ₈ and ≤30% on V; the floor value
Z²=33.50 and the split are footing-independent (Z is geometric).

**(6) Manufactured save AND manufactured kill — both hunted, neither found.**
- **No manufactured kill:** the BARE overshoot uses the identical first-moment closure that yields
  the galactic RAR; ν_bare at the cosmo element = ν(0.009–0.011) = 9.6–10.6 is the honest
  deep-MOND value, not inflated. The DEAD reading is faithful.
- **No manufactured save:** the σ₈-curing floor value (ν(Z)=1.083) is the *same* cH_Λ the EP removes
  locally — not an independent fitted number — so it is physically motivated, not a blunt fudge.
  **But** it is also not *derived* cosmologically (#4): it borrows a late-time dS result for the
  whole matter era. So the save is neither manufactured nor forced.

## Verdict

**BRACKETED — DEAD on the faithful fork, LCDM-DEGENERATE on the other; the attractive banked middle
(σ₈≈1.02 with bulk flows lifted toward Qin) is NOT reproduced by the derived prescription.** The
derivation is honest both ways: the horizon floor is a genuine dS-Unruh object (its value re-derived
from the embedding, = the scale that defines a₀), the galactic deep-MOND RAR is preserved in every
case (the floor is never applied to fast bound orbits — no manufactured save), and the BARE overshoot
is the faithful galactic-consistent reading (no manufactured kill). The whole cosmological verdict
turns on whether the FLRW growing mode couples to the pole or the first moment — a coupling the
pullback provably does not pin (PB-D4) **and** that #4 shows is background-illegitimate at the
z>0.7 matter-dominated epochs where growth accrues. Under the derived prescription:
- **BARE first-moment** (same closure as the RAR): σ₈ = 6.90/8.00 (8.5–9.9× Planck), V ~10–17× Qin →
  **DEAD overshoot** (the classic Nusser-2002 MOND-structure runaway inside this kernel).
- **Constant cH_Λ floor, frequency-gated** (the faithful constant-H_Λ reading): σ₈ = 4.84/5.56, still
  3.8–7.3× Planck for every r_gate → **DEAD** (high-z bare runaway un-undoable).
- **Rising c·H(z) floor**: σ₈ = 0.83, V35 = 350 → **VIABLE but LCDM-degenerate** (MI switched off).

The σ₈≈1.02 "cure" of the banked `mi_linear_cosmology` came exclusively from `FLOOR_const_allz`,
which the frequency argument (DERIVATION §4) and the background check (#4 here) both say is **not**
what the derived prescription gives. No 'proves' / 'closed' / TOE claim. a₀'s value and s=−1 remain
postulates.

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_kernel_argument && python3 kernel_argument.py && python3 growth_derived.py && python3 verify_independent.py` (all exit 0). Sources read (frozen read-only repo + local prep): `mi_field_theory/{BASELINE_ACTION,MATTER_COUPLING}.md` + `rederive_identity.py`, `mi_closure_pin/PULLBACK.md`, `mi_fingerprint/KERNEL_THEORY.md`, `mi_linear_cosmology/RESULT.md`.
