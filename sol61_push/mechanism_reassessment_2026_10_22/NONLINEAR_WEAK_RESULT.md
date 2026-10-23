# Polarization removes the vacuum-only response argument

**The useful new result is conditional but decisive for how to proceed:** retaining the nonlinear log potential in the formal leading weak-field reduction adds a positive k² restoring term on a polarized background. The vacuum k⁴ response cannot be extrapolated into a galaxy to explain why galaxies settle and clusters do not. The same reduced energy is convex for a fixed source, which supplies an equilibrium-stability route but no attractor or cold-sector selector.

Base ce12fb3210a7c660537813b3bd57c64393ceef7c. Self-review; ten symbolic checks and a conditional numerical illustration. No full relativistic galaxy background was solved. The existing master action §7.4 explicitly states that its exact static metric/P/cold system was not solved, despite stronger language in §5. The separate D9b multiplier lane concerns a modified action and was not edited.

## 1. Which reduction is being tested

Let K=4piG, c=1, P a spatial vector in the local weak-metric limit, and L the orthogonal longitudinal Helmholtz projector under stated compatible boundary conditions. Let T=I-L. Freeze the baryonic Newtonian source g_N=grad Phi_N. The leading static field Lagrangian is

```
L_static = -|grad Phi|²/(2K) + P.grad Phi - W(K|P|) - rho_b Phi
           -gamma(div P)²/2 -gamma|curl P|²/2.
```

Eliminating Phi with its Poisson equation gives grad Phi=g_N+K L P. Up to a source-only constant, the effective spatial energy is

```
U[P]=integral [W(K|P|)-K|L P|²/2
              +gamma((div P)²+|curl P|²)/2-g_N.P].
```

This is a formal leading weak-field construction from the static sector, not an exact elimination of the nonlinear ADM constraints. In the scalar kinetic sector use the already derived flat coefficient B=K(2+3beta)/beta, so the leading kinetic energy is eta||dot P||²/2 plus B||dot sigma||²/2 where L P=grad sigma and homogeneous modes are treated separately. This kinetic extension on nonzero P is an approximation, not a completed finite-background constraint reduction.

Conditions needed for interpreting it: weak metric potentials, local scales small compared with cosmological curvature scales, background variations slow enough for a frozen-coefficient wave calculation, and a nonvanishing constraint margin. Metric corrections, the gamma d lapse factor, polarization/shift corrections of relative scale eta|P|²K/beta, cosmological terms, and backreaction/motion of the source have not been bounded uniformly here. If beta is near its tiny principal bound, neglecting polarization/shift terms is not justified. These omissions are not covered by the symbolic Hessian checks.

## 2. A convex energy and the law as its stationary condition

Define q=K|P|/a0, 0<=q<1, and

```
F(|P|)=W(K|P|)-K|P|²/2
      =(a0²/K)[-q-ln(1-q)-q²/2]
      =(a0²/K) sum_{n>=3} q^n/n.
```

Because ||P||²=||LP||²+||TP||², the same energy can be written

```
U=integral F(|P|)+K||TP||²/2
  +gamma(||div P||²+||curl P||²)/2-integral g_N.P.
```

F is increasing and strictly convex as a radial function, with positive radial and tangential Hessian eigenvalues away from P=0:

```
F_radial''=K[(1-q)^(-2)-1],
F_tangential''=K[(1-q)^(-1)-1].
```

At P=0 both eigenvalues vanish, but F remains strictly convex (its leading term is proportional to |P|³). Thus U is convex, and strictly convex on the admissible fixed-boundary space. The source term is linear. Subject to those hypotheses, there is **at most one** stationary minimizer. Existence, cap regularity, boundary compatibility and a coercive norm must still be established for a particular problem.

For spherical P, curl P=0 and LP=P under compatible radial boundaries. Its stationarity equation is

```
a0 q²/(1-q) - gamma(div P)' = g_N.
```

In the zero-stiffness limit, g=g_N+a0 q gives g=a0 q/(1-q), hence

```
g_N=g²/(g+a0).
```

This recovers the law within the declared static approximation. It does not mean the exact finite-stiffness relativistic action has this algebraic law at every radius.

A fixed-source reduced model with positive kinetic energy conserves kinetic plus U. Around an existing minimizer, its relative energy is nonnegative, furnishing a Lyapunov candidate. A PDE stability theorem also needs well-posed evolution and a norm controlled by that energy. It does not prove asymptotic settling: under closed boundaries the excess energy remains in the system. Outgoing radiation could carry it away in an open problem, but no scattering, damping rate or attractor has been established.

Use a finite domain or carefully defined relative energies. For an isolated deep-MOND profile P~1/r, the absolute remainder-energy integral has a logarithmic large-radius issue; we do not claim a finite global energy for an isolated system extending indefinitely.

## 3. Why a polarized background changes the dispersion

Put x=g/a0 and q=x/(1+x) for the local zero-stiffness constitutive background. For scalar-restricted fluctuations along a wavevector making angle theta with P, direct differentiation gives

```
H_scalar/K=x+(x+x²)cos²(theta).
```

This would give

```
omega²=[K(x+(x+x²)cos²(theta)) k²+gamma k⁴]/[B+eta k²].
```

But oblique scalar restriction is not automatically invariant. The parent also has transverse modes. We therefore checked their mixing rather than calling the preceding formula the full oblique dispersion.

