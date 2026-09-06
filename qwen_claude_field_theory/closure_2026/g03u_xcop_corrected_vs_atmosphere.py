#!/usr/bin/env python3
"""
g03u -- the corrected X-COP profile (the lead's 2026-09-06 audit) against the dust atmosphere
===============================================================================================
The lead's cluster audit (cluster_measurement_audit_2026/) found that hunt_2026/h67b_xcop_core_eta.py read the gas profile's
RADIUS column as Mpc when it is R/R500, and recomputed the hydrostatic and baryonic accelerations of the twelve X-COP clusters at
the correct radii (results.json, 'rows': g_hse/a0, g_baryon/a0 per cluster and radius, both footings).  Every X-COP residual used
in g03q/g03r/g03s inherited the error.  Here the corrected rows are compared with the candidate's converged dust structure
(g03r's self-gravitating hydrostatic atmosphere, rho_d ~ exp(-r/H)/g, H = 0.42 e c^2/(|K_2| a0)), with ONE kernel law on both
sides at a time:

  needed dust:   M_d,req(<r)/M_b(<r) = mu(y_H) M_H/M_b - 1  with M_H = g_H r^2/G, M_b = g_b r^2/G, y_H = g_H/a0, for
                 (a) the exact exponential law mu = 1 - exp(-y) and (b) the g03j carrier law (exponential to y_t = 1, then the
                 saturated branch), medians over the twelve clusters (and over the seven with measured stellar profiles);
  model dust:    the atmosphere in the well of the MEDIAN corrected baryon profile M_b(<r) itself (not a model cluster),
                 normalised by the cold infall of g03r (Newtonian growth), g03s (the derived causal law, beta = 1.19) and g03r
                 (MOND-peculiar growth), scanned in |K_2|, both footings.

Checks that can fail:
  U1 [reported]  the corrected required-source profile is NOT core-heavy: the median M_d,req/M_b at 40 kpc and at 1 Mpc are both
                 below its peak (100-300 kpc) by more than 20% (the 'core-heavy residual' of THE_ACTION section 5.8 is withdrawn if so);
  U2 [law]       the exponential and carrier laws give required profiles within 0.05 dex rms of each other over 40-1000 kpc;
  U3 [reported]  some normalisation reproduces the corrected M_d,req/M_b within 0.15 dex rms over 40-1000 kpc at both footings;
  U3b [reported] the Newtonian-growth atmosphere matches the amplitude over 75-420 kpc within 0.15 dex rms;
  U4 [reported]  that best |K_2| lies inside the KiDS/cluster window of the same growth model (g03r: [5e4, 5e5] Newtonian;
                 g03s: [5e4, 2e5] derived law);  U4b: the peak radii agree within a factor 3;
  U5 [pincer]    that best |K_2| is below the linear-growth floor 2.7e6 of g03t -- reported: if U3-U4 pass while U5's floor
                 stands, the cluster fit and the cosmology cannot share a K_2.
"""
import numpy as np, math, json, sys, time, importlib.util
spec = importlib.util.spec_from_file_location("g03r", "g03r_converged_collapse_adaptive_shells.py"); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
spec2 = importlib.util.spec_from_file_location("g03s", "g03s_dust_growth_law.py"); Sx = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(Sx)
G, c, MSUN, kpc, Mpc, A0 = R.G, R.c, R.MSUN, R.kpc, R.Mpc, R.A0
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
T0 = time.time()
rows = json.load(open("cluster_measurement_audit_2026/results.json"))["rows"]
RADII = np.array([40, 50, 75, 100, 150, 200, 300, 420, 750, 1000], float)                             # 30 kpc has 4 clusters after the fix: excluded
def mu_exp(y): return 1 - np.exp(-y)
def mu_carrier(y):                                                                                   # g_N/g_tot for the g03j carrier: exponential below y_t = 1, saturated (g_psi = a0/e) above
    return np.where(y <= 1, 1 - np.exp(-y), 1 - 1/(math.e*np.maximum(y, 1e-30)))
