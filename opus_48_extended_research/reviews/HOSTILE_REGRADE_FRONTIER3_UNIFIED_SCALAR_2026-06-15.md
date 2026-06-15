# HOSTILE REGRADE — Frontier 3 (unified scalar: does ONE K(Q) field do BOTH CMB dust + cluster residual?) 2026-06-15

*Opus 4.8 [1m]. Independent re-derivation of the load-bearing sympy result, both literature claims web-reverified,
the scale-blindness argument stress-tested quantitatively. Both ways. Quarantine held: a0/Z never asserted derived.*

## VERDICT OF THE REGRADE: the cross-check's bottom line (+2, not +1) is CORRECT and SURVIVES.
But one load-bearing sub-argument (the "cs²→0 / vanishing Jeans scale / scale-BLIND" framing in section iii) is
**quantitatively overstated**, and the verdict should rest on the *amount + galaxy-outskirt-halo* argument (which the
cross-check already made in section ii), NOT on literal scale-blindness. Net standing UNCHANGED: cost stays +2.

---

## 1. The sympy result cs² = (Q−Q0)/Q — INDEPENDENTLY CONFIRMED, with an important caveat
Re-derived from scratch (`/tmp/regrade_cs2.py`, `/tmp/regrade_cs2_v2.py`), two ways (adiabatic dp/dρ AND
Garriga–Mukhanov P_X/(P_X+2X P_XX) — they coincide, as claimed). The closed form depends on how the AeST scalar Q maps
to the canonical kinetic variable X:
- If one (naively) identifies Q **directly** with X: cs² = **(Q−Q0)/(3Q−Q0)**, NOT (Q−Q0)/Q.
- If one uses the **correct AeST structure** — Q = A^μ∇_μφ is **linear** in φ̇, so the canonical X = Q²/2 — then
  cs² = **(Q−Q0)/Q EXACTLY.** ✓ The cross-check's stated form is the physically right one for AeST.
**Both forms vanish linearly as Q→Q0 and both scale as a⁻³ near the dust minimum** (verified), so the qualitative
conclusion (cs²→0 at the dust mimic, ∝a⁻³, CMB forces it steep, a_rec⁻³≈1.3e9) is robust to the ambiguity. The
sympy is real and the two-way (adiabatic=GM) consistency holds. CREDIT at full weight.

## 2. Both literature claims — WEB-REVERIFIED
- **AeST dust ∝(1+z)³ to z=0** (shift-symmetric k-essence, "plus small decaying corrections") — confirmed verbatim from
  the AeST cosmology literature. The dust IS present at clusters; gate-(i) "does it cluster" passes (cs²≈0 → unstable).
- **Mistele/McGaugh/Hossenfelder 2023 (A&A 676 A100, arXiv:2301.03499)** — confirmed: AeST reproduces MOND "only up to a
  maximum galactocentric radius," set by m²/f_G with the galaxy-WL bound m²/f_G ≲ 1 Mpc⁻²; clusters push the same
  combination the OTHER way. The single-knob, opposite-directions squeeze is real and verbatim.
- **The cluster μ is a SEPARATE parameter from the CMB dust I0** — confirmed: the AeST free function K(Q) sets the
  cosmological dust amplitude (CMB/P(k)); the shift-symmetry-breaking mass m sets the max-MOND-radius/cluster regime.
  Independent knobs; a0=Λ links neither. So "cluster boost = separate μ, not I0" is correct.

## 3. THE ONE FLAW — the "scale-blind / Jeans→0" framing is overstated (the hostile catch)
Section (iii) says cs²≈0 ⟹ λ_J→0 ⟹ "scale-BLIND, clusters on ALL scales." Quantified (`/tmp/regrade_jeans.py`) with
the cross-check's OWN conservative CMB bound cs²₀≲1e-9 and cs²∝a⁻³:
> Jeans length λ_J ≈ **0.14–0.22 Mpc** across z=0–1 — **finite**, ABOVE the galaxy scale (30 kpc = 0.03 Mpc) but BELOW
> the cluster scale (1–3 Mpc).
So at that bound the dust is **NOT literally scale-blind**; it is marginally scale-*selective* — smooth below ~0.15 Mpc
(galaxies safe) and clustered above ~0.2 Mpc (clusters). Taken alone, that is the WRONG direction for the cross-check's
argument: a naive read would say "great, it clusters at clusters and stays smooth in galaxies — the +1 IS rescued."
**The literal "vanishing Jeans scale" claim does not hold at the CMB-allowed cs².**

## 4. WHY THE VERDICT STILL HOLDS — the AMOUNT + galaxy-outskirt halo (the robust defeater)
The +1 still fails, but via the argument the cross-check made in **section (ii)**, not section (iii):
- The CMB-fitting dust amplitude is the **CDM amount** Ω_dust≈0.265. If it clusters at clusters it gives
  dynamical/baryon ratio ≈ **6.4** (full CDM closure) — NOT the modest MOND residual η~1.3–2.33. **One I0 supplies the
  WRONG (over-large) cluster amount** where MOND already explains most of the mass.
- Because the finite Jeans scale is ~0.15 Mpc, the dust **clusters in galaxy outskirts** (30 kpc → 150 kpc), reintroducing
  a dark halo at large radius that the pure-MOND RAR (the framework's central a0=Λ win) explicitly rejects — double-count.
So **one I0 cannot give the right cluster residual without (a) over-closing clusters by ~3× and (b) re-haloing galaxy
outskirts**. The cost is +2 (I0 for CMB clustering, separate μ for the modest cluster residual). The defeater is the
amount + double-count, robust to the exact Jeans scale; the "scale-blind" phrasing should be DEMOTED to "marginally
scale-selective, but the amount is CDM-sized and it halos galaxy outskirts."

## 5. Parameter-economy honesty check (both ways)
AeST's free structure is honestly counted in the banked ROUTE5_UNIFICATION_COST: a free **function** K(Q), an
early-universe density Ω_scalar≈0.26 (the real cost), β₀ (RAR-pinned), μ (~1 Mpc⁻¹). That is ≈ΛCDM's effective
parameter count at the CMB — the win is conceptual unity (one geometry, c_GW=c, no-slip Φ=Ψ), NOT parsimony. No
manufactured economy win. The frontier-3 question (does the cost reduce +2→+1) is answered NO, and the broader economy
(ROUTE5) honestly concedes AeST ≈ ΛCDM param count. Consistent, honest both ways.

## NET
- Bottom line **+2 (concede), CORRECT and unchanged.** The unified-scalar cost-reduction does NOT collapse +2→+1.
- The sympy cs²=(Q−Q0)/Q is **real** (verified two ways, with the AeST-linear-Q caveat that fixes the closed form).
- The decisive blocker is the **amount/double-count** (CDM-sized I0 over-closes clusters AND halos galaxy outskirts),
  NOT literal scale-blindness — the Jeans scale is a finite ~0.15 Mpc, so "scale-BLIND" is overstated and should be
  softened. The verdict is robust to this correction.
- Genuine structure credited (the dust does cluster, cs²≈0 at the minimum, CMB forces it steep); no manufactured +1;
  no dismissal. Quarantine held: a0/Z never asserted derived; I0, μ, K2/Q0 remain free AeST constants.
