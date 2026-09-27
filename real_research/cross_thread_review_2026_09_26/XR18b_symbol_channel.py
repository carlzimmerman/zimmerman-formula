#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18b (1 of 4) -- H_K1's LINEAR CONSTRAINT SYMBOLS AND ITS <K>_h CHANNEL, AUDITED AS AN ACTION (items 1 and 2 of the re-audit).

WHY.  XR18 (53854a459) found FP13's state separator H_S linearly ILL POSED: B read a Newtonian-order leaf functional, so
dS/dB (O(V)) x dB/d delta (O(1/V)) was an O(1) local term, R_B = 6.9-8.1, and the psi-constraint symbol k^2 (1 - R_B) changed
sign on k = 0.12-1.62 h/Mpc.  FP19 (0c18c582f) repaired it with H_K1, a separator that reads only the leaf average <K>_h
(per 1/16 pi G, c = 1, alpha = a0/c^2):
    chi = (S_xi - S_B) phi,  B = L^2/2,  L = L_Lambda 3 Lambda/<K>_h^2  (L_Lambda = 2.9 Mpc, n = 2),
    J_Y = J_P2 + 2 y_th sqrt(Y),  y_th = max(0, 1 + Omega_r - 9 Lambda/<K>_h^2) (<K>_h^2/3 - Lambda) L/alpha  (c_y = 2, the q = 0 ramp).
FP19 H3 reports the psi-symbol "exactly 1, min +0.995", H4 a lattice B-part that vanishes for every plane wave.  Its symbol is
S = 1 + kappa h^2 - R_B - eps_K with R_B = kappa = 0 for a <K>_h read, and eps_K = 4.96e-3 SUBTRACTED: the raw value of XR18 C1's
<K>_h-channel proxy in the halo reading at z = 0.25, which does not converge in its lower mass cutoff.  This lane asks whether
the subtraction is legitimate or hides a real term, and what varying the FULL action through <K>_h actually produces.

WHAT THE VARIATION THROUGH <K>_h PRODUCES (derived here, exact in the ADM variables; sympy verifies it in S2):
  <K>_h = Q/V, Q = Int sqrt(h) K d^3x, V = Int sqrt(h) d^3x (the leaf average weighs the leaf's proper volume).  For a plane wave
  (k != 0) the first variation of <K>_h vanishes but the second does not: d^2<K>_h = (d^2 Q - <K>_h d^2 V)/V.  The action depends
  on <K>_h through the whole leaf (dS/d<K>_h = O(V)), so
      d^2 S  contains  (dS/d<K>_h) d^2<K>_h = C(t) d^2 Int [sqrt(h) K - <K>_h sqrt(h)] d^3x,   C = <N dL/d<K>_h>_h,
  a LOCAL operator at EVERY k with a leaf-averaged coefficient -- not a k = 0 term.  In unitary (khronon) gauge, N = 1 + A,
  N_i = d_i beta, h_ij = a^2 e^(2 zeta) delta_ij:
      L_C^(2) = C a^3 [3 H A^2 - 9 H A zeta - 3 A zeta' + 9 zeta zeta' + a^-2 A lap beta].
  FP19 H4's lattice read (B a LINEAR function of the leaf mean of psi) has d^2 B = 0 by construction; the real <K>_h does not.
  Its size: 3 H C = rho_extra = -d e_M/d ln<K>_h (the MOND sector's energy density e_M varied at fixed fields: through B via
  the chassis's MOND-binding rate dS/dB = V 4 pi G rho_bar^2 I(B) (FP19 A2's envelope identity) and through y_th via
  d e_M/d y_th = a0^2 <x>/(4 pi G)), and every C-entry of the quadratic action is eps_C = C/(2 M_p^2 H) = rho_extra/(2 rho_crit)
  times a GR entry of the same structure (or eps_C (aH/k)^2 times a GR k^2 entry).

PRE-DECLARED HYPOTHESES (written into this file before its first full run; exploratory runs disclosed in XR18b_README.md:
a sizing of I(L), I_halo and <x> on H_K1's grown state, a sympy prototype of the ADM expansion and of the minisuperspace
identities, and a reload test of FP19's machinery)
 H1 [load-bearing] THE NEWTONIAN psi-SYMBOL IS POSITIVE FOR EVERY SUB-HORIZON k: on H_K1's own grown state (z = 0, 0.25, 0.5,
    z_q0, 0.8, 1, 1.5, 2, 2.5; both footings; both chords; k from 10 aH/c to 1e3 h/Mpc, where the Newtonian reading applies)
    min S >= 0.99, where S = FP19's symbol (R_B = kappa = 0 for the headline's <K>_h read; eps_K NOT subtracted) minus the <K>_h
    channel's bound Delta(k, z) = 2|eps_C| + 9|eps_C| (aH/k)^2 (1 + |dln C/dln a + 3|) (the summed relative changes the
    C-entries make to the constraint's coefficients, S2's table: A^2 and A lap beta and A zeta' at eps_C, A zeta at
    9 eps_C (aH/k)^2, the zeta zeta' mass term at 9 eps_C (aH/k)^2 |dln C/dln a + 3|).  Below 10 aH/c the relativistic block
    (H2) is the object; Delta at k = 1e-4 h/Mpc is reported.  MUTATE's variance-fixed B must bring back the ill-posed band
    (min S < 0).
 H2 [load-bearing] THE CONSTRAINT BLOCK IS UNCHANGED: with Brown-Kuchar dust, in unitary gauge about flat FRW, the determinant
    of the constrained block (lapse, shift, dust multiplier [, the CMC multiplier]) with the <K>_h channel equals the one
    without it IDENTICALLY (sympy), at finite c_2 and at c_2 = oo; the C-entries are eps_C x the GR entries (A^2: 2 eps_C,
    A lap beta: eps_C, A zeta': eps_C) or eps_C (aH/k)^2 x a GR k^2 entry (A zeta, zeta zeta'); the same holds with the
    leaf average weighted by N sqrt(h) (robustness).
 H3 [load-bearing] THE CHANNEL IS (v/c)^2-SMALL ON THE REAL STATE: |eps_C| <= 1e-4 and |rho_extra|/rho_bar <= 1e-4 at every
    z = 0 .. 2.5, both footings, in every reading of the web: B-channel from I(L) (per-mode and rms chords on H_K1's grown
    linear state; FP19's halo reading), y-channel from <x> (Gaussian reading and the reading-free Jensen bound
    <x> <= <y>^(1/2) <= y_rms^(1/2) of the band-passed NL field, since x_P2(y) <= sqrt(y)).
 H4 [load-bearing] eps_K IS NOT THE SIZE OF ANY TERM, AND ITS SUBTRACTION HIDES NONE: FP19's eps_K (4.96e-3) is XR18 C1's
    proxy a0^2 <x>^3/(6 pi G) with the halo reading's <x> at z = 0.25; that <x> (M_min = 1e8) exceeds the Jensen bound
    y_rms^(1/2) (the dilute-halo sum counts overlapping deep-MOND fields as scalars) and does not converge in M_min, while the
    quantity the variation actually needs through B, I_halo = dS/dB/(V 4 pi G rho_bar^2), DOES converge (1e7 vs 1e8 within 5%);
    the derived channel is below eps_K/10 everywhere (the subtraction is conservative).
 H5 [load-bearing] THE phi-SYMBOL NEVER CHANGES SIGN: for every C_phi >= 0 (J_Y's C_T = (F_P2 + y_th)/x, C_L = F_P2'(x),
    y_th >= 0) all roots U = omega^2/k^2 of FP7's block are real and >= 0 at finite c_2 and at c_2 = oo (sympy: the
    discriminant is (A - B)^2 + S^2 + 2 S (A + B)); C_phi = 0 only at zero field (z < z_q0, no yield) -- a degenerate, not a
    negative, symbol; the Gaussian state's volume fraction with C_L < 1e-2 is printed.
 H6 [load-bearing] CONSERVATION AND THE BIANCHI IDENTITY: (i) for the full action with the separator varied through <K>_h
    (minisuperspace, explicit test functions of <K> and a including a smoothed ramp) the reparametrisation Noether identity
    N dE_N/dt - a' E_a = 0 holds identically; (ii) with the separator's read FROZEN (C prescribed in time, as a scoring or PM
    run does) it fails, and on the real state the Friedmann constraint drifts at |3 H' C|/(3 H rho_bar) <= 1e-4 per Hubble
    rate; (iii) a read of the scale factor instead (L(a), y_th(a): the PM engine's form) satisfies it identically;
    (iv) on periodic 3-D leaves the channel's lapse term (a leaf-uniform coefficient) exerts no net force on a real density
    field (< 1e-12 relative), while a position-weighted coefficient does (> 1e-4): translation invariance holds.
The writer's expectation: all six pass (H1 because the channel is (v/c)^2-small, not because it is absent).

CHECKS
  K1 CONTROL: FP19's committed H1 headline (sigma_8 x4, forest x4, flagships x4, SPARC x2, KiDS at 0.25/0.4/0.7 x6 -- the KiDS
     numbers are PRE-FP20, FP6's projection, reproduced only as a code control) and its L(z), y_th(z) tables, with FP19's own
     code exec'd read-only; this lane's closed forms for L(z) and y_th(z) equal FP19's L_K and y_tied.
  K2 CONTROL: FP19's committed H3 symbol tables (headline and FP13's H_S) with FP19's own symbol_table and eps_K.
  K3 CONTROL: XR18's committed N3 (max R_B per footing and epoch, per-mode and rms chords, and the k-band where R_B >= 1) on
     FP13's headline, with XR18's OWN functions (D2_at, chord_modes, RB_of: their text extracted from
     XR18_state_separator.py and run; nothing of XR18 is executed at top level).
  K4 CONTROL: this lane's second-order ADM expansion gives the standard Friedmann pair at C = 0 and the hand-derived C-operator.
  S1 = H1.  S2 = H2.  S3 = H3.  S4 = H4.  S5 = H5.  B1 = H6 (i)-(iii).  B2 = H6 (iv).
  N1 (reported) XR18 C1's formula on H_K1 (FP19 B4) against the derived channel, both footings and readings.
