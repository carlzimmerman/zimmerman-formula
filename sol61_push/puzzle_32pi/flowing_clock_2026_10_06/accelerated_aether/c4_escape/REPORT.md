# Separate c4 action class: the sign reversal has a transverse-vector price

This is a changed action class, not a correction to the frozen previous run. Parent phase base07fa64b44891fc87697f53f86812287946481586. Add a shared-invariant term with the explicitly chosen convention +c4(A^mu nabla_mu A_nu)², so beta=c4-c1=1+c4 and

    K=[-theta²/2+beta a²-2omega²]/M²,
    S=E/2 int sqrt(-g)[R+M²F(K)+lambda(A²+1)]+S_m[g].

Matter remains minimally coupled. Standard references sometimes use the opposite c4 sign; beta is the physical acceleration coefficient here. Background omega=0, while perturbative transverse velocities and vorticity are retained. All principal and continuous-path hypotheses are those in the parent accelerated report.

## Shared F: scalar comparison versus an uncoupled vector

With h=F_K,s=F_KK/M², the exact quadratic aether derivative density is

    h[-(delta theta)²/2+beta(delta a)²-2(delta omega)²]
      +2s[-theta delta theta/2+beta a dot delta a]².

Thus ell=1+h/2-s theta²/2 is unchanged as a function of theta, while eta_ij=beta h delta_ij+2beta²s a_i a_j and the mixed vector is u_i=-beta s theta a_i. For k perpendicular a, all constraints give

    C=beta h, j=-(n-1)P/C,
    Kzz=(n-1)(n ell-1)/(ell-1).

The scalar restriction is unchanged when C is nonzero. At fixed negative K=-z,

    theta²=2(M²z+beta a²),
    ell_theta=ell_geo-beta(a²/M²)F_KK.

Positive beta therefore preserves the previous comparison and continuous-path obstruction. Negative beta reverses the inequality and could superficially keep ell above one; this is why c4 deserves an actual sign check.

In n=3 there is a physical transverse vector perpendicular to both a and k. It has delta theta=0, a dot delta a=0, so the F_KK mixing does not touch it. After the auxiliary metric transverse shift is eliminated, its principal density is

    beta h vdot²-h|grad v|².

Positive kinetic and spatial energy necessarily require h>0 and beta>0. If beta<0 and h>0, it is a ghost; choosing h<0 instead makes the spatial gradient energy negative. Hence the sign needed to reverse the scalar comparison is unavailable for a healthy shared-F two-derivative vector sector in this class. This is a necessary condition, not sufficient full health.

At beta=0, the vector time kinetic degenerates. Also the isolated theta=omega=0 invariant is identically K=0 for every gravitational acceleration. Static variation gives

    mu=1-beta F_K/2,
    div(mu gradPhi)=rho/(2E),   d=4.

Thus beta=0 has mu=1 and deletes this isolated aether MOND source operator. A negative beta with positive h likewise cannot reach the required critical mu(0)=0. The nonlinear source normalization and vector sign provide independent diagnostics.

## Independent acceleration operator and its degeneracy boundary

Consider instead adding M²G(a²/M²) outside the original F. It changes eta_ij by Gprime delta_ij+2Gdoubleprime a_i a_j/M², but adds no trace Hessian and no theta*a mixing. For perpendicular k, the scalar restriction remains Kzz=A whenever C=h+Gprime is finite and nonzero. This cannot repair an ordinary negative-A point merely by changing vector or lapse coefficients. Take G(0)=0 when preserving the original vacuum-root equation; otherwise its value is a changed vacuum offset.

There is an essential exception. At C=0, the old Schur division is invalid: the lapse becomes a multiplier imposing P=partial_k zeta=0 for nonzero k. The constraint rank changes and the prior negative scalar restriction is no longer a permissible reduced mode. This is a genuine degenerate/constrained escape that has NOT been audited for generic orientation, preservation under evolution, strong coupling or source matching. No theorem here rules it out. To traverse a whole ghost interval without a regular negative-A point would require this degeneracy wherever that interval is encountered, not merely a cancellation at an unrelated endpoint.

A further combined shared beta<0 plus independent G is another new theory, and the simple vector sign no-go no longer applies because Gprime can repair beta h. There is nevertheless an endpoint price for the old family. Let kappa0=Gprime(0), with G(0)=0. Necessary zero static stiffness for exact deep MOND gives beta h0+kappa0=2; this is a necessary condition, not a sufficient cubic source law. On its linear cosmological endpoint,

    eta_cos=beta hL+kappa0=2+beta(hL-h0).

For beta=-1 and the old h0=200/101,hL=1/10, eta_cos>2. The full constrained geodesic scalar has ell=1+hL/2>1 and gradient coefficient4/eta_cos-2<0, hence a cosmological gradient instability. This excludes that particular simple compensation with those same endpoints; changing F or a noncritical source floor changes the premise.

## Evidence and checkpoint

The analytical shared-c4 escape is closed under the declared regular positive-energy requirements: beta>0 preserves the perpendicular ghost-path obstruction, beta<0 has an untouched transverse ghost, and beta=0 deletes the isolated MOND operator. Independent acceleration degeneracy remains open as a changed constraint class, not silently excluded.

checks.py verifies the exact shared Hessian, perpendicular constraint reduction, beta comparison, physical source mu, compensating endpoint and the C=0 new constraint. Fresh version-2 runs below runs authenticate actual inputs; the sign-flip control reverses the claimed untouched transverse kinetic coefficient. No on-shell source solution, observational test or 32pi selector is established. SOURCE_PROVENANCE.json pins the unchanged parent derivation and prior action family.

Main_a passes11/11; flip_vector_a passes9/11 and rejects the wrong transverse kinetic sign and its false negative-beta health claim. Both manifests validate, input hashes unchanged. Caps wall30s,CPU20s/process,1MiB logs,one cooperative thread; no memory/affinity cap.
