#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L375 -- THE TRIGGERED CARRIER AROUND KiDS LENSES, RESOLVED: a self-consistent spherical shell model of each KiDS host halo
(secondary infall on a mass-accretion history, the carrier's own gravity, the bin's baryons), the carrier decaying and
kicked by L365's trigger, and the RETAINED CARRIER'S OWN PROJECTED PROFILE scored on KiDS-1000 with L360's machinery.

WHY.  L368's full window (v_k = 650 km/s, C-H/K's p = 2 kernel switch) passed KiDS with the carrier's surviving fraction
around galaxy-mass peaks S = 0.029, measured on a 0.39 Mpc/h mesh -- SUB-CELL for these halos (r_200 = 0.14-0.34 Mpc).
KiDS is not monotone in S (L368: the alternative footing fails at S = 0.2).  The mesh smooths the potential (fewer kicked
particles retained) and the trigger density (more carrier left undecayed): opposite biases.  This lane resolves both.

WHAT THE CARRIER FEELS.  The carrier is kernel-invisible (L353): by the reciprocity theorem it feels Newtonian gravity only
(baryons + carrier), not the baryons' phantom.  So a Newtonian shell model is the construction's own dynamics.
MODEL (per KiDS bin; L360's Moster+13 hosts M_200 = 4.2e11, 9.0e11, 1.9e12, 5.6e12 Msun at z_l = 0.25):
  * mass-accretion history M(z) = M_200 exp[-alpha (z - 0.25)] (Wechsler+02 form; alpha = 0.75 fiducial, 0.5 and 1.2
    bracket), started at z = 3 as an NFW (c = 4) and grown by secondary infall: new carrier shells enter at 2 r_200(z)
    with v_r = -v_200(z), v_t = 0.4 v_200(z);
  * spherical shells (exact Newton's theorem, the carrier's own gravity self-consistent), static baryons of the bin's
    fitted mass (Hernquist, a = 3 kpc (M_b/1e11)^0.3, + the rest of f_b M_200 as an NFW-shaped CGM), grown with M(z);
  * L365's trigger, unchanged: a cold carrier element decays at Gamma = 10 H(z) where the LOCAL total matter density has
    x~ = (3/2)(rho - rho_bar)/rho_crit(z) > 5; the daughter gets an isotropic kick v_k (once).
  * at z_l = 0.25 the carrier's 3D profile is projected with L352's own projector (loaded unedited via L360) and added
    to the switched phantom exactly as L360/L368 add the carrier's template; Delta chi^2 <= +4 against the unswitched model,
    both footings (L352's acceptance).  S = M_carrier(<0.5 Mpc/h) relative to the no-decay run (L367's definition).
PRE-DECLARED (before the run): H: at v_k = 650 km/s with the p = 2 switch, the fiducial accretion history passes KiDS on both
footings -- the sub-cell caveat does not reverse L368's KiDS verdict.
CHECKS
  C1 CONTROL: with the decay off (Gamma = 0) the same shell halo is a cold CDM-like carrier halo and KiDS rejects it
     (Delta chi^2 > +100 on both footings), as L360's M1 does with the NFW template: the pipeline can see a retained halo.
  C2 CONTROL: a static NFW + baryons in Jeans equilibrium (no decay, no infall) keeps M(<r_s) to within 10% over 5 Gyr
     (integrator and initial conditions).
  K1 = H.  K2 (informational): S per bin, the undecayed vs kicked split, alpha and baryon variants, v_k = 600 and 700, the
     p = 1 switch.
MUTATE=1: v_k = 0 in every decaying run (the decayed carrier stays): K1 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L375_triggered_carrier_galaxy_retention.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
from multiprocessing import Pool
from scipy.integrate import quad, cumulative_trapezoid

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L375_triggered_carrier_galaxy_retention"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L375", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_PASS = True                                                  # H, set before the run


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


# ---------------------------------------------------------------------------------- units: kpc, km/s, time kpc/(km/s)
G = 4.30091e-6                                                      # kpc (km/s)^2 / Msun
TU = 0.977792                                                       # Gyr per kpc/(km/s)
h = 0.6736; Om = (0.02237 + 0.1200) / h ** 2; OL = 1 - Om            # L352/L360's background
FB = 0.02237 / (0.02237 + 0.1200)
H0 = 100 * h / 1000.0                                               # km/s/kpc
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * G)                             # Msun/kpc^3
ZL = 0.25; ZSTART = 3.0; RAP = 500.0 / h                            # KiDS lens redshift; 0.5 Mpc/h aperture (L367)
M200_BINS = [4.17e11, 8.97e11, 1.91e12, 5.55e12]                    # L360's Moster+13 hosts
E = lambda z: math.sqrt(Om * (1 + z) ** 3 + OL)
c200 = lambda M: 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h)))   # Dutton-Maccio 2014 (L360)
mfn = lambda x: np.log(1 + x) - x / (1 + x)
_ZG = np.linspace(0.0, 12.0, 6001)
_TG = np.array([quad(lambda a: 1 / (a * H0 * math.sqrt(Om / a ** 3 + OL)), 0, 1 / (1 + z_))[0] for z_ in _ZG])
t_of_z = lambda z: float(np.interp(z, _ZG, _TG))
z_of_t = lambda t: float(np.interp(-t, -_TG, _ZG))


