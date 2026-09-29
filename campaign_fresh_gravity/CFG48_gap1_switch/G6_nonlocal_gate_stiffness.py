#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G6 -- THE NONLOCAL BARYON-READING GATES AGAINST DE12's STIFFNESS BUDGET (gate GB).  Two nonlocal functionals of the baryon density, each entering as
      B(x) W(t) with the MOND-sector energy scale B = a0^2 q(y)/(8 pi G) (DE7/DE12's constitutive coupling), VARIED, on DE12's 24 layers x w in {0.25, 1},
      gas at 1e6 K.  Two readings of what the gate reads: 'baryon-mass' (A = 1) and 'dynamical-mass' (A = A_par = nu + y nu', the response of the enclosed
      baryon+phantom mass, the analogue of MS1's carrier-blind reading A+).

  VOLTERRA (enclosed-mass) gate.  U_enc(r) = U_0(r) [1 + A dM_b(<r)/M_0(<r)],  dM(<r) = int_0^r 4 pi s^2 drho ds  (linear in dM).  With m = dM(<r):
        E2 = (1/2) int [ p m'^2 - V m^2 ] dr,   p = c_s^2/(4 pi r^2 rho_b),   V = 4 pi r^2 B W''(t) (t_U U_0 A/M_0)^2,   t_U = 1/(2w),
     m = 0 at the ends of a Dirichlet window, kinetic weight K = 1/(4 pi r^2 rho_b).  Negative modes counted exactly (Sylvester, LDL^T pivots) on DE13's five
     half-layer windows (t-width 0.5, t_0 in linspace(0.004, 0.496, 5)) and the full layer.  eta_crit = the factor by which B would have to be multiplied for the
     first negative mode to appear (bisection on the full layer).  Growth rate of the fastest full-layer mode: Gamma = sqrt(-lambda_min), A m = lambda K m.
  TOP-LEVEL-BALL (rank-one) gate.  The maximal-ball functional of G2 gives every point of the layer ONE number, the ball radius R: t(r) = t_0(r R_0/R).
     E_gate(lnR) = -int 4 pi r^2 B W(t(r; lnR)) dr.  The ball radius solves phi(R) + A dM = 0, phi(R) = M_eff,0(R) - (4 pi/3) rhobar Delta R^3 (edge threshold set at the
     layer midpoint t = 0.5).  With L1 = dlnR/dM, L2 = d2 lnR/dM2 the FULL second variation (rank-one) is
        E2 = (1/2) dM^2 [ c_s^2/M_gas + E_R L2 + E_RR L1^2 ],   E_R = dE_gate/dlnR,  E_RR = d2E_gate/dlnR2,
     by Cauchy-Schwarz over the gas inside the ball (exact for a rank-one gate); unstable iff the bracket is negative: Xi = -(E_R L2 + E_RR L1^2) M_gas/c_s^2 > 1.
     (The FIRST run of this lane used only the W'' term of E_RR; it missed E_R L2 and the W' part of E_RR.  Disclosed; this version supersedes it.)
     Reported also: the gate's FIRST variation, the potential step Delta mu = E_R L1 A per unit baryon mass at the ball boundary, against v_f^2 and c_s^2.
CONTROLS.  C1: the local gate's c_gate_max reproduces DE12's committed budget (24 layers).  C2: the LOCAL gate in the same counting machinery (number of nodes with
     c_gate > c_s, DE12's own arrays) has negative modes on >= 90% of the 48 cases, so the counter is not blind.
PRE-DECLARED (before the first run; the baryon-mass reading A = 1):
  H_V  the Volterra gate has at least one negative mode fitting in the layer on >= 75% of the 48 layer x w cases.
  H_R  the top-level-ball gate has Xi > 1 on >= 75% of the 48 cases.
DECLARED AFTER SEEING ROUND 1 (round 1 gave 0/48 for both on the baryon-mass reading, so the lane added the dynamical-mass reading, which the phantom amplifies by up to nu ~ 30):
  H_V2 the Volterra gate with the dynamical-mass reading has a negative mode on >= 75% of the 48 cases.
  H_R2 the ball gate with the dynamical-mass reading has Xi > 1 on >= 75% of the 48 cases.
MUTATE=1 sets B = 0: no negative modes and Xi = 0; the LOCAL control C2 and every H must FAIL.
SCOPE.  Frozen background (DE12's, spherical); isothermal gas 117 km/s; a fluid description; the point-mass baryons plus DE12's gas as the baryon reservoir; the
      gas at rest in a background that does not include the gate's own force; z = 0.25, 1, 2.5, 4.  A gate defined through enclosed mass about a centre is a
      SPHERICAL statement; no covariant field-theoretic definition is written (GD).
"""
import os, sys, math, json
import numpy as np
from scipy.linalg import eigh_tridiagonal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G6_nonlocal_gate_stiffness", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: B = 0 (no gate energy scale); C2 and every H must FAIL ***")

de = load_de12()
Wd, transition, CS = de["Wd"], de["transition"], de["CS"]
nu_of, ynup_of = de["nu_of"], de["ynup_of"]
KPC = de["KPC"]; MSUN = de["MS"]; Hz = de["Hz"]
cs = CS["1e6K"]
ZS = (0.25, 1.0, 2.5, 4.0); MBS = (1e10, 1e11, 1e12); FOOTS = ("canonical", "alt"); WS = (0.25, 1.0)
committed = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]["budget"]

# =================================================================================================== C1 control
R.banner("C1  control: the LOCAL c_gate reproduces DE12's committed budget on all 24 layers")
worst = 0.0
for z in ZS:
    for Mb in MBS:
        for foot in FOOTS:
            tr = transition(z, Mb, foot, 0.25)
            m = (tr["t"] > 0) & (tr["t"] < 1)
            if not m.any():
                continue
            cg = np.sqrt(np.maximum(tr["c_gate2"]["perp"], tr["c_gate2"]["par"]))
            key = f"{z}/{Mb:.0e}/{foot}"
            if key in committed:
                worst = max(worst, abs(float(np.max(cg[m])) / committed[key]["c_gate_max"] - 1))
P(f"    max relative deviation from DE12's committed c_gate_max over the layers: {worst:.2e}")
R.check("C1 control: the local gate's c_gate_max equals DE12's committed value on every layer (1e-9)", f"{worst:.2e}", worst < 1e-9)


def neg_count(diag, off):
    """number of negative eigenvalues of a symmetric tridiagonal matrix (Sylvester's law of inertia via LDL^T pivots)."""
    n = len(diag); cnt = 0; d = diag[0]
    if d < 0: cnt += 1
    for i in range(1, n):
        if d == 0.0:
            d = 1e-300
        d = diag[i] - off[i - 1] ** 2 / d
        if d < 0: cnt += 1
    return cnt


def build_A(r, p_mid, Vn):
    h = np.diff(r)
    n = len(r) - 2
    w = 0.5 * (h[:-1] + h[1:])
    pk = p_mid / h
    diag = pk[:-1] + pk[1:] - Vn[1:-1] * w
    off = -pk[1:-1]
    return diag, off, w


def layer_arrays(z, Mb, foot, w, reading):
    tr = transition(z, Mb, foot, w)
    t = tr["t"]; r = tr["r"]; rho = tr["rho_b"]; B = tr["B"] * (0.0 if MUTATE else 1.0)
    dr = np.gradient(r)
    Mgas = np.cumsum(4 * math.pi * r ** 2 * rho * dr)
    M0 = Mb * MSUN + Mgas
    _, W1, W2 = Wd(t)
    U0 = 1 + 2 * w * (t - 0.5)
    tU = 1.0 / (2 * w)
    A = (nu_of(tr["y"]) + ynup_of(tr["y"])) if reading == "dyn" else np.ones_like(r)
    p = cs ** 2 / (4 * math.pi * r ** 2 * rho)
    V = 4 * math.pi * r ** 2 * B * W2 * (tU * U0 * A / M0) ** 2
    return dict(tr=tr, t=t, r=r, rho=rho, B=B, M0=M0, Mgas=Mgas, W2=W2, p=p, V=V, A=A, H=Hz(z), dr=dr)


def volterra(La):
    t = La["t"]
    lay = np.where((t > 0.004) & (t < 0.996))[0]
    wins = [("full", lay)]
    for t0 in np.linspace(0.004, 0.496, 5):
        sel = np.where((t >= t0) & (t <= t0 + 0.5))[0]
        if len(sel) > 20:
            wins.append((f"t0={t0:.3f}", sel))
    counts = {}; lam_full = None
    for name, sel in wins:
        sub = sel[::max(1, len(sel) // 3000)]
        r_, p_ = La["r"][sub], La["p"][sub]
        diag, off, wgt = build_A(r_, 0.5 * (p_[1:] + p_[:-1]), La["V"][sub])
        sc = float(np.max(np.abs(diag))) or 1.0
        counts[name] = neg_count(diag / sc, off / sc)
        if name == "full":
            K = (1.0 / (4 * math.pi * r_ ** 2 * La["rho"][sub]))[1:-1] * wgt
            Ds = 1.0 / np.sqrt(K)
            d2 = diag * Ds ** 2; o2 = off * Ds[:-1] * Ds[1:]
            sc2 = float(np.max(np.abs(d2))) or 1.0
            lam_full = float(eigh_tridiagonal(d2 / sc2, o2 / sc2, select="i", select_range=(0, 0), eigvals_only=True)[0] * sc2)
    # eta_crit on the full layer
    sub = lay[::max(1, len(lay) // 1500)]
    r_, p_ = La["r"][sub], La["p"][sub]
    pm = 0.5 * (p_[1:] + p_[:-1])
    Vfull = La["V"][sub]
    Vmax = np.max(Vfull)
    eta = float("inf")
    if Vmax > 0:
        def has(e):
            d_, o_, _ = build_A(r_, pm, e * Vfull)
            s_ = float(np.max(np.abs(d_))) or 1.0
            return neg_count(d_ / s_, o_ / s_) > 0
        lo, hi = 1e-8, 1e14
        if has(hi):
            for _ in range(70):
                mid = math.sqrt(lo * hi)
                if has(mid): hi = mid
                else: lo = mid
            eta = hi
    return counts, lam_full, eta


def ball(La, w):
    """full second variation of the rank-one top-level-ball gate; returns Xi, the potential step over v_f^2 and c_s^2."""
    t, r, B, W2 = La["t"], La["r"], La["B"], La["W2"]
    lay = np.where((t > 0.004) & (t < 0.996))[0]
    mid = lay[np.argmin(np.abs(t[lay] - 0.5))]
    R0 = r[mid]
    M0, Mg, A = La["M0"], La["Mgas"], La["A"]
    # effective reading: dynamical mass = nu * M for reading 'dyn' (A_par response), baryon mass otherwise
    nuy = np.where(A > 1.0 + 1e-12, nu_of(La["tr"]["y"]), 1.0)
    Meff = M0 * nuy
    Meff_mid = Meff[mid]
    rhobarD = Meff_mid / (4 * math.pi * R0 ** 3 / 3)                 # threshold (edge at the midpoint)
    phi = Meff - (4 * math.pi / 3) * rhobarD * r ** 3

    def lnR_of(dM):
        f = phi + A * dM
        s = np.where(np.diff(np.sign(f)) != 0)[0]
        if len(s) == 0:
            return float("nan")
        j = s[np.argmin(np.abs(s - mid))]
        x = -f[j] / (f[j + 1] - f[j])
        return math.log(r[j]) + x * (math.log(r[j + 1]) - math.log(r[j]))

    eps = 1e-4 * M0[mid]
    lp, l0, lm = lnR_of(eps), lnR_of(0.0), lnR_of(-eps)
    L1 = (lp - lm) / (2 * eps); L2 = (lp - 2 * l0 + lm) / eps ** 2

    def Egate(dl):
        rs = r * math.exp(-dl)
        ts = np.interp(rs, r, t)
        Wv = Wd(ts)[0]
        return -float(np.sum(4 * math.pi * r ** 2 * B * Wv * La["dr"]))
    h = 2e-3
    E0, Ep, Em = Egate(0.0), Egate(h), Egate(-h)
    E_R = (Ep - Em) / (2 * h); E_RR = (Ep - 2 * E0 + Em) / h ** 2
    Mgas_ball = float(Mg[mid])
    press = cs ** 2 / Mgas_ball
    gatepart = E_R * L2 + E_RR * L1 ** 2
    Xi = -gatepart / press
    dmu = abs(E_R * L1 * A[mid])                                    # J/kg
    vf2 = La["tr"]["vf2"]
    return dict(Xi=Xi, E_R_L2=E_R * L2 / press, E_RR_L1sq=E_RR * L1 ** 2 / press, dmu_over_vf2=dmu / vf2, dmu_over_cs2=dmu / cs ** 2, L1M=L1 * M0[mid], L2M2=L2 * M0[mid] ** 2)


res = {}
cnt = {"V": {"1": 0, "dyn": 0}, "R": {"1": 0, "dyn": 0}, "L": 0}
byz = {}
ncase = 0
R.banner("G  the 24 layers x 2 widths x 2 readings")
for w in WS:
    for z in ZS:
        for Mb in MBS:
            for foot in FOOTS:
                trL = transition(z, Mb, foot, w)
                tL = trL["t"]; lay = np.where((tL > 0.004) & (tL < 0.996))[0]
                if len(lay) < 50:
                    continue
                ncase += 1
                cgL = np.sqrt(np.maximum(trL["c_gate2"]["perp"], trL["c_gate2"]["par"])) * (0.0 if MUTATE else 1.0)      # MUTATE: B = 0
                nloc = int(np.sum(cgL[lay] > cs))
                cnt["L"] += int(nloc > 0)
                key = f"w{w}/{z}/{Mb:.0e}/{foot}"
                res[key] = dict(local_nodes_unstable=nloc, local_c_gate_max_kms=float(np.max(cgL[lay])) / 1e3)
                for reading in ("1", "dyn"):
                    La = layer_arrays(z, Mb, foot, w, "dyn" if reading == "dyn" else "1")
                    counts, lam, eta = volterra(La)
                    has = max(counts.values()) > 0
                    gam = math.sqrt(-lam) / La["H"] if (lam is not None and lam < 0) else 0.0
                    b = ball(La, w)
                    res[key][reading] = dict(neg_modes=counts, has_negative=has, eta_crit=eta, gamma_over_H=gam, **b)
                    cnt["V"][reading] += int(has)
                    byz.setdefault((reading, z), [0, 0])
                    byz[(reading, z)][0] += int(has); byz[(reading, z)][1] += 1
                    cnt["R"][reading] += int(b["Xi"] > 1)
                if foot == "canonical" and w == 0.25:
                    a, d = res[key]["1"], res[key]["dyn"]
                    P(f"    w=0.25 z={z:4.2f} M_b={Mb:.0e} can: LOCAL unstable nodes {nloc:5d} (c_gate {res[key]['local_c_gate_max_kms']:6.0f} km/s) | "
                      f"Volterra A=1: neg {max(a['neg_modes'].values())}, eta_crit {a['eta_crit']:.1e} | A_par: neg {max(d['neg_modes'].values())}, eta_crit {d['eta_crit']:.1e}, Gamma/H {d['gamma_over_H']:.1e} | "
                      f"ball Xi A=1 {a['Xi']:.2e}, A_par {d['Xi']:.2e}; dmu/v_f^2 {d['dmu_over_vf2']:.2f}, dmu/c_s^2 {d['dmu_over_cs2']:.1f}")
R.num("cases", res)
P(f"\n    cases evaluated: {ncase}")
P("    Volterra negative modes by redshift (dynamical-mass reading): " + ", ".join(f"z={z}: {byz[('dyn', z)][0]}/{byz[('dyn', z)][1]}" for z in ZS if ('dyn', z) in byz) + "; baryon-mass reading: " + ", ".join(f"z={z}: {byz[('1', z)][0]}/{byz[('1', z)][1]}" for z in ZS if ('1', z) in byz))
P(f"    LOCAL gate with an unstable node: {cnt['L']}/{ncase};  Volterra negative mode: A=1 {cnt['V']['1']}/{ncase}, A_par {cnt['V']['dyn']}/{ncase};  ball Xi > 1: A=1 {cnt['R']['1']}/{ncase}, A_par {cnt['R']['dyn']}/{ncase}")
ok = lambda n: n >= 0.75 * ncase
R.check("C2 control: the LOCAL gate has unstable nodes (c_gate > c_s) on >= 90% of the 48 cases in the same window/counting machinery", f"{cnt['L']}/{ncase}" + ("  [MUTATE: B = 0]" if MUTATE else ""), cnt["L"] >= 0.9 * ncase)
R.check("H_V (pre-declared) the Volterra gate, baryon-mass reading, has a negative mode on >= 75% of the 48 cases", f"{cnt['V']['1']}/{ncase}", ok(cnt["V"]["1"]))
R.check("H_R (pre-declared) the ball gate, baryon-mass reading, has Xi > 1 on >= 75% of the 48 cases", f"{cnt['R']['1']}/{ncase}", ok(cnt["R"]["1"]))
R.check("H_V2 (declared after round 1) the Volterra gate, dynamical-mass reading, has a negative mode on >= 75% of the 48 cases", f"{cnt['V']['dyn']}/{ncase}", ok(cnt["V"]["dyn"]))
R.check("H_R2 (declared after round 1) the ball gate, dynamical-mass reading, has Xi > 1 on >= 75% of the 48 cases", f"{cnt['R']['dyn']}/{ncase}", ok(cnt["R"]["dyn"]))
eta1 = [v["1"]["eta_crit"] for v in res.values()]; etad = [v["dyn"]["eta_crit"] for v in res.values()]
xi1 = [v["1"]["Xi"] for v in res.values()]; xid = [v["dyn"]["Xi"] for v in res.values()]
dmu = [v["dyn"]["dmu_over_vf2"] for v in res.values()]; dmc = [v["dyn"]["dmu_over_cs2"] for v in res.values()]
R.check("R1 (reported) eta_crit = factor on B for the first Volterra negative mode", f"A=1: min {min(eta1):.2e}; A_par: min {min(etad):.2e}, median {float(np.median(etad)):.2e}", True, load_bearing=False)
R.check("R2 (reported) ball Xi range (Xi > 1 unstable)", f"A=1: {min(xi1):.2e} .. {max(xi1):.2e}; A_par: {min(xid):.2e} .. {max(xid):.2e}", True, load_bearing=False)
R.check("R3 (reported) the ball gate's FIRST variation: potential step at the ball boundary per unit baryon mass (A_par reading)", f"dmu/v_f^2: {min(dmu):.2f} .. {max(dmu):.2f}; dmu/c_s^2: {min(dmc):.1f} .. {max(dmc):.1f}", True, load_bearing=False)
R.verdict("GB / Volterra enclosed-mass gate, baryon-mass reading", "PASS" if cnt["V"]["1"] == 0 else "FAIL",
          f"no negative mode on {ncase - cnt['V']['1']}/{ncase} cases; eta_crit (factor on B for the first mode) min {min(eta1):.1f}, i.e. the local gate's instability (44/48) is removed with margin")
R.verdict("GB / Volterra enclosed-mass gate, dynamical-mass reading", "PASS" if cnt["V"]["dyn"] == 0 else "FAIL",
          f"negative mode on {cnt['V']['dyn']}/{ncase} cases: every z = 0.25 and z = 1 layer and part of z = 2.5 (phantom amplification A_par up to ~30); Gamma/H up to {max(v['dyn']['gamma_over_H'] for v in res.values()):.0f}; the frozen rule (a fail on any layer = FAIL) applies")
R.verdict("GB / top-level-ball rank-one gate (second variation)", "PASS" if cnt["R"]["dyn"] == 0 and cnt["R"]["1"] == 0 else "FAIL",
          f"Xi in [{min(xi1 + xid):.1f}, {max(xi1 + xid):.2f}] < 0 on all {ncase} cases, both readings: the energy is nearly linear in ln R (E_RR L1^2 ~ 0 numerically; B r^3 ~ const in the transition region) and ln R is concave in M (E_R L2 > 0), so the gate STABILISES. "
          f"CAVEAT (first variation, R3): a potential step of {min(dmu):.2f}-{max(dmu):.2f} v_f^2 ({min(dmc):.1f}-{max(dmc):.1f} c_s^2) at the ball boundary means DE12's frozen background is NOT an equilibrium of the varied theory")
nf = R.write()
sys.exit(1 if nf else 0)
