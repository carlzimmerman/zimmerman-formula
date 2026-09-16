# G152 — THE INVENTORY REVISION: the empirical count after waves 4–8

**Status:** 2026-09-16. G089's dimensionless inventory is re-run with the
wave-4–8 landings: G119 (the 0.62 = the kernel value), G124 (the 1.43 = a
shape functional), G095 (alpha = 2/3 structural; beta = 3/4 covariance),
G122 (the r^-1 dust shape, p* = +0.99), G099 (the MIGHTEE deep offset, an
OPEN). Every move below is a transcription of the committed landing
documents (their numbers re-stated, not recomputed); the only arithmetic
performed here is the counts ledger (C7), verified in-script. The rule set
is G089's own: DERIVED (a theorem of the committed chain), EMPIRICAL
(measured), CIRCULAR (ruled out, listed not recomputed), OPEN (a live
discrepancy with its instrument named).

---

## 1. THE SIX LANDINGS, AND WHAT EACH DOES TO THE LEDGER

### (a) 0.62 = r_break/r_M → DERIVED (G119)
The registered 6.1 kpc break IS the framework's own full-kernel value:
the zero-parameter μ₂-kernel solve at the registered inputs (a0 canonical,
g_ext L240 = 2.146e-10, M_b = 6.5e10, R_d = 2.5 kpc) gives r_cut = 6.13 kpc
→ **r_cut/r_M = 0.6232 vs 0.6200 (+0.5%)**, G119 V1 PASS. The input is
environmental only (the local field and the MW's baryon setup — measured
inputs, the same status as Λ); no fit parameter was touched. The deep-form
EFE line 0.6605 (+6.4%) is the kernel-free face; the kernel's interpolation
near g ~ a0 closes the last 6%. The alt footing (0.7250, +16.9%) is the
footing tension (A12), not a 0.62 matter. **A7: EMPIRICAL → DERIVED.**
Honest note: this is the strongest of the five promotions — a measured
break reproduced at +0.5% by the theory's own kernel on registered inputs.

### (b) 1.43 = r_half/r_M → DERIVED, a shape functional (G124)
G107's measured crossover ratio (median 1.43, 12/12 in [1/3, 3], band
[1.13, 2.05]) is reproduced by the committed-profile model with zero new
free parameters: f_gas(r) = M_gas/[M_gas + M_star + M_ph + M_dust](<r)
(baryons from the X-COP tables + h67b stars; phantom from the law itself,
M_ph(<r) = M_b(R500) r/r_M; dust from the G108 envelope, s = 2.38). Model
median **1.73**, 12/12 in [1/3, 3] under both the pooled-slope and the
closure amplitude conventions; the measured 1.43 sits −17% below the
zero-parameter median, inside the band at its low edge. Per-cluster
tracking Spearman **+0.958** — the model says WHICH clusters cross early
or late. The ratio is a SHAPE FUNCTIONAL: the phantom and dust AMPLITUDES
cancel (d ln/d ln A_ph = −0.008, d ln/d ln A_dust = +0.030); the value is
pinned by the baryon core c_b (+0.261), the envelope slope s (+0.254) and
the r_M normalisation alone. The 0.3-gap residual is the registered G108
V2 inner-window overshoot (34/292 negative bins), quantified as a ratio
shift, not a parameter. The alternative footing r_half/r_a0,tot = 0.83
(model) vs 0.84 (measured, 10/10). **A14 (the 1.43 row): EMPIRICAL →
DERIVED.** Honest limit: derived UP TO the committed shape band — c_b and
s are measured inputs, not tuned targets; the closed form is an elementary
profile with r_half the unique root of a monotone transcendental (no
radical), G124 V1.

### (c) the 2/3 exponent → DERIVED, structural (G095)
The temperature-ratio closed form T_obs/T_pred = 2 (M_dyn/M_b)(r_M/r)
plus the overdensity-500 definition R500 ~ M500^{1/3} gives the law's
structural exponent **alpha = 2/3** (virial T of the total enclosed mass
against the baryon floor; the −1/3 is textbook cluster self-similarity
T ~ M^{2/3}). alpha = 1/2 (BTFR-style) would require r ~ M_dyn^{1/2},
neither face. Empirically alpha_i spans 0.634–1.105, median 0.752 ± 0.115:
**2/3 sits at 0.74σ; 1/2 is excluded at 2.19σ.** The per-cluster exact
relation is the 3-factor closed form, not a power law. **A15: EMPIRICAL →
DERIVED** (the value 2/3 follows from the definitions; the pointwise
alpha_i are the check that prefers it).

