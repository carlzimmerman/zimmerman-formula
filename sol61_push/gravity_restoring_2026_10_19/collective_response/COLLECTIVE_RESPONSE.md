# Neutral atom–molecule collective response and the missing static restoring interaction

19 October 2026. Owner: `/root/collective_restoring`. Base contract: `CE-PARTICLE-2026-10-18 / CE-FM-085`, requested Git base `9516ee01c79f35c04b7556050669ba77b0c98b99`. The working repository changed concurrently to `5c3444b8f60820a4ea78ea1e798ce8429cf2622a` before the new finite run. `source_pins.json` and the manifest pin the actual source bytes. No shared current, ledger, manuscript, queue, publication or Git state was changed by this lane.

**Result.** Retaining both atom–molecule conversion phases and both neutral-bath number phases gives two explicit density/phase blocks. The conserved charge-even density has a gapless sound pole and a gapped conversion pole; the latter's density oscillator strength vanishes as `k^4` near zero momentum. The apparent inverse-density `1/k^2` term from the common phase is proportional to frequency squared and is inertia. It disappears in the static limit. Ordinary gravitational resummation subtracts `4 pi G/k^2` from the inverse density kernel and gives Jeans attraction. It supplies no positive static tether.

There is a further state restriction: the equal-density coherent neutral mixture is unstable to a charge-odd density mode on the original dilute branch. This holds also using the fully threshold-matched elastic coefficients, rather than only the bare rotating-wave contact. A neutral kinetic bath or separated condensates require different state calculations; the instability does not exclude such states.

The physical longitudinal displacement has a momentum-integrated phonon spectral weight linear in gap at low gap. Thus a bare phonon density-of-states argument does **not** rule out the infrared power required by the separate two-level dipole construction. However, the displacement is an inverse spatial derivative of conserved density, its modes carry momentum, and its oscillators are harmonic. No source-local saturating two-level ensemble or rational nonlinear law is thereby derived. The full Bogoliubov spectral measure also has a different particle-regime tail.

## 1. Contract, original parameters and state

Natural units are used; `z=k^2>0`, `grad -> i k`, and `delta rho=-chi_rho Phi_N`. Newton gravity is attractive with `K_G=4 pi G>0`. The desired positive restoring density kernel is `+K_G/z`, equivalent to `+(K_G/2)|P_L|^2` for `P_L=-i k delta rho/z`. The further target is the rational restoring remainder `R(u)=u^2/(a0-u)` with `u=K_G|P|<a0`. Neither coefficient matching nor a complete nonlinear law follows merely from identifying a gapless mode.

The original relativistic polynomial action has complex daughter `Phi` of charge one, complex source `X` of charge two, canonical kinetic terms and

\[
V=m^2|\Phi|^2+M^2|X|^2+g(X^*\Phi^2+\mathrm{c.c.})
  +\lambda_{\rm tot}|\Phi|^4,\quad
\lambda_{\rm tot}=\lambda_{\rm rep}+\frac{g^2}{M^2-4m^2},
\quad M>2m,\quad\lambda_{\rm rep}>0.
\]

The canonically rephased conservative NR envelope theory in the pinned positive-current note has atom fields `psi_sigma` and source fields `b_sigma`, `sigma=+,-`, with

\[
c=\frac{g}{2m\sqrt{2M}},\quad k_c=\frac{\lambda_{\rm tot}}{4m^2},
\quad\delta=M-2m,
\]
\[
H_{\rm NR}=\sum_\sigma\left[\frac{|\nabla\psi_\sigma|^2}{2m}
+\frac{|\nabla b_\sigma|^2}{2M}+\delta|b_\sigma|^2
+c(b_\sigma^*\psi_\sigma^2+\mathrm{c.c.})\right]
+k_c(n_+^2+n_-^2+4n_+n_-).
\]

