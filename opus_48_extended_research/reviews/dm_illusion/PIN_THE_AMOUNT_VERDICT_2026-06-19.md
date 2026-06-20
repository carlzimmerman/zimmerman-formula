# Can dS-Unruh PIN the dark-sector field AMOUNT (I0 ~ Omega_dm ~ 0.26)? — NO, it stays a free boundary datum (2026-06-19)

*Topic `pin_the_amount` of the dm-illusion workflow. The sharper question beyond the AeST-embedding's
`sqrt_lambda_pins_KQ`: even IF the dark field were DERIVED from dS-Unruh (frame->field), would a
VACUUM / HORIZON condition fix its amplitude? Calc in `pin_the_amount.py` (reproduced this session).
Both-ways; no manufactured relation; Verlinde mirage left dead. Quarantine held (a0/Z/kappa not derived).*

## ONE-LINE VERDICT

**NO. None of the four named dS-structural conditions — de Sitter horizon entropy S_dS, the Gibbons-Hawking
temperature setting a condensate density, a holographic/CKN bound, or a no-boundary/dS initial state — pins
the cold-dust amplitude I0 ~ Omega_dust ~ 0.26. Every one of them reproduces the dark-ENERGY scale (Lambda /
Omega_DE = 0.685), which a0 = c^2 sqrt(Lambda/32pi) ALREADY ties, and NONE delivers a SEPARATE cold a^-3
amplitude ~0.26 without a hand-tuned O(1) or a circular dust-entropy. The why-now ratio Omega_dm/Omega_Lambda
~ 0.39 is epoch-dependent and therefore CANNOT be a constant of the (a-independent) dS vacuum — it is a
genuine un-pinned boundary datum. The STRONG illusion claim ("the field AND its amount come from dS-Unruh")
does NOT survive at the amount. amount_pinned = FREE.**

## THE FOUR CONDITIONS, TESTED QUANTITATIVELY (pin_the_amount.py)

| dS condition | what it actually gives | pins 0.26? |
|---|---|---|
| (A) horizon entropy S_dS = A/4l_P^2 ~ 3.3e122 | a PURE hbar-laden number; = 1/(G hbar H^2/c^5), a function of Lambda ONLY. d rho_dust/d Lambda=0 => carries ZERO derivative onto the dust. Any "dust entropy" ratio already CONTAINS I0 = circular | **NO** |
| (B) Gibbons-Hawking T_GH = hbar H_L/2 pi kB ~ 2.2e-30 K | a thermal/quantum condensate at T_GH gives Omega ~ 1e-122 (the vacuum/CC scale) — it reproduces dark ENERGY, NOT a cold 0.26; and a thermal bath is the WRONG (w~1/3) equation of state for w=0 dust | **NO** |
| (C) holographic / CKN bound | reproduces rho ~ M_P^2 H^2 = the dark-energy magnitude (Omega_DE=0.685); O(1)=(3/8pi)^(1/4) is PURE GEOMETRY (banked door3). An INEQUALITY with a free O(1) cannot pin an equality target; demanding 0.26 = solving for the O(1) = circular | **NO** |
| (D) no-boundary / dS initial state | I0 is the shift-symmetric zero-mode displacement (Q-Q0) — a FLAT direction; Bunch-Davies/Hartle-Hawking has <phi>=0 and does NOT fix the homogeneous background; the no-boundary measure (where computable) favors large-volume/small-field-energy, not 0.26 | **NO** |

