# The CLASS Euler-equation hook — modified inertia in a real Boltzmann code (Fable priority #1)

*C. Zimmerman, 2026-06-09. The gold-standard run Fable asked for: inject the framework's deep-MOND shape into the photon–baryon **baryon Euler equation** inside CLASS (a real Boltzmann hierarchy), not the toy single-oscillator ODE — to convert the provisional Δχ²≈81 FLAT exclusion into a full-Boltzmann verdict and adjudicate the syllogism (framework's own shape + Planck ⇒ declining by elimination).*

## Result (one line)
**At full-Boltzmann grade the syllogism HOLDS: constant a₀ → Δχ²≈117 (CMB-excluded), rising → dead, declining → Δχ²≈0 (safe). The framework's own slow simple-IF shape plus Planck leaves DECLINING the lone CMB survivor** — vindicating the toy ODE's provisional ≈81 (same order). **Caveat:** modified inertia is *nonlinear in amplitude*, so this requires the physical-amplitude calibration (below); the number is "order 100, robustly ≫1," not precise to better than a factor of a few.

| Run (patched CLASS, both regimes) | peaks ℓ | max\|ΔCₗ/Cₗ\| | Δχ² (θ*-marg, CV-limited) | verdict |
|---|---|---|---|---|
| unmodified (`MOND_MODE=off`) | 221,537,816 | — (== standard ΛCDM) | — | validation ✓ (matches CAMB) |
| **declining** (physical amp) | 221,537,816 | 0.40% | **0.0** | **SAFE** |
| **constant a₀** (physical amp) | 220,535,815 | 6.6% | **116.6** | **EXCLUDED** |
| **rising** (physical amp) | 498,862,1218 | catastrophic | ≫10⁶ | **DEAD** |
| constant a₀ (CLASS-internal norm) | 221,537,816 | 0.002% | 0.0 | *artifact of unphysical normalization* |

## Method
- **Code:** CLASS v3.3.4 (the `classy` sdist), built as the `class` executable with system clang (Homebrew gcc-15 hits a macOS-SDK `_bounds.h` incompatibility; OMPFLAG is `-pthread`, no OpenMP needed).
- **Patch (`perturbations_mond.patch`, 3 regions of `source/perturbations.c`):** a file-scope helper `_zimmerman_gforce(gbar,a,k)` replaces the baryon net peculiar force g_bar by the framework's **own derived deep-MOND shape** g_obs = sign(g)·√(g² + |g|·a0_code). It is applied in **both** the post-tight-coupling (tca-off) **and** the tight-coupling (tca-on) baryon Euler, so the modification acts over the **full acoustic history**, not just at last scattering. The Hubble momentum-redshift term −(a′/a)θ_b is left unboosted. Branch and a₀(0) come from env vars (`MOND_MODE` ∈ {off,flat,rising,declining}, `MOND_A0`), so one binary serves every mode.
- **a₀(z):** flat = const; rising = a₀·√(Ω_m(1+z)³+Ω_Λ); declining = a₀·√(ρ_DE(z)) with DESI w₀wₐ (w₀=−0.752, wₐ=−0.86). Prescribed analytically on a fixed ΛCDM background, so the only thing that changes between modes is the inertia modification (clean comparison; the ΛCDM background stands in for an AeST-completed one that otherwise fits Planck).
- **Unit map:** a_proper[SI] = (c²/L_Mpc)·|g_bar|/(k·a) ⟹ a0_code = a₀(z)·k·a/(c²/L_Mpc)/A_phys.
- **The nonlinearity / amplitude calibration (the crux):** modified inertia is **nonlinear** in the acceleration, so its strength depends on the *absolute* perturbation amplitude — which CLASS integrates at an arbitrary O(1) normalization. Probing the code (`MOND_DBG=1`) gives a_proper_code ≈ 3.1×10⁻⁵ at recombination for the peak-1 modes; the physical baryon acceleration there is ≈10⁻⁹ m/s², so the physical amplitude is **A_phys = MOND_AMP ≈ 3.18×10⁻⁵** (reassuringly ≈ √A_s = 4.6×10⁻⁵). At `MOND_AMP=1` (CLASS-internal) the nonlinear boost is ~10⁵× too weak and *flat reads Δχ²=0* — the artifact in the last table row. **The physics requires the physical-amplitude run.**
- **Metric:** θ_*-marginalized (uniform ℓ-rescale, refitting the acoustic scale) cosmic-variance-limited Δχ² over ℓ=30–2000, f_sky=0.7, unlensed TT.

## Reproduce
```
pip download --no-deps --no-binary :all: classy -d /tmp/cs       # get the v3.3.4 sdist
mkdir /tmp/cm && cd /tmp/cm && tar xzf /tmp/cs/classy-3.3.4.0.tar.gz && cd classy-3.3.4.0
patch -p0 source/perturbations.c < .../cmb_class_mond/perturbations_mond.patch  # (paths in the diff header)
make class                                                       # system clang
# lcdm.ini: output=tCl, l_max_scalars=2600, lensing=no, Planck-2018 params, root=/tmp/cm/o_off_
for m in off flat rising declining; do
  MOND_MODE=$m MOND_A0=9.36e-11 MOND_AMP=3.18e-5 ./class run_$m.ini   # MOND_AMP=1 reproduces the artifact
done
python analyze_cmb_mond.py
```

## Honest caveats
1. **Amplitude/prescription dependence.** Δχ²≈117 scales with A_phys and the IF prescription; a factor ~2 in A_phys → factor ~4 in Δχ². So treat it as "robustly excluded (≫1), order 100," not a precise number. What's *robust*: declining is safe and rising is dead at **any** amplitude (a₀(z_rec) is 169× below / 2×10⁴× above the fluid acceleration respectively); only the *constant* case lives in the amplitude-sensitive window.
2. **Modeling choice.** Applying the (non-local) modified-inertia μ to a relativistic photon–baryon fluid as a local force-boost in both regimes is a defensible prescription (the framework's own shape), not a unique one.
3. **CV-limited, unlensed TT.** Real Planck noise + lensing would modestly reduce the high-ℓ contribution; most of the 117 is in the CV-dominated acoustic band, so the exclusion stands.
4. This stands in for the AeST-completed background (CDM-like clustering present so the peaks are realistic); the *separate* branch-independent obstruction — that a pure-baryon modified-inertia universe can't make Planck's 3rd peak without that extra field — is the P3/P2 result (`../cmb_third_peak_dm_mimic.py`).

## Bottom line for the syllogism
Fable: *"framework's derived shape + Planck ⇒ declining by elimination, every link conditional."* This run discharges the load-bearing link at full-Boltzmann grade: **constant a₀ is CMB-excluded under the framework's own slow-IF shape** (Δχ²≈117), rising dead, declining safe — the elimination runs *in the framework's favor*. The framework's rigidity (it can't take the faster-IF escape, since the slow IF is its one derived result) is what makes constant fail and declining win — a virtue, made quantitative. The evolution leg remains underived and non-adiabatic at z=3 (ε≈4–28); the telescope still settles the bet.
