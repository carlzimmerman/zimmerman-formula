# THE JOINT ω_c WINDOW — does a single crossover survive the galaxy AND the solar system?

**Date:** 2026-07-16. **Compute script:** `window_joint.py` (this dir; numpy only; **exit 0, all checks
PASS**; full log `window_joint.out`). Framework: **de Sitter–Unruh MODIFIED INERTIA** (Carl Zimmerman),
judged on its own terms — own ν(y)=√(1+1/y), μ(x)=K(x²), horizon-derived a₀=cH_Λ/Z. **Both footings
carried:** canonical a₀=9.36×10⁻¹¹ (ρ_DE, cH_Λ/Z), alt a₀=1.13×10⁻¹⁰ (ρ_tot/cH₀). s=−1 and a₀'s value
remain **POSTULATES**. Published action S_matter=−½∫√−g ρ_m[s uᵘK(□_u/a₀²)u_μ], K Herglotz, ∫dμ/|t|=1.

Upstream inputs (cited file:line): the a₀/2 landmine + the three readings — `planetary_doors/KERNEL_PLANETS.md`
§0–§7, `planetary_doors/BOUNDS.md` §1.2 (per-planet δg), §1.5 (LLR); the action-forced memory corner —
`mi_field_theory/CLOSURE_MAP.md` item (d) (`closure_map.py:59`); the survivor still needing a free corner —
`mi_closure_pin/CONSEQUENCES.md` §3, `rider_c_planetary.py`.

---

## 0. The question and the one-line answer

**Question.** Does a single crossover mechanism S(ω_orbit; ω_c) exist that **simultaneously** preserves
the galactic RAR (MI active at ω~1×10⁻¹⁵ rad/s) **and** passes every solar-system bound (MI suppressed at
ω~1×10⁻⁷, no excluded a₀/c secular drift, no observable transition signal at any probed ω)? Compute the
**exact allowed [ω_lo, ω_hi] window from ALL constraints jointly**, both footings.

**Answer (straight).** The window is **NON-EMPTY on both footings** — the framework **SURVIVES** at the
solar system:

| footing | ω_lo (RAR) | ω_hi (binding bound) | **WINDOW** | width |
|---|---|---|---|---|
| **canon** | 8.99×10⁻¹⁵ | 2.21×10⁻¹⁴ | **[9.0×10⁻¹⁵, 2.2×10⁻¹⁴] rad/s = τ ∈ [1.43, 3.53] Myr** | ×2.46 |
| **alt** | 1.09×10⁻¹⁴ | 1.83×10⁻¹⁴ | **[1.1×10⁻¹⁴, 1.8×10⁻¹⁴] rad/s = τ ∈ [1.73, 2.92] Myr** | ×1.69 |

**But the surviving corner is a FREE add-on — a 5th constant — NOT forced by any scale in the theory.**
The published action's *own* forced memory corner is ω_c=a₀/2c ≈ 1.6×10⁻¹⁹ rad/s (τ_mem=2c/a₀≈203/168 Gyr),
which sits **10⁴·⁸ (≈5 orders) BELOW** the window and is **RAR-dead** (it gates the rotation curves off too:
retained boost 2.7×10⁻⁹). So the framework passes the solar system **only** by paying an honest extra
postulate: a second, unforced ~Myr memory scale. This is a **conditional, two-sided-open pass**, not a
forced evasion — reported as such.

**Honest ceiling (non-negotiable):** at planetary accelerations (10⁴–10⁸ a₀) GR predicts zero anomaly and
healthy MOND-family theories predict near-zero; this window **discriminates only among the framework's own
readings, never vs ΛCDM.** A NON-EMPTY window is *survival*, not evidence *for* the framework.

---

## 1. The gate — justified from the memory structure, not ad hoc

The physical crossover is the **unique minimal causal single-corner object**: a one-pole (Debye) memory
relaxator with finite retention τ=1/ω_c. Time-domain kernel g(t)=ω_c e^{−ω_c t}θ(t); frequency response

  **G(ω) = 1/(1 + iω/ω_c)**,  Re G = 1/(1+(ω/ω_c)²),  Im G = −(ω/ω_c)/(1+(ω/ω_c)²).

The MI response is K_eff = 1 − S(|a|/a₀)·G(ω), with the deep-Newton landmine amplitude S→a₀/(2g_N). Two
channels fall out of the **same** G (machine-checked identity |G|²=Re G, `window_joint.py` gate block):

- **Reactive (radial)** anomalous accel = (a₀/2)·Re G(ω) → for ω≫ω_c: (a₀/2)(ω_c/ω)². *(the tail, gated)*
- **Dissipative (tangential)** accel = (a₀/2)·|Im G(ω)| → drives d ln r/dt = 2f_t/(ωr) = a₀ω_c/g_N *(a secular drift)*.

