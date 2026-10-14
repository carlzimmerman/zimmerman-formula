# C. The early-type excess: what can carry it (theory push, 2026-10-14)

Status: hand algebra only. No script was run (a 1024³ job is live). Every number is quoted from a committed lane or is
one-line arithmetic shown here. This proposes; it does not test. κ = ½ is FITTED; the cold energy's mass is required; not
theory closed. Units: G = a₀ = M_b = 1, r_M = √(G M_b/a₀), x = r/r_M. At log M_b = 11, r_M = 12.2 / 11.1 kpc and
V_f = 188 / 197 km/s (canonical / alt). So KiDS 50–100 kpc is x ≈ 4–8, and SLACS θ_E ≈ 4–5 kpc is x_E ≈ 0.2–0.3 (log M* ≈ 11.3–11.5).

## 0. Sizing the target first (this corrects the brief)

Law, ν_s, condensed point source: total M_tot(x) = (1 + D)/2 and tethered M_t(x) = (D − 1)/2, with D = √(1 + 4x²).
At x = 8, M_tot = 8.52 and M_t = 7.52 M_b.

+0.280 dex in ESD is a factor ×1.9. The answer depends on how the extra mass is booked:
- **(b) Additive** (the extra does not source a tether response; this is CFG714's construction and CFG781's model).
  - The required extra is ≈ 0.81 × M_t: V_x ≈ 0.9 V_f, the same figure as CFG714.
  - That is **≈ 6 M_b inside 100 kpc** at log M_b 11, not ~1 M_b.
- **(a) Free mass sources the tether** (the at-rest static minimum of the action: M_eq uses Q = baryons + free mass, as in
  ONE_SWING_ANSWER).
  - Solve (Q + √(Q² + 4x²Q))/2 = 1.81 × M_tot. This gives Q = 2.99 at x = 8 and 2.75 at x = 4.
  - So the free mass needed is **≈ 1.8–2.0 M_b**, almost flat from 50 to 100 kpc, so it is compact.
- The brief's "~1 M_b" matches neither booking. It matches CFG580's 0.55–0.8 M*, which came from the older ε estimator
  (baryons sourcing the law).

Booking (a) is **excluded by the record's own inner–outer consistency** (CFG713/714):
- At SLACS radii the free mass's own phantom is negligible (x_E < 1), so f_x/f_law needs the free mass ≈ 3 × M_t(x_E).
- At x = 8 booking (a) needs only ≈ 0.25 of an isothermal copy of the halo.
- Fitting both radii with one isothermal component, (a) is off by a factor ~3, while (b) fits both with V_x ≈ 0.9 V_f (CFG714 z 0.58 / 0.25).
- **So whatever carries the excess must NOT source the tether's response.** That means the tethered population is warm, not
  the at-rest static minimum. The 10-14 warm-tether witness proves this branch exists: the tether plus velocity stress
  supports the condensed-source template with any extra gravitating source h. For an isothermal h = V_x²/r it needs σ_t² = V_x²/2.

## 1. Merger-driven violent relaxation: tethered → free (route 1)

**1a. Surplus-only version: dead, already on record.**
- Sub-additivity gives the merger remnant a surplus of (Σ√f_i − 1)·T, which is 0.41 T for N = 2 (CFG726).
- Kept tethered, CFG776 expels it within 50–100 t₀ and it overshoots into a deficit.
- Made free and placed by energy (CFG726 P2): +0.031 (N = 2) and +0.075 (N = 3), against the needed ≥ +0.114 (2σ line).
- Even full memory (H-MM) overshoots eRASS1/ACCEPT OUTER (×1.75–2.2). The surplus is too small and sits too far out.

**1b. Action version: dead.**
- In the action the tether force a_T = W′(u)P̂ is a field. Every element of the medium at a point feels it, whether or not it
  is phase-mixed. CFG723's identity ∇·P = ρ − ρ̄ holds for any multi-stream flow.
- Phase mixing is also how the law is BUILT: CFG747/748's radial shells cross and land on the law while staying tethered. So
  "phase-mixed ⇒ untethered" (the Argon kernel) contradicts the record's own relaxation channel. It cannot be the trigger.
