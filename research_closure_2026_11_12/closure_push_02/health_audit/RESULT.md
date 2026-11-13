# Independent audit: finite-Pi Einstein-constrained scalar health

**Primary verdict: correct only after a stated restriction.** The local scalar
principal claim is supported for the specified regular-center construction,
nonzero D and h, and the classical continuum action with no imposed ultraviolet
cutoff. It is not a global evolved-background result, an all-wavelength spectrum,
or a proof that every admissible trajectory is unhealthy. A small radial-series
error was found and corrected below; it does not change the principal result.

I reconstructed the geometry, constrained matter action and high-frequency
polarization elimination independently. The audit script does not import the
author's checker. The exact reviewed snapshots and hashes are in[sources.json](sources.json).
The initial audit base is `2207a1df48348f01ca1084d4add5d214c55d0e7e`.

## Claim and dependency audit

At a center with N=1, spatially constant Q=q, P=0, Pi=p>0, isotropic extrinsic
curvature Kij=h gamma_ij, vanishing intrinsic Ricci tensor, and positive density,
the proposed coefficients are

    A0=q² H_QQ,
    c=1+gamma p-H_Pi+q H_QPi,
    D=H_PiPi-gamma,
    A_infinity=A0-c²/D,
    n_eff=q H_Q+p(1+gamma p-H_Pi).

The scalar principal dispersion is
`omega²=(n_eff/A_infinity) k² + lower orders`.

| Obligation | Audit outcome |
|---|---|
| Exact lapse/shift dependence after tangency | passed |
| Missing momentum or lambda-P contribution | passed: cancellation is on shell of normal P equation |
| Hamiltonian and physical radial divergence constraints | passed |
| Local regular-center data | passed with corrected cubic series and stated regularity |
| Time-current versus Einstein-energy compatibility | passed at the center; no background time evolution was executed |
| Independent full scalar ADM kinetic/gradient expansion | passed |
| Fixed-chi high-k polarization Legendre elimination | passed |
| Omitted finite-Pi metric mixing affects leading k²? | no for D!=0 on this center; affects lower orders |
| Anisotropic/curved/off-center generalization | not established by the center calculation |
| Degenerate D=0,h=0,A_infinity=0 or finite constraint poles | outside this elimination |
| Uniform high-q gate-family claim | passed with explicit half-line/nonconstant hypotheses |

## Why the momentum and current constraints do not remove the mode

In unitary gauge, P^0=0 and
`Pi=div(J)/sqrt(gamma)`, J^i=sqrt(gamma)P^i. Both Q=q/N and Pi are independent
of the shift. Integrating P.grad(lnN) by parts gives the exact bulk matter
action `N sqrt(gamma)[U(Q,Pi)-W]`, U=H-Pi-gamma Pi²/2 on p>0.
Thus the reduced matter action has no shift dependence. In a covariant
variation the apparent lambda-P momentum terms cancel using the normal P
equation. This is not an omitted momentum source or an assumption that the
clock's charge flux vanishes.

At the center, B=1+gamma p-H_Pi and the exact current derived independently in
current_transport gives

    rho_Q=H_Q+(B/q)p,     lambda/q=dot(B/q).

Its continuity equation is precisely

    q H_QQ Qdot+c pdot+3h n_eff=0.                            (T)

Meanwhile the Hamiltonian-source density is
`rho=qH_Q-H+p+gamma p²/2`, so
`rho_dot=qH_QQ Qdot+c pdot`. Einstein energy conservation yields exactly(T).
This checks the load-bearing center time-jet compatibility. It does not pretend
that higher radial time jets or an entire nonlinear background history were
numerically evolved. Constraint-preserving evolution must remain on a regular
auxiliary branch; a singular branch would require a separate reduction.

## Independent geometric and scalar calculation

I constructed the full 3D covariant Kij for scalar perturbations depending on
one coordinate, retaining the transverse covariant shift derivatives, and
expanded `N sqrt(gamma)(KijKij-K²)` directly. After spatial boundary terms, the
leading kinetic/shift terms are

    -3 M2 (zeta_dot-h alpha)²
       -2 M2 k² beta(zeta_dot-h alpha).

Consequently the nonzero-k momentum equation gives alpha=zeta_dot/h. The
spatial-curvature expansion independently gives
`M2 k² zeta²+2 M2 k² alpha zeta`. Integrating the latter cross term in time
with its a/h coefficient, rather than freezing that coefficient, yields
`M2 hdot k² zeta²/h²`. Einstein evolution at the center gives
`hdot=-K n_eff`, M2=1/(2K), producing the stated negative gradient term.

The exact matter Taylor expansion gives
`A0 alpha²/2-c alpha d+D d²/2`, plus a finite-Pi mixing
`-3pD zeta d` and derivative-free metric terms. For D!=0 the P constraint
makes d=O(alpha,zeta) at high k; the extra terms then give at most
zeta*zeta_dot or zeta², not a new leading k² term. Background first spatial
gradients and intrinsic Ricci tensor vanish at the chosen center. Nonzero P
away from that center would require its own anisotropic symbol calculation.

