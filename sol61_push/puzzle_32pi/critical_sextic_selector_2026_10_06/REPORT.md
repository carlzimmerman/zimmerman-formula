# Critical sextic coupling: a real quantum coefficient, not yet a gravity selector

The genuine large-N Bardeen–Moshe–Bander (BMB) critical coupling is **g₆=(4π)²**, distinct from the large-N ultraviolet fixed point **g₆*=192** in the declared canonical normalization. The critical leading-order gap equation allows an arbitrary mass and has flat relative vacuum energy; it does not fix a positive gravitational vacuum offset. A stable classical sextic auxiliary coupled to the source invariant eliminates to the opposite static cubic-energy sign from the inherited gravity candidate. These are specific missing arrows, not a no-go for all quantum completions.

Base requested `1db53a670a09a76c023e70784fddc5f351fb8a81`; exact inherited source hashes are in provenance.json. The actual symmetric covariant dictionary is retained as a comparison, not replaced with an O(N) quantum action.

## Primary normalization and quantum limits

Use canonical kinetic energy and potential g₆(φ²)³/(6N²). The modern primary convention is η(φ²)³/6!, so

    g₆ = ηN²/120,
    ηbar = ηN²/[(4π)² 5!] = g₆/(16π²).

The checked v1 equations (20)–(22) give β_ηbar=(24ηbar²−2π²ηbar³)/N+O(N⁻²). Consequently ηbar_BMB=1 and ηbar_UV=12/π² are different. In particular the BMB value is not a zero of the displayed finite-1/N beta coefficient. The numerical coefficient 192 is the leading UV value in this normalization, not an exact statement at arbitrary finite N. [Modern primary v1](https://arxiv.org/pdf/2502.07880v1), equations (1), (20)–(22), (76), (79).

The original paper's stability bound and distinction from 192 are independently visible in equations (8)–(9). Its nonperturbative discussion is not silently identified with the modern finite-1/N conclusion. The modern paper reports that the strict leading-order BMB phenomenon disappears at next order; this report neither recomputes that result nor treats the leading-order flat direction as a full finite-N phase theorem. [Original BMB primary](https://lss.fnal.gov/archive/1983/pub/Pub-83-053-T.pdf).

## Independent leading-order gap and energy reconstruction

At the tricritical point (vanishing mass and quartic relevant couplings), set ℏ=1 and define the subtracted composite per field ρ=⟨φ²⟩/N. In three Euclidean spacetime dimensions,

    ρ(m)=∫d³p/(2π)³ [1/(p²+m²)−1/p²]
        =−m²/(2π²)∫₀∞ dp/(p²+m²)=−m/(4π).

This renormalized ρ is negative; it is not a negative bare squared field or a gravitating mass density. The large-N cactus equation m²=g₆ρ² gives

    m²[1−g₆/(16π²)]=0.

At g₆=16π² every m≥0 satisfies this equation. With the same subtraction, the composite saddle functional is

    E_LO/N = g₆ρ³/6 − m²ρ/2 + (1/2)∫ln(p²+m²)
           = m³/(24π)[1−g₆/(16π²)],

because the mass-dependent determinant term is −m³/(12π). Its m derivative supplies the same stationary condition. At criticality its entire m direction is flat, with zero relative energy. Adding a constant E₀ changes neither stationarity nor the critical coupling and leaves E_LO=E₀ there. Thus neither a positive vacuum offset nor the selected mass is supplied by LO criticality. A dimensional-transmutation scale or a finite cutoff boundary condition would be additional input, not a value derived from this flat equation. Away from criticality this LO expression has a massless minimum below the critical value and is unbounded along m above it; these are LO properties, not a finite-N instability theorem.

The 4π in the gap calculation comes from a **three-dimensional Euclidean loop momentum** integral. It is not the solid angle of the physical three-space gravitational Gauss law merely because both numerical factors contain π.

## Cheapest source-coupling diagnostic

Declare a classical local static energy, independently of the quantum composite action,

    E(ψ,z)=E₀+κ[gψ⁶/6−hzψ²/2],  κ,g,h>0, z≥0.

For z>0 the real minima are ψ=±(hz/g)^(1/4). ψ=0 is unstable there. Their curvature and eliminated energy are

    E_ψψ|min = 4κhz >0,
    E_min(z)=E₀−κ h^(3/2) z^(3/2)/(3√g).

At z=0 the sextic minimum is ψ=0 with **zero quadratic gap**; the potential is stable but degenerate. The source-dependent minimum vanishes continuously and the source susceptibility is singular at zero. No nonzero vacuum oscillator mass or cold population follows from this classical branch.

In the inherited symmetric gravity source envelope M_eff=−A_off+z/2−z^(3/2)/12+…, the nonlinear static energy contribution has the opposite sign to M and therefore a **positive** z^(3/2) coefficient. The displayed stable sextic minimum instead gives a negative coefficient. Reversing the entire toy energy makes the cubic positive but turns its nonzero stationary point into a local maximum and makes the energy unbounded below. This comparison is explicitly about the declared static-energy ensemble, not an identification of all gravitational action terms with a positive Hamiltonian.

A useful changed-ensemble control is the Legendre conjugate in q=ψ²≥0:

    sup_q κ[hzq/2−gq³/6] = +κ h^(3/2)z^(3/2)/(3√g).

It produces a positive cubic as a dual/source-work functional, rather than the same energy minimum. A gravitational use would need the actual varied source/flux action and reciprocal matter force. This is a plausible construction ingredient, not a completed covariant bridge.

Even granting g=16π² by a separate coupling identification, the coefficient is proportional to κ h^(3/2)/(12π). The independent source normalization h and additive E₀ remain free. Rescaling h changes the acceleration response without changing the proposed critical quantum g. Thus assigning a target coefficient to h would insert the normalization that the selector was meant to derive.

## Dimension, ℏ and inherited vacuum dictionary

For a canonically normalized scalar in D spacetime dimensions, [φ]=(D−2)/2 and the sextic coupling has mass dimension 6−2D: it is classically marginal only at **D=3**. The inherited physical three-space gravity model has D=4, where the sextic coefficient is dimensionful. A reduction to a three-dimensional effective quantum sector, its cutoff and its embedding would have to be declared and derived; the primary critical number does not provide them.

As a loop-counting bookkeeping check, restoring a factor ℏ in each tadpole gives ρ=−ℏm/(4π) and gap m²=g₆ℏ²m²/(16π²) with unchanged canonical action coefficients. Thus the dimensionless critical combination is g₆ℏ² in that declared convention. This is not a units-complete dictionary relating a₀, measured Newton coupling, Λ, ℏ and a physical mass. No such dictionary is inferred here.

The inherited conditional vacuum relation is Λ/a₀²=χ_n A_off/2; imposing its UV normalization sets A_off=2C_resp(λ). The present quantum equations select neither λ nor C_resp, and the toy E₀ is not demonstrated to equal A_off in the same action. A numerical resemblance between 16π², 192 or a power of π and 32π therefore closes no gravity implication.

## Evidence and status

checks.py supplies 28 exact SymPy identities/sign checks: normalization, beta roots, convergent tadpole, gap and flat energy, offset freedom, dimensional counting, classical minima and their curvature, sign reversal and positive Legendre dual. Three controls test a falsely fixed critical mass, a positive stable-minimum cubic and conflation of BMB with the UV root. Source authentication is separate from these computations. Full NLO quantum dynamics, gravity coupling, cold abundance and observed cosmology are not implemented. Current manifests and execution results are reconciled in RUNS.md; REPORT is outside executable inputs.

The door supplies a genuine quantum critical coefficient and a potentially useful dual cubic, but the proposed selector is incomplete at the explicit source/energy/dimension/vacuum matching steps above. No all-model exclusion or world-novelty claim is made.
