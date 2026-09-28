#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG7 / FG016 -- THE PHANTOM'S EDGE DERIVED AS THE SPLASHBACK (FIRST-APOCENTRE) CAUSTIC.

CFG4's target law needs one declared number: where each bound system's phantom ends, x_e = r_edge / r_ta (r_ta = CFG4's
convention: where the galaxy's UNTRUNCATED law's mean enclosed density equals the GR top-hat turnaround contrast).  Its
window (CFG4_target VERDICT): KiDS needs x_e >= 0.30-0.31 with the unbound cold component's linear 2-halo term (A <= 2),
>= 0.47-0.50 without; the cold budget allows x_e <= 0.56 (lenient) down to 0.24-0.28 (strict).  FG016 derives the edge:
the phantom ends where the matter falling into the bound system first turns back -- the splashback caustic, the boundary of
the multi-stream (phase-mixed) region.

THE DERIVATION, step by step (each step computed here):
  1  COLLAPSE.  Spherical collisionless secondary infall in flat LCDM (CFG7_common's shell code; angular momentum at turnaround
     as XR28, jf ~ U(0.15, 0.35); power-law initial profiles, so the accretion rate s = dln M_ta/dln a is the controlled
     variable).  The splashback radius at an epoch = the 87th percentile (SPARTA's R_sp^87) of the first apocentres that happen
     within |dln a| <= 0.1 of it, each in units of the turnaround radius at its own time; 95th reported.  Its output:
     x_sp(s) (dynamical units) and Delta_sp(s) = the mean enclosed density inside it / rho_m.
     Two readings of the interior, never pooled:
       N  the cold matter gravitates normally (collisionless profile inside the caustic);
       G  the ground state: inside the current caustic the mass follows the law's shape M_b nu(y), normalised to the shells'
          mass there (T5 imposed at every step; M_b inferred); inside 3% of the caustic radius a uniform-density core replaces
          the law's point-mass limit (a numerical choice: that spike does not shape the outer caustic, but its orbits cost steps).
  2  T5 CLOSURE.  The phantom IS the cold matter inside the edge (CFG4 T5), so the law's mean enclosed density at the edge
     equals the collapse's Delta_sp: x_e = r(Delta_sp) / r(Delta_ta), both radii from the galaxy's own untruncated law (exact
     P2 / nu_mono shape, both footings).
  3  THE ACCRETION RATE IS THE LAW'S OWN.  With the edge at a fixed fraction of r_ta, the mass the law requires inside it grows
     as M_edge(a) = M_law(x_e r_ta(M_b(a), a); M_b(a)); T5 then fixes the accretion rate: s_law = dln M_edge / dln a, given
     the galaxy's baryonic growth beta_b = dln M_b / dln a in [0, 1] (declared bracket; an astrophysical input, not a constant).
     No LCDM accretion statistics enter.
  4  KiDS WITH THE DERIVED PROFILE.  The lens's mass profile is fixed with no free amplitude: the law inside the edge; beyond it
     the collapse's own infalling matter (the simulation's profile, scaled so that its mass inside the caustic equals the law's
     -- T5 -- and taken as the excess over the mean density).  This replaces CFG4's linear 2-halo template beyond the edge.
  5  THE BUDGET.  Omega_ph(x_e) from CFG4_target's committed table against Omega_c (and the turned-around share).

PRE-DECLARED (before this script's first full run; the exploratory smoke runs that fixed the edge definition are listed
under HISTORY)
  C1  CONTROL  EdS, eps = 1 (Bertschinger's point-mass seed, s = 1): the instantaneous outer caustic (the 99th-percentile radius
      of the crossed shells) at 0.364 r_ta (the radial self-similar caustic) within 3%, and the median first apocentre within 10% (its guard printed).
  C2  CONTROL  the GR top-hat 1 + delta_ta at z = 0 / 0.25 / 0.5 / 2 / 3 equals CFG4_switch's committed D1 table within 1%.
  C3  CONTROL  KiDS: FP1 E's machinery (exec'd read-only, FP20's exact projector) reproduces CFG4_switch's committed isolated-law
      chi^2 (139.800 / 133.948, P2) and its committed x-scan (the phantom cut at x r_ta, x = 0.3/0.4/0.5, with and without the
      2-halo, canonical and alt P2) to 1e-6.
  C4  CONTROL  CONVERGENCE: doubling the shells and halving the step moves x_sp87 and Delta_sp87 by <= 5% (s = 1, z = 0.25).
  C5  CONTROL  GUARD: in every production run no more than 0.5% of the crossed shells sit beyond the turnaround radius.
  H1  [the FG016 kill test, as IDEAS_100 wrote it] at the law's own accretion rate (beta_b in [0, 1]) the derived edge lies in
      CFG4's window [0.31, 0.48] at z = 0.25, reading G, P2, both footings.
  H2  [the decisive test] KiDS with the derived profile (the law inside the edge, the collapse's own infall outside, NO free
      2-halo amplitude) is within d chi^2 <= +9 of the untruncated law at the law's own accretion rate, reading N, both
      footings, P2 and nu_mono.
  H3  the lenient budget (z = 0.25, all of Omega_c, every galaxy) holds at the derived edge on both footings; the strict and
      satellites-merged budgets reported.
  R1  (reported) Adhikari, Dalal & Chamberlain's fit (reproduced in XR28 K2) against Delta_sp95 at the same s and Omega_m(z).
  R2  (reported) reading G against reading N: x_e and Delta_sp.
