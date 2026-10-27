# A shared scalar–baryon constrained ground state

Base: CE-SCALAR-DIPOLES-2026-10-19 / CE-FM-090. Initial observed HEAD:
`3ac0427149a2108afa8f102df4d82da33b9060c4`. Author write scope is this
`equilibrium/` directory only. Exact antecedent and output byte pins are in
`ARTIFACTS.json`; concurrent HEAD changes do not replace those pins.

**Achieved result.** In the original theory's matched, dilute daughter GP
sector, supplemented by a declared nonrelativistic degenerate baryon EOS,
there is an actual shared, isolated spherical ground state at every fixed
positive pair of species masses. It minimizes the *full* coupled Newtonian
energy against arbitrary admissible three-dimensional perturbations at those
masses. This is constrained energetic stability, including live baryons and
the scalar quantum gradient; it is stronger than a frozen-host spring or a
homology test. It is not an unconditional nonlinear orbital-stability theorem
for a global GP–Euler flow. The EOS, inventories and state preparation remain
environmental inputs. Nothing here selects their values from the scalar action.

## 1. Exact state and effective-theory contract

The canonical scalar theory has charge-one Phi, mass m; charge-two X, mass
M>2m; conversion g(X*Phi^2+c.c.); and

\[
 \lambda_{\rm tot}=\lambda_{\rm rep}+{g^2\over M^2-4m^2},\qquad
 \lambda_{\rm rep}>0.
\]

Use its already matched daughter contact
\(g_2=\lambda_{\rm rep}/(2m^2)\), not a new interaction. With mass-normalized
scalar amplitude \(f=\sqrt{\rho_d}\), define

\[
 \tau={\hbar^2\over2m^2},\qquad
 K={g_2\over2m^2}>0,
 \quad K={\lambda_{\rm rep}\over4m^4}\quad(\hbar=c=1).
 \tag{1}
\]

This lane uses a zero-temperature, locally isotropic, ideal degenerate
fermionic baryon fluid of constituent mass m_b and spin degeneracy g_b.
Counting occupied momenta gives

\[
 n_b={g_b p_F^3\over6\pi^2\hbar^3},\qquad
 P_b={g_b p_F^5\over30\pi^2\hbar^3m_b}
     =K_b\rho_b^{5/3},
\quad
 K_b={\hbar^2\over5m_b^{8/3}}
          \left({6\pi^2\over g_b}\right)^{2/3}>0.
 \tag{2}
\]

Here rho_b=m_b n_b. A different composition, entropy or constituent changes
this EOS. The fluid closure assumes local isotropic stress and adiabatic
perturbations preserving this barotrope. A collisionless waterbag requires its
own phase-space Casimirs and dynamics; it is not silently identified with this
fluid. Baryon masses, g_b, the validity of this material model and zero entropy
are declared state inputs. No scalar–baryon force beyond ordinary gravity is
introduced. Chemical conversion between the scalar and baryon fluids is absent.

Fix the *two* positive reference masses
\(\mathcal M_d=\int\rho_d\) and \(\mathcal M_b=\int\rho_b\).
The admissible rest-state energy is

\[
 \begin{split}
 E[\rho_d,\rho_b]&=T+S+B+W,\\
 T&=\tau\int|\nabla\sqrt{\rho_d}|^2,\quad
 S=K\int\rho_d^2,\quad
 B={3\over2}K_b\int\rho_b^{5/3},\\
 W&=-{G\over2}D(\rho,\rho),\quad
 D(a,b)=\iint{a(x)b(y)\over|x-y|}\,dx\,dy,\quad
 \rho=\rho_d+\rho_b.
 \end{split}
 \tag{3}
\]

The domain is nonnegative \(\rho_d\in L^1\cap L^2\),
\(\sqrt{\rho_d}\in H^1(\mathbb R^3)\), and
\(\rho_b\in L^1\cap L^{5/3}\), with the specified masses. The scalar phase
and baryon velocity add positive terms
\(\tau\int\rho_d|\nabla\vartheta|^2\) and
\(\tfrac12\int\rho_b|v_b|^2\). The minimum can therefore have constant phase
and zero baryon velocity. The Poisson energy (3) counts all self and mutual
gravity exactly once; no independent host spring is added to it.

This is the weak-field, low-energy, daughter-dominated projection of the
original action. Physical applications must also satisfy source-elimination,
diluteness, small binding/contact energy per particle, p_F << m_b c, small
compactness, and the barotropic fluid's material assumptions. The theorem
below is about (3); it does not assert all mathematical masses remain within
the original action's NR regime. Masses and central density can be chosen in
the weak-binding regime; their actual selection and production are not proved.

