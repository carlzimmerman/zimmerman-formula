# Reciprocal field action: growth, rotation, and the nonrotating excess branch

**The proposed mechanism does not yet pass the requested joint test.** Its new rotational mediator leaves linear scalar growth unchanged in the stated background, but the inherited cold compliance still constrains growth. The reciprocal baryon force changes circular velocities. In the passive, spherical nonrotating branch, the region with positive mismatch density has a rigorous radius bound R<=pi ell0. With the prior growth benchmark this is 1.384 kpc, too short to serve as an extended cluster-core surplus. This is not a cluster-lensing exclusion: compact surplus mass can affect larger radii, and no mass or lensing fit has been predicted.

A density-weighted coupling repairs the constant-coupling dilute-fluid wave-speed problem. Its force is derived below with the density variation included. It does not remove the nonrotating bound or supply dwarf masses. All review is self-review. No generally covariant completion is claimed.

Checkpoint RF-2026-10-22-1; base 581d52210bced1231c2517b1d894221edd171f40. Continuation of parent_compliance_2026_10_22, not a replacement of the canonical theory. Contracts, raw outputs, failed controls and manifests are retained here. No existing theory or observation files were modified.

## 1. The reciprocal action and its actual baryonic variation

Use conserved baryon and cold material currents. For a fixed preferred Newtonian frame, take

    L = rho_b v_b^2/2 + rho_c v_c^2/2 - U_b(rho_b)
        -|grad Phi|^2/(2K) -(rho_b+rho_c)Phi
        +eta |dot P|^2/2 -W(K|P|) -e^2/(2chi)
        +MX |dot X|^2/2 -DX |grad X|^2/2 -chi |X|^2/2
        +Mchi dot chi^2/2 -Dchi |grad chi|^2/2
        -mu^2(chi-chi0)^2/2 +g(rho_b) X.curl v_b,

where K=4piG, e=rho_c-rhobar-div P, chi>0, and W is the predecessor's logarithmic potential. All inertia/gradient coefficients are positive. The first version has constant g; the repaired version has g(rho_b)=g0 sqrt(rho_b). These are different models, with the latter's additional density force retained. No P-gradient stiffness is in this candidate. Adding one changes the static bound's premises.

The new coefficients, chi0 and the phase potential are inputs. rhobar is a fixed reference for local static work and a prescribed homogeneous background for the expanding diagnostic. A covariant origin for that reference, preferred-frame dynamics, metric constraints and relativistic stress tensor are not supplied. This is an explicit reduced action tested as a necessary precursor, not a completed parent action.

Integrating the curl term by parts under vanishing/periodic boundary terms gives the reciprocal baryonic momentum

    m_b = rho_b v_b + curl[g(rho_b) X].

The density derivative is equally necessary:

    L_rho_b = v_b^2/2-U_b'(rho_b)-Phi
              +g'(rho_b) X.curl v_b.

Material-current variations give

    (partial_t+v_b.grad)(m_b/rho_b)_i
      +(m_b/rho_b)_j partial_i v_b^j = partial_i L_rho_b.

Thus the baryons are neither prescribed sources nor test particles in a fixed extra field. The local kinetic Hamiltonian can be written |m_b-curl(gX)|^2/(2rho_b), with positive field kinetic terms. This shows the absence of a negative mechanical kinetic square for rho_b>0; it is not a full all-background constraint or hyperbolicity proof. In the static-reference, time-independent problem the action has the usual conserved total energy. Separate field/baryon energies exchange; the interaction cannot provide free work.

The other equations include

    laplacian Phi = K(rho_b+rho_c),
    D_t v_c = -grad[Phi+e/chi],
    eta P_ddot + partial_P W + grad(e/chi)=0,
    MX X_ddot-DX laplacian X+chi X = g(rho_b) curl v_b,
    Mchi chi_ddot-Dchi laplacian chi+mu^2(chi-chi0)
      = e^2/(2chi^2)-|X|^2/2.

Mass conservation is imposed by the material currents. A collisionless stellar population requires a kinetic/multistream extension beyond the barotropic fluid displayed here. None is silently supplied by calling random stellar velocities a coherent curl.

## 2. Linear scalar growth and transverse stability