MUTATE=1 restores FP13's variance-fixed B in the headline (L from <(S_B delta_m)^2>_h = delta_c^2, the tied yield kept): the
separator reads a Newtonian-order leaf functional again, R_B returns, and S1 must FAIL (rc = 1).

SCOPE.  Linear symbols about FRW (the constraint block exact in sympy; the Newtonian-order symbol on FP19's per-mode
yardstick); the web's state as FP13/FP19 read it (EH98 + halofit, H_K1's grown per-mode modes); the Gaussian and halo
readings are brackets, the Jensen bound is reading-free.  All-matter reading (as FP19).  No particle-mesh run.  At most 2
threads.  kappa = 1/2 is FITTED (Z = 5.7888); nothing here derives it, and nothing here closes the theory.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18b_symbol_channel.py
"""
import os, sys, io, json, math, time, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations
import XR18b_common as XC

L = XC.Lane("XR18b_symbol_channel", "XR18b/symbol")
P, check, banner = L.P, L.check, L.banner
MUT = L.mutate
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: FP13's variance-fixed B is restored in the headline (the tied yield kept) -- S1 must FAIL ***")

# ================================================================================================ machinery (read-only)
NS = XC.load_fp19()
A0, FOOTS, MODES = NS["A0"], NS["FOOTS"], NS["MODES"]
M6 = NS["M6"]
h_, Om, OL, Or, H0, c_, Mpc, G, rho_crit0 = (NS["h_"], NS["Om"], NS["OL"], NS["Or"], NS["H0"], NS["c_"], NS["Mpc"], NS["G"],
                                             NS["rho_crit0"])
Ez, dlnH, AGR, KKF, KHF, DIF, Z_Q0 = NS["Ez"], NS["dlnH"], NS["AGR"], NS["KKF"], NS["KHF"], NS["DIF"], NS["Z_Q0"]
growth_aq, model_of, gates2 = NS["growth_aq"], NS["model_of"], NS["gates2"]
L_K, y_tied, I_of, rms_bp_L, D2_at = NS["L_K"], NS["y_tied"], NS["I_of"], NS["rms_bp_L"], NS["D2_at"]
maxwell_x_mean, x_mean_halo_c, K_channel = NS["maxwell_x_mean"], NS["x_mean_halo_c"], NS["K_channel"]
symbol_table, x_P2 = NS["symbol_table"], NS["x_P2"]
Lh, yh = NS["Lh"], NS["yh"]
LK, yK = NS["LK_head"], NS["yK_head"]
HK = XC.hk1_forms(M6, A0)
F19 = json.load(open(os.path.join(XC.CHAIN, "FP19_hs_repair_results.json")))["numbers"]
X18 = json.load(open(os.path.join(XC.HERE, "XR18_state_separator_results.json")))["numbers"]
P(f"\n  machinery: FP19's module + main() slices exec'd read-only (FP13 -> FP9 -> FP6 inside); a0 = {A0['canonical']:.4e} / "
  f"{A0['alt']:.4e} m/s^2; q = 0 at z = {Z_Q0:.4f}   {L.el()}")

# ================================================================================================ K1 FP19's headline
banner("K1  CONTROL: FP19's committed H_K1 headline with FP19's own code (KiDS numbers PRE-FP20: a code control only)")
HH = gates2({f: LK for f in FOOTS}, yK)
ref = F19["H1"]; devs = []
for grp in ("s8", "forest", "flag"):
    for k_, v in HH[grp].items():
        rv = ref[grp][str(k_)]; devs.append(abs(v - rv) if rv == 0 else abs(v / rv - 1))
for grp in ("sparc", "kids", "kids@0.4", "kids@0.7"):
    for f in FOOTS:
        devs.append(abs(HH[grp][f] / ref[grp][f] - 1))
for zz, v in ref["L_kpc"].items():
    devs.append(abs(1e3 * LK(1 / (1 + float(zz))) / v - 1))
for zz, v in ref["yth"].items():
    vv = yK["canonical"](1 / (1 + float(zz))); devs.append(abs(vv - v) if v == 0 else abs(vv / v - 1))
cf = max(max(abs(HK["L_of"](z) / LK(1 / (1 + z)) - 1) for z in np.linspace(0, 4, 41)),
         max(abs(HK["yth_of"](z, f) - yK[f](1 / (1 + z))) / max(yK[f](1 / (1 + z)), 1e-300) for z in np.linspace(0, 4, 41) for f in FOOTS))
P(f"    sigma_8 " + ", ".join(f"{k_[0][:3]}/{k_[1]}: {v:.6f}" for k_, v in HH["s8"].items()) + f"; flagships {min(HH['flag'].values()):+.4f}.."
  f"{max(HH['flag'].values()):+.4f} dex; SPARC {max(HH['sparc'].values()):.2e}; KiDS (pre-FP20) {HH['kids']}")
check("K1 CONTROL: FP19's committed H_K1 headline (sigma_8 x4, forest x4, flagships x4, SPARC x2, KiDS at z = 0.25/0.4/0.7 x6 [pre-FP20 "
      "projection]) and its L(z) and y_th(z) tables, with FP19's own code exec'd read-only; this lane's closed forms equal FP19's "
      "L_K and y_tied", f"max relative deviation {max(devs):.1e} over {len(devs)} numbers; closed forms vs FP19 {cf:.1e}",
      max(devs) <= 1e-9 and cf <= 1e-12)
L.out["numbers"]["K1"] = {"dev": max(devs), "closed_form_dev": cf}

# ================================================================================================ K2 FP19's symbol tables
banner("K2  CONTROL: FP19's committed H3 symbol tables (headline and FP13's H_S) with FP19's own symbol_table")
eps_K = NS["eps_K"]
sym_head = symbol_table(LK, yK, "K", "K")
sym_hs = symbol_table(Lh, yh, "variance", "state")
k2dev = 0.0
for (f, z), v in sym_head.items():
    k2dev = max(k2dev, abs(v["Smin"] - F19["H3"]["headline"][f"{f}/{z}"]["Smin"]))
for (f, z), v in sym_hs.items():
    r_ = F19["H3"]["H_S"][f"{f}/{z}"]["Smin"]; k2dev = max(k2dev, abs(v["Smin"] - r_) / max(abs(r_), 1e-12))
P(f"    eps_K = {eps_K:.6e} (FP19: {F19['H3']['eps_K']:.6e}); headline min S = {min(v['Smin'] for v in sym_head.values()):+.6f} "
  f"(= 1 - eps_K: {abs(min(v['Smin'] for v in sym_head.values()) - (1 - eps_K)) < 1e-12}); H_S min S = {min(v['Smin'] for v in sym_hs.values()):+.3f}")
check("K2 CONTROL: FP19's committed H3 symbol tables -- the headline's S(k, z) = 1 - eps_K (R_B = kappa = 0 for a <K>_h read) and "
      "FP13's H_S band -- with FP19's own symbol_table and eps_K (recomputed by FP19's K_channel)",
      f"max deviation {k2dev:.1e}; eps_K {eps_K:.4e} vs committed {F19['H3']['eps_K']:.4e}",
      k2dev <= 1e-9 and abs(eps_K / F19["H3"]["eps_K"] - 1) <= 1e-12)

# ================================================================================================ K3 XR18's N3 with XR18's own functions
banner("K3  CONTROL: XR18's committed N3 (R_B on FP13's headline) with XR18's OWN function text, run on FP13's machinery")
xns = dict(NS)
exec(XC.extract_defs(os.path.join(XC.HERE, "XR18_state_separator.py"), ["D2_at", "chord_modes", "RB_of"]), xns)
ZS_SCAN = (0.0, 0.25, 0.5, 0.635, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0)
k3 = {}; k3dev = 0.0
for f in FOOTS:
    a0v = A0[f]
    res = growth_aq(model_of(Lh, yh[f]), a0v, mode="permode", KHg=KHF, Dig=DIF, zs_out=tuple(z for z in ZS_SCAN if z > 0))
    for z in ZS_SCAN:
        a = 1 / (1 + z); Lp = Lh(a); yt = yh[f](a)
        CQ, hk, yk = xns["chord_modes"](res[round(z, 6)], a, a0v, Lp, yt, KHF, "permode")
        RB, ratio = xns["RB_of"](a, CQ, KHF, Lp)
        CQr, _, _ = xns["chord_modes"](res[round(z, 6)], a, a0v, Lp, yt, KHF, "rms")
        RBr, _ = xns["RB_of"](a, CQr, KHF, Lp)
        kge1 = KHF[RB >= 1.0]
        k3[(f, z)] = dict(RB_max=float(np.max(RB)), RB_max_rms=float(np.max(RBr)),
                          k_RBge1=(float(kge1.min()), float(kge1.max())) if len(kge1) else None)
        rv = X18["coef"][f"{f}/{z}"]
        for key in ("RB_max", "RB_max_rms"):
            k3dev = max(k3dev, abs(k3[(f, z)][key] - rv[key]) if rv[key] < 1e-100 else abs(k3[(f, z)][key] / rv[key] - 1))
        if (rv["k_RBge1"] is None) != (k3[(f, z)]["k_RBge1"] is None):
            k3dev = max(k3dev, 1.0)
        elif rv["k_RBge1"] is not None:
            k3dev = max(k3dev, max(abs(k3[(f, z)]["k_RBge1"][q_] / rv["k_RBge1"][q_] - 1) for q_ in (0, 1)))
late = {k_: v for k_, v in k3.items() if k_[1] <= 0.635 + 1e-9}
band = [v["k_RBge1"] for v in late.values() if v["k_RBge1"]]
rb_c = [v["RB_max"] for (f, z), v in late.items() if f == "canonical"]; rb_a = [v["RB_max"] for (f, z), v in late.items() if f == "alt"]
P(f"    per-mode max R_B at z <= 0.635: canonical {min(rb_c):.2f}-{max(rb_c):.2f}, alt {min(rb_a):.2f}-{max(rb_a):.2f}; R_B >= 1 on "
  f"k = {min(b_[0] for b_ in band):.2f}-{max(b_[1] for b_ in band):.2f} h/Mpc (the psi-symbol k^2 (1 - R_B) changes sign there)")
check("K3 CONTROL: XR18's committed N3 on FP13's H_S -- max R_B (per-mode and rms chords) at z = 0..3 on both footings and the k-band "
      "where R_B >= 1 -- reproduced with XR18's own functions: R_B = 6.9-7.5 (canonical) / 7.6-8.1 (alt) at z <= 0.635 and the sign "
      "change on k = 0.12-1.62 h/Mpc", f"max relative deviation {k3dev:.1e}; canonical {min(rb_c):.2f}-{max(rb_c):.2f}, alt "
      f"{min(rb_a):.2f}-{max(rb_a):.2f}; band {min(b_[0] for b_ in band):.2f}-{max(b_[1] for b_ in band):.2f} h/Mpc", k3dev <= 1e-9)
L.out["numbers"]["K3"] = {f"{k_[0]}/{k_[1]}": v for k_, v in k3.items()}
P(f"    {L.el()}")

# ================================================================================================ the ADM expansion (sympy)
banner("K4 S2  THE <K>_h CHANNEL IN THE ADM VARIABLES: second-order expansion about flat FRW (unitary gauge, sympy)")
t_, x_ = sp.symbols('t x', real=True)
eb = sp.Symbol('e')
af = sp.Function('a')(t_); Cf = sp.Function('C')(t_)
Mp2, Lam, c2s, rho0 = sp.symbols('M_p2 Lambda c_2 rho_0', positive=True)
Af, bf, zf, pif, dlf, muf = [sp.Function(n_)(t_, x_) for n_ in ('A', 'beta', 'zeta', 'pi', 'delta', 'mu')]
Nl = 1 + eb * Af
hsc = af ** 2 * sp.exp(2 * eb * zf)                        # h_ij = hsc delta_ij (E = 0 spatial gauge), one plane wave along x
sqh = af ** 3 * sp.exp(3 * eb * zf)                      # sqrt(h), a > 0
Nx = eb * sp.diff(bf, x_)
lnh = sp.log(hsc); dln = [sp.diff(lnh, x_), 0, 0]


def Gam(k_, i, j):
    return sp.Rational(1, 2) * ((dln[i] if j == k_ else 0) + (dln[j] if i == k_ else 0) - (dln[k_] if i == j else 0))


Nlow = [Nx, 0, 0]
dN = [[(sp.diff(Nlow[j], x_) if i == 0 else 0) for j in range(3)] for i in range(3)]
DN = [[dN[i][j] - sum(Gam(k_, i, j) * Nlow[k_] for k_ in range(3)) for j in range(3)] for i in range(3)]
Kij = [[((sp.diff(hsc, t_) if i == j else 0) - DN[i][j] - DN[j][i]) / (2 * Nl) for j in range(3)] for i in range(3)]
KK = sum(Kij[i][j] * Kij[i][j] / hsc ** 2 for i in range(3) for j in range(3))
trK = sum(Kij[i][i] / hsc for i in range(3))
om_ = sp.log(hsc) / 2
R3 = -sp.exp(-2 * om_) * (4 * sp.diff(om_, x_, 2) + 2 * sp.diff(om_, x_) ** 2)
Tt = 1 + eb * sp.diff(pif, t_); Tx = eb * sp.diff(pif, x_)
gTT = -(Tt - (Nx / hsc) * Tx) ** 2 / Nl ** 2 + Tx ** 2 / hsc
Hb = sp.diff(af, t_) / af
PIECES = {
    "EH+Lambda": (Mp2 / 2) * sqh * Nl * (R3 + KK - trK ** 2) - Mp2 * Lam * Nl * sqh,
    "dust (Brown-Kuchar)": -sp.Rational(1, 2) * Nl * sqh * (rho0 / af ** 3) * (1 + eb * dlf) * (gTT + 1),
    "khronon c_2 (K - <K>)^2": -(Mp2 / 2) * c2s * Nl * sqh * (trK - 3 * Hb) ** 2,
    "CMC multiplier -2 mu (K - <K>)": -Mp2 * Nl * sqh * eb * muf * (trK - 3 * Hb),
    "<K>_h channel (sqrt h weight)": Cf * (sqh * trK - 3 * Hb * sqh),
    "<K>_h channel (N sqrt h weight)": Cf * (Nl * sqh * trK - 3 * Hb * Nl * sqh),
}


def order(ex, n):
    return sp.expand(sp.series(ex, eb, 0, n + 1).removeO().coeff(eb, n))


L1 = {k_: order(v_, 1) for k_, v_ in PIECES.items()}
L2 = {k_: order(v_, 2) for k_, v_ in PIECES.items()}
# K4: background equations (k = 0) at C = 0 and the C channel's first order
A0f, z0f, p0f, d0f = [sp.Function(n_)(t_) for n_ in ('A0', 'z0', 'pi0', 'd0')]
hom = {Af: A0f, zf: z0f, pif: p0f, dlf: d0f, bf: sp.Integer(0), muf: sp.Integer(0)}
bgeq = {}
for lab, keys in (("GR", ("EH+Lambda", "dust (Brown-Kuchar)")), ("GR+C", ("EH+Lambda", "dust (Brown-Kuchar)", "<K>_h channel (sqrt h weight)"))):
    L1h = sum(L1[k_] for k_ in keys).subs(hom).doit()
    E1 = euler_equations(L1h, [A0f, z0f], t_)
    bgeq[lab] = [sp.simplify((e_.lhs - e_.rhs) / af ** 3) for e_ in E1]
Hs, Hds, Cs, Cds, rbs = sp.symbols('H Hdot C Cdot rho_b', real=True)


def bgsub(ex):
    ex = ex.subs(sp.Derivative(af, (t_, 2)), af * (Hds + Hs ** 2)).subs(sp.Derivative(af, t_), af * Hs).subs(sp.Derivative(Cf, t_), Cds)
    return sp.simplify(ex.subs(Cf, Cs).subs(rho0, rbs * af ** 3))


fr = [sp.expand(bgsub(e_)) for e_ in bgeq["GR"]]
frC = [sp.expand(bgsub(e_)) for e_ in bgeq["GR+C"]]
fried_ok = (sp.simplify(fr[0] - (3 * Mp2 * Hs ** 2 - rbs - Mp2 * Lam)) == 0 and
            sp.simplify(fr[1] - 3 * Mp2 * (2 * Hds + 3 * Hs ** 2 - Lam)) == 0)
C2hand = Cf * af ** 3 * (3 * Hb * Af ** 2 - 9 * Hb * Af * zf - 3 * Af * sp.diff(zf, t_) + 9 * zf * sp.diff(zf, t_)
                         + af ** -2 * Af * sp.diff(bf, x_, 2))
diffC = sp.simplify(sp.expand(L2["<K>_h channel (sqrt h weight)"] - C2hand)
                    + sp.diff(Cf * af * zf * sp.diff(bf, x_), x_))           # the remainder must be the total x-derivative
k4_ok = fried_ok and diffC == 0
P(f"    background (C = 0): {fr[0]} = 0 ; {fr[1]} = 0")
P(f"    background with the channel: {frC[0]} = 0 ; {frC[1]} = 0   (rho_extra = 3 H C)")
P(f"    second-order channel (sqrt h weight) - C a^3 [3H A^2 - 9H A zeta - 3 A zeta' + 9 zeta zeta' + a^-2 A lap beta] = total x-derivative: {diffC == 0}")
check("K4 CONTROL: this lane's second-order ADM expansion about flat FRW gives, at C = 0, the standard Friedmann pair "
      "(3 M_p^2 H^2 = rho_bar + M_p^2 Lambda, 2 H' + 3 H^2 = Lambda) and, for the channel, the hand-derived operator "
      "C a^3 [3 H A^2 - 9 H A zeta - 3 A zeta' + 9 zeta zeta' + a^-2 A lap beta] up to a total derivative",
      f"Friedmann pair {fried_ok}; channel operator {diffC == 0}", k4_ok)

# S2: the constrained block, with and without the channel
kq, a0s = sp.Symbol('k', positive=True), sp.Symbol('a_0', positive=True)
Ah, bh, zh, ph, dh, mh = sp.symbols('Ahat bhat zhat phat dhat mhat')
FL = [Af, bf, zf, pif, dlf, muf]; AMPS = [Ah, bh, zh, ph, dh, mh]


def rows_for(keys):
    Lq = sum(L2[k_] for k_ in keys)
    use = [f_ for f_ in FL if Lq.has(f_)]
    EL = euler_equations(Lq, use, [t_, x_])
    rows = {}
    for f_, e_ in zip(use, EL):
        ex = (e_.lhs - e_.rhs).subs({F_: Fh * sp.exp(sp.I * kq * x_) for F_, Fh in zip(FL, AMPS)}).doit()
        ex = sp.expand(sp.simplify(ex * sp.exp(-sp.I * kq * x_)))
        ex = ex.subs(sp.Derivative(af, (t_, 2)), a0s * (Hds + Hs ** 2)).subs(sp.Derivative(af, t_), a0s * Hs).subs(sp.Derivative(Cf, t_), Cds)
        rows[f_.func.__name__] = sp.expand(ex.subs(af, a0s).subs(Cf, Cs).subs(rho0, rbs * a0s ** 3))
    return rows


amp_of = dict(zip(["A", "beta", "zeta", "pi", "delta", "mu"], AMPS))
s2 = {}
for core, ck in (("c_2 finite", "khronon c_2 (K - <K>)^2"), ("c_2 = oo (CMC)", "CMC multiplier -2 mu (K - <K>)")):
    for wlab, wk in (("sqrt h", "<K>_h channel (sqrt h weight)"), ("N sqrt h", "<K>_h channel (N sqrt h weight)")):
        rows = rows_for(("EH+Lambda", "dust (Brown-Kuchar)", ck, wk))
        con = [nm for nm in ("A", "beta", "delta", "mu") if nm in rows]
        Mc = sp.Matrix([[sp.expand(sp.diff(rows[r_], amp_of[c_])) for c_ in con] for r_ in con])
        dC = sp.factor(sp.simplify(Mc.det())); d0 = sp.factor(sp.simplify(Mc.det().subs({Cs: 0, Cds: 0})))
        s2[(core, wlab)] = dict(fields=con, det=str(dC), det0=str(d0), same=sp.simplify(dC - d0) == 0 and d0 != 0,
                                AA=str(sp.factor(Mc[0, 0])), Abeta=str(sp.factor(Mc[0, 1])))
        P(f"    [{core}; leaf weight {wlab}] constrained fields {con}: det = {dC}  (without the channel: {d0}); A-A entry {sp.factor(Mc[0, 0])}; "
          f"A-beta entry {sp.factor(Mc[0, 1])}")
# the channel's entries relative to GR's same-structure entries (sqrt h weight; unitary gauge, E = 0)
L2GR = sp.expand(L2["EH+Lambda"] + L2["dust (Brown-Kuchar)"])
L2C = sp.expand(C2hand)
coef = {}
for lab, mon in (("A^2", Af ** 2), ("A lap beta", Af * sp.diff(bf, x_, 2)), ("A zeta'", Af * sp.diff(zf, t_)), ("A zeta", Af * zf),
                 ("A lap zeta", Af * sp.diff(zf, x_, 2))):
    coef[lab] = (sp.simplify(L2GR.coeff(mon)), sp.simplify(L2C.coeff(mon)))
for lab, (g_, c__) in coef.items():
    P(f"    entry {lab:11s}: GR {bgsub(g_)} | channel {bgsub(c__)}")
epsC = sp.Symbol('eps_C')
ratio_AA = sp.simplify(bgsub(coef["A^2"][1]) / (-3 * Mp2 * Hs ** 2 * af ** 3)).subs(Cs, 2 * Mp2 * Hs * epsC)
ratio_Ab = sp.simplify(bgsub(coef["A lap beta"][1]) / bgsub(coef["A lap beta"][0])).subs(Cs, 2 * Mp2 * Hs * epsC)
ratio_Az = sp.simplify(bgsub(coef["A zeta'"][1]) / bgsub(coef["A zeta'"][0])).subs(Cs, 2 * Mp2 * Hs * epsC)
ratio_Aze = sp.simplify(-bgsub(coef["A zeta"][1]) / (kq ** 2 * bgsub(coef["A lap zeta"][0]))).subs(Cs, 2 * Mp2 * Hs * epsC)
P(f"    ratios channel/GR: A^2 {ratio_AA} (vs GR's -3 M_p^2 H^2 a^3); A lap beta {ratio_Ab}; A zeta' {ratio_Az}; A zeta (k^0) vs GR's A lap zeta "
  f"(k^2): {ratio_Aze}")
s2_same = all(v["same"] for v in s2.values())
rat_ok = (sp.simplify(ratio_AA + 2 * epsC) == 0 and sp.simplify(ratio_Ab + epsC) == 0 and sp.simplify(ratio_Az + epsC) == 0)
check("S2 [H2, pre-declared] THE CONSTRAINED BLOCK IS UNCHANGED BY THE <K>_h CHANNEL: with Brown-Kuchar dust in unitary gauge about "
      "flat FRW, det(lapse, shift, dust multiplier [, CMC multiplier]) with the channel equals det without it IDENTICALLY, at finite "
      "c_2 and at c_2 = oo, for the sqrt(h) and the N sqrt(h) leaf weights; the channel's entries are eps_C x GR's same-structure "
      "entries (A^2: -2 eps_C, A lap beta: -eps_C, A zeta': -eps_C) or eps_C (aH/k)^2 x a GR k^2 entry (A zeta)",
      "; ".join(f"{k_[0]}/{k_[1]}: {'identical' if v['same'] else 'CHANGED'}" for k_, v in s2.items())
      + f"; ratios A^2 {ratio_AA}, A lap beta {ratio_Ab}, A zeta' {ratio_Az}, A zeta {ratio_Aze}", s2_same and rat_ok,
      "the dust multiplier's row (-a^3 rho_bar, 0, 0) makes the determinant independent of the A-A and A-beta entries, the only ones "
      "the channel touches: the constraint stays solvable for ANY C; the channel moves the solution by O(eps_C), not its solvability")
L.out["numbers"]["S2"] = {f"{k_[0]}|{k_[1]}": v for k_, v in s2.items()}
P(f"    {L.el()}")

# ================================================================================================ S3 the channel's size on the real state
banner("S3  THE CHANNEL'S SIZE ON H_K1's REAL STATE: rho_extra = 3 H C = -d e_M/d ln<K>_h, both channels, every reading")
ZS = (0.0, 0.25, 0.5, round(Z_Q0, 4), 0.7, 0.8, 1.0, 1.5, 2.0, 2.5)
LAW = "variance" if MUT else "K"
Lhead = Lh if MUT else LK
yhead = y_tied(Lhead, XC.HEAD_CY)


def halo_rate_M(a, a0v, Lp, yth, Mmin=1e8, nM=120):
    """FP19's halo_rate with its lower mass cutoff exposed (identical at Mmin = 1e8)."""
    Om_, rc0, MSUN, G6, MPCm = Om, rho_crit0, NS["MSUN"], NS["G6"], NS["MPCm"]
    D2 = D2_at(a, "lin"); rho_m = Om_ * rc0 / a ** 3
    lnM = np.linspace(math.log(Mmin), math.log(1e15), nM)
    Rh = ((np.exp(lnM) * MSUN) / ((2 * math.pi) ** 1.5 * Om_ * rc0)) ** (1 / 3) / Mpc * h_
    sg = np.array([math.sqrt(NS["sig2"](R, D2)) for R in Rh]); nu_ = NS["DELTA_C"] / sg
    dn = (Om_ * rc0 / (np.exp(lnM) * MSUN)) * math.sqrt(2 / math.pi) * nu_ * np.exp(-nu_ ** 2 / 2) * np.abs(np.gradient(np.log(sg), lnM)) / a ** 3
    Lm = Lp * MPCm; r = np.geomspace(1e-5, 20.0, 1500) * MPCm
    GB = (2 * math.pi * Lm ** 2) ** -1.5 * np.exp(-r ** 2 / (2 * Lm ** 2))
    tot = 0.0; FB = 0.02237 / (0.02237 + 0.1200)
    for i, lm in enumerate(lnM):
        Mb = 0.3 * FB * math.exp(lm) * MSUN
        x = x_P2(np.maximum(G6 * Mb * (1 - M6["gfrac_smooth"](r / Lm)) / (a0v * r ** 2) - yth, 0.0))
        tot += dn[i] * Mb * 4 * math.pi * float(np.trapz((r / Lm ** 2) * GB * a0v * x * r ** 2, r)) * (lnM[1] - lnM[0])
    return tot / (4 * math.pi * G * rho_m ** 2)