MUTATE=1: the edge is put at the turnaround radius (x_e = 1): the lenient budget must fail; and C1 is re-run with the enclosed
mass frozen at its initial Lagrangian value (no shell crossing), which must miss 0.364.  rc = 1.

HISTORY (disclosed).  Scratch prototypes (not committed) fixed the engine: a physical softening swamped early gravity
(replaced by a comoving one); the step criterion used the net force, which cancels at pericentre (replaced by the size of each
pull); near-radial orbits (jf <= 0.12) are not resolved by this integrator (crossed shells beyond r_ta), so jf follows XR28's
committed U(0.15, 0.35); the 99th-percentile radius of crossed shells jumped between snapshots of one run (it reads whichever
few shells sit at apocentre), so the edge is the percentile of recent first apocentres, pooled over three seeds; the first smoke
run of C1 showed that with angular momentum the first apocentres SPREAD around Bertschinger's radial 0.364 (median 0.339, 95th
percentile 0.396: a non-radial orbit is shorter, so it loses less energy while the potential deepens), so C1 is stated on the
instantaneous caustic (0.359 in that run) and the apocentre median, and C1 starts at a_i = 5e-4 for more self-similar range;
that start made the earliest-collapsed shells orbit ~1e5 times, each resolved, so a first production run let shells past
their 15th pericentre (settled deep in the core) stop setting the step.  THAT FIRST PRODUCTION RUN FAILED ITS GUARD: C1
(a_i = 5e-4) ejected 25% of its crossed shells beyond r_ta and the lowest-accretion LCDM run (s = 0.6) 9.5% -- unresolved
settled shells get kicked out.  The exclusion is therefore REMOVED everywhere (every turned shell sets the step), C1 starts
at a_i = 0.002 as in the smoke run that reproduced Bertschinger, and the whole lane was re-run (these outputs).  The first
run's physics numbers (the edge, KiDS, the budget) agreed with these to within the noise; its log is summarised in
CFG7_README.  Two dry runs
(DRY=1: 600 shells, one seed, two accretion rates; outputs *_DRY, not committed) exercised the whole pipeline before the
production run; their numbers are not results; a constrained-
mean initial profile was tried and dropped (it collapses almost as a top hat: caustic at 0.04 r_ta).  Smoke runs at s = 1
(z = 0.25) gave x_sp87 = 0.33 and Delta_sp87 = 132 (dynamical), Delta_sp95 = 111 against the radial fit's 109.
Run: python3 campaign_fresh_gravity/CFG7_edge_fg016.py   (MUTATE=1 for the control; ~40 min on 10 processes)
"""
import os, sys, math, json, time
import numpy as np
from scipy.optimize import brentq
from multiprocessing import get_context

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
C4 = C.C4

MUTATE = os.environ.get("MUTATE", "0") == "1"
DRY = os.environ.get("DRY", "0") == "1"                                  # pipeline test only: tiny runs, separate '_DRY' outputs
NPROC = int(os.environ.get("NPROC", "10"))
MPC_M = C.MPC_M
MSUN_KG = 1.98840987e30


def main():
    R = C.Report("CFG7_edge_fg016" + ("_DRY" if DRY else ""), MUTATE)
    P, check = R.P, R.check
    P(__doc__.split("Run: python3")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the edge at x_e = 1 and C1 with a frozen mass profile -- both must FAIL ***")
    SW = json.load(open(os.path.join(HERE, "CFG4_switch_results.json")))["numbers"]
    TG = json.load(open(os.path.join(HERE, "CFG4_target_results.json")))["numbers"]

    # ============================================================================================ C2 the top-hat
    R.banner("C2  CONTROL: the GR top-hat turnaround contrast against CFG4_switch's committed D1 table")
    d1 = SW["D1"]; dev2 = 0.0
    for z in ("0.0", "0.25", "0.5", "2.0", "3.0"):
        mine = C.LCDM.one_plus_delta_ta(1 / (1 + float(z))); ref = d1[z]["one_plus_delta_ta"]
        dev2 = max(dev2, abs(mine / ref - 1))
        P(f"    z = {z:4s}: 1 + delta_ta {mine:.4f} (CFG4 {ref:.4f}); delta_lin,ta {C.LCDM.delta_lin_ta(1 / (1 + float(z))):.4f} "
          f"(CFG4 {d1[z]['delta_lin_ta']:.4f})")
    check("C2 CONTROL: the top-hat 1 + delta_ta equals CFG4_switch's D1 within 1% (z = 0, 0.25, 0.5, 2, 3)", f"max deviation {dev2:.2%}",
          dev2 <= 0.01)

    # ============================================================================================ C3 the KiDS machinery
    R.banner("C3  CONTROL: KiDS-1000 isolated lenses -- FP1 E's machinery, FP20's exact projector, CFG4_switch's committed numbers")
    GK = {"np": np, "math": math, "os": os, "REPO": C4.REPO, "G_SI": 6.67430e-11, "_trap": C4._trap}
    GK = C4.exec_slices(os.path.join(C4.CHAIN, "FP1_static_sector.py"),
                        [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
    FIX = C4.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
    RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
    LM, NPB = GK["LM"], GK["npb"]
    W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
    GN = 6.67430e-11
    A0S = C4.A0
    RHOM_ZL = GK["rho_m_z"] * MSK / C4.MPC ** 3
    DTA25 = SW["D1"]["0.25"]["one_plus_delta_ta"]

    def kids_chi2(Mfun, foot, Amax=0.0):
        T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
        for im, lm in enumerate(LM):
            Mb = 10 ** lm * MSK
            dS = FIX(Mfun(Mb, A0S[foot]), Mb)
            T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
        return GK["kfit"]({foot: T}, foot, W0, Amax)[0]

    def Mlaw_K(kfun):
        return lambda Mb, a0: Mb * kfun(GN * Mb / RRK ** 2 / a0)

    def r_bound(M, Delta):
        D = M / (4.0 / 3.0 * math.pi * RRK ** 3 * RHOM_ZL)
        k = np.where(D < Delta)[0]
        if not len(k) or k[0] == 0:
            return RRK[-1] if not len(k) else RRK[0]
        i = k[0]
        return float(math.exp(np.interp(math.log(Delta), [math.log(D[i]), math.log(D[i - 1])], [math.log(RRK[i]), math.log(RRK[i - 1])])))

    def M_trunc_xta(kfun, x):
        def f_(Mb, a0):
            M = Mlaw_K(kfun)(Mb, a0)
            rt = x * r_bound(M, DTA25)
            Mt = np.interp(rt, RRK, M)
            return np.where(RRK <= rt, M, Mt)
        return f_

    KERN = C.KERNELS
    BASE = {(f, k): kids_chi2(Mlaw_K(kf), f) for f in C.FOOTS for k, kf in KERN.items()}
    dev3 = max(abs(BASE[(f, k)] - SW["K3"]["base"][f"{f}|{k}"]) for f in C.FOOTS for k in KERN)
    XS_REF = SW["H2c"]["x"]
    for f in C.FOOTS:
        for A in (0.0, 2.0):
            for x in (0.3, 0.4, 0.5):
                mine = kids_chi2(M_trunc_xta(C.nu_p2, x), f, A) - BASE[(f, "P2")]
                ref = SW["H2c"]["scan"][f"{f}|P2|A{A:.0f}"][XS_REF.index(x)]
                dev3 = max(dev3, abs(mine - ref))
                P(f"    {f:9s} P2 A <= {A:.0f}: cut at x = {x}: d chi^2 {mine:+.4f} (CFG4 {ref:+.4f})")
    P("    isolated-law chi^2: " + ", ".join(f"{k[0]}|{k[1]} {v:.4f}" for k, v in BASE.items()))
    check("C3 CONTROL: KiDS machinery reproduces CFG4_switch's isolated-law chi^2 and its x-scan (x = 0.3/0.4/0.5, A = 0/2, both footings) "
          "to 1e-6", f"max deviation {dev3:.2e}", dev3 <= 1e-6)

    # ============================================================================================ the runs
    R.banner("THE COLLAPSE RUNS (process pool)")
    EPS = [0.195, 0.269, 0.358, 0.43, 0.5375, 0.717]                    # s(z = 0.25) = 0.43/eps = 2.2, 1.6, 1.2, 1.0, 0.8, 0.6
    NN, SEEDS = 2000, (7, 8, 9)
    if DRY:
        EPS, NN, SEEDS = [0.269, 0.43], 600, (7,)
    base = dict(M_ta_obs=4e12, a_norm=0.8, a_obs_list=[0.8, 1.0], N=NN, seeds=SEEDS)
    specs = [dict(tag="C1", cosmo="EdS", eps=1.0, M_ta_obs=1e12, a_norm=1.0, a_obs_list=[1.0], N=NN, seeds=SEEDS, a_i=0.002,
                  span=(1e-3, 12.0), n_resolve=10 ** 9, mutate_frozen=MUTATE),
             dict(tag="CONV", eps=0.43, M_ta_obs=4e12, a_norm=0.8, a_obs_list=[0.8], N=2 * NN, eta=0.015, seeds=SEEDS[:2],
                  n_resolve=10 ** 9)]
    for e in EPS:
        specs.append(dict(base, tag=f"N|{e}", eps=e, mode="N"))
        for f in C.FOOTS:
            specs.append(dict(base, tag=f"G|{f}|{e}", eps=e, mode="G", foot=f, kern="P2"))
    t0 = time.time()
    RES = {}
    with get_context("fork").Pool(NPROC) as pool:
        for r in pool.imap_unordered(C.job_pooled, sorted(specs, key=lambda s: -s.get("N", 2000) * (3 if s.get("mode") == "G" else 1))):
            RES[r["spec"]["tag"]] = r
            m8 = r["res"][sorted(r["res"])[0]]
            P(f"    {r['spec']['tag']:22s} done ({r['seconds']:.0f} s): a = {m8['a']:.2f} s = {m8['s_ta']:.2f} x_sp87 {m8['x_sp87']:.3f} "
              f"Delta_sp87 {m8['Delta_sp87']:.1f} x_sp95 {m8['x_sp95']:.3f} n_apo {m8['n_apo']} guard {m8['guard_frac_beyond_rta']:.4f}")
    P(f"    all runs done ({time.time() - t0:.0f} s)")

    # ============================================================================================ C1 C4 C5 R1
    R.banner("C1 / C4 / C5 / R1  the collapse engine's controls")
    c1 = RES["C1"]["res"]["1.0000"]
    check("C1 CONTROL: EdS eps = 1 -- the instantaneous outer caustic at 0.364 r_ta (Bertschinger's radial caustic) within 3% and the "
          "median first apocentre within 10%" + ("  [MUTATE: mass frozen]" if MUTATE else ""),
          f"x_c99 = {c1['x_c99']:.4f} ({c1['x_c99'] / 0.364 - 1:+.1%}); x_sp50 = {c1['x_sp50']:.4f} ({c1['x_sp50'] / 0.364 - 1:+.1%}); "
          f"x_sp87 = {c1['x_sp87']:.4f}, x_sp95 = {c1['x_sp95']:.4f}; Delta_sp87 = {c1['Delta_sp87']:.1f}; "
          f"guard {c1['guard_frac_beyond_rta']:.4f}",
          abs(c1["x_c99"] / 0.364 - 1) <= 0.03 and abs(c1["x_sp50"] / 0.364 - 1) <= 0.10)
    cv = RES["CONV"]["res"]["0.8000"]; ref = RES["N|0.43"]["res"]["0.8000"]
    dx = abs(cv["x_sp87"] / ref["x_sp87"] - 1); dd = abs(cv["Delta_sp87"] / ref["Delta_sp87"] - 1)
    check("C4 CONTROL: CONVERGENCE -- 2x the shells and half the step move x_sp87 and Delta_sp87 by <= 5% (s = 1, z = 0.25)",
          f"x_sp87 {ref['x_sp87']:.4f} -> {cv['x_sp87']:.4f} ({dx:.1%}); Delta_sp87 {ref['Delta_sp87']:.1f} -> {cv['Delta_sp87']:.1f} ({dd:.1%})",
          dx <= 0.05 and dd <= 0.05)
    guards = {t: max(v["guard_frac_beyond_rta"] for v in r["res"].values()) for t, r in RES.items() if t not in ("C1",)}
    check("C5 CONTROL: GUARD -- no more than 0.5% of the crossed shells beyond the turnaround radius in any production run",
          f"worst {max(guards.values()):.4f} ({max(guards, key=guards.get)})", max(guards.values()) <= 0.005)

    def adc14(s, Om):
        return 38.0 * Om ** (-0.57 - 0.02 * s) * math.exp(0.2 * Om + 0.52 * s ** 0.75)

    r1 = []
    for e in EPS:
        for ao in ("0.8000", "1.0000"):
            m_ = RES[f"N|{e}"]["res"][ao]; a_ = float(ao)
            Om = float(C.LCDM.Om_a(a_))
            r1.append((e, ao, m_["s_ta"], m_["Delta_sp95"], adc14(max(m_["s_ta"], 0.0), Om)))
    for e, ao, s_, dm, da in r1:
        P(f"    eps {e:6.4f} a {ao}: s = {s_:.2f}: Delta_sp95 {dm:6.1f} vs ADC14 (radial toy model) {da:6.1f} ({dm / da - 1:+.0%})")
    check("R1 (reported) Adhikari, Dalal & Chamberlain's radial toy-model fit against Delta_sp95 within 20%",
          f"worst {max(abs(dm / da - 1) for _, _, _, dm, da in r1):.0%}", all(abs(dm / da - 1) <= 0.2 for _, _, _, dm, da in r1), load_bearing=False)

    # ============================================================================================ the table Delta_sp(s)
    R.banner("THE COLLAPSE TABLE: splashback in dynamical units and its mean enclosed density, by accretion rate, epoch and reading")
    TAB = {}
    for rd in ["N"] + [f"G|{f}" for f in C.FOOTS]:
        for ao in ("0.8000", "1.0000"):
            rows = []
            for e in EPS:
                m_ = RES[f"{rd}|{e}"]["res"][ao]
                rows.append(dict(eps=e, s=m_["s_ta"], x87=m_["x_sp87"], x95=m_["x_sp95"], D87=m_["Delta_sp87"], D95=m_["Delta_sp95"],
                                 x87e=m_["x_sp87_err"], Mb_G=m_.get("Mb_G", float("nan")), rta=m_["r_ta_dta"]))
            TAB[(rd, ao)] = sorted(rows, key=lambda q: q["s"])
            P(f"    {rd:12s} z = {1 / float(ao) - 1:4.2f}: " + "; ".join(f"s {q['s']:.2f}: x87 {q['x87']:.3f} D87 {q['D87']:.0f}" for q in TAB[(rd, ao)]))
    R.num("TABLE", {f"{k[0]}|{k[1]}": v for k, v in TAB.items()})

    def D_of_s(rd, ao, s, key="D87"):
        rows = TAB[(rd, ao)]
        ss = np.array([q["s"] for q in rows]); dd_ = np.array([q[key] for q in rows])
        return float(math.exp(np.interp(s, ss, np.log(dd_))))

    # ============================================================================================ T5 closure + the law's accretion rate
    R.banner("THE LAW'S OWN ACCRETION RATE (T5) AND THE DERIVED EDGE x_e (CFG4's units)")
    LENS_LMB = SW["H2c"]["lens_logMb_P2_canonical"]
    LMB_MED = float(np.median(LENS_LMB))
    P(f"    the KiDS lenses' profiled log M_b (P2, canonical): {LENS_LMB}; median {LMB_MED:.3f}")

    def x_e_of(Delta, lmb, foot, kern, a):
        return C.x_edge_from_Delta(Delta, 10 ** lmb, C.A0[foot], KERN[kern], a)

    def s_law(lmb, foot, kern, a, x_e, beta_b, dlna=0.02):
        def Medge(ln_a):
            aa = math.exp(ln_a); Mb = 10 ** lmb * (aa / a) ** beta_b
            return float(C.M_law(Mb, x_e * C.r_ta_law(Mb, C.A0[foot], KERN[kern], aa), C.A0[foot], KERN[kern]))
        la = math.log(a)
        return (math.log(Medge(la + dlna)) - math.log(Medge(la - dlna))) / (2 * dlna)

    SELF = {}
    for rd in ["N"] + [f"G|{f}" for f in C.FOOTS]:
        for foot in C.FOOTS:
            if rd.startswith("G|") and rd != f"G|{foot}":
                continue
            for kern in ("P2", "nu_mono"):
                for ao in ("0.8000", "1.0000"):
                    a_ = float(ao)
                    for bb in (0.0, 0.5, 1.0):
                        s_ = 1.0; xe = 0.3
                        for _ in range(30):
                            D_ = D_of_s(rd, ao, s_)
                            xe = x_e_of(D_, LMB_MED, foot, kern, a_)
                            s_new = s_law(LMB_MED, foot, kern, a_, xe, bb)
                            if abs(s_new - s_) < 1e-4:
                                s_ = s_new; break
                            s_ = 0.5 * (s_ + s_new)
                        D_ = D_of_s(rd, ao, s_); D95 = D_of_s(rd, ao, s_, "D95")
                        xe = x_e_of(D_, LMB_MED, foot, kern, a_); xe95 = x_e_of(D95, LMB_MED, foot, kern, a_)
                        spread = [x_e_of(D_, l_, foot, kern, a_) for l_ in (9.0, 10.0, 11.0, 11.5)]
                        SELF[(rd, foot, kern, ao, bb)] = dict(s=s_, Delta87=D_, Delta95=D95, x_e=xe, x_e95=xe95, x_e_mass_spread=spread)
    for k, v in SELF.items():
        if k[2] == "P2":
            P(f"    {k[0]:12s} {k[1]:9s} {k[2]:7s} z = {1 / float(k[3]) - 1:4.2f} beta_b = {k[4]:.1f}: s_law = {v['s']:.2f}, Delta_sp87 = "
              f"{v['Delta87']:.0f} -> x_e = {v['x_e']:.3f} (95th: {v['x_e95']:.3f}); over log M_b 9-11.5: "
              + "/".join(f"{x:.3f}" for x in v["x_e_mass_spread"]))
    R.num("SELF", {"|".join(str(x) for x in k): v for k, v in SELF.items()})

    # ============================================================================================ H1 the kill test as written
    R.banner("H1  THE FG016 KILL TEST AS WRITTEN: x_e in [0.31, 0.48] at z = 0.25 (reading G, P2, beta_b in [0, 1])")
    xs_h1 = {(f, bb): SELF[(f"G|{f}", f, "P2", "0.8000", bb)]["x_e"] for f in C.FOOTS for bb in (0.0, 0.5, 1.0)}
    h1 = all(0.31 <= v <= 0.48 for v in xs_h1.values())
    check("H1 [the FG016 kill test] at the law's own accretion rate the derived edge lies in CFG4's window [0.31, 0.48] at z = 0.25 "
          "(reading G, P2, both footings, beta_b = 0, 0.5, 1)", "; ".join(f"{k[0][:3]} b{k[1]:.1f}: {v:.3f}" for k, v in xs_h1.items()), h1)

    # ============================================================================================ H2 KiDS with the derived profile
    R.banner("H2  KiDS WITH THE DERIVED PROFILE: the law inside the edge, the collapse's own infall outside, no free 2-halo amplitude")

    def mean_profile(rd, e, ao):
        m_ = RES[f"{rd}|{e}"]["res"][ao]
        rg = np.geomspace(1e-3, 30.0, 900)
        Ms = [np.interp(rg, np.array(p["r"]), np.array(p["M"]), left=np.nan, right=np.nan) for p in m_["profiles"]]
        M = np.nanmean(np.array(Ms), axis=0)
        ok = np.isfinite(M)
        return rg[ok], M[ok], m_

    RHOM_SIM = float(C.LCDM.rhom(0.8))

    def derived_Mfun(rd, e, kern):
        rg, Mg, m_ = mean_profile(rd, e, "0.8000")
        r_sp = m_["x_sp87"] * m_["r_ta_dta"]
        M_sp = float(np.interp(r_sp, rg, Mg))
        kf = KERN[kern]
        r_mpc = RRK / MPC_M

        def f_(Mb_kg, a0_si):
            Mb = Mb_kg / MSUN_KG
            a0u = a0_si / C.SI_ACC
            g = lambda ll: math.log(math.exp(ll) * M_sp) - math.log(float(C.M_law(Mb, math.exp(ll / 3.0) * r_sp, a0u, kf)))
            ll = brentq(g, -40.0, 40.0)
            lam = math.exp(ll); r_e = lam ** (1 / 3.0) * r_sp
            M_in = C.M_law(Mb, r_mpc, a0u, kf)
            M_e = float(C.M_law(Mb, r_e, a0u, kf))
            r_lim = lam ** (1 / 3.0) * rg[-1]                                      # the simulation's reach (scaled)
            rr_ = np.minimum(r_mpc, r_lim)
            M_sim = lam * np.interp(rr_ / lam ** (1 / 3.0), rg, Mg)
            M_out = M_e + (M_sim - lam * M_sp) - 4 * math.pi / 3 * (rr_ ** 3 - r_e ** 3) * RHOM_SIM   # held constant past the reach
            return np.where(r_mpc <= r_e, M_in, np.maximum(M_out, 0.0)) * MSUN_KG
        return f_

    KD = {}
    for e in EPS:
        for foot in C.FOOTS:
            for kern in ("P2", "nu_mono"):
                for A in (0.0, 2.0):
                    KD[("N", e, foot, kern, A)] = kids_chi2(derived_Mfun("N", e, kern), foot, A) - BASE[(foot, kern)]
            KD[(f"G|{foot}", e, foot, "P2", 0.0)] = kids_chi2(derived_Mfun(f"G|{foot}", e, "P2"), foot, 0.0) - BASE[(foot, "P2")]
    for foot in C.FOOTS:
        for kern in ("P2", "nu_mono"):
            P(f"    reading N {foot:9s} {kern:7s}: d chi^2 (A = 0 / A <= 2) at s = " +
              "; ".join(f"{RES[f'N|{e}']['res']['0.8000']['s_ta']:.2f}: {KD[('N', e, foot, kern, 0.0)]:+.1f} / {KD[('N', e, foot, kern, 2.0)]:+.1f}"
                        for e in EPS))
        P(f"    reading G {foot:9s} P2     : d chi^2 (A = 0) at s = " +
          "; ".join(f"{RES[f'G|{foot}|{e}']['res']['0.8000']['s_ta']:.2f}: {KD[(f'G|{foot}', e, foot, 'P2', 0.0)]:+.1f}" for e in EPS))

    def kd_at_s(rd, foot, kern, A, s):
        ss = np.array([RES[f"{rd}|{e}"]["res"]["0.8000"]["s_ta"] for e in EPS]); vv = np.array([KD[(rd, e, foot, kern, A)] for e in EPS])
        o = np.argsort(ss)
        return float(np.interp(s, ss[o], vv[o]))

    H2V = {}
    for foot in C.FOOTS:
        for kern in ("P2", "nu_mono"):
            for bb in (0.0, 0.5, 1.0):
                s_ = SELF[("N", foot, kern, "0.8000", bb)]["s"]
                H2V[(foot, kern, bb)] = dict(s=s_, d0=kd_at_s("N", foot, kern, 0.0, s_), d2=kd_at_s("N", foot, kern, 2.0, s_))
                P(f"    at the law's own accretion rate ({foot}, {kern}, beta_b = {bb}): s = {s_:.2f} -> d chi^2 {H2V[(foot, kern, bb)]['d0']:+.1f} "
                  f"(no 2-halo) / {H2V[(foot, kern, bb)]['d2']:+.1f} (A <= 2)")
    h2 = all(v["d0"] <= 9.0 for v in H2V.values())
    check("H2 [the decisive test] KiDS with the derived profile (law inside the edge, the collapse's infall outside, no free 2-halo) is "
          "within d chi^2 <= +9 of the untruncated law at the law's own accretion rate (reading N, both footings, P2 and nu_mono, "
          "beta_b = 0, 0.5, 1)", "; ".join(f"{k[0][:3]}/{k[1]}/b{k[2]:.1f}: s {v['s']:.2f} d {v['d0']:+.1f}" for k, v in H2V.items()), h2)
    R.num("KIDS", {"|".join(str(x) for x in k): v for k, v in KD.items()}); R.num("H2", {"|".join(str(x) for x in k): v for k, v in H2V.items()})

    # ============================================================================================ H3 the budget
    R.banner("H3  THE COLD BUDGET at the derived edge (CFG4_target's committed Omega_ph(x) table)")
    BT = TG["H3"]["budget"]; OMC = TG["H3"]["Omega_c"]; FTA = TG["H3"]["f_ta_web_k1"]
    XG = [0.2, 0.3, 0.31, 0.4, 0.48, 0.6, 0.8, 1.0]

    def om_ph(foot, kern, z, mcut, x):
        row = BT[f"{foot}|{kern}|z{z}|m{mcut}"]
        return float(math.exp(np.interp(math.log(x), np.log(XG), np.log([row[str(v)][0] for v in XG]))))

    CASES = [("lenient: z = 0.25, all of Omega_c", "0.8000", 0.25, 7.0, OMC),
             ("z = 0, all of Omega_c", "1.0000", 0.0, 7.0, OMC),
             ("z = 0.25, turned-around share", "0.8000", 0.25, 7.0, OMC * FTA),
             ("strict: z = 0, turned-around share", "1.0000", 0.0, 7.0, OMC * FTA),
             ("satellites merged (M_* >= 1e9), z = 0, turned-around share", "1.0000", 0.0, 9.0, OMC * FTA)]
    H3V = {}
    for foot in C.FOOTS:
        for kern in ("P2", "nu_mono"):
            for lab, ao, z, mc, lim in CASES:
                for bb in (0.0, 0.5, 1.0):
                    xe = 1.0 if MUTATE else SELF[("N", foot, kern, ao, bb)]["x_e"]
                    xg = 1.0 if MUTATE else SELF[(f"G|{foot}", foot, "P2", ao, bb)]["x_e"]
                    H3V[(foot, kern, lab, bb)] = dict(x_e=xe, x_e_G=xg, Om_ph=om_ph(foot, kern, z, mc, xe), limit=lim,
                                                      ok=om_ph(foot, kern, z, mc, xe) <= lim)
            P(f"    {foot:9s} {kern:7s}: " + "; ".join(
                f"[{lab.split(':')[0]}] x_e {H3V[(foot, kern, lab, 0.5)]['x_e']:.3f}: Omega_ph {H3V[(foot, kern, lab, 0.5)]['Om_ph']:.3f} vs "
                f"{H3V[(foot, kern, lab, 0.5)]['limit']:.3f} {'ok' if H3V[(foot, kern, lab, 0.5)]['ok'] else 'OVER'}" for lab, *_ in CASES))
    h3 = all(v["ok"] for k, v in H3V.items() if k[2].startswith("lenient"))
    check("H3 THE LENIENT BUDGET holds at the derived edge (z = 0.25, all of Omega_c, every galaxy; both footings, both kernels, "
          "beta_b = 0, 0.5, 1)" + ("  [MUTATE: x_e = 1]" if MUTATE else ""),
          "; ".join(f"{k[0][:3]}/{k[1]}/b{k[3]:.1f}: x_e {v['x_e']:.3f} Omega_ph {v['Om_ph']:.3f} <= {v['limit']:.3f}"
                    for k, v in H3V.items() if k[2].startswith("lenient") and k[3] == 0.5), h3)
    for lab, *_ in CASES[1:]:
        okc = all(v["ok"] for k, v in H3V.items() if k[2] == lab)
        P(f"    (reported) {lab}: {'holds' if okc else 'fails'} -- " + ", ".join(
            f"{k[0][:3]}/{k[1]}/b{k[3]:.1f} {v['Om_ph']:.3f}/{v['limit']:.3f}" for k, v in H3V.items() if k[2] == lab and k[3] == 0.5))
    R.num("H3", {"|".join(str(x) for x in k): v for k, v in H3V.items()})

    # ============================================================================================ R2 readings
    R.banner("R2  (reported) READING G AGAINST READING N")
    for foot in C.FOOTS:
        for bb in (0.0, 0.5, 1.0):
            a_ = SELF[("N", foot, "P2", "0.8000", bb)]; b_ = SELF[(f"G|{foot}", foot, "P2", "0.8000", bb)]
            P(f"    {foot:9s} beta_b {bb}: N: s {a_['s']:.2f} Delta {a_['Delta87']:.0f} x_e {a_['x_e']:.3f} | G: s {b_['s']:.2f} Delta "
              f"{b_['Delta87']:.0f} x_e {b_['x_e']:.3f}")

    # ============================================================================================ verdict
    R.banner("VERDICT")
    xN = [SELF[("N", f, "P2", "0.8000", b)]["x_e"] for f in C.FOOTS for b in (0.0, 0.5, 1.0)]
    xG = [SELF[(f"G|{f}", f, "P2", "0.8000", b)]["x_e"] for f in C.FOOTS for b in (0.0, 0.5, 1.0)]
    P(f"    The edge derived from collapse at the law's own accretion rate: x_e = {min(xG):.3f}-{max(xG):.3f} (reading G), "
      f"{min(xN):.3f}-{max(xN):.3f} (reading N) of CFG4's r_ta at z = 0.25 -- against CFG4's window [0.31, 0.48].")
    P(f"    KiDS with the derived profile (no free 2-halo): d chi^2 {min(v['d0'] for v in H2V.values()):+.1f} to "
      f"{max(v['d0'] for v in H2V.values()):+.1f}; with A <= 2 {min(v['d2'] for v in H2V.values()):+.1f} to {max(v['d2'] for v in H2V.values()):+.1f}.")
    R.num("RUN_SUMMARY", {t: dict(seconds=r["seconds"], res={ao: {k: v for k, v in m_.items() if k not in ("profiles", "per_seed")}
                                                              for ao, m_ in r["res"].items()}) for t, r in RES.items()})
    return R.write()


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
