# CFG793: does the committed action already contain a cold-energy → light portal?

**Label: NO BUILT-IN PORTAL. Q1 GRAVITATIONALLY SUPPRESSED (far below Gertsenshtein); Q2 rest-mass conversion forbidden by
the action (numerical check FAIL as frozen, explained below); Q3 light-producing η ≤ 4e-35, which is 32–34 orders short.**
HYPOTHETICAL ramjet context (CFG789–792).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (73d6bf1c5).
- **Script:** `OMP_NUM_THREADS=1 nice -n 10 python3 cfg793.py` (seconds) → `cfg793.out`, `cfg793_results.json`.
  `CFG793_MUTATE=1` → `cfg793_MUTATE.out`, `cfg793_results_MUTATE.json`, and exits 1 (it bites).
- **Inputs:** κ = ½ is fitted. L* is 5.75 pc or 1 kpc. c_P is scanned over c, 10⁻³c and 200 m/s. Both footings are used. ρ_c c² = 6.1e-5 J/m³
  (provisional).

## The derivation
Split Φ = Φ_P + Φ_ρ with ∇Φ_P = K P_L. The longitudinal P then drops out of −|∇Φ − KP|²/2K. Its only coupling is −ρΦ_P: plain
Newtonian gravity between the cold mass ∇·P and other energy. Electromagnetic energy gravitates, so a photon in a background
field B₀ couples through δρ = B₀·b/μ₀c². The flux-normalised mixing rate is

  Δ_P = √(2Kε₀) B √(c_P/c) / (2ωL*),  Δ_P/Δ_grav = √(c_P/c) ƛ/(√2 L*).

So the built-in portal is Gertsenshtein's graviton–photon mixing times an extra factor ƛ/L* (about 10⁻²⁵ for optical light). The
stiffness that screens the Solar System also decouples P from light.

## Results
| | value |
|---|---|
| K1 ODE vs analytic | 5e-13 PASS |
| K2 graviton (same routine) | 8.26e-38 (1 T, 1 m) = 4πGB²L²/μ₀c⁴ exactly; literature 8.3e-38 within 0.4% PASS |
| K3 two routes | 4e-16 PASS |
| Q1 best lab case (45 T, 100 m, c_P = c, L* 5.75 pc) | P = 1.7e-79 optical, 2.1e-73 at 2.24 meV (Gertsenshtein 1.7e-30) |
| Q1 magnetar (1e10 T, 10 km) | ≤ 1e-52 |
| Q1 with c_P < c | phase mismatch, coherence length 2.5e-10 m (10⁻³c): P ~ 1e-106 |
| Q2 static field | The Lagrangian is time-independent in the cold-energy frame, and continuity conserves cold mass, so η_rest = 0 exactly. A moving device sees ω ≤ v/L*, giving photons ≥ 118 ly long (0.998c) |
| Q2 energy budget | Gravity is conservative. Any device gains at most g d = 8.7e6 J/kg over 4.37 ly, while 0.1c needs 4.5e14 J/kg (×5e7 short; same at both footings because the local field is used) |
| Q3 η (light, moving 45 T / 100 m device at 0.1c) | 3.6e-35, an upper bound because the wavelength is far larger than the device. That is 32.4 orders below 0.01 and 34.4 below 1 |
| Q3 η (gravitational work on the craft, not light) | 1.5e-12 (1 mg/m², canonical), 1.9e-12 (alt), up to 3.4e-9 (1 g/m², local field) |

**Q2 FAIL as frozen (disclosed):** the bounded-clump crossing leaves a net/peak of 1.2e-3, not < 1e-6. The residual is the
potential difference still present at the finite ±40 pc endpoints. Energy is conserved to 3.6e-10. Moving the endpoints to
±400 and ±4000 pc gives 2.7e-5 and 4.3e-7 (reported, not graded). The uniform-gradient check passes (6.6e-13).

**MUTATE** (L* = ƛ, c_P = c): Δ_P/Δ_grav becomes exactly 1/√2, so the ƛ/L* factor is what suppresses. The Q1 class does not change,
because the G factor remains.

## Reading
1. The action's only photon–P link is gravity, and the stiffness suppresses it by a further (ƛ/L*)².
2. The action conserves cold mass, so no term of it can release cold energy's rest mass.
3. A static ambient field is conservative gravity. Moving through it only trades the craft's own kinetic energy, and the
   frequencies it sees are those of light-century wavelengths.

A working converter would therefore need a new, non-gravitational term that breaks cold-mass continuity
(∂ₜρ_c + ∇·j = −Γ). It would also have to be off in ordinary matter (CFG792) and stimulated by about 10³⁴ (CFG789/792). The committed action
contains nothing like it. κ fitted; not theory closed.
