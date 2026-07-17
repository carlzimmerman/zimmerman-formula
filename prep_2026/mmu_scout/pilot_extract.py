#!/usr/bin/env python3
"""
pilot_extract.py -- REAL-DATA pilot on MultimodalUniverse/manga (SCOUT lane, N=3 galaxies).

Proves the two extraction pipelines run on genuine MMU MaNGA DAP maps:

  TEST A (directional-EFE kill switch): per-side outer rotation asymmetry from the
    resolved stellar_vel field (template: prep_2026/wallaby_prep/perside_extractor.py),
    PLUS the deep-MOND feasibility gate -- does the IFU footprint reach g_bar < a0?
    Model-light gate on the framework's OWN RAR g_obs=sqrt(g_bar^2+g_bar a0):
    g_bar<a0  <=>  g_obs < sqrt(2) a0.  g_obs = V_c(r_out)^2 / r_out is measured
    directly (deprojected V_c + physical r from DAP spx_ellcoo r_h/kpc).  BOTH a0
    footings: canonical 9.36e-11 (cH_Lambda/Z, rho_DE) and alt 1.13e-10 (cH0, rho_tot).

  TEST B (MG-impossible anisotropy discriminator): resolved stellar_sigma profile,
    V/sigma, and a major-vs-minor LOS-sigma anisotropy proxy (spec:
    prep_2026/mi_closure_pin/CONSEQUENCES.md sec.1 -- d(offset)/d(radial-anisotropy)>0,
    MG-with-same-nu gives exactly 0).  These are PROXIES for a full Jeans/JAM beta;
    the pilot only proves the sigma map + anisotropy proxy extract cleanly on real data.

Geometry is recovered from the DAP maps themselves (no external NSA needed):
  - deprojected in-disk radius  R_ell = SPX_ELLCOO elliptical_radius (arcsec)
  - on-sky azimuth from major axis  phi = SPX_ELLCOO elliptical_azimuth (deg)
  - axis ratio q=b/a from  (R_sky/R_ell)^2 = 1-(1-q^2) sin^2(phi)  least-squares fit
    (R_sky from SPX_SKYCOO on_sky_x/y), inclination cos i = q (thin-disk; q0 flagged).
  - systemic v subtracted as the flux-weighted median of stellar_vel.
  - physical radius from SPX_ELLCOO r_h/kpc.

exit 0 on completion.  No hard-coded verdicts; all numbers computed from the data.
Values are PILOT proof-of-life (N=3, no g_ext vector, no warp/beam budget) -- they
feed NO physics claim.
"""
import os, sys, json, math
import numpy as np
import _mmu

HERE = os.path.dirname(os.path.abspath(__file__))
KPC_M = 3.0856775814913673e19
A0_CANON = 9.36e-11   # m/s^2  cH_Lambda/Z, rho_DE
A0_ALT   = 1.13e-10   # m/s^2  cH0,        rho_tot
DEEP_MOND_GOBS = math.sqrt(2.0)  # g_obs/a0 threshold where g_bar=a0 on the framework nu

# pilot galaxies: (shard, row) -- shard 3 has two 127-fibre bundles (best coverage,
# incl. low-z 10223-12704 at z=0.021); shard 8 is a 61-fibre (12082-6102).
PILOT = [(3, 0), (3, 1), (8, 0)]


def recover_axis_ratio(rsky, rell, phi_deg):
    """(R_sky/R_ell)^2 = 1 - (1-q^2) sin^2 phi  ->  linear fit, robust."""
    ok = np.isfinite(rsky) & np.isfinite(rell) & np.isfinite(phi_deg) & (rell > 1.0)
    if ok.sum() < 30:
        return np.nan
    u = (rsky[ok] / rell[ok]) ** 2
    s = np.sin(np.radians(phi_deg[ok])) ** 2
    # u = a + b s ; slope b = -(1-q^2)
    A = np.vstack([np.ones_like(s), s]).T
    coef, *_ = np.linalg.lstsq(A, u, rcond=None)
    b = coef[1]
    q2 = 1.0 + b
    q = math.sqrt(min(max(q2, 0.04), 1.0))  # clamp [0.2^2 ,1]
    return q


