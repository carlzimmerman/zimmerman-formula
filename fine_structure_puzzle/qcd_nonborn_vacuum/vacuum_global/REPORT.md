# Unconditioned QCD vacuum: new source audit and Weyl-contact estimator

The full physical A_rho(alpha), R=A_rho/m_p^3 and alpha remain uncalculated.
This package obtains a contact-complete nonperturbative observable for the
unconditioned sphere measure, its exact charge response and a measurable
bound. No hadron gap or controlled sector is promoted to a full QCD zero.

For t=log(H^-1), X=S_t, Y=S_tt and J=S_u with u=e^2, define

    E=<Y-4X>-Var X=W_tt-4W_t=4V rho_t.

If the physical small-H expansion has the explicitly controlled differentiated
remainder, A_rho=-lim H^3E/(4Omega), Omega=8pi^2/3. This observable cancels
the extensive flat vacuum term exactly. Local Einstein terms give only O(H)
contamination in the extracted coefficient; local curvature-squared and
constant W terms cancel. A common global r^3 action remains visible through
the mean contact term, even when every normalized sector probability misses
it. Measuring only trace variance would lose that information.

The exact charge response has a compact form. Put
F=Y-4X-(X-<X>)^2. Then

    E_u=<Y_u-4X_u>-2Cov(X,X_u)-Cov(F,J).

Thus |E_u| is bounded by
|<Y_u-4X_u>|+2 sigma_X sigma_Xu+sigma_F sigma_J on a positive measure.
All metric/current/measure/matching contacts are part of these quantities.
This supplies a finite-H bound and an omitted-insertion variance criterion,
with no numerical QCD moments invented. A global bound E,E_u=O(H^-3+delta),
delta>0, would imply zero coefficients if the required limits exist; neither
that cancellation nor differentiated uniformity is proved for physical QCD.
The independent full third-Weyl-derivative projector and its mixed fourth
cumulant response are also derived in DERIVATION.md.

These formulas add action contacts, joint cumulants and a quantitative bound
to the earlier FSP-006 finite-radius projectors. The old stencil itself,
forced/unconditioned wall distinction, pion zero coefficient, compact Haar
integral and weak-sphere answer are inherited, not rerun or renamed.

A new primary acquisition checked the accepted [Braguta et al.,
2602.20970v2](https://arxiv.org/abs/2602.20970v2), Phys. Rev. D 113,
094507 (2026), and its companion proceedings
[2603.01754v1](https://arxiv.org/abs/2603.01754v1). The accepted paper uses
thermal SU3 gluodynamics in a finite zero-curvature Rindler region, open
along z and periodic along x,y,tau. Its measured Polyakov-loop and spatial
transition observables supply no round-S4 vacuum metric derivative. The
source's alpha is acceleration, not electromagnetic charge. Its scale setting
also imports a string-tension calibration. The exact source-to-target
dictionary and PDF/text hashes are in SOURCE_RECEIPTS.json.

The actual source action does give a nonperturbative restricted result:
on a symmetric finite domain Z(eta)=Z(-eta), eta=a_acc a_lat, so W_eta(0)=0.
Its Hessian is 2 beta <sum z^2 E_x> minus the variance of
beta sum z(B_x-E_x). The explicit second action derivative is indispensable.
This is finite-regulator reflection symmetry, with an analytic neighborhood
shrinking as the z extent grows; it is neither a sphere coefficient nor an
unconditional infinite-volume exclusion of |acceleration| behavior. The
already audited Yamamoto source is inherited without a redundant new audit.

Run runs/weyl-001 completed 221 exact rational checks: 16 five-state
normalized ensembles, both Weyl projectors and their charge derivatives,
c-number normalization terms, Cauchy-Schwarz component bounds and a
reflection-paired source-action fixture. Independent -log Z formal Taylor
derivatives were compared with set-partition cumulants. The v2 manifest
validates against unchanged declared inputs. Runtime was 0.130115 seconds;
wall/CPU/output/thread caps were 35 seconds, 25 seconds, 64 KiB and one
conventional numerical thread. No address-space or affinity cap was used.
The finite calculation verifies the algebra and implementation in its stated
range, not any unknown QCD expectation value or asymptotic bound.

The physical leaf remains an absolutely normalized common-theory S4 measure
with X,Y,J,X_u,Y_u joint data, continuum control and uniform radius/charge
limits. First compare the contact cumulants against actual radius reweighting
and the inherited stress stencil, then test the explicitly stated cancellation
bound. No usable source supplying those data was acquired in this bounded
search; this is not a nonexistence or novelty claim. Review provenance is
self-audit plus exact finite checks; a separate independent review is not
claimed by this worker.
