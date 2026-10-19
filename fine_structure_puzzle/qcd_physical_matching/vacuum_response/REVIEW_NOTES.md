# Self-review and exact remaining obligations

Review scope: new DERIVATION.md, REPORT.md, checks.py and source extraction, 2026-10-19. Verdict for the finite-regulator identities: proved as written under the differentiability and source convention stated in Section 1. Verdict for a physical-QCD small-H extraction: conditional on its explicitly named uniform saddle, continuum, contact and differentiated-limit inputs. Verdict for determination of full A_rho: incomplete.

Dependency checks:

1. W_theta_theta=<Q^2> uses the regulated source +i theta Q, CP at theta=0, and no omitted theta-dependent source-only action. Passed at that specified regulator convention.
2. Q_t=Q_(e^2)=0 uses a geometric connection definition of integer charge. Passed for the smooth closed continuum object; naive finite-lattice/rounded Q needs additional treatment.
3. Metric covariance identity follows from normalized differentiation. Passed algebraically and by an independent direct finite-ensemble Taylor expansion.
4. The order-e^2 mixed identity includes I_t=Tcal_(e^2). Passed; omitting it changes the answer.
5. AFHO gives a normalized Fourier saddle. Exact source authenticated and extracted; applying it uniformly to QCD on the sphere is conditional. Fixed Q is not the typical-Q scaling regime; no termwise sum of its asymptotic series over all Q is used.
6. The H^5 coefficient in the Q=0 sector difference follows from Dlog chi=(a_chi/chi0)H+o(H). Passed under differentiated asymptotics. The non-Gaussian contribution is O(H^3) in X_top only with bounded cumulants and differentiated remainder.
7. All topology observables are blind to a common theta-independent factor. Passed as an information statement; not asserted as an admissible change to microscopic QCD.
8. Flat chiral/current data and flow EMT definitions do not supply the missing contacts/radius response. Primary source domains checked. No exhaustive absence or novelty claim.

Proofreading: self-review of all new mathematical prose and displays. Routine edits: clarified fixed-Q versus sector summation and source-defined contacts. Mathematical-token changes: none made during the final proofreading pass. Unresolved issues: physical inputs in items 2,5,6 and evaluation of the unconditioned stress. Validation: run_001 completed, 37 exact checks; manifest validation successful. This does not certify a physical QCD limit.
