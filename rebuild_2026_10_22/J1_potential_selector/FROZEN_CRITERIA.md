# J1_potential_selector — frozen criteria (written before any script or number; committed alone with the ledger)

Lane of the 2026-10-22 rebuild (`rebuild_2026_10_22/BRIEF.md`; `covariant_push_2026_10_22/BRIEF.md`; doors `BRIEF.md`,
`BRIEF_E_AUDIT.md` apply). κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. No
dark-matter particle. Never "theory closed". Never "the data favour the framework".

## Question

Is the depth of the local gravitational potential, |Φ|/c², the selector of the law's open excesses (cluster cores,
F1: data/law 1.68–1.85 canonical / 1.54–1.70 alt at MID; dwarf satellites, E3: +0.89 ± 0.13 dex above the screened
prediction), while isolated galaxies and the Solar System stay on the law? An EMOND-like idea (cf. Zhao & Famaey; Hodson &
Zhao 2017, A&A 598, A127, arXiv:1701.03369 — in the record only as `citations/works/hodson-2017-*.md`; their functional
form is NOT used or claimed here; the form below is this lane's own frozen choice).

Record checked before freezing: CFG914 (density threshold: NO COMMON ORDERING), CFG919 (kinematic selector: CONTRADICTED),
CFG921 / CFG928 (five posits P1–P5: none survives all facts; P1 = baryonic potential depth w r12 g_bar/c_*², internal only,
calibration impossible), H2 (AeST μ²Φ dust: wrong shape), opus_48 cluster review (density-a₀ route; SPARC environment
test d log a₀/d log(1+δ) = +0.052 ± 0.043). None tested the TOTAL potential depth including a host's potential as an a₀
multiplier. This lane does that, and does not repeat any of those selectors.

**Disclosed before freezing (not blind):** an order-of-magnitude estimate in my head says a satellite at 30–250 kpc from
the Milky Way sits in a SHALLOWER host potential than the Sun at 8 kpc. The test below is built to show this with numbers,
not to assume it.

## Part A — is a Φ-dependence in the action? (DERIVED / COMPUTED, sympy)

Premises: v3 static Lagrangian (C4, from BS24 Eq. 6 as transcribed there): N = e^{ψ/c²}, A_i = ∂_i ln N, Y = A·A/c⁴,
Q = 1/N (τ = t static), L ∝ N√h[−2J(Y) + 2K(Q)], K = μ²(Q − 1)²; A33/v3 clock term P^i D_i ln N; v4 (AeST, SZ21 via
H2): ∇²Φ̃ + μ²Φ = 4πGρ, K = −2Λ + K₂(Q − Q₀)², Q = (1 − Ψ)Q₀.
Checks (K6, sympy, residuals must be 0):
- (a) Y and the clock term P^i ∂_i ln N are invariant under ψ → ψ + C (a constant lapse rescaling = time reparametrisation).
- (b) The J sector obeys L_J(ψ + C) = e^{C/c²} L_J(ψ): its only Φ-dependence is the overall √−g = N factor, a
  post-Newtonian factor 1 + O(Φ/c²) (size ≤ 1e-5 in clusters).
- (c) The K(Q) sector is the only term not shift-covariant; its static Euler–Lagrange contribution is linear in ψ with
  coefficient ∝ μ² (the hydrostatic dust δρ = −μ²Φ/4πG, H2), with a free zero point.
Reading, frozen: if (a)–(c) hold, the action has **no a₀(Φ)**. Its Φ-dependence is (i) PN, too small by ~1e5 for a
×1.7–3 effect, and (ii) the μ² dust term, whose cluster shape H2 already excluded. Any a₀(Φ) used in Part B is then a
**POSTULATED addition: one function + one constant Φ_*, counted** (+1 function, +1 constant).

## Part B — the data test (one constant, set on one dataset)

**Form (frozen, chosen before looking):** a₀_eff = a₀ (1 + |Φ − Φ_ref| / Φ_*), Φ_ref = 0, applied pointwise in the
spherical AQUAL law g = ½g_N + √(¼g_N² + g_N a₀_eff) (μ = x/(1+x), F1's `g_aqual_sph`) and in E3's screened B_scr with
a₀ → a₀_eff. φ_* ≡ Φ_*/c² is the one constant, per footing.
**Potential (frozen, primary):** the Newtonian potential of the baryons, zero at infinity, superposed over the system and
its host(s): Φ = Φ_system + Φ_MW + Φ_M31 (hosts as Hernquist spheres, MW 6.0e10 M☉ (CFG332, E3), M31 1.0e11 M☉ (E3),
a = 3 kpc (D10/A60)). Clusters: from F1's own baryon model (gas β-model × (1 + f*), F1 PRIMARY). SPARC: spherical
integral of g_bar over the rotmod radii plus a Keplerian tail beyond the last point. Φ_ref = 0 is the far field.
Not used (reason): the law's own potential (log-divergent, needs a reference radius = a second constant). The monotone
bound M below covers it.

**Calibration (CAL).** F1 PRIMARY configuration exactly (AQUAL, native h 0.672 and 0.686, eRASS1 gas rescaled, β-model,
f* 0.20, data boost, catalogue miscentring), F1's measurement cache, per-band amplitude statistic and 30-patch jackknife.
Solve A_MID(φ_*) = 1 by bisection in log φ_* ∈ [1e-9, 1e-2], per footing and per h. CAL PASSES iff a root exists
in every cell. (Reported, not graded: the same with F1's A1 boost clipped at 1.)

**Predictions with no refit** (each footing at its own φ_*; graded at the h 0.672 φ_* and again at the h 0.686 φ_*; a
line passes only if it passes in both):
- **O1 cluster OUTER (first out-of-sample):** |A_OUTER − 1| ≤ 2σ_OUTER AND the per-bin profile χ² of A_k − 1 over bins 3–7
  (0.46–3 Mpc, 30-patch jackknife covariance with the Hartlap factor) ≤ 11.07 (5 bins; H2's line). Reported: INNER.
- **(a) SPARC RAR:** CFG914/CFG828 loader and cuts (q ≤ 2, i ≥ 30°, eV/V < 0.10, Υ_d 0.5, Υ_b 0.7); law = AQUAL ν of
  μ = x/(1+x). σ_i² = (2 eV/(V ln10))² + (0.10 dex)². PASS iff Δχ² = χ²(selector) − χ²(law) ≤ +9. Reported: Δχ² with a
  0.05 dex floor, small (M_b ≤ 3e9) and large galaxies separately, median shift in dex.
- **(b) dwarf satellites:** E3's 45 / 46 sub-threshold systems, E3's own build (Arroyo free-f binaries, MC, bootstrap
  median), screened B_scr at L★ = 24 pc with a₀ → a₀_eff(Φ at the system: own baryons at r12 + MW at distance_gc + M31 at
  distance_m31 from the LVD files). PASS iff the bootstrap median of the residual above the selector's screened prediction
  is within 2 sd of 0. Otherwise FAIL by the residual (dex).
- **(c) isolated field dwarfs and tidal dwarfs:** LVD local-field dwarfs with σ (all masses) and Lelli+2015's six TDGs
  (`real_research/data/tdg/lelli2015_tdgs.csv`; host as a point mass with M = g_Ne a₀,L15 D_p²/G, Φ = −g_Ne a₀,L15 D_p; D_p
  projected, so |Φ| is an upper bound). PASS iff the selector moves the predicted log g by ≤ 0.05 dex (median) and
  ≤ 0.10 dex (every system). Reported: the TDGs' data vs the isolated law (context; the base law's business, not graded).
- **(d) Solar System:** ε☉ = a₀_eff/a₀ at the Sun (MW Hernquist at R₀ = 8.122 kpc, plus the Sun's own potential at 1 AU).
  Conservative scalings of C6's margins: planets (Mars at L★ 24 pc: 0.173 of its bound) ∝ ε; Cassini Q₂ (max 3.6e-8 of
  Park) ∝ ε². PASS iff 0.173 ε☉ < 1 and 3.6e-8 ε☉² < 1.
- **(e) wide binaries (screened):** γ_v − 1 = 8.1e-6 (C6, L★ 24 pc) × ε☉² < 1e-2 (below any DR4 reach). PASS iff true.
- **M monotone bound (structural, graded with (b)):** for each satellite, the ε_need that closes its residual alone
  (central values, E3's screened B_scr). For ANY selector monotone in |Φ| and ANY host potential that deepens inward,
  ε(R☉) ≥ ε(satellite) whenever |Φ(R☉)| ≥ |Φ(satellite)|. Reported: fraction of satellites shallower than the Sun, median
  ε_need, and the Milky Way's predicted circular-speed inflation at R☉ (Hernquist MW, law) if ε(R☉) = median ε_need.

## Verdict rule (per footing, then both)

- **SELECTOR WORKS:** CAL, O1, (a), (b), (c), (d), (e) all PASS.
- **FAILS:** CAL impossible; or (b) FAILS and at least one of O1 / (a) FAILS.
- **PARTIAL:** otherwise (state which pass and which fail).
Part A's tag (DERIVED-from-action vs POSTULATED) is attached to whichever verdict results.

## Checks (script `j1_potential_selector.py`; one line each, exit 0 iff all pass)

- K1: F1's own reproduction checks (K1, K2, K4, K5, K6 from F1's exec'd input section) all PASS: same data.
- K2: φ_* → ∞ reproduces F1's committed PRIMARY A_MID and A_OUTER (both h, both footings) to ≤ 1e-6 relative.
- K3: the SPARC loader gives CFG828's n_sparc (2696).
- K4: φ_* → ∞ reproduces E3's residual above the screened prediction (canonical +0.886, alt +0.846) within 0.03 dex.
- K5: the cluster potential integrator on a Hernquist sphere matches −GM/(r + a) to ≤ 1e-3 at 0.05–10 Mpc.
- K6: Part A sympy identities (a)–(c), residuals 0.
- `--mutate`: the cluster potential keeps only −GM(<r)/r (drops the outer-shell term): K5 must FAIL; outputs in
  `*_MUTATE.*`.

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, single thread, minutes, no downloads. F1's KiDS cache and measurement
cache are read from session scratch (path as argv[1]); nothing of another lane is written.
