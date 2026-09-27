#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18b (4 of 4) -- A DE12-TYPE SECOND VARIATION OF H_K1 ON GALAXY BACKGROUNDS (item 5 of the re-audit: XR18's B1-B3 re-run for
H_K1, with the <K>_h channel that XR18b_symbol_channel derives written into the WKB count).

WHY.  DE12 showed that a local region gate, varied as an action term, is a k^0 negative bulk modulus on edge-layer gas (c_gate
1500-3700 km/s, 2e3-5e4 H at k = 1/kpc).  XR18 (B1-B3) found no such term in FP9's H_Y: its separators read first derivatives
and leaf averages only, DE12's convention gives zero growth on all 24 hosts, and the exact radial gas sector around each yield
surface is bounded (<= 31 H) and converged.  H_K1 differs from H_Y in two ways that matter here: (i) its leaf-average channel is
now a derived local operator, C a^3 [3 H A^2 - 9 H A zeta - 3 A zeta' + 9 zeta zeta' + a^-2 A lap beta] (XR18b_symbol_channel S2),
and (ii) it has NO yield below z_q0, so on an isolated host at z = 0.25 the band-passed field falls to 1e-24 a0 in the far field
(the Gaussian band-pass removes the host's monopole beyond ~3 L) and nothing plugs it.

PRE-DECLARED HYPOTHESES (written into this file before its first full run; exploratory runs disclosed in XR18b_README.md: DE12's
convention run on H_K1's 24 hosts -- 4e4-1.4e5 H at z = 0.25, located at r = 10-14 Mpc where the isolated host's y_bp is
1e-24-1e-22, and 0 at z >= 1 -- made before this file existed; H1 and H2 below are written knowing it)
 H1 [load-bearing] NO k^0 TERM IN THE FULL H_K1 ACTION: XR18's WKB engine (its own text, extracted) with the <K>_h channel's
    derived operator added (A = dPhi/c^2, zeta = -dPhi/c^2, zeta' = Gamma zeta, a^-2 lap beta = 3 (zeta' - H A) from the CMC
    condition) finds no k^0 coefficient except the gas's own c_s^2/(2 rho); the channel is O(k^-4).  MUTATE's DE12 gate must fail.
 H2 [load-bearing; EXPECTED TO FAIL at z = 0.25 on the exploratory run -- kept exactly as XR18 declared it] DE12's CONVENTION ON
    THE ISOLATED HOSTS: Gamma(1/kpc)/H = 0 for 1e6 K gas over the whole profile 1 kpc - 20 Mpc on all 24 hosts.
 H2w [load-bearing] THE SAME HOSTS EMBEDDED IN THE WEB: with the host's band-passed field combined with the web's own band-passed
    rms field (y_eff = (y_bp^2 + y_web^2)^(1/2), y_web = H_K1's band-passed NL rms at that z, the field the far field of any
    real host sits in), Gamma(1/kpc)/H = 0 for 1e6 K gas on all 24 hosts.
 H2z [load-bearing] AT THE ZEROS OF THE BAND-PASSED FIELD (below z_q0, unplugged): with the susceptibility window-averaged over
    1 kpc around an isotropic zero (Q''_win = (3/5)/sqrt(s x 1 kpc)), 1e6 K gas at k = 1/kpc does not grow at the web's zeros
    (s = y_rms/L, mean density) nor at cored centres (1e2-1e6 rho_bar, gas f_b x that); the 1e5 K rates are printed next to
    Newton's.
 H3 [load-bearing] THE EXACT RADIAL GAS SECTOR AROUND H_K1's YIELD SURFACES (z = 0.7, 0.8, 1, 2.5, 4; 30 hosts; 1e6 K and 1e5 K):
    the maximum growth rate is converged under grid doubling (< 5%) and under the regularised yield (eps/sqrt(y_th) = 1e-3,
    1e-4: < 5%), and the yield raises it over plain band-passed P2 on the same domain by less than x2 (XR18 H3 verbatim).
