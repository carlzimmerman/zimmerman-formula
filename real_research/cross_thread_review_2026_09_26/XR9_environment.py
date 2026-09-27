#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR9_environment.py -- THE SMALL-REGION DOOR, part 3 of 3: the galaxy-environment gates as the vacuum gate's threshold is
raised -- the Local Group zero-velocity radius, the two EFE samples (cluster-infall BTFR N = 314, Local Volume dwarfs
N = 92), the Coma ultra-diffuse galaxies, and the rotation-curve radii of SPARC.  Independent cross-thread review
(2026-09-26, night).  Read-only on every committed file.  XR6's two scripts are loaded as libraries (their definitions only,
MUTATE forced off; neither main block is run) and their committed numbers are the controls; KC/KD's loaders are imported
exactly as XR6 imported them (main() never called).

THE DOOR (XR9_kids_flagship.py has the full statement and the pre-declared hypothesis H).  XR6 found the converged model
(p = 1, x_c0 = 2.5) does not fix the EFE samples, the Local Group's R_0 (1.41/1.48 Mpc against 0.96 +- 0.03) or the Coma
UDGs: the data say galaxies behave as if isolated, with less MOND pull at ~1 Mpc than a large region gives.  Raising the
threshold shrinks every region (r_e ~ v_f/(H sqrt(x_c,eff))) and MS5's kappa-form cap with it (l_cap = v_cap/(H sqrt(x_c,eff))).
This lane asks, cell by cell (p in {1, 1.5}, x_c0 in {2.5, 3.5, 5, 7, 10, 14, 20}), whether those liabilities move into
their bands, and whether any new failure appears (a galaxy whose own region no longer covers its kinematics).