## 2. Full constrained minimum: boundedness and construction

**Proposition.** For fixed positive tau,K,K_b,G,M_d,M_b, the infimum of (3)
over this domain is finite and attained. At least one minimizer has both
densities spherically symmetric and nonincreasing about the same center.
It is a global minimum over the full three-dimensional domain, not merely the
radial domain. The same existence argument also applies to the TF functional
tau=0, with the scalar H1 requirement omitted.

The proof uses the following three ingredients. The only imported geometric
inequalities are symmetric-decreasing rearrangement for the Newton kernel
and the Pólya–Szegő inequality. Their precise source and hypotheses are checked
in `SOURCE_CHECKS.md`. No imported multi-fluid stability theorem is used.

### 2.1 Coercivity at fixed masses

Put M=M_d+M_b and p=5/3. A direct split of the Newton potential at radius R
and Hölder's inequality give

\[
 \sup_x\int{\rho(y)\over|x-y|}\,dy
 \le C\|\rho\|_{5/3}R^{1/5}+{M\over R}.
\]

Choose \(R=(M/\|\rho\|_{5/3})^{5/6}\), changing only an absolute constant.
Consequently

\[
 D(\rho,\rho)\le C M^{7/6}\|\rho\|_{5/3}^{5/6}
 = C M^{7/6}\left(\int\rho^{5/3}\right)^{1/2}.
 \tag{4}
\]

The scalar contribution satisfies
\(\int\rho_d^{5/3}\le M_d^{1/3}(\int\rho_d^2)^{2/3}\).
Writing \(A=\int\rho_d^2\), \(C_b=\int\rho_b^{5/3}\), we have

\[
 E\ge T+KA+{3\over2}K_b C_b
       -C(M_d,M_b,G)(A^{1/3}+C_b^{1/2}).
 \tag{5}
\]

Thus E is bounded below, and every minimizing sequence has bounded T,A,C_b.
The split proof avoids depending on a sharp HLS constant or its equality case.

### 2.2 A centered weak limit and continuity of the gravitational energy

Replace both densities in a minimizing sequence by their centered symmetric
decreasing rearrangements. Species masses and internal integrals are preserved;
T decreases, and D increases, including the mutual term. This produces a
radial minimizing sequence for the *unrestricted* infimum.

Take weak L2 and L5/3 limits, respectively. They are nonnegative radial
nonincreasing densities with masses at most M_d,M_b. The internal terms are
weakly lower semicontinuous. For the scalar gradient term one can use the
convex representation

\[
 \int|\nabla\sqrt a|^2
 =\sup_{z\in C_c^\infty(\mathbb R^3;\mathbb R^3)}
       \int a(-\nabla\cdot z-|z|^2).
 \tag{6}
\]

For smooth positive a this follows by completing the square, with the
optimizing field z=grad(a)/(2a). Smooth positive approximation and cutoffs
give its lower-semicontinuous extension; finiteness is equivalent to
sqrt(a) in H1 when a is integrable. This proves the needed lower
semicontinuity directly in the density topology. Equivalently, use weak H1
compactness of sqrt(a) and local strong L2 compactness.

For clarity, D is actually continuous along this radial sequence. By Newton's
shell formula, for every radial density of mass at most M,

\[
 V(r)=\int{\rho(y)\over|x-y|}\,dy\le {M\over r},\qquad r=|x|>0.
\]

The contribution to D with at least one point outside radius R is at most
\(2M^2/R\), uniformly. On a bounded ball, omit the region |x-y|<epsilon.
Its contribution is at most
\(C M\|\rho\|_{5/3}\epsilon^{1/5}\), by the same Hölder estimate as (4).
The remaining smooth bounded kernel on a compact product is uniformly
approximable by finite sums of products of continuous test functions. Local
weak measure convergence therefore implies convergence of its double integral.
Let epsilon tend to zero and R tend to infinity. This proves D_j -> D_* and

\[
 E_*\le\liminf_j E_j=I(M_d,M_b).
 \tag{7}
\]

The only possible failure of the mass constraints at this stage is escape
to infinity. It is excluded next without assuming strict convexity or a
one-component compactness theorem.

### 2.3 Missing mass cannot escape

Suppose the limit loses species masses delta_d>=0,delta_b>=0 with
delta=delta_d+delta_b>0. Pick a nonzero smooth radial q supported in
1<|x|<2, and normalize eta=q^2/(int q^2). Define
\(\eta_R(x)=R^{-3}\eta(x/R)\), and add precisely the missing masses:

