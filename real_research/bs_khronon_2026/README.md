# bs_khronon_2026 — the khronon sector of C-H/K (PAPER32 follow-through)

Status: 2026-09-25, PAPER32 deposited (qwen_claude_field_theory/papers_2026/PAPER32_moving_phantom_2026.tex).
PAPER32 left one open route: *"a khronon sector that itself behaves as dust on FRW, the route of
Blanchet & Skordis [BS24, BS25]. Running that route through the same two gates is the natural next
test."* This folder runs that route.

## The khronon fluid (committed in BSK1, from BS24's PN equations)
- rho_tau = (lap phi)/(4 pi G) - rho_m: the khronon "mass density" IS the MOND phantom.
- It is a conserved fluid carried by the aether: d_t rho + div(rho v) = 0, v = -grad sigma.
- Static linear response (WKB about a halo, f_theta = f + y f'(y) cos^2 theta):
  omega^2 = 4 pi G rho_0 (k^2 f_theta - mu^2)/(k^2 (1 - f_theta) + mu^2)   (BSK1 M4)
- Deep-web limit f(0) = 0: khronon dust's OWN gravity is inert on scales below 1/mu
  (the Euler force -grad phi + grad Xi cancels it) — it clusters under baryons only there (BSK1 M7).
- nu_mono required (nu_RAR is unstable beyond x = 2.54); GR-recovery tails unstable at the
  local orbital rate; a moving source keeps its phantom only inside r_follow ~ 2 G M_b/du^2;
  the phantom is amplified by 1/(1 - v_par^2/c_s^2) (resonance at the mode speed).

## BSK2 (this folder's result) — the khronon as FRW dust through the sigma_8 gate

Derived equation (BSK2 kernel, from BSK1 M4 at f -> 0, physical -> comoving k):

    Gamma^2(k, a) = 4 pi G rho_bar_tau(a) * mu^2 a^2 / (k^2 + mu^2 a^2)

Khronon dust self-clusters as ordinary dust only on comoving scales k < a mu (physical
lambda > 1/mu); the comoving activation edge k_c(a) = a mu GROWS with the scale factor —
a memory of the khronon mass in P(k) that no LambdaCDM component has.

Linear system integrated (sub-horizon Newtonian, khronon background = LambdaCDM background,
Omega_tau = Omega_dm): khronon dust feels baryons at every k and its own gravity with the
kernel only; baryons feel khronon dust fully; khronon(s -> 1) IS LambdaCDM dust (control).

Result (pre-registered gate = match LambdaCDM sigma_8 within the [0.80, 1.20] band):
- khronon dust at BS24's published khronon scale (mu ~ 1e-31 eV, 1/mu ~ 43 h^-1 Mpc)
  FAILS the gate: sigma_8 ratio 0.037 vs 0.80, ~26x under in amplitude.
- The gate is passed only for khronon masses above a FLOOR derived here:
        mu >= 4.7e-27 eV   (mu >= 1.1e3 h/Mpc)  <=>  hold scale 1/mu <= 1.4 kpc
- Registered tension (K5): khronon-as-DM needs a khronon ~5e4x heavier than the published
  khronon scale — the hold scale is GALACTIC (1.4 kpc), not cosmological.
- Falsifier (K4): khronon-dust P(k) < P_LambdaCDM(k) for k > mu(z=0) with the activation
  memory k_c(z) = a(z) mu (the suppression edge descends in comoving k toward z = 0).
  For khronon masses that pass the gate the edge sits below linear scales; the measurable
  falsifier there is the khronon-dust (phantom) profile below the hold scale (lensing-RAR
  at small radii) — BSK3.

Checks BSK2: 8/8 PASS.  Mutation control (MUTATE=1, khronon self-gravity never cancelled):
K3b, K4a, K4b FAIL as required.  Lanes re-run: python3 BSK2_frw_dust_sigma8.py.

## Open / pre-registered
- BSK3: the second gate of PAPER32's spec — khronon-dust lensing around isolated galaxies
  (1-3 Mpc flux, KiDS-1000 isolated lenses; the khronon-dust halo profile below/above the
  hold scale 1/mu; the web-field strength at isolated lenses) and cluster profiles (X-COP).
- The khronon mass mu itself: this lane derives a FLOOR from structure growth; the khronon
  action's own terms (c_2 window 7.3e-3..0.067, L340) do not fix mu — the floor is a new input.

## Honest scope
- Growth is linear, sub-horizon, Newtonian gauge, transfer-ratio sigma_8 (same primordial
  spectrum, khronon/LCDM growth ratios at matched k with LambdaCDM weights). Nonlinear
  corrections (halo formation) are not modeled.
- BS24's own khronon cosmology claims CMB agreement for their theory; this lane does not
  re-derive theirs — it runs the khronon fluid equations exactly as committed in BSK1
  (M4/M7) through the sigma_8 gate in the C-H/K footing with mu free. If BS24's khronon at
  1e-31 eV genuinely behaves as this fluid, their linear-scale claim is in tension with the
  result here (ratio 0.037); the difference (their khronon's stabilising terms vs the
  BSK1 M4/M7 response) is registered, not adjudicated here.
## BSX1 — the KiDS external-field gate on BS24's own DBI benchmarks (separate lane, separate session)

`BSX1_kids_external_field_gate.py` checks 8/8. Its MUTATE=1 control (a pure-dust khronon) fails G1 and E1, rc=1. It is labelled BSX, not BSK, so it does not collide with the BSK2/BSK3 sequence above; BSK1 is shared.

**What the MOND function reads.** Its argument is the acceleration of the khronon congruence, A = ∇Υ, with Υ = −4πGa²ρ_K Δ_K/(k² + k_J²) (BS24 eqs. 61b, 67). That is the khronon's own potential gradient, not the web's Newtonian field that C-H/K's kernel reads (BS2/BS3).

**Method.** Two-fluid sub-horizon GDM growth, run with BS24's own DBI background:
- w(a) and c_ad²(a) from their eqs. 89 and 94;
- the k-dependent sound speed of their eq. 71;
- their published benchmarks from Fig. 1.

**Controls.**
- ΛCDM gives σ₈ = 0.811.
- The ΛCDM field at z = 0.25 is 0.0134 a₀, against BS3's 0.0150.
- The late Jeans wavenumber is k_J = aμ exactly.
- A pure-dust khronon gives σ₈ = 0.82–0.85.

| benchmark | kernel field at KiDS lenses | vs bound 7.2e-5 | r_C (MW, BS24 eq. 38) | linear σ₈ |
|---|---|---|---|---|
| A: μ⁻¹ = 22.3 Mpc, λ_D = 1 | 1.7e-3 a₀ | ×24, fails | 1.7 Mpc | 0.21 |
| B: μ⁻¹ = 223 kpc, λ_D = 30 | 4.0e-5 a₀ | ×0.55, passes (linear theory at nonlinear k ~ k_J) | 0.08 Mpc | 0.26 |

**Scan over μ⁻¹ = 0.03–100 Mpc, λ_D = 1 and 30.**
- KiDS alone leaves no μ: the external-field bound needs μ⁻¹ ≲ 0.3 Mpc, while MOND-like lensing to ~1 Mpc needs μ⁻¹ ≳ 10 Mpc.
- σ₈ is 0.16–0.49 at every point.

**Reconciliation with BSK2 above.** BSK2 gets 0.037 of ΛCDM near μ⁻¹ ~ 43 h⁻¹ Mpc on a ΛCDM background, where the self-gravity cancellation acts at every epoch. BSX1 uses BS24's DBI history instead:
- before the DBI turning point (z ≈ 45 for A) c_ad → 0 and k_J → ∞, so the cancellation starts only after it;
- their eq. 90b gives twice the dust density early for λ_D = 1;
- the result is 0.26 of ΛCDM for A.

Both lanes find strong suppression. The size depends on the khronon's history before the turning point.

**Limits.** Linear theory. For B, the early epoch starts inside the integration window, so its suppression is a lower bound. The full static profile with the μ² term is not redone here; Mistele, McGaugh & Hossenfelder (2023) did it for AeST's identical static equation.