THE CAP.  MS5's kappa form (61a3a0858, the coordinating review's correction): U_cap = C min(lap Phi_X, v_cap^2 kappa_X^2),
kappa_X = 1/r for every spherical profile, so a spherical host's region = {the door's density condition} AND
{r <= l_cap(z)}, v_cap = 325 km/s.  The form XR6 used (threshold x max(1, v_loc^2/v_cap^2)) is WITHDRAWN; it is used here
ONLY to reproduce XR6's committed numbers (labelled "withdrawn-form control").  At the converged cell the kappa form puts
the clusters' edges at 2.9-3.0 Mpc (XR6: 3.5-3.7), so the model's own EFE numbers at x_c0 = 2.5 are this lane's, not XR6's.
A member galaxy's own region beyond its host's: the density condition as XR6 wrote it (host density + the galaxy's
scalar-sum phantom) with no v_loc term, and the kappa condition read two ways (both scored, a pass must hold under both):
  'galaxy'    kappa = 1/s: the member's own equipotentials as if it were alone, so its region is capped at s <= l_cap;
  'twofield'  kappa of the member's radial MOND field plus its host's (locally uniform) field and the host's curvature:
              exact for that superposition (derivation in galaxy_region_k's docstring).  Toward the host kappa =
              g_g/(s |g_g - g_h|) sets the region's extent; ACROSS the host's field kappa -> g_g^3/(s |F|^3) (deep MOND), so a
              member deep in a strong external field beyond its host's cap can lose the kappa condition at its own disc --
              such a galaxy is Newtonian with its carrier cleared: a NEW FAILURE, counted, never dropped.
  (A first development run read the second way as 'the galaxy's field must exceed the host's' and flagged 234 member-
  variants as new failures at the converged cell.  That prompted re-deriving the curvature: the step at g_g = g_h was
  wrong -- the curvature near a satellite falls as (g_g/g_h)^3/s across the external field and rises toward the saddle.
  The reading was replaced by the exact two-field form; none of that run's numbers is used.)

THE GATES (definitions fixed before the scan; each reported per cell, both footings):
  LG    XR6's (k02/XR4's) point-mass + Lambda shell model, the edge from the capped switch solved numerically at 97 epochs
        (kappa form; the closed form beside it), M_b = 1.145e11 and 1.72e11, carrier histories none / decay / full.
        Band |log10(R_0/0.96)| <= 0.10.  Gated on the model's own history ('decay': L388-like kicked retention):
        pass if some M_b lands in the band on BOTH footings.
  EFE-C the cluster-infall BTFR slope (d Delta/d log g_e) under operator A (L361's action: the host's in-region baryons,
        screened beyond: gaps Dirichlet, 1/m = 0.2, 0.5 Mpc), both forms (scalar sum, subtract), f_b(R500) 0.10/0.13/0.157,
        r = R_proj and 1.3 R_proj, baryons extended or cut at r200, kappa 'galaxy' and 'twofield'.  Pass = every variant within
        2 sigma of the observed slope AND no new failure.  The members inside a host's region are counted.
  EFE-D the Local Volume dwarfs' statistic C (XR4/XR6), host baryons x1, x1.5, x2; pass = every variant within 2 sigma.
  UDG   the eleven Coma UDGs (L23's pipeline as XR6 rebuilt it): inside Coma's region the EFE of Coma's baryons (L361);
        beyond it the screened, transmitted field (and Newtonian if its own region no longer covers r_1/2); the systematic
        floor recomputed on each cell's arm.  Pass = the central arm (beta-model, Einasto 3-D, f_b 0.13) below 2 sigma on
        both footings for every gap and kappa reading, with no Newtonian UDG.
  RC    SPARC's 175 rotation curves: every galaxy's fully-on radius at z = 0 (U = x_c,eff (1 + w), w = 0.25, kappa cap)
        must reach 3 R_last, so the RAR is untouched.

CHECKS
  C1 CONTROL (LG): XR6's committed R_0 table (closed-form edge, x_c0 = 2.0 / 2.5 / 2.97, both M_b, three histories, both
     footings) and its numerical-table R_0 are reproduced exactly (1e-9).
  C2 CONTROL (EFE, withdrawn-form control): with XR6's own switch functions at p = 1, x_c0 = 2.5 this lane's scoring loop
     reproduces XR6's committed cluster table (24 variants x 6 scenarios x 8 numbers, the classification) exactly.
  C3 CONTROL: XR6's committed dwarf rows (candidate, x1/x1.5/x2, both footings) are reproduced exactly.
  C4 CONTROL: XR6's committed Coma numbers (capped edges, the candidate offsets, floor and sigmas) are reproduced exactly.
  K1 (reported) the kappa form at the converged cell: the LG's R_0 (the kappa cap does not bind there) and the cluster
     edges (2.9-3.0 Mpc at z = 0.02-0.06).
  E1 [load-bearing; MUTATE must fail] THE REGIONS SHRINK AS THE DOOR SAYS: between p = 1, x_c0 = 2.5 and 20 the LG's z = 0
     edge and Coma's kappa edge fall by sqrt(x_c,eff ratio) within 5%.
  P6 (reported, diagnostic beyond the cells) the threshold at which each z ~ 0 liability would pass: the dwarf statistic
     and the Coma UDGs scanned in x_c,eff at their epoch up to 1000, the clusters at x_c0 = 40/100/300, and the LG with a
     constant threshold (p = 0) -- where the liabilities want the regions, whatever the gate's time dependence.
  Per-gate verdicts are REPORTED (not load-bearing); the pre-declared H is scored in XR9_gate_table.py.
MUTATE=1 freezes the threshold at the converged cell for every scan cell (the edges cannot move): E1 must FAIL (rc = 1).

SCOPE (XR6's, unchanged).  Spherical and 1-D throughout; the LG as one point mass at its barycentre (at the highest
thresholds the MW and M31 regions may no longer merge -- not modelled); member 3-D radii from projected radii; XR4's
f_b template; the galaxies' own regions in the scalar-sum form; the kappa condition for a member read two ways, not
solved in 3-D; the cap and the trigger have no complete action (MS5 gives the cap's gate term).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR9_environment.py   (MUTATE=1)
"""
import os, sys, json, math, time, io, contextlib, warnings, itertools, csv
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR9_environment"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR9 part 3 (environment)", "mutate": MUTATE, "checks": {}, "numbers": {}}
PS = (1.0, 1.5)
XC0S = (2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0)
CELLS = [(p, x0) for p in PS for x0 in XC0S]
V_CAP = 325e3
W_GATE = 0.25
ck = lambda p, x0: f"p{p:g}_x{x0:g}"
eff = lambda p, x0: (1.0, 2.5) if MUTATE else (p, x0)                 # MUTATE freezes the threshold


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


def load(path, cuts, name):
    """exec the definitions of a committed script (MUTATE forced off, stdout swallowed); cuts = [(start_marker, end_marker)]."""
    ns = {"__name__": name, "__file__": path}
    src = open(path).read().replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        for a_, b_ in cuts:
            chunk = src if a_ is None else src.split(a_)[1]
            chunk = chunk if b_ is None else chunk.split(b_)[0]
            exec(chunk, ns)
    return ns


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: every scan cell uses the converged cell's threshold; E1 must FAIL ***")
    MK = "# ============================================================================================ "
    LG = load(os.path.join(HERE, "XR6_lg_zero_velocity_mond_sector.py"), [(None, MK + "C1 / C2 controls")], "xr6lg")
    EF = load(os.path.join(HERE, "XR6_efe_udg_under_candidate.py"),
              [(None, MK + "PART A clusters"), (MK + "PART A clusters", "F500S = (0.10, 0.13, FCOS)"),
               (MK + "PART C Coma UDGs", "arm_L23 = lambda")], "xr6efe")
    XR6LG = json.load(open(os.path.join(HERE, "XR6_lg_zero_velocity_mond_sector_results.json")))["numbers"]
    XR6E = json.load(open(os.path.join(HERE, "XR6_efe_udg_under_candidate_results.json")))["numbers"]
    P(f"  XR6's LG and EFE/UDG definitions loaded (mains not run)   [{time.time() - T0:.0f}s]")

    # ============================================================================================ PART 1 the Local Group
    banner("PART 1 -- THE LOCAL GROUP's ZERO-VELOCITY RADIUS (XR6/XR4/k02's shell model; kappa-form edge)")
    G, Mpc, Msun, H0, OM_M, OM_L, FB = (LG[k_] for k_ in ("G", "Mpc", "Msun", "H0", "OM_M", "OM_L", "FB"))
    A0L6, LNA_TAB, run_cells, edge_table, dnu_mono = LG["A0"], LG["LNA_TAB"], LG["run_cells"], LG["edge_table"], LG["dnu_mono"]
    MB_LG = 1.145e11; MBS = (MB_LG, 1.5 * MB_LG); HISTS = ("none", "decay", "full"); R0M, BAND = 0.96, 0.10

    def edge_numeric_k(Mb, a0, z, xc0, p, wfac=1.0):
        """XR6's edge_numeric with MS5's kappa cap in place of the withdrawn local cap: U = min(x, (v_cap/(r H))^2) >=
        x_c,eff wfac (wfac = 1: the midpoint; 1 + w: fully on).  Returns the edge [m]."""
        E2 = OM_M * (1 + z) ** 3 + OM_L; H = H0 * math.sqrt(E2); Omz = OM_M * (1 + z) ** 3 / E2
        r = np.geomspace(1e-5 * Mpc, 40.0 * Mpc, 6000)
        GM = G * Mb * Msun; y = GM / (r ** 2 * a0)
        D = -2.0 * GM ** 2 * dnu_mono(y) / (r ** 5 * a0)
        x = 1.5 * Omz * FB + D / H ** 2
        xc = xc0 * E2 ** p * wfac
        on = (x >= xc) & (r <= V_CAP / (H * math.sqrt(xc)))
        ion = np.where(on)[0]
        if ion.size == 0:
            return 0.0
        i0 = ion[0]; off = np.where(~on[i0:])[0]
        i1 = len(r) - 1 if off.size == 0 else i0 + off[0]
        return math.sqrt(r[i1 - 1] * r[i1])

    def table_k(Mb, a0, xc0, p):
        return np.array([edge_numeric_k(Mb, a0, 1.0 / math.exp(l) - 1.0, xc0, p) for l in LNA_TAB])

    # ---- C1 LG controls
    ctl = []
    for foot, a0 in A0L6.items():
        for Mbv, hist, xc in itertools.product(MBS, HISTS, (2.0, 2.5, 2.97)):
            ctl.append(dict(foot=foot, Mb=Mbv, a0=a0, xc0=xc, p=1.0, hist=hist, edge="ms_abs"))
    tabs_local = {f: edge_table(MB_LG, A0L6[f], 2.5, 1.0, LG["VCAP"]) for f in A0L6}
    ctl += [dict(foot=f, Mb=MB_LG, a0=A0L6[f], xc0=2.5, p=1.0, hist="none", edge="ms_num", table=tabs_local[f]) for f in A0L6]
    tabs_k0 = {f: table_k(MB_LG, A0L6[f], 2.5, 1.0) for f in A0L6}
    ctl += [dict(foot=f, Mb=MB_LG, a0=A0L6[f], xc0=2.5, p=1.0, hist="none", edge="ms_num", table=tabs_k0[f]) for f in A0L6]
    Rc = run_cells(ctl)
    dc1 = 0.0
    for c, v in zip(ctl[:-4], Rc[:-4]):
        ref = XR6LG["R0"][f"{c['foot']}/{c['Mb']:.3e}/{c['hist']}"]["ms_abs"][(2.0, 2.5, 2.97).index(c["xc0"])]
        dc1 = max(dc1, abs(v / ref - 1))
    refT = XR6LG["S1_tables"]["R0_capped_table"]
    dc1 = max(dc1, abs(Rc[-4] / refT[0] - 1), abs(Rc[-3] / refT[1] - 1))
    check("C1 CONTROL (LG): XR6's committed R_0 table (closed-form MOND-sector edge, x_c0 = 2.0/2.5/2.97, both M_b, three "
          "histories, both footings; 36 cells) and its numerical capped-table R_0 (withdrawn local cap) are reproduced exactly",
          f"max relative difference {dc1:.1e}", dc1 < 1e-9)
    k1lg = [float(Rc[-2]), float(Rc[-1])]
    P(f"    kappa-form numerical table at the converged cell: R_0 = {k1lg[0]:.4f} / {k1lg[1]:.4f} Mpc (withdrawn-form table "
      f"{Rc[-4]:.4f} / {Rc[-3]:.4f}): the kappa cap does not bind on the LG (v_f = 195-226 km/s < v_cap)")

    # ---- the scan
    LGT = {}
    cells_run = []
    TABK = {}
    for (p, x0) in CELLS:
        pe, xe = eff(p, x0)
        for foot, a0 in A0L6.items():
            for Mbv in MBS:
                TABK[(ck(p, x0), foot, Mbv)] = table_k(Mbv, a0, xe, pe)
                for hist in HISTS:
                    cells_run.append(dict(key=ck(p, x0), foot=foot, Mb=Mbv, a0=a0, xc0=xe, p=pe, hist=hist, edge="ms_num",
                                          table=TABK[(ck(p, x0), foot, Mbv)]))
                    cells_run.append(dict(key=ck(p, x0), foot=foot, Mb=Mbv, a0=a0, xc0=xe, p=pe, hist=hist, edge="ms_abs"))
    P(f"    {len(TABK)} kappa-form edge tables built   [{time.time() - T0:.0f}s]")
    Rs = run_cells(cells_run)
    for c, v in zip(cells_run, Rs):
        LGT.setdefault(c["key"], {})[f"{c['foot']}/{c['Mb']:.3e}/{c['hist']}/{c['edge']}"] = float(v)
    for (p, x0) in CELLS:
        key = ck(p, x0); row = LGT[key]
        z0edge = {f"{f}/{Mbv:.3e}": float(TABK[(key, f, Mbv)][-1] / Mpc) for f in A0L6 for Mbv in MBS}
        inb = lambda R: abs(math.log10(R / R0M)) <= BAND if np.isfinite(R) else False
        dec_ok = any(all(inb(row[f"{f}/{Mbv:.3e}/decay/ms_num"]) for f in A0L6) for Mbv in MBS)
        any_ok = any(all(inb(row[f"{f}/{Mbv:.3e}/{h}/ms_num"]) for f in A0L6) for Mbv in MBS for h in HISTS)
        LGT[key] = dict(R0=row, edge_z0_Mpc=z0edge, pass_=dec_ok, pass_any_history=any_ok,
                        dex_decay={f"{f}/{Mbv:.3e}": math.log10(row[f"{f}/{Mbv:.3e}/decay/ms_num"] / R0M) for f in A0L6 for Mbv in MBS})
        P(f"  {key:9s} LG edge at z = 0 (M_b 1.145e11) {z0edge['canonical/1.145e+11']:.2f}/{z0edge['alt/1.145e+11']:.2f} Mpc | R_0 [Mpc] "
          f"decay: " + " ".join(f"{row[f'{f}/{Mbv:.3e}/decay/ms_num']:.3f}" for Mbv in MBS for f in A0L6)
          + " | none: " + " ".join(f"{row[f'{f}/{Mbv:.3e}/none/ms_num']:.3f}" for Mbv in MBS for f in A0L6)
          + " | full: " + " ".join(f"{row[f'{f}/{Mbv:.3e}/full/ms_num']:.3f}" for Mbv in MBS for f in A0L6)
          + f"  -> {'IN BAND' if dec_ok else 'out'} (any history: {'yes' if any_ok else 'no'})")
    P("    (order in each group: M_b 1.145e11 canonical, alt; 1.72e11 canonical, alt; band 0.76-1.21 Mpc; closed-form edges in the JSON)")
    OUT["numbers"]["LG"] = LGT
    OUT["numbers"]["LG_kappa_at_converged"] = k1lg

    # ============================================================================================ PART 2 EFE clusters
    banner("PART 2 -- THE CLUSTER-INFALL BTFR (N = 314): operator A with the kappa cap, cell by cell")
    KC, KD, A0, MSUN, MPC, KPC, GAPS = (EF[k_] for k_ in ("KC", "KD", "A0", "MSUN", "MPC", "KPC", "GAPS"))
    Gc = EF["G"]
    gal, cls, idx, memb, Vv, Mbg, lHIall, RHI, lMb_all, used = (EF[k_] for k_ in (
        "gal", "cls", "idx", "memb", "V", "Mb", "lHIall", "RHI", "lMb_all", "used"))
    Rp_m = EF["Rp"]
    cluster_Mb, cluster_switch, ms_profile, switch_state, region_edge, transmit, galaxy_region = (EF[k_] for k_ in (
        "cluster_Mb", "cluster_switch", "ms_profile", "switch_state", "region_edge", "transmit", "galaxy_region"))
    regress, boot_err, zero_point, predict, nu_mono_e, dnu_mono_e, fb_profile = (EF[k_] for k_ in (
        "regress", "boot_err", "zero_point", "predict", "nu_mono", "dnu_mono", "fb_profile"))
    KCnu = KC.nu
    F500S = (0.10, 0.13, EF["FCOS"]); GEOS = (("R_proj", 1.0), ("1.3 R_proj", 1.3)); EXTS = ("extended", "r200")

    def set_cell(p, x0):
        EF["XC0"], EF["PG"] = x0, p

    lcap_e = lambda z: V_CAP / (EF["Hz"](z) * math.sqrt(EF["xceff"](z)))

    def cluster_switch_k(c, a0, f500, ext, capped=True):
        r = np.geomspace(0.05 * c["r500"], 40.0 * MPC, 4000)
        Mbr = cluster_Mb(c, f500, ext, r)
        e, g, D, qb = ms_profile(r, Mbr, a0)
        on = switch_state(c["z"], D, qb, g, math.inf)[0]
        if capped:
            on = on & (r <= lcap_e(c["z"]))
        re, found = region_edge(r, on)
        return dict(r=r, Mb=Mbr, e=e, g=g, D=D, qb=qb, r_e=re, found=found)

    def galaxy_region_k(Mg, Rk, z, a0, e_loc, g_h, D_h, qb_h, r_host, variant):
        """XR6's galaxy_region with the withdrawn v_loc term removed (the door's density condition only) and MS5's kappa
        condition kappa_X >= 1/l_cap, read two ways ('none' = no cap, the uncapped reference):
          'galaxy'    kappa = 1/s, the member's own equipotentials as if alone: its region is capped at s <= l_cap;
          'twofield'  kappa of the member's radial MOND field g_g(s) plus the host's field g_h, locally uniform, plus the
                      host's own curvature weighted by its share, (g_h/|F|)/r_host.  Exact for that superposition:
                        kappa = (1/2)[(g_g' + 2 g_g/s)/|F| - (g_g'(g_g + g_h cos t)^2 + g_h^2 g_g sin^2 t/s)/|F|^3],
                      |F|^2 = g_g^2 + g_h^2 + 2 g_g g_h cos t.  Toward the host (t = 180 deg) kappa = g_g/(s |g_g - g_h|)
                      sets the region's extent (which decides merging and the screened gap); across the host's field
                      (t = 90 deg) kappa = (g_g' g_g^2 ... ) -> g_g^3/(s |F|^3) in deep MOND, the most restrictive azimuth,
                      decides whether the disc at R_k is still inside its own region.
        Returns (disc_on, R_e [m], region reaches R_k)."""
        lc = lcap_e(z); ik = 1.0 / lc
        GM = Gc * Mg
        Dd = 3.0 * GM / Rk ** 3; gd = GM / Rk ** 2
        on_d = bool(switch_state(z, np.array([D_h]), np.array([qb_h]), np.array([g_h]), math.inf, extra=Dd, Dextra=Dd, gextra=gd)[0][0])
        s = np.geomspace(Rk, 8.0 * MPC, 1200)
        gN_ = GM / s ** 2; y = (gN_ + e_loc) / a0
        gg = nu_mono_e(y) * gN_
        Dg = -2.0 * GM ** 2 * dnu_mono_e(y) / (s ** 5 * a0)
        on = switch_state(z, np.full_like(s, D_h), np.full_like(s, qb_h), np.full_like(s, g_h), math.inf,
                          extra=np.maximum(Dg, 0.0), Dextra=Dg, gextra=gg)[0]
        if variant == "galaxy":
            on = on & (s <= lc)
        elif variant == "twofield":
            hc = 1.0 / max(r_host, 1e-30)
            F180 = np.maximum(np.abs(gg - g_h), 1e-300)
            on = on & (gg / (s * F180) + (g_h / F180) * hc >= ik)
            gp = np.gradient(gg, s)[0]; g0 = gg[0]; F90 = math.sqrt(g0 ** 2 + g_h ** 2)
            k90 = 0.5 * ((gp + 2 * g0 / Rk) / F90 - (gp * g0 ** 2 + g_h ** 2 * g0 / Rk) / F90 ** 3) + (g_h / F90) * hc
            on_d = on_d and (k90 >= ik)
        if not on[0]:
            return on_d, float(Rk), False
        off = np.where(~on)[0]
        Re = float(s[-1]) if off.size == 0 else float(math.sqrt(s[off[0] - 1] * s[off[0]]))
        return on_d, Re, True

    BOOT = {}

    def classify(sw_c, gfun, r_m, a0, f500, ext, key, NEWF):
        """XR6's per-member classification (lines 380-413) against the host switches sw_c with a galaxy-region function."""
        e_gap = {g_: np.zeros(len(gal)) for g_, _ in GAPS}
        lab = np.array([""] * len(gal), dtype=object); nb = 0; Re_gal = np.full(len(gal), np.nan)
        for i in np.where(memb)[0]:
            j = int(idx[i]); c = cls[j]; S = sw_c[j]; r = r_m[i]
            e_i = Gc * float(cluster_Mb(c, f500, ext, np.array([r]))[0]) / r ** 2
            if r <= S["r_e"]:
                lab[i] = "a"
                for g_, _ in GAPS: e_gap[g_][i] = e_i
                continue
            lr = np.log(S["r"])
            at = lambda arr: float(np.interp(math.log(r), lr, arr))
            disc_on, Re, reach = gfun(Mbg[i], RHI[i], c["z"], a0, at(S["e"]), at(S["g"]), at(S["D"]), at(S["qb"]), r)
            Re_gal[i] = Re
            if (not disc_on) or (not reach):
                NEWF.append(dict(key=key, agc=gal[i]["agc"], disc_on=disc_on, Re_kpc=Re / KPC, RHI_kpc=RHI[i] / KPC))
            if r - Re <= S["r_e"]:
                lab[i] = "a (merged)"
                for g_, _ in GAPS: e_gap[g_][i] = e_i
                continue
            lab[i] = "b"; nb += 1
            Mcap = float(np.interp(math.log(S["r_e"]), lr, S["Mb"]))
            rho = r - Re
            for g_, minv in GAPS:
                e_gap[g_][i] = Gc * Mcap / rho ** 2 * transmit(rho, S["r_e"], minv)
        return e_gap, lab, nb, Re_gal

    def score_clusters(mode):
        """mode 'withdrawn' = XR6's switch and scenarios exactly (the control); 'kappa' = MS5's cap, operator A under both
        kappa readings and the uncapped reference, operator B beside them."""
        RES, CLASSF, NEWF, EDGES = {}, {}, [], {}
        for foot, a0 in A0.items():
            Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(Gc * Mbg * a0)
            for geo, dp in GEOS:
                r_m = np.zeros(len(gal)); x_m = np.zeros(len(gal)); ge = np.zeros(len(gal))
                for i in np.where(memb)[0]:
                    c = cls[idx[i]]; r = max(Rp_m[i] * dp, 0.05 * c["r500"])
                    r_m[i] = r; x_m[i] = r / c["r500"]
                    ge[i] = Gc * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / r ** 2
                lge = np.log10(ge[memb] / a0)
                if (foot, geo) not in BOOT: BOOT[(foot, geo)] = boot_err(Dobs, memb, lge)
                sobs, eobs = BOOT[(foot, geo)]
                for f500 in F500S:
                    for ext in EXTS:
                        key = f"{foot}/{geo}/{f500}/{ext}"
                        e_in = np.zeros(len(gal))
                        for i in np.where(memb)[0]:
                            c = cls[idx[i]]; r = r_m[i]
                            e_in[i] = Gc * float(cluster_Mb(c, f500, ext, np.array([r]))[0]) / r ** 2
                        scen = {}
                        if mode == "withdrawn":
                            sw = {j: cluster_switch(cls[j], a0, f500, ext, EF["VCAP_CAND"]) for j in used}
                            gfun = lambda Mg, Rk, z, a0_, e_, g_, D_, qb_, rh: galaxy_region(Mg, Rk, z, a0_, e_, g_, D_, qb_, EF["VCAP_CAND"])
                            e_gap, lab, nb, Re_gal = classify(sw, gfun, r_m, a0, f500, ext, key, NEWF)
                            if ext == "extended":
                                e0 = np.zeros(len(gal)); e0[memb] = fb_profile(x_m[memb], f500) * ge[memb]
                                scen["S0 XR4 switch, no cap (nu_RAR)"] = (e0, KCnu)
                            scen["S1 MOND-sector switch, no cap"] = (e_in, nu_mono_e)
                            for g_, _ in GAPS:
                                scen[f"S{2 + [x[0] for x in GAPS].index(g_)} capped, operator A, gap {g_}"] = (e_gap[g_], nu_mono_e)
                            scen["S5 capped, operator B (PM: all baryons in nu)"] = (e_in, nu_mono_e)
                            labs = {"withdrawn": (lab, nb)}
                        else:
                            sw = {j: cluster_switch_k(cls[j], a0, f500, ext, True) for j in used}
                            swu = {j: cluster_switch_k(cls[j], a0, f500, ext, False) for j in used}
                            labs = {}
                            for var in ("galaxy", "twofield"):
                                gfun = lambda Mg, Rk, z, a0_, e_, g_, D_, qb_, rh, var=var: galaxy_region_k(Mg, Rk, z, a0_, e_, g_, D_, qb_, rh, var)
                                e_gap, lab, nb, _ = classify(sw, gfun, r_m, a0, f500, ext, key + f"/kappa-{var}", NEWF)
                                labs[var] = (lab, nb)
                                for g_, _ in GAPS:
                                    scen[f"A kappa-{var} gap {g_}"] = (e_gap[g_], nu_mono_e)
                            gfun = lambda Mg, Rk, z, a0_, e_, g_, D_, qb_, rh: galaxy_region_k(Mg, Rk, z, a0_, e_, g_, D_, qb_, rh, "none")
                            e_gapu, labu, nbu, _ = classify(swu, gfun, r_m, a0, f500, ext, key + "/uncapped", [])
                            labs["uncapped"] = (labu, nbu)
                            for g_, _ in GAPS:
                                scen[f"A uncapped gap {g_}"] = (e_gapu[g_], nu_mono_e)
                            scen["B (PM: all baryons, unscreened)"] = (e_in, nu_mono_e)
                            if geo == "R_proj" and f500 == 0.13 and ext == "extended":
                                EDGES[foot] = {cls[j]["name"]: dict(kappa=sw[j]["r_e"] / MPC, uncapped=swu[j]["r_e"] / MPC,
                                                                    l_cap=lcap_e(cls[j]["z"]) / MPC, z=cls[j]["z"]) for j in used}
                        rows = {}
                        for sname, (ee, nuf) in scen.items():
                            Dp, Dq = predict(ee, a0, nuf)
                            sp, _ = regress(Dp, memb, lge); sq, _ = regress(Dq, memb, lge)
                            co, cp, sej = zero_point(Dobs, Dp, f"{foot}/{geo}")
                            rows[sname] = dict(slope_scalar=float(sp), sigma_scalar=float(abs(sobs - sp) / eobs),
                                               slope_subtract=float(sq), sigma_subtract=float(abs(sobs - sq) / eobs),
                                               zp_obs=float(co), zp_pred=float(cp), zp_err=float(sej), zp_sigma=float(abs(co - cp) / sej))
                        RES[key] = dict(obs=float(sobs), err=float(eobs), rows=rows,
                                        n_beyond={k_: int(v_[1]) for k_, v_ in labs.items()},
                                        n_members=int(memb.sum()))
                        if geo == "R_proj" and f500 == 0.13 and ext == "extended":
                            CLASSF[foot] = {k_: {c_: int(np.sum(v_[0][memb] == c_)) for c_ in ("a", "a (merged)", "b")} for k_, v_ in labs.items()}
        return RES, CLASSF, NEWF, EDGES

    # ---- C2 the withdrawn-form control
    set_cell(1.0, 2.5)
    RESw, CLw, NFw, _ = score_clusters("withdrawn")
    dc2 = 0.0
    for key, ref in XR6E["clusters"].items():
        mine = RESw[key]
        dc2 = max(dc2, abs(mine["obs"] - ref["obs"]), abs(mine["err"] - ref["err"]),
                  abs(mine["n_beyond"]["withdrawn"] - ref["n_beyond_cap"]))
        for sname, rv in ref["rows"].items():
            for k_, v_ in rv.items():
                dc2 = max(dc2, abs(mine["rows"][sname][k_] - v_))
    dcl = max(abs(CLw[f]["withdrawn"][c_] - XR6E["classification"][f][c_]) for f in A0 for c_ in ("a", "a (merged)", "b"))
    check("C2 CONTROL (EFE, withdrawn-form control): with XR6's own switch functions at p = 1, x_c0 = 2.5 this lane's scoring loop "
          "reproduces XR6's committed cluster table (24 variants x 6 scenarios x 8 numbers, members beyond the edge) and its "
          "classification exactly", f"max |diff| {dc2:.1e}; classification max |diff| {dcl}", dc2 < 1e-9 and dcl == 0)
    P(f"    [{time.time() - T0:.0f}s]")

    # ---- the scan
    CLU = {}
    for (p, x0) in CELLS:
        pe, xe = eff(p, x0); set_cell(pe, xe)
        RES, CLASSF, NEWF, EDGES = score_clusters("kappa")
        capA = [s_ for s_ in next(iter(RES.values()))["rows"] if s_.startswith("A kappa")]
        sig = [RES[k_]["rows"][s_][f_] for k_ in RES for s_ in capA for f_ in ("sigma_scalar", "sigma_subtract")]
        cen = [RES[k_]["rows"][s_][f_] for k_ in RES if k_.split("/")[1:] == ["R_proj", "0.13", "extended"]
               for s_ in capA for f_ in ("sigma_scalar", "sigma_subtract")]
        sigU = [RES[k_]["rows"][s_][f_] for k_ in RES for s_ in RES[k_]["rows"] if s_.startswith("A uncapped")
                for f_ in ("sigma_scalar", "sigma_subtract")]
        zpA = [RES[k_]["rows"][s_]["zp_sigma"] for k_ in RES for s_ in capA]
        nf = len(NEWF)
        nf_by = {var: sum(1 for x_ in NEWF if x_["key"].endswith("/kappa-" + var)) for var in ("galaxy", "twofield")}
        by_scen = {s_: [min(RES[k_]["rows"][s_][f_] for k_ in RES for f_ in ("sigma_scalar", "sigma_subtract")),
                        max(RES[k_]["rows"][s_][f_] for k_ in RES for f_ in ("sigma_scalar", "sigma_subtract"))]
                   for s_ in next(iter(RES.values()))["rows"]}
        by_form = {f_: [min(RES[k_]["rows"][s_][f_] for k_ in RES for s_ in capA), max(RES[k_]["rows"][s_][f_] for k_ in RES for s_ in capA)]
                   for f_ in ("sigma_scalar", "sigma_subtract")}
        inside = {f: {var: (CLASSF[f][var]["a"] + CLASSF[f][var]["a (merged)"]) / 314.0 for var in ("galaxy", "twofield", "uncapped")} for f in A0}
        edges_k = [v_["kappa"] for f in A0 for v_ in EDGES[f].values()]
        CLU[ck(p, x0)] = dict(sigma_range=[min(sig), max(sig)], sigma_central=[min(cen), max(cen)], sigma_uncapped=[min(sigU), max(sigU)],
                              zp_sigma_range=[min(zpA), max(zpA)], new_failures=nf, new_failures_by_reading=nf_by, new_failure_examples=NEWF[:20],
                              sigma_by_scenario=by_scen, sigma_by_form=by_form,
                              fraction_inside=inside, classification=CLASSF, cluster_edges_Mpc=[min(edges_k), max(edges_k)],
                              observed=[RES["canonical/R_proj/0.13/extended"]["obs"], RES["canonical/R_proj/0.13/extended"]["err"]],
                              central_slopes={f: {s_: [RES[f"{f}/R_proj/0.13/extended"]["rows"][s_]["slope_scalar"],
                                                       RES[f"{f}/R_proj/0.13/extended"]["rows"][s_]["slope_subtract"]]
                                                  for s_ in capA} for f in A0},
                              pass_=max(sig) <= 2.0 and nf == 0, pass_central=max(cen) <= 2.0 and nf == 0)
        if (p, x0) == (1.0, 2.5):
            OUT["numbers"]["clusters_full_table_converged_cell"] = RES
        P(f"  {ck(p, x0):9s} cluster edges (kappa) {min(edges_k):.2f}-{max(edges_k):.2f} Mpc; members inside (a + merged, canonical) "
          f"galaxy-kappa {inside['canonical']['galaxy']:.2f} two-field {inside['canonical']['twofield']:.2f} uncapped {inside['canonical']['uncapped']:.2f}; "
          f"slope sigma, operator A kappa: all variants {min(sig):.2f}-{max(sig):.2f}, central {min(cen):.2f}-{max(cen):.2f} "
          f"(uncapped {min(sigU):.2f}-{max(sigU):.2f}); zero point {min(zpA):.2f}-{max(zpA):.2f} sigma; new failures {nf_by} -> "
          f"{'PASS' if CLU[ck(p, x0)]['pass_'] else ('central pass' if CLU[ck(p, x0)]['pass_central'] else 'fail')}   [{time.time() - T0:.0f}s]")
        P(f"      by form (operator A kappa): scalar sum {by_form['sigma_scalar'][0]:.2f}-{by_form['sigma_scalar'][1]:.2f}, subtract "
          f"{by_form['sigma_subtract'][0]:.2f}-{by_form['sigma_subtract'][1]:.2f};  by scenario (max over systematics): "
          + ", ".join(f"{s_.replace('A kappa-', '').replace(' gap ', '/')}: {v_[1]:.1f}" for s_, v_ in by_scen.items()))
    OUT["numbers"]["clusters"] = CLU
    k0 = CLU["p1_x2.5"]
    P(f"  K1 (reported) the kappa form at the converged cell: cluster edges {k0['cluster_edges_Mpc'][0]:.2f}-{k0['cluster_edges_Mpc'][1]:.2f} Mpc "
      f"(XR6's withdrawn form: 3.53-3.73); slope sigma {k0['sigma_range'][0]:.2f}-{k0['sigma_range'][1]:.2f} (XR6: 2.18-6.63)")

    # ============================================================================================ PART 3 dwarfs
    banner("PART 3 -- THE LOCAL VOLUME DWARFS (N = 92): statistic C with each host's kappa-capped region")
    d = KD.load(ups_v=2.0)
    lsig = np.log10(np.array([g_["sig"] for g_ in d])); lM = np.log10(np.array([g_["Mb"] for g_ in d]))
    lrh = np.log10(np.array([g_["rh"] / KD.PC for g_ in d]))
    dmw = np.array([g_["dmw"] for g_ in d]); dm31 = np.array([g_["dm31"] for g_ in d])
    gNe0 = np.array([g_["gNe"] for g_ in d])
    fmw = np.where(np.isfinite(dmw) & (dmw > 0), Gc * KD.M_MW_BAR * MSUN / (np.where(np.isfinite(dmw) & (dmw > 0), dmw, 1.0) * KD.KPC) ** 2, 0.0)
    f31 = np.where(np.isfinite(dm31) & (dm31 > 0), Gc * KD.M_M31_BAR * MSUN / (np.where(np.isfinite(dm31) & (dm31 > 0), dm31, 1.0) * KD.KPC) ** 2, 0.0)
    host_mw = fmw >= f31
    r_host = np.where(host_mw, dmw, dm31) * KD.KPC
    DWB = {}
    for foot, a0 in A0.items():
        lge = np.log10(KD.true_external_field(gNe0, a0) / a0)
        q = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lge]
        cobs, _ = KD.partial_slope(lsig, q); eobs = KD.boot_slope(lsig, q)
        DWB[foot] = (q, float(cobs), float(eobs))

    def pred_slope(gNe_new, foot):
        q, _, _ = DWB[foot]
        dd = [dict(g_, gNe=gg) for g_, gg in zip(d, gNe_new)]
        return KD.partial_slope(np.log10(KD.predict_sigma(dd, A0[foot])), q)[0]

    def score_dwarfs(mode):
        out = {}
        for foot, a0 in A0.items():
            _, cobs, eobs = DWB[foot]
            for cgm in (1.0, 1.5, 2.0):
                edges = {}
                for hname, Mh in (("MW", KD.M_MW_BAR * cgm), ("M31", KD.M_M31_BAR * cgm)):
                    rr = np.geomspace(5.0 * KPC, 6.0 * MPC, 5000)
                    e_, g_, D_, qb_ = ms_profile(rr, np.full_like(rr, Mh * MSUN), a0)
                    if mode == "withdrawn":
                        on_ = switch_state(0.0, D_, qb_, g_, EF["VCAP_CAND"])[0]
                    else:
                        on_ = switch_state(0.0, D_, qb_, g_, math.inf)[0] & (rr <= lcap_e(0.0))
                    edges[hname] = region_edge(rr, on_)[0]
                inside = np.where(host_mw, r_host < edges["MW"], r_host < edges["M31"])
                sp = pred_slope(np.where(inside, gNe0 * cgm, 1e-30), foot)
                out[f"{foot}/{cgm}"] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs), n_outside=int((~inside).sum()),
                                            edges_Mpc={k_: v_ / MPC for k_, v_ in edges.items()}, obs=cobs, err=eobs)
        return out

    set_cell(1.0, 2.5)
    DWw = score_dwarfs("withdrawn")
    dc3 = 0.0
    for foot in A0:
        for cgm in (1.0, 1.5, 2.0):
            ref = XR6E["dwarfs"][foot]["candidate"][f"cgm{cgm}"]; mine = DWw[f"{foot}/{cgm}"]
            dc3 = max(dc3, abs(ref["slope"] - mine["slope"]), abs(ref["sigma"] - mine["sigma"]), abs(ref["n_outside"] - mine["n_outside"]),
                      *(abs(ref["edges_Mpc"][h_] - mine["edges_Mpc"][h_]) for h_ in ("MW", "M31")))
        dc3 = max(dc3, abs(XR6E["dwarfs"][foot]["obs"] - DWB[foot][1]), abs(XR6E["dwarfs"][foot]["err"] - DWB[foot][2]))
    check("C3 CONTROL (dwarfs, withdrawn-form control): XR6's committed candidate rows (host baryons x1/x1.5/x2, both footings: "
          "slope, sigma, dwarfs outside, host edges) and the observed statistic are reproduced exactly", f"max |diff| {dc3:.1e}", dc3 < 1e-9)
    DWT = {}
    for (p, x0) in CELLS:
        pe, xe = eff(p, x0); set_cell(pe, xe)
        rows = score_dwarfs("kappa")
        sg = [v_["sigma"] for v_ in rows.values()]
        DWT[ck(p, x0)] = dict(rows=rows, sigma_range=[min(sg), max(sg)], pass_=max(sg) <= 2.0,
                              fraction_inside={k_: 1 - v_["n_outside"] / 92.0 for k_, v_ in rows.items()})
        r1 = rows["canonical/1.0"]
        P(f"  {ck(p, x0):9s} host edges (x1, canonical) MW {r1['edges_Mpc']['MW']:.2f} / M31 {r1['edges_Mpc']['M31']:.2f} Mpc; dwarfs inside "
          f"{92 - r1['n_outside']}/92; statistic C sigma {min(sg):.2f}-{max(sg):.2f} (x1 canonical {r1['sigma']:.2f}) -> "
          f"{'PASS' if DWT[ck(p, x0)]['pass_'] else 'fail'}")
    OUT["numbers"]["dwarfs"] = DWT

    # ============================================================================================ PART 4 Coma UDGs
    banner("PART 4 -- THE COMA UDGs: inside Coma's kappa-capped region (EFE of Coma's baryons) or beyond it (screened)")
    run, budget, MODELS, BETA, UDG, A0L, ZCOMA, R500C, kpc23, G23, wmean = (EF[k_] for k_ in (
        "run", "budget", "MODELS", "BETA", "UDG", "A0L", "ZCOMA", "R500C", "kpc23", "G23", "wmean"))
    foot_of = lambda a0: "canonical" if a0 == A0L["canonical"] else "alt"

    def coma_profiles(mode):
        CO = {}
        for foot, a0 in A0L.items():
            for mname, gfn in MODELS.items():
                for f500 in F500S:
                    rk = np.geomspace(50.0, 40000.0, 5000)
                    Mtot = np.array([gfn(x_) for x_ in rk]) * (rk * kpc23) ** 2 / G23
                    Mbk = fb_profile(rk / R500C, f500) * Mtot
                    rm = rk * kpc23
                    e_, g_, D_, qb_ = ms_profile(rm, Mbk, a0)
                    if mode == "withdrawn":
                        on_ = switch_state(ZCOMA, D_, qb_, g_, EF["VCAP_CAND"])[0]
                    else:
                        on_ = switch_state(ZCOMA, D_, qb_, g_, math.inf)[0] & (rm <= lcap_e(ZCOMA))
                    CO[f"{foot}/{mname}/{f500}"] = dict(edge_m=region_edge(rm, on_)[0], prof=(rm, Mbk, e_, g_, D_, qb_))
        return CO

    # ---- C4 withdrawn-form control
    set_cell(1.0, 2.5)
    COw = coma_profiles("withdrawn")
    dce = max(abs(COw[k_]["edge_m"] / kpc23 - v_["capped"]) for k_, v_ in XR6E["udg"]["coma_edges_kpc"].items())
    arm_C = lambda a0, m_, k_, f500=0.13, **kw: run(a0, MODELS[m_], k_, "baryonic", "sphere", f500=f500, **kw)
    CAND = {f"{f}/{f5}": arm_C(A0L[f], BETA, "dmean", f500=f5) for f in A0L for f5 in F500S}
    fbs = (max(CAND[f"canonical/{f5}"]["me"] for f5 in F500S) - min(CAND[f"canonical/{f5}"]["me"] for f5 in F500S)) / 2
    _, systC = budget(arm_C, extra={"f_b(R500) template 0.10-0.157 (new)": fbs})
    sigC = [CAND[f"{f}/0.13"]["me"] / math.sqrt(CAND[f"{f}/0.13"]["se"] ** 2 + systC ** 2) for f in A0L]
    refU = XR6E["udg"]["candidate"]
    dc4 = max(max(abs(CAND[k_]["me"] - v_) for k_, v_ in refU["me"].items()), abs(systC - refU["floor"]),
              max(abs(a_ - b_) for a_, b_ in zip(sigC, refU["sigma"])))
    check("C4 CONTROL (UDGs, withdrawn-form control): XR6's committed Coma numbers -- Coma's capped edges (3 mass models x 3 f_b x "
          "2 footings), the candidate offsets (6), the recomputed floor and the two sigmas -- are reproduced exactly",
          f"edges max |diff| {dce:.1e} kpc; offsets/floor/sigma max |diff| {dc4:.1e} (floor {systC:.4f}, sigma {sigC[0]:.2f}/{sigC[1]:.2f})",
          dce < 1e-6 and dc4 < 1e-9)

    def make_arm(CO, gap, variant):
        """the candidate's arm at this cell: inside Coma's region the EFE of Coma's baryons (XR6's 'baryonic' arm); beyond it
        the member's own region (galaxy_region_k, this kappa reading) and the screened field transmitted across the gap
        (XR6's first-infall treatment).  A UDG whose own region no longer covers r_1/2 (disc_on False: the kappa condition
        across the external field) is scored NEWTONIAN (its carrier cleared) -- a new failure, never dropped."""
        minv = dict(GAPS)[gap]
        cache = {}

        def efield(a0, m_, k_, f500):
            key = (foot_of(a0), m_, k_, f500)
            if key in cache: return cache[key]
            Cm = CO[f"{key[0]}/{m_}/{f500}"]; rm, Mbk, e_, g_, D_, qb_ = Cm["prof"]; em = Cm["edge_m"]
            gfn = MODELS[m_]; ef, ins, don = [], [], []
            for u in UDG:
                r = u[k_]; rmr = r * kpc23
                if rmr <= em:
                    ef.append(float(fb_profile(np.array(r / R500C), f500)) * gfn(r)); ins.append(True); don.append(True)
                else:
                    at = lambda arr: float(np.interp(math.log(rmr), np.log(rm), arr))
                    d_on, Re, reach = galaxy_region_k(u["Mst"], u["r12"], ZCOMA, a0, at(e_), at(g_), at(D_), at(qb_), rmr, variant)
                    Mcap = float(np.interp(math.log(em), np.log(rm), Mbk)); rho = rmr - Re
                    ef.append(G23 * Mcap / rho ** 2 * transmit(rho, em, minv)); ins.append(False); don.append(bool(d_on and reach))
            cache[key] = (ef, ins, don)
            return cache[key]

        def arm(a0, m_, k_, f500=0.13, **kw):
            ef, _, don = efield(a0, m_, k_, f500)
            R_ = run(a0, MODELS[m_], k_, "given", "sphere", efield=ef, **kw)
            if not all(don):                                                 # Newtonian UDGs (new failures), L23's offset form
                oe = np.array(R_["oe"], float)
                for i, u in enumerate(UDG):
                    if not don[i]:
                        gobs = u["gobs"] * kw.get("sig_scale", 1.0) ** 2 / kw.get("dist_scale", 1.0); gbar = u["gbar"] * kw.get("ml_scale", 1.0)
                        oe[i] = math.log10(gobs) - math.log10(gbar)
                me, se = wmean(oe, R_["err"])
                R_ = dict(R_, oe=oe, me=me, se=se)
            return R_
        return arm, efield

    UDT = {}
    for (p, x0) in CELLS:
        pe, xe = eff(p, x0); set_cell(pe, xe)
        CO = coma_profiles("kappa")
        edges = [v_["edge_m"] / kpc23 / 1e3 for v_ in CO.values()]
        res = {}
        floor = None
        for var in ("galaxy", "twofield"):
            for gap, _ in GAPS:
                arm, efield = make_arm(CO, gap, var)
                if var == "galaxy" and gap == "Dirichlet":
                    cand = {f"{f}/{f5}": arm(A0L[f], BETA, "dmean", f500=f5) for f in A0L for f5 in F500S}
                    fbs_ = (max(cand[f"canonical/{f5}"]["me"] for f5 in F500S) - min(cand[f"canonical/{f5}"]["me"] for f5 in F500S)) / 2
                    _, floor = budget(arm, extra={"f_b(R500) template 0.10-0.157 (new)": fbs_})
                for f in A0L:
                    R_ = arm(A0L[f], BETA, "dmean", f500=0.13)
                    ef3, in3, don3 = efield(A0L[f], BETA, "dmean", 0.13)
                    res[f"{var}/{gap}/{f}"] = dict(me=R_["me"], se=R_["se"], sigma=R_["me"] / math.sqrt(R_["se"] ** 2 + floor ** 2),
                                                  n_inside=int(sum(in3)), n_newtonian=int(sum(not x for x in don3)),
                                                  n_inside_proj=int(sum(efield(A0L[f], BETA, "dproj", 0.13)[1])))
        sg = [v_["sigma"] for v_ in res.values()]
        nnew = max(v_["n_newtonian"] for v_ in res.values())
        UDT[ck(p, x0)] = dict(coma_edge_Mpc=[min(edges), max(edges)], rows=res, floor=floor, sigma_range=[min(sg), max(sg)],
                              newtonian_udgs_max=nnew, pass_=max(sg) < 2.0 and nnew == 0, pass_3sigma=max(sg) < 3.0)
        r0 = res["galaxy/Dirichlet/canonical"]; r2 = res["twofield/Dirichlet/canonical"]
        P(f"  {ck(p, x0):9s} Coma edge {min(edges):.2f}-{max(edges):.2f} Mpc; UDGs inside (Einasto 3-D / projected, canonical beta) "
          f"{r0['n_inside']}/11 / {r0['n_inside_proj']}/11; offset (galaxy-kappa, Dirichlet) {r0['me']:+.3f} / "
          f"{res['galaxy/Dirichlet/alt']['me']:+.3f} dex, two-field {r2['me']:+.3f} ({r2['n_newtonian']} UDG(s) Newtonian); floor "
          f"{floor:.3f}; sigma over gaps and kappa readings {min(sg):.2f}-{max(sg):.2f} -> {'PASS' if UDT[ck(p, x0)]['pass_'] else 'fail'}"
          f"   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["udg"] = UDT

    # ============================================================================================ PART 5 SPARC
    banner("PART 5 -- ROTATION CURVES (SPARC, 175): the fully-on radius at z = 0 against 3 R_last")
    SP = []
    with open(os.path.join(REPO, "real_research", "data", "sparc_master_clean.csv")) as fh:
        for row in csv.DictReader(fh):
            fn = os.path.join(REPO, "real_research", "data", "sparc_data", f"{row['name']}_rotmod.dat")
            if not os.path.exists(fn): continue
            rad = [float(l.split()[0]) for l in open(fn) if l.strip() and not l.startswith("#")]
            SP.append(dict(name=row["name"], Mb=(0.5 * float(row["L36"]) + 1.33 * float(row["MHI"])) * 1e9, Rlast_kpc=max(rad)))
    P(f"    {len(SP)} SPARC galaxies with rotmod files; M_b = 0.5 L[3.6] + 1.33 M_HI; R_last {min(s_['Rlast_kpc'] for s_ in SP):.1f}-"
      f"{max(s_['Rlast_kpc'] for s_ in SP):.1f} kpc")
    RCT = {}
    for (p, x0) in CELLS:
        pe, xe = eff(p, x0)
        worst = (np.inf, None); nfail = 0
        for s_ in SP:
            for foot, a0 in A0L6.items():
                rf_ = edge_numeric_k(s_["Mb"], a0, 0.0, xe, pe, wfac=1 + W_GATE) / Mpc * 1e3
                ratio = rf_ / s_["Rlast_kpc"]
                if ratio < worst[0]: worst = (ratio, f"{s_['name']} ({foot}, r_full {rf_:.0f} kpc, R_last {s_['Rlast_kpc']:.1f})")
                nfail += int(ratio < 3.0)
        ref = {lab: edge_numeric_k(Mbv, A0L6["canonical"], 0.0, xe, pe, wfac=1 + W_GATE) / Mpc * 1e3 for lab, Mbv in (("L* 1e11", 1e11), ("dwarf 1e9", 1e9))}
        RCT[ck(p, x0)] = dict(min_ratio=worst[0], worst=worst[1], n_below_3=nfail, pass_=nfail == 0, reference_full_kpc=ref)
        P(f"  {ck(p, x0):9s} fully-on radius: L* {ref['L* 1e11']:.0f} kpc, dwarf 1e9 {ref['dwarf 1e9']:.0f} kpc; min r_full/R_last {worst[0]:.1f} "
          f"({worst[1]}); galaxy-footings below 3: {nfail} -> {'PASS' if nfail == 0 else 'fail'}")
    OUT["numbers"]["rotation_curves"] = RCT

    # ============================================================================================ PART 6 where each passes
    banner("PART 6 -- DIAGNOSTIC: the threshold at which each z ~ 0 liability would pass, beyond the scanned cells "
           "(x_c,eff at the sample's epoch; reported, not gated)")
    XS = (2.5, 5.0, 10.0, 20.0, 40.0, 70.0, 100.0, 150.0, 200.0, 300.0, 500.0, 1000.0)
    DIAG = {"dwarfs": {}, "udg": {}, "LG_p0": {}, "clusters": {}}
    if not MUTATE:
        for x in XS:                                                      # dwarfs at z = 0: x_c,eff(0) = x
            set_cell(1.0, x); rows = score_dwarfs("kappa")
            DIAG["dwarfs"][x] = dict(sigma_max=max(v_["sigma"] for v_ in rows.values()),
                                     n_inside_min=min(92 - v_["n_outside"] for v_ in rows.values()),
                                     MW_edge_Mpc=rows["canonical/1.0"]["edges_Mpc"]["MW"])
        P("  dwarfs, statistic C (worst of x1-x2 and footings) vs x_c,eff(0): " + "; ".join(
            f"{x:g}: {v_['sigma_max']:.2f}s ({v_['n_inside_min']} in, MW edge {v_['MW_edge_Mpc'] * 1e3:.0f} kpc)" for x, v_ in DIAG["dwarfs"].items()))
        for x in XS:                                                      # Coma UDGs at z = 0.023: x_c,eff = x E^2(0.023)
            set_cell(1.0, x); CO = coma_profiles("kappa"); arm, efield = make_arm(CO, "Dirichlet", "galaxy")
            cand = {f"{f}/{f5}": arm(A0L[f], BETA, "dmean", f500=f5) for f in A0L for f5 in F500S}
            fbs_ = (max(cand[f"canonical/{f5}"]["me"] for f5 in F500S) - min(cand[f"canonical/{f5}"]["me"] for f5 in F500S)) / 2
            _, fl_ = budget(arm, extra={"f_b(R500) template 0.10-0.157 (new)": fbs_})
            sg_ = [cand[f"{f}/0.13"]["me"] / math.sqrt(cand[f"{f}/0.13"]["se"] ** 2 + fl_ ** 2) for f in A0L]
            DIAG["udg"][x] = dict(sigma_max=max(sg_), offset=cand["canonical/0.13"]["me"],
                                  n_inside=int(sum(efield(A0L["canonical"], BETA, "dmean", 0.13)[1])),
                                  edge_Mpc=CO[f"canonical/{BETA}/0.13"]["edge_m"] / kpc23 / 1e3)
        P("  Coma UDGs (galaxy-kappa, Dirichlet gap, floor recomputed) vs x_c0 (x_c,eff(0.023) = 1.022 x_c0): " + "; ".join(
            f"{x:g}: {v_['sigma_max']:.2f}s ({v_['offset']:+.2f} dex, {v_['n_inside']} in, edge {v_['edge_Mpc']:.2f})" for x, v_ in DIAG["udg"].items()))
        lgc = []
        for x in XS:                                                      # the LG with a CONSTANT threshold (p = 0)
            for foot, a0 in A0L6.items():
                tb = table_k(MB_LG, a0, x, 0.0)
                for hist in HISTS:
                    lgc.append(dict(x=x, foot=foot, Mb=MB_LG, a0=a0, xc0=x, p=0.0, hist=hist, edge="ms_num", table=tb))
        R_lg = run_cells(lgc)
        for c, v in zip(lgc, R_lg):
            DIAG["LG_p0"].setdefault(c["x"], {})[f"{c['foot']}/{c['hist']}"] = float(v)
        P("  LG R_0 [Mpc] with a CONSTANT threshold (p = 0), M_b 1.145e11, decay history canonical/alt: " + "; ".join(
            f"{x:g}: {v_['canonical/decay']:.3f}/{v_['alt/decay']:.3f} (full {v_['canonical/full']:.3f})" for x, v_ in DIAG["LG_p0"].items()))
        for x in (40.0, 100.0, 300.0):                                    # clusters (z = 0.02-0.06)
            set_cell(1.0, x); RES_, CLF_, NF_, ED_ = score_clusters("kappa")
            capA_ = [s_ for s_ in next(iter(RES_.values()))["rows"] if s_.startswith("A kappa")]
            sg_ = [RES_[k_]["rows"][s_][f_] for k_ in RES_ for s_ in capA_ for f_ in ("sigma_scalar", "sigma_subtract")]
            DIAG["clusters"][x] = dict(sigma_range=[min(sg_), max(sg_)], new_failures=len(NF_),
                                       inside_galaxy=(CLF_["canonical"]["galaxy"]["a"] + CLF_["canonical"]["galaxy"]["a (merged)"]) / 314.0,
                                       edges_Mpc=[min(v_["kappa"] for v_ in ED_["canonical"].values()), max(v_["kappa"] for v_ in ED_["canonical"].values())])
        P("  clusters, operator A kappa, all variants vs x_c0: " + "; ".join(
            f"{x:g}: {v_['sigma_range'][0]:.2f}-{v_['sigma_range'][1]:.2f}s ({v_['inside_galaxy']:.2f} inside, edges "
            f"{v_['edges_Mpc'][0]:.2f}-{v_['edges_Mpc'][1]:.2f} Mpc, new failures {v_['new_failures']})" for x, v_ in DIAG["clusters"].items()))
        first = lambda d_, lim: next((x for x in XS if x in d_ and d_[x]["sigma_max"] <= lim), None)
        lg_band = [x for x in XS if all(abs(math.log10(DIAG["LG_p0"][x][f"{f}/decay"] / R0M)) <= BAND for f in A0L6)]
        check("P6 (reported) WHERE EACH z ~ 0 LIABILITY WOULD PASS: the smallest scanned x_c,eff at which the dwarf statistic and "
              "the Coma UDGs fall to 2 sigma, against the constant thresholds that put the LG in its band",
              f"dwarfs <= 2 sigma first at x_c,eff(0) = {first(DIAG['dwarfs'], 2.0)} (<= 3 sigma: {first(DIAG['dwarfs'], 3.0)}); "
              f"UDGs <= 2 sigma first at x_c0 = {first(DIAG['udg'], 2.0)} (<= 3 sigma: {first(DIAG['udg'], 3.0)}); LG in band (decay, "
              f"both footings, constant threshold) at x_c = {lg_band or 'none of the scanned values'}", True, load_bearing=False)
        OUT["numbers"]["diagnostic_where_each_passes"] = {k_: {str(x): v_ for x, v_ in d_.items()} for k_, d_ in DIAG.items()}

    # ============================================================================================ E1 the edges move
    banner("E1  THE REGIONS SHRINK AS THE DOOR SAYS (MUTATE freezes the threshold)")
    e_lg = {k_: LGT[k_]["edge_z0_Mpc"]["canonical/1.145e+11"] for k_ in ("p1_x2.5", "p1_x20")}
    e_co = {k_: UDT[k_]["coma_edge_Mpc"][0] for k_ in ("p1_x2.5", "p1_x20")}
    want = math.sqrt(20.0 / 2.5)
    rl, rc_ = e_lg["p1_x2.5"] / e_lg["p1_x20"], e_co["p1_x2.5"] / e_co["p1_x20"]
    check("E1 THE REGIONS SHRINK: from x_c0 = 2.5 to 20 (p = 1) the LG's z = 0 edge and Coma's kappa edge fall by sqrt(8) = 2.83 "
          "within 5% -- MUTATE (threshold frozen) must fail this", f"LG {e_lg['p1_x2.5']:.3f} -> {e_lg['p1_x20']:.3f} Mpc (ratio {rl:.3f}); "
          f"Coma {e_co['p1_x2.5']:.3f} -> {e_co['p1_x20']:.3f} Mpc (ratio {rc_:.3f})", abs(rl / want - 1) < 0.05 and abs(rc_ / want - 1) < 0.05)

    # ============================================================================================ summary
    banner("SUMMARY (per cell: LG | EFE clusters | EFE dwarfs | Coma UDGs | rotation curves)")
    for (p, x0) in CELLS:
        k_ = ck(p, x0)
        P(f"  {k_:9s} LG {'PASS' if LGT[k_]['pass_'] else 'fail'} (decay dex {min(LGT[k_]['dex_decay'].values()):+.3f}..{max(LGT[k_]['dex_decay'].values()):+.3f}) | "
          f"clusters {'PASS' if CLU[k_]['pass_'] else 'fail'} ({CLU[k_]['sigma_range'][0]:.1f}-{CLU[k_]['sigma_range'][1]:.1f} s, new fail "
          f"{CLU[k_]['new_failures']}) | dwarfs {'PASS' if DWT[k_]['pass_'] else 'fail'} ({DWT[k_]['sigma_range'][0]:.1f}-{DWT[k_]['sigma_range'][1]:.1f} s) | "
          f"UDGs {'PASS' if UDT[k_]['pass_'] else 'fail'} ({UDT[k_]['sigma_range'][0]:.1f}-{UDT[k_]['sigma_range'][1]:.1f} s) | RC "
          f"{'PASS' if RCT[k_]['pass_'] else 'fail'} (min {RCT[k_]['min_ratio']:.1f})")
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
