#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR15b -- DOOR (b): A GRADIENT STIFFNESS THAT SWITCHES OFF INSIDE COLLAPSED REGIONS, (1/2) h(U) |grad U|^2, h = mu S(U).
Run because door (c) failed (XR15_smoothed_gate.py: no smoothing length brings every layer to Gamma <= H, one constant l
cannot also keep the flagship, and the capped branch and V0's loop are untouched).

WHY.  DE13's form (i), -(mu/2)|grad U|^2 with a constant mu, stabilises every DE12 layer from mu_U ~ 0.05 B r^2 (lambda_U =
0.21-0.22; universal eta_U = 8 pi G mu_U/c^4 = 3.2e-14), but acts wherever U varies: its potential is 32 v_f^2 at the
flagship radius and 2e8 v_f^2 at the Sun's distance (DE13 N1).  DE13's second open door: let the coefficient switch off
inside collapsed regions, h(U) = mu S(U), S = 1 on the layer and 0 deep inside, so the potential vanishes at r_F and at
the Sun.  Where it switches off, the switch has its own background term.

THE SECOND VARIATION (per delta U; checked against finite differences in B2):
    delta^2 [(1/2) int h(U) |grad U|^2] = int { h |grad dU|^2 - [ (1/2) h'' |grad U|^2 + h' lap U ] dU^2 },
so in DE13's variable eps = t_U dU:  s = S(U)/t_U^2 (the stiffness) and K0 = [(1/2) S'' |grad U|^2 + S' lap U]/t_U^2
(the switch's own term, destabilising where positive), entering DE13's E2 = 1/2 int {base eps^2 + mu s |grad eps|^2
- mu K0 eps^2} unchanged.  The switch: S = 1 - W(tau), tau = ln(U/U_1)/ln R, W DE12's smooth transition, U_1 = 1 + w (the
layer's inner edge, t = 1), so S = 1 across the whole layer and S = 0 for U >= U_1 R.

THE FIRST VARIATION (the repair's force on the baryons, A = 1 as DE13 N1):  Phi_rep = 4 pi G C mu [-div(S grad U) +
(1/2) S' |grad U|^2]; zero wherever U >= U_1 R.  The flagship (z = 2.5, M_b = 1e10, 1e10.5, 1e11, both footings) therefore
caps the switch width: R <= R_max = min U(r_F)/U_1.

METHOD.  DE13's machinery loaded unedited (its definitions only; its checks never run, its JSON never written): DE12's
transitions, DE13's base (gas at 1e6 K + the gate, the transverse A), its tridiagonal form with weights r^2 dr and Dirichlet
ends, and its exact negative-mode count (LDL^T pivots).  Each layer is resampled on 8000 points uniform in ln r from
U = 1.1 U_1 R (inside the switch) out to t = 0.004; negative modes are counted in DE13's five half-layer windows (in t) and in
three half-switch windows (in tau).  mu is one constant of the action: DE13's committed universal mu_U (galaxies).  A second
convention (the exact radial response A_par, with its own universal mu re-derived by DE13's bisection) is reported beside it.

PRE-DECLARED (written into this file before the main run):
  H_b [load-bearing]: some switch width R <= R_max leaves ALL 24 galaxy layers free of negative modes at the universal mu --
     in DE13's layer windows (the stiffness) and in the half-switch windows (the switch's own term against 1e6 K gas) --
     in DE13's convention; so the repair exerts no force at r_F (z = 2.5) or at the Sun.
  The writer's expectation before the run: H_b FAILS.  The universal mu is set by the most demanding layer and is orders of
  magnitude above what the low-redshift layers need, so their switch zones' own term overwhelms their gas, unless R is
  far larger than the flagship allows.

CHECKS
  B1 CONTROL: with S = 1 (no switch) this lane's assembly reproduces DE13's form (i) arrays exactly, and DE13's bisection
     on them returns DE13's committed lambda_U (three layers, 1e-12).
  B2 CONTROL: stiffness + K0 equal finite differences of the discretised (1/2) int h(U)|grad U|^2 r^2 dr (1e-4, three random
     directions); without K0 they miss by >= 1e-3.
  B3 [load-bearing; MUTATE's target] the switch's own term destabilises: for every R <= R_max some galaxy layer's switch
     zone has a negative mode at the universal mu; with K0 dropped (MUTATE) none does.
  H_b as pre-declared.
  R1-R4 (reported) per layer and R: negative modes in the layer and in the switch zone, the growth rate there against H and
     the layer's evolution rate; the smallest R that clears each switch zone at the universal mu and at the layer's own
     mu_U; the repair's potential and force in the switch zone and the layer (the KiDS lenses' interior), at r_F and at
     the Sun; the exact radial convention.
MUTATE=1 drops K0 (the switch's own background term): B3 must FAIL (rc = 1).

SCOPE.  DE12's frozen background and reduction; DE13's radial modes with the transverse A (conservative for the layer) and
the exact radial response as a check; isothermal 1e6 K gas; self-gravity and buoyancy neglected; spherical layers.  The
switch is one smooth family (a smooth step in ln U); other shapes (e.g. power laws, which never switch off) are not scanned.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR15_switched_stiffness.py
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
import scipy.sparse as sps
import scipy.linalg as sl
warnings.filterwarnings("ignore", message=".*overflow encountered.*")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR15_switched_stiffness"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR15b", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
if MUTATE: P("\n  *** MUTATE=1: the switch's own background term K0 is dropped; B3 must FAIL ***")

# ---------------------------------------------------------------------------------- DE13's machinery, loaded unedited
# (DE13's definitions block, which itself loads DE12's; DE13's checks never run, its JSON never written)
P13 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE13_gate_gradient_repair.py")
D13 = {"__name__": "de13", "__file__": P13}
_h13 = open(P13).read().split("# ============================================================================================ C1 C2 controls")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(_h13.replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D13)
D12 = D13["D12"]
transition, transition_on, Wd, G, MS, KPC, A0, nu_of, C_LIGHT = [D13[k] for k in (
    "transition", "transition_on", "Wd", "G", "MS", "KPC", "A0", "nu_of", "C_LIGHT")]
layer_fine, quad13, tri, neg_count, wcount, WINS, W_M, TU, CS2, GAL = [D13[k] for k in (
    "layer_fine", "quad", "tri", "neg_count", "wcount", "WINS", "W_M", "TU", "CS2", "GAL")]
ynup_of = D12["ynup_of"]
R13 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE13_gate_gradient_repair_results.json")))["numbers"]
ETA_U = R13["F1"]["eta_U_galaxies"]
MU_U = ETA_U * C_LIGHT ** 4 / (8 * math.pi * G)                           # DE13's universal (galaxies) mu_U
U1 = 1 + W_M                                                             # the layer's inner edge (t = 1)
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
RG = np.geomspace(0.05, 2e5, 12000) * KPC
SW_WINS = [(0.0, 0.5), (0.25, 0.75), (0.5, 1.0)]
P(f"  DE13 machinery loaded (definitions only); DE13's universal eta_U = {ETA_U:.3e}, mu_U = {MU_U:.3e} J/m   [{time.time() - T0:.0f}s]")


def switch(U, R):
    """S = 1 - W(tau), tau = ln(U/U1)/ln R, and its U-derivatives."""
    L = math.log(R)
    tau = np.log(np.maximum(U, 1e-300) / U1) / L
    W, W1, W2 = Wd(tau)
    return 1 - W, -W1 / (U * L), -(W2 / L - W1) / (U ** 2 * L), tau


def domain(z, Mb, foot, R, N=8000):
    """the layer plus the switch zone: from U = 1.1 U1 R inward of the layer out to t = 0.004, uniform in ln r."""
    tr = transition_on(RG, z, Mb, foot, W_M)
    U = (tr["t"] - 0.5) * 2 * W_M + 1
    m = (tr["t"] > 0) & (tr["t"] < 1)
    iout = np.where(m)[0].max()
    ro = float(np.interp(0.004, tr["t"][::-1], RG[::-1]))
    inner = np.where((U >= 1.1 * U1 * R) & (np.arange(len(U)) < iout))[0]
    ri = RG[inner.max()] if len(inner) else RG[0]
    return transition_on(np.geomspace(ri, ro, N), z, Mb, foot, W_M)


def quad_b(trf, R, conv="perp", drop_K0=False, no_switch=False):
    """DE13's quad for the switched stiffness: base (gas at 1e6 K + the gate), s = S/t_U^2, K0 = [(1/2) S'' |U'|^2 + S' lap U]/t_U^2."""
    r, t, rho, B = trf["r"], trf["t"], trf["rho_b"], trf["B"]
    _, W1, W2 = Wd(t)
    A = nu_of(trf["y"]) if conv == "perp" else nu_of(trf["y"]) + ynup_of(trf["y"])
    h = TU * 4 * math.pi * G * A / (trf["H"] ** 2 * trf["xce"])
    U = (t - 0.5) * 2 * W_M + 1
    dU = np.gradient(U, r); d2U = np.gradient(dU, r)
    base = CS2 / (rho * h ** 2) - B * W2
    if no_switch:
        S, dS, d2S, tau = np.ones_like(r), np.zeros_like(r), np.zeros_like(r), np.full_like(r, -1.0)
    else:
        S, dS, d2S, tau = switch(U, R)
    s = S / TU ** 2
    K0 = (0.5 * d2S * dU ** 2 + dS * (d2U + 2 * dU / r)) / TU ** 2
    if drop_K0:
        K0 = np.zeros_like(r)
    it = int(np.argmin(np.abs(t - 0.5)))
    return dict(r=r, t=t, U=U, tau=tau, base=base, s=s, K0=K0, S=S, dS=dS, dU=dU, unit=B[it] * r[it] ** 2, h=h, rho=rho,
                H=trf["H"], C=1 / (trf["H"] ** 2 * trf["xce"]), y=trf["y"])


def count(q, mu, lo, hi, var="t"):
    m = (q[var] >= lo) & (q[var] <= hi)
    return neg_count(q["r"][m], q["base"][m], q["s"][m], q["K0"][m], mu) if m.sum() > 3 else 0


def growth_b(q, mu, lo, hi, var="tau"):
    """the fastest growth rate on a window (displacement formulation with mass conservation, DE13's G1 scheme)."""
    m = np.where((q[var] >= lo) & (q[var] <= hi))[0]
    r, rho, hh = q["r"][m], q["rho"][m], q["h"][m]
    a, b, _ = tri(r, q["base"][m], q["s"][m], q["K0"][m], mu)
    n = len(a)
    Ke = sps.diags([a, b, b], [0, 1, -1], format="csr")
    Hh = sps.diags(hh[1:-1])
    ri = r[1:-1]; rh = 0.5 * (r[:-1] + r[1:]); rhoh = 0.5 * (rho[:-1] + rho[1:]); drh = np.diff(r)
    dri = 0.5 * (drh[:-1] + drh[1:])
    rows = np.repeat(np.arange(n), 2); cols = np.stack([np.arange(n), np.arange(n) + 1], 1).ravel()
    vals = np.stack([rh[:-1] ** 2 * rhoh[:-1] / (ri ** 2 * dri), -rh[1:] ** 2 * rhoh[1:] / (ri ** 2 * dri)], 1).ravel()
    D = sps.csr_matrix((vals, (rows, cols)), shape=(n, n + 1))
    Kx = (D.T @ Hh @ Ke @ Hh @ D).tocsr()
    mi = 1 / np.sqrt(rhoh * rh ** 2 * drh)
    Sm = (sps.diags(mi) @ Kx @ sps.diags(mi)).todia()
    ab = np.zeros((3, n + 1))
    for k in range(3):
        ab[2 - k, k:] = Sm.diagonal(k)
    ev = sl.eig_banded(ab, lower=False, eigvals_only=True, select="i", select_range=(0, 0))
    return math.sqrt(-ev[0]) / q["H"] if ev[0] < 0 else 0.0


def lam_bisect(q):
    """DE13's F1 bisection (log10 of mu in units of B r^2 at t = 1/2, DE13's five half-layer windows)."""
    lo, hi = -8.0, 8.0
    if max(wcount(q, 10 ** hi * q["unit"], wn) for wn in WINS) > 0:
        return None
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if max(wcount(q, 10 ** mid * q["unit"], wn) for wn in WINS) > 0: lo = mid
        else: hi = mid
    return 10 ** hi * q["unit"]


# ============================================================================================ B1 B2 controls
banner("B1  CONTROL: without the switch this lane's assembly is DE13's form (i), and DE13's bisection returns its lambda_U")
b1 = {}
for (z, Mb, foot) in ((0.25, 1e11, "canonical"), (2.5, 1e10, "alt"), (4.0, 1e12, "canonical")):
    trf = layer_fine(z, Mb, foot)
    q13 = quad13(trf, "i"); qb = quad_b(trf, 10.0, no_switch=True)
    arr = max(float(np.max(np.abs(q13[k] - qb[k]))) for k in ("base", "s", "K0"))
    mu = lam_bisect(qb)
    lam = math.sqrt(mu / qb["unit"])
    ref = R13["F1"]["rows"][KEY(z, Mb, foot)]["lam_U"]
    b1[KEY(z, Mb, foot)] = dict(array_diff=arr, lam_U=lam, lam_DE13=ref)
    P(f"    {KEY(z, Mb, foot)}: arrays differ by {arr:.1e}; lambda_U {lam:.12f} vs DE13's committed {ref:.12f}")
check("B1 CONTROL: with S = 1 the switched assembly reproduces DE13's form (i) arrays exactly and DE13's committed lambda_U (1e-12)",
      {k_: f"{v_['array_diff']:.0e} / {abs(v_['lam_U'] / v_['lam_DE13'] - 1):.0e}" for k_, v_ in b1.items()},
      all(v_["array_diff"] == 0.0 and abs(v_["lam_U"] / v_["lam_DE13"] - 1) < 1e-12 for v_ in b1.values()))
OUT["numbers"]["B1"] = b1

banner("B2  CONTROL: the switched stiffness's second variation against finite differences of its discretised functional")
trf = domain(0.25, 1e11, "canonical", 5.0, N=6000)
q = quad_b(trf, 5.0)
r, U = q["r"], q["U"]; dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1])
rng = np.random.default_rng(7)
b2w, b2wo = [], []
for _ in range(3):
    c0, wd, kw = rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.15), rng.uniform(5, 40)
    x = np.log(r / r[0]) / np.log(r[-1] / r[0])
    dUp = np.exp(-((x - c0) / wd) ** 2) * np.cos(kw * x); dUp[0] = dUp[-1] = 0.0

    def Erep(e):
        Ue = U + e * dUp
        Se = switch(0.5 * (Ue[1:] + Ue[:-1]), 5.0)[0]
        return 0.5 * np.sum(Se * (np.diff(Ue) / dr) ** 2 * rm ** 2 * dr)
    e = 1e-4
    fd = (Erep(e) + Erep(-e) - 2 * Erep(0.0)) / e ** 2

    def qf(K0):
        a, b, _ = tri(r, 0 * q["base"], q["s"] * TU ** 2, K0 * TU ** 2, 1.0)
        v = dUp[1:-1]
        return float(np.sum(a * v ** 2) + 2 * np.sum(b * v[:-1] * v[1:]))
    b2w.append(abs(qf(q["K0"]) / fd - 1)); b2wo.append(abs(qf(0 * q["K0"]) / fd - 1))
P(f"    with K0: {', '.join(f'{v:.1e}' for v in b2w)}; without: {', '.join(f'{v:.1e}' for v in b2wo)}")
check("B2 CONTROL: stiffness + K0 match the finite-difference second variation of (1/2) sum h(U)|grad U|^2 r^2 dr (1e-4); without "
      "K0 they miss by >= 1e-3", f"with {max(b2w):.1e}; without {max(b2wo):.1e}", max(b2w) < 1e-4 and max(b2wo) >= 1e-3,
      "the switch's own term -[(1/2) h''|grad U|^2 + h' lap U] is real and is in every count below")
OUT["numbers"]["B2"] = dict(with_K0=b2w, without_K0=b2wo)

# ============================================================================================ R1 the flagship caps the width
banner("R1  THE FLAGSHIP CAPS THE SWITCH WIDTH: the repair must be off (U >= U1 R) at r_F")
RMX = {}
for zf in (2.5, 4.0):
    for Mb in (1e10, 10 ** 10.5, 1e11):
        for f in ("canonical", "alt"):
            tr = transition(zf, Mb, f, W_M); rF = math.sqrt(G * Mb * MS / (0.1 * A0[f]))
            UF = (float(np.interp(rF, tr["r"], tr["t"])) - 0.5) * 2 * W_M + 1
            RMX[f"{zf}/{Mb:.2e}/{f}"] = UF / U1
R_MAX = min(v_ for k_, v_ in RMX.items() if k_.startswith("2.5/"))
P("    U(r_F)/U1: " + ", ".join(f"{k_}: {v_:.2f}" for k_, v_ in RMX.items()))
P(f"    R_max (z = 2.5, the flagship's epoch) = {R_MAX:.2f}; at z = 4 the cap would be {min(v_ for k_, v_ in RMX.items() if k_.startswith('4.0/')):.2f}")
OUT["numbers"]["R1_flagship_cap"] = dict(U_rF_over_U1=RMX, R_max=R_MAX)
P(f"  [{time.time() - T0:.0f}s]")


# ============================================================================================ R2 the scan
def evo_rate(z, Mb, foot):
    """the layer's own evolution rate: (1 + z) H |dr_e/dz| / L (U-edge, DE12's grid)."""
    re = []
    for zz in (z - 0.02, z + 0.02):
        tr = transition(zz, Mb, foot, W_M); re.append(float(np.interp(0.5, tr["t"][::-1], tr["r"][::-1])))
    tr = transition(z, Mb, foot, W_M)
    L = float(np.interp(0.0, tr["t"][::-1], tr["r"][::-1]) - np.interp(1.0, tr["t"][::-1], tr["r"][::-1]))
    return (1 + z) * abs(re[1] - re[0]) / 0.04 / L


banner("R2  EVERY GALAXY LAYER, EVERY SWITCH WIDTH: the layer (DE13's windows) and the switch zone (half-switch windows)")
RS = [1.5, 2.0, 3.0, 5.0, 8.0, round(R_MAX, 2), 20.0, 50.0, 100.0, 1000.0]
SCAN = {}
for (z, Mb, foot) in GAL:
    key = KEY(z, Mb, foot)
    muL = R13["F1"]["rows"][key]["mu_U"]
    rate = evo_rate(z, Mb, foot)
    row = dict(mu_universal_over_own=MU_U / muL, evo_rate_over_H=rate, R={})
    for R in RS:
        q = quad_b(domain(z, Mb, foot, R), R, drop_K0=MUTATE)
        nl = max(count(q, MU_U, *w) for w in WINS)
        ns = max(count(q, MU_U, *w, var="tau") for w in SW_WINS)
        nso = max(count(q, muL, *w, var="tau") for w in SW_WINS)
        g = growth_b(q, MU_U, 0.0, 1.0) if ns > 0 else 0.0
        go = growth_b(q, muL, 0.0, 1.0) if nso > 0 else 0.0
        m = (q["tau"] >= 0) & (q["tau"] <= 1)
        row["R"][R] = dict(layer_neg=nl, switch_neg=ns, switch_neg_own_mu=nso, Gamma_over_H=g, Gamma_own_over_H=go,
                           max_muK0_over_gas=float(np.max(MU_U * q["K0"][m] / q["base"][m])))
    SCAN[key] = row
    P(f"    {key:22s} mu/mu_own {row['mu_universal_over_own']:7.1f}; evolves at {rate:4.1f} H | switch-zone Gamma/H (universal mu) by R: " +
      " ".join(f"{row['R'][R]['Gamma_over_H']:.1e}" for R in RS) + f" | own mu at R_max: {row['R'][round(R_MAX, 2)]['Gamma_own_over_H']:.1e}"
      f"   [{time.time() - T0:.0f}s]")
P("    (R = " + ", ".join(str(R) for R in RS) + f"; R_max = {R_MAX:.2f} from the flagship)")
OUT["numbers"]["R2_scan"] = {k_: dict(v_, R={str(R): x_ for R, x_ in v_["R"].items()}) for k_, v_ in SCAN.items()}

RS_ok = [R for R in RS if R <= R_MAX + 1e-9]
b3 = all(any(SCAN[k_]["R"][R]["switch_neg"] > 0 for k_ in SCAN) for R in RS_ok)
worst = {R: max(SCAN[k_]["R"][R]["Gamma_over_H"] for k_ in SCAN) for R in RS}
clean_R = [R for R in RS if all(SCAN[k_]["R"][R]["switch_neg"] == 0 and SCAN[k_]["R"][R]["layer_neg"] == 0 for k_ in SCAN)]
check("B3 [MUTATE's target] the switch's own term destabilises: for every R <= R_max some galaxy layer's switch zone has a "
      "negative mode at the universal mu",
      f"layers with a negative switch-zone mode at R = {', '.join(str(R) for R in RS_ok)}: "
      f"{', '.join(str(sum(SCAN[k_]['R'][R]['switch_neg'] > 0 for k_ in SCAN)) for R in RS_ok)} of {len(SCAN)}; "
      f"fastest Gamma/H {', '.join(f'{worst[R]:.1e}' for R in RS_ok)}", b3,
      "where h switches off, -[(1/2) h''|grad U|^2 + h' lap U] ~ mu/r^2 exceeds the gas's stiffness; a wider switch only moves it "
      "inward, where mu/r^2 is larger")
check("H_b [pre-declared] some R <= R_max leaves all 24 galaxy layers free of negative modes at the universal mu (layer and "
      "switch zone), so the repair is off at r_F and at the Sun",
      f"R clearing every layer and switch zone: {clean_R if clean_R else 'none'} (scanned {RS[0]}-{RS[-1]})",
      any(R <= R_MAX + 1e-9 for R in clean_R))
own_all = {R: sum(SCAN[k_]["R"][R]["switch_neg_own_mu"] > 0 for k_ in SCAN) for R in RS}
P(f"    even with each layer's OWN mu_U (not one constant): layers with a negative switch-zone mode by R: {own_all}")
OUT["numbers"]["own_mu_unstable_layers_by_R"] = {str(k_): v_ for k_, v_ in own_all.items()}

# ============================================================================================ R3 the exact radial response
banner("R3  THE EXACT RADIAL RESPONSE (A_par): its own universal mu (DE13's bisection), and the switch zones at R_max")
mupar = {}
for (z, Mb, foot) in GAL:
    mupar[KEY(z, Mb, foot)] = lam_bisect(quad_b(layer_fine(z, Mb, foot), 10.0, conv="par", no_switch=True))
MU_PAR = max(v_ for v_ in mupar.values() if v_ is not None)
R3 = {}
for (z, Mb, foot) in GAL:
    key = KEY(z, Mb, foot)
    q = quad_b(domain(z, Mb, foot, R_MAX), R_MAX, conv="par", drop_K0=MUTATE)
    ns = max(count(q, MU_PAR, *w, var="tau") for w in SW_WINS)
    R3[key] = dict(switch_neg=ns, Gamma_over_H=growth_b(q, MU_PAR, 0.0, 1.0) if ns > 0 else 0.0,
                   layer_neg=max(count(q, MU_PAR, *w) for w in WINS))
P(f"    universal mu_par = {MU_PAR:.3e} J/m (eta = {8 * math.pi * G * MU_PAR / C_LIGHT ** 4:.2e}; DE13's convention {ETA_U:.2e}); at R_max: "
  f"switch zones unstable on {sum(v_['switch_neg'] > 0 for v_ in R3.values())}/{len(R3)} layers, fastest "
  f"{max(v_['Gamma_over_H'] for v_ in R3.values()):.2e} H; layers unstable {sum(v_['layer_neg'] > 0 for v_ in R3.values())}")
OUT["numbers"]["R3_exact_radial"] = dict(mu_par=MU_PAR, rows=R3)

# ============================================================================================ R4 the repair's force
banner("R4  THE REPAIR'S OWN FORCE at R_max: in the switch zone and the layer (the lenses' interior), at r_F and at the Sun")
R4 = {}
for (z, Mb, foot) in [(0.25, 1e11, "canonical"), (0.25, 1e11, "alt"), (0.25, 1e12, "canonical"), (1.0, 1e11, "canonical"),
                      (2.5, 1e11, "canonical"), (4.0, 1e10, "canonical")]:
    q = quad_b(domain(z, Mb, foot, R_MAX), R_MAX)
    r = q["r"]; a0 = A0[foot]
    S, dS = q["S"], q["dS"]; dU = q["dU"]
    Phi = 4 * math.pi * G * q["C"] * MU_U * (-np.gradient(r ** 2 * S * dU, r) / r ** 2 + 0.5 * dS * dU ** 2)
    grep = -np.gradient(Phi, r)
    gN = G * Mb * MS / r ** 2; gM = nu_of(q["y"]) * gN
    vf2 = math.sqrt(G * Mb * MS * a0)
    msw = (q["tau"] >= 0) & (q["tau"] <= 1); mly = (q["t"] > 0) & (q["t"] < 1)
    R4[KEY(z, Mb, foot)] = dict(Phi_switch_over_vf2=float(np.max(np.abs(Phi[msw])) / vf2), Phi_layer_over_vf2=float(np.max(np.abs(Phi[mly])) / vf2),
                                force_over_gMOND=float(np.max(np.abs(grep[msw | mly] / gM[msw | mly]))),
                                switch_kpc=(float(r[msw].min() / KPC), float(r[msw].max() / KPC)))
    v_ = R4[KEY(z, Mb, foot)]
    P(f"    {KEY(z, Mb, foot):22s}: switch zone {v_['switch_kpc'][0]:.0f}-{v_['switch_kpc'][1]:.0f} kpc; max |Phi_rep| {v_['Phi_switch_over_vf2']:.2e} v_f^2 "
      f"there, {v_['Phi_layer_over_vf2']:.2e} in the layer; max |g_rep|/g_MOND {v_['force_over_gMOND']:.2e}")
P("    at r_F (z = 2.5, R <= R_max) and at the Sun (U ~ 1e4-1e6 >> U1 R): S = S' = 0, the repair exerts no force (by construction)")
OUT["numbers"]["R4_repair_force"] = R4

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb} "
  f"({', '.join(n_.split()[0] for n_, ok, lb in CH if lb and not ok) or 'none'}); wrote {os.path.basename(fn)}   [{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
