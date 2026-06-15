# Route 4 — Holographic / Equipartition / CKN: does horizon-dof counting force κ = ½ (Z = √(32π/3))?

**C. Zimmerman, 2026-06-15.** *Independent re-derivation (sympy `/tmp/route4_*.py`), literature-verified
(Verlinde 1611.02269; Padmanabhan 1206.4916; CKN hep-th/9803132 + 2410.01471; Jacobson gr-qc/9504004). Tests whether
any emergent-gravity dof-counting program FORCES the coefficient. Banked context: `COEFFICIENT_DEFINITIVE_VERDICT.md`,
`FORCING_ROUTES_REWORKED.md`, `CKN_LAMBDA_VALUE_VERDICT_2026-06-06.md`. Verdict: **UNFORCED-POSIT — every route leaves a
free dof-counting O(1); none selects κ=½. Cleanest near-miss = Verlinde Z=6 (κ=0.482), off the framework's 5.789 by 3.5%.**

## The anchor (sympy `solve`, exact)
`a₀ = κ·c·√(Gρ_DE)`, `ρ_DE = Λc²/8πG` ⟹ `a₀ = κc²√(Λ/8π)`. Matching `a₀ = c²√(Λ/32π)` gives **κ = ½ exactly**, and
`Z ≡ cH_Λ/a₀ = √(8π/(3κ²))`, so **κ=½ ⟺ Z=√(32π/3)=5.789** (verified, difference = 0). Deriving Z ≡ deriving κ=½.

## The four sub-routes — implied Z, and what free input remains

| route | what the counting actually outputs | implied Z (κ) | free O(1)? |
|---|---|---|---|
| **(i) Verlinde** (1611.02269) | `a_M = cH/6`, the **/6** = area-vs-volume entanglement strain `d(d−1)\|₃=6` | **Z=6.0 (κ=0.482)** | **YES** — the 6 is a d=3 strain count, not ½ |
| **(ii) Padmanabhan** equipartition (1206.4916) | `dV/dt=ℓ_P²(N_sur−N_bulk)` ⟹ Friedmann `H²=8πGρ/3` | **a₀ NOT output** | the 8π & 3 are forced, but **no a₀ in the law** |
| **(iii) CKN** UV-IR (hep-th/9803132) | `ρ ≲ M_P²H²` (an **inequality**); saturating: `ρ_DE=(3/8π)M_P²H²` | **a₀ NOT output** | **YES** — `4/Z²=3/8π` sits in CKN's *free* slot |
| **(iv) Jacobson** Clausius (gr-qc/9504004) | `η=1/4ℏG ⟹ 8πG`; `8π=2π(Unruh)×4(=1/[BH ¼])` | **a₀ absent on dS saddle** | the single ¼ is *spent* in 8π; no 2nd ¼ |

### (i) Verlinde — Z=6, the cleanest near-miss, but NOT ½ (literature-confirmed)
Verlinde 2016 ("Emergent Gravity and the Dark Universe", 1611.02269): the dark force appears below `a₀ = cH₀/6`, where
`cH₀` is the de Sitter horizon acceleration and the **/6** plays the role of `a_M` in MOND. In the canonical convention
`Z=cH_Λ/a₀`, this is **Z=6 ⟹ κ=0.482**. The 6 is forced *within Verlinde's scheme* — it is the d=3 volume-law strain
factor `d(d−1)=6` — but it is **a different O(1) from the free-fall ½**. `Z=6 ≠ √(32π/3)=5.789` (a 3.5% gap). So
Verlinde *does* fix his coefficient, just to **6, not to the framework's value**. This is the sharpest the holographic
cluster gets: it lands the *right ballpark* (Z~6, excluding the naive 1–3) but selects a number 3.5% off and via a
volume-strain count, not a free-fall ½.

