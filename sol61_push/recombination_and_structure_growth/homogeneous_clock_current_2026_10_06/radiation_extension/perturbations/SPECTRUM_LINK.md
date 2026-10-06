# Actual radiation histories admit transverse crossings

This analytic note connects the conditional six-state theorem to an actual continuous Fourier spectrum. It is separate from the frozen executable inputs. It uses the parent tuned background with eta>0, kappa>0, 0<r_f<3/4, and d_f=1-4r_f/3>0; the perturbation theorem additionally requires 0<eta<1. No new numerical result or mode-transfer calculation is claimed.

Normalize x=a_FRW/a_f and k_bar=k/(H_star a_f). On the early upper branch 0<x<1 define the comoving kinetic envelope

`S_rad(x)=3eta[h(x)-1-eta] x²/kappa`.

The exact kinetic coefficient obeys

`K_c/M = kappa[k_bar²-S_rad(x)]/[x²(h(x)-eta)²]`.

The parent expansion gives `h=alpha x^-2+beta x^-1+gamma+o(1)`, with alpha=sqrt(2eta r_f)>0 and beta=eta d_f/alpha>0. Hence

`S_rad(x)=S_0+(3eta beta/kappa)x+O(x²)`,

`S_0=3eta sqrt(2eta r_f)/kappa>0`.

The background implicit derivative is `h'=B'(x)/f'(h)`; expanding this independently gives `h'=-2alpha x^-3-beta x^-2+o(x^-2)`. Thus S_rad' tends to the positive 3eta beta/kappa, rather than requiring an unjustified differentiation of a little-o remainder. S_rad extends continuously to x=0 with S_0 and has S_rad(1)=0. It therefore rises above S_0 near zero. Its maximum S_max on [0,1] is attained in the interior and is strictly larger than S_0.

For every level s in (S_0,S_max), continuity gives at least two distinct roots of S_rad(x)=s: one before an interior point above s and one after it toward x=1. Such modes are kinetic-positive in the earliest radiation limit and at the background fold but have a negative interval in between. This is a second class beyond modes below S_0, which are early-negative and must encounter at least one zero before the fold.

S_rad is real analytic on (0,1) and nonconstant. Its critical points are isolated and therefore countable; their image is a countable set of critical values. Choosing s in the nonempty open interval (S_0,S_max) outside that set makes every root transverse. At each such root,

`alpha_cross/M = -kappa H S_rad'(x)/[x(h-eta)²]`,

which is finite and nonzero. Both matter densities, q and Theta are finite and positive/nonzero there under the perturbation report's hypotheses. The six-state analytic simple-zero theorem therefore applies at these actual crossings. This proves the existence of uncountably many mode levels with at least two simple crossings in the continuous-spectrum model, without inferring universality from one numerical root.

For each affected real Fourier sector, generic linear initial data have the nonzero compatibility amplitude and the invariant clock-norm pole. A regular crossing restricts one amplitude. A finite-volume discrete spectrum, an explicitly restricted spectral domain, changed quadratic operators or a nonlinear completion must be assessed separately. This is not a claim that every mode crosses, every crossing is simple, or every conceivable cosmology is excluded; neither a nonlinear endpoint nor a quantum decay rate follows.