**Key structural fact:** a causal gate **cannot** suppress the reactive a₀/2 tail (Re G) without incurring
the dissipative secular drift (Im G) — Re and Im are a Kramers–Kronig pair; a frequency-dependent Re part
forces a nonzero Im part. **The drift ceiling is therefore not an optional add-on; it is forced by the
gate's causality.** The closed form d ln r/dt = a₀ω_c/g_N is verified against the direct 2f_t/(ωr) time-lag
evaluation to <10⁻⁹ (Mercury) and the a₀ω_c/g_N asymptote to <0.1% (Keplerian-consistent), no hard-code.

---

## 2. The bounds (re-fetched and re-cited this session)

| quantity | value (1σ) | role | source (verified) |
|---|---|---|---|
| **LLR Ġ/G** | **(−5.0 ± 9.6)×10⁻¹⁵ yr⁻¹** → 2σ ceiling 2.42×10⁻¹⁴ | **binding upper edge** | Biskupek & Müller 2021, *Universe* **7**:34 (arXiv:2012.12032) — value re-fetched |
| MESSENGER Ġ/G | < 4.0×10⁻¹⁴ yr⁻¹ (after solar mass-loss subtraction); η=(−6.6±7.2)×10⁻⁵ | drift anchor (Mercury) | Genova+ 2018, *Nat. Commun.* **9**:289 — value re-fetched |
| per-planet const-radial δg | Mercury 4.6e-14, Venus 8.0e-14, Earth 8.7e-15, **Mars 1.4e-15**, Jupiter 5.6e-13, **Saturn 7.0e-15** m/s² | reactive upper edge | Fienga & Minazzoli 2024, *Living Rev. Relativ.* **27**:1 Table 10 → Gauss secular (BOUNDS.md §1.2) |
| Cassini/EFE Q₂ | (1.6±1.8)×10⁻²⁷ s⁻², 2σ=5.2×10⁻²⁷ | (Door A wall, not this window) | Park+ 2026 (arXiv:2602.17884); Hees+ 2014 |

The a₀/2 landmine at full strength (Reading A, the RAR-carrying reduction) is excluded per planet by
**1017× (Mercury) … 33 429× (Mars) / 6686× (Saturn)** canonical, ×1.21 alt — recomputed in `window_joint.out`.
That is what the gate must suppress.

---

## 3. The three constraints, each edge traced to its bound

**LOWER edge — galactic RAR-preservation.** The gate must stay OPEN (Re G ≥ 0.90) at the deepest confirmed
MOND orbits, ω_gal(deep)=y·a₀/v = 3.0×10⁻¹⁵ (canon, y=0.8, v=25 km/s). Re G≥0.90 ⟹ ω_c ≥ 3·ω_gal:
**ω_lo = 8.99×10⁻¹⁵ (canon) / 1.09×10⁻¹⁴ (alt) rad/s.** *(If ω_c drops below this the gate closes on the
rotation curves themselves — RAR-dead.)*

**UPPER edge #1 — reactive perihelion (per planet).** (a₀/2)Re G(ω_p) ≤ δg_bound ⟹ ω_c ≤ ω_p·√(2δg/a₀).
Per-planet ceilings (canon): Mercury 2.6e-8, Venus 1.3e-8, Earth 2.7e-9, Mars 5.8e-10, Jupiter 1.8e-9,
**Saturn 8.27e-11** (binding). This edge is **loose** (8×10⁻¹¹) — it does not bind the window.

**UPPER edge #2 — secular drift (per body), the BINDING one.** d ln r/dt = a₀ω_c/g_N ≤ drift_bound ⟹
ω_c ≤ drift_bound·g_N/a₀. Anchors (canon): Mercury Ġ/G 5.4e-13, Mars proxy 1.9e-13, Saturn proxy 3.5e-14,
Moon tidal 3.8e-13, **Moon Ġ/G (Biskupek 2021 LLR 2σ) 2.21e-14** (binding). **ω_hi = 2.21×10⁻¹⁴ (canon) /
1.83×10⁻¹⁴ (alt) rad/s.**

**Transition observability.** The crossover τ~2 Myr (ω_c~10⁻¹⁴) is probed *only* by wide binaries and the
Oort cloud / long-period comets — nothing in the planetary regime orbits that slowly. At the max corner the
gate keeps just 0.0% (3 kAU) / 0.8% (10 kAU) / 6.2% (20 kAU, canon) of the MOND boost. This is a genuine
**prediction** (a Banik-type Newtonian wide-binary result), *not* a current exclusion — no dynamical bound
lives at ω~ω_c yet, so it adds no edge but is the sharp two-sided falsifier: a confirmed Chae-type
AQUAL-strength wide-binary boost **kills** the gated survivor.

