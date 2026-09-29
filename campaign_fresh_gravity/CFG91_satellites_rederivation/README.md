# CFG91 -- independent re-derivation of CFG42's satellites headline (the M31 LVD -2.67 sigma)

(The agent's working name was CFG88, taken meanwhile by another lane; the scripts and the frozen spec keep the name cfg88 / `CFG88_SPEC_FROZEN.txt`. This lane is CFG91.)

**Question (frozen: `CFG88_SPEC_FROZEN.txt`, sha256 e2bdf799..., before the frozen runs).** Does CFG42's headline reproduce from independent code: the derived cold-mass rule over-predicts the M31 LVD classical satellites at -2.67 sigma, and closes the MW ultra-faint offset (+0.325 -> -0.06 dex)? The agent read the READMEs and docstrings, h48 lines 92-110 (Moster and NFW definitions) and hunt_lib's constants before freezing; it opened the CFG42/CFG45 scripts, .out and JSON only after its frozen main, MUTATE and sensitivity runs (`cfg88_post.py` and `cfg88_post2.py` are labelled post-reading and change no frozen number).

**Result: the offsets reproduce to about three decimals in every cell; the headline significance -2.67 sigma does NOT reproduce under the error recipe frozen from the README (-1.49 sigma); it reproduces only under one specific recipe, found by reading CFG42's script.**
| cell (dex, canonical / alt) | CFG91 | CFG42 |
|---|---|---|
| UFD law (KM, 9 limits) / UFD rule | +0.3245 / +0.3044; -0.0586 / -0.0591 | +0.325 / +0.304; -0.059 / -0.059 |
| MW classical law / rule | +0.0269 / +0.0074; -0.1186 / -0.1207 | +0.027 / +0.008; -0.118 / -0.123 (rule differs by 0.0006 / 0.0023, unexplained) |
| Collins law / rule | +0.0639 / +0.0448; -0.0243 / -0.0164 | +0.064 / +0.045; -0.024 / -0.016 |
| M31 LVD law / rule (P1) | +0.0435 / +0.0307; -0.1068 / -0.1076 (A1 gas), -0.1070 / -0.1088 (A2 gas) | +0.044 / +0.031; -0.107 / -0.109 |
| **M31 LVD rule significance** | **-1.49 / -1.51 sigma (frozen recipe)**; -2.67 / -2.67 under CFG42's recipe | -2.67 / -2.66 |
| UFD rule sigma (total error) | -0.40 sigma (0.145) | -0.41 sigma (0.143) |
| UFD collapse-mass floor; f_ex UFD | 0.133 (alt 0.136); median 0.963, 100% > 0.5 | 0.133; 0.96, 100% |
| clamp | 33 of 40 clamped; M*(1e9) = 1.92e4 | 33 of 40; '1.6e4' (a loose label) |
| UFD scan at CFG42's grid | +0.279 / +0.052 / -0.059 / -0.142 | same; zero crossing about 3e8 (-0.006) |
| cusp factor for M_h x100 at small r | 2.31 as r -> 0 (2.42 at 0.05 kpc, 2.95 at 0.3 kpc) | 2.27 (and the README's 'M_h^0.13' is only the r -> 0 leading behaviour; the effective factor at real UFD radii is 2.4-3, not 1.8) |

**Why the significance differs (post hoc, after reading CFG42's script): the sigma is recipe-driven.** CFG42 uses 1.2533 rms / sqrt(n) as the error of a median and an Upsilon_V floor that moves only the stellar mass (the halo mass and infall gas stay at Upsilon = 2); the frozen recipe used a bootstrap and propagated Upsilon into the collapse mass and gas. For the LVD rule:
| error recipe | total error | z |
|---|---|---|
| analytic SE + fixed-halo Upsilon floor (CFG42's) | 0.040 | -2.67 |
| analytic SE + propagated Upsilon floor | 0.061 | -1.74 |
| bootstrap SE + fixed-halo Upsilon floor | 0.054 | -1.97 |
| bootstrap SE + propagated Upsilon floor (frozen) | 0.072 | -1.49 |
The pieces: analytic SE 0.039, bootstrap SE 0.054, fixed-halo floor 0.006, propagated floor 0.047. **The -2.67 sigma needs both the smaller analytic SE and the absence of an Upsilon_V -> SHMR -> halo term; the offset (-0.107) is robust, the significance is not.** (The gas 'expectation' is max(current gas, mean of the 5 neighbour ratios) in convention A2; the agent's primary A1 misses the alt LVD rule by 0.001 dex. Kernel: the README says nu_mono but the numbers need the exponential RAR, which reproduces to three decimals; P2 moves the LVD rule to -0.100 (z -2.49 under CFG42's recipe), Milgrom's simple nu to -0.111 (-2.76); nu_mono was not built.)

**Sensitivities (scored under CFG42's recipe; the frozen recipe gives smaller |z| throughout).** Concentration: Dutton-Maccio LVD -0.107 (z -2.67) / MW classical z -1.79 / UFD -0.059 (-0.41); Duffy 200c full -0.071 (-1.71) / -1.31 / +0.049 (+0.34); Duffy relaxed -0.096 (-2.30) / -1.59 / -0.007; Duffy full with a z = 0 fit -0.081 (-1.94); Duffy 200m applied to a 200c mass (inconsistent) -0.125 (-3.14). **The LVD verdict is moved across the -2 sigma line by the concentration alone** (agrees with CFG65's A1/A2/A3: -3.13 / -1.71 / -2.30); the UFD closes under every row. Kernel: RAR, P2 and simple nu move the LVD offset by at most 0.007 dex. Moster clamp (UFD rule offset at clamps 1e8 / 3e8 / 1e9 / 3e9 / 1e10 / unclamped): +0.079 / -0.006 / -0.059 / -0.116 / -0.164 / -0.041 (z +0.55 to -1.14, |z| < 2 at every value; the clamp never touches the LVD, classical or Collins samples). M31 LVD sample: all 34 -0.107; without the four dwarf ellipticals (M32, NGC 147/185/205) -0.094 (-1.35 sigma); M_V <= -7.7 (n = 27) -0.136 (-1.74 sigma), M_V > -7.7 (n = 7) -0.003; upper-limit gas at the limit -0.106, no gas -0.088; leave-one-out -0.119 to -0.095. **Source dependence, 13 galaxies shared with Collins+13:** LVD data give -0.217, Collins' own D, R_e, sigma and M_V give -0.081, LVD data rescaled to Collins' distances -0.196: a 0.14 dex swing on identical galaxies exceeds the headline offset (R_e differs most for And XXII 120 vs 252 pc, XXVII 326 vs 657 pc, XI 109 vs 158 pc).

**Controls.** Main run rc 0, all pass: sample counts 40 / 9 / 14 / 34 / 14 (calibration set 42, 32 detections); Newtonian limit; deep-MOND limit for RAR and P2; phi = 0 equals the bare law (3e-16); phi = 1 equals the sum by an independent direct formula (2.5e-13); f_ex in [0, 1]; NFW M(<R200) = M_h with monotone enclosed mass; the edge-phantom root-find matches its closed form (1e-7). **First-run failure kept** (`cfg88_FIRSTRUN.out`): the deep-MOND control C1b failed because its test point (y = 8e-15) sat below the agent's own kernel floor (1e-14); the point moved to y = 8e-8, no tolerance changed. MUTATE=1 (every M_coll / 100 after clamp), rc 1 by design: the UFD rule median is +0.322 (+2.44 sigma), so the UFD offset stays open, and f_ex > 0.5 in only 5% of UFDs so H3 fails, as CFG42 reports.

**What the agent would attack.** (1) The -2.67 sigma is a recipe artefact (above). (2) The -2 sigma line is crossed by the concentration alone (-1.71 under the 200c-consistent Duffy row, -1.94 under its z = 0 fit). (3) LVD size and photometry come from one compilation; distance and size inputs matter more than any model knob. (4) The UFD closure is a weak test: it passes for M_coll from about 3e8 to 1e10, the offset sliding from 0 to -0.164 (-1.14 sigma), and the collapse-mass floor 0.133 is 92% of the total error 0.144. (5) Untouched: the SPARC H4 lane, the Moster scatter, the inclusion of the M31 dwarf ellipticals, the meaning of nu_mono.

Nothing here says the data favour the framework; kappa = 1/2 is FITTED. Run in place in `CFG91_satellites_rederivation/`: `python3 cfg88.py` (rc 0), `MUTATE=1 python3 cfg88.py` (rc 1), `python3 cfg88_sens.py`, `python3 cfg88_post.py`, `python3 cfg88_post2.py`; output identical to the agent's.

## Portability and control-exit-code notes (from the equations chat's re-run of CFG75-99; appended, no result changed)
- **Absolute input paths.** The script reads its inputs through a hard-coded absolute path into the live repository tree, so a clean checkout at another location fails until the path is derived from `__file__` (or the repo root); the fix is pending the user's permission to edit the scripts (a batch edit was declined), and the numbers are unaffected.
- **MUTATE exit code.** The MUTATE run's exit 1 comes from a hard-coded condition in the script (`sys.exit(1 if not (abs(rule_u['z']) < 2) else 0)`: exit 1 whenever the mutated rule does not close the UFDs), not from a failing control; the run prints 'FAILED CONTROLS: none'. The informative signal is the two C4 lines (the UFD rule median stays open at +0.322, +2.44 sigma; H3 fails at fraction 0.050). The post-reading scripts `cfg88_post.py` and `cfg88_post2.py` write `run_post.log` and `run_post2.log`.

## Committed output names (appended)
- The `.log` files named above are git-ignored by the repository's `.gitignore`, so the committed copies of the same outputs carry the `.out` extension (same names otherwise; content identical to the in-place runs). Nothing else changed.
