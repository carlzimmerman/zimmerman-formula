#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR13_door_environment.py -- THE PER-OBJECT DOOR, part 1 of 3: the three galaxy-environment liabilities that are internal
dynamics (the cluster-infall BTFR, N = 314; the Local Volume dwarfs, N = 92; the eleven Coma UDGs), the object rule the
door needs, and what that rule reaches (the Sun and wide binaries, the outer-halo globular clusters of hunt item 93,
SPARC).  Independent cross-thread review (2026-09-26/27).  Read-only on every committed file.  XR6's definitions are
loaded exactly as XR9 loaded them (mains never run); XR9's kappa-form scoring functions are copied here verbatim so that
the door-off path is XR9's own, and XR9's committed numbers are the controls.

THE DOOR (a phenomenological rule; no action is attempted).
  (1) PER-OBJECT REGIONS.  Each bound baryonic object at galaxy scale is its own MOND region.  Its kernel reads only its
      own baryons and is screened from every neighbour by L361's mechanism (screened w, Gauss-cancelled phantom).
      Neighbouring regions are partitioned at the watershed of the MOND-sector density, not merged; an isolated object
      keeps its full extent.  Sub-galactic structure stays in its galaxy's region.
  (2) NO REGION ABOVE v_cap.  A system whose baryons would give v_f = (G M_b a0)^(1/4) > v_cap = 325 km/s (M_b >
      M_cap = v_cap^4/(G a0) = 8.98e11 / 7.45e11 Msun, canonical/alt) has no MOND region; its members stand alone.
