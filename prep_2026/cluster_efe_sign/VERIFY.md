# VERIFY — cluster-member EFE sigma-spread sign reconciliation (adversarial)

prep_2026/cluster_efe_sign/ · 2026-07-17 · re-ran the three lanes + independent probes.
Framework: de Sitter-Unruh MODIFIED INERTIA (Zimmerman). Credit Milgrom 1983 / 1999 PLA
253:273 / 2022 PRD 106 064060. No "proves". MI-class-generic (MI-vs-MG).

## Re-run status (exit 0, both footings)
- `setup_diagnose.py` exit 0 · `net_sign.py` exit 0 · `robustness.py` exit 0.
- Both footings (a0=9.36e-11 / 1.13e-10) run in every lane; sign fractions differ <2%.

## The seven hunts

**(1) Is the reconciliation REAL, or was the timescale chosen to give the sign?**
REAL. Two separable facts:
- The tau pin follows ALGEBRAICALLY from the kernel, independent of any sign:
  tau_E10 = 2c/a0 = 2Z/H_L, footing-free tau·H_L = 2Z = 11.578 → 203/168 Gyr. It is the
  eqn-book E10 memory committed across the corpus (mi_integrator, mi_spread), not invented here.
- Crucially, the ROBUST sign does NOT ride on the timescale at all: first-infall-pre-peri is the
  hottest zone at EVERY corner in the net_sign table (E10 203 Gyr +0.81%, H_Lambda 17.5 Gyr
  +5.97%, dwarf-v3 0.45 Gyr +3.15%), and 100% positive across tau=0.1–203 Gyr in the robustness
  scan. The timescale pin is used only to DOWNGRADE (freeze) the pericentre flip — it shrinks the
  discriminator's magnitude, i.e. it cuts AGAINST the framework's interest. That is the honest
  direction; a manufactured reconciliation would have used the timescale to inflate a win.

**(2) Does the robust sign survive a REALISTIC orbit distribution + projection + tidal?**
Split verdict — theory-space YES, data-space NOT SHOWN:
- Orbit distribution: CONFIRMED independently. I ran a 125-pt scan the scripts did NOT
  (masses 1e14–5e14, apo 2–5 Mpc, peri 0.2–0.6 Mpc, tau 0.3–203 Gyr, pre-infall field a_pre
  0–0.9 a0) — first-infall was NEGATIVE in 0/125. The physics is orbit-independent: on the
  monotonically-rising approach from a low-field past, the causal-memory felt field is always
  below the current field, so under-loaded → hotter, for ANY causal kernel. The sign only turns
  when a_pre EXCEEDS the matched shell (a member from a DENSER past — no longer "first infall"):
  at a_pre=1.2 a0 vs target ~1.0, excess still +3.5%. So the robust sign is genuinely
  distribution-robust, not one cherry-picked trajectory. **Not manufactured.**
- Projection scatter: NOT MODELED anywhere. Both lanes assume perfect infall-zone tagging
  (first-infall vs post-peri vs settled). Observationally you tag zones only via projected-radius
  / LOS-velocity phase-space proxies with large scatter + interlopers. The pre-registrable
  "first-infall hotter" handle inherits that dilution — unquantified here.
- Tidal confound: NOT MODELED anywhere, and the task flagged it explicitly. Tidal heating/
  stripping correlates with infall time in the SAME direction (dynamically-young first-infall vs
  tidally-processed long-resident), so it is DEGENERATE with the MI sign handle. The additional
  first-infall-hotter handle is therefore NOT a clean stand-alone observable until this is
  broken. This is the single biggest gap between "robust in dynamics" and "pre-registrable in data".

