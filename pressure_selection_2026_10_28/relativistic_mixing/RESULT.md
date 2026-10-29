# PN28 relativistic phase mixing: an exact normalization and a spatial discriminator

**Result.** The relativistic continuation changes the MC27 kinetic normalization from `2K/(3 ln R)` to

\[
\boxed{A_{\rm mix}=\frac{K}{\ln[Z(\beta\eta_{\min})/Z(\beta\eta_{\max})]},
\qquad P=A_{\rm mix}\ln R.}
\]

Here `A_mix=C/beta` is a phase-mixing pressure scale, **not yet the coefficient of a spatial logarithmic EOS**. The logarithmic partition ratio lies between `(3/2)ln R` and `3 ln R`. The old coefficient `2/3` is the nonrelativistic limit, not a relativistically protected normalization. Under the old, explicitly unproved energy/phase identifications, the broad-span control gives only **0.518–0.531 of the canonical target**, rather than the old 1.011 near-match, for the three illustrative density contrasts tested.

A separate exact continuation into a prescribed static gravitational field gives a stronger warning against inferring an EOS from the momentum tail: in the ultrarelativistic limit the same global `gamma=C/eta` construction yields **`P proportional to n^(4/3)`**, with finite phase endpoints. It does not yield a spatial logarithm in that limit.

**Disposition:** a new conditional kinetic calculation is complete; independent physical normalization is not. Neither a kinetic/vacuum energy identity, a physical phase span, nor a massive mixed-regime self-gravitating logarithmic attractor has been derived.

## 1. Provenance and assumptions

Requested base is `66c45c5082f651dd54e171f98c11acd9cb3d9086`. The commit exists. HEAD was `52b354a1f316c1e89343db5fde30d12d6804575b` on initial read and advanced during this task. The four MC27 inputs are present in the workspace but absent from the requested commit; they must not be described as base-committed evidence. Their exact SHA-256 hashes and base-presence checks are in [INPUTS.json](INPUTS.json). No source outside this directory was changed.

This is new analytical route work, self-reviewed and checked with bounded computations. It uses the earlier homogeneous entropy-mixture ansatz as a **conditional definition**, not a proved gravitational relaxation law. The mathematical contract is:

- one massive species, `m>0`, in its local rest frame; canonical three-momentum measure `d^3p`;
- number phase-density levels `eta>0`; `f(p)` integrates to number density `n`, and `rho=mn` is rest-mass density;
- kinetic energy `E(p)=sqrt(m²c⁴+p²c²)-mc²` and group velocity `v=partial E/partial p`;
- isotropy, a spatially homogeneous reference box, positive energy multiplier `beta`;
- finite fixed phase interval `0<eta_min<eta_max<infinity`, with level volume per spatial volume `gamma(eta)=C/eta`;
- dilute occupancy, so the exclusion denominator is replaced by one, as in MC27.

Using mass rather than number phase-density changes the constant unit convention and multiplier; it does not change the dimensionless ratios derived here. It still requires a fixed phase-space measure. The full excluded entropy problem at the same prescribed phase volumes has not been inverted. Neither phase-level shape nor its endpoints are selected by this calculation.

## 2. Exact one-level partition and moments

Put `t=beta*eta`, `z=t*m*c²` and

\[
Z(t)=\int_{\mathbb R^3} e^{-tE(p)}\,d^3p.
\]

The normalized mixture is

\[
f(p)=\int\frac{\eta\gamma(\eta)}{Z(\beta\eta)}
e^{-\beta\eta E(p)}\,d\eta
=C\int_{\eta_{\min}}^{\eta_{\max}}
\frac{e^{-\beta\eta E(p)}}{Z(\beta\eta)}\,d\eta.
\]

Thus every interval `d eta` carries the same particle number `C*d eta`, and

\[
n=C(\eta_{\max}-\eta_{\min}).
\]

Define `K_nu(z)=integral_0^infinity exp(-z cosh u) cosh(nu u) du`. Substituting `p=mc sinh u` into the radial momentum integral gives `Z=pi*m³c³*exp(z)*(K_3-K_1)`. Integrating the derivative of `exp(-z cosh u)sinh(2u)` establishes `K_3-K_1=4K_2/z`. Therefore

\[
\boxed{Z(t)=4\pi m^3c^3\,\frac{e^z K_2(z)}{z}.}
\]

