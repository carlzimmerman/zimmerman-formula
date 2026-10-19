# Independent derivation of the matrix discriminator

Coordinator review, begun from Carone arXiv:2512.12044v1, Tables I-II and Eqs. (3)-(5), (8), (16)-(18), and the raw charge transcription in FSP-U. The derivation below was made before reading the route author's final report. It is an independent algebra review within the same agent team, not an external referee report or independent quantum-gravity calculation. Final input hashes are recorded in REVIEW_INPUTS.json.

## Claim card and verdict

Assume B is a fixed symmetric positive-definite charge-trace matrix, F=16 pi^2 f_g>0 is constant, and the one-loop phenomenological flow above the gravity crossover is

dH/dt=(H B H-F H)/(8 pi^2), with H positive definite and t=log(mu).

The claims about its full-rank fixed point and its continuum of UV-complete solutions are **proved as written under this ODE assumption**. The application to a fundamental gravity completion is **conditional on a named input**: the actual universal gravity correction, its coupled critical surface and the physical matching problem. These are two different claim cards, not a proof of the existence of that UV theory.

## Derivation

For invertible H the fixed-point equation implies B H=F I, so H*=F B^-1 uniquely. It is positive definite. Linearizing yields delta(H B H-F H)=F delta H, hence every symmetric-matrix perturbation at this point has physical flow eigenvalue F/(8 pi^2)=2 f_g. These directions are UV repulsive; using the usual critical-exponent convention theta=-eigenvalue gives theta=-2 f_g. The route script multiplies the beta vector field by 16 pi^2, so its three eigenvalues 2F have the same meaning. Holding f_g fixed is an essential hypothesis.

Define X=B^(1/2) H B^(1/2)/F. Then dX/dt=2 f_g(X^2-X). Every eigenspace remains invariant, and an eigenvalue x solves dx/dt=2 f_g x(x-1). For 0<x0<1,

x(t)=x0/[x0+(1-x0) exp(2 f_g t)],

which approaches zero in the UV. The value x=1 stays fixed; values above 1 develop a finite positive-time pole. Thus 0<=X<=I is the positive-semidefinite UV-finite cone of this constant-coefficient flow, and the fixed points are orthogonal projectors in X coordinates. In two dimensions the full-rank fixed point is unique, while rank-one projectors have a continuous orientation.

The continuum can retain an interacting Abelian UV endpoint: for a fixed rank-one orthogonal projector P, X(t)=P+x(t)(I-P) remains positive definite at every finite time and tends to P. This establishes non-uniqueness without relying only on trajectories whose entire Abelian sector is Gaussian in the UV. To demand the full-rank endpoint is an additional physical branch condition.

At a rank-one boundary the change from triangular couplings G to H=G G^T ceases to be a local diffeomorphism. The eigenvalue for a vanishing gY in G coordinates is -f_g, while the corresponding H eigenvalue is -2 f_g because H depends quadratically on that vanishing coupling. There is no contradiction with the route script's rescaled triangular spectrum (-F,0,2F). One must not equate boundary eigenvalues across this singular coordinate change.

## A charge-based correlated test

For a nonzero top and bottom fixed point in the restricted third-generation truncation, subtracting beta_t/y_t and beta_b/y_b cancels the common left-doublet contribution, the common universal Yukawa gravity term and the non-Abelian gauge terms. The result is

y_t*^2-y_b*^2=q_u^T H* q_u-q_d^T H* q_d,

where q_u and q_d are right-handed charge vectors in the same fixed basis as B. This relation is a UV statement, not a relation between the measured quark masses without RG evolution.

For B-L, B=[[41/6,16/3],[16/3,11]], det B=841/18, q_u=(2/3,1/3), q_d=(-1/3,1/3). Direct inversion gives H*/F=[[198,-96],[-96,123]]/841. The charge-norm difference is 2F/841, and the surviving hypercharge gY*^2=6F/41. Hence their ratio is 41/2523. For chi, B=[[41/6,-2/9],[-2/9,497/27]], H*/F=[[2982,36],[36,1107]]/20369; the norm difference is 18F/20369 and the ratio to gY*^2 is 123/20369. These two ratios eliminate F and constitute a conditional correlation test. They are not the Standard Model-only ratio 1/3.

## Source application and exact gap

Carone's Eq. (8) sets F using the empirically evolved hypercharge coupling; the quoted critical F in Eq. (13) consequently is not an alpha prediction. The assumptions on linear gravity, scheme and truncation uncertainties are explicit near Eq. (1). I checked these source passages and the charge table directly in the versioned PDF. The matrix result sharpens what those assumptions select; it does not remove them.

The remaining implication is to fix the appropriate gravity/branch/crossover data independently, obtain viable scalar and flavor trajectories, and match the unique physical photon to alpha(0). A fit of gravity parameters to measured Yukawas can test a correlated relation but remains conditional on the input extraction, scalar model and declared crossover. No independent audit of the full numerical inverse boundary-value solver is claimed in this proof review; its convergence and holdout result have their own computation records.
