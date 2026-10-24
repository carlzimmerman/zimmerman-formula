# O1_ownership_action — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, before any script or number)

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² (canonical / alt), never pooled. No dark-matter particle: the cold
sector is "cold energy", a field/medium. Not "theory closed". Nothing here says the data favour the framework.
Compute: one thread, `nice -n 15`, < 1 GB RSS, minutes. No downloads. All other lanes read-only.

## 0. The question

Z★ (Z1 DESIGN §2) needs rule R2, **ownership**: cold dust is held in the free-fall frame of the bound system that owns it.
R2 has no action. U1's T3 shows that in literal v3 held dust is weightless in a static host, so a falling satellite carries
none. Can any action in the v3s family (v3s + mimetic dust, local, one action) make ownership follow? Verdict:
**DERIVED** (name the action) / **CONDITIONAL** (one named cost) / **NO-GO** (theorem; name the must-keep that blocks it).

Coordinator addition (received before this freeze, so frozen here, not an amendment): evaluate **VS**, H5's velocity
screening (568a6b6709): a system moving at V through its host's held khronon holds a phantom only inside
r_cap = 2GM_b/V². Test (i) ownership by formation, (ii) removing γ_L (L★) against Cassini, the outer globulars, wide
binaries and the isolated RAR, (iii) the constant count; say plainly where it fails.

## 1. Must-keeps (pass lines; every one scored per candidate)

