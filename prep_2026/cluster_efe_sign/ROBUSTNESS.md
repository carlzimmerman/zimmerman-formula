# Cluster-member EFE sigma-spread — SIGN robustness / kill-switch map

**Lane:** robustness / kill-switch. **Script:** `robustness.py` (exit 0, `robustness.out`).
**Verdict: OUTCOME B — SIGN-ROBUST-ONE-ZONE.** The infall-phase sigma-spread sign is
**robust and pre-registrable in the first-infall pre-pericentre zone (sign = HOTTER)**, and
**timescale-hostage / NOT pre-registrable** in the post-pericentre / backsplash / ancient
zones. Both footings (a0 = 9.36e-11 / 1.13e-10). MI-class-generic (MI-vs-MG). a0 value and
the s=−1 postulate are POSTULATES; the sign depends on s=−1. No "proves".
Credit: Milgrom 1983 (MOND) / 1999 PLA 253:273 (nu-kernel) / 2022 PRD 106 064060 (MI-EFE).

---

## 1. The contradiction, resolved (which banked calc was right)

The banked lanes clashed on sign because of **two labelling errors on top of one correct
baseline**, not a numerical disagreement. All lanes use the same boost
`B(A) = 1/mu_fw(A/a0)`, `A = a_in + theta·a_ex`, `theta` decreasing. `B` is **monotonically
decreasing in the loading A** (verified symbolically, `dB/dA < 0` everywhere): more external
loading ⇒ more Newtonian ⇒ **less boost ⇒ COOLER**; less loading ⇒ **more boost ⇒ HOTTER**.

| banked calc | sign it prints | verdict |
|---|---|---|
| **predict.py baseline** ("plungers/backsplash HOTTER") | POSITIVE | **CORRECT** — matches the code + `rederive_mi_spread.py` |
| GAP E4/E7 ("plungers less boosted", NEGATIVE) | NEGATIVE | **TEXT-LABEL BUG** — conflates "low theta" with "low boost"; low theta = **less** loading = **more** boost |
| predict.py §2 + D3 pericentre flip (first-infall DEFICIT / post-peri EXCESS) | flip | **BACKWARDS** — encodes "cold isolated past" as low-y (= maximal theta-loading) instead of a_ex→0 (zero loading). In field-space the polarity inverts. |

**GAP E7's kill condition self-trips.** E7 reads *"sign statistic significantly POSITIVE
(plungers more boosted) at ≥3σ falsifies."* But the framework's own correct prediction **is
positive** (first-infall hotter, 100% of the scan grid). A real detection of the true signal
would be logged as a falsification. **E7's kill polarity is inverted and must be replaced:**

- **Corrected KILL** = first-infall members significantly **COOLER** (excess < 0) at ≥3σ, OR
  the fixed-field spread consistent with **zero** at ≥3σ power.
- **Corrected SUPPORT** = first-infall **HOTTER** + spread in the 6–14% envelope + E6 radial rise.
- E5 (DS-substructure cut) and E6 (radial-profile separator) are unaffected — only the sign polarity flips.

---

## 2. Separation of the two pieces (raw-loading vs memory — the "competition" dissolved)

- **Instantaneous `theta(y_cur)` boost** — the banked **6–13%** (reproduced both footings). This
  is the *current-configuration* piece: a member currently plunging (high `y_cur`, low theta) is
  less-loaded ⇒ hotter. **Partly MG-SHARED** (MG also has a `theta_MG(y_cur)` EFE) — not by
  itself MG-impossible.
- **History piece (MG-impossible)** — at **fixed current field AND fixed `y_cur`**, two members
  differ only through the **memory-weighted felt field** `a_ex_felt`. Sign of the relational
  excess = `sign(a_ex_cur − a_ex_felt)` — **hotter iff felt field is below current field**.
  MG gives `a_ex_felt ≡ a_ex_cur` ⇒ exactly zero (theorem, re-verified symbolically, any a0,
  any interpolation).

The verify lane's earlier "raw-loading (+) vs memory (−) compete, net ambiguous" was an
**artifact of the y_hist-as-loading bug**. Once the felt field is written in FIELD space, both
pieces are the same monotone `B(loading)` and **reinforce** — they do not compete.