This integral derivation is provided directly; no external normalization convention is imported. In particular, this is the canonical equal-time measure, not `d^3p/E`.

For one normalized level, integration of `div_p[p exp(-tE)]` over momentum gives

\[
\langle p\cdot v\rangle_t=\frac3t,
\qquad P_{\rm per\ particle}=\frac1t.
\]

The kinetic mean follows by differentiation:

\[
\langle E\rangle_t=-\partial_t\ln Z(t)
=mc^2\left[\frac{K_1(z)}{K_2(z)}+\frac3z-1\right].
\]

It is useful to define

\[
D(z)=t\langle E\rangle_t
=3+z\frac{K_1(z)}{K_2(z)}-z.
\]

The pressure–energy bounds need no special-function inequality. Direct differentiation of the kinetic energy gives

\[
p\cdot v=E\,\frac{E+2mc^2}{E+mc^2}.
\]

For `0<E<infinity` the factor is strictly between 1 and 2. Consequently every positive finite-temperature massive distribution has

\[
\frac{K}{3}<P<\frac{2K}{3},
\qquad \frac32<D(z)<3.
\]

The limits are `D->3/2` for `z->infinity` and `D->3` for `z->0`. Here `K` excludes rest energy. Including rest energy adds `rho*c²` and changes the energy budget without changing pressure; it cannot be silently included in the proposed equality to vacuum energy.

## 3. The exact broad-level normalization

Integrate the one-level moments over `C*d eta`:

\[
P=\frac C\beta\int_{\eta_{\min}}^{\eta_{\max}}\frac{d\eta}{\eta}
=\frac C\beta\ln R,\qquad R=\frac{\eta_{\max}}{\eta_{\min}},
\]

\[
K=C\int\langle E\rangle_{\beta\eta}\,d\eta
=\frac C\beta\ln\frac{Z(\beta\eta_{\min})}{Z(\beta\eta_{\max})}.
\]

Writing `A_mix=C/beta`, `z_min=beta*eta_min*mc²`, `z_max=R*z_min`, and

\[
I=\ln\frac{Z(\beta\eta_{\min})}{Z(\beta\eta_{\max})}
=\int_{z_{\min}}^{z_{\max}}D(z)\,d\ln z,
\qquad \bar D=I/\ln R,
\]

gives the compact exact system

\[
\boxed{K=A_{\rm mix} I,\quad P=A_{\rm mix}\ln R,\quad
\rho c^2=A_{\rm mix}(z_{\max}-z_{\min}).}
\]

Thus

\[
\boxed{\frac{K}{3\ln R}<A_{\rm mix}<\frac{2K}{3\ln R}.}
\]

The pressure contribution per logarithmic phase interval is always `A_mix`. Its kinetic-energy contribution is `A_mix*D(z)`, which changes by a factor of two between limits. The nonrelativistic statement that each logarithmic phase interval carries `3A_mix/2` of kinetic energy is not valid in the hot part of a broad relativistic mixture.

**Selection test.** `K` and the ratio `R` alone do not fix `A_mix`: the interval's location relative to the relativistic scale remains free. Continuously move both `z` endpoints at fixed `R`, and choose `C/beta=K/I`; the bounds are approached at the two ends. The bounded run exhibits fixed `K=1,R=10^6` with `A_mix=0.0241281,0.0245977,0.0316943,0.0482506` at `z_max=10^-3,1,10^3,10^9`. These are different rest densities, not different states with every physical input held fixed.

If **the entire phase distribution**, including `C` and endpoints, and the energy are given, normalization can instead be determined conditionally. Equivalently, specifying `rho`, `K`, and `R` fixes the dimensionless temperature interval through `K/(rho*c²)=I/(z_max-z_min)`. For a fixed level interval, the kinetic mean decreases strictly with beta because `partial_beta <E>_(beta eta)=-eta*Var(E)<0`. This gives uniqueness of that conditional temperature choice. It is state determination after supplying inputs, not a universal relation to vacuum energy.

## 4. Momentum tails and their limited meaning

In an intermediate range where both phase endpoints are remote from the dominant inverse energy, the limiting partition functions give:

| Limit | Partition | Mixture tail |
|---|---|---|
| Nonrelativistic `p<<mc`, contributing `z>>1` | `Z(t)~(2*pi*m/t)^(3/2)` | `f(p)~[3m*A_mix/(2*pi)] p^-5` |
| Ultrarelativistic `p>>mc`, contributing `z<<1` | `Z(t)~8*pi/(c³*t³)` | `f(p)~[3*A_mix/(4*pi*c)] p^-4` |

These follow by changing variable to `beta*eta*E` in the finite mixture and extending its endpoints only in the stated intermediate limit. At fixed finite `eta_min`, the ultimate high-momentum tail remains exponentially cut off. The low-momentum distribution is regular. The `p^-4` tail is not a velocity tail extending beyond `c`.

In either intermediate limit,

\[
\frac{dK}{d\ln p}=4\pi p^3E(p)f(p)\longrightarrow3A_{\rm mix}.
\]

The momentum span corresponding to a phase span is `ln R/2` in the nonrelativistic regime and `ln R` in the ultrarelativistic regime. This directly accounts for the change from `3/2` to `3` in the energy normalization.

These formulas concern momentum-space moments. No spatial potential, self-consistent halo, or `P(rho)` relation has entered them. Holding the phase-volume distribution fixed while varying beta already changes pressure at the same number density; homogeneous mixing alone is not a barotropic closure.

## 5. A new spatial discriminator: the static relativistic extension

There is a useful concrete continuation that tests the temptation to equate the new tail with a spatial logarithm. Consider a **prescribed** static spacetime

\[
ds^2=-N(x)^2c^2dt^2+h_{ij}dx^i dx^j,\qquad N>0,
\]

on a finite reflecting spatial domain, with no shift. Let `p` be local orthonormal momentum. The mass-shell equation gives the conserved one-particle Hamiltonian

\[
H=N(x)\epsilon(p),\qquad \epsilon=\sqrt{m^2c^4+p^2c^2}.
\]

An additive reference rest energy is irrelevant to a normalized level. For relativistic momenta, replacing this Hamiltonian by `E_kin+m*Phi` drops the gravitational coupling to kinetic energy and is not this continuation.

With global `gamma_total(eta)=C_total/eta`, define

\[
Z_{\rm tot}(t)=\int d^3p\,e^{-t\epsilon(p)},\qquad
\mathcal Z(t)=\int_V dV\, Z_{\rm tot}(N(x)t).
\]

The same dilute level-volume normalization now fixes

\[
f(x,p)=C_{\rm total}\int
\frac{e^{-\beta\eta N(x)\epsilon(p)}}{\mathcal Z(\beta\eta)}\,d\eta.
\]

This is stationary along trajectories since it is a function of the conserved Hamiltonian. It does not solve the Einstein equations for `N,h`. Its local moments are

\[
n(x)=C_{\rm total}\int\frac{Z_{\rm tot}(N t)}{\mathcal Z(t)}\,d\eta,
\]

\[
P(x)=C_{\rm total}\int\frac{Z_{\rm tot}(N t)}{Nt\,\mathcal Z(t)}\,d\eta,
\quad t=\beta\eta.
\]

At fixed fugacities/global normalizations, differentiation gives the exact hydrostatic moment identity

\[
\frac{dP}{d\ln N}=-(\varepsilon_{\rm total}+P).
\]

In the **massless limit**, or uniformly ultrarelativistic occupied levels, `Z_tot(t)=8*pi/(c³t³)`. Put `V_N=integral_V N^-3 dV`. For exactly massless particles the finite-endpoint expressions are then exact:

\[
n(x)=\frac{C_{\rm total}(\eta_{\max}-\eta_{\min})}{V_N}N^{-3},
\qquad
P(x)=\frac{C_{\rm total}\ln R}{\beta V_N}N^{-4},
\qquad \varepsilon_{\rm total}=3P.
\]

Therefore `P/P0=(n/n0)^(4/3)` along this stationary solution. Global phase-volume conservation is included in `V_N`; this is not a freely chosen local Maxwellian normalization. For a small but finite mass, the result is the controlled all-hot limit; a rest-mass-density comparison can then be made with `rho=mn`. In the exactly massless case `n` is number density, not rest-mass density.

The conserved energy for this static extension is the **Killing energy** `integral N*epsilon_total dV`, not the unweighted local proper-energy integral. In the massless case it equals `3*C_total*ln R/beta`. A proposed vacuum energy budget has to specify which covariant energy and spatial domain it means before importing the homogeneous identity.

