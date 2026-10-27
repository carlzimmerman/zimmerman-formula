You are helping with an emergent-gravity framework (carlzimmerman/zimmerman-formula). I want ONE genuinely new idea, not a restatement. Work in this order and keep the answer under ~1,200 words plus code.

STATE OF PLAY (all audited, do not re-derive or re-propose)
- Law: g_N = g^2/(g+a0), a0 = kappa * c * sqrt(G * rho_DE), kappa = 1/2 is FITTED. In (c, G, rho_DE) units a0 has NO pi; the pi in Z = sqrt(32pi/3) is Friedmann's 8pi/3, so the only open number is the rational 1/2.
- Gate mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) equals the Deser-Levin form with quadrature floor a_floor = a0/2. A floor equal to kappa_dS = cH would give a0 = 2cH, i.e. 2Z = 11.58 too large. Thermodynamic/horizon/instanton/Wald/Brown-York/Komar/Seeley-DeWitt/Moyal/Kramers-Kronig routes all fail to output kappa or Z.
- Action: L = -|grad Phi - K P|^2/(2K) - rho Phi - W_rem(u) - (gamma/2)|grad P|^2, K = 4 pi G, u = K|P|, K W_rem'(u) = u^2/(a0-u). Eliminating P gives an AQUAL-like static sector (div(mu grad Phi) = K rho, mu = g/(g+a0)), so "no external-field effect" is a DEFINITION (CFG693 free-fall basins), not an outcome.
- Dead ends: hot-gas selector is not in the action (chi_tether put in by hand); free pool tracking gas (CFG432, 6-8 sigma excluded); UFD hysteresis/infall/tidal (CFG463/327/336); BH cold-energy-to-dark-energy conversion vs DESI CPL (excluded as parametrised; needs ~8e3 M_BH per hole); numerology like 1+R/(2pi), (1+z)^-0.217, 0.65 constants.
- Open: (1) why the gate scale is sqrt(G rho_DE) and not H; (2) the rational 1/2; (3) what fixes the cluster/elliptical free component (k ~ 0.6-0.75 R0, profile NFW-like, not gas-tied); (4) whether the basin definition is derivable from a nonlocal term in the action.

RULES
1. Every number must come from a stated equation. No constant may be chosen after seeing a target. If you need an extra posit, name it and count it.
2. Before any result, state the pass/fail criterion and a mutation that must fail.
3. Report failures as loudly as wins. Do not say the theory is closed.
4. No LambdaCDM halo shapes or mass functions as inputs.

TASK
Pick the single most promising open item above. (a) State a concrete mechanism in one paragraph with its equation of motion or action term. (b) Show by symbolic algebra that it outputs the target number with zero inserted constants, or say it does not. (c) Give the one measurement that would kill it (name the dataset and the predicted number with an error). (d) List the two strongest objections to your own idea and whether your calculation answers them.
Return: the idea, the algebra (sympy), the kill test, the objections. If you cannot find one that survives rule 1, say that plainly and name the least-bad candidate and its cost in extra posits.
