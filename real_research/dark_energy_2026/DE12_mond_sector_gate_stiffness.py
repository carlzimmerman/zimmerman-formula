#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE12 -- THE MOND-SECTOR GATE AS AN ACTION TERM: THE BARYON STIFFNESS BUDGET, THE GATE'S OWN FORCE, AND THE SLIP.

WHY.  The model the threads converged on (M*) switches MOND on where the MOND sector's own density crosses the vacuum
threshold.  CV3 writes that gate in constrained-field form, U = C[lap(u - v) + div((nu - 1) grad S w)]: it reads the
auxiliaries, never the metric's curvature.  MS5 wrote the region cap as U_cap = C m(lap Phi_X, v_cap^2 kappa_X^2).
DE7 showed that any smooth on/off gate has f'' > 0 somewhere (Lean DE7 T1).  For the curvature reading that convexity
lands on the metric (a wrong-sign k^4 term, repaired at the cost of slip).  For the MOND-sector reading it lands
somewhere else: the auxiliaries are slaved to the baryons by their constraints (lap(u - v) = 4 pi G rho_b, and w by
L361's source), so the gate's second variation is a k^0 term in the BARYON density -- a negative contribution to the
gas's pressure.  This lane prices that, and the gate's first variation (a potential felt by baryons and light alike).

THE REDUCTION (frozen background, high k against the transition width):
  dU/d rho_b = (4 pi G/(H^2 x_c,eff)) A,   A(theta) = nu + y nu' cos^2(theta)     (the phantom's own response: nu_perp,
      d(y nu)/dy along g; the on-branch phantom in CV3's form is ungated);
  kappa branch (MS5, where v_cap^2 kappa^2 < lap Phi_X): dU/d rho_b = (v_cap^2 kappa/|g|)(k_perp/k)^2 (4 pi G A/(H^2 x_c))
      and d2U/d rho_b^2 = v_cap^2 (k_perp/k)^4 (4 pi G A)^2 / (2 |g|^2 H^2 x_c) (MS5's definite-sign W'/2 piece);
  the gate's second variation, per (delta rho_b)^2:  S = B [W'' t_U^2 (U_rho)^2 + W' t_U U_rhorho],  t_U = 1/(2w),
      B = a0^2 q(y^2)/(8 pi G) (DE7's constitutive coupling; the V0 writer measured dL/df within ~10% of it at edges);
  the gas: delta^2 E = (1/2)(c_s^2/rho_b - S)(delta rho_b)^2, so it is stable only if c_s^2 > c_gate^2 = rho_b S, and
      otherwise grows at Gamma(k) = k sqrt(c_gate^2 - c_s^2) above the Jeans scale;
  the gate's first variation through u (CV1's chassis: the u equation feeds Phi): Phi_gate = -4 pi G B W' t_U C
      = -a0^2 q W'/(4 w H^2 x_c,eff), felt by baryons and by light (Phi is the metric potential) -- no slip at this order.
      (The w channel adds a term of the same order; it is the V0 writer's CV3.)
  slip: U depends on the metric only through the Laplacian's coefficients, so the gate's anisotropic stress is
      ~ B W' t_U C d_i d_j chi and psi - phi ~ 3 b W' Omega_L(z) Phi_N/(w x_c,eff): a factor ~ (v/c)^2 below DE7's
      curvature-gate slip.

THE TRANSITIONS.  Isolated spherical systems at z = 0.25, 1, 2.5, 4: point-mass baryons M_b = 1e10, 1e11, 1e12 (galaxies)
and 1e14 (a cluster, where the kappa cap is active), both footings.  The gas around each system follows its host's matter
(the NFW continued past r200, plus the mean): rho_b = f_b (rho_NFW + rho_bar_m).  Its sound speed is c_s at T = 1e5 K
(37 km/s, WHIM) and T = 1e6 K (117 km/s).  The gate: MS2's MOND-sector reading, p = 1, x_c0 = 2.5, w = 0.25 and 1.

CHECKS
  C1 CONTROL [numeric, 3-d periodic grid] the QUMOND phantom's response to a small plane-wave baryon perturbation on a
     uniform background field reproduces A(theta) = nu + y nu' cos^2(theta) at theta = 0 and 90 deg (y = 1e-3, 1e-1) to 2%.
  C2 CONTROL the gate potential's closed form equals -4 pi G B W' t_U C evaluated on the profile (identity, 1e-12).
  G1 [pre-declared hypothesis, load-bearing] on M* (w = 0.25) the gate's negative stiffness beats the gas pressure
     (c_gate > c_s at T = 1e6 K) somewhere on EVERY galaxy transition at z = 0.25, and the growth rate there, at
     k = 1/kpc, exceeds H(z) by more than 1e3: the varied MOND-sector gate makes transition-layer gas unstable on
     sub-Myr to Myr timescales.
  G2 (reported) where it bites: the baryon mass in the unstable part of each layer, against the system's baryons;
     and the broad gate (w = 1) alongside, since c_gate scales as 1/w.
  G3 (reported) the A = 1 control: MS1's other leak-free reading, U = C rho_b (the baryons alone), at its own transition.
  G4 (reported) the gate potential: max |Phi_gate|/v_f^2 per transition, and the flagship's zero-point shift at r_F
     (z = 2.5-4, both footings) -- zero wherever r_F sits on the plateau.
  G5 (reported) the slip estimate, against DE7's curvature-gate numbers.
  G6 (reported) the kappa-capped cluster.
MUTATE=1 removes the phantom's amplification (A = 1) and takes the gate at w = 1: G1 must FAIL (rc = 1).

SCOPE.  Frozen background; the fluid description of the gas (it fails below the gas's mean free path, ~0.3 kpc in
the WHIM); isothermal sound speed; point-mass baryons for the MOND field; the u channel of the gate's first variation.
This is not a simulation of the instability's nonlinear outcome.

Run from the repository root:  python3 real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE12_mond_sector_gate_stiffness"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE12", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_FAIL_BUDGET = True                                             # G1, set before the run


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: A = 1 and w = 1; G1 must FAIL ***")

# ---------------------------------------------------------------------------------- L352's constants and kernel
P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
L52 = {"__name__": "l352", "__file__": P52}
_s = open(P52).read().split('banner("Z1')[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s, L52)
G, H0, Om, OL, rho_crit0, A0, LYG, YG, HM, DH = [L52[k] for k in ("G", "H0", "Om", "OL", "rho_crit0", "A0", "LYG", "YG", "HM", "DH")]
MS = 1.98892e30; KPC = L52["Mpc"] / 1e3; KB, MP = 1.380649e-23, 1.67262e-27
FB = 0.02237 / (0.02237 + 0.1200); h = 0.6736
E2 = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                      # L359's gate background
Hz = lambda z: H0 * math.sqrt(Om * (1 + z) ** 3 + OL)
h_of = lambda y: np.interp(np.log10(y), LYG, HM)
dh_of = lambda y: np.interp(np.log10(y), LYG, DH)
QG = 2.0 * ((2.0 / 3.0) * YG[0] ** 1.5 + np.concatenate([[0.0], np.cumsum(0.5 * (HM[1:] + HM[:-1]) * np.diff(YG))]))
q_of = lambda y: np.interp(np.log10(y), LYG, QG)
nu_of = lambda y: 1.0 + h_of(y) / y
# nu' from nu = 1 + h/y: nu' = h'/y - h/y^2;  y nu' = h' - h/y
ynup_of = lambda y: dh_of(y) - h_of(y) / y
V_CAP = 325e3
CS = {"1e5K": math.sqrt(KB * 1e5 / (0.6 * MP)), "1e6K": math.sqrt(KB * 1e6 / (0.6 * MP))}
P(f"  constants loaded; gas sound speeds: {', '.join(f'{k} {v / 1e3:.0f} km/s' for k, v in CS.items())}   [{time.time() - T0:.0f}s]")


def Wd(t):
    t = np.asarray(t, float)
    inside = (t > 0) & (t < 1)
    tt = np.where(inside, t, 0.5)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    W = 1 / (1 + np.exp(ell))
    gq = 1 / tt ** 2 + 1 / (1 - tt) ** 2
    gp = -2 / tt ** 3 + 2 / (1 - tt) ** 3
    W1 = W * (1 - W) * gq
    W2 = W * (1 - W) * ((1 - 2 * W) * gq ** 2 + gp)
    W = np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, W))
    return W, np.where(inside, W1, 0.0), np.where(inside, W2, 0.0)