\[
 \widetilde\rho_d=\rho_{d,*}+\delta_d\eta_R,\qquad
 \widetilde\rho_b=\rho_{b,*}+\delta_b\eta_R.
 \tag{8}
\]

These are admissible at the full requested masses. Since the core is radial
nonincreasing, \(\rho_{i,*}(r)\le3M_i/(4\pi r^3)\). On the added annulus,
the scalar contact-energy increase is O(R^-3). The baryon internal increase
is O(R^-2), using
\((a+b)^{5/3}-a^{5/3}\le C(a^{2/3}b+b^{5/3})\).
Fisher information is subadditive:

\[
 { |\nabla(a+b)|^2\over a+b}
 \le { |\nabla a|^2\over a}+{ |\nabla b|^2\over b}.
\]

Hence the quantum-energy increase is at most
\(\tau\delta_d R^{-2}\int|\nabla\sqrt\eta|^2\). Cross gravity with the core
is nonpositive. The self-gravity of the added mass alone gives

\[
 E[\widetilde\rho_d,\widetilde\rho_b]-E_*
 \le O(R^{-2})+O(R^{-3})
       -{G\delta^2\over2R}D(\eta,\eta)<0
 \tag{9}
\]

for sufficiently large R. This also works if the weak limit is identically
zero. But (7) and admissibility imply
\(I\le E[\widetilde\rho_d,\widetilde\rho_b]<E_*\le I\), a contradiction.
Both masses are retained and (7) is equality. The proposition follows.

This argument resolves a real issue absent from a finite-box variational
ansatz: neither species can lower the infimum by evaporating its remaining
inventory at infinite radius. It does not select the fixed inventories.

## 3. Equilibrium equations and precise stability conclusion

The minimizing densities obey, with separate mass multipliers mu_d,mu_b,

\[
 \begin{split}
 -\tau\nabla^2 f+(2Kf^2+U)f&=\mu_d f,\\
 \rho_b&=\left[{2(\mu_b-U)\over5K_b}\right]_+^{3/2},\\
 \nabla^2U&=4\pi G(f^2+\rho_b),\qquad U(\infty)=0.
 \end{split}
 \tag{10}
\]

The nonnegative scalar ground amplitude can be taken positive everywhere by
the elliptic strong maximum principle. The baryon density has a nonempty core
because its mass is positive. The two species therefore truly overlap in one
self-consistent potential. Baryon integrability forces mu_b<0: mu_b>0 would
give an asymptotically nonzero density, while mu_b=0 with
U~-GM/r would give rho_b~r^-3/2 and infinite mass. Its free surface is
U(R_b)=mu_b. The finite-GP scalar has a smooth tail; it does not share a sharp
cutoff with the baryons. The numerical examples have mu_d<0 and exponentially
small outer scalar tails. Separate chemical potentials are required at fixed
separate masses, even though gravity is shared.

For regular density variations a=delta rho_d,b=delta rho_b, the full density
Hessian is

\[
 \begin{split}
 \delta^2E={\tau\over2}\int\rho_d
         \left|\nabla{a\over\rho_d}\right|^2
       +2K\int a^2
       +{5\over3}K_b\int\rho_b^{-1/3}b^2
       -G D(a+b,a+b).
 \end{split}
 \tag{11}
\]

The baryon term is evaluated where rho_b>0, with admissible one-sided
variations at the surface. At the minimizer (11) is nonnegative for every
admissible mass-preserving direction, int a=int b=0. Scalar phase and baryon
velocity variations add nonnegative kinetic quadratic forms. This is a full
constrained-energy result, not a radial test. Translations of the whole
configuration and the global scalar phase remain exact zero directions.

The exact statement of stability is:

* No finite admissible perturbation at the fixed masses has lower energy.
* No allowed negative constrained Hessian direction exists at this minimum.
* For a well-defined Hamiltonian linearization JL on the constrained tangent
  space, with self-adjoint L>=0 and skew-adjoint J, there is no finite-energy
  eigenmode with Re(lambda)>0 in the relevant operator domains. Indeed
  Re(lambda)<z,Lz>=0; positivity then forces Lz=0 for such an eigenmode,
  contradicting JLz=lambda z. This is a conditional spectral statement, not a
  construction of all operator domains or the continuous spectrum.
* For a smooth mass- and energy-conserving GP–Euler evolution, energy excess
  above the minimum is conserved. A theorem converting this to closeness to
  a unique orbit requires coercivity/compactness in the chosen phase-space
  norm and suitable flow existence. Those dynamical assertions are not proved
  here. Ideal Euler flow can require a separate treatment after shocks.

