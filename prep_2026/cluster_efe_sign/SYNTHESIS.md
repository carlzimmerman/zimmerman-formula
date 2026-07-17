# SYNTHESIS — Cluster-member EFE sigma-spread sign, RECONCILED

Carl Zimmerman's de Sitter-Unruh **modified-inertia** framework
(a0 = cH_Lambda/Z = 9.36e-11 canonical; horizon-derived; own dS-Unruh
interpolation nu(y) = sqrt(1 + 1/y)). This is the well-defined gate that had
to close before the cluster-EFE MG-impossible discriminator (D3 sign-flip,
DOI 10.5281/zenodo.21179352) could be pre-registered.

Lanes: `setup_diagnose.py`/`SETUP.md`, `net_sign.py`/`NET_SIGN.md`,
`robustness.py`/`ROBUSTNESS.md`, `VERIFY.md`. All exit 0, both footings
(a0 = 9.36e-11 and 1.13e-10). Frozen `zimmerman-formula` repo and
`prep_2026/{sigma_spread,cluster_efe_channel,mi_integrator}` left READ-ONLY.

---

## 1. HEADLINE

The GAP-vs-predict sign contradiction is **RESOLVED, and the resolution is
real (not manufactured by a timescale choice).** The banked scripts did not
disagree on physics — two of them carried **labelling errors** on top of one
correct baseline. Corrected: a **less-net-loaded / first-infall member is
HOTTER** than a matched long-resident member at the same cluster-centric
field. That sign is **robust in exactly one zone — first-infall pre-pericentre**
— across both footings, all committed memory timescales, and both kernel
shapes (confirmed 0/125 flips on an independent orbit-distribution scan).
The full **dated pericentre sign-flip** (predict.py sec.2 + D3) is **backwards
in polarity AND timescale-hostage** and is **downgraded / retracted**.
**Outcome (B): SIGN-ROBUST-ONE-ZONE.**

---

## 2. OUTCOME — (B) SIGN-ROBUST-ONE-ZONE

**Is the sign robust or fragile?** ROBUST in one zone; FRAGILE elsewhere.

- **ROBUST (pre-registrable):** first-infall pre-pericentre member = POSITIVE /
  HOTTER / largest excess. 100% of the realistic scan grid (tau_mem 0.1–203 Gyr
  x {exp low-pass, E13 pure-phase} kernel x depth 0.1–1.0 a0 x pre-infall field
  0–0.3 a0 x both footings), and an independent 125-point orbit-distribution
  scan (masses 1e14–5e14 Msun, apo 2–5 Mpc, peri 0.2–0.6 Mpc): **0/125 flips.**
  Structural reason, timescale-free: on a monotonically **rising** approach from
  a low-field past, the causal memory-felt field is **always below** the current
  field, so the member is under-loaded, so nu-boosted hotter, for **any causal
  kernel**. The signal is essentially **monotone in accumulated loading**
  (~time-since-infall), NOT a sharp dated event.
- **FRAGILE (NOT pre-registrable):** recent post-peri / backsplash — COOLER at
  short tau (remembers the hot pericentre) FLIPPING to HOTTER at the committed
  E10 tau (felt dominated by the low pre-infall past); 61%/39% grid split.
  Ancient/virialized ~zero, sign undefined. The **dated pericentre sign-flip is
  timescale-hostage and was backwards in the banked calc** — not pre-registrable.

**Which banked calc was right (correct the wrong ones):**
- `predict.py` **BASELINE** — "plungers / under-loaded members HOTTER"
  (POSITIVE) — **CORRECT.** Matches the code, `rederive_mi_spread.py`, and all
  four lanes here.
