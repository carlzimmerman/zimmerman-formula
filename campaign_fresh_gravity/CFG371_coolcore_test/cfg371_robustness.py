"""CFG371 POST-FREEZE robustness (labelled; the frozen verdict stands as computed). Shared-variable check: t_c and X_in both
depend on the core gas (t_c ~ 1/rho_gas; X_in divides by M_b). Alternatives that do not divide by the gas, and partial correlations."""
import json, os, numpy as np
from astropy.io import fits
from scipy.stats import spearmanr, rankdata
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
J = json.load(open(os.path.join(HERE, "cfg371_results.json")))
xdir = os.path.join(REPO, "real_research", "data", "xcop"); r500j = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
import sys; sys.path.insert(0, os.path.join(HERE, "..")); import CFG4_common as C4
G, MSUN, KPC = 6.674e-8, 1.989e33, 3.0857e21; a0 = 9.3603e-9
def partial(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz); ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    return float(np.corrcoef(ex, ey)[0, 1])
out = {}
for subset in ("primary", "all12"):
    rows = [r for r in J["rows"] if (r["primary"] or subset == "all12")]
    tc, Xb, Xh, X5, fg, M5 = [], [], [], [], [], []
    for r in rows:
        nm = r["name"]; d = os.path.join(xdir, nm)
        hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
        fgp = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data
        R500 = r500j[nm]["R500"] * 1000; M500 = r500j[nm]["M500"] * 1e14; rin = 0.1 * R500
        Mh = float(np.interp(rin, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float)))
        Mg = float(np.exp(np.interp(np.log(0.1), np.log(np.asarray(fgp["RADIUS"], float)), np.log(np.asarray(fgp["MGAS"], float)))))
        if r["primary"]:
            ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
            Ms = float(np.exp(np.interp(np.log(rin), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
        else:
            Ms = 0.1 * Mg
        Mb = Mg + Ms; gN = G * Mb * MSUN / (rin * KPC) ** 2
        Mlaw = C4.nu_mono(np.array([gN / a0]))[0] * Mb
        tc.append(r["t_c_Gyr"]); Xb.append((Mh - Mlaw) / (5.364 * Mb)); Xh.append((Mh - Mlaw) / Mh); X5.append((Mh - Mlaw) / M500)
        fg.append(Mg / Mh); M5.append(M500)
    tc, Xb, Xh, X5, fg, M5 = map(np.array, (tc, Xb, Xh, X5, fg, M5))
    res = dict(N=len(tc), rho_frozen=float(spearmanr(tc, Xb).correlation),
               rho_excess_over_Mtot=float(spearmanr(tc, Xh).correlation), rho_excess_over_M500=float(spearmanr(tc, X5).correlation),
               partial_frozen_given_M500=partial(tc, Xb, M5), partial_frozen_given_fgas=partial(tc, Xb, fg),
               partial_Mtot_given_fgas=partial(tc, Xh, fg), rho_tc_fgas=float(spearmanr(tc, fg).correlation))
    out[subset] = res
    print(f"{subset} (N {res['N']}): frozen rho {res['rho_frozen']:+.2f} | excess/M_tot(<r) {res['rho_excess_over_Mtot']:+.2f} | excess/M500 "
          f"{res['rho_excess_over_M500']:+.2f} | partial|M500 {res['partial_frozen_given_M500']:+.2f} | partial|f_gas {res['partial_frozen_given_fgas']:+.2f} "
          f"| (excess/M_tot) partial|f_gas {res['partial_Mtot_given_fgas']:+.2f} | rho(t_c, f_gas) {res['rho_tc_fgas']:+.2f}")
json.dump(out, open(os.path.join(HERE, "cfg371_robustness_results.json"), "w"), indent=1)
