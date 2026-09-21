"""Finite research checks; output JSON. Neither observational discovery nor proof."""
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from astropy.table import Table
from scipy.integrate import quad
from scipy.stats import spearmanr
from transport import run_suite, integrated_rate_temperature

HERE = Path(__file__).resolve().parent
K = 1.380649e-23
ME = 9.1093837139e-31
C = 299792458.
SIGMA_T = 6.6524587051e-29
DAY = 86400.


def mean_time(sigma_kms, n_cm3, temp):
    return ME*(sigma_kms*1000)**2/(2*K*SIGMA_T*C*n_cm3*1e6*temp)


def catalog():
    path = HERE / "data/deGraaff2026_mnras_lrds_withdups_blackbody_eline_fits.fits"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "8a319c5c4ba2700475247bf4a70e42baeb6d2e03b5a25365efd82808e52ed91c")
    t = Table.read(path)
    assert len(t) == 181 and sum(t["use_dG26"]) == 146
    med = lambda name: np.asarray(t[name], dtype=float)[:, 2]
    lb, lh, te = med("logL_MBB"), med("logLHa_total"), med("Teff")
    sel = np.asarray(t["use_dG26"], bool) & (t["zspec"] < 4.5) & np.isfinite(lb+lh+te)
    ratio = 10**(lh[sel]-lb[sel])
    assert len(ratio) == 47
    rng = np.random.default_rng(9212610)
    bootstrap = np.median(rng.choice(ratio, (10000, len(ratio))), axis=1)
    rows = []
    for i in np.where(sel)[0]:
        rows.append(dict(pid=int(t["pid"][i]), srcid=int(t["srcid"][i]),
                         z=float(t["zspec"][i]), logL_MBB=float(lb[i]),
                         logLHa_total=float(lh[i]), temperature_MBB=float(te[i]),
                         Ha_over_MBB=float(10**(lh[i]-lb[i]))))
    # Countermodel to a universal 1/15: energy bookkeeping itself leaves two knobs.
    # y=0.45 is an illustrative Case-B yield, NOT a fitted dense-LRD gas parameter.
    e_ha = 1239.841984/656.28
    energy_models = []
    for eion in (13.6, 20., 30., 50.):
        for thermal_fraction in (.3, .6, 1.):
            line_fraction = .45*e_ha/eion
            energy_models.append(dict(mean_ionizing_eV=eion,
                thermal_capture_fraction=thermal_fraction,
                Ha_over_thermal=line_fraction/(thermal_fraction*(1-line_fraction))))
    # BB ionizing deficit is a toy continuum hypothesis; MBB T is not atmosphere T.
    toy = []
    for temp in (4233., 4662., 6000., 10000.):
        kt_ev = 8.617333262145e-5*temp
        x0 = 13.6/kt_ev
        photons = quad(lambda x: x*x*np.exp(-x)/(1-np.exp(-x)), x0, np.inf)[0]
        line_to_bol = .45*e_ha/kt_ev * photons/(math.pi**4/15)
        toy.append(dict(temperature_K=temp, Ha_over_bol_max_caseB_BB=line_to_bol,
                        median_observed_over_toy=float(np.median(ratio)/line_to_bol)))
    rho, p = spearmanr(lb[sel], np.log10(ratio))
    return dict(rows=rows, n=47, total_entries=181, unique_sources=146,
                ratio_quantiles_5_16_50_84_95=np.percentile(ratio,[5,16,50,84,95]).tolist(),
                log10_ratio_std=float(np.std(np.log10(ratio))),
                bootstrap_median_95pct=np.percentile(bootstrap,[2.5,97.5]).tolist(),
                above_one_fifteenth=int(np.sum(ratio>1/15)),
                exploratory_spearman_with_LBB=dict(rho=float(rho),p_unadjusted=float(p)),
                energy_countermodels=energy_models, toy_blackbody_budget=toy)


def main():
    # Independent deterministic benchmarks for the transport ingredients.
    assert abs(quad(lambda u: 3/8*(1+u*u), -1, 1)[0]-1) < 1e-12
    assert abs(quad(lambda u: u*3/8*(1+u*u), -1, 1)[0]) < 1e-12
    assert abs(quad(lambda u: u*u*3/8*(1+u*u), -1, 1)[0]-.4) < 1e-12
    pos = np.array([[.1, .2, .3]])
    direct = np.array([[0., 0., 1.]])
    exact = integrated_rate_temperature(pos, direct, np.array([.25]), 2., 3., 4.)[0]
    numeric = quad(lambda s: 2*(1+3*(.05+(.3+s)**2))*(1+4*(.05+(.3+s)**2)),0,.25)[0]
    assert np.isclose(exact,numeric,rtol=1e-13)
    # SI/cgs benchmark: n_e=1e8 cm^-3 implies a 5.80-day mean free-flight time.
    free_flight = 1/(1e8*1e6*SIGMA_T*C)/DAY
    assert 5.8 < free_flight < 5.81
    simulations = run_suite()
    values = []
    # W is FWHM of a FULL normalized Laplace profile, not of a selected wing.
    for width in (1000., 2000.):
        sigma = width/(math.sqrt(2)*math.log(2))
        for density in (10**6.5, 1e8, 1e10):
            dt = mean_time(sigma, density, 1e4)
            values.append(dict(full_Laplace_FWHM_kms=width,
                rms_width_kms=sigma, electron_density_cm3=density,
                temperature_K=1e4, residence_upper_days=dt/DAY,
                central_sphere_amplitude_floor_P200days=max(0.,1-2*math.pi*dt/(200*DAY)),
                distributed_source_amplitude_floor_P200days=max(0.,1-4*math.pi*dt/(200*DAY))))
    # An exact case: a fixed path without scattering has zero observer delay.
    assert mean_time(1000.,1e8,1e4) > 0
    assert np.isclose(mean_time(2000.,1e8,1e4)/mean_time(1000.,1e8,1e4),4)
    # Necessary density ceiling for attenuation to A at period P, central sphere.
    sigma = 2000/(math.sqrt(2)*math.log(2))
    density_ceiling = ME*(sigma*1000)**2*2*math.pi/(2*K*SIGMA_T*C*1e4*.9*200*DAY)/1e6
    result = dict(status="conditional standard-physics constraint; no new law established",
        transport=simulations, numerical_examples=values,
        mean_free_flight_days_ne1e8=float(free_flight),
        density_ceiling_cm3_for_W2000_P200days_A0p1=float(density_ceiling),
        catalog=catalog(), python=sys.version, numpy=np.__version__)
    output = Path(sys.argv[1])
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("catalog","transport")},indent=2))
    print("Transport ratios:", [r["v2_over_2_exposure"] for r in simulations])
    print("Catalogue median:", result["catalog"]["ratio_quantiles_5_16_50_84_95"][2])
    print("Catalogue 95% bootstrap:", result["catalog"]["bootstrap_median_95pct"])


if __name__ == "__main__":
    main()
