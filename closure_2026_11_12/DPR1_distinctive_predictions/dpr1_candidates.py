#!/usr/bin/env python3
"""DPR1 candidate table: B, R1, R2 per candidate, the expected error of the dated data, the separations, the class.

Every number is either copied from a committed record file (path given beside it) or computed here from the record's
adopted constants; nothing is fitted to any measurement except where a rival is defined by a published fit (R1's Milky Way
NFW, fitted to the DESI paper's own NFW extrapolation as PLT1 quotes it).  Criteria: FROZEN_CRITERIA.md (ded8ccd8e4).
Run: python3 dpr1_candidates.py -> dpr1_candidates.json, dpr1_candidates.out.  Light: one thread, < 1 s.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from scipy.optimize import brentq, least_squares
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, RES = [], {}
def P(s=""):
    print(s, flush=True); OUT.append(s)
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
K3 = 3.0                                                            # the frozen margin, in units of sigma_D

def sep(b_band, r_band, s):
    """distance between nearest band edges in units of s (0 if the bands overlap)."""
    lo1, hi1 = min(b_band), max(b_band); lo2, hi2 = min(r_band), max(r_band)
    gap = max(0.0, lo2 - hi1, lo1 - hi2); return gap / s

# ============================================================ 1. Euclid DR1 error scaling for lensing statistics (rule of section 3)
# KiDS-1000: 1006 deg2, n_eff 6.17 arcmin^-2 (CFG590 FROZEN_CRITERIA, "recalled, PROVISIONAL").  Euclid DR1: ~1,900 deg2 (A6,
# PROVISIONAL web read).  Euclid n_eff: 30 arcmin^-2 is the mission's design figure (recalled here, PROVISIONAL); a conservative 20
# is carried as the second case.  The lens sample is assumed to scale with area at KiDS's density (a bright, photo-z sample of the
# same kind); sigma_stat proportional to (A_lens x n_eff)^(-1/2) on the lens-source pair count.
A_K, N_K, A_E = 1006.0, 6.17, 1900.0
SCALE = {"nominal (n_eff 30)": math.sqrt(A_E * 30.0 / (A_K * N_K)), "conservative (n_eff 20)": math.sqrt(A_E * 20.0 / (A_K * N_K))}
P("1. Euclid DR1 / KiDS-1000 statistical-error scale factor (PROVISIONAL inputs): " + "; ".join(f"{k} {v:.3f}" for k, v in SCALE.items()))
RES["euclid_scale"] = SCALE

# ============================================================ 2. KO2 own-field statistic (primary design), early and late types
# KiDS (closure_2026_11_09/KO2_kids_own_field_by_type/RESULT.md): s_tot = sqrt(s_jk^2 + 0.05^2); early 0.487 +- 0.071, late 0.277 +- 0.183.
# B: 0.038 / 0.007 (canonical / alt), ko2_formB.json (A3, declared before the result).  R2: the law as the lens's own field gives the
# floor 0.9999 (KiDS lenses are isolated enough that the law's external-field truncation lies far beyond the windows; R2's value is
# taken as the floor).  R1: from this lane's plant, dpr1_ko2_r1.json (read below if present).
S_SYS = 0.05
KO2 = {"early": dict(s_tot=0.071, meas=0.487, B={"canonical": 0.038, "alt": 0.007}),
       "late": dict(s_tot=0.183, meas=0.277, B={"canonical": 0.038, "alt": 0.007})}
# form B's own per-type values (ko2_formB.json, primary noiseless) where stored
try:
    FB = json.load(open(os.path.join(HERE, "..", "..", "closure_2026_11_09", "KO2_kids_own_field_by_type", "ko2_formB.json")))
    for f in FOOT:
        for t in ("early", "late"):
            KO2[t]["B"][f] = FB["foot"][f]["primary"]["noiseless"][t]["R"]
    P("   form B values read from ko2_formB.json (primary, noiseless)")
except Exception as e:
    P(f"   ko2_formB.json not read ({type(e).__name__}); RESULT.md values used")
R1V = {}
for tag in ("", "_c135", "_c074", "_z0"):
    fn = os.path.join(HERE, f"dpr1_ko2_r1{tag}.json")
    if os.path.exists(fn):
        J = json.load(open(fn)); R1V[tag or "_primary"] = {f: {t: J["foot"][f]["primary"]["noiseless"][t]["R"] for t in ("early", "late")} for f in FOOT}
P(f"   R1 plants found: {sorted(R1V) or 'none'}")
RES["ko2"] = {}
for t, d in KO2.items():
    s_jk = math.sqrt(d["s_tot"] ** 2 - S_SYS ** 2)
    for sc_name, sc in SCALE.items():
        sD = math.sqrt((s_jk / sc) ** 2 + S_SYS ** 2)
        for f in FOOT:
            b = d["B"][f]; r2 = 0.9999
            r1s = [R1V[k][f][t] for k in R1V] if R1V else []
            r1band = (min(r1s), max(r1s)) if r1s else None
            sB1 = sep((b, b), r1band, sD) if r1band else None; sB2 = sep((b, b), (r2, r2), sD)
            post = (d["meas"] - b) / d["s_tot"]
            row = dict(type=t, footing=f, case=sc_name, sigma_D=sD, B=b, R1_band=r1band, R2=r2, sep_B_R1=sB1, sep_B_R2=sB2,
                       kids_measurement=d["meas"], kids_minus_B_in_kids_s_tot=post)
            RES["ko2"][f"{t}|{f}|{sc_name}"] = row
            P(f"   KO2 {t:5s} {f:9s} {sc_name:24s}: sigma_D {sD:.4f}; B {b:.3f}; R1 {('%.3f-%.3f' % r1band) if r1band else 'NOT COMPUTED'}; R2 {r2:.4f}; "
              f"|B-R1| {('%.1f' % sB1) if sB1 is not None else '-'} sD, |B-R2| {sB2:.1f} sD; KiDS sits {post:+.2f} KiDS s_tot from B")

# ============================================================ 3. Host-free shape statistic (ONE1 / SRH1R), Euclid scaling of the record's T differences
# SRH1R RESULT (closure_2026_11_10/SRH1R_blind_lensing_regrade/RESULT.md), canonical / alt, T(all), k free, 12 dof:
# ref (R1, cold reference everywhere) 7.73 / 7.73; one1 (B: the law's halo to x_t) 9.49 / 8.48; inf (law to r_ta, the nearest R2
# proxy in the record) 9.45 / 8.47.  With data near one model, T(other) - T(that) approximates the squared model distance in
# KiDS errors; it scales with sigma^-2.  A proxy: the record does not store the model vectors.
T = {"canonical": dict(ref=7.73, one1=9.49, inf=9.45), "alt": dict(ref=7.73, one1=8.48, inf=8.47)}
RES["hostfree"] = {}
for f in FOOT:
    for sc_name, sc in SCALE.items():
        d1 = math.sqrt(max(0.0, T[f]["one1"] - T[f]["ref"]) * sc ** 2); d2 = math.sqrt(max(0.0, T[f]["one1"] - T[f]["inf"]) * sc ** 2)
        RES["hostfree"][f"{f}|{sc_name}"] = dict(sep_B_R1=d1, sep_B_R2=d2)
        P(f"3. host-free shape T, {f:9s} {sc_name:24s}: |B-R1| ~ {d1:.2f} sigma, |B-R2| ~ {d2:.2f} sigma (Euclid-scaled proxy)")

# ============================================================ 4. Gaia DR4 wide binaries (pooled gamma-hat, 3-30 kAU)
# B: rule 5 (a body that brought no charge has no halo) -> Newtonian 1.000 (CQ2 seal, DR4 map S1).  R1: Newton 1.000.
# R2: CW1 bare law 1.149 +- 0.027 / 1.208 +- 0.007 (DR4 map S4).  sigma_D: sqrt(0.020^2 + sigma_fit^2), sigma_fit 0.03 at N ~ 8,000
# (DR4 map section 3 and S3; DR3's 0.055 at its N as the pessimistic case).
for sfit in (0.03, 0.055):
    sD = math.sqrt(0.02 ** 2 + sfit ** 2)
    for f, r2 in (("canonical", (1.149 - 0.027, 1.149 + 0.027)), ("alt", (1.208 - 0.007, 1.208 + 0.007))):
        RES[f"wb|{f}|{sfit}"] = dict(sigma_D=sD, B=1.0, R1=1.0, R2=r2, sep_B_R1=0.0, sep_B_R2=sep((1, 1), r2, sD))
        P(f"4. wide binaries {f:9s} sigma_fit {sfit}: sigma_D {sD:.3f}; B 1.000, R1 1.000, R2 {r2[0]:.3f}-{r2[1]:.3f}; |B-R1| 0, |B-R2| {sep((1, 1), r2, sD):.1f} sD")

# ============================================================ 5. a0 at the ALMA redshifts: B's band and R2
# B: a0 = kappa c sqrt(G rho_DE(z)).  With form B's carried cosmology (CO1: the cold reference's fit, constant dark energy) a0 is
# constant -> equal to R2.  With PAPER66's CPL benchmark (w0 -0.838, wa -0.62; forecasts/noncondor_2026_11_04) a0 falls.  B's band is
# the envelope of the two.  Deep-regime speed ratio = (a0 ratio)^(1/4).
def a0_ratio(z, w0, wa):
    a = 1 / (1 + z); return math.sqrt(a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a)))
RES["a0z"] = {}
for name, z in (("vc875", 4.5505), ("AzTEC/C159", 4.567), ("z 1.5 discs", 1.5), ("z 2.33 (AZ2)", 2.33)):
    rc = a0_ratio(z, -0.838, -0.62); band_v = (rc ** 0.25, 1.0)
    RES["a0z"][name] = dict(z=z, a0_ratio_cpl=rc, a0_ratio_constant=1.0, vflat_ratio_band=band_v, R2=1.0, sep_B_R2=0.0)
    P(f"5. a0(z) {name:14s} z {z}: B a0 ratio [{rc:.4f} (CPL), 1 (constant)]; V_flat ratio [{band_v[0]:.4f}, 1]; R2 1 -> B's band contains R2")

# ============================================================ 6. Milky Way enclosed-mass slope 100-200 kpc and potential depth (Gaia DR4 era)
MB = 6.6814e10                                                      # census baryons (EFC1)
def M_law(r_kpc, a0, Mb=MB):
    rM = math.sqrt(G * Mb * MSUN / a0) / KPC; return Mb * (0.5 + math.sqrt(0.25 + (r_kpc / rM) ** 2))
# R1: NFW fitted to the DESI paper's own extrapolation (PLT1: 7.53 / 9.65 / 11.27 x 10^11 at 100 / 150 / 200 kpc)
rr = np.array([100.0, 150.0, 200.0]); mm = np.array([7.53, 9.65, 11.27]) * 1e11
def mn(x): return np.log1p(x) - x / (1 + x)
fit = least_squares(lambda p: np.log(10 ** p[0] * mn(rr / 10 ** p[1])) - np.log(mm), x0=[11.5, 1.3])
Mn, rs = 10 ** fit.x[0], 10 ** fit.x[1]
def M_nfw(r): return Mn * mn(r / rs)
RES["mw"] = dict(nfw_norm=Mn, nfw_rs_kpc=rs, nfw_fit_resid=fit.fun.tolist())
P(f"6. R1 Milky Way NFW (fit to DESI's own extrapolation): r_s {rs:.1f} kpc; residuals {np.round(fit.fun, 4).tolist()}")
for f in FOOT:
    a0 = A0[f]
    sB = math.log(M_law(200, a0) / M_law(100, a0)) / math.log(2); sR1 = math.log(M_nfw(200) / M_nfw(100)) / math.log(2)
    rM = math.sqrt(G * MB * MSUN / a0) / KPC
    rcap = brentq(lambda r: M_law(r, a0) - (1 + 59.49) * MB, 10, 5000)
    # potential depth beyond 30 kpc (the inner part is common: all three fit the same rotation curve inside)
    def dphi(Mfun, rmax): return quad(lambda r: G * Mfun(r) * MSUN / (r * KPC) ** 2 * KPC, 30, rmax, limit=400)[0] / 1e6   # (km/s)^2
    MBf = lambda r: M_law(min(r, rcap), a0)
    MR2 = lambda r: min(M_law(r, a0), 19e11)                          # EFC1 row L 0.03 a0: saturation 19 x 10^11 (crude cut)
    out = {}
    for rmax in (300.0, 460.0, 1e5):
        db, d1, d2 = dphi(MBf, rmax), dphi(M_nfw, rmax), dphi(MR2, rmax)
        if rmax > 1e4:
            db += G * MBf(rmax) * MSUN / (rmax * KPC) / 1e6; d1 += G * M_nfw(rmax) * MSUN / (rmax * KPC) / 1e6; d2 += G * MR2(rmax) * MSUN / (rmax * KPC) / 1e6
        out[rmax] = tuple(math.sqrt(2 * v) for v in (db, d1, d2))
    RES["mw"][f] = dict(slope_B=sB, slope_R1=sR1, M200_B=M_law(200, a0), M200_R1=M_nfw(200), r_M_kpc=rM, r_cap_kpc=rcap,
                        v_reach_from_30kpc={str(k): v for k, v in out.items()})
    P(f"   {f:9s}: slope dlnM/dlnr 100-200 kpc  B {sB:.3f}  R1 {sR1:.3f}  (R2 at a literature field, EFC1 canonical table: line at 200 kpc 13.4 vs B 13.7);"
      f" M(200) B {M_law(200, a0) / 1e11:.2f}e11 R1 {M_nfw(200) / 1e11:.2f}e11; B's cap {rcap:.0f} kpc")
    for k, v in out.items():
        P(f"      speed to climb from 30 kpc to {('infinity' if k > 1e4 else '%.0f kpc' % k)}: B {v[0]:.0f}, R1 {v[1]:.0f}, R2 (crude) {v[2]:.0f} km/s")

# ============================================================ 7. Conditional on the joint: where the break sits against what dated data reach
# FLD1 table (canonical): R_fold(z) for log M_b 10.45: 139 / 76 / 48 / 17.2 kpc at z 0 / 1 / 2 / 4; RC100's worst galaxy at 0.39 R_fold;
# vc875's conditional examples reach 5 kpc (forecasts/noncondor_2026_11_04).  Extrapolated with ln R_fold linear in ln(1+z).
zz = np.array([0, 1, 2, 4.0]); RF = np.array([139, 76, 48, 17.2])
cf = np.polyfit(np.log1p(zz), np.log(RF), 2)
rf455 = float(np.exp(np.polyval(cf, math.log1p(4.5505))))
RES["joint"] = dict(R_fold_logMb10p45_z4p55_kpc=rf455, vc875_reach_over_R_fold=5.0 / rf455, rc100_worst=0.39, sparc_worst=0.47)
P(f"7. joint (CONDITIONAL): R_fold(log M_b 10.45, z 4.55) ~ {rf455:.1f} kpc; vc875's 5 kpc is {5.0 / rf455:.2f} of it; RC100 worst 0.39, SPARC worst 0.47 (FLD1)")

# ============================================================ 8. Group share and the cosmic-shear 1-halo term (copied numbers)
P("8. share to turnaround: B 5.410 / 5.412 (CO1 fit) and R1 the same fit's cold-to-baryon ratio: identical by construction; GO2 error on f_ret 0.9-1.8 vs a gate of 0.20")
P("   cosmic shear: B - R1 matter power 0.6 / 1.0 % at k 1 and 5.1 / 8.8 % at k 3 h/Mpc (CO1); R1's own baryonic-feedback spread at k 1-3 is larger (literature, PROVISIONAL)")
RES["share"] = dict(B=(5.410, 5.412), R1="same fit", sigma_GO2=(0.9, 1.8))
RES["cosmic_shear"] = dict(dP_k1=(0.006, 0.010), dP_k3=(0.051, 0.088))
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "dpr1_candidates.json"), "w"), indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
open(os.path.join(HERE, "dpr1_candidates.out"), "w").write("\n".join(OUT) + "\n")
