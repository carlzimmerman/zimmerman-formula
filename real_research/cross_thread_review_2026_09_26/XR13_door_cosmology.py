#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR13_door_cosmology.py -- THE PER-OBJECT DOOR, part 3 of 3: what the door costs where clusters and groups lose their MOND
regions (part (2): no region above v_cap), and what it leaves alone -- (e) KiDS, (f) cosmic shear on MS3/MS4's halo model,
(g) X-COP with L388's retention, (h) Harvey and El Gordo, (i) the 2e13 groups of hunt item 7.  Independent cross-thread
review (2026-09-26/27).  Read-only on every committed file: MS4's machinery is loaded exactly as XR9_cosmic_shear.py loads
it (MS4's main never run); L321's X-COP loader and observable are reimplemented and checked against L354's committed rows;
hunt item 7's group computation is reimplemented and checked against its committed medians; L370's and XR9's committed
results are read.

THE DOOR (XR13_door_environment.py has the full statement).  Part (2): a system whose baryons exceed M_cap = v_cap^4/(G a0)
(8.98e11 / 7.45e11 Msun) has no MOND region; its member galaxies are regions of their own.

THE GATES (definitions fixed before scoring; the model's cell p = 1, x_c0 = 2.5, w = 0.25; both footings).
  (f) SHEAR   MS4's R(k) (L363's halo model at z = 0.5, the MOND-sector door variable, L388's retention at 600 km/s, MS5's
              kappa cap at 1.75 Mpc).  Door: halos whose observed bound baryons (GP0) exceed M_cap carry no halo phantom; the
              bracket's upper end gives them their central galaxy's own phantom (Moster+13 stars + cold gas, if below M_cap).
              Gate: XR9's gate-table reading 0.8 <= R <= 1.2 over k = 0.1-1 h/Mpc on both footings; MS3/MS4's one-sided
              R <= 1.2 reported beside it.
  (g) X-COP   L321/L354's observable on the 12 X-COP clusters: M_dyn(R500)/M_HSE with the retained carrier eps x (1 - f_b)
              x the cluster's NFW; M* (additive: nu_mono on the baryons + the carrier) against the door (no region: baryons
              + carrier, Newtonian).  Two-sided rule after 6% non-thermal support: 0.8 <= ratio <= 1.2, i.e. eps in
              [eps_lo, eps_hi] (L366's eps_bounds).  The window: the kicks in 575-650 km/s whose L388 retention lies in the
              bounds -- L388's own statistic (median over halos >= 1e14 Msun/h) and, per mass bin, its top bin (every X-COP
              cluster has M(<1 Mpc/h) >= 5e14).
  (h) MERGERS  L370's own kernel-off run (MUTATE: nu = 1, real mass = lensing mass) is the door's cluster physics exactly;
              its committed El Gordo and Harvey numbers are read beside L370's main run.
  (i) GROUPS  hunt item 7's 20 Lovisari X-ray groups (2-14e13 Msun) at R500: the carrier retention each needs, M* (the
              group's own MOND region) against the door (no group region: the baryons, plus the central galaxy's own phantom
              if it is below M_cap -- M_BGG = 0.3-0.6 of the SHMR stars -- or nothing); against L388's retention at those
              masses (its lowest bin, 6e13-1e14 in M(<1 Mpc/h), is an upper bound for the lighter groups).  Gate: the same
              two-sided 20% rule as X-COP on the median group, at some kick in 575-650 km/s.
  (e) KiDS    the committed score (XR9 at the cell, DE10) and whether the door changes any input of that model.  Scoped: the
              satellites a real lens carries have their own watershed basins (cones behind them), which the model has not got;
              the phantom-flux fraction they would take is estimated from the Milky Way's own satellites.

CHECKS
  C1 CONTROL: MS4's committed worst R at the cell (capped 1.75 Mpc: 1.0491/1.1243) is reproduced exactly (1e-12).
  C2 CONTROL: L354's committed X-COP rows (median M_dyn/M_HSE at each committed eps, both footings, every f_d) are reproduced
     from the X-COP data with L321's formula (1e-9), and L366's eps bounds (0.2863 / 0.7679) from them.
  C3 CONTROL: hunt item 7's eta(R500) medians are reproduced: canonical 1.80-2.11, alt 1.54-1.81.
  D5 [load-bearing; MUTATE must fail] in the scored halo model no halo above M_cap carries a halo phantom.
  D6 [load-bearing; MUTATE must fail] the scored X-COP observable carries no MOND term.
  G5 (reported) (f) shear passes (two-sided) with the door.   G6 (reported) (g) X-COP has a window with the door.
  G7 (reported) (i) the groups pass with the door.   G8 (reported) (e) KiDS unchanged.   G9 (reported) (h) L370's kernel-off run.
