# The Koide Dirac-Normalization Bridge — VERDICT: NULL (the 167th re-labeling)

**Date:** 2026-06-25
**Task:** Does the framework's GRAVITY side (a0 = c²√(Λ/32π), dS-Unruh modified-inertia MOND)
force the charged leptons onto the **Dirac / √(3/2)** normalization (= deriving Koide Q=2/3,
the a0↔flavor bridge), and does that survive the mass-ratio tradeoff?

**Verdict: NULL.** The bridge does **not** close. The framework lives in the correct
symmetry home (Singh's exceptional-Jordan-algebra / J₃(O) / Spin(8)-triality), the exact-2/3
normalization **is geometrically available** inside that algebra (√(3/2) → K=2/3 exact,
sympy-verified), and Singh's **own** EJA derives a MOND with a0=cH₀ of the framework's exact
form — so the bridge was tested in its single most favorable, framework-native, gravity-linked
venue. But **nothing** — not the EJA algebra, not Singh's U(1)grav/MOND/a0, not the framework's
dS-Unruh spine — **forces** the Dirac √(3/2) normalization; the algebra forces the **Majorana
√(3/8)** value (fitting the measured ratios, K=0.669163 ≠ 2/3), and forcing √(3/2) to recover
exact 2/3 **destroys** the charged-lepton mass ratios (negative √-mass). This is Singh's OWN
central published result, with **no 2-parameter escape**. SM mass sector stays WALLED.

---

## 1. The phase-independent Koide identity (the entire unforced content)

Brannen circulant √m_k = M(1 + r·cos(φ + 2πk/3)) gives, **sympy-exact** (phase φ cancels):

    K = 1/3 + r²/6 ,   K = 2/3  ⟺  r = ±√2  ⟺  √m-vector at 45°.

So "force Koide 2/3" ≡ "force r=√2". Verified φ-independent at φ=0, 0.3, 1, 2.

EJA equally-spaced triple (c−δ, c, c+δ) gives K = 1/3 + (2/9)(δ/c)², equivalent to
**r_eff² = (4/3)(δ/c)²**. Hence:
- Majorana δ²=3/8 → r_eff² = 1/2 (r_eff = 1/√2) → K = 5/12 (bare) / 0.66916 (tilted ladder)
- **Dirac δ²=3/2 → r_eff² = 2 (r_eff = √2) → K = 2/3 EXACT** (sympy-verified, residual 0)

## 2. Singh's construction — read VERBATIM (2108.05787, 2304.01213, 2508.10131)

What actually selects δ, in Singh's own words (extracted from the PDFs, not the abstracts):

**2108.05787 (mass ratios), §IV verbatim:** "as we go from the Majorana neutrino case to the
Dirac neutrino case... in the roots for the charged fermions, **the factor of √(3/8) gets
replaced everywhere by √(3/2). This makes a crucial difference to the mass ratios... with the
Dirac neutrino leading to ratios which do not agree with known values.**"

**2108.05787 Eq.62-63 verbatim:** Majorana set → K_th = 0.669163 ≈ 2/3 (his Eq.62). And his
Eq.63 (the bare Dirac triple): **(1+√(3/2))² + 1 + (1−√(3/2))²) / 3² = 2/3** — labelled
"the eigenvalues of charged leptons... **for the Dirac neutrino case exactly satisfy the Koide
formula**." Verbatim follow-up: "This might be happening because **prior to symmetry breaking**
the left-handed charged fermions and right-handed fermions... come from Dirac neutrinos which
**post symmetry breaking** become two distinct Majorana neutrinos."

**2508.10131 (2025 follow-up) Eq.7-9 verbatim:** "Prior to the triality symmetry breaking,
the neutrino is a Dirac neutrino, and... for the charged families, δ²=3/2. **Symmetry breaking...
halves the value of δ for the charged families.** Choosing the Dirac-set spread... (δ/k)²=3/2...
**we obtain the exact Koide value K=2/3.**" After breaking: δ²=3/8 (Majorana) + the Dynkin-Z2
endpoint tilt G → K_th≈0.66916. Verbatim: "**this small offset directly measures the finite
size of triality breaking** (through X and G); **before breaking (k=1, (δ/k)²=3/2) Koide is
exact.**"

