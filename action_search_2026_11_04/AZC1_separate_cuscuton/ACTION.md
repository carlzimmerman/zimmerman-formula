# AZC1: an explicit candidate action; health remains open

**Result:** an explicit covariant candidate gives the exact dark-energy density
tie, an evolving homogeneous branch, and a positive restricted static response
block. It avoids C''s specific derivative-of-density insertion. It is **not yet
a healthy completion**: the coupled two-foliation constraint problem is open.
No observational gate has been promoted, and kappa = 1/2 remains fitted.

Frozen criteria commit: `ec40c887a0`. Evidence: `runs/main_portable/` (28/28
checks), plus three negative controls that fail their intended invariants.

## 1. The action

Use signature (-,+,+,+), c=1, K=4 pi G and Mpl^2=1/(8 pi G). Let tau be the
existing v3s clock, Q=sqrt(-d tau.d tau), n_mu=-d_mu tau/Q,
h_mu_nu=g_mu_nu+n_mu n_nu, A_mu=n^nu nabla_nu n_mu, and D its spatial
derivative. P is a spatial covector with n.P=0; lambda enforces that constraint.
Put p=K sqrt(P_mu P^mu), with 0<=p<a. Write

    S = integral sqrt(-g) {
          R/(4K) + P^mu A_mu - W(p,a)
          - (gamma_L/2) [max(D_mu P^mu,0)]^2
          + mu_K^2 (Q-1)^2/(2K) + lambda n_mu P^mu
          + (b/phi) sqrt(2X) - (m2/2) phi^2
        } d^4x + S_m[g,matter],

    W(p,a) = (a^2/K) [-p/a - log(1-p/a)],
    X = -g^mu_nu d_mu phi d_nu phi / 2,
    a = alpha phi,        alpha^2 = kappa^2 G m2/2,
    gamma_L = K L_star^2/2.

Here b,m2,alpha,phi are positive and X>0. The two scalars are independent:
**do not replace tau by phi** when varying A, D, or P. Matter remains minimally
coupled to g. There is no bare Lambda in this candidate.

A cleaner equivalent normalization uses chi=alpha phi, which has acceleration
units and directly denotes the local scale:

    L_DE = (b/chi) sqrt(-dchi.dchi) - chi^2/(kappa^2 G),
    a0 = chi.

The rest of the action is unchanged with W(p,chi). Thus m2 and alpha do not
supply two additional physical parameters; their ratio is fixed and the field
normalization can be removed. The action still posits its functions, b, kappa,
L_star and mu_K. It derives neither the numerical kappa nor the cosmic scale b.

With hbar=1 as well, [G]=mass^-2, [a]=mass, [P]=mass^3,
[W]=mass^4 and [b]=mass^3 in the chi normalization; all displayed terms then
have mass dimension four. Lambda here refers only to the absent vacuum term;
the lower-case lambda above is a constraint multiplier.

## 2. What changed from C''

C'' sets a^2 proportional to X+V for a canonical scalar. Consequently W
depends on its velocity. Retaining the khronon velocity exposes the negative
kinetic contribution reported in CT14.

Here P_DE=(b/phi)sqrt(2X)-V, with V=m2 phi^2/2, satisfies

    rho_DE = 2X P_DE,X - P_DE = V,
    rho_DE,X = P_DE,X + 2X P_DE,XX = 0.

Therefore a^2=kappa^2 G rho_DE exactly on the timelike branch, and
d ln a/d ln rho_DE=1/2. W depends on phi but not dphi, so it adds no direct
phi-velocity Hessian. The energy density here is the rest-frame density of
the displayed DE sector; outside FRW the interaction has its own stress and
must not be silently counted as zero. On FRW P=A=0, W=0, so the sector split
is unambiguous for this identity.

This avoids the **specific C'' coupling**, not every possible instability.
The cuscuton is a constrained/elliptic sector in its own foliation; it is not
a conventional canonical scalar whose health can be inherited automatically.

## 3. Homogeneous dynamics, without a bare cosmological constant