About a homogeneous state P=X=0, chi=chi0 and e=0, a scalar peculiar velocity is proportional to its wavevector. Its curl vanishes. The source for chi is quadratic. Therefore the new mediator and phase do not enter the linear scalar sector. This statement holds also for g=g0 sqrt(rho_b): the density variation of g multiplies fields of higher perturbative order.

The cold matching energy still has A0=1/chi0 and ell0^2=1/(K chi0). In the quasistatic P limit its cold self-gravity fraction is

    S(a,k)=1/[1+(k_com ell0/a)^2].

Using N=ln a, the diagnostic equations are

    delta_b''+delta_b'/2 = (3/2)(f_b delta_b+f_c delta_c),
    delta_c''+delta_c'/2 = (3/2)(f_b delta_b+f_c S delta_c),
    f_b=1/6.364, f_c=5.364/6.364.

I integrated these from a=1/1101 to 1 with equal dust-growing initial density/velocity amplitudes. This is an EdS subhorizon diagnostic with a fast P response, not a radiation/late-dark-energy calculation or CMB likelihood. Both initial conditions and the final reference amplitude are held fixed. A growth rate close to unity today does not restore amplitude lost earlier.

| ell0 | k_com /Mpc | final total-density amplitude / dust |
|---|---:|---:|
| .440422 kpc | .01 | .999995 |
| .440422 kpc | .1 | .999500 |
| .440422 kpc | 1 | .955654 |
| 133.787 kpc | .01 | .774841 |
| 133.787 kpc | .1 | .295811 |
| 133.787 kpc | 1 | .117510 |

The shorter length preserves the chosen .1/Mpc benchmark closely but already suppresses the 1/Mpc diagnostic by 4.43%. It is not an all-scale growth pass. The large length needed by the predecessor's constant-matching galaxy benchmark loses most of its .1/Mpc amplitude. These numbers do not select any microscopic parameter.

For a homogeneous transverse material displacement xi and one mediator polarization X, the quadratic block is

    L_k=rho_b xi_dot^2/2+MX X_dot^2/2+g k X xi_dot
        -(chi0+DX k^2)X^2/2.

Its nonzero frequency is

    omega^2=[chi0+(DX+g^2/rho_b)k^2]/MX,

with the remaining zero-frequency material mode. The displayed branch is stable for positive coefficients. Its high-k speed grows without bound as rho_b tends to zero if g is constant. This is a problem for extending the constant-g field model to arbitrarily dilute baryonic fluid, not evidence of a ghost in the homogeneous block.

For g=g0 rho_b^alpha the feedback term is g0^2 rho_b^(2alpha-1). If this power must remain bounded at both zero and infinite density with fixed coefficients, alpha=1/2 is the unique power. It yields speed squared (DX+g0^2)/MX. A causal upper speed still has to be imposed and derived from a relativistic completion. Uniform principal speed alone is not full causality. The coupling is nonanalytic at exact vacuum, where fluid variables themselves need a formulation; no vacuum boundary theorem was proved.

## 3. Rotation curves: the reciprocal correction cannot be omitted

For stationary axisymmetric circular flow in cylindrical coordinates, v=v_phi(r), X=X_z(r), define

    Q=-[g(rho_b)X_z]'/rho_b,
    Z=g'(rho_b)X_z omega_b,  omega_b=v'+v/r.

The radial fluid equation is

    Phi'+[U_b'(rho_b)]' = v^2/r+Q(v/r-v')+Z'.

In the local adiabatic approximation X_z=g omega_b/chi, neglecting the mediator gradient and time terms, take chi locally constant. This approximation requires the omitted terms to be small on the actual background; it is not a solved disc.

For constant g and v=V r^p,

    Phi'+[U_b']'=(v^2/r)[1+f(1-p)^2(1+p)],
    f=g^2/(rho_b chi r^2).

For a flat curve and negligible pressure this is v^2=r Phi'/(1+f). A strengthened matching state can therefore lower the measured circular speed relative to the bare gravitational prediction. Rigid rotation (p=1) and zero vorticity (p=-1) have no such local correction. The earlier single-coordinate inertia toy must not be substituted for this field equation.