def r200_of(M, z):
    return (3 * M / (4 * math.pi * 200 * RHOC0 * E(z) ** 2)) ** (1 / 3)


def halo(cfg):
    """one shell-model halo; returns the carrier's radial mass histogram at z_l and diagnostics."""
    tag, b, Mb, vk, gam, alpha, grow_b, N, seed = cfg
    rng = np.random.default_rng(seed)
    M0 = M200_BINS[b]; c0 = c200(M0); r0 = r200_of(M0, ZL); rs0 = r0 / c0
    ab = 3.0 * (Mb / 1e11) ** 0.3; Mcgm = max(FB * M0 - Mb, 0.0)
    Mz = (lambda z: M0 * math.exp(-alpha * (z - ZL))) if alpha > 0 else (lambda z: M0)

    def Mst(r, z):                                                   # static baryons (+ CGM), grown with the halo
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * r ** 2 / (r + ab) ** 2 + Mcgm * np.minimum(mfn(r / rs0) / mfn(c0), 1.0))

    def rho_st(r, z):
        f = Mz(z) / M0 if grow_b else 1.0
        return f * (Mb * ab / (2 * math.pi * r * (r + ab) ** 3) +
                    np.where(r < r0, Mcgm / (4 * math.pi * rs0 ** 3 * mfn(c0)) / ((r / rs0) * (1 + r / rs0) ** 2), 0.0))

    zs = ZSTART if alpha > 0 else 1.1
    m = (1 - FB) * M0 / N                                            # equal-mass carrier shells
    Mi = Mz(zs); ci = 4.0 if alpha > 0 else c0; ri = r200_of(Mi, zs) if alpha > 0 else r0; rsi = ri / ci
    Ni = int(round((1 - FB) * Mi / m))
    u = rng.random(Ni) * mfn(ci); xg = np.geomspace(1e-5, ci, 20000); r = np.interp(u, mfn(xg), xg) * rsi
    rg = np.geomspace(1e-3 * rsi, ri, 4000)
    rho_c = (1 - FB) * Mi / (4 * math.pi * rsi ** 3 * mfn(ci)) / ((rg / rsi) * (1 + rg / rsi) ** 2)
    Mc_r = (1 - FB) * Mi * mfn(rg / rsi) / mfn(ci)
    integ = rho_c * G * (Mst(rg, zs) + Mc_r) / rg ** 2               # Jeans (isotropic), truncated at r_200
    tail = -np.concatenate([[0.0], cumulative_trapezoid(integ[::-1], rg[::-1])])[::-1]
    sg = np.sqrt(np.maximum(np.interp(r, rg, tail / rho_c), 0.0))
    v = rng.normal(size=(Ni, 3)) * sg[:, None]
    vr = v[:, 0].copy(); L = r * np.hypot(v[:, 1], v[:, 2]); cold = np.ones(Ni, bool)
    Mc_rs0 = float(np.mean(r < rsi)) * Ni * m

    t0, t1 = t_of_z(zs), t_of_z(ZL)
    dt = 1.0e-3 / TU; nstep = int(math.ceil((t1 - t0) / dt)); dt = (t1 - t0) / nstep
    rmin = 0.05; edges = np.geomspace(0.05, 2e4, 240); rmid = np.sqrt(edges[1:] * edges[:-1])
    vol = 4 / 3 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    carry = 0.0; t = t0; z = zs; ndec = 0

    def acc(r, z):
        order = np.argsort(r); rank = np.empty(len(r), int); rank[order] = np.arange(len(r))
        return -G * (Mst(r, z) + m * (rank + 0.5)) / r ** 2 + L ** 2 / r ** 3

    a_ = acc(r, z)
    for i in range(nstep):
        vr += 0.5 * dt * a_
        r = r + dt * vr
        neg = r < rmin; r[neg] = 2 * rmin - r[neg]; vr[neg] = np.abs(vr[neg])
        t += dt; z = z_of_t(t)
        if alpha > 0:                                                # secondary infall on the accretion history
            carry += (1 - FB) * (Mz(z) - Mz(z_of_t(t - dt))) / m
            k = int(carry); carry -= k
            if k > 0:
                Mnow = Mz(z); rn = 2 * r200_of(Mnow, z); v200 = math.sqrt(G * Mnow / r200_of(Mnow, z))
                r = np.concatenate([r, np.full(k, rn) * (1 + 0.05 * rng.random(k))])
                vr = np.concatenate([vr, np.full(k, -v200)]); L = np.concatenate([L, rn * 0.4 * v200 * np.ones(k)])
                cold = np.concatenate([cold, np.ones(k, bool)])
        a_ = acc(r, z)
        vr += 0.5 * dt * a_
        if gam > 0 and cold.any():                                   # L365's trigger on the local total density
            cnt, _ = np.histogram(r, edges)
            rho_tot = cnt * m / vol + rho_st(rmid, z)
            xt = 1.5 * (np.interp(r, rmid, rho_tot) - Om * RHOC0 * (1 + z) ** 3) / (RHOC0 * E(z) ** 2)
            idx = np.where(cold & (xt > 5.0))[0]
            hit = idx[rng.random(len(idx)) < 1 - math.exp(-gam * H0 * E(z) * dt)]
            if len(hit):
                nh = rng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                vt_old = L[hit] / r[hit]
                vr[hit] += vk * nh[:, 0]
                L[hit] = r[hit] * np.hypot(vt_old + vk * nh[:, 1], vk * nh[:, 2])
                cold[hit] = False; ndec += len(hit)
    hist_all, _ = np.histogram(r, edges); hist_cold, _ = np.histogram(r[cold], edges)
    return tag, dict(edges=edges, m=m, hist=hist_all, hist_cold=hist_cold, n=len(r), n_cold=int(cold.sum()),
                     Mc_rs_init=Mc_rs0, Mc_rs_final=float(np.sum(r < rsi)) * m, rs=rsi, r200=r0,
                     M_ap=float(np.sum(r < RAP)) * m, M_ap_cold=float(np.sum((r < RAP) & cold)) * m)


