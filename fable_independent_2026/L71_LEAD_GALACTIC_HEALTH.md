# L71 — the lead's integrable-clock action in a galactic deep-MOND background: L60 does NOT reappear, but health is NOT established

**The last surviving construction — the lead's integrable-clock action — does NOT inherit the L60 deep-MOND
kill in a galaxy, and this is now shown ON a galactic deep-MOND background rather than only at the flat-vacuum
cosmological design point L66 was confined to. But it is NOT thereby a cleared live candidate. Its galactic
static MOND background exists only at leading weak-field order; the perturbation-coefficient sector that would
decide its propagating health is pinned only at the cosmological design point S = 0.1 and, by the lead's own
IC31, may not be extrapolated to galactic S — so the full L60-style transverse verdict is UNDERSPECIFIED — and
the one channel that IS computable on the galactic configuration, the IC-4 auxiliary-gradient Hessian, is
indefinite there (det G = −4u²ξ² < 0 at π = 0, and π = 0 is exactly the static galactic branch), with the
lead's repair matched only at the π ≠ 0 cosmological witness.** The verdict is therefore not "healthy" and not
"same-mechanism unstable": it is **escape of the specific L60 mechanism confirmed to extend into the galaxy,
plus a genuinely under-determined sector and a distinct, unresolved new-mechanism concern.** Both a₀ footings.

2026-09-09. Lane L71 of [CHARTER.md](CHARTER.md), answering the named next computation against
[L66_LEAD_ACTION_HEALTH.md](L66_LEAD_ACTION_HEALTH.md), [L60_ANISOTROPIC_HEALTH.md](L60_ANISOTROPIC_HEALTH.md)
and [L69_HEALTHY_DEEPMOND.md](L69_HEALTHY_DEEPMOND.md).
Script: [L71_lead_galactic_health.py](L71_lead_galactic_health.py) → [L71_lead_galactic_health.out](L71_lead_galactic_health.out).
**18 checks, 18 PASS / 0 FAIL; exit 0; runtime 1 s.**

Polarity: each check asserts a **statement** and PASS means the statement is true. Several PASSes are negative
for the construction — read the statement. Both a₀ footings on every dimensional number: 9.3619×10⁻¹¹ /
1.1279×10⁻¹⁰ m s⁻². Nothing under `closure_2026/` was imported, executed as evidence, or copied. The Dirac
counter and the deposited-kill reproduction are fable_independent_2026's own machinery (validated 64/64 in L60,
18/18 in L66). The lead's action structure was **rebuilt** from the equations printed in its own markdown
(`ACTION.md`, `IC20_JOINT_COMPLETION.md`, `IC30_RADIAL_BRIDGE.md`, `AUXILIARY_SYMBOL.md`, `IC31_PINNED_EXTERIOR.md`,
`USER_ACTION_*`), and its reference numbers were read once, offline, and hard-coded as reproduction targets the
rebuild must hit.

---

## 1. Controls, first — including reproducing the kill and the structure identification

| control | required | got |
|---|---|---|
| CTRL-1 ADM general relativity | 2 | **2** (4 primary + 4 secondary, all first class) |
| CTRL-2 GR + one minimally coupled scalar | 3 | **3** |
| CTRL-3 Einstein-aether (c₁…c₄ = 1/5,1/7,1/11,1/13) | 5 | **5** |
| CTRL-4 khronometric (same c's, u hypersurface-orthogonal) | 3 | **3** |
| CTRL-5 **deposited static 3×3 threshold** J_crit = (2−K_B)/(2−c₁₄) | 0.9000009 | **0.9000009** |
| CTRL-6 **deposited threshold acceleration** s = g_N/a₀ | 0.3985 | **0.3985** (g_N < 3.73e−11 / 4.49e−11) |
| CTRL-7 **deposited 1 kpc e-folding time** | 0.74 Myr | **0.737 Myr** (canonical) / **0.737 Myr** (alt) |
| CTRL-8 **L66 structure ID** | (I) shares / (II) escapes | **reproduced** — (I) carries `2b P'φ'`, (II) has no separate scalar |

The kill provably fires when present: the deposited static 3×3 on (lapse n, spatial trace hT, MOND scalar δφ)
has lapse effective stiffness `c₁₄ − (½)²/(⅛) = c₁₄ − 2` (the −2 is the Einstein Hamiltonian constraint), and
eliminating the metric gives `C_eff = (2−K_B)[(2−K_B) − (2−c₁₄)J]/(2−c₁₄)`, sign change at
J = (2−K_B)/(2−c₁₄) = 0.9000009. **A health verdict from a test that could not reproduce the known kill would
be worthless; this one reproduces it — threshold, acceleration and growth rate, both footings.**

---

## 2. The galactic background, from the lead's own action (BG-1, BG-2, BG-3)

`IC30_RADIAL_BRIDGE.md` §2–3 is the lead's own static spherical reduction of the integrable-clock action. With
`N = e^Φ`, `h_ij = e^{−2Ψ}δ_ij`, `w = (u−1)Φ`, `S = (2−u)Φ`, `ξ = ln N = S+w = Φ`, the leading weak-field
quasi-static equations are

    Δ(Φ−Ψ) = 0,   (Ψ−Φ)″ − (Ψ−Φ)′/r = 0,   div[(1 − e^{−|∇Φ|/a₀}) ∇Φ] = ρ_b/(2m),   G_N = 1/(8πm),

and varying the clock's own acceleration invariant fixes

    |a|² = a₀² ln²(1−u²),   |a| = e^Ψ|Φ′|,   **u² = 1 − e^{−y} = μ(y)**,   y = |∇Φ|/a₀.

This is a genuine MOND background: **the MOND interpolation μ(y) = 1 − e^{−y} rides the clock's acceleration,
not a separate scalar's kernel** (exactly L66's structure identification, now on the galactic solve). Solving
`(1 − e^{−g/a₀}) g = g_N` for a spherical M_b = 10¹¹ M_⊙ source (the same model L60 used) gives, on the
canonical footing, r_M = 12.20 kpc and deep-MOND rows out to 200 kpc with g → √(g_N a₀) and v_c flat to 8%
(alt: r_M = 11.12 kpc). These are the L60 danger rows s = g_N/a₀ < 0.4 — the exact regime that kills the
deposited action.

