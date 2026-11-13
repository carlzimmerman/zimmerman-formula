# From the constrained FRW scalar to density growth

Scope: the operative QX17 action, `P=Pi=0` background, ungated quadratic clock (also the flat gate to quadratic order), and **zero stiffness Hessian at Pi=0**. The exact one-component calculation includes the metric constraints and a cosmological constant. The two-component calculation below is its cold, subhorizon, Newtonian limit with pressureless baryons. It is not a radiation-era or CMB likelihood calculation. This is an independent derivation; no growth-gate numerical driver was imported.

## 1. Normalization and the homogeneous charge

Use proper time, `h=dot(a)/a`, `K=4 pi G`, `M2=1/(2K)`, proper wavenumber `k=k_com/a`, and

```text
F(Q)=mu^2 (Q-1)^2/(2K),       q=Qbar>0,
n=F_Q(q)=mu^2(q-1)/K,        a^3 n=n_c=constant,
rho=q F_Q-F=n(q+1)/2,        p=F=K n^2/(2mu^2),
rho+p=q n,                  q-1=K n/mu^2=I0/(2mu^2 a^3).
3 M2 h^2=rho+rho_Lambda,     dot(h)=-K q n.
```

Thus `n` is the homogeneous conserved clock charge, not exactly its energy density. The equality `rho=n` is a cold-limit approximation. The density has a dust term and a term proportional to `a^-6`. In particular, `w=(q-1)/(q+1)` and the background adiabatic sound speed is `(q-1)/q`; the latter is not the constrained, scale-dependent perturbative pressure coefficient derived below.

The Einstein normalization gives `G_mn=2K T_mn`, so the subhorizon Poisson factor is **K**, not `2K` or `K/2`.

## 2. Exact scalar constraint reduction and density observable

Choose unitary clock gauge with `tau=tau(t)`, `q=dot(tau)`, lapse `N=1+alpha`, spatial metric `a^2 exp(2zeta) delta_ij`, and scalar shift. Tangency gives `P^0=0`. With `J^i=sqrt(gamma)P^i`, the exact bulk matter action is `N sqrt(gamma)[F(q/N)-Pi-W(P)]`. At the origin, `W(P)=K P^2/2+O(|P|^3)`. The quadratic matter terms are

```text
L2_m/a^3 = q^2 F_QQ alpha^2/2 - alpha d - K |delta P|^2/2,
d=div(delta J)/a^3.
```

The longitudinal P constraint gives `P_i=partial_i alpha/K` and `d=-k^2 alpha/K`. The Einstein momentum constraint for the single clock component is `alpha=dot(zeta)/h` at nonzero k. The lapse equation fixes the shift. Using the background equations, the exact reduced action is

```text
S2 = 1/2 integral dt d^3k a^3/h^2 [ A dot(zeta)^2 - q n k^2 zeta^2 ],
A=(mu^2 q^2+k^2)/K,
d_t[a^3 A dot(zeta)/h^2]+a^3 q n k^2 zeta/h^2=0.              (1)
```

The Hamiltonian density and isotropic pressure before imposing the P equation are `rho=qF_Q-F+Pi+O(P^2)` and `p=F+O(P^2)`. Consequently their comoving perturbations are

```text
delta rho_com = -q^2 F_QQ alpha+d = -A alpha,
delta p_com   = -q n alpha,
c_eff^2(k)    = delta p_com/delta rho_com = q n/A.             (2)
```

There is no linear anisotropic stress. The matter shift variation vanishes in this gauge after enforcing tangency, so it is the clock's energy-comoving gauge. Baryon perturbations add momentum to the constraint; the single-component lapse relation must not be reused unchanged for that multi-component system.

The current supplies the same distinction. At linear order, its normal charge perturbation is `delta rho_Q=delta F_Q+d/q`, hence `delta rho_com=q delta rho_Q`. Although the homogeneous P is zero, the multiplier need not be: at zero stiffness `lambda=-dot(q)/q`. Its flux term in the covariant clock current is linear in P and cannot be discarded on a time-dependent background. The ADM and energy-conservation derivations above already include that effect.

Define the normalized comoving enthalpy perturbation `Delta=delta rho_com/(q n)`. The conventional comoving fractional energy perturbation is `(1+w)Delta`. Set

```text
Y=a^3 A dot(zeta)/h^2 = -n_c q Delta/h,
B=dot(q)/q-dot(h)/h.
```

Equation (1) then gives exactly

```text
dot(Delta)+B Delta = k^2 zeta/h,
ddot(Delta)+(2h+dot(q)/q)dot(Delta)
  +[c_eff^2 k^2+dot(B)+(2h+dot(h)/h)B]Delta=0.                (3)
```

This maps the physical observable without freezing the time-dependent gravitational coefficients. A positive `zeta` gradient in (1) does not imply the absence of gravitational density growth. In the cold limit, `dot(q)/q` is small, `dot(h)=-Kn`, and `ddot(h)=-3h dot(h)` to leading order, including a constant Lambda. The background term in (3) becomes `dot(h)=-Kn`, and

```text
ddot(delta_d)+2h dot(delta_d)
 = Kn [1-k^2/(mu^2+k^2)]delta_d
 = Kn mu^2/(mu^2+k^2) delta_d.                               (4)
```

An isolated-polytrope replacement `1-k^2/mu^2` drops the polarization contribution to A and creates an acoustic cutoff absent from (4).

## 3. Independent Newtonian canonical derivation with baryons