For the repaired g=g0 sqrt(rho_b), additionally put rho_b proportional to r^-n. The full material variation, including Z', gives

    Phi'+[U_b']'=(v^2/r)[1+f0(1-p^2)(n-2p)],
    f0=g0^2/(chi r^2).

For a flat curve this becomes 1+n f0. In a declining-density region n>0 it again lowers speed at fixed gravitational field. For a declared fractional speed tolerance epsilon, the local flat-pressureless comparison would require n f0<=(1-epsilon)^(-2)-1. This is a diagnostic requirement, not a SPARC fit or a derivation of g0. The coefficient can be made small only by a parameter choice that must also sustain the proposed phase change.

The first density-coupling run exposed an error in the guessed general-slope expression: it lacked the -2p contribution. The independent Cartesian variation was retained, and a cylindrical derivation confirmed the correction. Contracted flat, rigid and zero-vorticity limits were unaffected. See DENSITY_CORRECTION.md; original failed output is preserved.

No global disc solution with varying chi, finite boundaries, self-consistent cold inventory and all 175 SPARC galaxies was computed. The result is a necessary backreaction formula, not a claim that rotation curves are preserved.

## 4. Nonrotating dwarfs and clusters: a radius theorem for positive surplus

On a spherical stationary branch with zero mean baryonic vorticity, choose the passive solution X=0. With regularity and boundary/asymptotic chi>=chi0, the scalar equation implies chi>=chi0 by the minimum principle: at an interior minimum below chi0, its left side would be negative and its right side nonnegative.

Static cold chemical equilibrium defines h=mu_c-Phi, so e=chi h. Retaining the P equation is essential. It gives

    partial_P W=grad Phi,
    u=K|P|=a0 g/(g+a0), g=Phi'>=0,
    (r^2 q_a(g))'/r^2 = K rho_b+K chi h,
    q_a(g)=g-u=g^2/(g+a0)<=g.

In units x=r/ell0, s=h/(a0 ell0), y=g/a0=-s', define Q=x^2 q(y), q(y)=y^2/(1+y). Then, while s>0,

    Q' >= x^2 s,    0<=Q<=-x^2 s',

because rho_b>=0 and chi>=chi0. Assume a regular centre with Q(0)=0, finite positive s(0), and an attractive monotone potential. Suppose s stays positive to x=pi. Multiply the first inequality by phi=sin x/x, positive and decreasing on (0,pi). Using phi(pi)=0,

    integral_0^pi x^2 s phi dx
       <= integral Q' phi dx
       = -integral Q phi' dx
       <= integral x^2 s' phi' dx
       = -pi s(pi)+integral x^2 s phi dx.