- `GAP_STATEMENT.md` **E4/E7** — NEGATIVE "plungers less boosted" + positive-sign
  KILL — **TEXT-LABEL BUG.** It conflates low-theta with low-boost; in EFE
  physics **low theta = less external loading = less suppression = MORE boost.**
  E7's kill-condition is therefore backwards and **self-trips the framework's own
  correct prediction** (this is the verify-lane "weak-memory population self-trips
  E7"). Must be inverted before any pre-registration.
- `predict.py` sec.2 + `D3_amplitude_vs_settledness.py` **pericentre sign-flip**
  (first-infall DEFICIT / post-peri EXCESS) — **INVERTED in polarity** (encodes
  the cold isolated past as low-y = theta~2 = MAXIMAL loading, when isolation is
  a_ex -> 0 = zero loading for any theta) **AND timescale-hostage.** Downgrade /
  retract.

**Pinned timescale.** The framework's committed memory is the eqn-book **E10
covariant kernel tau_mem = 2c/a0 = 2Z/H_Lambda = 203 Gyr (canonical) / 168 Gyr
(alt)** — footing-free (tau*H_Lambda = 2Z = 11.58), the object the MI integrator
(19/19) and `mi_spread.py` actually integrate. This follows **algebraically from
the kernel, independent of any sign** — it is not tuned to buy the reconciliation.
Cluster crossing ~1–2 Gyr, so tau_mem(E10)/T_cross ~100–200x => **DEEP ADIABATIC**:
felt loading = ~203-Gyr average of a_ex, dominated by the isolated pre-infall past
for every member. The 0.45 Gyr Lorentzian used by predict.py/D3 is the dwarf-v3
memory, **NOT anchored to E10**; it is the only thing that made the pericentre flip
a resolvable sub-orbit transient. Dropping it for E10 **freezes the flip out** —
exactly the correction `mi_spread.py` already made for the star-orbit observable
(6–13% -> sub-percent). Honest caveat: E13's |K| = 1 pure-phase branch means a
one-time ramp is felt with gain ~1 and a phase **delay** (not a hard freeze), so a
group-delay transient of order the delay may survive — but its **sign is
unchanged** (less-net-loaded = hotter); only magnitude/transient-survival is
timescale-hostage.

**History-spread magnitude vs the shared boost.**
- **Shared instantaneous theta(y_cur) boost** = the banked **6–13%** band
  (reproduced 6.1–12.0%, fiducial theta0=2 -> ~9.5–10.4%). This is
  **current-configuration / partly MG-SHARED** — MG has its own theta_MG(y_cur)
  EFE — so it is **NOT the discriminant.**
- **MG-impossible HISTORY spread** (at fixed y_cur AND fixed current field) rides
  on top of that boost. At the committed **E10 203/168 Gyr** memory it is
  **residence-time-limited: ~0.3–1.5%** absolute (relational Delta ~4–9.5%,
  ~78% grid-robust), because both members lag the field nearly equally. It only
  reaches **~7–24%** at the short (secularly-unstable-band) 0.45 Gyr corner.
  So the practically-detectable MG-impossible signal at the framework's own
  committed timescale is **modest, a sub-fraction of the shared boost.**

**Both footings.** Materially identical: <2% difference on every sign fraction;
tau*H_Lambda = 2Z = 11.58 is footing-free. Neither a0 value changes the verdict.

**RAW-LOADING(+) vs MEMORY(-) competition — resolved as an artifact.** In field
space both branches agree (under-loaded = hotter); the spurious "-cooler" branch
came only from the y_hist-as-loading encoding bug. Net sign is set unambiguously
by sign(a_ex,felt - a_ex,now). No real competition.

**Theorem-grade claim (unchanged, sole).** **MG = 0 at fixed true field** — MG's
EFE is instantaneous, so two members at identical current field have identical MG
sigma regardless of history. Verified symbolically (d/d(history) = 0, any
interpolation, any a0). The **EXISTENCE** of the fixed-field history spread is
therefore MG-impossible and pre-registrable **regardless of sign.** (Honest: the
sympy "theorem" is a construction — there is no history variable in the algebraic-
MOND EFE to differentiate — but the underlying physics, Milgrom's instantaneous
EFE, is correct.)

**Verifier caveats folded in (refine, do not overturn B):**
- **Projection scatter + same-signed tidal confound are UNMODELED** in all lanes.
  Tidal heating/stripping correlates with infall time in the **same direction** as
  the MI sign handle — degenerate. Zone-tagging assumes perfect phase-space
  labels. => the sign is robust in **dynamics-space**, but its recoverability as a
  clean **observable** is NOT yet established.
- The "100% robust" headline is the **absolute** statistic; the more observable
  **relational** statistic is ~78% robust. Both are shown; do not oversell.

---

## 3. PRE-REGISTRATION STATEMENT (corrected, internally consistent)

**Pre-registrable — TWO tiers:**

**(i) EXISTENCE (theorem-grade, MG-impossible, sign-independent):**
> At fixed cluster-centric gravitational field, cluster members exhibit a
> nonzero internal-sigma spread correlated with infall history. In any
> instantaneous-EFE gravity (MG/AeST, Milgrom 1983) this spread is exactly zero;
> a nonzero fixed-field history spread is MG-impossible. (Sole theorem-grade
> claim; independent of the sign and of the s = -1 postulate.)

**(ii) LEADING SIGN — pre-register ONLY the first-infall pre-pericentre zone
(Outcome B), conditional on s = -1:**
> Among members matched at the same cluster-centric field, **first-infall
> pre-pericentre members are HOTTER (larger internal sigma) than matched
> long-resident / post-pericentre members**; equivalently, sigma-excess
> **decreases monotonically with accumulated loading (~time-since-infall)**.
> This inverts GAP_STATEMENT E4's negative label and the D3 pre-peri-deficit,
> and matches predict.py's baseline. Magnitude: ~0.3–1.5% absolute / ~4–9.5%
> relational at the framework-committed E10 (203/168 Gyr) memory, up to ~7–24%
> only if the memory is short (0.45 Gyr). Falsifier (corrected polarity): a
> significantly **NEGATIVE** fixed-field sign (first-infall COOLER at >=3sigma),
> or zero spread. CONDITIONAL on the s = -1 postulate (s = +1 flips it) and on
> resolving observational zone-tagging + breaking the same-signed tidal
> degeneracy — neither yet demonstrated.

**Do NOT pre-register:** the dated pericentre sign-flip (predict.py sec.2 + D3,
DOI 10.5281/zenodo.21179352) — backwards in polarity and timescale-fragile.
**That D3 sign-flip pre-registration should be DOWNGRADED / retracted.**

MI-class-generic (MI-vs-MG, not this-framework-vs-Milgrom). No "proves". a0 value
and s = -1 are POSTULATES. Credit Milgrom 1983 / 1999 PLA 253:273 / 2022 PRD 106
064060.

---

## 4. NEXT

1. **Fix the prediction lane in the frozen repo (on Carl's go):** re-issue
   `GAP_STATEMENT.md` E4/E7 with the corrected POSITIVE sign and the INVERTED
   kill-condition (first-infall COOLER = falsifier); annotate predict.py sec.2 +
   D3 as downgraded/retracted for the pericentre flip.
2. **Release the D3 hostage:** amend DOI 10.5281/zenodo.21179352 to the
   existence-only + first-infall-hotter statement above.
3. **Close the two real gaps before claiming detectability:** (a) forward-model
   projection scatter + noisy phase-space zone proxies; (b) break the same-signed
   tidal (heating/stripping) degeneracy — an infall-time-correlated confound that
   currently mimics the MI sign.
4. **Optional physics follow-on:** compute the explicit E13 K(Box_u) group delay
   to settle whether any pure-phase transient survives at E10 tau (sign already
   fixed; only magnitude/transient-survival is at stake).
