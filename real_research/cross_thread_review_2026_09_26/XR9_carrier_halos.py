#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR9_carrier_halos.py -- the carrier halos for XR9's small-region door, re-run with each cell's own refitted lens masses.

WHY.  The KiDS gate of the small-region door (XR9_small_region_kids_flagship_shear.py) scores the converged model's
triggered carrier resolved around each KiDS lens, as DE10 did at p = 1, x_c0 = 2.5.  The carrier is L375's shell model:
its infall feels the bin's baryons (Hernquist M_b + the rest of f_b M_200 as an NFW-shaped CGM), so the halo depends on
the cell through the bin's fitted baryonic mass.  DE10 reused L390's masses (refitted on the curvature branch at
x_c,eff(0.25) = 3.2477).  At a higher threshold the best-fit M_b per bin moves; the carrier halo must be re-run with the
new masses, exactly as L390 did at its own cell (rule 3 of the KiDS machinery's owner, 2026-09-26).

WHAT THIS SCRIPT DOES (nothing else; the scoring is the main XR9 script's):
  1. THE REFIT, L390's recipe on the scored switch.  For every XR9 cell (p in {1, 1.5}, x_c0 in {2.5, 3.5, 5, 7, 10, 14,
     20}) the four KiDS bins' baryonic masses are refitted on the model being scored: DE8's region operator (sigma = 1,
     1/m = 0.1 Mpc, loaded unedited), the MOND-sector reading x = 4 pi G (rho_b + rho_ph - f_b rho_bar_m)/H^2 (MS2's
     door, carrier-blind), MS3's local cap (v_cap = 325 km/s), the smooth gate at w = 0.25, x_c,eff(0.25) = x_c0 E^(2p)
     (L359's background), switch only, canonical footing, the free 2-halo amplitude A in [0, 20] (L352's fit_model, as
     L390 ran it).  M_b per bin = the best grid mass (L352's LM grid, 0.1 dex) of that fit.
  2. THE HALOS.  L375's halo() imported unchanged; each distinct (bin, M_b, kick) is run once with L390/DE10's seed rule
     seed = 1200 + 10 b + int(v_k)//25 (the same seed at every mass, so the mass effect is not Monte-Carlo noise), alpha =
     0.75, Gamma = 10 H, grow_b = True, N = 60000 -- DE10's configuration exactly.  DE10's own eight halos (L390's masses,
     v_k = 600 and 650) are in the list, for the main script's control.
  3. THE CACHE.  Each halo's radial histogram (L375's 240 edges to 20 Mpc: the carrier's own infall region is kept, no
     r_200 truncation) is written to XR9_carrier_halos_results.json after EVERY halo, so the run can be split: each call
     runs at most XR9_MAXN (default 6) missing halos, single-threaded (~70 s each on the loaded machine), and exits.
     Re-run until it reports "all halos present".
CHECKS
  P1 (reported) the refitted masses per cell; P2 (reported) whether the p = 1, x_c0 = 2.5 refit on the MOND-sector switch
  equals L390's curvature-branch masses (if not, the main script's control uses L390's and its scan row uses the refit).
  H1 (on completion) every planned halo is present and each conserves its particle count (n within 1% of N).
No MUTATE: this script only produces inputs (the main script's MUTATE switches the carrier's lensing off).

Run from the repository root (repeat until complete):
    XR9_MAXN=6 python3 real_research/cross_thread_review_2026_09_26/XR9_carrier_halos.py
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
sys.path.insert(0, DS)
from L375_triggered_carrier_galaxy_retention import halo, M200_BINS   # noqa: E402  (L375's shell model, unchanged)

SLUG = "XR9_carrier_halos"
CACHE = os.path.join(HERE, SLUG + "_results.json")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
PS = (1.0, 1.5)
XC0S = (2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0)
VK = (600.0, 650.0)
W_REFIT = 0.25
V_CAP = 325e3
NPART = 60000
MAXN = int(os.environ.get("XR9_MAXN", "6"))
E2G = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                     # L359's gate background (DE1-DE10)

