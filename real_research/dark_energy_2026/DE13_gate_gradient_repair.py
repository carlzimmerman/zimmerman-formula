#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE13 -- CAN A GRADIENT STIFFNESS REPAIR DE12's OBSTRUCTION?  The exact second variation of mu|grad U|^2 and mu|grad f|^2.

WHY.  DE12 (7f84b3546) found that the converged model's MOND-sector gate, varied as an action term, is a negative bulk
modulus for the baryons in each transition layer: omega^2 = (c_s^2 - c_gate^2) k^2 with c_gate = 1500-3700 km/s at
z = 0.25, a gradient instability worst in the UV.  The review asked for the natural repair, a gradient stiffness on the
gate, and whether it pushes every unstable mode out of the layer (k_c below 1/L_layer).  Two forms:
  (i)  - (mu_U/2) |grad U|^2    the review's form;
  (ii) - (mu_f/2) |grad f|^2    a gradient energy on the gate itself (f = W(t)), nonzero only where f varies.
Both read only MOND-sector fields, so MS1's reciprocity holds for any functional of Phi - v (MS5 A1's identity), and they
add a Korteweg-like energy for the constraint-slaved baryons, not a new propagating field.
THE EXACT SECOND VARIATION.  Take the gate variable eps = delta t = h delta rho_b, with h = t_U U_rho and the transverse
A = nu of DE12 (its worst direction).  To second order a layer's energy is
    E2 = 1/2 int { [c_s^2/(rho_b h^2) - B W''] eps^2 + mu s |grad eps|^2 - mu K0 eps^2 } d^3x,
    form (i):  s = 1/t_U^2,  K0 = 0                                     (the term is quadratic in U);
    form (ii): s = W'^2,     K0 = (W''^2 + W' W''') |grad t|^2 + 2 W' W'' lap t.
K0 is the repair's own background term: to second order, f's change couples to the background gradient grad f.  At both
edges of the layer W''^2 + W'W''' ~ 2 W''^2 > 0, so K0 destabilises.  It scales with mu exactly as the stiffness does,
so on scales longer than W's own variation length the repair destabilises the layer however large mu is.
METHOD.  Each layer is resampled on 8000 points uniform in ln r over t in [0.004, 0.996].  DE12's transition() is used
with the radial grid as an argument (that one line replaced; C2 checks it is DE12's on DE12's grid).  The radial form is
discretised with weights r^2 dr and Dirichlet ends.  Negative modes are counted exactly: they are the negative LDL^T
pivots of the tridiagonal matrix (Sylvester's law of inertia).  A mode FITS IN THE LAYER if it has negative energy on a
Dirichlet window half the layer wide (t-width 0.5, five windows), i.e. k >= 2 pi/L, the review's lenient scale.  The
full-layer count, which also admits layer-wide modes, is reported alongside.

CHECKS
  C1 CONTROL: with no repair this lane's c_gate reproduces DE12's committed value (z = 0.25, 1e11, canonical) exactly.
  C2 CONTROL: DE12's transition() with the grid as an argument is DE12's transition() on DE12's grid, exactly.
  C3 CONTROL: the second variation (stiffness + K0) matches finite differences of the discretised
     1/2 int |grad W(t0 + s eps)|^2 r^2 dr to 1e-4 on three random eps; without K0 it misses by >= 1e-3 on at least one.
  C4 CONTROL: without the repair every galaxy layer has negative modes (DE12's instability in this lane's discrete form);
     gas alone has none.
  R1 [pre-declared in the first run; kept exactly as run] form (ii)'s scale-free lambda = sqrt(mu_f/(B r^2)) that makes
     mu' k^2 >= c_gate^2 - c_s^2 at k = 1/L on every galaxy layer lies in [0.05, 2].  See RESULT.
  E1 [load-bearing; added after R1] the repair's own second variation (form ii, gate and gas off) is indefinite on every
     galaxy layer, with a negative mode inside a half-layer window.
  E2 [load-bearing; added after R1] form (ii) stabilises no galaxy layer: for every lambda in 1e-3 to 1e5 (33 log steps,
     mu_f = lambda^2 B r^2 at t = 1/2), some half-layer window keeps a negative mode.
  E3 [load-bearing; added after E2] on every galaxy layer one direction eps* has negative energy under the gate and gas
     alone (G[eps*] < 0) and under the repair alone (R[eps*] < 0): eps* is the repair's lowest mode on the outer
     half-window.  Then G + mu R < 0 for EVERY mu >= 0 (Lean DE13.no_mu_stabilises), so E2 holds for all mu, not only
     the scanned range.
  G1 (reported) the fastest residual mode's growth rate at the lambda with the fewest modes: displacement formulation,
     with mass conservation built in, on 1500 and 3000 points.
  F1 (reported) form (i) stabilises every layer above a minimum mu_U; per layer, and the universal eta_U = 8 pi G mu_U/c^4.
  N1 [load-bearing; threshold set in the second run before its numbers] form (i)'s own potential, taken with the smallest
     universal mu_U that stabilises every galaxy layer, exceeds v_f^2 at the flagship radius r_F (z = 2.5, 1e11) and at
     the Sun's distance (z = 0, 6e10 Msun, 8 kpc).
  R3 (reported) form (ii)'s edge potential per lambda^2: max |Phi_f|/v_f^2 at lambda = 1 on each layer.
MUTATE=1 drops K0, the repair's own background term: E1, E2 and E3 must FAIL (rc = 1).
RESULT.  First run: R1 FAILED (lambda = 241 on galaxies, 536 with the cluster).  Its criterion was the WKB stiffness
mu' k^2 alone at k = 1/L; it has no K0, and it asks for stiffness at the layer's edges, where W'^2 -> 0.  The exact
second variation (this run) supersedes it.  Form (ii) stabilises no layer at any strength.  Form (i) stabilises every
layer, but its own potential is enormous wherever U varies.  R1 is kept exactly as declared.

SCOPE.  DE12's frozen-background reduction and profiles; isothermal fluid gas at 1e6 K; spherical isolated systems;
radial modes with the transverse amplification (conservative: A_par < A_perp only strengthens the gas term); self-gravity
and buoyancy are neglected at the modes' scales (r/60 to r/5, kr >> 1).  Other coefficient shapes h(U)|grad U|^2 (a
stiffness that switches off inside collapsed regions) are not covered.

