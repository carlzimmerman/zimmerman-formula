# CFG9 — the kernel's shape from local virial equilibrium

Script: `CFG9_local_virial.py`, about 20 s.
- Outputs: `CFG9_local_virial.out` and `CFG9_local_virial_results.json`.
- MUTATE control: `CFG9_local_virial_MUTATE.out` and `_MUTATE_results.json`, where D1 fails as designed (rc = 1).

κ = ½ is fitted. Both a₀ footings are used throughout.

## The result (exact, for a point mass)

Take a point baryonic mass M, and put a cold component around it in isotropic Jeans equilibrium in the total field.
Require every shell to be virialized in its own circular speed, σ² = V_c²/2 at every radius.

- The Jeans equation then gives ρ = K/(r³g).
- With u = r²g, the mass equation integrates to u² = (GM)² + 4πGK r², so

  **g = √(g_N² + a₀ g_N), with a₀ = 4πK/M.**

  This is exactly the framework's kernel P2, ν = √(1 + 1/y), at every radius.

The converse also holds. P2 is the only law whose point-mass phantom is locally virialized at every radius, because the ODE's solution is unique.

Two equivalent statements:
- The component's pressure obeys 4πr²P = a₀M/2: its pressure force on any sphere is half of a₀ times the enclosed baryonic mass.
- P = a₀ g_N/(8πG) at every radius. CFG7/FG004 had found this only in the deep limit.

So P2's shape follows from one kinematic statement. a₀ is the component's charge per unit baryonic mass. The framework ties it to the vacuum through a₀ = κc√(Gρ_Λ).

| check | result |
|---|---|
| D1: the theorem, for g_N/a₀ from 1e-4 to 1e4, both footings | max deviation 8.8e-8, **pass** |
| D2: uniqueness within ν_β = (1 + y^−β)^{1/2β} | only β = 1 is locally virialized. Maximum departures: β = 0.5, 0.33; β = 0.75, 0.20; β = 1.5, 0.99; β = 2, 8.9; ν_mono, 0.097 (at g_N ≈ a₀). **pass** |
| D3: the constant-charge closure integrated as an ODE equals P2 | 3.6e-12, **pass** |
| MUTATE: β = 2 in place of P2 | D1 fails, rc = 1 |

**What it says about the kernel.**
- The principle selects P2, not the contract kernel ν_mono.
- On SPARC, P2 fits 0.004–0.008 dex rms worse than ν_mono. CFG4's committed H2 gives 0.1083 against 0.1003 (canonical) and 0.1035 against 0.0991 (alt).
- The contract is unchanged.
- **Correction (added 2026-09-28): "slightly" understated it.** CFG4's committed shape bootstrap in the ν_β family (1000 resamples, Υ profiled) puts β at **0.48 [0.40, 0.59]** (canonical, 95%) and **0.55 [0.45, 0.77]** (alt). P2's β = 1 loses to the best β in 1000 of 1000 resamples. Applied everywhere, **SPARC excludes P2's transition shape.**
- The theorem fixes the shape only where the baryons look like a point mass. SPARC's transition region, y ~ 0.1–10, lies largely inside the baryons.
- Whether the point-mass-regime points alone prefer β = 1 is a direct test of the principle. That is CFG13.
- **Update (CFG13, CFG14): calibrated.** CFG4's galaxy bootstrap under-covers β̂'s spread by about 5×. The estimator is median-unbiased.
  - Against 60 noise realizations of each truth, **P2 applied everywhere is disfavoured at p ≈ 0.03 (about 2σ)** on the canonical footing and at p ≈ 0.03–0.13 on alt. It is not excluded at >99.9%.
  - ν_mono is fully consistent.
  - SPARC's point-mass-regime points (β̂ 0.72 / 0.88) do not discriminate. The preference comes from inside the baryons.

## Inside real baryons (SPARC, CFG4's committed Υ, CFG9's own statistic)

**S1: the law's phantom is not locally virialized.** σ²_Jeans / (V_c²/2) by region:

| region | σ²_Jeans / (V_c²/2) |
|---|---|
| g_bar < 0.1 a₀ | 1.24–1.43 |
| 0.1 a₀ < g_bar < a₀ | 1.46–1.67 |
| g_bar > a₀ | 1.69–1.75 |

The inner phantom is about 70% hotter than local virial.

**S1b: it is isothermal at the flat speed.** Against V_flat²/2, the same σ² reproduces FG004's committed H1 medians (0.93, 0.92, 1.005, 1.006) to within 0.004. This control was added after the first run to reconcile CFG9's reference with FG004's.

**S2 and S2b: a constant-charge component overshoots.** A locally virialized component with a constant charge (C = a₀M_b,tot/4π) becomes a central isothermal sphere.
- It exceeds the law at g_bar > a₀ by +0.06 to +0.09 dex (S2b, added after the first run).
- Against the data the excess is +0.15 to +0.21 dex (S2, which passed as pre-declared). Part of that margin is the law's own inner offset at CFG4's single global Υ.

**S3: a charge that tracks the enclosed baryons nearly matches P2.** The closure with the charge set by M_b(<r) is identical to P2 for a point mass. It reaches:
- at P2's Υ: 0.1106 against P2's 0.1076 (canonical) and 0.1049 against 0.1031 (alt), within 0.002–0.003 dex;
- at ν_mono's Υ: 0.014–0.019 dex worse than ν_mono.

## Standing

The lane is half derived.
- **Derived:** outside the baryons, the kernel's shape (P2) follows from local virial equilibrium, with a₀ as the charge per unit baryonic mass.
- **Open:** inside the baryons the component is not locally virialized. Its charge, or equivalently its heating above local virial, must track the enclosed baryons.

The obvious candidate principle is the pressure law P = a₀g_N/(8πG) taken inside the baryons as well. It is exact for a point mass, linear in the baryons, and adds no constant. It is the next lane, CFG10.

Nothing here says the theory is closed.
