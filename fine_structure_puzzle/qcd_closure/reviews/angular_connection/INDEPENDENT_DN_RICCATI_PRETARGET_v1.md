# Independent pre-target reconstruction: DN and Riccati

Written before reading RAW_DERIVATION_v1.md or any author constants, 2026-10-19 UTC. Author proof files have only been listed. Scope supplied by parent: a Hermitian angular radial operator with fixed orthogonal projector Q, V >= p(p-1)/r^2 I+h(r)^2 Q, V <= B/r^2 I+Q, p=J-1, R>=4, h>=1/2 for r>=2.

## Domain qualifications

The DN conclusions require P(R) to be the Friedrichs/regular-origin variational DN matrix of -u''+Vu=0, not an arbitrary positive Riccati solution. Assume J>=1, u(0)=0 in the energy sense, and V is locally admissible. Mere positivity of P does not select this normalization. For example V=0 and P(r)=epsilon/(1+epsilon*r) are positive Riccati solutions with arbitrarily small P(R), contradicting P(R)>=c/R. A general B supplies no J-uniform upper constant unless B=O(J^2).

## Variational lower bound with constants derived independently

For q=max(1,p), q(q-1)=p(p-1) for p in the nonnegative integers except p>=1, where q=p. Completion of the square gives the scalar DN lower bound q/R on every component:

 integral_0^R (|u'|^2+p(p-1)|u|^2/r^2) >= (q/R)|u(R)|^2.

Here q>=J/2 for J>=1. On [R/2,R] the charged mass is at least 1/4. Dropping all other positive energy and allowing free data at R/2 gives charged endpoint energy >=(1/2)tanh(R/4)|Q u(R)|^2 >=(1/2)tanh(1)|Q u(R)|^2. Thus P >=(q/R)I and P >=c0 Q, c0=(1/2)tanh(1). Taking their half sum yields

 P >= J/(4R) I +(1/4)tanh(1) Q >= (1/8)(J/R I+Q).

The last bound uses tanh(1)>1/2. This is intentionally a convenient, nonoptimal constant. It does not presume commutation of P and Q.

## Variational upper bound

Let a=(1+sqrt(1+4B))/2, so a(a-1)=B, and let a>=1. For boundary vector v, choose

 u(r)=(r/R)^a [(I-Q)+exp(r-R)Q]v.

The neutral trial energy for B/r^2 is a/R. In the charged block, w=(r/R)^a exp(r-R) obeys w''/w=B/r^2+2a/r+1, hence integration by parts gives energy for B/r^2+1 no larger than w(R)w'(R)=a/R+1. Consequently

 P <= (a/R)I+Q <= max(a/J,1) Z, Z=(J/R)I+Q.

If B<=b J^2 then a/J<=1+sqrt(b), a usable uniform bound. No matrix simultaneous diagonalization is used: the comparison potential and this trial path are diagonal in the *fixed* projector Q.

## Exact noncommuting Riccati identity

For P'=V-P^2, P0'=V0-P0^2, D=P-P0, W=V-V0,

 D'=W-PD-DP0.

If E_P(R,s) is the fundamental propagator solving d_R E=-P(R)E and F_P0(R,s) solves d_R F=-F P0(R), then

 D(R)=E_P(R,s)D(s)F_P0(R,s)+integral_s^R E_P(R,t)W(t)F_P0(R,t) dt.

This ordered formula is valid without commutativity. If P,P0 >=mJ/r I, their Euclidean propagators satisfy ||E||,||F|| <=(s/R)^(mJ), giving

 ||D(R)|| <=(s/R)^(2mJ)||D(s)||+integral_s^R(t/R)^(2mJ)||W(t)||dt.

After scaling, ||Z(R)^(-1/2)D(R)Z(R)^(-1/2)|| <=(R/J)||D(R)||.

This elementary estimate is insufficient by itself to prove a sharp J-uniform exponential tail/connection remainder. Earlier forcing survives as an algebraic neutral mode. Any stronger weighted estimate needs a separately justified argument. In particular, P>=cZ does not permit treating Z^(-1/2)P Z^(1/2) as Hermitian or replacing its Hermitian part by cZ: P and Q need not commute.

## Moving boundary and fixed core normalization checkpoints

A moving relative boundary must be applied to the actual wall block and neutral Schur complement after the charged block is removed. A constant rotation or an assumed purely Dirichlet endpoint changes the determinant. A connection determinant additionally requires a fixed origin normalization and a specified reference normalization. Positivity and coercivity alone do not fix that multiplicative constant. These are independent obligations when the target is read.
