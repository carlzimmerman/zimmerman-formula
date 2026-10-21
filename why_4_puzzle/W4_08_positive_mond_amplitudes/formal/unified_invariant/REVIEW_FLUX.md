# Independent review by the flux-geometry investigator

2026-10-20. Base `431f22bd6`; criteria-only `89bf113b0`.
This is an independent action-level review of P1, P3 and the isolated
P0 vacuum variation. My authored `FLUX_GEOMETRY.md` is a separate route,
not independently certified by this review. I did not read the shared
RESULT or its verdict. No script, numerical scan, download, build,
Lean run, shared-status edit or commit was performed for this review.

## 1. Exact reviewed artifacts and source scope

All paths below are within this directory. SHA256 pins:

- `INDUCED_QUANTUM.md`:
  `2d3df2d6b09f1195b39d4ce195474406d988e8a7e4f5cb9f292e7c3984291026`.
- `SOURCES_INDUCED.md`:
  `3b8767823d429b3a410d19d8e33722cc8d0fa075e0f54d28dc59a30ca4117689`.
- `SINGLE_FUNCTION.md`:
  `a209e5d048c49ba5e9a7473fd09753784bfa9f98930dd4b0e08c8b5b481fbf2e`.
- `SOURCES_FUNCTION.md`:
  `e9edd93ffea3ed0c4781a82a4350d68755df4b1b41ff0157685a2cf91e02f907`.
- `MATRIX_MODEL.md`, section 2 only:
  `49605568df5daba99f73b57c5a41a042d5567680a81150af2d2bf85a7fb0edf1`.
- `SOURCES_MATRIX.md`, the corresponding 2026 primary card only:
  `1a8620dd2374cface7943ee44ca4da98206a59e63da20b95d5dbe27539601a94`.

I independently opened Donoghue--Menezes1712.04468v3, including its
trace-correlator and contact-term equations; Zlosnik--Ferreira--
Starkman0607411v5, including its actual static source; and Battye--
Pace--Trinh1707.06508v1, including its background stress and clock
restriction. Their exact version headers agree with the cards. The
remaining induced-gravity auxiliary cards were read as cards, not
independently reauthenticated in full. The phase/frame and finite-k
calculations below are independent derivations from the written actions.

For P0 I independently read Steinacker2601.08031v1 in both versioned
HTML and PDF text, including equations 3.9 and 3.12--14 and the
divergence-free-frame qualification. The PDF text preserves the same
sign discrepancy. A requested PDF screenshot was unsupported; no
rendered-page inspection or source-byte hash is claimed.

## 2. P1: the physical Einstein response and the current portal

The packet correctly keeps the source's +--- conventions inside its
sum rules. Its Q=Pi_AZ'(0)/12 and epsilon=Pi_AZ(0)/16 use the stated
vacuum subtraction and Yang--Mills contact prescription. I checked the
zero-moment coefficient Pi_AZ(0)/16; dropping the two-graviton contact
term instead gives Pi_AZ(0)/8. This is not an unsubtracted positive
spectral formula or a positive same-state vacuum theorem.

Independently varying the static -+++ Einstein bracket gives

    L=M^2[(grad Psi)^2-2 grad Phi.grad Psi]-rho Phi,
    2M^2 Delta Psi=rho,       Delta(Phi-Psi)=0.

With the decaying harmonic branch, Psi=Phi and

    L_reduced=-M^2|grad Phi|^2-rho Phi,
    C2=M^2=2Q,       G=1/(8pi M^2).

The trace probe therefore cannot be counted as an additional physical
scalar mediator. This is the local low-momentum Einstein response,
not a demonstrated high-gradient MOND crossover coefficient.

For the anomaly-free background U(1), varying Gamma[B+d alpha]=Gamma[B]
and integrating the infinitesimal alpha term gives div(delta Gamma/
delta B)=0 with the stated domain and boundary contract. On the static
rest congruence a=d ln N. Thus B=lambda a is pure gauge and its hidden
current response disappears exactly on that branch. The result does
not require a free determinant or a mass gap.

For B=mu u the field is not pure gauge: F_0i=mu partial_i N. Its
Maxwell term contributes +Z_B mu^2 h^2/2 to the static Lagrangian,
so C2=M^2-Z_B mu^2/2. A current electric term ell3|e|^3 instead gives
the metric energy term -ell3 mu^3 h^3. Both the altered Newton
coefficient and the required sign ell3<0 are correct for this map.
No claimed cubic or quadratic cancellation is produced by the Ward
identity, and the electric response is not silently treated as a
stable Lorentzian vacuum.

## 3. P1: total stress and retained phase/frame modes

For the written P(X)+lambda_u(u^2+1) action, vary u and g before
normalizing. On the selected rest configuration, w=d theta-mu u=-mu u,

    lambda_u=mu^2 P_X,
    T_mu nu=2(mu^2 P_X-lambda_u)u_mu u_nu+P g_mu nu=P g_mu nu.

Hence its total rest-state density is -P, whereas the fixed-B matter
density alone is mu n-P. The distinction is essential. The stable
grand-ground-state trial inequality P(mu^2)-P(0)>=0 follows directly
from minimizing H-mu Q while retaining the neutral state as a trial;
it supplies a nonpositive total shift in this particular reservoir
model, not a general assertion about all finite-density gravity.

