# A mass and spectral-strength test for the scalar dipole dictionary

Date: 2026-10-19. Parent: CE-GRAV-2026-10-19 / CE-FM-087.
This is an independent derivation in the retained nonrelativistic Hamiltonian,
with an explicit finite regulator control. It supplies necessary conditions;
it does not identify a physical internal dipole in the original theory.

## 1. The operator whose strength is actually fixed

Write the retained positive-frequency branch as atomic field psi and source
field b, with kinetic masses m and M, and local conversion

    H_c = c3 integral (b^dagger psi^2 + psi^dagger^2 b).

For either branch sigma=+,-, the local conserved reference density is

    rho_Q = m sum_sigma (n_psi,sigma + 2 n_b,sigma).

This is the emergent positive inventory of the conservative NR truncation,
not the exact signed relativistic Noether density. Hard reactions outside
this truncation can violate it. All statements below concern its conserved
Hamiltonian. The kinetic masses are retained as m and M: setting M=2m here
would discard a known detuning correction.

For Fourier rho_Q,k, a local conversion has weights 2m-2m=0. Hence
[H_c,rho_Q,k]=0 pointwise. Local density contacts, detunings, and an ordinary
Newtonian density-density interaction also commute with this density. For
each canonical species s, direct differentiation of the kinetic operator gives

    [rho_-k,[T_s,rho_k]] = k^2 (w_s^2/m_s) N_s.

Thus, in a finite-volume, stationary ground state, define the symmetrized
positive spectral measure per volume

    S_rho(k,omega) = (1/(2V)) sum_{n!=0}
      (|<n|rho_k|0>|^2 + |<n|rho_-k|0>|^2)
      delta(omega-(E_n-E_0)).

The exact first moment in this Hamiltonian is

    integral_0^infinity omega S_rho d omega = (k^2/2) rho_I,
    rho_I = sum_sigma [m n_psi,sigma + (4m^2/M) n_b,sigma].       (1)

The derivation does not require a condensate or weak density interactions.
It does require continuum quadratic dispersion, canonical local commutators,
a well-defined operator domain and a finite first moment in the ground state.
An arbitrary finite UV regulator changes the kinetic identity; the lattice
control below uses its actual hopping sum rule rather than asserting (1)
at finite spacing. Any continuum limit needs its own matching/domain control.
For a finite self-gravitating object the response is a matrix in positions
or modes; a translation-invariant scalar S(k,omega) is then not assumed.
Equation (1)'s double commutator can still be evaluated without replacing
that matrix by an artificial homogeneous medium.

The difference from reference mass is explicit:

    rho_Q-rho_I = sum_sigma [2m (M-2m)/M] n_b,sigma.

For daughter-only matter rho_I=rho_Q. In a molecule-dominated gas its
relative difference is (M-2m)/M, about 1.9994e-4 for u_star=0.02.
These are kinematic inventory statements, not bounds on all stress corrections.

### Why bare rest mass is not an interchangeable source

For rho_R=m n_psi+M n_b and delta=M-2m, the same calculation gives

    [rho_R,-k,[H_c,rho_R,k]] = -delta^2 H_c.                   (2)

Its first moment has a k-independent reactive contribution even at k=0.
The operator integral rho_R is not conserved under conversion. The full
relativistic gravitational source is stress-energy, including kinetic,
interaction and conversion energy. In particular, total energy at k=0 is
H and [H,H]=0. Equation (2) is evidence against replacing that source by
bare rest masses in a cancellation-sensitive calculation. Equations (1)-(2)
are not asserted as relativistic stress-energy sum rules. Derivative matching
corrections to the NR action likewise have to be included at their claimed order.

## 2. The normalization becomes a precise moment condition

For k>0 define the longitudinal displacement operator Pi_L=i rho_Q,k/k,
up to the Fourier sign convention, so delta rho_Q=-div Pi. Its measure
S_Pi=S_rho/k^2 obeys

    M_1 := integral omega S_Pi d omega = rho_I/2.

A static external force coupled as -E Pi has positive ground-state
susceptibility

    chi_Pi(0,k)=2 integral S_Pi/omega d omega = 2 M_-1.        (3)

An internal zero mode needs separate treatment; if the inverse moment
diverges then no finite static susceptibility follows. The target
chi_Pi=1/K, K=4piG, would require

    Omega_eff^2 := M_1/M_-1 = K rho_I.                       (4)

This is the harmonic mean of squared excitation frequencies, weighted by
their first-moment strengths. It is a testable Jeans-frequency condition,
not a prediction that all microscopic frequencies are equal. If only a
subset of modes is proposed as the dipoles, its M_1 is at most rho_I/2;
using the full rho_I in (4) additionally assumes exhaustion of the sum rule.

For a one-pole daughter fluid, Omega_eff^2=cs^2 k^2+k^4/(4m^2) before
gravitational feedback. It tends to zero, rather than K rho_I. Self-gravity
can generate frequencies proportional to G rho in actual finite bound
objects, as the other lanes demonstrate. Their source overlap and mode
strength, rather than dimensional scaling alone, decide (3).

The response in (3) is to the source term specified in its Hamiltonian.
For a material constitutive kernel the macroscopic Newtonian field must
not also be integrated out as an additional interaction and then counted
again. Internal binding gravity in a resolved object and macroscopic
field feedback require an explicit separation of scales.

