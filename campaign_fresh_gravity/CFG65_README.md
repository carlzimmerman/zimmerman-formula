# CFG65 — is the debris result robust to the halo shape? A Burkert core removes both the closure and the over-prediction

Script: `CFG65_debris_shape.py` (about 20 s). Outputs: `.out`, `_results.json`, and the MUTATE pair (all profiles × 100). Written by a delegated agent with the question and the three alternatives declared before the first run, and re-run here (main passes 7 of 7; the MUTATE run fails its headline as required).

## The frozen question

The sum rule's debris uses an NFW shape with the Dutton–Maccio concentration. Reviews flagged the cusp and c(M) as the fragile assumption behind both the ultra-faint closure (CFG42) and the classical-satellite over-prediction (CFG42/45; CFG59's SLUGGS-against-LVD conflict). Three parameter-free alternatives were declared in advance: **(A)** NFW with Duffy+2008 c(M) (A1: CFG23's committed 200m row; A2, A3: the full and relaxed 200c rows); **(B)** a Burkert core at r_core = r_s (one declared choice, not scanned); **(C)** Einasto with α = 0.17 and r_−2 = r_s. A result is SHAPE-ROBUST if the ultra-faint offset stays within 2σ of zero and the LVD over-prediction stays beyond −2σ or within 0.05 dex.

## Results (canonical, dex; σ in brackets; alt within 0.02)

| profile | UFD KM median | MW classical | M31 LVD | SLUGGS | X-ray |
|---|---|---|---|---|---|
| bare law | +0.325 | +0.027 | +0.044 | +0.080 | +0.280 |
| DM (committed) | −0.059 (−0.41σ) | −0.118 | −0.107 (−2.67σ) | +0.007 (+0.39σ) | +0.125 |
| A1 Duffy 200m | −0.098 (−0.62σ) | −0.130 | −0.125 (−3.13σ) | −0.010 | +0.077 |
| A2 Duffy 200c | +0.049 (+0.35σ) | −0.089 | −0.071 (−1.71σ \| −1.90σ) | +0.016 | +0.154 |
| A3 Duffy relaxed 200c | −0.007 (−0.05σ) | −0.106 | −0.096 (−2.30σ) | +0.010 | +0.135 |
| **B Burkert core** | **+0.284 (+3.91σ)** | −0.028 | **−0.006 (−0.09σ)** | +0.048 (+2.62σ) | +0.250 |
| C Einasto | −0.117 (−0.75σ) | −0.130 | −0.124 (−3.11σ) | +0.000 | +0.101 |

- **A (all three) and C are SHAPE-ROBUST:** the ultra-faint offset stays under 0.75σ and the LVD offset moves by at most 0.036 dex. **Caveat:** under A2 the LVD significance drops to −1.7σ | −1.9σ, below the −2σ line; it passes only through the 0.05-dex clause, so the over-prediction is robust in size but marginal in significance under the 200c-consistent concentration.
- **B is SHAPE-SENSITIVE on both results:** the cusp is what closes the ultra-faints (the cored profile leaves them at +0.28 dex, 3.9σ), and the same core removes the LVD over-prediction (−0.09σ), while SLUGGS becomes a 2.0–2.6σ under-prediction. **The trade CFG42 anticipated is real: a core cures the classical dwarfs and loses the ultra-faints.**
- **φ conflict (CFG59):** the LVD and SLUGGS intervals stay disjoint for DM, A1, A2, A3 and C. Under B the test reads "does not persist" only because SLUGGS's interval is empty (no φ reaches 1σ); there is still no common φ.

## Controls and caveats

C1: DM reproduces CFG45's committed numbers to 1e-6 (48 comparisons); C2: the generic function equals h48's committed `nfw_enclosed` (30 masses × 40 radii); C3: every profile matches direct numerical integration of its density to 1.6 × 10⁻¹¹; C4: the bare law is identical across configurations; C5: the φ analysis reproduces CFG59; C6: the absurd profile (DM × 100) flips the ultra-faint gate. The first run's C3 failed on a bug in the control (it demanded strict monotonicity inside h48's x = 10⁻⁴ clip plateau); fixed and disclosed in the docstring, with no result changed.

**The Duffy coefficients for A2 and A3 were transcribed from memory by the agent; only A1 is CFG23's committed row.** A1 also mixes a 200m concentration with a 200c mass (disclosed, not corrected). The A results should be read as approximate until the coefficients are checked. The ultra-faint closure needs the debris mass at 0.03–0.3 kpc to be at least about 0.55 of the NFW value (a cored profile gives 0.015–0.16). The ultra-faint error bar is dominated by the collapse-mass floor and Moster's 10⁹ clamp. Burkert with r_core = r_s and Einasto with α = 0.17 are single declared choices: this is not a claim that all cored profiles fail. The multi-epoch lane (CFG51) was not run.

## Standing

**The debris result is robust to the concentration relation and to an Einasto profile, and it is not robust to a core.** A cusp is what closes the ultra-faints and what over-predicts the classical dwarfs; a core removes both. Nothing here says the theory is closed.
