# Clock fields, proper time, and the gravitational-wave–light delay

## Conclusion

Update before publication: Claude's subsequent commit `63c71679b` (L210)
acknowledges the independent sign and retained-counterterm corrections and
withdraws the affected L205/L207/L208/L209 and L206-pressure claims. The
historical audit below identifies exactly what was checked; it is not a claim
that those withdrawn conclusions remain the other agent's position. The exact
turning-point result in section 8 is an additional calculation.

The clock framework has a precise, testable meaning for a scalar clock's rate relative to metric proper time. It does not yet derive the origin of time, and GW170817's gamma-ray delay is not evidence that this clock exists. For the current action, the homogeneous tensor calculation instead gives a common gravitational-wave and photon propagation cone. This is a useful compatibility result, not a completed gravity theory.

There is also a concrete correction to the latest proposed time equation. Commit `0eee1a513` formalizes a pressure-to-clock-rate identity whose pressure premise omits a counterterm in the canonical action. Keeping that term and distinguishing clock-argument derivatives from proper-time derivatives cancels the claimed cubic correction on the tracked branch. The algebra in the Lean theorem is valid; its application to this action requires correction.

Carl Zimmerman's suggestion that the gravitational-wave–light ordering might probe the primordial clock motivated this investigation. That credit is for the research question, not for the previously published multimessenger timing equations. No coefficient has been refitted, no local/environment-dependent acceleration scale has been introduced, and no observation has been reclassified to obtain a desired result.

## 1. The observation and what it does not say

For GW170817/GRB170817A, the measured gamma-ray onset followed the inferred merger time by **1.74 ± 0.05 seconds**, corrected to a common geocentric reference. This is not the optical discovery delay, nor evidence that the signals were emitted together. The original collaboration's speed interval assumed emission from zero to ten seconds after the GW peak and used a conservative 26 Mpc distance. Those assumptions are explicitly model dependent.[^1]

The optical counterpart was discovered about 10.9 hours after the merger. Discovery time is not a measurement of how much more slowly optical photons traveled. Different radiation components are produced, escape, and become observable on different timescales.[^2]

A merger can precede jet formation, jet escape through surrounding ejecta, and gamma-ray production. These contributions and relativistic viewing geometry can produce seconds of observed delay without changing vacuum propagation speeds. Zhang analyzes this decomposition explicitly.[^3] Relativistic radiation/hydrodynamic calculations by Gottlieb and collaborators provide concrete examples, including a successful-jet/cocoon configuration with approximately 1.8 seconds of delay. Their agreement does not uniquely identify the source parameters.[^4]

Thus neither “gravity was faster” nor “the clock slowed light” follows from arrival ordering alone. The experiment detected strain in interferometers; “felt before light” is not a separate human-sensation measurement.

## 2. The timing equation, with its nuisance parameter retained

Define the observed lag as photon arrival minus GW arrival, and define

\[
\delta=(c_T-c_\gamma)/c_\gamma.
\]

For a constant-speed, common-distance, low-redshift model, independently constructing the two arrival times gives

\[
t_\gamma=t_{e,\gamma}+D/c_\gamma,
\qquad t_T=t_{e,T}+D/[c_\gamma(1+\delta)],
\]

\[
\boxed{\Delta t_{\rm obs}=\Delta t_e+
 \frac{D}{c_\gamma}\frac{\delta}{1+\delta}.}
\]

The exact inversion is

\[
r=\frac{c_\gamma(\Delta t_{\rm obs}-\Delta t_e)}{D},
\qquad \delta=\frac{r}{1-r}.
\]

Here the source lag is expressed in observer-equivalent seconds; cosmological redshifting is neglected in this low-redshift illustration. The result immediately allows three possibilities: later gamma emission with equal speeds, a smaller emission lag with faster GWs, or a larger emission lag with slower GWs. An unknown emission lag is an actual identifiability problem, not a numerical inconvenience.

Using published timing inputs and SI units, the new script finds:

