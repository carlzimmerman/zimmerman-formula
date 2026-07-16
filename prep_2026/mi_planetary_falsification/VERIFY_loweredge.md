# VERIFY — full-SPARC hardening of the omega_c lower edge

**Verdict: UPHELD.** The joint planetary window survives on BOTH footings after
hardening the lower edge with the full SPARC deep-MOND distribution. Reproduced
independently; no manufactured save, no manufactured kill.

Audited script: `loweredge_fullsparc.py` (this dir). Independent re-derivation:
fresh parser + own selection + cut sweep (scratchpad `indep_verify.py`).

## 1. Re-run of the audited script
`python3 loweredge_fullsparc.py` -> **exit 0**, ALL CHECKS PASS.
Hard-coded-verdict grep: the only `check()` calls against literals are (a) `k==3`
(a math identity of the gate) and (b) the two upper-edge values reproduced to ±2%
of `window_joint.py` (a reuse-consistency check). The OPEN/CLOSED verdict itself is
computed from `omega_hi > omega_lo` — **no hard-coded pass/fail.**

## 2. Independent recomputation (my own code, my own selection)
Numbers match to all printed digits:

| footing | MAX(omega_gal) | binding orbit | lower edge 3·MAX | LLR upper | verdict |
|---|---|---|---|---|---|
| canon | 5.9414e-15 | UGC05721 | 1.7824e-14 | 2.2101e-14 | OPEN x1.240 |
| alt   | 5.9414e-15 | UGC05721 | 1.7824e-14 | 1.8306e-14 | OPEN x1.027 |

omega_gal = v_rot/r confirmed as the correct frequency: in a circular orbit the
centripetal acceleration vector rotates at Ω = v/r = a_c/v, so the AC tone the
memory gate sees is exactly the orbital angular frequency. Correct.

## 3. Is the binding orbit a GENUINE confirmed-MOND point? — the key caveat
UGC05721: Q=1 (best), inc=61° (well above the 30° floor) — a **good-quality,
good-inclination galaxy**, not a junk one. BUT the binding **point** is the
*innermost radius* r=0.09 kpc, V=16.5 km/s on a curve that rises to Vflat=79.7.
At D=6.18 Mpc that radius subtends ~3 arcsec (≈ beam scale), so V there is
beam-smeared / on the rising inner branch — its large omega=v/r is a *small-r
geometric* effect, not a slow flat-curve deep-MOND orbit. It formally passes the
cut (g_bar=7.03e-11 < a0, y=0.75 canon / 0.62 alt), and the framework's own RAR
fit includes such points, so **keeping it is the conservative choice** — it is the
point that most *raises* the lower edge (pushes toward closure). The whole top of
the distribution (NGC2403, NGC6789, NGC5585, …) is likewise innermost-ring
dominated. Direction check: including these arguable beam-artifacts RAISES the
edge; dropping each galaxy's innermost radius LOWERS MAX to 4.62e-15 → lower edge
1.39e-14 → both footings survive comfortably (canon x1.59, alt x1.32). **So the
near-closure of alt rests entirely on one plausibly-artifact inner ring; the
SURVIVE verdict is robust to removing it.** This is disclosed in the script.

## 4. Is the selection honest? (stricter + looser, both ways)
| cut | canon | alt |
|---|---|---|
| stricter Q≤1 | OPEN x1.240 | OPEN x1.027 |
| stricter inc≥45 | OPEN x1.240 | OPEN x1.027 |
| stricter y<0.5 (deeper MOND) | OPEN x1.635 | OPEN x1.355 |
| looser inc≥25 | OPEN x1.240 | OPEN x1.027 |
| looser y<1.5 | **CLOSED x0.834** | **CLOSED x0.690** |
| drop 1 innermost/gal | OPEN x1.594 | OPEN x1.321 |
| drop 2 innermost/gal | OPEN x2.158 | OPEN x1.788 |

Fine y-scan: the verdict is OPEN on a **wide plateau y<0.8 … y<1.3** (identical
MAX=5.941e-15, UGC05721 throughout). It flips CLOSED only at y<1.5 — and that
closer, NGC2998, has its binding point at **y=1.46** (g_bar=1.4·a0, an inner ring
of a massive spiral, Vflat=210): a **near-Newtonian, NOT deep-MOND** point. So the
standard deep-MOND boundary g_bar<a0 (y<1) sits in the middle of a stable plateau,
not on a knife-edge. Tightening the cut widens the window; only pushing the cut
*out of the deep-MOND regime* closes it. **The cut is not tuned to open, and not
tuned to close.**

## 5. LLR upper edge — unchanged
Recomputed independently from the same formula d ln r/dt = a0·omega_c/g_N ≤ LLR
2σ Gdot/G = 24.2e-15/yr (Biskupek & Müller 2021): canon 2.2101e-14, alt 1.8306e-14
rad/s — identical to `window_joint.py:136-142`. Not touched by this task.

## 6. Manufactured save / manufactured kill — hunted equally
- **Save?** No. The single highest (innermost, conservative) point was retained;
  it is the one closest to closing the window.
- **Kill?** No. The window survives on the standard cut; closure requires a
  non-standard loose cut that admits a near-Newtonian point.
- **Knife-edge honesty:** alt at +2.7% from closure is reported straight; it is
  driven wholly by one inner-ring point, and the script says so.

## Bottom line
UPHELD. Window survives both footings, substantially narrowed (canon x1.24, alt
x1.027). The alt knife-edge is real but fragile-in-the-safe-direction: it hangs on
one innermost-ring point that is plausibly a beam artifact; drop it and alt widens
to x1.32. The genuine physical lower edge is likely *below* the reported 3·MAX
(the true deep-MOND flat-curve orbits sit lower in omega than the beam-scale inner
rings), so the window is if anything wider than reported. Gate corner remains a
FREE 5th constant — unchanged. No manufactured save or kill.
