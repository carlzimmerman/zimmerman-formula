# CFG815 FROZEN CRITERIA: CFG814's rule on ALL 318 eRASS1 clusters and the 8 ACCEPT clusters (committed before any script)

**Rule (CFG814, unchanged).** H-EX split, retained baryons tether their own cold share and the expelled share is free (Method
A; CFG809 machinery). Per-system retention f_eff = (gas < 3 Mpc + M_cond) / (gas < r_ta + M_cond). The gas density follows the
system's own profile out to r200m = 2.2 R500, then ρ ∝ r^−3 to the framework turnaround radius r_ta (CFG654 Δ_ta(z), fixed
point). Bracket F: r^−3 to 2 r200m, then r^−2.
- **Stellar mass:** a relation log M_cond = a log M_gas,3Mpc + b, fitted ONCE (ordinary least squares) on the 76 λ-matched
  clusters with M_cond = λ × 10^10.7. Here M_gas,3Mpc is the harness's total gas within 3 Mpc. It is then applied uniformly
  to all 318 eRASS1 clusters and the 8 ACCEPT clusters. a and b are reported. No other change.
- **eRASS1:** gas = the harness beta model; R500 from the catalogue.
- **ACCEPT:** gas = the CFG686 measured profiles as built in the harness; R500 := the harness's R_X fixed point (declared
  proxy).

## Pass rules (ν_s primary; both footings, never pooled)
1. **eRASS1 318:** MID and OUTER within 2σ (30-patch jackknife), AND every gas-mass tercile |Z_MID| < 3.
2. **ACCEPT 8:** OUTER within 2σ (bootstrap).

**Classes:**
- **PASS:** both pass on ≥ 1 footing (primary profile P). ROBUST if bracket F also passes.
- **PARTIAL:** one passes.
- **FAIL:** neither.

**Scope (stated).** eFEDS is not rerun. It passed under H-EX with measured catalogue condensed masses (CFG809: p 0.044/0.087),
which is a different retention input; consistency is stated, not re-tested. KiDS early types are not part of this lane.

## Controls
- K1: on the 76 λ-matched clusters, the relation-based M_cond run gives MID within 1σ of CFG814's λ-based 1.08.
- K2: the ALL control (pooled, fs 0.20, constant 0.90) reproduces CFG727's stored eRASS1 MID 1.40 and ACCEPT OUTER 0.92.
- Report the f_eff distribution per tercile.

κ = ½ fitted; cold energy mass required; not theory closed.