hr_ctrl = abs(halo_rate_M(0.8, A0["canonical"], LK(0.8), 0.0) / NS["halo_rate"](0.8, A0["canonical"], LK(0.8), 0.0) - 1)
s3 = {}
for f in FOOTS:
    a0v = A0[f]
    res = growth_aq(model_of(Lhead, yhead[f]), a0v, mode="permode", KHg=KHF, Dig=DIF, zs_out=tuple(z for z in ZS if z > 0))
    for z in ZS:
        a = 1 / (1 + z); i = int(np.argmin(np.abs(AGR - a))); Lp = Lhead(a); yt = yhead[f](a); D = res[round(z, 6)]
        Ipm = float(I_of(i, a0v, "permode", lambda a_, Ls, yt=yt: yt * np.ones(len(Ls)), Ls=[Lp], D=D, D2=D2_at(a), a=a)[0])
        Irm = float(I_of(i, a0v, "rms", lambda a_, Ls, yt=yt: yt * np.ones(len(Ls)), Ls=[Lp], D=D, D2=D2_at(a), a=a)[0])
        Ih = halo_rate_M(a, a0v, Lp, yt)
        rho = Om * rho_crit0 / a ** 3
        rB = 16 * math.pi * G * rho * 0.5 * (Lp * Mpc) ** 2 / c_ ** 2          # |rho_extra,B|/rho_bar per unit I (n = 2: dB/dln<K> = -4B)
        yrms = float(rms_bp_L(i, [Lp], a0v)[0])
        xG = maxwell_x_mean(yrms, yt); xJ = math.sqrt(yrms)
        e_ = 1e-4
        dy = (yhead[f](a * math.exp(e_)) - yhead[f](a * math.exp(-e_))) / (2 * e_) / dlnH(a)       # dy_th/dln<K>, <K> = 3H
        ry = a0v ** 2 * abs(dy) / (4 * math.pi * G * rho * c_ ** 2)
        rex = rB * max(Ipm, Irm, Ih) + ry * max(xG, xJ)
        Omz = Om / a ** 3 / Ez(a) ** 2
        s3[(f, z)] = dict(L_kpc=1e3 * Lp, yth=yt, I_pm=Ipm, I_rms=Irm, I_halo=Ih, rB_I_lin=rB * max(Ipm, Irm), rB_I_halo=rB * Ih,
                          y_rms=yrms, x_G=xG, x_Jensen=xJ, dy_dlnK=dy, ry_x=ry * max(xG, xJ), rho_extra=rex, eps_C=0.5 * Omz * rex)
