# Particle-level saturation from a declared two-orbital projection

Parent: `CE-SHARED-STATE-2026-10-19 / CE-FM092`. Observed HEAD:
`e54c33252909e38a529a69f7adac265e37b54cb4`. Input byte pins are in
`source_pins.json`. This lane writes only its assigned directory.

**Result and exact scope.** A finite stock of the original daughter bosons,
projected onto two spatial orbitals of a stated positive baryonic gravitational
environment, has a derived, bounded population response. Its manybody Hilbert
space has dimension `N+1`; its contact, tunnelling, gravitational self terms,
recoil and common-gravity source are obtained from spatial overlaps. This is a
particle projection rather than an inserted distribution of two-level sites.
The complete rigid-host source has exactly zero internal uniform mass dipole
and a nonzero finite-wavelength operator. In the finite projection, a simple
largest source eigenvalue gives a generic high-field deficit proportional to
`E^-2`. The coherent two-mode GP limit has the same power. The isolated gapped
finite-N ground response is odd and analytic at zero field, so it does not
equal the requested rational law there or at arbitrarily high field.

The positive double-lobed baryon density, its mechanical support and fixed
shape, the scalar stock, its preparation and the two-orbital approximation are
environmental/state inputs. The Gaussian orbitals below are an explicit
Galerkin choice, not certified continuum eigenfunctions. No continuum
truncation error or actual baryon material phase is established. In particular,
the formal finite-matrix limit `E -> infinity` is not a high-field theorem for
the unconfined original continuum. This construction gives a genuine
particle-level bounded projection and a concrete route to finite-window
saturation; it does not establish that window in a selected physical state.

## 1. Action, matching and source retained

Use the original canonical complex fields, charges one and two,

\[
 V=m^2|\Phi|^2+M^2|X|^2+g_s(X^*\Phi^2+X\Phi^{*2})
   +\lambda_{\rm tot}|\Phi|^4,\qquad M>2m,
\]
\[
 \lambda_{\rm tot}=\lambda_{\rm rep}+{g_s^2\over M^2-4m^2},
 \qquad g_2={\lambda_{\rm rep}\over2m^2}>0.                 \tag{1}
\]

The contact convention is `(g2/2) psi† psi† psi psi`. The positive-square
ancestor alone has `lambda_rep=0`; its repulsive extension and full threshold
matching, including the removed negative-frequency correction, are pinned.
No additional scalar-baryon interaction is used. The Newtonian source is the
complete scalar plus baryon rest mass at the retained NR order. Relativistic
interaction, kinetic and gravitational binding contributions to the metric
source are higher-order matching obligations, not extra negative masses.

The NR projection presupposes a dilute single-sign prepared daughter sector,
negligible real `X` stock, small velocities and potentials, and all retained
excitation/contact scales below both the rest scale and `M-2m`. Finite-basis
contact arithmetic is a regulated tree-level projection, not a new all-loop
renormalization claim.

Let a rigid but freely translating baryonic body have mass `Mb`, center `Y`,
and centered positive density

\[
 \rho_b(s)={M_b\over2(\pi B^2)^{3/2}}
 \{e^{-|s-a\hat z|^2/B^2}+e^{-|s+a\hat z|^2/B^2}\}.       \tag{2}
\]

Its Newtonian potential is exactly

\[
 U_b(s)=-{GM_b\over2}\sum_{\epsilon=\pm1}
 {\operatorname{erf}(|s-\epsilon a\hat z|/B)
  \over|s-\epsilon a\hat z|}.                              \tag{3}
\]

This is a specified ordinary positive-mass environment. Its internal stress,
two-lobed shape stability and large internal excitation gap are not derived
from the scalar action. Treating the host as rigid is a stated reduction;
its whole-body recoil is retained exactly below.

For scalar coordinates `s_i=x_i-Y`, define `S=sum_i s_i`,
`Mtot=Mb+Nm`, `alpha=m/Mtot`. The total center is
`R=Y+alpha S`. At `R=0`, `Y=-alpha S` and `x_i=s_i-alpha S`.
In canonical momenta conjugate to the `s_i`, the exact rigid-body relative
Hamiltonian at the retained Newtonian order is

\[
 H_0=\sum_i\left[{p_i^2\over2m}+mU_b(s_i)\right]
       +{(\sum_i p_i)^2\over2M_b}
       +\sum_{i<j}\left[g_2\delta^3(s_i-s_j)
                    -{Gm^2\over|s_i-s_j|}\right].           \tag{4}
\]