Run from the repository root:  python3 real_research/dark_energy_2026/DE13_gate_gradient_repair.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np
import scipy.sparse as sp
import scipy.linalg as sl

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE13_gate_gradient_repair"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE13", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_LAMBDA_IN = (0.05, 2.0)                                         # R1, set before the first run


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
if MUTATE: P("\n  *** MUTATE=1: the repair's background term K0 is dropped; E1, E2 and E3 must FAIL ***")

# ---------------------------------------------------------------------------------- DE12's machinery, loaded unedited
P12 = os.path.join(HERE, "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_src = open(P12).read()
_head = _src.split("# ============================================================================================ C1 the amplification")[0]
_trans = _src.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]                                    # the definitions only (not C2's check)
_GRID_LINE = "r = np.geomspace(1.0, 2e4, 20000) * KPC"
assert _trans.count(_GRID_LINE) == 1
_trans_on = _trans.split("def transition(")[1].replace(_GRID_LINE, "r = rgrid")
_trans_on = "def transition_on(rgrid, " + _trans_on
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans + "\n" + _trans_on).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
transition, transition_on, Wd, G, MS, KPC, A0, CS, nu_of, FB = [D12[k] for k in (
    "transition", "transition_on", "Wd", "G", "MS", "KPC", "A0", "CS", "nu_of", "FB")]
