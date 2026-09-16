#!/usr/bin/env python3
"""M01_equipartition.py — THE EQUIPARTITION + GAUSS FLUX on real SPARC
baryonic masses, both a0 footings. Companion to lean/M01_equipartition.lean
(certified: rM_sq, equipartition, gauss_flux, surface_density).

Physical claims (registered in the repo):
  r_M      = sqrt(G M_b / a0)                          one boundary
  M_ph(<r) = sqrt(G M_b a0) * r / G                    Gauss-map phantom mass
  equipartition: M_ph(<r_M) = M_b EXACTLY              G03G (2e-16), G090
  surface density: M_b/(pi r_M^2) = a0/(pi G) = 213.74 Msun/pc^2   G083/H037

M_b from the REPO convention (real_research/framework_a0_law_of_nature.py):
  Mstar = Upsilon_* * L36 * 1e9 Msun,  Upsilon_* = 0.5 (UPS_D)
  Mgas  = 1.33 * MHI * 1e9 Msun                        (1.33 = He+metals)
  M_b   = (0.5*L36 + 1.33*MHI) * 1e9 Msun,  Msun = 1.98892e30 kg

Checks (measurement and threshold printed separately; no literal True):
  V1  |M_ph(r_M)/M_b - 1| < 1e-9 on every sampled galaxy, both footings
      (the equipartition identity IS exact algebra; the residual is float)
  V2  residual mean and max over the sample reported per footing
  V3  Sigma_bar(<r_M) = a0/(pi G) in Msun/pc^2 within 1e-6 relative
  V4  slope of log M_ph vs log M_b = 1.000 within 1e-9 (mass linearity)
"""
import csv, json, math

G = 6.67430e-11        # m^3 kg^-1 s^-2
MSUN = 1.98892e30      # kg
KPC = 3.0857e19        # m
PC = 3.0857e16         # m
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m/s^2, repo footings
UPS, HE = 0.5, 1.33    # repo convention: M/L_3.6 disk, He correction

def M_ph_b(rM, Mb, a0):
    """sqrt(G Mb a0) * r_M / G — the Gauss-map phantom enclosed mass."""
    return math.sqrt(G * Mb * a0) * rM / G

def main():
    rows = list(csv.DictReader(open("real_research/data/sparc_master_clean.csv")))
    # keep rows with usable L36/MHI; sample up to 20 spread over the mass range
    usable = [(r["name"], float(r["L36"]), float(r["MHI"])) for r in rows
              if r["L36"] and r["MHI"] and float(r["L36"]) > 0]
    # deterministic spread: sort by log-Mb then take every k-th to span the range
    def Mb_of(L36, MHI): return (UPS * L36 + HE * MHI) * 1e9 * MSUN
    usable.sort(key=lambda t: math.log10(Mb_of(t[1], t[2])))
    k = max(1, len(usable) // 20)
    sample = usable[::k][:20]
    if len(sample) < 20:
        sample = usable  # fewer rows: take all

    checks = []
    for tag, a0 in A0.items():
        resids = []
        sbar_resids = []
        for name, L36, MHI in sample:
            Mb = Mb_of(L36, MHI)
            rM = math.sqrt(G * Mb / a0)                 # m
            Mph = M_ph_b(rM, Mb, a0)                    # kg
            resid = Mph / Mb - 1.0
            resids.append(abs(resid))
            # Sigma_bar(<r_M) in Msun/pc^2 — compare to a0/(pi G) in kg/m^2
            # converted: a0*PC^2/(pi G MSUN) [Msun/pc^2]
            sbar = Mb / (math.pi * (rM / PC) ** 2) / MSUN
            sbar_ref = a0 * PC ** 2 / (math.pi * G * MSUN)
            sbar_resids.append(abs(sbar / sbar_ref - 1.0))
        maxr = max(resids); meanr = sum(resids) / len(resids)
        maxs = max(sbar_resids)
        ok1 = maxr < 1e-9
        ok3 = maxs < 1e-6
        # V4: log M_ph vs log M_b slope (mass linearity) — fit over sample
        xm = [math.log10(Mb_of(L36, MHI)) for _, L36, MHI in sample]
        ym = [math.log10(M_ph_b(math.sqrt(G * Mb_of(L36, MHI) / a0),
                                Mb_of(L36, MHI), a0)) for _, L36, MHI in sample]
        n = len(xm); sx = sum(xm); sy = sum(ym)
        sxx = sum(x * x for x in xm); sxy = sum(a * b for a, b in zip(xm, ym))
        slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
        ok4 = abs(slope - 1.0) < 1e-9
        checks.append(dict(footing=tag, n=len(sample),
                           max_resid_equipartition=maxr,
                           mean_resid_equipartition=meanr,
                           max_resid_surf_density=maxs,
                           slope_logMph_logMb=slope,
                           V1_pass=bool(ok1), V3_pass=bool(ok3), V4_pass=bool(ok4)))
        print(f"[{tag}] n={len(sample)}  max|M_ph/M_b - 1| = {maxr:.3e} "
              f"(thr 1e-9 {'PASS' if ok1 else 'FAIL'})", flush=True)
        print(f"[{tag}] mean residual = {meanr:.3e}   "
              f"max|Sigma_bar/(a0/piG) - 1| = {maxs:.3e} "
              f"(thr 1e-6 {'PASS' if ok3 else 'FAIL'})", flush=True)
        print(f"[{tag}] slope log(M_ph) vs log(M_b) = {slope:.12f} "
              f"(thr |.-1|<1e-9 {'PASS' if ok4 else 'FAIL'})", flush=True)

    # V2: both-footing summary
    ok_all = all(c["V1_pass"] and c["V3_pass"] and c["V4_pass"] for c in checks)
    print(f"\nV2 summary: {sum(1 for c in checks if c['V1_pass'])}/{len(checks)} "
          f"footings V1-clean; all-of {ok_all}", flush=True)

    out = dict(lane="M01_equipartition", n_clusters=0, a0=A0,
               convention=dict(Upsilon_star=UPS, He=HE, source=
                   "real_research/framework_a0_law_of_nature.py"),
               sample=[dict(name=n, L36=l, MHI=m) for n, l, m in sample],
               checks=checks, verdict="PASS" if ok_all else "FAIL")
    with open("deepseek_moa/M01_equipartition.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nM01 COMPLETE: verdict {out['verdict']} — written "
          f"deepseek_moa/M01_equipartition.json", flush=True)

if __name__ == "__main__":
    main()