Here `n_sigma=|psi_sigma|^2`, `s_sigma=|b_sigma|^2`, and each conserved envelope number is `q_sigma=n_sigma+2s_sigma`. The positive reference mass density is `rho_0=m(q_++q_-)`. These two number symmetries belong to the retained conservative soft theory. Only their signed difference is an exact microscopic charge; number-changing/hard-mode leakage remains an independent approximation obligation. Condensation is a separate state hypothesis and has not been established by particle production.

Choose a homogeneous equal-density coherent stationary branch,

\[
\psi_\sigma=\sqrt n\,e^{-i\mu t},\qquad
b_\sigma=-\beta e^{-2i\mu t},\qquad
\beta=\frac{cn}{\Delta}>0,\qquad \Delta=\delta-2\mu>0,
\]
\[
\mu=6k_cn-2c\beta=2n(3k_c-c^2/\Delta).
\]

The minus sign minimizes the conversion energy. This is a stationary saddle, and its full stability is checked below. The actual source kinetic mass `M` is retained. The difference between the leading conserved reference mass and rest mass is `delta(s_++s_-)`; its use as a gravitational approximation requires the cold-error bounds of the pinned note.

## 2. Complete quadratic density and phase blocks

Let `theta_a,sigma` and `theta_b,sigma` be the deviations of the atomic and source phases from this branch. In each sign sector the canonical phase term is

\[
\mathcal L_{\rm Berry}=-\delta n_\sigma\dot\theta_{a,\sigma}
                         -\delta s_\sigma\dot\theta_{b,\sigma}.
\]

Use the orthonormal even/odd combinations `x_e,o=(x_+ +- x_-)/sqrt(2)` for the density vector `x_sigma=(delta n_sigma,delta s_sigma)^T`, and the same combinations for `theta`. Then

\[
\mathcal L_2=\sum_{p=e,o}\left[-x_p^T\dot\theta_p
-\frac12x_p^TA_p(z)x_p-\frac12\theta_p^TB(z)\theta_p\right]
-\sqrt2m\Phi_N r^Tx_e,\qquad r=\binom12,
\]
\[
\boxed{\quad
A_e(z)=\begin{pmatrix}
6k_c+z/(4mn)&-c/\beta\\
-c/\beta&cn/(2\beta^3)+z/(4M\beta^2)
\end{pmatrix},\qquad
A_o(z)=A_e(z)-\begin{pmatrix}8k_c&0\\0&0\end{pmatrix}.\quad}
\]
\[
\boxed{\quad B(z)=z\begin{pmatrix}d_a&0\\0&d_b\end{pmatrix}
+Jvv^T,\quad d_a=n/m,\quad d_b=\beta^2/M,
\quad J=2cn\beta,\quad v=\binom2{-1}.\quad}
\]

The density-gradient terms are the full quadratic quantum pressures. The conversion energy is `c n beta (2 theta_a-theta_b)^2`, giving `J vv^T`. The vector `r` is its null direction, and `r^T v=0`: conversion locks the relative phase without gapping the weighted total number phase. There are two such common phases in the conservative neutral RWA theory, one even and one odd. Gravity sources only the even block at the displayed mass order. A number-leaking microscopic correction need not preserve both.

The script independently differentiates the original polynomial energy in Cartesian real and imaginary field perturbations, rotates its Hessians into charge parity, and transforms them to the density/phase basis. This checks the factors of two and the cross-contact factor four without assuming the final response matrices.

For `A=[[a,b],[b,D]]`, abbreviate

\[
d=d_a+4d_b,\quad L=D+4a-4b=v^TAv,
\quad t=a d_a+Dd_b.
\]

At `z>0`, `B` is positive and invertible, with the exact expression

\[
\boxed{\quad
B^{-1}=\frac{Jrr^T+z\operatorname{diag}(d_b,d_a)}
 {z[Jd+z d_ad_b]}.
\quad}
\]

