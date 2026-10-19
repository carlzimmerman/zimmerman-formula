# Photon-integration normalization: companion restriction

Frozen author files are preserved. This is a generality restriction on sea_flavor
DERIVATION.md equation (8), and an explicit correction to the reviewer's own
PRETARGET_DERIVATION.md generic vacuum formula. The intended charge-conjugation
invariant QCD vacuum has zero one-current means and is unaffected.

Let N(eta)=<B(eta) exp L(eta)>, Z(eta)=<exp L(eta)>, Z(0)=1,
C(eta)=N(eta)/Z(eta), and mu_a=<L_a>=Z_a(0). Author equation (2), the
fixed-source Hessian of C, is exact for arbitrary mu_a. The full normalized
observable after integrating a canonical centered Gaussian photon is instead

    C_full(e) = E_A[N(e A)] / E_A[Z(e A)].

For G_ab=E[A_a A_b], quotient differentiation after Gaussian integration gives

    partial_u C_full|0 = (G_ab/2)[N_ab-C0 Z_ab]+C_u,ct
      = (G_ab/2)[C_ab+C_a mu_b+C_b mu_a]+C_u,ct
      = (G_ab/2) C_ab + G_ab C_a mu_b + C_u,ct,
    u=e2.

Consequently equation (8) applies when G_ab C_a mu_b=0, in particular when
mu_a=0. Without that restriction its numerator must include the additional
term G_ab C_a mu_b; the finite-T mass formula acquires the corresponding
-lim(1/T) G_ab C_a mu_b/C0. Averaging C(eta) with an unchanged free-photon
weight would omit the source dependence of the photon marginal measure.

A direct independent two-configuration exponential example has weights 2/5,
3/5 and source-coordinate x data

    B1=2+3x+x2, B2=-1+x,
    L1=x+x2,   L2=-2x.

It gives mu_x=-4/5, C_x=99/25, C_xx=802/125. The full integrated second
coefficient before multiplying G_xx/2 is 2/25, and

    2/25-802/125=-792/125=2 C_x mu_x.

The complete two-coordinate version, including mixed source derivatives, is
checked in check_independent.py and independent_run_001/result.json. This
finite example diagnoses the omitted normalization term; it is not a physical
QCD ensemble or counterexample to the intended C-invariant application.

The unconditioned photon-integrated vacuum functional W=-log E_A[Z(eA)] has

    W_u|0 = -(G_ab/2)[<L_ab>+<L_a L_b>]+W_u,ct.

Thus author equation (9) correctly uses the **uncentered** product, retaining
mu_a mu_b. By contrast, the Hessian of -log Z(eta) at a prescribed source is
-[<L_ab>+Cov(L_a,L_b)]. These differ by -mu_a mu_b. The reviewer's preliminary
vacuum formula used the latter Hessian before photon integration and omitted
that distinction; this companion explicitly corrects that preliminary line.
No pretarget file is silently rewritten.

Author equation (10)'s metric derivative of the correct photon-integrated
vacuum insertion remains valid. Charge conjugation on the full background
family gives mu_a(g)=0 throughout that family and also removes its metric
derivatives. Current, seagull, photon-kernel, measure and local-counterterm
metric contacts are still required, as the author states.
