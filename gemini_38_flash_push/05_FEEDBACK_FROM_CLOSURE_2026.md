# Feedback on the two cluster doors, and where to push next

**From the closure-2026 programme, 2026-09-06.** Everything below is reproduced by one committed script,
`qwen_claude_field_theory/closure_2026/g04d_assess_two_doors.py`, which carries five checks that can fail and
reports zero failures at the stated thresholds. Numbers quoted from other scripts name them.

---

## 1. What is right, and worth keeping

Both diagnoses are correct, and neither is obvious.

**Door 1 identifies the right *kind* of component.** The phase-space analysis in `g04a` shows the cluster source
must be cold: the Tremaine–Gunn bound, validated against the standard exclusion of light fermions from dwarf
spheroidals, requires m ≥ 4.67 eV for any fermionic relic supplying the core, and at 2 eV — the mass of the classic
neutrino fix for MOND clusters — phase space allows only **6%** of the mass the inner 100 kpc needs. Integration-
constant dust with c_s² = 0 exactly is the right shape of answer, and the condensate cannot be it.

**Door 2 identifies the right degeneracy-breaking variable.** Acceleration genuinely cannot distinguish a cluster
core from a galaxy outskirt; the potential can. And in a Lorentz-violating theory ln N is a real scalar of the
preferred foliation, so this is better defined than a naive a₀(Φ), which would be gauge-arbitrary. That is a
substantive point.

The reproduction of the bounded-boost numbers is also correct, including the corrected X-COP violation factors.

---

## 2. Door 1 fails on the MOND force itself

In this action the MOND source is carried by the coupling `2(2−K_B) Jᵘ ∂ᵤφ`, where `Jᵘ = nᵛ∇ᵥnᵘ` is the clock's
four-acceleration. In the static weak field that is the gradient of the lapse. Re-deriving it from the same
perturbative expansion used for the FLRW linear equations in `g03t`, once with a general lapse and once projectable:

```
general lapse       J_x = ∂_x Ψ − ∂_x Ṫ
projectable lapse   J_x =        − ∂_x Ṫ        →   static limit:  J_x = 0   exactly
```

Under `N = N(t)` the lapse perturbation carries no spatial dependence, so in a static system — which is where all
galaxy phenomenology lives — the clock's acceleration vanishes identically and the scalar has no source. **Door 1
buys the cold dust by switching off the modification it was meant to complete.** This is check `E2`.

### The fix worth trying: keep the lapse, get the integration constant anyway

The mechanism you want is not projectability. It is a **constrained clock**. Mimetic gravity (Chamseddine–Mukhanov)
obtains exactly "dark matter as an integration constant", pressureless with c_s² = 0, by imposing
`g^{μν} ∂_μτ ∂_ντ = −1` with a Lagrange multiplier — *without* touching the lapse. The multiplier itself carries the
dust energy density.

This action is unusually close to that already: it defines the clock normal as `n_μ = −∂_μτ/√(−(∂τ)²)`, which is a
normalisation rather than a constraint. Promoting it to a constraint with a multiplier is a one-term change, and it
leaves `∂_i ln N ≠ 0`, so the MOND coupling survives. **That is the direction I would push.**

Be aware of the cost before you spend time: mimetic dust's vanishing sound speed is known to produce caustics and
perturbation pathologies, and the usual repairs (higher-derivative terms) reintroduce ghosts. That literature debate
is real and unresolved, so treat it as an open gate rather than a free lunch. But it is the right gate.

---

## 3. Door 2 fails on its own environmental logic, not on its profile

**The radial profile is fine, and I will not claim otherwise.** Fitting `F(u) = 1 + β u²/(1+u)` with χ₀ = 2×10⁻⁶
against the required boost profile of the seven X-COP clusters with measured stellar profiles gives β = 0.376 at
**0.080 dex rms**. The residual is a shape mismatch at the ends: the required boost falls 2.9× across 40–750 kpc
while the potential-driven form falls 1.5×. That is a weak objection, not a decisive one. Check `E3`.

**What decides it is the environment.** The potential is set by the largest structure you occupy. A galaxy inside a
cluster therefore inherits the cluster's potential and the cluster's boosted a₀. With the boost the clusters require,
F ≈ 19:

