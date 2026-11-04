# AZ23 — exact causal kernel for the critical clock

κ = ½ FITTED; not theory closed

**PASS** for the conditional linear-response calculation, **FAIL** for normalization selection within that linear problem, **NO VERDICT** for the nonlinear physical mechanism, **NOT EVALUABLE** for physical κ. These verdicts apply separately to canonical and alt; neither footing is used as a cosmological input. No full requirement or RQ3 row is established.

Criteria commit: 6a5e4dec1b. This is an explicit time-dependent continuation of K748, not another static endpoint run. The older endpoint analysis left time-dependent evolution open. Scope: its inherited quadratic scalar action, a nonzero Fourier mode, de Sitter H>0, and an infinitesimal conserved comoving baryonic density. Such a probe expands with the background; it is not a stationary galaxy. The validity of the cusp's quadratic reduction and the quantum cutoff remain conditional inputs.

## Derivation

After eliminating the shift, retain the lapse n and curvature perturbation ζ:

    L/a³ = B/2 {6(ζdot−Hn)² + X(2ζ²+4nζ+2n²)} − ρn,
    X = k_com²/a²,  Xdot = −2HX,  ρdot = −3Hρ.

Lapse variation gives n=(6Hζdot−2Xζ+ρ/B)/D, D=6H²+2X. The source-dependent part of the reduced action is

    L_source/a³ = −6Hρ ζdot/D + 2Xρ ζ/D − ρ²/(2BD).

Its last term is independent of ζ, but must not be dropped when checking the lapse reconstruction. The kinetic coefficient is K=6X/(3H²+X). Varying the reduced action, including derivatives of both a³ and X, yields

    ζddot + H[1+2X/(3H²+X)] ζdot
      + 2H²X/(3H²+X) ζ
      = ρ/(6B) (X+9H²)/(X+3H²).

Set y=sqrt(X)/H>0, so ydot=−Hy and ρ=BH² Q y³. The two homogeneous modes and one particular solution are

    u=y,    v=y²−3,    ζ_p=Q y³/12=ρ/(12BH²).

Their time Wronskian is −Hy(y²+3), nonzero on the declared domain. Thus for t≥s the causal Green function is

    G(t,s) = [y(t)(y(s)²−3) − y(s)(y(t)²−3)]
             / [H y(s)(y(s)²+3)],

and G=0 for t<s. It has G(s,s)=0 and ∂_t G(s+,s)=1. For any specified forcing within this linear theory, convolution with G gives the zero-initial-data solution. For the conserved probe the complete solution is ζ=ζ_p+A y+D0(y²−3), with A,D0 fixed by initial data. The reconstructed lapse is n=−ζ_p−A y−D0 y². D0 is an integration constant, not the lapse denominator D.

At fixed comoving mode and future time, y tends to zero: the homogeneous curvature approaches a constant plus a decaying term. At subhorizon y≫1, the modes reproduce the roots −H and −2H of the constant-coefficient equation. These statements concern linear mode evolution, not nonlinear stability or physical attraction to a unique vacuum normalization.

## What changed

We now have an exact retarded inverse of the inherited critical scalar operator. The formal division by 2−alpha that fails in static response is unnecessary. Cosmic redshift matters: freezing X in the kinetic coefficient gives the nonzero residual −6H²y/(y²+3) on the first exact mode.

For initial perturbations proportional to probe mass, the entire finite-time response remains proportional to that mass. It cannot be the universal square-root mass response of deep MOND. This is a scoped linear result; it does not rule out a singular late-time limit of the nonlinear cusp equations, nor does it turn the earlier static runaway into a physical impossibility theorem.

The next concrete calculation is to derive the leading nonlinear term from the **undivided** constrained cusp action, then use this Green function in its causal integral equation. Its first discriminator is whether the small-source expansion remains uniform in time. A nonuniform limit could justify a nonlinear late-time branch; a uniform bound would remove that escape in its stated regime. Neither outcome alone selects the cusp width or proves b=1. No such nonlinear term or selection equation has been derived here.

## Evidence and limits

`results.json`: **20/20 checks**, including exact symbolic mode, source, lapse and Green-function residuals; subhorizon known-answer roots; a redshift MUTATE that bites; two kernel-checked finite Lean identities; a deliberately false Lean identity rejected; input hashes unchanged. Exact residual margins are zero; the mutant residual is displayed above and is nonzero for H,y>0. No observational margins exist because no observations were graded. These are self-reviewed symbolic computations with SymPy, not an independently reviewed proof of the field theory. Lean certifies the finite rational witnesses only, not the causal PDE or physical κ.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ23_causal_critical_response/run.py`.

H,B,k_com,Q and initial data remain symbolic, unselected/FITTED if assigned. F,c1,c2,m and cusp width are inherited unselected model choices. No data download, new particle, cold component, coefficient scan or remote push. The goal of deriving κ=½ remains unmet.