- What a merger actually does to tethered cold energy, per CFG749, is to give it v ≳ 0.3 V_f. With self-gravity cancelled it
  is then **unbound and leaves**. In the action alone, mergers make a deficit, not an excess.

**1c. The surviving postulate, H-VR (violent-relaxation untethering).**

> The tether holds only what it can bind. An element whose tether-frame energy turns positive,
> E_t = v²/2 + Φ_b + Φ_push > 0 (CFG749's unbinding), detaches into a free collisionless population. That population feels
> full gravity, its own included, and no cubic push.

Comments:
- There is no new constant. The threshold is CFG749's own: v_esc,t² ≲ 2V_f²/x (baryons only, push makes it weaker), so ≈ 0.7 V_f at x = 4 and ≈ 0.3 V_f at x = 20.
- In the full potential the detached element IS bound: its depth is ~V_f² ln(r_edge/r), with v ~ V_f. So it stays.
- It is a two-population postulate, the same class CFG781's review accepted, and it is NOT derived from the action.

**Kick estimate.**
- In a merger of baryonic mass ratio μ, violent relaxation gives δv² ~ μ V_f² inside the region where the potential fluctuates.
- Conversion needs μ ≳ 2/x locally. A major merger (μ ≈ 1) converts the tethered halo beyond ~2 r_M. Inner shells convert
  later as the free tracer phase-mixes.
- A μ ≲ 0.1 accretion converts only beyond ~20 r_M (≳ 250 kpc), which is irrelevant inside 100 kpc. **This is why discs
  are spared.** The disc-survival criterion (no μ ≳ 0.1–0.2 merger since the disc formed) and the conversion threshold are the
  same inequality.

**Converted fraction.**
- Let η be the fraction of the tethered law mass inside the scrambled radius r_v that becomes free.
- One complete major merger gives η ≈ 1. Sequential conversions add, because the tethered law re-forms from the outer supply
  between them (CFG743: ≤ 1.4 Gyr in galaxies; CFG748: cold infall fills the law to 20 r_M).

**Where the free mass ends up.**
- Violent relaxation gives a tracer with σ ≈ V_c/√2 in a flat-V_c potential, so ρ_x ∝ r⁻² (isothermal) down to the centre,
  with M_x(<r) = η M_t(<r_v)·r/r_v.
- For r_v ≫ r_M this is V_x² ≈ η V_f² (to 1 − ½/x_v). **A complete conversion is a phase-mixed copy of the law's own halo,
  V_x ≈ V_f.** CFG714's V_x ≈ 0.9 V_f means η ≈ 0.81. This is the first time the record has a mechanism that gives an O(1)
  number near the measured one without tuning.

**Mass conservation (supply).**
- Supply S = 5.364 × M_b/0.10 = 53.6 M_b. The free copy inside 100 kpc is ≈ 0.81 × 7.5 ≈ 6 M_b.
- Re-forming the tethered law on top costs another 7.5 M_b out of S. The supply edge moves from x ≈ 53 to ≈ 47 (650 → 570 kpc).
- **Conservation allows +0.28 easily.** The constraint is the postulate, not the budget. (Within the remnant's own pool,
  without refill, you get only Σ√f_i − 1 = 0.41: the refill from the outer supply is load-bearing.)

**Inner (SLACS) vs outer (KiDS), route 3.**
- The free component is ρ ∝ r⁻² to the centre. The law's tethered part is sub-isothermal at x < 1 (M_t ≈ x²).
- So at 5 kpc the free/law ratio is ≈ η·x_E/M_t(x_E) ≈ η/x_E (3D) ≈ 3 for η = 0.81 and x_E = 0.25.
- CFG713 found f_x = 0.36/0.34, about 3× / 2.5× the law's own cold fraction. CFG714 already showed numerically that one
  isothermal component links 5 kpc to 100 kpc, and CFG715 that GCs at 10–50 kpc agree.
- H-VR supplies the reason the component is isothermal (a violently relaxed tracer) and why its amplitude is ≈ the law's
  (it is a converted copy).
- Caveat: my projected-mass bookkeeping at x_E is ±×2. CFG714's committed number is the one to quote.

**Predicted KiDS offset.**
- Δ = log₁₀[1 + η_e·M_t/M_tot] − log₁₀[1 + η_l·M_t/M_tot] − 0.027 (the law's own early − late, CFG658). M_t/M_tot = 0.88 at x = 8 and 0.78 at x = 4.

| η_early (η_late = 0) | Δ at 50 kpc | Δ at 100 kpc |
|---|---|---|
| 0.3 | +0.064 | +0.075 |
| 0.5 | +0.116 | +0.132 |
| 0.81 (CFG714's V_x) | +0.186 | +0.207 |
| 1.0 | +0.223 | +0.248 |

**Brutal point.** η is the POPULATION-AVERAGE converted fraction of KiDS f30 early types at log M* ≈ 10.8.
- Most early types at that mass are fast rotators (ATLAS3D-type statistics, from memory, PROVISIONAL). Many are not
  dry-major-merger remnants.
- If conversion needs a μ ≳ 0.3 merger and only ~30–50% had one, then η̄ ≈ 0.3–0.5 and Δ ≈ +0.07 to +0.13, which is a 2σ
  FAIL to marginal.
- H-VR reaches +0.28 only if almost every early type had a complete conversion (η̄ ≳ 0.8).
- The same tension appears in SLACS: from memory, most SLACS lenses with IFU kinematics are fast rotators, yet f_x shows no
  class trend (CFG713: "no trend with size or mass"; kinematic class not tested).
- **Hand estimate: Δ ≈ +0.19 (range +0.07 to +0.25)**, vs +0.280 ± 0.083.

**Late types / SPARC.**
- Discs have η ≈ 0 (no μ ≳ 0.1 merger since disc formation). μ < 0.1 accretion converts nothing inside ~250 kpc. SPARC is
  untouched.
- This is much safer than H-MM, where 3% accretion raised V by ×1.12 (CFG726 T-S2): here the threshold removes it.
- Danger: discs that rebuilt after a gas-rich major merger would carry η ≈ 1 and a lifted outer V (×√1.8 = 1.34 at x ≳ 4).
  The prediction is that such discs sit high on the RAR and on KiDS late-type lensing. CFG583/584 are underpowered for this
  and saw no trend.

**Clusters.**
- Clusters are merger-built, so η ≈ 1 inside the relaxed region. eRASS1 MID (0.5–1.2 Mpc) needs ×1.91 (CFG687), i.e.
  η ≈ 0.9–1. ACCEPT MID ×1.70 needs η ≈ 0.75. The η is the SAME as for early types, unlike every earlier route.
- OUTER (1.2–3 Mpc) matches the law, so r_v ≲ 1.2 Mpc in clusters while r_v ≳ 100 kpc in galaxies.
- **r_v is NOT derived.** As r_v = c·r_ta, galaxies (r_ta ≈ 1.6 Mpc for M_ta = 6.4e12) and clusters (r_ta ≈ 8 Mpc) need
  c ∈ [0.06, 0.15]. A shell-crossing derivation would have to land there. Until it does, c is a hidden constant and clusters
  cannot be scored honestly.
- eFEDS groups (law short by +0.43 dex, ×2.7): η = 1 gives at most ×1.9, PARTIAL.
- Bullet main core (needs ×3 over the law's 0.32): η ≈ 2, i.e. two sequential conversions. The free part is collisionless,
  so it follows the galaxies (offset sign right).
- Cluster-mass slope s = 0.90 vs the law's 0.47: H-VR keeps the law's √M scaling at fixed η, so **it does not fix s**. The
  open problem stays open.

**Cosmic shear.**
- A free copy in early types and cluster cores adds small-scale power. T12 (Δχ² +2.03, post-preview) could turn.
- This must be a guard in any run.

## 2. Bigger catchments for early types (route 2): dead

- **Catchment is additive under merging.** Σ M_i/0.10 = M_b/0.10, so dry mergers bring exactly their share and S/M_b = 53.6
  is invariant.
- Supply sets only the edge, at x_e ≈ S/M_b ≈ 54 (≈ 650 kpc). Inside x ≤ 8 the tethered profile is the law whatever S is:
  changing S by ×2 moves the 50–100 kpc ESD by 0.
- Overflow needs S above the capacity ≈ M_b·x_ta ≈ 100–130 M_b (r_ta ≈ 1.2–1.6 Mpc), which takes a catchment ratio of
  ≳ 19–24 instead of 10. That means early types must have LOST ≳ half their peak baryons. That is CFG776's regime, and any
  overflow is placed at turnaround energy (CFG721 G9; CFG726 P2-like lifts ≲ +0.03 inside 100 kpc).
- Hot gas opens the supply only for M_h > 8 M_c (CFG727 addendum).
- **Route 2 cannot produce +0.28 at 50–100 kpc, at any catchment.**

## 4. Everything else

- **Uncounted baryons:** dead. Hot gas is CFG580/581, cool CGM CFG582 (short ×6.3), a bottom-heavy IMF CFG713 (wrong slope
  sign). A constant M/L_K may inflate the excess by 0.05–0.15 (CFG669), so the true target may be +0.13 to +0.23. That
  helps H-VR (η̄ ≈ 0.5–0.8 then suffices).
- **Law change by geometry (spheroid vs disc):** dead. At x ≥ 4 the monopole dominates (≤ 0.02 dex), and it is already in
  −0.027.
- **Kernel change:** dead. ν_s vs ν_mono differ by ≤ 0.01 everywhere (CFG721).
- **Basin/environment:** old and young early types have the same companion counts (CFG586). Isolation-selected KiDS lenses
  leave no basin lever; not a carrier.
- **Hot-gas selector (CFG745/781, M_free = 5.364 M_hot):**
  - Its amount is ~0.9–1.3 M_b at M_hot 0.17–0.25 M*. That is enough only under booking (a), which §0 excludes, or if
    concentrated.
  - Its frozen placement is at TURNAROUND energy (Method B), so the mass mostly sits at ~r_ta. My estimate is that it lifts
    50–100 kpc by ≲ +0.05 (like CFG726 P2). It will likely FAIL T-K; CFG781 decides.
  - It predicts an offset that rises with M_hot/M_b. H-VR predicts a flat one.
- **Late-type deficit instead of early excess:** inner halos fill (CFG748, x ≤ 20 at ≥ 0.985 even mass-starved), so there is
  no deficit at x ≤ 8. Dead.

## 5. Verdict

| route | status | why |
|---|---|---|
| merger surplus (H-MM, free or tethered) | DEAD | CFG726/776: too small when free, expelled when tethered |
| merger untethering inside the action | DEAD | tether is a field force; phase mixing builds the law (CFG747); kicked tethered energy escapes (CFG749) |
| **H-VR: untether-on-unbinding postulate + refill** | **ALIVE, conditional** | O(1) η ≈ 0.8 needed, ≈ 1 natural; isothermal; links SLACS → KiDS → cluster MID with one η; spares discs by the same inequality that spares discs from destruction |
| bigger catchments / dry-merger supply | DEAD | additivity; supply sets only the edge |
| uncounted baryons, geometry, kernel, environment, late deficit | DEAD | §4 |
| hot-gas selector (CFG781) | pending; my estimate is FAIL on T-K | placement at turnaround |

What H-VR still lacks:
- (i) a derivation of detachment from an action. It is a postulate, the same status as the Argon kernel.
- (ii) r_v, which is undetermined (c ∈ [0.06, 0.15] if ∝ r_ta).
- (iii) the population η̄. Merger statistics without ΛCDM simulations are thin, and the fast-rotator majority is a real threat.
- (iv) booking (b) requires the tethered population to be warm (σ_t ≈ V_x/√2). This is natural after a merger but not derived.
- If (i)–(ii) are ever derived it is a mechanism. Today it is a mechanism-shaped rule with one undetermined scale.

## 6. Decisive tests

1. **Merger-indicator split at fixed Ks M_b and colour (KiDS).**
   - Round (b/a ≥ 0.8, slow-rotator proxy) minus flattened (b/a ≤ 0.6) early types: H-VR predicts Δ ≥ +0.10. The hot-gas
     selector predicts ~0. This must be power-checked first: the half-sample error ≈ 0.12 may be too large, and the B21
     released stacks have no shape split (CFG721).
   - Better still, with a tidal-feature/shell flag where one exists.
2. **Mass-flatness.** H-VR's ratio is independent of M_b at fixed η (excess ∝ the law's own √M_b r). The hot-gas selector
   rises with M_hot/M_b. KiDS in 3 Ks-M_b bins: slope dΔ/dlogM_b. CFG713 already saw no mass trend in SLACS f_x (consistent).
3. **SLACS f_x vs kinematic class** (fast vs slow rotators, published IFU subsample): H-VR predicts f_x(slow) > f_x(fast).
   If the fast rotators carry f_x ≈ 0.36 as well, H-VR's merger link is dead.
4. **Discs with a major-merger history** (counter-rotating, post-merger gas-rich remnants) should sit ≈ +0.25 dex high in
   outer V² and lensing.

## Proposed frozen criteria (single best candidate: H-VR)

```
CFG7xx  H-VR: violent-relaxation untethering (ask for an ID; grep LEDGER first)
Model (no new constant; rule declared, not derived):
  tethered  = law of condensed baryons (nu_s primary, nu_mono bracket; both footings, never pooled), warm (booking b),
              cut at supply 5.364*M_cond/0.10;
  free      = eta * M_t,law(<r_v) placed as isothermal tracer: M_x(<r) = eta*M_t(<r_v)*min(r/r_v,1);
              eta from DATA ONLY: eta_slacs = (V_x/V_f)^2 from CFG714 (0.81 can / its alt value), applied unchanged to KiDS;
  r_v       = bracket {150, 300, 600 kpc} for galaxies (reported); clusters NOT scored (r_v underived), reported at
              r_v in {0.6, 1.2} Mpc.
Targets / rules:
  T1 KiDS early-late at matched Ks M_b (CFG669 T2 harness): pred = log(1+eta*M_t/M_tot)-0.027 within 2 sigma of
     +0.280+-0.083 at every r_v bracket.  Hand estimate +0.19..+0.21 -> PASS expected (Z~1); NOT independent of CFG714.
  T2 (decisive, new) KiDS Ks-M_b 3-bin slope of the early-late offset: H-VR |slope| < 2 sigma of 0; report the
     hot-gas selector's predicted slope alongside. Fail = slope > 0 at Z>=2 in the hot-gas direction.
  T3 (decisive, new) shape split round (b/a>=0.8) minus flat (b/a<=0.6) early types, matched Ks M_b and colour:
     H-VR predicts >= +0.10; FAIL if <= 0 with sigma <= 0.06. If sigma > 0.06: UNDERPOWERED, no verdict (declared now).
  T4 SPARC guard: discs eta = 0 -> RAR rms unchanged (identity); report the gas-rich-major-merger subsample if flagged.
  T5 guard: cosmic-shear T12 rerun with free copies in early types (eta_slacs) - report delta chi^2; no verdict weight.
Controls: K1 eta=0 reproduces the law to 1e-12; K2 isothermal tracer mass = eta*M_t(<r_v) to 1e-9.
MUTATE: M1 eta := 0 for round, eta_slacs for flat (sign flip) -> T3 must flip sign; M2 free placed at r_ta energy
  (Method B) -> T1 must drop below +0.10 (shows placement is load-bearing).
Verdict: SUPPORTED iff T1 and (T2 or T3 decisive pass); CONDITIONAL if T1 only; FAIL if T2 or T3 fails as frozen.
Disclosures: detachment is a postulate; r_v underived; eta population value borrowed from SLACS; fast-rotator majority
  (memory, provisional) is the main threat; kappa fitted; cold energy mass required; not theory closed.
```