### (ii) Padmanabhan — equipartition outputs Friedmann, never a₀
Verified two things in sympy: (a) the screen equipartition `½N_sur k_B T_Unruh = Mc²` reproduces Newton **exactly**
(`g = GM/R²`, difference=0); (b) at the cosmological horizon the equipartition condition `N_sur=N_bulk` outputs the
**Friedmann equation** `H²=8πGρ/3` (literature-confirmed: Padmanabhan substitutes `ρ=−p` for pure dS and gets exactly
this). So **the 8π and the 3 of Z² ARE Padmanabhan-forced — but as the Friedmann constraint, not as an a₀ coefficient.**
a₀ is simply **not an output** of holographic equipartition; the law fixes `H(ρ)`, not `a₀/cH`. Padmanabhan's
equipartition *does* carry an explicit ½ (`E=½Nk_BT`), but sympy confirms that ½ multiplies a horizon **energy**
(`E_equi(dS) = √3 c⁴/G√Λ`), not the a₀ map — it does **not** transfer to κ. Different ½'s (equipartition-energy vs
free-fall-kinematic).

### (iii) CKN — fixes the ρ magnitude, parks 4/Z² in its own free slot (sympy-exact)
CKN gives an **inequality** `ρ_vac ≲ M_P²H²` (depleted-dof / no-black-hole argument), with an **undetermined O(1)**.
Saturating it + the Friedmann route gives `ρ_DE = (3/8π)M_P²H_Λ²` (sympy: ratio = **3/8π exactly**). And **`4/Z² = 3/8π`
identically** (sympy). So the framework's coefficient `4/Z²` is *precisely* the number that lives in **CKN's free O(1)
slot** — the bound permits it but **does not require** it (≲, not =). CKN welds a₀ and ρ_DE to one √Λ ladder at the
correct 10⁻¹²² magnitude (the genuine win, per `CKN_LAMBDA_VALUE_VERDICT`), but **places the coefficient by hand
(saturation), not forces it.**

### (iv) Jacobson — the one BH ¼ is already inside Einstein's 8π
`8π = 2π(Unruh) × 4`, and the `4 = 1/(BH quarter)` (sympy: `8π−2π·4=0`). The single Bekenstein–Hawking ¼ is **spent
building the Einstein 8πG** (Jacobson's `η=1/4ℏG`). For `32π=4×8π` you need a **second, independent** ¼ — and there is
none on the de Sitter saddle (a₀ enters AeST only through `|Y|^{3/2}`, and `Ȳ=0` on FRW, so the horizon partition
function sees Λ but never a₀). A *literal* second quarter, κ=¼, gives **Z=11.58**, off by ~2×. So the "32π=8π×4 = Einstein
× entropy-quarter" reading is **numerology, not a forced combination**: the entropy-quarter the story invokes is the
*same* ¼ already counted once inside the 8π — using it twice double-counts, and using a genuinely new ¼ gives the wrong
number (11.58, not 5.789).

## Both-ways honesty
- **NOT a manufactured deficit:** the *scale* `a₀~c√(Gρ_Λ)` and the *ballpark* `Z~6` are genuinely forced/over-determined
  by every holographic route — that is real physics (why the Milgrom coincidence is robust), and the 8π & 3 inside Z ARE
  GR-forced (Friedmann). The framework is *at* the frontier (Verlinde, Padmanabhan, CKN, Singh 2026 all match, none derives).
- **NOT a manufactured win:** no route forces **κ=½**. Verlinde forces a *different* O(1) (6, via volume strain); Padmanabhan
  and CKN don't output a₀ at all (Friedmann / an inequality); Jacobson's lone ¼ is already inside 8π. The `32π=8π×4` framing
  is a **post-hoc pattern-match** (the ¼ is double-counted; a real 2nd ¼ → 11.58). The κ=½ is a **free-fall kinematic posit**
  sitting in the free dof-counting slot every program leaves open.

## Verdict
**UNFORCED-POSIT.** Holographic dof-counting forces the *scale* and the *ballpark* (Z~6, GR-traceable 8π & 3) but **not**
the coefficient κ=½/Z=5.789. Cleanest near-miss: **Verlinde Z=6 (κ=0.482), 3.5% off, and via a volume-strain 6 not a
free-fall ½.** Consistent with the banked multi-route null (`COEFFICIENT_DEFINITIVE_VERDICT.md`): structurally unfixable by
equilibrium horizon entropy. **Quarantine holds.** Moot empirically — every falsifiable test (the a₀(z)∝√ρ_DE bet) is
coefficient-free.