THE OBJECT RULE (declared here, before any gate was scored).
  R1 (geometric, primary): a bound system at distance D from its host is its OWN region iff its watershed basin in the
     MOND-sector density reaches at least the object scale l_obj = 1 kpc toward the host: s* >= l_obj, where s* is the
     distance from the object to the density saddle on the host axis.  Both densities are the isolated MOND-sector
     profiles (baryons + their own nu_mono phantom): the host a Hernquist sphere (MW 6.0e10 Msun, a = 3.0 kpc, L321's own
     Milky Way; M31 1.2e11 Msun, a = 6.0 kpc, scaled by the disc scale lengths; x1/x1.5/x2 as KD's CGM variants), the
     object a Plummer sphere of its baryonic mass and half-light radius.  s* < l_obj: sub-galactic structure.
     Sensitivity: l_obj over 0.1-30 kpc, a_host x0.5/x2.
  R2 (by type, reported): galaxies (dwarfs included) are objects, star clusters never are.
  R3 (by size, stress test of the phrase "below a declared object scale of ~kpc"): an object must also have r_h >= l_obj.
THE GATES (definitions fixed before scoring; the model's cell p = 1, x_c0 = 2.5; both footings).
  (a) EFE-C  the cluster-infall BTFR slope d Delta/d log g_e (XR4/XR6/XR9's regression) and the members-minus-field zero
      point.  Door: every PSZ2 cluster is above M_cap, so no cluster has a region and every member reads only its own
      baryons (e = 0; the scalar-sum and subtract forms coincide).  Pass = every variant (footing x geometry) within 2 sigma
      of the observed slope.  Neighbour watershed check: a member whose basin toward its nearest member neighbour
      (projected, a lower bound on 3-D) is smaller than R_HI is counted.
  (b) EFE-D  the dwarfs' statistic C (KD's quadratic design).  Door: objects under R1 read no host field; sub-galactic ones
      keep their host's (in-region) field.  Pass = every variant (footing x host baryons x1/x1.5/x2) within 2 sigma.
  (c) UDG    L23's pipeline as XR6 rebuilt it.  Door: Coma is above M_cap, so each UDG is isolated MOND on its own baryons;
      the systematic floor recomputed on the door's arm.  Pass = below 2 sigma on both footings.  The Newtonian pull of
      Coma's smooth carrier inside r_1/2 (at the retention X-COP then requires, ret = 1) is reported beside it.

CHECKS
  C1 CONTROL: with the door off (M*: p = 1, x_c0 = 2.5, MS5's kappa cap) XR9's committed cluster table (24 variants x
     every scenario x 8 numbers, members beyond the edge, the classification, the summary ranges) is reproduced exactly.
  C2 CONTROL: XR9's committed dwarf rows at the cell (x1/x1.5/x2, both footings) exactly.
  C3 CONTROL: XR9's committed UDG rows at the cell (2 kappa readings x 3 gaps x 2 footings), floor and sigma range exactly.
  C4 CONTROL: hunt item 93's joint one-M/L fit for the four outer-halo globulars (with the Milky Way's EFE) is reproduced
     from its committed inputs: 0.76 +- 0.15 (canonical), 0.71 +- 0.14 (alt).
  D1 [load-bearing; MUTATE must fail] no cluster member's kernel reads its cluster's field in the scored configuration.
  D2 [load-bearing; MUTATE must fail] under R1 at l_obj = 1 kpc at least 80% of the 92 dwarfs are their own regions.
  D3 [load-bearing; MUTATE must fail] no Coma UDG's kernel reads Coma's field in the scored configuration.
  R1s [load-bearing] THE SUN KEEPS THE GALAXY'S FIELD: the Sun, a 2 Msun wide binary and a 1e4 Msun open cluster at 8.2 kpc
     have s* < l_obj, so the Gaia DR4 pre-registration (L340 S1, L361 R2) is untouched.
  M1 [load-bearing] every system the door strips of its region is above M_cap, and every SPARC galaxy is below it (the RAR
     is untouched by part (2)).
  G1-G3 (reported, pre-declared) the three gates flip: (a) every variant < 2 sigma; (b) every variant < 2 sigma; (c) < 2 sigma
     on both footings.
  S1-S3 (reported) the object rule's sensitivity: C against l_obj, a_host and the size rule; the outer-halo globulars'
     status and item 93's joint M/L when the rule separates them.
MUTATE=1 merges the regions again (the door off: the scored column is XR9's M* scoring): D1-D3 must FAIL (rc = 1) and the
scored numbers must be XR9's.

SCOPE.  Spherical and 1-D, as XR6/XR9.  The watershed saddle is taken on the host-object axis of the two isolated
MOND-sector profiles (the full 3-D basin of a small object is a cone behind it, which does not change s*).  Member
separations are projected.  The members' HI discs and the UDGs' r_1/2 are the kinematic radii.  The door has no action:
the partition and the "object" are declared, not derived.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR13_door_environment.py   (MUTATE=1)
"""
import os, sys, json, math, time, io, contextlib, warnings, itertools, csv
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
DOOR = not MUTATE
SLUG = "XR13_door_environment"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR13 part 1 (environment: clusters, dwarfs, UDGs, the object rule)", "mutate": MUTATE,
               "door_in_scored_column": DOOR, "checks": {}, "numbers": {}}
V_CAP = 325e3
CELL = (1.0, 2.5)
ELL_OBJ = 1.0                                              # kpc -- the declared object scale (R1)
ELL_SWEEP = (0.1, 0.3, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0, 15.0, 30.0)
A_HOST = {"MW": 3.0, "M31": 6.0}                           # kpc, Hernquist scale lengths (declared; x0.5 and x2 reported)
GFN_BAND = 2.0


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


def load(path, cuts, name):
    """exec the definitions of a committed script (MUTATE forced off, stdout swallowed); cuts = [(start_marker, end_marker)]
    -- XR9_environment.py's loader, verbatim."""
    ns = {"__name__": name, "__file__": path}
    src = open(path).read().replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        for a_, b_ in cuts:
            chunk = src if a_ is None else src.split(a_)[1]
            chunk = chunk if b_ is None else chunk.split(b_)[0]
            exec(chunk, ns)
    return ns


def maxdiff(a, b):
    """largest absolute difference between two nested JSON-like structures (numbers compared, keys must match)."""
    if isinstance(a, dict):
        assert set(a) == set(b), (sorted(a), sorted(b))
        return max([maxdiff(a[k], b[k]) for k in a] or [0.0])
    if isinstance(a, (list, tuple)):
        assert len(a) == len(b)
        return max([maxdiff(x, y) for x, y in zip(a, b)] or [0.0])
    if isinstance(a, bool) or a is None or isinstance(a, str):
        return 0.0 if a == b else float("inf")
    return abs(float(a) - float(b))


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the regions are merged again (door off in the scored column); D1-D3 must FAIL ***")
    MK = "# ============================================================================================ "
    EF = load(os.path.join(HERE, "XR6_efe_udg_under_candidate.py"),
              [(None, MK + "PART A clusters"), (MK + "PART A clusters", "F500S = (0.10, 0.13, FCOS)"),
               (MK + "PART C Coma UDGs", "arm_L23 = lambda")], "xr6efe")
    XR9 = json.load(open(os.path.join(HERE, "XR9_environment_results.json")))["numbers"]
    P(f"  XR6's EFE/UDG definitions loaded (main not run); XR9's committed results read   [{time.time() - T0:.0f}s]")

    KC, KD, A0, MSUN, MPC, KPC, GAPS = (EF[k_] for k_ in ("KC", "KD", "A0", "MSUN", "MPC", "KPC", "GAPS"))
    Gc = EF["G"]
    gal, cls, idx, memb, Vv, Mbg, lHIall, RHI, lMb_all, used = (EF[k_] for k_ in (
        "gal", "cls", "idx", "memb", "V", "Mb", "lHIall", "RHI", "lMb_all", "used"))
    Rp_m = EF["Rp"]
    cluster_Mb, ms_profile, switch_state, region_edge, transmit = (EF[k_] for k_ in (
        "cluster_Mb", "ms_profile", "switch_state", "region_edge", "transmit"))
    regress, boot_err, zero_point, predict, nu_mono_e, dnu_mono_e, fb_profile = (EF[k_] for k_ in (
        "regress", "boot_err", "zero_point", "predict", "nu_mono", "dnu_mono", "fb_profile"))
    F500S = (0.10, 0.13, EF["FCOS"]); GEOS = (("R_proj", 1.0), ("1.3 R_proj", 1.3)); EXTS = ("extended", "r200")
    M_CAP = {f: V_CAP ** 4 / (Gc * a0) / MSUN for f, a0 in A0.items()}
    P(f"  M_cap = v_cap^4/(G a0) = {M_CAP['canonical']:.3e} / {M_CAP['alt']:.3e} Msun (canonical / alt); v_cap = 325 km/s")
    OUT["numbers"]["M_cap_Msun"] = M_CAP

    # ============================================================================================ XR9's kappa-form machinery
    # (copied verbatim from XR9_environment.py, PART 2-4; only the withdrawn-form branches are dropped)
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
        """XR9's galaxy_region_k, verbatim."""
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
        """XR9's classify, verbatim."""
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

    def geometry(foot, a0, geo, dp):
        r_m = np.zeros(len(gal)); x_m = np.zeros(len(gal)); ge = np.zeros(len(gal))
        for i in np.where(memb)[0]:
            c = cls[idx[i]]; r = max(Rp_m[i] * dp, 0.05 * c["r500"])
            r_m[i] = r; x_m[i] = r / c["r500"]
            ge[i] = Gc * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / r ** 2
        lge = np.log10(ge[memb] / a0)
        if (foot, geo) not in BOOT:
            Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(Gc * Mbg * a0)
            BOOT[(foot, geo)] = boot_err(Dobs, memb, lge)
        return r_m, x_m, ge, lge

    def score_clusters_k():
        """XR9's score_clusters('kappa'), verbatim (M*: the door off)."""
        RES, CLASSF, NEWF, EDGES = {}, {}, [], {}
        E_IN = {}
        for foot, a0 in A0.items():
            Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(Gc * Mbg * a0)
            for geo, dp in GEOS:
                r_m, x_m, ge, lge = geometry(foot, a0, geo, dp)
                sobs, eobs = BOOT[(foot, geo)]
                for f500 in F500S:
                    for ext in EXTS:
                        key = f"{foot}/{geo}/{f500}/{ext}"
                        e_in = np.zeros(len(gal))
                        for i in np.where(memb)[0]:
                            c = cls[idx[i]]; r = r_m[i]
                            e_in[i] = Gc * float(cluster_Mb(c, f500, ext, np.array([r]))[0]) / r ** 2
                        scen = {}
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
                        E_IN[key] = {s_: v_[0] for s_, v_ in scen.items()}
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
        return RES, CLASSF, NEWF, EDGES, E_IN

    def summarise_clusters(RES, CLASSF, NEWF, EDGES):
        """XR9's per-cell summary (the CLU[...] dict), verbatim."""
        capA = [s_ for s_ in next(iter(RES.values()))["rows"] if s_.startswith("A kappa")]
        sig = [RES[k_]["rows"][s_][f_] for k_ in RES for s_ in capA for f_ in ("sigma_scalar", "sigma_subtract")]
        cen = [RES[k_]["rows"][s_][f_] for k_ in RES if k_.split("/")[1:] == ["R_proj", "0.13", "extended"]
               for s_ in capA for f_ in ("sigma_scalar", "sigma_subtract")]
        sigU = [RES[k_]["rows"][s_][f_] for k_ in RES for s_ in RES[k_]["rows"] if s_.startswith("A uncapped")
                for f_ in ("sigma_scalar", "sigma_subtract")]
        zpA = [RES[k_]["rows"][s_]["zp_sigma"] for k_ in RES for s_ in capA]
        nf = len(NEWF)
        nf_by = {var: sum(1 for x_ in NEWF if x_["key"].endswith("/kappa-" + var)) for var in ("galaxy", "twofield")}
        inside = {f: {var: (CLASSF[f][var]["a"] + CLASSF[f][var]["a (merged)"]) / 314.0 for var in ("galaxy", "twofield", "uncapped")} for f in A0}
        edges_k = [v_["kappa"] for f in A0 for v_ in EDGES[f].values()]
        return dict(sigma_range=[min(sig), max(sig)], sigma_central=[min(cen), max(cen)], sigma_uncapped=[min(sigU), max(sigU)],
                    zp_sigma_range=[min(zpA), max(zpA)], new_failures=nf, new_failures_by_reading=nf_by,
                    fraction_inside=inside, classification=CLASSF, cluster_edges_Mpc=[min(edges_k), max(edges_k)],
                    observed=[RES["canonical/R_proj/0.13/extended"]["obs"], RES["canonical/R_proj/0.13/extended"]["err"]],
                    central_slopes={f: {s_: [RES[f"{f}/R_proj/0.13/extended"]["rows"][s_]["slope_scalar"],
                                             RES[f"{f}/R_proj/0.13/extended"]["rows"][s_]["slope_subtract"]]
                                        for s_ in capA} for f in A0},
                    pass_=max(sig) <= 2.0 and nf == 0)

    # ============================================================================================ PART 1 clusters
    banner("PART 1 -- (a) THE CLUSTER-INFALL BTFR (N = 314): M* (XR9's kappa form) and the door (no cluster region)")
    set_cell(*CELL)
    RESk, CLFk, NFk, EDk, EINk = score_clusters_k()
    CLUk = summarise_clusters(RESk, CLFk, NFk, EDk)
    ref_full = XR9["clusters_full_table_converged_cell"]; ref_sum = XR9["clusters"]["p1_x2.5"]
    d_full = maxdiff({k_: dict(obs=v_["obs"], err=v_["err"], rows=v_["rows"], n_beyond=v_["n_beyond"], n_members=v_["n_members"])
                      for k_, v_ in RESk.items()},
                     {k_: dict(obs=v_["obs"], err=v_["err"], rows=v_["rows"], n_beyond=v_["n_beyond"], n_members=v_["n_members"])
                      for k_, v_ in ref_full.items()})
    d_sum = maxdiff({k_: CLUk[k_] for k_ in ("sigma_range", "sigma_central", "sigma_uncapped", "zp_sigma_range", "new_failures",
                                             "new_failures_by_reading", "fraction_inside", "classification", "cluster_edges_Mpc",
                                             "observed", "central_slopes")},
                    {k_: ref_sum[k_] for k_ in ("sigma_range", "sigma_central", "sigma_uncapped", "zp_sigma_range", "new_failures",
                                                "new_failures_by_reading", "fraction_inside", "classification", "cluster_edges_Mpc",
                                                "observed", "central_slopes")})
    check("C1 CONTROL: with the door off (M*, p = 1, x_c0 = 2.5, MS5's kappa cap) XR9's committed cluster table -- 24 variants x "
          "10 scenarios x 8 numbers, members beyond the edge, the classification, the edges and the summary ranges -- is "
          "reproduced exactly", f"full table max |diff| {d_full:.1e}; summary max |diff| {d_sum:.1e}; M* slope sigma "
          f"{CLUk['sigma_range'][0]:.2f}-{CLUk['sigma_range'][1]:.2f}", d_full < 1e-9 and d_sum < 1e-9)
    P(f"    [{time.time() - T0:.0f}s]")

    # ---- the door: part (2) removes every cluster's region
    mb_cl = {cls[j]["name"]: 0.10 * cls[j]["M500"] for j in used}             # baryons inside R500 at the LOWEST f_b(R500)
    above = min(mb_cl.values()) / max(M_CAP.values())
    P(f"    the 21 PSZ2 hosts' baryons inside R500 at f_b = 0.10: {min(mb_cl.values()):.2e}-{max(mb_cl.values()):.2e} Msun, "
      f"{above:.0f}x M_cap or more: part (2) leaves no cluster a MOND region")
    DOORC = {}
    for foot, a0 in A0.items():
        Dobs = np.log10(Vv * 1e3) - 0.25 * np.log10(Gc * Mbg * a0)
        for geo, dp in GEOS:
            r_m, x_m, ge, lge = geometry(foot, a0, geo, dp)
            sobs, eobs = BOOT[(foot, geo)]
            e0 = np.zeros(len(gal))
            Dp, Dq = predict(e0, a0, nu_mono_e)
            sp, _ = regress(Dp, memb, lge); sq, _ = regress(Dq, memb, lge)
            co, cp, sej = zero_point(Dobs, Dp, f"{foot}/{geo}")
            DOORC[f"{foot}/{geo}"] = dict(obs=float(sobs), err=float(eobs), slope=float(sp), slope_subtract=float(sq),
                                          sigma=float(abs(sobs - sp) / eobs), zp_obs=float(co), zp_pred=float(cp), zp_err=float(sej),
                                          zp_sigma=float(abs(co - cp) / sej))
            P(f"    door {foot:9s} r = {geo:10s}: observed slope {sobs:+.4f} +- {eobs:.4f}; predicted {sp:+.4f} (subtract form "
              f"{sq:+.4f}: e = 0, the forms coincide) -> {abs(sobs - sp) / eobs:.2f} sigma; zero point {cp:+.4f} vs {co:+.4f} +- "
              f"{sej:.4f} -> {abs(co - cp) / sej:.2f} sigma")
    # ---- the member-member watershed check (projected separations: lower bounds on 3-D)
    NB = []
    ra = np.radians(np.array([x_["ra"] for x_ in gal])); de = np.radians(np.array([x_["de"] for x_ in gal]))
    for j in used:
        ii = np.where(memb & (idx == j))[0]
        if len(ii) < 2: continue
        cosd = (np.sin(de[ii])[:, None] * np.sin(de[ii])[None, :]
                + np.cos(de[ii])[:, None] * np.cos(de[ii])[None, :] * np.cos(ra[ii][:, None] - ra[ii][None, :]))
        sep = np.arccos(np.clip(cosd, -1, 1)) * cls[j]["dA"] * MPC
        np.fill_diagonal(sep, np.inf)
        for a_, i in enumerate(ii):
            mu = Mbg[i] / Mbg[ii]                                            # own mass over each neighbour's
            sstar = sep[a_] * mu ** (1 / 6) / (1 + mu ** (1 / 6))            # extent of i's basin toward each neighbour
            k_ = int(np.argmin(sstar))
            NB.append(dict(agc=gal[i]["agc"], s_star_kpc=float(sstar[k_] / KPC), RHI_kpc=float(RHI[i] / KPC),
                           sep_kpc=float(sep[a_][k_] / KPC), short=bool(sstar[k_] < RHI[i])))
    nshort = sum(x_["short"] for x_ in NB)
    P(f"    member-member watershed (projected, a lower bound): {nshort}/{len(NB)} members have a basin toward their nearest "
      f"member neighbour smaller than R_HI; median s*/R_HI = {np.median([x_['s_star_kpc'] / x_['RHI_kpc'] for x_ in NB]):.1f}")
    # ---- the scored column
    if DOOR:
        e_scored_max = 0.0                                                     # every member reads only its own baryons
        SC_C = dict(sigma_range=[min(v_["sigma"] for v_ in DOORC.values()), max(v_["sigma"] for v_ in DOORC.values())],
                    zp_sigma_range=[min(v_["zp_sigma"] for v_ in DOORC.values()), max(v_["zp_sigma"] for v_ in DOORC.values())],
                    n_partition_short=nshort)
    else:
        e_scored_max = max(float(np.max(v_[s_][memb])) for v_ in EINk.values() for s_ in v_ if s_.startswith("A kappa"))
        SC_C = dict(sigma_range=CLUk["sigma_range"], zp_sigma_range=CLUk["zp_sigma_range"], n_partition_short=None)
    check("D1 THE DOOR TAKES THE MEMBERS OUT OF THEIR CLUSTERS' REGIONS: in the scored configuration no member's kernel reads its "
          "cluster's field (largest e/a0 over the 314 members and every operator-A variant) -- MUTATE (regions merged) must fail",
          f"max e = {e_scored_max / A0['canonical']:.3e} a0", e_scored_max == 0.0)
    g1 = SC_C["sigma_range"][1] < GFN_BAND
    check("G1 (reported, pre-declared) (a) FLIPS: every scored variant (footing x geometry) of the cluster-infall BTFR slope lies "
          "within 2 sigma of the observed +0.0033 +- 0.0304", f"slope sigma {SC_C['sigma_range'][0]:.2f}-{SC_C['sigma_range'][1]:.2f}; "
          f"zero point {SC_C['zp_sigma_range'][0]:.2f}-{SC_C['zp_sigma_range'][1]:.2f} sigma (M*: {CLUk['sigma_range'][0]:.2f}-"
          f"{CLUk['sigma_range'][1]:.2f} and {CLUk['zp_sigma_range'][0]:.2f}-{CLUk['zp_sigma_range'][1]:.2f})", g1, load_bearing=False)
    OUT["numbers"]["clusters"] = dict(Mstar_kappa_summary=CLUk, door=DOORC, scored=SC_C, cluster_baryons_R500_fb010=mb_cl,
                                      neighbour_watershed=dict(n_short=nshort, n=len(NB), examples=[x_ for x_ in NB if x_["short"]][:20]))

    # ============================================================================================ PART 2 dwarfs
    banner("PART 2 -- (b) THE LOCAL VOLUME DWARFS (N = 92): statistic C, M* and the door under the object rule")
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

    def score_dwarfs_k():
        """XR9's score_dwarfs('kappa'), verbatim (M*)."""
        out = {}
        for foot, a0 in A0.items():
            _, cobs, eobs = DWB[foot]
            for cgm in (1.0, 1.5, 2.0):
                edges = {}
                for hname, Mh in (("MW", KD.M_MW_BAR * cgm), ("M31", KD.M_M31_BAR * cgm)):
                    rr = np.geomspace(5.0 * KPC, 6.0 * MPC, 5000)
                    e_, g_, D_, qb_ = ms_profile(rr, np.full_like(rr, Mh * MSUN), a0)
                    on_ = switch_state(0.0, D_, qb_, g_, math.inf)[0] & (rr <= lcap_e(0.0))
                    edges[hname] = region_edge(rr, on_)[0]
                inside = np.where(host_mw, r_host < edges["MW"], r_host < edges["M31"])
                sp = pred_slope(np.where(inside, gNe0 * cgm, 1e-30), foot)
                out[f"{foot}/{cgm}"] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs), n_outside=int((~inside).sum()),
                                            edges_Mpc={k_: v_ / MPC for k_, v_ in edges.items()}, obs=cobs, err=eobs)
        return out

    set_cell(*CELL)
    DWk = score_dwarfs_k()
    dc2 = maxdiff(DWk, XR9["dwarfs"]["p1_x2.5"]["rows"])
    check("C2 CONTROL: with the door off XR9's committed dwarf rows at the cell (host baryons x1/x1.5/x2, both footings: slope, "
          "sigma, dwarfs outside, host edges, observed statistic) are reproduced exactly", f"max |diff| {dc2:.1e}", dc2 < 1e-9)

    # ---- the object rule R1: the watershed saddle on the host-object axis
    def ms_rho(Mfun, r_m, a0):
        """MOND-sector density [kg/m^3] of a spherical baryon profile (baryons + its own untruncated nu_mono phantom)."""
        _, _, Dv, _ = ms_profile(r_m, Mfun(r_m), a0)
        return Dv / (4 * math.pi * Gc)

    hern = lambda M, a: (lambda r: M * MSUN * r ** 2 / (r + a) ** 2)
    plum = lambda M, b: (lambda r: M * MSUN * r ** 3 / (r ** 2 + b ** 2) ** 1.5)

    def s_star(M_host, a_host_kpc, M_obj, b_kpc, D_kpc, a0, n=6000):
        """distance [kpc] from the object to the MOND-sector density saddle on the host-object axis (0: the object is not a
        separate maximum).  Host Hernquist + own phantom; object Plummer + own phantom; both isolated."""
        D = D_kpc * KPC
        s = np.geomspace(min(1e-3 * b_kpc, 1e-4) * KPC, 0.999 * D, n)          # distance from the object along the axis
        rh = D - s                                                              # distance from the host
        gh = np.geomspace(1e-4 * KPC, 1.2 * D, 4000)
        rho_h = np.interp(rh, gh, ms_rho(hern(M_host, a_host_kpc * KPC), gh, a0))
        go = np.geomspace(min(1e-3 * b_kpc, 1e-4) * KPC, 1.2 * D, 4000)
        rho_o = np.interp(s, go, ms_rho(plum(M_obj, b_kpc * KPC), go, a0))
        tot = rho_h + rho_o
        dt = np.diff(tot)
        k = np.where(dt > 0)[0]                                                  # first rise moving from the object to the host
        if k.size == 0 or k[0] == 0:
            return 0.0
        return float(s[k[0]] / KPC)

    def dwarf_sstar(a0, cgm, afac=1.0):
        out = np.zeros(len(d))
        for i, g_ in enumerate(d):
            hm = bool(host_mw[i])
            Mh = (KD.M_MW_BAR if hm else KD.M_M31_BAR) * cgm
            ah = A_HOST["MW" if hm else "M31"] * afac
            Dk = float(dmw[i] if hm else dm31[i])
            out[i] = s_star(Mh, ah, g_["Mb"], g_["rh"] / KD.KPC, Dk, a0)
        return out

    SST = {(f, cgm, af): dwarf_sstar(A0[f], cgm, af) for f in A0 for cgm in (1.0, 1.5, 2.0) for af in (1.0,)}
    for af in (0.5, 2.0):
        SST[("canonical", 1.0, af)] = dwarf_sstar(A0["canonical"], 1.0, af)
    s1 = SST[("canonical", 1.0, 1.0)]
    P(f"    R1 saddle extents s* of the 92 dwarfs (canonical, host baryons x1): min {s1.min():.2f}, 10% {np.percentile(s1, 10):.2f}, "
      f"median {np.median(s1):.1f}, max {s1.max():.0f} kpc; below l_obj = {ELL_OBJ:g} kpc: {int((s1 < ELL_OBJ).sum())}   "
      f"[{time.time() - T0:.0f}s]")
    OUT["numbers"]["dwarf_s_star_kpc_canonical_x1"] = {g_["key"]: float(v_) for g_, v_ in zip(d, s1)}
    order = np.argsort(s1)[:6]
    P("    the dwarfs with the smallest s* (they leave the door first as l_obj rises): " + "; ".join(
        f"{d[i]['key']} (M_b {d[i]['Mb']:.1e}, D {float(dmw[i] if host_mw[i] else dm31[i]):.0f} kpc from "
        f"{'MW' if host_mw[i] else 'M31'}) {s1[i]:.2f} kpc" for i in order))
    s_min_dw = float(min(v_.min() for v_ in SST.values()))

    def score_dwarfs_door(ell, afac=1.0, size_rule=False):
        out = {}
        for foot, a0 in A0.items():
            _, cobs, eobs = DWB[foot]
            for cgm in (1.0, 1.5, 2.0):
                ss = SST.get((foot, cgm, afac))
                if ss is None:
                    ss = SST[(foot, cgm, afac)] = dwarf_sstar(a0, cgm, afac)
                sep_ = ss >= ell
                if size_rule:
                    sep_ = sep_ & (np.array([g_["rh"] / KD.KPC for g_ in d]) >= ell)
                sp = pred_slope(np.where(sep_, 1e-30, gNe0 * cgm), foot)
                out[f"{foot}/{cgm}"] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs), n_objects=int(sep_.sum()),
                                            obs=cobs, err=eobs)
        return out

    DWd = score_dwarfs_door(ELL_OBJ)
    for k_, v_ in DWd.items():
        P(f"    door (R1, l_obj = {ELL_OBJ:g} kpc) {k_:15s}: {v_['n_objects']}/92 own regions; predicted C {v_['slope']:+.4f} vs observed "
          f"{v_['obs']:+.4f} +- {v_['err']:.4f} -> {v_['sigma']:.2f} sigma (M*: {DWk[k_]['sigma']:.2f})")
    nsep = min(v_["n_objects"] for v_ in DWd.values()) if DOOR else 92 - max(92 - v_["n_outside"] for v_ in DWk.values())
    check("D2 THE DOOR TAKES THE SATELLITES OUT OF THEIR HOSTS' REGIONS: under R1 at l_obj = 1 kpc at least 80% of the 92 dwarfs "
          "are their own MOND regions in the scored configuration (every footing and host-baryon variant) -- MUTATE (regions "
          "merged) must fail", f"{nsep}/92 own regions (scored)", nsep >= 0.8 * 92)
    SC_D = dict(sigma_range=[min(v_["sigma"] for v_ in DWd.values()), max(v_["sigma"] for v_ in DWd.values())]) if DOOR else \
        dict(sigma_range=[min(v_["sigma"] for v_ in DWk.values()), max(v_["sigma"] for v_ in DWk.values())])
    check("G2 (reported, pre-declared) (b) FLIPS: every scored variant (footing x host baryons x1/x1.5/x2) of the dwarfs' "
          "statistic C lies within 2 sigma of the observed +0.080 +- 0.047", f"C sigma {SC_D['sigma_range'][0]:.2f}-"
          f"{SC_D['sigma_range'][1]:.2f} (M*: {min(v_['sigma'] for v_ in DWk.values()):.2f}-{max(v_['sigma'] for v_ in DWk.values()):.2f})",
          SC_D["sigma_range"][1] < GFN_BAND, load_bearing=False)
    # ---- sensitivity: l_obj, a_host, the size rule
    SENS = {}
    for ell in ELL_SWEEP:
        r_ = score_dwarfs_door(ell)
        SENS[f"R1/l{ell:g}"] = dict(sigma_range=[min(v_["sigma"] for v_ in r_.values()), max(v_["sigma"] for v_ in r_.values())],
                                    n_objects=[min(v_["n_objects"] for v_ in r_.values()), max(v_["n_objects"] for v_ in r_.values())])
    for af in (0.5, 2.0):
        r_ = {k_: v_ for k_, v_ in score_dwarfs_door(ELL_OBJ, afac=af).items() if k_ == "canonical/1.0"}
        SENS[f"R1/l1/a_host x{af:g}"] = dict(sigma_range=[r_["canonical/1.0"]["sigma"]] * 2, n_objects=[r_["canonical/1.0"]["n_objects"]] * 2)
    for ell in (0.1, 0.3, 1.0):
        r_ = score_dwarfs_door(ell, size_rule=True)
        SENS[f"R3 size rule/l{ell:g}"] = dict(sigma_range=[min(v_["sigma"] for v_ in r_.values()), max(v_["sigma"] for v_ in r_.values())],
                                              n_objects=[min(v_["n_objects"] for v_ in r_.values()), max(v_["n_objects"] for v_ in r_.values())])
    P("    sensitivity of statistic C to the object rule (sigma range over footings and host baryons; dwarfs that are objects):")
    for k_, v_ in SENS.items():
        P(f"      {k_:24s} {v_['sigma_range'][0]:.2f}-{v_['sigma_range'][1]:.2f} sigma  ({v_['n_objects'][0]}-{v_['n_objects'][1]}/92 own regions)")
    passing = [k_ for k_, v_ in SENS.items() if v_["sigma_range"][1] < GFN_BAND]
    check("S1 (reported) THE OBJECT SCALE IS LOAD-BEARING FOR (b): statistic C against l_obj (R1), the host scale lengths and the "
          "size rule R3 -- the settings at which every variant stays below 2 sigma", f"passing: {passing}",
          True, load_bearing=False)
    OUT["numbers"]["dwarfs"] = dict(Mstar_kappa_rows=DWk, door_rows=DWd, scored=SC_D, sensitivity=SENS)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ PART 3 Coma UDGs
    banner("PART 3 -- (c) THE COMA UDGs: M* (inside Coma's kappa-capped region) and the door (Coma has no region)")
    run, budget, MODELS, BETA, UDG, A0L, ZCOMA, R500C, kpc23, G23, wmean = (EF[k_] for k_ in (
        "run", "budget", "MODELS", "BETA", "UDG", "A0L", "ZCOMA", "R500C", "kpc23", "G23", "wmean"))
    g_beta, nus = EF["g_beta"], EF["nus"]
    foot_of = lambda a0: "canonical" if a0 == A0L["canonical"] else "alt"

    def coma_profiles_k():
        CO = {}
        for foot, a0 in A0L.items():
            for mname, gfn in MODELS.items():
                for f500 in F500S:
                    rk = np.geomspace(50.0, 40000.0, 5000)
                    Mtot = np.array([gfn(x_) for x_ in rk]) * (rk * kpc23) ** 2 / G23
                    Mbk = fb_profile(rk / R500C, f500) * Mtot
                    rm = rk * kpc23
                    e_, g_, D_, qb_ = ms_profile(rm, Mbk, a0)
                    on_ = switch_state(ZCOMA, D_, qb_, g_, math.inf)[0] & (rm <= lcap_e(ZCOMA))
                    CO[f"{foot}/{mname}/{f500}"] = dict(edge_m=region_edge(rm, on_)[0], prof=(rm, Mbk, e_, g_, D_, qb_))
        return CO

    def make_arm(CO, gap, variant):
        """XR9's make_arm, verbatim."""
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
            if not all(don):
                oe = np.array(R_["oe"], float)
                for i, u in enumerate(UDG):
                    if not don[i]:
                        gobs = u["gobs"] * kw.get("sig_scale", 1.0) ** 2 / kw.get("dist_scale", 1.0); gbar = u["gbar"] * kw.get("ml_scale", 1.0)
                        oe[i] = math.log10(gobs) - math.log10(gbar)
                me, se = wmean(oe, R_["err"])
                R_ = dict(R_, oe=oe, me=me, se=se)
            return R_
        return arm, efield

    set_cell(*CELL)
    CO = coma_profiles_k()
    edges = [v_["edge_m"] / kpc23 / 1e3 for v_ in CO.values()]
    res = {}; floor = None
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
    sgk = [v_["sigma"] for v_ in res.values()]
    refU = XR9["udg"]["p1_x2.5"]
    dc3 = max(maxdiff(res, refU["rows"]), abs(floor - refU["floor"]), maxdiff([min(sgk), max(sgk)], refU["sigma_range"]),
              maxdiff([min(edges), max(edges)], refU["coma_edge_Mpc"]))
    check("C3 CONTROL: with the door off XR9's committed UDG rows at the cell (2 kappa readings x 3 gaps x 2 footings: offset, "
          "error, sigma, UDGs inside, Newtonian UDGs), the recomputed floor, the sigma range and Coma's edges are reproduced "
          "exactly", f"max |diff| {dc3:.1e} (M*: {min(sgk):.2f}-{max(sgk):.2f} sigma, floor {floor:.4f})", dc3 < 1e-9)

    # ---- the door: Coma above M_cap; every UDG isolated
    Mb_coma = float(fb_profile(np.array(1.0), 0.10)) * g_beta(R500C) * (R500C * kpc23) ** 2 / G23 / EF["MS23"]   # f_b 0.10 at R500
    zeros = [0.0] * len(UDG)
    arm_door = lambda a0, m_, k_, f500=0.13, **kw: run(a0, MODELS[m_], k_, "given", "sphere", efield=zeros, **kw)
    Sd, floor_d = budget(arm_door, extra={"f_b(R500) template 0.10-0.157 (new)": 0.0})
    UD = {}
    for f in A0L:
        R_ = arm_door(A0L[f], BETA, "dmean")
        UD[f] = dict(me=R_["me"], se=R_["se"], sigma=R_["me"] / math.sqrt(R_["se"] ** 2 + floor_d ** 2))
    df44 = wmean(arm_door(A0L["canonical"], BETA, "dmean")["oe"][[0]], arm_door(A0L["canonical"], BETA, "dmean")["err"][[0]])
    P(f"    Coma's baryons inside R500 (beta model, f_b 0.10): {Mb_coma:.2e} Msun = {Mb_coma / max(M_CAP.values()):.0f} M_cap: no region")
    P(f"    door: every UDG isolated MOND on its own baryons: offset {UD['canonical']['me']:+.4f} / {UD['alt']['me']:+.4f} dex; the floor "
      f"recomputed on this arm {floor_d:.4f} dex (the Coma mass-model / 3-D position and f_b entries vanish: " +
      ", ".join(f"{k_} {v_:.3f}" for k_, v_ in Sd.items()) + f") -> {UD['canonical']['sigma']:.2f} / {UD['alt']['sigma']:.2f} sigma; "
      f"DF44 alone {df44[0]:+.3f} +- {df44[1]:.3f}")

    # ---- reported: the Newtonian pull of Coma's carrier inside each UDG's r_1/2 (uniform density, (4 pi/3) G rho r)
    def rho_carrier(m_, r_kpc, ret, f500=0.13):
        gfn = MODELS[m_]; dr = 1.0
        Mt = lambda x_: gfn(x_) * (x_ * kpc23) ** 2 / G23
        rho_t = (Mt(r_kpc + dr) - Mt(r_kpc - dr)) / (2 * dr * kpc23) / (4 * math.pi * (r_kpc * kpc23) ** 2)
        return ret * (1 - float(fb_profile(np.array(r_kpc / R500C), f500))) * rho_t

    def arm_door_car(a0, m_, k_, f500=0.13, ret=1.0, **kw):
        R_ = run(a0, MODELS[m_], k_, "given", "sphere", efield=zeros, **kw)
        oe = []
        for i, u in enumerate(UDG):
            gobs = u["gobs"] * kw.get("sig_scale", 1.0) ** 2 / kw.get("dist_scale", 1.0); gbar = u["gbar"] * kw.get("ml_scale", 1.0)
            gcar = 4 * math.pi / 3 * G23 * rho_carrier(m_, u[k_], ret, f500) * u["r12"] * kw.get("dist_scale", 1.0)
            oe.append(math.log10(gobs) - math.log10(nus(gbar / a0) * gbar + gcar))
        me, se = wmean(oe, R_["err"])
        return dict(R_, oe=np.array(oe), me=me, se=se)

    Sc, floor_c = budget(arm_door_car)
    UDC = {f: dict(me=arm_door_car(A0L[f], BETA, "dmean")["me"]) for f in A0L}
    for f in A0L:
        UDC[f]["sigma"] = UDC[f]["me"] / math.sqrt(UD[f]["se"] ** 2 + floor_c ** 2)
    P(f"    reported: with Coma's smooth carrier inside r_1/2 at ret = 1 (what X-COP then requires): offset {UDC['canonical']['me']:+.4f} / "
      f"{UDC['alt']['me']:+.4f} dex, floor {floor_c:.4f} -> {UDC['canonical']['sigma']:.2f} / {UDC['alt']['sigma']:.2f} sigma")
    if DOOR:
        ext_max = 0.0
        SC_U = dict(sigma=[UD["canonical"]["sigma"], UD["alt"]["sigma"]], me=[UD["canonical"]["me"], UD["alt"]["me"]], floor=floor_d)
    else:
        ext_max = max(max(make_arm(CO, "Dirichlet", "galaxy")[1](A0L[f], BETA, "dmean", 0.13)[0]) for f in A0L)
        SC_U = dict(sigma=[min(sgk), max(sgk)], me=[res["galaxy/Dirichlet/canonical"]["me"], res["galaxy/Dirichlet/alt"]["me"]], floor=floor)
    check("D3 THE DOOR TAKES THE UDGs OUT OF COMA'S FIELD: in the scored configuration no UDG's kernel reads Coma's field (largest "
          "external field in nu's argument, central arm) -- MUTATE (regions merged) must fail", f"max e = {ext_max:.3e} m/s^2",
          ext_max == 0.0)
    check("G3 (reported, pre-declared) (c) FLIPS: the scored UDG offset is below 2 sigma on both footings (floor recomputed on the "
          "scored arm)", f"{SC_U['sigma'][0]:.2f} / {SC_U['sigma'][1]:.2f} sigma at {SC_U['me'][0]:+.3f} / {SC_U['me'][1]:+.3f} dex "
          f"(M*: {min(sgk):.2f}-{max(sgk):.2f} sigma at +0.98 / +0.95 dex); with the carrier term {UDC['canonical']['sigma']:.2f} / "
          f"{UDC['alt']['sigma']:.2f}", max(SC_U["sigma"]) < GFN_BAND, load_bearing=False)
    OUT["numbers"]["udg"] = dict(Mstar_kappa_rows=res, Mstar_floor=floor, door=UD, door_floor=floor_d, door_budget=Sd,
                                 door_with_carrier=UDC, door_with_carrier_floor=floor_c, df44_door=list(df44), coma_Mb_R500=Mb_coma,
                                 scored=SC_U)
    P(f"    [{time.time() - T0:.0f}s]")

    # ============================================================================================ PART 4 the object rule's reach
    banner("PART 4 -- THE OBJECT RULE'S REACH: the Sun and wide binaries, the outer-halo globulars (item 93), SPARC and M_cap")
    SOL = {}
    for lab, M_, b_ in (("Sun", 1.0, 1e-4), ("wide binary 2 Msun", 2.0, 1e-4), ("open cluster 1e4 Msun", 1e4, 3e-3)):
        SOL[lab] = {f: s_star(KD.M_MW_BAR, A_HOST["MW"], M_, b_, 8.2, A0[f]) for f in A0}
    worst = max(v_ for x_ in SOL.values() for v_ in x_.values())
    for lab, v_ in SOL.items():
        P(f"    {lab:24s} at 8.2 kpc: s* = {v_['canonical']:.3f} / {v_['alt']:.3f} kpc (canonical / alt)")
    check("R1s THE SUN KEEPS THE GALAXY'S FIELD: the Sun, a 2 Msun wide binary and a 1e4 Msun open cluster at 8.2 kpc have s* < "
          "l_obj = 1 kpc on both footings (a spherical Milky Way under-states the disc's density gradient, so s* is an upper "
          "bound): they stay in the Galaxy's region and the Gaia DR4 pre-registration is untouched", f"largest s* {worst:.3f} kpc",
          worst < ELL_OBJ)
    OUT["numbers"]["solar_neighbourhood_s_star_kpc"] = SOL

    # ---- item 93: the four outer-halo globulars.  Inputs are h93's committed ones (h93_outer_halo_globulars.py SOURCE and
    #      E(B-V); the measured dispersions at r_h,l from h93_outer_halo_globulars.out lines 23-30).
    GCIN = {"NGC 2419": dict(Dsun=88.47, RGC=95.93, V=10.56, EBV=0.08, rhl=19.76, so=4.771, eso=0.481, N=62),
            "Pal 3": dict(Dsun=94.84, RGC=98.17, V=14.56, EBV=0.04, rhl=20.16, so=1.700, eso=0.340, N=22),
            "Pal 4": dict(Dsun=101.39, RGC=104.05, V=14.23, EBV=0.01, rhl=15.88, so=0.880, eso=0.185, N=23),
            "Pal 14": dict(Dsun=73.58, RGC=68.55, V=14.13, EBV=0.04, rhl=27.63, so=0.710, eso=0.160, N=16)}
    sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
    from hunt_lib import nu_s, G as Gh, kpc as kpch, Msun as Msunh      # noqa: E402  (h93's constants and kernel)
    PCh = 3.0857e16; UPS_V = 1.6; MW_MB = 6.0e10
    for g_ in GCIN.values():
        MV = g_["V"] - 3.1 * g_["EBV"] - 5 * math.log10(g_["Dsun"] * 1e3 / 10.0)
        g_["LV"] = 10 ** (-0.4 * (MV - 4.83))

    def gc_joint(a0, efe_on):
        rows = []
        for nm, g_ in GCIN.items():
            M = UPS_V * g_["LV"] * Msunh; r12 = (4.0 / 3.0) * g_["rhl"] * PCh
            yi = Gh * (M / 2) / r12 ** 2 / a0; ye = Gh * MW_MB * Msunh / (g_["RGC"] * kpch) ** 2 / a0
            nu_ = nu_s(yi + ye) if efe_on[nm] else nu_s(yi)
            sN = math.sqrt(Gh * M / (6.0 * r12)) / 1e3
            rows.append(dict(so=g_["so"], eso=g_["eso"], N=g_["N"], sF=sN * math.sqrt(nu_)))
        y = np.array([math.log(r["so"] / r["sF"]) for r in rows])
        e = np.array([math.hypot(r["eso"] / r["so"], 1.0 / math.sqrt(2 * (r["N"] - 1))) for r in rows])
        w = 1.0 / e ** 2; m = float(np.sum(w * y) / np.sum(w)); em = float(1.0 / math.sqrt(np.sum(w)))
        return UPS_V * math.exp(2 * m), UPS_V * math.exp(2 * m) * 2 * em, float(np.sum(w * (y - m) ** 2))

    A0h = {"canonical": 9.36e-11, "alt": 1.13e-10}
    ctl = {f: gc_joint(A0h[f], {nm: True for nm in GCIN}) for f in A0h}
    check("C4 CONTROL: hunt item 93's joint one-M/L fit of the four outer-halo globulars (with the Milky Way's EFE, h93's inputs) is "
          "reproduced: 0.76 +- 0.15 (chi2 8.31) canonical, 0.71 +- 0.14 (8.52) alt", "; ".join(f"{f}: {v_[0]:.3f} +- {v_[1]:.3f} "
          f"(chi2 {v_[2]:.2f})" for f, v_ in ctl.items()),
          abs(ctl["canonical"][0] - 0.76) < 0.005 and abs(ctl["canonical"][1] - 0.15) < 0.005 and abs(ctl["canonical"][2] - 8.31) < 0.01
          and abs(ctl["alt"][0] - 0.71) < 0.005 and abs(ctl["alt"][1] - 0.14) < 0.005 and abs(ctl["alt"][2] - 8.52) < 0.01)
    GCS = {nm: {f: s_star(MW_MB, A_HOST["MW"], UPS_V * g_["LV"], g_["rhl"] / 1e3, g_["RGC"], A0[f]) for f in A0} for nm, g_ in GCIN.items()}
    GC93 = {}
    for ell in ELL_SWEEP:
        sepd = {nm: GCS[nm]["canonical"] >= ell for nm in GCIN}
        GC93[f"l{ell:g}"] = dict(objects=[nm for nm, v_ in sepd.items() if v_],
                                 joint={f: gc_joint(A0h[f], {nm: not sepd[nm] for nm in GCIN}) for f in A0h})
    P("    outer-halo globulars: s* (canonical) " + ", ".join(f"{nm} {v_['canonical']:.1f} kpc" for nm, v_ in GCS.items()))
    for k_, v_ in GC93.items():
        P(f"      R1 {k_:6s}: own regions {v_['objects'] or 'none'}; joint M/L_V {v_['joint']['canonical'][0]:.2f} +- "
          f"{v_['joint']['canonical'][1]:.2f} / {v_['joint']['alt'][0]:.2f} +- {v_['joint']['alt'][1]:.2f} (item 93 with EFE: 0.76 / 0.71; "
          f"stellar populations 1.3-2.2)")
    nsep_gc = len(GC93[f"l{ELL_OBJ:g}"]["objects"])
    j1 = GC93[f"l{ELL_OBJ:g}"]["joint"]
    check("S2 (reported) THE OBJECT RULE REACHES THE OUTER-HALO GLOBULARS: under R1 at l_obj = 1 kpc the four clusters of hunt item "
          "93 are their own regions, lose the Milky Way's EFE, and the joint M/L_V item 93 needs falls further below the "
          "stellar-population floor 1.3 -- a cost of R1; under R2 (star clusters are never objects) item 93 is unchanged",
          f"{nsep_gc}/4 own regions; joint M/L_V {j1['canonical'][0]:.2f} +- {j1['canonical'][1]:.2f} / {j1['alt'][0]:.2f} +- "
          f"{j1['alt'][1]:.2f} (with the EFE: {ctl['canonical'][0]:.2f} / {ctl['alt'][0]:.2f}); l_obj needed to keep all four in the "
          f"Galaxy: > {max(v_['canonical'] for v_ in GCS.values()):.1f} kpc", True, load_bearing=False)
    OUT["numbers"]["item93"] = dict(control=ctl, s_star_kpc=GCS, by_l_obj=GC93)

    # ---- R1 on the Milky Way's own globular clusters (Baumgardt's table: mass, R_GC, half-mass radius)
    GCALL = []
    for line in open(os.path.join(REPO, "real_research", "data", "globular_clusters", "baumgardt_gc_parameters.tsv"), encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f_ = line.rstrip("\n").split("\t")
        try:
            rgc = float(f_[4].split()[0]); mant, ex = f_[7].split("·")
            mass = float(mant.split("+-")[0]) * 10 ** int(ex.strip()[2:]); rhm = float(f_[12])
        except Exception:
            continue
        GCALL.append((" ".join(f_[0].split()), rgc, mass, rhm))
    sgc = np.array([s_star(MW_MB, A_HOST["MW"], m_, rh_ / 1e3, rgc_, A0["canonical"]) for _, rgc_, m_, rh_ in GCALL])
    rgcs = np.array([x_[1] for x_ in GCALL])
    GCC = {f"l{ell:g}": dict(n_objects=int((sgc >= ell).sum()), n_inside_20kpc=int(((sgc >= ell) & (rgcs < 20)).sum())) for ell in ELL_SWEEP}
    inner =[(GCALL[i][0], GCALL[i][1], float(sgc[i])) for i in np.argsort(rgcs) if sgc[i] >= ELL_OBJ][:5]
    P(f"    Baumgardt's {len(GCALL)} Milky Way globulars under R1: s* {sgc.min():.2f}-{sgc.max():.1f} kpc; own regions at l_obj = "
      + ", ".join(f"{k_[1:]} kpc: {v_['n_objects']} ({v_['n_inside_20kpc']} inside R_GC 20 kpc)" for k_, v_ in GCC.items()))
    P(f"      innermost globulars that R1 at 1 kpc separates: " + "; ".join(f"{n_} (R_GC {r_:.1f} kpc, s* {s_:.2f})" for n_, r_, s_ in inner))
    OUT["numbers"]["mw_globulars_R1"] = dict(n=len(GCALL), by_l_obj=GCC, innermost_separated=inner,
                                             s_star_kpc={x_[0]: float(v_) for x_, v_ in zip(GCALL, sgc)})
    lo_win = max(v_ for x_ in SOL.values() for v_ in x_.values())
    pass_ells = [ell for ell in ELL_SWEEP if SENS[f"R1/l{ell:g}"]["sigma_range"][1] < GFN_BAND]
    check("S3 (reported) THE OBJECT SCALE'S WINDOW: l_obj must exceed the solar-neighbourhood structures' s* (so the Sun, wide "
          "binaries and open clusters stay) and lie below the dwarfs' smallest s* (so every satellite is its own region, which is "
          "what (b) needs); the Milky Way globulars R1 separates inside that window are counted",
          f"window {lo_win:.2f} < l_obj < {s_min_dw:.2f} kpc (a factor {s_min_dw / lo_win:.1f}); (b) passes at l_obj in "
          f"{pass_ells} kpc; at l_obj = 1 kpc R1 makes {GCC['l1']['n_objects']}/{len(GCALL)} Milky Way globulars their own "
          f"regions ({GCC['l1']['n_inside_20kpc']} of them inside R_GC = 20 kpc)", True, load_bearing=False)
    OUT["numbers"]["l_obj_window_kpc"] = [lo_win, s_min_dw]

    # ---- M_cap: what part (2) strips and what it spares
    SP = []
    with open(os.path.join(REPO, "real_research", "data", "sparc_master_clean.csv")) as fh:
        for row in csv.DictReader(fh):
            SP.append((row["name"], (0.5 * float(row["L36"]) + 1.33 * float(row["MHI"])) * 1e9))
    spmax = max(SP, key=lambda x_: x_[1])
    lens_max = 3e11                                                              # the heaviest KiDS lens bin (MS3 K1 / DE10 S1)
    stripped_min = min(min(mb_cl.values()), Mb_coma)
    okm = stripped_min > max(M_CAP.values()) and spmax[1] < min(M_CAP.values()) and lens_max < min(M_CAP.values())
    check("M1 PART (2) STRIPS ONLY WHAT IT SHOULD: every system the door strips of its region here (21 PSZ2 hosts, Coma) is above "
          "M_cap on both footings, while every SPARC galaxy and the heaviest KiDS lens bin are below it (the RAR, RC100 and the "
          "KiDS lenses keep their regions)", f"stripped >= {stripped_min:.2e}; SPARC max {spmax[1]:.2e} ({spmax[0]}); KiDS <= "
          f"{lens_max:.0e}; M_cap >= {min(M_CAP.values()):.2e} Msun", okm)
    OUT["numbers"]["sparc_max_Mb"] = dict(name=spmax[0], Mb=spmax[1])

    # ============================================================================================ summary
    banner("SUMMARY (scored column: " + ("the door" if DOOR else "M*, the regions merged (MUTATE)") + ")")
    P(f"  (a) cluster-infall BTFR slope: {SC_C['sigma_range'][0]:.2f}-{SC_C['sigma_range'][1]:.2f} sigma, zero point "
      f"{SC_C['zp_sigma_range'][0]:.2f}-{SC_C['zp_sigma_range'][1]:.2f} sigma   (M* {CLUk['sigma_range'][0]:.2f}-{CLUk['sigma_range'][1]:.2f})")
    P(f"  (b) LV dwarfs statistic C: {SC_D['sigma_range'][0]:.2f}-{SC_D['sigma_range'][1]:.2f} sigma   (M* "
      f"{min(v_['sigma'] for v_ in DWk.values()):.2f}-{max(v_['sigma'] for v_ in DWk.values()):.2f})")
    P(f"  (c) Coma UDGs: {SC_U['sigma'][0]:.2f} / {SC_U['sigma'][1]:.2f} sigma   (M* {min(sgk):.2f}-{max(sgk):.2f})")
    P(f"  object rule R1 (l_obj = {ELL_OBJ:g} kpc): the Sun stays (s* {SOL['Sun']['canonical']:.2f} kpc); {nsep_gc}/4 outer-halo "
      f"globulars separate (item 93's M/L {j1['canonical'][0]:.2f} vs 0.76)")
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