The one-body reduced-mass correction and two-body mass-polarization term in
the square are both kept. It is inconsistent to keep a baryonic well while
fixing its COM when calculating the common gravitational source.

## 2. Explicit orthonormal wavefunctions and overlaps

Start with normalized real 3D Gaussians

\[
 \phi_L(s)=(\pi\ell^2)^{-3/4}e^{-|s+a\hat z|^2/(2\ell^2)},
 \qquad \phi_R(s)=\phi_L(-s),\qquad
 s_0=\langle\phi_L|\phi_R\rangle=e^{-a^2/\ell^2}.            \tag{5}
\]

Set `p=(1+s0)^(-1/2)`, `q=(1-s0)^(-1/2)`,
`A=(p+q)/2`, `B0=(p-q)/2`. The explicitly orthonormal orbitals are
`wL=A phiL+B0 phiR`, `wR=B0 phiL+A phiR`.
Use the real matrix `C=[[A,B0],[B0,A]]` to transform every one-body matrix
and all four indices of every interaction tensor. `B0` is not the host width
`B` in (2).

For primitive centers `c_i=+/- a zhat`, put
`Sij=exp[-|ci-cj|²/(4ell²)]`, `cij=(ci+cj)/2`. Define
`F(d,L)=erf(d/L)/d`, with `F(0,L)=2/(sqrt(pi)L)`. Direct Gaussian integration
gives

\[
 K_{ij}={\hbar^2\over2m}S_{ij}
 \left[{3\over2\ell^2}-{|c_i-c_j|^2\over4\ell^4}\right],
\]
\[
 V_{ij}=-{GmM_b\over2}S_{ij}
       \sum_{\epsilon=\pm1}F(|c_{ij}-\epsilon a\hat z|,
                             \sqrt{\ell^2+B^2}),
\]
\[
 (p_z)_{ij}={i\hbar(c_{i,z}-c_{j,z})\over2\ell^2}S_{ij}.
                                                               \tag{6}
\]

The contact primitive tensor is

\[
 I_{ijkl}={(2\pi)^{-3/2}\over\ell^3}
 \exp\left[-{\sum_{r=i,j,k,l}|c_r|^2-
                     |c_i+c_j+c_k+c_l|^2/4\over2\ell^2}\right]. \tag{7}
\]

For the convention
`H2=(1/2)sum v_ij;kl a_i† a_j† a_l a_k`, the gravitational primitive tensor
and mass-polarization tensor are

\[
 v^{G}_{ij;kl}=-Gm^2 S_{ik}S_{jl}
       F(|c_{ik}-c_{jl}|,\sqrt2\ell),
 \qquad
 v^{\rm mp}_{ij;kl}={(p_z)_{ik}(p_z)_{jl}\over M_b}.        \tag{8}
\]

The transverse projected momentum matrices vanish by parity. Thus (4)
projects to `h=(1+m/Mb) K+V` and
`v=g2 I+vG+vmp`, all transformed by `C`. Scalar self-gravity is included
once; it is not added to an already scalar-containing external potential.

Dropping recoil and interaction overlap terms temporarily, define
`J=-(K+V)_LR`, `U=g2 int wL^4`, and write

\[
 H_{\rm BH}=-J(a_L^\dagger a_R+{\rm h.c.})
 +{U\over2}[n_L(n_L-1)+n_R(n_R-1)].                         \tag{9}
\]

This is a derivation of the two-site Hamiltonian from the spatial daughter
field, with its explicit omissions stated. The computation uses (4),(6)-(8),
not merely (9).

## 3. Interwell contact and density-assisted tunnelling

Parity leaves three real contact integrals

\[
 I_A=\int w_L^4=\int w_R^4,\quad
 I_B=\int w_L^3w_R=\int w_Lw_R^3,\quad
 I_C=\int w_L^2w_R^2.
\]

Put `U=g2 IA`, `T=g2 IB`, `W=g2 IC`. The complete projected contact is

\[
 H_c={U\over2}[n_L(n_L-1)+n_R(n_R-1)]+2W n_Ln_R
 +{W\over2}(a_L^{\dagger2}a_R^2+{\rm h.c.})
 +T[a_L^{\dagger2}a_La_R+a_R^{\dagger2}a_Ra_L+{\rm h.c.}]. \tag{10}
\]

In a fixed-N sector the last line is exactly
`T(N-1)(aL†aR+h.c.)`, so the density-assisted change is
`J_eff=J-T(N-1)`. The factor `2W` in the density term differs from the
`W/2` pair-transfer coefficient. The script independently compares this
closed fixed-N expansion with the four-index contact tensor in every case.