Neither a strictly positive l=1 gap nor a universal internal mode count follows
from existence of the minimum. Common translations necessarily stay gapless.

Under the mass-preserving dilation rho_i(x)->s^3 rho_i(sx),

\[
 E(s)=s^2(T+B)+s^3S+sW,\quad
 2(T+B)+3S+W=0,\quad
 E''(1)=2(T+B)+6S>0.
 \tag{12}
\]

This virial/homology relation is a useful independent check. By itself it would
be insufficient to establish the full stability result; that result comes
from the global minimization proof.

## 4. Common-cutoff mixed Lane–Emden comparison

In the TF reduction tau=0, (10) becomes
\(2K\rho_d+U=\mu_d\) and
\((5/2)K_b\rho_b^{2/3}+U=\mu_b\). A common compact support boundary requires
mu_d=mu_b=mu. This is an additional relation among state data; it is not
automatic at fixed separate masses. Put h=mu-U, h(0)=h_c>0, and

\[
 \rho_{d,c}={h_c\over2K},\quad
 \rho_{b,c}=\left({2h_c\over5K_b}\right)^{3/2},\quad
 \eta={\rho_{b,c}\over\rho_{d,c}},\quad
 a^2={K\over2\pi G},\quad r=ax,\quad h=h_c\theta.
\]

The shared solution is the single scalar ODE

\[
 \theta''+{2\over x}\theta'=-\theta-\eta\theta^{3/2},\qquad
 \theta(0)=1,\quad\theta'(0)=0,
 \tag{13}
\]

up to its first zero x1; set both densities to zero outside R=ax1 and match
to U=-G(M_d+M_b)/r. In the interior,
\(\rho_d=\rho_{d,c}\theta\),
\(\rho_b=\rho_{b,c}\theta^{3/2}\). Its masses are

\[
 M_d=4\pi a^3\rho_{d,c}\int_0^{x_1}x^2\theta dx,\quad
 M_b=4\pi a^3\rho_{d,c}\eta\int_0^{x_1}x^2\theta^{3/2}dx,
\quad
 \mu=-{G(M_d+M_b)\over R}.
 \tag{14}
\]

The first zero is finite and x1<=pi. For eta=0, theta=sin(x)/x. For eta>0,
comparison with this n=1 solution, or the Wronskian integrated on (0,pi),
forces x1<pi. These are exact stationary TF equilibria. Equations (13)-(14)
alone do not prove that every central-parameter member is the global minimum
at its resulting two masses. The general existence proof supplies a full
TF minimum at each mass pair, potentially with unequal cutoffs. A claim that
one particular common-cutoff ODE member is that minimum needs an additional
uniqueness or stability argument and is not substituted for the proof in §2.

For fixed microscopic K and declared K_b, eta is proportional to sqrt(h_c),
so (13) is a one-parameter common-cutoff subfamily of the two-mass problem.
The action fixes K; the baryon EOS and h_c are additional data. At finite tau,
equal chemical potentials do not restore equal compact supports because the
scalar quantum tail remains. Literal TF scalar edges have divergent kinetic
energy, so they must never be inserted into (3) as finite-GP trial states
without smoothing.

A further safe continuation statement follows variationally. At fixed masses,
the minimum energies I_tau tend to I_0 as tau decreases to zero: I_tau>=I_0,
and smooth mass-preserving approximations to a TF minimizer give limsup<=I_0.
Centered minimizers are weakly compact, and the same shell argument excludes
mass loss for any tau_j->0. Their subsequential limits are TF minimizers;
convergence of the positive internal-energy norms gives strong L2 scalar and
L5/3 baryon density convergence, while tau_j I(rho_d,j)->0. This establishes
convergence to the *set of TF minima*, without identifying that set with an
arbitrary common-cutoff member or giving a boundary-layer error rate, a mode
gap, a Love number, or formation dynamics.

## 5. Explicit bounded stationary controls

`check_equilibrium.py` solves four TF ODEs and six full coupled stationary
BVPs. The full-GP controls and eta=1 TF seed use units
4piG=1,K=1/2,K_b=2/5, so the two specific enthalpies are rho_d and
rho_b^(2/3). The other TF eta values test (13) as a dimensionless ODE family;
at fixed h_c=1 they correspond to different K_b, while eta=0 is the pure
scalar limit. Reported radial masses N_i=int r^2 rho_i dr omit a common 4pi.
The eta=1,h_c=1 TF profile gives

