#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR14_kids_mstar_carrier.py -- KiDS-1000 ON M*'S OWN CARRIER.  Part 2 of 2: DE10's KiDS fit on M*'s gate, scored on the
carrier halos XR14_carrier_halos.py re-ran with L388's phantom-inclusive trigger.  Cross-thread review, 2026-09-26
(night).  Read-only on every other file.

WHY.  DE10 (dabce1b73) scored KiDS for the converged model at -37.0/-34.0 (hard) and -32.3/-29.3 (w = 0.25) at 600 km/s,
but with L375's carrier (the Newtonian-matter trigger).  XR10 finds that row off M* on the carrier.  M*'s carrier is L388's
trigger, which reads the PHANTOM-INCLUSIVE x~.  This lane moves the KiDS row onto it.

THE MODEL AS SCORED (DE10's code path; each piece loaded from its committed source):
  gate     DE8's region operator (L361/CV1, operator A: screened w, gated phantom, sigma = 1, 1/m = 0.1 Mpc; lensing on
           Phi = u + f P with f' P), MS2's MOND-sector reading x = 4 pi G (rho_b + rho_ph - f_b rho_bar_m)/H^2
           (carrier-blind), p = 1, x_c0 = 2.5 at z_l = 0.25, the smooth gate W(t) at w = 0.02 (hard) and 0.25, the region
           connected to the centre;
  cap      MS5's kappa form: U = min(x, v_cap^2 kappa_X^2/H^2), kappa_X = 1/r for a spherical lens, v_cap = 325 km/s.
           Every region stops at l_cap(0.25) = v_cap/(H sqrt(x_c,eff)) = 2.35 Mpc; it binds only where v_f > v_cap, and
           KiDS lenses have v_f <= 247 km/s (K1 checks it does not bind anywhere on the fit's mass grid).  DE10's withdrawn
           local form appears ONLY in C1, which reproduces DE10, and in K1's comparison (labelled);
  carrier  XR14_carrier_halos.py: L375's shell model (secondary infall, the bins' baryons + CGM, L390's refitted masses and
           DE10's seeds, N = 60000) with L388's trigger rule (x~_m + x~_ph > 5, Gamma = 10 H, kick v_k) at every kick
           575-650 km/s, on each footing's a0.  Two readings of "the phantom" the trigger reads, scored separately:
             M*    ('MSPH') the phantom of M*'s own gate (MOND-sector reading + kappa cap), as the same-model PM run L396;
             L388  ('L388') the phantom switched by L388's own matter-only reading, as L388's code does (a branch mix).
           Variant: FK1's conversion (n^2 trigger on the cold carrier's own density, E^4 gate, sharp), 575 and 650 km/s.
           Each carrier's projected profile enters the lens through DE10's template (L375's), at FIXED amplitude fs = 1;
  fit      L352's KiDS machinery through DE8 (Brouwer+21 four bins, full covariance, M_b profiled per bin on L352's grid,
           a linear 2-halo term per bin); Delta chi^2 against L352's unswitched model; pass = <= +4 on both footings.
  THE ANTI-FAKE RULES (the DE thread's, set for XR9): the carrier amplitude is fixed at fs = 1 in every gated score
  (fitted amplitudes are labelled diagnostics); the 2-halo amplitude is capped at A <= 2 in the gated score, re-scored
  against the unswitched baseline with the same bound, and reported per bin; DE10's A <= 20 is reported beside it.

CHECKS
  C0 CONTROL: this lane's fit loop reproduces L352's unswitched baseline chi^2 exactly (A <= 20); the A <= 2 baseline.
  T0 CONTROL: the halo cache's trace control (L388's trigger read from source) and mesh control C3 passed, and its cell is
     this gate's cell (x_c,eff(0.25) from X_C0 and P_GATE equals XCE).
  C1 CONTROL (L375's trigger restored): (a) the 'L375' halos equal XR9's cache of L375's own halo() bit for bit; (b) their
     retention S equals L390's committed S at 600 and 650 km/s; (c) with DE10's configuration (withdrawn local cap,
     fs = 1, A <= 20) they reproduce DE10's committed KiDS table and preferred amplitudes exactly (2 kicks x 2 widths x 2
     footings, 1e-9).
  C2 CONTROL (the pipeline can fail): the no-decay carrier halo on M*'s gate is rejected, Delta chi^2 > +100 on both
     footings (fs = 1, A <= 2 and A <= 20).
  C3b CONTROL: the gate the M* carrier's trigger reads (the halo script's 'MSPH' switch) is this lane's scored gate: for
     point-mass baryons its hard edge equals gate_mond's (kappa form) within 1%, at z = 0.25 and 1, M_b = 1e11 and 1e12
     (the kappa cap binds for the latter), both footings.
  K1 CONTROL (MS5's cap is non-binding): with M*'s carrier, the kappa-capped score equals the uncapped and the withdrawn-
     local-form scores exactly at every kick, width and footing, and the kappa cap changes f nowhere on the fit's mass grid.
  H1  [pre-declared, load-bearing] M*'S CARRIER ('MSPH') passes KiDS: Delta chi^2 <= +4 on both footings, at w = 0.02 and
      0.25, at every kick 575, 600, 625, 650 km/s (fs = 1, A <= 2).
  H1b [pre-declared, load-bearing] L388's carrier AS WRITTEN ('L388') passes on the same terms.
  V1-V5 (reported): A <= 20 (DE10's bound); A and log M_b per bin; the switch alone (fs = 0) and the carrier's share of the
     score; DE10's carrier (C1's halos) on M*'s gate and rules; 'as run' (the canonical carrier on the alt footing);
     retention S (<0.5 Mpc/h) per bin, decayed fraction, the decays the phantom alone caused, the trigger's reach at z_l;
     the FK1 variant; the diagnostic best carrier amplitude (fs in [0, 1]; [0, 3], unphysical above 1).
MUTATE=1: the scored carriers come from XR14_carrier_halos_results_MUTATE.json (v_k = 0: triggered, nothing kicked; one
run per trigger, bin and footing, used at every kick); H1 and H1b must FAIL (rc = 1).  C1 and C2 read the main cache.

SCOPE.  Spherical, isolated lenses; one accretion history (L375's fiducial) with L390's masses (the MOND-sector refit at
this cell, XR9's, differs by 0.1 dex in two bins and moved the L375-carrier score by <= 0.03); static baryons; the trigger's
phantom is L377's spherical QUMOND form (operator B in the trigger, operator A in the lensing) with a hard switch, and the
shell model has no cosmic background beyond the halo's own infall; the upper-branch phantom is read ungated in the gate
(on-branch convention); the heat filter omitted; the trigger and cap posited (no action for the trigger).

Run from the repository root (after XR14_carrier_halos.py has completed):
    python3 real_research/cross_thread_review_2026_09_26/XR14_kids_mstar_carrier.py        (MUTATE=1 for the control)
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR14_kids_mstar_carrier"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR14 (KiDS on M*'s carrier)", "mutate": MUTATE, "checks": {}, "numbers": {}}
FEET = ("canonical", "alt")
VK = (575.0, 600.0, 625.0, 650.0)
VKV = (575.0, 650.0)
WS = (0.02, 0.25)
V_CAP = 325e3                                                         # m/s (MS3/MS5)
A_PHYS, A_WIDE = 2.0, 20.0
EXPECT_PASS = True                                                    # H1 and H1b, set before any score was computed
XCE = 2.5 * (0.3138 * 1.25 ** 3 + 0.6862)                             # x_c,eff(0.25) at p = 1, x_c0 = 2.5 (L359's background)


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
    if MUTATE: P("\n  *** MUTATE=1: the scored carriers are the v_k = 0 halos (triggered, nothing kicked); H1 and H1b must FAIL ***")

    # ------------------------------------------------------------------------------ DE8's operator and fit, unedited
    P8 = os.path.join(DEDIR, "DE8_kids_sigma_axis_both_branches.py")
    D8 = {"__name__": "de8", "__file__": P8}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P8).read().split("# ============================================================================================ C1 C2 C3 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
    (solve_region, esd_from_mlens, Wg, rr, nu_vec, G, MS, A0, KPC_, Ed, Sd, Ci, twoh_cache, LM, project_M2, annulus_esd,
     Rp, Rd, MPCm, esd_bin, Hz, Om, rho_crit0) = [D8[k] for k in (
        "solve_region", "esd_from_mlens", "Wg", "rr", "nu_vec", "G", "MS", "A0", "KPC_", "Ed", "Sd", "Ci", "twoh_cache",
        "LM", "project_M2", "annulus_esd", "Rp", "Rd", "MPCm", "esd_bin", "Hz", "Om", "rho_crit0")]
    BASE20 = D8["BASE"]; FB = D8["FB"]; rho_bar = D8["rho_bar"]; H_L = D8["H_L"]
    P(f"  DE8 loaded (L352's KiDS data, operator A, 2-halo template); x_c,eff(0.25) = {XCE:.4f}   [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------ the carrier halos
    HC = json.load(open(os.path.join(HERE, "XR14_carrier_halos_results.json")))    # M*'s carrier: L388's trigger, re-run
    HMU = json.load(open(os.path.join(HERE, "XR14_carrier_halos_results_MUTATE.json"))) if MUTATE else None
    EDG = np.array(HC["edges_kpc"]); CFG = HC["config"]
    R90 = json.load(open(os.path.join(DS, "L390_kids_resolved_linear_gate_results.json")))["numbers"]
    MB90 = R90["M_b"]["p=1, x_c0=2.5"]

    def halo(tag):
        """the scored carriers come from the MUTATE cache under MUTATE (v_k = 0, one run per trigger/bin/footing)."""
        if MUTATE and not tag.startswith(("L375_", "nodecay_")):
            parts = tag.split("_"); parts[-1] = "v0"
            return HMU["halos"]["_".join(parts)]
        return HC["halos"][tag]

    def carrier_rho_si(d):                                            # DE10's carrier_rho_si (L375's template density step)
        e = EDG; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
        rho = np.array(d["hist"]) * d["m"] / vol
        return np.interp(np.log(rr / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3

    _TC = {}

    def template(tag):
        if tag not in _TC:
            d = halo(tag)
            M2 = project_M2(carrier_rho_si(d))
            _TC[tag] = annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[d["b"]])
        return _TC[tag]

    def tset(mode, foot_a0, v):
        """the four bins' carrier templates for one trigger, the footing whose a0 its trigger used, and one kick."""
        if mode == "FK1":
            return [template(f"FK1_b{b}_v{int(v)}") for b in range(4)]
        if mode in ("L375", "nodecay"):
            return [template(f"L375_b{b}_v{int(v)}" if mode == "L375" else f"nodecay_b{b}") for b in range(4)]
        return [template(f"{mode}_{foot_a0}_b{b}_v{int(v)}") for b in range(4)]

    # ------------------------------------------------------------------------------ M*'s gate (DE10's, MS5's kappa cap)
    def gate_mond(Mb, a0, w, xce, form="kappa", H=None, rhob=None):
        """MS2's door on the point-mass lens (baryons + phantom, carrier-blind), smooth width w, region connected to the
        centre; form 'kappa' = MS5's cap (the scored gate); 'local' = DE10's withdrawn form (C1, K1); 'none' (K1)."""
        H = H_L if H is None else H; rhob = rho_bar if rhob is None else rhob
        Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
        rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2)
        x = 4 * math.pi * G * (rho - FB * rhob) / H ** 2
        if form == "local":
            g = G * Mdyn / rr ** 2
            vloc2 = g ** 2 / np.maximum(4 * math.pi * G * rho, 1e-300)
            t = (x / (xce * np.maximum(1.0, vloc2 / V_CAP ** 2)) - 1) / (2 * w) + 0.5
        elif form == "kappa":
            t = (np.minimum(x, (V_CAP / (rr * H)) ** 2) / xce - 1) / (2 * w) + 0.5
        else:
            t = (x / xce - 1) / (2 * w) + 0.5
        f = Wg(t)
        off = np.where(t <= 0)[0]
        if off.size: f[off[0]:] = 0.0
        return f

    _ESD = {}

    def model(b, lm, foot, w, form="kappa"):
        key = (b, round(float(lm), 3), foot, w, form)
        if key not in _ESD:
            Mb = 10 ** lm * MS; a0 = A0[foot]
            f = gate_mond(Mb, a0, w, XCE, form)
            extra = solve_region(Mb, a0, f, 100 * KPC_, 1.0)
            _ESD[key] = esd_from_mlens(Mb, extra, b)
        return _ESD[key]

    def fit(foot, TCs, fs, amax, base, w, form="kappa"):
        """DE10/XR9's fit: per bin the grid mass with the smallest diagonal chi^2 (2-halo amplitude A in [0, amax]), then
        the full-covariance chi^2 minus the baseline.  Returns (Delta chi^2, [(log M_b, A) per bin])."""
        mods, per = [], []
        for b in range(4):
            best = None
            for lm in LM:
                mk0 = (model(b, lm, foot, w, form) if w is not None else esd_bin(b, lm, A0[foot], 0.0, "none", False)[0]) \
                    + (fs * TCs[b] if TCs is not None else 0.0)
                t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, amax)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, mk, float(lm), A)
            mods.append(best[1]); per.append((round(best[2], 2), round(best[3], 3)))
        dv = np.concatenate(Ed) - np.concatenate(mods)
        return float(dv @ Ci @ dv) - base, per

    # ============================================================================================ C0 the baseline
    banner("C0 T0  CONTROLS: the fit loop's baseline; the halo cache's trace and mesh controls, and its cell")
    B20 = {f_: fit(f_, None, 0.0, A_WIDE, 0.0, None) for f_ in FEET}
    B2 = {f_: fit(f_, None, 0.0, A_PHYS, 0.0, None) for f_ in FEET}
    d0 = max(abs(B20[f_][0] - BASE20[f_]) for f_ in FEET)
    BASE = {A_WIDE: {f_: B20[f_][0] for f_ in FEET}, A_PHYS: {f_: B2[f_][0] for f_ in FEET}}
    check("C0 CONTROL: the fit loop (A <= 20) reproduces L352's unswitched baseline chi^2 on both footings",
          f"{ {f_: round(B20[f_][0], 4) for f_ in FEET} } vs L352 { {f_: round(BASE20[f_], 4) for f_ in FEET} } (max |diff| {d0:.1e}); "
          f"A <= 2 baseline { {f_: round(B2[f_][0], 4) for f_ in FEET} }, A per bin { {f_: [a for _, a in B2[f_][1]] for f_ in FEET} }",
          d0 < 1e-9, "the A <= 2 score is taken against the unswitched model fitted with the same bound")
    OUT["numbers"]["baseline"] = {"A<=20": {f_: dict(chi2=B20[f_][0], per_bin=B20[f_][1]) for f_ in FEET},
                                  "A<=2": {f_: dict(chi2=B2[f_][0], per_bin=B2[f_][1]) for f_ in FEET}}
    cell = CFG["cell"]
    xce_carrier = cell["X_C0"] * (0.3138 * 1.25 ** 3 + 0.6862) ** cell["P_GATE"]
    t0ok = bool(HC["T0"]["ok"] and HC["C3"]["ok"] and abs(xce_carrier - XCE) < 1e-12 and CFG["kicks"] == list(VK)
                and (not MUTATE or (HMU["T0"]["ok"] and HMU["C3"]["ok"])))
    check("T0 CONTROL: the halo cache's trace control (L388's trigger read from its source) and its mesh control (C3: the "
          "spherical phantom = L377's phantom() on a 3-d mesh) passed, and the carrier's cell is the scored gate's cell",
          f"T0 {HC['T0']['ok']}, C3 {HC['C3']['ok']} (edge mesh/sphere {HC['C3']['edge_mesh_Mpc_h']:.3f}/{HC['C3']['edge_sphere_Mpc_h']:.3f} "
          f"Mpc/h; enclosed phantom mesh/sphere " + ", ".join(f"{r_['mesh'] / r_['sphere_analytic']:.4f}" for r_ in HC["C3"]["rows"]
                                                              if r_["sphere_analytic"] > 0) + f"); carrier cell (X_C0, P_GATE) = "
          f"({cell['X_C0']}, {cell['P_GATE']}) -> x_c,eff(0.25) {xce_carrier:.4f} = XCE {XCE:.4f}; kicks {CFG['kicks']}; "
          f"XC_TRIG {CFG['XC_TRIG']}, Gamma {CFG['GAMMA_TRIG']} H", t0ok)

    # ============================================================================================ C1 DE10 reproduced
    banner("C1  CONTROL (L375's trigger restored): XR9's halos bit for bit, L390's S, DE10's committed table")
    X9 = json.load(open(os.path.join(HERE, "XR9_carrier_halos_results.json")))
    lm90 = [round(math.log10(x), 2) for x in MB90]
    hist_same = all(HC["halos"][f"L375_b{b}_v{int(v)}"]["hist"] == X9["halos"][f"b{b}_lm{lm90[b]:.2f}_v{int(v)}"]["hist"]
                    and HC["halos"][f"L375_b{b}_v{int(v)}"]["m"] == X9["halos"][f"b{b}_lm{lm90[b]:.2f}_v{int(v)}"]["m"]
                    for b in range(4) for v in (600.0, 650.0))
    S_of = lambda tag, b: HC["halos"][tag]["M_ap"] / HC["halos"][f"nodecay_b{b}"]["M_ap"]
    dS = max(abs(S_of(f"L375_b{b}_v{int(v)}", b) - R90["table"][f"v{int(v)}"]["S"][b]) for b in range(4) for v in (600.0, 650.0))
    DE10 = json.load(open(os.path.join(DEDIR, "DE10_kids_converged_model_results.json")))["numbers"]["table"]
    c1, d1 = {}, 0.0
    for v in (600.0, 650.0):
        TCs = tset("L375", None, v)
        for w in WS:
            k = {f_: fit(f_, TCs, 1.0, A_WIDE, BASE20[f_], w, "local")[0] for f_ in FEET}
            bf = {f_: min(((fs_, fit(f_, TCs, fs_, A_WIDE, BASE20[f_], w, "local")[0]) for fs_ in np.linspace(0.0, 1.2, 13)),
                          key=lambda t_: t_[1]) for f_ in FEET}
            ref = DE10[f"v{int(v)}/w{w}"]
            d1 = max(d1, *(abs(k[f_] - ref["kids"][f_]) for f_ in FEET), *(abs(bf[f_][1] - ref["best_fs"][f_][1]) for f_ in FEET),
                     *(abs(bf[f_][0] - ref["best_fs"][f_][0]) for f_ in FEET))
            c1[f"v{int(v)}/w{w}"] = dict(kids=k, best_fs=bf)
    check("C1 CONTROL: with L375's trigger restored, (a) the halos equal XR9's cache of L375's own halo() bit for bit, (b) their "
          "retention equals L390's committed S, (c) DE10's configuration (withdrawn local cap, fs = 1, A <= 20) reproduces "
          "DE10's committed KiDS table and preferred amplitudes (2 kicks x 2 widths x 2 footings)",
          f"(a) histograms identical: {hist_same}; (b) max |S - S_L390| {dS:.1e}; (c) "
          + "; ".join(f"{k_}: {v_['kids']['canonical']:+.3f}/{v_['kids']['alt']:+.3f}" for k_, v_ in c1.items()) + f" (max |diff| {d1:.1e})",
          hist_same and dS < 1e-12 and d1 < 1e-9, "this lane's copy of L375's shell model and DE10's scoring path are exact; only "
          "the trigger differs in what follows")
    OUT["numbers"]["C1_DE10_reproduced"] = c1

    # ============================================================================================ C2 the pipeline can fail
    banner("C2 C3b K1  CONTROLS: a retained carrier fails; the trigger's gate is the scored gate; the kappa cap does not bind")
    T0d = tset("nodecay", None, 650.0)
    c2 = {f"A<={am:g}": {f_: fit(f_, T0d, 1.0, am, BASE[am][f_], 0.25)[0] for f_ in FEET} for am in (A_PHYS, A_WIDE)}
    check("C2 CONTROL: the no-decay (CDM-like) carrier halo on M*'s gate is rejected: Delta chi^2 > +100 on both footings "
          "(fs = 1, w = 0.25, A <= 2 and A <= 20)", f"{ {k_: {f_: round(x, 1) for f_, x in v_.items()} for k_, v_ in c2.items()} }",
          min(x for v_ in c2.values() for x in v_.values()) > 100, "the pipeline sees a retained halo")
    OUT["numbers"]["C2_nodecay"] = c2

    # C3b: the 'MSPH' trigger's switch (XR14_carrier_halos.xph_switched) against gate_mond for a point-mass lens
    sys.path.insert(0, HERE)
    with contextlib.redirect_stdout(io.StringIO()):
        import XR14_carrier_halos as XH                                # its main does not run on import
    c3b, d3b = [], 0.0
    for z in (0.25, 1.0):
        xce_z = 2.5 * (0.3138 * (1 + z) ** 3 + 0.6862)
        Hz_ = Hz(z); rhob_z = Om * rho_crit0 * (1 + z) ** 3
        for lMb in (11.0, 12.0):
            for f_ in FEET:
                Mb = 10 ** lMb
                rk = np.geomspace(1.0, 2e4, 20000)                     # kpc
                _, fs_ = XH.xph_switched("MSPH", rk, np.full_like(rk, Mb), np.zeros_like(rk), z, XH.A0_KMS[f_])
                e_sph = float(rk[np.where(fs_)[0].max()]) if fs_.any() else 0.0
                fg = gate_mond(Mb * MS, A0[f_], 1e-6, xce_z, "kappa", H=Hz_, rhob=rhob_z)
                e_gate = float(rr[np.where(fg >= 0.5)[0].max()] / MPCm * 1e3) if (fg >= 0.5).any() else 0.0
                fn = gate_mond(Mb * MS, A0[f_], 1e-6, xce_z, "none", H=Hz_, rhob=rhob_z)
                e_none = float(rr[np.where(fn >= 0.5)[0].max()] / MPCm * 1e3) if (fn >= 0.5).any() else 0.0
                d3b = max(d3b, abs(e_sph / e_gate - 1))
                c3b.append(dict(z=z, lMb=lMb, foot=f_, edge_trigger_gate_kpc=e_sph, edge_scored_gate_kpc=e_gate,
                                edge_uncapped_kpc=e_none, cap_binds=bool(e_none > 1.01 * e_gate)))
    check("C3b CONTROL: the gate M*'s carrier's trigger reads is the scored gate: for point-mass baryons the hard edges agree "
          "(z = 0.25 and 1; M_b = 1e11, 1e12; both footings), including where the kappa cap binds",
          "; ".join(f"z{r_['z']:g}/1e{r_['lMb']:g}/{r_['foot'][:3]}: {r_['edge_trigger_gate_kpc']:.0f} vs {r_['edge_scored_gate_kpc']:.0f} kpc"
                    f"{' (cap binds; uncapped ' + format(r_['edge_uncapped_kpc'], '.0f') + ')' if r_['cap_binds'] else ''}" for r_ in c3b)
          + f"; max rel diff {d3b:.1e}", d3b < 0.01 and any(r_["cap_binds"] for r_ in c3b))
    OUT["numbers"]["C3b"] = c3b

    # K1: MS5's kappa cap on the KiDS lenses
    dfk = 0.0
    for b in range(4):
        for lm in LM:
            for f_ in FEET:
                for w in WS:
                    dfk = max(dfk, float(np.max(np.abs(gate_mond(10 ** lm * MS, A0[f_], w, XCE, "kappa")
                                                       - gate_mond(10 ** lm * MS, A0[f_], w, XCE, "none")))))
    dk = 0.0
    for v in VK:
        for f_ in FEET:
            TCs = tset("MSPH", f_, v)
            for w in WS:
                sk_ = [fit(f_, TCs, 1.0, A_PHYS, BASE[A_PHYS][f_], w, form)[0] for form in ("kappa", "none", "local")]
                dk = max(dk, max(sk_) - min(sk_))
    lcap = V_CAP / (H_L * math.sqrt(XCE)) / MPCm
    vfmax = {f_: (G * 10 ** LM.max() * MS * A0[f_]) ** 0.25 / 1e3 for f_ in FEET}
    check("K1 CONTROL: MS5's kappa cap does not bind on KiDS lenses: with M*'s carrier the kappa-capped, uncapped and withdrawn-"
          "local-form scores are identical (every kick, width, footing; A <= 2), and the kappa cap changes f nowhere on the "
          "fit's mass grid", f"max score spread {dk:.1e}; max |f_kappa - f_none| over {len(LM)} masses x 4 bins x 2 footings x 2 "
          f"widths = {dfk:.1e}; l_cap(0.25) = {lcap:.2f} Mpc; largest grid v_f {vfmax['canonical']:.0f}/{vfmax['alt']:.0f} km/s < 325",
          dk < 1e-9 and dfk == 0.0, "the kappa form binds only where v_f > v_cap; stated as non-binding, not assumed")
    OUT["numbers"]["K1"] = dict(score_spread=dk, max_df=dfk, l_cap_Mpc=lcap, vf_max_kms=vfmax)

    # ============================================================================================ the KiDS table
    banner("KiDS ON M*'S CARRIER: fs = 1, A <= 2 gated (A <= 20 beside it); every kick, both widths, both footings")

    def score(mode, v, f_, foot_a0=None, diag=False):
        """one carrier set scored on one footing: {w: {...}}; foot_a0 = the footing whose a0 the trigger used."""
        TCs = tset(mode, foot_a0 or f_, v)
        out = {}
        for w in WS:
            g2, p2 = fit(f_, TCs, 1.0, A_PHYS, BASE[A_PHYS][f_], w)
            g20, p20 = fit(f_, TCs, 1.0, A_WIDE, BASE[A_WIDE][f_], w)
            s2, ps2 = fit(f_, TCs, 0.0, A_PHYS, BASE[A_PHYS][f_], w)
            r_ = dict(gate=g2, per_bin=p2, A20=g20, per_bin_A20=p20, switch_only=s2, switch_only_per_bin=ps2)
            if diag and w == 0.25:
                sc1 = [(fs_, fit(f_, TCs, fs_, A_PHYS, BASE[A_PHYS][f_], w)[0]) for fs_ in np.linspace(0.0, 1.0, 11)]
                sc3 = [(fs_, fit(f_, TCs, fs_, A_PHYS, BASE[A_PHYS][f_], w)[0]) for fs_ in np.linspace(0.0, 3.0, 31)]
                r_["diag_best_fs_0_1"] = min(sc1, key=lambda t_: t_[1])
                r_["diag_best_fs_0_3_unphysical_above_1"] = min(sc3, key=lambda t_: t_[1])
            out[str(w)] = r_
        return out

    TAB = {"MSPH": {}, "L388": {}, "L388_as_run": {}, "L375_on_Mstar_gate": {}, "FK1": {}}
    for mode in ("MSPH", "L388"):
        for v in VK:
            TAB[mode][f"v{int(v)}"] = {f_: score(mode, v, f_, diag=not MUTATE) for f_ in FEET}
            row = TAB[mode][f"v{int(v)}"]
            P(f"  {('M* (MSPH)' if mode == 'MSPH' else 'L388 as written'):16s} v_k {v:3.0f}: w 0.02 "
              f"{row['canonical']['0.02']['gate']:+7.2f}/{row['alt']['0.02']['gate']:+7.2f}   w 0.25 "
              f"{row['canonical']['0.25']['gate']:+7.2f}/{row['alt']['0.25']['gate']:+7.2f}   | A<=20: "
              f"{row['canonical']['0.02']['A20']:+7.2f}/{row['alt']['0.02']['A20']:+7.2f}, {row['canonical']['0.25']['A20']:+7.2f}/"
              f"{row['alt']['0.25']['A20']:+7.2f} | switch alone (w 0.25) {row['canonical']['0.25']['switch_only']:+6.2f}/"
              f"{row['alt']['0.25']['switch_only']:+6.2f}   [{time.time() - T0:.0f}s]")
            P(f"      A per bin (A <= 2, w 0.25) canonical {[a for _, a in row['canonical']['0.25']['per_bin']]} alt "
              f"{[a for _, a in row['alt']['0.25']['per_bin']]}; log M_b {[m for m, _ in row['canonical']['0.25']['per_bin']]} / "
              f"{[m for m, _ in row['alt']['0.25']['per_bin']]}")
    for v in VK:                                                      # 'as run': L388 ran canonical only
        TAB["L388_as_run"][f"v{int(v)}"] = {"alt": score("L388", v, "alt", foot_a0="canonical")}
    if not MUTATE:
        for v in (600.0, 650.0):
            TAB["L375_on_Mstar_gate"][f"v{int(v)}"] = {f_: score("L375", v, f_) for f_ in FEET}
    for v in VKV:
        TAB["FK1"][f"v{int(v)}"] = {f_: score("FK1", v, f_) for f_ in FEET}
    OUT["numbers"]["table"] = TAB

    def worst(mode, kicks=VK, ws=WS, lab="gate"):
        return max(TAB[mode][f"v{int(v)}"][f_][str(w)][lab] for v in kicks for f_ in FEET for w in ws)

    banner("H1 H1b  THE PRE-DECLARED HYPOTHESES")
    w1 = worst("MSPH")
    check("H1 [pre-declared] M*'S CARRIER (L388's trigger reading M*'s own gate's phantom) passes KiDS: Delta chi^2 <= +4 on "
          "both footings, w = 0.02 and 0.25, every kick 575-650 km/s (fs = 1, A <= 2)",
          "; ".join(f"v{int(v)}: " + ", ".join(f"w{w} {TAB['MSPH'][f'v{int(v)}']['canonical'][str(w)]['gate']:+.1f}/"
                                                f"{TAB['MSPH'][f'v{int(v)}']['alt'][str(w)]['gate']:+.1f}" for w in WS) for v in VK)
          + f"  (worst {w1:+.2f})", (w1 <= 4.0) == EXPECT_PASS)
    w1b = worst("L388")
    check("H1b [pre-declared] L388's carrier AS WRITTEN (its matter-only switch in the trigger) passes on the same terms",
          "; ".join(f"v{int(v)}: " + ", ".join(f"w{w} {TAB['L388'][f'v{int(v)}']['canonical'][str(w)]['gate']:+.1f}/"
                                                f"{TAB['L388'][f'v{int(v)}']['alt'][str(w)]['gate']:+.1f}" for w in WS) for v in VK)
          + f"  (worst {w1b:+.2f})", (w1b <= 4.0) == EXPECT_PASS)

    # ============================================================================================ reported
    banner("V1-V5  REPORTED: DE10 beside M*'s carrier, the carrier's share, retention, the variants, 'as run'")
    cmp_ = {}
    for v in (600.0, 650.0):
        for w in WS:
            k_ = f"v{int(v)}/w{w}"
            cmp_[k_] = {f_: dict(DE10_committed=DE10[k_]["kids"][f_],
                                 DE10_carrier_on_Mstar_rules=(TAB["L375_on_Mstar_gate"][f"v{int(v)}"][f_][str(w)]["gate"] if not MUTATE else None),
                                 Mstar_carrier=TAB["MSPH"][f"v{int(v)}"][f_][str(w)]["gate"],
                                 L388_as_written=TAB["L388"][f"v{int(v)}"][f_][str(w)]["gate"]) for f_ in FEET}
            P(f"    {k_:10s}: DE10 committed (A<=20, withdrawn cap, L375 carrier) {DE10[k_]['kids']['canonical']:+7.2f}/{DE10[k_]['kids']['alt']:+7.2f}"
              + (f" | DE10's carrier on M*'s rules {cmp_[k_]['canonical']['DE10_carrier_on_Mstar_rules']:+7.2f}/{cmp_[k_]['alt']['DE10_carrier_on_Mstar_rules']:+7.2f}" if not MUTATE else "")
              + f" | M*'s carrier {cmp_[k_]['canonical']['Mstar_carrier']:+7.2f}/{cmp_[k_]['alt']['Mstar_carrier']:+7.2f}"
              f" | L388 as written {cmp_[k_]['canonical']['L388_as_written']:+7.2f}/{cmp_[k_]['alt']['L388_as_written']:+7.2f}")
    OUT["numbers"]["compare_DE10"] = cmp_
    share = {mode: max(abs(TAB[mode][f"v{int(v)}"][f_]["0.25"]["gate"] - TAB[mode][f"v{int(v)}"][f_]["0.25"]["switch_only"])
                       for v in VK for f_ in FEET) for mode in ("MSPH", "L388")}
    share_min = {mode: min(abs(TAB[mode][f"v{int(v)}"][f_]["0.25"]["gate"] - TAB[mode][f"v{int(v)}"][f_]["0.25"]["switch_only"])
                           for v in VK for f_ in FEET) for mode in ("MSPH", "L388")}
    check("V1 the carrier's share of the score: |Delta chi^2(fs = 1) - Delta chi^2(fs = 0)| at w = 0.25 (A <= 2), and "
          "the diagnostic best amplitude", "; ".join(f"{m_}: {share_min[m_]:.2f}-{share[m_]:.2f}" for m_ in share)
          + ("" if MUTATE else "; best fs in [0,1] (M*, v600) " + "/".join(
              f"{TAB['MSPH']['v600'][f_]['0.25']['diag_best_fs_0_1'][0]:.1f}({TAB['MSPH']['v600'][f_]['0.25']['diag_best_fs_0_1'][1]:+.1f})" for f_ in FEET)
              + ", in [0,3] (unphysical above 1) " + "/".join(
              f"{TAB['MSPH']['v600'][f_]['0.25']['diag_best_fs_0_3_unphysical_above_1'][0]:.1f}"
              f"({TAB['MSPH']['v600'][f_]['0.25']['diag_best_fs_0_3_unphysical_above_1'][1]:+.1f})" for f_ in FEET)),
          True, load_bearing=False)
    RET = {}
    src = HMU if MUTATE else HC
    rmid_ = np.sqrt(EDG[1:] * EDG[:-1]); vol_ = 4 / 3 * math.pi * (EDG[1:] ** 3 - EDG[:-1] ** 3)
    for tag, d in sorted(src["halos"].items()):
        if tag.startswith("nodecay"):
            continue
        b = d["b"]; nd = HC["halos"][f"nodecay_b{b}"]["M_ap"]
        reach = d["diag"]["r_trig_kpc"]
        if tag.startswith("FK1"):                                     # FK1's conversion front at z_l: the outermost radius where
            on_ = np.where(np.array(d["hist"]) * d["m"] / vol_ >= XH.nt_fk1(d["diag"]["z_end"]))[0]   # the carrier reaches n_t
            reach = float(rmid_[on_.max()]) if on_.size else 0.0      # (the halo script's field scans from the empty centre: 0)
        RET[tag] = dict(S=d["M_ap"] / nd, S_cold=d["M_ap_cold"] / nd, decayed=d["diag"]["n_decayed"] / d["n"],
                        phantom_only=d["diag"]["n_decayed_phantom_only"] / max(d["diag"]["n_decayed"], 1),
                        reach_kpc=reach, switch_kpc=d["diag"].get("r_switch_kpc"))
    OUT["numbers"]["retention"] = RET
    for mode, lab, kv in (("L375", "L375 (DE10)", "v600"), ("L388_canonical", "L388 as written, can", "v600"),
                          ("L388_alt", "L388 as written, alt", "v600"), ("MSPH_canonical", "M* (MSPH), can", "v600"),
                          ("MSPH_alt", "M* (MSPH), alt", "v600"), ("FK1", "FK1 variant", "v575")):
        tags = [t for t in RET if t.startswith(mode + "_") and t.endswith("_" + ("v0" if MUTATE else kv))]
        if tags:
            tags.sort(key=lambda t: int(t.split("_b")[1][0]))
            P(f"    retention {lab:22s} ({'v_k = 0' if MUTATE else kv}): S by bin {[round(RET[t]['S'], 3) for t in tags]}, decayed "
              f"{[round(RET[t]['decayed'], 3) for t in tags]}, phantom-only share {[round(RET[t]['phantom_only'], 3) for t in tags]}, "
              f"{'conversion front' if mode == 'FK1' else 'trigger reach'} at z_l {[round(RET[t]['reach_kpc']) for t in tags]} kpc"
              + (f", phantom switched to {[round(RET[t]['switch_kpc']) for t in tags]} kpc" if RET[tags[0]]["switch_kpc"] else ""))
    check("V2 retention per bin (M(<0.5 Mpc/h) against the no-decay halo), decayed fraction, the decays the phantom "
          "alone caused, and the trigger's reach at z_l, per trigger", "see the retention lines and the results JSON", True,
          load_bearing=False)
    asrun = max(TAB["L388_as_run"][f"v{int(v)}"]["alt"][str(w)]["gate"] for v in VK for w in WS)
    check("V3 'as run': L388 ran canonical only; its canonical-a0 carrier scored on the alt footing",
          "; ".join(f"v{int(v)}: " + ", ".join(f"w{w} {TAB['L388_as_run'][f'v{int(v)}']['alt'][str(w)]['gate']:+.1f}" for w in WS) for v in VK)
          + f" (worst {asrun:+.2f})", True, load_bearing=False)
    wf = worst("FK1", kicks=VKV)
    check("V4 the FK1 variant (n^2 trigger on the cold carrier's own density, E^4 gate, sharp): its KiDS score",
          "; ".join(f"v{int(v)}: " + ", ".join(f"w{w} {TAB['FK1'][f'v{int(v)}']['canonical'][str(w)]['gate']:+.1f}/"
                                                f"{TAB['FK1'][f'v{int(v)}']['alt'][str(w)]['gate']:+.1f}" for w in WS) for v in VKV)
          + f" (worst {wf:+.2f}; {'passes' if wf <= 4 else 'FAILS'} the <= +4 rule)", True, load_bearing=False)
    wA20 = {m_: worst(m_, lab="A20") for m_ in ("MSPH", "L388")}
    check("V5 DE10's bound A <= 20: the same scores with the 2-halo amplitude free to 20",
          "; ".join(f"{m_} worst {x:+.2f}" for m_, x in wA20.items()), True, load_bearing=False)

    banner("SUMMARY")
    P(f"  KiDS-1000 on M*'s gate (MOND-sector switch, p = 1, x_c0 = 2.5, MS5's kappa cap -- non-binding, sigma = 1, 1/m = 0.1 Mpc),")
    P(f"  fs = 1, A <= 2, both footings, w = 0.02/0.25, kicks 575-650 km/s:")
    P(f"    M*'s carrier (L388's trigger on M*'s own gate's phantom): worst Delta chi^2 {w1:+.2f} -> {'PASS' if w1 <= 4 else 'FAIL'}")
    P(f"    L388's carrier as written (its matter-only switch):         worst Delta chi^2 {w1b:+.2f} -> {'PASS' if w1b <= 4 else 'FAIL'}")
    P(f"    FK1 variant (575/650):                                       worst Delta chi^2 {wf:+.2f} -> {'PASS' if wf <= 4 else 'FAIL'}")
    P(f"    'as run' (canonical carrier on alt):                         worst Delta chi^2 {asrun:+.2f}")
    OUT["numbers"]["summary"] = dict(worst_Mstar=w1, worst_L388_as_written=w1b, worst_FK1=wf, worst_as_run=asrun, worst_A20=wA20)
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o)))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