Orthogonalization creates small negative tails in the localized orbitals;
`IB` need not be positive. With Gaussian separation, `IB` starts at overlap
order `s0`, whereas `IC` starts at order `s0²`. Suppressing these terms
requires `|T|(N-1) << |J|` and the relevant `W N²` matrix elements small
relative to the scales being resolved. Merely requiring small density
overlap is insufficient if `J` is exponentially tiny. The general tensor
calculation avoids dropping them.

## 4. Complete common source with exact recoil

Probe the actual common Newtonian potential
`U_ext(x)=-E sin(kz)/k`. Its internal operator, before any orbital projection,
is

\[
 D_k={m\over k}\sum_i\sin[k(s_{i,z}-\alpha S_z)]
      +{M_bF_b(k)\over k}\sin[-k\alpha S_z],
\qquad F_b(k)=e^{-B^2k^2/4}\cos(ka),\qquad H_E=H_0-ED_k.
                                                               \tag{11}
\]

This source includes the scalar mass and the recoiling whole baryon profile.
For a uniform field its exact first moment is

\[
 D_0=mS_z-\alpha(Nm+M_b)S_z=0.                              \tag{12}
\]

Equation (12) is an operator identity in the unprojected relative system;
the conclusion does not follow from setting a code branch to zero.

An efficient **exact projected** version of (11) exists for every finite N.
Let

\[
 A_{ij}(t)=\langle w_i|e^{it z}|w_j\rangle
 =\left[C^T\{S_{ij}e^{it c_{ij,z}-t^2\ell^2/4}\}C\right]_{ij}.
                                                               \tag{13}
\]

The braces mean a primitive two-by-two matrix before applying `C`. Let
`Gamma_N(A)` be the action of `A` on the symmetric N-fold tensor power in
the normalized number basis `|N-n,n>`, and define

\[
 Q=m\left.{d\over dt}\Gamma_N\{A(-k\alpha)
                    +t A[k(1-\alpha)]\}\right|_{t=0}
    +M_bF_b(k)\Gamma_N[A(-k\alpha)].
\]
\[
                 D_k^{(N)}={Q-Q^\dagger\over2ik}.           \tag{14}
\]

The derivative selects one scalar exponential while the other N-1 particles
carry the COM recoil exponential. Thus (14) projects the full manybody
source; replacing it by `N` independent fixed-anchor sources would be wrong.
For N=1,2 the implementation is independently compared with an explicit
distinguishable-particle tensor product followed by symmetrization.

In the heavy-host limit, for fixed N, the leading source becomes the
one-body operator

\[
 D_k=m\sum_i\{\sin(ks_{i,z})/k-F_b(k)s_{i,z}\}
       +O(Nm/M_b),                                        \tag{15}
\]

where the remainder is a fixed-state/moment expansion; it is not a uniform
operator-norm bound over arbitrary positions. The recoil term survives
`Mb -> infinity`: the host displacement is small but its source mass is
large. Parity makes the real off-diagonal one-body matrix element vanish.
The diagonal source per right particle is

\[
 d_k={m\over\sqrt{1-s_0^2}}
 \left[e^{-\ell^2k^2/4}{\sin(ka)\over k}
                 -a e^{-B^2k^2/4}\cos(ka)\right]
\]
\[
 ={ma k^2\over\sqrt{1-s_0^2}}
       \left[{a^2\over3}+{B^2-\ell^2\over4}\right]+O(k^4).
                                                               \tag{16}
\]

Then `D_k=d_k(nR-nL)` at this leading order. The finite-N calculation uses
(14) with finite `Mb`, not this approximation. The internal source is
`O(k²)`, its density Fourier perturbation is `O(k³)`, and its static
susceptibility is `O(k⁴)` for a fixed gapped Hamiltonian. No claim is made
about every source shape, every gap-closing family, or every original state.

## 5. Exact finite-N ground response, spectrum and saturation

All matrices in (4),(14) act on the complete fixed-N basis `n=0,...,N`.
In the approximation (9),(16), the diagonal entries are

\[
 H_{nn}={U\over2}[(N-n)(N-n-1)+n(n-1)]-Ed_k(2n-N),
\quad H_{n+1,n}=-J\sqrt{(n+1)(N-n)}.                       \tag{17}
\]