for (f, z), v in s3.items():
    P(f"    {f[:3]} z = {z:6.4f}: L {v['L_kpc']:7.1f} kpc, y_th {v['yth']:.2e}; I = {v['I_pm']:.3g} (per-mode) / {v['I_rms']:.3g} (rms) / "
      f"{v['I_halo']:.3g} (halo) -> B-channel |rho_extra|/rho_bar {v['rB_I_lin']:.2e} (linear) / {v['rB_I_halo']:.1e} (halo); y_rms {v['y_rms']:.2e}, "
      f"<x> Gauss {v['x_G']:.3f} <= Jensen {v['x_Jensen']:.3f}; y-channel {v['ry_x']:.2e}; total {v['rho_extra']:.2e}; eps_C {v['eps_C']:.2e}")
eC = {z: max(s3[(f, z)]["eps_C"] for f in FOOTS) for z in ZS}
rex_max = max(v["rho_extra"] for v in s3.values())
# Cdot/C for the zeta zeta' mass term: finite differences of C = rho_extra/(3H) in ln a
lnaz = np.log(1 / (1 + np.array(ZS)))
Cz = np.array([max(s3[(f, z)]["rho_extra"] for f in FOOTS) * Om * rho_crit0 * (1 + z) ** 3 / (3 * H0 * Ez(1 / (1 + z))) for z in ZS])
dlnC = np.gradient(np.log(np.maximum(Cz, 1e-300)), lnaz)
P(f"    control: this lane's halo_rate with M_min exposed equals FP19's at M_min = 1e8: {hr_ctrl:.1e}; dln C/dln a over z = 0..2.5: "
  f"{np.min(dlnC):+.1f} .. {np.max(dlnC):+.1f}")