if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    # ------------------------------------------------------------------------------ DE8's operator and fit, unedited
    P8 = os.path.join(DEDIR, "DE8_kids_sigma_axis_both_branches.py")
    D8 = {"__name__": "de8", "__file__": P8}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P8).read().split("# ============================================================================================ C1 C2 C3 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
    (solve_region, esd_from_mlens, Wg, rr, nu_vec, G, MS, A0, KPC_, Ed, Sd, twoh_cache, LM) = [
        D8[k] for k in ("solve_region", "esd_from_mlens", "Wg", "rr", "nu_vec", "G", "MS", "A0", "KPC_", "Ed", "Sd",
                        "twoh_cache", "LM")]
    FB, rho_bar, H_L = D8["FB"], D8["rho_bar"], D8["H_L"]
    P(f"  DE8 loaded   [{time.time() - T0:.0f}s]")

    def gate_mond(Mb, a0, w, xce):
        """DE10's gate_mond with the threshold as an argument: MS2's door, MS3's local cap, smooth width w."""
        Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
        rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2)
        x = 4 * math.pi * G * (rho - FB * rho_bar) / H_L ** 2
        g = G * Mdyn / rr ** 2
        vloc2 = g ** 2 / np.maximum(4 * math.pi * G * rho, 1e-300)
        scale = np.maximum(1.0, vloc2 / V_CAP ** 2)
        t = (x / (xce * scale) - 1) / (2 * w) + 0.5
        f = Wg(t)
        off = np.where(t <= 0)[0]
        if off.size: f[off[0]:] = 0.0
        return f

    def refit_masses(xce, w=W_REFIT, foot="canonical"):
        """L390's recipe on the scored switch: per bin, the grid mass with the smallest diagonal chi^2, A in [0, 20]."""
        a0 = A0[foot]; out = []
        for b in range(4):
            best = None
            for lm in LM:
                Mb = 10 ** lm * MS
                mk0 = esd_from_mlens(Mb, solve_region(Mb, a0, gate_mond(Mb, a0, w, xce), 100 * KPC_, 1.0), b)
                t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, float(lm))
            out.append(round(best[1], 2))
        return out

    PLAN = {}
    for p in PS:
        for x0 in XC0S:
            xce = x0 * E2G(0.25) ** p
            PLAN[f"p{p:g}_x{x0:g}"] = dict(p=p, xc0=x0, xce_025=xce, lm_refit=refit_masses(xce))
            P(f"    cell p = {p:g}, x_c0 = {x0:4.1f}: x_c,eff(0.25) = {xce:7.3f}; refitted log M_b per bin "
              f"{PLAN[f'p{p:g}_x{x0:g}']['lm_refit']}   [{time.time() - T0:.0f}s]")
    R90 = json.load(open(os.path.join(DS, "L390_kids_resolved_linear_gate_results.json")))["numbers"]
    MB90 = R90["M_b"]["p=1, x_c0=2.5"]
    lm90 = [round(math.log10(x), 2) for x in MB90]
    same = PLAN["p1_x2.5"]["lm_refit"] == lm90
    P(f"  P1 (reported) refitted masses above.  P2 (reported): L390's masses at p = 1, x_c0 = 2.5 (curvature branch) = "
      f"{lm90}; the MOND-sector refit there = {PLAN['p1_x2.5']['lm_refit']} -> {'identical' if same else 'DIFFERENT'}")

    # ------------------------------------------------------------------------------ the halo list
    cfgs = {}
    for b in range(4):                                             # DE10's own halos (L390's masses), for the control
        for v in VK:
            cfgs[f"b{b}_lm{lm90[b]:.2f}_v{int(v)}"] = (b, MB90[b], v)
    for k_, c_ in PLAN.items():
        for b in range(4):
            for v in VK:
                tag = f"b{b}_lm{c_['lm_refit'][b]:.2f}_v{int(v)}"
                if tag not in cfgs:
                    cfgs[tag] = (b, 10 ** c_["lm_refit"][b], v)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    cache.setdefault("halos", {})
    cache["plan"] = PLAN; cache["L390_lm"] = lm90; cache["refit_equals_L390_at_p1_x2.5"] = same
    cache["config"] = dict(N=NPART, alpha=0.75, gamma=10.0, grow_b=True, seed_rule="1200 + 10 b + int(v_k)//25", w_refit=W_REFIT,
                           v_cap_kms=V_CAP / 1e3, switch="MOND-sector (MS2 door), DE8 operator sigma = 1, 1/m = 0.1 Mpc")
    missing = [t for t in cfgs if t not in cache["halos"]]
    P(f"  {len(cfgs)} distinct halos planned ({len(cfgs) - len(missing)} already cached, {len(missing)} missing); this call runs "
      f"up to {MAXN}   [{time.time() - T0:.0f}s]")
    json.dump(cache, open(CACHE, "w"), indent=0)
    for tag in missing[:MAXN]:
        b, Mb, v = cfgs[tag]
        t1 = time.time()
        _, d = halo((tag, b, Mb, v, 10.0, 0.75, True, NPART, 1200 + 10 * b + int(v) // 25))
        cache = json.load(open(CACHE))
        cache["halos"][tag] = dict(b=b, Mb=Mb, v_k=v, seed=1200 + 10 * b + int(v) // 25, m=float(d["m"]), n=int(d["n"]),
                                   M_ap=float(d["M_ap"]), M_ap_cold=float(d["M_ap_cold"]), hist=[int(x) for x in d["hist"]],
                                   hist_cold=[int(x) for x in d["hist_cold"]], r200_kpc=float(d["r200"]))
        cache["edges_kpc"] = [float(x) for x in d["edges"]]
        json.dump(cache, open(CACHE, "w"), indent=0)
        P(f"    halo {tag:22s} (M_b {Mb:.3e}, v_k {v:.0f}, seed {1200 + 10 * b + int(v) // 25}): n = {d['n']}, "
          f"M(<0.5 Mpc/h) = {d['M_ap']:.3e} Msun   [{time.time() - t1:.0f}s; total {time.time() - T0:.0f}s]")
    cache = json.load(open(CACHE))
    still = [t for t in cfgs if t not in cache["halos"]]
    if still:
        P(f"\n  {len(still)} halos still missing: re-run this script.   [{time.time() - T0:.0f}s]")
        sys.exit(0)
    okn = all(abs(cache["halos"][t]["n"] / NPART - 1) < 0.01 for t in cfgs)
    P(f"\n  H1 all {len(cfgs)} planned halos present; particle counts within 1% of N: {okn}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if okn else 1)