def perside_rotation(g, cos_min=0.5, n_rings=8, outer_frac=0.6):
    """Per-side deprojected rotation curve + signed outer asymmetry + deep-MOND gate."""
    M = g["maps"]
    if "stellar_vel" not in M:
        return None
    v, viv = M["stellar_vel"]
    rell = M["spx_ellcoo_elliptical_radius"][0]
    phi = M["spx_ellcoo_elliptical_azimuth"][0]
    rkpc = M["spx_ellcoo_r_h/kpc"][0]
    sx = M["spx_skycoo_on_sky_x"][0]
    sy = M["spx_skycoo_on_sky_y"][0]
    w = M["spx_mflux"][0] if "spx_mflux" in M else np.ones_like(v)
    rsky = np.hypot(sx, sy)

    valid = np.isfinite(v) & np.isfinite(viv) & (viv > 0) & np.isfinite(rell)
    if valid.sum() < 50:
        return None
    q = recover_axis_ratio(rsky, rell, phi)
    inc = math.degrees(math.acos(q)) if np.isfinite(q) else np.nan
    sini = math.sqrt(max(1 - q * q, 1e-4)) if np.isfinite(q) else np.nan

    ww = np.where(valid & np.isfinite(w) & (w > 0), w, 0.0)
    vsys = float(np.average(v[ww > 0], weights=ww[ww > 0]))
    cphi = np.cos(np.radians(phi))

    wedge = valid & (np.abs(cphi) >= cos_min)
    dv = v - vsys
    vrot = np.full_like(v, np.nan)
    vrot[wedge] = dv[wedge] / (sini * cphi[wedge])

    rmax = np.nanpercentile(rell[valid], 97)
    edges = np.linspace(0, rmax, n_rings + 1)
    curves = []
    for k in range(n_rings):
        sel = wedge & (rell >= edges[k]) & (rell < edges[k + 1])
        row = {"R_as": 0.5 * (edges[k] + edges[k + 1])}
        for side, m in (("rec", sel & (cphi > 0)), ("app", sel & (cphi < 0))):
            vv = vrot[m]
            wv = np.where(np.isfinite(w[m]) & (w[m] > 0), w[m], 1.0)
            if vv[np.isfinite(vv)].size >= 4:
                fin = np.isfinite(vv)
                row[side] = float(np.average(vv[fin], weights=wv[fin]))
                row[side + "_n"] = int(fin.sum())
                # physical radius (kpc) for this ring, flux-weighted
                rk = rkpc[m]
                fk = np.isfinite(rk)
                row[side + "_rkpc"] = float(np.average(rk[fk])) if fk.any() else np.nan
        curves.append(row)

    r_out_min = outer_frac * rmax
    outer = [c for c in curves if c["R_as"] >= r_out_min and "app" in c and "rec" in c]
    res = {"plateifu": g["plateifu"], "z": g["z"], "q_ba": q, "inc_deg": inc,
           "vsys": vsys, "rmax_as": float(rmax), "curves": curves}
    if outer:
        va = np.mean([c["app"] for c in outer])
        vr = np.mean([c["rec"] for c in outer])
        denom = abs(va) + abs(vr)
        A = 2.0 * (abs(va) - abs(vr)) / denom if denom > 1e-6 else float("nan")
        Vc = 0.5 * denom
        r_out_kpc = np.nanmean([c.get("app_rkpc", np.nan) for c in outer] +
                               [c.get("rec_rkpc", np.nan) for c in outer])
        g_obs = (Vc * 1e3) ** 2 / (r_out_kpc * KPC_M) if r_out_kpc > 0 else np.nan
        res.update({"A_outer": float(A), "Vc_outer_kms": float(Vc),
                    "r_out_kpc": float(r_out_kpc),
                    "g_obs_outer": float(g_obs),
                    "g_obs_over_a0_canon": float(g_obs / A0_CANON),
                    "g_obs_over_a0_alt": float(g_obs / A0_ALT),
                    "reaches_deepMOND_canon": bool(g_obs / A0_CANON < DEEP_MOND_GOBS),
                    "reaches_deepMOND_alt": bool(g_obs / A0_ALT < DEEP_MOND_GOBS)})
    return res


def anisotropy_proxy(g, cos_min=0.5):
    """Resolved stellar_sigma profile + V/sigma + major/minor LOS-sigma ratio (proxies)."""
    M = g["maps"]
    if "stellar_sigma" not in M:
        return None
    sig, siv = M["stellar_sigma"]
    # instrumental correction (quadrature) if present
    if "stellar_sigmacorr_fit" in M:
        corr = M["stellar_sigmacorr_fit"][0]
        sig_c = np.sqrt(np.clip(sig ** 2 - corr ** 2, 0, None))
    else:
        sig_c = sig
    rell = M["spx_ellcoo_elliptical_radius"][0]
    rre = M["spx_ellcoo_r/re"][0]
    phi = M["spx_ellcoo_elliptical_azimuth"][0]
    w = M["spx_mflux"][0] if "spx_mflux" in M else np.ones_like(sig)
    v = M["stellar_vel"][0] if "stellar_vel" in M else None

    valid = np.isfinite(sig_c) & np.isfinite(siv) & (siv > 0) & (sig_c > 0)
    if valid.sum() < 50:
        return None
    ww = np.where(valid & np.isfinite(w) & (w > 0), w, 0.0)

    # luminosity-weighted sigma within 1 Re
    inRe = valid & (rre <= 1.0)
    sig_e = float(np.average(sig_c[inRe], weights=np.clip(w[inRe], 0, None))) if inRe.sum() > 10 else np.nan

    # V/sigma (rotational vs pressure support), within 1 Re, flux-weighted
    vsig = np.nan
    if v is not None:
        vsys = float(np.average(v[ww > 0], weights=ww[ww > 0]))
        vv = np.abs(v - vsys)
        num = np.sum(w[inRe] * vv[inRe] ** 2)
        den = np.sum(w[inRe] * sig_c[inRe] ** 2)
        vsig = float(math.sqrt(num / den)) if den > 0 else np.nan

    # major-vs-minor LOS sigma anisotropy proxy at matched radius (0.5-1.0 Re annulus)
    cphi = np.cos(np.radians(phi))
    ann = valid & (rre >= 0.5) & (rre <= 1.0)
    maj = ann & (np.abs(cphi) >= 0.87)   # within 30 deg of major axis
    minr = ann & (np.abs(cphi) <= 0.5)   # >60 deg from major axis (near minor)
    sig_maj = float(np.average(sig_c[maj], weights=np.clip(w[maj], 0, None))) if maj.sum() > 8 else np.nan
    sig_min = float(np.average(sig_c[minr], weights=np.clip(w[minr], 0, None))) if minr.sum() > 8 else np.nan
    ratio = sig_maj / sig_min if (np.isfinite(sig_maj) and np.isfinite(sig_min) and sig_min > 0) else np.nan

    # radial sigma gradient (log-log slope) 0.2-1.0 Re -- radial-anisotropy proxy
    prof = ann | (valid & (rre >= 0.2) & (rre < 0.5))
    slope = np.nan
    rr = rre[valid & (rre >= 0.2) & (rre <= 1.2)]
    ss = sig_c[valid & (rre >= 0.2) & (rre <= 1.2)]
    if rr.size > 20:
        b = np.polyfit(np.log10(rr), np.log10(ss), 1)
        slope = float(b[0])

    return {"plateifu": g["plateifu"], "z": g["z"],
            "n_sigma_spaxels": int(valid.sum()),
            "sigma_e_kms": sig_e, "V_over_sigma": vsig,
            "sigma_maj_kms": sig_maj, "sigma_min_kms": sig_min,
            "sigma_maj_over_min": ratio,
            "logsigma_logR_slope": slope}


