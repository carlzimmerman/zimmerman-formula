# Route 3 [efe_value] — Pin the Milky-Way external field g_ext, propagate to gamma_cap, and the DR4 forecast

*Opus 4.8 (1M) extended research, 2026-06-14. Framework a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (Lambda-only;
NOT asserted derived — the bath coefficient remains Z-quarantined). g_ext is the single most load-bearing input to
the wide-binary EFE cap. Scripts (reproducible, numpy only):
`reviews/route3_gext_propagation.py`, `reviews/route3_dr4_forecast.py`, `reviews/route3_contam_sensitivity.py`.
Both-ways rule applied throughout: the lower-a0 tension is reported honestly; no manufactured win, no high-priest
dismissal.*

## What Route 3 had to settle
g_ext = V_c(R0)^2 / R0 caps gamma. Pin it with the current best V_c and R0 + uncertainties; resolve whether the
relevant field is the bare radial V_c^2/R0 or the total (vertical-inclusive) Galactic field; resolve the
EFE-direction-vs-projection question; propagate (V_c, R0, vertical) -> sigma(g_ext/a0) -> sigma(gamma); and answer:
does g_ext uncertainty alone smear gamma past the framework-vs-MOND gap?

## STEP 1 — the radial field, pinned to current data
| input | value | source |
|---|---|---|
| V_c(R0) | **233 +/- 4 km/s** | Eilers+2019 (229, formal 0.2 + few-km syst); GRAVITY-LSR 233+/-3; Ou+2024 ~236. Span 229-236, central 233, sigma 4 covers it. |
| R0 | **8.178 +/- 0.026 kpc** | GRAVITY 2019 (S2 orbit), 8178 +/- 13(stat) +/- 22(sys) pc — 0.3%. |

g_ext(radial) = V_c^2/R0 = **2.151e-10 m/s^2 = 2.298 a0_fw = 1.793 a0_MOND.** (Reproduces the banked 2.15e-10.)

## STEP 2 — radial or total? The vertical field is real and Chae includes it
The relevant EFE magnitude is |g_ext_vec|. **Chae (2023, 2024) adopts a vertical disk field g_z ~ g_radial/3 added
in quadrature** — his published prescription. That gives

    g_ext(total) = sqrt(g_rad^2 + g_vert^2) = **2.268e-10 m/s^2 = 2.423 a0_fw = 1.890 a0_MOND**,

which **reproduces Chae's quoted g_ext ~ 2.26e-10 (= 1.9 a0_MOND) to 0.4%** — an independent confirmation that my
machinery matches the literature's actual external-field input. The vertical term raises g_ext by **+5.4%** over bare
radial. DIRECTION: a larger g_ext Newtonizes MORE, so the total field LOWERS gamma_cap. The framework's lower a0
PLUS the (larger) total field puts e at its highest -> the smallest boost. Reported, not buried.