The writer's expectation: H1, H2w, H2z, H3 pass; H2 fails at z = 0.25 (the isolated host's exponentially vanishing band-passed
field, which H_K1 does not plug below z_q0 -- a real property of the separator on an isolated host, not of the web).

CHECKS
  K1 CONTROL: the WKB engine given DE12's gate term returns DE12's S identically (sympy), and on DE12's own profiles reproduces
     DE12's committed c_gate_max and Gamma(1/kpc)/H on all 24 layers (XR18 K1's recipe).
  K2 CONTROL: XR18's committed B2 (H_Y, 24 hosts: Gamma(1/kpc)/H at 1e6 and 1e5 K, max window-averaged Q'') and B3 (H_Y base rates,
     1e6 K) reproduced with XR18's own radial functions (text extracted).
  B1 = H1.  B2 = H2.  B2w = H2w.  B2z = H2z.  B3 = H3.
  B3r (reported) the radial gas sector at z = 0.25 (no yield) on [1 kpc, 3 L] and on [1 kpc, 20 Mpc], isolated and embedded.
MUTATE=1 inserts DE12's local density-read gate (XR18's MUTATE): B1, B2w and B3 must FAIL (rc = 1).

SCOPE.  Frozen backgrounds (DE12's 24 hosts: point-mass baryons for the MOND field, gas f_b (rho_NFW + rho_bar)), the planar
WKB count for the order statement, the l = 0 sector exact; the web embedding is a bracket (the web's field direction is
random; its magnitude is added in quadrature).  At most 2 threads.  kappa = 1/2 is FITTED (Z = 5.7888); nothing here derives
it, and nothing here closes the theory.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18b_second_variation.py
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from scipy.linalg import eigh
import XR18b_common as XC

L = XC.Lane("XR18b_second_variation", "XR18b/second_variation")
P, check, banner = L.P, L.check, L.banner
MUT = L.mutate
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: DE12's local density-read gate is inserted into H_K1 -- B1, B2w and B3 must FAIL ***")

# ================================================================================================ machinery (read-only)
NS9, D12 = XC.load_base()
M6 = NS9["M6"]; A0 = dict(NS9["A0"]); FOOTS = ("canonical", "alt")
x_P2 = NS9["x_P2"]; gfrac = M6["gfrac_smooth"]; G6 = M6["G6"]; MPCm = M6["MPCm"]
KPC, MS, CS, transition, Wd = D12["KPC"], D12["MS"], D12["CS"], D12["transition"], D12["Wd"]
nu_of, ynup_of, G12 = D12["nu_of"], D12["ynup_of"], D12["G"]
XRSV = os.path.join(XC.HERE, "XR18_second_variation.py")
xns = dict(np=np, math=math, eigh=eigh, x_P2=x_P2, L_phys=NS9["L_phys"], y_th_z=NS9["y_th_z"], gfrac=gfrac,
           shell_frac=M6["shell_frac"], MPCm=MPCm, G6=G6, transition=transition, KPC=KPC, MS=MS, A0=A0,
           LLh=NS9["LL_of"](1.3, 2.0), FLh=(1e-6, 4.0, NS9["YIELD"]), Z_N=2.0)
exec(XC.extract_defs(XRSV, ["hy_host", "x_yield", "cum_Q2", "r_yield", "radial_operator", "growth", "host_grid", "node_Q2w"]), xns)
hy_host_HY = xns["hy_host"]
HK = XC.hk1_forms(M6, A0)
R12 = json.load(open(os.path.join(XC.DE, "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]
R18 = json.load(open(os.path.join(XC.HERE, "XR18_second_variation_results.json")))["numbers"]
NSf = XC.load_fp19()
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
P(f"\n  machinery: FP9 (FP6 inside), DE12's host definitions and FP19 exec'd read-only; XR18's WKB engine and radial functions "
  f"extracted as text; a0 = {A0['canonical']:.4e} / {A0['alt']:.4e}   {L.el()}")


def hk1_host(z, Mb, foot, r):
    a0 = A0[foot]; Lz = HK["L_of"](z) * MPCm; yth = HK["yth_of"](z, foot)
    yN = G6 * Mb * MS / (r ** 2 * a0)
    return dict(yN=yN, ybp=yN * (1 - gfrac(r / Lz)), yth=yth, L=Lz, a0=a0)


def y_web(z, foot):
    a = 1 / (1 + z); i = int(np.argmin(np.abs(NSf["AGR"] - a)))
    return float(NSf["rms_bp_L"](i, [NSf["LK_head"](a)], A0[foot])[0])


# ================================================================================================ the WKB engine (XR18's own text)
banner("K1 B1  THE WKB ORDER COUNT OF THE FULL H_K1 ACTION (XR18's engine, extracted), DE12's gate as the control")
src = open(XRSV).read()
blk = src[src.index("k, h, Gs, rho, cs, Cth, GNG, ac, lam, Gam,"): src.index("\nrows = []")]
wns = {"sp": sp, "MUTATE": MUT}
exec(blk, wns)
k, Gs, rho, cs, cl, Gam, dPhi = wns["k"], wns["Gs"], wns["rho"], wns["cs"], wns["cl"], wns["Gam"], wns["dPhi"]
Cch, Hs = sp.symbols("C_K H", positive=True)
A_ = dPhi / cl ** 2; zeta_ = -dPhi / cl ** 2; zdot = Gam * zeta_; lapb = 3 * (zdot - Hs * A_)
USE = dict(wns["USE"])
USE["H_K1's <K>_h channel: C [3H A^2 - 9H A zeta - 3 A zeta' + A a^-2 lap beta + 9 zeta zeta'] (XR18b S2; CMC shift)"] = \
    Cch * (3 * Hs * A_ ** 2 - 9 * Hs * A_ * zeta_ - 3 * A_ * zdot + A_ * lapb + 9 * zeta_ * zdot)
rows = []; k0_total = sp.Integer(0)
for nm, ex in USE.items():
    order, k0 = wns["k_order"](ex)
    rows.append((nm, order, k0)); k0_total += k0
k0_total = sp.simplify(k0_total)
for nm, order, k0 in rows:
    P(f"    {nm[:112]:112s} leading k-order {str(order):>4s}; k^0 coefficient {k0}")
# K1: the gate term through the engine = DE12's S; DE12's committed numbers on its own profiles
GT = wns["GATE_TERM"]; Bg, W1s, W2s, tU, Umax, Urr, A_expr = wns["Bg"], wns["W1s"], wns["W2s"], wns["tU"], wns["Umax"], wns["Urr"], wns["A_expr"]
order_g, k0_g = wns["k_order"](GT[1])
k1_sym = sp.simplify(-2 * k0_g - Bg * (W2s * tU ** 2 * (Umax * A_expr) ** 2 + W1s * tU * Urr)) == 0 and order_g == 0
Aamp = sp.Symbol("A", real=True)
S_fun = sp.lambdify((Bg, W1s, W2s, tU, Umax, Aamp, Urr), Bg * (W2s * tU ** 2 * (Umax * Aamp) ** 2 + W1s * tU * Urr), "numpy")
k1dev = 0.0
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    m = (tr["t"] > 0) & (tr["t"] < 1)
    _, W1, W2 = Wd(tr["t"])
    Umx = 4 * math.pi * G12 / (tr["H"] ** 2 * tr["xce"])
    Sper = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]), 0.0)
    Spar = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
    cg = np.sqrt(np.maximum(tr["rho_b"] * np.maximum(Sper, 0), tr["rho_b"] * np.maximum(Spar, 0)))
    cmax = float(np.max(cg[m])); gam = (1 / KPC) * math.sqrt(max(cmax ** 2 - CS["1e6K"] ** 2, 0.0)) / tr["H"]
    ref = R12["budget"][KEY(z, Mb, f)]
    k1dev = max(k1dev, abs(cmax / ref["c_gate_max"] - 1), abs(gam / ref["Gamma_over_H"] - 1))
check("K1 CONTROL (DE12): XR18's WKB engine (its own text) given DE12's gate returns DE12's S = B[W'' t_U^2 U_rho^2 + W' t_U U_rhorho] "
      "identically, and DE12's committed c_gate_max and Gamma(1/kpc)/H on all 24 layers are reproduced",
      f"symbolic identity {k1_sym}; max relative deviation {k1dev:.1e}", k1_sym and k1dev <= 1e-12)
chan = [(nm, order, k0) for nm, order, k0 in rows if nm.startswith("H_K1's")][0]
b1_gas = sp.simplify(k0_total - cs ** 2 / (2 * rho)) == 0
others = [nm for nm, order, k0 in rows if k0 != 0 and not nm.startswith("gas")]
check("B1 [H1, pre-declared] NO k^0 TERM IN THE FULL H_K1 ACTION: with the <K>_h channel's derived operator added, every term's second "
      "variation is O(k^-1) or smaller except the gas's own c_s^2/(2 rho); the channel is O(k^-4)",
      f"k^0 total {k0_total} (gas only: {b1_gas}); other k^0 terms: {others or 'none'}; channel order {chan[1]}",
      b1_gas and not others and chan[1] == -4,
      "the <K>_h channel reads the metric's expansion and volume, (v/c)^2 relative to the Newtonian terms; DE12's obstruction needs a "
      "read of a second derivative of a constraint-slaved potential, which H_K1 does not have")
L.out["numbers"]["B1"] = {"rows": [(nm, str(o), str(c)) for nm, o, c in rows], "k0_total": str(k0_total)}
P(f"    {L.el()}")

# ================================================================================================ K2 XR18's B2/B3 on H_Y
banner("K2  CONTROL: XR18's committed B2 and B3 (H_Y) with XR18's own radial functions")
kW = 1 / KPC


def b2_host(z, Mb, f, hostfun, yw=0.0, T="1e6K", gate=False):
    tr = transition(z, Mb, f, 0.25)
    r = tr["r"]; H = tr["H"]
    bg = hostfun(z, Mb, f, r)
    yfun = (lambda rr_: hostfun(z, Mb, f, rr_)["ybp"]) if yw == 0 else (lambda rr_: np.sqrt(hostfun(z, Mb, f, rr_)["ybp"] ** 2 + yw ** 2))
    hk = 1 - math.exp(-0.5 * (kW * bg["L"]) ** 2)
    X = xns["cum_Q2"](r, yfun, bg["yth"])
    Qwin = (np.interp(r + 0.5 / kW, r, X) - np.interp(r - 0.5 / kW, r, X)) * kW
    g2 = 4 * math.pi * G6 * tr["rho_b"] * (1 + hk ** 2 * Qwin) - CS[T] ** 2 * kW ** 2
    if gate:
        _, W1, W2 = Wd(tr["t"])
        Umx = 4 * math.pi * G12 / (H ** 2 * tr["xce"])
        Spar = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
        Sper = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]), 0.0)
        g2 = g2 + tr["rho_b"] * np.maximum(np.maximum(Spar, Sper), 0) * kW ** 2
    j = int(np.argmax(g2))
    return float(np.sqrt(max(np.max(g2), 0.0))) / H, float(np.max(Qwin)), float(r[j] / KPC), float(yfun(np.array([r[j]]))[0])


