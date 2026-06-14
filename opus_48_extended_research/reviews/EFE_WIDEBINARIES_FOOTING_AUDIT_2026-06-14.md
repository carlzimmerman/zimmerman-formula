# Audit — EFE + Wide-Binaries front: which a0 did Fable use?

*Opus 4.8 independent footing audit, 2026-06-14. Front: `efe_widebinaries`. Framework a0 = 9.36e-11 m/s^2
(= c^2 sqrt(Lambda/32pi) = (c/2)sqrt(G rho_DE), pure dark energy). Rule (both ways): a verdict at the wrong a0 is
invalid — retract false-deficits AND false-wins. Do NOT modify real_research/.*

## Where a0 enters this front
The EFE strength and the wide-binary boost depend on a0 ONLY through `y = g_ext/a0` (and `g_int/a0` in the
transition regime). Lower a0 => larger y => MORE external-field Newtonization => SMALLER boost. The MW external
field at the Sun is g_ext ~= V^2/R ~= 2.1e-10 m/s^2 (convention-fixed, footing-independent), so:
- framework a0 = 9.36e-11 => y = 2.22-2.30  (prompt's "2.3")
- canonical  a0 = 1.20e-10 => y = 1.73-1.79  (prompt's "1.8")
- cH0/Z footing 1.124e-10  => y = 1.85-1.86  (the recurring rho_total/cH0 bug)

Deep-MOND subtlety (already self-corrected in the corpus, `EFE_VS_Z_CORRECTION_2026-06-09.md`,
`reviews/efe_vs_z_recompute.py`): in the DEEP-MOND regime the EFE *suppression RATIO* is a0-INDEPENDENT (the
sqrt(a0) cancels; depends on g_ext/g_N only — I reproduced this exactly, ratio 3.452 at all three a0). The a0
footing matters for the wide-binary gamma SPECIFICALLY because WB pairs sit in the *transition* regime
(g_int ~ a0), where gamma=G_eff/G depends on y=g_ext/a0.

## Script-by-script footing verdict

| script | a0 used | y reported | footing call |
|---|---|---|---|
| `reviews/widebinary_chae2601_confront.py` | **9.36e-11 + 1.2e-10** (both) | 2.22 / 1.73 | CLEAN |
| `reviews/widebinary_saadting_2603_confront.py` | **9.36e-11 + 1.2e-10** (both) | 2.22 / 1.73 | CLEAN |
| `reviews/toe_law/mi_f4_widebinary_efe.py` | **9.36e-11 primary + 1.2e-10** | **2.30** / 1.79 | CLEAN |
| `reviews/project14_wide_binaries.py` | 9.36e-11 (computed correctly) | prints 2.23 | CLEAN |
| `efe_clinch_framework.py` | **9.36e-11 re-anchored + 1.2e-10 rival** | n/a (SPARC) | CLEAN |
| `reviews/project_wide_binary_prediction.py` | **cH0/Z = 1.124e-10** (footing BUG) + hardcoded y=1.86 | 1.86 | **MIS-FOOTED** |
| `EFE_paper.tex` (Zenodo) | mixes: a0 from Lambda, but EFE quoted as **1.8 a_0** (canonical) | 1.8 | **MIS-FOOTED text** |
| `sparc_efe_real_externalfield.py`, `sparc_efe_per_galaxy_environment.py` | 1.2e-10 | n/a | non-load-bearing (null either way; superseded by clinch) |

## The two real footing errors — and their DIRECTION

### 1. `project_wide_binary_prediction.py` — cH0/Z footing bug (mild FALSE-WIN)
Line 35 computes `a0 = c*H0/Z` with H0=67 km/s/Mpc and Z=2sqrt(8pi/3). This evaluates to **1.124e-10**, NOT
9.36e-11 — it is the rho_total/cH0 footing, 20% ABOVE the framework value (the exact "footing bug" MEMORY flags;
`cH0/Z` uses rho_crit, the framework uses rho_DE = `cH_Lambda/Z = cH0 sqrt(OmegaL)/Z = 9.36e-11`). Section 2 then
HARDCODES `y = 1.86`, which is internally consistent with the script's own wrong a0 (g_ext/1.124e-10 = 1.86) but
NOT with the framework's footing.

Re-run on the framework a0 (y = 2.23 instead of 1.86):
- simple-mu boost: **+13.4% -> +11.6%** ; standard-mu: **+2.6% -> +1.8%**

Direction: **FALSE-WIN (mild).** The wrong (higher) a0 understated y, so it OVERSTATED the framework's WB boost by
~2 percentage points. The framework's true predicted signal is SMALLER (~2-12%, low end ~1.8%). The doc's verdict
band "~3-15%" should read "~2-12%". Non-load-bearing: the verdict (marginal / contested / non-diagnostic /
"neither confirms nor refutes") is unchanged.

### 2. `EFE_paper.tex` — wide-binary boost quoted at canonical 1.8 a_0 (mild FALSE-WIN)
Lines 120, 146-147: "a Milky-Way-like field (1.8 a_0)" and "the framework here predicts a small residual boost
(~+5%)". The **1.8 a_0** EFE strength is the canonical-a0=1.2e-10 reading; on the framework's OWN a0=9.36e-11 the
same physical g_ext is **2.3 a_0**, so the boost is SMALLER. Standard-nu boost: 1.117 at y=1.8 -> ~1.078 at y=2.3
(i.e. ~+5% -> ~+4%). Line 31 separately quotes a_0~=1.2e-10 in the intro framing while line 156 gives the
framework a_0=c^2 sqrt(Lambda/32pi)=0.9-1.1e-10 — the paper mixes footings in prose. Direction: **FALSE-WIN
(mild)** — the framework's true WB residual is slightly smaller than the paper's +5%. Verdict (small residual
boost, between DM-zero and isolated-MOND, "no detection yet decisive") unchanged.

## The verdict the prompt asked about: "gamma ~ 1.03-1.24"
That range is the framework-footing (y~2.2-2.3) EFE gamma band, computed CORRECTLY in the clean confront scripts:
- `widebinary_chae2601_confront.py` and `..._saadting...`: framework footing gamma in **[1.04, 1.25]**
  (standard-mu 1.04 -> simple-mu 1.25), vs canonical-footing [1.06, 1.30]. The lower framework a0 gives a band
  ~2-4% LOWER than canonical — reported, and it does not flip any verdict.
- The DIRECTION is reported HONESTLY in both scripts: measured Chae/Saad-Ting gamma=1.56-1.60 sits ABOVE even the
  framework's most generous cap on both footings, and "a higher measured boost pulls toward a HIGHER effective a0,
  so the LOWER rho_DE footing sits slightly FURTHER from the central value — a mild DIRECTIONAL tension." This is
  the framework-correct read: the lower a0 makes the framework look slightly WORSE against the high measured gamma,
  and the corpus does NOT hide that (no false-win there; if anything it states the small deficit honestly).

So the headline gamma band is on the CORRECT (framework) footing. The only over-statements are the two mild
false-wins above (project_wide_binary_prediction.py's +13%/+3% and the paper's +5%), both of which made the
framework's predicted SIGNAL look ~2 points larger than the framework footing gives.

## Both-ways summary (predicted EFE gamma = G_eff/G, g_ext = 2.08e-10)
| footing | y=g_ext/a0 | gamma_std | gamma_simple |
|---|---|---|---|
| framework 9.36e-11 | 2.22 | 1.037 | 1.247 |
| cH0/Z 1.124e-10 (bug) | 1.85 | 1.053 | 1.288 |
| canonical 1.2e-10 | 1.73 | 1.059 | 1.304 |

## Bottom line
- **No false-DEFICIT** on this front. The framework-footing tension against the high measured Chae/Saad-Ting
  gamma=1.6 is reported honestly and is REAL on the framework footing (the lower a0 genuinely predicts a smaller
  boost). It is not a high-priest artifact — it survives at the correct a0.
- **Two mild FALSE-WINS to flag:** (i) `project_wide_binary_prediction.py` uses a0=cH0/Z=1.124e-10 (the
  rho_total/cH0 footing) + hardcoded y=1.86, overstating the predicted boost (+13%/+3% should be +12%/+2% at
  framework a0); (ii) `EFE_paper.tex` quotes the MW EFE as 1.8 a_0 (canonical) and the WB boost as +5%, both ~1
  notch high vs the framework's own 2.3 a_0 / ~+4%. Neither flips a verdict — every binding conclusion is
  "marginal / contested / non-diagnostic / neither confirms nor refutes."
- The strongest, most a0-robust result here is the corpus's OWN self-correction: in deep-MOND the EFE suppression
  ratio is a0-INDEPENDENT (verified exact), so the a0(z) "EFE strengthens/weakens with z" overclaim was already
  retracted (EFE_VS_Z_CORRECTION_2026-06-09.md). The footing only bites in the transition regime, which is exactly
  where wide binaries live.
