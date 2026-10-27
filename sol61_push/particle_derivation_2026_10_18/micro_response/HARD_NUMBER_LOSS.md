# A hard weighted-number-loss channel in the original cubic action

19 October 2026 UTC. This bounded calculation concerns the original charged carrier action, not the separately tuned real-mediator host. It supports a restricted emergent positive-current hierarchy. It is not a cosmological abundance, halo-density or complete reaction-network theorem.

**Result.** The charge-neutral source pair has the allowed tree reaction `X+X−→Phi+Phi−`. With the original cubic coupling `g`, its source-CM-threshold cross section times the incoming relative flux velocity is

$$
\boxed{\langle\sigma v_{\rm rel}\rangle_{p\to0}
=\frac{\beta_f g^4}{2\pi M^6},\qquad
\beta_f=\sqrt{1-m^2/M^2}.}
$$

For the declared `m=1 MeV`, `u*=.02`, `r_lambda=2`, `sigma0/m=.3 cm²/g` benchmark this is `5.5476552e−25 cm³/s`. Per positive source the loss/decay ratio is

$$
\boxed{\frac{\Gamma_{\rm ann,+}}{\Gamma_{\rm dec}}
=2.0349854\times10^{-4}\,\frac{n_{X-}}{M^3}.}
$$

The density on the right is in natural units and is **per opposite-charge species**. A neutral total source density `n_X=n_X++n_X−` has `n_X−=n_X/2`. The smallness criterion is this explicit ratio; the word “dilute” without a state/density convention does not establish it.

## 1. Original action, charge flow and unique tree graph

Use `hbar=c=1`, signature `+---`, and the original interaction

$$
L_{\rm int}=-g(X^*\Phi^2+X\Phi^{*2})-\lambda_{\rm tot}|\Phi|^4,
\quad q_\Phi=1,\quad q_X=2,\quad M>2m.
$$

Label incoming momenta `P1` for `X+`, `P2` for `X−`, and outgoing momenta `K1` for `Phi+`, `K2` for `Phi−`. The source vertices have Feynman factor `−2ig`: differentiating with respect to the two identical daughter fields gives the factor two. The `X+` vertex can emit the outgoing `Phi+`, while its remaining daughter line joins the conjugate vertex. Define

$$
t=(P_1-K_1)^2.
$$

There is one exchanged-`Phi` diagram at order `g²`, with

$$
i\mathcal M=(-2ig)^2\frac{i}{t-m^2},\qquad
\boxed{\mathcal M=-\frac{4g^2}{t-m^2}.}
$$

There is no additional `u=(P1−K2)²` diagram for these specified charges: an `X+` vertex attached to outgoing `Phi−` would need a charge-three internal line, absent from the action. Interchanging the external charge labels describes the conjugate/labeled process, not a second graph to add to this amplitude. Same-sign source pairs cannot end in two daughters because their charges would not match. The original quartic has no external `X` leg and supplies no direct `X X* Phi Phi*` contact at this tree order. Additional interactions or loop-induced mixed quartics are not included.

At incoming CM momentum `p=0`, each incoming and outgoing energy is `M`. The final momentum is

$$
k_f=\sqrt{M^2-m^2},\qquad t-m^2=-M^2,
\qquad \mathcal M_0=+4g^2/M^2.
$$

Since `M>2m`, `k_f>sqrt(3)m`; these are hard daughters, unlike the slow daughters of a single near-threshold source decay. At the benchmark `k_f/m=1.7325126`, versus single-decay momentum `.02m`. The final daughters each have energy approximately `2m` and speed `.866083c`.

The external source is unstable, so the cross section is understood for prepared narrow source quasiparticles. The benchmark has `Gamma_dec/M≈9.35e−10`, making that vacuum narrow-width approximation parametrically well separated from the mass scale. This does not specify how such a stock is prepared or maintained.

## 2. Flux, phase space and the identical-particle factors

The incoming `X+` and `X−` are distinct species, and the final `Phi+` and `Phi−` are also distinct. Thus neither the event rate nor the integrated final phase space has an identical-particle `1/2!` factor. The factors two are already in the two cubic vertices.

With invariant flux `F=sqrt[(P1·P2)²−M⁴]`,

$$
\sigma=\frac1{4F}\int d\Phi_2|\mathcal M|^2,
\qquad v_{\rm rel}=\frac F{E_1E_2},\qquad
\int d\Phi_2=\frac{\beta_f}{8\pi}
$$

for the angle-independent threshold amplitude. Therefore

$$
\sigma v_{\rm rel}=\frac{|\mathcal M_0|^2\beta_f}{32\pi M^2}
=\frac{\beta_f g^4}{2\pi M^6}.
$$

This is the usual incoming Lorentz flux velocity; in the equal-mass CM frame it is `2p/E`. The cross section itself diverges as `1/v_rel` at the exothermic threshold, while `sigma v_rel` is finite.

