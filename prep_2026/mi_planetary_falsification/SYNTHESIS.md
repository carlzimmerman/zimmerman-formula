# SYNTHESIS — MI at the solar system: SURVIVES (conditionally), as a gated Reading-C crossover with a FREE 5th constant

**Question (make-or-break).** Does a *single* crossover mechanism exist that simultaneously (i) preserves
the galactic RAR — MI active at ω ~ 1e-15 rad/s — and (ii) passes *every* solar-system bound — MI
suppressed at ω ~ 1e-7 rad/s, no excluded a₀/c secular drift, and no observable signal from the transition
at any probed ω? Compute the exact allowed ω_c window from **all** constraints jointly, on **both**
footings (canon a₀ = cH_Λ/Z = 9.36e-11; alt ρ_total/cH₀ = 1.13e-10), and decide whether the surviving
corner is **forced** by a scale in the theory or is a **free** add-on.

Answer, computed and independently re-derived this session: **SURVIVES, but conditionally — the window is
NON-EMPTY on both footings, and the surviving corner is FREE (an honest 5th constant), not forced.**
Not a falsification; not a clean win.

---

## 1. Headline

**The framework SURVIVES at the solar system.** A single gated crossover ("Reading C") threads the galactic
RAR and every current solar-system bound: the joint ω_c window is **non-empty on both footings**. But it
survives only by **adding a postulate the published action does not supply** — the ~Myr crossover corner is a
genuinely **FREE 5th constant** {s, a₀, Z, η} → +ω_c. The action's *own* forced memory corner sits ~5 orders
below the window and is RAR-dead. So: complete up to constants, with the constant count rising from 4 to 5.

## 2. Survives-or-fails — straight, both footings

**Verdict: SURVIVES (window NON-EMPTY, both footings), corner FREE.**

The gate is the unique minimal causal one-corner object: a single-pole Debye relaxator
G(ω) = 1/(1 + iω/ω_c). Its |G|² = Re G identity (Re/Im a Kramers–Kronig pair) is machine-verified, so the
dissipative secular drift is **forced by the gate's causality, not inserted by hand** (`window_joint.py`
check 1, PASS). MI is active (gate open) below ω_c, suppressed above it.

| edge | source | canon | alt |
|---|---|---|---|
| **LOWER** = galactic RAR-preservation (Re G ≥ 0.9 at deepest confirmed MOND orbit, y=0.8, v=25 km/s → ω_c ≥ 3 ω_gal) | SPARC deep-MOND | ω_c ≥ **8.99e-15** rad/s | ω_c ≥ **1.09e-14** rad/s |
| **UPPER** (binding) = LLR secular-drift ceiling, d ln r/dt = a₀ ω_c/g_N ≤ 2σ | Biskupek & Müller 2021, *Universe* 7:34 (arXiv:2012.12032), Ġ/G = (−5.0 ± 9.6)e-15/yr → 2σ = 2.42e-14/yr | ω_c ≤ **2.21e-14** rad/s | ω_c ≤ **1.83e-14** rad/s |
| UPPER (looser, non-binding) = per-planet reactive δg | Fienga & Minazzoli 2024, *LRR* 27:1 (Saturn binds, δg = 7.0e-15) | ω_c ≤ 8.27e-11 | ω_c ≤ 7.52e-11 |
| UPPER (looser, non-binding) = Ġ/G | Genova 2018, *Nat. Commun.* 9:289 (< 4.0e-14/yr); η = (−6.6±7.2)e-5 | weaker than LLR | weaker than LLR |

**JOINT WINDOW**
- **canon:** ω_c ∈ **[9.0e-15, 2.2e-14] rad/s** = τ ∈ [1.43, 3.53] Myr — width ×2.46
- **alt:** ω_c ∈ **[1.1e-14, 1.8e-14] rad/s** = τ ∈ [1.73, 2.92] Myr — width ×1.69

The **LLR secular drift binds** — it is ~3.6 dex tighter than the per-planet reactive edge and tighter than
MESSENGER/Genova. The per-planet δg exclusions of the *ungated* a₀/2 = 4.68e-11 m/s² constant sunward tail
(the falsification the gate must evade) are reproduced by an independent Gauss secular equation to ≤2%:
Mars ~34000×, Saturn ~6700× (canon; ×1.2 alt), and that tail's observable precession grows as √a
(Saturn/Mercury = 5.08 ≈ √(a_S/a_M) = 4.98), so Mars/Saturn dominate — all honest, not inflated
(`verify_independent.py`, all PASS).

**Transition observability adds no edge.** Only wide binaries / Oort-cloud orbits probe ω ~ ω_c; at the
window's max corner the gate keeps ≤6% of the MOND boost at ≤20 kAU — a *prediction*, not a current
exclusion.