NEED = {}; MB = {}
print("=" * 110); print("g03u -- the corrected X-COP profile against the dust atmosphere"); print("=" * 110, flush=True)
for foot, a0 in A0.items():
    for subset in ("all", "stellar"):
        need_e, need_c, mb = [], [], []
        for rk in RADII:
            R_ = [r for r in rows if r["footing"] == foot and r["r_kpc"] == rk and (subset == "all" or r["stellar_file_present"])]
            yH = np.array([r["g_hse_over_a0"] for r in R_]); yb = np.array([r["g_baryon_over_a0"] for r in R_])
            need_e.append(np.median(mu_exp(yH)*yH/yb - 1)); need_c.append(np.median(mu_carrier(yH)*yH/yb - 1)); mb.append(np.median(yb*a0*(rk*kpc)**2/G))
        NEED[(foot, subset, "exp")] = np.array(need_e); NEED[(foot, subset, "carrier")] = np.array(need_c); MB[(foot, subset)] = np.array(mb)
    print(f"  {foot}: corrected required M_d/M_b (exponential law), all twelve: {np.round(NEED[(foot, 'all', 'exp')], 2).tolist()} at r = {RADII.astype(int).tolist()} kpc", flush=True)
    print(f"  {foot}: same, seven with stellar profiles:                 {np.round(NEED[(foot, 'stellar', 'exp')], 2).tolist()}", flush=True)
    print(f"  {foot}: carrier law, all twelve:                            {np.round(NEED[(foot, 'all', 'carrier')], 2).tolist()}", flush=True)
    print(f"  {foot}: median M_b(<r) [1e12 Msun]:                         {np.round(MB[(foot, 'all')]/1e12/MSUN, 2).tolist()}", flush=True)
ne = NEED[("canonical", "all", "exp")]; ipk = int(np.argmax(ne))
check("U1 [reported] the corrected required-source profile is not core-heavy: M_d,req/M_b at 40 kpc and at 1 Mpc are both > 20% below its peak", ne[0] < 0.8*ne[ipk] and ne[-1] < 0.8*ne[ipk], f"40 kpc {ne[0]:.2f}, peak {ne[ipk]:.2f} at {RADII[ipk]:.0f} kpc, 1 Mpc {ne[-1]:.2f}")
rmsl = float(np.sqrt(np.mean((np.log10(NEED[("canonical", "all", "exp")]) - np.log10(NEED[("canonical", "all", "carrier")]))**2)))
check("U2 [law] the exponential and carrier laws give required profiles within 0.05 dex rms of each other over 40-1000 kpc", rmsl < 0.05, f"rms {rmsl:.3f} dex")
# ---- the well: the median corrected baryon profile, used by the atmosphere through R.baryon_M ----
def make_well(foot):
    rr = RADII*kpc; mb = MB[(foot, "all")]; lr, lm = np.log(rr), np.log(mb)
    s_in = (lm[1] - lm[0])/(lr[1] - lr[0]); s_out = (lm[-1] - lm[-2])/(lr[-1] - lr[-2])
    def Mb_of(r, Mb, kind):
        r = np.asarray(r, float); out = np.exp(np.interp(np.log(np.clip(r, rr[0], rr[-1])), lr, lm))
        out = np.where(r < rr[0], mb[0]*(r/rr[0])**s_in, out); out = np.where(r > rr[-1], mb[-1]*(r/rr[-1])**s_out, out); return out
    return Mb_of
# ---- normalisations: the cold infall of the three growth models (turned-around mass and r_ta), both footings ----
print("  cold infall normalisations (cluster, z_c = 0.3):", flush=True)
NORM = {}
for foot, a0 in A0.items():
    oN = R.run("cluster", 1e30, N=800, newton=True, cs_fixed=0.0, a0=a0); oM = R.run("cluster", 1e30, N=800, cs_fixed=0.0, a0=a0)
    Sx.BETA = 1.19; oD = Sx.run_dyn("cluster", 2.5e5, growth="dynamic", N=400, a0=a0)
    NORM[(foot, "Newtonian growth (g03r)")] = (oN["Macc"], oN["r_ta"]); NORM[(foot, "derived causal law (g03s)")] = (oD["Macc"], oD["r_ta"]); NORM[(foot, "MOND-peculiar growth (g03r)")] = (oM["Macc"], oM["r_ta"])
    print(f"    {foot}: turned-around mass / share: Newtonian {oN['Macc']/oN['Mshare']:.3f}, derived {oD['Macc']/oD['Mshare']:.3f}, MOND-peculiar {oM['Macc']/oM['Mshare']:.3f}; r_ta {oN['r_ta']/Mpc:.1f}, {oD['r_ta']/Mpc:.1f}, {oM['r_ta']/Mpc:.1f} Mpc  ({time.time()-T0:.0f}s)", flush=True)
