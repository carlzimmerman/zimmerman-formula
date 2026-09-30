#!/usr/bin/env python3
"""Run the frozen SINS AO pipeline (FROZEN_CRITERIA_2026-09-30.md, f9290e8d4) on all 35 galaxies, variants A (0.15 arcsec, S/N>5) and B (0.10 arcsec, S/N>4)."""
import numpy as np, pandas as pd, glob, os, re, json, hashlib, sys
from astropy.io import fits
from astropy.cosmology import Planck18
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sins_pipeline as P
D = "/Users/carlzimmerman/new_physics/_external_data/sins_ao/cubes/SINS-ZCSINF_AO_release/"; T = "../highz_literature_tables/sins_ao/"
t1 = pd.read_csv(T + "sins_ao_table1_sample.csv").set_index("source"); t4 = pd.read_csv(T + "sins_ao_table4_integrated_Halpha.csv").set_index("source"); t6 = pd.read_csv(T + "sins_ao_table6_kinematics.csv").set_index("source")
MAIN = {"ZC400569": "ZC400569", "ZC407376": "ZC407376"}       # tables hold N/S components next to the base name; the README centre is the main component
def num(x):
    try: return float(x)
    except Exception: return np.nan
AMEND = len(sys.argv) > 1 and sys.argv[1] == 'amend1'; SUF = '_AMEND1' if AMEND else '_FROZENRULE'
rows, profs = [], []
for f in sorted(glob.glob(D + "*_data_cut.fits")):
    name = os.path.basename(f).split("_")[0]; pa_inf = float(re.search(r"PA([+-]\d+)", f).group(1))
    z = num(t1.loc[name, "z_Halpha"]); sig = num(t4.loc[name, "sigma_tot_kms"]); sini = num(t6.loc[name, "sin_i"]); dv = num(t6.loc[name, "half_dv_obs_kms"]); pakin = num(t6.loc[name, "PA_kin_deg"])
    h = fits.open(f)[0]; data = h.data.astype(float); noise = fits.open(f.replace("data_cut", "noise_cut"))[0].data.astype(float); hd = h.header
    wave = hd["CRVAL3"] + (np.arange(data.shape[0]) + 1 - hd["CRPIX3"]) * hd["CDELT3"]
    centre = (hd["CRPIX1"] - 1, hd["CRPIX2"] - 1)
    kpc = Planck18.kpc_proper_per_arcmin(z).value / 60.0
    res = {}
    for var, fw, snr in (("A", 0.15, 5.0), ("B", 0.10, 4.0)):
        try: res[var] = P.process(data, noise, wave, z, sig if np.isfinite(sig) else 100.0, sini, fwhm=fw, snr_cut=snr, centre=centre, amend1=AMEND)
        except Exception as e: res[var] = dict(status="error: %s" % e, nacc=0)
        r = res[var]
        for p in r.get("profile", []):
            profs.append(dict(galaxy=name, variant=var, R_arcsec=p["R_arcsec"], R_kpc=p["R_arcsec"] * kpc, n_spaxels=p["n"], Vlos_kms=p["Vlos"], eVlos_kms=p["eVlos"], Vrot_kms=p["Vlos"] / sini if np.isfinite(sini) and sini > 0 else np.nan, sigma_obs_kms=p["sigma"]))
    a = res["A"]; prof = pd.DataFrame(a.get("profile", []))
    thin = True; vhalf = np.nan
    if len(prof):
        prof = prof[prof.n >= 3]
        neg, pos = (prof.R_arcsec < 0).sum(), (prof.R_arcsec > 0).sum(); thin = bool(neg < 3 and pos < 3)
        if len(prof) >= 2: vhalf = (prof.Vlos.max() - prof.Vlos.min()) / 2
    th = a.get("theta_cube", np.nan); pa_sky = (th + pa_inf) % 180 if np.isfinite(th) else np.nan
    pa_sky2 = (th - pa_inf) % 180 if np.isfinite(th) else np.nan
    d1 = abs(((pa_sky - pakin) + 90) % 180 - 90) if np.isfinite(pa_sky) and np.isfinite(pakin) else np.nan
    d2 = abs(((pa_sky2 - pakin) + 90) % 180 - 90) if np.isfinite(pa_sky2) and np.isfinite(pakin) else np.nan
    # C3: rms of V_los difference on common bins
    rms = np.nan
    if a.get("status") == "ok" and res["B"].get("status") == "ok":
        pa_, pb_ = pd.DataFrame(a["profile"]).set_index("R_arcsec").Vlos, pd.DataFrame(res["B"]["profile"]).set_index("R_arcsec").Vlos
        com = pa_.index.intersection(pb_.index)
        if len(com) >= 2:
            d = pa_.loc[com].values; e = pb_.loc[com].values; rms = float(np.sqrt(np.mean((d - e) ** 2)))
    rows.append(dict(galaxy=name, PASINF=pa_inf, z=z, kpc_per_arcsec=kpc, sigma_tot=sig, sini=sini, statusA=a.get("status"), nacc_A=a.get("nacc"), statusB=res["B"].get("status"), nacc_B=res["B"].get("nacc"), nbins_A=len(prof), thin=thin,
                     irregular=("Irr" in " ".join(str(v) for v in t6.loc[name].values)), vsys_A=a.get("vsys", np.nan), theta_cube_A=th, PA_sky_plusPASINF=pa_sky, PA_sky_minusPASINF=pa_sky2, PA_pub=pakin, dPA_best=np.nanmin([d1, d2]) if np.isfinite(d1) or np.isfinite(d2) else np.nan,
                     half_dV_mine=vhalf, half_dV_pub=dv, C1_ratio=vhalf / dv if np.isfinite(dv) and dv > 0 else np.nan, C3_rms_AB=rms, Rout_arcsec=float(prof.R_arcsec.abs().max()) if len(prof) else np.nan))
    print(name, "A:", a.get("status"), a.get("nacc"), "B:", res["B"].get("status"), res["B"].get("nacc"), "half_dV mine %.1f pub %s" % (vhalf, dv), flush=True)
pd.DataFrame(rows).to_csv("sins_ao_per_galaxy%s.csv" % SUF, index=False); pd.DataFrame(profs).to_csv("sins_ao_profiles%s.csv" % SUF, index=False)
