# Persistent singular rank-one pencil and actual Morse modes

19 October 2026. Owner `/root/actual_dressed`. Base HEAD supplied by coordinator: `62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Parent scratch `/private/tmp/halo_actual_dressed_20261019.md`, SHA-256 `dfe7f9b8577f428ba44ba9ffb68e11f76e35ac05050b10f2057757fe70697436`. This is a separate new scratch artifact; the parent note and existing review packets were not edited. Analytic only; no scientific code, numerical integration, arrays, or process operations.

**Outcome.** The rank-one Fredholm pencil has a complete algebraic classification. With an additional explicitly stated reciprocal finite-part pairing, persistent singularity for the actual shell operator reduces to a nonzero homogeneous threshold field with zero critical trace. That field need not be an energy-space eigenmode. If it is an eigenmode, energy integrability at the two-dimensional Morse point does not establish bounded receiving work: a bounded kinetic quotient, equivalently quadratic domination by the Morse detuning, is a genuine extra condition. Projection removes a pole only after the energy mode is identified and does not by itself prove a regular reduced boundary inverse. No actual threshold mode is asserted to exist or be absent.

## 1. Complete Fredholm pencil lemma

Let `Y` be a complex Banach space, `A:Y->Y` Fredholm of index zero, `v in Y` nonzero, `ell in Y*`, and

    A_c=A-c*v tensor ell,  c in C.

Put `N=ker A`, `N*=ker A'` (the annihilator of `Ran A`), and `d=dim N=dim N*`.

**Lemma.**

1. If `d=0`, `A_c` is invertible exactly when `1-c*ell(A^-1 v)!=0`.
2. If `d>=2`, every `A_c` is singular. In particular `ker A intersect ker ell` has dimension at least `d-1` and is a common kernel.
3. If `d=1`, choose nonzero `n in N`, `psi in N*`. Some `A_c` is invertible if and only if `ell(n)!=0` and `psi(v)!=0`. When these two couplings are nonzero, every `c!=0` gives an invertible `A_c`.
4. Consequently, when `A` is singular, **every** `A_c` is singular if and only if

       ker A intersect ker ell !={0}
          or ker A' intersect {psi:psi(v)=0}!={0}.             (P)

The two alternatives in (P) are different in general; persistent singularity need not imply a common kernel without an additional reciprocal structure.

**Proof.** Part 1 is direct rank-one inversion. Part 2 follows because every functional on a space of dimension at least two has a nonzero kernel. For part 3, a vector `n` with `ell(n)=0` remains in every kernel. A cokernel functional `psi` with `psi(v)=0` annihilates every `Ran A_c`. Conversely assume both couplings nonzero and `c!=0`. If `A_c x=0`, applying `psi` gives `ell(x)=0`, then `Ax=0`, then `x=0` because `ell(n)!=0`. Rank-one perturbations preserve the Fredholm index; hence injectivity gives invertibility. This also proves part 4, including all multiplicities.

This proof does not assume that `A` is selfadjoint or diagonalizable. In particular it does not infer a common kernel from the determinant of a nonnormal finite-dimensional surrogate.

## 2. A reciprocal conditional reduction appropriate to the actual shell operator