Take the zero-charge khronon background Q=1, P=0, flat FRW, and conserved
baryonic dust. For the decreasing scalar branch, the scalar equation gives

    V_phi = 3 (b/phi) H,
    m2 phi^2 = 3 b H,
    rho_DE = 3 b H/2.

With Hc=b/(2 Mpl^2), Friedmann and dust conservation give

    H^2 - Hc H = rho_b/(3 Mpl^2),
    Hdot = -3 H^2 (H-Hc)/(2H-Hc),
    w_DE = -H/(2H-Hc),
    q_dec = (H-2Hc)/(2H-Hc).

Thus H>Hc has positive DE enthalpy and decreasing phi; Hc<H<2Hc accelerates.
It approaches H=Hc and X=0 asymptotically. The original square-root action is
not differentiable at X=0, so this is **not** a regular attained rolling de
Sitter solution. The earlier pure-vacuum rolling-de-Sitter obstruction stands.

This branch uses baryonic dust and no added cold sector. It is not a fit to
the expansion history, nor a solution of the CMB/growth problem. The density
tie is exact, but the model does not realize every possible DE history. In
particular, reproducing CT7's specific evolving history gates remains untested.

The change of variable psi=log(phi/phi_ref) makes the kinetic term b sqrt(2X_psi)
and the potential exponential in psi. This homogeneous mechanism is known;
it is not a new discovery. See the source record below.

## 4. Fixed-scale galaxy equation

Hold phi spatially constant and suppress stiffness only on scales where that
approximation is justified. Varying P gives

    g = p/(1-p/a),       p = a g/(a+g).

In the spherical, static, dust-free weak-field reduction the lapse equation
is g_b=g-p. Hence

    g = [g_b + sqrt(g_b^2 + 4 a g_b)]/2.

This is the desired law S. The screening term is retained in the full action;
it cannot be neglected to claim a Solar-System pass. Variable phi, its stress,
the external field and global matching must be included before G1, G2 or G4
can be graded. This calculation proves only the fixed-scale reduction.

## 5. A restricted static positivity result

The potentially useful result is joint convexity, including a conservative
Newtonian subtraction. Let Wbar=K W and

    U(p,a)=Wbar(p,a)-p^2/2,
    s=p/(a-p)>0.

Direct differentiation gives

    U_pp = s(s+2),
    U_pa = -s^2,
    U_aa = s^2-2s+2 log(1+s),
    det Hess(U) = 2s[(s+2)log(1+s)-2s].

These signs hold for every finite s>0. For the last expression set
q(s)=log(1+s)-2s/(s+2). Then q(0)=0 and

    q'(s)=s^2/[(s+1)(s+2)^2]>0.

Also U_aa(0)=0 and U_aa'=2s^2/(1+s)>0. Therefore the two-by-two radial/scale
Hessian is positive definite. For a vector p, its transverse eigenvalue is
(Wbar_p/p)-1=s>0. Since a is linear in phi, the corresponding joint Hessian
in (vector p,phi) is positive definite as well. Adding V''=m2>0, the positive
cuscuton spatial-gradient quadratic term, and the convex switched stiffness
does not spoil this restricted statement.

Why subtract p^2/2? In the usual static PN reduction, eliminating the
Newtonian lapse supplies an energy term -||Pi_L p||^2/(2K). Since the
longitudinal projector has norm at most one, subtracting the full ||p||^2/(2K)
is the conservative local bound. This argument assumes the specified static
source/constraint reduction and its boundary conditions; it does **not**
include all DE-lapse couplings or prove positivity of the full gravitational
Hamiltonian. At p=0 the Hessian degenerates; no uniform ellipticity at that
endpoint is claimed.

This is an analytic result with symbolic verification and a 65-point
high-precision corroboration, not a universal claim inferred from sampling.
It suggests that the new algebraic P-phi coupling need not recreate the
static sign failure. It does not establish the coupled propagating spectrum.

## 6. The decisive unresolved health obligation

There are two foliations. In a tau-adapted local chart, write u=partial_t phi,
z=|grad phi|, and C=b/phi>0. At fixed metric and phi,

    partial_u^2 [C sqrt(u^2-z^2)]
       = -C z^2/(u^2-z^2)^(3/2),       |u|>z.