k2dev = 0.0
for (z, Mb, f) in GAL:
    g6, qw, _, _ = b2_host(z, Mb, f, hy_host_HY)
    g5, _, _, _ = b2_host(z, Mb, f, hy_host_HY, T="1e5K")
    ref = R18["B2"][KEY(z, Mb, f)]
    k2dev = max(k2dev, abs(g6 - ref["Gamma_over_H"]), abs(g5 - ref["Gamma_1e5K"]) / max(ref["Gamma_1e5K"], 1e-300) if ref["Gamma_1e5K"] > 0 else abs(g5),
                abs(qw / ref["Qwin_max"] - 1))


def b3_rates(z, Mb, f, hostfun, T, tag, gate=False):
    xns["hy_host"] = hostfun
    N, Ng, eps_r, plain = {"base": (300, 120, 0.0, False), "fine": (600, 240, 0.0, False), "eps1e-3": (300, 120, 1e-3, False),
                           "eps1e-4": (300, 120, 1e-4, False), "plainP2": (300, 120, 0.0, True)}[tag]
    r, rho, rY, tr = xns["host_grid"](z, Mb, f, N=N, Ng=Ng)
    Q2w, bg = xns["node_Q2w"](r, z, Mb, f, eps=eps_r * math.sqrt(max(bg_yth(z, f, hostfun), 1e-300)), plain=plain)
    gS = None
    if gate:
        rc = 0.5 * (r[1:] + r[:-1]); _, W1, W2 = Wd(tr["t"])
        Umx = 4 * math.pi * G12 / (tr["H"] ** 2 * tr["xce"])
        Sg = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
        gS = np.maximum(np.interp(rc, tr["r"], Sg), 0.0)
    K, Mm = xns["radial_operator"](r, rho, Q2w, CS[T] ** 2, bg["L"], gate_S=gS)
    return xns["growth"](K, Mm) / tr["H"], rY


