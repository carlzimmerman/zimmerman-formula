# CFG965 derivation: can self-gravitating cold mass carry the L* stiffness?

Every equation below is checked by `cfg965.py` (check names in brackets). Units: K = 4πG, γ = γ_L = K L*²/2 = 2πG L*².
κ = ½ FITTED; footings never pooled; AQUAL μ = x/(1+x) only; not theory closed.

## 1. What NA-3 needs

The polytrope has two ingredients, and both must act on the **same** cold mass:
1. the stiffness acts on that mass's own density, p = (γ/2)ρ² = πG L*²ρ² [K5];
2. that mass feels its own Newtonian gravity: the −4πGρ Jeans term survives.

Then E[M] = ∫[−GM²/2r² + γ(M′)²/(8πr²)] dr gives γρ′ = −GM/r², i.e. ∇²ρ + (2/L*²)ρ = 0 [K2]. So ρ ∝ sin(kr)/(kr),
k = √2/L*, with edge πL*/√2 = 2.2214 L*, half-density radius 1.3403 L* and M = 4π²(L*/√2)³ρ_c [K1]. The scout's hand values
(L* = 77.6 / 90.0 pc; M = 3.9e6 / 6.1e6 M☉ at 0.6 M☉ pc⁻³) are reproduced to 0.3 % [K1].

## 2. The structural obstruction: the stiffness sits in the sector that cancels self-gravity