**On the static (η=0) branch the trace momentum and auxiliary vanish (BG-2):** IC30 §2 shows E_q = E_s = E_z = 0
with t > 0, E4 ≥ 0, 2D > 3A²/t force the unique real root q = z = s = 0, i.e. **π = 0**. This is the
configuration the propagating sector must be perturbed about.

**But the background is fully specified only at LEADING order (BG-3).** IC30's own words: "not a full nonlinear
identity Φ=Ψ, a full PPN calculation, or a global matched galaxy"; and `IC18`, `IC30`, `IC35` **each explicitly
disclaim a matched galaxy solution**. The static leading-order MOND field exists; a completed galactic solution
does not.

---

## 3. The L60 mechanism does not reappear (MECH-1, MECH-2, L69-1)

**No lapse-channel subtraction (MECH-1).** Rebuilding IC20's reduced scalar Hamiltonian
`h(S,q,z,R) = −e^{2S}q²/(6v) − A(S)qz − e^S P0 − D(S)z² − E4(S)z⁴ − vR`, `v = e^{S+2wc}/2 + z²`, and evaluating
on the static q = z = 0 branch gives **H_Sq = ∂²h/∂S∂q = 0** (verified symbolically). So the clock-lapse Schur
`K = a − C²/(2M)` that L66 identified has C = 0 — **no subtraction**. There is no separate MOND scalar and no
`2(2−K_B)a^μ∂_μφ` coupling, so no `C_{n,φ} = (2−K_B)` mixing and no wrong-sign `(2−K_B)²/(2−c₁₄)` feed. The
L60 mechanism has no analog on the galactic background.

**No deep-MOND softening (MECH-2) — the decisive structural contrast.** L60 fires because the deposited
transverse stiffness `Σ_⊥ = J_Y = s/Δ → 0` in deep MOND, so a fixed positive subtraction (0.9) beats a
vanishing stiffness. The integrable-clock analog — the clock-lapse gradient coefficient
`B = m e^{S+2wc}(1−u²)` — carries `(1−u²) = e^{−y} → 1` as y → 0, so **B stays O(1) positive in deep MOND**
(B/m → e^{2wc} ≈ 0.95), while at the same accelerations the deposited J_Y falls to 0.06 and below.

| deep-MOND row (canonical) | s = g_N/a₀ | integrable-clock B/m | deposited Σ_⊥ = J_Y |
|---|---|---|---|
| 50 kpc | 0.060 | **0.73** | 0.27 |
| 80 kpc | 0.023 | **0.81** | 0.16 |
| 120 kpc | 0.010 | **0.86** | 0.10 |
| 200 kpc | 0.004 | **0.89** | 0.06 |

**Both reasons the L60 kill fires — the fixed subtraction and the vanishing stiffness — are absent.**

**L69 does not bind (L69-1).** L69's necessary condition is `Σ_⊥ > λ²/(κ_φ χ_lapse)`, where λ = C[n,φ] is
both the matter→scalar source and the wrong-sign feed. Action (II) has no separate scalar, so
**λ_eff = C = H_Sq = 0** on the static branch ⇒ the RHS is 0 ⇒ the condition collapses to `Σ_⊥ > 0`, which holds
(B and the curvature coefficient v₀ = e^{S+2wc}/2 are both positive in deep MOND). **This is exactly L69's own
"λ = 0" disjunct — its named escape route — realised structurally, and now verified on the galactic solve.** So
against the L60/L69 axis the verdict is **outcome (c): no lapse-channel subtraction, escaped in the galaxy, not
only at the design point.**

---

## 4. What is NOT settled: a genuinely under-determined sector and a distinct live concern

