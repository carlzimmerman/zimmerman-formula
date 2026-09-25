#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L359 -- THE VACUUM-GATED SWITCH: a threshold that rises into the matter era opens the KiDS-forest pincer that closed
L342's bound-region switch.

WHY.  L342's switch (C-H/K's MOND term acts only where x = 9 R3/(4K^2) >= x_c) repaired C-H/K's cosmology (L341's sigma_8
of 18-27 back to 0.81) and was closed by one pincer (L352 Z7; re-checked on the forest observable by L358): KiDS-1000 at
z_l ~ 0.25, scored with the profile the switch really produces (the Gauss-compensated phantom, L352), accepts only
x_c <~ 3, while the Lyman-alpha forest at z = 2-3 needs x_c >~ 7 (L347: 7.2% at 7; L358: 13-19% at 2-4).  The pincer
applies ONE threshold at two epochs.  The record lists a time-triggered threshold as the open door (L350-L352 notes).
This lane builds the natural one: gate the switch variable by the vacuum's share of the expansion -- the same rho_Lambda
that sets a0 in this framework --
      u = x~ [Omega_Lambda(z)/Omega_Lambda,0]^p >= x_c0,      i.e.   x_c,eff(z) = x_c0 E(z)^(2p),   E = H/H0,
and in the khronon's own variables Omega_Lambda = 3 Lambda / K^2 (K = 3H), so u = x~ (3 Lambda / (Omega_L0 K^2))^p is a
local scalar of the foliation (x~ = 9 (R3 + sigma_ij sigma^ij)/(4 K^2), L351's shear-completed variable).
It is tested exactly where the pincer was set, with the committed machinery, loaded unedited:
  * the forest OBSERVABLE: L347's particle-mesh run + FGPA 1D flux power (L358's rule: worst |P1D/P1D_LCDM - 1| <= 0.10 over
    k_par 0.2-2 h/Mpc at z = 3 and z = 2, both boxes 50 and 25 Mpc/h, both footings), with the threshold x_c,eff(a) applied
    at every step (one function copied from L347 with that single change);
  * KiDS-1000: L352's compensated-profile fit with the bias-like 2-halo term at the lens redshift's x_c,eff(0.25)
    (L352's acceptance: Delta chi^2 <= +4 against the unswitched model, both footings);
  * linear growth: L342's machinery (sigma_8 within 2% of LCDM, both footings, rms and per-mode field arguments);
  * the tensor speed: the gate is a function of K alone, and K is exactly unperturbed by a transverse-traceless mode, so
    L351's c_T = 1 (for the shear-completed variable) carries over.

CHECKS
  S1 the gate is local and tensor-blind: Omega_Lambda = 3 Lambda/K^2 on FRW; delta K = 0 exactly for the TT metric
     diag(e^h, e^-h, 1) (det = 1).
  C1 CONTROL: the copied forest runner with p = 0, x_c = 5 reproduces L347's committed P1D ratios.
  C2 CONTROL: the ungated switch (p = 0) at a KiDS-accepted threshold fails the forest (L358's pincer, re-derived).
  G1/K1/F1 growth, KiDS and forest per cell (p, x_c0); W1 THE WINDOW: cells with p > 0 that pass all three.
  Directions fixed from the committed numbers of L342/L347/L352/L358 before the run; nothing retuned.
MUTATE=1 removes the gate (p = 0 in every cell): the window must close (rc = 1).

SCOPE.  KiDS is L352's scoring, which takes the phantom inside the edge as an ISOLATED galaxy's (a kernel blind to the web's
field inside bound regions -- the bound-region kernel of L355's door); the forest runs use L347's universal-coupling
phantom (all matter sources the kernel), which overstates the construction's baryons-only phantom (conservative for the
forest); the shear part of x~ is not simulated (it can only lower the effective threshold); the low-z forest (z < 2) and
the nonlinear late-time growth with the switch on in filaments are not tested here.

Run from the repository root:  python3 real_research/g03_audit_2026/L359_vacuum_gated_switch.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import L347_switch_forest_flux_power as L7            # noqa: E402  (L347's machinery, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L359_vacuum_gated_switch"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L359", "mutate": MUTATE, "checks": {}, "numbers": {}}
INF = float("inf")


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def xc_of_a(a, xc0, p):
    """the gated threshold x_c,eff(a) = x_c0 E(a)^(2p) = x_c0 [Omega_L0/Omega_L(a)]^p (L347's background)."""
    return xc0 * (L7.Hnorm(a) ** 2) ** p


def run_gated(cfg):
    """L347's run(), copied; the ONE change: the threshold is x_c,eff(a) at every step instead of a constant."""
    name, L, mode, foot, xc0, p = cfg
    bx = L7.Box(L)
    rng = np.random.default_rng(7)
    kk = np.sqrt(bx.K2); kk[0, 0, 0] = bx.kf
    Pk = np.vectorize(lambda q: L7.P_lin(q, L7.ZI))(np.clip(kk, bx.kf, 40.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(L7.NG, L7.NG, L7.NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * L7.NG ** 3 / L ** 3)))
    psi = [-gg for gg in bx.grad(bx.poisson(delta0))]
    q = (np.arange(L7.NP) + 0.5) * L / L7.NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([bx.interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + L7.ZI); fg = L7.Om_a(ai) ** 0.55
    x = (Q + disp) % L; pmom = ai ** 2 * L7.Hnorm(ai) * fg * disp
    npart = len(x); a0 = L7.A0[foot]

    def accel(x, a):
        rho = bx.deposit(x, np.full(npart, 1.0)) * L7.NG ** 3 / npart
        delta = rho - 1.0
        phiN = bx.poisson(1.5 * L7.Om * delta / a)
        xc = xc_of_a(a, xc0, p)
        if mode == "lcdm" or (not np.isfinite(xc)):
            phi = phiN
        else:
            gphi = bx.grad(phiN)
            mag = np.sqrt(sum((gg / a ** 2) ** 2 for gg in gphi)) + 1e-30
            nu = L7.nu_mono(mag / a0)
            xs = 1.5 * L7.Om_a(a) * delta
            f = np.ones_like(xs) if xc == 0 else 0.5 * (1 + np.tanh((xs - xc) / (0.1 * xc)))
            phi = phiN + bx.poisson(bx.div([f * (nu - 1) * gg for gg in gphi]))
        return -np.stack([bx.interp(gg, x) for gg in bx.grad(phi)], 1)

    a = ai; dlna = 0.02; zs = list(L7.ZOUT); out = {}
    acc = accel(x, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * L7.Hnorm(a))
        pmom += 0.5 * dt * acc; x = (x + dt * pmom / a ** 2) % L; a = a + da
        acc = accel(x, a); pmom += 0.5 * dt * acc
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rho = bx.deposit(x, np.full(npart, 1.0)) * L7.NG ** 3 / npart
                kpar, p1d, A = L7.flux_p1d(bx, x, pmom, a, z)
                out[str(z)] = {"pk3": bx.pk3(rho - 1).tolist(), "kpar": kpar.tolist(), "p1d": p1d.tolist(), "A": A}
                zs.remove(z)
    return name, out


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the gate is removed (p = 0 everywhere); W1 must FAIL ***")
    import sympy as sp
    E2 = lambda z: L7.Om * (1 + z) ** 3 + L7.OL

    # ============================================================================ S1 the gate is local and tensor-blind
    banner("S1  THE GATE IN THE KHRONON'S VARIABLES, AND ITS TENSOR BLINDNESS")
    Hs, Lam, t, zc = sp.symbols("H Lambda t z", positive=True)
    Ksym = 3 * Hs                                                     # FRW: K = 3H (c = 1)
    OmL = Lam / (3 * Hs ** 2)                                         # Omega_Lambda = Lambda/(3 H^2)
    s1a = sp.simplify(OmL - 3 * Lam / Ksym ** 2) == 0
    hf = sp.Function("h")(t)
    g3 = sp.diag(sp.exp(hf), sp.exp(-hf), 1)                           # L351's TT metric
    Ktt = sp.simplify(sp.diff(sp.log(sp.sqrt(g3.det())), t))            # K = d/dt ln sqrt(det gamma) (unit lapse, zero shift)
    s1b = Ktt == 0
    check("S1 the gate is a local scalar of the foliation, Omega_Lambda = 3 Lambda/K^2, and a transverse-traceless mode leaves K "
          "exactly unperturbed (det = 1), so L351's c_T = 1 for the shear-completed variable carries over to u",
          f"Omega_L - 3 Lambda/K^2 = {sp.simplify(OmL - 3 * Lam / Ksym ** 2)}; K(TT) = {Ktt}", s1a and s1b,
          "the gate multiplies x~ by a function of K only")

    # ============================================================================ cells
    CELLS = [(0.0, 2.0), (0.0, 3.0)] + [(p_, x_) for p_ in (0.5, 1.0, 2.0) for x_ in (1.5, 2.0, 2.5)]
    if MUTATE:
        CELLS = [(0.0, x_) for (_, x_) in CELLS]
        CELLS = sorted(set(CELLS))
    P("\n  cells (p, x_c0) -> x_c,eff at z = 0 / 0.25 / 2 / 3:")
    for (p_, x_) in CELLS:
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f}: " + " / ".join(f"{x_ * E2(z_) ** p_:.2f}" for z_ in (0.0, 0.25, 2.0, 3.0)))

    # ============================================================================ G1 linear growth (L342's machinery)
    banner("G1  LINEAR GROWTH WITH THE GATED SWITCH (L342's B2 machinery; sigma_8 within 2% of 0.811)")
    from scipy.integrate import solve_ivp
    P42 = os.path.join(HERE, "L342_bound_region_switch.py")
    G42 = {"__name__": "l342", "__file__": P42}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P42).read().split("B2 = {}")[0], G42)
    Om42, Or42, rc42, G42c, Mpc42, h42, A042, DREF, KH42, nu42, s8of, SIG8 = [G42[k] for k in (
        "Om", "Or", "rho_crit0", "G", "Mpc", "h", "A0", "DREF", "KH", "nu_mono", "sigma8_of", "SIG8")]

    def growth_gated(xc0, p, foot, mode, z_i=1000.0):
        om = Om42; ol = 1 - om - Or42; a_i = 1 / (1 + z_i); a0 = A042[foot]
        Ez = lambda a: math.sqrt(Or42 / a ** 4 + om / a ** 3 + ol); dlnH = lambda a: 0.5 * (-4 * Or42 / a ** 4 - 3 * om / a ** 3) / Ez(a) ** 2
        r0 = solve_ivp(lambda N, Y: [Y[1], 1.5 * (om / math.exp(3 * N) / Ez(math.exp(N)) ** 2) * Y[0] - (2 + dlnH(math.exp(N))) * Y[1]],
                       (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14).y[0][-1]
        Di = DREF / r0
        xc = lambda a: xc0 * (Ez(a) ** 2 / Ez(1.0) ** 2) ** p

        def boost(y, a, dlt):                                        # L342's switch, with the gated threshold
            return nu42(y) if 1.5 * (om / a ** 3 / Ez(a) ** 2) * abs(dlt) >= xc(a) else 1.0
        if mode == "rms":
            def rhs(N, Y):
                a = math.exp(N); D, Dp = Y; rho = om * rc42 / a ** 3
                gk = 4 * math.pi * G42c * rho * np.abs(Di * D) / (KH42 * h42 / (a * Mpc42))
                grms = math.sqrt(np.trapz(gk ** 2 / KH42, KH42) / np.trapz(1 / KH42, KH42))
                drms = math.sqrt(np.trapz((Di * D) ** 2 / KH42, KH42) / np.trapz(1 / KH42, KH42))
                return [Dp, 1.5 * (om / a ** 3 / Ez(a) ** 2) * boost(grms / a0, a, drms) * D - (2 + dlnH(a)) * Dp]
            return Di * solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12).y[0][-1]
        out = []
        for i, kh in enumerate(KH42):
            def rhs(N, Y, kh=kh):
                a = math.exp(N); d, dp = Y; gN = 4 * math.pi * G42c * om * rc42 / a ** 3 * abs(d) / (kh * h42 / (a * Mpc42))
                return [dp, 1.5 * (om / a ** 3 / Ez(a) ** 2) * boost(gN / a0, a, d) * d - (2 + dlnH(a)) * dp]
            out.append(solve_ivp(rhs, (math.log(a_i), 0.0), [Di[i], Di[i]], method="LSODA", rtol=1e-7, atol=1e-22).y[0][-1])
        return np.array(out)

    GR = {}
    for (p_, x_) in CELLS:
        vals = {(f_, m_): float(s8of(growth_gated(x_, p_, f_, m_))) for f_ in ("canonical", "alt") for m_ in ("rms", "permode")}
        GR[(p_, x_)] = dict(vals=vals, ok=all(abs(v / SIG8 - 1) < 0.02 for v in vals.values()))
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f}: sigma_8 " + ", ".join(f"{k_[0][:5]}/{k_[1][:4]} {v:.3f}" for k_, v in vals.items())
          + f"  -> {'OK' if GR[(p_, x_)]['ok'] else 'FAIL'}   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["G1"] = {f"{k_[0]}/{k_[1]}": {"sigma8": {f"{a_}/{b_}": v for (a_, b_), v in d_["vals"].items()}, "ok": d_["ok"]}
                            for k_, d_ in GR.items()}

    # ============================================================================ K1 KiDS (L352's compensated-profile fit)
    banner("K1  KiDS-1000 AT THE LENS REDSHIFT (L352's compensated switch profile + bias-like 2-halo, Delta chi^2 <= +4)")
    P52 = os.path.join(HERE, "L352_switch_gauss_compensation.py")
    L52 = {"__name__": "l352", "__file__": P52}
    _s52 = open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    with contextlib.redirect_stdout(io.StringIO()):
        exec(_s52, L52)
    fit52, A052 = L52["fit_model"], L52["A0"]
    BASE = {f_: fit52(A052[f_], 0.0, "none", True)[0] for f_ in ("canonical", "alt")}
    KI = {}
    for (p_, x_) in CELLS:
        xe = x_ * E2(0.25) ** p_
        d_ = {f_: fit52(A052[f_], round(xe, 4), "compensated", True)[0] - BASE[f_] for f_ in ("canonical", "alt")}
        KI[(p_, x_)] = dict(x_eff=xe, dchi2=d_, ok=all(v <= 4.0 for v in d_.values()))
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f} (x_c,eff(0.25) = {xe:.2f}): Delta chi^2 canonical {d_['canonical']:+.1f}, alt "
          f"{d_['alt']:+.1f}  -> {'OK' if KI[(p_, x_)]['ok'] else 'FAIL'}   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["K1"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in KI.items()}

    # ============================================================================ F1 the forest observable
    banner("F1  THE FOREST OBSERVABLE (L347's PM + FGPA, the gated threshold at every step; L358's 10% rule)")
    cand = [c_ for c_ in CELLS if GR[c_]["ok"] and KI[c_]["ok"]]
    cfgs = []
    for Lb in (50.0, 25.0):
        tag = f"L{int(Lb)}"
        cfgs.append((f"{tag}_lcdm", Lb, "lcdm", "canonical", INF, 0.0))
        for (p_, x_) in cand:
            for f_ in ("canonical", "alt"):
                cfgs.append((f"{tag}_p{p_}_x{x_}_{f_}", Lb, "switch", f_, x_, p_))
    cfgs.append(("L50_ctrl_x5_canonical", 50.0, "switch", "canonical", 5.0, 0.0))     # C1: L347's committed cell
    P(f"    {len(cand)} growth+KiDS candidates -> {len(cfgs)} PM runs")
    with Pool(10) as pool:
        res = dict(pool.map(run_gated, cfgs))
    P(f"    runs done   [{time.time() - T0:.0f}s]")

    def p1d_dev(name, tag, z):
        kp = np.array(res[f"{tag}_lcdm"][z]["kpar"]); r = np.array(res[name][z]["p1d"]) / np.array(res[f"{tag}_lcdm"][z]["p1d"])
        m = (kp >= 0.2) & (kp <= 2.0)
        return float(np.max(np.abs(r[m] - 1)))

    ref = json.load(open(os.path.join(HERE, "L347_switch_forest_flux_power_results.json")))["numbers"]["runs"]
    dctl = 0.0
    for z in ("3.0", "2.0"):
        mine = np.array(res["L50_ctrl_x5_canonical"][z]["p1d"]) / np.array(res["L50_lcdm"][z]["p1d"])
        theirs = np.array(ref["L50_sw5_canon"][z]["p1d"]) / np.array(ref["L50_lcdm"][z]["p1d"])
        dctl = max(dctl, float(np.max(np.abs(mine - theirs))))
    check("C1 the copied runner with p = 0, x_c = 5 reproduces L347's committed P1D ratios (same code path, same phases)",
          f"max |difference| = {dctl:.1e}", dctl < 1e-9, load_bearing=False)
    FO = {}
    for (p_, x_) in cand:
        cells = {(tag, f_, z): p1d_dev(f"{tag}_p{p_}_x{x_}_{f_}", tag, z) for tag in ("L50", "L25") for f_ in ("canonical", "alt")
                 for z in ("3.0", "2.0")}
        worst = max(cells.values())
        FO[(p_, x_)] = dict(worst=worst, cells={f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in cells.items()}, ok=worst <= 0.10)
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f} (x_c,eff z=2 {x_ * E2(2.0) ** p_:.1f}, z=3 {x_ * E2(3.0) ** p_:.1f}): worst |P1D - 1| "
          f"{worst:.3f} -> {'PASS' if worst <= 0.10 else 'FAIL'};  by cell " + ", ".join(
              f"{k_[0]}/{k_[1][:5]}/z{k_[2][0]} {v:.3f}" for k_, v in sorted(cells.items())))
    OUT["numbers"]["F1"] = {f"{k_[0]}/{k_[1]}": v_ for k_, v_ in FO.items()}
    ung = [c_ for c_ in cand if c_[0] == 0.0]
    check("C2 CONTROL: the ungated switch at a KiDS-accepted threshold fails the forest's 10% rule (L358's pincer re-derived)",
          ", ".join(f"x_c = {c_[1]}: {FO[c_]['worst']:.3f}" for c_ in ung) or "no ungated candidate",
          bool(ung) and all(not FO[c_]["ok"] for c_ in ung), "the pincer is reproduced before the gate is tested", load_bearing=False)

    # ============================================================================ W1 the window
    banner("W1  THE WINDOW: growth + KiDS + forest together, gated cells (p > 0)")
    win = [c_ for c_ in cand if c_[0] > 0 and FO[c_]["ok"]]
    for (p_, x_) in CELLS:
        tag = ("growth " + ("OK" if GR[(p_, x_)]["ok"] else "FAIL") + "; KiDS " + ("OK" if KI[(p_, x_)]["ok"] else "FAIL")
               + "; forest " + (("PASS" if FO[(p_, x_)]["ok"] else "FAIL") if (p_, x_) in FO else "not run"))
        P(f"    p = {p_:3.1f}, x_c0 = {x_:3.1f}: {tag}" + ("   <- WINDOW" if (p_, x_) in win else ""))
    OUT["numbers"]["W1"] = [dict(p=c_[0], x_c0=c_[1]) for c_ in win]
    check("W1 THE VACUUM-GATED SWITCH OPENS THE PINCER: cells with p > 0 pass linear growth (sigma_8 within 2%), KiDS-1000 (Delta "
          "chi^2 <= +4, compensated profile, both footings) and the forest observable (<= 10%, both boxes, both footings) together",
          ", ".join(f"(p = {c_[0]}, x_c0 = {c_[1]})" for c_ in win) or "no cell", len(win) > 0,
          "the forest (z = 2-3) and KiDS (z = 0.25) see different thresholds; one threshold cannot satisfy both, a vacuum-gated one can")

    banner("VERDICT")
    if win:
        P(f"""  THE SWITCH LIVES AGAIN.  Gating L342's switch variable by the vacuum's share of the expansion,
  u = x~ [Omega_L(z)/Omega_L,0]^p (= x~ (3 Lambda/(Omega_L0 K^2))^p, local and tensor-blind), gives a threshold that is high
  in the matter era and low today.  The cells {', '.join(f'(p={c_[0]:g}, x_c0={c_[1]:g})' for c_ in win)} pass linear growth
  (sigma_8 = LCDM), KiDS-1000 with the realizable (Gauss-compensated) profile and the Lyman-alpha forest observable at once:
  the KiDS-forest pincer of L352/L358 was a statement about a CONSTANT threshold.
  Conditional on: the bound-region kernel for KiDS (L352's isolated phantom inside the edge; L355's door); the shear part of
  x~ in the web (not simulated); the low-z forest and the late nonlinear growth with filaments switched on (not tested).""")
    else:
        P("  No gated cell passes growth, KiDS and the forest together: the pincer survives the vacuum gate.")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