# ============================================================================================ C1 the amplification
banner("C1  CONTROL: the phantom's response to a plane-wave baryon perturbation is A(theta) = nu + y nu' cos^2 theta")
N1 = 64; Lb = 1.0
kx = np.fft.fftfreq(N1, d=Lb / N1) * 2 * np.pi
KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
xs = np.arange(N1) * Lb / N1
X, Y, Zc = np.meshgrid(xs, xs, xs, indexing="ij")


def spec_grad(f):
    F = np.fft.fftn(f)
    return [np.real(np.fft.ifftn(1j * kk * F)) for kk in (KX, KY, KZ)]


def spec_div(v):
    return sum(np.real(np.fft.ifftn(1j * kk * np.fft.fftn(vv))) for kk, vv in zip((KX, KY, KZ), v))


def phantom_density(dphi, g0, a0=1.0):
    """4 pi G rho_ph = div[(nu - 1) grad phi_N] for phi_N = g0 x + dphi (uniform field along x plus a perturbation)."""
    gx, gy, gz = spec_grad(dphi)
    gx = gx + g0
    mag = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    nu1 = nu_of(mag / a0) - 1
    return spec_div([nu1 * gx, nu1 * gy, nu1 * gz])


c1 = {}
for y0 in (1e-3, 1e-1):
    for th, (mx, my) in (("0deg", (1, 0)), ("90deg", (0, 1))):
        eps = 1e-6 * y0
        kvec = 2 * np.pi * np.array([mx, my, 0]) / Lb
        drho = eps * np.cos(kvec[0] * X + kvec[1] * Y)                 # 4 pi G delta rho_b (units: a0 per length)
        dphi = np.real(np.fft.ifftn(-np.fft.fftn(drho) / K2))
        r1 = phantom_density(dphi, y0) - phantom_density(0 * dphi, y0)
        Ameas = float(np.sum(r1 * drho) / np.sum(drho * drho)) + 1.0
        Apred = float(nu_of(y0) + (ynup_of(y0) if th == "0deg" else 0.0))
        c1[f"y{y0:g}/{th}"] = (Ameas, Apred)
        P(f"    y = {y0:g}, theta = {th}: measured A = {Ameas:.4f}, predicted {Apred:.4f}")