**The propagating health is UNDERSPECIFIED by the lead's action (SPEC-1).** The full transverse gradient
stiffness needs the reduced Hessian H_SS, H_RR, H_qR on a **curved** galactic background (R ≠ 0). The `−vR`
term shifts `H_SS` by `−v₀″(S) R = −R e^{S+2wc}/2` (verified symbolically), so whether `H_SS − 2Bk²` keeps the
negative sign that made L66's clock-lapse Schur **stabilising** at the design point now depends on the
coefficient functions A(S), D(S), E4(S) at galactic S. Those are pinned only at the cosmological design point
S = 0.1 by `design()`'s targets (A_*=E_*=0.1, H_SS=−3, H_Sq=0, cUV²=0.2) and extended by an exponential ansatz;
**IC31 §1 forbids extrapolation** ("No coefficient extrapolation outside the represented S interval is
allowed"), and IC20 §7's adverse control (H_SS = −1000) already gives finite-k ω² < 0. There is no calibration
relating the action's dimensionless S to a galactic potential. **The full L60-style transverse verdict cannot
be evaluated on the calibrated action** — this is the finding the task named as legitimate: the construction
cannot yet be tested to a verdict in a galaxy because this sector is uncalibrated.

**A distinct new-mechanism concern is live exactly on the galactic configuration (NEW-1, NEW-2).**
`AUXILIARY_SYMBOL.md`'s auxiliary transverse gradient Hessian, off the witness, is
`G = [[2αλ, βλ+2uξ], [βλ+2uξ, 2γλ+2ξ²]]` with `λ = ρ/ρ₀ ∝ (π/π₀)²`. At π = 0, λ = 0 and
**det G = −(2uξ)² = −4u²ξ² < 0** (reproduced symbolically). **π = 0 IS the static galactic branch (BG-2)**, and
there ξ = Φ ≠ 0 and u² = 1−e^{−y} ≠ 0 wherever there is acceleration — so the auxiliary principal symbol is
**indefinite exactly on the static galaxy** (in deep MOND the indefinite piece scales as u² ≈ y → 0, weakening
but not vanishing or changing sign). This is a **different mechanism** from L60's lapse-channel subtraction. The
lead's repair — a negative-semidefinite square `−mV e^{uξ}α|Dξ + bDu|²` — is constructed and matched **only at
the π ≠ 0 expanding cosmological witness** (ξ₀ = ¼, u₀ = ⅔, π₀ = −3mVe^{−1/2}h ≠ 0); its extension into the
π = 0 galactic deep-MOND regime is **uncomputed** (AUXILIARY_SYMBOL: "a separate construction must specify the
interpolation").

---

## 5. Verdict, in three sentences

**The integrable-clock action does NOT inherit the L60 deep-MOND lapse-channel kill in a galaxy — on the
galactic static MOND background it has no separate scalar, H_Sq = 0 so no wrong-sign subtraction, and its
clock-lapse gradient coefficient B ∝ (1−u²) = e^{−y} stays O(1) instead of softening to zero the way the
deposited Σ_⊥ = J_Y → 0 does, so both ingredients of the kill are absent and L69's condition collapses to the
satisfied Σ_⊥ > 0; this is outcome (c), confirmed to extend from the design point into deep MOND.** But it is
**not thereby a cleared live candidate**: the propagating-sector health that would decide it is UNDERSPECIFIED
by the lead's own action — the perturbation coefficients A(S), D(S), E4(S) are pinned only at the cosmological
design point S = 0.1, IC31 forbids extrapolating them to galactic S, and no S↔galaxy calibration exists — so
the full L60-style transverse verdict **cannot yet be evaluated**, and separately the IC-4 auxiliary-gradient
Hessian is indefinite (det G = −4u²ξ² < 0) exactly on the static (π = 0) galactic branch, repaired only at the
π ≠ 0 cosmological witness. **The honest one-line state is: L60's specific mechanism is provably escaped in the
galaxy, but the last construction is neither healthy nor killed there — it is blocked by an uncalibrated
coefficient sector and a distinct, unresolved indefinite auxiliary symbol at π = 0.**

---

## 6. What is open, named

1. **The perturbation coefficients at galactic S.** Until A(S), D(S), E4(S) are calibrated for a galactic
   background (with a stated S↔potential relation) and IC31's no-extrapolation rule is lifted by a principled
   extension, the sign of H_SS − 2Bk² on the curved galaxy — hence the propagating scalar's transverse
   stiffness — is not decidable. This is the single blocking item for a health verdict.
2. **The indefinite auxiliary Hessian at π = 0.** det G = −4u²ξ² < 0 on the static galactic branch is a
   distinct (b)-type channel; whether the lead's negative-semidefinite-square repair, built at the π ≠ 0
   cosmological witness, extends to π = 0 in deep MOND is the uncomputed question this lane hands forward.
3. **The nonlinear endpoint** (inherited from L60/L69): an under-determined linear sector is not a statement
   about where a background settles; it is a statement that the linear health cannot yet be read off.

κ = ½ remains fitted, and this lane never says otherwise. Nothing here is closed.