No particle-count cut is made within this projected sector. Let
`epsilon_nu(E), |nu,E>` be the eigenpairs of the full projected matrix.
The exact ground polarization is

\[
 P_N(E)=-\partial_E\epsilon_0(E)
       =\langle0,E|D_k^{(N)}|0,E\rangle.                   \tag{18}
\]

Its actual zero-field spectral measure is the discrete pushforward

\[
 \sum_{\nu>0}|\langle\nu|D_k^{(N)}|0\rangle|^2
                  \delta_{\Omega_\nu},\qquad
 \Omega_\nu=\epsilon_\nu-\epsilon_0,
\quad \chi_N=2\sum_{\nu>0}{|D_{\nu0}|^2\over\Omega_\nu}. \tag{19}
\]

This is an actual collective particle spectrum. It is not a population of
independent saturating sites labelled by each transition. All transitions
share the same N particles; counting the source mass again for every gap
would duplicate the stock.

Let `dmax` be the simple maximum eigenvalue of the finite source matrix and
`|r>` its eigenvector. Write the other source eigenvalues/eigenvectors as
`d_j,|j>`. Ordinary finite-matrix perturbation about `-E D` gives

\[
 \epsilon_0(E)=-Ed_{\max}+\langle r|H_0|r\rangle
              -{\mathcal A\over E}+O(E^{-2}),
\quad \mathcal A=\sum_{j\ne r}
       {|\langle j|H_0|r\rangle|^2\over d_{\max}-d_j}\ge0,
\]
\[
             d_{\max}-P_N(E)={\mathcal A\over E^2}
                                      +O(E^{-3}).            \tag{20}
\]

The expansion holds for the finite matrix once `E min(dmax-dj)` dominates
its bounded `H0` scales. It is strictly `E^-2` when `A>0`. If all couplings
from `|r>` vanish, `A=0`, so `|r>` is an exact eigenvector of both matrices
and is exactly polarized once that branch is the ground state; no universal
nonzero coefficient is claimed. At fixed positive beta, thermal corrections
between separated source branches are exponentially suppressed at large E,
in addition to the same virtual-mixing power law.

For one noninteracting atom with `D=d sigma_z`, the projection gives exactly

\[
 P_1(E)={d^2E\over\sqrt{J^2+d^2E^2}},\quad
 P_{N,U=0}=N P_1,\quad
 dN-P_{N,U=0}\sim{NJ^2\over2dE^2}.                         \tag{21}
\]

Thus the familiar two-state formula can arise as the N=1 spatial projection
of the actual boson; it is not an independent microscopic postulate.
For finite repulsion the first all-right leakage in (17) has amplitude
`J sqrt(N)/[2Ed-U(N-1)]`. Its polarization loss starts at
`2d N J²/[2Ed-U(N-1)]²`; pair hopping and source non-diagonality are retained
in (20). Repulsion changes the crossover and susceptibility without changing
the generic finite-matrix power.

## 6. Coherent GP response and comparison with the target rational law

The fixed-N coherent orbital state is

\[
 |z,\varphi;N\rangle={1\over\sqrt{N!}}
 [\sqrt{(1-z)/2}\,a_L^\dagger+
 e^{i\varphi}\sqrt{(1+z)/2}\,a_R^\dagger]^N|0\rangle.
                                                               \tag{22}
\]

For (9), the coherent energy per particle at its phase minimum is

\[
 e(z)=-J\sqrt{1-z^2}+{U(N-1)\over4}(1+z^2)-Edz.
\]
\[
 Ed={Jz\over\sqrt{1-z^2}}+{U(N-1)z\over2}.                 \tag{23}
\]

For repulsive U and J>0 this gives a unique static minimum with `|z|<1`.
Its susceptibility is `N d²/[J+U(N-1)/2]`. With
`h=Ed` and `h-U(N-1)/2 >> J`,

\[
 1-z={J^2\over2[h-U(N-1)/2]^2}+o(h^{-2}).                  \tag{24}
\]

The population bound is generated by a finite particle inventory. The
Legendre derivative diverges as `(1-|z|)^(-1/2)` at the boundary. The target
`P=Psat E/(a0+|E|)` instead has a boundary force proportional to
`(Psat-|P|)^(-1)` and high-field deficit `Psat a0/|E|`. These are different
nonlinear equations of state.