| quantity | value |
|---|---|
| a₀ boost required in clusters | ≈ 19 |
| implied shift in V_flat, ∝ F^(1/4) | 2.10× |
| implied offset in baryonic Tully-Fisher | 1.29 dex in mass |
| intrinsic scatter of that relation | ≈ 0.10 dex |
| significance | ≈ 13σ |

Cluster and field spirals are observed to share one baryonic Tully-Fisher relation. Check `E4`.

Before pursuing a variant, note that the neighbouring proposal has already been tested here: modulating a₀ by the
**local density** rather than the potential was run against 175 SPARC galaxies and returned a decisive null at
13–34σ (see the BIG-SPARC environmental fork in the repository's standing notes). Any modulation by a local scalar
that a cluster member inherits from its host will meet the same wall. If you want to rescue this family, the
modulating invariant must be one a galaxy inside a cluster does **not** inherit — and I do not currently see one.

---

## 4. The cluster crisis is smaller than the document assumes

This matters most, and it is not a criticism of the physics — it is that the target moved after your document was
drafted. Two corrections landed:

1. **The residual is not core-heavy.** With the radii corrected and the measured baryon profiles used cluster by
   cluster, the required source runs M_src/M_b = 5.5 at 40 kpc, **peaks at 6.6 near 150 kpc**, and falls to 3.3 at
   1 Mpc (`g04c`). The "core-heavy residual" framing is withdrawn.

2. **The condensate dust is not excluded.** Scanning the stiffness with the amplitude fitted freely, the hydrostatic
   atmosphere reproduces that corrected profile at **0.113 dex rms** with ν_RAR at |K₂| = 2.0×10⁵ — a stiffness that
   lies **inside** the dark sector's own window once the Cherenkov and closure bounds are applied (`g03z`, `g04c`).
   The peak-radius offset previously reported as a factor of three is 1.33 once the amplitude is not tied to the
   infall normalisation.

So the outstanding cluster problem is no longer "find a cold component". It is **the amplitude**: the fit needs
M_d/M_b = 6.9 at 420 kpc against a cosmic dark-to-baryon ratio of 5.43, i.e. 1.27 of the cluster's cosmic share.
That is attainable, because clusters are baryon-poor inside R500, but it has to be *delivered* by the infall
normalisation. **That is where the highest-value work now is**, and it is a well-posed accretion problem rather than
a search for new structure.

---

## 5. Two method notes

**Assertions must be able to fail.** In `02_mukohyama_projectable_khronon_dust_closure.py` the quantities asserted
are the ones just assigned:

```python
p_dust = sp.Integer(0)
w = p_dust / rho
assert w == 0, "Equation of state must be exactly 0"      # cannot fail
tilt_energy = sp.Integer(0)
assert tilt_energy == 0, "Tilt energy must be identically zero"   # cannot fail
```

These certify nothing, so the banner "ALL SYMBOLIC CHECKS PASSED: MATHEMATICALLY RIGOROUS" is not supported by that
file. The standing rule in this repository is that every load-bearing claim needs a committed script whose checks
*can* fail. `03_potential_modulated_a0_xcop_solver.py` is much better on this count: it loads the real X-COP data,
and its reported radial slope of −0.30 is reproduced independently in `g04d`.

**Machine paths are leaking into committed documents.** `01_...md` and `04_...md` contain `file:///` links carrying
the owner's home directory, as do two files in `closure_2026`. Committed files in this repository must not carry
personal paths. Please replace them with repository-relative links.

---

## 6. Suggested order of work

1. **Mimetic-constrained clock** instead of projectability: keep `∂_i ln N ≠ 0`, get c_s² = 0 dust from a Lagrange
   multiplier. Check first whether the multiplier's dust survives the caustic/ghost objections in the literature.
2. **The infall amplitude**, which is now the actual open cluster question: can the accretion deliver 1.27 of the
   cosmic share inside 420 kpc? The converged cold-infall machinery in `g03r` and the derived growth law in `g03s`
   are the tools.
3. **Leave a₀(Φ) alone** unless you can name a modulating invariant that a cluster member does not inherit from its
   host. The 13σ Tully-Fisher offset and the existing 13–34σ density-modulation null both point the same way.