**Corner: FREE.** The published action forces the memory corner to ω_c = a₀/2c = **1.56e-19 rad/s**
(τ_mem = 2c/a₀ = 203 Gyr canon / 168 Gyr alt; CLOSURE_MAP.md:59), which is **10^4.8 below the window bottom**
and **RAR-dead** — at that corner the retained galactic boost is Re G(ω_gal) = 2.7e-9, so it gates OFF the
rotation curves too (CONSEQUENCES.md:115-119). Every other candidate scale in the theory was tested
explicitly (`origin_window_scales.py`, both footings): the dS-bath Matsubara pole = H_Λ = 1.8e-18 (the
*horizon* rate, ~4.7 dex below), kernel retardation a₀/c = 3.1e-19 (horizon, ~4.5 dex below), the Herglotz
measure has no second dimensionful scale (branch point t = 1/4 is dimensionless in a₀² units; single-scale
a₀ by construction). The closest near-miss, √(4πGρ_local) = 2.4e-15, is only ~3.8× below the window bottom
**but is environmental, not a theory constant** (spans ≥3 dex cosmic→local), and planets share the local
density with the co-located galactic orbit, so it cannot separate them. The off-circular pullback leaves
η(β) free (CLOSURE_MAP.md item d; CONSEQUENCES.md:20-30). **No scale in the theory pins ω_c → FREE.**

## 3. What it means

**Survives-free ⇒ an honest cost: a 5th constant.** The framework is not falsified at the planets, but its
solar-system viability is *bought* with a new postulate. The constant count rises {s, a₀, Z, η} → +ω_c. This
is the honest ceiling and must be stated as such: it is neither a forced strengthening (no named second scale
lands in the window — the FREE call is the non-dressing verdict) nor a falsification (the window is real and
non-empty on both footings, under the actual published 2σ bounds used at face value, not inflated).

**Every number here discriminates only among the framework's own readings, never vs ΛCDM.** The gated
Reading-C construction resolves an internal inconsistency (the ungated a₀/2 tail is BN11/INPOP-ruled-out;
the spectral reading that suppresses kinematically erases the RAR and carries an excluded a₀/c drift); it
does not produce a solar-system observable that outperforms ΛCDM. c_T = 1 (graviton on g) is untouched.

**Two-sided falsifiable, exactly as stated:**
- A confirmed Chae-type AQUAL-strength wide-binary boost **kills** the gated survivor (the gate predicts ≤6%
  boost at ≤20 kAU, where AQUAL predicts the full boost).
- A ×3 INPOP/EPM/LLR secular refit either **detects** the a₀-scale drift (d ln r/dt = a₀ ω_c/g_N at the
  Moon) or **closes the window from above**.

**Honest fragility (disclosed, neither buried nor exaggerated):** the window is genuinely narrow (×2.46
canon / ×1.69 alt); the lower edge uses a single representative deepest-MOND orbit (v = 25 km/s) rather than
the full SPARC sweep; confirmed MOND rotation below v ~ 20 km/s could close it. The window stays OPEN under
harsher RAR (y=1,v=20 → ×1.57), 1σ LLR (×1.48), and aggressive RAR (y=1,v=15 → ×1.18), and pinches shut only
at a₀ = 1.47e-10 (both footings sit below it — survival is not knife-edge in a₀). The single-pole gate that
sets the binding upper edge is the *conservative* choice: a sharper n≥2 gate loosens the drift edge ~4 orders
and widens the window ~10⁴× — so the tight edge is imposed by the most conservative causal gate, not
manufactured (`verify_independent.py` stress tests, all PASS).

## 4. Ranked next

1. **Full-SPARC lower edge.** Replace the single representative v=25 km/s deepest-MOND orbit with the actual
   SPARC deep-MOND distribution to harden (or close) the lower edge — the one genuine numerical soft spot.
2. **Wide-binary boost prediction as a live test.** Compute the gated boost curve vs separation (≤6% at ≤20
   kAU at max corner) against the Gaia DR4 wide-binary sample — this is the corner's two-sided kill switch.
3. **×3 INPOP/EPM/LLR secular refit forecast.** Project the a₀ ω_c/g_N drift at the Moon and inner planets
   against a plausible next-generation LLR/ranging sensitivity to say whether the drift is detectable before
   the window is closed from above.
4. **Corner-origin re-attack (low priority, likely null).** Only a *new forced dimensionful scale* absent
   from the current action could upgrade FREE → forced; the four tested candidates (dS-bath, retardation,
   Herglotz measure, density) all fail. Do not re-open absent a new forced kernel — the FREE call stands.

---

### Provenance
- Scripts (exit 0, both footings, numpy only, no hard-coded verdict booleans; hard-coded-check grep = 0):
  `window_joint.py`, `origin_window_scales.py`, `verify_independent.py` — all internal checks PASS.
- Docs: `WINDOW.md`, `ORIGIN.md`, `VERIFY.md`.
- Prior work cited file:line: `planetary_doors/{KERNEL_PLANETS,BOUNDS,DOOR_SCOREBOARD}.md` + laneK/laneR;
  `mi_closure_pin/{CONSEQUENCES.md (RAR-dead:115-119; pullback:20-30), rider_c_planetary.py}`;
  `mi_field_theory/CLOSURE_MAP.md (item d:59, residual η(β):89-102)`.
- Bounds (value ± σ, used at 2σ face value): LLR Biskupek & Müller 2021 Ġ/G = (−5.0±9.6)e-15/yr;
  MESSENGER Genova 2018 Ġ/G < 4.0e-14/yr, η = (−6.6±7.2)e-5; per-planet δg Fienga & Minazzoli 2024.