A useful finite-momentum check is available without a numerical scattering calculation. Put

$$
E^2=M^2+p^2,\quad k^2=E^2-m^2,\quad z=\cos\vartheta,
\quad t-m^2=-(A-Bz),
\quad A=M^2+2p^2,\quad B=2pk.
$$

Then `A²−B²=M⁴+4m²p²>0`, so the virtual daughter never has an on-shell pole in the physical angular range. No real-intermediate-source subtraction is required for this graph. Integrating `∫[-1,1]dz/(A−Bz)²=2/(A²−B²)` gives

$$
\boxed{\sigma v_{\rm rel}(p)
=\frac{g^4\sqrt{1-m^2/E^2}}
 {2\pi E^2(M^4+4m^2p^2)}.}
$$

It approaches the stated threshold formula. Four direct Simpson angular integrals at `p/M=.0001,.001,.01,.1` independently check the closed expression within the declared `2e−12` relative gate.

For comparison, a single source decays into two identical same-charge daughters. Its final-state factor is `1/2!`, its amplitude is `−2g`, and

$$
\Gamma_{\rm dec}=\frac1{2M}\frac1{2!}(4g^2)
 \frac{\beta_{\rm dec}}{8\pi}
=\frac{g^2\beta_{\rm dec}}{8\pi M},\qquad
\beta_{\rm dec}=\sqrt{1-4m^2/M^2}
=\frac{u_*}{\sqrt{1+u_*^2}}.
$$

Here `M=2m sqrt(1+u*²)`; replacing `beta_dec` by `u*` is only the small-`u*` approximation.

## 3. Event moments and the restricted positive current

In a dilute factorized source gas with negligible occupied hard final states,

$$
R_{\rm ann}=n_{X+}n_{X-}\langle\sigma v_{\rm rel}\rangle,
\qquad \Gamma_{\rm ann,+}=n_{X-}\langle\sigma v_{\rm rel}\rangle.
$$

There is no `1/2` in this event rate because the two initial species are distinct. The event stoichiometry in order `(X+,X−,Phi+,Phi−)` is `(-1,-1,+1,+1)`. Consequently:

| Quantity | Change per event |
|---|---:|
| exact signed `U(1)` charge, weights `(2,−2,1,−1)` | 0 |
| all-mode weighted positive number, weights `(2,2,1,1)` | −2 |
| soft-only weighted number, hard daughters excluded | −4 |
| ordinary particle count with weight one per particle | 0 |

Thus “number loss” here means the emergent mass/charge-weighted positive NR number, not a violation of the exact signed charge or of an exact relativistic particle-number symmetry. Initial weighted number four becomes two if the hard daughters are counted. Restricting to the cold/soft sector makes it four to zero. In contrast, each isolated `X±→2Phi±` decay preserves the weighted positive number.

The exact initial energy `2M` equals the final energy `2sqrt(m²+k_f²)`. Rest energy changes from `2M` to `2m`, releasing `2(M−m)` as hard kinetic energy. For the nearly `M=2m` source, this is an order-one rest-energy redistribution. The original signed-charge lower bound `E≥m|Q|` has `Q=0` for this source pair and provides no nonzero neutral-stock protection. The positive-frequency NR approximation omits this hard reaction; its weighted positive current therefore cannot be promoted to an exact identity of the full relativistic theory.

Inverse annihilation and Bose factors would replace the forward dilute product by the vacuum collision kernel weighted with

`f_X+ f_X−(1+f_Phi+)(1+f_Phi−)−f_Phi+ f_Phi−(1+f_X+)(1+f_X−)`.

The occupation functions in that expression are evaluated on the hard on-shell momenta. Final stimulation, inverse hard populations and density-dependent dispersion corrections are not determined by the vacuum cross section. A coherent/dense source state needs its own calculation.

## 4. Benchmark rate hierarchy

The original declared benchmark is reconstructed from its parameter definitions, without importing/running the older thermal script:

$$
\lambda_{\rm rep}=\sqrt{8\pi m^3(\sigma_0/m)},\quad
g^2=\lambda_{\rm rep}(4m^2u_*^2)/r_\lambda.
$$

The code uses the existing unit conversion constants and obtains:

| Quantity | Value |
|---|---:|
| `M` | `2.000399960 MeV` |
| `lambda_rep` | `0.00587528017` |
| `g` | `2168.00003 eV` |
| `sigma v`, natural units | `4.75243095e−8 GeV⁻²` |
| `sigma v` | `5.54765517e−25 cm³/s` |
| `Gamma_dec` | `2.84013679e12 s⁻¹` |
| decay lifetime | `3.52095717e−13 s` |

The exact threshold comparison is