**Intersection ⟹ NON-EMPTY on both footings** (§0 table). The window is bounded **below** by the galactic
RAR (Biskupek's LLR does not touch it) and **above** by Biskupek 2021 LLR Ġ/G — a clean, two-sided,
data-pinned interval.

---

## 4. Forced or free? — the make-or-break sub-question

**FREE — an honest 5th constant.** Three independent facts, all machine-checked:

1. **The action's own corner is 5 orders away.** Descent from S forces the memory corner to the action
   scale ω_c=a₀/2c = 1.56×10⁻¹⁹ rad/s (τ_mem = 2c/a₀ = 203 Gyr canon / 168 Gyr alt) — `CLOSURE_MAP.md`
   item (d). That is **10⁴·⁸ below** the window bottom.
2. **That forced corner is RAR-dead.** At ω_c=a₀/2c the retained galactic boost Re G(ω_gal)=2.7×10⁻⁹ — it
   suppresses the planetary tail but **also** gates the rotation curves off. So the action's corner is not a
   clean evasion; it fails the galaxy.
3. **No second scale supplies the ~Myr corner.** The off-circular Wightman pullback left the reduction
   weighting η(β) FREE (pole ≥ H_Λ for all weightings; `CONSEQUENCES.md` §0) — it does **not** pin the
   corner either. Of the SPEC's three named candidate scales, only the ~Myr "d1-pole" lands in the window;
   the ω_int (~0.4 Gyr) and H_Λ (~17.5 Gyr) corners are RAR-dead.

**Therefore:** the surviving corner ω_c~10⁻¹⁴ rad/s (τ~2 Myr) is **not forced by any principle or physical
scale in the published theory** — it is an **extra postulate**. Adopting the gated Reading C to pass the
solar system means the framework **gains a 5th constant** ({s=−1, a₀, Z, η} → +ω_c). Dressing it as "forced"
would be a manufactured save; it is not forced.

---

## 5. Verdict

- **Window: NON-EMPTY, both footings.** canon [9.0×10⁻¹⁵, 2.2×10⁻¹⁴] rad/s (τ 1.43–3.53 Myr, ×2.46);
  alt [1.1×10⁻¹⁴, 1.8×10⁻¹⁴] rad/s (τ 1.73–2.92 Myr, ×1.69). Lower edge ← galactic RAR-preservation;
  upper edge ← Biskupek & Müller 2021 LLR Ġ/G (binding; the per-planet δg reactive edge is 3–4 orders looser).
- **The framework SURVIVES at the solar system** — a single Debye-relaxator crossover with the corner in
  this ~Myr sliver simultaneously keeps the galactic RAR and clears every cited bound (per-planet δg,
  MESSENGER + LLR Ġ/G drift, transition-region observability).
- **The survival is CONDITIONAL and the corner is FREE.** The published action forces the corner to ~200 Gyr
  (RAR-dead), not into the window; nothing forces the Myr corner. This is an honest extra postulate — a 5th
  constant — **not** a forced suppression. **Not a falsification; not a clean win either.**
- **Falsifiable two ways:** (1) a confirmed Chae-type AQUAL-strength wide-binary boost kills the gated
  survivor (the gate keeps ≤6% of the boost at ≤20 kAU); (2) the drift at the max corner sits **at** current
  Saturn/Mars secular sensitivity — a dedicated INPOP/EPM secular refit improving ×3 either detects it or
  closes the window from above.

**Honest ceiling (repeat):** every number here separates the framework's own readings; none can prefer the
framework over ΛCDM. c_T=1 (graviton on g) untouched; both footings carried; s=−1 and a₀'s value postulated;
no "theory closed/complete" claim.

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_planetary_falsification && python3 window_joint.py`
(exit 0). Sources read (frozen read-only repo cited above): `planetary_doors/{KERNEL_PLANETS,BOUNDS,DOOR_SCOREBOARD}.md`,
`laneK_kernel_planets.py`, `laneR_bounds_compute.py`; `mi_closure_pin/{CONSEQUENCES.md, rider_c_planetary.py}`;
`mi_field_theory/CLOSURE_MAP.md`. Bounds re-fetched this session: Biskupek & Müller 2021 (arXiv:2012.12032),
Genova+ 2018 (Nat. Commun. 9:289). All new work in `prep_2026/mi_planetary_falsification/` only.*