MUTATE=1 merges the regions again (the scored columns are M*'s): D5 and D6 must FAIL (rc = 1).

SCOPE.  MS3/MS4's halo model (isolated regions per halo, one lens epoch, P(k)); L321's one-number X-COP observable at R500
and L388's retention measured in 1 Mpc/h spheres in three 100 Mpc/h boxes.  L388's boxes ran with the cluster phantoms on;
the carrier feels only the Newtonian potential of all matter (L353/L361), so removing them moves its retention only through
the baryons' response -- second order, not re-run.  The groups' stellar masses come from an SHMR (h7's bracket); the BGG share
is declared.  The satellite-basin estimate uses the Milky Way's own census as a template lens, far-field cones scaled to
host-centric radius, and each satellite's own edge scaled from the Local Group's.  The door has no action.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR13_door_cosmology.py   (MUTATE=1)
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MSDIR = os.path.join(REPO, "real_research", "mond_sector_gate_2026")
DSDIR = os.path.join(REPO, "real_research", "dark_sector_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
DOOR = not MUTATE
SLUG = "XR13_door_cosmology"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR13 part 3 (clusters and groups lose their regions: shear, X-COP, mergers, groups, KiDS)",
               "mutate": MUTATE, "door_in_scored_column": DOOR, "checks": {}, "numbers": {}}
V_CAP = 325e3
W = 0.25
NT = 0.06
TAGS = ("v575", "v600", "v625", "v650")


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the regions are merged again (M*'s halo phantoms and X-COP observable scored); D5, D6 must FAIL ***")
    L388 = json.load(open(os.path.join(DSDIR, "L388_linear_gate_pooled_results.json")))["numbers"]

    # ============================================================================================ (f) cosmic shear
    banner("(f) COSMIC SHEAR on MS3/MS4's halo model: M*'s halo phantoms against the door's (none above M_cap)")
    p4 = os.path.join(MSDIR, "MS4_smooth_gate_shear.py")
    M4 = {"__name__": "ms4", "__file__": p4}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(p4).read().split('banner("C1  CONTROL: a near-sharp gate')[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M4)
    GP0, KC, RHO, PNL, PLIN, h, ZS = (M4[k_] for k_ in ("GP0", "KC", "RHO", "PNL", "PLIN", "h", "ZS"))
    G, MS, A0, I1, nfw_uk = (M4[k_] for k_ in ("G", "MS", "A0", "I1", "nfw_uk"))
    FB, dn, bh, LMH, dlnM, XLIN, KG = (M4[k_] for k_ in ("FB", "dn", "bh", "LMH", "dlnM", "XLIN", "KG"))
    ret_L388, tsm = M4["ret_L388"], M4["transform_smooth"]
    MS4R = json.load(open(os.path.join(MSDIR, "MS4_smooth_gate_shear_results.json")))["numbers"]["table"]
    M_CAP = {f: V_CAP ** 4 / (G * a0) / MS for f, a0 in A0.items()}
    P(f"  MS4/MS3/L363 loaded (main not run): z = {ZS}, x_lin = {XLIN:.4f}; M_cap = {M_CAP['canonical']:.3e} / {M_CAP['alt']:.3e} Msun   "
      f"[{time.time() - T0:.0f}s]")

    def R_full(xc, a0, rcap, w, mode="Mstar", mcap=None, ret=ret_L388):
        """MS4's R_smooth line for line, returning R(k) at every gated k (XR9's R_full); mode 'door': halos with observed bound
        baryons above mcap carry no halo phantom; 'door+central': they carry their central galaxy's own phantom instead (if
        that galaxy is below mcap).  Also returns the phantom power from halos above mcap (for D5)."""
        P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC); Pabove = 0.0
        for lm in LMH:
            M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
            Mb = float(GP0.M_bound(M, ZS, "observed"))
            if mode != "Mstar" and Mb > mcap:
                Mc = float(GP0.moster_Mstar(M, ZS)); Mc = Mc + float(GP0.cold_gas(np.array(Mc)))
                tr = tsm(M, Mc, xc, a0, rcap, w) if (mode == "door+central" and Mc <= mcap) else np.zeros_like(KC)
            else:
                tr = tsm(M, Mb, xc, a0, rcap, w)
            if mcap is not None and Mb > mcap:
                Pabove += float(np.max(n * tr ** 2 * dlnM / RHO ** 2))
            uk = nfw_uk(M, KC)
            P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
            fr = ret(M); mass_1h = (FB + (1 - FB) * fr) * M
            rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
            X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
        R = (PNL - rm + 2 * (X1 + I1 * B * PLIN) + P1 + B ** 2 * PLIN) / PNL
        return {q: float(np.interp(math.log(q * h), np.log(KC), R)) for q in KG}, Pabove

    SH = {}
    for f, a0 in A0.items():
        for mode in ("Mstar", "door", "door+central"):
            Rk, Pab = R_full(XLIN, a0, 1.75, W, mode=mode, mcap=M_CAP[f])
            SH[f"{f}/{mode}"] = dict(R_k=Rk, max=max(Rk.values()), min=min(Rk.values()), phantom_power_above_Mcap=Pab)
    d1 = max(abs(SH[f"{f}/Mstar"]["max"] - MS4R["0.25/2.5/1.75"][f]) for f in A0)
    check("C1 CONTROL: MS4's committed worst R at the cell (w = 0.25, x_c0 = 2.5, capped at 1.75 Mpc) is reproduced exactly with "
          "the door off", f"{SH['canonical/Mstar']['max']:.6f} / {SH['alt/Mstar']['max']:.6f} vs {MS4R['0.25/2.5/1.75']['canonical']:.6f} / "
          f"{MS4R['0.25/2.5/1.75']['alt']:.6f} (max |diff| {d1:.1e})", d1 < 1e-12)
    for k_, v_ in SH.items():
        P(f"    {k_:24s}: R(k) " + " ".join(f"{q}:{r_:.3f}" for q, r_ in v_["R_k"].items()) + f"  -> max {v_['max']:.3f}, min {v_['min']:.3f}")
    MB_OBS = {lm: float(GP0.M_bound(10 ** lm, ZS, "observed")) for lm in (12.5, 13.0, 13.2, 13.3, 13.5, 14.0)}
    lm_cut = {f: float(np.interp(math.log10(M_CAP[f]), [math.log10(v_) for v_ in MB_OBS.values()], list(MB_OBS.keys()))) for f in A0}
    P(f"    halos lose their phantom above M = 10^{lm_cut['canonical']:.2f} / 10^{lm_cut['alt']:.2f} Msun (observed bound baryons = M_cap at z = 0.5)")
    scored = "door" if DOOR else "Mstar"
    pab = max(SH[f"{f}/{scored}"]["phantom_power_above_Mcap"] for f in A0)
    check("D5 THE DOOR REMOVES THE CLUSTER PHANTOMS FROM THE SHEAR MODEL: in the scored configuration no halo above M_cap carries a "
          "halo phantom (its largest one-halo phantom power over k) -- MUTATE (regions merged: M*) must fail", f"{pab:.3e}", pab == 0.0)
    two = {m_: all(0.8 <= SH[f"{f}/{m_}"]["min"] and SH[f"{f}/{m_}"]["max"] <= 1.2 for f in A0) for m_ in ("Mstar", "door", "door+central")}
    one = {m_: all(SH[f"{f}/{m_}"]["max"] <= 1.2 for f in A0) for m_ in ("Mstar", "door", "door+central")}
    check("G5 (reported, pre-declared) (f) SHEAR PASSES WITH THE DOOR: 0.8 <= R(k) <= 1.2 over k = 0.1-1 h/Mpc on both footings "
          "(XR9's gate-table reading), under both ends of the central-galaxy bracket",
          f"door: max {max(SH[f'{f}/door']['max'] for f in A0):.3f}, min {min(SH[f'{f}/door']['min'] for f in A0):.3f}; with the "
          f"central galaxies' phantoms min {min(SH[f'{f}/door+central']['min'] for f in A0):.3f}; M*: max "
          f"{max(SH[f'{f}/Mstar']['max'] for f in A0):.3f}, min {min(SH[f'{f}/Mstar']['min'] for f in A0):.3f}; one-sided R <= 1.2 "
          f"(MS3/MS4's code): door {one['door']}, M* {one['Mstar']}", two["door"] and two["door+central"], load_bearing=False)
    OUT["numbers"]["shear"] = dict(table=SH, halo_mass_cut_log10=lm_cut, two_sided=two, one_sided=one)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ (g) X-COP
    banner("(g) X-COP: M_dyn(R500)/M_HSE with the retained carrier -- M* (additive, nu_mono on the baryons) and the door (Newtonian)")
    from astropy.io import fits
    Gk = 4.30091727e-6; KPC_M = 3.0856775814913673e19; hh = 0.6736
    RHO_C0 = 2.775e11 * hh ** 2 / 1e9; FBX = 0.16

    def nfw(M200, c, rhoc=RHO_C0):
        r200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
        m = lambda x: np.log(1 + x) - x / (1 + x)
        return (lambda r: M200 * m(np.asarray(r, dtype=float) / rs) / m(c)), r200, rs
    R500J = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
    CL = []
    for name, meta in R500J.items():                                    # L321_carrier_z0_retention_gate.py lines 186-209
        d_ = os.path.join(REPO, "real_research", "data", "xcop", name)
        if not os.path.isdir(d_): continue
        hm = fits.open(os.path.join(d_, f"{name}_hydro_mass.fits"))
        Rk, Mf = hm[1].data["RADIUS"], hm[1].data["M_FORW"]
        par = {row["MODEL"].strip(): (float(row["RS"]), float(row["C200"])) for row in hm[2].data}
        fg = fits.open(os.path.join(d_, f"{name}_fgas_profile.fits"))[1].data
        R5 = meta["R500"] * 1000.0
        Mgas = float(np.interp(1.0, fg["RADIUS"], fg["MGAS"]))
        ms_path = os.path.join(d_, f"{name}_mstar.fits")
        if os.path.exists(ms_path):
            st = fits.open(ms_path)["MSTAR_SMOOTHED"].data; Mst = float(np.interp(R5, st["RADIUS"], st["MSTAR"]))
        else:
            Mst = 0.015 * float(np.interp(R5, Rk, Mf))
        rs, c = par["NFW"]
        rhoc_z = RHO_C0 * (0.315 * (1 + meta["z"]) ** 3 + 0.685)
        M200 = 200 * rhoc_z * 4 / 3 * math.pi * (c * rs) ** 3
        Mn, _, _ = nfw(M200, c, rhoc_z)
        CL.append(dict(name=name, R500=R5, Mhse=float(np.interp(R5, Rk, Mf)), Mb=Mgas + Mst, Mcarr=(1 - FBX) * float(Mn(R5)),
                       M200=M200, c=c, rhoc=rhoc_z, z=meta["z"], M1Mpch=float(Mn(1000.0 / hh))))
    # L354's kernel (nu_mono, L340) and the additive observable of L321 with its magnitude EFE g_e = 0.01 a0
    from scipy.optimize import brentq
    h_rar = lambda y: np.where(np.asarray(y, float) < 1e4, np.asarray(y, float) / np.expm1(np.sqrt(np.minimum(np.asarray(y, float), 1e4))), 0.0)
    dh_rar = lambda y, e=1e-6: (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
    Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
    LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
    DH = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
    H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
    nu_mono = lambda y: 1.0 + np.interp(np.log10(np.maximum(np.asarray(y, float), 1e-12)), LYG, H_MONO) / np.maximum(np.asarray(y, float), 1e-12)
    FOOT = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

    def cl_ratio(cl, eps, obs, foot):
        A0k = FOOT[foot] * KPC_M / 1e6
        R = cl["R500"]; gb = Gk * cl["Mb"] / R ** 2; gc = Gk * eps * cl["Mcarr"] / R ** 2
        g = (nu_mono(np.sqrt(gb ** 2 + (0.01 * A0k) ** 2) / A0k) * gb + gc) if obs == "additive" else (gb + gc)
        return float(g) * R ** 2 / Gk / cl["Mhse"]

    ratio = lambda eps, obs, foot: float(np.median([cl_ratio(cl, eps, obs, foot) for cl in CL]))
    L354 = json.load(open(os.path.join(DSDIR, "L354_carrier_lagrangian_additive_window_results.json")))["numbers"]["W1"]["table"]
    d2 = max(abs(ratio(r_["eps"], "additive", k_.split("_")[0]) - r_["ratio"]) for k_, rows in L354.items() for r_ in rows)

    def eps_bounds(rows_by_foot):
        """L366_triggered_carrier_cluster_retention.py eps_bounds(): a line through ratio_nt against eps, per footing."""
        out = {}
        for foot, pts in rows_by_foot.items():
            e = np.array([p_[0] for p_ in pts]); r = np.array([p_[1] for p_ in pts]); cf = np.polyfit(e, r, 1)
            out[foot] = (float((0.8 - cf[1]) / cf[0]), float((1.2 - cf[1]) / cf[0]))
        return out
    bM = eps_bounds({foot: sorted([(r_["eps"], r_["ratio_nt"]) for k_, rows in L354.items() if k_.startswith(foot) for r_ in rows])
                     for foot in FOOT})
    loM, hiM = max(v_[0] for v_ in bM.values()), min(v_[1] for v_ in bM.values())
    check("C2 CONTROL: L354's committed X-COP rows (median M_dyn/M_HSE at each committed eps, both footings, f_d 0.8-0.95) are "
          "reproduced from the X-COP data with L321's additive observable, and L366's two-sided bounds from them",
          f"rows max |diff| {d2:.1e}; bounds {loM:.4f}-{hiM:.4f} (L388 used {L388['eps_bounds']['lo']:.4f}-{L388['eps_bounds']['hi']:.4f})",
          d2 < 1e-9 and abs(loM - L388["eps_bounds"]["lo"]) < 1e-9 and abs(hiM - L388["eps_bounds"]["hi"]) < 1e-9)
    # the door: the Newtonian observable; the two-sided bounds on the median exactly (the ratio is linear in eps per cluster)
    bD = {}
    for foot in FOOT:
        f_ = lambda e, t: ratio(e, "newton", foot) * (1 - NT) - t
        bD[foot] = (brentq(lambda e: f_(e, 0.8), 0.0, 5.0), brentq(lambda e: f_(e, 1.2), 0.0, 5.0))
    loD, hiD = max(v_[0] for v_ in bD.values()), min(v_[1] for v_ in bD.values())
    P(f"    the carrier fraction X-COP needs (two-sided 20% after 6% non-thermal support): M* {loM:.3f}-{hiM:.3f}; the door (no "
      f"region: baryons + carrier) {loD:.3f}-{hiD:.3f}")
    P(f"    X-COP clusters' M(<1 Mpc/h) {min(c_['M1Mpch'] for c_ in CL):.2e}-{max(c_['M1Mpch'] for c_ in CL):.2e} Msun: every one in L388's top "
      f"bin (>= 2.5e14 Msun/h)")
    XW = {}
    for t in TAGS:
        e_pool = L388["table"]["pooled"][t]["eps_cl"]; e_top = L388["retention_by_mass"][t]["2.5e+14-1.0e+17"][0]
        XW[t] = dict(eps_pooled=e_pool, eps_top_bin=e_top,
                     Mstar_pooled=loM <= e_pool <= hiM, Mstar_top=loM <= e_top <= hiM,
                     door_pooled=loD <= e_pool <= hiD, door_top=loD <= e_top <= hiD,
                     ratio_nt_door_pooled=ratio(e_pool, "newton", "canonical") * (1 - NT),
                     ratio_nt_door_top=ratio(e_top, "newton", "canonical") * (1 - NT))
        P(f"    {t}: L388 retention pooled >= 1e14 {e_pool:.3f} / top bin {e_top:.3f} -> M* {'in' if XW[t]['Mstar_pooled'] else 'out'}/"
          f"{'in' if XW[t]['Mstar_top'] else 'out'}; door ratio {XW[t]['ratio_nt_door_pooled']:.3f} / {XW[t]['ratio_nt_door_top']:.3f} -> "
          f"{'in' if XW[t]['door_pooled'] else 'OUT'}/{'in' if XW[t]['door_top'] else 'OUT'}")
    win_M = [t for t in TAGS if XW[t]["Mstar_pooled"]]
    win_D = {k_: [t for t in TAGS if XW[t][k_]] for k_ in ("door_pooled", "door_top")}
    # the kick the top bin would need (linear in v_k across L388's runs; beyond them it is an extrapolation, labelled)
    vk = np.array([575.0, 600.0, 625.0, 650.0]); et = np.array([XW[t]["eps_top_bin"] for t in TAGS])
    cf = np.polyfit(vk, et, 1); vk_need = float((loD - cf[1]) / cf[0])
    P(f"    the top bin's retention falls {cf[0] * 100:+.3f} per 100 km/s; reaching the door's {loD:.3f} needs v_k ~ {vk_need:.0f} km/s "
      f"(a linear extrapolation below L388's range, not a run)")
    xcop_newton = DOOR
    mond_term = 0.0 if xcop_newton else float(ratio(0.5, "additive", "canonical") - ratio(0.5, "newton", "canonical"))
    check("D6 THE DOOR REMOVES THE X-COP CLUSTERS' PHANTOM: the scored observable carries no MOND term (the scored ratio minus its "
          "Newtonian part at eps = 0.5) -- MUTATE (regions merged: M*'s additive observable) must fail", f"{mond_term:.3e}", mond_term == 0.0)
    check("G6 (reported, pre-declared) (g) X-COP HAS A WINDOW WITH THE DOOR: some kick in 575-650 km/s puts L388's retention inside "
          "the door's two-sided bounds (L388's pooled statistic; its top mass bin reported beside it)",
          f"door window: pooled {win_D['door_pooled'] or 'none'}, top bin {win_D['door_top'] or 'none'} (needs eps >= {loD:.3f}; the top "
          f"bin holds {min(et):.3f}-{max(et):.3f}); M*'s window (pooled): {win_M}", bool(win_D["door_pooled"]), load_bearing=False)
    OUT["numbers"]["xcop"] = dict(bounds_Mstar=[loM, hiM], bounds_door=[loD, hiD], by_kick=XW, window_Mstar=win_M, window_door=win_D,
                                  vk_needed_top_bin_extrapolated=vk_need, clusters=[dict(name=c_["name"], Mb_over_Mhse=c_["Mb"] / c_["Mhse"],
                                                                                          Mcarr_over_Mhse=c_["Mcarr"] / c_["Mhse"],
                                                                                          M1Mpch=c_["M1Mpch"]) for c_ in CL])
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ (i) groups
    banner("(i) THE 2e13 GROUPS (hunt item 7's 20 Lovisari X-ray groups at R500): the carrier each needs, M* against the door")
    sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
    from hunt_lib import nu_s, G as Gh, kpc as kpch, Msun as Msunh, A0 as A0h      # noqa: E402  (item 7's constants and kernel)
    lp = os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")
    Lr = [l_.rstrip("\n").split("\t") for l_ in open(lp) if l_.strip() and not l_.startswith("#")]
    lh = {h_: i for i, h_ in enumerate(Lr[0])}
    GR = [dict(name=d_[lh["name"]], kT=float(d_[lh["kT_keV"]]), R500=float(d_[lh["R500_kpc"]]), M500=float(d_[lh["M500_1e13"]]) * 1e13,
               Mg500=float(d_[lh["Mgas500_1e12"]]) * 1e12) for d_ in Lr[1:]]
    mstar500 = lambda M500: 1.7e12 * (M500 / 1e14) ** 0.60                   # h7's KVM18 SHMR
    SBR = 1.5

    def mond_required_baryons(g_obs, r, a0):                                 # h7's, verbatim
        lo, hi = 1e-18, 1e-6
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            if nu_s(mid / a0) * mid < g_obs: lo = mid
            else: hi = mid
        return math.sqrt(lo * hi) * r ** 2 / Gh

    ETA = {}
    for foot, a0 in A0h.items():
        e_lo, e_hi = [], []
        for g_ in GR:
            r = g_["R500"] * kpch; gobs = Gh * g_["M500"] * Msunh / r ** 2
            Mreq = mond_required_baryons(gobs, r, a0) / Msunh; Ms = mstar500(g_["M500"])
            e_lo.append(Mreq / (g_["Mg500"] + Ms * SBR)); e_hi.append(Mreq / (g_["Mg500"] + Ms / SBR))
        ETA[foot] = (float(np.median(e_lo)), float(np.median(e_hi)))
    check("C3 CONTROL: hunt item 7's eta(R500) medians over the stellar bracket are reproduced from its data and formula: canonical "
          "1.80-2.11, alt 1.54-1.81", f"canonical {ETA['canonical'][0]:.2f}-{ETA['canonical'][1]:.2f}, alt {ETA['alt'][0]:.2f}-{ETA['alt'][1]:.2f}",
          abs(ETA["canonical"][0] - 1.80) < 0.005 and abs(ETA["canonical"][1] - 2.11) < 0.005 and abs(ETA["alt"][0] - 1.54) < 0.005
          and abs(ETA["alt"][1] - 1.81) < 0.005)
    # L388's retention at the groups' masses: M(<1 Mpc/h) from an NFW through M500 (Dutton-Maccio c), L388's bins by v_k
    c200_dm14 = lambda M200: 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / hh)))

    def m_1mpch(M500):
        """NFW with Dutton-Maccio c, normalised so that M(<R500) = M500 at 500 rho_c; mass inside 1 Mpc/h (physical, z ~ 0)."""
        m = lambda x: math.log(1 + x) - x / (1 + x)
        R500 = (3 * M500 / (4 * math.pi * 500 * RHO_C0)) ** (1 / 3)
        M200 = M500 * 1.4
        for _ in range(30):
            c = c200_dm14(M200); r200 = (3 * M200 / (4 * math.pi * 200 * RHO_C0)) ** (1 / 3); rs = r200 / c
            M200 = M500 * m(c) / m(R500 / rs)
        return M200 * m((1000.0 / hh) / rs) / m(c)
    BINS = ((6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17))

    def ret_group(M500, t):
        mm = m_1mpch(M500)
        for b0, b1 in BINS:
            if b0 <= mm < b1:
                return L388["retention_by_mass"][t][f"{b0:.1e}-{b1:.1e}"][0], False
        return L388["retention_by_mass"][t]["6.0e+13-1.0e+14"][0], True       # below L388's lowest bin: its value, an UPPER bound

    GRP = {}
    for foot, a0 in A0h.items():
        mcap = V_CAP ** 4 / (Gh * a0) / Msunh
        for sb in (SBR, 1 / SBR):
            for fbgg in (0.3, 0.6):
                rows = []
                for g_ in GR:
                    r = g_["R500"] * kpch; Ms = mstar500(g_["M500"]) * sb; Mb = g_["Mg500"] + Ms
                    gN = Gh * Mb * Msunh / r ** 2; Mmond = nu_s(gN / a0) * gN * r ** 2 / Gh / Msunh
                    Mbgg = fbgg * Ms
                    gB = Gh * Mbgg * Msunh / r ** 2
                    Mph_bgg = (nu_s(gB / a0) - 1.0) * gB * r ** 2 / Gh / Msunh if Mbgg < mcap else 0.0
                    Mcar = (1 - FBX) * g_["M500"]
                    rows.append(dict(name=g_["name"], M500=g_["M500"], Mb=Mb, above_cap=Mb > mcap, bgg_region=Mbgg < mcap,
                                     frac_Mstar=Mmond / g_["M500"], frac_door_bgg=(Mb + Mph_bgg) / g_["M500"], frac_door_newton=Mb / g_["M500"],
                                     eps_need_Mstar=(g_["M500"] - Mmond) / Mcar, eps_need_door_bgg=(g_["M500"] - Mb - Mph_bgg) / Mcar,
                                     eps_need_door_newton=(g_["M500"] - Mb) / Mcar,
                                     **{f"ratio_{t}_{m_}": ((Mnc + ret_group(g_["M500"], t)[0] * Mcar) / g_["M500"]) * (1 - NT)
                                        for t in TAGS for m_, Mnc in (("Mstar", Mmond), ("door_bgg", Mb + Mph_bgg), ("door_newton", Mb))}))
                GRP[f"{foot}/stars x{sb:.2f}/BGG {fbgg}"] = rows
    below = sum(ret_group(g_["M500"], "v600")[1] for g_ in GR)
    ab = min(sum(r_["above_cap"] for r_ in rows) for rows in GRP.values())
    P(f"    {len(GR)} groups, M500 {min(g_['M500'] for g_ in GR):.1e}-{max(g_['M500'] for g_ in GR):.1e}; baryons inside R500 above M_cap in "
      f"{ab}/{len(GR)} (every variant): no group keeps a region; {below} groups lie below L388's lowest mass bin (its retention is an upper bound)")
    SUMG = {}
    for k_, rows in GRP.items():
        med = lambda key: float(np.median([r_[key] for r_ in rows]))
        SUMG[k_] = dict(frac_Mstar=med("frac_Mstar"), frac_door_bgg=med("frac_door_bgg"), frac_door_newton=med("frac_door_newton"),
                        eps_need_Mstar=med("eps_need_Mstar"), eps_need_door_bgg=med("eps_need_door_bgg"), eps_need_door_newton=med("eps_need_door_newton"),
                        **{f"ratio_{t}_{m_}": med(f"ratio_{t}_{m_}") for t in TAGS for m_ in ("Mstar", "door_bgg", "door_newton")})
        s_ = SUMG[k_]
        P(f"    {k_:34s}: non-carrier share of M500 -- M* {s_['frac_Mstar']:.2f}, door {s_['frac_door_bgg']:.2f} (BGG's own phantom) / "
          f"{s_['frac_door_newton']:.2f} (none); carrier needed eps {s_['eps_need_Mstar']:.2f} / {s_['eps_need_door_bgg']:.2f} / "
          f"{s_['eps_need_door_newton']:.2f}; with L388's retention the NT-corrected ratio at 575/650: M* {s_['ratio_v575_Mstar']:.2f}/"
          f"{s_['ratio_v650_Mstar']:.2f}, door {s_['ratio_v575_door_bgg']:.2f}/{s_['ratio_v650_door_bgg']:.2f}")
    okM = {t: all(0.8 <= s_[f"ratio_{t}_Mstar"] <= 1.2 for s_ in SUMG.values()) for t in TAGS}
    okD = {t: all(0.8 <= s_[f"ratio_{t}_{m_}"] <= 1.2 for s_ in SUMG.values() for m_ in ("door_bgg", "door_newton")) for t in TAGS}
    lret = [L388["retention_by_mass"][t]["6.0e+13-1.0e+14"][0] for t in TAGS]
    check("G7 (reported, pre-declared) (i) THE GROUPS PASS WITH THE DOOR: at some kick in 575-650 km/s the median group's "
          "M_dyn(R500)/M_HSE (6% non-thermal) lies within 20% in every variant (stellar bracket, BGG share, BGG region or none, "
          "both footings), with L388's retention",
          f"door kicks passing: {[t for t in TAGS if okD[t]] or 'none'}; M*: {[t for t in TAGS if okM[t]] or 'none'}; the door needs "
          f"eps {min(s_['eps_need_door_bgg'] for s_ in SUMG.values()):.2f}-{max(s_['eps_need_door_newton'] for s_ in SUMG.values()):.2f} where "
          f"L388's lowest bin holds {min(lret):.2f}-{max(lret):.2f} (M* needs {min(s_['eps_need_Mstar'] for s_ in SUMG.values()):.2f}-"
          f"{max(s_['eps_need_Mstar'] for s_ in SUMG.values()):.2f})", any(okD.values()), load_bearing=False)
    # the step at M_cap: a galaxy-scale system just below M_cap keeps full MOND; one just above keeps its baryons only
    STEP = {}
    for foot, a0 in A0h.items():
        mcap = V_CAP ** 4 / (Gh * a0) / Msunh
        for r_kpc in (300.0, 500.0):
            r = r_kpc * kpch; gN = Gh * mcap * Msunh / r ** 2
            STEP[f"{foot}/{r_kpc:.0f} kpc"] = float(nu_s(gN / a0))
    P("    the step part (2) puts at M_b = M_cap: the non-carrier mass at 300-500 kpc falls by a factor nu = " + ", ".join(
        f"{k_} {v_:.1f}" for k_, v_ in STEP.items()) + " from just below M_cap to just above it (h55: eta flat from 5e12 to 1.6e15, no step)")
    OUT["numbers"]["groups"] = dict(eta_control=ETA, summary=SUMG, kicks_pass_Mstar=okM, kicks_pass_door=okD, step_factor_at_Mcap=STEP,
                                    rows=GRP)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ (h) mergers
    banner("(h) HARVEY AND EL GORDO: L370's own kernel-off run IS the door's cluster physics (no phantom; real = lensing mass)")
    L370 = {k_: json.load(open(os.path.join(REPO, "real_research", "merger_infall_2026", f"L370_boosted_infall_mergers{s_}_results.json")))
            for k_, s_ in (("main", ""), ("kernel_off", "_MUTATE"))}
    MER = {}
    for k_, d_ in L370.items():
        ch = {c_.split()[0]: v_["measured"] for c_, v_ in d_["checks"].items()}
        MER[k_] = dict(A1_real_over_lensing=ch.get("A1"), A3_el_gordo_dchi=ch.get("A3"), B2_intact=ch.get("B2"), B3_core_decayed=ch.get("B3"),
                       B4_uniform_055=ch.get("B4"), B5_intact_nfw=ch.get("B5"), B6_decayed_nfw=ch.get("B6"), B7_population=ch.get("B7"))
        P(f"    L370 {k_:10s}: El Gordo {MER[k_]['A3_el_gordo_dchi']}; Harvey intact {MER[k_]['B2_intact']}, NFW fit {MER[k_]['B5_intact_nfw']}; "
          f"core-decayed {MER[k_]['B3_core_decayed']}; uniform 0.55 {MER[k_]['B4_uniform_055']}")
        P(f"                     population (100 kpc / 150 kpc / NFW), sigma from Harvey's mean: {MER[k_]['B7_population']}")
    check("G9 (reported) (h) WHAT THE DOOR DOES TO THE MERGERS (L370's own kernel-off run): El Gordo reverts to LCDM's tension (the "
          "phantom's ease is lost); Harvey passes with an intact or uniformly depleted carrier, and a core-decayed carrier fails "
          "harder at 100 kpc apertures than with the phantom", f"El Gordo Delta chi: M*-like {MER['main']['A3_el_gordo_dchi']} -> door "
          f"{MER['kernel_off']['A3_el_gordo_dchi']}; Harvey intact {MER['kernel_off']['B2_intact']}; core-decayed "
          f"{MER['main']['B3_core_decayed']} -> {MER['kernel_off']['B3_core_decayed']}", True, load_bearing=False)
    OUT["numbers"]["mergers_L370"] = MER

    # ============================================================================================ (e) KiDS
    banner("(e) KiDS-1000: the committed score and whether the door changes any input of it; the watershed's satellites (scoped)")
    X9K = json.load(open(os.path.join(HERE, "XR9_kids_flagship_results.json")))["numbers"]["kids"]["p1_x2.5"]
    kd = {f: X9K["kids"][f"w0.25/v600/{f}"]["gate"] for f in ("canonical", "alt")}
    lmax = max(b_[0] for f in kd for b_ in kd[f]["per_bin"])
    P(f"    XR9 at the cell (kappa cap, w = 0.25, v_k = 600, fs = 1, A <= 2): Delta chi^2 {kd['canonical']['dchi2']:+.2f} / {kd['alt']['dchi2']:+.2f} "
      f"(DE10: -32.3 / -29.3); fitted lens baryons up to 10^{lmax:.1f} Msun < M_cap")
    # the satellites' watershed basins: the Milky Way's own satellite census (the LVD file KD reads) as a template lens.  Each
    # satellite's basin, seen from the host at host-centric radius R, covers the directions within alpha(R/D) of the satellite
    # (the separatrix of this lane's watershed, satellite at 0 and host at 1 in units of D); the sky fraction the host's
    # region loses at R is the UNION of those caps over the real Galactocentric directions (Monte Carlo on the sphere).
    sys.path.insert(0, HERE)
    from XR13_door_local_group import separatrix                           # noqa: E402  (this lane's own watershed)
    import csv as _csv
    from astropy.coordinates import SkyCoord, Galactocentric
    import astropy.units as u_
    SAT = []
    for r_ in _csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv"))):
        try:
            dmod = float(r_["distance_modulus"]); mv = float(r_["apparent_magnitude_v"]) - dmod
            ra, de = float(r_["ra"]), float(r_["dec"])
        except Exception:
            continue
        Mb_ = 2.0 * 10 ** (-0.4 * (mv - 4.83))                              # KD's Upsilon_V = 2 (stars; HI added where measured)
        try:
            if r_.get("mass_HI", "").strip() and not r_.get("mass_HI_ul", "").strip(): Mb_ += 1.33 * 10 ** float(r_["mass_HI"])
        except Exception:
            pass
        gc = SkyCoord(ra=ra * u_.deg, dec=de * u_.deg, distance=10 ** (dmod / 5 + 1) * u_.pc).transform_to(Galactocentric())
        xyz = np.array([gc.x.to(u_.kpc).value, gc.y.to(u_.kpc).value, gc.z.to(u_.kpc).value])
        D_ = float(np.linalg.norm(xyz))
        if D_ < 300.0 and Mb_ > 0:
            SAT.append(dict(key=r_["key"], Mb=Mb_, D_kpc=D_, n=xyz / D_, host=r_.get("host", "")))
    CONE = {}
    for s_ in SAT:
        q = math.sqrt(6.0e10 / s_["Mb"])
        rrq, phq, zsq, pts = separatrix(q, smax=800.0)
        Rh = np.hypot(pts[:, 0], pts[:, 1] - 1.0); al = np.arctan2(pts[:, 0], 1.0 - pts[:, 1])
        o = np.argsort(Rh); Rh, al = Rh[o], np.maximum.accumulate(al[o])
        s_.update(Rh=Rh, alpha=al, s_star=float(zsq), own_edge=1850.0 * (s_["Mb"] / 1.145e11) ** 0.25)
        CONE[s_["key"]] = dict(Mb=s_["Mb"], D_kpc=s_["D_kpc"], host=s_["host"], half_angle_far_deg=float(np.degrees(al[-1])),
                               own_edge_kpc=s_["own_edge"])
    rng = np.random.default_rng(11); vv = rng.normal(size=(40000, 3)); vv /= np.linalg.norm(vv, axis=1)[:, None]
    RR = (50.0, 100.0, 200.0, 300.0, 500.0, 1000.0)

    def union(R_, rule, skip=()):
        cov = np.zeros(len(vv), bool)
        for s_ in SAT:
            if s_["key"] in skip: continue
            x_ = R_ / s_["D_kpc"]
            if x_ <= 1.0 - s_["s_star"] or (rule == "refined" and R_ > s_["D_kpc"] + s_["own_edge"]): continue
            a_ = float(np.interp(x_, s_["Rh"], s_["alpha"]))
            cov |= (vv @ s_["n"]) > math.cos(a_)
        return float(cov.mean())
    lost = {f"{R_:.0f} kpc": dict(refined=union(R_, "refined"), strict=union(R_, "strict"),
                                  refined_without_MCs=union(R_, "refined", skip=("lmc", "smc"))) for R_ in RR}
    big = sorted(CONE.items(), key=lambda kv: -kv[1]["Mb"])[:3]
    P(f"    the Milky Way's {len(SAT)} catalogued satellites within 300 kpc (LVD, Upsilon_V = 2; the LMC and SMC included); far-field "
      f"basin half-angles " + ", ".join(f"{k_} {v_['half_angle_far_deg']:.0f} deg" for k_, v_ in big) + ", the rest "
      f"{min(v_['half_angle_far_deg'] for v_ in CONE.values()):.0f}-{sorted(v_['half_angle_far_deg'] for v_ in CONE.values())[-4]:.0f} deg")
    P("    sky fraction of the host's region inside satellite basins (the union over real directions; refined rule: each basin only "
      "out to the satellite's own edge / strict: to the host's edge / refined without the Magellanic Clouds):")
    P("      " + "; ".join(f"R {k_}: {v_['refined']:.3f} / {v_['strict']:.3f} / {v_['refined_without_MCs']:.3f}" for k_, v_ in lost.items()))
    worst = max(v_["refined"] for v_ in lost.values())
    check("G8 (reported) (e) KiDS IS UNCHANGED IN THE COMMITTED MODEL: every fitted lens bin is below M_cap and the lenses are isolated "
          "(no neighbour > 10% in stellar mass within 3 Mpc), so the door changes no input of XR9's/DE10's score.  NOT established "
          "for real lenses: satellites below the isolation cut own watershed basins that the committed model has not got, and the "
          "phantom flux through a sphere at R falls by the sky fraction they cover",
          f"XR9 {kd['canonical']['dchi2']:+.2f} / {kd['alt']['dchi2']:+.2f} (pass <= +4); lens baryons <= 10^{lmax:.1f} Msun; a Milky-Way-like "
          f"satellite system covers up to {worst:.2f} of the host's sky (refined rule; {max(v_['refined_without_MCs'] for v_ in lost.values()):.2f} "
          f"without the Magellanic Clouds)", 10 ** lmax < min(M_CAP.values()) and max(kd[f]["dchi2"] for f in kd) <= 4.0, load_bearing=False)
    OUT["numbers"]["kids"] = dict(XR9_dchi2={f: kd[f]["dchi2"] for f in kd}, lens_logMb_max=lmax, satellite_basins=CONE,
                                  sky_fraction_lost=lost)
    # ---- is part (2) what breaks the clusters?  Rule (1)'s watershed alone gives every member a basin (a cone behind it):
    # the far-field sky fraction per member against its mass ratio, and the union for N members placed at random
    OM = {}
    for mu in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        _, _, _, pts = separatrix(math.sqrt(1.0 / mu), smax=800.0)
        OM[f"{mu:.0e}"] = (1 - math.cos(math.atan2(pts[-1][0], -pts[-1][1]))) / 2
    rngc = np.random.default_rng(5)
    UN = {}
    for lab, mus in (("rich cluster: 100 members at mu = 1e-5-1e-3", 10 ** rngc.uniform(-5, -3, 100)),
                     ("group: 15 members at mu = 1e-3-1e-1", 10 ** rngc.uniform(-3, -1, 15))):
        nd = rngc.normal(size=(len(mus), 3)); nd /= np.linalg.norm(nd, axis=1)[:, None]
        cov = np.zeros(len(vv), bool)
        for mu, n_ in zip(mus, nd):
            om = float(np.interp(math.log10(mu), [-6, -5, -4, -3, -2], [OM[k_] for k_ in ("1e-06", "1e-05", "1e-04", "1e-03", "1e-02")]))
            cov |= (vv @ n_) > 1 - 2 * om
        UN[lab] = float(cov.mean())
    P("    rule (1) alone, the members' basins (far-field sky fraction per member): " + ", ".join(f"mu {k_}: {v_:.3f}" for k_, v_ in OM.items())
      + "; union for random placements: " + "; ".join(f"{k_}: {v_:.2f}" for k_, v_ in UN.items()))
    check("G10 (reported) PART (2) IS NOT THE ONLY THING THAT EMPTIES THE CLUSTERS: under rule (1)'s watershed alone a rich cluster's "
          "members carve most of its region's sky into their own basins, so dropping part (2) would not restore the cluster phantoms "
          "that X-COP, shear, the groups and El Gordo leaned on", "; ".join(f"{k_}: {v_:.2f} of the sky" for k_, v_ in UN.items()),
          True, load_bearing=False)
    OUT["numbers"]["members_shred_regions"] = dict(sky_fraction_per_member=OM, union=UN)

    # ============================================================================================ summary
    banner("SUMMARY (scored column: " + ("the door" if DOOR else "M*, regions merged (MUTATE)") + ")")
    sc_sh = SH[f"canonical/{scored}"], SH[f"alt/{scored}"]
    P(f"  (f) shear R(k): max {max(s_['max'] for s_ in sc_sh):.3f}, min {min(s_['min'] for s_ in sc_sh):.3f} (two-sided band 0.8-1.2)")
    P(f"  (g) X-COP carrier bounds: {(loD if DOOR else loM):.3f}-{(hiD if DOOR else hiM):.3f}; L388 pooled {min(v_['eps_pooled'] for v_ in XW.values()):.3f}-"
      f"{max(v_['eps_pooled'] for v_ in XW.values()):.3f}, top bin {min(et):.3f}-{max(et):.3f}")
    P(f"  (i) groups: kicks passing {[t for t in TAGS if (okD if DOOR else okM)[t]] or 'none'}")
    P(f"  (h) El Gordo {MER['kernel_off' if DOOR else 'main']['A3_el_gordo_dchi']}; (e) KiDS {kd['canonical']['dchi2']:+.2f} / {kd['alt']['dchi2']:+.2f}")
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