**Common structural reason (the real result, not four numerology misses):** all four conditions are functions of
the dS BULK constant Lambda. I0 is an INTEGRATION CONSTANT — a boundary/initial datum — of the shift-symmetric
phi-bar EOM (a^3 K'(Q)=I0 for ANY I0). A boundary constant is orthogonal to every bulk coupling by construction;
`d rho_dust/d Lambda = 0` is the exact statement. dS-Unruh thermodynamics acts on the COUPLINGS (it fixes Lambda,
and via a0=c^2 sqrt(Lambda/32pi) the dark-ENERGY face) and has no operator that converts a bulk coupling into an
initial datum. **Even a fully DERIVED field would carry a free zero-mode amplitude** — deriving the kinetic term
(topic 1, which the corpus finds NOT done) would still leave I0 as the integration constant of its EOM.

## THE ONE MECHANISM THAT *COULD* PIN A FREE AMPLITUDE — AND WHY IT IS ABSENT (adversarial both-ways)

The honest hardest pro-pinning route: a SCALING ATTRACTOR / TRACKER. A tracker potential drives the field to the
background density from a wide range of initial conditions, locking rho_field/rho_background to a fixed ratio —
that WOULD pin the amount independent of I0. **But the AeST scalar is NOT a tracker.** It is shift-symmetric
k-essence whose energy density is pure dust ρ ∝ (1+z)^3 plus small DECAYING corrections (Skordis-Zlosnik;
confirmed in the AeST cosmology literature this session). A pure a^-3 dust with a free amplitude has NO
attractor — its amplitude IS the integration constant. The coincidence-problem literature is explicit that a
free-amplitude dust component requires the ratio to be "set to a specific value in the early Universe" (the
textbook signature of an un-pinned boundary datum), and that even time-varying dark energy "does not resolve
the coincidence puzzle." So the lone amplitude-pinning mechanism is structurally absent here. Credit where due:
IF AeST's K(Q) had a tracker, this verdict could flip — it does not.

## WHY-NOW Omega_dm/Omega_Lambda ~ 0.39 IS A GENUINE UN-PINNED DATUM

The ratio is TIME-DEPENDENT (rho_dm ∝ a^-3, rho_Lambda = const), crossing 1 near today and → 0 in the future.
A quantity that depends on the epoch a(t) cannot be a constant of the a-independent dS vacuum. It is fixed by
I0 (the amplitude) AND the epoch we observe at — a textbook "why now" coincidence. dS-Unruh fixes the CONSTANT
piece (Lambda) and a0 (~sqrt(Lambda)); it has no handle on the a^-3 amplitude or on "which a we live at." NOT a
dS constant => un-pinned.

## VERLINDE CROSS-CHECK — the "dS-entropy illusion" route does NOT revive, and would not even help

Verlinde 2016's apparent DM is a RESPONSE to baryons — `M_D^2(r) = (cH0 r^2/6G) d[M_b(r) r]/dr` — i.e. it has NO
free cosmological Omega_dm at all; the "dark matter" is slaved to the baryon profile + cH0. If that route worked
it would OVER-pin (zero free dark numbers). But it is a BANKED MIRAGE here and stays dead: wrong footing
(cH0 not cH_Lambda), 1/6 != 1/Z=1/5.789, and it FAILS clusters (Tian+ 2020) and RC shapes (Lelli-McGaugh 2017,
unobserved residual-radius correlation). The framework's AeST dust is the OPPOSITE structure — a FREE
cosmological amplitude that fits clusters+CMB PRECISELY BECAUSE it is free, not a baryon response. You cannot
have both: "pinned by dS" (Verlinde, dead) XOR "free amplitude that fits" (AeST, alive). The alive route is the
un-pinned one. **verlinde_revived = FALSE.**

## HONEST LINE (both ways)

- **The illusion thesis at the AMOUNT does NOT hold.** "The field AND its amount come from dS-Unruh" is not
  supported. The amount is a free boundary datum even granting a derived field.
- **The defensible reduced claim** (held, not retracted): the dark sector is plausibly the gravitational
  sector's own FIELD energy (AeST K(Q) condensate), NOT a particle — and the CMB 3rd peak REQUIRES that energy
  density (~Omega_dm, CAMB-verified): it is "field not particle," NOT "nothing there." That is topic-3's result
  and is untouched here; this topic only kills the stronger "amount is also derived" extension.
- **No manufactured relation.** Crediting Omega_dust ≈ Omega_dm as a dS-Unruh prediction would be manufactured
  (it is an O(1) abundance coincidence; Bridge-1: a0 absent from linear theory; tested four ways, all circular
  or off by ~120 orders). Conceded loudly.

## SOURCES
- Calc: `opus_48_extended_research/reviews/dm_illusion/pin_the_amount.py` (this session, reproduced).
- Banked: `aest_embedding/SQRT_LAMBDA_PINS_KQ_VERDICT_2026-06-19.md` + `sqrt_lambda_pins_KQ.py` (postulated-field
  version); `DARK_SECTOR_CMB_CLUSTERS_2026-06-19.md` (CMB needs the cold energy); `AEST_EMBEDDING_2026-06-19.md`
  (I0 free integration constant; Bridge-1); `MI_KERNEL_FROM_DSUNRUH_2026-06-19.md`; `TOE_LITERATURE_MAP_2026-06-15.md`
  (Verlinde mirage, CKN door3 geometric O(1)); `LENSING_NOGO_CLOSED_FINAL_2026-06-17.md` (preferred-frame forced).
- Lit: Skordis & Zlosnik 2021 (arXiv:2007.00082) shift-symmetric k-essence dust; Verwayen-Skordis-Zlosnik 2024
  (arXiv:2304.05134); Verlinde 2016 (arXiv:1611.02269) apparent-DM-as-baryon-response; Lelli-McGaugh-Schombert
  2017 (1702.08865) + Tian+2020 (1807.01689) Verlinde failures; coincidence-problem reviews (Sahni;
  arXiv:astro-ph/0411033, arXiv:1410.2509) — free-amplitude dust = "set in the early Universe," no tracker.
