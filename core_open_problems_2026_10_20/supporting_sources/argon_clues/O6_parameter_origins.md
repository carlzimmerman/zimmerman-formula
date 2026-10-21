# O6: parameter origins (support deliverable for sol61's THEORY_NEXT_STEPS_2026-10-15, item O6)

Written 2026-10-15 in `argon_clues/` (my folder; no sol61 or astra file edited). The frozen October 14 theory, its criteria and predictions are untouched. κ = ½ is FITTED; nothing here says the theory is closed.
O6 asks for a table labelling each quantity derived / measured / bounded / selected with independent evidence and sensitivity, and a test of any proposed coefficient-selection route against the existing rescaling/zero-mode freedom before a long computation. This file supplies both from committed results (`o6_screen.py`, Lean `lean/ArgonClues.lean`).

**Two completion standards stay distinct (as O6 requires):** (A) a predictive effective theory with measured constants: κ, R₀ and L* are inputs and the galaxy law follows from the action given them; (B) a theory in which the October 14 open-input list is eliminated, which needs derivations of κ, R₀ and L* that do not exist. Nothing below reaches (B).

## Output of `o6_screen.py`
```
1. dimensionless groups of (a0, c, G, rho_DE): 1  -> exponents [[-2, 2, 1, 1]]  (order: a0,c,G,rho)
   => a0/(c sqrt(G rho_DE)) = kappa is the ONLY dimensionless number. A derivation of a0 is a derivation of one pure number; dimensional analysis alone cannot supply it.
   with L* added: 2 groups; second group: L* * a0/c^2 or L*/(c/sqrt(G rho))  (the stiffness length in Hubble-ish units: 1.85e-10)

2. SCREEN every proposed selection route R(kappa) against: (a) static scale covariance (Lean: scale_gN/scale_tether/scale_nu); (b) a continuous vacuum-offset family (sol61 open_items item 4).
   A route passes only if its output is NOT invariant under (g,a0)->(lam g, lam a0) AND it contains rho_DE or Lambda and c in its inputs. Static-class routes fail (a) by construction: they contain neither.
   hemisphere average (1/2)       fails the screen: typed pairing (a0 = <cos> c sqrt(K/4pi rho))
   Komar/Gauss 1/2                fails the screen: ratio of two normalisations
   Galileo drift (lambda=1)       fails the screen: cross-term coefficient inserted
   S2 orientation                 fails the screen: projection x solid angle chosen
   Deser-Levin / horizon routes   fails the screen: give cH x rational (floor a0/2 => 2Z off)
   Friedmann conversion           fails the screen: identity, moves the gate scale choice (sqrt(G rho) vs H)

3. INVENTORY (status labels: DERIVED / MEASURED / BOUNDED / SELECTED)
   - kappa (a0/c sqrt(G rho_DE))      MEASURED (and posited = 1/2)  
       evidence: CFG493 GLS: 0.417 +- 0.095 (canonical), 0.345 +- 0.078 (alt); 1/2 at 0.80 / 1.63 sigma; floor 9.3% from shared systematics; kernel choice moves it +0.06-0.09 dex
       derivation status: no derivation survives: Lean no-go (static class), sol61 continuous offset family, 10+ audited routes
   - Omega_c/Omega_b = R0             MEASURED                      
       evidence: 5.364 (CMB; native 5.376); census: no net conversion > 2.3% of cold energy (CFG779, cold_to_baryon.py)
       derivation status: dust equations preserve any initial ratio (sol61 item 5): needs an independently normalised production history
   - L* (stiffness length)            BOUNDED                       
       evidence: >= 5.75 pc (Saturn bound, CFG691); SPARC fine to >= 1 kpc; GC X2 minimum ~25 pc (4 clusters); UFD median cost +0.03 / +0.08 / +0.16 / +0.30 dex at 5.75 / 10 / 15 / 25 pc; Gaia DR4: boost (1/2)(s/L*)^2
       derivation status: joint window ~10-15 pc if globulars and UFDs are both taken at face value; no derivation
   - gamma                            tied to L*                    
       evidence: gamma = K L*^2/2 (canonical theory)
       derivation status: inherits L*
   - a0 footing (Lambda vs rho_crit)  SELECTED (declared)           
       evidence: 9.36e-11 vs 1.13e-10 m/s^2, both reported
       derivation status: footing is a convention for kappa = 1/2; never pooled
   - basin / no-EFE rule              SELECTED (data-forced)        
       evidence: satellite lensing: no-EFE chi2 0.7 vs EFE 99.5 (PAPER44)
       derivation status: no local action derives it (Stueckelberg, transport, scalar potential all fail)
   - free fraction (2/3 of R0 f_hot)  SELECTED                      
       evidence: level matches X-COP median (0.05-0.08 dex), rank test fails (rho 0.46-0.48, p 0.12-0.13)
       derivation status: mechanism for the partition not derived

4. SENSITIVITY of downstream numbers
   k = (2/3) R0 f_hot: dk/k = dR0/R0 (1:1); R0 5.364 -> 4.80 moves the X-COP level by 0.048 dex.
   a0 ~ kappa: GLS 1-sigma 25 percent in kappa = 0.099 dex; the sealed ALMA gas predictions shift ~ (0.5-1) x that in log M_gas (CFG571 note: stellar-mass branch moves them 0.6 dex).
   L* in [5.75, 25] pc: UFD median +0.03 -> +0.30 dex; GC X2 8.5 -> 3.1; Solar System excludes < 5.75.
```

## Lean-certified facts used by the screen (`lean/ArgonClues.lean`, 34 theorems, no sorry; `ArgonClues_MUTATE.lean` is rejected)
- `scale_gN`, `scale_tether`, `scale_nu`: the static law is covariant under (g, a₀) → (λg, λa₀) with ν invariant, so a₀ is a unit inside the static action class and any route that stays inside that class passes no screen.
- `friedmann_units`, `Z_factor`: the π in Z is Friedmann's; in (c, G, ρ_DE) units a₀ is π-free, so the open number is the single rational ½ (Buckingham: one dimensionless group, κ).
- `floor_ratio`, `gate_is_DL`: the gate's quadrature floor is a₀/2; a floor equal to κ_dS would be a factor 2Z = 11.58 off.
- `M_crit_value`, `phantom_cap`, `inner_solution`: stiffened point-mass inner solution u₀ = GM/(2L*²), saturation at M_crit = 2a₀L*²/G ≈ 4.4×10⁴ M☉, inner phantom ≤ M_crit/2.

## What would count as passing the O6 screen
A proposed κ route must (i) be built from a computed, not chosen, factor; (ii) use ρ_DE (or Λ) and c, which the static action lacks; (iii) not be invariant under the vacuum-offset family of sol61 open_items item 4; (iv) reproduce κ on the canonical footing within the CFG493 band (0.417 ± 0.095) and state its alt-footing prediction. No route examined so far passes (i)–(iii).

## Joint L* note (new, numerical, not Lean)
UFD median offsets and outer-halo globular X² pull L* in opposite directions; a joint window ≈ 10–15 pc exists at face value (four clusters, Plummer baryons, binary-inflation caveat for Pal 3). It is a pair of bounds, not a derivation; the sealed Gaia DR4 statement (boost ≤ ½(s/L*)²) is safe for any larger L*.