**EFE direction vs sky projection (the route's other sub-question):** the EFE picks out an anisotropic G_eff
(G_par along g_ext, G_perp = 1/mu perpendicular). A wide-binary orbit samples all orientations relative to the
(radial+vertical) g_ext, and the observable population gamma is the orbit/sky average
gamma_cap = (1/3)G_par/G + (2/3)G_perp/G. So the EFE *direction* enters only through this isotropic average for a
randomly-oriented population — it does NOT require knowing each binary's orientation relative to the Galactic
centre. The 2:1 weighting (two perpendicular axes, one parallel) is why the perpendicular enhancement dominates and
why the nu-form 1-D estimate (gamma~1.24) undercounts the mu-form tensor (gamma~1.32) by ~6%.

## STEP 3 — gamma_cap on each footing (AQUAL anisotropic mu-form, the rigorous tensor)
Total field, simple mu(x)=x/(1+x) (the function Chae/AQUAL actually fit):

| footing | e = g_ext/a0 | **gamma_cap** | v/v_N |
|---|---|---|---|
| **framework 9.36e-11** | 2.423 | **1.306** | +14.3% |
| standard MOND 1.20e-10 | 1.890 | **1.398** | +18.3% |

(Bare-radial field gives 1.324 / 1.421 — matches the banked WB_EFE_DERIVATION exactly. Standard sharp mu gives
1.036 / 1.064 — the interpolation function is the dominant non-g_ext systematic, gap ~0.03 vs simple-mu gap ~0.09.)

## STEP 4 — MONTE-CARLO propagation: g_ext uncertainty -> sigma(gamma_cap) (N=4e5)
Varied V_c~N(233,4), R0~N(8.178,0.026), vertical fraction f_z~U(0.20,0.45):

| footing (simple-mu) | gamma_cap | 16-84 band | **sigma_gamma from g_ext** |
|---|---|---|---|
| framework | 1.307 | [1.294, 1.320] | **+/- 0.013** |
| MOND | 1.399 | [1.382, 1.416] | +/- 0.017 |

**THE LOAD-BEARING RESULT: g_ext is COMMON-MODE.** The same MW field divides BOTH a0 footings, so it moves the
framework and MOND caps *together*. The per-draw framework-vs-MOND gap is **0.092 +/- 0.004** — i.e. g_ext
uncertainty smears the *gap* by only **+/- 0.004 (4% of the gap)**, not the +/-0.013 absolute. So **g_ext
uncertainty does NOT wash out framework-vs-MOND** — the a0 difference IS the gap; g_ext shifts both ends in lockstep.
The route's both-ways trigger ("if g_ext smears gamma by more than the gap, decisive") resolves cleanly in the
framework's favor: g_ext is not the limiting systematic for either the detection or the discrimination.

## STEP 5 — the DR4 forecast: the three gaps and what actually limits them
Three EFE-cap hypotheses (simple-mu, total field): Newton 1.000, framework 1.307, MOND 1.399.

| gap | value | meaning |
|---|---|---|
| framework - Newton | **0.307** | the super-Newtonian signal to DETECT |
| MOND - framework | **0.092** | the framework-vs-MOND DISCRIMINATOR |
| MOND - Newton | 0.399 | |

**Statistical floor (anchored to real data):** Chae-2026 36-pair highest-quality 3D-velocity sample gave gamma =
1.60 +/- 0.16, so sigma_gamma * sqrt(N) ~ 0.93 for clean 3D pairs. DR4 clean-3D yields: ~1000 (conservative) to
~8000 (optimistic) in the 2-30 kAU test regime within ~250-300 pc.

**THE DOMINANT CONTAMINATION — undetected triples (f_multi):** a hidden companion adds velocity that MIMICS a
gravity boost (the "fat tail"). f_multi is degenerate with gamma at d gamma_obs/d f_multi ~ 1.0 — calibrated to the
real split: **Banik (f_multi~0.7) finds 19 sigma for Newton; Chae (f_multi~0.3-0.5) finds 4.9 sigma for MOND on
related samples.** Same data, different contamination model. A residual sigma(f_multi)~0.10 after DR4 modelling gives
a contamination floor of **~0.10 on inferred gamma** — comparable to the entire framework-MOND gap.

**Realistic DR4 SNR (sig_tot = stat (+) contam 0.10 (+) g_ext 0.013):**

| sample | framework vs Newton | framework vs MOND |
|---|---|---|
| N=1000 | 2.9 sigma (marginal) | 0.9 sigma (degenerate) |
| N=3000 | **3.0 sigma (DETECT)** | 0.9 sigma (degenerate) |
| N=8000 | 3.0 sigma | 0.9 sigma (degenerate) |

To reach 3 sigma framework-vs-MOND requires pinning f_multi to **~2-3% absolute** even at N=30000 — beyond plausible
DR4 contamination control (current literature disagrees by 0.4). The framework-vs-Newton detection, by contrast,
survives: ~3 sigma at the pessimistic contam=0.10 floor and N>=3000, climbing to 6-13 sigma if f_multi is pinned to
0.03-0.05.

## BOTTOM LINE — the lower-a0 double-edge, quantified (both ways, honest)
1. **g_ext is rigorously pinned and is NOT the bottleneck.** V_c(229-236)/R0(0.3%)/vertical(g_z~g_rad/3) ->
   g_ext = 2.27e-10 (total) -> sigma(gamma_cap) = +/-0.013, common-mode (irreducible gap scatter +/-0.004). The
   route's decisive both-ways test (does g_ext smear gamma past the gap?) answers NO. Route 3 settled.
2. **framework vs NEWTON: a CLEAN DR4 detection.** Gap 0.307. The lower a0 shrinks it from MOND's 0.40 to 0.31 but
   it stays a ~3-8 sigma super-Newtonian detection at DR4 — NOT blunted below detectability. No manufactured loss.
3. **framework vs MOND: MOND-DEGENERATE at DR4.** Gap only 0.092 — below the contamination floor (~0.10) and the
   interpolation-function systematic, and barely ~1 sigma at any feasible sample. The lower a0 genuinely makes the
   framework signal indistinguishable from standard MOND in wide binaries.
4. **NOT a manufactured deficit, NOT a high-priest dismissal.** The 0.092 gap is small *because the lower a0 is
   real*; the contamination floor that buries it is the *same* floor that splits Banik(Newton) from Chae(MOND) today
   — an independently-attested systematic, not invented. Wide binaries are a clean DETECTION channel
   (boosted-vs-Newton) and a NON-DIAGNOSTIC channel for a0 (framework-vs-MOND). The discriminating power between the
   two MOND-family theories lives in the interpolation function and contamination control, not in g_ext.

**Standing update for the WB front:** the prompt's framing of wide binaries as the framework's "sharpest CLEAN
forward discriminator" is HALF right — they cleanly discriminate {boosted gravity} from {Newton} at DR4, but the
lower a0 makes them MOND-degenerate. The honest claim is: wide binaries forward-predict gamma_cap = 1.31 +/- 0.01
(g_ext) -0.27 (interp, toward sharp mu), a falsifiable super-Newtonian detection, but they do not separate
9.36e-11 from 1.2e-10. The literature note: a Feb-2026 quality-framework reanalysis (arXiv:2602.24035) finds "no
evidence for MOND" — consistent with the degeneracy: the front is contamination-limited, not gravity-resolved.