The cold weak-field action gives the same result without borrowing the one-component momentum constraint. Let s be the clock phase perturbation and `x=dot(s)-Phi`, suppress background tadpoles, and keep the leading quadratic terms:

```text
L2/a^3 = (mu^2/2K)x^2 + x Pi - K P^2/2
         - n |grad(s)|^2/(2a^2) - |grad(Phi)|^2/(2K a^2)
         - delta rho_b Phi + L2_b.
```

For each Fourier mode the auxiliary polarization gives `Pi=k^2 x/K`. The perturbed conserved charge is `delta N=(mu^2+k^2)x/K`; it is the leading clock contribution to the Poisson source. The resulting phase, continuity and Poisson equations are

```text
dot(s)=Phi+K n delta_d/(mu^2+k^2),
dot(delta_d)=-k^2 s,
-k^2 Phi=K(n delta_d+rho_b delta_b).
```

The pressureless baryons obey their own continuity and geodesic equations. Therefore

```text
ddot(delta_d)+2h dot(delta_d)
 = K[rho_b delta_b+n f delta_d],      f=mu^2/(mu^2+k^2),
ddot(delta_b)+2h dot(delta_b)
 = K[rho_b delta_b+n delta_d].                               (5)
```

For `N_e=ln a` the left sides divided by `h^2` are `delta''+(2+h'/h)delta'`; the right sides are divided by `h^2`. Baryon forcing in the dark equation is **not multiplied by f**. Corrections include finite `q-1`, horizon-scale effects, baryon pressure, radiation and photon drag. In the stated limit `delta_d=delta N/n` agrees with (3)'s observable up to these corrections.

As an external convention check, Ma and Bertschinger, *Cosmological Perturbation Theory in the Synchronous and Conformal Newtonian Gauges*, [arXiv:astro-ph/9506072v1](https://arxiv.org/pdf/astro-ph/9506072), equations (23), (30), and (67), supply the Einstein normalization and separate fluid/baryon equations. Their Thomson-drag term is one reason (5) is not a pre-recombination transfer calculation. They do not prove the QX17 polarization reduction.

## 4. What a finite stiffness changes

If the action is explicitly modified to have a smooth constant quadratic stiffness Hessian `Gamma>=0` at Pi=0, then

```text
A_Gamma=mu^2 q^2/K+k^2/(K+Gamma k^2),
c_eff,Gamma^2=q n/A_Gamma.
```

At fixed background, increasing Gamma decreases A and increases the pressure term. Thus zero Gamma is a growth-favorable reference among these smooth quadratic theories. It is not a rigorous growth envelope for the literal nonsmooth model. The original `gamma Pi_+^2/2` is C1, has no single quadratic Hessian at Pi=0, and a sign-changing Fourier mode samples both branches at arbitrarily small amplitude. One cannot assign it a single linear transfer function by silently selecting Gamma=0 or Gamma=gamma. A specified smooth completion or directional/nonlinear perturbation treatment remains necessary. A smooth flat blend with second derivative zero gives (1) at linear order.

## 5. Growth delay and limits of the imported mu floor

For (5), `f=1/2` at `1+z_t=mu/k_com`. This is a gradual crossover, not a hard growth onset. For `mu=198.25 Mpc^-1` the illustrative crossover redshifts at `k_com=0.2,2,20/3 Mpc^-1` are `990.25,98.125,28.7375`. Baryons continue to source the dark density before this crossover.

For an Einstein-de Sitter diagnostic with fixed baryon fraction `f_b` and temporarily fixed f, the source matrix on `(delta_d,delta_b)` is

```text
M = [[(1-f_b)f, f_b], [1-f_b, f_b]],
lambda_+ = [(1-f_b)f+f_b+sqrt(((1-f_b)f-f_b)^2+4f_b(1-f_b))]/2,
p_+ = [-1+sqrt(1+24lambda_+)]/4,         delta proportional a^p_+.
```

At `f_b=0.16`, even f=0 has a growing exponent about 0.613; f=1 has exponent 1. This frozen-f exercise is not an integrated growth ratio. A lower mu can produce a substantial accumulated delay, but a numerical or observational lower bound requires matched initial amplitudes, both species, the expansion history, and an actual observable. Arbitrarily normalizing the late-time density would remove the evidence being tested.

Using only the archive's illustrative `I0=4.037e-8 Mpc^-2`, `mu=198.25` has `q-1≈0.0202` and `w≈0.0100` at z=3400. The condition `q-1=1` is reached near z=12486. For mu=25120, the corresponding offset at z=3400 is about `1.26e-6`; `q-1=1` occurs near z=315018. These are background diagnostics, not radiation-era likelihood bounds. Radiation and photon-baryon coupling invalidate the pressureless two-fluid approximation around equality/recombination even when the clock itself is cold.

The historical `mu≈25120 Mpc^-1` floor cannot be re-certified from the isolated-fluid factor. Conversely, deriving (5) does not prove that mu=198.25 fits structure or the CMB. That lower-mu branch remains a distinct transfer/likelihood obligation. The companion growth-gate audit numerically compares bounded histories; this lane establishes the equations and their validity domain only.

## 6. Evidence contract

`check_growth_derivation.py` checks exact symbolic normalization, density-action conversion, cold-limit cancellation, and the two-fluid source matrix. It also compares the exact zeta-action first-order system against the independently transformed density ODE on a finite-q, self-consistent single-clock-plus-Lambda background, and tabulates illustrative crossover/offset values. The contract records the tested domain and excludes a cosmological fit, nonlinear formation, and the literal one-sided stiffness's missing linearization. Accepted output and provenance are linked from `RESULT.md`.
