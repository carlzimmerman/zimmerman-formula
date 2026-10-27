# CFG692: gravitating polarization — the bound charge as the cold mass

**Label: LENSING (Newtonian), LEDGER, STABILITY: PASS. EXTERNAL FIELD (S2): FAIL. SPARC (C2): FAIL by the Υ band (same
interpolation as CFG690). R0: R0-SHAPED (criticality + SI). Attractor: UNTESTED. Not a mechanism that passes CFG679.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (097b2feee), 2026-10-12. Block CFG690–699.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory
  closed"; nothing here says the data favour the framework.
- **Script:** `cfg692.py`, seconds, exit 0 → `cfg692.out`, `cfg692_results.json`. `CFG692_MUTATE=1` exits 1 as designed → `_MUTATE`
  outputs. Reads `CFG4_common` and `CFG4_galaxy_law_results.json` read-only.

## The construction
A vacuum polarization field P whose bound charge ∇·P is gravitating mass. Newtonian limit:

L = −|∇Φ|²/8πG − (ρ_b + ∇·P)Φ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|²,
W = 2πG P² + (4πG)²P³/3a₀.

The quadratic sits exactly at criticality, W″(0) = 4πG. The cubic is the scale-invariant term. There are no dipole carriers and
no particle species.

## Results

| test | result |
|---|---|
| **T1** static law | u = (a₀/2)(√(1 + 4g/a₀) − 1); **deep g_N = g²/a₀ exactly; μ → 1 at high g**. Inverse: **g = g_N + √(a₀g_N)**, the same interpolation as astra's sector (CFG690). PASS |
| **T2** stability, fixed baryons, γ = 0 | W″ − 4πG = 8πG u/a₀ > 0; transverse margin 4πG u/a₀ > 0; positive-definite for every k direction and every u > 0 (max condition 0.9999 < 1 at u = 10⁻⁴a₀). **PASS without stiffness.** The margins → 0 as u/a₀ → 0: the medium is near-critical in the deep regime |
| **T3** lensing + ledger | ρ_c = ∇·P enters the one Poisson equation, so Newtonian lensing equals dynamics. Deep: ρ_c = √(GMa₀)/(4πG r²) > 0, M_c(<r) = √(GMa₀) r/G ∝ r, equal to the surface flux of P. **Cold mass is moved, not created.** The compensating negative bound charge sits where P falls to zero, at the edge of each polarized region. PASS (structural); M3a CONDITIONAL on Φ = Ψ in a relativistic completion |
| **T4** raw SPARC | 0.1012 @ Υ 0.46 / 0.1007 @ 0.42 (= CFG690). Υ below band: **FAIL** (C2) |
| **T5** external field | satellite at g_i = 0.01 a₀: isolated boost **102**; in g_e = 0.1 a₀: **6.5 (∥) / 11.9 (⊥)**; in g_e = a₀: 1.8 / 2.6. **S2 FAIL** |
| **T6** Solar System (γ = 0) | Δg/g_N = 1.3e-4 (1 AU), 1.2–1.3e-3 (Saturn): needs stiffness screening (cf. CFG691) |
| MUTATE | off-critical W″(0) = 1.1 × 4πG plus screening sign: T1 fails (deep ratio ∞); ν = 1: 0.2755. All bite |

## Reading: what the attempt found

1. **Three of the four missing pieces have a working form.** Let the cold mass be the bound charge of a polarizable vacuum:
   - it **lenses like mass**, because it sits in the one Poisson equation;
   - it is **conserved**: halo mass is displaced from the edge of the polarized region, not created;
   - its static medium is **stable without stiffness**, unlike the carrier-fluid dipolar model, whose growing mode came from the
     carriers.

   The deep law then follows from two conditions only: the vacuum sits at gravitational **criticality** (W″(0) = 4πG, infinite
   linear susceptibility), and the leading nonlinearity is scale-invariant with a₀ as its scale.
2. **The one thing it cannot do is ignore the external field.** The medium responds to the local total field. A satellite in a
   host field sits on the host's polarized background, where the susceptibility is finite, so its boost collapses (102 → 6–12).
   This holds for any local medium whose response is a nonlinear function of the local field. It is the same wall as S2 + S3 in
   MECHANISM_JOINT §6: the selector must read each system's **own** enclosed baryons.
3. **So the precise remaining gap is narrow.** It is a polarizable vacuum whose susceptibility is set per bound system, by that
   system's own baryons, not by the local total field. Equivalently, criticality must be restored inside each bound system, so the
   polarization can respond to a satellite independently of the host's background. Nothing on the record does this; it is the
   one property left to derive.
4. **Two further gaps, both inherited:**
   - the interpolation g = g_N + √(a₀g_N) asks for Υ_disk 0.42–0.46 (C2). Higher-order terms in W would change it, but would be
     chosen (R0).
   - criticality is a tuning to G (R0).

## Disclosures
- One MUTATE run applies the off-critical and screening-sign changes together (the criteria list them as separate teeth). T1
  fails, so both bite. Separate runs were not made.
- T5 uses linear response about a uniform host background, in two polarizations. It is not a full satellite solution.
- The structure is Blanchet's gravitational polarization (MECHANISM_JOINT §7). New here: the pure-field stability result, the
  identity with CFG690's interpolation, and the quantified external-field collapse.