dev1 = max(abs(a / b - 1) for a, b in c1.values())
check("C1 CONTROL: the plane-wave response reproduces A = nu + y nu' cos^2 theta (y = 1e-3, 1e-1; theta = 0, 90 deg) to 2%",
      f"max rel dev {dev1:.1e}", dev1 < 0.02)
OUT["numbers"]["C1"] = c1


# ============================================================================================ the transitions
def host(Mb, z):
    """the host of M_b (L360's bins' Moster-like ratio, f_b-scaled) and its NFW, continued past r200."""
    M200 = Mb / (0.3 * FB) if Mb < 1e13 else Mb / FB                    # galaxies: 30% of the cosmic baryons bound; clusters: all
    rhoc = rho_crit0 * E2(z) * (Hz(z) / (H0 * math.sqrt(E2(z)))) ** 2
    c = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / h))) * (1 + z) ** -0.5
    r200 = (3 * M200 * MS / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
    rho_s = M200 * MS / (4 * math.pi * rs ** 3 * (math.log(1 + c) - c / (1 + c)))
    return dict(M200=M200, r200=r200, rs=rs, rho_s=rho_s)


def transition(z, Mb, foot, w, amp=True, cap=False):
    a0 = A0[foot]; H = Hz(z); xce = 2.5 * E2(z)
    rho_bar = Om * rho_crit0 * (1 + z) ** 3
    hs = host(Mb, z)
    r = np.geomspace(1.0, 2e4, 20000) * KPC
    y = G * Mb * MS / (r ** 2 * a0)
    rho_ph = Mb * MS * (h_of(y) - y * dh_of(y)) / (2 * math.pi * r ** 3 * y)            # point-mass on-branch phantom
    rho_nfw = hs["rho_s"] / ((r / hs["rs"]) * (1 + r / hs["rs"]) ** 2)
    rho_b = FB * (rho_nfw + rho_bar)                                                   # gas tracing the host + the mean
    xms = 4 * math.pi * G * (rho_b + rho_ph - FB * rho_bar) / H ** 2                    # MS2's door, contrast form
    gN = G * Mb * MS / r ** 2; g = nu_of(y) * gN
    xkap = (V_CAP ** 2 / r ** 2) / H ** 2                                              # MS5's kappa branch (kappa = 1/r)
    use_kap = cap & (xkap < xms)
    U = np.where(use_kap, xkap, xms) / xce
    t = (U - 1) / (2 * w) + 0.5
    _, W1, W2 = Wd(t)
    tU = 1 / (2 * w)
    B = a0 ** 2 * q_of(y) / (8 * math.pi * G)
    A_perp = nu_of(y) if amp else np.ones_like(y)
    A_par = (nu_of(y) + ynup_of(y)) if amp else np.ones_like(y)
    Umax = 4 * math.pi * G / (H ** 2 * xce)
    out = {"r": r, "t": t, "rho_b": rho_b, "B": B, "g": g, "y": y, "use_kap": use_kap, "H": H, "xce": xce}
    S = {}
    for lab, A in (("perp", A_perp), ("par", A_par)):
        Urho = Umax * A
        if cap:
            # kappa branch: transverse k only (k_perp = k) for the worst case; along g (k_perp = 0) it vanishes
            kfac = (V_CAP ** 2 * (1 / r) / g) if lab == "perp" else 0.0 * r
            Urho_k = kfac * Urho
            # U = v_cap^2 kappa^2/(H^2 x_c), delta kappa = (4 pi G A delta rho)/(2|g|) at k_perp = k: U_rhorho = 2 v_cap^2 (dkappa/drho)^2/(H^2 x_c)
            Urr_k = (V_CAP ** 2 * (4 * math.pi * G * A) ** 2 / (2 * g ** 2 * H ** 2 * xce)) if lab == "perp" else 0.0 * r
            Urho = np.where(use_kap, Urho_k, Urho)
            Urr = np.where(use_kap, Urr_k, 0.0)
        else:
            Urr = 0.0 * r
        S[lab] = B * (W2 * tU ** 2 * Urho ** 2 + W1 * tU * Urr)
    out["c_gate2"] = {lab: rho_b * np.maximum(S[lab], 0.0) for lab in S}
    out["Phi_gate"] = -4 * math.pi * G * B * W1 * tU / (H ** 2 * xce)
    out["Phi_closed"] = -a0 ** 2 * q_of(y) * W1 / (4 * w * H ** 2 * xce)
    out["vf2"] = math.sqrt(G * Mb * MS * a0)
    return out


banner("C2  CONTROL: the gate potential's closed form")
tr = transition(0.25, 1e11, "canonical", 0.25)
c2 = float(np.max(np.abs(tr["Phi_gate"] - tr["Phi_closed"])) / max(np.max(np.abs(tr["Phi_closed"])), 1e-300))
check("C2 CONTROL: Phi_gate = -4 pi G B W' t_U C equals -a0^2 q W'/(4 w H^2 x_c,eff) on the profile", f"{c2:.1e}", c2 < 1e-12)

# ============================================================================================ G1 G2 the budget
banner("G1 G2  THE BARYON STIFFNESS BUDGET ON REAL TRANSITIONS (M*: MOND-sector door, p = 1, x_c0 = 2.5)")
W_M = 1.0 if MUTATE else 0.25
AMP = not MUTATE
ZS = (0.25, 1.0, 2.5, 4.0)
MBS = (1e10, 1e11, 1e12)
TAB = {}
for z in ZS:
    for Mb in MBS:
        for foot in ("canonical", "alt"):
            tr = transition(z, Mb, foot, W_M, amp=AMP)
            m = (tr["t"] > 0) & (tr["t"] < 1)
            if not m.any():
                continue
            cg = np.sqrt(np.maximum(tr["c_gate2"]["perp"], tr["c_gate2"]["par"]))
            cmax = float(np.max(cg[m]))
            unst = m & (cg > CS["1e6K"])
            dr = np.gradient(tr["r"])
            M_unst = float(np.sum(4 * math.pi * tr["r"][unst] ** 2 * tr["rho_b"][unst] * dr[unst])) / MS
            k1 = 1 / KPC
            gam = k1 * math.sqrt(max(cmax ** 2 - CS["1e6K"] ** 2, 0.0))
            r_e = float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1])) / KPC
            TAB[f"{z}/{Mb:.0e}/{foot}"] = dict(c_gate_max=cmax, M_unstable=M_unst, M_unst_over_Mb=M_unst / Mb,
                                               Gamma_over_H=gam / tr["H"], r_edge_kpc=r_e,
                                               Phi_gate_over_vf2=float(np.max(np.abs(tr["Phi_gate"][m])) / tr["vf2"]))
            P(f"    z = {z:4.2f} M_b = {Mb:.0e} {foot:9s}: edge {r_e:7.1f} kpc; max c_gate {cmax / 1e3:9.0f} km/s "
              f"(gas 37/117 km/s); unstable gas {M_unst:.2e} Msun ({M_unst / Mb:.2e} of M_b); Gamma(k = 1/kpc)/H = {gam / tr['H']:.1e}; "
              f"max |Phi_gate|/v_f^2 = {TAB[f'{z}/{Mb:.0e}/{foot}']['Phi_gate_over_vf2']:.3f}")
