# Effective viscous flux: a derivative-free Volterra identity and its exact limit

Base checkpoint: **X48-FLOOR-2026-11-01-B**. Observed shared HEAD:
`a7bade87f24f37a759b840f0ebb78b80a2d82aac`; the source hashes below, rather
than the moving shared HEAD, pin the operator. This route owns this file only.
The law, coefficients, initial data, and numerical records were not changed.

**Result.** The old viscosity has an especially simple exact constitutive
primitive. It removes the large spatial derivatives from a time-integrated
momentum identity. The memory stress can also be bounded in that identity
without estimating the heat operator, its derivatives, or the total variation
of a cell's temperature history. This is more than a formal effective-velocity
calculation. It yields the exact nonlinear Green-operator equation (12).
It does **not** prove the common central-quarter compression interval. The
remaining obstacle is recovery of an instantaneous divergence bound from this
smoothed equation; an explicit admissible-state construction below shows why
uniform amplitude bounds on its potentials cannot perform that recovery.
This construction is an obstruction to that inference, not a trajectory
counterexample to the specified startup problem.

## 1. Exact primitive, retaining the whole material law

Shift time so activation is at `s=0`. Use the normalized parameters in the
target. Write signed compression as `x_i=-theta_i`; the original heater uses
`C_i=(x_i)_+`. Set

\[
 \kappa(\rho)=\tfrac12\rho W(\rho)h(\rho),\qquad
 g(K)=\frac{K}{K+1/100},\qquad P=K\rho^2h.
\]

The exact stress, including signed memory damping, is

\[
 S=P+\kappa(x-2)_++\kappa g(K)x.                 \tag{1}
\]

The material polynomial has `W'=h` on every branch, including the joins.
Consequently the function

\[
 \boxed{\quad
 F(\rho)=\frac{W(\rho)^2-9/4}{4},\qquad
 F'(\rho)=\tfrac12Wh,\qquad \dot F=\kappa x
 \quad}                                                   \tag{2}
\]

is an exact primitive, not an asymptotic one. Here `F=0` for `rho<=1` and
`F>=0` globally. This identity uses only the exact continuity equation
`dot rho=rho*x`; it is valid during expansion as well as compression.

Put `E= kappa*(2-x)_+`. On every branch of (1),

\[
 S=(1+g)\dot F-2\kappa+P+E.                    \tag{3}
\]

In particular, `E=0` on `x>=2`. If `1<=rho<=2`, write `delta=rho-1`.
Since `W-3/2=delta^3-delta^4/2`, (2) gives the useful exact estimates

\[
 \frac38\delta^3\le F(\rho)\le\delta^3.
                                                               \tag{4}
\]

Thus the old-viscosity primitive starts at cubic order in the density
excess. This captures the coefficient variation in `kappa` exactly instead
of linearizing it around homogeneous dust.

## 2. Integrating momentum removes the spatial derivatives

Let `A_i=4*pi*r_i^2`, `m_i=i*dm`, with the actual nodal masses
`mu_i=dm` for `i<N` and `mu_N=dm/2`. The exact momentum equation is

\[
 \dot u_i=\frac{A_i}{\mu_i}(S_i-S_{i+1})
                         -\frac{Gm_i}{r_i^2},\qquad S_{N+1}=0.
\]

Define the cell-indexed tail potential and its nonnegative reaction by

\[
 J_i=\sum_{j=i}^N\frac{\mu_ju_j}{4\pi r_j^2},\qquad
 B_i=\sum_{j=i}^N\mu_j\left(
       \frac{Gm_j}{4\pi r_j^4}
                   +\frac{2u_j^2}{4\pi r_j^3}\right)\ge0.
\]

Differentiation and telescoping give, exactly,

\[
 \boxed{\quad \dot J_i=S_i-B_i,\qquad
 \int_0^sS_i(v)\,dv=J_i(s)-J_i(0)+\int_0^sB_i(v)\,dv.\quad}
                                                               \tag{5}
\]