The real-frequency density inverse is `A-(omega+i0)^2 B^{-1}`. The complete conserved even mass-density susceptibility is consequently

\[
\boxed{\quad
\chi_\rho(\omega,k)=
\frac{2m^2z\{d[JL-s]+z d_ad_bL\}}
 {s^2-s[JL+zt]+\det(A)z[Jd+z d_ad_b]},
\qquad s=(\omega+i0)^2,\quad A=A_e(z).
\quad}
\]

Equivalently it is `2m^2 r^T[A-s B^{-1}]^{-1}r`. The mode frequencies satisfy

\[
\Omega_\pm^2=\frac12\left[T\pm\sqrt{T^2-4\det(A)\det(B)}\right],
\quad T=JL+zt,\quad \det B=z[Jd+zd_ad_b].
\]

At zero momentum the roots are `0` and `Omega_g^2=J L(0)`. If `A(0)>0`, the sound coefficient is

\[
c_s^2=\frac{d\det A(0)}{L(0)}
=\frac{d}{r^TA(0)^{-1}r}.
\]

The uniform source overlap with the conversion mode is zero because total weighted number is conserved. More strongly, at the gapped pole its conserved-density numerator is `O(z^2)`, hence its pole residue is `O(k^4)` when the gap stays nonzero and distinct. This follows directly by writing `A(z)=A(0)+z Q` and `Omega_g^2(z)=J L(0)+O(z)` in the boxed numerator: its apparent `O(z)` term cancels. A source resonance can enhance finite-momentum dynamic response; it does not furnish a uniform static internal dipole.

## 3. Static limit, inertia and gravity

Putting `omega=0` before taking `k` small gives

\[
\chi_\rho(0,k)=2m^2r^TA_e(z)^{-1}r
              =\frac{2m^2L(z)}{\det A_e(z)}.
\]

All phase denominators cancel in this static limit. In the hydrodynamic regime the common phase gives

\[
\chi_\rho(\omega,k)=\frac{\rho_I k^2}{c_s^2k^2-(\omega+i0)^2}
+\hbox{higher-derivative/gapped contributions},\qquad
\rho_I=2m^2d.
\]
\[
\boxed{\quad \chi_\rho^{-1}=\frac{c_s^2}{\rho_I}
-\frac{(\omega+i0)^2}{\rho_I k^2}+\cdots.\quad}
\]

The `1/k^2` term is frequency dependent and has the inertial sign in real time. On the imaginary-frequency axis it is `+omega_E^2/(rho_I k^2)`. Choosing `omega_E^2=rho_I K_G` would imitate the desired coefficient at one imposed imaginary frequency. It is not a static interaction, depends on the state, and vanishes for `omega_E=0`. In terms of `P_L`, this piece is an ordinary local time kinetic term `|dot P_L|^2/(2rho_I)`. The material static energy remains proportional to `k^2|P_L|^2` at finite compressibility.

For fixed nonzero frequency away from a pole,

\[
\chi_\rho(\omega,k)=-\frac{\rho_I k^2}{(\omega+i0)^2}+O(k^4).
\]

For `omega=v k`, the static-type inverse approaches the finite constant `(c_s^2-v^2)/rho_I`. These noncommuting limits account for the common phase singularity without creating a positive static density pole.

Now impose Poisson self-consistency `-k^2 Phi_N=K_G(rho_b+delta rho)`. The matter inverse changes to

\[
\boxed{\quad \chi_{\rm grav}^{-1}(\omega,k)
=\chi_{\rm matter}^{-1}(\omega,k)-\frac{K_G}{k^2}.\quad}
\]

The minus sign follows from attractive Newton gravity, independently of how the material susceptibility was computed. The low-energy mode becomes `Omega^2=c_s^2 k^2-K_G rho_I+...`, with quantum pressure supplying its `k^4` correction. A finite-box restriction above the Jeans threshold can stabilize a band of modes; it does not reverse the interaction sign or normalize a positive material tether.

