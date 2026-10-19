# FSP-H-001: what a framework hydrogen bridge actually supplies

Parent: FSP-001. Base Git: `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty tree. Owner/write scope: `fine_structure_puzzle/atomic_bridge/hydrogen/`. Dated candidate: **H-MICRO-2026-10-19**, separately labelled microscopic continuation of the frozen S2 static action. No frozen theory file was changed.

The alpha goal is **not reached**. A specific physical bridge was derived and tested: if the frozen stiff medium action remains valid for microscopic mass sources and has a reciprocal quantum pair limit, its leading hydrogen correction is

\[
\delta V(r)=c_1r+\mathrm{constant},\qquad
c_1={Gm_em_p\over L_*^2}.
\]

At the most responsive allowed stiffness length, L*=5.75 pc, this gives **delta nu(1s to 2s)=1.16158180968e-78 Hz** and **delta mean radius / mean radius = -7.8505252e-95**. The two dark-energy footings give the same leading coefficient; the dependence on a0 cancels from this local term. Ordinary Newton gravity supplies a much larger but still negligible 2.1740030e-24 Hz transition shift. These are radial expectation and response calculations, not force comparisons alone.

There is also a structural obstruction: for fixed masses and an alpha-independent medium energy, the atomic ground energy is strictly decreasing with alpha. Minimizing atomic energy or atomic size therefore supplies no stationary equation selecting alpha. A mass-generation/Maxwell-normalization mechanism would need additional couplings and dynamics.

## 1. What is assumed, and what the framework states

The frozen canonical action has K=4piG, u=K|P| and

\[
\mathcal L=-{|\nabla\Phi-KP|^2\over2K}-\rho_b\Phi-W_{\rm rem}(u)
-{\gamma\over2}|\nabla P|^2,
\quad KW_{\rm rem}'(u)={u^2\over a_0-u},\quad {\gamma\over K}={L_*^2\over2}.
\]

This describes a modified gravitational field and a material medium; it does not replace the inertial kinetic term of an electron with an acceleration-dependent inertia. Its source is a gravitational mass density. The Coulomb force is not an extra contribution to g_N in this field equation. The frozen cold-medium population, its continuum cutoff, its current action, and its response to quantum sources are not specified at atomic scales.

H-MICRO makes explicit additional assumptions: ordinary electron and proton rest mass both couple reciprocally to Phi; microscopic source density becomes the operator sum_i m_i delta(x-x_i), with self terms removed; the quadratic medium can be eliminated into a conservative pair kernel. This is distinct from coupling only to baryon number, from a passive electron that never sources the medium, and from using a classical expectation density m|psi|² in a nonlinear Schrodinger-Newton equation. The latter introduces wavepacket-dependent self terms and does not derive the same Hamiltonian. A fixed, localized proton is a useful test-source limit, not a derivation of a quantum medium.

No carrier mass, occupancy, coherence length below L*, noise spectrum or dynamical high-frequency susceptibility was invented. If continuum response fails at atomic wave number, the numbers here are conditional extrapolations. The calculation establishes no bound on every possible microscopic completion.

## 2. Finite-mass hydrogen and its information content

Let M=me+mp, R=(me re+mp rp)/M, r=re-rp, P=pe+pp and p=(mp pe-me pp)/M. Directly substituting the canonical transformation gives

\[
{p_e^2\over2m_e}+{p_p^2\over2m_p}={P^2\over2M}+{p^2\over2\mu},
\qquad \mu={m_em_p\over m_e+m_p}.
\]

With kappa=alpha hbar c, the leading relative Hamiltonian is

\[
H_{\rm rel}={p^2\over2\mu}-{\kappa\over r}
-{Gm_em_p\over r}+\delta V_{\rm medium}(r)
+\delta V_{\rm charge\ size}+H_{\rm rel/QED/spin}.
\]

The last terms include relativistic, recoil beyond reduced mass, radiative, hyperfine, nuclear structure and polarization effects; this computation does not claim an experimental hydrogen spectrum at their precision. The electromagnetic charge normalization is alpha(0), the low-energy coupling, already supplied as input. No running to a high energy value or derivation of Maxwell's coefficient has occurred.

For the leading Coulomb problem, a=hbar/(mu alpha c), En=-mu c² alpha²/(2n²). Thus

\[
d\log a=-d\log\alpha-{m_p\over M}d\log m_e-{m_e\over M}d\log m_p,
\quad d\log|E_n|=2d\log\alpha+{m_p\over M}d\log m_e+{m_e\over M}d\log m_p.
\]

Numerically, a=5.29465409463e-11 m and mean r_1s=1.5a=7.94198114194e-11 m. The proton-mass elasticity is only 0.000544320575; the electron-mass elasticity is 0.999455679. Atomic radius is not an independently defined fixed boundary. Its standard wavefunction scale mostly probes the electron mass and alpha. A nuclear mass measurement, charge radius, QCD scale and a galactic baryonic inventory are separate inputs.

At r=a, the proton's Newton gravitational field is 3.98225e-17 m/s², whereas the electron's electromagnetic acceleration is 9.03437e22 m/s². The former is the gravitational source field. Neither evaluating a total electromagnetic acceleration in a MOND interpolation formula nor changing the electron kinetic energy is licensed by S2. The ratio of the ordinary gravitational and Coulomb forces is alpha_G/alpha=4.40789e-40, where alpha_G=G me mp/(hbar c).

## 3. Derive the response from S2, including reciprocity

Variation in Phi gives div(grad Phi-KP)=K rho. Variation in P gives

\[
\nabla\Phi-KP=R(u)\hat P-\gamma\Delta P,
\qquad R(u)={u^2\over a_0-u}.
\]

In a spherical, isolated local branch, grad Phi=g_N er+u er. With lambda²=gamma/K=L*²/2,

\[
g_N=R(u)-\lambda^2\left(u''+{2u'\over r}-{2u\over r^2}\right).
\]

The vector Laplacian is essential. For weak microscopic polarization and short distances, the derivative term dominates, and a point source has u=GM/L*² at leading order, since Delta(u er)=-2u er/r². Treating u as a scalar would erase this term and give the wrong microscopic law.

Reciprocity can be checked without a one-way test-particle force. Linearize in an isotropic medium Hessian A>=0. Its longitudinal static response gives

\[
\Phi(k)=-{4\pi G\rho(k)\over k^2}
\left[1+{1\over A+\lambda^2 k^2}\right].
\]

The second term has a symmetric real Green kernel; inserting rho=me delta_e+mp delta_p into one-half rho Phi retains one cross term. For A>0 this gives the exact pair correction

\[
\delta V_A(r)=-{Gm_em_p\over A r}(1-e^{-qr}),\qquad q={\sqrt A\over\lambda}.
\]

Subtracting its r=0 constant yields

\[
\delta V_A^{\rm ren}=C\left[1-{1-e^{-qr}\over qr}\right]
=c_1r-{c_1q\over3}r^2+\cdots,
\quad C={Gm_em_pq\over A},\quad c_1={Gm_em_p\over2\lambda^2}.
\]

The A->0 limit after constant subtraction is c1r. A local linear potential does not fix an absolute ionization threshold: that requires the entire exterior and its potential zero. For the explicit A>0 screened example the physical delta V tends to zero at infinity; its leading atomic effect includes a common negative constant. At canonical A=Aperp=2.478553 and L*=5.75 pc, that constant is -5.14861e-85 J, while the local 1s excitation-sensitive term is +2.56557e-112 J. A positive local first-order energy term does not mean the full additional attraction reduces binding.

The actual Galactic background is anisotropic. CFG770 gives Ai=R/ue transversely and R'(ue) longitudinally, and mi=(Ai+lambda²k²)/(Ai+1+lambda²k²). Expansion at large k gives the same isotropic 1/(lambda²k²) leading response; anisotropy and background dependence first enter higher orders and regular tidal terms. At canonical ge=2.32e-10, Apar=11.10033. The proton perturbation u/ue=5.32e-62, so amplitude linearization itself is extremely safe under the candidate continuum extension. It does not establish that the extension is physically admitted.

The no-background nonlinear crossover length is L*²/(2 rM), rM=sqrt(Gmp/a0). It is 4.56e47 m at the canonical floor. This is a diagnostic that an isolated proton's extrapolated macroscopic halo cannot be assumed to settle out to its formal asymptote within the universe. The local high-k coefficient does not require that fictitious asymptote; matching, background and medium formation still need their own physics.

## 4. Actual radial perturbation and size response

Normalize x=r/a. The radial probability densities are 4x² exp(-2x), x²(2-x)² exp(-x)/8 and x⁴ exp(-x)/24 for 1s,2s,2p. Integrating these gives mean x=(1.5,6,5). Hence

\[
\delta E_{1s}={3\over2}c_1a,\quad
\delta E_{2s}=6c_1a,\quad
\delta E_{2p}=5c_1a,\quad
\delta\nu_{1s\to2s}={9c_1a\over2h},\quad
\delta\nu_{2p\to2s}={c_1a\over h}.
\]

This is a specific l-dependent pattern. A shift of alpha in a pure Coulomb Hamiltonian preserves the nonrelativistic 2s/2p degeneracy; this perturbation splits it. It therefore cannot be entirely absorbed into reinterpreting alpha or reduced mass.

Let epsilon=c1 a/(mu c² alpha²). In reduced atomic units H=-Delta/2-1/x+epsilon x. For psi_1s proportional to exp(-x), write delta psi=epsilon f psi. Direct substitution gives f=(3-x²)/2, with mean f=0, and

\[
{d\langle x\rangle\over d\epsilon}=2\langle xf\rangle=-3,
\qquad {\delta\langle r\rangle\over\langle r\rangle}=-2\epsilon+O(\epsilon^2).
\]

The independent radial eigensolver gives derivatives 1.50000623, 6.00000754, 4.99999701 for the three level energies on dx=.005, and -3.00005633 for ground radius. Refining dx=.01 to .005 improves the Coulomb benchmarks and leading susceptibilities. Physical epsilon=3.92526261e-95 is far below binary64 resolution; the code computes amplified derivatives and then rescales. It never subtracts total numerical energies to claim that it resolved this physical shift.

| L* | 1s to 2s shift, Hz | 2p to 2s shift, Hz | ground relative mean-radius shift |
|---|---:|---:|---:|
| 5.75 pc | 1.16158181e-78 | 2.58129291e-79 | -7.85052522e-95 |
| 1000 pc | 3.84047986e-83 | 8.53439969e-84 | -2.59557990e-99 |

These leading entries hold separately on both a0 footings. L* is a measured/bounded input, not selected to fit alpha. A unit-strength atomic epsilon would require L*=1.1116e-30 m under this formula, wholly inconsistent with its pc-scale stiffness input; this is a rejection diagnostic, not a proposed fitted parameter.

For the explicit isotropic screened pair, exact first-order dimensionless expectations are, with z=qa,

\[
{\delta E_{1s}^{\rm ren}\over c_1a}={2(z+3)\over(z+2)^2},\quad
{\delta E_{2s}^{\rm ren}\over c_1a}={12+20z+15z^2+4z^3\over2(1+z)^4},\quad
{\delta E_{2p}^{\rm ren}\over c_1a}={10+20z+15z^2+4z^3\over2(1+z)^4}.
\]

At the canonical floor, z=6.64406e-28 and screening changes the 1s-to-2s first-order result by -1.91939e-27 fraction. These rational forms avoid catastrophic subtraction of the common constant.

A bound also controls perturbation theory in that explicit global model. The renormalized potential satisfies 0<=V<=C, so its operator norm is C. In each fixed-l radial sector an isolated Coulomb level has separation Delta from the other levels. For C<Delta/2, the projected resolvent identity and the spectral norm bound give |E-En-mean V|<=C²/(Delta-2C). The relevant gaps are 3Eh/8 for 1s and 5Eh/72 for 2s. Adding their error bounds gives **1.57e-117 Hz** for the transition, compared with its 1.16e-78 Hz first-order shift. This is a conditional analytic bound for the point-source isotropic screened extension, not a proof for the whole nonlinear anisotropic medium. Both the exact radial integral and the bounded global potential rule out a hidden large binding change within that declared extension.

## 5. Finite proton and source distinctions

For a uniform proton mass ball of radius Rm, the symmetric short-distance kernel is the spatial average of |r-s|. Direct angular and radial integration gives

\[
f_{R_m}(r)=\begin{cases}
3R_m/4+r^2/(2R_m)-r^4/(20R_m^3),&r<R_m,\\
r+R_m^2/(5r),&r\ge R_m.
\end{cases}
\qquad \delta V=c_1 f_{R_m}(r).
\]

It is regular at the center and matches both potential and force at the surface. Outside, the force is c1[1-Rm²/(5r²)], not exactly the point-source constant. In the illustrative uniform ball Rm=sqrt(5/3) rp_charge, Rm/a=2.049999e-5; exact Coulomb expectation values change the transition result by -1.4008320e-11 fraction. The leading exterior correction depends on the mass second moment, <s²>/(3r), so the uniform sphere is a source-shape diagnostic, not a measured proton mass distribution.

Electromagnetic finite charge size is different. Its leading ns correction is delta Ens=(2/3) kappa rp_charge²/(n³ a³), giving about 1.10544e6 Hz for 1s. This does not identify a gravitational mass radius or select alpha. It shows the distinct source moments and the degree to which ordinary structure corrections exceed this medium term.

## 6. Deliberately different gravitational control

[Milgrom 2014, arXiv:1311.2579v2, Eq. (23)](https://arxiv.org/html/1311.2579v2) gives a reciprocal classical force in an isolated, scale-invariant deep-MOND point-mass limit. Its potential is A_log log(r/rref), with

\[
A_{\log}={2\over3}\sqrt{Ga_0}\big[(m_e+m_p)^{3/2}-m_e^{3/2}-m_p^{3/2}\big].
\]

The symmetric coefficient is 0.984578 times the one-way test-mass coefficient me sqrt(Gmp a0). Integrating the pure logarithmic model against Coulomb radial states gives delta nu_12=(A_log/h)(3/4+log 2), equal to 6.31452e-21 Hz canonical and 6.94169e-21 Hz alternative. Its 2p-to-2s result is A_log/(6h). These are conditional diagnostics of a different pure-log model; a full unstiffened interpolation, its small-r/high-g correction, external field and quantum matching were not solved. The result is not a prediction of frozen S2, which contains L* and loses the required microscopic scale invariance. Replacing S2 by this control would change the computed transition by a factor 5.43614e57. The source theorem does not license replacing the total Coulomb acceleration with a gravitational acceleration.

## 7. Can a natural atomic stationarity condition select alpha?

Within the candidate, the answer is no, by a sign argument independent of the tiny numerical coefficient. Take fixed positive masses, a positive normalized nuclear charge profile, and any alpha-independent gravitational/medium operator. At a normalized stationary ground state,

\[
{dE_0\over d\alpha}=-\hbar c\langle 1/r\rangle<0
\]

for a point charge. A finite nuclear charge replaces 1/r by its positive averaged Coulomb kernel and preserves the sign. At a jointly stationary wavefunction and medium field, their implicit derivatives vanish in the envelope derivative and the same explicit negative term remains. Thus even a fully relaxed static medium cannot supply dE/dalpha=0 without additional alpha-dependent terms. This proof fixes the masses, background, number of atoms, self-energy convention and medium parameters. Alpha-dependent particle masses, charged medium, vacuum terms or a varying gauge kinetic function are new physical mechanisms outside its hypotheses.

Differentiability is not essential: using a minimizing state at alpha1 as a trial state at alpha2>alpha1 gives E0(alpha2)<=E0(alpha1)-(alpha2-alpha1) hbar c mean(1/r)_alpha1<E0(alpha1). This requires a common admissible domain and an attained stable minimum; it also applies when the medium configuration is included among the trial variables. A field stationary point that is not a stable minimum does not become a vacuum-selection mechanism by this argument.

Atomic radius stationarity is a different equation. An exponential trial state of scale b gives

\[
E(b)={\hbar^2\over2\mu b^2}-{\kappa+Gm_em_p\over b}+{3c_1b\over2},
\quad {3c_1b^3\over2}+(\kappa+Gm_em_p)b-{\hbar^2\over\mu}=0.
\]

The left side has positive derivative for b>0 and crosses zero once for every positive alpha. It selects b conditional on alpha, not alpha. The exact radius susceptibility above is preferable to this trial state's approximate coefficient. The physical ionization energy has the same alpha derivative when the free rest masses and environment are held fixed; changing the potential zero cannot manufacture a selector.

## 8. Verification, limits, and continuation

`run003/manifest.json` has status `completed` and passes the installed v2 manifest validator against current inputs. It records actual before/after hashes, software, dirty Git revision, command, bounds and output hashes. `run001` (49 checks) and `run002` (53 checks) are retained historical evidence from earlier script revisions; their code hashes differ from the present script and they must not be validated as current-script runs. The current run has 63 passing assertions. Arithmetic is 100 decimal digits for scale separation and binary64 for independent radial quadratures and eigenvalues. No random sampling was used.

Executed controls include radial normalization and known Coulomb energies; angular convolution versus independent source-ball formula at 12 source/position pairs; exact radial moments; two grid resolutions; an orthogonal Dalgarno solution; mass-exchange reciprocity; the G=0 limit; the L* inverse-square law; exact screened rational identities against direct radial quadrature at z=.1,1,4; and a Cartesian finite-difference check of the radial vector Laplacian. Deliberate scalar-Laplacian and unstiffened-law substitutions are evaluated and detected. The EM-acceleration source mismatch is an analytic type/parameter-dependence control, not an independently executed alternate microscopic theory. No historical galaxy code was run.

Proof status is **conditional on named microscopic continuation assumptions**, with a self-review of derivations and orthogonal numerical checks. The coordinator independently rederived the S2 variation, vector Laplacian, Fourier coefficient -8piG/(L*² k⁴), reciprocal cross-term normalization, transition sign and Dalgarno susceptibility on 2026-10-19. The coordinator also checked the screened exact kernel, bound 0<=W<=C, fixed-l spectral gaps, resolvent remainder C²/(Delta-2C), and uniform-source finite-size factor. Alpha-monotonicity scope has an author's self-review. Passing computations are not a quantum-medium existence proof. No global novelty claim is made.

The first unresolved implication is from a coarse-grained static material action and a condensed-source prescription to a reciprocal, regulated electron/proton quantum source action. Resolve source charge (mass, baryon number or another current), finite carrier/coherence cutoff and the P susceptibility D(omega,k) before claiming atomic predictions. A static proton limit should reproduce the local kernel; a joint quantum treatment must preserve translation invariance, remove or renormalize self terms, and distinguish its pair correlation from an expectation-density closure. Material relaxation/noise and recoil require dynamical checks; no cold particle automatically supplies the assumed quantum propagator.

The executable immediate check is a fresh reproduction:

```bash
python3 fine_structure_puzzle/atomic_bridge/hydrogen/reproduce.py --run run004
```

The next physical discriminator is to supply the microscopic action's longitudinal static transfer T(k)=delta Phi/Phi_Newton and evaluate it at k around 1/a=1.89e10 m^-1. The current continuation requires T(k)=1/(lambda²k²) at large k. If a completion instead couples electromagnetism or masses to a selected scalar, derive its extra explicit alpha derivative and test whether it can cancel -hbar c mean(1/r) using independently fixed couplings. No new numerical fit to alpha can substitute for this missing action.
