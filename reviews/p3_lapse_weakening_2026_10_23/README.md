# Does P3's strong-coupling estimate account for v3's weak-lapse regime? — RESULT

Owner's request (2026-10-23). Criteria `FROZEN_CRITERIA.md` committed `30871e8eef` before any script; AMENDMENT A1
(post-result) discloses a confounded reported slope and adds a controlled scan. κ = ½ FITTED. Footings canonical / alt,
never pooled. No dark-matter particle. Not theory closed. P3's code is run read-only from the hashed script (sha256
1aaf59ad…cb67bb6d); its functions are extracted verbatim.

## Verdict: YES — P3 accounts for it where it can matter. The Solar System is unaffected. Two inert P3 input defects.

1. **P3's formula already carries the factor (W1).** P3's Z_P = k²/(Q̄²(KM_L + γ_Lk²)) and its unitary-gauge Schur
   complement E2(i) are the same object as v3's lapse-operator Schur complement S
   (`reviews/v3_constraint_algebra_2026_10_23/`, V2). S = −2 × P3's Schur and −S·N₀ = Q̄²Z_P, with residuals 0.
   "The 1/(1+x)² weakening" is P3's M_L.
2. **In the Solar System, x is not g/a₀ (W2).** In the lapse operator, x is the background-P variable
   x = u₀/(a₀ − u₀), with u₀ = K|P₀|.
   - The Sun's screened P has K|P| = GM/(c²L★²) exactly (sympy, linear screened point mass), so u₀/a₀ = 1.5e-7 to
     3.7e-6 across L★ 20–90 pc on both footings.
   - The unscreened Galactic P at the Sun gives x_e ≈ 1.4–1.7 (v_c ≈ 200 km/s at 8.2 kpc), bracketed 1–3. So M_L is
     only 4–16, never (1e8)².
   - **Correction to the v3 README:** its "x = 1e9 (Solar-System accelerations)" was a misidentification. x ~ 1e9
     needs P near the cap, which screening prevents in the Solar System. A correction note is added there.
3. **P3's Solar-System rows are unaffected (W3).** Rerunning P3's own `scales()` with u₀ = a₀x_e/(1+x_e) plus the Sun's
   value and M_kk = M_L or M_T (x_e 1–3, 180 rows, both footings, L★ 20/24/90 pc): max eps is still **1.312e-3**
   (Eot-Wash, L★ = 90 pc), and |eps/eps_P3 − 1| ≤ **4.4e-12**. In the lab and the Solar System kL★ ~ 1e6–1e22 ≫ √(2M_L),
   so γ_Lk² dominates χ and M_L drops out.
4. **Two P3 input defects, both inert (W5b, W3).**
   - P3 feeds the Solar-System rows u₀ = 2Φ/L★. That is 6–33 × a₀/c², outside W's domain u < a₀; the screened value
     is GM/(c²L★²). Then du = a₀ − u₀ < 0, and `scales()` silently skips the W-cubic vertex V6 (`if lh <= 0: continue`).
     P3's committed rows reproduce exactly (0.0 relative) and confirm V6 is absent.
   - P3 uses M_kk = 1, omitting the Galactic x_e.
   - With both corrected, V6 eps ≤ 4.4e-100 and no eps_max moves by more than 4.4e-12.
   - These are worth a one-line erratum in P3; neither changes a verdict.
5. **Where the weakening is real, it stays harmless (W4).** In unscreened galaxy interiors, three Hernquist models at
   r = 5L★ to 50 kpc (2,160 rows, both footings, three L★, k r = 3, 30 and k = 1/L★), x reaches 932 and M_L 8.7e5. The
   max eps is **3.4e-86**, against P3's 1e-2 line. Ignoring the weakening (MUTATE, M_kk = 1) moves individual rows by up
   to 10^4.4, which clears the frozen 2× threshold, and *raises* the worst value to 5.8e-85.
6. **How eps scales with M_L at fixed inputs (AMENDMENT A1, reported only).** The weak lapse lowers the clock
   gradient vertices V1/V4: slope −0.3 to −1.2, and exactly **−0.50** in the clean regime E = c_πk, Z_P > μ_K²
   (G1, k r = 300), as hand-derived. It raises the cubic time-derivative vertices V2/V3 and the K(Q)-dust vertex V5:
   slope up to **+1.45 ≈ +3/2**, i.e. eps ∝ (1+x)³. Physically, a weak lapse operator means a small kinetic coefficient
   Z ≈ k²/(KM_L), so the khronon becomes a gapped mode, ω² ≈ ρ_τKM_L. The vertices whose coefficient is not
   suppressed along with Z grow. This growth starts from 1e-86, so it could matter only where an unscreened
   high-acceleration region also had a non-negligible base eps. P3's BH cap rows already feed M_L at the cap.

## Checks

| run | result |
|---|---|
| `p3_weak_lapse.py` (`.out`, `_results.json`) | **5/5 PASS** (W1, W2, W5b, W3, W4) |
| `--mutate` (`_MUTATE.out`) | W4 sensitivity max \|Δlog₁₀ eps\| = 4.41 ≥ 0.30 (W5a PASS-as-required); worst W4 eps 5.8e-85 |
| `p3_weak_lapse_partial.py` (`.out`, `.json`) | controlled slopes per vertex, 18 cases (AMENDMENT A1, reported only) |

Disclosed: the slopes printed in the main run's W4 line (+0.71 / +1.25) are confounded. They were fitted along radius,
and the MUTATE run gives +2.19 / +0.75 with M_L ≡ 1. The controlled values are in item 6. All runs: one thread,
nice 15, under 1 s.

## What this does not do

It does not re-derive P3's decoupling-limit method (O(1) loop factors, first order in background gradients, the vertex
set V1–V6). It does not treat non-spherical saddles (H4's regions, where G < 0 and P3's estimate does not apply), DBI K,
or the BH cap rows (P3 already feeds them M_L at the cap). The Galactic x_e is a bracket built from v_c ≈ 200 km/s, not
a fitted MW model.