**⟹ THE SELECTOR IS NEUTRINO-NATURE + OCTONIONIC-TRIALITY/EW SYMMETRY BREAKING, NOT GRAVITY.**
δ²=3/8 is "fixed by the cubic on the coassociative slice" (2508.10131 abstract verbatim) — a
dimensionless E6/F4 characteristic-cubic eigenvalue. The SAME √(3/8) also sets the fine-structure
constant: α = (9/1024)exp[(2/3)(1/3 − √(3/8))] ≈ 1/137.04 (2304.01213 verbatim) — proving δ is a
pure algebraic number, **g_*-free and cosmology-free**. Singh's only dimensionful inputs are
L_Planck, t_Planck, ℏ.

⚠️ **The "Λ" in 2508.10131 is NOT the cosmological constant.** It is the internal **proto-centre
log Λ := ln k = ln(qs)** (his §B, "Proto-centre Λ and proto-spacing δ"). Do not confuse it with
the framework's Λ. The cosmological constant never enters δ in any of the three papers.

## 3. The TRADEOFF — REAL, SHARP, mutually exclusive, Singh's own result (mpmath dps=40)

| normalization | δ² | Koide K | √(m_μ/m_e) (PDG 14.379) | √(m_τ/m_e) (PDG 58.968) |
|---|---|---|---|---|
| **Dirac √(3/2)** | 3/2 | **2/3 EXACT** | **−17.30** (dev −220%, NEGATIVE) | 171.3 (dev +190%) |
| **Majorana √(3/8)** | 3/8 | 0.669163 (+0.375%) | 14.097 (dev −1.96%) | 58.640 (dev −0.56%) |

At the Koide point δ=√(3/2), the charge-1/3 eigenvalue triple has **1/3 − √(3/2) = −0.8914 < 0**:
the smallest √-mass goes **negative** → the charged-lepton spectrum is **destroyed**, K_pred(ladder)
= 1.234. The tradeoff is **structural, not cosmetic** — a real √-mass cannot be negative, so no
smooth one-knob correction rescues it without flipping a sign (= abandoning the equally-spaced
ansatz that produced 2/3).

**No 2-parameter escape.** K(δ) is monotone; the algebra forces √(3/8) (K=0.66916). The only δ
where Singh's *tilted* ladder hits K=2/3 is a TUNED δ≈0.6085 (0.63% off √(3/8), forced by nothing)
that itself leaves the ratios ~2% off. The exact-2/3 normalization and the ratio-fitting
normalization are the two endpoints of a **halving** (δ²: 3/2 → 3/8, √-ratio exactly 2) and cannot
be reconciled. Singh resolves it explicitly IN FAVOR of the mass ratios (keeps Majorana √(3/8),
Koide approximate).

## 4. Route B (EJA↔Λ/dS shared-root) — the most promising thread, fully tested: NULL

The crux: in 2304.01213 BOTH √(3/8) AND a0 appear — is the SAME invariant feeding both?
**No — they are two disjoint uses of J₃(O), glued at a section boundary:**

- **√(3/8) block** (2304.01213 lines ~280–300): the F4 characteristic-cubic eigenvalue spread
  `q + ε√(3/8)` setting mass ratios + α. Contains **zero** a0/MOND/Hubble/cosmology (grep = 0).
- **a0 block** (lines ~385–412): introduced via "We now explain how **cosmological considerations**
  bring this ratio down..." — a SEPARATE argument starting from the **observational** input
  N_U ≈ 10⁸⁰ + black-hole surface gravity `GM_U/R_H² = a0 = cH₀`, giving the coupling **B = √(G·a0)**
  (his Eq.10, "agrees with the coupling constant in Milgrom's MOND law"). Contains **zero**
  √(3/8) (grep = 0).