The difference `rho_I != rho_ref` is an explicit `delta/M` effect when the source kinetic mass is kept as `M`: at `M=2m`, `rho_I=2m(n+2 beta^2)=rho_ref`. At the example below it is a relative `6.46e-5` difference. It must not be used as an exact equivalence-principle statement beyond the controlled NR order.

There is a related source pitfall. If one couples only the separate rest-energy inventory `h=(m,M)` to a probe, then `h^T v=2m-M=-delta`, and at `k=0` its internal conversion susceptibility is `2J delta^2/(Omega_g^2-s)`. This is the nonconservation of rest inventory during conversion, not a new force. A claim at that correction order must include detuning, interactions and the complete stress-energy vertex. On the homogeneous stationary branch the derivative of the *full* conserved Hamiltonian is `(m+mu)r`, rather than `(m,M)`, so the conversion overlap cancels at zero momentum. The leading gravitational calculation consistently uses `m r` and records its cold approximation.

## 4. An exact parameter example and neutral stability

An original-action point with no introduced mediator or contact is

\[
m=1,\quad M=201/100,\quad c=1/100,\quad\lambda_{\rm rep}=1,
\quad g^2=201/125000,\quad\lambda_{\rm tot}=10427/10025,
\]
\[
\Delta=1/200,\quad\mu=1/400,\quad
n=401/243832\simeq0.001644575,\quad
\beta=401/121916\simeq0.003289150.
\]

Thus `delta/m=0.01`, `mu/m=0.0025`, and `beta^2/n=0.0065783`. The source has been retained, so `mu/Delta=0.5` does not invalidate a source elimination that was never made. This is a small-energy coherent saddle of the conservative NR model. It is not evidence that the original production mechanism prepares it.

| Block | Conversion gap | Sound coefficient squared | Static reference-density susceptibility |
|---|---:|---:|---:|
| Even | 0.0051952670 | 0.0023459178 | 1.4204285733 |
| Odd | 0.0051078972 | -0.0008940970 | -3.7268985613 |

The odd negative susceptibility is a saddle diagnostic, not an equilibrium physical compressibility. At `k=10^-3`, its small root is `Omega_-^2=-8.9385065e-10`; the even root is `+2.3461463e-9`. Four fixed momenta per block are recorded in the finite evidence. They confirm the stated saddle and the even-block dynamic formula; no parameter survey is claimed.

Indeed, the original bare-RWA odd Hessian obeys the exact identity

\[
\det A_o(0)=-\frac{k_c cn}{\beta^3}-\frac{c^2}{\beta^2}<0.
\]

For sufficiently small nonzero momentum, `B>0` and `A_o` has a negative eigenvalue, so one dynamical squared frequency is negative. On the dilute branch where `J L_o(0)>0`, it is the sound mode. At other densities the conversion gap itself can be unstable; the determinant result alone should not be called a universal sound-branch instability.

The instability is not removed by silently using the fully matched same-charge contact in every channel. The original tree amplitudes give

\[
g_{\rm same}=\frac{\lambda_{\rm rep}}{2m^2},\qquad
g_{\rm cross}=\frac{\lambda_{\rm tot}-g^2/M^2}{m^2}.
\]

The different identical/distinguishable NR vertex factors are essential. For same charge the relativistic threshold amplitude is `-4 lambda_rep=-8m^2 g_same`; after crossing the source exchange has zero threshold invariant and amplitude `-4(lambda_tot-g^2/M^2)=-4m^2 g_cross`. Consequently

\[
\boxed{\quad g_{\rm cross}-g_{\rm same}
=\frac{\lambda_{\rm rep}}{2m^2}
+\frac{4g^2}{M^2(M^2-4m^2)}>0.\quad}
\]