### (d) the 3/4 beta → DERIVED, the M500–M_b covariance (G095)
The closed form's residual M_b-drift cancels exactly at **beta = 3/4**:
M_b-independence of T_obs/T_pred iff (2/3)(β−1) + 1/6 = 0 ⇔ β = 3/4. The
sample's fitted M500 ~ M_b^β gives β = 0.634 ± 0.107 — 3/4 at 1.08σ — and
the ratio's 0.05-dex constancy across all 12 clusters is that covariance
doing its job (residual 0.079 dex about the closed form). **A16:
EMPIRICAL → DERIVED.** Honest note: 3/4 is the derived constancy
CONDITION; the measured covariance (0.634 ± 0.107) is the empirical CHECK
that nearly satisfies it — the classification is of the relation, and the
check is on the record.

### (e) the r^-1 dust shape → DERIVED, p* = +0.99 (G122)
The coherency systematic decomposes: the pooled R(x) residual is monotone
in r/R500 (Spearman −1.000), and the closed form R = [2x/(x−1)]·a_c·(r/R500)^−p
with ONE universal **p* = +0.99** — the framework's own r^-1 — closes the
curve to **0.097 dex** from 0.313 (12/12 clusters < 0.15; the literal
3-parameter form without per-cluster freedom closes at 0.119). The
free-dust normalization IS one profile shape (r/R500)^−0.99 with a
per-cluster amplitude. **A17: EMPIRICAL → DERIVED.** Honest limit: the
SHAPE is derived/closed; the amplitude's mass-ordering (rho(amp, M500) =
−0.59, p = 0.045; q = −0.41) and its residual floor remain the named thorn
(see V3).