def main():
    print(__doc__.split("Geometry")[0].strip())
    print("\n" + "=" * 78)
    print("PILOT: real MMU/manga galaxies (N=%d).  Both a0 footings on the deep-MOND gate." % len(PILOT))
    print("  a0_canon = %.3g   a0_alt = %.3g   deep-MOND begins at g_obs/a0 < %.3f" %
          (A0_CANON, A0_ALT, DEEP_MOND_GOBS))
    print("=" * 78)
    outA, outB = [], []
    for shard, row in PILOT:
        try:
            p = _mmu.shard_path(shard, download=True)
        except Exception as e:
            print(f"  [shard {shard}] HF fetch failed: {e} -> skipped")
            continue
        g = _mmu.load_galaxy(p, row)
        print(f"\n--- {g['plateifu']}  (z={g['z']:.4f}) ---")

        rA = perside_rotation(g)
        if rA is None:
            print("  TEST A: no usable stellar_vel wedge -> honest null for this galaxy")
        else:
            print(f"  TEST A  q=b/a={rA['q_ba']:.3f} inc={rA['inc_deg']:.1f}deg vsys={rA['vsys']:+.1f} rmax={rA['rmax_as']:.1f}\"")
            if "A_outer" in rA:
                print(f"    outer: Vc={rA['Vc_outer_kms']:.1f} km/s @ r={rA['r_out_kpc']:.1f} kpc")
                print(f"    signed per-side asymmetry A = {rA['A_outer']:+.4f}  [PILOT]")
                print(f"    g_obs(outer) = {rA['g_obs_outer']:.3e} m/s^2")
                print(f"    g_obs/a0 = {rA['g_obs_over_a0_canon']:.2f} (canon) / {rA['g_obs_over_a0_alt']:.2f} (alt)"
                      f"   deep-MOND<{DEEP_MOND_GOBS:.2f}?  canon={rA['reaches_deepMOND_canon']} alt={rA['reaches_deepMOND_alt']}")
            else:
                print("    outer rings incomplete -> no asymmetry/gate this galaxy")
            outA.append(rA)

        rB = anisotropy_proxy(g)
        if rB is None:
            print("  TEST B: no usable stellar_sigma -> null")
        else:
            print(f"  TEST B  sigma_e={rB['sigma_e_kms']:.1f} km/s  V/sigma={rB['V_over_sigma']:.2f}  "
                  f"sig_maj/min={rB['sigma_maj_over_min']:.3f}  dlnσ/dlnR={rB['logsigma_logR_slope']:+.2f}  "
                  f"({rB['n_sigma_spaxels']} spaxels)")
            outB.append(rB)

    out = {"a0_canon": A0_CANON, "a0_alt": A0_ALT, "deepMOND_gobs_over_a0": DEEP_MOND_GOBS,
           "testA_rotation": outA, "testB_anisotropy": outB}
    with open(os.path.join(HERE, "pilot_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=lambda x: None if (isinstance(x, float) and math.isnan(x)) else x)
    print("\n" + "=" * 78)
    print("PILOT NOTE: N=3 proof-of-life; no g_ext vector, no beam/warp systematics budget.")
    print("  Feeds NO physics claim.  Deep-MOND gate uses the framework's own RAR mapping.")
    print(f"  results: {os.path.join(HERE, 'pilot_results.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
