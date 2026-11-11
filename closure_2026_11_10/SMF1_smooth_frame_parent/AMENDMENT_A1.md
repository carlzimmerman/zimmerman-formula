# SMF1 AMENDMENT A1 (post hoc): is each failing gate wave-specific? (2026-11-10)

Committed alone, after the result (origin 884ddfb854) and before the checks below are written or run. It was asked for
by the coordinating session. It changes no criterion, threshold, gate or label. It adds a reading and three checks that
say whether a **collisionless** carrier escapes, meaning a kinetic, multi-stream, non-wave carrier in the same B-Tm-smooth
structure. No other lane covers that member.

## Definition

A gate is **WAVE-SPECIFIC** if it fails because the carrier is a wave. That covers nodes, interference fringes, the
de Broglie core against the law's inner density a0/(2 pi G r), quantum pressure, phase locking, or the ultralight mass
window. Otherwise the gate is **NOT** wave-specific, and the collisionless member is decided by it too.

## Readings fixed now (before the checks)

| item | status in RESULT | reading | collisionless member |
|---|---|---|---|
| S0b, net fill of the polarization charge (Gauss) | FAIL | NOT wave-specific. The identity uses only the frame's continuity equation, N = mu_K^2 h/K + div P, and P = 0 on a free-falling boundary. No carrier variable enters | does not escape |
| S0c, the exchange is off where the halo is counted once | FAIL | NOT wave-specific. A carrier with a non-negative phase-space density can hand charge to the frame only where it exists, so the transfer is proportional to the local carrier density. For point particles a local action cannot change their number at all | does not escape |
| S0a, rho = rho_b + rho_Psi | PASS | NOT wave-specific (rho_Psi becomes the carrier's density) | same |
| S0d, detuning and lock (reported) | reported | WAVE-SPECIFIC (it needs Psi's phase) | does not apply: a kinetic carrier has no phase to lock |
| S0c trade, standing delta (reported) | reported | WAVE-SPECIFIC in its rate model (phase lock and band average) | a kinetic loss term gamma f gives delta >= (d ln C/dt)/gamma; stated, not graded |
| S0e, the held edge layer (reported) | reported | NOT wave-specific: the Jeans empty-core step, the accreted-spin shortfall and the frame's depth-dust do not involve the wave. The "irrotational exchange product" item is wave-specific (phase lock) | a kinetic source could deposit carrier with a velocity spread; the empty-core and spin items still apply |
| S1 stiffness band, c1 = -lambda_s + ... (reported) | reported | the -lambda_s term is NOT wave-specific (it comes from the frame). Its cutoff (quantum pressure) IS wave-specific | the cutoff becomes the carrier's velocity dispersion. Escapes only if sigma^2 >= lambda_s on the band; checked in C3 as a fluid estimate |
| S2(d), the m window | PASS | WAVE-SPECIFIC | does not apply |

## Checks to run (script `smf1_a1_collisionless.py`, Lean `SMF1_A1.lean` and its false twin)

- **C1.** The S0b balance with a kinetic carrier. The frame's source is the loss term S = Int gamma(v) f(v) dv; the
  identity must hold with residual 0 and contain no carrier variable except through S.
- **C2.** Kinetic starvation. S = n Int gamma(v) g(v) dv, with f = n g and Int g = 1, vanishes at n = 0 (sympy). Lean: if
  every f_i >= 0 and the f_i sum to 0, then every gamma_i f_i sums to 0.
- **C3.** The collisionless fluid limit of S1. Drop the exchange lock (g_x = 0), since a kinetic carrier has no phase,
  and replace quantum pressure with an isothermal dispersion term sigma^2 (valid below the free-streaming scale). Report:
  - the k^2 coefficient c1 of the growing root (sympy, residual 0);
  - the condition for the -lambda_s band to be stabilized;
  - the largest ell it allows with sigma at the record's forest line (9.2 km/s at z = 3).

  This is an estimate: a fluid stand-in for a kinetic carrier, not a Vlasov computation.
- **MUTATE MA1.** In C2, let f take negative values; starvation must fail. The Lean twin's false statements must fail to
  compile.

Compute etiquette (coordinating session): while BX1's production run is live, run one job at a time, single-thread,
nice 19.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
