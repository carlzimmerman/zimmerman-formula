# LGS1 — the Dovekie supernova lanes with the legacy low-redshift supernovae dropped

Criteria and harness: a917faa500 (alone first, before any number). Labels: `lgs1_collect.out`, `lgs1_results.json`.
Commit ids, local / origin: criteria a917faa500 / 823b098e6c; result 4fdcc846de / f58039cda2.
Per-run files: `lgs1_cfg684_<sample>.{json,out}`, `lgs1_cfg689_<mode>_<sample>.{json,out}`.
A re-read of committed lanes. It adopts nothing and edits no ledger.

## Verdict
- **CFG684 (no CMB, no native ruler): LEGACY-DEPENDENT.** The flat-a0 Ω_m moves by −0.0150 when the 197 legacy
  supernovae are dropped, more than the combined sd. A size control (197 random DES supernovae dropped) moves it by
  −0.0001 to +0.0006. The tracking floor at z 2.33 is lost, but the control loses it too.
- **CFG689 (the framework's own ruler), D5 and TD5F: STABLE at every redshift, CLASS UNCHANGED.** The tracking band that
  X54 took from TD5F (0.68–1.04 at z 2.33) becomes 0.65–1.01.

## Harness checks
`full` through the harness equals the committed files exactly: CFG684 max |diff| 0 (both combinations), CFG689 D5 and
TD5F max |diff| 0 in the tracking quantiles. The committed lane files are untouched.

## Part A — CFG684
| sample | n | combination | Δχ²_max | flat-a0 Ω_m | √X(1.5) band | √X(2.33) band |
|---|---|---|---|---|---|---|
| full | 1,820 | BAO+DES5 | 1.67 | 0.3067 ± 0.0074 | 0.791–1.579 | 0.690–2.168 |
| full | 1,820 | BAO+DES5+CC | 1.72 | 0.3070 ± 0.0073 | 0.787–1.574 | 0.687–2.166 |
| des_only | 1,623 | BAO+DES5 | 0.11 | 0.2917 ± 0.0085 | 0–1.488 | 0–2.019 |
| des_only | 1,623 | BAO+DES5+CC | 0.16 | 0.2920 ± 0.0080 | 0–1.496 | 0–2.026 |
| rand197 (control) | 1,623 | BAO+DES5 | 1.44 | 0.3073 ± 0.0077 | 0.562–1.588 | 0–2.169 |
| rand197 (control) | 1,623 | BAO+DES5+CC | 1.50 | 0.3069 ± 0.0077 | 0.651–1.579 | 0–2.166 |

- **A1:** NOT BROKEN in every row. Without the legacy set the χ² is nearly flat in Ω_m (0.11–0.16 against 1.67–1.72).
- **A2:** `des_only` LEGACY-DEPENDENT in both combinations (shift −0.0150; combined sd 0.0113 / 0.0108).
  `rand197` ROBUST (+0.0006 / −0.0001). So the shift comes from the legacy set, not from the loss of 197 objects.
  Context only: the nested-sample sd is 0.0042 / 0.0032.
- **A3:** FLOOR LOST for `des_only` and for `rand197`. The floor at z 2.33 that CFG684's README credited to DES5 does not
  survive the loss of 197 supernovae of either kind, so it cannot be put on the legacy set alone. Reported: at z 1.0 and
  1.5 the control keeps a floor (0.80–0.85 and 0.56–0.65) and `des_only` does not (0).

## Part B — CFG689 (60,000 steps, same seeds; chain check K4 ok in both modes)
Tracking √X, 68% band and median:

| mode | z* | committed | legacy dropped | B1 |
|---|---|---|---|---|
| D5 | 1.0 | 0.811–1.057 (0.950) | 0.805–1.036 (0.934) | STABLE |
| D5 | 1.2 | 0.780–1.059 (0.941) | 0.789–1.048 (0.936) | STABLE |
| D5 | 1.5 | 0.677–1.099 (0.927) | 0.716–1.099 (0.937) | STABLE |
| D5 | 2.33 | 0.338–1.207 (0.908) | 0.506–1.222 (0.953) | STABLE |
| TD5F | 1.0 | 0.912–1.031 (0.973) | 0.870–0.991 (0.932) | STABLE |
| TD5F | 1.2 | 0.895–1.003 (0.949) | 0.860–0.969 (0.916) | STABLE |
| TD5F | 1.5 | 0.781–1.032 (0.912) | 0.762–1.004 (0.889) | STABLE |
| TD5F | 2.33 | 0.678–1.045 (0.879) | 0.654–1.009 (0.848) | STABLE |

- **B2:** CLASS UNCHANGED in both modes (P1 DEGENERACY BROKEN; D5 P0 FLAT CONSISTENT).
- e_3σ changes by at most 0.011 (D5, z 2.33: 0.086 → 0.097).

## Reported, no frozen label
- **P2 (constant dark energy, the script's own class).** TD5F: Δχ² 11.32 / 5, 2.00σ, HINT → 9.02 / 5, 1.61σ,
  CONSISTENT WITH CONSTANT. The committed value sat on the 2σ line. D5: 7.78 → 6.96, CONSISTENT WITH CONSTANT both.
- **The script's native H0 (post hoc; not in the criteria).** The criteria said nothing here measures H0. That was wrong:
  CFG689 prints a native H0 in its P3 block. Median and 68% band, km/s/Mpc:
  D5 67.85 (67.28–68.43) → 69.40 (68.51–70.26); TD5F 67.73 (67.18–68.28) → 69.27 (68.42–70.13).
  Dropping the legacy set raises it by about 1.5 and widens the band by about half. No label is attached.

## What this does and does not say
- The CFG684 flat-a0 Ω_m and its "all four SN choices agree" line lean on the legacy supernovae. The CFG689 tracking
  bands and classes do not.
- It does not say which supernova sample is right. arXiv:2610.23657 argues the legacy set is offset by about +0.065 mag;
  this lane does not test that.
- X54 and RF5 were not re-run and stay open. The TD5F band X54 used moves from 0.68–1.04 to 0.65–1.01.
- No w0–wa fit was made. Nothing here grades the framework.

kappa = 1/2 FITTED; not theory closed.
