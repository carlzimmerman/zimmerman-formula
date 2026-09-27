#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR9_kids_flagship.py -- THE SMALL-REGION DOOR, part 1 of 3: KiDS-1000 with the carrier's own lensing, and the z = 2.5
flagship, scanned over the vacuum gate's threshold.  Independent cross-thread review (2026-09-26, night).  Read-only on
every committed file: DE8's operator and fit, MS2's door and DE9's smooth flagship are loaded unedited or reimplemented
with a control that reproduces their committed numbers.

THE DOOR.  The converged model's MOND regions are large (an L* galaxy's edge ~1.4-1.7 Mpc at z = 0) because the
switch-only KiDS cap x_c,eff(0.25) <= 3.867 (DE2; 4.35 on the MOND-sector reading at w = 0.25, DE9) was derived with
NO carrier lensing.  DE10 then found that with the carrier's lensing KiDS passes easily at p = 1, x_c0 = 2.5 (-37/-34
hard, -32/-29 at w = 0.25).  The door: RAISE the threshold (smaller regions, r_e ~ v_f/(H sqrt(x_c,eff))) and let the
CDM-like carrier and the correlated matter (the 2-halo term) supply the lensing at 0.5-3 Mpc.

PRE-DECLARED HYPOTHESIS (given by the coordinating review before any scan cell was computed; reported either way):
  H  some threshold ABOVE the switch-only KiDS cap passes KiDS with the carrier, and at that threshold the Local Group
     zero-velocity radius and the cluster-infall EFE slope move into their bands (the second half is scored by
     XR9_environment.py; the verdict is XR9_gate_table.py's).
  The door FAILS if KiDS needs the private phantom out to >~ 1.5 Mpc even with the carrier.

THE MODEL AS SCORED (each piece from its committed source):
  switch   DE8's region operator (L361/CV1: screened w, gated phantom P, sigma = 1, 1/m = 0.1 Mpc; lensing on Phi = u + f P
           with f' P), MS2's MOND-sector reading x = 4 pi G (rho_b + rho_ph - f_b rho_bar_m)/H^2 (carrier-blind), the smooth
           gate f = W(t), t = (U/x_c,eff - 1)/(2w) + 1/2 at w = 0.25 (DE9's window width; w = 0.02 reported beside it);
  cap      MS5's kappa form (61a3a0858): U = min(x, v_cap^2 kappa_X^2/H^2), kappa_X = 1/r for a spherical lens, so every
           region stops at l_cap(z) = v_cap/(H sqrt(x_c,eff)), v_cap = 325 km/s (MS3).  The withdrawn local form
           threshold x max(1, v_loc^2/v_cap^2) is used ONLY in the control that reproduces DE10 (labelled);
  gate     x_c,eff(z) = x_c0 E(z)^(2p) (L359's background), p in {1, 1.5}, x_c0 in {2.5, 3.5, 5, 7, 10, 14, 20};
  carrier  L375's shell-model halos, re-run with each cell's refitted lens masses (XR9_carrier_halos.py, L390's recipe on
           the scored switch; seeds DE10's), v_k = 600 and 650 km/s, projected to 20 Mpc (the carrier's own infall kept);
  fit      L352's KiDS machinery through DE8 (Brouwer+21 four bins, full covariance, M_b profiled per bin, linear 2-halo
           term per bin); Delta chi^2 against L352's unswitched model with the same 2-halo bound; pass = <= +4 on both
           footings (DE10's rule).
  THE OWNER'S FIVE RULES (2026-09-26), built in before scoring:
    1 the carrier amplitude is physical, fs = 1 in every gated score; fitted amplitudes are DIAGNOSTICS, labelled
      (fs in [0, 1] -- at most the halo's own post-trigger carrier -- and fs in [0, 3], unphysical above 1);
    2 the 2-halo amplitude (the lens bias) is capped at A <= 2 in the gated score; A per bin is reported for every
      cell, and the uncapped A <= 20 (DE10's) is reported beside it;
    3 the carrier halos are re-run with each cell's refitted masses (not DE10's L390 masses);
    4 the flagship caps x_c0 hard (DE9's MOND-sector cap), heavier galaxies first: cells above it are MARKED failing;
    5 the forest only gets easier as the threshold rises: every cell carries DE11's pass (worst 0.0041) as a lower
      bound "by monotonicity from DE11" (every scan cell's x_c,eff(z) >= the converged cell's at every z >= 0).
  THE FLAGSHIP (z = 2.5, M_b = 1e10, 1e10.5, 1e11, 1e11.5, both footings, carrier cleared):
    (a) MS2's door at r_F (g_bar = 0.1 a0), hard, loaded unedited, f_CGM = 0 gated (0.1, 0.3, 1 reported), plus the
        kappa cap (r_F <= l_cap(2.5));
    (b) DE9's smooth flagship on DE8's operator (MOND-sector reading, w = 0.25, sigma = 1, 1/m = 0.1 Mpc) with the kappa
        cap: the zero-point shift at r_F must stay >= -0.05 dex (DE9's tolerance).  Gate = (a) and (b).

CHECKS
  C0 CONTROL: this lane's fit loop reproduces L352's unswitched baseline chi^2 exactly (A <= 20).
  C1 CONTROL: with DE10's configuration (L390-mass halos, the withdrawn local cap, fs = 1, A <= 20), DE10's committed
     KiDS table (2 kicks x 2 widths x 2 footings) and its preferred amplitudes are reproduced exactly (1e-9).
  C2 CONTROL: the halo plan's refitted masses equal the refit on the kappa-form switch (the halos match the scored
     switch).
  C3 (reported) at p = 1, x_c0 = 2.5 the kappa form scores DE10's configuration identically (neither cap binds on the
     fitted lenses).
  C4 CONTROL: MS2's committed F1 rows (door on at r_F and the shift, p = 1, x_c0 = 2.5, M_b <= 1e11, 4 CGM shares, both
     footings) are reproduced exactly.
  C5 CONTROL: DE9's committed smooth flagship cap on the MOND-sector reading at w = 0.25 (329.36 / 436.19) is
     reproduced (1e-6 relative) -- DE9's gate had no cap.
  C6 CONTROL (switch only, DE9's cap): with fs = 0 and A <= 20 the switch alone passes at DE9's MOND-sector w = 0.25 cap
     x_c,eff(0.25) = 4.3473 and fails 1/256 of a grid step above it (4.3477).
  M1 [load-bearing; MUTATE must fail] THE CARRIER'S LENSING IS IN THE SCORE: at every cell |Delta chi^2(run's fs) -
     Delta chi^2(fs = 0)| > 1 on both footings (w = 0.25, v_k = 600, A <= 2).
  SO (reported) switch-only behaviour: with fs = 0 (A <= 20) KiDS passes at x_c,eff(0.25) <= 4.35 and fails at every
     cell above -- DE2/DE9's switch-only cap.  Under MUTATE this IS the gated column.
  H-K [pre-declared, reported] the KiDS half of H: some cell with x_c,eff(0.25) > 4.35 passes KiDS (fs = 1, A <= 2, both
     kicks, both footings, w = 0.25).
  H-R (reported) where the passing cells put the lens regions: the largest fully-on radius and the f = 0 radius of the
     fitted lenses at z = 0.25 -- the door fails if KiDS needs the phantom out to >~ 1.5 Mpc.
  KC (reported) the KiDS cap itself with the carrier: the largest x_c,eff(0.25) passing (w = 0.25, fs = 1, A <= 2, both
     kicks and footings), bisected between the converged cell and x_c0 = 3.5, with the halos of either cell.
  F1 (reported) the flagship per cell: (a), (b), both, and the largest x_c0 per mass.
MUTATE=1 switches the carrier's lensing off (fs = 0 in every gated score): the scan must recover DE2/DE9's switch-only
behaviour (high thresholds fail KiDS) and M1 must FAIL (rc = 1).

SCOPE.  Spherical, isolated lenses (no neighbour phantoms beyond the linear 2-halo term); one accretion history (L375's
fiducial); the carrier's profile from the shell model; the upper-branch phantom read ungated in the switch variable
(on-branch convention); the heat filter omitted.  The cap and the trigger have no action for the trigger yet (MS5 gives
the cap's).  The 2-halo term is L352's linear one with a free amplitude: A is the lens bias times the linear matter
correlation, not the neighbours' phantoms.

Run from the repository root (after XR9_carrier_halos.py is complete):
    python3 real_research/cross_thread_review_2026_09_26/XR9_kids_flagship.py          (MUTATE=1 for the control)
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEDIR = os.path.join(REPO, "real_research", "dark_energy_2026")
MSDIR = os.path.join(REPO, "real_research", "mond_sector_gate_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR9_kids_flagship"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR9 part 1 (KiDS + flagship)", "mutate": MUTATE, "checks": {}, "numbers": {}}
FEET = ("canonical", "alt")
PS = (1.0, 1.5)
XC0S = (2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0)
CELLS = [(p, x0) for p in PS for x0 in XC0S]
VK = (600.0, 650.0)
W_GATE, W_HARD = 0.25, 0.02
V_CAP = 325e3
A_PHYS, A_WIDE = 2.0, 20.0
FS_RUN = 0.0 if MUTATE else 1.0
SO_CAP = 4.347265625000002                                           # DE9: MOND-sector w = 0.25 switch-only KiDS cap
E2G = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                       # L359's gate background (DE1-DE10)
ck = lambda p, x0: f"p{p:g}_x{x0:g}"


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
    if MUTATE: P("\n  *** MUTATE=1: the carrier's lensing is switched off (fs = 0 in every gated score); M1 must FAIL ***")

    # ------------------------------------------------------------------------------ DE8's operator and fit, unedited
    P8 = os.path.join(DEDIR, "DE8_kids_sigma_axis_both_branches.py")
    D8 = {"__name__": "de8", "__file__": P8}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P8).read().split("# ============================================================================================ C1 C2 C3 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
    (solve_region, esd_from_mlens, Wg, rr, rf, nu_vec, G, MS, A0, KPC_, N, Ed, Sd, Ci, twoh_cache, LM, project_M2,
     annulus_esd, Rp, Rd, MPCm, esd_bin, Hz, Om, rho_crit0) = [D8[k] for k in (
        "solve_region", "esd_from_mlens", "Wg", "rr", "rf", "nu_vec", "G", "MS", "A0", "KPC_", "N", "Ed", "Sd", "Ci",
        "twoh_cache", "LM", "project_M2", "annulus_esd", "Rp", "Rd", "MPCm", "esd_bin", "Hz", "Om", "rho_crit0")]
    BASE20 = D8["BASE"]; FB = D8["FB"]; rho_bar = D8["rho_bar"]; H_L = D8["H_L"]
    P(f"  DE8 loaded (L352's KiDS data, operator, 2-halo template)   [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------ the carrier halos
    HC = json.load(open(os.path.join(HERE, "XR9_carrier_halos_results.json")))
    PLAN, LM90 = HC["plan"], HC["L390_lm"]
    EDG = np.array(HC["edges_kpc"])
    need = {f"b{b}_lm{lm:.2f}_v{int(v)}" for c_ in PLAN.values() for b, lm in enumerate(c_["lm_refit"]) for v in VK}
    need |= {f"b{b}_lm{LM90[b]:.2f}_v{int(v)}" for b in range(4) for v in VK}
    miss = sorted(t for t in need if t not in HC["halos"])
    if miss:
        P(f"  {len(miss)} carrier halos missing from XR9_carrier_halos_results.json ({miss[:4]} ...): run XR9_carrier_halos.py first")
        sys.exit(2)
    R90 = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L390_kids_resolved_linear_gate_results.json")))["numbers"]
    MB90 = R90["M_b"]["p=1, x_c0=2.5"]

    def carrier_rho_si(tag):                                          # DE10's carrier_rho_si (L375's template density step)
        d = HC["halos"][tag]
        e = EDG; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
        rho = np.array(d["hist"]) * d["m"] / vol
        return np.interp(np.log(rr / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3

    _TC = {}

    def template(tag):
        if tag not in _TC:
            b = HC["halos"][tag]["b"]
            M2 = project_M2(carrier_rho_si(tag))
            _TC[tag] = annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[b])
        return _TC[tag]

    # ------------------------------------------------------------------------------ the gate (DE10's, the cap as an option)
    def gate_mond(Mb, a0, w, xce, form="kappa", H=None, rhob=None):
        """MS2's door on the point-mass lens (baryons + phantom, carrier-blind), smooth width w, region connected to the
        centre; form 'kappa' = MS5's cap (U = min(x, (v_cap/(r H))^2)); 'local' = DE10's withdrawn form; 'none'."""
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

    def model(b, lm, foot, w, xce, form):
        key = (b, round(float(lm), 3), foot, w, round(xce, 9), form)
        if key not in _ESD:
            Mb = 10 ** lm * MS; a0 = A0[foot]
            _ESD[key] = esd_from_mlens(Mb, solve_region(Mb, a0, gate_mond(Mb, a0, w, xce, form), 100 * KPC_, 1.0), b)
        return _ESD[key]

    def fit(foot, TCs, fs, amax, base, mfun):
        """L352/DE8/DE10's fit: per bin the grid mass with the smallest diagonal chi^2 (2-halo amplitude A in [0, amax]),
        then the full-covariance chi^2 minus the baseline.  Returns (Delta chi^2, [(log M_b, A) per bin])."""
        mods, per = [], []
        for b in range(4):
            best = None
            for lm in LM:
                mk0 = mfun(b, lm) + (fs * TCs[b] if TCs is not None else 0.0)
                t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, amax)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, mk, float(lm), A)
            mods.append(best[1]); per.append((round(best[2], 2), round(best[3], 3)))
        dv = np.concatenate(Ed) - np.concatenate(mods)
        return float(dv @ Ci @ dv) - base, per

    # ============================================================================================ C0 baseline
    banner("C0  CONTROL: this lane's fit loop reproduces L352's unswitched baseline; the baseline with A <= 2")
    unsw = lambda foot: (lambda b, lm: esd_bin(b, lm, A0[foot], 0.0, "none", False)[0])
    B20 = {f_: fit(f_, None, 0.0, A_WIDE, 0.0, unsw(f_)) for f_ in FEET}
    B2 = {f_: fit(f_, None, 0.0, A_PHYS, 0.0, unsw(f_)) for f_ in FEET}
    d0 = max(abs(B20[f_][0] - BASE20[f_]) for f_ in FEET)
    BASE = {A_WIDE: {f_: B20[f_][0] for f_ in FEET}, A_PHYS: {f_: B2[f_][0] for f_ in FEET}}
    check("C0 CONTROL: the fit loop with A <= 20 reproduces L352's unswitched baseline chi^2 (both footings)",
          f"{ {f_: round(B20[f_][0], 4) for f_ in FEET} } vs L352 { {f_: round(BASE20[f_], 4) for f_ in FEET} } (max |diff| {d0:.1e}); "
          f"baseline A per bin (A <= 20): { {f_: [a for _, a in B20[f_][1]] for f_ in FEET} }; with A <= 2: chi^2 "
          f"{ {f_: round(B2[f_][0], 3) for f_ in FEET} }, A { {f_: [a for _, a in B2[f_][1]] for f_ in FEET} }", d0 < 1e-9,
          "the unswitched (isolated-QUMOND) baseline is scored against the same 2-halo bound as the model it is compared with")
    OUT["numbers"]["baseline"] = {"A<=20": {f_: dict(chi2=B20[f_][0], per_bin=B20[f_][1]) for f_ in FEET},
                                  "A<=2": {f_: dict(chi2=B2[f_][0], per_bin=B2[f_][1]) for f_ in FEET}}

    # ============================================================================================ C1 DE10 reproduced
    banner("C1-C3  CONTROLS: DE10's committed KiDS table; the halos' masses; the kappa cap at the converged cell")
    DE10 = json.load(open(os.path.join(DEDIR, "DE10_kids_converged_model_results.json")))["numbers"]["table"]
    XCE0 = 2.5 * (0.3138 * 1.25 ** 3 + 0.6862)
    T90 = {v: [template(f"b{b}_lm{LM90[b]:.2f}_v{int(v)}") for b in range(4)] for v in VK}
    c1, d1 = {}, 0.0
    for v in VK:
        for w in (W_HARD, W_GATE):
            mf = lambda foot, w=w: (lambda b, lm: model(b, lm, foot, w, XCE0, "local"))
            k = {f_: fit(f_, T90[v], 1.0, A_WIDE, BASE20[f_], mf(f_))[0] for f_ in FEET}
            bf = {f_: min(((fs_, fit(f_, T90[v], fs_, A_WIDE, BASE20[f_], mf(f_))[0]) for fs_ in np.linspace(0.0, 1.2, 13)),
                          key=lambda t_: t_[1]) for f_ in FEET}
            ref = DE10[f"v{int(v)}/w{w}"]
            d1 = max(d1, *(abs(k[f_] - ref["kids"][f_]) for f_ in FEET), *(abs(bf[f_][1] - ref["best_fs"][f_][1]) for f_ in FEET),
                     *(abs(bf[f_][0] - ref["best_fs"][f_][0]) for f_ in FEET))
            c1[f"v{int(v)}/w{w}"] = dict(kids=k, best_fs=bf)
    check("C1 CONTROL: DE10's configuration (L390-mass halos re-run here with DE10's seeds, the WITHDRAWN local cap, fs = 1, "
          "A <= 20) reproduces DE10's committed KiDS table and preferred amplitudes, 2 kicks x 2 widths x 2 footings",
          "; ".join(f"{k_}: {v_['kids']['canonical']:+.3f}/{v_['kids']['alt']:+.3f}" for k_, v_ in c1.items()) + f" (max |diff| {d1:.1e})",
          d1 < 1e-9, "the carrier halos, templates, operator and fit are DE10's; this is the control for the withdrawn cap form")
    OUT["numbers"]["C1_DE10_reproduced"] = c1
    # C2: the plan's masses are the kappa-form refit (L390's recipe: switch only, canonical, A <= 20, w = 0.25)
    refit_k = {}
    for (p, x0) in CELLS:
        xce = x0 * E2G(0.25) ** p
        per = fit("canonical", None, 0.0, A_WIDE, BASE20["canonical"], lambda b, lm: model(b, lm, "canonical", W_GATE, xce, "kappa"))[1]
        refit_k[ck(p, x0)] = [lm for lm, _ in per]
    same = all(refit_k[k_] == PLAN[k_]["lm_refit"] for k_ in refit_k)
    check("C2 CONTROL: the carrier halos' masses (XR9_carrier_halos.py's plan) are the refit on the scored kappa-form switch "
          "(L390's recipe) at every cell", f"identical at {sum(refit_k[k_] == PLAN[k_]['lm_refit'] for k_ in refit_k)}/{len(refit_k)} cells",
          same)
    k3 = {}
    for v in VK:
        mf = lambda foot: (lambda b, lm: model(b, lm, foot, W_GATE, XCE0, "kappa"))
        k3[v] = {f_: fit(f_, T90[v], 1.0, A_WIDE, BASE20[f_], mf(f_))[0] for f_ in FEET}
    d3 = max(abs(k3[v][f_] - c1[f"v{int(v)}/w{W_GATE}"]["kids"][f_]) for v in VK for f_ in FEET)
    check("C3 (reported) at p = 1, x_c0 = 2.5 the kappa-form cap scores DE10's configuration as the withdrawn local form does "
          "(w = 0.25): neither cap binds on the fitted KiDS lenses", f"max |diff| {d3:.1e}", d3 < 1e-6, load_bearing=False)

    # ============================================================================================ the KiDS scan
    banner("THE KiDS SCAN: kappa-cap MOND-sector switch, carrier re-run per cell, fs = 1 gated with A <= 2 (and A <= 20 beside it)")
    lcap = lambda xce, H=H_L: V_CAP / (H * math.sqrt(xce)) / MPCm      # l_cap in Mpc
    KT = {}
    for (p, x0) in CELLS:
        key = ck(p, x0); xce = x0 * E2G(0.25) ** p; lmr = PLAN[key]["lm_refit"]
        row = dict(p=p, xc0=x0, xce_025=xce, l_cap_025_Mpc=lcap(xce), lm_refit=lmr, kids={}, edges={})
        for w in (W_GATE, W_HARD):
            for v in VK:
                TCs = [template(f"b{b}_lm{lmr[b]:.2f}_v{int(v)}") for b in range(4)]
                for f_ in FEET:
                    mf = lambda b, lm, f_=f_, w=w: model(b, lm, f_, w, xce, "kappa")
                    r_ = {}
                    for lab, fs, am in (("gate", FS_RUN, A_PHYS), ("gate_A20", FS_RUN, A_WIDE),
                                        ("switch_only_A2", 0.0, A_PHYS), ("switch_only_A20", 0.0, A_WIDE)):
                        d_, per = fit(f_, TCs, fs, am, BASE[am][f_], mf)
                        r_[lab] = dict(dchi2=d_, per_bin=per)
                    if w == W_GATE and not MUTATE:
                        sc1 = [(fs_, fit(f_, TCs, fs_, A_PHYS, BASE[A_PHYS][f_], mf)[0]) for fs_ in np.linspace(0.0, 1.0, 11)]
                        sc3 = [(fs_, fit(f_, TCs, fs_, A_PHYS, BASE[A_PHYS][f_], mf)[0]) for fs_ in np.linspace(0.0, 3.0, 31)]
                        r_["diag_best_fs_0_1"] = min(sc1, key=lambda t_: t_[1])
                        r_["diag_best_fs_0_3_unphysical_above_1"] = min(sc3, key=lambda t_: t_[1])
                    row["kids"][f"w{w}/v{int(v)}/{f_}"] = r_
        # the fitted lenses' regions at z = 0.25 (w = 0.25, v = 600 gate fit, canonical and alt)
        for f_ in FEET:
            ed = []
            for b, (lmb, _) in enumerate(row["kids"][f"w{W_GATE}/v600/{f_}"]["gate"]["per_bin"]):
                ff = gate_mond(10 ** lmb * MS, A0[f_], W_GATE, xce, "kappa")
                on1 = np.where(ff >= 1 - 1e-9)[0]; onp = np.where(ff > 0)[0]
                ed.append(dict(lm=lmb, r_full_Mpc=float(rr[on1.max()] / MPCm) if on1.size else 0.0,
                               r_zero_Mpc=float(rr[onp.max()] / MPCm) if onp.size else 0.0))
            row["edges"][f_] = ed
        g = [row["kids"][f"w{W_GATE}/v{int(v)}/{f_}"]["gate"]["dchi2"] for v in VK for f_ in FEET]
        row["pass"] = all(x <= 4.0 for x in g)
        row["pass_A20"] = all(row["kids"][f"w{W_GATE}/v{int(v)}/{f_}"]["gate_A20"]["dchi2"] <= 4.0 for v in VK for f_ in FEET)
        row["pass_hard"] = all(row["kids"][f"w{W_HARD}/v{int(v)}/{f_}"]["gate"]["dchi2"] <= 4.0 for v in VK for f_ in FEET)
        row["switch_only_pass_A20"] = all(row["kids"][f"w{W_GATE}/v600/{f_}"]["switch_only_A20"]["dchi2"] <= 4.0 for f_ in FEET)
        row["switch_only_pass_A2"] = all(row["kids"][f"w{W_GATE}/v600/{f_}"]["switch_only_A2"]["dchi2"] <= 4.0 for f_ in FEET)
        KT[key] = row
        gg = lambda lab, v=600: "/".join(f"{row['kids'][f'w{W_GATE}/v{v}/{f_}'][lab]['dchi2']:+6.1f}" for f_ in FEET)
        P(f"  {key:9s} x_c,eff(0.25) {xce:6.2f} (l_cap {row['l_cap_025_Mpc']:.2f} Mpc): gate fs={FS_RUN:g}, A<=2: v600 {gg('gate')} "
          f"v650 {gg('gate', 650)} {'PASS' if row['pass'] else 'fail'} | A<=20 {gg('gate_A20')} | switch only A<=20 "
          f"{gg('switch_only_A20')} A<=2 {gg('switch_only_A2')} | hard w: "
          + "/".join(f"{row['kids'][f'w{W_HARD}/v600/{f_}']['gate']['dchi2']:+6.1f}" for f_ in FEET) + f"   [{time.time() - T0:.0f}s]")
        P(f"      A per bin (gate, v600): canonical {[a for _, a in row['kids'][f'w{W_GATE}/v600/canonical']['gate']['per_bin']]}, alt "
          f"{[a for _, a in row['kids'][f'w{W_GATE}/v600/alt']['gate']['per_bin']]};  A<=20: canonical "
          f"{[a for _, a in row['kids'][f'w{W_GATE}/v600/canonical']['gate_A20']['per_bin']]};  lens log M_b "
          f"{[m for m, _ in row['kids'][f'w{W_GATE}/v600/canonical']['gate']['per_bin']]};  regions (canonical) full-on / f=0 "
          + ", ".join(f"{e_['r_full_Mpc']:.2f}/{e_['r_zero_Mpc']:.2f}" for e_ in row["edges"]["canonical"]) + " Mpc")
        if not MUTATE:
            P("      DIAGNOSTIC (not gated) best carrier amplitude, A <= 2: fs in [0, 1] "
              + "/".join(f"{row['kids'][f'w{W_GATE}/v600/{f_}']['diag_best_fs_0_1'][0]:.1f}({row['kids'][f'w{W_GATE}/v600/{f_}']['diag_best_fs_0_1'][1]:+.1f})" for f_ in FEET)
              + "; fs in [0, 3] (unphysical above 1) "
              + "/".join(f"{row['kids'][f'w{W_GATE}/v600/{f_}']['diag_best_fs_0_3_unphysical_above_1'][0]:.1f}({row['kids'][f'w{W_GATE}/v600/{f_}']['diag_best_fs_0_3_unphysical_above_1'][1]:+.1f})" for f_ in FEET))
    OUT["numbers"]["kids"] = KT

    # ============================================================================================ C6, M1, SO, H-K, H-R
    banner("C6 M1 SO H-K H-R  THE SWITCH-ONLY CAP, THE CARRIER'S ROLE, AND THE DOOR'S KiDS HALF")
    so = {}
    for xt in (SO_CAP, SO_CAP + 0.1 / 256):
        so[xt] = {f_: fit(f_, None, 0.0, A_WIDE, BASE20[f_], lambda b, lm, f_=f_: model(b, lm, f_, W_GATE, xt, "none"))[0] for f_ in FEET}
    check("C6 CONTROL: with fs = 0 and A <= 20 (DE9's switch-only fit, no cap) the switch alone passes at DE9's MOND-sector "
          "w = 0.25 KiDS cap x_c,eff(0.25) = 4.3473 and fails 1/256 of DE9's grid step above it",
          f"at 4.3473: {so[SO_CAP]['canonical']:+.2f}/{so[SO_CAP]['alt']:+.2f}; at 4.3477: {so[SO_CAP + 0.1 / 256]['canonical']:+.2f}/"
          f"{so[SO_CAP + 0.1 / 256]['alt']:+.2f}", max(so[SO_CAP].values()) <= 4.0 < max(so[SO_CAP + 0.1 / 256].values()))
    dm = {k_: min(abs(r_["kids"][f"w{W_GATE}/v600/{f_}"]["gate"]["dchi2"] - r_["kids"][f"w{W_GATE}/v600/{f_}"]["switch_only_A2"]["dchi2"])
                  for f_ in FEET) for k_, r_ in KT.items()}
    check("M1 THE CARRIER'S LENSING IS IN THE SCORE: at every cell |Delta chi^2(run's fs) - Delta chi^2(fs = 0)| > 1 on both "
          "footings (w = 0.25, v_k = 600, A <= 2) -- MUTATE (fs = 0) must fail this", f"smallest difference {min(dm.values()):.2f}",
          min(dm.values()) > 1.0)
    above = [k_ for k_, r_ in KT.items() if r_["xce_025"] > SO_CAP]
    so_ok = all((not KT[k_]["switch_only_pass_A20"]) for k_ in above) and all(KT[k_]["switch_only_pass_A20"] for k_ in KT if k_ not in above)
    check("SO (reported) switch-only behaviour: with fs = 0 (A <= 20) KiDS passes below DE9's switch-only cap (4.35) and fails at "
          "every cell above it -- under MUTATE this is the gated column",
          f"cells above the cap: {above}; switch-only passes there: {[k_ for k_ in above if KT[k_]['switch_only_pass_A20']]}; "
          f"below: {[k_ for k_ in KT if k_ not in above]} pass {[KT[k_]['switch_only_pass_A20'] for k_ in KT if k_ not in above]}",
          so_ok, load_bearing=False)
    passing = [k_ for k_ in KT if KT[k_]["pass"]]
    hk = [k_ for k_ in above if KT[k_]["pass"]]
    check("H-K [pre-declared, reported] the KiDS half of the door: some cell with x_c,eff(0.25) above the switch-only cap passes "
          "KiDS with the carrier (fs = 1, A <= 2, both kicks, both footings, w = 0.25)",
          f"passing cells: {passing}; above the switch-only cap: {hk}; with A <= 20 (DE10's bound) passing: "
          f"{[k_ for k_ in KT if KT[k_]['pass_A20']]}; hard gate (w = 0.02) passing: {[k_ for k_ in KT if KT[k_]['pass_hard']]}",
          len(hk) > 0, load_bearing=False)
    rz = {k_: max(e_["r_zero_Mpc"] for f_ in FEET for e_ in KT[k_]["edges"][f_]) for k_ in KT}
    rfull = {k_: max(e_["r_full_Mpc"] for f_ in FEET for e_ in KT[k_]["edges"][f_]) for k_ in KT}
    check("H-R (reported) the lens regions of the passing cells: the largest fully-on radius and f = 0 radius over the four "
          "fitted lenses at z = 0.25 (the door fails if KiDS needs the phantom out to >~ 1.5 Mpc)",
          "; ".join(f"{k_}: {rfull[k_]:.2f}/{rz[k_]:.2f} Mpc{' (passes)' if KT[k_]['pass'] else ''}" for k_ in KT), True, load_bearing=False)
    OUT["numbers"]["door_kids"] = dict(passing=passing, above_switch_only_cap=above, passing_above_cap=hk,
                                       lens_region_full_Mpc=rfull, lens_region_zero_Mpc=rz)

    # ============================================================================================ KC the carrier-inclusive cap
    banner("KC  THE KiDS CAP ITSELF: the largest x_c,eff(0.25) that passes (w = 0.25, run's fs, A <= 2, both kicks and footings)")

    def kids_worst(xce, lmr):
        worst = -math.inf
        for v in VK:
            TCs = [template(f"b{b}_lm{lmr[b]:.2f}_v{int(v)}") for b in range(4)]
            for f_ in FEET:
                worst = max(worst, fit(f_, TCs, FS_RUN, A_PHYS, BASE[A_PHYS][f_],
                                       lambda b, lm, f_=f_: model(b, lm, f_, W_GATE, xce, "kappa"))[0])
        return worst

    KC_ = {}
    for lab, lmr in (("halos at p1_x2.5's refit masses", PLAN["p1_x2.5"]["lm_refit"]), ("halos at p1_x3.5's refit masses", PLAN["p1_x3.5"]["lm_refit"])):
        lo, hi = 2.5 * E2G(0.25), 3.5 * E2G(0.25)
        wl, wh = kids_worst(lo, lmr), kids_worst(hi, lmr)
        if wl <= 4.0 < wh:
            for _ in range(12):
                mid = 0.5 * (lo + hi)
                if kids_worst(mid, lmr) <= 4.0: lo = mid
                else: hi = mid
            KC_[lab] = dict(cap=lo, bracket=[lo, hi], x_c0_max_p1=lo / E2G(0.25), x_c0_max_p15=lo / E2G(0.25) ** 1.5)
        else:
            KC_[lab] = dict(cap=None, worst_at_ends=[wl, wh])
        P(f"    {lab}: " + (f"cap x_c,eff(0.25) = {KC_[lab]['cap']:.4f} -> x_c0 <= {KC_[lab]['x_c0_max_p1']:.3f} at p = 1, "
                            f"{KC_[lab]['x_c0_max_p15']:.3f} at p = 1.5" if KC_[lab]["cap"] else f"no crossing in [3.25, 4.55]: {KC_[lab]}")
          + f"   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["kids_cap_with_carrier"] = KC_
    check("KC (reported) THE KiDS CAP WITH THE CARRIER at w = 0.25 (the largest x_c,eff(0.25) passing on both kicks and footings, "
          "A <= 2; bisected, the fit is a step function of the threshold) against the switch-only cap 4.3473 (DE9)",
          "; ".join(f"{k_}: {v_['cap']:.4f}" if v_.get("cap") else f"{k_}: none" for k_, v_ in KC_.items()), True,
          "how far the carrier's own lensing moves the threshold KiDS allows", load_bearing=False)

    # ============================================================================================ the flagship
    banner("F  THE FLAGSHIP AT z = 2.5: (a) MS2's door at r_F with the kappa cap; (b) DE9's smooth operator, w = 0.25, kappa cap")
    P2 = os.path.join(MSDIR, "MS2_mond_sector_door_flagship_web.py")
    M2 = {"__name__": "ms2", "__file__": P2}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P2).read().split("# ============================================================================================ C1, C2 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M2)
    MS2R = json.load(open(os.path.join(MSDIR, "MS2_mond_sector_door_flagship_web_results.json")))["numbers"]["F1"]
    E2m, Om_zm, rho_bar_m, rho_switch, halo2, G2, MSUN2, A02, KPC2, nu2 = (M2[k_] for k_ in (
        "E2", "Om_z", "rho_bar_m", "rho_switch", "halo", "G", "MSUN", "A0", "KPC", "nu"))
    H0m = math.sqrt(8 * math.pi * G2 * M2["D4"]["rho_crit"](0.0) / 3)          # MS2/DE4's H0 (h = 0.6736)
    d4 = 0.0
    for fc, rows in MS2R.items():
        for rw in rows:
            sh, on = M2["shift"](10 ** rw["lMb"], rw["foot"], 2.5, 1.0, 2.5, 0.0, float(fc), "contrast", "mond")
            d4 = max(d4, abs(sh - rw["door_shift"]), abs(float(on) - float(rw["door_on"])))
    check("C4 CONTROL: MS2's committed F1 rows (door on at r_F and the zero-point shift; p = 1, x_c0 = 2.5; M_b = 1e10-1e11; "
          "f_CGM = 0, 0.1, 0.3, 1; both footings) are reproduced exactly", f"max |diff| {d4:.1e}", d4 < 1e-12)

    def door(Mb, foot, p, x0, fcgm):
        """MS2's door at r_F (hard, contrast reading) AND the kappa cap r_F <= l_cap(2.5); returns (on, shift, X_F density,
        X_F kappa): the largest x_c,eff(2.5) the density keeps on at r_F, and the largest the kappa cap allows."""
        z = 2.5; a0 = A02[foot]
        on_d, rF, H = M2["switch_on"](Mb, foot, z, p, x0, 0.0, fcgm, "contrast", "mond")     # MS2's own door, unedited
        rs = rho_switch(Mb, foot, z, 0.0, fcgm, "mond", rF, H)
        xce = x0 * E2m(z) ** p
        Hz_ = H0m * math.sqrt(E2m(z))
        on_k = rF <= V_CAP / (Hz_ * math.sqrt(xce))
        on = bool(on_d and on_k)
        g_fw = float(nu2(0.1)) * 0.1 * a0
        sh = 2 * math.log10(((g_fw if on else 0.1 * a0)) / g_fw)
        XF_d = 1.5 * Om_zm(z) * (rs / rho_bar_m(z) - M2["FB"])           # MS2's threshold(), inverted for x_c,eff
        XF_k = (V_CAP / (Hz_ * rF)) ** 2
        return on, sh, XF_d, XF_k, rF / KPC2

    # (b) DE9's smooth flagship on DE8's operator, MOND-sector reading, with or without the kappa cap
    def flag_shift(xce, w, foot, form, Mb, z=2.5):
        a0 = A0[foot]; Hz_ = Hz(z); rhob = Om * rho_crit0 * (1 + z) ** 3
        rF = math.sqrt(G * Mb / (0.1 * a0))
        f = gate_mond(Mb, a0, w, xce, form, H=Hz_, rhob=rhob)
        extra = solve_region(Mb, a0, f, 100 * KPC_, 1.0)
        gF = G * (Mb + float(np.interp(math.log(rF), np.log(rf), extra))) / rF ** 2
        return 2 * math.log10(max(gF, 1e-300) / (float(nu_vec(np.array([0.1]))[0]) * 0.1 * a0))

    def cap_flag(w, foot, form, Mb, tol=-0.05):                        # DE9's cap_flagship, bisection unchanged
        lo, hi = 20.0, 5000.0
        if flag_shift(lo, w, foot, form, Mb) < tol: return lo
        for _ in range(50):
            mid = math.sqrt(lo * hi)
            if flag_shift(mid, w, foot, form, Mb) >= tol: lo = mid
            else: hi = mid
        return lo

    DE9F = json.load(open(os.path.join(DEDIR, "DE9_smooth_gate_window_results.json")))["numbers"]["flagship_cap"]["mond"]["0.25"]
    c5 = {f_: cap_flag(W_GATE, f_, "none", 1e11 * MS) for f_ in FEET}
    d5 = max(abs(c5[f_] / DE9F[f_] - 1) for f_ in FEET)
    check("C5 CONTROL: DE9's committed smooth flagship cap on the MOND-sector reading at w = 0.25 (1e11 Msun; DE9's gate, no "
          "cap) is reproduced", f"{c5['canonical']:.4f}/{c5['alt']:.4f} vs DE9 {DE9F['canonical']:.4f}/{DE9F['alt']:.4f} "
          f"(max rel diff {d5:.1e})", d5 < 1e-6)
    MBF = (10.0, 10.5, 11.0, 11.5)
    capk = {f"{l}/{f_}": cap_flag(W_GATE, f_, "kappa", 10 ** l * MS) for l in MBF for f_ in FEET}
    FT = {}
    for (p, x0) in CELLS:
        key = ck(p, x0); xce25 = x0 * E2G(2.5) ** p
        rows_a, rows_b = [], []
        for l in MBF:
            for f_ in FEET:
                for fc in (0.0, 0.1, 0.3, 1.0):
                    on, sh, XFd, XFk, rFk = door(10 ** l, f_, p, x0, fc)
                    rows_a.append(dict(lMb=l, foot=f_, fcgm=fc, on=on, shift=sh, XF_density=XFd, XF_kappa=XFk, rF_kpc=rFk))
                rows_b.append(dict(lMb=l, foot=f_, shift=flag_shift(xce25, W_GATE, f_, "kappa", 10 ** l * MS),
                                   cap_xce=capk[f"{l}/{f_}"]))
        pa = all(r_["on"] and abs(r_["shift"]) <= 0.10 for r_ in rows_a if r_["fcgm"] == 0.0)
        pb = all(r_["shift"] >= -0.05 for r_ in rows_b)
        pa11 = all(r_["on"] and abs(r_["shift"]) <= 0.10 for r_ in rows_a if r_["fcgm"] == 0.0 and r_["lMb"] <= 11.0)
        pb11 = all(r_["shift"] >= -0.05 for r_ in rows_b if r_["lMb"] <= 11.0)
        lost = sorted(set(r_["lMb"] for r_ in rows_b if r_["shift"] < -0.05) | set(r_["lMb"] for r_ in rows_a
                                                                                   if r_["fcgm"] == 0.0 and not r_["on"]))
        FT[key] = dict(xce_25=xce25, door=rows_a, smooth=rows_b, pass_door=pa, pass_smooth=pb, pass_=pa and pb,
                       pass_upto_1e11=pa11 and pb11, masses_lost=lost,
                       l_cap_25_kpc=V_CAP / (H0m * math.sqrt(E2m(2.5)) * math.sqrt(xce25)) / KPC2)
        P(f"  {key:9s} x_c,eff(2.5) {xce25:7.1f} (l_cap {FT[key]['l_cap_25_kpc']:5.0f} kpc): door (a) {'ok' if pa else 'FAIL'}, smooth (b) "
          f"{'ok' if pb else 'FAIL'} -> {'PASS' if pa and pb else 'FAIL'} (to 1e11 only: {'pass' if pa11 and pb11 else 'fail'}); masses lost "
          f"{lost or '-'}; smooth shifts canonical " + " ".join(f"{r_['shift']:+.2f}" for r_ in rows_b if r_["foot"] == "canonical"))
    OUT["numbers"]["flagship"] = FT
    OUT["numbers"]["flagship_caps_smooth_kappa"] = capk
    P("  the smooth flagship cap x_c,eff(2.5) with the kappa cap, by mass (canonical/alt): "
      + "; ".join(f"1e{l}: {capk[f'{l}/canonical']:.0f}/{capk[f'{l}/alt']:.0f}" for l in MBF)
      + "  -> x_c0 max at p = 1: " + ", ".join(f"1e{l}: {min(capk[f'{l}/canonical'], capk[f'{l}/alt']) / E2G(2.5):.1f}" for l in MBF)
      + "; at p = 1.5: " + ", ".join(f"1e{l}: {min(capk[f'{l}/canonical'], capk[f'{l}/alt']) / E2G(2.5) ** 1.5:.2f}" for l in MBF))
    check("F1 (reported) the flagship per cell (M_b 1e10-1e11.5, both footings, carrier cleared): MS2's door at r_F with the "
          "kappa cap AND DE9's smooth shift >= -0.05 dex", "; ".join(f"{k_}: {'PASS' if v_['pass_'] else 'FAIL (lost ' + str(v_['masses_lost']) + ')'}"
                                                                      for k_, v_ in FT.items()), True, load_bearing=False)
    OUT["numbers"]["forest"] = {k_: "pass by monotonicity from DE11 (converged cell worst 0.0041 vs 0.10; every scan cell's "
                                    "x_c,eff(z) >= the converged cell's at every z >= 0)" for k_ in KT}

    # ============================================================================================ summary
    banner("SUMMARY")
    for k_ in KT:
        r_ = KT[k_]
        P(f"  {k_:9s} KiDS (fs = {FS_RUN:g}, A <= 2) {'PASS' if r_['pass'] else 'fail'}  worst "
          f"{max(r_['kids'][f'w{W_GATE}/v{int(v)}/{f_}']['gate']['dchi2'] for v in VK for f_ in FEET):+6.1f}  |  flagship "
          f"{'PASS' if FT[k_]['pass_'] else 'fail'}  |  lens regions full-on <= {rfull[k_]:.2f} Mpc")
    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o)))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
