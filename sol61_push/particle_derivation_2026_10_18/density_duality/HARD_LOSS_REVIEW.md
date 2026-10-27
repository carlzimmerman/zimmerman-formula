# Independent audit of the hard source-pair loss calculation

**Normalized claim:** the original cubic gives the stated leading vacuum
tree kernel for X_+ X_- -> Phi_+ Phi_-, its decay-rate comparison and the
integrated weighted-number defect for the specified homogeneous dilute
decay-plus-annihilation stock.

**Primary verdict: proved as written**, within the narrow-quasiparticle,
tree, vacuum, factorized-occupation and toy-stock assumptions stated in
../micro_response/HARD_NUMBER_LOSS.md. This is an independent algebra and
implementation audit by a separate agent with shared context. The stored
finite run was inspected and validated, not independently rerun. No full
reaction-network, cosmological production, conserved positive microscopic
mass, density-response or halo theorem follows.

## Independent amplitude and normalization reconstruction

The X vertex has two identical daughter legs, hence factor -2ig. Charge
flow forces the outgoing Phi_+ leg to the X_+ vertex and the Phi_- leg to
the conjugate vertex. The remaining charged daughter propagator connects
those two vertices. There is exactly one graph at this order for these
specified charge labels; there is no allowed alternative u graph to add.

For t=(P_X+ - K_Phi+)^2,

\[
 \mathcal M=-{4g^2\over t-m^2},\quad
 t-m^2\big|_{p=0}=-M^2,\quad
 |\mathcal M_0|^2={16g^4\over M^4}.
\]

The two incoming charges are distinct, as are the two outgoing charges.
Their event count is n_+ n_- sigma v, with no factor 1/2. Combining
1/(4E_1E_2) with integrated two-body phase space beta_f/(8 pi) gives

\[
 \sigma v_{\rm rel}={|\mathcal M_0|^2\beta_f\over32\pi M^2}
   ={\beta_f g^4\over2\pi M^6},\qquad
 \beta_f=\sqrt{1-m^2/M^2}.
\]

At nonzero CM p, the reconstructed denominator is -(A-Bz),
A=M^2+2p^2, B=2p sqrt(M^2+p^2-m^2). Its discriminant
A^2-B^2=M^4+4m^2p^2 is positive. Integrating its inverse square over
z gives the note's finite-p CM expression. The flux velocity is 2p/E;
this is the incoming invariant/Moller flux convention, not the final
daughter speed. No real intermediate pole is hidden in the angular range.

In contrast, X_+ -> Phi_+ Phi_+ has identical final daughters. Including
the one factor 1/2! yields

\[
 \Gamma_{\rm dec}={g^2\beta_{\rm dec}\over8\pi M},\qquad
 \beta_{\rm dec}={u_*\over\sqrt{1+u_*^2}},\qquad
 {\Gamma_{\rm ann,+}\over\Gamma_{\rm dec}}
    ={4 n_{X-}g^2\beta_f\over M^5\beta_{\rm dec}}.
\]

The density is per opposite sign; a neutral total source stock must be
divided by two. These factors, the exact beta_dec and the source/daughter
momentum scales all agree. The numerical conversion multiplies sigma v
in GeV^-2 by (hbar c)^2 c and divides a GeV width by hbar. The benchmark
reconstruction uses the stated identical-boson contact normalization and
g^2=lambda_rep (M^2-4m^2)/r_lambda. The recorded values are consistent:
sigma v=5.54765517e-25 cm^3/s and Gamma_dec=2.84013679e12 s^-1.

## Weighted stoichiometry and the integrated toy stock

The event vector (-1,-1,+1,+1) in source+/source-/daughter+/daughter-
order has exact signed-charge moment zero. Its positive weighted moment
is -2 when the hard daughters are counted, and -4 in the soft-only EFT.
Ordinary unweighted quasiparticle number happens to be unchanged here.
Each final daughter has momentum sqrt(M^2-m^2)>sqrt(3)m and is hard.
Thus no approximate soft-current conservation follows just from exact
signed charge conservation; all receivers are part of energy accounting.

For the stated neutral per-sign stock, let kappa=sigma v and
alpha=kappa n0/Gamma. Directly from
dot n=-Gamma n-kappa n^2,

\[
 \int_0^\infty n\,dt={\log(1+\alpha)\over\kappa},\quad
 {N_{\rm ann}\over n_0}=1-{\log(1+\alpha)\over\alpha}.
\]

The initial soft weighted stock is 4n0, so its fractional defect is this
same expression; the all-mode weighted defect is half as large. The
integral identity

\[
 \alpha-\log(1+\alpha)=\int_0^\alpha{x\over1+x}\,dx
\]

proves 0<epsilon_soft<alpha/2 for every alpha>0, with small-alpha behavior
alpha/2-alpha^2/3+O(alpha^3). The two exact derivative checks in run 002
agree with this proof. The numerical <= upper comparison is appropriate:
at tiny alpha the strict analytic gap can round away in binary64. It is
the integral proof, not floating strictness, that establishes the bound.

This supplies a controlled **single-channel** conditional example for the
emergent current. It does not establish alpha for an actual prepared
production state, the absence of inverse/hard populations, or a bound on
pure-daughter 4->2 and other allowed losses. A replenished source reservoir
cannot use this integrated depletion formula.

## Checks, limits and exact artifact pins

| Obligation | Status |
|---|---|
| Unique graph, cubic factors and sign | Passed by independent charge-flow/amplitude calculation |
| Final-state symmetry and incoming event count | Passed; annihilation charges distinct, decay daughters identical |
| Threshold and finite-p phase-space kernel | Passed by independent CM/angle integration |
| Decay beta and per-opposite-density ratio | Passed, including stated unit conversions |
| Full versus soft weighted defects and energy | Passed with the hard receiver retained |
| Integrated neutral-stock formula and strict bound | Passed analytically under the toy assumptions |
| Author implementation and 34 stored controls | Passed by code/output audit; not rerun |
| Complete physical current-conservation hierarchy | Not established and not claimed |

Final reviewed source SHA-256 values:

| Artifact within micro_response/ | SHA-256 |
|---|---|
| HARD_NUMBER_LOSS.md | a8275b0d793b31e39ec6bbc8ab60ed88bf2248573f7bca4dbc9bd82b3552c421 |
| check_hard_number_loss.py | 5a371f1079dc06c42302abddf18e1b3acdf0ea3a43d8929a057d2148b30caf77 |
| hard_number_loss_contract.json | 0c43ca1452e3f6970af32760241f4cd407a7dc0e9cd62b61c3d1b5888de23b84 |
| hard_loss_run_002/results.json | 94cd8173733fcd2c53331232f6b4b23c8a815e450a2857736b75e8518a5ade1a |
| hard_loss_run_002/manifest.json | 7ea440e81b3fd61f732bc9a502c2ebf5b85acb97f3cb8be5692c5f1d61f765f7 |

Executed the installed mathbox computation-audit validate_manifest.py on
hard_loss_run_002/manifest.json with the project root. It returned a valid
evidence record, run status completed; all 34 recorded checks pass. The
actual code and results were read in full within this assigned bounded
scope. No external theorem, novelty claim, all-channel search or numerical
kinetic simulation was needed for this algebraic audit. No author file
was edited by this reviewer.