def bg_yth(z, f, hostfun):
    return hostfun(z, 1e11, f, np.array([1.0]))["yth"]


for (z, Mb, f) in GAL[:6]:
    v, _ = b3_rates(z, Mb, f, hy_host_HY, "1e6K", "base")
    k2dev = max(k2dev, abs(v / R18["B3"][KEY(z, Mb, f)]["1e6K"]["base"] - 1) if R18["B3"][KEY(z, Mb, f)]["1e6K"]["base"] > 0 else abs(v))
check("K2 CONTROL: XR18's committed B2 (H_Y: Gamma(1/kpc)/H at 1e6 K and 1e5 K, max window-averaged Q'', 24 hosts) and B3 base rates "
      "(1e6 K, the z = 0.25 hosts) reproduced with XR18's own radial functions", f"max deviation {k2dev:.1e}", k2dev <= 1e-9)
P(f"    {L.el()}")

# ================================================================================================ B2 DE12's convention, isolated hosts
banner("B2  DE12's CONVENTION ON H_K1's 24 ISOLATED HOSTS: Gamma(1/kpc)/H for 1e6 K gas, whole profile 1 kpc - 20 Mpc")
b2, b2w = {}, {}
for (z, Mb, f) in GAL:
    g, qw, rmax, yat = b2_host(z, Mb, f, hk1_host, gate=MUT)
    b2[KEY(z, Mb, f)] = dict(Gamma_over_H=g, Qwin_max=qw, r_kpc=rmax, y_there=yat)
    yw = y_web(z, f)
    gw, qww, rw, yw_at = b2_host(z, Mb, f, hk1_host, yw=yw, gate=MUT)
    gw5, _, _, _ = b2_host(z, Mb, f, hk1_host, yw=yw, T="1e5K", gate=MUT)
    b2w[KEY(z, Mb, f)] = dict(Gamma_over_H=gw, Gamma_1e5K=gw5, Qwin_max=qww, y_web=yw)
    P(f"    {KEY(z, Mb, f):22s}: isolated Gamma/H {g:9.3g} (max Q''_win {qw:.2e} at r = {rmax:7.0f} kpc, y_bp there {yat:.1e}) | embedded (y_web "
      f"{yw:.2e}): Gamma/H {gw:.3g} at 1e6 K, {gw5:.3g} at 1e5 K; max Q''_win {qww:.3g}")
