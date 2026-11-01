# TP02 threshold/RG contract

Frozen before numerical RG-improved execution. Inputs: the unchanged TP01
complete canonical-K SU(5) spectrum and its representation blocks, the raw
MV28 action, and the TP02 coordinator contract. No old science is edited.

First establish rather than assume the one-loop reduced Callan-Symanzik
identity. With Delta=30h^2+lambda^2, U0=f^2lambda^2/Delta, the complete
threshold logarithm must satisfy beta1.dU0=STrM^4/(32pi^2). The retained
field is canonical X at the reference scale; transported X(t) obeys
dlnX/dt=-gammaX. On the re-minimized classical valley T=sqrt(Delta)X/lambda
obeys dlnT/dt=-gamma_eff, whereas a(t)=sqrt(2fh/Delta) does not equal the
transport of the original heavy A background. This distinction is an
order-two matching issue and must be reported.

Reference trial inputs: f(Q0)=1, Q0=1, h(Q0)=lambda(Q0) in
{.01,.03,.05,.1}, g(Q0)=sqrt(29/200)*lambda(Q0). The critical gauge relation
is only an input comparator at Q0, never reimposed on the running flow.
All h,lambda,g,f and the X field run; the complete finite one-loop spectrum
is evaluated on the running classical valley. The pressure portal remains
the old exp(2s) comparator defined with s at the reference field coordinate,
not a microscopic coupling derived here.

Evaluate matching scales Q=eta*Mref(X0), eta={.5,1,2}, with Mref a stated
positive smoothly varying physical tree threshold proxy, also Q=Q0 as a
fixed-scale comparator. Use Mref=sqrt(c0)*sqrt(1+z0^2),
c0=f0 h0 lambda0^2/Delta0,z0=h0X0/sqrt(c0), covering the field-dependent
heavy threshold while remaining nonzero at the origin. This is a scale
prescription, not new dynamics. Restrict radial searches to a declared
compact interval around the TP01 dimensionless minimum7.36714 and its
pressure boundary; retain missing roots or failed pressure gates.

Controls: exact CS identity and field transport dictionary; full-threshold
Q derivative; RK4 characteristic step refinement; independent log-field
derivative stencils/direct differentiation; scale variation; old fixed
one-loop limit. Use fifty-digit arithmetic. Every evaluated mass must
remain real nonnegative in the rigid tree spectrum; explicitly retain
light sectors. Canonical X,T wavefunctions are not identified with constant
canonical s.

Higher-order scope: RG-resummed one-loop with specified beta/gamma functions
is not a complete finite two-loop threshold result. Where feasible include
the logarithmic terms required by the reduced CS equation through two-loop
order, separately from the unknown finite two-loop reduced potential and
heavy-valley displacement. Do not use scale variation as a proved bound
on an unknown finite matching function. Another worker reconstructs the
beta/gamma functions independently; that exact interface will be pinned
before its use. No selected UV coupling, gravity completion or occupied
material state is presumed.

Execution: one numerical thread, at most180 wall seconds per run and
170 CPU seconds, no enforced unsupported affinity/address-space limit;
report measured RSS. Contracts precede each finite extension, outputs use
fresh v2 runner directories, failures are preserved. No installations,
downloads, production jobs, queue changes or Git mutations.
