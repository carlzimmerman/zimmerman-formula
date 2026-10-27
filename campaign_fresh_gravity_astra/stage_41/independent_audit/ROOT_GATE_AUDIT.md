# FGF054 coordinator moment-gate audit

Normalized claim: for a fixed symmetric stationary interval of half-width
R epsilon, R>1, enclosing the prescribed polynomial velocity packet, the
strict leading-order collar/moment certificate admits a comparison coefficient
Btime exactly when (15/8)R^2 < Btime < (R-1)V/S. Optimizing only this interval
criterion over R gives V/S>15/2, attained as the least required ratio at R=2.
The resulting PDE upper bound remains conditional on actual source/field
control, existence of the classical domain used in the contradiction, and
compatibility with the specified coupled equations.

Primary verdict: **conditional on a named input** for the PDE implication;
the stated strict interval optimization itself is proved as written. The
condition V/S>15/2 is necessary and sufficient for this specified strict
leading-order certificate, not for PDE breakdown, bounded physical speed,
or any other mechanism.

## Exact exposure and evidence

The independent proof and input freeze were completed at
2026-10-06T10:49:05.892869+00:00 before any new author/root mathematical proof
exposure. Their unchanged SHA256 values are:

- INDEPENDENT_DERIVATION.md: 72add437747afe767cab6f9949dfa76049ec0ece1fe0a8f4a4080cdf48be281e
- INDEPENDENT_FREEZE.json: bcd8367f15b397a917536f1035421ea2be6e756b950b030b94dec4544bd8e94c

At 2026-10-06T10:49:41.233812+00:00 the reviewer checked the candidate hash
before first reading `campaign_fresh_gravity_astra/stage_41/coordinator/ROOT_MOMENT_GATE.md`:
4eb5c7ca5e9250ed0b0663feddffd4ec192978a34fc79c5088729527748d8f54.
This is new root exposure after the independent freeze. No new author raw
proof/result or other stage41 root file was read. The candidate itself credits
its earlier author R=2 and reviewer exterior-buffer progress previews; neither
this audit nor that candidate is characterized as blind independent discovery.
The eventual author audit must record this intervening root exposure.

## Reconstructed proof and obligations

The dependency graph is: known hydrostatic solution and characteristic
uniqueness -> exact exterior collars under a strict travel margin -> fixed
endpoint mass and pressure-retaining momentum -> positive-density first-moment
capacity -> conditional small field-transfer error -> strict interval algebra.

Let A=x*-R epsilon and D=x*+R epsilon. The distance from either endpoint to
the initial packet is (R-1)epsilon. A hydrostatic comparison cone centered
at an endpoint can have radius r epsilon with r<R-1. At time
T=Btime epsilon/V its surviving half-width is at least
[r-S Btime/V]epsilon. Some r<R-1 leaves a positive constant-times-epsilon
open collar exactly when S Btime/V<R-1. This establishes the stated strict
collar condition for these cones. It is not a universal converse about domains
of dependence with more detailed family-dependent geometry.

On every existing compact positive classical prefix, comparison along the
known H characteristics produces a coefficient-difference term times the
unknown solution's finite first derivative. The integral uniqueness inequality
therefore gives equality to H without assuming a global bound on the unknown
matter speed. This argument needs the solution on the cone; it does not create
core existence. The note preserves that distinction.

At fixed endpoints the exact collars give nv=0 and n=rho. Consequently
M'=0. The actual conservative momentum equation yields

    P'=-[nv^2+cs^2 n]_A^D-int_A^D ng
       =int_A^D(rho g0-ng),

because cs^2 rho_x=-rho g0. Thus pressure does not vanish separately; its
endpoint stress supplies precisely the background-force term. For
I=int_A^D(x-A)n, continuity gives I'=P, and n>0 gives I<M(D-A).
Writing F(t)=int_0^t int_A^D(ng-rho g0) yields P=P0-F and the note's
strict survival inequality int_0^T F > P0T-Delta0.

With y=(x-x*)/epsilon and fixed R, smooth density gives uniformly
rho(x*+epsilon y)=rho*+O(epsilon). The three exact leading integrals are

    M=epsilon int_-R^R rho(x*+epsilon y)dy
      =2R rho*epsilon+O(epsilon^2),
    Delta0=epsilon^2 int_-R^R(R-y)rho(x*+epsilon y)dy
      =2R^2 rho*epsilon^2+O(epsilon^3),
    P0=V epsilon int_-1^1(1-y^2)^2 rho(x*+epsilon y)dy
      =(16/15)rho*V epsilon+O(V epsilon^2).

The signs and factor of two are correct. All parameters in these errors are
fixed as epsilon shrinks. If the actual force satisfies |g|<=G uniformly,
|F(t)|<=M(G+sup|g0|)t, hence |int_0^T F|=O(epsilon^3).
The positive moment margin dominates this error exactly when its fixed leading
coefficient (16/15)Btime-2R^2 is strictly positive. This gives
Btime>(15/8)R^2. Equality and epsilon-dependent choices are not resolved by
this strict-leading-coefficient comparison, as the note explicitly states.

The interval is nonempty iff V/S>(15/8)R^2/(R-1). For R>1,
R^2/(R-1)=4+(R-2)^2/(R-1)>=4, with equality only at R=2.
Thus the optimized strict certificate condition is V/S>15/2. At equality
there is no strict interval; this algebra does not rule out a refined equality
analysis or other PDE mechanism. No numerical computation is needed.

Obligation matrix:

- Exact polynomial, fixed physical units and epsilon-independent parameters: passed.
- Stationary cone overlap and explicit positive collar width: passed for the stated geometry.
- Known-solution uniqueness on existing classical prefixes: passed; core existence remains separate.
- Continuity, fixed endpoint mass, pressure stress and transfer signs: passed.
- Initial mass, momentum and capacity coefficients: passed.
- Force-transfer O(epsilon^3): conditional on the named actual uniform force bound.
- Nonempty strict interval and optimization: passed in the precisely stated certificate class.
- Actual source/field closure and full lower lifespan: not supplied by this root note and correctly left conditional.
- Evolved matter speed and V<Vmax: correctly retained as obligations, not proved here.
- V=0 hydrostatic control: passed; no positive momentum certificate exists.
- Both normalizations and frozen histories: scoped correctly with separate compatible backgrounds.
- Full energy/both field fluxes: inherited model requirements, not separately rederived in this root note.
- Physical causality, metric completion, sharp PDE lifespan and novelty: out of scope.

## Safe result and remaining gap

No algebraic or domain error was found in this scoped note. Its strongest safe
standalone result is the optimized conditional certificate above. The smallest
missing PDE implication is a proof on every candidate continuation through
Btime epsilon/V of the actual compact field/source bound and propagated matter
ceiling, together with a same-domain lower construction. The independent frozen
reviewer derivation supplies a separate conservative cell but is not silently
substituted into the candidate. A later author audit must inspect the author's
raw closure and construction rather than promote this optimization alone.

Commands: one Python hashlib SHA256 check followed by source text display;
plain-file writing and final SHA256 provenance checks. Zero mathematical
executable computations, external-source lookups, numerical tests, installs,
services, or changes outside the exclusive audit directory.
