# Independent final audit: from controlled layers to corner matching

**Primary verdict: correct only after the explicit outer-convergence
restriction below.** The canonical/Hilbert identity and Einstein matching
bridge are valid. In the intersection of the reviewed layer hypotheses,
with a full on-shell approximation and no unidentified bulk stress/current
defect, they exclude a thin-layer connection between distinct same-sign
positive-charge endpoints in the PF02 convexity range. This is a restricted
nonexistence statement about that approximation class, not a formation
theorem or an exclusion of all singular continuations.

## 1. Direct normal-stress identity

Use the diagonal base metric -N^2 dt^2+L^2 dx^2 and transverse area factor
exp(2beta). Set

    a=phi_t, b=phi_x, r^2=a^2/N^2-b^2/L^2,
    T=P_t+2P beta_t, ell=P_x+2P beta_x,
    D=(-bT+a ell)/(NLr), E=NL exp(2beta).

Here Lm=E F(D,r^2/2,P,phi). Its L dependence is precisely the volume
factor and the physical normal covectors b/L, ell/L, with a/N,T/N fixed.
Therefore, on either switch branch (and at its C1 boundary),

    L partial_L Lm=Lm-b partial_b Lm-ell partial_ell Lm.

The normal matter Hamiltonian in the original first-order representation
is

    Hx_m=b pi_phi^x+P_x pi_P^x+beta_x(pi_beta^x)_matter-Lm
        =b partial_b Lm+ell partial_ell Lm-Lm,

because (pi_beta^x)_matter=2P pi_P^x. Thus

    Hx_m=-L partial_L Lm.

With the Hilbert convention delta Sm=(1/2)integral E T^{mu nu}
delta g_mu nu, varying g_xx=L^2 gives

    L partial_L Lm=E T^x_x,
    Hx_m=-E T^x_x.

The sign is negative. No assertion that arbitrary canonical and Hilbert
stress tensors coincide is used. Tangential T may be nonzero; the identity
does not assume stationary profiles.

If P is represented by its proper amplitude after eliminating n.P=0,
equivalence to the fundamental covariant Hilbert variation is on shell
of the native polarization/constraint equations. It follows from the
chain rule for the metric-dependent field redefinition; equation-of-motion
terms must not be discarded off shell. The argument applies to smooth
on-shell approximants and to their regular outer limits. It does not
assign a stress to an undefined singular field redefinition directly.

The author's `pf07/auxiliary001/result.json` reports the corresponding
exact symbolic identity among nine passing checks. This audit independently
derived it by homogeneity; the symbolic result is supporting algebra, not
proof of the limiting assumptions.

## 2. What must converge

Assume a family of smooth solutions of the full coupled native equations,
including scalar, polarization and all Einstein equations, on a shrinking
neighborhood of a regular timelike interface. Require the quantitative
clock, cap, characteristic, anchored-A, strong endpoint, and current-
measure assumptions established in AUXILIARY_STRESS.md and
POLARIZATION_MEASURE.md. In addition require:

* Locally uniform metric convergence to a continuous nondegenerate metric,
  uniform bounds on its first derivatives, and regular one-sided first
  derivative traces. Induced tangential derivatives have a common regular
  trace. Use a common-oriented normal and a fixed/adapted timelike chart.
* The limiting bulk matter stress is the native Hilbert stress evaluated
  on the stated regular outer solutions, with the corresponding statement
  for bulk currents. Strong enough convergence away from the layer is a
  sufficient formulation. For example require strong convergence of all
  algebraic stress variables r,A,P,mu and frame gradients on compact outer
  subsets, and the necessary regular trace limits. Merely weak convergence
  of fields is not sufficient to identify nonlinear stress.
* The layer estimate gives vanishing **absolute** stress integral, not
  just cancellation of signed components. AUXILIARY_STRESS.md supplies
  this via |T|<=C(1+mu) and vanishing mu mass under its bounds.
* There are no extra surface forces, surface matter sectors, dipole
  sources, or unaccounted bulk oscillatory/effective stresses. If other
  matter is present, its corresponding conservation and surface content
  must be accounted for rather than assigned to the native scalar sector.

An equivalent compact assumption is convergence of total stress to the
identified piecewise native outer stress with no surface part, together
with enough regularity to take its normal traces. This is a genuine
restriction. Absence of a surface measure alone does not prove that a
weak bulk stress equals the stress of weakly limiting endpoint fields.

## 3. Einstein delta matching

Uniformly bounded metric first derivatives make their quadratic products
have vanishing mass in a shrinking strip. They therefore cannot supply
a gravitational surface concentration there. With continuous metric and
regular one-sided derivatives, the remaining possible singular curvature
is the ordinary extrinsic-curvature jump.

The delta part of the full Einstein equations, with zero matter surface
stress, gives

    [K_ij]-h_ij[K]=0