### (f) the 1.4–1.6× MIGHTEE deep offset → OPEN, the footing's pressure (G099)
G099: zero-parameter rms 0.190 dex on 80 rings (≤ 0.2 PASS), scatter 0.132
dex AT the SPARC benchmark, and a systemic deep-end offset −0.151 ± 0.015
dex (−9.9σ, n = 72) — the data sit **1.4–1.6× above** the law's committed
amplitude at g_N < 0.2 a0, matching the paper's OWN a0 = 1.69 ± 0.13e-10
preference on this sample (its 2σ tension with the SPARC-anchored RAR).
This is not derived and not dismissed: it is a measured, instrumented
discrepancy — the deep-end pressure on the footing tension (waveboard:
"a real systematics-level pressure on the footing, which was 0.754–0.783;
MIGHTEE pushes HIGHER"). Shape (−1/2) confirmed. **A18: EMPIRICAL →
OPEN**, registered under A12 (the footing), with MIGHTEE as its pressure
vector; the discriminator is named (the paper's own a0 fit vs the
SPARC-anchored RAR; the G133 MIGHTEE-footing fit is already dispatched).

---

## 2. THE REVISED INVENTORY (old vs new, per entry)

### Table A — the framework's named numbers

| # | Combination | Registered value | G089 class | REVISED class | Reason (landing) |
|---|---|---|---|---|---|
| A1 | Z = √(32π/3) | 5.7888 | DERIVED | DERIVED | unchanged; its VALUE carries the one free datum (§3) |
| A2 | c H0/a0 = Z/√Ω_Λ ("the seven") | 6.9943 ≈ 7 | CIRCULAR | CIRCULAR | L260 Z6: same algebra as the definition |
| A3 | triad σ²/v_flat² = κ = c_s² | 1/2 exact | DERIVED | DERIVED | value inherits n = 2 (A5) |
| A4 | z* = 4 z_c | 4 | DERIVED | DERIVED | unchanged |
| A5 | n = 2 (the μ₂ family) | 2 | EMPIRICAL | **EMPIRICAL** | the ONE empirical premise (STATE.md; G009/G019); untouched by waves 4–8 |
| A6 | κ vs Milgrom's 1/(2π) | Δχ² 63.9 vs 154.3, ~2.2σ | EMPIRICAL | **EMPIRICAL** | the comparative test is measured; the π-free content is A11/C6 |
| A7 | 0.62 = r_break/r_M | 0.6232 kernel (+0.5% vs 0.6200) | EMPIRICAL | **DERIVED** | G119: the registered break IS the zero-parameter full-kernel value at registered inputs; environmental input only |
| A8 | lensing floor ratio | +0.355 dex (2.26×) KiDS; +0.419 (2.62×) re-stack | OPEN | OPEN | unchanged; conversion-class envelope ±0.196 dex |
| A9 | 209.0 / 17.7 M☉/pc² | one law, two reading conventions | DERIVED | DERIVED | unchanged |
| A10 | ⟨Σ_ph⟩(<r_M) = a0/(πG) | 213.75 M☉/pc² | DERIVED | DERIVED | Lean G083; unchanged |
| A11 | geometric π-content | 32π/3, 16π, 4π, π, π/2 | DERIVED | DERIVED | unchanged |
| A12 | footing ratios a0_DE/a0_gal | 0.754–0.783 band | OPEN | OPEN | now carries the MIGHTEE pressure (A18); the 0.7250 alt-footing face of the 0.62 is this item, not A7 |
| A13 | cluster amplitude (T ratio value) | 0.28 ± 0.05 dex / 3.6× | OPEN | OPEN | G095 closed the STRUCTURE (the 0.28 = 2 f r_M/R500) and the scatter (HSE); the amplitude's value remains the open cluster normalization |
| **A14** | **gas-crossover ratio r_half/r_M** | measured 1.43 (12/12); model 1.73 | EMPIRICAL (G107 V2b) | **DERIVED** | G124: a shape functional of the committed profiles (amplitudes cancel); Spearman +0.958; derived up to the shape band [1.23, 2.40] ⊃ measured [1.13, 2.05] |
| **A15** | **T-ratio structural exponent alpha** | 2/3 (emp 0.752 ± 0.115) | EMPIRICAL (G095 V2b) | **DERIVED** | G095: closed form + overdensity-500 def; 2/3 at 0.74σ; 1/2 excluded 2.19σ |
| **A16** | **M500–M_b covariance exponent beta** | 3/4 (fitted 0.634 ± 0.107) | EMPIRICAL (G095 V2c) | **DERIVED** | G095: the derived M_b-independence condition of the closed form; confirmed at 1.08σ by the sample |
| **A17** | **free-dust radial shape p*** | +0.99 (= r^-1) | EMPIRICAL (free-dust profile, G093-family) | **DERIVED** | G122: ONE universal p* closes the coherency curve 0.313 → 0.097 dex (12/12 < 0.15) |
| **A18** | **MIGHTEE deep-end offset** | −0.151 ± 0.015 dex (1.4–1.6×), −9.9σ, n = 72 | EMPIRICAL (G099) | **OPEN** | G099: measured discrepancy, shape confirmed, amplitude conflicted — the footing's pressure (feeds A12); G133 dispatched |

### Table B — the rest of the dimensionless content

| # | Combination | Registered value | G089 class | REVISED class | Reason |
|---|---|---|---|---|---|
| B1 | equipartition M_ph(<r_M)/M_b | = 1, |ratio−1| ≤ 2.2e-16 | DERIVED | DERIVED | unchanged |
| B2 | linear law M_dark/M_b = r/r_M | coefficient 1 | DERIVED | DERIVED | unchanged |
| B3 | coefficient-1 chain (ρ, g², v⁴, c_deep) | exactly 1 | DERIVED | DERIVED | unchanged |
| B4 | Ω_Λ = 32π a0²/(3 H0² c²) | 0.6857 vs 0.6847 | DERIVED | DERIVED | agreement is the CHECK (C3) |
| B5 | flatness residual Ω_dm | 0.2650 | DERIVED | DERIVED | unchanged |
| B6 | scalar w | −1 → +1, 0 at X = 1.4978 | DERIVED | DERIVED | unchanged |
| B7 | coincidence epoch z(w=0) | 0.49 | DERIVED | DERIVED | unchanged |
| B8 | funnel z*(R) = 4z_c; e^{+R/3} flare | 140.63 pc; 9.6472; 2136 | DERIVED | DERIVED | unchanged |
| B9 | GC boundary r_M/r_h = η/2 | 3.39 exact | DERIVED | DERIVED | identity; η measured (B9n) |
| B9n | η | 7.0 ± 1.16 | EMPIRICAL | **EMPIRICAL** | G074: unchanged — one of the five remaining |
| B10 | relation T_pred/T_obs = 0.53² | 0.28 (3.6×) | DERIVED (relation) / OPEN (value) | DERIVED (relation) / OPEN (value) | G095 deepened the relation's derivation (closed form, 2/3, 3/4, HSE scatter); the value remains A13 OPEN |
| B11 | RAR tightness floors | 0.064 / 0.055 dex | EMPIRICAL | **EMPIRICAL** | G010/G013: unchanged — one of the five remaining |
| B12 | dSph floor agreement | median −0.00 dex (7 dwarfs; 0.222/34) | EMPIRICAL | **DERIVED** | re-classified to the B4/B7 convention: the FLOOR σ_pred = (G M_b a0)^{1/4}/√2 is derived; the −0.00 median is the empirical CHECK of it, not a separate datum — same structure G089 already used for B4/B7 |
| B13 | r_in = 0.3 r_M | 0.3 declared | EMPIRICAL | **EMPIRICAL** | G071/G072: declared convention — one of the five remaining |
| B14 | high-z discriminating ratio | 20:1 (0.33/0.13 dex) | DERIVED | DERIVED | unchanged |

### Table C — CIRCULAR (unchanged, 7): C1–C7 as in G089; none of the waves
4–8 landings touch them, and none is recomputed as a coincidence. (G095's
reading of the 0.28 as f^alpha is NOT a power-law claim about the cluster
amplitude — G095 V4(4) explicitly does not re-derive the normalization;
the C-table stands.)

---

## 3. THE COUNTS AND THE PARAMETER COUNT

### The revised ledger (C7 arithmetic, computed)

| Class | G089 | REVISED | Delta |
|---|---|---|---|
| DERIVED | 17 | **23** | +6 (A7, B12, A14, A15, A16, A17) |
| EMPIRICAL | 7 | **5** | −2 (A7, B12 leave; A18 leaves to OPEN) |
| CIRCULAR (ruled out) | 7 | 7 | 0 |
| OPEN | 3 | **4** | +1 (A18 MIGHTEE joins A8, A12, A13) |
| Live entries (A+B, excl. C) | 27 | **32** | +5 new rows (A14–A18) |
| Truly free parameters | 1 | **1** | 0 |

Remaining EMPIRICAL, stated one by one: **A5 n = 2** (the one empirical
premise, SPARC-selected, not free in any fit), **B9n η = 7.0 ± 1.16**
(G074), **B11 the 0.064/0.055 dex floors** (G010/G013), **B13 r_in = 0.3 r_M**
(declared convention, G071/G072), **A6 κ vs Milgrom's 1/(2π)** (the measured
comparative statistics; the value κ = 1/2 itself is Z-derived, C6).