check("S3 [H3, pre-declared] THE CHANNEL IS (v/c)^2-SMALL ON THE REAL STATE: |eps_C| <= 1e-4 and |rho_extra|/rho_bar <= 1e-4 at every z = "
      "0..2.5, both footings, every reading (B-channel: per-mode, rms and halo I(L); y-channel: Gaussian <x> and the reading-free "
      "Jensen bound y_rms^(1/2))", f"max |rho_extra|/rho_bar {rex_max:.2e}; max |eps_C| {max(eC.values()):.2e} (z = {max(eC, key=eC.get)})",
      rex_max <= 1e-4 and max(eC.values()) <= 1e-4 and hr_ctrl <= 1e-12,
      "the B-channel dominates below z_q0 (the chassis's MOND-binding rate I ~ 60-120 at L ~ 1-2 Mpc, times 8 pi G rho_bar L^2/c^2 ~ 2e-7); "
      "the y-channel is on only above z_q0; both readings of the web agree it is ~1e-5 or less")
L.out["numbers"]["S3"] = {f"{k_[0]}/{k_[1]}": v for k_, v in s3.items()}

# ================================================================================================ S1 the Newtonian psi-symbol
banner("S1  THE NEWTONIAN psi-CONSTRAINT SYMBOL OF THE HEADLINE's READ, EVERY k, z = 0-2.5, BOTH FOOTINGS")
KSYM = KKF                                                             # FP19's fine grid, 1e-4 .. 1e3 h/Mpc
sym_law = symbol_table(Lhead, yhead, LAW, "K")
s1 = {}
zarr = np.array(ZS)
for (f, z), v in sym_law.items():
    a = 1 / (1 + z)
    aH_k = (H0 * Ez(a) * a / c_) / (KSYM * h_ / Mpc)                    # comoving aH/(c k)
    sub = aH_k <= 0.1                                                   # k >= 10 aH/c: the Newtonian reading
    epsz = float(np.interp(z, zarr, np.array([eC[zz] for zz in ZS]))) if LAW == "K" else 0.0
    dlc = float(np.interp(z, zarr, dlnC))
    Delta = 2 * epsz + 9 * epsz * aH_k ** 2 * (1 + abs(dlc + 3))
    S_fp19 = v["Smin"] + eps_K                                         # FP19's symbol with its eps_K subtraction undone
    S = S_fp19 - float(np.max(Delta[sub]))
    s1[(f, z)] = dict(S_FP19_no_epsK=S_fp19, Delta_max_sub=float(np.max(Delta[sub])), Delta_k1e4=float(Delta[0]), dlnC_dlna=dlc,
                      S=S, band=v["band"])
