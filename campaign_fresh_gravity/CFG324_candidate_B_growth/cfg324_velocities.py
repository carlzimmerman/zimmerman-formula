#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG324 part 2 -- PECULIAR VELOCITIES: 6dFGSv fundamental-plane distances against the 2M++ density cube -> f sigma_8 at z ~ 0.04,
compared with each reading's prediction from part 1 (cfg324_growth_lensing_results.json).

Frozen criteria: FROZEN_CRITERIA.md (197ee7c08), section 3.2 and 4.  Data on disk only: real_research/data/fp_6dfgs_campbell2014.tsv
(J band, Js = 1) and real_research/data/twompp_density.npy.  No downloads.  kappa = 1/2 fixed; the readings' a0 dependence enters
only through part 1's predictions.

Model: log R_e,i = a log sigma_0 + b log I_e + c + eta_i,  eta_i = -log10(1 - v_i/cz_i),  v_i = beta u_i + V_ext . rhat_i,
u_i = the radial beta = 1 velocity from the cube (v(k) = i 100 delta(k) kvec/k^2 km/s), least squares in log R_e.
f sigma_8,obs = beta_corrected x sigma_8,g,lin (the cube's own top-hat 8 Mpc/h rms, smoothing and nonlinear corrections).
MUTATE (CFG324_MUTATE=1): R1's prediction x 2 (growth amplitude x2); R1's velocity row must FAIL (rc = 1).

Run from the repository root (after part 1):  python3 campaign_fresh_gravity/CFG324_candidate_B_growth/cfg324_velocities.py
"""
import os, sys, io, json, math, time, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg324_common as K
import numpy as np
import pandas as pd
from scipy import fft as sfft
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares
from classy import Class

warnings.filterwarnings("ignore")
R = K.Run("cfg324_velocities")
P, banner, check = R.P, R.banner, R.check
P(__doc__.strip())
if K.MUTATE:
    P("\n  *** MUTATE=1: R1's predicted f sigma_8 is doubled (growth x2); R1's velocity row must FAIL ***")
rng = np.random.default_rng(324)
CKMS = 299792.458
P1 = json.load(open(os.path.join(K.HERE, "cfg324_growth_lensing_results.json")))["numbers"]

# ================================================================================================ the FP sample
banner("D  DATA: 6dFGSv J-band fundamental-plane sample (Campbell et al. 2014, VizieR J/MNRAS/443/1231) and the 2M++ cube")
L = open(os.path.join(K.DATA, "fp_6dfgs_campbell2014.tsv")).read().splitlines()
i0 = [k for k, l in enumerate(L) if l.startswith("recno")][0]
df = pd.read_csv(io.StringIO("\n".join([L[i0]] + L[i0 + 3:])), sep="\t", na_values=["", " "], skipinitialspace=True, dtype=str)
for c in ("cz", "cz.gr", "JlogRe", "JlogIe", "logVd", "Jlogr", "Jtot", "RAJ2000", "DEJ2000", "Js"):
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df[df["Js"] == 1].dropna(subset=["cz", "JlogRe", "JlogIe", "logVd", "RAJ2000", "DEJ2000", "Jtot"]).reset_index(drop=True)
czu = df["cz.gr"].fillna(df["cz"]).to_numpy(float)
s_, i_, r_ = df["logVd"].to_numpy(float), df["JlogIe"].to_numpy(float), df["JlogRe"].to_numpy(float)
mJ = df["Jtot"].to_numpy(float)
N = len(df)
zmed = float(np.median(czu / CKMS))
P(f"    J-band sample: {N} galaxies (Js = 1); cz {czu.min():.0f}-{czu.max():.0f} km/s (group cz where given: {df['cz.gr'].notna().sum()}); "
  f"median z = {zmed:.4f}; log sigma_0 >= {s_.min():.3f}; J_tot <= {mJ.max():.3f}")
# C3a: the catalogue's log R_e from the angular radius and cz (angular-diameter distance, H0 = 100 h)
th = 10 ** df["Jlogr"].to_numpy(float) / 206264.806
zz = czu / CKMS
dres = np.log10(th * czu / 100.0 / (1 + zz) * 1000.0) - r_
off, rms_ = float(np.median(dres)), float(np.std(dres - np.median(dres)))
check("C3a CONTROL: the catalogue's log R_e (kpc/h) is reproduced from its angular radius and cz (group cz where given) to rms <= 0.005 dex",
      f"rms {rms_:.4f} dex about a median offset {off:+.4f} dex", rms_ <= 0.005)

# positions, Galactic Cartesian (Mpc/h), redshift space
ra, de = np.radians(df["RAJ2000"].to_numpy(float)), np.radians(df["DEJ2000"].to_numpy(float))
xeq = np.vstack([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)])
MG = np.array([[-0.0548755604, -0.8734370902, -0.4838350155], [0.4941094279, -0.4448296300, 0.7469822445],
               [-0.8676661490, -0.1980763734, 0.4559837762]])
rhat = (MG @ xeq).T
pos = rhat * (czu / 100.0)[:, None]

# ================================================================================================ the velocity field
cube = np.load(os.path.join(K.DATA, "twompp_density.npy"))
NG, CEN, SP = 257, 128, 400.0 / 256.0
NP, OFF = 384, (384 - 257) // 2
pad = np.zeros((NP, NP, NP), np.float32); pad[OFF:OFF + NG, OFF:OFF + NG, OFF:OFF + NG] = cube
dk = sfft.rfftn(pad, workers=2)
kx = 2 * math.pi * sfft.fftfreq(NP, d=SP).astype(np.float32); kz = 2 * math.pi * sfft.rfftfreq(NP, d=SP).astype(np.float32)
VF = []
for comp in range(3):
    KX = kx[:, None, None]; KY = kx[None, :, None]; KZ = kz[None, None, :]
    K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
    KC = (KX, KY, KZ)[comp]
    VF.append(sfft.irfftn(1j * 100.0 * dk * KC / K2, s=(NP, NP, NP), workers=2).astype(np.float32))
    del K2
LGC = CEN + OFF
v0 = np.array([VF[c][LGC, LGC, LGC] for c in range(3)])
# direct sum at the origin (h85's definition: 3 < r < 200 Mpc/h, beta = 1)
ax = (np.arange(NG) - CEN) * SP
X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij"); RR = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
m = (RR > 3.0) & (RR < 200.0); w = cube[m] / RR[m] ** 3 * SP ** 3
vd = (100.0 / (4 * math.pi)) * np.array([np.sum(w * X[m]), np.sum(w * Y[m]), np.sum(w * Z[m])])
ang = math.degrees(math.acos(np.clip(np.dot(v0, vd) / np.linalg.norm(v0) / np.linalg.norm(vd), -1, 1)))
lb = lambda v: (math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(v[2] / np.linalg.norm(v))))
P(f"    beta = 1 velocity at the Local Group: FFT {np.linalg.norm(v0):.0f} km/s toward (l, b) = ({lb(v0)[0]:.1f}, {lb(v0)[1]:.1f}); "
  f"direct sum (3-200 Mpc/h) {np.linalg.norm(vd):.0f} km/s toward ({lb(vd)[0]:.1f}, {lb(vd)[1]:.1f}); angle {ang:.1f} deg")
check("C3b CONTROL: the FFT velocity at the origin points within 15 deg of the direct-sum apex (h85's definition)", f"{ang:.1f} deg", ang <= 15)
idx = (pos / SP + LGC).T
VG = np.vstack([map_coordinates(VF[c], idx, order=1, mode="nearest") for c in range(3)]).T
u = np.sum(VG * rhat, axis=1)
P(f"    radial beta = 1 velocities at the galaxies: rms {np.std(u):.0f} km/s, range {u.min():.0f} to {u.max():.0f}")

# ================================================================================================ the fit
banner("F  THE FIT: FP (a, b, c) + beta + V_ext, least squares in log R_e with the exact eta; bootstrap; mocks for the estimator bias")


def design(uu, cz):
    g = 1.0 / (cz * math.log(10))
    return np.column_stack([s_, i_, np.ones(N), uu * g, rhat * g[:, None]])


def fit(rr, uu, sel=None):
    sel = np.arange(N) if sel is None else sel
    A = design(uu, czu)[sel]; y = rr[sel]
    p0 = np.linalg.lstsq(A, y, rcond=None)[0]

    def res(p):
        v = p[3] * uu[sel] + rhat[sel] @ p[4:7]
        eta = -np.log10(np.clip(1 - v / czu[sel], 1e-3, None))
        return y - (p[0] * s_[sel] + p[1] * i_[sel] + p[2] + eta)
    sol = least_squares(res, p0, method="lm")
    return sol.x, float(np.std(sol.fun))


pD, scat = fit(r_, u)
P(f"    data: a = {pD[0]:.3f}, b = {pD[1]:.3f}, c = {pD[2]:.3f}; beta = {pD[3]:.3f}; V_ext = ({pD[4]:.0f}, {pD[5]:.0f}, {pD[6]:.0f}) km/s "
  f"(|V_ext| = {np.linalg.norm(pD[4:7]):.0f}); FP scatter {scat:.4f} dex")
check("C3c CONTROL: the FP scatter in log R_e lies in 0.07-0.15 dex", f"{scat:.4f}", 0.07 <= scat <= 0.15)
t0 = time.time()
BOOT = np.array([fit(r_, u, rng.integers(0, N, N))[0][3] for _ in range(500)])
sb = float(np.std(BOOT, ddof=1))
P(f"    bootstrap (500): sigma_beta = {sb:.4f} ({time.time() - t0:.0f} s)")
# shuffled-u null
ush = u[rng.permutation(N)]
pS, _ = fit(r_, ush)
check("C3d CONTROL: with the predicted velocities shuffled among galaxies the fitted beta is consistent with 0 within 3 sigma",
      f"beta_shuffled = {pS[3]:+.3f} ({pS[3] / sb:+.2f} sigma)", abs(pS[3]) <= 3 * sb)
# mocks: estimator bias under the magnitude limit and the sigma_0 floor
MLIM = float(mJ.max())
bias = []
for _ in range(50):
    vtrue = pD[3] * u + rhat @ pD[4:7]
    eta = -np.log10(np.clip(1 - vtrue / czu, 1e-3, None))
    rm = pD[0] * s_ + pD[1] * i_ + pD[2] + eta + rng.normal(0, scat, N)
    mm = mJ - 5.0 * (rm - r_)
    sel = np.where(mm <= MLIM)[0]
    bias.append(fit(rm, u, sel)[0][3] - pD[3])
bias = np.array(bias)
bmean, bstd = float(np.mean(bias)), float(np.std(bias, ddof=1))
beta_c = pD[3] - bmean
sbeta = math.sqrt(sb ** 2 + bstd ** 2)
P(f"    mocks (50, beta_true = {pD[3]:.3f}, the catalogue's J_tot <= {MLIM:.2f} re-applied): mean bias {bmean:+.4f}, spread {bstd:.4f}; "
  f"beta_corrected = {beta_c:.3f} +- {sbeta:.3f}")
R.num("fit", dict(N=N, z_med=zmed, a=pD[0], b=pD[1], c=pD[2], beta=pD[3], V_ext=pD[4:7], fp_scatter=scat, sigma_beta_boot=sb,
                  beta_shuffled=pS[3], mock_bias_mean=bmean, mock_bias_spread=bstd, beta_corrected=beta_c, sigma_beta=sbeta,
                  lg_fft_kms=np.linalg.norm(v0), lg_direct_kms=np.linalg.norm(vd), lg_angle_deg=ang))

# ================================================================================================ sigma_8 of the cube
banner("S  sigma_8,g OF THE CUBE: top-hat 8 Mpc/h rms inside r < 100 Mpc/h, octant jackknife; presmoothing and nonlinear corrections (CLASS)")
KX = kx[:, None, None]; KY = kx[None, :, None]; KZ = kz[None, None, :]
kk = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2); x8 = kk * 8.0
with np.errstate(invalid="ignore", divide="ignore"):
    WT = np.where(x8 > 1e-6, 3 * (np.sin(x8) - x8 * np.cos(x8)) / x8 ** 3, 1.0).astype(np.float32)
d8 = sfft.irfftn(dk * WT, s=(NP, NP, NP), workers=2)[OFF:OFF + NG, OFF:OFF + NG, OFF:OFF + NG]
del VF, dk
msk = RR < 100.0
s8c = float(np.sqrt(np.mean(d8[msk] ** 2)))
s8c_mean = float(np.std(d8[msk]))
octs = [msk & ((X >= 0) == bool(a)) & ((Y >= 0) == bool(b)) & ((Z >= 0) == bool(c)) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
jk = np.array([np.sqrt(np.mean(d8[msk & ~o] ** 2)) for o in octs])
s8jk = float(np.sqrt(7 / 8 * np.sum((jk - jk.mean()) ** 2)))
# corrections from CLASS LCDM shape at z = 0
XR = json.load(open(os.path.join(K.REPO, "real_research", "cross_thread_review_2026_09_26", "XR26_cmb_results.json")))["numbers"]["K1"]
cl = Class()
cl.set({"h": XR["H0"] / 100, "omega_b": 0.02237, "omega_cdm": 0.1200, "ln_A_s_1e10": 3.044, "n_s": 0.9649, "tau_reio": 0.0544,
        "output": "mPk", "non_linear": "halofit", "P_k_max_h/Mpc": 50.0, "z_max_pk": 0.0})
cl.compute(); hC = cl.h()
kh = np.geomspace(1e-4, 40, 4000)
plin = np.array([cl.pk_lin(k * hC, 0.0) for k in kh]) * hC ** 3; pnl = np.array([cl.pk(k * hC, 0.0) for k in kh]) * hC ** 3
Wth = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
sig = lambda p, Wf: math.sqrt(K.trapz(kh ** 2 * p * Wf ** 2, kh) / (2 * math.pi ** 2))
C_sm = sig(pnl, Wth(8 * kh)) / sig(pnl, Wth(8 * kh) * np.exp(-0.5 * (4 * kh) ** 2))
C_nl = sig(plin, Wth(8 * kh)) / sig(pnl, Wth(8 * kh))
s8g = s8c * C_sm * C_nl
s8sys = abs(C_sm * C_nl - 1) * s8g
s8err = math.sqrt(s8jk ** 2 + s8sys ** 2)
P(f"    cube: sigma_8 = {s8c:.4f} (about zero) / {s8c_mean:.4f} (about the sample mean); jackknife +- {s8jk:.4f}")
P(f"    corrections (CLASS LCDM, z = 0): presmoothing (4 Mpc/h Gaussian) x {C_sm:.4f}; nonlinear -> linear x {C_nl:.4f}; "
  f"sigma_8,g,lin = {s8g:.4f} +- {s8jk:.4f} (jk) +- {s8sys:.4f} (sys = full size of the corrections)")
fs8_obs = beta_c * s8g
fs8_err = fs8_obs * math.sqrt((sbeta / beta_c) ** 2 + (s8err / s8g) ** 2)
P(f"    f sigma_8,obs (z = {zmed:.3f}) = {beta_c:.3f} x {s8g:.3f} = {fs8_obs:.4f} +- {fs8_err:.4f}")
R.num("sigma8_g", dict(cube=s8c, cube_about_mean=s8c_mean, jackknife=s8jk, C_smooth=C_sm, C_nl=C_nl, lin=s8g, sys=s8sys,
                       fs8_obs=fs8_obs, fs8_err=fs8_err))

# ================================================================================================ the readings
banner("V  EACH READING'S f sigma_8(z_eff) AGAINST THE MEASUREMENT (|z| <= 2 PASS, > 3 FAIL, else NOT DETERMINED)")
ZG = np.array(P1["fs8_grid_z"])


def fsgrid(d):
    out = {}
    for k_, v in d.items():
        out[float(k_)] = v
    zs = np.array(sorted(out)); return float(np.interp(zmed, zs, [out[z] for z in zs]))


PRED = {"R1": fsgrid(P1["R1"]["fs8"]) * (2.0 if K.MUTATE else 1.0)}
for f in K.FOOTS:
    PRED[f"R2-est|{f}"] = fsgrid(P1["R2"][f"{f}|est"]["fs8"])
    PRED[f"R2-min|{f}"] = fsgrid(P1["R2"][f"{f}|min"]["fs8"])
    PRED[f"R3|{f}"] = fsgrid(P1["R3"][f]["fs8"])
    PRED[f"chassis|{f}"] = fsgrid(P1["chassis"][f]["fs8"])
VV = {}
for k_, v in PRED.items():
    zv = (v - fs8_obs) / fs8_err
    VV[k_] = dict(pred=v, z=zv, verdict="PASS" if abs(zv) <= 2 else ("FAIL" if abs(zv) > 3 else "NOT DETERMINED"))
    P(f"    {k_:18s}: predicted {v:8.4f}   z = {zv:+8.2f}   {VV[k_]['verdict']}")
check("V1 R1 (B as declared) VELOCITIES: not FAIL (|z| <= 3; pre-declared PASS or ND, P 0.7)",
      f"predicted {VV['R1']['pred']:.4f} vs {fs8_obs:.4f} +- {fs8_err:.4f}: z = {VV['R1']['z']:+.2f} ({VV['R1']['verdict']})",
      VV["R1"]["verdict"] != "FAIL")
check("V2 (reported) the chassis 'all matter feels nu_mono' FAILS the velocities on both footings (|z| > 3)",
      "; ".join(f"{f}: z = {VV[f'chassis|{f}']['z']:+.1f}" for f in K.FOOTS),
      all(VV[f"chassis|{f}"]["verdict"] == "FAIL" for f in K.FOOTS), load_bearing=False)
for lab in ("R2-est", "R2-min", "R3"):
    check(f"V3 (reported) {lab} VELOCITIES PASS on both footings (|z| <= 2)",
          "; ".join(f"{f}: z = {VV[f'{lab}|{f}']['z']:+.2f} {VV[f'{lab}|{f}']['verdict']}" for f in K.FOOTS),
          all(VV[f"{lab}|{f}"]["verdict"] == "PASS" for f in K.FOOTS), load_bearing=False)
R.num("velocity_scores", VV)

# ================================================================================================ verdicts
banner("VERDICT PER READING (lensing from part 1, velocities here; the weaker footing decides; R2 = ND if its variants disagree)")
worst = lambda vs: "FAIL" if "FAIL" in vs else ("NOT DETERMINED" if "NOT DETERMINED" in vs else "PASS")
LV = P1["lens_verdicts"]
VEL = {"R1": VV["R1"]["verdict"],
       "R2-est": worst([VV[f"R2-est|{f}"]["verdict"] for f in K.FOOTS]),
       "R2-min": worst([VV[f"R2-min|{f}"]["verdict"] for f in K.FOOTS]),
       "R3": worst([VV[f"R3|{f}"]["verdict"] for f in K.FOOTS])}
VEL["R2"] = VEL["R2-est"] if VEL["R2-est"] == VEL["R2-min"] else "NOT DETERMINED"
if K.MUTATE:
    LV = dict(LV); LV["R1"] = "(part 1 MUTATE run decides lensing)"
FINAL = {}
for k_ in ("R1", "R2", "R3"):
    pair = [LV[k_], VEL[k_]]
    FINAL[k_] = "FAIL" if "FAIL" in pair else ("PASS" if all(p == "PASS" for p in pair) else "NOT DETERMINED")
    P(f"    {k_}: lensing {LV[k_]}; velocities {VEL[k_]}  ->  {FINAL[k_]}")
P(f"    B's growth is TESTED: {'yes' if FINAL['R1'] in ('PASS', 'FAIL') else 'no'} (R1, B as declared, gets {FINAL['R1']})")
R.num("verdicts", dict(lensing=LV, velocities=VEL, final=FINAL))
sys.exit(R.finish())