The last equality uses (x^2 phi')'=-x^2 phi and x^2 phi'(pi)=-pi. It forces s(pi)<=0, a contradiction. Hence the first zero obeys

    R_positive_e <= pi ell0.

This bound is independent of a0 and of the passive scalar's nonlinear stiffness; it applies to both footings. It also allows nonnegative extended baryonic sources. It is conditional on the stated action (no P-gradient term), static spherical branch, regular centre and scalar boundary conditions. A point-mass singularity, moving/turbulent phase, different boundary state or added spatial operator needs a new analysis.

In the local phase-equilibrium limit, chi=chi0+h^2/(2mu^2). The exact radial equations become those in CONTRACT.md. Twenty declared central-amplitude/source cases were integrated with two algorithms/tolerances. All first-zero radii were below pi ell0; the largest was 3.102624 ell0. The largest relative repeat difference was 3.05e-7. These numerical checks support the written proof; they do not replace it or count as observed galaxies.

Using the predecessor's .440422-kpc growth bound gives

    R_positive_e <= 1.383627 kpc.

**Interpretation:** there is room for a compact dwarf-scale positive surplus, but its mass, central amplitude and formation history are not selected. The same passive phase cannot sustain a regular extended positive mismatch region on cluster-core scales under that benchmark. The bound is on e=rho_c-rhobar-div P, not on total cold density. Beyond its zero, negative e is possible while total rho_c remains positive; that exterior must be solved and matched, not discarded.

A compact surplus can lens outside 1.4 kpc, and its polarization response can also affect the potential there. Therefore this theorem alone does not reject every cluster profile or supply a lensing likelihood. The existing CFG922/CFG929 reports describe a substantial MID-versus-OUTER shape requirement. No mapping from our compact surplus to those data has been derived, so the observed dwarf/cluster excess remains unexplained. Imposing a core mass to match it would be an input, not this mechanism's prediction.

### Positive polarization stiffness does not remove this bound

STIFFNESS_EXTENSION.md adds positive gamma |grad P|^2/2 and derives the signed radial polarization equation. With g>=0, a regular centre and nonnegative outer polarization, a negative interior minimum of P_r is impossible. Consequently u>=0 and Q=r^2(g-u)<=r^2 g still hold. These are the only polarization properties the comparison proof needs. The radius bound therefore survives this extension even though the exact algebraic galaxy law no longer holds.

Its quasistatic growth response is also no larger: with t=gamma k^2/K, S_gamma-S_0=-t z^2/[(1+z)(1+t+z)]<=0. Adjusting this positive stiffness alone cannot open the tested growth/radius window. Different polarization boundary states or extra interactions are outside that statement.

### Sensitivity to the chosen growth tolerance

The 1.384-kpc number uses the predecessor's strict local exponent criterion. To avoid making that tolerance do all the work, TRADEOFF_CONTRACT.md declares a separate sensitivity calculation using the integrated amplitude at k=.1/Mpc. For a desired positive-surplus radius R, the theorem requires ell0>=R/pi. Evaluating the permissive zero-gradient model at equality gives:

| desired positive-surplus radius | minimum ell0 | retained final amplitude / dust |
|---|---:|---:|
| 10 kpc | 3.183 kpc | .975508 |
| 100 kpc | 31.831 kpc | .556205 |
| 500 kpc | 159.155 kpc | .274670 |

Increasing ell0 only lowers the response in these equations: their first-order density/velocity system has nonnegative off-diagonal coefficients, and the cold source coefficient decreases with ell0. Thus this is an optimistic comparison for the stated history. It is not a likelihood or an assertion about a compact source's lensing extent.

Conversely, demanding .99, .95 or .90 retention in this diagnostic permits positive-surplus radii at most 6.264, 14.811 or 22.570 kpc. Even a much looser 10% amplitude-loss allowance does not produce a 100-kpc extended passive surplus in this candidate. The integrated history remains the stated EdS approximation; a full cosmological theory must be checked on its own equations.

## 5. Where the joint test stands

| Requested property | Result for the tested candidate |
|---|---|
| Cosmological growth | New rotational mediator absent at linear scalar order; inherited compliance must remain small. .1/Mpc diagnostic can be close to dust, not a full cosmological pass |
| Rotation curves | Reciprocal correction derived and nonzero in typical flat, declining-density regions. No demonstrated common parameter choice that preserves curves and produces strong matching |
| Dwarf excess | Compact passive surplus mathematically possible; no selected mass, profile, formation or retention |
| Cluster excess | Passive extended surplus limited to pi ell0. Compact-source alternative and lensing projection untested; no explanation established |
| Relativistic parent | Not established; only an explicit reciprocal reduced action and homogeneous principal tests |

The density-weighted mediator is a better-defined field candidate than the prior oscillator toy, but it has not solved the target. The main new obstruction is that the growth-compatible passive phase has too short a positive-surplus region for an extended cluster mechanism. Rotation can alter the phase only where its independently modeled source is present, and it changes baryon motion reciprocally.

## 6. Verification and open continuations

Current runs: run2, 21/21 checks; density_run2, 7/7; stiffness_run, 4/4; tradeoff_run, 7/7. Mutation removes the reciprocal baryon force and the cold restoring density and fails 5 checks; density_mutation2 removes the required density force and fails 3; stiffness_mutation reverses the gradient energy and fails 3. Their manifests record actual versions, input hashes and statuses. All numerical tests are small and single-threaded. No observational refit, install, download, commit or push occurred.

Open, not exhausted: full FRW dynamics with finite P inertia; covariant clock/current completion; nonlinear characteristic matrix; finite P stiffness; actual turbulent/kinetic baryon source; a self-consistent rotating halo with an independently specified cold inventory; compact surplus lensing; radiation/transport and survival. These continuations change or extend named premises and cannot inherit passes automatically. The exact next steps and scope are in HANDOFF.md.