g2max = max(v["Gamma_over_H"] for v in b2.values())
fail_hosts = [k_ for k_, v in b2.items() if v["Gamma_over_H"] > 0]
check("B2 [H2, pre-declared as XR18 declared it; EXPECTED to fail at z = 0.25] DE12's CONVENTION ON THE ISOLATED HOSTS: Gamma(1/kpc)/H = 0 "
      "for 1e6 K gas over 1 kpc - 20 Mpc on all 24 hosts",
      f"max Gamma/H {g2max:.3g}; hosts with growth: {len(fail_hosts)} ({', '.join(sorted({k_.split('/')[0] for k_ in fail_hosts})) or 'none'}); "
      f"where: r = {min((b2[k_]['r_kpc'] for k_ in fail_hosts), default=0):.0f}-{max((b2[k_]['r_kpc'] for k_ in fail_hosts), default=0):.0f} kpc, y_bp "
      f"{min((b2[k_]['y_there'] for k_ in fail_hosts), default=0):.0e}-{max((b2[k_]['y_there'] for k_ in fail_hosts), default=0):.0e}", g2max == 0.0,
      "below z_q0 H_K1 has no yield, so the isolated host's far field, where the Gaussian band-pass has removed the monopole "
      "(y_bp ~ 1e-24), carries an unbounded P2 susceptibility dx/dy ~ y^(-1/2) and gas is linearly unstable there at 1/kpc; under H_Y "
      "the yield plugged it")