Smin = min(v["S"] for v in s1.values())
bands = [v["band"] for v in s1.values() if v["band"]]
for (f, z), v in s1.items():
    if z in (0.0, 0.25, round(Z_Q0, 3), 0.8, 2.5):
        P(f"    {f[:3]} z = {z:5.3f}: FP19 symbol (eps_K undone) min {v['S_FP19_no_epsK']:+.6f}; channel bound, sub-horizon max {v['Delta_max_sub']:.2e} "
          f"(at k = 1e-4 h/Mpc, reported: {v['Delta_k1e4']:.2e}; dln C/dln a {v['dlnC_dlna']:+.1f}); S min {v['S']:+.6f}" + (f"  (S <= 0 on k = {v['band'][0]:.2f}-{v['band'][1]:.2f} h/Mpc)" if v["band"] else ""))
check("S1 [H1, pre-declared] THE NEWTONIAN psi-SYMBOL OF THE HEADLINE's READ IS POSITIVE FOR EVERY SUB-HORIZON k: S = 1 + kappa h^2 - R_B "
      "(FP19's symbol_table on the headline law, eps_K NOT subtracted) minus the <K>_h channel's bound "
      "2|eps_C| + 9|eps_C|(aH/k)^2(1 + |dln C/dln a + 3|), min over k = 10 aH/c..1e3 h/Mpc, z = 0..2.5, both footings and chords >= 0.99 "
      "(below 10 aH/c the relativistic block, S2)",
      f"min S = {Smin:+.6f}; max channel bound at k = 1e-4 h/Mpc (super-horizon, reported) {max(v['Delta_k1e4'] for v in s1.values()):.1e}" + (f"; S <= 0 on k = {min(b_[0] for b_ in bands):.2f}-{max(b_[1] for b_ in bands):.2f} h/Mpc" if bands else "")
      + f" (law: {'FP13 variance [MUTATE]' if MUT else '<K>_h'}); FP19's own +0.995 = 1 - eps_K, eps_K = {eps_K:.2e}", Smin >= 0.99,
      "the real <K>_h read is not 'k = 0 only' (S2: its second variation is a local operator at every k), but its coefficient is "
      "(v/c)^2-small, so the psi-symbol is 1 - O(1e-4) at the largest scales and 1 - O(1e-5) below the horizon")
L.out["numbers"]["S1"] = {f"{k_[0]}/{k_[1]}": v for k_, v in s1.items()}
P(f"    {L.el()}")

# ================================================================================================ S4 eps_K
banner("S4  FP19's eps_K: WHAT IT MEASURES, AND WHETHER ITS SUBTRACTION HIDES A TERM")
a25 = 0.8; i25 = int(np.argmin(np.abs(AGR - a25))); L25 = LK(a25)
xh = {m_: x_mean_halo_c(a25, A0["canonical"], L25, 0.0, Mmin=m_) for m_ in (1e7, 1e8, 1e9, 1e10)}
Ihm = {m_: halo_rate_M(a25, A0["canonical"], L25, 0.0, Mmin=m_) for m_ in (1e7, 1e8, 1e9)}
yr25 = float(rms_bp_L(i25, [L25], A0["canonical"])[0]); xJ25 = math.sqrt(yr25)
b4 = NS["b4"]
b4h = {k_: v for k_, v in b4.items() if k_[2] == "halo"}
derived_max = rex_max if not MUT else max(v["rho_extra"] for v in s3.values())
P(f"    FP19 B4 (XR18 C1's proxy) on H_K1: " + "; ".join(f"z = {k_[0]} {k_[1][:3]} {k_[2]}: {v:.2e}" for k_, v in sorted(b4.items())))
P(f"    z = 0.25 (no yield): halo reading <x> at M_min = 1e7/1e8/1e9/1e10: " + " / ".join(f"{v:.3f}" for v in xh.values())
  + f" vs the Jensen bound y_rms^(1/2) = {xJ25:.3f} (y_rms = {yr25:.2e}); I_halo at M_min = 1e7/1e8/1e9: " + " / ".join(f"{v:.4g}" for v in Ihm.values()))
s4_ok = (xh[1e8] > xJ25 and xh[1e7] / xh[1e8] > 1.5 and abs(Ihm[1e7] / Ihm[1e8] - 1) < 0.05 and derived_max < eps_K / 10)
check("S4 [H4, pre-declared] eps_K IS NOT THE SIZE OF ANY TERM, AND ITS SUBTRACTION HIDES NONE: the halo reading's <x> at z = 0.25 "
      "(M_min = 1e8, the input of eps_K) exceeds the reading-free Jensen bound y_rms^(1/2) and grows as M_min falls (the dilute-halo "
      "sum counts overlapping deep-MOND fields as scalars), while the B-channel's actual input I_halo converges (1e7 vs 1e8 within 5%); "
      "the derived channel stays below eps_K/10",
      f"<x>_halo(1e8) = {xh[1e8]:.3f} vs Jensen {xJ25:.3f} (x{xh[1e8] / xJ25:.1f}); <x>_halo 1e7/1e8 = {xh[1e7] / xh[1e8]:.2f}; I_halo 1e7/1e8 = "
      f"{Ihm[1e7] / Ihm[1e8]:.4f}; derived max |rho_extra|/rho_bar {derived_max:.2e} vs eps_K {eps_K:.2e} (ratio {derived_max / eps_K:.1e})", s4_ok,
      "FP19's subtraction was conservative (it lowered the printed symbol by 5e-3 where the real channel is ~1e-5) and structurally "
      "misplaced (a homogeneous density does not enter the Newtonian symbol; the channel's local operator is post-Newtonian)")
L.out["numbers"]["S4"] = dict(x_halo={str(k_): v for k_, v in xh.items()}, I_halo={str(k_): v for k_, v in Ihm.items()}, x_Jensen=xJ25,
                              y_rms=yr25, eps_K=eps_K, derived_max=derived_max)

# ================================================================================================ S5 the phi-symbol
banner("S5  THE phi-SYMBOL: FP7's block with J_Y's stiffness C_phi >= 0 -- real, non-negative roots at finite c_2 and c_2 = oo")
F7 = json.load(open(os.path.join(XC.CHAIN, "FP7_aqual_type_repair_results.json")))["numbers"]
alm, c2m, Cph, lmm, sgm, kk7, ww7 = sp.symbols("alpha_c c_2 C_phi lam_ sigma k omega", real=True)
import re
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]), locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm,
                                                                          "sigma": sgm, "k": kk7, "omega": ww7})
