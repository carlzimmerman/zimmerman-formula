"""CFG379 POST-FREEZE (labelled; the frozen FAILS stands): C1 failed because the ledger's X-COP 0.576 is CFG4's value at r = 1 Mpc (0.70-0.95 R500),
not at R500 (0.430 here). This re-evaluates the cluster class at r = 1 Mpc from the same FITS files, both footings, both catchments.
Run: python3 cfg379_postfreeze.py (no MUTATE; reported only).
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, "..")); REPO = os.path.abspath(os.path.join(CFG, ".."))
sys.path.insert(0, os.path.join(CFG, "CFG100_kids_mass_rederivation"))
import cfg100_lib as L  # noqa: E402
COSMIC = 5.364; FC_M = COSMIC / (COSMIC + 1); G, A0 = L.G_MPC, L.A0
def nu(y): return float(L.nu_mono(np.array([y]))[0])
S_RC = L.OM * FC_M * L.RHOC0 * (2 * math.pi) ** 1.5 * (3.0 / L.H) ** 3
xdir = os.path.join(REPO, "real_research", "data", "xcop"); r500j = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
cfg4 = {c["name"]: c for c in json.load(open(os.path.join(CFG, "CFG4_clusters_results.json")))["numbers"]["C"]["canonical|nu_mono|b0.0"]}
out, lines = {}, []
def say(s=""): print(s); lines.append(s)
say("CFG379 POST-FREEZE: X-COP at r = 1 Mpc (the ledger's aperture)")
rows = []
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r500j: continue
    R500 = r500j[nm]["R500"] * 1000.0; r = 1000.0; xr = r / R500
    fg = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data; hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    Mg = float(np.exp(np.interp(math.log(xr), np.log(np.asarray(fg["RADIUS"], float)), np.log(np.asarray(fg["MGAS"], float)))))
    msf = os.path.join(d, f"{nm}_mstar.fits")
    if os.path.exists(msf):
        ms = fits.open(msf)["MSTAR_SMOOTHED"].data
        Ms = float(np.exp(np.interp(math.log(r), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    else:
        Ms = 0.10 * Mg
    Mb, Mt = Mg + Ms, float(np.interp(r, np.asarray(hm["RADIUS"], float), np.asarray(hm["M_FORW"], float)))
    row = dict(name=nm, Mb=Mb, Mtot=Mt, fb=Mb / Mt, fb_cfg4=cfg4[nm]["fb"])
    for f in ("canonical", "alt"):
        Mph = (nu(G * Mb / (r / 1000) ** 2 / A0[f]) - 1) * Mb; den = COSMIC * Mb
        rta = L.r_ta_law(Mb, A0[f], 0.0); S_TA = FC_M * Mb * nu(G * Mb / rta ** 2 / A0[f])
        row[f] = dict(r_ph=Mph / den, f_A=(Mt - Mb - Mph) / den, r_tot=(Mt - Mb) / den, r_TA=min(Mph, S_TA) / den, r_RC=min(Mph, S_RC) / den,
                      bind_TA="SUPPLY" if S_TA < Mph else "TARGET", bind_RC="SUPPLY" if S_RC < Mph else "TARGET")
    rows.append(row)
    say(f"  {nm:8s} fb {row['fb']:.3f} (CFG4 {row['fb_cfg4']:.3f})  r_ph {row['canonical']['r_ph']:.3f}|{row['alt']['r_ph']:.3f}  f_A {row['canonical']['f_A']:+.3f}  r_tot {row['canonical']['r_tot']:.3f}  r_RC {row['canonical']['r_RC']:.3f}")
for f in ("canonical", "alt"):
    fa = [r_[f]["f_A"] for r_ in rows]; lo, hi = np.percentile(fa, [16, 84])
    res = {}
    for c in ("r_TA", "r_RC"):
        p = float(np.median([r_[f][c] for r_ in rows])); ok = abs(p - 0.576) <= 0.10 or lo <= p <= hi
        nb = sum(r_[f]["bind_" + c[2:]] == "SUPPLY" for r_ in rows)
        res[c] = dict(pred=p, passes=bool(ok), supply_binds=f"{nb}/{len(rows)}")
    out[f] = dict(f_A_median=float(np.median(fa)), f_A_16_84=[float(lo), float(hi)], r_tot_median=float(np.median([r_[f]["r_tot"] for r_ in rows])), **res)
    say(f"  {f}: measured f_A median {np.median(fa):.3f} (16-84 {lo:.2f}-{hi:.2f}); TA pred {res['r_TA']['pred']:.3f} {'PASS' if res['r_TA']['passes'] else 'fail'} "
        f"(supply binds {res['r_TA']['supply_binds']}); RC pred {res['r_RC']['pred']:.3f} {'PASS' if res['r_RC']['passes'] else 'fail'} (supply binds {res['r_RC']['supply_binds']}); r_tot median {out[f]['r_tot_median']:.3f}")
say("Groups and MW are unchanged (they fail on both catchments), so the lane verdict stays FAILS at either cluster aperture.")
json.dump(dict(rows=rows, summary=out), open(os.path.join(HERE, "cfg379_postfreeze_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg379_postfreeze.out"), "w").write("\n".join(lines) + "\n")