It vanishes at z=0 and is negative for nonzero z. This is a warning about
using a tilted chart for an elliptic field, **not by itself a physical ghost
or DOF count**. It rules out the shortcut of claiming uniform nondynamical
behavior from a homogeneous Hessian alone.

Required next calculation: formulate the coupled action in phi-adapted ADM
variables while retaining a freely varying tau. Derive all primary and
secondary constraints, preserve them in time, and reduce the scalar principal
symbol on a background with nonparallel dphi and dtau. Check whether there
is a common admissible evolution/boundary prescription. Then match to a
regular cosmological-plus-galactic background and verify the timelike domain.
Identifying the two foliations by hand is a new theory, not this calculation.

**G0 remains UNDECIDED.** A full physical DOF count, nonsingular constraint
algebra and stable reduced spectrum have not been obtained. Existing v3s
instantaneous constraints, moving-source limitations and out-of-scope failures
remain. The proposed action is a research candidate, not a replacement for the
owner's adopted scoped action.

## 7. Source applicability and prior-route distinction

- Afshordi et al., *Cuscuton Cosmology*, arXiv:astro-ph/0702002v2, equations
  (4)-(6) and section IV.3: the isolated exponential-potential cuscuton has
  the relevant homogeneous expansion law. Our psi change of variables gives
  the dictionary. **Verified for this isolated homogeneous mechanism;
  inapplicable as a proof of health for the added v3s coupling.**
  https://arxiv.org/html/astro-ph/0702002v2
- Gomes and Guariento, *Hamiltonian analysis of the cuscuton*,
  arXiv:1703.08226v1, sections IV-V: homogeneous and general inhomogeneous
  formulations require care about constraint structure. **Read as a warning;
  no theorem about this coupled action is inferred.**
  https://arxiv.org/html/1703.08226
- Bhattacharyya et al., *Revisiting the cuscuton as a Lorentz-violating gravity
  theory*, arXiv:1612.01824v2, sections I-II: timelike domain and preferred
  foliation/auxiliary-vector formulation. **Exact extension to two interacting
  foliations unverified.**
  https://arxiv.org/html/1612.01824v2

HTML primary sources read on 2026-11-04; no PDF or data downloads and no
full-text retention. No observational bounds or density inputs from these
papers enter the calculation. Their rendered decorative dates were not used
as version identifiers.

Local prior work: CT10 already identifies rho_X=0 as the potential-only exact
tie option. The October cuscuton report examines a different force kernel and
a **same-foliation** acceleration response; its no-rolling-pure-vacuum result
is respected here. CT6's CMC escape constrains the v3s clock itself; that is
not an automatic theorem about this independent scalar. These distinctions
justify testing, not declaring an escape. Searches covered the current CT
lanes, the nearest cuscuton report and references, and selected campaign
records. Global novelty was not investigated or claimed.

## 8. Evidence and continuation

- `check_action.py`: the mathematical identities and finite corroboration.
- `contract.json`: explicit finite assertion, versions and non-claims.
- `runs/main_portable/`: 28/28, exit 0, runner status completed.
- `runs/mutate_kinetic/`: 24/28, exit 1; +X breaks density and Hessian identities.
- `runs/mutate_tie/`: 26/28, exit 1; squared phi scaling breaks the tie.
- `runs/mutate_cross/`: 26/28, exit 1; doubled cross term breaks positivity.

The first runner invocation rejected CPU affinity on this host before launch.
The subsequent `runs/main/` attempt failed in child resource setup. These are
execution failures, not mathematical failures. The portable runs retain
60-second wall and 55-second CPU limits and single-thread environment caps;
OS affinity and address-space enforcement were unavailable. This is a small
pure symbolic/high-precision calculation, not a heavy compute job. No criteria
or pass tolerances were changed.

Proof/review status: author self-review of the displayed identities, signs,
domain and scope; no independent agent review. Source matching does not
certify the new action. The next work is the two-foliation constraint test in
section 6, before any observational fitting or adoption.