### The parameter count: still ONE (Z) — not fewer, and why

**The theory has exactly ONE free dimensionless parameter after the
revision: Z ↔ Ω_Λ ↔ a0/cH_Λ — unchanged.** The ledger:

1. **Z** — one datum, the vacuum scale in dimensionless form (canonical
   form f(0) = −1, C5's integration constant; G031 Lemma 1: one scale, two
   sectors). Its form √(32π/3) is the canonical coefficient; its VALUE is
   the one measured datum the action itself carries (Λ → a0). Nothing in
   waves 4–8 touches it. To go below one would require deriving the vacuum
   scale's MAGNITUDE from a UV completion (G089 V3(iv)) — not done, so
   "fewer than one" is not available.
2. **Empirical premises, not parameters (unchanged):** n = 2 (A5) — the one
   premise, never fitted; the κ-test statistics (A6) — a measurement of
   MOND's 2π contra the framework's π-free κ.
3. **Measured INPUTS to derived statements, not parameters (grown but
   unchanged in kind):** Λ (into a0); the environmental g_ext L240 and the
   MW setup M_b, R_d (into the 0.62 via the kernel, G119); the per-cluster
   X-COP baryon tables and c_b, the G108 envelope slope s = 2.38 and
   per-cluster dust amplitudes (into the 1.73 and p*, G124/G122); the
   sample's M500–M_b covariance as the check of 3/4 (G095). Each is a
   measured input the theory READS, exactly as Λ is — not a coefficient of
   the action.