For the dilute matched two-atom condensate, the even and odd sound coefficients are `n(g_same+g_cross)/m` and `n(g_same-g_cross)/m`. The odd one is negative. Neither global neutrality nor finite total charge prevents a nonzero-momentum charge-segregation perturbation of zero integrated charge. A finite box can omit sufficiently long modes; a mixed normal gas can also obtain positive odd free-energy curvature from entropy. For example the dilute classical equal-density mixture adds `T/n` to each diagonal curvature and is stable in that channel when `T/n>g_cross-g_same`. Its temperature and kinetic distribution still need to be established from the original dynamics.

## 5. Actual spectral weights and the rational-ensemble comparison

Use the convention `chi_O(omega,k)=sum_j F_j(k)/[Omega_j(k)^2-(omega+i0)^2]`. At zero temperature a one-quantum matrix element per volume has squared weight `F_j/(2Omega_j)`. The following oscillator formulas apply to the stable even quadratic block if odd perturbations are constrained, or to the stable single-component comparator below. They are not an equilibrium spectral theorem for the full unstable neutral saddle. For the even sound branch,

\[
F_\rho(k)=\rho_I k^2+O(k^4),\quad\Omega=c_s k+O(k^3),
\quad |\langle1_k|\rho_k|0\rangle|^2/V
=\frac{\rho_I k}{2c_s}+O(k^3).
\]

The momentum-integrated *squared-matrix-element* measures in three dimensions are

\[
\mathcal J_\rho(\Delta)=\int\frac{d^3k}{(2\pi)^3}
 \frac{F_\rho(k)}{2\Omega(k)}\delta(\Delta-\Omega(k))
=\frac{\rho_I\Delta^3}{4\pi^2c_s^5}+\cdots,
\]
\[
\boxed{\quad \mathcal J_{P_L}(\Delta)
=\frac{\rho_I\Delta}{4\pi^2c_s^3}+\cdots.\quad}
\]

The second formula divides the density matrix element by `k^2`, because `P_L=-i k rho/k^2`. Counting only phonon modes gives a `Delta^2` density of states, but it omits the operator matrix element. Counting density weights gives `Delta^3`, but it omits the inverse derivative defining longitudinal displacement. Either shortcut would misidentify the infrared power relevant to a proposed `P` source. The linear power is therefore real under these state assumptions.

A full comparator is available in the matched dilute single-component limit, with `rho_I -> rho_0` and

\[
\Omega(k)^2=c_s^2k^2+\frac{k^4}{4m^2},\qquad
\chi_\rho=\frac{\rho_0 k^2}{\Omega(k)^2-s}.
\]
\[
S(\Delta)=\sqrt{c_s^4+\Delta^2/m^2},\qquad
k(\Delta)^2=2m^2[S(\Delta)-c_s^2],
\]
\[
\boxed{\quad
\mathcal J_{P_L}(\Delta)=\frac{\rho_0 k(\Delta)}{4\pi^2S(\Delta)},
\qquad \mathcal J_\rho(\Delta)=k(\Delta)^2\mathcal J_{P_L}(\Delta).
\quad}
\]

This follows from the `k^2 dk/(2pi^2)` momentum measure and `F_P/(2Omega)=rho_0/(2Omega)`, including the Jacobian `d k/d Delta`. The infrared expression above follows exactly. In a particle-like NR window `m c_s << k << m`, the same expression has

\[
\mathcal J_{P_L}(\Delta)\sim
\frac{\rho_0 m\sqrt{2m}}{4\pi^2\sqrt\Delta}.
\]

The mathematical NR continuum has this asymptotic as `k -> infinity`; the physical action permits using it only if a particle-like window exists below its NR and dilute cutoffs. It differs from the `Delta^-2` tail and finite total dipole weight of the separate exact two-level ensemble `w(Delta)=p_sat a Delta/(a^2+Delta^2)^(3/2)`. No equality of the two measures is asserted: one uses squared operator matrix elements of propagating harmonic modes, the other a dipole-weighted population of localized two-level systems. A mass-density form factor and a localization/occupation map would be needed before their normalizations could even be equated.

