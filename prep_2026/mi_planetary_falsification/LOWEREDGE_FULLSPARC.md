# HARDENING THE LOWER EDGE — full-SPARC deep-MOND distribution vs the single-orbit estimate

**Date:** 2026-07-16. **Compute script:** `loweredge_fullsparc.py` (this dir; numpy only; **exit 0, all
checks PASS**; full log `loweredge_fullsparc.out`). Framework: **de Sitter–Unruh MODIFIED INERTIA** (Carl
Zimmerman), judged on its own terms; both footings a₀=9.36×10⁻¹¹ (canon) / 1.13×10⁻¹⁰ (alt). This lane
**only** recomputes the LOWER edge of the joint ω_c window; the gate and the LLR upper edge are reused
unchanged from `window_joint.py`.

---

## The soft spot this closes

`window_joint.py:110` set the lower edge from a **single representative** deep-MOND orbit (v=25 km/s,
y=0.8 → ω_gal=3.0×10⁻¹⁵, lower edge 3ω_gal=8.99×10⁻¹⁵ canon). But **ω_gal = v/r is the orbital angular
frequency** and it scales orbit-by-orbit: the AC content of the centripetal acceleration a body feels is a
tone at exactly ω_orbit = v/r (a_c points at the center and rotates once per orbit; ω = a_c/v = v/r). The
gate — a single-pole low-pass Re G=1/(1+(ω/ω_c)²), reused from `window_joint.py:79` — must stay OPEN
(Re G≥0.90 ⟹ ω_c ≥ 3·ω_gal, k=√(0.9/0.1)=3, reused from `window_joint.py:111`) at **every** confirmed
deep-MOND orbit. So the binding lower edge is **3·MAX(ω_gal)** over the whole confirmed-deep-MOND sample.

**Selection (stated, same cuts the RAR uses):** Q≤2, inclination≥30°, deep-MOND g_bar=V_bar²/r < a₀
(both footings), V_bar²=sign(Vgas)Vgas²+0.70·Vdisk²+0.98·Vbul² (framework best-fit M/L,
`rar_framework_a0_mlfit.py:56`). 151 galaxies qualify; 2188 (canon)/2271 (alt) deep-MOND points scanned.

## Result — window SURVIVES both footings, but hardened ~×2

| footing | MAX ω_gal | hardened lower = 3·MAX | LLR upper (fixed) | **WINDOW** | width | vs old edge |
|---|---|---|---|---|---|---|
| **canon** | 5.94×10⁻¹⁵ | **1.78×10⁻¹⁴** | 2.21×10⁻¹⁴ | **[1.78, 2.21]×10⁻¹⁴** | ×1.24 | ×1.98 higher |
| **alt** | 5.94×10⁻¹⁵ | **1.78×10⁻¹⁴** | 1.83×10⁻¹⁴ | **[1.78, 1.83]×10⁻¹⁴** | **×1.027** | ×1.64 higher |

**The binding MAX is set by UGC05721** (Q=1, inc=61°) at its innermost radius r=0.09 kpc, V_rot=16.5 km/s,
g_bar=7.0×10⁻¹¹ (y=0.75 canon / 0.62 alt). The full-SPARC MAX is **≈2× larger** than the single-orbit
estimate, so the hardened lower edge nearly **doubles** and the window collapses from ×2.46 → ×1.24 (canon)
and ×1.69 → **×1.027** (alt).

## Sensitivity and robustness (the honest reading)

- **The alt footing is on a knife-edge.** It CLOSES if any confirmed deep-MOND orbit has ω_gal > ω_hi/3 =
  **6.10×10⁻¹⁵**; the observed MAX 5.94×10⁻¹⁵ sits just **+2.7%** under. One marginally faster-in-angular-
  frequency confirmed dwarf orbit would falsify the framework at the planets on the alt footing. Canon has
  +24% headroom (closes above 7.37×10⁻¹⁵).
- **Robustness — drop each galaxy's innermost radius** (rising-curve/beam-smearing guard): MAX falls to
  4.62×10⁻¹⁵ (UGC05721's 2nd point, r=0.27 kpc, V=38.5), lower edge 1.39×10⁻¹⁴, and **both footings
  survive comfortably** (canon ×1.59, alt ×1.32). So the near-closure of the alt footing is driven by a
  single innermost point; the survival verdict itself is robust to removing it.

## Verdict

**WINDOW SURVIVES on both footings** after full-SPARC hardening — the gated Reading C still threads the
galaxy and the solar system — but the window is **substantially narrower** than the single-orbit estimate,
and the **alt footing is razor-thin (×1.027, +2.7%)**: it is one marginally faster confirmed deep-MOND
dwarf orbit away from closing. The corner remains a **FREE 5th constant** (unchanged conclusion; the
action forces ~200 Gyr, RAR-dead). Not a falsification; not a clean win — a hardened, two-sided-open pass
whose alt footing now sits at the edge of closure.

*Reproduce:* `cd /Users/carlzimmerman/new_physics/prep_2026/mi_planetary_falsification && python3 loweredge_fullsparc.py`
(exit 0). Real SPARC read-only from `zimmerman-formula/real_research/data/{sparc_data/*_rotmod.dat,
sparc_master_clean.csv}`. Reused machinery cited inline to `window_joint.py`.