b2w_max = max(v["Gamma_over_H"] for v in b2w.values())
check("B2w [H2w, pre-declared] THE SAME HOSTS EMBEDDED IN THE WEB (y_eff = (y_bp^2 + y_web^2)^(1/2), y_web = H_K1's band-passed NL rms): "
      "Gamma(1/kpc)/H = 0 for 1e6 K gas on all 24 hosts",
      f"max Gamma/H (1e6 K) {b2w_max:.3g}; 1e5 K (reported) max {max(v['Gamma_1e5K'] for v in b2w.values()):.3g}; max Q''_win "
      f"{max(v['Qwin_max'] for v in b2w.values()):.3g}", b2w_max == 0.0,
      "the B2 growth lives only where the host's own band-passed field is below the web's by 20 orders of magnitude; a real host's far "
      "field sits in the web's field, whose susceptibility is <= 1/(2 sqrt(y_web)) ~ 5")
L.out["numbers"]["B2"] = b2; L.out["numbers"]["B2w"] = b2w

# ================================================================================================ B2z at the zeros
banner("B2z  AT THE ZEROS OF THE BAND-PASSED FIELD BELOW z_q0: gas at k = 1/kpc with the window-averaged susceptibility")
b2z = {}
for f in FOOTS:
    for z in (0.0, 0.25, 0.5):
        a = 1 / (1 + z); Lp = NSf["LK_head"](a) * MPCm; yw = y_web(z, f)
        rho_bar = M6["Om"] * M6["rho_crit0"] / a ** 3; FB = 0.02237 / (0.02237 + 0.1200)
        Hz = D12["Hz"](z)
        cases = {"web zero (mean density)": (yw / Lp, rho_bar)}
        for dens in (1e2, 1e4, 1e6):
            cases[f"cored centre {dens:.0e} rho_bar"] = ((4 * math.pi / 3) * G6 * dens * rho_bar / A0[f], dens * rho_bar)
        for lab, (s, rho_loc) in cases.items():
            Qw = 0.6 / math.sqrt(s * KPC)
            rho_g = FB * rho_loc
            gate_add = 0.0
            out = {}
            for T in ("1e6K", "1e5K"):
                g2m = 4 * math.pi * G6 * rho_g * (1 + Qw) - CS[T] ** 2 * kW ** 2
                g2n = 4 * math.pi * G6 * rho_g - CS[T] ** 2 * kW ** 2
                out[T] = (math.sqrt(max(g2m, 0.0)) / Hz, math.sqrt(max(g2n, 0.0)) / Hz)
            b2z[(f, z, lab)] = dict(s=s, Qwin=Qw, **{f"{T}": v for T, v in out.items()})
for (f, z, lab), v in b2z.items():
    if f == "canonical":
        P(f"    z = {z} {lab:28s}: s = {v['s']:.2e}/m, Q''_win(1 kpc) {v['Qwin']:.3g}; Gamma/H 1e6 K {v['1e6K'][0]:.3g} (Newton {v['1e6K'][1]:.3g}); "
          f"1e5 K {v['1e5K'][0]:.3g} (Newton {v['1e5K'][1]:.3g})")