OUT["numbers"]["budget"] = TAB
z25 = [v for k, v in TAB.items() if k.startswith("0.25/")]
g1 = all(v["c_gate_max"] > CS["1e6K"] and v["Gamma_over_H"] > 1e3 for v in z25) and len(z25) > 0
check("G1 [pre-declared] on M* (w = 0.25) the gate's negative stiffness beats 1e6 K gas pressure on every z = 0.25 galaxy "
      "transition, growing at k = 1/kpc faster than 1e3 H(z)",
      f"min c_gate {min(v['c_gate_max'] for v in z25) / 1e3:.0f} km/s; min Gamma/H {min(v['Gamma_over_H'] for v in z25):.1e}",
      g1 == EXPECT_FAIL_BUDGET,
      "the varied MOND-sector gate makes the transition-layer gas unstable (a new obstruction for M* at the action level)")
G1b = {}
for Mb in MBS:
    trw = transition(0.25, Mb, "canonical", 1.0, amp=AMP)
    mw = (trw["t"] > 0) & (trw["t"] < 1)
    cgw = np.sqrt(np.maximum(trw["c_gate2"]["perp"], trw["c_gate2"]["par"]))
    G1b[f"{Mb:.0e}"] = float(np.max(cgw[mw])) if mw.any() else None