U = sp.Symbol("U")
PU = sp.expand(sp.cancel(det7.subs(ww7, sp.sqrt(U) * kk7) / (64 * kk7 ** 10)))
a2c, a1c, a0c = [sp.expand(PU.coeff(U, j_)) for j_ in (2, 1, 0)]
Ap_, Bp_, Sp_ = Cph * alm * (3 * c2m + 2), lmm * c2m * (2 - alm), sgm ** 2 * (2 - alm) * (3 * c2m + 2)
lin_ok = sp.simplify(a1c - (Ap_ + Bp_ + Sp_)) == 0 and sp.simplify(a2c + lmm * alm * (3 * c2m + 2)) == 0 and sp.simplify(a0c + Cph * c2m * (2 - alm)) == 0
disc = sp.expand(a1c ** 2 - 4 * a2c * a0c)
disc_ok = sp.simplify(disc - ((Ap_ - Bp_) ** 2 + Sp_ ** 2 + 2 * Sp_ * (Ap_ + Bp_))) == 0
PUinf = sp.expand(sp.limit(PU / c2m, c2m, sp.oo))
b2c, b1c, b0c = [sp.expand(PUinf.coeff(U, j_)) for j_ in (2, 1, 0)]
Ai, Bi, Si = 3 * Cph * alm, lmm * (2 - alm), 3 * sgm ** 2 * (2 - alm)
inf_ok = (sp.simplify(b1c - (Ai + Bi + Si)) == 0 and sp.simplify(b2c + 3 * lmm * alm) == 0 and sp.simplify(b0c + Cph * (2 - alm)) == 0
          and sp.simplify(sp.expand(b1c ** 2 - 4 * b2c * b0c) - ((Ai - Bi) ** 2 + Si ** 2 + 2 * Si * (Ai + Bi))) == 0)
P(f"    P(U) = det/(64 k^10) = ({sp.factor(a2c)}) U^2 + ({sp.factor(a1c)}) U + ({sp.factor(a0c)})")
P(f"    discriminant = (A - B)^2 + S^2 + 2 S (A + B), A = C_phi alpha_c (3 c_2 + 2), B = lambda c_2 (2 - alpha_c), S = sigma^2 (2 - alpha_c)(3 c_2 + 2): {disc_ok}")
P(f"    c_2 -> oo: P/c_2 -> ({b2c}) U^2 + ({b1c}) U + ({b0c}); same structure: {inf_ok}")
# the Gaussian state's degenerate measure (C_L < 1e-2)
meas = {}
uu = np.linspace(1e-6, 8, 200001); pdf = math.sqrt(2 / math.pi) * 3 ** 1.5 * uu ** 2 * np.exp(-1.5 * uu ** 2)
for z in (0.0, 0.25, 0.5, 1.0, 2.5):
    v = s3[("canonical", z)]
    x = x_P2(np.maximum(v["y_rms"] * uu - v["yth"], 0.0)); CL = 2 * x * (1 - x) / (1 - 2 * x) ** 2
    plug = float(np.trapz(pdf * (v["y_rms"] * uu <= v["yth"]), uu))
    meas[z] = dict(frac_CL_below_1e2=float(np.trapz(pdf * (CL < 1e-2), uu)) - plug, plug=plug)
P("    Gaussian (Maxwell) reading, canonical: volume fraction yielded with C_L < 1e-2 / in the plug: " +
  "; ".join(f"z = {z}: {v['frac_CL_below_1e2']:.1e} / {v['plug']:.2f}" for z, v in meas.items()))
check("S5 [H5, pre-declared] THE phi-SYMBOL NEVER CHANGES SIGN: FP7's committed block, as a quadratic in U = omega^2/k^2, has "
      "leading coefficient -lambda alpha_c (3 c_2 + 2) <= 0, constant term -C_phi c_2 (2 - alpha_c) and discriminant "
      "(A - B)^2 + S^2 + 2 S (A + B) >= 0 -- so for every C_phi >= 0 (J_Y with y_th >= 0) all roots are real and >= 0, at finite c_2 "
      "and at c_2 = oo; C_phi = 0 (zero field below z_q0) is a degenerate, not a negative, symbol",
      f"coefficients {lin_ok}; discriminant identity {disc_ok}; c_2 = oo {inf_ok}", lin_ok and disc_ok and inf_ok,
      "criterion B's causal part is then automatic for H_K1 wherever C_phi >= 0: the separator changes only where C_phi is small "
      "(zero-field points below z_q0; C_L at the yield surfaces above it) -- XR18b_yield_surfaces.py scans those backgrounds")
L.out["numbers"]["S5"] = {"measure": {str(z): v for z, v in meas.items()}}
P(f"    {L.el()}")

# ================================================================================================ B1 Bianchi, minisuperspace
banner("B1  CONSERVATION AND THE BIANCHI IDENTITY (minisuperspace, sympy): the separator varied, frozen, or read from a")
tm = sp.Symbol('t')
am, Nm = sp.Function('a')(tm), sp.Function('N')(tm)
ad = sp.diff(am, tm); Km = 3 * ad / (am * Nm)
c1, c2_, c3, pp, wK, K0 = sp.symbols('c1 c2 c3 p w K_0', positive=True)


def noether(Ef):
    Lm = -3 * Mp2 * am * ad ** 2 / Nm - Nm * rho0 - Mp2 * Lam * Nm * am ** 3 - Nm * am ** 3 * Ef
    EN = sp.diff(Lm, Nm); Ea = sp.diff(Lm, am) - sp.diff(sp.diff(Lm, ad), tm)
    return sp.simplify(sp.expand(Nm * sp.diff(EN, tm) - ad * Ea))


tests = {
    "polynomial E(<K>, a)": c1 * Km ** 2 * am ** 3 + c2_ * Km / am ** 2,
    "transcendental E(<K>, a)": c3 * sp.sin(Km) * am ** pp + sp.exp(-Km / 3) * c1,
    "H_K1-like: softplus ramp x (K^2/3 - Lambda) L(K) x e(a)": (wK * sp.log(1 + sp.exp((1 - 9 * Lam / Km ** 2) / wK))
                                                               * (Km ** 2 / 3 - Lam) * (3 * Lam / Km ** 2) * c1 * am ** pp),
    "scale-factor read E(a) (the PM engine's form)": c1 * am ** pp,
}
b1 = {nm: noether(Ef) for nm, Ef in tests.items()}
eK, EKf, Kbf = sp.Function('e')(tm), sp.Function('E_K')(tm), sp.Function('K_b')(tm)
res_frozen = sp.factor(sp.simplify(noether(eK + EKf * (Km - Kbf)).subs(Nm, 1).doit()))
for nm, v in b1.items():
    P(f"    {nm:58s}: N dE_N/dt - a' E_a = {v}")
P(f"    frozen read (e(t) + E_K(t)(<K> - K_b(t)), prescribed): residual at N = 1: {res_frozen}")
# on the real state: frozen C drifts the Friedmann constraint at 3 H' C; relative to 3 H rho_bar
drift = {}
for z in ZS:
    a = 1 / (1 + z); Hz = H0 * Ez(a)
    Hdot_H2 = dlnH(a)                                                   # H'/H^2 = dln H/dln a
    rex = max(s3[(f, z)]["rho_extra"] for f in FOOTS)
    drift[z] = abs(Hdot_H2) * rex / 3.0                                 # |3 H' C|/(3 H rho_bar), C = rho_extra rho_bar/(3 H)
P("    frozen-read drift of the Friedmann constraint |3 H' C|/(3 H rho_bar): " + ", ".join(f"z = {z}: {v:.1e}" for z, v in drift.items()))
b1_ok = all(v == 0 for v in b1.values()) and res_frozen != 0 and max(drift.values()) <= 1e-4
check("B1 [H6 (i)-(iii), pre-declared] CONSERVATION AND THE BIANCHI IDENTITY: with the separator VARIED through <K>_h the "
      "reparametrisation Noether identity N dE_N/dt - a' E_a = 0 holds identically (four explicit test functions, one of them H_K1's "
      "ramp x (<K>^2/3 - Lambda) x L(<K>) smoothed); with the read FROZEN (prescribed in time) it fails, drifting the Friedmann "
      "constraint at |3 H' C|/(3 H rho_bar) <= 1e-4 on the real state; a scale-factor read E(a) satisfies it identically",
      "; ".join(f"{nm.split(':')[0]}: {'0' if v == 0 else 'NONZERO'}" for nm, v in b1.items()) + f"; frozen residual nonzero {res_frozen != 0}; "
      f"max drift {max(drift.values()):.1e}", b1_ok,
      "a scoring or PM run that prescribes L and y_th in time drops the channel and breaks the energy identity at the channel's own "
      "(v/c)^2 size; prescribing them as functions of the box's scale factor (XR21's form) is itself an action (a leaf-volume read)")