This is an explicit, consistent counterexample to the implication “relativistic `p^-4` mixing tail implies spatial logotropic pressure.” It leaves open a genuinely massive mixed-temperature, self-gravitating core with a separately derived exchange/boundary mechanism. It supplies no proof that such a core cannot exist.

## 6. Recompute the old near-match as a labelled conditional control

For comparison only, retain both unproved identifications used in MC27:

`K=Vphys=rho_Lambda*c²`, and `ln R=1/0.00353241107337=283.0927599391702`.

Also specify the illustrative rest-density contrast `d=rho/rho_Lambda`. The exact system requires

\[
\frac{I}{z_{\max}-z_{\min}}=\frac1d,
\qquad z_{\min}=z_{\max}e^{-\ln R},
\qquad \frac{A_{\rm mix}}{V_{\rm phys}}=\frac1I.
\]

| Illustrative `d` | `D_bar` | Conditional `A_mix/Vphys` | Ratio to `0.0023294580123` |
|---:|---:|---:|---:|
| `10^3` | 2.92943953 | 0.001205831708 | 0.51764475 |
| `10^6` | 2.89290449 | 0.001221060386 | 0.52418218 |
| `10^9` | 2.85637029 | 0.001236678274 | 0.53088670 |

The old nonrelativistic value was `0.002354940716`; the pure ultrarelativistic limit is `0.001177470358`. The very broad phase span places most logarithmic levels on the hot side even when the bulk rest density is large. In the mixed limit `z_min<<1<<z_max`,

\[
I=3\ln R-\frac32\ln z_{\max}
+\frac12\ln(8/\pi)+o(1),
\]

which explains the table. Here the remainder tends to zero as `z_min->0,z_max->infinity` with the displayed mixed hierarchy.

This is **not** a new prediction for the physical logotropic coefficient. The energy-to-vacuum and phase-to-density maps remain unproved, and section 5 shows why the spatial-EOS bridge must also be derived. What fails is the numerical robustness of the old homogeneous kinetic near-match under the specified relativistic repair.

## 7. Verification, controls and limits

The pre-run [contract.json](contract.json) and [check_relativistic_mixing.py](check_relativistic_mixing.py) produced [run_001/manifest.json](run_001/manifest.json), status `completed`. All ten declared checks passed. They include a symbolic pressure/energy identity, seven independent energy-variable partition/moment quadratures, four phase-span energy-integral comparisons, six tail points, a fixed-energy/fixed-span counterfamily, and the three conditional energy-density solutions. Maximum level-energy discrepancy was `2.1e-13`; maximum phase-integral relative discrepancy was `6.4e-14`.

The partition implementation uses scaled Bessel functions in its central range, the small-z expansion below `10^-6`, and a four-term large-z expansion above `10^5`. Independent energy-variable quadrature covers both asymptotic implementations. These are numerical error checks, not rigorous interval bounds. Universal pressure bounds and limiting powers follow from the written arguments, not the finite samples.

The separately frozen [lapse_contract.json](lapse_contract.json) and [check_lapse_extension.py](check_lapse_extension.py) produced [run_lapse/manifest.json](run_lapse/manifest.json), status `completed`. Four checks passed for finite two-cell prescribed lapse fields: global number normalization, the all-hot `4/3` pressure-density power, the Killing-energy moment, and the hydrostatic identity. This is a moment-discriminant calculation, not a simulation or a self-consistent spacetime.

Both manifests passed the computation-audit v2 validator against current input hashes. No expensive job, halo fit, external download, or original-source mutation was performed. No external theorem or novel-literature claim is needed for the displayed elementary phase and mass-shell derivations. Mathematical proofreading was confined to this new report: energy conventions, positive domains, dimensions, phase measure, and the distinction between momentum tails and spatial EOS were checked.

**Next required physical step:** derive, from one explicit parent dynamics, the selected phase spectrum and its relativistic cutoffs, the conserved energy/transfer budget, and a spatial distribution satisfying the actual gravity equations. That parent must determine how `K`, `rho`, `R` and the local logarithmic response co-vary. The completed relativistic calculation supplies exact conditions it must satisfy; it does not supply that parent.