$$
\frac{\Gamma_{\rm ann,+}}{\Gamma_{\rm dec}}
=\frac{4n_{X-}g^2\beta_f}{M^5\beta_{\rm dec}}
=2.0349854198\times10^{-4}\frac{n_{X-}}{M^3}
=1.953305\times10^{-37}\frac{n_{X-}}{\mathrm{cm}^{-3}}.
$$

Equality with the decay rate would require

$$
n_{X-}^{\rm crit}=4914.0401M^3
=39335.9107m^3=5.1195265\times10^{36}\;\mathrm{cm}^{-3}.
$$

For an explicitly nondegenerate NR source gas, `n/M³≪1` is already a very generous density bound: at small velocities its phase-space occupancy condition is stronger. Under that stated condition the annihilation/decay ratio is well below `2.04e−4`. But a criterion such as a small gas parameter `n a³` alone does not imply `n/M³≪1`; an occupied or coherent state can have different density scales and must not inherit the gas conclusion. The equality density is a comparison of two vacuum rates, not a claim that the vacuum-rate approximation remains valid at that density.

## 5. Integrated defect in a specified decay-only stock

One can turn the rate comparison into a bounded emergent-current statement under additional explicit assumptions. Let a static homogeneous initial stock have equal per-sign source densities `n0`. Retain only independent decay and the channel above; ignore expansion, inverse reactions, occupied hard final modes, further collisions and changing mean fields. The equal per-sign density obeys

$$
\dot n=-\Gamma n-s_vn^2,\qquad
s_v=\sigma v,\qquad \alpha=s_vn_0/\Gamma,
\qquad
n(t)=\frac{n_0e^{-\Gamma t}}{1+\alpha(1-e^{-\Gamma t})}.
$$

The annihilation event count per initial volume is

$$
N_{\rm ann}=\int_0^\infty s_vn(t)^2dt.
$$

Integrating the density equation gives `n0=Gamma∫n dt+N_ann`. Changing integration variable from time to density yields

$$
\int_0^\infty n\,dt
=\int_0^{n_0}\frac{dn}{\Gamma+s_vn}
=\frac1{s_v}\log(1+\alpha),
$$

and hence

$$
\frac{N_{\rm ann}}{n_0}=1-\frac{\log(1+\alpha)}{\alpha}
=\frac\alpha2-\frac{\alpha^2}{3}+O(\alpha^3).
$$

The initial weighted positive stock is `4n0`. Each event removes four units from the soft current, or two if all hard daughters are included. The corresponding fractional defects are therefore

$$
\boxed{\epsilon_{\rm soft}=1-\frac{\log(1+\alpha)}{\alpha},\qquad
\epsilon_{\rm all}=\frac12\epsilon_{\rm soft}.}
$$

The strict analytic bound `0<epsilon_soft<alpha/2` for `alpha>0` follows from `alpha−ln(1+alpha)=∫[0,alpha]x/(1+x) dx`, whose integrand lies strictly between zero and `x`. The numerical table uses a non-strict rounded upper comparison at very small `alpha`; the strict inequality is an analytic statement, not a binary64 comparison.

For example, `n0/M³=10⁻6` gives `alpha=2.0349854e−10`, `epsilon_soft≈1.0174927e−10` and `epsilon_all≈5.0874635e−11` in this specified stock. This is an integrated small channel defect during rapid source decay. It is not a bound for a replenished source reservoir, long-lived hard bath, expanding universe, condensed state or complete interacting reaction network.

## 6. Scope, provenance and what remains open

`check_hard_number_loss.py`, `hard_number_loss_contract.json` and `hard_loss_run_002/` provide **34 exact/finite checks**: vertex and threshold algebra, flux and phase-space factors, finite-momentum angular identity, exact decay velocity and ratio, charge/weighted-number/energy moments, the integrated-defect identities, benchmark conversion and four independent direct angular integrals. The runner-v2 manifest records actual revisions and unchanged before/after input hashes, and validates with status `completed`. The earlier successful 32-check `hard_loss_run_001` is preserved; run 002 adds two exact integrated-inequality identities and permits equality from floating rounding in the numerical upper comparison. No prior response code or run manifest was changed.

All load-bearing channel formulas are derived above from the source action and elementary Lorentz phase space. No external literature or novelty claim is used. The declared benchmark/action inputs are pinned by the runner; this calculation does not authorize any portal or additional interaction merely because an input source discusses it.

This is the leading tree hard-loss process for a source/antisource pair through the original cubic vertices. It is not an exhaustive enumeration of weighted-number-changing channels: the existing pure-daughter `4→2` channels, other source-assisted reactions, dense Bose enhancements, inverse hard populations, medium masses, and their combined hierarchy remain unresolved here. Exact signed `U(1)` conservation survives throughout. The safe new conclusion is conditional: a prepared nondegenerate NR source stock with `alpha≪1`, negligible hard occupation, and no other competitive losses has a parametrically small defect from this particular channel while it decays. A physical emergent-positive-current or halo theorem still requires its full state-dependent reaction budget.
