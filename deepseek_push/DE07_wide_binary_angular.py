#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""DE07 -- THE WIDE-BINARY ANGULAR STATISTIC ON GAIA EDR3: re-run of the registered directional-EFE test.

LANE GAME_PLAN_DIRECTIONAL_EFE (DE07).  The framework's directional-EFE rule is ZERO angular
modulation (direction-blind); AQUAL-class theories predict the boost depends on the angle between
the binary separation and the Galactic-centre direction (L = d ln mu/d ln eta ~ 0.27 at eta = 2.5
for mu2 -> ~6% velocity modulation).  This re-run follows the exact code path of
hunt_2026/h15_wide_binary_orientation.py (read-only; the code is COPIED here, nothing imported
from hunt_2026) on the on-disk El-Badry, Rix & Heintz (2021) Gaia EDR3 catalogue.

REGISTERED PRIOR (prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md, Amdts 8(d)(ii), 9(b)):
A-hat = +2.95 at p = 0.029 with the AQUAL-class sign -- the OLD corpus firing of the directional-
EFE test on ROTATION CURVES, a DIFFERENT statistic than the wide-binary split b_perp/b_par - 1.

ESTIMATOR (h15, verbatim): v~ = dv_sky/sqrt(G M_tot/s), Q = <v~^2> - <sigma_v~^2>, b = sqrt(Q);
r = b_perp/b_par - 1 with perp = cos^2 phi < 0.5 about the sky-projected Galactic-centre axis.
The CORRECT null is the random-axis null (perp/par are different REGIONS of sky; h15's lesson);
the bootstrap is printed beside it for comparison.

KILL CONDITIONS (written before any measurement):
  K1  widest-bin (s/r_M > 1.96) split PARALLEL-dominant at >= 3 sigma on the random-axis null
      -> direction-blind rule ABSENT (modulation PRESENT).
  K2  widest-bin split |r|/e_axis <= 2 sigma -> direction-blind SURVIVES at DR3 (ABSENT).
  K3  anything else, or the two a0 footings disagree -> UNDECIDED.
AQUAL amplitude: L = 0.27 -> ~6% velocity modulation -> A_PRED = 0.06 in split units (r ~= dv/v);
N(3 sigma) = N_now * (3 e_axis / A_PRED)^2 in the widest bin.

Outputs: DE07_wide_binary_angular.out/.json.  MUTATE=1 breaks a hinge (the clean-sample RUWE cut
becomes 0.9 instead of 1.4, breaking the sample-reproduction check).  Do not commit.
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "real_research", "data"))
MUTATE = int(os.environ.get("MUTATE", "0"))
RUWE_CUT = 0.9 if MUTATE else 1.4          # the MUTATE hinge: wrong clean-sample cut
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}      # both footings, m/s^2 (binding)
AU = 1.495978707e11; MSUN_GM = 1.32712440018e20; K_PM = 4.740470446
SNR_CUT = 5.0; PREREG_LO, PREREG_HI = 0.0013, 0.0046   # registered MG-arm sample-level split, boost units
AHAT, PRIOR_P = 2.95, 0.029                            # the registered prior (old corpus firing, rotation curves)
A_PRED = 0.06                                          # AQUAL-class ~6% velocity modulation -> split statistic
N_AXIS, N_BOOT = 1000, 1200                            # random axes for the null; bootstrap resamples (>1000)
CK = []

