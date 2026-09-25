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