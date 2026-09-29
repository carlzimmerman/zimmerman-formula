#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG120 script B -- extended baryons: the frozen G1 metric on exponential spheres for the universal kernels (K*, the best RM fit, a
recalled RM set), T1e (K_{M_tot}: the mass-functional-kernel escape, a DIAGNOSTIC OUTSIDE THE DOOR) and T1f (far-shell leakage).
Written to CFG120_FROZEN_CRITERIA.md (commit e8b9fbcdf).

Profiles (declared before the run): (P1) exponential sphere with h = 2.0 kpc for every mass (CFG44 B1's Bcommon default, COMPACT expsphere);
(P2) h = 0.1 r_M(M); (P3) h = 0.5 r_M(M).  Masses: the 13-point grid; x in [0.1, 30] (r_M from the total baryon mass); both footings.
G1 metric R = C_model/C_target in [0.9, 1.1]; C_target = (a0/4pi) M_b(<r) exactly, C_model from the model's own g_tot.
T1f: exponential sphere (h = 2 kpc, M = 1e9, 1e10, 1e12) plus a shell of 10 M at R' = 4 r*, r* = r_M and 3 r_M; pass line |Delta C / C| <= 0.10.
Claims (CHECKS) = pre-declared expectations (frozen section 8): universal kernels fail on extended baryons; K_Mtot misses on extended baryons
and leaks; far-shell leakage of every positive kernel exceeds 10 percent.  If a claim is false it is reported false (kept).
MUTATE=d : kernel sign flipped (K -> -K): the claim 'the far shell ADDS dark density inside r*' must FAIL.  MUTATE=a,b,c: no bite here (declared).
Run: python3 cfg120_B_mass_functional_kernel.py    (MUTATE=d for the control)
"""
import os, sys, math, json
import numpy as np
import multiprocessing as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg120_common import *

R = Report("cfg120_B_mass_functional_kernel")
P, check = R.P, R.check
R.head(__doc__.split("Run: python3")[0])
if MUTATE in ("a", "b", "c"):
    P(f"\n  MUTATE={MUTATE}: no bite in script B (declared); the main claims are evaluated unchanged.")


class Neg:
    """K -> -K (MUTATE=d)"""
    def __init__(self, k):
        self.k = k
        self.name = "-" + k.name
    def K(self, s): return -self.k.K(s)
    def m(self, r): return -self.k.m(r)
    def Q(self, s): return -self.k.Q(s)


def load_fit(foot, a0f):
    fn = os.path.join(HERE, f"cfg120_rmfit_{foot}.json")
    if os.path.isfile(fn):
        return json.load(open(fn))["fit3"]
    return fit_rm(a0f, MASSES, None, None)


_KC = {}


def mk_kernels(foot, a0f):
    if foot in _KC:
        return _KC[foot]
    f3 = load_fit(foot, a0f)
    Ks = build_Kstar(a0f, MASSES, None)[0]
    ks = {"K* (best universal, ln-centred)": Ks,
          f"RM best fit (A={f3['A']:.3g}, lam={f3['lam']:.3g}, mu={f3['mu']:.2g})": RM(f3["A"], f3["lam"], f3["mu"]),
          "RM recalled (A=1, lam=3 kpc, mu=0.1/kpc)": RM(1.0, 3.0, 0.1)}
    if MUTATE == "d":
        ks = {k: Neg(v) for k, v in ks.items()}
    _KC[foot] = ks
    return ks


def case(args):
    """one (kernel-key, profile, mass) -> (Rmin, Rmax, max|R-1|) over x in [0.1, 30]"""
    foot, a0f, kname, prof, M, mode = args
    ks = mk_kernels(foot, a0f) if mode == "univ" else None
    rMv = rM(M, a0f)
    h = {"P1": 2.0, "P2": 0.1 * rMv, "P3": 0.5 * rMv}[prof]
    kern = ks[kname] if mode == "univ" else KM(rMv)               # K_Mtot: the sphere's own total mass
    rg, Rv, _, _, _ = C_ratio_sphere(kern, M, h, a0f)
    dom = rg >= 0.1 * rMv * (1 - 1e-9)
    Rd = Rv[dom]
    return (float(Rd.min()), float(Rd.max()), float(np.max(np.abs(Rd - 1))))


def shell_case(args):
    foot, a0f, kname, M, rstar_x, mode = args
    rMv = rM(M, a0f)
    h = 2.0
    rstar = rstar_x * rMv
    Rsh = 4.0 * rstar
    msh = 10.0 * M
    rgrid = np.unique(np.concatenate([np.geomspace(1e-3 * h, rstar, 400)]))
    out = {}
    for tag, with_shell in (("without", False), ("with", True)):
        if mode == "univ":
            kern = mk_kernels(foot, a0f)[kname]
        else:                                                    # K_Mtot: the total baryon mass (incl. the shell) sets rM
            kern = KM(rM(M * (11.0 if with_shell else 1.0), a0f))
        rhoD = rhoD_sphere(kern, exp_rho(M, h), rgrid, 60 * h)
        if with_shell:
            rhoS = msh / (2 * rgrid * Rsh) * (kern.Q(rgrid + Rsh) - kern.Q(np.abs(rgrid - Rsh)))
            rhoD_tot = rhoD + rhoS
        else:
            rhoD_tot = rhoD
        MD = cum_mass(rgrid, rhoD_tot)
        Mb = float(Mb_exp(M, h, rstar))
        C = 4 * math.pi * G * rstar * rhoD_tot[-1] * (Mb + MD[-1])
        out[tag] = dict(rhoD=float(rhoD_tot[-1]), R=float(C / (a0f * Mb)))
    return dict(drho=out["with"]["rhoD"] / out["without"]["rhoD"] - 1.0, dC=out["with"]["R"] / out["without"]["R"] - 1.0,
                R_without=out["without"]["R"], R_with=out["with"]["R"])


if __name__ == "__main__":
    ctx = mp.get_context("fork")
    pool = ctx.Pool(12)
    # ================================================================================================ G1 on exponential spheres, universal kernels
    R.banner("G1 (extended baryons, universal LTI kernels): R = C_model/C_target on exponential spheres, x in [0.1, 30]")
    univ_summary = {}
    for foot, a0f in FOOTINGS.items():
        knames = list(mk_kernels(foot, a0f).keys())
        jobs = [(foot, a0f, kn, pf, M, "univ") for kn in knames for pf in ("P1", "P2", "P3") for M in MASSES]
        outs = pool.map(case, jobs)
        k = 0
        P(f"\n  --- footing {foot} ---")
        for kn in knames:
            for pf in ("P1", "P2", "P3"):
                seg = outs[k:k + len(MASSES)]
                k += len(MASSES)
                allpass = all(o[0] >= BAND[0] and o[1] <= BAND[1] for o in seg)
                univ_summary[(foot, kn, pf)] = dict(passes=allpass, Rmin=min(o[0] for o in seg), Rmax=max(o[1] for o in seg),
                                                    per_mass=[(float(M), o[0], o[1]) for M, o in zip(MASSES, seg)])
                P(f"    {kn:52s} {pf}: R over all masses in [{min(o[0] for o in seg):.3g}, {max(o[1] for o in seg):.3g}]  (per-mass Rmax at 1e9/1e12: {seg[0][1]:.3g}/{seg[-1][1]:.3g});  meets the 10% line at every mass: {allpass}")
    R.num("univ_extended", {f"{a}|{b}|{c}": v for (a, b, c), v in univ_summary.items()})
    anypass = [key for key, v in univ_summary.items() if v["passes"]]
    check("B.1 (frozen expectation) no universal LTI kernel (K*, best RM fit, recalled RM) meets the 10 percent line on the exponential spheres at every mass",
          f"cases that pass: {anypass if anypass else 'none of 18 (kernel x profile x footing)'}", not anypass)
    R.gate("G1(extended baryons, universal kernels)", "FAIL" if not anypass else "PASS(some)", f"{sum(v['passes'] for v in univ_summary.values())} of {len(univ_summary)} kernel x profile x footing cases meet the line")

    # ================================================================================================ T1e  K_Mtot on exponential spheres
    R.banner("T1e  the mass-functional kernel K_{M_tot} (a DIAGNOSTIC outside the door: not linear in rho_b, postulates the target) on exponential spheres")
    kmt = {}
    for foot, a0f in FOOTINGS.items():
        jobs = [(foot, a0f, "K_Mtot", pf, M, "mtot") for pf in ("P1", "P2", "P3") for M in MASSES]
        outs = pool.map(case, jobs)
        k = 0
        P(f"\n  --- footing {foot} ---")
        for pf in ("P1", "P2", "P3"):
            seg = outs[k:k + len(MASSES)]
            k += len(MASSES)
            allpass = all(o[0] >= BAND[0] and o[1] <= BAND[1] for o in seg)
            nfail = sum(not (o[0] >= BAND[0] and o[1] <= BAND[1]) for o in seg)
            kmt[(foot, pf)] = dict(passes=allpass, Rmin=min(o[0] for o in seg), Rmax=max(o[1] for o in seg), n_fail_masses=nfail,
                                   per_mass=[(float(M), o[0], o[1]) for M, o in zip(MASSES, seg)])
            P(f"    {pf}: R over all masses in [{min(o[0] for o in seg):.4g}, {max(o[1] for o in seg):.4g}];  masses outside [0.9,1.1]: {nfail} of {len(MASSES)};  meets the line at every mass: {allpass}")
            P("        per mass (M, Rmin, Rmax): " + "; ".join(f"{M:.1e}: {o[0]:.3f}-{o[1]:.3f}" for M, o in zip(MASSES[::3], seg[::3])))
    R.num("Kmtot_extended", {f"{a}|{b}": v for (a, b), v in kmt.items()})
    any_kmt_pass = [k_ for k_, v in kmt.items() if v["passes"]]
    check("B.2 (frozen expectation) K_{M_tot} misses the target on extended baryons: for every profile family at least one mass leaves the 10 percent band",
          f"cases where K_Mtot passes at every mass: {any_kmt_pass if any_kmt_pass else 'none'}", not any_kmt_pass)
    R.gate("T1e (K_Mtot on extended baryons; diagnostic, outside the door)", "FAIL" if not any_kmt_pass else "PASS(some)", "; ".join(f"{a}/{b}: R in [{v['Rmin']:.3g}, {v['Rmax']:.3g}]" for (a, b), v in kmt.items() if a == "canonical"))

    # ================================================================================================ T1f  far-shell leakage
    R.banner("T1f  far-shell leakage: C should depend on M_b(<r) only; add a shell of 10 M at R' = 4 r* to an exponential sphere (h = 2 kpc)")
    leak = {}
    for foot, a0f in FOOTINGS.items():
        P(f"\n  --- footing {foot} ---")
        knames = list(mk_kernels(foot, a0f).keys()) + ["K_Mtot (total mass incl. shell)"]
        jobs = []
        for kn in knames:
            for M in (1e9, 1e10, 1e12):
                for xs_ in (1.0, 3.0):
                    jobs.append((foot, a0f, kn, M, xs_, "mtot" if kn.startswith("K_Mtot") else "univ"))
        outs = pool.map(shell_case, jobs)
        for j, o in zip(jobs, outs):
            leak[(j[0], j[2], j[3], j[4])] = o
        for kn in knames:
            rowsl = [(j[3], j[4], o) for j, o in zip(jobs, outs) if j[2] == kn]
            P(f"    {kn}")
            for M, xs_, o in rowsl:
                P(f"        M = {M:.0e}, r* = {xs_:g} r_M: Delta rho_D/rho_D = {o['drho']:+.3f};  Delta C / C = {o['dC']:+.3f}   (R without/with shell: {o['R_without']:.3f} / {o['R_with']:.3f})")
    R.num("leakage", {"|".join(map(str, k)): v for k, v in leak.items()})
    pos = [v["drho"] for k, v in leak.items() if not k[1].startswith("K_Mtot")]
    check("B.3 the far shell ADDS dark density inside r* for every positive universal LTI kernel (leakage is positive by construction)", f"min Delta rho_D/rho_D over universal kernels/masses/footings = {min(pos):+.3f}", min(pos) > 0)
    mag_univ = [abs(v["dC"]) for k, v in leak.items() if not k[1].startswith("K_Mtot")]
    mag_kmt = [abs(v["dC"]) for k, v in leak.items() if k[1].startswith("K_Mtot")]
    check("B.4 (frozen expectation) every kernel leaks more than 10 percent of C at r* = r_M and 3 r_M (universal LTI kernels and K_Mtot)",
          f"|Delta C/C| over universal kernels: min {min(mag_univ):.3f}, max {max(mag_univ):.3f}; K_Mtot: min {min(mag_kmt):.3f}, max {max(mag_kmt):.3f}; cases <= 0.10: universal {sum(m <= 0.10 for m in mag_univ)}, K_Mtot {sum(m <= 0.10 for m in mag_kmt)}",
          min(mag_univ) > 0.10 and min(mag_kmt) > 0.10)
    P("\n  (the target itself has Delta C = 0 exactly: C_target = (a0/4pi) M_b(<r), unchanged by baryons outside r; a leakage above the 10 percent line fails the far-shell property)")
    R.gate("T1f (far-shell leakage)", "FAIL" if (min(mag_univ) > 0.10 and min(mag_kmt) > 0.10) else "MIXED", f"|DeltaC/C| universal {min(mag_univ):.3f}..{max(mag_univ):.3f}; K_Mtot {min(mag_kmt):.3f}..{max(mag_kmt):.3f} (pass line 0.10)")
    nf = R.write()
    sys.exit(1 if nf else 0)
