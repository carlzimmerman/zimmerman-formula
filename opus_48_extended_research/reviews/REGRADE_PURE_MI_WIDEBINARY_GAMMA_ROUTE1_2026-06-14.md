# REGRADE — Route [pure_mi_gamma]: wide-binary EFE boost on the framework's dS-Unruh modified inertia

*Opus 4.8 (1M) adversarial regrade, 2026-06-14. Verifier reproduced every load-bearing number from scratch
(/tmp/regrade_mi.py, regrade_weights.py, regrade_compare.py, regrade_mivsmg.py, regrade_identity_proof2.py,
regrade_final.py). Framework a0 = 9.36e-11 (Lambda-only). Quarantine held: a0/Z never asserted derived.*

## BOTTOM LINE

The route's **number is right** (gamma_cap = 1.137, reproduced independently three ways) and its **direction is right**
(the published 1.32 headline IS too high and should drop). But the route's **central mechanism claim is FALSE**, and
that false claim is load-bearing for two of its conclusions (the "MI vs MG theory-class gap" and the "hidden
discriminator"). The headline should drop from 1.32 to ~1.137 — but because the prior used the **wrong interpolation
(simple-mu)**, NOT because the prior used "modified-gravity machinery." The route's own "modified-inertia" tensor IS the
modified-gravity EFE tensor, algebraically, to 1e-16.

## (c) Is the MI gamma number right? — YES, verified independently

Reproduced from the exact 2D vector EOM `mu(|a|/a0) a_vec = F_vec` (no analytic shortcut), mu = exact inverse companion
of the framework's nu(y)=sqrt(1+1/y):
- perp (transverse) response = **nu(e) = 1.19795**
- par (radial) response = **1.01635**
- isotropic 3D orbit-average (2/3 perp + 1/3 par) = **1.13742** (Monte-Carlo over isotropic n_hat: 1.13740)
- operating-point subtlety correct: x_op = |a_ext|/a0 = nu(e)·e = 2.7534, giving the exact identity 1/mu(x_op) = nu(e).

The mu used is genuinely the framework's (inverse companion of dS-Unruh nu), NOT simple-mu, NOT standard-mu. The (2/3,1/3)
weighting is correct (eigenvalue multiplicity 2 for the transverse plane, 1 for the field axis; <(n.zhat)^2>=1/3). **No
arithmetic smuggle. The 1.137 is the correct value of the object the route computed.**

## (a)+(b) Did it smuggle normal MOND? / Is the MI-EFE derivation actually distinct from AQUAL? — THE KILL

**The route did NOT smuggle simple-mu into the number. But it smuggled a false PHYSICAL LABEL.** The route's
"static-Jacobian modified-inertia" tensor is *identically equal* to the AQUAL/QUMOND **modified-gravity** 1D-EFE tensor
at any fixed interpolation. Proven two ways:

1. Numerically, framework nu, e=2.2985:
   - STATIC-MI (route): perp 1.19795, long 1.01635
   - AQUAL/QUMOND (MG): perp = nu(e) = 1.19795, long = nu(e)+e nu'(e) = 1.01635
   - difference: perp 0.0, long < 1e-16, across e in [0.05, 100].
2. Symbolically/high-precision: the identity `1/[mu(x_op)(1+L_mu)] = nu(e) + e nu'(e)` holds for ANY inverse-companion
   (mu,nu) pair (it is forced by mu being the inverse of nu), so the route's tensor and the MG-EFE tensor are the same
   object — there is no MI-vs-MG difference in this static computation, only an interpolation choice.

**Consequence — the 1.137-vs-1.32 gap is 100% an INTERPOLATION difference, not a theory-class difference.** Feeding the
route's *own* machinery simple-mu reproduces the headline: simple-mu transverse = 1.3277, isotropic = 1.2401 — i.e. the
"1.32" the route attributes to "AQUAL modified gravity" is just the **simple-mu** number, which the route's MI tensor
also produces. The clean decomposition (one machinery, two axes):

| interpolation | a0 | e | transverse=nu(e) | iso cap |
|---|---|---|---|---|
| dS-Unruh (framework) | 9.36e-11 | 2.298 | 1.198 | **1.137** |
| dS-Unruh (framework) | 1.20e-10 | 1.793 | 1.248 | 1.174 |
| simple-mu | 9.36e-11 | 2.298 | 1.328 | 1.240 |
| simple-mu | 1.20e-10 | 1.793 | 1.399 | 1.295 |

The real correction is: **the prior headline used simple-mu (the wrong interpolation for this framework); the framework's
own dS-Unruh nu gives 1.137.** The route reached the right new number but mis-attributed the cause to "MI vs MG."

## (b) Is the MI-EFE derivation correct as MI? — NO, it is the MG tensor relabeled

Genuine Milgrom modified inertia is **time-nonlocal / trajectory-dependent**. Milgrom 2023 (arXiv:2310.14334) states the
MI EFE "depend[s] in different ways on dimensionless characteristics of the system, such as frequency ratios of the
external and internal fields, eccentricity of trajectories" — i.e. the inertia is a functional of the whole orbit, not an
instantaneous algebraic function of |a|. The instantaneous `mu(|a|/a0)a=F` the route solved is exactly the form that
reproduces the modified-GRAVITY EFE tensor (shown above). So the route did NOT compute a genuine MI-EFE distinct from MG;
it computed the MG-EFE tensor with the framework's interpolation and labeled it MI. The route's own banked docstring flags
this ("true MI evaluates the kernel on the full helical trajectory") but the headline ignores its own caveat.

## (d) Does the MI-vs-MG distinction open a hidden discriminator? — NO, spurious/wishful

The route claims the perp/par anisotropy (1.198/1.016) is "a genuine MI-vs-MG signature" separable by an
orientation-resolved DR4 velocity field. But that exact anisotropy is ALSO the MG (AQUAL/QUMOND) anisotropy — proven
identical to 1e-16. The static computation cannot distinguish MI from MG by construction, so there is **no hidden
discriminator here.** A real MI-vs-MG discriminator would have to exploit the genuine MI time-nonlocality (frequency/
eccentricity dependence) — which the route did not compute and which is far beyond a cap or even an anisotropy
measurement. The "hidden discriminator opens" claim is wishful and should be struck.

## (e) Both ways — the regrade verdict

- **No manufactured win:** correct. The new number (1.137) is genuinely lower than the published 1.32; the route does not
  inflate the framework. Good.
- **No lazy "MI=MG so 1.32 stands":** the regrade does NOT do this. 1.32 should fall to ~1.137 — but the *reason* is the
  interpolation (simple-mu -> dS-Unruh nu), not the theory class. The deficit-direction (thinner Newton clinch, worse
  MOND degeneracy) is correct and survives the re-attribution: gap-to-Newton 0.137; std-MOND-on-same-nu cap 0.174, so the
  within-interpolation a0 gap is ~0.037 and WB remain non-diagnostic of a0. These downstream numbers are unaffected by the
  mislabel because they only depend on the (correct) 1.137 value.
- **The route OVER-claimed specialness:** it dressed an interpolation correction as a deep "MI is different from MG"
  result and minted a non-existent discriminator from it. That is a (small) manufactured-significance, in the opposite
  direction from a win — it makes the framework look like it has a clean MI-vs-MG handle it does not have.

## What to bank

1. **Headline correction CONFIRMED:** framework wide-binary EFE cap = **gamma_cap ~ 1.137** (transverse 1.198, isotropic
   1.137, v/v_N = 1.066, +6.6%), framework a0=9.36e-11, robust 1.11-1.20 across the orbit-average convention. The prior
   1.20-1.32 was too high.
2. **Re-attribute the cause:** the prior headline was high because it used **simple-mu** (the wrong interpolation), NOT
   because it used "modified-gravity / AQUAL machinery." The static EFE tensor is identical for MI and MG at fixed nu.
3. **STRIKE the "MI vs MG theory-class gap" framing and the "hidden discriminator."** Both rest on a false premise. The
   genuine MI-vs-MG difference is time-nonlocal (Milgrom 2310.14334) and was not computed; the static anisotropy is shared
   by MG.
4. **Downstream standing UNCHANGED from the route's:** Newton clinch thinner (~3-4 sigma at DR4, not 5-8), MOND degeneracy
   worse (a0 gap within the framework's nu ~0.037), WB still a clean-ish framework-vs-Newton test and NOT an a0 test, front
   does not flip. These follow from the (correct) 1.137 regardless of the mislabel.
