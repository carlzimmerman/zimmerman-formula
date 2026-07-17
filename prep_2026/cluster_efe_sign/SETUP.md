# SETUP / DIAGNOSIS — Cluster-member EFE sigma-spread SIGN reconciliation

**Lane:** setup/diagnosis. **Date:** 2026-07-17. **Script:** `setup_diagnose.py` (exit 0, numpy/sympy, both footings).
**Frozen repo read-only; outputs only here.** Framework = de Sitter–Unruh **modified INERTIA**,
a0 = cH_Λ/Z = 9.36e-11, g_obs = √(g_bar²+g_bar·a0), own ν = √(1+1/y). Milgrom 1983/1999 (PLA 253:273)
wellhead credit for the ν-kernel; Milgrom 2022 (PRD 106 064060) for the two-frequency EFE θ(y).
**a0 value + s=−1 are POSTULATES; MG=0 at fixed true field is the sole theorem-grade claim. No "proves".**

## The contradiction (as posed)
- **GAP_STATEMENT.md E4/E7** (`sigma_spread/`): sign **NEGATIVE** — "plungers less boosted", first-infall
  DEFICIT (cooler). E7 kill-condition: a significantly **POSITIVE** sign *falsifies* θ-decreasing.
- **predict.py** (`cluster_efe_channel/`): baseline **POSITIVE** — "plungers HOTTER"; **PLUS** a dated
  pericentre **sign-flip** (pre-peri DEFICIT / post-peri EXCESS), τ_M ≈ 0.45 Gyr.
- **D3** (`reviews/residual_doors_2026_07/D3_amplitude_vs_settledness.py`, DOI 10.5281/zenodo.21179352)
  pre-registers the *same* flip (post-peri EXCESS(+), first-infall/pre-peri DEFICIT(−)), τ_mem ≈ 0.45 Gyr.

## Divergence diagnosis — it is NOT a numeric clash
Both banked calcs use the **same** boost `B = 1/μ_fw(A/a0)`, `A = a_in + a_ex·θ(y)`, θ decreasing. Running it:
`σ_ratio` **rises** 1.060 (y=0.05, settled) → 1.174 (y=1.5, plunger). **The code says plungers are HOTTER.**

1. **GAP E4/E7 negative = a TEXT-LABEL BUG.** The script GAP cites
   (`rederive_spread_and_power.py`) *prints* "SIGN robust: plungers less boosted" while its own boost
   loop outputs plungers hotter. The error: conflating "plunger has LOW θ" with "plunger has LOW boost".
   In EFE physics **low θ = less external loading = less suppression = MORE boost**. GAP's sign is
   inverted at the text level, and **E7's kill-condition is backwards** — a significantly positive sign is
   the framework's OWN correct prediction, so E7 would *self-trip* the framework. (The verify lane's
   "weak-memory population self-trips E7" is this same inversion surfacing.)
2. **predict.py's BASELINE ("plungers HOTTER") is CORRECT** and matches the code and
   `rederive_mi_spread.py`'s synthesis. The banked calc that was **right on sign = predict.py baseline**.
3. **predict.py / D3 pericentre SIGN-FLIP (first-infall DEFICIT) is backwards.** It encodes the "cold
   isolated past" as `y_hist ≈ 0.1` (LOW y). But θ(y≈0) ≈ 2 is **maximal** loading, so "low-y past" =
   memory of the cluster field applied *adiabatically* (θ=2), **not** memory of isolation. Isolation is
   `a_ex → 0` ⇒ loading `a_ex·θ → 0` for any θ. Holding a fixed nonzero a_ex while sending y_hist→0
   injects **max** past loading and produces a spurious deficit.

## Separation (shared instantaneous vs MG-impossible history)
`A_felt = a_in + L(t)`, `L` = memory-weighted external loading.
- **Instantaneous piece** (member equilibrated to the current field): `L = a_ex·θ(y_cur)`. Spread across
  y_cur = the banked **6–13%** (reproduced both footings, band 6.1–12.0%, fiducial θ0=2 → 10.4%).
  Sign: higher y_cur / less loading = HOTTER. *Partly shared* — an MG modeler handed the y_cur label can
  attempt to fit its field correlation.
- **History piece** (the clean MG-impossible one): at **fixed** current field *and* fixed y_cur, two
  members with different past L differ **only in MI** (memory kernel). **MG=0** — verified symbolically
  for both the y-channel (`d/dy=0`) and the history-channel (`d/d(history)=0`), any interpolation, any a0.
  This is the sole theorem-grade claim and is **untouched** by the sign confusion.