\[
 x_1=2.36924317416,\quad N_d=1.26043509806,\quad
 N_b=0.841802494120,\quad\mu=-0.887303428838.
\]

Hold these two masses fixed in the full-GP problem. The scalar and baryon
chemical potentials split, as they must for independent constraints. Fine
box results (L=14,tolerance=2e-7) are:

| tau | mu_d | mu_b | baryon R_b | scalar rms | baryon rms |
|---:|---:|---:|---:|---:|---:|
| 0.2 | -0.735073833 | -0.789236986 | 2.630070773 | 1.966827634 | 1.483209837 |
| 0.05 | -0.841924998 | -0.857254068 | 2.444647154 | 1.613739132 | 1.377993309 |
| 0.0125 | -0.874420073 | -0.878436172 | 2.391242834 | 1.513113744 | 1.350401787 |

The actual benchmark tau is fixed once m and the dimensional mass/enthalpy
units are chosen; it is not a tunable extra force. These values test a
dimensionless family and do not claim to be the original 1 MeV scalar's
particular physical parameter point. Full numerical density and potential
arrays are in `run_002/profiles.json`.

The largest relative mass discrepancy over all six BVPs is 6.59e-8, and the
largest relative virial discrepancy is 1.73e-8. The L=10 versus L=14 energy
differences are below 2.7e-8 relative, with matched refinement of tolerance.
The pure n=1 TF radius differs from pi by 1.16e-12; its integrated mass differs
from pi by 9.91e-10. The solver's reported residual, boundary conditions,
independent integral masses and virial relation are all checked. The largest
fine-box reported RMS ODE residual is 1.97e-7. Floating residuals are not
interval certificates. No Hessian spectrum or global optimality of these
particular stationary BVP outputs is claimed; global continuum minimum
existence and nonnegative constrained Hessian are established separately
in §§2-3.

For the tau=.05 fine profile, an independently meaningful *restricted* rigid
relative translation has

\[
 \kappa={4\pi G\over3}\int\rho_d\rho_b\,d^3x,\qquad
 \omega_{\rm rigid}^2={\kappa\over\mu_I}=0.267624596189,
\quad
 \mu_I={M_dM_b\over M_d+M_b}.
 \tag{15}
\]

This positive curvature checks live overlap. It is not identified with an
eigenfrequency of the coupled shape-changing fluid/GP problem. That problem
must retain the full Hessian (11), inertia, free surface and scalar tail. In
particular, it cannot add (15) to gravity a second time.

## 6. What the construction does and does not provide

The resulting equilibrium supplies a consistent shared density, pressure,
potential, sizes and variational fluctuation operator for specified state
data. Unlike independent copied baryon hosts, it counts the shared baryon
inventory and Poisson binding once. Its finite masses and outer boundary
remove the homogeneous medium's unsupported Jeans background assumption.

It does not supply occupied local dipoles. The uniform gravitational source
still couples only to the COM; translating the whole configuration costs no
energy, and the full relative source includes recoil. A normal-mode spectrum
must be computed from this state, and occupations require a temperature,
distribution or production preparation beyond its ground density. A positive
relative trial curvature does not select an occupied gap distribution. Its
size, chemical potentials and the scale of (15) retain mass/EOS dependence.
The original scalar action has not chosen M_d,M_b,K_b, an abundance, or an
acceleration scale. No saturation law or p_sat/a=1/(4piG) follows from this
minimum alone.

The strongest safe next step is to take a specified minimizing state (or a
numerically controlled stationary candidate with separately checked Hessian),
solve its coupled source-preserving l=1 spectrum, and calculate source matrix
elements and state-specific occupation weights. An exact translational zero
and recoil must remain in that calculation. Nonlinear finite-displacement
binding/escape and any saturation then follow from the same one-copy energy.

## 7. Evidence status

* Full constrained-minimum existence: analytic proof in §2, with the two
  rearrangement inputs source-checked. Present review status: author self-review;
  any independent review must be attached separately.
* Energetic and Hessian stability: consequence of that exact constrained
  minimum; dynamical spectral statement conditional on the stated Hamiltonian
  domains; nonlinear orbital stability/uniqueness not proved.
* Mixed TF and full-GP example profiles: finite numerical assertion verified
  over the explicit cases in the contract, conditional on floating tolerance.
  The BVPs are stationary controls, not certified minimizers.
* TF minimum-set convergence: variational argument above; no surface/mode
  convergence rate and no identification with an arbitrary ODE branch member.
* Original physical prediction target: open. This packet resolves a stable
  shared-state *construction* within a declared EOS/EFT, not the occupation,
  saturation, source normalization or environmental selection obligations.
