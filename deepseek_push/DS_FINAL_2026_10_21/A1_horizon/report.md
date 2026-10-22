# A1_horizon — can κ = 1/2 be derived? and what exactly is "1/12 of the horizon"?

## Claim

κ = 1/2 is **not derivable** from the dimensional data {c, G, ħ, Λ, H}: the map
(a0, Λ, H, …) → κ has a free function in it, and the only pure-Λ dimensionless invariant,
ħGΛ/c³ = 2.8448e-122, is so small that every analytic coefficient function with O(1)
derivatives is constant to 122 digits — so κ is an *input*, not a consequence (no-go A).
Nor is it derivable from horizon entropy-cell counting: the specified strain-saturation
principle gives κ = 4√(π/3) = **4.093307**, missing 1/2 by the exact factor
8√(π/3) = **8.186614**, and a class theorem kills the whole family — every member has
κ² ∈ ℚ·π^(odd), hence κ irrational, hence κ ≠ 1/2 (no-go B). The "1/12" statement is
neither independent nor exact: it is the *same single equation* a0² = Λc⁴/32π rewritten
with 12 in place of the irrational 2Z = √(32π/3) = 11.5776201; read literally,
"a0 = 2cH/12" gives κ = Z/12 = 0.4824008, which is 3.52 % from 1/2. So "deriving the
twelfth" ≡ "deriving n = 1/κ = 2", and the integer 2 appears nowhere in any horizon count
(the count is N = 3.313e122). Status:
**NO-GO(obstruction)** for the derivability question, **DERIVED** for the arithmetic audit.

## Derivation

### 1. The one identity, exactly

All of §1 is exact algebra (K1–K3), written in SI with c explicit.

    (1.1)  a0 = κ c √(G ρ_Λ),   ρ_Λ = Λc²/(8πG),   H_Λ² = 8πGρ_Λ/3 = Λc²/3
    (1.2)  Z ≡ 2√(8π/3) = √(32π/3) = 5.788810036,   2Z = √(128π/3) = 11.577620073
    (1.3)  a0/(cH_Λ) = κ c√(Gρ_Λ) / (c√(8πGρ_Λ/3)) = κ·√(3/8π) = 2κ/Z
    (1.4)  κ = 1/2  ⟺  a0/(cH_Λ) = 1/Z = 0.1727471  ⟺  a0 = c²√(Λ/32π) = 9.354173e-11
    (1.5)  2√(32π/3) = 2Z because 32π/3 = 4·(8π/3); the sympy residual of (1.5) is 0 (K1)

Eq. (1.4) is the whole content of the "horizon coincidence": a0 is 1/Z of the horizon
surface gravity cH_Λ, *given* the two Einstein substitutions in (1.1).

### 2. "1/12 of the horizon" is eq. (1.4) with 12 substituted for 2Z

