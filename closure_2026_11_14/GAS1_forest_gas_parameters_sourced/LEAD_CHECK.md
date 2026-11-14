# GAS1 LEAD CHECK (2026-11-14): commit ids, what the lead checked, and what stays provisional

Written by the lead session after the lane's files were committed. A look-up lane: not blind, not graded, relabels
nothing, computes no forest number. The agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| SCOPE.md (alone, before any look-up) | ddeb2deaa5 | 77096a2dad |
| SOURCES.md, CONVENTION.md, READING.md, fetch_log.md | a785a73dd5 | 0a572a515e |

## What the lead checked

- **The convention, in the code.** Both builds multiply the density field by exp(-0.5 (k lambda)^2):
  `frz3r_core.py` (`gas`, used by FRZ4, FRZ6, FWN1 and FWN2's build A) and `fwn1r_lib.py` (`gas`, used by FRZ6R, FWN1R
  and FWN2's build B). lambda is comoving, in Mpc/h, and the primary is coded as 0.079 x 0.6736. This is the lead's own
  reading of the two files and agrees with CONVENTION.md.
- **The web calls.** The agent's tool calls were listed by script: 7 searches and 24 page fetches. Every query is a
  generic bibliographic one and every page is an arXiv abstract or full-text page. No query or address carries
  anything about this repository, its owner or the machine. Nothing was saved to disk from the web.
- **The scope was frozen first.** SCOPE.md was committed 11 minutes before the other files and holds the placement
  rule.
- The committed files hold no home path.

## What stays provisional

- The lead did not re-read the papers. Every number marked SEEN IN TEXT was read by the agent through a page-fetch
  tool that passes the page through a small model; the agent says so and asks for a spot-check against the PDFs. Until
  someone reads the tables by eye, every number in SOURCES.md is PROVISIONAL in the house sense, and so is every
  placement in READING.md.
- The placement script was run in the agent's scratch space and is not committed; its inputs are all in SOURCES.md.
- Reading 2 (a factor 1/2 between the flux-fitted smoothing scale of Kulkarni et al. 2015 and Walther et al. 2019 and
  the density-defined one) rests on one figure caption that gives no derivation. It is not settled which reading holds.

## What the lane says, in the lead's words (nothing relabelled)

- The record's lambda_P is defined exactly as in the quasar-pair measurement (Rorai et al. 2017), so that measurement
  can be compared with the code's value without a conversion.
- The pair 91.4 and 138.6 comoving kpc is that measurement's 16th and 84th percentile at z = 3.0, as the record said;
  its median is 113.8. The record's primary, 79, is a simulation value. Against that measurement the primary is low
  at z 3 (inside twice the error, outside once).
- Under Reading 1 the two smoothing values that trigger FRAGILE flags, 39.5 (half) and 158 (double), are mostly outside
  the measurements: 39.5 is inside twice the error at z 2.2 only, 158 inside twice the error at z 3.0 only.
- The two slope values that trigger FRAGILE flags, gamma 1.2 and 1.6, are each inside the 1 sigma range of at least
  one measurement at z 3.0 and 4.4; at z 2.2, 1.6 is inside 1 sigma and 1.2 inside 2 sigma. The measurements of gamma
  disagree with each other by more than their errors.
- So the FRAGILE flags of the forest labels between settled-radius factors 3 and 5 (FRZ6, FWN1R, FWN2) stay live
  through gamma whichever reading of the smoothing convention holds. The flags that rest only on half the smoothing
  scale rest on a value the measurement-matched convention mostly excludes; under Reading 2 that value is allowed.
- What would settle it for the gate: gamma and the smoothing scale fitted with the layout rather than held fixed (FRZ5
  did this for the full layout only), or a hydrodynamic forest model.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