P("    the lead track's broad gate (w = 1), z = 0.25, canonical: max c_gate " + ", ".join(
    f"{k}: {v / 1e3:.0f} km/s" for k, v in G1b.items() if v))
OUT["numbers"]["w1_broad_gate"] = G1b
check("G2 (reported) the baryon mass in the unstable part of each layer", {k: f"{v['M_unst_over_Mb']:.1e}" for k, v in TAB.items()},
      True, load_bearing=False)

# ============================================================================================ G3 the A = 1 control
banner("G3  THE A = 1 CONTROL: MS1's other leak-free reading, U = C rho_b (baryons alone)")
G3 = {}
for z in (0.25, 2.5):
    for Mb in (1e11,):
        for foot in ("canonical",):
            trA = transition(z, Mb, foot, 0.25, amp=False)
            m = (trA["t"] > 0) & (trA["t"] < 1)
            cg = np.sqrt(np.maximum(trA["c_gate2"]["perp"], trA["c_gate2"]["par"]))
            G3[f"{z}/{Mb:.0e}"] = float(np.max(cg[m])) if m.any() else None
            P(f"    z = {z}, 1e11 canonical, A = 1 (same edge): max c_gate {G3[f'{z}/{Mb:.0e}'] / 1e3 if G3[f'{z}/{Mb:.0e}'] else float('nan'):.1f} km/s")
