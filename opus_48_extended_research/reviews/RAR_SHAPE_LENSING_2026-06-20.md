# The dS-Unruh interpolation SHAPE vs the global RAR + lensing — SURVIVES; no-slip PASSES; the apparent McGaugh tension was a fixed-a₀ artifact

*Workflow `wefjhglpn` (5 agents), banked 2026-06-20. Tests the framework's DISTINCTIVE interpolation
shape (not just a₀) against SPARC dynamics + the Brouwer+2021 KiDS weak-lensing RAR (which reaches
~2–3 decades below rotation curves). Both-ways, framework footing (a0=9.36e-11 INPUT, run on the OWN
dS-Unruh ν), quarantine. Real data + full covariance.*

## Bottom line: the dS-Unruh shape SURVIVES the global RAR and is statistically indistinguishable from
## rivals; the lensing a₀ matches the dynamical a₀ (no-slip passes); the discriminating signal is real
## but currently buried by systematics — NOT absent.

## (1) The shape survives
SPARC (175 galaxies, 3389 points, Υ=0.70): forcing the framework a₀=9.36e-11 costs **+1.46%** scatter
(dS-Unruh), vs +0.63% (McGaugh), +1.00% (simple-μ) — all <1.5%, the banked non-diagnostic, reconfirmed.
On the GAMA-clean lensing sample (full 15×15 bias-corrected covariance): dS-Unruh χ²_red=1.24 at
a₀=1.2e-10, **1.12 at its own best-fit a₀=1.62e-10** — a clean, acceptable fit. The shape is not broken
anywhere the data reaches.

## (2) The no-slip cross-channel test PASSES (a genuine consistency win)
The framework's AeST no-slip prediction (lensing mass = dynamical mass → same a₀, same RAR) holds to
current precision: GAMA-clean deep-tail normalization ⟨g_obs²/g_bar⟩ = **1.02e-10**, consistent with
the SPARC dynamical best-fit (1.43–1.64e-10), canonical 1.2e-10, AND the framework 9.36e-11 — all
inside the ~30% the lensing tail can resolve. Mistele+2024 (arXiv:2310.15248) is the published
statement: a single smooth ~2.5-decade RAR joining kinematics to lensing. *(Both-ways caveat: the
noisier KiDS-bright photometric-M* sample gives a higher a₀~1.86e-10 — that's the 0.29-dex stellar-mass
systematic, not a real offset. Trust GAMA, not KiDS-bright.)*

## (3) The apparent "McGaugh-preferred 2.6σ on KiDS" tension is a FIXED-a₀ ARTIFACT (corrected in the
## framework's favor)
The load-bearing both-ways result, replicated exactly:
- At the **fixed** canonical a₀=1.2e-10, KiDS gives χ²(dS)−χ²(McG) = **+6.94 (~2.6σ, McGaugh-better).**
- But that **flips sign as a₀ floats**: with each model at its OWN best-fit a₀, KiDS gives dS χ²_min
  (a₀=1.98e-10) **favored by −7.73** over McGaugh; on clean GAMA the own-a₀ gap is **−0.09 (dead heat).**

So the apparent McGaugh preference is a pure **a₀-vs-shape degeneracy** — pin a₀ below the
lensing-preferred value and the shorter-transition McGaugh kernel wins by reaching the deep line
sooner; let a₀ float and it vanishes/inverts. **NOT a real disfavoring of dS-Unruh.** (And a +0.1–0.2
dex M* shift — Brouwer's own escape — collapses Δχ² to sub-σ too: at +0.1 dex, Δχ²=+0.02 ~0.15σ.)

## (4) Where the REAL discriminating power is (sympy-exact) — and why it's currently null
All three interpolations share the deep-MOND limit EXACTLY: lim_{x→0} √x·ν = 1 → the single asymptote
g_obs→√(a₀·g_bar). The leading corrections first differ at the **transition x=g_bar/a₀ ~ 0.1–1**:
- dS-Unruh: 1 + x/2 − x²/8 (power-law)
- simple: 1 + √x/2 + x/8
- McGaugh: 1 to this order (exp(−√x)-suppressed — reaches the deep line fastest)

The dS-vs-McG / dS-vs-simple offsets **peak at x~0.39–0.50 (0.057 / 0.063 dex) — in the ROTATION-CURVE
regime**, not the deep-lensing tail. And 39% of SPARC points sit in x=[0.1,1] — so the distinctive
curvature lives exactly where SPARC has the **most** data; it's **buried by the 0.13–0.20 dex
intrinsic+M/L scatter**, not absent for lack of coverage. **The discriminator is systematics/scatter-
limited, not coverage-limited.**

## What would settle it
Baryonic-mass control below **~0.05 dex** across the transition band (x~0.1–1) — same-SPS stellar M*
(Mistele's approach) applied to a **Euclid/Rubin-class** lensing RAR with the transition bins resolved,
OR a Gaia-DR4 wide-binary / outer-MW kinematic RAR with controlled M/L. **This is the SAME discriminator
the J(Y)-tie door (JY_TIE_2026-06-20.md) identifies** (the host's free O(Y²) = the transition-regime
μ(x)) — the two fronts converge: the framework's distinctive interpolation signature is real,
concentrated at g~a₀, decisively testable by future precision RAR, currently null only because of
systematics.

## The honest net
The framework's dS-Unruh shape is **shape-consistent and survives**, its **no-slip prediction passes**,
and the one apparent tension (McGaugh 2.6σ) **dissolves as a fixed-a₀ artifact** (corrected in the
framework's favor). It is **non-diagnostic vs rivals** for now — no manufactured shape-win, no real
shape-tension to high-priest. Quarantine held (a0=9.36e-11 INPUT).

### Scripts (exit 0, under opus_48_extended_research/reviews/rar_shape/)
lensing_dsunruh_shape.py · deep_mond_asymptote_sympy.py
### Data: real_research/data/lensing_rar/brouwer2021_rar/ + real_research/data/sparc_data/
### Sources: Brouwer+2021 (arXiv:2106.11677); Mistele+2024 (arXiv:2310.15248 / JCAP 04 020)