There is no spatial derivative in (5), nor any derivative of `K`, `rho`, or
the moving conductance. The half exterior mass is retained. A localized
version replaces the tail sum by `j=i,...,j_*-1`; its stress is
`S_i-S_{j_*}`. Thus cutting off the exterior does not silently remove a
boundary term: it creates the explicit accumulated boundary stress
`integral S_{j_*}`.

The potential is also the exact inverse of the compression operator. Use
the operator from `startup_energy_route.md`,

\[
 a_i=A_i^2/\mu_i,\quad a_0=0,\qquad
 (\mathcal L_r f)_i=
 \frac{a_i(f_{i+1}-f_i)-a_{i-1}(f_i-f_{i-1})}{V_i},
 \qquad f_{N+1}=0.
\]

Because `J_i-J_{i+1}=mu_i*u_i/A_i` and `J_{N+1}=0`,

\[
 \mathcal L_rJ=x,\qquad
 J=-\mathcal G_rx,\qquad \mathcal G_r=(-\mathcal L_r)^{-1}.
                                                               \tag{6}
\]

The inverse exists and is positive on every valid finite grid. One direct
proof is summation by parts:
`sum V_i*f_i*(-L_r f)_i=sum a_i*(f_i-f_{i+1})^2`, with the center
coefficient zero and the exterior value zero. Its kernel is trivial, and
the elementary minimum principle gives positivity of the inverse.

## 3. Memory heat disappears from the integrated constitutive estimate

Here is a bound specific to the full stress, not to an old-viscosity model.
Suppose a particular cell obeys

\[
 2<c\le x_i(v)\le U\quad(0\le v\le s),\qquad \rho_i(0)=1.
                                                               \tag{7}
\]

Then `F_i` is nondecreasing. Integrate (3), using `E=0`, and define

\[
 M_i(s)=\int_0^s g(K_i(v))\,dF_i(v),\quad
 A_i^{\rm int}(s)=\int_0^s\kappa_i(v)\,dv,\quad
 P_i^{\rm int}(s)=\int_0^sP_i(v)\,dv.
\]

These are ordinary time integrals along each exact finite-dimensional
solution. In particular,

\[
 \int_0^sS_i=F_i(s)+M_i(s)-2A_i^{\rm int}(s)+P_i^{\rm int}(s),
 \quad
 0\le M_i(s)\le g_{*,i}(s)F_i(s),                         \tag{8}
\]

where `g_{*,i}=sup_{0<=v<=s}g(K_i(v))<=1`. Moreover,
`2*kappa<= (2/c)*dot F`, so

\[
 \boxed{\quad
 (1-2/c)F_i(s)\le\int_0^sS_i(v)\,dv
       \le(1+g_{*,i}(s))F_i(s)+P_i^{\rm int}(s).
 \quad}                                                   \tag{9}
\]

No bound on `dot K`, `H`, or a spatial difference occurs in this proof.
In particular, large or oscillatory heat fluxes do not invalidate (8)-(9).
Integrating `dot[(1+g)F]` first and then bounding `F*g'*H` pointwise would
lose this advantage.

For completeness, the existing prefix maximum argument makes the memory
and thermal corrections explicitly small under the same compression
bootstrap on a prefix. Let its maximum memory be `K_*(s)`. Outward heat
has no positive contribution at a prefix maximum. Therefore

\[
 K_*(s)\le\frac{a}{b}
 \left[\exp\left(bU^2e^{2UT}s^3\right)-1\right],\quad
 a=U(U/2-1),\ b=50U^2,\quad T\le\log(2)/U.             \tag{10}
\]

Indeed `rho<=exp(Us)`, `h<=3U^2*exp(2UT)*s^2`, and the exact two
heaters obey `Q<=h*(a+b*K)` at the prefix maximum. Setting

\[
 C_K=aU^2e^{2UT}\exp\left(bU^2e^{2UT}T^3\right)
\]

gives `K_*(s)<=C_K*s^3`. Hence, uniformly over that prefix and over `N`,

\[
 M_i(s)\le100C_Ks^3F_i(s),\qquad
 P_i^{\rm int}(s)\le\tfrac12U^2e^{4UT}C_Ks^6.         \tag{11}
\]