Wherever a live formulation writes the stiffness, it writes it on the medium's displacement or potential (the one
exception, CFG938's rejected local form (a), is in §4):
- canonical S2 + S3 (ID): −(γ/2)|∇P|² with ∇·P = ρ_c;
- CFG938: −(3γ/4K²)τ_μντ^μν of χ, where D²χ = Kρ_c (the medium's own potential);
- v3: −(γ_L/2)(D·P)², with the khronon density ρ_τ = D·P − μ_K²Ξ/K.

The same sector carries the hold (tether) W(K|P|) = u²/2K + W_rem(u). Its quadratic part u²/2K is the medium's own Newtonian
field energy with the opposite sign. CFG941's theorem D-T shows the deep law forces this coefficient to be exactly 1. One
Fourier mode (ρ_b = B cos kx, ρ_c = C cos kx) gives ⟨L⟩ = K B(B + 2C)/4k²: the C² term (self-gravity) is exactly 0 [K6].

So **any cold mass that carries the stiffness is held, and held mass has no linear self-gravity.** The scout's own
pre-flight noted this for the canonical action (CFG888 S4). The question left was whether some formulation has *untethered*
mass that still carries the stiffness. Sections 3–4 go through them.

## 3. The screened theory v3 (primary)

### 3.1 The equations
H4's PN Lagrangian (A1) is
L = −|∇φ|²/2K − ρ_mφ + P·∇Ξ − W(K|P|) − (γ_L/2)(∇·P)² + μ_K²Ξ²/2K, with Ξ = φ − σ̇ + |∇σ|²/2.
- The khronon fluid moves with v = −∇σ and feels the force −∇ψ = −∇φ + ∇Ξ.
- The P equation is ∇Ξ = [a₀u/(a₀ − u)]P̂ − γ_L∇(∇·P), u = K|P|.
- So v3's cold fluid is pushed by −γ_L∇(D·P). Where μ_K can be dropped, D·P = ρ_τ, and this is exactly the pressure
  πG L*²ρ_τ². **v3 gives its cold fluid the NA-3 equation of state.** The open question is self-gravity.

### 3.2 μ_K = 0: exact nonlinear statics, spherical [D1a–D1d]
- Cold dust at rest needs ψ = const, i.e. Ξ = φ + C. With P radial, 4πr²p = M(<r) (Gauss), so u = GM/r².
- Eliminating φ on shell turns the v3 static Lagrangian into minus CFG938's E[M] exactly [D1a].
- Euler–Lagrange [D1b]:

  **γ_L D′ = u²/(a₀ − u) − g_N,b**,  D = ∇·P.

- With baryons, this is the screened law R(u) = g_N,b + γ_L D′ (CFG938 S2d2). At γ → 0 it is g_N = g²/(g + a₀) [D1c].
- **With no baryons, D′ ≥ 0 everywhere: an isolated lump's density can only rise outward.** The hold returns the lump's own
  field u, plus u²/(a₀ − u), so the net self-force points outward. The stiffness then pushes outward as well.
- Numerically, from central fields u(L*)/a₀ = 0.001 / 0.05 / 0.2 / 0.5, the density rises monotonically (by ×1573 / 33 / 9.0 /
  4.0) until the hold cap u → a₀ at r = 25.1 / 5.09 / 2.46 / 1.38 L*. There is no edge [D1d].
- Velocity dispersion only adds outward support (U1 T1, D4), so the cold case is the most favourable.

### 3.3 Linear dispersion [K3, K4]
ω² = ρ_τ[k²/χ − K], χ = k²/(KM_θ + γ_L k²) + μ_K²/K (H4, reproduced exactly).
- The compliance is a sum of two springs in series, the P sector's k²/(KM_θ + γ_L k²) and the BS dust's μ_K²/K.
- At μ_K = 0: ω² = ρ_τ[K(M_θ − 1) + γ_L k²]. The stiffness is there; the self-gravity −K is over-cancelled, because
  M_θ ∈ [1 + x, (1 + x)²] ≥ 1. This is CFG938 S5a term by term, via M_L − 1 = R′ and M_T − 1 = R/u [K4].
- The NA-3 dispersion ρ(γ_L k² − K) would need M_θ = 0, i.e. no hold. There is then no Jeans-marginal scale at all [D2e].

### 3.4 μ_K > 0: v3's self-gravitating BS dust [D2a–D2c]
On scales k ≲ μ_K the BS dust feels its own gravity again (U1). The static (ω = 0) condition is

  γ_L k⁴ + [K(M_θ − 1) − μ_K²γ_L] k² − K M_θ μ_K² = 0  [D2a].

- The regular bounded static mode is D ∝ sin(k_s r)/(k_s r), with ρ_τ = (M_θ + L*²k_s²/2) D [D2c]. So **v3's self-bound
  K-dust lump has the n = 1 shape.** Its size is set by k_s(μ_K, L*, M_θ), not by L* alone.
- Limits at M_θ = 1 [D2b]:
  - μ_K L* ≫ 1: k_s → μ_K. This is the record's own π/μ polytrope (H2 line 80: "π/μ ≥ 3.1 Mpc for μ ≤ 1").
  - μ_K L* ≪ 1: k_s² → √2 μ_K/L*, the geometric mean of the two scales.
- NA-3's k_s = √2/L* needs μ_K L* = s* = √(2M_θ/(1 + M_θ)), which is 1 at M_θ = 1. That is a coincidence relation between
  two constants, which the theory does not contain.

### 3.5 Numbers (`cfg965_results.json` → D2)
- **Targets:** CFG877's r_t (198.98 pc canonical, 162.56 pc alt) as the edge, and CFG870's r_c = 104 pc as the half radius.
- **Hold bracket:** M_θ ∈ {1, 1 + x_cl, (1 + x_cl)²}, where x_cl = G M_cl/(r_t² a₀) = 0.1975 on both footings. That value is
  ≈ 16/81 by CFG877's construction, so it carries no data information.

| L* (canonical / alt) | 1/μ_K needed | μ_K needed (h/Mpc, h 0.674) | × BS cap 14.8 | × growth 411 | d ln R / d ln L* |
|---|---|---|---|---|---|
| D10 floor 21.68 / 22.85 pc | 94–269 / 88–194 pc | 5.5e3–1.6e4 / 7.6e3–1.7e4 | 372–1063 / 516–1141 | 13–38 / 19–41 | 0.07–0.49 / 0.10–0.48 |
| E4 native 28.85 / 29.12 pc | 91–207 / 85–156 pc | 7.2e3–1.6e4 / 9.5e3–1.8e4 | 485–1102 / 642–1182 | 17.5–40 / 23–43 | 0.11–0.48 / 0.14–0.47 |
| 90 pc | 69–89 / 64–72 pc | 1.7e4–2.2e4 / 2.1e4–2.3e4 | 1122–1462 / 1384–1575 | 40–53 / 50–57 | 0.21–0.33 / 0.21–0.30 |
| soft edge 2.04 / 2.14 kpc | 55–63 / 52–55 pc | 2.3e4–2.7e4 / 2.7e4–2.9e4 | 1581–1826 / 1826–1936 | 57–66 / 66–70 | ≤ 0.002 |

- **Allowed range:** the smallest requirement over every cell, at the most favourable h = 0.73, is **344 × BS24's cap**.
  No allowed μ_K exists [D2d].
- **Literal-K BBN line:** every requirement sits below it (ratio ≤ 1.6e-4), so the literal quadratic K would still have no
  radiation era (Q6). Only the DBI K (Q7) escapes that.
- **What the size measures:** the elasticity d ln R/d ln L* is at most 0.49 and falls to 0.07 once the hold excess M_θ − 1 is
  included. A dwarf lump's size would therefore measure μ_K (and the hold), not L*.
- **At the BS cap:** the v3 lump is 3.9–38.5 kpc across the L* window at M_θ = 1, and 128–173 kpc with the hold bracket.
  To get NA-3's radius at the cap, μ_K would need to be 47–5019 × the cap.
- **The record's halo warning:** above the cap, the record says, v3's dust "forms galaxy halos and double-counts against the
  law" (THEORY_V3_DRAFT line 64; CFG946). At the required 1/μ_K ≈ 50–270 pc the dust would self-gravitate in every galaxy.
  That is not tested here.

### 3.6 v4 (AeST + γ_L)
S4 shows v4's spherical statics are v3's with μ_K → μ (THEORY_V3_DRAFT line 87), so the same algebra applies. H2's
constraint C3 (μ ≤ 1 Mpc⁻¹) puts every requirement at ≥ 3714 × the bound. v4 is also ill-posed off symmetry (I1).

## 4. The other formulations (table in `cfg965.out`, citations checked 29/29) [D5a]

| formulation | stiffness on own density | linear self-gravity | NA-3? | live? |
|---|---|---|---|---|
| canonical S2 + S3 (ID) | yes | none (critical quadratic) | no: statics = §3.2 | yes |
| canonical S4 free population | not written | Newtonian | no: no action for it | (postulate) |
| CFG938 parent, χ-tidal stiffness | yes | none (S5a) | no | yes (CONDITIONAL) |
| CFG939 single medium | yes | none (D-T) | no | yes |
| class A (CFG541/638/882) | no (bath σ_J² pressure) | Newtonian | no | yes |
| **CFG941 R1** (W_full → W_rem) | yes | Newtonian | **yes** [D3] | **no**: law fails 1.64 / 1.88, NOT REPAIRABLE |
| CFG941 R2 (two populations) | free population: no | free: Newtonian | no | no |
| CFG941 R3n / R3θ / R3ℓ | the switch removes it along with the tether | where off: Newtonian | no | no (R3θ: ghost) |
| **CFG938 local EOS (a) + tether off** | yes | Newtonian | **yes** [D4] | **no**: BBN if the medium exists then; switch unwritten |
| CFG848 | no (zero-stiffness force) | free: Newtonian | no | no |
| SCT (CFG953) | no (R0–R9 have none) | Newtonian | no | no (SCT-M retired after CFG960 SC1x) |

- **R1 lump [D3].** γρ′ = −u + u²/(a₀ − u). Its edge is R/L* = 2.2215 at u → 0 (1.00004 × πL*/√2), and 2.273 / 2.337 /
  2.532 at u(L*)/a₀ = 0.05 / 0.1 / 0.2. This is the NA-3 lump, in a variant that breaks the galactic law.
- **CFG938 local EOS [D4].** ε_int = (γ/2)ρ² gives p = πG L*²ρ². With Newtonian self-gravity this is NA-3 exactly. CFG938 S2d3
  gives ε_stiff/ε_rad at BBN as 1.3e3 (24 pc) to 2.3e6 (1 kpc), and 10 % of radiation at z = 3.5e6 / 8.3e4.
  - A population that first becomes free after z ≈ 8e4 would escape that bound.
  - The remaining obstruction is that no formulation writes this term for the free population, or writes the switch
    (CFG938 B1 UNTESTED; THEORY_CANONICAL 10-18: S4 is not derivable from the single medium).

## 5. What a formulation would need (not proposed here)

1. A local internal energy (γ/2)ρ_f² for the **untethered** population, with the same γ as the tethered sector's χ-tidal
   term. That is two different stiffness terms sharing one constant.
2. A written untethering switch (CFG938 B1).
3. It must also avoid CFG941 R2's failure, where free mass enters the law's source.

Even then, the lane would have derived only the clump's size, not its mass.

## 6. Controls

- **K1–K6** reproduce the scout's hand numbers, H4's dispersion, the H4 ≡ CFG938 identity, and CFG888 S1/S4 exactly.
- **MUTATE** (c₂ = 0: the hold loses its critical quadratic) behaves as frozen.
  - K3, K4 and K6 fail, because the record's dispersions and the mode cancellation are no longer reproduced.
  - D1c fails, because the law is lost.
  - D1d fails: the v3 lump now has an edge, R/L* = 2.2224 at u(L*)/a₀ = 0.001 (1.0004 × πL*/√2).
  - D2e fails: the μ_K = 0 static wavenumber becomes √2/L*.
  - The outcome flips to A-PASS.
  - Result: 11/18 PASS, exit 1 (`cfg965_MUTATE.out`, `cfg965_results_MUTATE.json`).
