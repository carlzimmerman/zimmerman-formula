# FGF055 coordinator refinement audit

**Normalized claim.** For each fixed finite physical cell with V>0, fixed Btime>0, and a positive classical solution on the fixed interval [A,D]=[x*-2epsilon,x*+2epsilon] through T=Btime epsilon/V, assume the full Q/scale/isothermal-fluid equations, compatible smooth hydrostatic background, initial n=rho and the stated exact polynomial velocity packet. Assume uniformly in epsilon that n<=Nbar, |g-g0|<=Cg epsilon throughout the slab, and at both endpoints |v|<=Cv epsilon² and |n-rho|<=Cn epsilon². Then the exact variable-mass capacity identity in the target holds, and its two dynamical error terms are O(epsilon^4). The original leading capacity gap remains rho*[(16/15)Btime-8]epsilon².

**Primary verdict: conditional on a named input.** The named input is the actual full-system, epsilon-uniform density/field/endpoint bounds just stated on the required classical slab. All algebraic identities and the conditional estimates checked here pass. This audit does not prove those inputs or accept FGF055 as a whole. There is no internal sign or order defect identified in this refinement.

## Scope, provenance and source pins

Reviewer: `/root/fgf055_refinement_audit`, a separate narrow audit attached to FGF055. The coordinator note expressly credits an author progress preview; its derivation is not a blind discovery. This reviewer saw the assignment, the target note, the task specification and pinned FGF054 derivation, but no new FGF055 author proof or other reviewer proof. The target was verified against the assigned hash before its contents were read. Sources were pinned before use:

| Role | Repository-relative path | SHA256 |
|---|---|---|
| Target | `campaign_fresh_gravity_astra/stage_42/coordinator/ROOT_MOMENT_REFINEMENT.md` | `f76e4eb4d3c173fec403d7fcdf54bd6deacf920b63d02d3d13bb27f3258eccf0` |
| Task | `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/tasks/FGF-055.md` | `a06015358472e6f8b4b0c90ec8a88a433687e58f01acb468e04e1ce393369346` |
| Actual equations | `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-054/fgf054_run_001/DERIVATION.md` | `947d5fa84514f1bba8bedc96da98f9b2049ec56ea2e08cc1f3bde7c4724b3a09` |

FGF054 §§2,6,7 provide equations (2.1), the hydrostatic equations (2.2), and momentum/energy definitions. Those local identities were re-derived below; its stationary collars, field estimates and maximal-germ theorem are not imported. No external theorem or literature mechanism is used. No applicable AGENTS.md was found in the checked repository/target ancestry, and no root `.mathbox` ledger was present. Writes are confined to this audit folder.

## Dependency graph and obligations

Full equations + classical regularity -> local continuity/momentum and integration by parts -> exact variable-mass capacity identity.

Hydrostatic compatibility + initial n=rho -> exact force subtraction and initial mass reference.

Assumed endpoint velocity + assumed density ceiling -> O(epsilon³) mass drift -> exact mass-defect force split. Assumed field deviation + smooth background + density ceiling -> O(epsilon²) remaining bulk force. Assumed endpoint density -> O(epsilon²) pressure residual. These -> O(epsilon^4) integrated dynamical error.

Original polynomial packet + smooth rho -> initial moments -> strict leading gap when Btime>15/2. The full field equations separately imply boundary momentum/energy balances; neither boundary balance is set to zero.

| Obligation | Result |
|---|---|
| Continuity, momentum, first-moment and capacity signs | Passed |
| Hydrostatic pressure subtraction | Passed |
| Exact mass-defect decomposition | Passed |
| Uniform O(epsilon^4) dynamical estimate under inputs | Passed conditionally |
| Actual derivation of density/field/endpoint bounds | Not addressed; named input |
| Full field stress and both field energy fluxes retained | Passed |
| Stationary P+field-momentum conservation used | No; correctly excluded |
| Initial constants and strict Btime threshold | Passed |
| New existence, restart or maximal-domain theorem | Out of scope |
| Fast-field-uniform constants or numerical verification | Not claimed |

## Decisive derivation

Write [h]=h(D)-h(A), L=D-A=4epsilon, j=nv and Qm=nv²+cs²n. From n_t=-j_x and j_t=-(Qm)_x-ng,

    M'=j(A)-j(D),
    P'=-[Qm]-int ng,
    I'=-[(x-A)j]+int j=P-L j(D).

Thus Delta=LM-I=int(D-x)n>0 and Delta'=L j(A)-P. The right endpoint current cancels in this combination, not separately. Hydrostatics gives cs²[rho]=-int rho g0, so P'=-R for exactly the target R. Integrating P(t)=P0-int_0^t R(s)ds gives

    Delta(T)=Delta0-P0 T+int_0^T(T-t)R(t)dt
                               +L int_0^T j(A,t)dt.

All signs therefore match, including the positive left-current term.