---

## 3. The timescale pin (the crux)

Two banked memories disagree ~450×:

- **E10 covariant kernel:** `tau_mem = 2c/a0 = 2Z/H_Λ = 203 Gyr (canonical) / 168 Gyr (alt)`,
  footing-free (`tau·H_Λ = 2Z = 11.58`). This is the **committed** framework memory, `>>` the
  cluster crossing time (~1–2 Gyr) ⇒ **deep adiabatic**.
- **dwarf-v3 Lorentzian corner ~0.45 Gyr** (used by predict.py/D3) — makes the flip a resolvable
  sub-orbit transient, but is **not** anchored to E10.

The scan sweeps the **whole range 0.1–203 Gyr** and **both kernel shapes** (Mode-II exp
low-pass AND the **E13 |K|=1 pure-phase group-delay** branch). Result:

- The **first-infall** sign is **timescale-INDEPENDENT** (rising field ⇒ felt < cur for *any*
  causal kernel ⇒ always hotter).
- The **post-peri absolute** sign **flips with tau**: cooler at short tau (felt remembers the hot
  pericentre) → hotter at the E10 deep-adiabatic end (felt dominated by the low pre-infall past).
- At the **committed E10 memory**, the **population-relational** spread is **small/frozen**
  (~0.3–9.5%, both members lag equally — residence-time-limited), reproducing exactly the
  correction `mi_spread.py` already made for the star-orbit lane (6–13% → sub-%). The larger
  numbers only appear at the un-anchored short-tau (dwarf-v3) end.

---

## 4. The pre-registrability map (both footings)

| zone | field slope | sign of history excess | robust? | pre-registrable? |
|---|---|---|---|---|
| **first-infall pre-peri** | rising | **+ HOTTER** (100% of grid) | **YES** — all tau, both kernels, both footings, depth 0.1–1.0 a0, pre-field 0–0.3 a0 | **YES** |
| recent post-peri | falling | − at short tau, + at E10 tau | **NO** (61%/39%) | no (timescale-hostage) |
| backsplash | rising (later orbit) | tau-dependent | no | no |
| ancient / virialized | ~constant, phase-mixed | ~0, undefined | no | no |

**Population-relational discriminator** (the honest MG-impossible observable, no adiabatic
reference needed): `Δ = sigma_excess(first-infall) − sigma_excess(post-peri)` at matched current
field. `Δ > 0` (first-infall hotter than post-peri) wherever the signal is **resolvable**
(short-to-moderate tau, magnitude ~7–30%); freezes toward zero / ambiguous at the deep-adiabatic
E10 end. **MG gives Δ = 0 identically.**

---

## 5. What to pre-register

1. **PRE-REGISTER** — first-infall pre-pericentre members are **HOTTER** (positive fixed-field
   sigma excess) than settled/post-peri members at the same cluster-centric field. Robust across
   the entire realistic parameter space. **This depends on the s=−1 postulate — state it.**
2. **DO NOT PRE-REGISTER** — the pericentre sign-**flip** (banked predict.py §2 + D3
   "No Pump-Free Corner", DOI 10.5281/zenodo.21179352). It is backwards in polarity AND
   timescale-hostage. The D3 sign-flip pre-registration is the hostage this lane releases:
   **only the first-infall-hotter sign and the existence of the fixed-field spread survive.**
3. **CORRECT GAP_STATEMENT.md E4/E7** — invert the kill polarity (§1 above). The frozen repo
   is read-only; this correction is banked here for the maintainer to fold into the estimator spec.
4. **THEOREM-GRADE (unchanged):** MG = 0 at fixed **true** field. The **existence** of the
   fixed-field spread is MG-impossible and pre-registrable **regardless of sign**; the first-infall
   sign is an **additional** (postulate-dependent) handle. Magnitude stays kernel/tau-hostage
   (6–13% instantaneous theta piece is partly MG-shared; the MG-impossible history piece is small
   at the committed E10 memory).

**Scope:** MI-vs-MG (MI-class-generic; also non-zero for Milgrom's linear no-EFE MI). Not a
this-framework-vs-Milgrom test. Underpowered on in-hand data either way (GAP §3: 0.1–0.4σ).
