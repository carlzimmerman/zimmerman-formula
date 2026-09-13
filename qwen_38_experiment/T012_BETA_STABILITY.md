# T012 beta-stability interior/edge

| quantity | formula | sign over beta in [0.25,4] | selects beta=1? |
|---|---|---|---|
| ghost K''(x) | beta M^4 (1-x^2)^(-3/2) | >0 for all beta>0, |x|<1 | NO |
| gradient c_s^2(x) | (1-x^2)/(3-x^2) | >0 for all |x|<1, beta-independent | NO |
| stable interval | [0.2500, 4.0000] (full scan band; all beta>0) | -- | beta=1 INTERIOR |

CONCLUSION: CONFIRMED.  Both the ghost condition (K''>0) and the gradient condition (c_s^2>0) hold over the ENTIRE beta in [0.25, 4] (indeed for all beta>0) and all |u|<Lambda_D.  beta=1 is a strictly INTERIOR point (left margin 0.7500, right margin 3.0000 to the window edges); stability does NOT select it.  The only edge of the stable region is the FIELD-space wall |u|=Lambda_D (c_s^2->0 there), which is beta-independent.  The DBI Lagrangian's stability is beta-blind; nothing in the stability analysis singles out beta=1 -- consistent with R5 (beta=1 is SELECTED, not derived).