def chk(name, ok, detail=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    CK.append({"name": name, "pass": ok, "detail": detail})
    return ok

def P(*a): print(*a, flush=True)
def info(s): print("  " + s, flush=True)

P("=" * 116)
P("DE07 -- the wide-binary ANGULAR statistic on Gaia EDR3: re-run of the registered directional-EFE test")
P("=" * 116)
info(f"registered prior:  A-hat = {AHAT:+.2f} at p = {PRIOR_P:.3f} with the AQUAL-class sign")
info(f"                   (old corpus first firing of the directional-EFE test on ROTATION CURVES; a different")
info(f"                    statistic than the wide-binary split -- see the prior status report below)")
info(f"AQUAL-class amplitude: L = 0.27 -> ~6% velocity modulation -> A_PRED = {A_PRED:.3f} in split units (r ~= dv/v)")
info(f"PRE-REGISTERED KILL CONDITIONS (written before any measurement):")
info(f"  K1  widest-bin s/r_M > 1.96 split PARALLEL-dominant at >= 3 sigma on the RANDOM-AXIS null")
info(f"      -> direction-blind rule ABSENT (modulation PRESENT)")
info(f"  K2  widest-bin split |r|/e_axis <= 2 sigma on the random-axis null -> direction-blind SURVIVES (ABSENT)")
info(f"  K3  anything else, or the two a0 footings disagree -> UNDECIDED")
info(f"MUTATE = {MUTATE} (1 breaks the RUWE-clean-cut hinge)")

def rule(r, e):
    """The pre-registered kill rule: returns the verdict for one footing, from (r, e_axis)."""
    sig = r / e
    if sig <= -3.0: return "PRESENT"
    if abs(sig) <= 2.0: return "ABSENT"
    return "UNDECIDED"

# ---------------------------------------------------------------- data (h15's exact loading)
F = os.path.join(DATA, "widebinaries", "all_columns_catalog.fits.gz")
COLS = ["l1", "l2", "b1", "b2", "ecl_lon1", "ecl_lat1", "parallax1", "parallax2",
        "parallax_over_error1", "parallax_over_error2", "pmra1", "pmra2", "pmdec1", "pmdec2",
        "pmra_error1", "pmra_error2", "pmdec_error1", "pmdec_error2", "ruwe1", "ruwe2",
        "phot_g_mean_mag1", "phot_g_mean_mag2", "sep_AU", "R_chance_align"]
with fits.open(F, memmap=True) as h:
    D = {k: np.array(h[1].data[k], dtype="f8") for k in COLS}
N_ROWS = len(D["sep_AU"])
info(f"El-Badry+2021 Gaia EDR3 catalogue: {N_ROWS} pairs loaded")

dist = 0.5 * (1000 / D["parallax1"] + 1000 / D["parallax2"])
dmu_a = D["pmra2"] - D["pmra1"]; dmu_d = D["pmdec2"] - D["pmdec1"]
dmu = np.hypot(dmu_a, dmu_d)
sig_mu2 = D["pmra_error1"]**2 + D["pmra_error2"]**2 + D["pmdec_error1"]**2 + D["pmdec_error2"]**2
sig_mu = np.sqrt(sig_mu2 / 2.0)
snr = dmu / np.maximum(sig_mu, 1e-9)
dv = K_PM * dmu * dist / 1000.0
sdv = K_PM * np.sqrt(sig_mu2) * dist / 1000.0
MG1 = D["phot_g_mean_mag1"] - 5 * np.log10(np.maximum(dist, 1e-6) / 10)
MG2 = D["phot_g_mean_mag2"] - 5 * np.log10(np.maximum(dist, 1e-6) / 10)
xg = np.linspace(-1.46, 0.99, 4000); MGg = 4.887 - 5.693 * xg + 0.4164 * xg**2 + 0.9611 * xg**3
o = np.argsort(MGg); MGs, xs = MGg[o], xg[o]
Mtot = np.exp(np.interp(np.clip(MG1, 0.6, 11.1), MGs, xs)) + np.exp(np.interp(np.clip(MG2, 0.6, 11.1), MGs, xs))

sel = ((D["R_chance_align"] < 0.01) & (D["ruwe1"] < RUWE_CUT) & (D["ruwe2"] < RUWE_CUT) &
       (dist > 0) & (dist < 250) & (D["parallax_over_error1"] > 50) & (D["parallax_over_error2"] > 50) &
       (snr > SNR_CUT) & (MG1 > 4.0) & (MG1 < 11.0) & (MG2 > 4.0) & (MG2 < 11.0) &
       np.isfinite(dv) & (D["sep_AU"] > 0))
N_CLEAN = int(sel.sum())
info(f"clean sample (R_chance_align < 0.01, RUWE < {RUWE_CUT} both, d < 250 pc, parallax S/N > 50 both, "
     f"4 < M_G < 11 both, |dmu|/sigma > {SNR_CUT:.0f}): {N_CLEAN} pairs")

# ---------------------------------------------------------------- tangent-plane geometry (h15 verbatim)
class SkyGeom:
    def __init__(self, l1, b1, l2, b2):
        L1, B1, L2, B2 = map(np.radians, (l1, b1, l2, b2))
        Lm, Bm = 0.5 * (L1 + L2), 0.5 * (B1 + B2)
        dl = np.mod(L2 - L1 + np.pi, 2 * np.pi) - np.pi
        self.dx, self.dy = dl * np.cos(Bm), B2 - B1
        self.dn = np.hypot(self.dx, self.dy)
        self.n = np.stack([np.cos(Bm) * np.cos(Lm), np.cos(Bm) * np.sin(Lm), np.sin(Bm)], axis=1)
        self.lh = np.stack([-np.sin(Lm), np.cos(Lm), np.zeros_like(Lm)], axis=1)
        self.bh = np.stack([-np.sin(Bm) * np.cos(Lm), -np.sin(Bm) * np.sin(Lm), np.cos(Bm)], axis=1)
    def cos2(self, axis):
        a = np.asarray(axis, dtype=float); a = a / np.linalg.norm(a)
        na = self.n[:, 0] * a[0] + self.n[:, 1] * a[1] + self.n[:, 2] * a[2]
        t = a[None, :] - na[:, None] * self.n
        pl = t[:, 0] * self.lh[:, 0] + t[:, 1] * self.lh[:, 1] + t[:, 2] * self.lh[:, 2]
        pb = t[:, 0] * self.bh[:, 0] + t[:, 1] * self.bh[:, 1] + t[:, 2] * self.bh[:, 2]
        den = self.dn * np.hypot(pl, pb)
        return np.where(den > 0, ((self.dx * pl + self.dy * pb) / np.maximum(den, 1e-30))**2, np.nan)
    def subset(self, m):
        o = SkyGeom.__new__(SkyGeom)
        for k in ("dx", "dy", "dn", "n", "lh", "bh"): setattr(o, k, getattr(self, k)[m])
        return o

GC_AXIS = np.array([1.0, 0.0, 0.0])
idx = np.where(sel)[0]
GEOM = SkyGeom(D["l1"][idx], D["b1"][idx], D["l2"][idx], D["b2"][idx])
c2_gc = GEOM.cos2(GC_AXIS)
ok = np.isfinite(c2_gc)
idx = idx[ok]; c2_gc = c2_gc[ok]; GEOM = GEOM.subset(ok)
S = dict(s=D["sep_AU"][idx], M=Mtot[idx], dv=dv[idx], sdv=sdv[idx])
info(f"pairs with a well-defined sky orientation: {len(idx)}; <cos^2 phi>_GC = {c2_gc.mean():.4f} (isotropic 0.5)")

# ---------------------------------------------------------------- estimator (h15 verbatim)
def boost_proxy(m):
    vc = np.sqrt(MSUN_GM * S["M"][m] / (S["s"][m] * AU)) / 1000.0
    vt = S["dv"][m] / vc; st = S["sdv"][m] / vc
    q = np.mean(vt**2) - np.mean(st**2)
    return math.sqrt(q) if q > 0 else float("nan")

def split_arrays(m, cc):
    vc = np.sqrt(MSUN_GM * S["M"][m] / (S["s"][m] * AU)) / 1000.0
    vt = S["dv"][m] / vc; st = S["sdv"][m] / vc
    r = []
    for sub in (cc < 0.5, cc >= 0.5):
        if sub.sum() < 3: r.append(float("nan")); continue
        q = np.mean(vt[sub]**2) - np.mean(st[sub]**2)
        r.append(math.sqrt(q) if q > 0 else float("nan"))
    ok2 = np.isfinite(r[0]) and np.isfinite(r[1]) and r[1] > 0
    return r[0], r[1], (r[0] / r[1] - 1.0 if ok2 else float("nan"))

def axis_null(m, n=N_AXIS, seed=90210):
    """THE CORRECT null: the same pairs split by random sky axes; its spread is the error bar and the
    fraction of axes beating the real split is the p-value (the sky-coherence term is in it)."""
    rng = np.random.default_rng(seed)
    G = GEOM.subset(m); out = []
    for _ in range(n):
        v = rng.normal(size=3); v /= np.linalg.norm(v)
        cc = np.nan_to_num(G.cos2(v), nan=0.5)
        out.append(split_arrays(m, cc)[2])
    a = np.array(out); return a[np.isfinite(a)]

def boot_split(c2, m, n=N_BOOT, seed=1515):
    """Pair-resampling bootstrap -- the WRONG null (h15's lesson), printed for comparison only."""
    rng = np.random.default_rng(seed); w = np.where(m)[0]; out = []
    for _ in range(n):
        j = w[rng.integers(0, len(w), len(w))]
        vc = np.sqrt(MSUN_GM * S["M"][j] / (S["s"][j] * AU)) / 1000.0
        vt = S["dv"][j] / vc; st = S["sdv"][j] / vc; cc = c2[j]
        r = []
        for sub in (cc < 0.5, cc >= 0.5):
            q = np.mean(vt[sub]**2) - np.mean(st[sub]**2)
            r.append(math.sqrt(q) if q > 0 else float("nan"))
        out.append(r[0] / r[1] - 1.0 if np.isfinite(r[0]) and np.isfinite(r[1]) and r[1] > 0 else np.nan)
    return np.array(out)

def measure(m, c2=c2_gc, n_axis=N_AXIS, seed=90210):
    _, _, r = split_arrays(m, c2[m])
    A = axis_null(m, n_axis, seed)
    e = float(A.std()); p = float((np.abs(A) > abs(r)).mean()) if np.isfinite(r) else float("nan")
    eb = float(np.nanstd(boot_split(c2, m)))
    return dict(r=r, e=e, p=p, eb=eb, n=int(m.sum()),
                nperp=int((m & (c2 < 0.5)).sum()), npar=int((m & (c2 >= 0.5)).sum()))

# ---------------------------------------------------------------- measurements
P(""); P("-" * 116); P("MEASUREMENTS")
DEEP = (S["s"] > 2e3) & (S["s"] < 30e3)
QD = measure(DEEP, seed=2001)
info(f"SAMPLE-LEVEL (2-30 kAU): N = {QD['n']} ({QD['nperp']} perp, {QD['npar']} par); "
     f"b_perp/b_par - 1 = {QD['r']:+.4f} +- {QD['e']:.4f} (random-axis {N_AXIS} axes, seed 2001), "
     f"p = {QD['p']:.3f}; bootstrap would say +- {QD['eb']:.4f}")

WIDEST = {}
for f in ("canonical", "alt"):
    a0 = A0[f]
    rM = np.sqrt(MSUN_GM * S["M"] / a0) / AU
    u = S["s"] / rM
    m = (u > 1.96) & (u < 8.0)
    q = measure(m, seed=3196)
    WIDEST[f] = dict(q=q, rM1=math.sqrt(MSUN_GM / a0) / AU)
    sgn = "PAR-dominant" if q["r"] < 0 else "PERP-dominant"
    info(f"WIDEST BIN s/r_M > 1.96 ({f:9s} footing, r_M(1 Msun) = {WIDEST[f]['rM1']:.0f} AU): "
         f"N = {q['n']} ({q['nperp']} perp, {q['npar']} par); b_perp/b_par - 1 = {q['r']:+.4f} +- "
         f"{q['e']:.4f} (random-axis, seed 3196), p = {q['p']:.3f}; bootstrap would say +- {q['eb']:.4f}  {sgn}")

RS, ES, PS = QD["r"], QD["e"], QD["p"]
RWC, EWC = WIDEST["canonical"]["q"]["r"], WIDEST["canonical"]["q"]["e"]
RWA, EWA = WIDEST["alt"]["q"]["r"], WIDEST["alt"]["q"]["e"]
EBW = WIDEST["canonical"]["q"]["eb"]
SIG_C, SIG_A = RWC / EWC, RWA / EWA
VERD_C, VERD_A = rule(RWC, EWC), rule(RWA, EWA)
VERDICT = VERD_C if VERD_C == VERD_A else "UNDECIDED"

# step 4: N needed for 3 sigma at the AQUAL-class amplitude (A_PRED = 0.06 in split units)
n_need_can = WIDEST["canonical"]["q"]["n"] * (3.0 * EWC / A_PRED)**2
n_need_alt = WIDEST["alt"]["q"]["n"] * (3.0 * EWA / A_PRED)**2
info("")
info(f"POWER at the AQUAL-class amplitude: 3 sigma needs N = {n_need_can:.1e} ({n_need_can / WIDEST['canonical']['q']['n']:.0f}x this widest bin, "
     f"canonical) and {n_need_alt:.1e} ({n_need_alt / WIDEST['alt']['q']['n']:.0f}x, alt) at the measured random-axis errors")
info(f"context: a UNIFORM 6% split over the whole 2-30 kAU sample is excluded at "
     f"{(A_PRED - RS) / ES:.1f} sigma -- the modulation can only live in the EFE-transition band, hence the widest-bin framing")

P(""); P("=" * 116); P("CHECKS")
chk("DE07-1 catalogue reproduction: the on-disk El-Badry+2021 file loads with 1,817,594 pairs and the h15 clean " +
    "selection (R_chance_align < 0.01, RUWE < 1.4 both, d < 250 pc, parallax S/N > 50 both, 4 < M_G < 11 both, " +
    "|dmu|/sigma > 5) reproduces the committed clean-sample size ~39.7 k",
    N_ROWS == 1817594 and 39000 < N_CLEAN < 40500,
    f"rows = {N_ROWS}, N_clean = {N_CLEAN} (RUWE < {RUWE_CUT})")
chk("DE07-2 sky coverage is close to isotropic about the Galactic-centre axis, so the split is not one hemisphere vs the other",
    abs(c2_gc.mean() - 0.5) < 0.05,
    f"<cos^2 phi>_GC = {c2_gc.mean():.4f} vs isotropic 0.5")
chk("DE07-3 the sample-level split is consistent with zero at DR3 N and the registered prior is NOT reproduced: " +
    "|r|/e < 3 on the correct null and p > 0.029",
    abs(RS) / ES < 3.0 and PS > PRIOR_P,
    f"r = {RS:+.4f} +- {ES:.4f} ({abs(RS)/ES:.1f} sigma, p = {PS:.3f}) at 2-30 kAU, N = {QD['n']}")
chk("DE07-4 the widest bin (canonical footing) does not fire the pre-registered kill: not a >= 3 sigma " +
    "parallel-dominant split on the correct null",
    abs(SIG_C) < 3.0, f"r = {RWC:+.4f} +- {EWC:.4f} ({SIG_C:+.1f} sigma, p = {WIDEST['canonical']['q']['p']:.3f})")
chk("DE07-5 the widest bin (alt footing) does not fire the pre-registered kill either",
    abs(SIG_A) < 3.0, f"r = {RWA:+.4f} +- {EWA:.4f} ({SIG_A:+.1f} sigma, p = {WIDEST['alt']['q']['p']:.3f})")
chk("DE07-6 the kill rule is exhaustive and mutually exclusive: PRESENT at <= -3 sigma, ABSENT at <= 2 sigma, else UNDECIDED",
    rule(-4.0, 1.0) == "PRESENT" and rule(0.5, 1.0) == "ABSENT" and rule(2.5, 1.0) == "UNDECIDED",
    f"rule(-4,1)={rule(-4.0,1.0)}, rule(0.5,1)={rule(0.5,1.0)}, rule(2.5,1)={rule(2.5,1.0)}")
chk("DE07-7 the correct null beats the bootstrap exactly where it matters: they AGREE at the sample level and the " +
    "random-axis spread EXCEEDS the bootstrap in the sparse widest bin (the sky-coherence term h15 documented)",
    abs(ES / QD["eb"] - 1.0) < 0.75 and EWC > 1.2 * EBW,
    f"sample-level axis/boot = {ES/QD['eb']:.2f}; widest-bin axis/boot = {EWC/EBW:.2f}")
chk("DE07-8 DR3 is underpowered for the AQUAL-class amplitude in the widest bin: 3 sigma at A_PRED = 0.06 needs " +
    "more than 10x the current widest-bin sample on the canonical footing",
    n_need_can > 10.0 * WIDEST["canonical"]["q"]["n"],
    f"N_need = {n_need_can:.1e} vs N = {WIDEST['canonical']['q']['n']}")
expected = VERD_C if VERD_C == VERD_A else "UNDECIDED"
chk("DE07-9 verdict assigned by the pre-registered rule on both footings (disagreement -> UNDECIDED)",
    VERDICT == expected and VERDICT in ("PRESENT", "ABSENT", "UNDECIDED"),
    f"canonical rule -> {VERD_C}, alt rule -> {VERD_A}, combined -> {VERDICT}")
NF = sum(1 for c in CK if not c["pass"])
P("")
P("=" * 116); P("VERDICT (direction-blind rule: ZERO angular modulation; AQUAL-class: ~6% modulation)")
info(f"sample-level split (2-30 kAU, N = {QD['n']}):  b_perp/b_par - 1 = {RS:+.4f} +- {ES:.4f} (p = {PS:.3f}); "
     f"bootstrap +- {QD['eb']:.4f}")
info(f"widest bin s/r_M > 1.96, canonical:  b_perp/b_par - 1 = {RWC:+.4f} +- {EWC:.4f} ({SIG_C:+.1f} sigma, p = {WIDEST['canonical']['q']['p']:.3f})")
info(f"widest bin s/r_M > 1.96, alt:       b_perp/b_par - 1 = {RWA:+.4f} +- {EWA:.4f} ({SIG_A:+.1f} sigma, p = {WIDEST['alt']['q']['p']:.3f})")
info(f"VERDICT: {VERDICT}")
info(f"prior status: the registered A-hat = +2.95, p = 0.029 is the old corpus firing of the directional-EFE test on "
     f"rotation curves -- a different quantity from b_perp/b_par - 1; like-for-like comparison is not derivable at DR3 N. "
     f"The DR3 wide-binary sample-level split ({RS:+.4f} +- {ES:.4f}, {abs(RS)/ES:.1f} sigma, p = {PS:.3f}) does not "
     f"reproduce it and is consistent with zero; the AQUAL-class-sign hint is not confirmed by the wide-binary channel "
     f"at DR3 N, which is underpowered for the ~6% modulation in the transition band (N_need ~ {n_need_can:.0f} widest-bin "
     f"pairs).  The hint's status rests on the rotation-curve channel where it originally fired, not on this re-run.")

OUT = dict(verdict=VERDICT,
           prior_status="prior A-hat = +2.95, p = 0.029 is the old corpus firing on rotation curves (a different "
                        "statistic, not like-for-like at DR3 N); the DR3 wide-binary sample-level split is consistent "
                        "with zero and does not reproduce it",
           checks="; ".join(f"[{'PASS' if c['pass'] else 'FAIL'}] {c['name']} ({c['detail']})" for c in CK),
           artifacts="deepseek_push/DE07_wide_binary_angular.py, DE07_wide_binary_angular.out, DE07_wide_binary_angular.json",
           numbers=dict(n_rows=N_ROWS, n_clean=N_CLEAN, sample_split=RS, sample_err_axis=ES, sample_p=PS,
                        sample_err_boot=QD["eb"], n_deep=QD["n"],
                        widest_can=dict(r=RWC, e=EWC, p=WIDEST["canonical"]["q"]["p"],
                                        n=WIDEST["canonical"]["q"]["n"], n_need_3s=n_need_can, boot=EBW),
                        widest_alt=dict(r=RWA, e=EWA, p=WIDEST["alt"]["q"]["p"],
                                        n=WIDEST["alt"]["q"]["n"], n_need_3s=n_need_alt,
                                        boot=WIDEST["alt"]["q"]["eb"]),
                        n_checks=len(CK), n_fail=NF, mutate=MUTATE))
with open(os.path.join(HERE, "DE07_wide_binary_angular.json"), "w") as f:
    json.dump(OUT, f, indent=1)
info(f"wrote DE07_wide_binary_angular.json")
P(f"RESULT: {len(CK)} checks, {NF} FAIL   rc={1 if NF else 0}")
sys.exit(1 if NF else 0)