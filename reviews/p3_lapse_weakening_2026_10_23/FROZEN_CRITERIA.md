# Does P3's strong-coupling estimate account for the weak-lapse regime? — FROZEN CRITERIA (before any script or number)

Owner's request (2026-10-23): "check whether P3's strong-coupling estimate accounts for the 1/(1+x)² weakening of v3's
lapse operator at high acceleration (Solar System), frozen criteria first, both footings, mutate." Inputs, read-only:
`rebuild_2026_10_22/P3_v3_strong_field/` (script sha256 1aaf59ad…cb67bb6d, results JSON) and
`reviews/v3_constraint_algebra_2026_10_23/` (V2's Schur complement S). κ = ½ FITTED; canonical a₀ = 9.36e-11 / alt
1.13e-10 m/s², never pooled. No dark-matter particle. Not theory closed. Small jobs, one thread, nice 15.

## What I found reading P3 before freezing (not blind; stated so it cannot steer)

- P3's kinetic coefficient is `Z_P = k²/(Q̄²(K M_L + γ_L k²))` (E1), and its unitary-gauge Schur complement E2(i) is
  `k²/(2N₀(K M_L + γ_L k²))`. Up to sign and normalisation this is my S at κ = 1, μ_K = 0, g₀ = 0. **So P3's formula
  carries the M_L = (1+x)² factor.** What matters is the value of M_L it is fed.
- In the lapse operator, **x is the background-P variable**: x = u₀/(a₀ − u₀), with u₀ = K|P₀|. It is not the local
  g/a₀. My v3 README called x = 1e9 "Solar-System accelerations"; that is a misidentification, to be corrected forward.
- P3's Solar-System/lab rows (Eot-Wash, planets, double pulsar) pass `M_kk = 1.0` and `u₀ = 2Φ/L★`. My hand estimate
  of the screened point-mass solution (r ≪ L★, u ≪ a₀) is K P = ∇(φ − Φ_N), so u₀ = GM/(c²L★²). That is ~(L★/r)
  smaller than 2Φ/L★, and 2Φ/L★ exceeds a₀/c² (W's domain is u < a₀). Then du = a₀ − u₀ < 0, and `scales()` skips the
  W-cubic vertex V6 for those rows (`if lh <= 0: continue`). The committed JSON confirms V6 is absent there.
- The Galaxy's own P at the Sun is unscreened (r ≫ L★), so the Solar-System background is P₀ ≈ P_e with
  x_e = g_gal/a₀ ≈ 1–3, M_L = (1+x_e)² ≈ 4–16, not 1. Expectation: this does not matter for P3's rows, because there
  kL★ ≫ √(2M_L) (Eot-Wash kL★ ~ 2e22), so γ_L k² dominates χ. Where the weakening is real is the unscreened
  high-acceleration interior of galaxies (r ≫ L★, x ≫ 1). Hand scaling in P3's own formulas, gapped regime
  k²/M_L ≫ μ_K²: ε_V1 ∝ M_L^(−1/2) (safer), but ε_V5 (K(Q) dust vertex) ∝ M_L^(3/2) (grows).

## Checks (`p3_weak_lapse.py`; P3's `scales()` and `zP_of()` are extracted verbatim from the hashed P3 script and run
read-only; `--mutate` described in W5)

- **W1 (identity, sympy).** With κ = 1, μ_K = 0, g₀ = 0 and k ∥ P₀: my S = −k²/(N₀(K M_L + γ_L k²)) = −2 × P3's E2(i)
  Schur, and −S·N₀ = Q̄²Z_P(N₀Q̄ = 1). PASS iff all residuals are 0.
- **W2 (the Solar-System x, both footings).** (i) sympy: the linear screened equations (∇φ = K P − γ_L∇(∇·P),
  ∇²φ = K(ρ + ∇·P)) give, for a point mass at r ≪ L★, K|P| = GM/(c²L★²) exactly to leading order in r/L★. (ii) Report
  u₀/a₀ for the Sun (1 AU) and the Earth (surface), and P3's 2Φ/L★ ÷ (a₀/c²). (iii) The Galactic x_e ∈ {1, 1.69 (v_c
  200 km/s at 8.2 kpc, canonical), 1.40 (alt), 2, 3} → M_L, M_T. PASS iff the Sun's u₀/a₀ ≤ 1e-4 at every L★ in P3's
  list {20, 24, 90} pc and both footings. Reading: the Solar-System lapse-operator x is x_e ~ 1–3, not g/a₀.