| Calculation | Result | Interpretation |
|---|---:|---|
| Light travel time for the illustrative 40 Mpc distance | 130.46 million years | Low-redshift distance/c approximation |
| Fractional speed excess if all 1.74 seconds is propagation at 40 Mpc | 4.2263 × 10⁻¹⁶ | Conditional on simultaneous emission |
| Central interval at 26 Mpc with 0–10-second emission prior | [−3.0866 × 10⁻¹⁵, +6.5020 × 10⁻¹⁶] | Reproduction of the conventional rounded range |
| Include the ±0.05-second timing endpoints | [−3.1053 × 10⁻¹⁵, +6.6888 × 10⁻¹⁶] | Endpoint propagation, not a new posterior |

Numerical precision was increased from 50 to 90 decimal digits; these quantities agree to relative 10⁻³⁵. These extra digits verify arithmetic, not astronomical distance accuracy. The calculations use the published measurement, not a fresh analysis of detector streams.

For a homogeneous expanding background with present scale factor one, small speed excess and a common reference path, the first-order generalization is

\[
\boxed{\Delta t_{\rm obs}=(1+z_s)\Delta t_{e,\rm source}
 +\int_0^{z_s}\frac{\delta(z)}{H(z)}\,dz
 +\Delta t_{\rm path}+\Delta t_{\rm other}.}
\]

The integral follows by comparing comoving distances \(\int v\,dt/a\) and using \(dt/a=-dz/H\). It is not the lookback integral \(\int dz/[(1+z)H]\). Path effects here mean departures from the common homogeneous reference propagation; they must not be counted twice inside the speed term. Source position offsets, finite-wavelength effects, and dispersive/instrumental corrections require their own treatment.

A 2025 forecast by Colangeli, Leyde and Baker derives the same timing structure for a specified tensor-speed history. It also explicitly warns that an artificially narrow near-zero emission-lag prior biases inference. The paper concerns simulated future observations, not a measured speed anomaly.[^5]

The script computes a three-event Jacobian with an independently free emission lag per event: its rank is three for four unknowns. The general obstruction is exact in the linearized timing model: changing a common propagation parameter can be offset by changing each unrestricted emission lag. A population can constrain propagation only with additional information or justified population assumptions; adding events alone does not remove unrestricted nuisance parameters.

## 3. What the framework means by a clock

Use signature \((-+++)\), \(c=1\), a Lorentzian physical metric, and a scalar \(\tau\) with timelike gradient. Define

\[
s=\sqrt{-g^{\mu\nu}\partial_\mu\tau\partial_\nu\tau}>0,
\qquad n_\mu=-\partial_\mu\tau/s.
\]

These definitions give

\[
\boxed{n_\mu n^\mu=-1,\qquad n^\mu\partial_\mu\tau=s.}
\]

Along the unit-normal congruence, parametrized by metric proper time \(t_p\),

\[
\boxed{\frac{d\tau}{dt_p}=s.}
\]

This is a meaningful rate comparison. It does not identify the scalar's numerical value with an atomic clock reading. Ordinary matter is coupled to the metric; a direct nonmetric atomic-clock response would require a new coupling and corresponding tests.

The new Lean file `ClockGeometry.lean` proves the local Lorentz-frame normalization, directional rate, positivity, and invariance of the normal under positive rescaling of both the clock gradient and its norm. A rescaling of the scalar need not be a symmetry of the complete action: explicit coefficient functions and their normalization matter. These are conditional geometric proofs, not a proof that the assumed clock field occurs in nature.

A separate Christoffel-symbol calculation with

\[
ds^2=-N(t,x)^2dt^2+a(t)^2d\mathbf x^2,\qquad \tau=t
\]

gives the clock-normal acceleration and expansion separately:

\[
a_\mu=n^\nu\nabla_\nu n_\mu=(0,\partial_x\ln N,0,0),
\qquad \theta=\nabla_\mu n^\mu=\frac{3\dot a}{aN}.
\]

Therefore homogeneous FLRW can have **zero normal acceleration and nonzero expansion**. One cannot put \(cH\) into an acceleration-based MOND kernel merely by calling both quantities “cosmological acceleration.” Whether a particular action uses acceleration, expansion, a scalar gradient, or another invariant must be derived. This geometric distinction does not by itself decide the actual candidate's nonlinear cosmological force law.