With Newtonian potential U and g=-grad U, an ordinary displacement xi has
Pi=rho_0 xi, delta rho=-div Pi and source energy -g.Pi. If instead one uses
the density-dual variable P=-Pi, then delta rho=div P and the source energy
is +g.P. Equality of response magnitudes is not a license to reverse that
source sign. Pi_L defined from a Fourier density is also nonlocal; the
sum rule does not turn it into a local internal dipole.

For finite temperature, Kubo weights are population differences, or
(1-exp(-beta omega)) times the unsymmetrized structure factor. Raw occupied
emission counts cannot be inserted into (3). For a nonstationary produced
state, even positive-frequency spectral passivity is not automatic.

## 3. A dynamical constraint on the rational gap construction

Consider the previously constructed independent two-level sites, now with
an arbitrary positive dipole matrix element d(Delta), actual spacing

    H_Delta = d [Delta 1 + Delta sigma_x - E sigma_z],
    Omega(Delta)=2d(Delta) Delta.

Let n(Delta) be the number density of sites per dDelta and
w(Delta)=n(Delta)d(Delta). For all sites in their zero-field ground state,
the dipole operator d sigma_z has off-diagonal matrix element d. Therefore

    S_site(omega) = integral w(Delta)d(Delta)
                        delta(omega-2d(Delta)Delta) dDelta,
    chi_site = integral w(Delta)/Delta dDelta,
    M_1,site = 2 integral w(Delta) d(Delta)^2 Delta dDelta.    (5)

The static response fixes w, not d or the actual frequency distribution:

    w_target = p_sat a Delta/(a^2+Delta^2)^(3/2),
    chi_site = p_sat/a.

If these sites exhaust the longitudinal reference-mass response, equations
(1) and (5) require the additional matching condition

    4 integral w_target d(Delta)^2 Delta dDelta = rho_I,       (6)
    p_sat/a = 1/(4piG).

The second equation alone is no microscopic normalization. If unmodeled
levels carry strength, the left side of (6) is an upper-bounded subset;
their own inverse moment must be counted before claiming the full target.

### Constant dipoles fail a finite oscillator-strength budget

For fixed d=d0, a cutoff L gives

    integral_0^L Delta w_target dDelta
      = p_sat a [asinh(L/a)-L/sqrt(a^2+L^2)].                 (7)

It diverges logarithmically. Consequently the exact unbounded target
with constant d has M_1=+infinity and cannot exhaust a finite-density
conserved reference-mass response. This does not forbid a finite cutoff
approximation on a stated finite force range.

### A real loophole: variable dipoles

Do not generalize the constant-d result to all spectra. Taking
d=d0(Delta/a)^(-alpha), the UV first moment converges for alpha>0,
and the site number integral integral w/d converges for alpha<1.
The IR first moment converges for alpha<3/2, while site number converges
for alpha>-2. Thus every 0<alpha<1 passes both elementary integrability
tests. The illustrative alpha=1/3 choice has Omega proportional to
Delta^(2/3). With d0 chosen so 4d0^3 a=m, each site obeys
2 Omega d^2=m; a one-particle coordinate sum-rule budget is then compatible
with (6) after counting the corresponding particles. This is only an
algebraically compatible family. No original scalar bound state, actual
dipole operator, site occupation or saturation has been obtained from it.
In particular d diverges at soft gaps in this family, leaving localization
unproved; exact finite two-level canonical coordinates are not implied.
For self-gravitating internal coordinates the physical gravitational
source still has the center-of-mass and source-overlap constraints.

Finally, if the sites are identified with *actually excited* emitted
particles of energy Omega, their occupied excitation energy density is

    integral n(Delta) Omega(Delta) dDelta
      = 2 integral Delta w(Delta) dDelta.                    (8)

The same logarithm now diverges regardless of d. This is a conditional
finite-production-energy obstruction to that identification, also found
independently in the occupied-spectrum lane. An unoccupied high-gap site's
ground state does not cost its excitation gap, so (8) does not exclude all
possible ground-state polarizable media. A proof must specify which state
and which of these two interpretations is intended.

## 4. Verification and limits

`check_sum_rules.py` uses complete periodic four-site Q=2 and Q=4 sectors
(dimensions 14 and 85), local source conversion, diagonal contacts and
kinetic masses M=2.002 and 2.03. It checks 24 full-matrix double-commutator
identities, 24 independent eigenbasis first-moment evaluations, eight
zero-mode controls, and seven integral controls. Largest operator residual
was 1.84e-15. Lattice kinetic weights retain 2(1-cos k); the continuum k^2
identity is derived above, rather than substituted into the lattice test.
Bare-rest and reference densities give different k=0 moments as predicted.

`run_001` completed with 45-second wall, 30-second CPU and one-thread caps.
An earlier launch was rejected before execution because the contract lacked
the required mathematics.inputs field; the contract was corrected before
the fresh run directory existed. No result was overwritten.

For convention comparison only: [Hu et al., arXiv:1001.0772v2](https://arxiv.org/pdf/1001.0772v2)
distinguish structure-factor and response weights in Eqs. (2)-(3) and
energy-weighted versus inverse moments in their sum-rule discussion.
Their number-normalized S must be multiplied by number density and by
mass squared for the one-species mass convention here. Equations (1)-(8)
were derived explicitly for this packet; the paper is not a source for
the Phi/X conversion correction or the rational-spectrum conclusion.

The missing implication is now sharper: produce a source-preserving joint
distribution of actual d, Omega, and state populations which satisfies
both the static inverse moment and the finite dynamical mass budget,
while respecting the physical gravity operator and the desired locality.
