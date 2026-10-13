> **ID NOTE (2026-10-12): this lane is CFG670.** Its directory and commits say CFG665, which collided with another session's same-day use of that number (see LEDGER CFG670–679). Cite it as CFG670. Sealed files and hashes are unchanged.

# CFG665: GW messenger theorems — CERTIFIED (Lean 4)

**Label: CERTIFIED** (all of T1–T7 compile, zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}; T6 ratio ≥ 1e5 on
both footings). Criteria: `FROZEN_CRITERIA.md` (1bbc63af3), committed alone first, 2026-10-12. Block CFG660–669.

- **Lean:** `fable_independent_2026/lean_2026/CFG665_gw_messenger.lean` → `CFG665_gw_messenger.out` (exit 0, 14 `#print axioms`
  lines, none with `sorryAx`). Run: `cd fable_independent_2026/lean_2026 && lake env lean CFG665_gw_messenger.lean`.
- **MUTATE:** `CFG665_gw_messenger_MUTATE.lean` → `.out`, exit 1, exactly three errors at M1 (line 16), M2 (34), M3 (49); each false
  variant is also refuted positively (`M1_refuted`, `M2_refuted`, `M3_refuted` compile), so the failures are not tactic accidents.
- **Settings:** κ = ½ FITTED; footings separate; cold energy mass required; no particle species; not "theory closed". Lean certifies
  mathematics, not physics.

## What is certified

| | theorem | statement |
|---|---|---|
| T1 | `local_lag` | 0 ≤ B < 1 ⇒ 1/√(1−B) − 1 ≥ B/2 |
| T2 | `path_delay`, `shared_metric_zero` | B ≥ B_min on a segment of length L ⇒ lag integral ≥ B_min L/2; one shared metric ⇒ exactly 0 |
| T3 | `floor_sqrt`, `floor_mono`, `floor_mono_deep`, `grad_floor` | both kernels: (ν−1)y ≥ min(√y,1)/(1+√2) for all y>0; ν_mono deep: ≥ √y/φ; physical: (ν−1)g ≥ √(a0GM)/((1+√2)s) when g ≥ GM/s² and GM/s² ≤ a0 |
| T4 | `accumulated_tilt` | B′ ≤ −K/s on (r1,R), B(R) ≥ 0 ⇒ B(r) ≥ K ln(R/r) |
| T5 | `no_hiding_direction` | any straight sightline from radius ≥ R2 to the Sun (radius ≤ rs) reaches radius R2 at some t1, stays ≤ R2 after, and has ≥ R2 − rs of path left — for every sky direction |
| T6 | `log_ratio_ge_one`, `mw_delay_canonical`, `mw_delay_alt`, `mw_ratio` | Milky Way alone, M_enc ≥ 5e10 M☉, void at 300 kpc, 100 kpc of path with B ≥ K: Δt ≥ **2.3e6 s** (canonical; exact 2.364e6) and ≥ **2.5e6 s** (alt; exact 2.599e6) ⇒ ≥ **1.3e6 ×** the 1.7 s GW170817 bound (exact 1.39e6 / 1.53e6) |
| T7 | `double_count` | F ≥ g_bar > 0 ⇒ 1 ≤ (2F − g_bar)/F < 2 |

## Reading

1. **No sky direction escapes.** Any sector that tilts the photon cone but not the graviton cone (or the reverse) by the framework's
   own deep-MOND tilt makes light arrive ≥ 27 days after the GW from **every** direction, from the Milky Way alone, under **either**
   kernel. GW170817 saw 1.7 s. A single shared metric gives exactly zero. So the direction-dependent arrival-time test the owner
   asked about cannot separate the surviving framework from ΛCDM: both predict zero.
2. **What survives:** the extra pull must sit in the one metric that light and GWs share — real stress-energy (the record's
   post-CFG663 reading: real cold mass bound to each system, 1812f594a). T7 shows why the alternative failed CFG663: a response that
   does not lens, plus cold mass fixed by lensing, counts the law twice, a factor in [1, 2) — CFG663 measured ×1.8.
3. **GW-decay constraints** (Creminelli et al.) apply to a scalar field coupled to gravity, not to real cold mass; moot on the
   surviving branch, live only if a field-theory completion is revived (needs astra's action).

## Premises, not certified

The disformal metric and grad|B| = 4(ν−1)g/c² (UNIFICATION.md); B non-increasing outward between 10 kpc and the Sun; curved photon
paths (radius 1-Lipschitz in arclength, cited); M_enc ≥ 5e10 M☉ outside 10 kpc (input, below the 6e10 used in the record); G ≥
6.674e-11, M☉ ≥ 1.988e30, kpc ≥ 3.0856e19 m (all rounded down); the 1.7 s measurement.

## ΛCDM audit of the GW side (10-12)

`prep_2026/gw170817_check/` inputs are baryonic masses, a 40 Mpc distance, and the framework's ν — no halo, no cosmological model.
**Defect:** it uses ν = √(1+a0/g) rather than the record's ν_mono; T3 covers both kernels, and ν_mono's floor is the stronger one,
so the exclusion only strengthens. The 1.7 s bound is a direct arrival-time measurement. Caveat for the GW questions list:
standard-siren Ξ bounds and lensed-GW rate forecasts in the literature usually assume a ΛCDM background or subhalo mass function;
ask for the raw measured quantities (distance–redshift pairs, sensitivity to a given lens mass), not ΛCDM-derived rates.

## DISCLOSURE (2026-10-12, same day): kernel mislabel in T3, closed by a Lean addendum
T3's `nuMono` (½ + √(¼ + 1/y)) is the MOND "simple ν", **not** the record's ν_mono (FP1/L340: ν = 1 + h(y)/y, h the exponential-RAR
phantom with a monotone tail). T3/T6 as certified hold for the simple ν and for P2 (√(1 + 1/y), the framework's own law). The
record's ν_mono is now covered in the regime T6 uses (g ≤ a0 on the 10–110 kpc shell): `fable_independent_2026/lean_2026/
CFG670_record_kernel_floor.lean` → `.out` (exit 0, zero sorry, standard axioms): `hrar_floor` (s/(1+√2) ≤ s²/(e^s − 1) for
0 < s ≤ 1, via the exp chord bound) and `grad_floor_deep`. Premise (numeric, not certified): the FP1 table equals the RAR formula
on y ≤ 1. Hence T6's ≥ 2.3e6 / 2.5e6 s bound holds for all three kernels; verdict unchanged.