The phase equation must also hold. In an expanding homogeneous FRW
state it requires partial_t[a^3(2mu P_X)]=0 on this constant-X rest
ansatz. At H>0, fixed mu and fixed nonzero P_X are therefore not a
stationary expanding solution. The stress cancellation is a local
homogeneous-rest diagnostic, not by itself a constructed de Sitter
medium. Choosing theta constant describes the selected rest state;
one cannot arbitrarily gauge transform theta and keep B=mu u fixed
at the same time. These state qualifications were sent to the author
and are incorporated in the final pinned packet.

Directly substituting u_0=-sqrt(1+v^2), u_i=v_i gives

    X=mu^2+2mu pi_dot+pi_dot^2-(grad pi)^2+2mu v.grad pi+O(3).

The v^2 terms cancel. With A=P_X+2mu^2P_XX, B_p=P_X and positive
Maxwell coefficient K, I independently obtain

    A K omega^4-B_p K k^2 omega^2-2mu^2 B_p^2 k^2=0.

For A,B_p,K>0 and nonzero k its omega^2 roots have negative product.
This is a genuine instability of the specified flat minimal model,
not a result for a curved, higher-derivative or otherwise completed
frame theory. The B_p=0 endpoint is degenerate and is not certified.

## 4. P3: actual de Sitter constraints and boundary

The background lapse variation and stress agree with the stated
action: 3H^2=m^2(2IF'-F)/2 and
p=-epsilon-3B c2(F'+2IF'')Hdot. At constant H the varied stress is
vacuum-like. I reconstructed G(K)-K G_K=0 at the root and
G_KK=-4/3+2c2 Q, with Q=F'+2IF''. Since delta K=3U-b, the extra
quadratic term c2 Q(3U-b)^2 added to the Einstein trace bracket gives
exactly the reported lambda_eff and S coefficients.

For lambda>1, solving the actual shift and lapse gives

    C=2S/(lambda-1), D=CH^2+alpha X,
    b=SU/(lambda-1), n=(CH zeta_dot-2X zeta)/D.

The mixed term has boundary a^3(2CHX/D)zeta^2. With Xdot=-2HX its
coefficient derivative divided by a^3 is
2CH^2X(CH^2+3alpha X)/D^2. Subtraction gives independently

    K_z=C alpha X/D,
    V_z=2X^2[C(alpha+2)H^2+alpha(2-alpha)X]/D^2.

Both are positive for finite nonzero k, lambda>1 and 0<alpha<2.
The friction H+2alpha HX/D is positive, and the stated fixed-mode
late-time boundedness argument has integrable coefficient errors.
This does not give a uniform-in-k estimate, nonlinear or quantum
health, a cutoff, or a regular homogeneous kinetic limit.

The source comparison also passes. In the stipulated subcurvature
slow-source window, Psi=Phi and G_bg=G_bare/(1-alpha/2). This is a
linear weak-source response about the actual nonzero-I0 state; it
cannot be replaced by a flat-I=0 square-root source law. The alpha=2
endpoint cannot use this division, and a cusp at I0 has a singular
expansion Hessian because delta I=(6c2H/m^2)delta K.

I checked the opposite-branch deformation directly:

    2I g'-g=(I+4/I)exp(-1/I^2),
    dH^2/deta=m^2(2I0 g'-g)/(3S).

Its nonzero derivative and unchanged I>=0 action are correct for the
stated smooth class. They do not assert permission under an additional
microscopic analyticity principle. The explicit toy has F=-8/3,
F'=1,F''=0 at I0=-1, H=m/3, lambda=2,alpha=1 and c_s^2=1/5.
Its flat a=m/3 and C3=2B/m agree, but are not same-state weak-source
MOND data. No healthy-halo counterfamily or physical R follows.

## 5. P0: independently resolve the isolated vacuum sign

Hold rho_M and V0 fixed and put v=sqrt|G|, k=rho_M^2 V0. Then

    S_v=-int k/v,
    delta v=-(v/2)G_mu nu delta G^{mu nu},
    delta S_v=-(1/2)int (k/v)G_mu nu delta G^{mu nu}.

Under the source's equation 3.9 definition this is unambiguously

    T_v,mu nu=+rho^-4 V0 G_mu nu.

Its trace reverse is -rho^-4 V0 G_mu nu. Substitution back into 3.9
gives the positive frame variation printed in 3.13; the minus metric
tensor in printed 3.14 gives the opposite variation. The versioned
PDF contains this same disagreement, so it is not an HTML-only issue.
For -+++ a valid isolated vacuum-form tensor here has epsilon=-rho^-4V0.

The source's frame is divergence-free, with multiplier ambiguity, and
its simplified equations omit further sectors. An unrestricted local
Hilbert variation of this isolated term is not a complete derivation
of the constrained matrix background stress. In particular a varying
rho makes this isolated tensor nonconserved by itself. Restoring
constraints, dilaton/axion, internal-modulus dependence and the other
background equations is necessary for a full gravity conclusion.
The report's narrow sign warning and refusal to identify positive V0
with positive physical dark energy are therefore warranted.

## 6. Review outcome

The independent raw calculations above agree with the packets under
their stated ensemble, background, boundary and EFT conditions. The
P1 expanding-phase qualification is now explicit in its final text,
without altering its algebra. No reviewed packet establishes a
healthy same-state positive MOND response with a selected invariant.
No target number, universal no-go, full microscopic health statement
or end-to-end Lean proof is certified. The standing goal remains open.
