# CANDIDATE REGISTRY — register BEFORE computing; never re-run a dead line

Format: `C### | definition (one line) | gating variable | timing | bookkeeping | free parameters (count) | first-gate kill condition (pre-registered) | status | killed by (H-entry, gate, number)`

Dead before this loop started (do not re-run; see fable_independent_2026/FINDINGS.md):
C000a | sound speed / pressure support (any c_s^2) | density (Jeans) | always | clustering reduced | 1 | — | DEAD | L185/L186 G5 vs G1: c_s^2 <= 1e-9 for the forest gives lambda_J < 7 kpc
C000b | two-body decay or kicks, universal lifetime | none | universal | mass redistributed | 2 (tau, v_k) | — | DEAD | L167/L168 G5 vs G1: tau >= 41 Gyr vs tau <= 20 Gyr
C000c | late collapse / suppressed primordial power (top-down) | none | primordial | clustering reduced | 1 (k_cut) | — | DEAD | L187 G5: regeneration 0.45 at k = 5, z = 2.2 for k_cut = 2
C000d | velocity filter / internal-clock fluid | velocity | always | clustering reduced | 1 | — | DEAD | L173/L174 G6 shear C_l(1000) 0.27-0.76
C000e | potential-depth threshold | potential | always | clustering reduced | 1 | — | DEAD | L175 G5
C000f | uniform time-dependent coupling (f falling to 0.58) | epoch | DE-era | coupling reduced | 1 | — | DEAD | L177 G6 S8 0.48-0.54 (knife-edge only with a kernel that overshoots, L178)
C000g | environment-switched medium | environment | always | coupling switched | 1 | — | DEAD | KiDS interleaving (closure_2026)
C000h | thermal relic, fuzzy/wave, condensates, Pauli | — | — | — | — | — | DEAD | hunt_2026/g03*-g04*

Live lines (append below):
