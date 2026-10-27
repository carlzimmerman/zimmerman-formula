# CFG691 — can astra's stiffness hide the sector from the Sun and keep it in galaxies? (frozen criteria)

Block CFG690–699. Written before any CFG691 script or number. Committed alone. κ = ½ fitted; both footings
(9.3603e-11 / 1.1312e-10), never pooled; the cold energy's mass is required; no particle species; not theory closed.

## Why
CFG690: astra's stiffless (γ = 0) sector leaves a power-law residual Δg/g_N = (a₀/g_N)^{1/2}, about 10⁻³ at Saturn. astra says
stiffness suppresses the central response with an onset ℓ_γ = γ/(βB) ∝ M^{−1/2}. This lane asks whether one stiffness constant
can pass the record's Solar-System gates and still leave SPARC galaxies on the law.

## The sector (astra, read only, `STABLE_SOURCED_RESPONSE.md`)
Spherical static equation −γ[p″ + 2p′/r − 2p/r²] + βp² = D/a, D = αM(<r)/4πr². Anomalous acceleration (α/a)p, with
αB/a = (G a₀ M)^{1/2} (astra's matching).

**Reduction (to be verified in the script, K1).** For a point mass, with s = r/ℓ_γ and p = (B/ℓ_γ) q(s), the equation becomes the
parameter-free −[q″ + 2q′/s − 2q/s²] + q² = 1/s², with q → 1/s (s ≫ 1) and q → ½ (s ≪ 1, regular). The anomalous acceleration is
g_an = (G a₀ M)^{1/2}/r · S(s), S(s) = s·q(s). Inside ℓ_γ it is the constant GM/L*², where **L*² = 2 r_M ℓ_γ** and
r_M = (GM/a₀)^{1/2}. L* is one universal length, the sector's single new constant (CFG679 R1).

For an extended system the lane uses g = g_N + (a₀ g_N)^{1/2} S(r/ℓ_γ(M_b)), with M_b the total baryonic mass. This is the
point-mass screening applied to the enclosed field. It is disclosed as an approximation and is relevant only where ℓ_γ is
comparable to the measured radii.

## Gates
**G-SS (Solar System, the record's CFG3 gates, both footings).** Isolated Sun. Pass needs both:
- sunward anomaly at 1 AU < 3.66e-14 m/s² (FP1);
- anomalous enclosed mass inside Saturn's orbit (9.54 AU), M = g_an r²/G, < 6.7e-11 M☉ (Pitjev & Pitjeva 2013 via f29).

This gives **L*_min** per footing: the smallest L* that passes both. CFG3's Q2 quadrupole gate needs the Galaxy's external field,
which is not modelled here. It is reported as UNTESTED.

**G-GAL (raw SPARC, the CFG4 statistic as copied in CFG690).** Screened form, Υ_disk profiled on 0.30–1.20. M_b per galaxy is
V_bar²R/G at its last point, at the profiled Υ. **L*_max** per footing is the largest L* on a log grid (0.01–1000 pc, 0.01 dex)
at which the screened rms is still ≤ 0.110 dex, the CFG4 line.

**Verdict.**
- **WINDOW OPEN** iff L*_min < L*_max on both footings.
- **WINDOW CLOSED** otherwise.
- The Υ band is reported, not used. CFG690 already fails it at γ = 0, and that failure is inherited whatever the verdict here.
  A WINDOW OPEN verdict is never a C2 pass.

**Reported only (no verdict weight), at L* = L*_min:**
- ℓ_γ and the screening factor S for the record's ultra-faint and classical dwarfs (stellar masses and half-light radii as in
  the record's UFD lane CFG259, if the inputs load read-only; else not reported);
- wide binaries (1 + 1 M☉ at 10³–10⁴ AU);
- the size of the constant pull GM/L*² for the Sun.

## Controls (load-bearing; exit 1 if any fails)
- **K1:** the numerical q(s) satisfies the ODE to residual ≤ 1e-6 (relative). S(s) ≥ 0.999 at s = 10³. q(s) → ½ within 1e-3 at
  s = 10⁻³. In physical units the inner g_an equals GM/L*² within 1e-3.
- **K2:** at L* → 0 (no screening) the SPARC fit reproduces CFG690 T3 (rms and Υ) to 1e-6, both footings.

## MUTATE (`CFG691_MUTATE=1`, exit 1 iff both bite)
- **M1:** no stiffness (S ≡ 1). G-SS must FAIL on both gates.
- **M2:** the scalar Laplacian (the −2q/s² term dropped). The inner limit q → ½ must fail K1.