The full potential Hessian W has eigenvalues wr=K(1+x)² along P and wt=K(1+x) perpendicular to it. In the longitudinal/transverse wave basis, eliminating the massive in-plane transverse response at low frequency gives the Schur complement

```
H_eff = W_LL-K-W_LT²/W_TT,
H_eff/K = x(1+x+cos²(theta))/(1+x-x cos²(theta)).
```

The denominator is >=1 for x>=0, so this is positive at x>0. The corresponding leading low-k branch is omega² approximately (H_eff/B)k². This elimination requires frequencies and gamma k² small compared with the transverse stiffness scale; it is not an exact finite-frequency three-mode dispersion formula.

Parallel and perpendicular propagation decouple, and there the earlier rational dispersion is exact for the frozen reduced model:

```
parallel: H_eff/K=x(2+x),
perpendicular: H_eff/K=x.
```

At x=0 the k² coefficient vanishes, recovering the vacuum k⁴ branch. Positivity also follows directly from the full spatial Hessian: W''>=K I and subtracting K L cannot create a negative quadratic direction; the gradient energy is positive. This statement concerns this reduced energy, not every nonlinear ADM mode.

## 4. Size of the effect in one declared illustration

Inputs: x=1, beta=0.02798 (the record's upper-bound input), L*=24pc, gamma=eta=K L*²/2, and inverse wavenumber k^-1=10kpc. These are not fitted here. At fixed x and L*, a0 cancels, so the same dimensionless calculation applies to both footings.

| direction | inverse angular frequency | omega/(ck) | k² restoring term / k⁴ term |
|---|---:|---:|---:|
| perpendicular | 0.2815 Myr | 0.1159 | 347,222 |
| parallel | 0.1625 Myr | 0.2007 | 1,041,667 |
| vacuum, x=0 | 165.86 Myr | not the polarized value | zero |

The 10kpc number is an illustrative frozen patch, **not** a demonstration that a real galaxy is uniform over that length. These are inverse angular frequencies, not relaxation times or front speeds. The beta value is not predicted and changing it changes the rates. No causality conclusion follows from a low-frequency phase speed alone.

The decisive implication is that the vacuum estimate was missing a term that dominates the restoring force in this example. Therefore our earlier 78–150kpc vacuum response radius must not be interpreted as a galaxy/cluster transition radius. It remains a property of the unpolarized approximation only.

## 5. What would constitute genuine mechanism progress next

A full finite-stiffness polarized background satisfying the same action remains required. This calculation gives two concrete checks for it: the reduced energy should approach the convex expression above in the appropriate weak-field limit, and its polarized finite-wavelength spectrum should reproduce the appropriate k² term where the approximation is valid. Failure of those checks would identify a bad reduction or a missing constraint contribution.

Even if they pass, the essential formation question remains: where does settling energy go, and what conserved interaction determines the cold-sector sourcing fraction? Convexity is not a substitute for that interaction. Radiation is an available hypothesis to test, not a newly established mechanism. The ongoing multiplier candidate is a separate route and may have separate conservation and stability obstructions.

## 6. Literature check

SciSpace was queried with: 'What prior work derives convex energy or nonlinear stability for gravitational polarization models of MOND, including the dispersion of perturbations around a nonzero polarized background and relaxation by outgoing waves?'

It returned, among others, Joachim Frenkler, *Non-Linear Stability of Spherical Systems in MOND*, arXiv:2402.11043v2 (22 March 2024), https://arxiv.org/abs/2402.11043v2. The primary abstract describes nonlinear stability for classes of spherical collisionless and fluid MOND equilibria. That is adjacent prior work, not a theorem about A33. Its hypotheses and proof have not been transferred here.

A primary publisher search also located *Dipolar dark matter simulations on galaxy scales with the ramses code*, MNRAS 517 (2022), https://academic.oup.com/mnras/article/517/1/498/6713968. The indexed publisher text distinguishes frozen-component stability from an instability in live simulations. Full-page retrieval failed, so exact equation-level comparison remains unverified. It reinforces the need to distinguish fixed-source energy from coupled-medium evolution, but supplies no proof for this model.

Gravitational polarization and MOND stability are established research topics. No claim of global novelty is made for convexity, polarization or wave relaxation. The model-specific algebra above is a local research result requiring comparison and independent review.

## 7. Verification and scope

The baseline script checks the radial/tangential Hessian, direct Cartesian Hessian, constitutive law, energy derivative, scalar angular stiffness, transverse Schur complement, two decoupling limits, and vacuum limit. It does not certify the full weak-field truncation error or solve a galaxy. The first probe had a Python syntax typo in two substitution calls; it was corrected before any numerical result. The subsequent transverse-mode extension was recorded as a post-probe audit addition, not disguised as pre-registration.

The bounded run, input/output hashes and software versions are in `nonlinear_weak_run/manifest.json`; the source is `nonlinear_weak_checks.py`. The deliberate mutation deletes F and must remove the nonlinear stiffness. The overall theory and research objective remain open.

Verification outcome: baseline **10/10**, validated manifest status `completed`; nonlinear-remainder deletion mutation **2/10**, expected exit 1, with the k² stiffness removed and response reverting to the vacuum example. Mutation outputs are separate diagnostics. Self-proofreading checked the distinction between the Hessians of W and F, scalar restriction versus full-vector mixing, angular frequency versus relaxation, and the approximation scope. No manuscript or adopted theory statement was changed.
