"""LAM9: build the template npz from the 1092 extracted E-MILES spectra (criteria 9c1f411110, amendment A1); check C4.
Downloaded data are untrusted: this script lives outside the data folder and takes every path as an argument.
Run: python3 -I lam9_templates.py FITS_DIR OUT_MASS_BI OUT_MASS_CH OUT_MASS_KU OUT_NPZ
Writes OUT_NPZ and, in this folder, lam9_templates.out / .json. Single thread, under a minute. κ = ½ FITTED; not theory closed."""
import os, sys, json
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
from importlib import resources
import numpy as np
from astropy.io import fits
import ppxf.ppxf_util as util
HERE = os.path.dirname(os.path.abspath(__file__))
FD, MBI, MCH, MKU, ONPZ = sys.argv[1:6]
GAMMAS = [0.30, 0.50, 0.80, 1.30, 1.50, 1.80, 2.00, 2.30, 2.50, 2.80, 3.00, 3.30, 3.50]
AGES = [1.00, 1.25, 1.50, 2.00, 2.50, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 10.00, 12.00, 14.00]
METALS = [-0.96, -0.66, -0.35, 0.06, 0.26, 0.40]
ZTAB = {-0.96: -0.9614, -0.66: -0.6575, -0.35: -0.3512, 0.06: 0.0600, 0.26: 0.2559, 0.40: 0.3971}  # out_mass [M/H] values
LMIN, LMAX = 3500.0, 9400.0
OUT = []; RES = {"lane": "LAM9", "step": "templates", "note": "κ = ½ FITTED; not theory closed"}
def P(s=""): print(s, flush=True); OUT.append(s)

def table(fn):
    """IMF slope [M/H] Age Mtotal M(*+remn) M* Mremn Mgas M(*+remn)/Lv M*/Lv Mv -> dict keyed (slope, MH, age)."""
    T = {}
    for l in open(fn):
        c = l.split()
        if len(c) < 12 or not c[1].replace(".", "").isdigit(): continue
        T[(round(float(c[1]), 2), round(float(c[2]), 4), round(float(c[3]), 4))] = dict(Mtot=float(c[4]), Msr=float(c[5]), MLV=float(c[9]))
    return T
TBI, TCH, TKU = table(MBI), table(MCH), table(MKU)
P(f"mass tables: BI {len(TBI)} rows, CH {len(TCH)}, KU {len(TKU)}")

names, gam, age, met = [], [], [], []
for a in AGES:
    for z in METALS:
        for g in GAMMAS:
            names.append(f"Ebi{g:.2f}Z{'m' if z < 0 else 'p'}{abs(z):.2f}T{a:07.4f}_iTp0.00_baseFe.fits"); gam.append(g); age.append(a); met.append(z)
lam_full = None; spec = None
for k, nm in enumerate(names):
    with fits.open(os.path.join(FD, nm)) as h:
        hd = h[0].header; d = np.asarray(h[0].data, dtype=np.float64)
        if lam_full is None:
            assert hd["NAXIS1"] == 53689 and abs(hd["CRVAL1"] - 1680.2) < 1e-6 and abs(hd["CDELT1"] - 0.9) < 1e-9 and hd["CRPIX1"] == 1, nm
            lam_full = hd["CRVAL1"] + hd["CDELT1"] * (np.arange(hd["NAXIS1"]) + 1 - hd["CRPIX1"]); cut = (lam_full >= LMIN) & (lam_full <= LMAX)
            spec = np.empty((int(cut.sum()), len(names)), np.float64)
        else:
            assert hd["NAXIS1"] == 53689 and abs(hd["CRVAL1"] - 1680.2) < 1e-6 and abs(hd["CDELT1"] - 0.9) < 1e-9, nm
        assert np.all(np.isfinite(d)) and d.min() >= 0, nm
        spec[:, k] = d[cut]
lam = lam_full[cut]; gam, age, met = np.array(gam), np.array(age), np.array(met)
P(f"read {len(names)} spectra; kept {lam[0]:.1f}-{lam[-1]:.1f} A ({len(lam)} px at 0.9 A, air)")

def lum(band):
    """Band luminosity in solar units per M_sun formed, as ppxf.sps_util.sps_lib.mass_to_light computes it."""
    p1 = util.synthetic_photometry(lam, spec, band, redshift=0, quiet=True)
    f1 = p1.flux / (4 * np.pi * 3.085677581491367e+19 ** 2) * 3.828e+33
    a = np.load(resources.files("ppxf") / "sps_models/spectra_sun_vega.npz")
    p2 = util.synthetic_photometry(a["lam"], a["flux_sun"], band, redshift=0, quiet=True)
    return np.ravel(f1 / p2.flux)