| id | must-keep | pass line (frozen) | source of the target |
|---|---|---|---|
| M1a | **OWN**: a satellite carries its held phase | the derived differential acceleration of the held phase relative to the satellite's baryons, ε = \|Δa\|/g_host, satisfies ε ≤ ε_B = 0.344 (canonical) / 0.317 (alt) at r = 50, 100, 250 kpc in the MW model (M_b 6e10 M☉, E_mid), **and** the internal law argument contains no host term | CFG945 (ε_B from CFG874's statistic) |
| M1b | satellites flat in host field | predicted d log g / d log x_e at fixed M_V inside 2σ of −0.05 ± 0.19, i.e. in [−0.43, +0.33] | Z2 README "Task 2", A1 item 3 |
| M2 | TDGs, DF2/DF4 dust-free and Newtonian | the candidate does not give them a held phase (they formed from material moving relative to the parent's khronon, r_cap < r½); U1's native B0 pass is kept | U1 README Part (c) |
| M3 | isolated field galaxies keep the phantom and the RAR | (i) isolated static limit is AQUAL with μ = x/(1+x), sympy residual 0; (ii) a galaxy assembled from N ≥ 2 progenitors keeps the same law (deviation ≤ 0.01 dex); (iii) no new term in the law | P4; U1 A2; CFG945 (two-label floor) |
| M4 | Solar-System screening / Cassini | anomalous quadrupole tide ≤ Hees 9.0e-27 s⁻² (and Park 5.2e-27), or the X3 lemma (D·P ≥ 0 within 1 kpc) untouched | D7d, C6, X3 |
| M5 | well-posedness | no c² < 0 introduced; no creation of negative held charge; no caustic of a new field forced within a Hubble time in a static host; X3's switch and H4's lesson respected | X3, H4, H5 |
| M6 | linear growth like dust | the new term vanishes on FRW at linear order, so s(k) = 1 (Z1 K8) | Z1 |
| M7 | constants | count continuous constants; a new one is allowed only if derived from a₀, L★, c, G, Λ | owner rule |
| M8 | one local action | variational, local, NR limit Galilean (Milne) invariant (CFG678) | owner rule |

## 2. Candidates (each: action term, sympy EOM of the held phase, its frame, M1–M8)

- **(a1)** baryon–khronon drag −(β/2)ρ_b\|v_τ − v_b\|². **(a2)** hard alignment v_τ = v_b where ρ_b > 0 (multiplier).
  **(a3)** the gate "\|Φ_int\| > \|Φ_ext\|" (locality check only).
- **(b)** hold argument relative to the owner's centre-of-mass frame: ∇Ξ → ∇Ξ + Ẍ_q, with a collective coordinate X_q tied
  to the owner's baryon centroid by a multiplier.
- **(c)** multi-stream particles (posited, as in L1) with the khronon velocity slaved to the local mean dust flow.
- **(d)** ownership by formation history inside v3s's own variables (memory test).
- **(e)** per-owner khronon fields τ_q (variational labels). **(f)** (e) plus an inter-label exchange V(τ₁ − τ₂).
- **(g)** reported only: Ξ-neutral (free) dust as the carried mass (Z★'s R1 release without R2).
- **(VS)** the coordinator's velocity screening + ownership by formation, with γ_L removed.

## 3. Derivations and checks (sympy residuals must be identically 0 unless a tolerance is given)

- **K1 (T-G)** Ξ = Φ − σ̇ + ½\|∇σ\|² is invariant under x = x′ + D(t), σ′ = σ + Ḋ·x′ + f(t), Φ′ = Φ + D̈·x′ (with f chosen);
  and ∇Ξ = ∇Φ + Dv_τ/Dt (the law argument is the khronon congruence's proper acceleration).
- **K2 (T-W, 1D exact)** for the 1D PN system with any odd increasing hold flux f, any local stiffness U(s) and any internal
  term that vanishes where ρ_b = 0, the total force on all matter in [z₁, z₂] is a boundary function B(z₂) − B(z₁),
  B = −Φ_z²/8πG + H(Ξ_z)/4πG − U-pressure, H(s) = ∫₀ˢ t f′(t) dt.
- **K3** H is even and strictly increasing in \|s\|; hence a composite with net held charge falls at the mean external field
  iff the ambient khronon gradients at its two edges are antisymmetric (ambient khronon unheld).
- **K4 (T-W, 3D)** linear-medium stress identity: force on a held charge q in a uniform external Ξ gradient E is qE
  (U1 D7 reproduced with this lane's code).
- **K5 (T-E)** spherical host, any khronon motion: \|∇Ξ_amb\| = f⁻¹(G M_τ,host(<r)/r²); for the static held AQUAL host
  f⁻¹(G M_ph/r²) = g exactly, so ε = 1.
- **K6 (T-N)** per-label khronons: separate continuity per label (Noether); N labels static in one galaxy give
  ∇·[(1 − N(1 − μ))∇Φ] = 4πGρ_b, floor at x = N − 1.
- **K7 (T-R)** a flat rotation curve has ∇×v_b = v_c/R ≠ 0; v_τ = −∇σ is curl-free.
- **K8 (T-X)** V(σ₁ − σ₂) makes ∂_tρ₁ + ∇·(ρ₁v₁) = −V′, ∂_tρ₂ + ∇·(ρ₂v₂) = +V′: the sum is conserved, each label is not,
  and charge pairs of opposite sign appear where V′ ≠ 0.
- **K9 (a1)** the drag term's σ Euler–Lagrange equation (the drag enters as a charge flux, not a force).
- **K10 (T-M)** v3s's P has no time derivative in the PN Lagrangian (β = η = 0): no memory variable.
- **K11 (T-C)** zero-charge exterior label flow is geodesic; radial infall from rest in a flat-curve host reaches the centre at
  t = √(π/2) r₀/v_c.
- **K12** record reproduced first: D10 per-cell Δχ²_Newton (JSON), U1 N5 satellite / Coma / TDG medians (JSON), Z1's r_s
  for a MW-like host (55 kpc ± 2), H5's r_cap ≤ 0.25 pc for its systems at their speeds.
- **K13** peak RSS < 1 GB.

## 4. Numbers (both footings)

- **N1** ε(r) at 20, 50, 100, 250, 400 kpc for (i) the held v3s host (AQUAL), (ii) Z★'s supply-edge statics beyond
  r_s = r_M√(f_s(f_s + 1)), f_s = 5.364.
- **N2** the largest fraction φ_max(r) of the host's phantom inside r compatible with ε ≤ ε_B (what OWN would cost the host).
- **N3** VS: r_cap for the Sun (V = 220 and 250 km/s), the four D10 globulars at H5's PROXY speeds and at V_apo,10 = 36 km/s,
  the Solar-System anomalous tide 2πG²ρ̄M☉/(V²r) at r = 1, 9.5, 30 AU with ρ̄ = 0.0447 / 0.0514 M☉/pc³ (X3/H4 Galactic
  phantom at the Sun), and the response suppression (ω_p r_M/V)² at r_M = √(GM☉/a₀).
- **N4** (g) reported: gas-loss fractions needed under "free dust only" (Δ = log₁₀(√(M_o/M_n) − 1), deep limit) vs Z★'s
  (Δ = ½ log₁₀(M_o/M_n)), for X1's four classes.

## 5. Verdict rules (frozen)

- A candidate is **DERIVED** if it passes M1–M8. **CONDITIONAL** if it passes M1–M6 with exactly one named cost in M7 or M8.
  **NOT VIABLE** otherwise; **EXCLUDED BY THEOREM** if a K-check theorem shows it cannot pass M1a together with M3 or M5.
- Overall: DERIVED if any candidate is DERIVED; else CONDITIONAL if any is CONDITIONAL; else **NO-GO** with the blocking
  must-keep named.
- VS tiles: Cassini PASS if N3's tide ≤ Hees and Park; outer globulars PASS if D10's Δχ²_Newton < 3.84 in all 18 cells
  **and** r_cap < r½ for all four at both speeds; WB = prediction only (Newtonian), no score; TDG/DF2/DF4 = U1 B0 carried
  over; isolated RAR PASS if the derived V_rel gives r_cap ≥ R_last; satellites and Coma UDGs **FAIL** if U1's B0 sits
  > 3 sd above the data (U1 N5) and Z2's V3D C2–C4 class is ROBUST; group members DEPENDS (U1 F5).

## 6. Mutate (`O1_MUTATE=1`, exit 1 by design)

- **Mu1** the satellite's held phase invisible to the host Ξ (charge seen by the ambient field set to 0): ε → 0, OWN passes,
  so the K5/N1 OWN line must flip.
- **Mu2** N = 1 label: the floor disappears, so the K6 floor check must flip.
- **Mu3** D10's Newton column replaced by its AQUAL column: the VS globular tile must FAIL.
- **Mu4** f replaced by an even (non-odd) flux: K3's "iff" must fail.