## History-spread sign done correctly (field-space, not y)
Encode history by the felt external **field** (physical), not by y. The EFE suppresses boost, so a member
that has felt **less** net loading is **hotter**:
- **first-infall** (field rising toward peri; memory of the lower/isolated outside): felt < now → **HOTTER (excess)**.
- **backsplash / post-peri** (field falling from peak; memory of the higher pericentre): felt > now → **COOLER (deficit)**.

This is the **exact inverse** of predict.py/D3 (first-infall +15.5%, backsplash −5.6%, both footings). The
leading contrast is unambiguous: **less-net-loaded / first-infall / higher-y_cur member is HOTTER.** Same
sign as the instantaneous piece.

## Timescale pin (the crux)
Two candidate memories, disagreeing by ~450×:

| memory | value | anchor |
|---|---|---|
| **E10 covariant kernel** τ_mem = 2c/a0 = 2Z/H_Λ | **203 Gyr** (can) / **168 Gyr** (alt), footing-free (τ·H_Λ=2Z=11.58) | equation-book E10; the object `mi_integrator/` (19/19) and `mi_spread.py` integrate |
| dwarf-v3 Lorentzian (D3/predict) | ~0.45 Gyr | **not** anchored to E10 |

Cluster infall/crossing times are ~1–2 Gyr, so **τ_mem(E10)/T_cross ≈ 100–200×**. Reasoning from the
framework's OWN kernel (Carl's framework-first rule):
- The committed memory is the **horizon memory, 203/168 Gyr ≫ crossing time → DEEP ADIABATIC.** The felt
  loading is the ~203-Gyr average of a_ex, which for any cluster member (in-cluster ≤~10 Gyr, most 1–5 Gyr)
  is dominated by the pre-infall isolated past (a_ex≈0). So felt loading is small for everyone; the residual
  spread is set by **residence-time** differences (~few %), leading sign **recent-infall HOTTER**, and there
  is **NO sharp pericentre flip**.
- **predict.py/D3's 0.45 Gyr is a different (phenomenological) number, not the E10 memory.** It is the only
  thing that makes the pericentre flip a sub-orbit resolvable transient. Dropping it for the committed E10
  memory freezes the flip out — exactly the correction `mi_spread.py` already made for the star-orbit
  observable (6–13% → sub-percent, same τ_mem ≫ τ_orbit reason).
- **Honest caveat:** E13 puts real orbital frequencies on the |K|=1 pure-phase branch (unit gain, phase
  lag), so a fast one-time ramp is felt with gain ~1 and a phase **delay** — a genuine felt≠current transient
  of order the group delay, not a hard freeze. Pinning that delay needs the explicit K(□_u) group-delay
  (follow-on compute). Either way the **sign** is unchanged (less-net-loaded = hotter); only the magnitude
  and whether a resolvable transient survives are timescale-hostage.

## Verdict (honest, both ways) — outcome (C)-leaning-(B)
- The **pericentre SIGN-FLIP is NOT pre-registerable**: it is backwards (isolated-past mis-encoding) and
  timescale-hostage (needs the un-anchored 0.45 Gyr). **The D3 D3_amplitude_vs_settledness sign-flip
  pre-registration should be downgraded/retracted on this basis.**
- **Pre-registerable** claims: (i) **EXISTENCE** of a fixed-radius history spread (MG=0, theorem-grade);
  (ii) the **leading sign** that a less-net-loaded / first-infall / higher-y_cur member is **HOTTER** than
  a matched long-resident member at the same radius — which **inverts GAP E4's negative label and the D3
  pre-peri-deficit**, and matches predict.py's baseline.
- **Magnitude** is timescale-hostage: ~few % (frozen, E10) … ~6–13% (instantaneous). The framework-consistent
  (E10) value is the smaller, frozen one.
- **MG = 0** at fixed true field is untouched and remains the sole theorem-grade claim. MI-class-generic
  (MI-vs-MG, not this-framework-vs-Milgrom). a0 value + s=−1 are postulates; **the sign tracks the s=−1
  postulate.** No "proves".

### Follow-on for the prediction lane
1. Re-issue GAP E4/E7 with the **corrected sign** (first-infall/plunger HOTTER = POSITIVE) and **invert the
   E7 kill-condition** (a significantly *negative* sign at fixed radius would be the falsifier).
2. Retract/retire the pericentre sign-flip as a pre-registered discriminator; keep existence + leading sign.
3. Compute the explicit K(□_u) group-delay to fix the magnitude between the frozen (few %) and instantaneous
   (6–13%) bounds.