For the second estimate use `P=K*rho^2*h` and integrate `s^5`.
Equations (8)-(11) place the memory and thermal corrections at order `s^6`
in the integrated stress. The nonlinear old-viscosity primitive is order
`s^3`. This separation is exact under the stated bootstrap and does not
assume spatial regularity. It does not establish that bootstrap.

Combining (5), (6), and (8), on the branch `x>2`, yields the promised exact
nonlinear equation:

\[
 \boxed{\quad
 \mathcal G_{r(s)}x(s)+F(\rho(s))
 =\mathcal G_{r(0)}C_a\mathbf1
   +\int_0^sB(v)\,dv
   +2A^{\rm int}(s)-P^{\rm int}(s)-M(s),\qquad
 \dot\rho=\rho x.
 \quad}                                                   \tag{12}
\]

This absorbs old-viscosity coefficient variation into the exact increasing
function `F`; it introduces no commutator of `L_r` and a reference graph.
Away from the branch `x>2`, retain the additional term
`-integral E` on the right. Thus (12) is not predicated on a modified law.

## 4. Why a full local primitive still cannot eliminate heat

The tempting instantaneous primitive is `Y=(1+g(K))*F(rho)`. Its exact
derivative gives

\[
 S=\dot Y-2\kappa+P+E-Fg'(K)(Q+H).                \tag{13}
\]

There is a short algebraic impossibility statement behind this residual.
There is no local state function `Y(rho,K)` such that, for arbitrary
admissible instantaneous states on the active branch,

\[
 S=\dot Y+R(\rho,K)
\]

with `R` independent of `x` and `H`. Varying a neighboring heat state while
holding local `rho,K,x` fixed changes `H`, so the coefficient `Y_K` must
vanish. Matching the coefficient of `x` then requires
`rho*Y_rho=kappa(rho)*(1+g(K))`, which is incompatible with `Y_K=0`
where `kappa>0` and `g'!=0`. This only rules out this class of local
transformations; it does not rule out a coupled or nonlocal estimate.

The heat term in (13) has the exact weighted-flux form

\[
 dm\,Fg'H=a_i^H(L_{i-1}-L_i),\qquad a_i^H=F_i g'(K_i)/W_i.
\]

For a prefix `1,...,j`, its sum is

\[
 \sum_{i\le j}dm\,F_i g_i'H_i
 =\sum_{i<j}(a_{i+1}^H-a_i^H)L_i-a_j^HL_j.
\]

The outward sign `L_i>=0` does not determine the interior commutator:
`F/W` increases with density, while `g'` decreases with `K`. There is no
specified density ordering that gives a sign to their product differences.
The Stieltjes estimate (8) succeeds because it integrates this issue out;
it does not supply an instantaneous scalar maximum principle.

## 5. Exact bottleneck: the Green potential smooths divergence twice

Equation (12) is a nonlinear diffusion equation for density with a memory
potential when `x=dot(log rho)` is substituted. Its monotone function `F`
is promising. However, a uniform amplitude bound on the right side of
(12), or on its small corrections (11), cannot be inverted into a uniform
pointwise bound on `x`. The inverse Green map has mesh-dependent norm.

Here is an explicit verification at a fixed valid homogeneous geometry.
Fix `rho_*>1`, let `b=(1/(4*rho_*))^(1/3)` and
`r_i=b*(i/N)^(1/3)`. Thus `V_i=dm/rho_*`. Choose
`k=floor(N/8)` for `N>=32`, so `k>=4` lies strictly inside the target
quarter. Fix `D>0` and define a potential `Z` by

\[
 Z_k=\frac{D V_k}{a_k+a_{k-1}},\qquad Z_i=0\ (i\ne k).
\]

Then

\[
 (\mathcal L_rZ)_k=-D,\qquad
 (\mathcal L_rZ)_{k-1},(\mathcal L_rZ)_{k+1}>0,
 \qquad \|Z\|_\infty=O(N^{-2}).                    \tag{14}
\]

The last statement follows directly from

\[
 \frac{a_i}{V_i}=144b^4\rho_*N^2(i/N)^{4/3}\qquad(i<N),
\]

