# POWER LANE — can the STAR-ORBIT-within-one-system σ-spread be detected? (2026-07-17)

**Script:** `power.py` (+ `power.out`, exit 0, numpy, both footings). **Companions:** `mi_spread.py`
/ `MI_SPREAD.md` (the honest re-derived magnitude), `mg_zero.py` / `MG_ZERO.md` (the MG=0 theorem).

> **Scope note — two DIFFERENT observables, do not conflate.** This lane is the *star-orbit-within-ONE-
> pressure-supported-system* spread (individual stars on different-eccentricity orbits inside one dSph),
> honest magnitude **0.2–1% in σ** (`mi_spread.py`, 2026-07-17). The earlier `power_analysis.py` /
> `POWER_cluster_efe_channel.md` (2026-07-16) powers the **distinct** cluster-member **EFE subsystem-
> boost** (a whole member galaxy's internal dispersion vs its infall phase, banked **6–13%**). Both are
> MG-impossible; they are ~30× apart in amplitude and are measured differently. The cluster-EFE doc is
> **preserved unchanged**; it is the powerable-nearer cluster route. THIS file is the star-orbit lane.

de Sitter–Unruh **MODIFIED INERTIA** (Zimmerman). ν(y)=√(1+1/y), y=g_bar/a₀, a₀=cH_Λ/Z=9.36e-11;
inertia = time-nonlocal functional of the body's own worldline through K(□_u/a₀²), τ_mem=2c/a₀=2Z/H_Λ
(E10, exact). Milgrom 1983/1999 wellhead credit for the ν-kernel; distinctive content = the cH_Λ/Z
coefficient + the MI completion. **a₀'s value and s=−1 remain postulates.**

---

## The observable and the magnitude it must clear (re-derived, not assumed)

At radius r every star feels the **same** g_bar(r); a local μ(|a|) gives all the same |a| → no spread.
MI's non-adiabatic Jensen gap makes an eccentric orbit's memory-averaged effective inertia differ from a
circular one at the same energy → an intrinsic **LOS-dispersion spread across eccentricity families**,
beyond anisotropy/projection/measurement. Sign **negative** (eccentric orbits run cooler). Because
τ_mem = 203/168 Gyr ≫ every real T_orb (deep adiabatic, no resonance), the honest amplitude is:

| regime | RMS fractional σ-spread f | where |
|---|---|---|
| **fiducial** (cored / real-kernel-matched) | **0.20–0.35%** | classical dSph |
| point-mass **ceiling** (sharpest cusp, hard bound) | 0.70–1.00% | idealized, not real cored dSph |
| ellipticals/dE (y≫1, near-Newtonian internal) | ~0.08% | essentially dead |

Both footings shift f **<20%** (a₀ cancels at fixed depth y) → all N-to-3σ shift **<44%** (N∝1/f²).
**MG = exactly 0** (airtight theorem, `MG_ZERO.md`) — a clean detection *would* be MG-impossible, *if* detectable.

## The estimator and its Fisher floor (the wall no estimator beats)

Per star: v_i ~ N(0, σ_i²+e_i²), ln σ_i = ln σ̄ + f·x_i, x = standardized per-star **orbit tag**
(eccentricity). The efficient (score/MLE) test has Fisher info I_ff = 2Nw² with **w = σ²/(σ²+e²)**
(measurement error down-weights the *variance*-information **quadratically**), attenuated by
**D = corr(measured proxy, true eccentricity)**:

> **z = f · w · D · √(2N)**  →  **N₃σ = (3 / (f·w·D))² / 2**

`power.py` validates this analytic floor against an efficient-score Monte-Carlo (analytic vs MC medians
agree to ≤2%: 2.208/2.203, 1.104/1.080, 1.682/1.683), confirms √N scaling (1.99), and calibrates the
null (f=0 → z mean +0.000, sd 1.006 over 20k trials).

## What the real systems give (per-star LOS velocities, cited specs)

| system | N (public) | σ [km/s] | e_v [km/s] | w | y | perfect-tag z (fid 0.28% \| ceil 0.85%) |
|---|---|---|---|---|---|---|
| Fornax | 2600 | 11.7 | 2.0 | 0.97 | 0.60 | 0.20 \| 0.60 |
| Sculptor | 1500 | 9.2 | 2.0 | 0.95 | 0.30 | 0.15 \| 0.44 |
| Draco | 700 | 9.1 | 2.0 | 0.95 | 0.25 | 0.10 \| 0.30 |
| Crater II (diffuse, **deepest** y) | 150 | 2.7 | 2.0 | 0.65 | 0.08 | 0.03 \| 0.10 |
| Antlia II (diffuse, deep y) | 200 | 5.7 | 2.0 | 0.89 | 0.10 | 0.05 \| 0.15 |
| **stacked classical+diffuse** | **~7,130** | — | — | 0.93 | — | **0.22–0.39 \| 0.78–1.11** |

Per-star velocity error (~2 km/s bright RGB, Walker+2009) is **not** the wall (w=0.65–0.97). The
**amplitude and the count pull opposite**: the deepest-MOND systems (Crater II/Antlia II) that maximize f
have the **fewest** stars. **Even a PERFECT orbit tag gives z<0.5 in every single system**, and the
perfect-tag stack of the *entire* ~7k-star dSph reservoir reaches only z≈0.8–1.1 at the point-mass
ceiling, z<0.4 at the fiducial magnitude.

## The binding wall: there is no per-star orbit tag (D)

The estimator needs a per-star eccentricity tag. Every source fails where the counts live:

- **(a) Gaia per-star internal PM** — the internal-velocity PM signal is ~17–25 **µas/yr** at dSph
  distances vs a DR3 per-star error ~500 µas/yr → **S/N ≈ 0.03–0.05**. Gaia delivers the N-averaged
  **bulk systemic** PM only, **not** a per-star tag. **D_Gaia ≈ 0.**
- **(b) LOS-only DF inference** — a single LOS velocity + position does not fix an orbit's eccentricity
  (E,L-degenerate); statistical deprojection reaches **D ≲ 0.1–0.2** and *is* the β-anisotropy channel
  that MG reproduces (`MG_ZERO.md` Jeans) → confound-limited, not clean.
- **(c) HST/JWST multi-epoch internal PM** (Sculptor Massari+2018; Draco) — the **only** genuine per-star
  3D route: ~few-km/s per-star tangential velocities for a **few hundred** bright stars in **2–3** systems,
  **D≈0.3–0.4**, and only where the effect is *not* deepest. Best real single-system z ≈ **0.05**.
- **(d) tag-free (excess LOSVD kurtosis)** — the orbit-family variance enters the 4th moment as ~f² ≈
  8e-6, unmeasurable, and degenerate with β/triaxiality/binaries. **Hopeless.**

## N-to-3σ grid (both footings folded into the f-band; w=0.95)

| tag quality D | f=0.20% | f=0.35% | f=0.70% | f=1.00% |
|---|---|---|---|---|
| **1.0** perfect (Fisher ceiling) | 1.25e6 | 4.1e5 | 1.0e5 | 5.0e4 |
| **0.35** HST/JWST 3D (best real) | 1.0e7 | 3.3e6 | 8.3e5 | 4.1e5 |
| **0.15** LOS-DF (confound-limited) | 5.5e7 | 1.8e7 | 4.5e6 | 2.2e6 |

## Other venues — both weak for THIS observable

- **Ellipticals** (MaNGA ~10⁴, ATLAS3D 260): internally y≫1 → f~0.08%, and IFU gives **binned** σ+h4,
  **no per-star tag**. N₃σ ~8e6 tracers. **Dead.**
- **Clusters** (Coma ~1000 caustic members, e_cz~39 km/s, σ_cl~1042): τ_mem/T_orb~22 (least adiabatic)
  but still deep-adiabatic → same f-band; perfect-tag z@0.35% ≈ 0.16, and the "orbit tag" for a member
  galaxy (its 3D cluster orbit) is unavailable (D~0.1–0.2). The **powerable** cluster observable is the
  *distinct* member-galaxy EFE channel (`POWER_cluster_efe_channel.md`), **not** this star-orbit one.

---

## VERDICT — **UNDERPOWERED, NEEDS: ~10⁴·⁵–10⁵·⁵ clean per-star velocities in one deep-MOND dSph + a per-star 3D orbit tag Gaia cannot provide**

- **POWERED NOW? NO** — two independent walls, either alone fatal:
  - **W1 (count):** the Fisher floor needs **N ~ 7e4 (ceiling 1%) to ~6e5 (fiducial 0.2%)** clean per-star
    velocities in a *single* deep-MOND system even with a perfect tag; the biggest dSph has 2,600 and the
    whole stacked reservoir ~7,130 (perfect-tag z<1.1 at ceiling, <0.4 fiducial). **Gap ×10–90.**
  - **W2 (tag):** per-star eccentricity is unmeasurable where the counts are (Gaia per-star PM S/N~0.05;
    LOS-DF D≲0.2 and MG-degenerate; only HST/JWST 3D reaches D~0.35 for ~300–500 stars in 2–3 systems →
    best real single-system z~0.05). Realistic-D N₃σ: **5.6e5 (ceiling) to 5.2e6 (fiducial).**
- **EXISTING DATA THAT BITES? NONE.** Walker+2009 / Gaia DR3 / MaNGA / ATLAS3D / Coma all fall ×10²–10⁶
  short. Ellipticals dead (y≫1, no per-star tag); clusters give only the distinct EFE channel.
- **WHAT POWERS IT (both required, neither exists today):** (i) **~10⁴·⁵–10⁵·⁵ clean per-star LOS
  velocities** in a single diffuse deep-MOND dSph/UDG — only the **point-mass-ceiling ~1% corner** is
  within ~1–2 orders of a plausible 30m-class (ELT/MSE/DESI-successor) campaign; the realistic fiducial
  0.2–0.35% needs ~10⁵·⁵–10⁶ and is out of reach — **plus** (ii) a **per-star 3D orbit/eccentricity tag**
  at dSph distances (multi-epoch space astrometry well beyond Gaia's per-star precision).
- **Both footings:** f shifts <20% → all N shift <44%. The discriminator is **not footing-hostage**; it is
  **magnitude- and tag-hostage**. This is a *clean* MG-impossible discriminator that is **structurally
  underpowered at its honest magnitude** — short not merely of data but of a per-star orbit tag.

No "proves" language for the framework value/sign; **MG=0 is the only theorem-grade claim** and is
labelled as such. Both footings shown throughout (`power.py`, exit 0).