At zero field, a parity-symmetric finite matrix with a simple gapped ground
has `P(-E)=-P(E)` and a convergent local analytic expansion
`P=chi E+c3 E³+...`. The target has the term
`-Psat E|E|/a0²` and fails to be twice differentiable at zero. Accordingly,
the exact rational law cannot be the response of this isolated finite-N
gapped projection on a neighborhood of zero. Infinite, gap-closing,
critical, disordered or formation-selected ensembles require separate
construction. This is not an all-state no-go for the original action.

## 7. Occupations are conditional predictions from a stated preparation

For fixed N and temperature T within the retained sector,

\[
 p_\nu(E)={e^{-\beta\epsilon_\nu(E)}\over Z_N(E)},\qquad
 P_{N,\beta}(E)=\sum_\nu p_\nu(E)D_{\nu\nu}(E).             \tag{25}
\]

This is a normalizable finite-dimensional trace. It is not the unrestricted
finite-temperature trace of an unconfined cluster, whose scattering and
breakup channels are absent from the projection. At a parity-symmetric
nondegenerate zero field,

\[
 \chi_{N,\beta}=2\sum_{\mu<\nu}
 {p_\mu-p_\nu\over\epsilon_\nu-\epsilon_\mu}|D_{\mu\nu}|^2.
                                                               \tag{26}
\]

Degenerate energy pairs require the corresponding continuous divided-
difference limit; diagonal thermal variance must be included if symmetry
does not make the source diagonal elements vanish. The tested matrices have
resolved simple zero-field eigenvalues and parity-odd D.

A specified initial coherent state (22) has energy-measurement probabilities
`pnu=|<nu|z,phi;N>|²`. These describe an energy measurement or the dephased
ensemble; the coherent time-dependent state also has interference terms.
The run records the balanced, phase-zero state. A weak specified pulse gives
`pnu ~ |Dnu0|² |Etilde(Omeganu/hbar)|²/hbar²` at leading order, not an
arbitrary target gap weight. Temperature, pulse shape, scalar N, host
abundance and spatial distribution are additional preparation data; the
bare action does not choose them.

## 8. Bounded computation and numerical results

`check_two_mode.py`, `contract.json`, `source_pins.json` and
`run_004/manifest.json` define the current evidence. `run_004/results.json`
stores every source eigenvalue, manybody gap, ground source weight,
conditional thermal/coherent population, response sample and check result.

Orbital units set `hbar=m=ell=1`, energy unit `hbar²/(m ell_phys²)`.
The final declared dimensionless environment is

`a=3.5, B=.7, Mb/m=1e9, G_dim=1e-8`, hence `G_dim Mb=10`.
Use `N=1,2,4,8,12` and dimensionless contact `g2=1e-4,5e-4`.
These are ten full matrices of maximum dimension 13, not a parameter search.
The orbital units should not be mistaken for setting the Compton wavelength
equal to the orbit size. For example `m ell_phys=100` in natural units gives
`Eunit/(mc²)=1e-4` and `lambda_rep=.02,.1` for the two contacts. This is a
weak NR-compatible scaling illustration, not a match to the project's 1 MeV
benchmark or a certified ordinary-baryon material state. The scalar mass,
physical G, size and host mass must jointly realize the dimensionless G;
these cannot be independently chosen when applying a fixed benchmark.

Analytic overlap evaluation gives

\[
 s_0=4.785117392129009\,10^{-6},\qquad
 J=1.744506771768059\,10^{-5},
\]
\[
 I_A=.06349363593641533,\quad
 I_B=-1.5124763741484154\,10^{-7},\quad
 I_C=2.1743933539515196\,10^{-12}.                            \tag{27}
\]

For the largest N/contact, `|T|(N-1)/J=4.77e-5`; the onsite gravitational
pair coefficient is about `-7.97886e-9`. Both are kept, including the still
smaller pair transfer and mass-polarization terms.

At `k=.25`, the actual full-recoil finite-N controls include:

| N | g2 | first gap | P_sat | chi_ground | chi_beta, beta J=1 |
|---:|---:|---:|---:|---:|---:|
| 1 | .0001 | .0000348901 | .7961975 | 36338.66 | 27675.31 |
| 4 | .0001 | .0000438596 | 3.1847900 | 91154.83 | 89939.13 |
| 4 | .0005 | .0000696026 | 3.1847900 | 33065.64 | 33370.03 |
| 12 | .0001 | .0000609157 | 9.5543699 | 140916.02 | 140949.45 |
| 12 | .0005 | .0001146221 | 9.5543699 | 37154.39 | 37155.69 |