b2z_ok = all(v["1e6K"][0] == 0.0 for v in b2z.values())
check("B2z [H2z, pre-declared] AT THE UNPLUGGED ZEROS BELOW z_q0: 1e6 K gas at k = 1/kpc, with the susceptibility window-averaged over "
      "1 kpc around an isotropic zero, does not grow at the web's zeros (mean density) or at cored centres (1e2-1e6 rho_bar)",
      f"max Gamma/H at 1e6 K {max(v['1e6K'][0] for v in b2z.values()):.3g}; 1e5 K (reported): max {max(v['1e5K'][0] for v in b2z.values()):.3g} "
      f"(Newton alone {max(v['1e5K'][1] for v in b2z.values()):.3g})", b2z_ok)
L.out["numbers"]["B2z"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in b2z.items()}
P(f"    {L.el()}")

# ================================================================================================ B3 the exact radial gas sector
banner("B3  THE EXACT RADIAL GAS SECTOR AROUND H_K1's YIELD SURFACES (z = 0.7-4), gas at 1e6 K and 1e5 K")
GALY = [(z, Mb, f) for z in (0.7, 0.8, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
b3 = {}
for (z, Mb, f) in GALY:
    row = {}
    for T in ("1e6K", "1e5K"):
        res = {}
        for tag in ("base", "fine", "eps1e-3", "eps1e-4", "plainP2"):
            res[tag], rY = b3_rates(z, Mb, f, hk1_host, T, tag, gate=MUT)
        cg = abs(res["fine"] / res["base"] - 1) if res["base"] > 0 else (0.0 if res["fine"] == 0 else 1.0)
        ce = max(abs(res["eps1e-3"] / res["base"] - 1), abs(res["eps1e-4"] / res["base"] - 1)) if res["base"] > 0 else 0.0
        ratio = res["base"] / res["plainP2"] if res["plainP2"] > 0 else (0.0 if res["base"] == 0 else float("inf"))
        row[T] = dict(res, conv_grid=cg, conv_eps=ce, ratio_vs_P2=ratio, r_Y_kpc=rY / KPC)
    b3[KEY(z, Mb, f)] = row
    v6, v5 = row["1e6K"], row["1e5K"]
    P(f"    {KEY(z, Mb, f):22s} r_Y {v6['r_Y_kpc']:7.1f} kpc | 1e6 K: H_K1 {v6['base']:.3g} (fine {v6['fine']:.3g}, eps {v6['eps1e-3']:.3g}/{v6['eps1e-4']:.3g}), "
      f"plain P2 {v6['plainP2']:.3g} | 1e5 K: H_K1 {v5['base']:.3g} (fine {v5['fine']:.3g}), plain P2 {v5['plainP2']:.3g}  [Gamma/H]")
cgm = max(v[T]["conv_grid"] for v in b3.values() for T in v); cem = max(v[T]["conv_eps"] for v in b3.values() for T in v)
rtm = max(v[T]["ratio_vs_P2"] for v in b3.values() for T in v); gm3 = max(v[T]["base"] for v in b3.values() for T in v)
check("B3 [H3, pre-declared] THE EXACT RADIAL GAS SECTOR AROUND H_K1's YIELD SURFACES (30 hosts at z = 0.7-4, 1e6 K and 1e5 K): the maximum "
      "growth is converged under grid doubling (< 5%) and under the regularised yield (< 5%), and the yield raises it over plain "
      "band-passed P2 on the same domain by less than x2",
      f"max grid change {cgm:.1%}; max eps change {cem:.1%}; max H_K1/plain-P2 {rtm:.2f}; max Gamma/H {gm3:.3g}",
      cgm < 0.05 and cem < 0.05 and rtm < 2.0)
L.out["numbers"]["B3"] = b3
P(f"    {L.el()}")

# ================================================================================================ B3r z = 0.25, no yield
banner("B3r  (reported) THE RADIAL GAS SECTOR AT z = 0.25 (NO YIELD): host-dominated domain [1 kpc, 3 L] and the whole [1 kpc, 20 Mpc]")
b3r = {}
for (z, Mb, f) in [g_ for g_ in GAL if g_[0] == 0.25]:
    tr = transition(z, Mb, f, 0.25); bg = hk1_host(z, Mb, f, tr["r"]); yw = y_web(z, f)
    for dom, rb in (("[1 kpc, 3 L]", 3 * bg["L"]), ("[1 kpc, 20 Mpc]", 2e4 * KPC)):
        for emb in ("isolated", "embedded"):
            r = np.geomspace(1.0 * KPC, rb, 500)
            rho = np.exp(np.interp(np.log(r), np.log(tr["r"]), np.log(tr["rho_b"])))
            yfun = (lambda rr_: hk1_host(z, Mb, f, rr_)["ybp"]) if emb == "isolated" else \
                (lambda rr_, yw=yw: np.sqrt(hk1_host(z, Mb, f, rr_)["ybp"] ** 2 + yw ** 2))
            edges = np.concatenate([[r[0]], 0.5 * (r[1:] + r[:-1]), [r[-1]]])
            re_ = np.unique(np.concatenate([edges, r]))
            X = xns["cum_Q2"](re_, yfun, 0.0)
            Q2w = np.diff(np.interp(edges, re_, X))
            K, Mm = xns["radial_operator"](r, rho, Q2w, CS["1e6K"] ** 2, bg["L"])
            b3r[(KEY(z, Mb, f), dom, emb)] = xns["growth"](K, Mm) / tr["H"]
for (hk_, dom, emb), v in b3r.items():
    if hk_.endswith("canonical"):
        P(f"    {hk_:22s} {dom:16s} {emb:9s}: Gamma/H (1e6 K) {v:.3g}")
check("B3r (reported) z = 0.25, no yield: the exact radial 1e6 K gas sector on the host-dominated domain and on the whole profile, "
      "isolated and web-embedded", f"isolated whole-profile max {max(v for k_, v in b3r.items() if k_[1].startswith('[1 kpc, 20') and k_[2] == 'isolated'):.3g}; "
      f"embedded whole-profile max {max(v for k_, v in b3r.items() if k_[1].startswith('[1 kpc, 20') and k_[2] == 'embedded'):.3g}; host-dominated "
      f"max {max(v for k_, v in b3r.items() if k_[1].startswith('[1 kpc, 3')):.3g}", True, load_bearing=False)
L.out["numbers"]["B3r"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v for k_, v in b3r.items()}

banner("VERDICT")
nlb = sum(1 for _, ok, lb in L.ch if lb and not ok)
pf = {k_: ("PASS" if L.out["checks"][k_]["ok"] else "FAIL") for k_ in ("B1", "B2", "B2w", "B2z", "B3")}
P(f"""  Item 5 (the DE12-type second variation).  No k^0 term in H_K1's action, the <K>_h channel included (O(k^-4)){' [MUTATE: DE12 gate]' if MUT else ''}
    (B1: {pf['B1']}).  DE12's convention on isolated hosts: {pf['B2']} -- max {g2max:.3g} H at z = 0.25, in the far field where the host's
    band-passed field is ~1e-24 a0 and H_K1 has no yield; embedded in the web's own band-passed field it is {b2w_max:.3g} (B2w: {pf['B2w']}), and at the
    web's zeros and cored centres 1e6 K gas does not grow at 1/kpc (B2z: {pf['B2z']}).  Around H_K1's yield surfaces the exact radial gas
    sector is bounded ({gm3:.3g} H max), converged and not raised above plain P2 (B3: {pf['B3']}).
  Not 'closed'.  kappa = 1/2 FITTED.  {sum(1 for _, o_, _l in L.ch if o_)}/{len(L.ch)} checks pass; load-bearing failures: {nlb}.""")
L.out["ledger"] = [
    dict(link="XR18b-B1", status="DERIVED" if L.out["checks"]["B1"]["ok"] else "FAILS", what="no k^0 term in H_K1's action (the <K>_h channel O(k^-4))"),
    dict(link="XR18b-B2", status="FAILS" if not L.out["checks"]["B2"]["ok"] else "DERIVED",
         what="DE12's convention on an ISOLATED host at z < z_q0: the unplugged far-field zero gives 1e4-1e5 H at 1/kpc (no yield below z_q0)"),
    dict(link="XR18b-B2w", status="DERIVED" if L.out["checks"]["B2w"]["ok"] else "FAILS", what="embedded in the web's band-passed field: no growth at 1/kpc"),
]
L.finish()