- **W3 (P3's rows with corrected inputs).** Rerun P3's `scales()` for its Eot-Wash, planets and double-pulsar rows
  with u₀ = a₀x_e/(1+x_e) (+ the Sun's screened value), M_kk = M_L(x_e) for every x_e in W2(iii) (and M_T as a bracket),
  du = a₀ − u₀ > 0, so V6 is now computed. **PASS iff** at every row/footing/L★/x_e: eps_max ≤ 1e-2 (P3's frozen
  line) and |eps_max/eps_max(P3 committed) − 1| ≤ 0.10. Reading: PASS ⇒ "P3's Solar-System strong-coupling verdict
  is unaffected; the V6 omission and M_kk = 1 were inert there".
- **W4 (where the weakening is real: unscreened galaxy interiors).** Spherical Hernquist models, AQUAL background
  (μ = x/(1+x)): G1 M = 1e11 M☉, a = 2 kpc; G2 M = 1e12 M☉, a = 3 kpc; G3 compact M = 1e11 M☉, a = 0.3 kpc.
  r ∈ logspace(log10(5 L★), log10(50 kpc), 40); x(r); u₀ = a₀x/(1+x); M_L = (1+x)²; K D·P from the AQUAL P* (G = K D·P
  (1 + γ_L D·P) + μ_K²(Q̄−1)/Q̄, Q̄ − 1 = 1e-6 as P3); k ∈ {3/r, 30/r, 1/L★}; ω = v_c/r. eps per vertex via P3's
  `scales()`. Both footings, L★ ∈ {20, 24, 90} pc. **PASS iff** eps_max ≤ 1e-2 everywhere (P3's frozen line). Reported:
  max x reached, the worst vertex, and eps vs M_L for V1 and V5 (the predicted M_L^(−1/2) and M_L^(3/2) trends).
- **W5 (MUTATE, sensitivity).** W4 rerun with M_kk = 1 and du = a₀ (the weakening ignored, as in P3's Solar-System
  rows). Required: the max over W4 of |log10(eps_max(mutate)/eps_max(W4))| ≥ log10 2. Otherwise W4 is insensitive to
  M_L and says nothing. Also W3 with u₀ = 2Φ/L★ restored: V6 must disappear again (reproduces P3's committed eps_max to
  1e-12 relative).

Not tested: P3's decoupling-limit method itself (O(1) loop factors, first order in background gradients), the
non-spherical saddles (H4's region), the BH cap rows (P3 already feeds them M_L at the cap), and the DBI K.

## AMENDMENT A1 (POST-RESULT; main run 5/5 PASS, MUTATE run kept)

Main run: W1–W4 and W5b PASS. MUTATE (M_kk = 1, du = a₀ in W4): max |log₁₀(eps_mut/eps)| = 4.41 ≥ log₁₀2, so W5a
PASS-as-required. The worst W4 eps rises from 3.4e-86 to 5.8e-85 when the weakening is ignored. **Disclosed
defect in a reported (non-gated) quantity:** the "d log eps / d log M_L" slopes (V1 +0.71, V5 +1.25) were fitted along
the radial profile, so r, k, G and ω vary together with M_L. The MUTATE run (M_L ≡ 1) also gives non-zero "slopes"
(+2.19 / +0.75), which proves the confounding. They do not test the hand trends (V1 ∝ M_L^(−1/2), V5 ∝ M_L^(3/2)).
Added, reported only: `p3_weak_lapse_partial.py` scans M_kk ∈ [1, 1e6] at fixed (r, k, G, ω, L★, footing), with
du = a₀/√M_kk tied as at the cap. It reports the partial slope per vertex in each regime (E = ω/c or c_π k;
Z_P ≷ μ_K²). No threshold; nothing in W1–W5 changes.