OUT["numbers"]["A1_control"] = G3
check("G3 (reported) without the phantom's amplification the gate's c_gate falls by ~A (the A^2 is the story)", G3, True,
      load_bearing=False)

# ============================================================================================ G4 the gate potential at r_F
banner("G4  THE GATE POTENTIAL AT THE FLAGSHIP RADIUS (z = 2.5-4), both footings")
G4 = {}
for z in (2.5, 3.0, 3.5, 4.0):
    for foot in ("canonical", "alt"):
        tr = transition(z, 1e11, foot, 0.25)
        a0 = A0[foot]
        rF = math.sqrt(G * 1e11 * MS / (0.1 * a0))
        gg = -np.gradient(tr["Phi_gate"], tr["r"])
        gF = float(np.interp(rF, tr["r"], gg))
        gM = float(nu_of(0.1)) * 0.1 * a0
        sh = 2 * math.log10(max((gM + gF) / gM, 1e-300))
        tF = float(np.interp(rF, tr["r"], tr["t"]))
        G4[f"{z}/{foot}"] = dict(shift_dex=sh, t_at_rF=tF)
        P(f"    z = {z}, {foot:9s}: t(r_F) = {tF:.3f}; gate force at r_F / g_MOND = {gF / gM:+.3e}; zero-point shift {sh:+.4f} dex")
OUT["numbers"]["flagship_gate_force"] = G4
check("G4 (reported) the flagship zero-point shift from the gate's own force", {k: round(v["shift_dex"], 4) for k, v in G4.items()},
      True, "zero wherever r_F sits on the plateau (t >= 1)", load_bearing=False)

# ============================================================================================ G5 slip and G6 the cluster
banner("G5 G6  THE SLIP, AND THE KAPPA-CAPPED CLUSTER")
G5 = {}
for z in (0.25, 2.5):
    tr = transition(z, 1e11, "canonical", 0.25)
    m = (tr["t"] > 0) & (tr["t"] < 1)
    b = (tr["B"] * 8 * math.pi * G) / (L52["c"] ** 2 * 3 * OL * H0 ** 2)                # b = B/(M^2 Lambda) = 8 pi G B/(c^4 Lambda)
    _, W1, _ = Wd(tr["t"])
    OmL = OL / (Om * (1 + z) ** 3 + OL)
    slip_rel = float(np.max((3 * b * W1 * OmL / (0.25 * tr["xce"]))[m]))                  # (psi - phi)/Phi_N
    G5[str(z)] = slip_rel
    P(f"    z = {z}: MOND-sector gate slip / Phi_N <= {slip_rel:.1e}  (DE7's curvature gate: 5.7% of g at z = 0.25, 43% at 2.5)")
trc = transition(0.25, 1e14, "canonical", 0.25, cap=True)
mc = (trc["t"] > 0) & (trc["t"] < 1)
cgc = np.sqrt(np.maximum(trc["c_gate2"]["perp"], trc["c_gate2"]["par"]))
G6 = dict(cap_active_frac=float(np.mean(trc["use_kap"][mc])) if mc.any() else None,
          c_gate_max=float(np.max(cgc[mc])) if mc.any() else None)
P(f"    cluster 1e14 at z = 0.25 with the kappa cap: cap active on {G6['cap_active_frac']} of its layer; max c_gate "
  f"{(G6['c_gate_max'] or 0) / 1e3:.0f} km/s (ICM ~ 1000 km/s)")
OUT["numbers"]["slip"] = G5; OUT["numbers"]["cluster_kappa"] = G6
check("G5 (reported) the MOND-sector gate's slip is post-Newtonian-suppressed", G5, True, load_bearing=False)
check("G6 (reported) the kappa-capped cluster layer", G6, True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