C_LIGHT = D12["L52"]["c"]
R12 = json.load(open(os.path.join(HERE, "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]["budget"]
P(f"  DE12 machinery loaded   [{time.time() - T0:.0f}s]")
W_M = 0.25; TU = 1 / (2 * W_M)
CS2 = CS["1e6K"] ** 2
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
CLU = [(z, 1e14, f) for z in (0.25, 1.0, 2.5, 4.0) for f in ("canonical", "alt")]
LAMS = np.logspace(-3, 5, 33)
WINS = [(0.0, 0.5), (0.125, 0.625), (0.25, 0.75), (0.375, 0.875), (0.5, 1.0)]


def W3(t, d=1e-5):
    return (Wd(t + d)[2] - Wd(t - d)[2]) / (2 * d)


def layer_fine(z, Mb, foot, N=8000, tlo=0.004, thi=0.996):
    tr = transition(z, Mb, foot, W_M)
    r, t = tr["r"], tr["t"]
    if not ((t > 0) & (t < 1)).any():
        return None
    ri = float(np.interp(thi, t[::-1], r[::-1])); ro = float(np.interp(tlo, t[::-1], r[::-1]))   # t falls outward
    return transition_on(np.geomspace(ri, ro, N), z, Mb, foot, W_M)


def quad(trf, form, drop_K0=False):
    """the layer's radial second variation in eps = delta t: base (k^0, gate + gas), stiffness s, repair term K0."""
    r, t, rho, B = trf["r"], trf["t"], trf["rho_b"], trf["B"]
    _, W1, W2 = Wd(t)
    h = TU * 4 * math.pi * G * nu_of(trf["y"]) / (trf["H"] ** 2 * trf["xce"])
    U = (t - 0.5) * 2 * W_M + 1
    dU = np.gradient(U, r); d2U = np.gradient(dU, r)
    gt, lapt = TU * dU, TU * (d2U + 2 * dU / r)
    base = CS2 / (rho * h ** 2) - B * W2
    if form == "ii":
        s = W1 ** 2
        K0 = (W2 ** 2 + W1 * W3(t)) * gt ** 2 + 2 * W1 * W2 * lapt
    else:
        s = np.full_like(r, 1 / TU ** 2); K0 = np.zeros_like(r)
    if drop_K0:
        K0 = np.zeros_like(r)
    it = int(np.argmin(np.abs(t - 0.5)))
    return dict(r=r, t=t, base=base, s=s, K0=K0, unit=B[it] * r[it] ** 2, h=h, rho=rho, H=trf["H"])


def tri(r, base, s, K0, mu):
    """diag, off-diagonal of E2's matrix (interior nodes, Dirichlet ends)."""
    dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1]); sm = 0.5 * (s[1:] + s[:-1])
    wgt = np.zeros_like(r); wgt[1:] += 0.5 * dr; wgt[:-1] += 0.5 * dr
    off = mu * sm * rm ** 2 / dr
    diag = (base - mu * K0) * r ** 2 * wgt
    diag[1:] += off; diag[:-1] += off
    return diag[1:-1], -off[1:-1], r ** 2 * wgt


def neg_count(r, base, s, K0, mu):
    a, b, _ = tri(r, base, s, K0, mu)
    cnt, d = int(a[0] < 0), a[0]
    for i in range(1, len(a)):
        d = a[i] - b[i - 1] ** 2 / (d if d != 0 else 1e-300)
        cnt += d < 0
    return int(cnt)


def wcount(q, mu, win, base=None):
    m = (q["t"] >= win[0]) & (q["t"] <= win[1])
    bb = q["base"] if base is None else base
    return neg_count(q["r"][m], bb[m], q["s"][m], q["K0"][m], mu)


# ============================================================================================ C1 C2 controls
banner("C1 C2  CONTROLS: DE12's c_gate and DE12's transition on DE12's grid")
ly = transition(0.25, 1e11, "canonical", 0.25, amp=True)
_m = (ly["t"] > 0) & (ly["t"] < 1)
cmax = float(np.sqrt(np.max(np.maximum(ly["c_gate2"]["perp"], ly["c_gate2"]["par"])[_m])))
ref = R12["0.25/1e+11/canonical"]["c_gate_max"]
check("C1 CONTROL: the unrepaired c_gate reproduces DE12's committed value (z = 0.25, 1e11, canonical)",
      f"{cmax / 1e3:.3f} vs {ref / 1e3:.3f} km/s", abs(cmax / ref - 1) < 1e-12)
lyg = transition_on(np.geomspace(1.0, 2e4, 20000) * KPC, 0.25, 1e11, "canonical", 0.25, amp=True)
c2 = max(float(np.max(np.abs(lyg[k] - ly[k]))) for k in ("t", "rho_b", "B")) + \
    max(float(np.max(np.abs(lyg["c_gate2"][k] - ly["c_gate2"][k]))) for k in ("perp", "par"))
check("C2 CONTROL: transition() with the grid as an argument is DE12's on DE12's grid", f"max |diff| {c2:.1e}", c2 == 0.0)

# ============================================================================================ C3 finite-difference check
banner("C3  CONTROL: the second variation of 1/2 int |grad f|^2 against finite differences of the discretised functional")
trf = layer_fine(0.25, 1e11, "canonical", 6000)
q = quad(trf, "ii")
r, t = q["r"], q["t"]; dr = np.diff(r); rm = 0.5 * (r[1:] + r[:-1])
rng = np.random.default_rng(3)
rel_with, rel_without = [], []
for trial in range(3):
    c0, wd, kw = rng.uniform(0.15, 0.85), rng.uniform(0.02, 0.1), rng.uniform(5, 40)
    eps = np.exp(-((t - c0) / wd) ** 2) * np.cos(kw * t); eps[0] = eps[-1] = 0.0

    def Es(sc):
        f = Wd(t + sc * eps)[0]
        return 0.5 * np.sum(((f[1:] - f[:-1]) / dr) ** 2 * rm ** 2 * dr)
    sc = 1e-4
    fd = (Es(sc) + Es(-sc) - 2 * Es(0.0)) / sc ** 2

    def qform(K0):
        a, b, _ = tri(r, 0 * q["base"], q["s"], K0, 1.0)
        e = eps[1:-1]
        return float(np.sum(a * e ** 2) + 2 * np.sum(b * e[:-1] * e[1:]))
    rel_with.append(abs(qform(q["K0"]) / fd - 1)); rel_without.append(abs(qform(0 * q["K0"]) / fd - 1))
check("C3 CONTROL: stiffness + K0 matches the functional's finite-difference second variation (1e-4); without K0 it does not",
      f"with K0: {', '.join(f'{x:.1e}' for x in rel_with)}; without: {', '.join(f'{x:.1e}' for x in rel_without)}",
      max(rel_with) < 1e-4 and max(rel_without) >= 1e-3)

# ============================================================================================ C4 R1 E1 E2
banner("C4 R1 E1 E2  THE FORM (ii) REPAIR ON EVERY LAYER (w = 0.25, 1e6 K gas)")
ROWS, c4_unrep, c4_gas, e1_ok, e2_ok = {}, [], [], [], []
old = {}
for (z, Mb, foot) in GAL + CLU:
    key = f"{z}/{Mb:.0e}/{foot}"
    trf = layer_fine(z, Mb, foot)
    if trf is None:
        continue
    q = quad(trf, "ii", drop_K0=MUTATE)
    gas_only = CS2 / (q["rho"] * q["h"] ** 2)
    unrep = max(wcount(q, 0.0, wn) for wn in WINS)
    gas = max(wcount(q, 0.0, wn, base=gas_only) for wn in WINS)
    qrep = max(wcount(q, 1.0, wn, base=0 * q["base"]) for wn in WINS)
    half = [max(wcount(q, l ** 2 * q["unit"], wn) for wn in WINS) for l in LAMS]
    full = [neg_count(q["r"], q["base"], q["s"], q["K0"], l ** 2 * q["unit"]) for l in LAMS]
    ib = int(np.argmin(half))
    ROWS[key] = dict(unrepaired=unrep, gas_only=gas, Q_rep_neg=qrep, min_half=int(half[ib]), lam_best=float(LAMS[ib]),
                     min_full=int(min(full)), stable_lams=[float(l) for l, c in zip(LAMS, half) if c == 0])
    if Mb < 1e13:
        c4_unrep.append(unrep > 0); c4_gas.append(gas == 0); e1_ok.append(qrep > 0); e2_ok.append(min(half) > 0)
    st = ROWS[key]["stable_lams"]
    P(f"    {key:24s}: unrepaired {unrep:4d} modes; repair alone {qrep:3d}; best lambda {LAMS[ib]:.2g} leaves {half[ib]} "
      f"(full layer {min(full)}); stable lambda: {('%.3g-%.3g' % (min(st), max(st))) if st else 'none'}")
    # R1 as run in the first run: mu' k^2 >= c_gate^2 - c_s^2 at k = 1/L (the layer's width), the WKB stiffness only
    tr = transition(z, Mb, foot, W_M, amp=True)
    rr, tt = tr["r"], tr["t"]; mm = (tt > 0) & (tt < 1)
    L = float(rr[mm].max() - rr[mm].min())
    _, W1o, _ = Wd(tt)
    Urho = 4 * math.pi * G * nu_of(tr["y"]) / (tr["H"] ** 2 * tr["xce"])
    need = mm & (tr["c_gate2"]["perp"] > CS2)
    if need.any():
        ex = (tr["c_gate2"]["perp"] - CS2)[need]
        stifff = (tr["rho_b"] * (W1o * TU * Urho) ** 2)[need]
        with np.errstate(divide="ignore"):
            old[key] = float(np.max(np.sqrt(ex / (stifff * (1 / L) ** 2) / (tr["B"][need] * rr[need] ** 2))))
OUT["numbers"]["form_ii"] = ROWS
check("C4 CONTROL: without the repair every galaxy layer has negative modes; gas alone has none",
      f"unrepaired unstable on {sum(c4_unrep)}/{len(c4_unrep)}; gas alone stable on {sum(c4_gas)}/{len(c4_gas)}",
      all(c4_unrep) and all(c4_gas))
lam_gal = max(v for k, v in old.items() if "1e+14" not in k); lam_all = max(old.values())
OUT["numbers"]["R1_first_run_criterion"] = dict(lam_galaxies=lam_gal, lam_all=lam_all)
check("R1 [pre-declared, first run, kept as run] form (ii)'s lambda at k = 1/L (WKB stiffness only) lies in [0.05, 2]",
      f"lambda_galaxies = {lam_gal:.3f} (with the cluster: {lam_all:.3f})",
      EXPECT_LAMBDA_IN[0] <= lam_gal <= EXPECT_LAMBDA_IN[1],
      "superseded by E1/E2: the criterion had no K0 and asked for stiffness at the edges, where W'^2 -> 0")
check("E1 the repair's own second variation (form ii, gate and gas off) is indefinite on every galaxy layer, with a "
      "negative mode inside a half-layer window",
      f"indefinite on {sum(e1_ok)}/{len(e1_ok)} galaxy layers; negative modes per layer "
      f"{sorted(set(v['Q_rep_neg'] for k, v in ROWS.items() if '1e+14' not in k))}", all(e1_ok) and len(e1_ok) == len(GAL),
      "K0 grows with mu exactly as the stiffness does: more repair, more instability on scales longer than W's own")
check("E2 form (ii) stabilises no galaxy layer: for every lambda in 1e-3 to 1e5, some half-layer window keeps a negative mode",
      f"no stable lambda on {sum(e2_ok)}/{len(e2_ok)} galaxy layers; fewest modes left "
      f"{min(v['min_half'] for k, v in ROWS.items() if '1e+14' not in k)}-{max(v['min_half'] for k, v in ROWS.items() if '1e+14' not in k)}"
      f" at lambda {min(v['lam_best'] for k, v in ROWS.items() if '1e+14' not in k):.2g}-"
      f"{max(v['lam_best'] for k, v in ROWS.items() if '1e+14' not in k):.2g}",
      all(e2_ok) and len(e2_ok) == len(GAL), "a gradient energy on the gate cannot repair DE12's obstruction at any strength")

E3 = {}
for (z, Mb, foot) in GAL:
    q = quad(layer_fine(z, Mb, foot, 4000), "ii", drop_K0=MUTATE)
    m = (q["t"] >= WINS[0][0]) & (q["t"] <= WINS[0][1])
    aR, bR, wts = tri(q["r"][m], 0 * q["base"][m], q["s"][m], q["K0"][m], 1.0)
    aG, bG, _ = tri(q["r"][m], q["base"][m], q["s"][m], 0 * q["K0"][m], 0.0)
    Rm = np.diag(aR) + np.diag(bR, 1) + np.diag(bR, -1)
    Gm = np.diag(aG) + np.diag(bG, 1) + np.diag(bG, -1)
    ev, V = sl.eigh(Rm, np.diag(wts[1:-1]), subset_by_index=[0, 0])
    v = V[:, 0]
    Rv, Gv = float(v @ Rm @ v), float(v @ Gm @ v)
    tv = float(np.sum(q["t"][m][1:-1] * v ** 2) / np.sum(v ** 2))
    E3[f"{z}/{Mb:.0e}/{foot}"] = dict(R=Rv, G=Gv, t_mean=tv, both_negative=bool(Rv < 0 and Gv < 0))
OUT["numbers"]["E3"] = E3
nb = sum(v["both_negative"] for v in E3.values())
check("E3 one direction is destabilised by the gate and gas AND by the repair on every galaxy layer: unstable for every mu >= 0",
      f"{nb}/{len(E3)} layers; the direction sits at t ~ {min(v['t_mean'] for v in E3.values()):.3f}-"
      f"{max(v['t_mean'] for v in E3.values()):.3f} (the outer, convex half)", nb == len(GAL),
      "G + mu R < 0 for all mu >= 0 when G < 0 and R <= 0 (Lean DE13.no_mu_stabilises)")


# ============================================================================================ G1 growth
banner("G1  THE RESIDUAL MODES' GROWTH (displacement formulation, mass conserved)")


def growth(z, Mb, foot, lam, N):
    trf = layer_fine(z, Mb, foot, N)
    q = quad(trf, "ii", drop_K0=MUTATE)
    r = q["r"]; a, b, _ = tri(r, q["base"], q["s"], q["K0"], lam ** 2 * q["unit"])
    n = len(a)
    Ke = sp.diags([a, b, b], [0, 1, -1], format="csr")
    Hh = sp.diags(q["h"][1:-1])
    ri = r[1:-1]; rh = 0.5 * (r[:-1] + r[1:]); rhoh = 0.5 * (q["rho"][:-1] + q["rho"][1:]); drh = np.diff(r)
    dri = 0.5 * (drh[:-1] + drh[1:])
    # xi on the N-1 half points; delta rho_i = -(rh^2 rho xi)_{i+1/2} - (rh^2 rho xi)_{i-1/2}) / (r_i^2 dr_i)
    rows = np.repeat(np.arange(n), 2); cols = np.stack([np.arange(n), np.arange(n) + 1], 1).ravel()
    vals = np.stack([rh[:-1] ** 2 * rhoh[:-1] / (ri ** 2 * dri), -rh[1:] ** 2 * rhoh[1:] / (ri ** 2 * dri)], 1).ravel()
    D = sp.csr_matrix((vals, (rows, cols)), shape=(n, n + 1))
    Kx = (D.T @ Hh @ Ke @ Hh @ D).tocsr()
    mi = 1 / np.sqrt(rhoh * rh ** 2 * drh)
    S = (sp.diags(mi) @ Kx @ sp.diags(mi)).todia()
    ab = np.zeros((3, n + 1))
    for k in range(3):
        dk = S.diagonal(k)
        ab[2 - k, k:] = dk
    ev = sl.eig_banded(ab, lower=False, eigvals_only=True, select="i", select_range=(0, 2))
    return ev, q["H"]


G1 = {}
for (z, Mb, foot) in [(0.25, 1e11, "canonical"), (4.0, 1e11, "alt")]:
    key = f"{z}/{Mb:.0e}/{foot}"
    lb = ROWS[key]["lam_best"]
    row = {}
    for N in (1500, 3000):
        ev, H = growth(z, Mb, foot, lb, N)
        row[N] = math.sqrt(-ev[0]) / H if ev[0] < 0 else 0.0
    ev0, H = growth(z, Mb, foot, 0.0, 3000)
    row["unrepaired_N3000"] = math.sqrt(-ev0[0]) / H if ev0[0] < 0 else 0.0
    G1[key] = dict(lam=lb, **{str(k): v for k, v in row.items()})
    P(f"    {key}: at lambda {lb:.2g} the fastest mode grows at Gamma/H = {row[1500]:.2e} (N 1500), {row[3000]:.2e} (N 3000); "
      f"unrepaired (grid-limited, Gamma ~ k): {row['unrepaired_N3000']:.2e}")
OUT["numbers"]["G1"] = G1
check("G1 (reported) the residual modes' growth at the best lambda (Gamma/H), 1500 and 3000 points", G1, True, load_bearing=False)

# ============================================================================================ F1 N1 form (i)
banner("F1 N1  FORM (i): the smallest mu_U that stabilises each layer, and its own potential")
F1 = {}
for (z, Mb, foot) in GAL + CLU:
    trf = layer_fine(z, Mb, foot)
    if trf is None:
        continue
    q = quad(trf, "i")
    lo, hi = -8.0, 8.0                                                   # log10 of mu in units of B r^2 at t = 1/2
    if max(wcount(q, 10 ** hi * q["unit"], wn) for wn in WINS) > 0:
        F1[f"{z}/{Mb:.0e}/{foot}"] = None; continue
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if max(wcount(q, 10 ** mid * q["unit"], wn) for wn in WINS) > 0: lo = mid
        else: hi = mid
    mu = 10 ** hi * q["unit"]
    F1[f"{z}/{Mb:.0e}/{foot}"] = dict(mu_U=mu, lam_U=math.sqrt(10 ** hi), eta_U=8 * math.pi * G * mu / C_LIGHT ** 4)
galF = {k: v for k, v in F1.items() if v is not None and "1e+14" not in k}
muU = max(v["mu_U"] for v in galF.values())
etaU = 8 * math.pi * G * muU / C_LIGHT ** 4
P("    lambda_U = sqrt(mu_U/(B r^2)) per galaxy layer: " + ", ".join(f"{k}: {v['lam_U']:.2f}" for k, v in galF.items()))
P(f"    universal (galaxies) mu_U: eta_U = {etaU:.2e};  clusters: " +
  ", ".join(f"{k}: eta_U {v['eta_U']:.1e}" for k, v in F1.items() if v is not None and "1e+14" in k))
OUT["numbers"]["F1"] = dict(rows=F1, eta_U_galaxies=etaU)
check("F1 (reported) form (i) stabilises every layer above a minimum mu_U (half-layer windows)",
      f"stabilised {len([v for v in F1.values() if v is not None])}/{len(F1)}; lambda_U "
      f"{min(v['lam_U'] for v in galF.values()):.2f}-{max(v['lam_U'] for v in galF.values()):.2f}; eta_U = {etaU:.2e}", True,
      load_bearing=False)
R3U = {}
for lab, (z, Mb, rq) in {"flagship r_F, z = 2.5, 1e11": (2.5, 1e11, None), "the Sun, z = 0, 6e10 at 8 kpc": (0.0, 6e10, 8.0)}.items():
    tr = transition(z, Mb, "canonical", W_M, amp=True)
    r = tr["r"]; y = tr["y"]
    rho_ph = Mb * MS * (D12["h_of"](y) - y * D12["dh_of"](y)) / (2 * math.pi * r ** 3 * y)
    C = 1 / (tr["H"] ** 2 * tr["xce"])
    U = 4 * math.pi * G * (tr["rho_b"] + rho_ph) * C
    lapU = np.gradient(r ** 2 * np.gradient(U, r), r) / r ** 2
    PhiU = -4 * math.pi * G * muU * lapU * C                            # A = 1: a lower bound on the response
    rr_q = math.sqrt(G * Mb * MS / (0.1 * A0["canonical"])) if rq is None else rq * KPC
    R3U[lab] = float(abs(np.interp(rr_q, r, PhiU)) / tr["vf2"])
OUT["numbers"]["form_i_cost"] = R3U
check("N1 form (i)'s own potential, taken with the smallest universal mu_U, exceeds v_f^2 at r_F and at the Sun's distance",
      "; ".join(f"{k}: {v:.2e} v_f^2" for k, v in R3U.items()), all(v > 1.0 for v in R3U.values()),
      "the term acts wherever U varies: inside every galaxy (and, on smaller scales still, at every stellar surface)")

# ============================================================================================ R3 form (ii)'s edge potential
banner("R3  FORM (ii)'s EDGE POTENTIAL per lambda^2 (the review's question on the edge profile)")
R3 = {}
for z in (0.25, 2.5, 4.0):
    for Mb in (1e10, 1e11, 1e12):
        tr = transition(z, Mb, "canonical", W_M, amp=True)
        r, tt = tr["r"], tr["t"]; mm = (tt > 0) & (tt < 1)
        f, W1o, _ = Wd(tt)
        lapf = np.gradient(r ** 2 * np.gradient(f, r), r) / r ** 2
        it = int(np.argmin(np.abs(tt - 0.5)))
        muf = tr["B"][it] * r[it] ** 2                                    # lambda = 1
        Phif = -4 * math.pi * G * muf * lapf * W1o * TU / (tr["H"] ** 2 * tr["xce"])
        R3[f"{z}/{Mb:.0e}"] = float(np.max(np.abs(Phif[mm])) / tr["vf2"])
P("    max |Phi_f|/v_f^2 at lambda = 1: " + ", ".join(f"{k}: {v:.2f}" for k, v in R3.items()))
OUT["numbers"]["form_ii_edge_potential_per_lambda2"] = R3
check("R3 (reported) form (ii)'s edge potential at lambda = 1, max over the layer", f"{min(R3.values()):.2f}-{max(R3.values()):.2f} v_f^2",
      True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
