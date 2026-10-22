# FGF044 recovered author package

Primary self-review verdict: **proved as written**, on the exact domain below.
Worker outcome: `supports_scoped_claim`; orchestrator acceptance remains
**unreviewed**. Exact continuity removes the persistent cubic spacetime flux.
The exact global energy inequality fails; only a quantified vanishing error is
proved. This is not an exact coupled solution.

## Provenance and recovery boundary

The original author was `/root/coupled_dynamics`, as identified by the recovery
dispatch. Its FGF044 execution stopped with a usage-limit error before packaging.
At recovery the run directory contained only `DERIVATION.md` (14312 bytes), with
SHA256 `5603934d74e5f9236a388aee63adfe714ad6fb8e218f95de4a5436fec7c5d9fb`.
Those bytes are preserved. Its actual reasoning start and finish times were not
instrumented here and are not reconstructed from filesystem times.

This report and metadata were prepared by the explicit recovery agent
`/root/fgf044_package_recovery`. This is a reconstruction and **self-review of
the author package**, not an independent author or reviewer proof. Only the
original author derivation, task, framework, contract, and pinned ancestry were
used. No new stage-31 root/reviewer proof files were read. The reconstruction
and initial REPORT write preceded two messages from the recovery reviewer
`/root/fgf044_author_review_recovery`: no blocking correction was found; keep
the N-dependent energy-increase interval distinct from the cubic-flux fast
scale, and distinguish interior from initial-trace residual rates. These cues
agree with the already-written report and are disclosed rather than erased
from the recovery provenance. All nine task ancestry hashes match. No
mathematical correction was found, so no correction
file was created. No task, queue, claim, ancestry, or other run file was edited.

## Exact claim and domain

Fix the inherited static signed-Q diagnostic crossing on a finite interval
`I=(-d,d)`, with positive density rho, fields phi0, chi0, unchanged field walls
and mass, positive physical coefficients C=4piG, tau, sigma, J, cs^2, S0,
and fixed positive density reference rho_ref. The background equations are

    B0_x=C rho, cs^2 rho_x=-rho g0, J chi0_xx=U'(chi0)-T0,
    g0=phi0_x, a=a_ref exp(chi0),
    B(g,a)=sgn(g)(sqrt(a^2+4g^2)-a)/2, W_g=B, T=-W_chi,
    U(chi)=S0[cosh(2chi)-1]/4.

Select x* in a fixed compact regular neighborhood with g0>0, hence rho_x<0.
Fix v0,L>0 and a finite T>0, independent of dimensionless integer N. For every
sufficiently large N with `[x*-L/N^3,x*+L/N^3]` inside that neighborhood, use
exactly f(y)=(1-y^2)^2 for |y|<1 and zero otherwise, and
v_N=v0 N f(N^3(x-x*)/L). Hold the fields at their background; solve continuity
from n_N(0)=rho by the prescribed velocity flow. No profile replacement or
smoothing is made. C^1,1 regularity, piecewise smoothness, and distributional
first-derivative equations suffice; no C-infinity or uniform-in-N regularity
is assumed. All stated estimates are for this one family and its zero-velocity
control. They apply to each fixed finite slab, not to a growing time horizon.

Both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 remain separate positive reference
choices with adopted a=kappa c sqrt(G rho_Lambda). Constant-vacuum and frozen-H
reference comparisons are distinct. A genuinely evolving-H history is outside
this fixed-reference proof and requires additional work/reservoir accounting.

## Dependency reconstruction and decisive checks

The dependency graph is acyclic: inherited action/static background -> explicit
flow -> mass/Jacobian identities -> entropy and transport estimates -> full
energy/current estimates -> actual residual bounds. The initial energy failure
uses the same flow, hydrostatic sign, and an integration by parts. All leaves
are either the declared inherited background/action, elementary identities
reconstructed below, or the fixed domain assumptions. There is no numerical
or unverified literature leaf.

1. **Finite flow and exact continuity — passed.** The coordinate
   H=y/[2(1-y^2)]+log[(1+y)/(1-y)]/4 has H'=1/f and maps (-1,1) onto R.
   Y_s=H^{-1}(H(y)+s), s=v0 N^4 t/L, stays interior for every finite s.
   Its physical map has Jacobian f(Y_s)/f(y)>0, extended continuously as 1 at
   support edges. Pushforward n(X_t(b))=rho(b)/partial_b X_t conserves mass
   and solves n_t+(n v)_x=0, including the initial trace. The outer map is the
   identity. No entering particles, sheet masses, or support-edge deltas occur.
2. **Finite supply and full cubic transport — passed.** Only
   m_N=integral_(J_N)rho=O(N^-3) moves, and displacement is between 0 and 2l_N.
   Thus integral_0^T integral j=integral rho(b)[X_T(b)-b]<=2l_N m_N.
   An additional direct characteristic check of the same accounting is

       integral_0^T integral n v^3/2
       = (1/2) integral_(J_N) rho(b) integral_b^{X_T(b)} v(x)^2 dx db
       <= V_N^2 l_N m_N=O(N^-4).

   This identity uses dx=v dt along each interior characteristic and gives
   the same bound as the preserved derivation; no outside supply is assumed.