Lr, LV = lum("SDSS/r"), lum("Johnson-Cousins_V")
mass = np.array([TBI[(g, ZTAB[z], a)]["Msr"] for g, z, a in zip(gam, met, age)])
mlv_tab = np.array([TBI[(g, ZTAB[z], a)]["MLV"] for g, z, a in zip(gam, met, age)])
ups_r = mass / Lr
i13 = {(a, z): k for k, (g, a, z) in enumerate(zip(gam, age, met)) if abs(g - 1.30) < 1e-9}
ups_r13 = np.array([ups_r[i13[(a, z)]] for a, z in zip(age, met)])

# C4: synthetic Johnson-Cousins V M(*+remn)/L_V against the MILES table, five templates, within 3 %
c4 = []
for g, a in ((0.80, 12.0), (1.30, 12.0), (2.30, 12.0), (3.30, 12.0), (1.30, 2.0)):
    k = int(np.flatnonzero((np.abs(gam - g) < 1e-9) & (np.abs(age - a) < 1e-9) & (np.abs(met - 0.06) < 1e-9))[0])
    mine = mass[k] / LV[k]; c4.append(dict(gamma=g, age=a, mh=0.06, ml_v_synthetic=float(mine), ml_v_table=float(mlv_tab[k]), ratio=float(mine / mlv_tab[k])))
    P(f"C4 Gamma_b {g:.2f}, {a:5.2f} Gyr, [M/H] +0.06: M/L_V synthetic {mine:.4f}, table {mlv_tab[k]:.4f}, ratio {mine / mlv_tab[k]:.4f}")
c4ok = all(abs(x["ratio"] - 1) <= 0.03 for x in c4)
P(f"C4 (all five within 3 %): {'PASS' if c4ok else 'FAIL -> NO VERDICT on every question'}")
# reference IMF ratios on the full table grid (53 ages x 12 [M/H]): Ups_V(BI 1.3) / Ups_V(CH) and / Ups_V(KU)
tab_age = np.array(sorted({k[2] for k in TCH})); tab_mh = np.array(sorted({k[1] for k in TCH}))
rCH = np.array([[TBI[(1.30, m, a)]["MLV"] / TCH[(1.30, m, a)]["MLV"] for m in tab_mh] for a in tab_age])
rKU = np.array([[TBI[(1.30, m, a)]["MLV"] / TKU[(1.30, m, a)]["MLV"] for m in tab_mh] for a in tab_age])
ia, im = int(np.argmin(np.abs(tab_age - 12.0))), int(np.argmin(np.abs(tab_mh - 0.06)))
P(f"reference ratios at 12 Gyr, [M/H] +0.06: Ups_V(BI 1.3)/Ups_V(CH) {rCH[ia, im]:.4f}; Ups_V(BI 1.3)/Ups_V(KU) {rKU[ia, im]:.4f}")
P(f"alpha range of single templates (Ups_r / Ups_r at Gamma_b 1.3), 12 Gyr +0.06: " +
  ", ".join(f"{g:.1f}: {ups_r[k] / ups_r13[k]:.3f}" for g in GAMMAS for k in np.flatnonzero((np.abs(gam - g) < 1e-9) & (age == 12.0) & (met == 0.06))))
os.makedirs(os.path.dirname(ONPZ), exist_ok=True); tmp = ONPZ + ".part.npz"
np.savez(tmp, lam=lam, spec=spec.astype(np.float32), gamma=gam, age=age, metal=met, names=np.array(names), mass=mass, Lr=Lr, LV=LV,
         mlv_table=mlv_tab, ups_r=ups_r, ups_r13=ups_r13, tab_age=tab_age, tab_mh=tab_mh, ratio_CH=rCH, ratio_KU=rKU, fwhm=2.51)
os.replace(tmp, ONPZ)
RES.update(n=len(names), lam_range=[float(lam[0]), float(lam[-1])], C4=c4, C4_pass=bool(c4ok), ratio_CH_12Gyr_p006=float(rCH[ia, im]), ratio_KU_12Gyr_p006=float(rKU[ia, im]))
open(os.path.join(HERE, "lam9_templates.out"), "w", encoding="utf-8").write("\n".join(OUT) + "\nκ = ½ FITTED; not theory closed.\n")
json.dump(RES, open(os.path.join(HERE, "lam9_templates.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