Neither normalization nor these equations derives an initial time, a thermodynamic arrow, or a quantum theory of clocks. Those questions need extra physical content and boundary conditions.

## 4. Vary the same action before interpreting the clock's rate

The action currently tested in the canonical closure implementation is

\[
S=\int\!d^4x\sqrt{-g}\left[
\frac{M^2}{2}(R-2\Lambda)+P(X,\tau)-V(\tau)
+sW(Y,\tau)+\gamma X\Box\chi\right]+S_m[g,\psi],
\]

\[
X=-\nabla_\mu\chi\nabla^\mu\chi,
\quad Y=(g^{\mu\nu}+n^\mu n^\nu)\partial_\mu\chi\partial_\nu\chi.
\]

Here \(M^2>0\) and \(\gamma\) are constant. The two scalar fields have different roles; the tensor result below does not count away their scalar dynamics or constraints.

For flat homogeneous FLRW with arbitrary lapse, let

\[
Q=\dot\chi/N,\quad s=\dot\tau/N>0,\quad H=\dot a/(aN),\quad W_0(\tau)=W(0,\tau).
\]

After integration by parts, the sector's homogeneous Lagrangian per coordinate spatial volume is

\[
L_{\rm hom}=Na^3[P(Q^2,\tau)-V(\tau)]
+a^3\dot\tau W_0(\tau)-2\gamma a^2\dot a Q^3.
\]

The lapse, scale-factor, scalar-velocity, and clock variations give, independently,

\[
\rho=2Q^2P_X-P+V-6\gamma HQ^3,
\qquad p=P-V+sW_0+2\gamma Q^2\frac{dQ}{dt_p},
\]

\[
j=2QP_X-6\gamma HQ^2,\qquad
\frac{d(a^3j)}{dt_p}=0,
\]

\[
\boxed{P_\tau-V_\tau-3HW_0=0.}
\]

The last equation is a genuine homogeneous clock Euler–Lagrange equation; the equation-of-state identity \(p=w\rho\) is not a replacement for it. The variation remains a homogeneous reduction, not the full four-dimensional Dirac analysis. Derivative notation matters: \(P_\tau\) holds \(X\) fixed.

### The correction to Claude's latest commit

The canonical coefficient function in `nonlinear_evolution_2026/constitutive.py` contains

\[
W_0=U-2\gamma\bar q^2\bar q',\qquad
\bar q'=d\bar q/d\tau.
\]

On the tracked branch \(Q=\bar q(\tau)\), the chain rule is

\[
\frac{dQ}{dt_p}=s\bar q'.
\]

Since \(P=0\) and \(V=U\) on that branch, keeping both cubic contributions gives

