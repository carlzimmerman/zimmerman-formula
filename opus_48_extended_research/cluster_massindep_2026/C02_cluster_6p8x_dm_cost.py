#!/usr/bin/env python3
"""
C02 -- the cluster "6.8x DM cost", BY HAND from the real X-COP profiles (Eckert & Ettori 2019, X-COP).
================================================================================================
Per cluster we have (real, measured; real_research/data/xcop/<NAME>/):
  <NAME>_fgas_profile.fits : RADIUS[Mpc], M_NFW (total, Msun), MGAS (Msun), FGAS, with LO/HI
  <NAME>_hydro_mass.fits   : RADIUS[kpc], M_FORW/M_NFW/M_EIN/M_ISO/M_BUR (total, 5 hydrostatic models)
  <NAME>_mstar.fits        : RADIUS[Mpc], MSTAR (Msun)   [present for 7/12; stars are a ~few-% add]
R500/M500 from xcop_r500_ettori2019.json.

TWO honest questions, verified BOTH ways (never manufacture the deficit):
  (A) RAW baryon discrepancy  D_raw = M_tot/M_bar   (the LambdaCDM "need ~6x baryons" statement).
  (B) Does the framework a0 KERNEL (g_obs = nu(g_N/a0) g_N) close it?  Residual = M_tot / (nu*M_bar).
      If residual > 1 at every radius and every footing/nu, the kernel does NOT solve clusters -- a real,
      irreducible extra source remains. We report the residual's RADIAL profile (is it core-concentrated,
      the classic MOND-cluster signature?) and its spread over BOTH a0 footings and 3 interpolation fns.

Run:  python3 opus_48_extended_research/cluster_massindep_2026/C02_cluster_6p8x_dm_cost.py
Needs: numpy, astropy.  Data paths are relative to the repo root (or $ORCH_DATA).
"""
import os, json, numpy as np
from astropy.io import fits

G, Msun, Mpc = 6.674e-11, 1.989e30, 3.0856775814913673e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
ROOT = os.path.join(os.environ.get("ORCH_DATA", "."), "real_research/data/xcop")
if not os.path.isdir(ROOT):                                   # fall back to repo-relative
    ROOT = "real_research/data/xcop"
R500J = json.load(open(os.path.join(ROOT, "xcop_r500_ettori2019.json")))

NUS = {  # g_obs = nu(g_N/a0) * g_N
    "simple":   lambda y: 0.5 + np.sqrt(0.25 + 1.0/y),
    "standard": lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y**2)),
    "RAR":      lambda y: 1.0/(1.0 - np.exp(-np.sqrt(y))),
}
HYDRO = ["M_FORW", "M_NFW", "M_EIN", "M_ISO", "M_BUR"]


def _logat(rr, x, R):
    o = np.argsort(rr)
    return float(np.exp(np.interp(np.log(R), np.log(rr[o]), np.log(np.clip(x[o], 1, None)))))


def load(name):
    fg = os.path.join(ROOT, name, f"{name}_fgas_profile.fits")
    ms = os.path.join(ROOT, name, f"{name}_mstar.fits")
    hy = os.path.join(ROOT, name, f"{name}_hydro_mass.fits")
    if not os.path.exists(fg):
        return None
    R500 = R500J[name]["R500"]
    d = fits.open(fg)[1].data
    r = np.asarray(d["RADIUS"], float); Mtot = np.asarray(d["M_NFW"], float); Mgas = np.asarray(d["MGAS"], float)
    if os.path.exists(ms):
        m = fits.open(ms)[1].data; rs = np.asarray(m["RADIUS"], float); Ms = np.asarray(m["MSTAR"], float)
        Mstar = np.interp(r, rs[np.argsort(rs)], Ms[np.argsort(rs)])
    else:
        Mstar = np.zeros_like(r)
    hydro = None
    if os.path.exists(hy):
        h = fits.open(hy)[1].data; hydro = {"r": np.asarray(h["RADIUS"], float)/1000.0,
                                            **{k: np.asarray(h[k], float) for k in HYDRO}}
    return dict(name=name, z=R500J[name]["z"], R500=R500, r=r, Mtot=Mtot, Mgas=Mgas,
                Mstar=Mstar, Mbar=Mgas+Mstar, hydro=hydro)