if __name__ == "__main__":
    P(__doc__)
    # ------------------------------------------------------------------------------ L360's KiDS machinery (unedited)
    P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
    N60 = {"__name__": "l360", "__file__": P60}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P60).read().split("BASE = {")[0], N60)
    fit_comb, fit_model, carrier_esd, A052, XE59 = N60["fit_comb"], N60["fit_model"], N60["carrier_esd"], N60["A0"], N60["XE59"]
    project_M2, annulus_esd, rr, Rp, Rd, MS = [N60[k] for k in ("project_M2", "annulus_esd", "rr", "Rp", "Rd", "MS")]
    MPCm = N60["L52"]["MPCm"]
    FOOT = ("canonical", "alt"); SW = ("p=1, x_c0=1.5", "p=2, x_c0=2.0")
    XE = {c_: round(XE59[(float(c_.split(",")[0][2:]), float(c_.split("=")[2]))], 4) for c_ in SW}
    BASE = {f_: fit_model(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
    fitsw = fit_model(A052["canonical"], XE["p=2, x_c0=2.0"], "compensated", True)[1]
    MB = [10 ** lm_ for lm_, _, _ in fitsw]                          # the bins' fitted baryonic masses (switch alone)
    P(f"  KiDS bins: M_200 = {M200_BINS}; fitted M_b (p = 2 switch, canonical) = {[f'{x:.2e}' for x in MB]}")

    N = int(os.environ.get("L375_N", "60000"))
    VKW = 0.0 if MUTATE else 650.0
    cfgs = []
    for b in range(4):
        cfgs.append((f"b{b}_nodecay", b, MB[b], 650.0, 0.0, 0.75, True, N, 100 + b))
        cfgs.append((f"b{b}_fid", b, MB[b], VKW, 10.0, 0.75, True, N, 200 + b))
        cfgs.append((f"b{b}_a0.5", b, MB[b], VKW, 10.0, 0.5, True, N, 300 + b))
        cfgs.append((f"b{b}_a1.2", b, MB[b], VKW, 10.0, 1.2, True, N, 400 + b))
        cfgs.append((f"b{b}_bstatic", b, MB[b], VKW, 10.0, 0.75, False, N, 500 + b))
        cfgs.append((f"b{b}_v600", b, MB[b], 0.0 if MUTATE else 600.0, 10.0, 0.75, True, N, 600 + b))
        cfgs.append((f"b{b}_v700", b, MB[b], 0.0 if MUTATE else 700.0, 10.0, 0.75, True, N, 700 + b))
    cfgs.append(("b1_eq", 1, MB[1], 0.0, 0.0, 0.0, True, N, 900))    # C2: static NFW, no decay, no infall (5 Gyr)
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run")
    with Pool(int(os.environ.get("L375_POOL", "4"))) as pool:
        res = dict(pool.map(halo, cfgs, chunksize=1))
    P(f"  {len(cfgs)} halos done   [{time.time() - T0:.0f}s]")

    def template(runs):
        """per bin: the carrier's 3D density at z_l (kg/m^3 on L352's grid) -> annulus-averaged Delta Sigma (L352's projector)."""
        TC = []
        for b, d in enumerate(runs):
            e = d["edges"]; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
            rho = d["hist"] * d["m"] / vol                           # Msun/kpc^3
            rho_si = np.interp(np.log(rr / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3
            M2 = project_M2(rho_si)
            TC.append(annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[b]))
        return TC

    def kids(TC, cell):
        return {f_: float(fit_comb(A052[f_], XE[cell], TC, [1.0])[0] - BASE[f_]) for f_ in FOOT}

    banner("C1, C2  CONTROLS")
    eq = res["b1_eq"]; dev_eq = abs(eq["Mc_rs_final"] / eq["Mc_rs_init"] - 1)
    check("C2 a static NFW + baryons in Jeans equilibrium (no decay, no infall, 5 Gyr) keeps M(<r_s) within 10%",
          f"M(<r_s) final/initial = {eq['Mc_rs_final'] / eq['Mc_rs_init']:.3f}", dev_eq < 0.10)
    TC0 = template([res[f"b{b}_nodecay"] for b in range(4)])
    k0 = {c_: kids(TC0, c_) for c_ in SW}
    check("C1 with the decay off the shell-model carrier halo is rejected by KiDS (Delta chi^2 > +100, both switch cells, both "
          "footings), as L360's M1 rejects the NFW template", f"{k0}", min(v for d in k0.values() for v in d.values()) > 100)

    banner("THE RETAINED CARRIER AROUND KiDS LENSES (z_l = 0.25)")
    VAR = ("fid", "a0.5", "a1.2", "bstatic", "v600", "v700")
    TAB = {}
    for var in VAR:
        runs = [res[f"b{b}_{var}"] for b in range(4)]
        S = [runs[b]["M_ap"] / res[f"b{b}_nodecay"]["M_ap"] for b in range(4)]
        Sc = [runs[b]["M_ap_cold"] / res[f"b{b}_nodecay"]["M_ap"] for b in range(4)]
        TC = template(runs)
        kd = {c_: kids(TC, c_) for c_ in SW}
        TAB[var] = dict(S=S, S_cold=Sc, kids=kd, pass_p2=all(v <= 4.0 for v in kd["p=2, x_c0=2.0"].values()),
                        pass_p1=all(v <= 4.0 for v in kd["p=1, x_c0=1.5"].values()))
        P(f"    {var:8s}: S (<0.5 Mpc/h) by bin " + ", ".join(f"{s_:.3f}" for s_ in S) + "  (undecayed part " +
          ", ".join(f"{s_:.3f}" for s_ in Sc) + ")  |  KiDS p=2 " +
          f"{kd['p=2, x_c0=2.0']['canonical']:+.1f}/{kd['p=2, x_c0=2.0']['alt']:+.1f} {'ok' if TAB[var]['pass_p2'] else 'FAIL'}; p=1 "
          f"{kd['p=1, x_c0=1.5']['canonical']:+.1f}/{kd['p=1, x_c0=1.5']['alt']:+.1f} {'ok' if TAB[var]['pass_p1'] else 'FAIL'}")
    OUT["numbers"].update(M_b=MB, table=TAB, controls=dict(C1=k0, C2=eq["Mc_rs_final"] / eq["Mc_rs_init"]))
    check("K2 (informational) S per bin, the undecayed share, the accretion-history and baryon variants, v_k = 600/700, p = 1",
          "see table", True, "reported either way", load_bearing=False)

    banner("K1  THE HYPOTHESIS (set before the run)")
    f_ = TAB["fid"]
    check("K1 = H: at v_k = 650 km/s with the p = 2 switch, the resolved fiducial carrier halo passes KiDS on both footings",
          f"Delta chi^2 {f_['kids']['p=2, x_c0=2.0']}; S by bin {[round(s_, 3) for s_ in f_['S']]}", f_["pass_p2"] == EXPECT_PASS)

    banner("VERDICT")
    P(f"""  Resolved (spherical, self-consistent, secondary-infall) KiDS hosts at v_k = 650 km/s: S = {[round(s_, 3) for s_ in f_['S']]}
  (L367's sub-cell PM value: 0.02-0.04); KiDS with the p = 2 switch: {f_['kids']['p=2, x_c0=2.0']}.
  Variants passing (p = 2): {[v_ for v_ in VAR if TAB[v_]['pass_p2']]}; failing: {[v_ for v_ in VAR if not TAB[v_]['pass_p2']]}.
  LIMITS: spherical symmetry (no mergers, no triaxial orbits), a smooth accretion history, static baryons (their MOND boost
  does not act on the carrier, L353), one lens redshift (z_l = 0.25), the trigger posited (no action).""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
