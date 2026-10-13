"""CFG724: does SPARC's dark surface density stay below the derived cold-energy capacity Sigma_max = a0/(pi G) (CFG722)?
Raw SPARC rotmod (Vobs, errV, Vgas, Vdisk, Vbul). Upsilon_disk 0.5, Upsilon_bul 0.7 (standard 3.6um; bracket 0.3/0.8).
Sigma_dark(<R) = M_dark(<R) / (pi R^2), M_dark = (Vobs^2 - Vbar^2) R / G. Ceiling: a0/(pi G); MOND-style plateau context a0/(2 pi G).
Also reported: the mean dark surface density at the radius where g_bar = a0 (the 'law radius').  kappa = 1/2 FITTED."""
import glob, os, json, numpy as np
G = 4.30091e-3            # pc (km/s)^2 / Msun
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
conv = 3.0857e16 / 1e6     # m/s^2 -> (km/s)^2/pc
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "real_research", "data", "sparc_data")
files = sorted(glob.glob(os.path.join(D, "*_rotmod.dat")))
out = {}
for ud, ub in [(0.5, 0.7), (0.3, 0.5), (0.8, 1.0)]:
    rows = []
    for f in files:
        try: d = np.loadtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[0] < 3: continue
        R = d[:, 0] * 1e3; Vo, eV, Vg, Vd, Vb = d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
        Vbar2 = Vg * np.abs(Vg) + ud * Vd * np.abs(Vd) + ub * Vb * np.abs(Vb)
        Md = (Vo**2 - Vbar2) * R / G; Sig = Md / (np.pi * R**2)
        dSig = 2 * Vo * eV * R / G / (np.pi * R**2)
        gbar = np.maximum(Vbar2, 1e-9) / R
        rows.append(dict(name=os.path.basename(f)[:-11], R=R, Sig=Sig, dSig=dSig, gbar=gbar))
    res = {}
    for k, a0 in A0.items():
        cap = a0 * conv / (np.pi * G); half = cap / 2
        nviol, n3, maxz, sig_at_law = 0, 0, [], []
        allS = np.concatenate([r["Sig"] for r in rows]); alld = np.concatenate([r["dSig"] for r in rows])
        z = (allS - cap) / np.maximum(alld, 1e-9)
        for r in rows:
            gb = r["gbar"]; a = a0 * conv
            i = np.where(gb < a)[0]
            if len(i): sig_at_law.append(r["Sig"][i[0]])
        res[k] = dict(cap=cap, half_cap=half, n_points=int(len(allS)), n_galaxies=len(rows),
                      frac_above_cap=float(np.mean(allS > cap)), n_above_cap_3sigma=int(np.sum(z > 3)),
                      max_Sig=float(np.max(allS)), p99_Sig=float(np.percentile(allS, 99)), median_Sig=float(np.median(allS)),
                      median_Sig_at_law_radius=float(np.median(sig_at_law)), n_law=len(sig_at_law),
                      worst=[(r["name"], float(np.max(r["Sig"]))) for r in sorted(rows, key=lambda r: -np.max(r["Sig"]))[:5]])
    out[f"ud{ud}_ub{ub}"] = res
    for k, v in res.items():
        print(f"Y=({ud},{ub}) {k}: ceiling a0/(piG) = {v['cap']:.0f} Msun/pc^2 (half {v['half_cap']:.0f}); {v['n_points']} pts / {v['n_galaxies']} gal; "
              f"above ceiling {100*v['frac_above_cap']:.1f}% (>3sigma: {v['n_above_cap_3sigma']}); max {v['max_Sig']:.0f}, p99 {v['p99_Sig']:.0f}, median {v['median_Sig']:.0f}; "
              f"median at law radius {v['median_Sig_at_law_radius']:.0f} (n {v['n_law']}); worst {v['worst'][:3]}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfg724_results.json"), "w"), indent=1, default=float)