Three obstructions prevent using the matching low-gap exponent as the missing derivation:

1. A source at wavevector `k` couples to that `P_L(k)`. A uniform source selects zero momentum; it does not independently tilt every momentum mode. Integrating all momenta to obtain `J_P` does not turn them into distinct internal gaps co-located at each spatial point. The full static kernel is still `chi_P^{-1}(0,k)=k^2 chi_rho^{-1}(0,k) -> 0`.
2. A harmonic mode with Hamiltonian `p^2/(2I)+I Omega^2 x^2/2-E q x` has `p_ind=q^2 E/(I Omega^2)`, linear with no finite saturation. Its ground-state energy shift is `-q^2 E^2/(2I Omega^2)`. It does not have the avoided-crossing response `E/sqrt(Delta^2+E^2)` assumed by the two-level construction.
3. Uniform ordinary gravity couples to center-of-mass mass. At fixed total weighted number its spatially constant potential is proportional to the identity; a uniform acceleration translates the center of mass. The canonical action supplies no internal positive/negative gravitational mass dipole. Boundaries, gradients, tidal fields or an added differential force would be new inputs, and must be distinguished from the original uniform source.

The conversion branch has a nonzero gap and cannot provide a low-gap tail on this fixed branch. Approaching a gap-closing transition changes the hypotheses; one must then calculate the critical spectral function and source matrix elements anew. No all-loop or all-state exclusion follows from this branch calculation.

## 6. Kinetic state and scope of the Ward statement

For a collisionless bath with frozen species populations, the linearized Vlasov response of a species of mass density `rho_i`, Maxwell dispersion `sigma_i`, and gravitational acceleration `-grad Phi_N` is

\[
\chi_i(\omega,k)=\frac{\rho_i}{\sigma_i^2}[1+\zeta_i Z(\zeta_i)],
\quad\zeta_i=\frac{\omega+i0}{\sqrt2 k\sigma_i},\quad
Z(\zeta)=\frac1{\sqrt\pi}\int\frac{e^{-x^2}}{x-\zeta}\,dx,
\]

where the retarded contour is fixed by `Im zeta>0` before continuation. This formula follows by integrating `delta f=(k dot grad_v f_0)/(k dot v-omega) Phi_N`. It gives `chi_i(0,k)=rho_i/sigma_i^2`, while its fixed-frequency small-`k` behavior is `-rho_i k^2/omega^2`. Summing species and imposing Newton gravity again produces the attractive Jeans denominator. Conversion or collisions require a separately specified collision kernel and time-scale regime; neither a temperature nor a Maxwell state follows from the action. This comparator therefore closes the simple collisionless-order-of-limits route, not the entire nonequilibrium kinetic program.

For any exactly conserved density, continuity and a regular finite-frequency current response constrain its fixed-nonzero-frequency density response to vanish as `k^2`. This explains the frequency-dependent inverse pole. The Ward identity alone does **not** constrain the static compressibility: in other systems a genuinely incompressible or density-gapped phase can have `chi(0,k) proportional to k^2`, and hence a positive inverse `1/k^2`. Such a phase has not been derived for this continuum neutral bath. It must not be ruled out by exchanging limits in a Ward identity.

At tree level on a positive-amplitude branch the density constraint can be varied through finite local amplitude perturbations at finite static energy cost. This directly precludes a diverging positive static density curvature from those same fields. More precisely, for a stable finite local quadratic density matrix `A(k)` and nonzero fixed source vector `h`, minimizing at fixed `h^T x=delta rho` gives curvature `C_rho=1/(h^T A^{-1}h)`. The admissible trial `x=h delta rho/(h^T h)` bounds it above by `h^T A h/(h^T h)^2`. Finite entries near `k=0` preclude `C_rho ~ +K_G/k^2`, including a semidefinite limit when the constrained minimum exists. This is a classical static finite-field statement. It assumes the trial direction is physically admissible and does not prove that the exact quantum effective functional is local.