Define the pure number g ≡ 2cH_Λ/a0 ("how many a0-lengths make the doubled horizon
acceleration"). From (1.3), a0/(cH_Λ) = 2/g, so

    (2.1)  κ = Z/g            [erratum: earlier printings had (Z/2)/g; A62 proved the correct form, see A62 §6]
    (2.2)  g = 12   ⟹  κ = Z/12 = 0.4824008      ("the twelfth", taken literally)
    (2.3)  g = 2Z   ⟹  κ = 1/2 exactly           (the exact statement, 2cH/a0 = 2Z)
    (2.4)  12/2Z = 1.0364825,  i.e. the "twelfth" is 3.52 % away from κ = 1/2

So "1/12 of the horizon" and "κ = 1/2" are **the same equation**, differing only by the
substitution 2Z → 12; and that substitution is provably never exact: (2Z)² = 32π/3 is
irrational, while 12² = 144 is not. The "12" is not an integer that a derivation could
produce — it is 4√(8π/3) rounded. Deriving it would mean deriving 8π/3 (Einstein) *plus*
the integer n = 1/κ = 2. (Numerology control, K13: a0/(cH0) = 0.1429374 is 1/7 to 5.62e-4,
sixty times tighter than the 1/12 hit, and equally meaningless.)

### 3. Every place a factor of 2 can enter, and which of them are actually free

| entry point | factor in a0 | factor in κ | status |
|---|---|---|---|
| horizon radius R = c/H_Λ vs diameter 2c/H_Λ | 1 vs 1/2 | Z/2 ↔ Z/4 | free (geometry) |
| T = ħH/2π vs ħH/π | 1 vs 2 | Z/4π ↔ Z/2π | free (temperature normalisation) |
| entropy S = A/4ℓ_P² vs A/ℓ_P² | 4× in N → 2× (energy ∝ a²) | 2× | enters saturation principles only (3.3) |
| comoving vs proper radius | R/a(t) | — | **not free at the horizon** (3.2) |
| enclosed mass vs surface gravity | 1 | — | **identically 1** (3.1) |
| H_Λ vs H0 | — | ×H0/H_Λ = 1.2093036 | free, and it destroys the menu |

    (3.1)  For de Sitter, the enclosed vacuum mass and the Misner–Sharp mass coincide
           identically:  M = (4π/3)R³ρ_Λ = (4π/3)(c³/H³)(3H²/8πG) = c³/(2GH) = c²R/(2G).
           So "enclosed mass vs surface gravity" contributes NO factor. (K10, sympy)
    (3.2)  The Hubble radius is defined proper; a comoving radius is R/a(t) with a = 1 at the
           horizon by construction. Using the matter-era apparent horizon (3/2)c/H instead
           gives κ = 2Z/3 = 3.859207 — not a member of the quoted menu.
    (3.3)  The entropy normalisation never enters the *temperature* (Unruh/menu) route — only
           R and T do — so it is invisible in §4. It enters saturation principles through
           the per-cell volume: N → 4N gives V_cell/4, and since stored energy is quadratic
           in a, a0 → 2a0 (κ → 2κ). It is fixed by Bekenstein–Hawking, i.e. an external input.

### 4. The full menu, and the five quoted numbers

With κ = (Z/2)/g, the discrete ladder g ∈ {1/2, 1, 2, π, 2π, 4π, 8π} gives:

| g | κ | exact | what it physically is |
|---|---|---|---|
| 1/2 | **5.788810** | Z | a0 = 2cH_Λ: twice the surface gravity; equivalently T = H/π (GH temperature with R → c/2H) |
| 1 | **2.894405** | Z/2 | a0 = cH_Λ: the horizon surface gravity; Unruh T(a0) = T_dS |
| 2 | 1.447203 | Z/4 | a0 = cH_Λ/2: diameter used as radius, R = 2c/H |
| π | **0.921318** | Z/2π | a0 = cH_Λ/π = 2cT_dS: twice the de Sitter temperature, in acceleration units |
| 2π | **0.460659** | Z/4π | a0 = cH_Λ/2π = cT_dS: Milgrom's classic "a0 ≈ cH/2π" |
| 4π | **0.230329** | Z/8π | a0 = cH_Λ/4π = cT_dS/2: Milgrom's value with the diameter |
| **Z** | **0.5** | — | canonical; **not on the ladder** |

The five numbers in the task are exactly rows 1, 2, 4, 5, 6: 5.789 = Z, 2.894 = Z/2,
0.921 = Z/2π, 0.461 = Z/4π, 0.230 = Z/8π (K4: max deviation 4.05e-4, the 3-dp rounding).
The ladder is complete in the sense that every entry is a "which 2π and which radius"
choice; κ = 1/2 is **not** a member (K5): it needs g = Z = 5.788810, which is 0.494 away
from the nearest ladder point (2π). Equivalently (1/Z² = 3/32π = 0.0298416): at a0 the
stored strain energy is 2.984 % of one cell quantum, not 100 %.

Two further readings of the same ladder, for calibration:
- κ = 1/2 sits **8.540 % above** the Milgrom entry Z/4π (ratio 2π/Z = 1.085402). That 8.5 %
  is the well-known tension between a0 and cH/2π, and it is exactly the factor by which
  the Einstein 8π/3 bookkeeping differs from a pure 2π bookkeeping.
- With H0 instead of H_Λ every entry rescales by 1.2093036 (= 1/√Ω_Λ), so "0.461" would
  read 0.557. The five quoted numbers only reproduce with H_Λ; that choice is itself an
  unstated premise in the folklore.

### 5. No-go A — no function of {c, G, ħ, Λ, H} fixes κ

    (5.1)  Exponent matrix over (M,L,T) for (c,G,ħ,Λ,H): nullspace dimension 2 (K6),
           spanned by  ħGH²/c⁵  and  c²Λ/H²;  their product is ħGΛ/c³.
    (5.2)  Imposing H = H_Λ (the pure-Λ Friedmann identity, itself part of the theory)
           fixes the second combination to 1/3, leaving exactly ONE invariant
           x = ħGΛ/c³ = 2.8448e-122  (ln(1/x) = 279.87).
    (5.3)  Therefore the most general vacuum-tied acceleration is
           a0 = c√(Gρ_Λ)·F(x),  κ = F(x),  F arbitrary.
    (5.4)  F ≡ κ is an admissible function for every κ ∈ ℝ₊: the data {c,G,ħ,Λ,H} admit
           every value of κ. No function of them "fixes" it.
    (5.5)  If F is analytic at 0 with sup|F′| = O(1), |κ − F(0)| ≤ x·sup|F′| < 1e-120. So
           even the class of analytic F carries no information: κ = F(0), a pure number.
           Natural non-constant choices (√x = 1.69e-61, ln(1/x) = 279.87, 1/ln(1/x) = 0.00357,
           e^(−1/x) ≈ 0) miss 1/2 by ≥ 0.496 (K7).

Conclusion: κ requires a **discrete** principle — an integer count — not dimensional
analysis. (The brief's "unique dimensionless combination" holds only *after* imposing
H = H_Λ; with H free there are two, (5.1), and the second is fixed to 1/3 by the theory's
own Friedmann identity — which does not weaken the no-go.)

### 6. Candidate discrete principle P1: saturate the horizon's entropy cells

    (6.1)  N = S_dS = A/(4ℓ_P²) = πc⁵/(GħH²) = 3.313016e122 cells;  ℓ_P² = Għ/c³
    (6.2)  E_cell ≡ k_BT_dS = ħH/2π = 3.031589e-53 J, and V_cell = V/N = (4/3)Għ/(c²H)
           = 5.781030e-44 m³, i.e. an ℓ_cell = 3.866652e-15 m cube.
           Exact identity: ρ_Λc²V_cell = (3H²/8πG)c²·(4/3)Għ/(c²H) = ħH/2π = E_cell: the cell's
           *thermal* and *vacuum* energies agree identically — "cell's own energy" is unambiguous.
    (6.3)  Principle: the vacuum is elastic with the only modulus available, μ = ρ_Λc²; a
           uniform acceleration strains it by ε = a/(cH_Λ) (the fractional light-speed
           deficit, i.e. the Rindler strain, accumulated over one horizon); strain-energy
           density u = ½μ ε²; saturation when the strain energy stored in one cell equals
           that cell's own energy:  u(a0)·V_cell = E_cell.
    (6.4)  uV_cell = a²ħ/(4πc²H); setting = ħH/2π gives a² = 2H²c², i.e.
           a0 = √2 cH_Λ = 7.657900e-10 m/s².
    (6.5)  κ_P1 = √2·H/√(Gρ_Λ) = √2·(Z/2) = Z/√2 = 4√(π/3) = 4.093306832
    (6.6)  mismatch to 1/2: 8√(π/3) = 8.186613664;  a0 is 8.1815 × a0_can

P1 is a **constitutive premise**, not a theorem: μ = ρ_Λc² and ε = a/(cH_Λ) are choices
(there is no other modulus, and no other horizon-scale strain, available). The test is
whether the resulting κ is 1/2 — it is not, and §7 shows no constitutive variant reaches 1/2
without inserting Z. The principle therefore **fails**, exactly and unambiguously, by
8.19× (and, if adopted, it is also empirically dead: a0 = 7.658e-10 is 8.18 × a0_can, which
the rotation-curve scale excludes). Its variants (solved from their own SI functionals in K9):

| variant | change | κ | vs 1/2 |
|---|---|---|---|
| P1a | no elastic ½ (energy, not elastic energy) | Z/2 = 2.894405 | ×5.789 |
| P1b | cell capacity = 2 quanta (two DoF) | Z = 5.788810 | ×11.578 |
| P1d | surface-tension strain, dA = 2εA | Z/16 = 0.361801 | ×0.724 |
| P1c | strain measured with the *cell* length ℓ_cell | 1.757e41 | ×3.514e41 |

P1c is the diagnostic: attaching the strain to the cell size (3.87e-15 m) instead of the
horizon size (1.66e26 m) moves a0 by 40 orders of magnitude — a per-cell principle is a
statement about the ratio (cell scale)/(horizon scale), and only the horizon-normalised
choice is dimensionally sane.

### 7. No-go B — the whole class cannot reach a rational κ

Every member of the class has a0 = cH_Λ·(pure number), the pure number being assembled from
the discrete bookkeeping choices. Each choice contributes a factor from a fixed set:

    (7.1)  radius/diameter → 2^{±1};  A/4 vs A → 2^{±2} in N → 2^{±1} in a0 (energy ∝ a²);
           T = ħH/2π → π^{−1};  a = 2πT → π^{+1};  A = 4πR² → π^{+1};
           elastic ½ → 2^{±1/2} (because ε = √2).
           Hence  g = 2^(a/2) π^b  with a,b ∈ ℤ: integer powers of π, half-integer powers
           of 2 at worst. The class never produces π^{1/2} or 3^{−1/2}.
    (7.2)  κ = √(8π/3)/g   ⟹   κ² = (8π/3)/(2^a π^{2b}) = (8/(3·2^a))·π^(1−2b),
           a rational times an ODD power of π.
    (7.3)  π^(odd) is irrational (π is transcendental), so κ² and hence κ is irrational for
           every (a,b).  But κ = 1/2 ∈ ℚ.  Hence κ = 1/2 ∉ image(class). ∎
    (7.4)  Equivalently: κ = 1/2 needs g = 2√(8π/3) = 2^{3/2}·π^{1/2}·3^{−1/2}, i.e. a factor
           π^{1/2} and a factor 3^{−1/2}. Neither is producible — √π ∉ ℚ(π) (if √π = f/g
           for polynomials f,g then Xg² = f², but Xg² has a root of odd multiplicity at
           X = 0 and f² does not), and ℚ(π) ∩ ℚ̄ = ℚ, so √3 ∉ ℚ(π). The 3^{−1/2} is the
           Einstein 8π/3 normalisation itself, which is the whole point.

Corollary (check K11, 169 lattice points): the closest lattice member to 1/2 is
g = 2⁻⁴π⁴ = 6.0881 → κ = 0.4754, still 0.0246 away. **This is the theorem the task asked
for**: no counting of horizon cells with 2's and π's can produce 1/2, because such counts
carry √π (through H² = 8πGρ/3 and T = ħH/2π) and no integer count cancels it. To land on
1/2 one must insert 1/Z = √(3/32π) by hand — which is precisely the premise κ = 1/2.

### 8. The ħ "one quantum per cell" variant

    (8.1)  N·T_dS = (πc⁵/GħH²)(ħH/2π) = c⁵/(2GH) = M_h c²   identically (K10, sympy)
    (8.2)  N·T_dS = M_h c²  ⟺  ρ = 3H²/(8πG)   (solving (8.1) for ρ)
    (8.3)  hence this variant **is the Friedmann equation**, rewritten. It is an identity,
           not a constraint: it fixes no acceleration scale, and therefore no κ.

Read instead as fixing an acceleration (a0 = 2πT_dS = cH_Λ) it returns κ = Z/2 = 2.894405,
the row-2 menu entry, again 5.789× off. So the ħ variant neither succeeds nor fails
interestingly: it is empty as a κ principle. Its one virtue is (8.1) — an exact statement of
holographic equipartition (the dS entropy count at T_dS reproduces the horizon mass
exactly), which is why cell-counting *looks* like it should work and does not.

## Status

**NO-GO(obstruction)**. Sub-results: §1–§4 **DERIVED** (exact identities, K1–K5, K12, K13);
§5 **NO-GO** (the dimensional data underdetermine κ; the only invariant is 2.8448e-122);
§6–§7 **NO-GO** (the specified discrete principle gives κ = 4.093307, and the whole class has
irrational κ, so κ = 1/2 is unreachable); §8 **identity**, not a derivation. The missing
premise, named exactly: **a discrete principle that yields n = 1/κ = 2 as a count.** Nothing
in the horizon's bookkeeping produces that integer; it produces Z = 2√(8π/3) instead.

## Checks (a1_checks.py, 13/13 PASS, exit 0, 0.6 s)

- K1 2√(32π/3) − 2Z ≡ 0 (sympy), value 11.577620073
- K2 a0/(cH_Λ) = 1/Z exactly; both Einstein substitutions verified symbolically
- K3 a0/(cH) = 2κ/Z; g=12 → κ=Z/12=0.4824008; g=2Z → κ=1/2; ratio 12/2Z = 1.0364825
- K4 five quoted numbers = Z/8π, Z/4π, Z/2π, Z/2, Z to 4.05e-4 (3-dp targets)
- K5 κ=1/2 is not on the ladder; nearest entry is 0.039341 away; needs g = Z
- K6 nullspace dim 2 without the Friedmann identity, 1 with it; x = ħGΛ/c³ = 2.845e-122
- K7 every natural non-constant F misses 1/2 by ≥ 0.496; analytic F is F(0) to 1e-120
- K8 P1 solved by root-finding on SI energies: κ = 4.093306832, mismatch 8.186614
- K9 four variants solved numerically, closed forms matched to 1e-8; all κ²/π ∈ ℚ
- K10 N·T_dS = M_hc² ⟺ ρ = 3H²/8πG, identically (it is Friedmann)
- K11 169-point lattice: closest κ to 1/2 is 0.4754; proof in (7.2)–(7.4)
- K12 κ=1/2 → a0 = 9.354173e-11 vs a0_can = 9.36e-11 (0.06 %)
- K13 a0/(cH0) = 1/7 to 5.62e-4 — a tighter integer hit than 1/12, hence no derivation

Mutation control: `--mutate=m1..m4` each breaks only its targeted checks
(K1+K3; K2; K5+K9; K8) and prints MUTATION CONFIRMED. See MUTATE.md.

## What this does not do

- Does not prove κ ≠ 1/2 in nature. It proves κ = 1/2 is outside two well-defined classes:
  functions of {c,G,ħ,Λ,H}, and horizon counts carrying only integer powers of π.
- Does not exclude discrete principles that produce the integer 2 *directly* (a topological
  count, a polarization count, a two-sided diamond). Those are not cell counts and would
  need their own independent prediction; none is constructed here.
- Does not adjudicate the alt footing (a0 = 1.13e-10, BRIEF §4) or any data; no fits were run.
- Does not touch the turn-off y_t / Λ–a0 closure of BRIEF §1 (lane C2).
- The 0.065 % discrepancy between ρ_Λ computed from Λ (5.834769e-27) and the BRIEF's quoted
  5.831e-27 is inherited, not resolved here; it does not affect any ratio.

## Next

1. The only live route to κ = 1/2 is a principle that outputs n = 2 as a count. The three
   candidates worth pricing are χ(S²) = 2 (Gauss–Bonnet), two transverse graviton
   polarizations, and a two-sided causal diamond. Each must predict something besides κ;
   if the source is χ(S²) = 2 the value is topological and must be identical for
   Schwarzschild, dS and Rindler horizons — that universality is the falsifiable content.
2. Pre-registered discriminator between κ = 1/2 and the nearest menu entry Z/4π: the two
   differ by 8.54 % in a0, so a determination of a0 at 2 % would separate them at 4.27σ
   (3σ needs σ(a0)/a0 ≤ 2.847 %).
3. A revived strain principle must be horizon-normalised (P1c: the cell-normalised version is 40
   orders of magnitude wrong) and must contain 3/32π explicitly — i.e. premise insertion.