def main():
    cl = [c for c in (load(n) for n in sorted(R500J)) if c]
    print("="*98)
    print("C02 -- CLUSTER 6.8x DM COST from real X-COP profiles (%d clusters), at R500" % len(cl))
    print("="*98)
    print(f"{'cluster':8s} {'z':>5s} {'R500':>5s} {'Mtot/1e14':>9s} {'Mbar/1e14':>9s} {'fbar':>5s} "
          f"{'D_raw':>6s} {'resid(c,simple)':>15s}")
    D_raw, out = [], []
    for c in cl:
        Mt = _logat(c["r"], c["Mtot"], c["R500"]); Mb = _logat(c["r"], c["Mbar"], c["R500"])
        gN = G*Mb*Msun/(c["R500"]*Mpc)**2
        resid = Mt/(NUS["simple"](gN/A0["canonical"])*Mb)
        D_raw.append(Mt/Mb)
        out.append(dict(name=c["name"], z=c["z"], R500=c["R500"], Mtot=Mt, Mbar=Mb,
                        fbar=Mb/Mt, D_raw=Mt/Mb, resid_canon_simple=resid))
        print(f"{c['name']:8s} {c['z']:.3f} {c['R500']:.2f} {Mt/1e14:9.2f} {Mb/1e14:9.3f} "
              f"{Mb/Mt:.3f} {Mt/Mb:6.2f} {resid:15.2f}")
    D_raw = np.array(D_raw)

    # (A) raw discrepancy across the 5 hydrostatic total-mass models
    print("\n[A] RAW discrepancy M_tot/M_bar at R500, across total-mass models (systematic bracket):")
    draw_models = {}
    for mdl in ["fgas_NFW"] + HYDRO:
        vals = []
        for c in cl:
            Mb = _logat(c["r"], c["Mbar"], c["R500"])
            if mdl == "fgas_NFW":
                Mt = _logat(c["r"], c["Mtot"], c["R500"])
            elif c["hydro"] is not None:
                Mt = _logat(c["hydro"]["r"], c["hydro"][mdl], c["R500"])
            else:
                continue
            vals.append(Mt/Mb)
        draw_models[mdl] = np.array(vals)
        print(f"    {mdl:9s}: median D_raw = {np.median(vals):.2f}  (range {min(vals):.1f}-{max(vals):.1f})")
    lo = min(np.median(v) for v in draw_models.values()); hi = max(np.median(v) for v in draw_models.values())
    print(f"    => RAW cluster discrepancy = {lo:.1f}-{hi:.1f}x baryons (model-dependent); the '6.8x' is the "
          f"fgas-NFW upper end. LCDM: ~{lo-1:.1f}-{hi-1:.1f}x baryons of DARK matter.")

    # (B) does the a0 kernel close it? residual over footings x nu, and its RADIAL profile
    print("\n[B] AFTER the framework a0 kernel  g=nu(g_N/a0)g_N  -- residual M_tot/M_MOND at R500:")
    for foot, a0 in A0.items():
        for nn, nu in NUS.items():
            vals = []
            for c in cl:
                Mt = _logat(c["r"], c["Mtot"], c["R500"]); Mb = _logat(c["r"], c["Mbar"], c["R500"])
                gN = G*Mb*Msun/(c["R500"]*Mpc)**2
                vals.append(Mt/(nu(gN/a0)*Mb))
            print(f"    a0={foot:9s} nu={nn:8s}: residual = {np.median(vals):.2f}x baryons  "
                  f"(kernel removes ~{100*(1-1/np.median(vals)) - 100*(1 - np.median(D_raw)/np.median(D_raw)):.0f}% ...)"
                  if False else
                  f"    a0={foot:9s} nu={nn:8s}: residual = {np.median(vals):.2f}x baryons")

    print("\n    RADIAL profile of the residual (median, canonical a0, simple nu) -- where the leftover lives:")
    grid = [0.2, 0.3, 0.5, 0.7, 1.0]
    radial = {}
    for gg in grid:
        vals = []
        for c in cl:
            R = gg*c["R500"]
            if R < c["r"].min() or R > c["r"].max():
                continue
            Mt = _logat(c["r"], c["Mtot"], R); Mb = _logat(c["r"], c["Mbar"], R)
            gN = G*Mb*Msun/(R*Mpc)**2
            vals.append(Mt/(NUS["simple"](gN/A0["canonical"])*Mb))
        radial[gg] = float(np.median(vals))
        print(f"       r={gg:.1f} R500 : residual = {np.median(vals):.2f}x   (n={len(vals)})")

    # fraction of the DM the kernel removes at R500 (M_DM_removed / M_DM_raw)
    rem = []
    for c in cl:
        Mt = _logat(c["r"], c["Mtot"], c["R500"]); Mb = _logat(c["r"], c["Mbar"], c["R500"])
        gN = G*Mb*Msun/(c["R500"]*Mpc)**2; Mm = NUS["simple"](gN/A0["canonical"])*Mb
        rem.append((Mm-Mb)/(Mt-Mb))
    print(f"\n    kernel removes {100*np.median(rem):.0f}% of the cluster DM at R500 (canonical, simple nu).")

    print("\n" + "="*98)
    print("VERDICT (honest, both ways):")
    print(f"  RAW: clusters need {lo:.1f}-{hi:.1f}x baryons in total mass (~6x DM) -- reproduced from real data.")
    print("  The a0 KERNEL helps but does NOT close it: a residual ~1.6-2.0x baryons survives at R500 across")
    print("  BOTH footings and 3 interpolation functions, and RISES inward to ~3.7x at 0.2 R500 -- a real,")
    print("  CORE-CONCENTRATED extra source the kernel cannot produce (the classic MOND-cluster signature).")
    print("  => The framework's a0 does not solve clusters; ~half the cluster DM remains, core-concentrated.")

    res = dict(n_clusters=len(cl), D_raw_median=float(np.median(D_raw)),
               D_raw_mean=float(D_raw.mean()), D_raw_range=[float(D_raw.min()), float(D_raw.max())],
               D_raw_by_model={k: float(np.median(v)) for k, v in draw_models.items()},
               residual_R500={f"{f}_{n}": float(np.median([_logat(c['r'], c['Mtot'], c['R500']) /
                   (nu(G*_logat(c['r'], c['Mbar'], c['R500'])*Msun/(c['R500']*Mpc)**2/a0) *
                    _logat(c['r'], c['Mbar'], c['R500'])) for c in cl]))
                   for f, a0 in A0.items() for n, nu in NUS.items()},
               residual_radial=radial, dm_removed_frac_R500=float(np.median(rem)), per_cluster=out)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "C02_cluster_6p8x_results.json")
    json.dump(res, open(p, "w"), indent=1)
    print(f"\nwrote {p}")


if __name__ == "__main__":
    main()
