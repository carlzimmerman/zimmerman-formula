# ALL FRONTS — PMNS/A4 forcing + the honest empirical ledger + best open lead

**Date:** 2026-06-26  **Status:** both-ways, anti-circular, footing-locked, NO git push.
**Scripts (re-run & confirmed this session):**
- `real_research/pmns_a4_tbm_forcing_test.py` (mpmath dps=40)
- `real_research/rar_framework_a0_mlfit.py` (framework's OWN dS-Unruh ν, a0=9.361e-11)

Framework: a0 = c² √(Λ/32π) = 9.36e-11 m/s² (gravity = theorem-grade one-parameter EFT).
SM sector kernel-free (44.5M-expr brute force). Koide r=√2 beyond symmetry-forcing (covariance no-go).

---

## FRONT 1 — Does discrete flavor FORCE the measured PMNS angles? → **FORCE-ONLY-TRIBIMAXIMAL-WITH-TUNED-DEVIATION, and the framework's triality is DISJOINT.**

Carl's fresh framing was right to test: mixing **ANGLES** are a different *kind* of object than Koide
**MAGNITUDES** — an angle is a VEV alignment (vacuum direction) a discrete symmetry CAN pin via residual
generators, whereas a magnitude r is a free real modulus for any group (the Koide covariance no-go). That
asymmetry is **CONFIRMED, and credited loud.** But the SM win Carl hoped for does not land, for an *empirical*
reason, not a structural one — and the framework supplies neither the family group nor the angles.

### (a) Unbroken A4/S4 GROUP-FIXES exact tribimaximal with ZERO free reals — and it is EXCLUDED.
Re-run (dps=40):
- th12 = arcsin(1/√3) = **35.264°** (sin² = 1/3), th23 = **45°**, th13 = **0** exactly.
- th13 = 0 is **EXCLUDED at ~65σ** (measured 8.52±0.13°, Daya Bay/RENO 2012). **Exact TBM is dead.**
- The **survivor** is th12: TBM 35.26° vs measured 33.4–33.68° is only **~2.2–2.7σ** — the solar angle is near-TBM.
- A5 golden-ratio: th12 = 31.72° (GR1, 2.8σ) or 36.00° (GR2, 3.3σ), and **also forces th13 = 0** → same exclusion.

### (b) After breaking, the symmetry FORCES ONE SUM RULE; the rest is TUNED.
- **TM2** (S4→Z2 residual, preserve TBM middle column): sin²th12 = (1/3)/(1−sin²th13) → th12 = **35.72°** given
  the measured th13, **~2.9σ** off, with **NO free th12 parameter.** A genuine symmetry-forced th12(th13) relation.
- "th13 ~ θ_C/√2" (Cabibbo haze) = 9.13° — right ORDER, ~4.7σ off in value; coefficient is which-residual-dependent.
- **Parameter count (the honest forced-vs-tuned line):** generic PMNS has 4 physical params. Realistic
  A4/S4/Δ27 + flavon models reach the measured angles only by spending **FREE VEV-alignment params** — they
  FORCE **1 sum rule** (a 1–2 param reduction) and leave th13's value, th23's octant, and dCP **TUNED, by the
  model-builders' own count.** Discrete flavor forces a RELATION, **NOT the 4 measured values.**

### (c) Is the framework's Spin(8)-triality the A4? → **NO. DISJOINT, two ways.**
- Spin(8) triality = the **outer-automorphism S3 (order 6)**. The TBM-forcing families are A4(12)/S4(24)/Δ27(27)/
  A5(60) — all LARGER. **S3 is not even a subgroup of A4** (the classic "no order-6 subgroup of A4"), so triality-S3
  cannot be an A4 residual.
- **Coleman-Mandula severs it regardless of containment:** triality is the outer automorphism of the *spacetime*
  isometry SO(d+1,1) (the same dS-horizon character used in the Koide channel-measure no-go). The family group acts
  on *internal* flavor space and must be a direct product with Poincaré. They cannot be identified. **The flavor
  sector is disjoint from the gauge home** — the same severance that killed the channel-measure route.

### FRONT 1 verdict
**Discrete flavor FORCES exact tribimaximal (which th13≠0 KILLS at 65σ), and after breaking forces at most ONE
sum rule (TM2 th12(th13), ~3σ) — the measured angles are otherwise TUNED VEV-misalignments.** Carl's
angle-vs-magnitude distinction **HOLDS and is credited** (the angle is genuinely more forceable in principle: 4
params, 0 free reals at TBM, no covariance no-go). **But** the clean forced pattern is *empirically* dead, the
deviation is tuned, and the framework's order-6 triality S3 is NOT the A4/S4/A5 parent — with Coleman-Mandula
keeping flavor disjoint from the gauge home. **No framework number forces the PMNS angles.** Quarantine held.
Both-ways: real forceability and the near-TBM th12 / TM2 sum rule credited; no derivation manufactured.

> Note vs the wider walls: this is a *weaker and different* wall than Koide's. Koide is a structural
> covariance no-go (r free for ANY group). PMNS is an *empirical* exclusion of the clean case (th13≠0). Both
> end at the same place — no forced SM number — but the PMNS angle is the genuinely more forceable object, and
> that nuance is worth keeping on the record as a correct instinct that simply ran into a measured reactor angle.

---

## FRONT 2 — The honest empirical ledger (in-hand vs-ΛCDM win + live fronts at TRUE significance)

### Footing locked (the wrong-deficit trap, avoided BOTH ways)
RE-RUN CONFIRMED, `rar_framework_a0_mlfit.py`, framework's OWN dS-Unruh ν: g_obs = √(g_bar² + g_bar·a0),
a0 FIXED at the Λ-derived **9.361e-11**:

```
  Upsilon_disk   RAR scatter[dex]   mean offset
       0.60          0.117            +0.051
       0.70          0.108            +0.007   <- BEST (fine grid confirms 0.70)
       0.80          0.116            -0.031
  reg-MOND (a0=1.2e-10, Up=0.5):  0.122 dex
```

**0.108 dex @ Υ=0.70 BEATS reg-MOND's 0.122 by 0.014 dex, mean offset +0.007 (≈ zero residual).** Υ=0.70 is
inside the Spitzer 3.6µm pop-synth range (~0.5–0.8). The framework's Λ-derived a0 sits **at the RAR optimum.**

**Both-ways footing note (load-bearing):** the "−22% / 0.130 dex" headline in `FRAMEWORK_EMPIRICAL_STANDING.md`
row 8 is the **McGaugh-ν framing — the WRONG interpolation for the framework.** Under McGaugh's ν the optimum
drifts to ~7.8e-11 @ Υ=0.70 (looks +20% high) or ~1.4e-10 @ Υ=0.50 (looks −20% low) — **BOTH are
interpolation/M-L artifacts, not robust deficits.** On the framework's OWN dS-Unruh ν the optimum IS ~9.4e-11.
Across {McGaugh, simple, dS-Unruh}×{Υ=0.5,0.7} the optimum spans ~7.5e-11..1.8e-10 with ≤~2% scatter penalty
everywhere — SPARC RAR is **NON-diagnostic of the exact a0 value**, but on the framework's own shape it is
**at/near optimal and beats reg-MOND.** No manufacture either direction. (Standing row 8 still carries the
McGaugh framing — it should be footnoted to the framework's-own-ν optimum; LOCAL fix, not pushed here.)

### In-hand vs-ΛCDM position (what is REAL now, stated honestly)

**(1) RAR scatter model-comparison — REAL WIN.** 0.108 < 0.122 dex on the framework's own ν, one physical M/L.
ONE Λ-derived number predicts ~147 clean SPARC galaxies / 2696 points with tighter scatter than reg-MOND — a
population/scatter statement ΛCDM cannot match without per-galaxy halo tuning. **A genuine vs-ΛCDM win.**

**(2) a0 universality — stated HONESTLY (the load-bearing nuance, do NOT overclaim).** The win is the
RAR-TIGHTNESS, **NOT** a clean per-galaxy a0-invariance. Per-galaxy a0 is M/L-degenerate (a0 and Υ both scale
g_bar), so "a0 is the same in every galaxy" is NOT available — the diagnostic is the **small global scatter at
fixed a0**, not galaxy-by-galaxy constancy.

**(3) The EFE ~4–5σ (Chae 2020/2021) — vs-ΛCDM distinctive, MOND-shared, CONTESTED.** The published Chae
external-field-effect detection (~4–5σ RC downturn correlated with environment) is **ΛCDM/SEP-FORBIDDEN** (under
the strong equivalence principle a uniform external field is invisible to internal dynamics → dark matter
CANNOT produce it; only modified dynamics can). The framework's MI-EFE reproduces it. **Two honest caveats:**
(a) CONTESTED — Banik's camp finds a weaker/null EFE; the in-house SPARC reproduction (`efe_clinch_framework.py`)
is RIGHT-SIGNED but UNDERPOWERED (Method-b r=+0.218, p~0.15) and does NOT independently reproduce Chae's 4–5σ;
(b) MOND-SHARED — distinctive vs DARK MATTER, not vs other MOND theories. State as **"vs-ΛCDM distinctive,
MOND-shared, contested ~4–5σ"** — never a clean framework-specific 5σ win.

**NET in-hand vs-ΛCDM:** ONE solid scatter win (RAR 0.108<0.122) + ONE ΛCDM-forbidden-but-MOND-shared-and-
contested signature (Chae EFE). No manufactured per-galaxy invariance; no high-priested dismissal of the real
EFE physics.

### Live prediction table at TRUE significance (each tagged; MOND-shared flagged)

**FRONT A — a0(z) BTFR-sign [vs-ΛCDM, framework-DISTINCTIVE, the hostage].** a0(z)/a0(0)=√(ρ_DE(z)/ρ_DE0);
coefficient+interpolation CANCEL, only w(z) enters. Under DESI DR2 evolving-DE (w crosses −1 at 3.1–4.2σ):
parameter-free **+6.15% a0 bump @z=0.405** (locked to DESI's phantom-divide crossing), declining to **−26% @z=3**.
Cleanest test = SIGN of the z≥2 deep-MOND BTFR offset: **−0.033 dex (−7.3% V) BELOW local @z=3** (const-MOND sits
ON it; rising-cH rival +0.166 ABOVE, already excluded). **TRUE significance NOW: HOSTAGE / non-diagnostic** —
DESI is the INPUT (ρ_DE) not an output confirmation; single-z prior-capped sub-3σ; the lone direct datum
(MUSE-DARK III / Ciocan 2026, raw rising ~2×) is M/L- & ΛCDM-degenerate (Magneticum gives apparent a0 ×3 with no
fundamental a0) = non-diagnostic, NOT a kill. **GATES:** DESI DR3 ~2026–27 (make-or-break, currently FAVORED
3–4σ); ALMA BTFR-sign ~2028–30; ELT/HARMONI clean 5σ early-mid 2030s. DISSOLVES (not falsified) to ordinary
constant-a0 MOND if DR3 reverts to w=−1.

**FRONT B — s^TX SME boost dipole [vs-ΛCDM via Lorentz-violation; the SOLE MI-vs-MG discriminator].**
s^TX=(a0/2|a|)·β_cmb·n_X, per-body 1/|a| ladder, signed NEGATIVE, CMB-apex direction (RA 167.9/Dec −6.9),
locked ratios s^TY:s^TX:s^TZ=0.208:−0.971:−0.120. Saturn(=Cassini) |s^TX|=**8.68e-10** = binding body. **TRUE
significance: ~1.5× from the tightest published combined bound** (Kostelecký-Russell Data Tables v19, Jan-2026:
s̄^TX=(−0.2±1.3)e-9, framework 0.67σ INSIDE) — **LIVE/falsifiable, NOT a detection, NOT excluded by any 2024–26
result.** CORRECTS banked ~9.6× (superseded INPOP-only 8.3e-9). The ONLY front separating modified-INERTIA from
modified-GRAVITY (Cassini Q2 excludes MG interp-functions at 8.7–15σ; MI evades). **GATE:** ~2028–2032,
ANALYSIS-limited (SME-in-loop ephemeris refit of existing Cassini+LLR+VLBI; published DR4 reach is order-of-mag,
not a confirmed σ). BepiColombo does NOT bind it.

**FRONT C — the relational σ-spread [vs-ΛCDM AND vs-MG; MG-IMPOSSIBLE, the genuinely-distinctive one].**
Cluster/dwarf member dispersion correlates with infall phase at matched radius — MI ~6–13%, MG EXACTLY 0
(depends only on momentary a_ex, Milgrom-2022 verbatim), CDM 0. NON-a0-degenerate, MG-impossible. **TRUE
significance: above-floor IN PRINCIPLE only** for plunging diffuse/UDG/dSph members; needs resolved
plunging-dwarf subset + unknown θ(y). **GATE: decadal ELT ~2032+.** Both-ways: the SCALAR member-σ SIGN
(~17σ ~2027–28) is **MOND-SHARED** (MI and MG both → σ DOWN) = decisive MOND-vs-CDM but NOT framework-
distinctive; the **relational SPREAD** is the distinctive piece.

**FLAGGING:** Front A = distinctive vs-ΛCDM (hostage to DESI w(z)). Front B = sole MI-vs-MG discriminator.
Front C scalar-sign = MOND-shared; relational-spread = framework/MI-distinctive. All other galaxy/cluster fronts
are MOND-shared or a0-degenerate.

---

## FRONT 3 — Best remaining open lead

**FRONT A (a0(z) BTFR-sign) is the best live lead, but it is a HOSTAGE, not a door the framework controls** —
it make-or-breaks on DESI DR3's w(z) (~2026–27), not on framework work. The best lead the *framework's own
content* still controls and that has not been closed is:

**The s^TX SME boost-dipole channel (Front B) is the best remaining OPEN lead** — it is the ONLY in-hand,
data-limited (not theory-limited) test that separates the framework's modified-INERTIA realization from the
modified-GRAVITY class that Cassini Q2 has already cornered at 8.7–15σ. It sits at ~1.5× the tightest current
bound (LIVE, falsifiable, not excluded), the prediction is parameter-free and sky-locked (CMB-apex, negative,
fixed ratios), and the deciding analysis is an SME-in-loop ephemeris refit of *existing* Cassini+LLR+VLBI data —
so it can move on ~2028–32 timescales **without new instruments.** This is the one place where the framework's
distinctive physics (the a0/2|a| per-body boost ladder) is exposed to data that already exists.

Secondary open lead: **Front C's relational σ-spread is the only MG-IMPOSSIBLE observable** — if a resolved
plunging-dwarf subset with measured θ(y) ever materializes (ELT ~2032+), it is the single cleanest
framework-vs-everything discriminator. But it is decadal and demands an unknown interpolation θ(y), so it is a
longer-horizon lead than s^TX.

On the SM side: **there is no open lead.** Koide is re-label-dead (covariance no-go + dS-Unruh fails 4 lethal
legs); PMNS is force-only-TBM-with-tuned-deviation + Coleman-Mandula-disjoint (this session); the 44.5M-expr
brute force is kernel-free. The SM mass/mixing sector is firmly walled — do not re-open absent a NEW forced
kernel in the gauge/Yukawa sector.

---

## WHAT TO TELL CARL (both-ways)

**The good, loud:** Your angle-vs-magnitude instinct was RIGHT — a mixing angle is genuinely more
symmetry-forceable than a Koide magnitude (TBM fixes all 4 params with 0 free reals; no covariance no-go). And
the in-hand gravity win is REAL on YOUR OWN footing: 0.108 dex @ Υ=0.70 on the framework's dS-Unruh ν beats
reg-MOND's 0.122 — your Λ-derived a0 sits at the RAR optimum. Never let anyone quote the "−22% / 0.130 dex"
number at you; that is the McGaugh-ν wrong-deficit trap, and it cuts both ways (it can be made to look +20% high
too). On your own ν, the value is convention-compatible and the scatter win is genuine.

**The honest walls, no caving:** Discrete flavor does NOT force the measured PMNS — it forces exact TBM, which
the reactor angle th13=8.5° kills at 65σ; after breaking it forces one sum rule (TM2, ~3σ) and the rest is
tuned. And your Spin(8) triality is the order-6 S3 — too small to be the A4/S4/A5 family group, and
Coleman-Mandula keeps the spacetime/gauge triality disjoint from the internal flavor group regardless. There is
no SM win here where Koide failed; the SM sector stays walled.

**Where to push:** The live action is entirely on the gravity side and it is NOT "no doors." The best open lead
you control is the **s^TX SME boost-dipole** (~1.5× the tightest bound, the sole MI-vs-MG discriminator, decided
by an ephemeris refit of EXISTING data ~2028–32). The make-or-break is **DESI DR3 (~2026–27)** for the a0(z)
BTFR-sign hostage — currently FAVORED 3–4σ, dissolves to ordinary MOND if w reverts to −1. Watch both; neither
needs new theory from you.

---

**Both-ways discipline applied:** credited real forceability + the RAR win + the ΛCDM-forbidden EFE physics;
refused the manufactured TBM/PMNS derivation, the manufactured per-galaxy a0-invariance, and the McGaugh-ν
wrong-deficit. NEVER "no doors" — s^TX and DESI DR3 are live. No git push.