Possible changes of premises include an emergent long-range gauge constraint, a density-gapped or topological phase, inhomogeneity, boundaries, nonzero superflow, an altered gravitational source, or nonlocal quantum/thermal kernels. The bare microscopic action has not supplied any of these as the required physical tether. An added repulsive massless mediator could supply a positive static pole, but would be a separate interaction and require its own matching; it has not been introduced here.

## 7. Evidence, review and continuation

`contract.json` declares the bounded finite assertion before execution. `check_collective.py` checks the Cartesian derivation, both parity blocks, exact retarded density numerator, inverse phase matrix, conservation limit, fully matched neutral interaction difference, one original-action rational state at four momenta per parity, four imaginary-frequency matrix inversions, and the full Bogoliubov spectral Jacobian and limiting coefficients.

`run_002/manifest.json` has status **completed**, **50 passing exact/finite assertions**, unchanged pinned inputs, Python 3.9.6 and SymPy 1.14.0. The manifest was validated against the project root. The process took less than one second under a 45-second wall cap, 35-second CPU cap, 1 MiB log cap and one conventional numerical thread. `run_001` is preserved as a `launch-failed` attempt: the requested POSIX memory cap failed in `preexec_fn` on this macOS host before the mathematical program started. The successful rerun omitted that optional cap; no mathematical assertion is drawn from run 001.

The displayed formulas have a separate hand derivation and a self-review; an independent author-free derivation remains for the coordinator's review. The finite checks establish the stated implemented identities and example, not an all-state theorem or an actual condensate history.

An adjacent primary-source check authenticated Bellitti, Goldstein and Laumann, *Lifetime of excitations in atomic and molecular Bose–Einstein condensates*, Phys. Rev. A **107**, 033304 (2023), DOI [10.1103/PhysRevA.107.033304](https://doi.org/10.1103/PhysRevA.107.033304), accepted manuscript dated 21 February 2023, available from [APS/CHORUS](https://link.aps.org/accepted/10.1103/PhysRevA.107.033304). Equations (1)–(10) display conserved `N_a+2N_m`, the conversion interaction and its relative-phase locking; pages 1–2 distinguish Goldstone and gapped branches. Our dictionary is their `alpha -> c`, `nu -> delta`, `Psi_m -> -b`; their molecular self-repulsion and atom–molecule elastic coupling are **not** imported. This is adjacent consistency support for retaining both modes, not an external theorem proving our response, stability or gravity claim. The earlier Ho–Shenoy arXiv version was discoverable but its exact PDF fetch failed; no claim here relies on it.

Continuation contract:

- **Resolved within scope:** complete coherent neutral RWA density/phase response, actual matched neutral demixing sign, dynamic source/resonance distinction, and both density and displacement spectral weights. No positive static restoring pole or rational force law was constructed.
- **First unproved implication for the rational route:** a physical source-local internal dipole variable with finite saturation, its occupation, and the required weighted gap spectrum must emerge from the original fields. The inverse-divergence phonon displacement does not establish that map.
- **Open changed-state route:** determine whether actual production yields a kinetic mixture, charge-separated condensates, or a different phase, with conversion/leakage rates and gravitational source consistently matched. A new state is needed before rerunning response; repeating the same homogeneous saddle is not informative.
- **Open critical route:** if an admissible density-gapped or conversion-critical state is supplied, calculate its source-specific static susceptibility and nonlinear matrix elements. A closing gap alone does not determine their signs, locality or rational spectrum.
- **Review resumption:** independently derive the boxed matrices and conserved-density numerator, then check their physical source dictionary. Their algebra is pinned by the completed finite run; any changed source or state requires a fresh contract rather than extending its conclusion silently.