\[
\boxed{p=-U+s(U-2\gamma\bar q^2\bar q')
+2\gamma\bar q^2s\bar q'=U(s-1).}
\]

The extra cubic term proposed by L206 and used as a premise in the new Lean theorem is absent on this branch. Dropping the counterterm changes the action; forgetting the factor \(s\) changes the derivative convention. Neither is a derivation of a new time law.

Additionally, the advertised density formula requires actual expansion to match the reference function used inside \(P\). More generally, on the tracked scalar branch,

\[
\rho=\frac{U}{m_{\rm rel}}+6\gamma\bar q^3(\bar H-H),
\qquad m_{\rm rel}=1-\frac{2d\bar q^2}{U}.
\]

Only when \(H=\bar H\), with nonzero \(U,m_{\rm rel}\), does \(p=w\rho\) yield

\[
\boxed{s-1=w/m_{\rm rel}.}
\]

That remains a conditional relation, not a determination of \(w\) or an existence theorem for all its values. Clock and scalar conservation equations must hold simultaneously with the Einstein equations. The detailed pressure audit records the further conditional restrictions from the frozen reference-flow identities. No coefficient functions were reconstructed to force a different background.

The theorem named `clock_rate_from_conservation` in commit `0eee1a513` has an algebraic equation-of-state premise, not a differential conservation hypothesis. Its proof is not fraudulent: it proves the written implication. The missing link is the physical premise and its interpretation. The new `PressureIdentity.lean` certifies the retained-counterterm cancellation and corrected equation-of-state implication.

## 5. The tensor and photon clocks agree on the tested background

For aligned homogeneous scalars use the tensor perturbation

\[
g_{ij}=a^2(e^h)_{ij},\quad h_i{}^i=0,\quad \partial_i h_{ij}=0.
\]

The spatial determinant is \(a^6\), independent of \(h\). The scalar invariants on this tensor-only branch are \(Y=0\), \(X=Q^2\), and \(s=\dot\tau\) in proper-time gauge. Thus \(P,V,sW\) add no tensor principal derivative terms. The homogeneous cubic term is proportional to \(Q^3K\), and \(K=3H\) is independent of the traceless tensor perturbation.

The direct curvature/ADM calculation gives

\[
\boxed{S_T^{(2)}=\frac{M^2}{8}\int dt_p\,d^3x\,a^3
\left[\dot h_{ij}\dot h_{ij}-a^{-2}(\partial_kh_{ij})^2\right].}
\]

The code also constructs \(F_{\mu\nu}\), raises its indices, and expands the minimally coupled Maxwell action for a transverse photon polarization. For tensor and photon variables separately it differentiates the resulting Lagrangians, computes kinetic and spatial-gradient coefficients, and takes their ratio. It obtains

\[
\boxed{c_T^2=c_\gamma^2=1,\qquad M^2>0.}
\]

The speeds in the current output are computed, not assigned. The general single-scalar Horndeski tensor formulas provide a cross-check for the Einstein-plus-cubic sub-sector: constant \(G_4=M^2/2\) and vanishing \(G_5\) give equal positive tensor coefficients. The extra clock operator was examined explicitly here rather than assumed to be covered by that single-scalar result.[^6]

This establishes the homogeneous principal tensor cone. It does not establish healthy scalar propagation, a complete degree-of-freedom count, or global inhomogeneous signal transport. In particular, a scalar sound speed is not the tensor speed. Peak arrival shifts from source dynamics, scattering, wave effects, or mode conversion are distinct calculations.

A universal metric lapse alters the coordinate speeds of both signals together. For \(ds^2=-N^2dt^2+A^2dx^2\), either null ray has coordinate speed \(N/A\) and local proper speed one. Changing the time label cannot produce a relative arrival delay. A genuine disformal difference between photon and tensor metrics can: the separate control \(\widetilde g=Cg+Bnn\) gives \(c_\gamma^2/c_T^2=1-B/C\), on its Lorentzian domain. That is a diagnostic alternative, not a modification adopted for this candidate.

## 6. A timing test that removes the emission lag

For two resolved images A and B of one strongly lensed multimessenger transient, define

\[
\boxed{\mathcal D=(t_{\gamma,B}-t_{T,B})
 -(t_{\gamma,A}-t_{T,A}).}
\]

Writing each arrival as a redshifted emission time plus a path travel time gives

\[
\mathcal D=(T_{\gamma,B}-T_{\gamma,A})-(T_{T,B}-T_{T,A}).
\]

The unknown common emission lag cancels exactly; this algebra is certified in Lean. Equal corresponding propagation delays imply zero. Spatially separated emission regions, microlensing, finite-wavelength propagation, lens evolution and image-identification errors must be controlled before interpreting a nonzero measurement.

This is the already published Collett–Bacon strategy, not a new prediction invented here. It trades sensitivity to the full source distance for a cleaner differential lens baseline: a propagation contribution common to both images cancels too. Their illustrative speed sensitivity is about 10⁻⁷, much weaker numerically than the conditional GW170817 range, but independent of an intrinsic emission-lag assumption.[^7]

One should also avoid unqualified absolute cosmological Shapiro-delay estimates as a theory-independent discriminator. Minazzoli, Johnson-McDaniel and Sakellariadou identify gauge/reference and cosmological boundary issues; the mapping to a specific alternative theory must be supplied. This does not erase GW170817 or ordinary measured Solar-System Shapiro delay.[^8]

## 7. What would constitute real progress from here

The global input \(a_0=\tfrac12c\sqrt{G\rho_\Lambda}\) and the exact exponential MOND kernel do not, on their own, determine an emission lag, a photon coupling, or a tensor characteristic. With the input \(a_0=9.36\times10^{-11}\,\mathrm{m\,s^{-2}}\), the dimensional time \(c/a_0\) is about \(1.015\times10^{11}\) years. Obtaining seconds requires additional dynamics and scales, not a dimensional claim that the observed delay was predicted. The fitted one-half remains fitted.

The narrow calculation worth doing next is **propagation on an on-shell inhomogeneous clock/galaxy background**, retaining the complete coupled principal matrix and physical matter metric. It must determine whether the homogeneous shared tensor cone survives relevant gradients, whether mode conversion affects the waveform, and whether the scalar branch is stable. It must not invent an extra photon delay or reconstruct coefficient functions to match 1.74 seconds.

If that check remains luminal, the productive clock tests are its independently predicted metric potentials, scalar response, structure evolution, and source/waveform effects—not an assumed speed split. Explaining galactic MOND, clusters and cosmology from the same action remains open. No Lean certificate here changes that status.

## 8. Later commits and evidence boundaries

While this investigation was running, commits `483311234` (L207) and `587101084` (L208) added a positive \(\beta Y^{3/2}\) operator and an assumed matter response \(\Phi=\Phi_N+c_\chi\chi\). These are proposals beyond the frozen action checked above. Their source was inspected, but their emitted PASS counts are not used here as evidence for a completed theory.

The claimed window \(1<4d\ell/U<8\) cannot currently be adopted by the research scout. Its lower endpoint uses L205's reversed gradient-energy sign: on its stated \(Q=0,\gamma=0\) branch the actual scalar gradient-energy coefficient is \(-2F_Y\), not \(+2F_Y\). The new independent `health/REPORT.md` gives exact rational counterexamples and the correct generic small-gradient condition \(U>4d\ell\) for the original operator. Adding a positive \(\beta Y^{3/2}\) further changes that energy test; the old inequality cannot simply be transplanted.

The upper endpoint in L207 is assigned through `hmax = CH0_OVER_A0`, after setting `CH0_OVER_A0 = 7.0`. Its test checks that assignment, not an action-derived identification of the homogeneous kernel argument with \(cH\). Section 3 demonstrates why expansion and clock-normal acceleration must be distinguished. Finally, L208 explicitly assumes the physical potential rather than deriving the metric/matter coupling. Its conditional numerical history test does not repair either missing implication. These findings specify what must be corrected before launching parameter searches; they do not prove that every modified action fails.

### A sharp replacement for the turning-point claim

The follow-up calculation differentiates L207's proposed \(W\) exactly. For \(d,\ell,\beta>0\), its stationary points of \(W_Y\) obey

\[
W_{YY}=-\frac{d}{2\ell}(1+Y/\ell)^{-3/2}
+\frac{3\beta}{4\sqrt Y}=0,
\qquad
\beta^2=\frac{4d^2}{9\ell}\frac{z}{(1+z)^3},\quad z=Y/\ell>0.
\]

The factorization

\[
4(1+z)^3-27z=(2z-1)^2(z+4)\ge0
\]

gives the exact necessary bound, attained at \(z=1/2\),

\[
\boxed{\beta^2\le\frac{16d^2}{243\ell}.}
\]

For strict inequality there are two positive turning points: the lower is a **maximum** of \(W_Y\), and the upper is a minimum. At equality there is a double zero with no sign change; above the bound there are no turning points. L207's assigned `Y_min` approximates the lower root and therefore misidentifies its type. The exact condition for a falling \(W_Y\) at a specified \(Y_*\) is

\[
\boxed{\beta^2<\frac{4d^2}{9\ell}
 \frac{Y_*/\ell}{(1+Y_*/\ell)^3}.}
\]

This condition does not insert \(cH/a_0\) or assume that \(\beta\) cancels. Three additional Lean theorems certify the factorization, profile bound, and necessary polynomial coefficient inequality. The derivative, sign analysis and numerical root controls are in `health/turning/`. On the restricted \(Q=0\) scalar branch, the added positive operator gives leading physical stiffness \(-3\beta\sqrt Y\), so finding turning points still does not establish health. This is a sharp constitutive gate for the proposed operator, not a completed theory or a globally novel mathematical theorem.

## 9. Source record

Code and exact execution records are described in `VERIFICATION.md`. The separate `closure_front_2026/health/pressure/REPORT.md` contains the current-action pressure audit; `closure_front_2026/boosted/REPORT.md` contains tensor, clock-geometry and moving-source results. Earlier tensor output is superseded by `tensor_result_v2.json`, whose speeds are derived from action coefficients.

Primary-source search covered the original collaboration publications, source-emission calculations, tensor-action formulas, lensed timing tests, and targeted 2025–2026 updates through 2026-09-12. The directly verified recent addition is the 2025 forecast, not a newly established anomaly. No global novelty claim is made. Research and computation auditing kept the measured facts, assumptions, symbolic results, finite numerical checks and formal algebra separate.

### Sources

[^1]: LIGO Scientific Collaboration, Virgo Collaboration, Fermi GBM and INTEGRAL. “Gravitational Waves and Gamma-Rays from a Binary Neutron Star Merger: GW170817 and GRB 170817A.” *ApJL* 848 L13 (2017), §§2.2, 4.1. [Published paper](https://ntrs.nasa.gov/api/citations/20170011356/downloads/20170011356.pdf). DOI 10.3847/2041-8213/aa920c.
[^2]: LIGO Scientific Collaboration. “The dawn of multi-messenger astrophysics: Observations of a binary neutron star merger.” [Official observational summary](https://ligo.org/science-summaries/GW170817MMA/), image/discovery chronology. Checked 2026-09-12.
[^3]: Bing Zhang. “The Delay Time of Gravitational Wave–Gamma-Ray Burst Associations.” *Frontiers of Physics* 14(6), 64402 (2019); arXiv:1905.00781v2, §§2,4–5. [Author paper](https://arxiv.org/pdf/1905.00781). DOI 10.1007/s11467-019-0913-4.
[^4]: Ore Gottlieb, Ehud Nakar, Tsvi Piran and Kenta Hotokezaka. “A cocoon shock breakout as the origin of the γ-ray emission in GW170817.” *MNRAS* 479, 588–600 (2018), §§3–6. [Published article](https://academic.oup.com/mnras/article/479/1/588/5033690). DOI 10.1093/mnras/sty1462.
[^5]: Elena Colangeli, Konstantin Leyde and Tessa Baker. “A Bright Future? Prospects for Cosmological Tests of GR with Multimessenger Gravitational Wave Events.” *JCAP* 05 (2025) 078; arXiv:2501.05560v2, 28 May 2025, Eq.2.10 and §§3.1,5. [Versioned full text](https://arxiv.org/html/2501.05560v2).
[^6]: Tsutomu Kobayashi, Masahide Yamaguchi and Jun'ichi Yokoyama. “Generalized G-inflation: Inflation with the most general second-order field equations.” *Prog. Theor. Phys.* 126, 511–529 (2011); arXiv:1105.5723, §4.1, Eqs.4.3–4.8. [Author paper](https://arxiv.org/pdf/1105.5723). Their kinetic variable is half the normalization used in this report; constant G4 and zero G5 make that distinction immaterial for this tensor comparison.
[^7]: Thomas E. Collett and David Bacon. “Testing the Speed of Gravitational Waves over Cosmological Distances with Strong Gravitational Lensing.” *PRL* 118, 091101 (2017); arXiv:1602.05882v2, §II. [Published paper](https://pure.port.ac.uk/ws/portalfiles/portal/6842399/PhysRevLett.118.091101.pdf). DOI 10.1103/PhysRevLett.118.091101.
[^8]: Olivier Minazzoli, Nathan K. Johnson-McDaniel and Mairi Sakellariadou. “Shortcomings of Shapiro delay-based tests of the equivalence principle on cosmological scales.” *PRD* 100, 104047 (2019); arXiv:1907.12453v2. [Author paper](https://arxiv.org/pdf/1907.12453). DOI 10.1103/PhysRevD.100.104047.