**(3) Kill-switch self-trip anywhere realistic?**
Confirmed as flagged: GAP E7's verbatim kill ("positive sign at ≥3σ falsifies") self-trips the
framework's own correct first-infall-hotter signal (100% of grid). The proposed CORRECTED kill
("first-infall COOLER at ≥3σ, or spread consistent with zero") does NOT self-trip (first-infall
never negative in either the scripts' or my extended scan). Correct diagnosis and correct fix.
Caveat: a NAIVE measurement that fails to isolate first-infall (projection dilution, or lands on
the fragile post-peri population) could read negative and falsely trip — another reason the
projection gap matters operationally.

**(4) Is the shared-vs-MG-impossible separation clean?**
Clean. The relational spread is computed at FIXED theta0 and FIXED current field a_ex(now), so the
shared instantaneous theta(y_cur) boost (the banked 6–13%, partly MG) is a common multiplicative
factor that cancels in the member-to-member difference; only the memory-felt field differs. The
MG-impossible history piece is not contaminated by the shared boost. Reproduced: shared boost
~9.5%, MG-impossible history span 1.3–1.5% (E10) up to 7.7–8.4% (0.45 Gyr).

**(5) Both footings.** Materially identical: every sign fraction within <2%, tau·H_L=2Z
footing-free. Confirmed.

**(6) Sign rides on s=-1 — flagged?** Yes, repeatedly and correctly in both scripts and both
verdicts ("s=+1 flips it"). Adequate.

**(7) Manufactured robust-sign AND manufactured fragile-downgrade, equally?**
Neither is manufactured. The robust sign is real (independent 0/125 orbit-distribution confirm,
structural reason). The pericentre-flip fragility is real (post-peri excess genuinely runs −6% at
short tau to +64% at long tau — a true sign flip, not staged humility). Balanced.

## Residual caveats the verdict should carry (do not overturn Outcome B)
1. **Projection + tidal unmodeled** — the robust sign is established in dynamics-space, not shown
   recoverable in projected phase space; the same-signed tidal confound is a live degeneracy on
   the sign handle. The "first-infall hotter is pre-registrable" claim must be stated as
   *conditional on* solving zone-tagging and breaking the tidal degeneracy.
2. **Magnitude at the committed timescale is modest** — at E10 (203 Gyr) the relational
   population spread freezes to ~4–5% (robustness Delta) and the "absolute" 100%-robust framing
   leans on a settled reference that does not physically equilibrate on 203 Gyr (net_sign's
   "ancient" member is felt≈0.056 a0, barely loaded). The headline "100% robust" uses the
   less-observable absolute statistic over the more-honest 78%-robust relational one; both are
   shown, but the emphasis is slightly generous.
3. **MG=0 "symbolic theorem" is tautological** — the sympy checks (net_sign L189-191,
   robustness L126-128) write the MG expression WITHOUT a history/y variable, so d/d(hist)=0 is
   trivial construction, not derivation. The physical claim (algebraic MOND/AQUAL EFE is
   instantaneous → zero history spread) is CORRECT and standard (Milgrom), so the conclusion
   stands; only the "verified symbolically, theorem-grade" framing overstates what the code shows.
4. **Flip-freeze rests on the E10-governs premise** — the 0.45 Gyr dwarf-v3 corner is a real
   corpus object (used by predict.py/D3); the downgrade of the pericentre flip depends on
   accepting that the horizon memory (not the orbital-band corner) governs the cluster observable.
   Defensible and sign-independent, but a framework-internal choice, not proven.

## VERDICT
**UPHELD (Outcome B), with the projection/tidal caveats made explicit.**
The reconciliation is real, not manufactured. The GAP-vs-predict contradiction genuinely resolves:
predict.py's POSITIVE baseline (under-loaded/first-infall HOTTER) is correct; GAP E4/E7's NEGATIVE
label + positive-sign kill is a real text-label bug (low theta = less loading = MORE boost) and
must be inverted before any pre-registration; predict.py/D3's pericentre sign-FLIP is both
backwards in polarity (isolation mis-encoded as low-y = maximal theta-loading instead of a_ex→0)
and timescale-hostage, and should be downgraded/retracted (D3 DOI 10.5281/zenodo.21179352).

Pre-registrable: (i) the EXISTENCE of a fixed-true-field history spread — MG-impossible,
theorem-grade regardless of sign (physics correct; symbolic "proof" is only a construction);
(ii) the first-infall-pre-peri = hotter correlation — robust across orbit distribution, timescale,
both footings and both kernel shapes, CONDITIONAL on the s=-1 postulate AND on solving
observational zone-tagging + breaking the same-signed tidal degeneracy (neither addressed here).
NOT pre-registrable: the dated pericentre sign-flip. The practically-detectable MG-impossible
magnitude at the committed E10 memory is modest (~few %). No "proves".
Credit Milgrom 1983 / 1999 PLA 253:273 / 2022 PRD 106 064060.