So a0 enters only the rotation-curve coupling B; δ is the flavor spread. They never share an
invariant. Sympy shared-root test, dps=40:

    gravity a0-norm = (3/8π)^(1/4) = 0.587787...     (the framework's a0-from-Λ geometry)
    flavor   δ_Maj  = √(3/8)       = 0.612372...
    a0_norm⁴ = 3/(8π) = 0.119366   vs   δ_Maj² = 3/8 = 0.375
    ratio = 1/π = 0.318310...   → NOT shared (the π lives INSIDE a0_norm, δ is π-free).

The near-miss is a **trap**: both carry the rational 3/8, but a0_norm has a 1/π inside a 4th root
and δ is pi-free. No relation (==, inverse, ², ⁴) matches (all sympy residuals ≠ 0).

## 5. Smuggle check — CLEAN (and any "gravity forces √(3/2)" WOULD be a smuggle)

The only two routes to √(3/2)/Dirac are (i) **assume a Dirac neutrino** (the physical input Singh
rejects on ratio grounds — circular w.r.t. wanting 2/3), or (ii) **demand K=2/3** and invert
K=1/3+2δ²/9 → δ²=3/2 (literally inputting the target). sympy: K=2/3 ⟺ δ=√(3/2) exactly, so
"force δ=√(3/2)" is **logically identical to** "impose Koide 2/3." No independent gravity/dS/a0/Λ
principle in Singh OR the framework yields √(3/2). Quarantine HELD: a0/Z/κ/Koide never asserted
derived; 2/3 and r=√2 enter only as the empirical/algebraic target.

**Scale audit (mpmath):** the dS/a0 spine quantum ℏH_Λ ~ 1.4e-33 eV sits ~10³⁸·⁵ BELOW the
charged-lepton scale (0.5 MeV–1.8 GeV) — no dynamical contact. The closest flavor↔cosmology touch
(m_ν ~ ρ_Λ^(1/4) ~ meV) is a mass-SCALE coincidence that does not touch Q=2/3 (neutrino Koide Q is
a free function of m₁: 0.586 at m₁=0, 0.382 at 0.01 eV).

**Consistency with banked results:** matches the four-leg dS-Unruh kill (KOIDE_FROM_DSUNRUH
2026-06-20: magnitude gap 10³⁶·⁴, wrong channel, 1/m-vs-log shape, flavor-blind) and the
cross-fermion falsifier (Q_up=0.849, Q_down=0.731 ≠ 2/3, recomputed here from PDG) — any flavor-
blind / geometry-only forcing of r=√2 is refuted because the SAME geometry must give 2/3 for
quarks, and it does not.

## 6. Both-ways ledger

**CREDIT (full weight):** The framework lives in the RIGHT symmetry home. Singh's EJA/J₃(O)/
Spin(8)-triality IS the framework's own triality structure; it FORCES the equally-spaced √-mass
triple Koide/Brannen need (the 1+2 democratic+standard decomposition); Singh's OWN EJA derives a
MOND with a0=cH₀ of the framework's exact form. The √(3/2)/Dirac normalization IS available inside
the geometry and DOES give K=2/3 EXACTLY (sympy). This is a real, correctly-localized,
framework-native target.

**CONCEDE (full weight, decisive):** Nothing forces the Dirac √(3/2). The algebra forces Majorana
√(3/8) (fits ratios, K=0.669 ≠ 2/3), and forcing √(3/2) for exact 2/3 destroys the charged-lepton
ratios (−220%, negative root) — Singh's own central result, no 2-parameter escape. The promising
"Singh ties EJA to Λ/dS" thread, read VERBATIM, ties the cosmological scale ONLY to the gravity
coupling (a0~cH₀ via N_U + black-hole surface gravity), **never to the flavor spread δ** — the
bridge has no load-bearing connection.

**This is NOT a manufactured deficit and NOT a manufactured win.** It is the honest expected
result with a sharp reason (the tradeoff = Singh's own Eq.7-9 / Eq.62-63), the 167th re-labeling.
No maximal-re-verification flag needed beyond the reproduced numerics. Quarantine held both ways.
SM mass sector stays WALLED.

## Files
- Verification scripts: `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/koide_dsunruh/`
  (eja_singh_delta_structure_verify.py, eja_singh_tradeoff_massratios.py, routeB_shared_root_verify.py,
   tradeoff_2param_escape.py, ladder_softness.py, bridge_final_verify.py, koide_geometry_crossfermion.py)
- Singh PDFs extracted to /tmp/ (2108.05787, 2304.01213, 2508.10131) — verbatim grep-confirmed.