for the induced three-metric h_ij and one consistently oriented normal.
Taking the three-dimensional trace yields [K]=0, hence [K_ij]=0.
This uses the full Einstein equations, not only the conformal reduced
variations. It does not assume the omitted gauge constraints are solved
merely because a reduced action was written.

In a conformal rest chart with Sigma:x=0,

    K_tt=-exp(alpha)alpha_x,
    K_yy=K_zz=exp(2beta-alpha)beta_x,

up to a simultaneous sign convention for the normal. Thus
[alpha_x]=[beta_x]=0. Their tangential derivatives are common by trace
regularity. The gravitational normal Hamiltonian from the first-order
conformal action,

    Hx_G=Mpl^2 exp(2beta)
          (2alpha_x beta_x+beta_x^2+2alpha_t beta_t+beta_t^2),

is consequently continuous.

This argument excludes gravitational surface concentration under the
uniform first-derivative bound. It does not exclude unresolved bulk
oscillatory gravity outside the layer; that is addressed by the outer-
identification assumption, not by the delta-junction calculation.

## 4. Normal Hilbert flux continuity

For smooth on-shell matter, in a fixed-interface chart,

    partial_mu(E T^mu_nu)
      =(1/2)E T^{rho sigma} partial_nu g_rho sigma.

Bounded metric first derivatives and the vanishing absolute stress mass
in the shrinking strip make the integrated right-hand side vanish.
There is no need to assume the connection is continuous beforehand;
boundedness is enough for this estimate. The identified bulk stress has
ordinary normal traces and no surface measure. Distributional balance
therefore gives

    [E T^x_nu]=0.

For a moving interface use the normal contraction including its velocity,
or transform to its rest chart. At fixed Sigma and common metric values,
the nu=x case and section 1 give [Hx_m]=0. Together with section 3,

    [Hx_G+Hx_m]=0.

This supplies the actual normal-stress condition required by PF02. It
does not identify a general reduced canonical stress with a gravitational
energy tensor. The particular identity was derived explicitly above.

## 5. Completion of the restricted obstruction

The independently reviewed finite-measure lemmas give normal polarization
and scalar flux continuity when their controlled explicit sources have
no surface part. Strong continuous P,phi and common regular tangential
traces allow evaluation of the endpoint currents from the native outer
fields. Section 4 supplies normal Hamiltonian continuity; section 3
supplies ordinary metric derivative continuity.

At each interface event the common tangential quantity
T=P_t+2P beta_t contributes only the affine term -J v T to the matter
partial Legendre transform. It cancels from v f'-f and does not change
f'''. For positive gamma, 0<gamma exp(-2alpha)phi_t^2<1/3, strictly
positive endpoint q, and same-sign nonzero endpoint v, PF02's strict
convexity argument excludes distinct velocities satisfying all the
matching conditions. Equal velocities and common polarization flux
force equal D and ell as well. Thus there is no distinct normal-state
connection in this intersected class.

The layer is allowed to visit the off branch internally. The exclusion
uses its endpoint fluxes and the proved absence of surface storage/stress;
it does not assume the entire layer stays on branch. The auxiliary
multiplier estimate is what controls the negative-divergence segment.

## 6. Verdict limits

The combined statement is a valid restricted no-layer theorem once all
the listed hypotheses are explicit. A purported connection can escape
the theorem only by violating at least one hypothesis; this does not
prove that such an escape exists, is unique, or predicts an outgoing
observable. In particular the result does not prove that smooth native
evolution must form the excluded endpoint configuration, or that finite
signed action implies the compactness, frame bounds, or strong traces.

The key remaining assumption exposed by this final bridge is **native
outer stress/current identification without a bulk oscillatory defect**.
The layer estimates alone do not supply it. If it is omitted, the bridge
does not justify inserting endpoint fields into PF02's classical fluxes.

## Audit matrix and provenance

| Obligation | Status |
| --- | --- |
| Diagonal-base normal homogeneity identity | passed |
| Hilbert sign and metric-dependent representation | passed on shell |
| No quadratic gravitational surface mass | passed under uniform first-derivative bound |
| Extrinsic-curvature and gravitational Hx continuity | passed using full Einstein equations and regular traces |
| Normal stress flux matching | passed with vanishing absolute layer stress and bounded connection |
| Bulk stress/current equals native outer expression | required explicit restriction |
| PF02 contradiction under intersected hypotheses | passed |
| Full smooth-data formation or all singular continuations excluded | out of scope |

Independent delegated proof audit, 2026-11-06. No numerical experiment
was performed. Read `pf07/STATUS.md` and the nine-check symbolic output;
neither was treated as a substitute for the limiting argument.

Reviewed SHA-256 inputs:

    AUXILIARY_STRESS.md d5df21248bfe0fae37585b038fb9f77e4117e22e1eb26f161224ef36400d4b08
    pf07/auxiliary_checks.py 97b45efea063b0ef547ceac75ce3cd3e426968c21a4b8cff75a088c6c1507c14