4. **The revision adds zero parameters:** five EMPIRICAL→DERIVED moves were
   executed with committed inputs only; one entry moved to OPEN (a
   discrepancy, never a parameter); the parameter count and the premise
   count are separate ledgers (L260 Z5 / G089 V2's own point — the honest
   count is this §3, not C7's old "one scale" phrasing).

**Statement: ONE free parameter (Z); five named empirical premises/inputs
(n, η, floors, r_in, κ-test); four OPEN items; everything else derived.**

---

## 4. VERDICTS

**V1 — the revised inventory is complete and the moves are sourced.**
All six task items land as classified: (a) A7 0.62 → DERIVED (kernel
0.6232, +0.5%, environmental input only); (b) A14 1.43 → DERIVED (shape
functional 1.73, amplitudes cancel, Spearman +0.958); (c) A15 2/3 →
DERIVED (structural, G095); (d) A16 3/4 → DERIVED (the M500–M_b
covariance's derived constancy condition, G095); (e) A17 r^-1 → DERIVED
(p* = +0.99, 0.097 dex, G122); (f) A18 MIGHTEE 1.4–1.6× → OPEN (G099, the
footing's pressure). B12 is additionally re-classified to the B4/B7
check-reading convention (stated explicitly, not smuggled). Counts:
**23 DERIVED / 5 EMPIRICAL / 7 CIRCULAR / 4 OPEN, 32 live entries** —
arithmetic verified (23+5+4 = 32; 23+5+7+4 = 39). **PASS.**

**V2 — the parameter count statement survives the revision: exactly ONE
(Z).** Not fewer: Z remains the one datum whose value is measured rather
than derived; the revision shrank the EMPIRICAL list, grew the DERIVED
list, and added one OPEN — it added zero parameters and removed zero
parameters. The statement is the §3 ledger attached to the §2 table, which
is exactly how G089 V2 survived L260 Z5. **PASS.**

**V3 — the honest statement: the framework's empirical residue, and the
measure of its closure.** Exactly five dimensionless numbers remain
measurement-bound (A5 n = 2; B9n η = 7.0 ± 1.16; B11 the 0.064/0.055 dex
floors; B13 r_in = 0.3 r_M; A6 κ vs 1/(2π)), plus four named OPEN
discrepancies (A8 the lensing-floor absolute value, A12 the footing
0.754–0.783 — now under MIGHTEE's upward 1.4–1.6× pressure, A13 the
cluster amplitude 3.6×/0.28, and the residual floor of the dust-amplitude
mass-ordering, G122's q = −0.41 thorn). The closure measure: of the 32
live dimensionless entries, **23 are derived (71.9%), 5 are measured
(15.6%), 4 are open (12.5%)**, behind ONE free datum (Z). The residue in
one sentence: the theory reads in the vacuum scale (Z), the μ₂ slope
n = 2, one dwarf-scale constant (η), one curve-tightness floor pair, one
declared inner-cut convention, and the κ/2π comparative statistics —
everything else it has printed is algebra on those, and every remaining
discrepancy has its instrument named. What a TOE still needs, in G089's
order: (i) n = 2 from dark-sector microphysics (G009/G019 closed every
structural route); (ii) the footing — now sharpened by MIGHTEE, which
pushes the galactic a0 HIGHER, away from the DE anchor, not toward it;
(iii) the cluster amplitude's mass-ordering (G122's thorn); (iv) Z's
magnitude from a UV completion. **PASS.**

---

## 5. SOURCES (all committed)

- G089 (the inventory being revised; its JSON ledger 17/7/7/3, 1 parameter)
- G119 (the 0.62: full-kernel r_cut = 6.13 kpc → 0.6232, +0.5%; 6/6 PASS)
- G124 (the 1.43: model median 1.73, 12/12 in [1/3, 3], Spearman +0.958,
  amplitudes cancel; 7/8 PASS — the C2 closure FAIL is the registered
  finding)
- G095 (alpha = 2/3 at 0.74σ, 1/2 at 2.19σ; beta = 3/4 at 1.08σ; HSE
  scatter = 0.053 dex; 10/11 PASS)
- G122 (p* = +0.99, 0.313 → 0.097 dex, 12/12 < 0.15; 5/5 PASS)
- G099 (MIGHTEE-HI: rms 0.190, deep −0.151 ± 0.015 dex, −9.9σ, n = 72,
  1.4–1.6×; 2/3 PASS — V2 FAIL is the finding)
- G107 (the measured 1.43 / 0.84 rows, 12/12 / 10/10), G108 (envelope
  s = 2.38; V2 amplitude caveat 34/292), G074 (η = 7.0 ± 1.16),
  G010/G013 (0.064/0.055), G071/G072 (r_in), G002/G009/G019 (n = 2),
  EMPIRICAL_TESTS A13 / L4-33/L4-34 (κ vs 1/(2π)), STATE.md, WAVEBOARD
  (waves 4–8 landing summaries; the MIGHTEE-footing-pressure line).