Initial n=rho implies M0=int rho. With g*=g0(x*), expansion and regrouping give identically

    int(ng-rho g0)=int n(g-g0)+g*(M-M0)
                                      +int(g0-g*)(n-rho).

There is no density perturbation estimate hidden in this equality. In particular, positivity and the density ceilings alone give int|n-rho|<=4epsilon(Nbar+rhobar). For K0>=sup|g0_x|,

    |M(t)-M0|<=2Nbar Cv epsilon² t,
    |int n(g-g0)|<=4Nbar Cg epsilon²,
    |int(g0-g*)(n-rho)|<=8K0(Nbar+rhobar)epsilon².

The endpoint pressure and kinetic contributions obey respectively

    |cs²[n-rho]|<=2cs² Cn epsilon²,
    |[nv²]|<=2Nbar Cv² epsilon^4.

Set a=4Nbar Cg+8K0(Nbar+rhobar)+2cs²Cn. Without absorbing orders, the entire dynamical remainder is bounded in absolute value by

    a epsilon² T²/2
      +Nbar Cv² epsilon^4 T²
      +|g*| Nbar Cv epsilon² T³/3
      +4Nbar Cv epsilon³ T.

With T=Btime epsilon/V these four terms have orders epsilon^4, epsilon^6, epsilon^5 and epsilon^4. This proves the target's O(epsilon^4) claim for fixed V>0 and fixed physical coefficients, without density gradients, total variation or interior pointwise smallness of n-rho. It also distinguishes the O(epsilon³) instantaneous mass-defect force from its O(epsilon^5) contribution after time weighting.

Direct integration of f=(1-y²)² gives int_-1^1 f=16/15. Smoothness of rho yields Delta0=8rho*epsilon²+O(epsilon³) and P0T=(16/15)rho*Btime epsilon²+O(epsilon³). For fixed Btime>15/2 a classical slab satisfying all inputs through T contradicts Delta(T)>0 when epsilon is sufficiently small. Equality Btime=15/2 is undecided. This conditional contradiction supplies neither the actual input estimates nor a lower existence time or a maximal-domain definition.

## Full field accounting

Use p=phi_t, g=phi_x, w=chi_t, k=chi_x, a=a_ref exp chi and Tscale=-W_chi. The pinned full equations are

    g_t=p_x, tau p_t=(B_Q)_x-Cn,
    k_t=w_x, sigma w_t=Jk_x+Tscale-U_s', chi_t=w.

With mf and Sf defined exactly as in the target, differentiation gives

    mf_t+Sf_x=ng.

The decisive sign is (g B_Q-W)_x=g(B_Q)_x+Tscale k. This cancels the scale term in mf_t; the U_s' k terms also cancel. Consequently

    (P+int mf)'=-[nv²+cs²n+Sf].

Even mf(0)=0 does not imply int mf=P0-P: the missing quantity would be -int_0^t[nv²+cs²n+Sf]ds. The target correctly retains this stress term and does not invoke stationary-collar conservation.

For an arbitrary fixed density reference nref, set e=cs²n(log(n/nref)-1). This reproduces the pinned normalized convention when nref=1. The complete densities and flux are

    E=nv²/2+e+n phi
        +(tau p²/2+W+sigma w²/2+Jk²/2+U_s)/C,
    F=nv[v²/2+cs²log(n/nref)+phi]-(p B_Q+Jwk)/C.

Fluid plus interaction has source +np, the Q part has source -np-Tscale w/C, and the scale part has source +Tscale w/C. Thus E_t+F_x=0 and (int E)'=F(A)-F(D). Both p B_Q and Jwk remain. The narrow hypotheses give no license to delete or generally bound the full boundary energy/stress terms; the capacity proof does not require doing so. Autonomous fixed a_ref is essential to this stated energy accounting.

## Remaining gap and strongest safe statement

The refinement is valid as a conditional estimate, including for arbitrarily fast but fixed finite field speeds. It is not uniform as those speeds diverge. The next necessary check belongs to parent FGF055: prove the actual density/field bounds on a contained full-speed cone and the exterior fluid trace bounds for the same solutions and horizon. Those proofs must retain the density source, scale response and varying background, without assuming the interior gradient/variation bounds that this refinement avoids. Compatible existence/restart and any lower-time claim remain separate obligations.

V=0 is a separate exact hydrostatic control; no epsilon/V formula applies there. Each a0 value and each individually frozen history uses its own compatible background and constants. No evolving-reference, physical metric/photon/two-DOF, criterion B, empirical or novelty conclusion is supported by this audit.

Verification was analytic. Administrative commands used `shasum -a 256` before source reads, then rechecked all three pins and JSON syntax after writing. No mathematical executable computation, service, installation, commit or outside-folder write was performed. Self-proofreading covered this entire audit and its JSON companion; no source mathematical tokens were edited.