A separate derivation removes reliance on that Schur calculation. At high k
the longitudinal P equation implies delta[NU_Pi]=0 at leading order: W_P
contributes lower spatial order. Set chi=NU_Pi and eliminate Pi in

    L_eff(N)=N U(q/N,Pi)-chi Pi.

Its exact implicit lapse Hessian is `A0-c²/D`. Its pressure is
`U-Pi U_Pi=H-pH_Pi+gamma p²/2`; its energy is `qH_Q-U`. Their sum is n_eff.
This independently reproduces both the kinetic and gradient coefficients.
For n_eff>0 and A_infinity<0, the characteristic has imaginary frequency
growing proportionally to k. That is a physical scalar principal instability,
not merely the sign of an auxiliary P block or bounded Jeans growth.

## Background ODE and a genuine series correction

For gamma_ij=psi^4 delta_ij and physical radial polarization v,

    Pi=psi^-2[v'+2v/r+4(psi'/psi)v],
    Pi'=-psi² W_v/D,
    psi''+2psi'/r=psi^5(6h²-4K rho)/8.

All factors check. Taking h²=2K rho(0)/3 makes the central intrinsic Ricci
tensor zero. The center equations can be written as regular Volterra
integrals, for example

    v(r)=r^-2 psi(r)^-4 integral_0^r s² psi(s)^6 Pi(s) ds,
    Pi(r)=p-integral_0^r psi(s)² W_v(v(s))/D(s) ds.

The corresponding double integral for psi has bounded r^-2 integral_0^r s²
kernels. On a small enough interval with D bounded away from zero, psi>0 and
polarization below its cap, these maps have the usual local contraction
property. This is local constraint data, not a global halo construction.

The original W has `W_v=K v/(1-Kv/a0)`. Therefore the correct first terms are

    v=pr/3+O(r³),
    Pi=p-Kp r²/(6D0)-K²p² r³/(27a0D0)+O(r⁴),
    psi=1+O(r⁴).

The author's earlier `Pi=p-Kp r²/(6D0)+O(r⁴)` omitted the cubic term.
Replacing its remainder by O(r³), or retaining the displayed cubic term,
repairs it. The radial |r|³ term means one should not describe the center
as Cartesian C-infinity; C² regularity is sufficient for the coefficients
used here. The omission is negligible at the numerical start radius and
does not change p,D0,c,A_infinity or the principal sign. A separate exact
series check rejects that omission. The correction was sent to the author.

## Independent numerical witness and gate-family theorem

At exact decimal q=1+10^-6, C=10^6, Pic=p=K=a0=1, gamma=10^-8 and
S(u)=exp(-u³), an independent60-digit evaluation gives

    A_infinity = -596965.0195749891,
    n_eff       = 1.735760731740091,
    rho         = 1.735759255222326,
    D           = 1.093638323514327e-6,
    omega²/k²   = -2.907642281914391e-6.

The small differences from the author's float64 values come from representing
q-1 near10^-6; all signs agree. The independently derived leading Newtonian
transport limit agrees in sound-speed squared within5.15e-7 relative at this
point. The author supplied a local constrained radial integration; I audited
its equations, initial series and diagnostic method rather than claiming an
independent full background evolution.

[GATE_LEMMA.md](GATE_LEMMA.md) proves the separate calculus lemma. For every
nonconstant positive nonincreasing C² S on[0,infinity) with S'(0)=0, some u>0
satisfies `0<S''<S'^2/(2S)`. The proof uses a positive interior maximum of
g=-S' and points immediately after its last maximum plateau. S''(0)=0 and
S(infinity)=0 are not needed. Constant gates, finite domains, and nonflat
gates require different statements; explicit counterexamples are retained.

At this u, for every fixed finite gamma,Pic,C>0 (also gamma=0),

    A_infinity/(Cq²) -> 2S-S'^2/S'' <0,
    n_eff/(Cq²) -> 2S-uS' >0,
    rho/(Cq²) -> S >0.

Thus the unrestricted classical field domain contains unhealthy local
constrained states for every such gate and fixed stiffness. This excludes
uniform health over that unrestricted domain. It does **not** show that every
state is unstable or that a separately justified bounded domain or cutoff
contains the witness. The author's positive-principal example remains valid
as a restricted example, not a complete stability certificate.

## Evidence, provenance, and remaining limits

The independent run verifies24 identities/sign/limit checks, including two
mutations; the separate series run verifies3 more. Both computations are
bounded, with raw results and manifests retained. The checked source versions
are snapshotted; later author documentation changes are not silently treated
as the same bytes. No files outside this audit directory were changed.

The principal argument requires arbitrarily short wavelengths within the
classical action. A physical ultraviolet cutoff, new operators, a restricted
invariant state domain, extra matter perturbations, or a nonsmooth crossing
of the one-sided stiffness switch needs a new calculation. No claim of a
global halo, all-wavelength spectrum, fully evolved constraint solution, or
observational exclusion follows solely from this audit.

**Strongest supported conclusion:** the stated finite-positive-Pi branch has
a GR-inclusive unbounded scalar principal instability, and the flat-gate
family cannot be uniformly healthy on its unrestricted classical field domain.
The simple claim that the instability disappears after imposing Einstein
constraints fails this independent reconstruction.