whose coefficient stays bounded above and below on these three cells.
Perturb a homogeneous compression `C_a` by
`delta x=L_r Z`, and choose the compatible nodal velocities through
`delta u_i=(A_i/mu_i)*(Z_i-Z_{i+1})`. Only nodes `k-1,k` change;
their changes are `O(N^-1)`. The density, `F`, and constant nonnegative
`K` are unchanged, while `delta J=Z` and the central compression drops by
the fixed amount `D`. For instance `D=C_a-4+eta` makes `x_k=4-eta`,
with `0<eta<1`. All these are valid instantaneous states with positive
compression. They are not the specified initial state or solutions starting
from it.

Thus even an `O(N^-2)` error in the derivative-free flux potential can hide
an order-one compression defect. Energy or potential-amplitude estimates
alone cannot close this route. The missing estimate must use the evolution
and its dissipation, to exclude states of the form (14) along the actual
startup trajectory. A mesh-uniform localized comparison or temporal
regularity theorem for the nonlinear Volterra equation (12) could do so.
Such a theorem must control instantaneous `dot(log rho)`; lower density
growth by itself is only an integrated compression statement.

This is a new form of the unresolved leaf, not an assumption of the old
remainder bound (NE). The exact growing coefficient has been absorbed into
`F`, and the full heat-memory stress has been bounded without spatial
derivatives. What remains is a nonlinear pointwise-in-time estimate for
(12), including its moving Green operator and physical boundary, rather
than a pointwise estimate on `L_r(delta S)`.

## 6. Verification and pinned inputs

All identities were derived from the pinned semidiscrete law. No external
theorem, trajectory integration, finite-grid extrapolation, altered stress,
or assumed regularity estimate is used. An exact SymPy expansion checked the
joining-polynomial primitive in (2). Exact rational shell data with symbolic
`pi` checked (5) and (6), including the center and the half exterior mass;
all residuals were identically zero. These checks verify algebra, not any
universal trajectory assertion. Algebraic self-review also checked the
sign in (5), the exterior half mass, (6), the full-branch correction `E`,
the Stieltjes bounds, the `s^6` thermal integral, and the construction (14).
A mathematical proofreading pass covered this new file, including notation,
indices, display delimiters, and the distinction between an admissible state
and the actual trajectory. No independent mathematical audit is claimed.

SHA-256 paths are relative to `stable_stress_search/`:

| Input | SHA-256 |
| --- | --- |
| `material.py` | `4b7c86c2d377151223f584cb31daf42a214fb5e7a0eb5a7cedf7443618dda390` |
| `collapse.py` | `14326419b85c7400923aee98f76562c85a46dcc59fa1cd8af3f8740f91b72baf` |
| `entropy_transport/convective_transport.py` | `ee8ac635b8edc91208f1fcc5765aa7e0999a3975f286dd5b52384f75dfe63e97` |
| `entropy_transport/transport.py` | `2d93b679135ca176a16327f094c114eb1e9dbc21ba4adc56c2e209d60f78ee8c` |
| `entropy_transport/README.md` | `8719a07f915902b829030d178636e27602f362c0f0b0e4e9e5d02039f575d2f6` |
| `entropy_transport/DERIVATION.md` | `e08312d0dc3be7f3f2d225ca938a7872ceec6d4c2532db2102f54c7a984910da` |
| `entropy_transport/floor_theorem/seed_route.md` | `752944eb3c0c7ff87007b5ca1c3f5a46bb768d8215645914ad6b211cebcd053d` |
| `entropy_transport/floor_theorem/startup_energy_route.md` | `06630aecae84c9b618e84c1ddded3f2025f7a89f7dca634bbbb05f50d0e2380b` |
| `entropy_transport/floor_theorem/STATUS.md` | `d05a94e8f701f0e1d5076dc9c3fbaf7468bb8b5822a493e64e275d867ae712f6` |

The requested common `T>0` with `C_i(t_a+s)>=4` for all
`i<=ceil(N/4)`, `N>=32`, is still unproved. None of the estimates above
changes that quantifier or certifies it from sampled solutions.
