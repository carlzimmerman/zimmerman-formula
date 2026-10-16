# CFG815: CFG814's rule on all 318 eRASS1 clusters + ACCEPT. FAIL (both profiles). The 76-cluster pass does not generalise

- **Stellar masses:** relation log M_cond = 0.397 log M_gas + 6.847, fitted once on the 76 λ clusters.
- **Retention per cluster:** from the eROSITA outskirt profile.
- **Controls:** K1 (76-subset MID 1.195 vs CFG814 1.08 ± 0.14) PASS; K2 (ALL control vs CFG727, 0 deviation) PASS.

| profile | eRASS1 MID / OUTER | terciles MID | ACCEPT OUTER | verdict |
|---|---|---|---|---|
| plain capped law (ALL) | 1.85 / 1.01 | 1.22 / 2.21 / 2.06 | 1.07 | — |
| **P** (r^−3 to r_ta), canonical | 1.18 (Z +2.3) / 0.83 (Z −2.3) | 1.21 / **1.64 (Z +4.6)** / 0.90 | 0.42 (Z −5.5) | FAIL |
| **F** (flattening), canonical | 1.08 / 0.79 (Z −3.1) | 1.18 / **1.51 (Z +4.0)** / 0.81 | 0.32 | FAIL |

The f_eff medians per tercile are 1.00 / 0.83 / 0.63 (P).

**Reading.**
- The rule improves on the plain law in every tercile, but the middle gas tercile stays short (Z +4 to +4.6). The outer band
  and the heavy tercile tip into overshoot.
- **The tercile needs are non-monotonic.** Across CFG809/813/815, the light tercile fits with no freeing, the middle wants the
  most, and the heavy wants an intermediate amount. No smooth retention law gives that shape. This points to a sample or
  selection effect (e.g. Eddington bias in low-mass eRASS1 M_gas, flagged in CFG687; tercile redshifts 0.15 / 0.24 / 0.31),
  not to the free-cold-energy rule.

**ACCEPT diagnostic** (`diag_accept_loo.py`):
- Two low-z 2PIGG groups (z ≈ 0.07) carry 43% of the OUTER weight, and every model overshoots them, including the plain law
  (0.60 / 0.32).
- The "ACCEPT passes with no free mass" result was itself a cancellation: these groups are overshot while A1835, A2744 and
  A3088 are short ×1.8–2.5.
- There is no clean giant-cluster signal.

κ fitted; cold energy mass required; not theory closed.