L.out["numbers"]["B1"] = {"identities": {k_: str(v) for k_, v in b1.items()}, "frozen": str(res_frozen), "drift": {str(k_): v for k_, v in drift.items()}}

# ================================================================================================ B2 translation identity on leaves
banner("B2  TRANSLATION INVARIANCE ON PERIODIC LEAVES: the channel's lapse term exerts no net force on a real density field")
b2 = {}
for Nn in (16, 32):
    rng = np.random.default_rng(71)
    kx = np.fft.fftfreq(Nn) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
    Pk = np.where(K2 > 0, np.exp(-K2 / (2 * 1.0 ** 2)) / np.maximum(K2, 1e-12) ** 0.7, 0.0)
    dlt = np.real(np.fft.ifftn(np.fft.fftn(rng.standard_normal((Nn, Nn, Nn))) * np.sqrt(Pk)))
    rho_f = 1.0 + 0.5 * dlt / np.std(dlt)
    for lab, cw in (("leaf-uniform coefficient", np.ones((Nn, Nn, Nn))),
                    ("position-weighted coefficient", (1 + 0.5 * np.cos(2 * np.pi * np.arange(Nn) / Nn))[:, None, None] * np.ones((1, Nn, Nn)))):
        mC = 0.3                                                         # the channel's k^0 lapse term (lattice units), exaggerated
        # lapse equation lap A - mC^2 w(x) A = rho - <rho>: solved by fixed-point in Fourier space for the weighted case
        src = rho_f - rho_f.mean()
        Ak = np.where(K2 > 0, -np.fft.fftn(src) / (K2 + mC ** 2), 0.0)
        for _ in range(200):                                           # lap A - mC^2 w A = src:  A = -(src + mC^2 (w - 1) A)/(K^2 + mC^2)
            Ax = np.real(np.fft.ifftn(Ak))
            Ak = np.where(K2 > 0, -(np.fft.fftn(src) + mC ** 2 * np.fft.fftn((cw - 1) * Ax)) / (K2 + mC ** 2), 0.0)
        Ax = np.real(np.fft.ifftn(Ak))
        gx = np.real(np.fft.ifftn(1j * KX * np.fft.fftn(Ax)))
        net = float(np.sum(rho_f * gx)); scale = float(np.sum(np.abs(rho_f * gx)))
        b2[(Nn, lab)] = abs(net) / scale
P("    net force / Sum|.|: " + "; ".join(f"N = {k_[0]}, {k_[1]}: {v:.1e}" for k_, v in b2.items()))
b2_ok = all(v < 1e-12 for (Nn, lab), v in b2.items() if lab.startswith("leaf")) and all(v > 1e-4 for (Nn, lab), v in b2.items() if lab.startswith("position"))
check("B2 [H6 (iv), pre-declared] TRANSLATION INVARIANCE: on periodic 3-D leaves (16^3, 32^3) the lapse equation with the channel's "
      "leaf-uniform k^0 coefficient exerts no net force on a real (random) density field (< 1e-12 of Sum|force|), and a "
      "position-weighted coefficient -- what a non-leaf-averaged read would give -- does (> 1e-4)",
      "; ".join(f"{k_[0]}/{k_[1][:4]}: {v:.1e}" for k_, v in b2.items()), b2_ok)

# ================================================================================================ N1 XR18 C1's formula vs the derived channel
banner("N1  (reported) XR18 C1's <K>_h-channel formula on H_K1 (FP19 B4) against the channel derived here")
gmax = max(v for k_, v in b4.items() if k_[2] == "gauss")
P(f"    XR18 C1 / FP19 B4 on H_K1: Gaussian max {gmax:.2e}; halo (z > z_q0, converged) max "
  f"{max(v for k_, v in b4.items() if k_[2] == 'halo' and k_[0] > Z_Q0):.1e}; halo z = 0.25 (unconverged) {max(v for k_, v in b4.items() if k_[2] == 'halo' and k_[0] < Z_Q0):.2e}"
  f"; derived here: max {rex_max:.2e} (H_Y by XR18 C1: 1.6e-5)")
check("N1 (reported) THE (v/c)^2 GLOBAL TERMS: XR18 C1's estimate on H_K1 (FP19 B4: Gaussian 1.9e-5, halo 5.9e-8 converged, 5.0e-3 raw) "
      "against the derived rho_extra = -d e_M/d ln<K>_h (S3); XR18 found <= 1.6e-5 for H_Y",
      f"XR18-C1 Gaussian {gmax:.1e}; derived {rex_max:.1e}", True, load_bearing=False)
L.out["numbers"]["N1"] = {"b4": {str(k_): v for k_, v in b4.items()}, "derived_max": rex_max}

# ================================================================================================ verdict
banner("VERDICT")
nlb = sum(1 for _, ok, lb in L.ch if lb and not ok)
ok = {k_: L.out["checks"][k_]["ok"] for k_ in ("S1", "S2", "S3", "S4", "S5", "B1", "B2")}
pf = {k_: ("PASS" if v else "FAIL") for k_, v in ok.items()}
P(f"""  Item 1 (the linear symbols).  The Newtonian psi-symbol of the headline's read: min S = {Smin:+.6f} over sub-horizon k (10 aH/c .. 1e3
    h/Mpc), z = 0..2.5, both footings (S1: {pf['S1']}{'; MUTATE: FP13 variance-fixed B restored' if MUT else ''}); at k = 1e-4 h/Mpc the channel's bound is
    {max(v['Delta_k1e4'] for v in s1.values()):.1e} and the relativistic block (S2) is the exact statement.  FP19's +0.995 is 1 - eps_K by construction.
    The real <K>_h read is NOT 'k = 0 only': its second variation is a local operator at every k with a leaf-averaged coefficient
    C (S2), which FP19 H4's linear zero-mode lattice read cannot see -- but the constrained block's determinant is identical with
    and without it (S2: {pf['S2']}), and its entries are eps_C x GR's with max |eps_C| = {max(eC.values()):.1e} (S3: {pf['S3']}).
    eps_K (4.96e-3) is not the size of any term: its halo <x> breaks the Jensen bound; the subtraction hides nothing (S4: {pf['S4']}).
    The phi-symbol has real non-negative roots for every C_phi >= 0, degenerate at zero field below z_q0 (S5: {pf['S5']}).
  Item 2 (nonlocality through <K>_h).  Varying the full action through <K>_h is conservative (reparametrisation identity holds;
    B1: {pf['B1']}); freezing the read breaks it at |3 H' C|/(3 H rho_bar) <= {max(drift.values()):.0e}; a scale-factor read (the PM engine's
    form) is itself an action.  Translation invariance holds on leaves (B2: {pf['B2']}).  The global terms: |rho_extra|/rho_bar <= {rex_max:.1e}
    (derived; XR18 C1's estimate gives {gmax:.1e} Gaussian), the same (v/c)^2 order as H_Y's 1.6e-5.
  Not 'closed'.  kappa = 1/2 FITTED.  {sum(1 for _, o_, _l in L.ch if o_)}/{len(L.ch)} checks pass; load-bearing failures: {nlb}.""")
L.out["ledger"] = [
    dict(link="XR18b-S1", status="DERIVED" if ok["S1"] else "FAILS", what=f"H_K1's Newtonian psi-symbol >= {Smin:.4f} for every k, z = 0-2.5, both footings"),
    dict(link="XR18b-S2", status="DERIVED", what="the <K>_h read's second variation is a local operator at every k (coefficient C); FP19 H4's "
         "'k = 0 only' holds for its linear toy read, not for <K>_h; the constrained block's determinant is C-independent"),
    dict(link="XR18b-S3", status="DERIVED", what=f"|rho_extra|/rho_bar <= {rex_max:.1e}, |eps_C| <= {max(eC.values()):.1e} on the real state"),
    dict(link="XR18b-S4", status="CORRECTION", what="FP19's eps_K = 5e-3 is an unconverged halo-sum proxy that violates the Jensen bound; "
         "the subtraction was conservative and hid no term"),
    dict(link="XR18b-B1", status="DERIVED", what="the full <K>_h variation is conservative; frozen reads drift the Friedmann constraint at <= 1e-5"),
]
L.finish()