3. **Polynomial compression and entropy — passed.** With delta_+=1-Y and
   delta_-=1+Y, d(1/delta_+)/ds<=4 and -d(1/delta_-)/ds<=4.
   The latter implies delta_-(s)/delta_-(0)<=1+4s delta_-(s)<=1+8s;
   the former gives the reciprocal bound for delta_+. Hence
   (1+8s)^-2<=partial_b X_t<=(1+8s)^2. With
   h_N(t)=2log(1+8v0 N^4 t/L)+2l_N sup|partial_x log rho|,
   D(n|rho)<=m_N h_N(t)=O(N^-3 log N) uniformly on [0,T].
4. **Full energy and interaction — passed.** The inherited complete density is

       E=n v^2/2+e(n)+n Phi
         +[tau Phi_t^2/2+W+sigma X_t^2/2+J X_x^2/2+U]/C,
       e(n)=cs^2 n[log(n/rho_ref)-1].

   Frozen field terms cancel exactly in E-E0. With
   mu=cs^2 log(rho/rho_ref)+phi0 constant,
   E-E0=n v^2/2+cs^2 h(n,rho)+mu(n-rho). Mass conservation cancels the
   last term only after integration. Therefore Erel=K+cs^2 D, and
   Erel<=epsilon_N=V_N^2 m_N/2+cs^2 m_N h_N(T)->0 uniformly. The full
   density L1 norm is <=epsilon_N+2|mu|m_N. No interaction is omitted.
5. **Exact global energy inequality — failed, as claimed.** D'(0)=0 and
   Erel'(0)=-(1/3)integral rho_x v_N^3>0. The derivative approaches
   -rho_x(x*)v0^3 L integral f^3/3>0. Each sufficiently large N therefore
   violates Erel(t)<=Erel(0) at some small positive time. The valid approximate
   budget is Erel(t)<=Erel(0)+epsilon_N. Failure of the exact inequality is
   retained evidence, not a failed verification of the reported theorem.
6. **Complete current and time limits — passed.** Since field velocities vanish,
   S=n v^3/2+j[cs^2 log(n/rho_ref)+phi0]. Its spacetime L1 norm is
   O(N^-4)+O(N^-6 log N). At t=0 its cubic part tends to
   F_* delta_x*, F_*=rho(x*)v0^3 L integral f^3/2>0. At each fixed t>0 it
   tends to zero by the pushforward formula and dominated convergence, also
   uniformly on [t0,T] for fixed t0>0. At t=s L/(v0 N^4), its measure
   coefficient is rho(x*)v0^3 L integral f(Y_s(y))^3 dy/2. These distinct
   limits describe the initial transient. The slab L1 bound excludes a
   surviving time-delta flux. No N/time limit is freely exchanged.
7. **All actual residuals and topologies — passed.** The exact residuals are

       Rc=0, Rphi=C(n-rho), Rchi=0,
       Rm=j_t+[n v^2+cs^2(n-rho)]_x+(n-rho)g0,
       Rcomb=j_t+[n v^2+cs^2(n-rho)]_x.

   This retains the changed-density signed-Q source. Rphi is O(N^-3) in
   L-infinity_t L1_x. Rm and Rcomb are O(N^-3) against compact interior
   spacetime C1 tests of bounded value and first derivatives in fixed units:
   their integrand bounds are ||j||_L1tx=O(N^-6),
   ||n v^2||_L1tx=O(N^-5), and ||n-rho||_L1tx=O(N^-3).
   Primitive and conservative matter residuals agree because Rc=0.
   Field kinematic identities and field initial perturbations are exact.
   No uniform-time spatial momentum residual or strong residual norm is claimed.
8. **Local energy, boundaries, and control — passed.** For RE=partial_t E+
   partial_x S the compact spacetime C1-test bound is
   T[epsilon_N+2|mu|m_N]+||S||_L1tx ->0. Tests including t=0 add the actual
   energy trace O(N^-1) and momentum trace O(N^-2); tests including t=T have
   equally vanishing terminal density traces. Mass has its exact rho trace.
   Wall mass/current perturbations and field-velocity fluxes vanish exactly.
   A nonzero initial spatial flux measure is not an energy-density time trace.
   For v=0 the flow is identity, n=rho, and all relative energies, currents,
   displacements, and residuals vanish exactly.

## Verification record, units, and remaining implication

Verification consisted of the analytic reconstruction above, source SHA256
comparison, preservation of the original derivation, and result-contract/hash
validation. There were zero mathematical executables, experiments, samples,
parameter scans, seeds, or numerical tolerance claims. The 120-second numerical
process bound is not applicable; no CPU, memory, thread, or log limit is claimed
as enforced on a numerical process that did not exist.

l_N,L are lengths; V_N,v0 velocities; omega_N an inverse time; N,s,H are
dimensionless. Mass is per transverse area, entropy has mass-per-area units,
energy is per area, and the slab-integrated current is energy per area times
length. All asymptotic constants depend only on the fixed background,
neighborhood, coefficients, v0,L,T and reference units.

The smallest remaining implication is to supply an approximation of the actual
coupled momentum and field dynamics with a justified energy-admissibility rule.
This prescribed flow fails the exact global inequality, so its weak residual
convergence cannot serve as that existence or admissibility theorem. The exact
coupled solution, finite-nonzero-energy compactness, uniqueness, stability,
physical scale reservoir, metric/photon/DOF completion, calibrated observations,
RAR/M/filtered-MONO transfer, and historical novelty are out of scope. The
current finite-supply test is closed; any next task must change this unresolved
dynamical/admissibility gate rather than repeat the static cubic moment test.