# ---- the scan ----
WINDOW = {"Newtonian growth (g03r)": (5e4, 5e5), "derived causal law (g03s)": (5e4, 2e5), "MOND-peculiar growth (g03r)": (5e4, 2e5)}
K2S = np.geomspace(3e4, 3e6, 25); BEST = {}
for foot, a0 in A0.items():
    R.baryon_M = make_well(foot); Mb_r = MB[(foot, "all")]
    for growth in WINDOW:
        Macc, r_ta = NORM[(foot, growth)]; best = None
        for K2 in K2S:
            ac = R.atmosphere("cluster", K2, Macc, max(r_ta, 3*Mpc), a0=a0, ngrid=600); Md_r = np.interp(RADII*kpc, ac["r"], ac["Md"])
            ratio = Md_r/Mb_r; need = NEED[(foot, "all", "exp")]
            rms = float(np.sqrt(np.mean((np.log10(np.maximum(ratio, 1e-6)) - np.log10(need))**2)))
            trend_m = float(np.polyfit(np.log10(RADII), np.log10(np.maximum(ratio, 1e-6)), 1)[0]); trend_d = float(np.polyfit(np.log10(RADII), np.log10(need), 1)[0])
            if best is None or rms < best[1]: best = (K2, rms, ratio, trend_m, trend_d, ac["H"])
        BEST[(foot, growth)] = best
        print(f"  {foot:9s} {growth:28s}: best |K_2| = {best[0]:.2e} (H = {best[5]/kpc:.0f} kpc), rms {best[1]:.3f} dex, trend model {best[3]:+.2f} vs data {best[4]:+.2f}; window {WINDOW[growth]}", flush=True)
        print(f"            model M_d/M_b at 40..1000 kpc: {np.round(best[2], 2).tolist()}", flush=True)
        print(f"            needed (exp law):             {np.round(NEED[(foot, 'all', 'exp')], 2).tolist()}", flush=True)
ok3 = {gr: all(BEST[(f, gr)][1] < 0.15 for f in A0) for gr in WINDOW}
check("U3 [reported] some normalisation reproduces the corrected M_d,req/M_b within 0.15 dex rms over 40-1000 kpc at both footings", any(ok3.values()), json.dumps({gr: [round(BEST[(f, gr)][1], 3) for f in A0] for gr in WINDOW}))
sel = (RADII >= 75) & (RADII <= 420)
ok3b = {gr: all(float(np.sqrt(np.mean((np.log10(BEST[(f, gr)][2][sel]) - np.log10(NEED[(f, 'all', 'exp')][sel]))**2))) < 0.15 for f in A0) for gr in WINDOW}
check("U3b [reported] the Newtonian-growth atmosphere at its best |K_2| matches the corrected profile's amplitude over 75-420 kpc within 0.15 dex rms at both footings (the mismatch is confined to r < 50 kpc, where the model is low, and r > 750 kpc, where it is high)", ok3b["Newtonian growth (g03r)"], json.dumps({gr: [round(float(np.sqrt(np.mean((np.log10(BEST[(f, gr)][2][sel]) - np.log10(NEED[(f, 'all', 'exp')][sel]))**2))), 3) for f in A0] for gr in WINDOW}))
ok4 = {gr: all(WINDOW[gr][0] <= BEST[(f, gr)][0] <= WINDOW[gr][1] for f in A0) for gr in WINDOW}
check("U4 [reported] the best |K_2| lies inside the KiDS/cluster window of the same growth model at both footings", any(ok4.values()), json.dumps({gr: [f"{BEST[(f, gr)][0]:.1e}" for f in A0] for gr in WINDOW}))
ipm = {f: RADII[int(np.argmax(BEST[(f, 'Newtonian growth (g03r)')][2]))] for f in A0}; ipd = {f: RADII[int(np.argmax(NEED[(f, 'all', 'exp')]))] for f in A0}
check("U4b [reported] the model's peak radius of M_d/M_b (Newtonian growth, best K_2) lies within a factor 3 of the data's at both footings", all(ipm[f]/ipd[f] < 3 and ipd[f]/ipm[f] < 3 for f in A0), f"model peaks {ipm}, data peaks {ipd} kpc")
check("U5 [pincer, reported] the best |K_2| of every normalisation is below g03t's linear-growth floor 2.7e6 (so the cluster fit and the cosmology cannot share a K_2 while that floor stands)", all(BEST[(f, gr)][0] < 2.7e6 for f in A0 for gr in WINDOW), "")
print(f"\n  caveats: medians of a heterogeneous sample against one spherical atmosphere in the median well; the assembly history and the infall normalisations are the g03r/g03s models; the 30-kpc point is dropped (four clusters after the fix); no covariance; the lead's audit rows are used as given (its own caveats apply: tabulated reconstructions, HSE).  total {time.time()-T0:.0f}s")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(1 if FAILS else 0)
