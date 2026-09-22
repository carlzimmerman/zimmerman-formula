# CAPSTONE — the κ=1/2 channel-count derivation is closed by a no-go

An independent, reproduce-before-contradict audit of the κ=1/2 derivation program
(deepseek PD01/PD05/PD08/PD10/PD22 + G084 + L279). Nine committed, runnable scripts. Conclusion,
stated both ways: **κ=1/2 is an empirically anchored constant, not a first-principles derivation.**
This is neither "provably underivable" (a stale over-claim) nor "derived" — it is *measured, with
structure, and structurally obstructed for the sources MOND governs.*

## The chain of results

1. **κ is not degree-2-dependent** (`K_AUDIT_slope_is_degree2_independent.py`). κ = 1/(2·cp) needs only
   the deep-MOND slope μ'(0)=2cp, which is independent of the OR-composition's degree-2 uniqueness
   (P4) and the completion shape. So the circular degree-2 joint (`K_AUDIT_degree2_circularity.py`)
   is off κ's critical path. κ rests on: (i) two channels, (ii) symmetry + one-channel exactness,
   (iii) cp=1 measured (k01 zero mode).

2. **The two-channel count fails for dust** (`K_AUDIT_two_channel_dust_obstruction.py`). The second
   channel is the metric slip (G_kk = 2∇²(Φ−Ψ)). For a pressureless (dust) source, matter anisotropic
   stress = 0, and the framework's own L279 (lensing=dynamics, γ=1) sets Φ=Ψ → the second channel is
   un-sourced → engaged count = 1 → κ=1, contradicting the measured κ=1/2.

3. **Sourcing channel B is a NO-GO** (`K_AUDIT_channelB_nogo.py`), across all single-field routes:
   scalar (Bekenstein: conformal can't cancel the anisotropic slip universally; disformal is
   GW170817-dead), vector (α₁ = −2(K_B+2) = O(1) un-tunable, plus only one channel), tensor
   (GW170817 + BD-ghost).

4. **Loophole 1 closes harder** (`K_AUDIT_loophole1_closure.py`). A beyond-Bekenstein
   (higher-derivative/DHOST) coupling doesn't help: by the null-cone lemma, GW-safe ⟺ the matter
   metric is conformal to the graviton metric, for *any* coupling — and conformal cannot cancel the
   O(1) slip. Coupling-independent.

5. **Loophole 2 closes** (`K_AUDIT_loophole2_closure.py`). No non-slip second channel exists for
   static dust: the "channel count" is basis-dependent, and the physical invariant (rank of the
   source→engaged-response map) is 1 for dust. The specific non-slip candidates all fail (separate
   scalar violates the one-field ontology; TT graviton polarizations don't source the static
   potential; gradient-invariant branches collapse for a static field).

6. **Loophole 3 closes** (`K_AUDIT_loophole3_closure.py`). Giving up universal lensing=dynamics
   (a source-dependent γ) needs an O(1) slip to engage channel B, which predicts a factor ~2–4
   mismatch between the lensing and dynamical RAR normalisations — contradicting the KiDS
   galaxy-galaxy-lensing RAR (Brouwer 2021) and the framework's own γ=1 lensing success.

## The verdict

The "κ = 1/(channel count)" derivation is **closed by a no-go**: no GW-safe, α₁-safe, single-metric
mechanism delivers the second engaged channel (count 2, slope 2) for the pressureless sources MOND
governs, whether by a metric slip (routes 3–4), a non-slip channel (5), or a non-universal γ (6).
The sharpest single statement: the channel count is basis-dependent, and its physical invariant
(the engaged-response rank) is **1 for static dust**, not 2 — so the observed slope 2 (κ=1/2) is
**empirical**, and cp=1 is measured because the framework's own k01 theorem proves it underivable.

## Two honest caveats (what could still reopen it)

- **DHOST-degeneracy sliver (loophole 1):** a fine-tuned DHOST-degenerate construction keeping
  c_GW=c_light while carrying an O(1) *unscreened* slip is argued implausible (it is exactly the
  fifth-force slip post-GW170817 DHOST suppresses, and must also give γ=1 unscreened AND slope 2),
  but a dedicated DHOST scan is needed to exclude it outright.
- **Lensing confrontation (loophole 3):** the a0_lens ≈ a0_dyn agreement is the published Brouwer
  result + the framework's committed γ=1 fit, not a from-scratch redo of the ESD→g_obs deprojection.

Absent one of these, the derivation is closed. κ=1/2 stands as a measured constant of nature —
two-valued in structure {1/2, 1}, selected to 1/2 empirically (cp to 0.33%), and structurally
un-derivable as a channel count for the matter it describes.
