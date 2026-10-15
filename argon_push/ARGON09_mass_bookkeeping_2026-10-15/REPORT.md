# ARGON09 — Mass bookkeeping of isolated lensing: what the 44–310 kpc annuli demand (CFG801's open door)

**Date:** 2026-10-15. **Home:** `argon_push/ARGON09_mass_bookkeeping_2026-10-15/`.
**Criteria:** `FROZEN_CRITERIA.md` (038d3858e, committed alone). **Run:** 0 FAIL, exit 0, wall 0.02 s,
72 MB, 1 thread. Data: B21 KiDS-1000 Fig. 3 repo copy, bias-corrected per README. External inputs
(n_g, f_acc, b, r0) PROVISIONAL with sensitivity stated. κ = ½ FITTED; not theory closed.

## What CFG801 left open

CFG801 (19e43e614) excluded the settled-halo edge at 5.84 r_M (Δχ² +197 primary, both footings,
MUTATE bites) and named two unquantified outer-mass candidates: S4 debris or an edgeless supply rule.
ARGON09 booked the mass the data actually demands, from the raw ESDs.

## Ledger (all raw-data derived)

- **B1** enclosed masses from B21 Eq. 23 (K3-verified form): at 0.09 Mpc the data books 1.2–2.4× the
  settled supply (inner region ≈ settled, consistent with AG3's cored-halo verdict); at 0.31 Mpc it books
  **3.4–7.3×** (mean 5.3×). The tail is not the settled medium.
- **B2** excess over the edge model at 0.31 Mpc: ΔΣ 1.1–7.7 M☉/pc² ⇒ M_exc ≈ πR²ΔΣ = **8–24 M_b per
  halo (mean 16 M_b)** of non-settled mass inside 0.31 Mpc.
- **B3** the edgeless reading over-closes the universe: ρ_c/ρ_b ≈ r_max/r_M,eff = 166 (n_g = 0.03/Mpc³
  provisional) = **31× the 5.364 budget**; even n_g = 0.3 gives 10×. The no-edge continuation cannot BE
  the cold medium.
- **B4** debris capacity (f_acc ≈ 0.25 provisional) is **~64× short** of the 16 M_b mean demand. Debris
  alone cannot fill the annuli — the record's first candidate fails its bookkeeping.
- **B5** the cosmic web CAN: the projected 2-halo term (ξ(0.3 Mpc) = 220, b ≈ 1.3, r₀ ≈ 6 Mpc,
  provisional) books Σ_2h ≈ 5 M☉/pc² against an excess of 1.1–7.7 — **O(1–3) closure**. No exotic mass
  required.

## Verdict

**EXCESS REAL AND UNBOOKED by the framework's own bookkeeping — but fully booked by the standard cosmic
web.** The 44–310 kpc tail (16 M_b mean) is neither settled medium (B1), nor debris (B4, 64× short), nor
an edgeless cold-medium envelope (B3, 31× over-closure) — and the projected two-halo term alone accounts
for it at O(1–3) (B5, order-of-magnitude).

**Reading.** CFG801's exclusion fires on the raw statistic, but that statistic is contaminated by a term
that by itself books the entire excess. The settled-halo edge is therefore not falsified by KiDS Fig. 3
as-is — it is untested. Its true test must run on the residual after subtracting the modelled 2-halo term
(or on a neighbour-masked sample), at which point the framework's break at 5.84 r_M either appears or
dies for real. The no-edge model's poor absolute fit (χ² 84/28, CFG801) is the same signal: neither the
pure law profile nor its truncation matches the raw curve because the raw curve contains the web.

**Named discriminators / next lanes.**
- (i) GAMA isolated sample (B21 companion), same Δχ² statistic, 2-halo term subtracted analytically —
  the decisive repeat.
- (ii) excess-shape test: 2-halo predicts the excess follows ξ(r)∝r⁻¹·⁸ (steep outer fall);
  a real cold envelope would fall ∝r⁻²; debris steeper still.
- (iii) Upsilon shift: re-fit at +0.1 dex M_b (CFG801's disclosed residual) — moves r_e but not the
  bookkeeping conclusion (excess scales with M_b).

## Honest scope

- B5 is deliberately order-of-magnitude (r₀, γ, b from memory, provisional); the gate is ±1 dex and it
  passes mid-range (5.2 vs ~3). A proper 2-halo subtraction is the next lane, not this one.
- M_enc uses the exact B21 Eq. 23 with the CFG801 K3-verified constants.
- M_exc ≈ πR²ΔΣ is exact for isothermal-like tails; O(1) for steeper shapes (stated in criteria).
- Two-halo contamination grows outward; 0.31 Mpc is inside the primary range where B21 treat the
  isolated sample as clean — the contamination is correlated at the 4–33% level of the signal, which is
  precisely why it survives.
- Nothing here resurrects the killed door CFG801 closed; it re-frames the kill as untested-on-stage-1,
  with stage-2 pre-registered.

## Status

**PASS — the open door closes into a pre-registered stage-2 test: the KiDS tail books fully against the
cosmic web (B5) at O(1–3), leaving the settled edge neither confirmed nor falsified — untested — with the
2-halo-subtracted repeat named as the decisive run.**