In the last row the spectral coefficient in (20) is
`A=2.293597342191859e-9`. The directly diagonalized
`E²(P_sat-P)` at the formal dimensionless bias
`E(P_sat/N)/J=1e5` is `2.2940556910648857e-9`, a relative difference
`1.9984e-4`. Across all ten matrices the maximum such relative difference
is below `2.0e-4`; the tested tolerance is .004. These largest biases are
finite-matrix asymptotic controls, not claims of continuum two-mode validity.

For `N=12,g2=.0005`, `chi/k^4` is `1.1232231e7,1.1223343e7,
1.1187857e7,1.1046895e7` at `k=.01,.02,.04,.08`, respectively.
This verifies approach to the derived small-k power in that fixed state.
The balanced coherent state's ground-state energy-measurement weight is
`.82288418`, while its Gibbs ground weight at `beta J=1` is `.99859697`.
The first three source-carrying weights include `2.12762478`, `.00465094`,
and `.0000472995`; parity-forbidden intervening transitions have numerical
weights near zero. A selected preparation changes actual populations and
thermal susceptibility; it does not turn these transitions into separately
stocked TLS hosts.

All **88** final checks pass: explicit Gram orthonormality; independent
N=1,2 source tensor-product projection; noninteracting N=4 closed response;
independent contact tensor/number-basis expansion; matrix Hermiticity and
parity; ground/thermal Kubo versus symmetric source derivatives; generic
high-field coefficient; and the finite-k source power. Calculation uses
float64/complex128 with explicit tolerances, not interval certification.
`validate_manifest.py --root ...` accepts the final record with status
`completed`. Runtime is under one second. Each run was capped at 45 seconds
wall, 30 seconds process CPU and one conventional numerical-library thread,
with 131072 log bytes; no hard memory or affinity cap was requested.

Historical `run_001` is preserved as failed: its first illustrative
Gaussian trial subspace gave the wrong sign of the parity splitting; using
that signed J as a positive scale then produced invalid negative beta/bias
checks. A second exploratory parameter choice passed, and the third was
rescaled to admit the weak-NR illustration. `run_004` adds an independent
contact normalization audit and removes a tautological zero-branch test.
The code/contract evolved; only `run_004` is current evidence. Earlier
records should not be validated against the changed current inputs or
reported as unchanged-source reproductions. The first failure is not a
physical counterexample or an ignored passing tolerance.

## 9. Validity, normalization and the remaining obligation

The projection (4),(14) is exact **inside the specified Gaussian symmetric
subspace**. Calling it a controlled approximation to a selected continuum
state requires additional work: determine the actual isolated orbital
subspace of (3), its gap to omitted bound/scattering states; bound contact,
self-gravity and source-induced mixing outside it; check baryon internal
deformation, breakup/escape and a full physical material model. A usual
candidate hierarchy is

\[
 J,\ UN,\ |E|\,d_k\ll\Delta_{\rm orb},\ \Delta_b,
\quad |E|\,\|Q D_kP\|\ll\Delta_{\rm sep},                 \tag{28}
\]

with P the proposed orbital sector and Q its complement on the relevant
states/domains. Equation (28) is a condition, not a demonstrated estimate
for these Gaussian controls. Because `J` can be much smaller than an
orbital gap, a population crossover may in principle occur before orbital
distortion; that hierarchy must be established rather than inferred from
small overlap. The finite gravitational environment permits escape and
higher orbitals; a finite-dimensional hard population bound is not a hard
bound on continuum displacement or on arbitrary excitation.

For an independently specified host number density `n_h`, the weak-source
effective response would be `n_h chi_N` in a separated-host regime with its
actual source form factor and packing conditions. Already at N=1,
`chi=d_k²/J`; repulsion, N, temperature, finite recoil and geometry modify it.
The universal normalization would require

\[
                    4\pi G n_h\chi_N=1,                    \tag{29}
\]

which selects an inventory/profile relation. The scalar action and this
specified environment supply no such relation. A frequency or tunnelling
scale depending on gravity does not eliminate `n_h`, the source overlaps,
the contact and preparation factors. The physical internal source tends
to zero as `k²`; its susceptibility tends to zero as `k⁴` in this fixed
gapped control, while `1/(4piG)` does not.

The useful new result is the explicit nonlinear population mechanism and
its real manybody occupied-spectrum dictionary with recoil-preserved
source. The open target still needs a supported continuum state with a
controlled saturation window, a derived formation-selected population of
such states, and a source-preserving coarse graining that fixes both the
nonlinear law and its normalization. No universal exclusion of all other
original-action phases follows from this supported two-orbital case.