The actual species order is `(t,f)`, `w_i=-F_{i,E}>0`, `dm=2*pi*C_Gamma*dJ*dL`, `C_Gamma=4*pi^2`, `nu_{ik}=k*Omega_i`, and `nu_c=n*Omega_j(q_c)>0` at one eccentric interior nondegenerate minimum. The physical kernels remain

    P_ff=P_ft=P_tf=-G/max(r,r'),
    P_tt=2*(G^2/a_0)*integral_{max(r,r')}^infinity M_t(s)*s^-4 ds.

Let `e_c` be the real signed zero-mass orbital measure with `ell(phi)=integral phi de_c=phi_{j,n}(q_c)`, and let

    beta=4*pi^2*C_Gamma*nu_c*w_j(q_c)
              /(n*sqrt(det D^2 Omega_j(q_c)))>0,
    v_0=-beta*P e_c,
    A=I-P T_+,

where `T_+` denotes the *regular finite-part source operator at the threshold*, after the leading local source `-beta*Lambda*e_c tensor ell` has been removed. This is the same sign convention as the parent note.

To avoid differentiating arbitrary `C^gamma` fields, use source duality, not the derivative form involving `H^-1`. The following explicit domain conditions suffice:

- take `Y=C^gamma(I)^2` with `0<gamma<1/2`;
- `T_+` and `T_-` are bounded source maps from `Y` to its continuous conjugate dual, with `T_+^*=T_-` in the sesquilinear source pairing;
- their imaginary form is the regular-channel optical form

      Im <phi,T_+ phi>
          =-pi*nu_c*sum_regular integral_(nu_{ik}=nu_c)
                w_i*|phi_{i,k}|^2*(2*pi*C_Gamma)
                   d sigma/|grad nu_{ik}| <=0;                (D)

- the corresponding jump source vanishes on a field whose regular resonant traces vanish; equivalently `T_+ phi=T_- phi` for such a field;
- the physical reciprocal `P` acts on these source duals and its source pairing is symmetric: `<S,P T>=<P S,T>` with the usual anti-linearity convention.

These are independent finite-part pairing assumptions. They do **not** follow just from norm continuity of `R=P T_+` on `Y`, and no ordinary inverse of `A` is used here.

There is a local justification for their use on compact eccentric charts: the actual `P` is jointly Lipschitz; interpolation gives `P:Y*->C^(1-gamma)`, compactly into `Y` for `gamma<1/2`. Symmetric smooth kernel approximations converge in the mixed `C^gamma` kernel norm, since the error is `O(epsilon^(1-2*gamma))`; hence dual symmetry extends from ordinary measures. The local Morse finite-part bilinear form subtracts the constant coarea density `beta*conjugate(ell(phi))*ell(psi)`; the remaining density is `O(s^(gamma/2))` and is integrable after division by `s`. At each regular channel the same bilinear form is an ordinary principal value with Holder numerator. The high-harmonic nonresonant tail is bounded by orbitwise Parseval and Cauchy-Schwarz. **A complete global verification, particularly at circular/support-edge channels, is not claimed here.** Alternatively one can work with finite signed source measures if their existence and the boundary pairing are separately established.

**Conditional actual corollary.** Under these pairing assumptions, `A` is Fredholm of index zero, and

    every A_c=A-c*v_0 tensor ell is singular
       if and only if D=ker A intersect ker ell is nonzero.    (AD)

**Proof, independently of the ordinary-inverse construction.** Compactness follows from `P:Y*->Y` compact and `T_+` bounded. Let `n in ker A`, and put `S_n=T_+ n`; then `n=P S_n`. Reciprocity makes `<n,T_+ n>=<P S_n,S_n>` real. By (D), every regular resonant trace of `n` vanishes, so `T_+ n=T_- n`.

Define a continuous cokernel functional by the source pairing

    psi_n(y)=<S_n,y>.

Using `T_+^*=T_-`, equality of the two sources on `n`, and reciprocity of `P`, one obtains

    psi_n(Ay)=<S_n,y>-<P S_n,T_+ y>
             =<S_n,y>-<n,T_+ y>=0.

The map `n -> psi_n` is conjugate-linear and injective: if the source functional `psi_n` is zero, then `S_n=0` and `n=P S_n=0`. Since the kernel and cokernel have equal finite dimensions, it identifies them. Finally

    psi_n(v_0)=-beta*<S_n,P e_c>
               =-beta*<n,e_c>
               =-beta*conjugate(ell(n)).                     (C)

Thus a common cokernel annihilating `v_0` is present exactly when a common kernel annihilated by `ell` is present. Apply (P) to obtain (AD). This proof explicitly supplies the boundary-pairing step missing from a mere appeal to an ordinary inverse; if the stated pairing assumptions have not been verified, (AD) must remain conditional.

## 3. What quotienting the persistent dark kernel does, algebraically

Continue under the reciprocal assumptions, and set `D=ker A intersect ker ell`. Let

    R_D={y in Y:psi_n(y)=0 for every n in D}.

Then `A_c D=0`, `Ran A_c subset R_D`, `v_0 in R_D`, and `ell` descends to `Y/D`. The induced frozen pencil

    Abar_c:Y/D -> R_D

is Fredholm of index zero and is invertible for at least one finite `c`.

To see this, `D` has dimension `d` if `ell` annihilates all of `ker A`, and dimension `d-1` otherwise. In the first case the induced `Abar_0` is already invertible, since its domain kernel and range cokernel have both been removed. In the second case the induced kernel and cokernel are each one-dimensional, with nonzero rank-one coupling by (C), so part 3 of the pencil lemma applies. This is a quotient statement for a **frozen** finite-part operator, not a bound for the physical frequency-dependent resolvent.

For an inhomogeneous equation `A_c x=f`, the quotient requires the compatibility conditions `psi_n(f)=0`, `n in D`. The aligned logarithmic source is compatible at leading order because `psi_n(v_0)=0`. Its regular forcing need not be compatible. At nearby frequencies `A(z)-A(nu_c)` can couple the dark subspace back to the complement; Holder continuity alone does not control the inverse of the resulting small finite-dimensional matrix. Hence quotienting a persistent kernel does not by itself prove a projected limiting-absorption estimate.

## 4. Actual interpretation: threshold response versus energy eigenmode

If `n in D`, its critical coefficient `n_{j,n}(q_c)` is zero. Other regular resonant traces vanish under (D). The formal kinetic amplitude is

    u_{i,k}(q)=nu_{ik}(q)*n_{i,k}(q)/(nu_{ik}(q)-nu_c),
    h=-w*u.

On compact positive-weight eccentric charts, Holder regularity and the zero traces make each resonant term locally `L1`: a regular resonance has `|u|<=C*|s|^(gamma-1)`, while the Morse point has `|u|<=C*r^(gamma-2)` and two-dimensional area `r dr dtheta`. Both are integrable for `gamma>0`. Thus, **once the global source pairing/integrability is justified**, `n=P h` describes a homogeneous distributional threshold response. It is not automatically an eigenvector of the conserved-energy generator.

At the Morse point `nu-nu_c` is comparable to `r^2`, where `r=|q-q_c|`. If the numerator `N(q)=n_{j,n}(q)` is `C^1`, local energy integrability implies

    N(q_c)=0,  grad N(q_c)=0.                                (E)

A nonzero value gives an `r^-3 dr` divergence of `|u|^2 dm`; a nonzero gradient gives a logarithmic `dr/r` divergence on an angular sector. If `N in C^(1,eta)`, `eta>0`, the two zero jets yield `N=O(r^(1+eta))` and local energy integrability. But for `eta<1` this only gives

    u=O(r^(eta-1)),

which may be unbounded. The actual energy-to-field estimate supplies only `C^(1,1/2)` radial fields; smooth eccentric orbit extraction transfers at most this regularity to actions. Consequently the already proved field regularity and energy integrability do not force quadratic vanishing. This is a regularity obstruction to an implication, not construction of an actual singular eigenmode.

If the full `h` is in the energy space and the eigen-equation holds there, it is an actual neutral eigenmode at `nu_c`. Positive conserved `Q` permits it. If `h` has infinite energy, a `Q`-orthogonal spectral projection cannot remove it; it remains a possible threshold resonance requiring separate analysis.

## 5. Exact necessary and sufficient quotient for the work of one mode

Suppose an actual neutral mode has field `exp(-i*nu_c*t)*n`. On a receiving orbit with frequency `omega(q)=k*Omega_i(q)` and detuning `delta=omega-nu_c`, its receiving work coefficient is

    W_k(t,q)=-i*nu_c*n_{i,k}(q)
                       *integral_0^t exp(i*delta*s) ds.

For `delta!=0`,

    sup_(t>=0) |W_k(t,q)|
                      =2*nu_c*|n_{i,k}(q)|/|delta(q)|.        (MW)

At `delta=0` it is zero if the receiving trace vanishes, and grows linearly otherwise. Thus, on a compact receiving chart where all exact resonant traces vanish, uniform receiving work for this mode is equivalent to

    sup_(q:delta(q)!=0) |n_{i,k}(q)|/|delta(q)| < infinity.   (BQ)

At the Morse extremum, (BQ) is precisely the quadratic domination `|N(q)|<=C*|q-q_c|^2`. This is weaker than requiring a smooth quotient but stronger than energy integrability or zero first jets in `C^(1,eta)` for `eta<1`. A `C^(1,1)` numerator with (E), or a `C^2` numerator with (E), does imply (BQ). At a regular resonant curve, `C^1` numerator plus vanishing trace gives (BQ) by division in a transverse coordinate; this is why the previous regular-frequency mode argument does not automatically extend to a Morse point.

There is also a necessity statement for a proposed theorem covering **all** smooth compact canonical data. If an energy eigenmode has an unbounded local label `h_nu/w` on a compact positive-weight eccentric receiver set, an estimate uniform in time for the full work of every such datum cannot hold. Indeed a uniform work bound gives a uniform label bound there by the exact orbit endpoint identity and the uniform field bound. The Cesaro averages

    (1/T)*integral_0^T exp(i*nu_c*t)*h(t) dt

converge in the energy space to the `nu_c` spectral projection. On a compact set with `w` bounded below, division by `w` preserves local `L2` convergence, while the averages inherit the uniform `Linfinity` label bound. Their limit must therefore have a bounded label. Smooth compact canonical data are dense in the energy space; the projection onto the finite-dimensional field kernel is onto, so one can choose such data with any prescribed eigenprojection. This contradicts an unbounded-label eigenmode. This argument is conditional on existence of such an actual eigenmode; none is constructed here.

Removing an eigenprojection from the continuous part can therefore support a full work theorem only if either its modal work is separately bounded by (BQ), or the admissible data are explicitly restricted to have zero projection. Removing it formally is insufficient. Even after this issue is settled, a regular reduced boundary inverse must still be proved.

## 6. Status and continuation

- **Proved as written:** general Fredholm rank-one pencil classification; exact single-mode work quotient; energy integrability versus quadratic domination at a two-dimensional Morse extremum; the spectral-average necessity argument under its stated actual-mode hypothesis.
- **Conditional on explicit pairing inputs:** actual kernel/cokernel identification, characterization (AD), and the frozen quotient reduction. The proof avoids the derivative pairing on arbitrary `C^gamma` fields and does not reuse an unavailable ordinary inverse.
- **Open:** global finite-part source pairing at all boundaries, existence or absence of any threshold response, energy membership of any such response, modal quadratic domination, and a projected dynamic limiting-absorption theorem.

The cheapest next mathematical discriminator is to establish the quadratic receiving quotient for every energy member of the actual dark threshold kernel, or show that a particular member violates it. A regularity upgrade from the actual integral equation to `C^(1,1)` action coefficients would suffice together with the zero jets, but no such upgrade is proved here. For nonenergy threshold responses, spectral projection is unavailable and an independent finite-part/resonance analysis is required. This is a bounded checkpoint, not a claim that the route is exhausted.

Review provenance: self-review only. Parent and fresh auditor should independently check the duality assumptions before applying the actual corollary. The algebra and work identity do not depend on that corollary.

## 7. Inputs and hashes

SHA-256 at reading; repository paths are relative to `/Users/carlzimmerman/new_physics/zimmerman-formula`.

- `/private/tmp/halo_actual_dressed_20261019.md`: `dfe7f9b8577f428ba44ba9ffb68e11f76e35ac05050b10f2057757fe70697436`.
- `reviews/latest_results_push_2026_10_19_codex/KINETIC_SCREENING.md`: `2e5c6fa7d535b64b4e4c6188a5a8d1a70d59aa40dfe8808f468227a646214ddd`.
- `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md`: `ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4`.
- `CLAUDE_HANDOFF_KINETIC_CONFINEMENT_2026-10-19.md`: `2af7be5626d3c90b7fe646f1cab4ff60fdb3bab15eefcbd644250f809823de71`.

No external source or novelty claim. Only text reads, analytic derivations, creation of this scratch file, and a SHA-256 check were used in this continuation.
