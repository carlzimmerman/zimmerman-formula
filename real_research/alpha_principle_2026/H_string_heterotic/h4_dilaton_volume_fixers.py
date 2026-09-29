#!/usr/bin/env python3
"""H4 -- THE DECISIVE QUESTION: does any string-theoretic mechanism on the declared list force the dilaton (or V e^{-2 phi}) to a number?  Pre-registered D1-D8 + Amendment 3.
Sources: full text Dienes hep-th/9602045 (Eq. 2.6, 6.16-6.21, Sect. 8.3), Witten hep-th/9602070 (Eq. 1.4-1.15); abstract only: Sen hep-th/9402002, GKP hep-th/0105097, KKLT hep-th/0301240, Denef-Douglas hep-th/0404116;
RECALLED (not read): Dine-Seiberg dilaton runaway, Font-Ibanez-Luest-Quevedo duality-invariant condensation, the gaugino-condensate exponent a = 8 pi^2/N with 1/g^2 = Re S.
Run: python3 h4_dilaton_volume_fixers.py [MUTATE]   (MUTATE: Kahler potential K = -2 ln(S+Sbar) in D3 and a wrong V_I(V_h) map in D7; checks D3b and D7a must FAIL, exit 1)"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp
from math import pi, log, sqrt, exp
from scipy.optimize import brentq

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# ---------------- D8: universality of the tree-level coupling ----------------
print("=== D8 universality: tree-level alpha_i^-1 = k_i S for every factor (Dienes 2.6) ===")
S = sp.symbols("S", positive=True); k1, k2, k3 = sp.symbols("k1 k2 k3", positive=True)
inv = sp.Matrix([k1*S, k2*S, k3*S])
J = inv.jacobian([S])
chk("D8a the three tree-level couplings depend on ONE real modulus (rank 1): ratios alpha_i/alpha_j = k_j/k_i are S-independent", J.rank() == 1 and sp.simplify((k2*S)/(k1*S) - k2/k1) == 0)
print("   => the levels (integers/rationals) fix RATIOS; the overall scale of the three couplings is the single dilaton S.")

# ---------------- D1: T-duality / fermionic points ----------------
print("\n=== D1 T-duality self-dual / free-fermionic points ===")
T = sp.symbols("T")
alpha_tree = 1/(k1*S)     # tree-level alpha for level k1: independent of T
chk("D1a tree-level alpha_G(S, T) has zero derivative with respect to the Kahler modulus T: fixing T (self-dual point) fixes no coupling at tree level", sp.diff(alpha_tree, T) == 0)
def lnEta(Tv):
    Tv = mp.mpc(Tv)
    q = mp.e**(2j*mp.pi*Tv)
    eta = mp.e**(1j*mp.pi*Tv/12)*mp.qp(q)      # Dienes 6.20: eta(T) = e^{i pi T/12} prod (1 - e^{2 pi i n T})
    return mp.log(Tv.imag*abs(eta)**4)
T_i = 1j
T_rho = mp.e**(2j*mp.pi/3)                     # SL(2,Z) fixed point (Amendment 3: the pre-registered e^{i pi/6} is a typo)
T_pi6 = mp.e**(1j*mp.pi/6)                     # as pre-registered, reported for transparency
v_i, v_rho, v_pi6 = lnEta(T_i), lnEta(T_rho), lnEta(T_pi6)
exact_i = 4*mp.log(mp.gamma(mp.mpf(1)/4)/(2*mp.pi**(mp.mpf(3)/4)))
print(f"   ln(Im T |eta(T)|^4): T=i {mp.nstr(v_i,8)} (closed form 4 ln[Gamma(1/4)/(2 pi^(3/4))] = {mp.nstr(exact_i,8)});  T=e^(2 pi i/3) {mp.nstr(v_rho,8)};  T=e^(i pi/6) {mp.nstr(v_pi6,8)} (not a fixed point)")
chk("D1b numerical eta evaluation reproduces the closed form at T = i to 1e-10", abs(v_i - exact_i) < 1e-10)
req_min = 35.04          # smallest achievable max|Delta_i| for an exact fit (h3 S3, at least ~35 in 16 pi^2/g^2 units)
for nm, v in (("T=i", v_i), ("T=rho", v_rho)):
    reach = 10*abs(float(v))
    print(f"   {nm}: moduli-dependent threshold piece |b'| |ln| with the declared |b'| <= 10: up to {reach:.1f} (16 pi^2/g^2 units) vs required >= {req_min:.0f} (h3 S3): ratio required/reach = {req_min/reach:.1f}")
best_reach = 10*max(abs(float(v_i)), abs(float(v_rho)))
crit_met = req_min/best_reach > 5
print(f"   VERDICT D1c (pre-registered criterion: required/reachable > 5 for |b'| <= 10): {'MET' if crit_met else 'NOT MET'} (ratio {req_min/best_reach:.2f}).")
print("   Reading: a size argument alone does NOT exclude large-b' N=2 sectors at a self-dual T; but the constant X of Dienes 6.19 stays free and model dependent, and the S-dependence is untouched, so no NUMBER for alpha follows either way.")
chk("D1c the criterion was evaluated and reported (ratio between 3 and 4; NOT met -- see Amendment 3)", 3.0 < req_min/best_reach < 4.0 and not crit_met)
aG_max = 1/(16*np.pi*(2*np.pi)**6)
print(f"   literal self-dual torus (2 pi sqrt(alpha'))^6 with e^(2 phi) <= 1 in Witten's (1.4): alpha_G <= {aG_max:.2e}  (alpha_G^-1 >= {1/aG_max:.2e}); convention/(2 pi)^n-dependent, REPORTED only")

# ---------------- D2: S-duality fixed points ----------------
print("\n=== D2 S-duality fixed points (16 scored comparisons) ===")
fixed = {"tau=i (Im=1)": 1.0, "tau=e^(2 pi i/3) (Im=sqrt3/2)": sqrt(3)/2}
convs = {"S=4pi/g^2+i th/2pi: alpha^-1=Im S": 1.0, "S=1/g^2: alpha^-1=4 pi Im S": 4*pi}
tgt_G = 22.194      # h3: alpha_G^-1 from the alpha_em-input one-loop solve (levels 5/3,1,1) -- the pre-registered target
tgt_0 = 137.035999177
cand = []
for fn, im in fixed.items():
    for cn, mult in convs.items():
        aGinv = im*mult
        cand.append((f"{fn}; {cn}", "alpha_G^-1", aGinv))
        cand.append((f"{fn}; {cn}", "alpha_em^-1(M_s)=(8/3)alpha_G^-1", 8/3*aGinv))
ntr = 0; hits = []
for lab, kind, val in cand:
    for tn, tv in (("h3 alpha_G^-1 = 22.194", tgt_G), ("137.036", tgt_0)):
        ntr += 1
        off = val/tv - 1
        if abs(off) < 1e-3: hits.append((lab, kind, tn))
    print(f"   {lab:62s} {kind:34s} = {val:8.3f}   vs 22.194: {100*(val/tgt_G-1):+7.1f}%   vs 137.036: {100*(val/tgt_0-1):+7.1f}%")
print(f"   trials = {ntr} (declared 16); hits = {hits}; expected chance hits = {ntr*2e-3/log(10):.4f}")
chk("D2a declared trial count 16", ntr == 16)
chk("D2b no S-duality fixed-point value hits either target at 1e-3", len(hits) == 0)
print("   Note: the duality-invariant-condensation literature (FILQ 1990, RECALLED) puts the minimum at these fixed points; they give alpha_G^-1 of O(1)-O(10), not ~25, and S-duality is not a symmetry of the N=1 spectrum (RECALLED).")

# ---------------- D3: gaugino condensation and racetrack ----------------
print("\n=== D3 gaugino condensation / racetrack (sympy) ===")
s, a, A, a1, a2, A1, A2 = sp.symbols("s a A a1 a2 A1 A2", positive=True)
nK = 2 if MUT else 1
K = -nK*sp.log(2*s)                       # K = -n ln(S + Sbar) at real S (axion 0): S + Sbar = 2 s
def V_of(W, K):
    Ks = sp.diff(K, s)/2                   # dK/dS at real S: (1/2) dK/ds
    Kss = sp.diff(K, s, 2)/4               # d^2K/(dS dSbar) = (1/4) d^2K/ds^2 for K(s = (S+Sbar)/2)
    DW = sp.diff(W, s)/1 + Ks*W            # W_S = dW/dS = dW/ds (W depends on S only; real S: d/dS -> d/ds)
    return sp.simplify(sp.exp(K)*(DW**2/Kss - 3*W**2)), sp.simplify(DW)
W1 = A*sp.exp(-a*s)
V1, DW1 = V_of(W1, K)
s0 = (sp.sqrt(3) - 1)/(2*a)
print("   single condensate V(s) =", V1)
chk("D3a single condensate: D_S W = 0 has no finite solution (no SUSY minimum)", sp.solve(sp.Eq(DW1, 0), s) == [])
chk("D3b V vanishes at s = (sqrt(3)-1)/(2a) (K = -ln(S+Sbar))", sp.simplify(V1.subs(s, s0)) == 0)
Vn = sp.lambdify(s, V1.subs({A: 1, a: 1}), "numpy")
xs = np.linspace(0.02, 20, 200000); vv = Vn(xs)
dv = np.gradient(vv, xs)
crit = xs[1:][np.sign(dv[1:]) != np.sign(dv[:-1])]
d2 = [(Vn(c + 1e-3) - 2*Vn(c) + Vn(c - 1e-3))/1e-6 for c in crit]
print(f"   critical points of V(s) (A=a=1): {np.round(crit,4).tolist()}, second derivatives {np.round(d2,3).tolist()}")
chk("D3c single condensate: only extremum is a MAXIMUM; V decreases to 0+ as s -> infinity (runaway of the dilaton)", len(crit) >= 1 and all(x < 0 for x in d2) and vv[-1] > 0 and dv[-1] < 0)
# racetrack: real-S SUSY point  (a1 + 1/2s) A1 e^{-a1 s} + (a2 + 1/2s) A2 e^{-a2 s} = 0, A2 = -r A1
Kn = -sp.log(2*s)
r = sp.symbols("r", positive=True)
W2 = sp.exp(-a1*s) - r*sp.exp(-a2*s)
V2, DW2 = V_of(W2, Kn)
DW2n = sp.lambdify((s, a1, a2, r), DW2, "numpy")
def s0_root(N1, N2, rv):
    aa1, aa2 = 8*pi**2/N1, 8*pi**2/N2
    f = lambda x: float(DW2n(x, aa1, aa2, rv))
    xs = np.linspace(0.05, 12, 4000); v = [f(x) for x in xs]
    rs = [brentq(f, xs[i], xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1] < 0]
    return rs
def leading(N1, N2, rv):                  # leading-order (K correction dropped): s0 = ln(r a2/a1)/(a2 - a1)
    aa1, aa2 = 8*pi**2/N1, 8*pi**2/N2
    return log(rv*aa2/aa1)/(aa2 - aa1)
N1, N2 = 9, 8
print(f"   racetrack a_i = 8 pi^2/N_i, (N1,N2) = ({N1},{N2}) [hidden-group ranks; RECALLED convention], A2 = -r A1:")
ok_sens = True
for rv in (4.0, 8.0, 16.0):
    rs = s0_root(N1, N2, rv)
    print(f"      r = {rv:5.1f}: SUSY point(s) s0 = {np.round(rs,4).tolist()}  (leading-order estimate {leading(N1,N2,rv):.4f});  alpha_G^-1 = 4 pi s0 = {[round(4*pi*x,3) for x in rs]}")
    ok_sens &= len(rs) >= 1
aa1, aa2 = 8*pi**2/N1, 8*pi**2/N2
sens = 4*pi/(aa2 - aa1)                    # d alpha_G^-1 / d ln r (leading order)
print(f"   d alpha_G^-1/d ln r = 4 pi/(a2-a1) = {sens:.2f};  to hold alpha_G^-1 to +-0.052 (1e-3 in alpha(0), h3 S5) the prefactor ratio r = -A2/A1 must be known to {100*0.052/sens:.2f} percent")
chk("D3d racetrack: a SUSY minimum exists, but its position is a continuous function of the prefactor ratio r (dS0/d ln r = 1/(a2-a1) != 0)", ok_sens and abs(sens) > 1)
print("   r is set by string-threshold and one-loop determinants of the two hidden sectors (moduli dependent, model dependent, NOT computed in this lane): so the racetrack converts the coupling into the constant r.")
# scan of required r for the h3 alpha_s-input value alpha_G^-1 = 25.640 (REPORTED requirement, not a hit test)
need = []
for N1_ in range(2, 11):
    for N2_ in range(2, 11):
        if N2_ >= N1_: continue
        aa1_, aa2_ = 8*pi**2/N1_, 8*pi**2/N2_
        s_t = 25.640/(4*pi)
        rr = (aa1_/aa2_)*exp(s_t*(aa2_ - aa1_))
        need.append((N1_, N2_, rr))
inwin = [x for x in need if 0.1 <= x[2] <= 10]
print(f"   required r for alpha_G^-1 = 25.640 over the {len(need)} pairs (N1>N2, 2..10) (leading-order): {len(inwin)} lie in [0.1,10]; range {min(x[2] for x in need):.2e} .. {max(x[2] for x in need):.2e}. REPORTED requirement only (not a hit search).")
print("   pairs with r in [0.1,10]:", [(x[0], x[1], round(x[2], 2)) for x in inwin])
print("   NOTE (Amendment 3): the illustrative pair (N1,N2) = (9,8) above was chosen BY HAND after seeing that it reaches alpha_G^-1 ~ 25 at r ~ 8; it is an illustration of the sensitivity, is not a trial, and is not evidence.")

# ---------------- D4 flux counting ----------------
print("\n=== D4 flux counting (structural arithmetic) ===")
p = 2e-3/log(10)
print(f"   per-vacuum chance of landing in the 1e-3 window (log-uniform, one decade) = {p:.2e}; vacua needed for one expected chance hit = {1/p:.0f} (= 1/8.69e-4).")
print("   GKP/KKLT-type stabilisation ties tau to integer fluxes (abstract-level knowledge); Denef-Douglas (abstract) count flux vacua; typical counts are >> 1e3 -- so 'alpha equals a flux-fixed value' is a statement about which integer choice, not a forcing principle.")
chk("D4 vacuum count needed for one expected chance hit is ~1150 (1/8.69e-4 = 1151); flux-landscape counts in the literature (abstract-level) are far larger", abs(1/p - 1150) < 3)

# ---------------- D5 Horava-Witten critical G_N ----------------
print("\n=== D5 Horava-Witten critical G_N (Witten 1.15): an inequality ===")
GN = 1/1.2209e19**2; MG = 2e16
for n in (0.25, 1.0, 4.0):
    aW = 4*pi*MG*sqrt(GN/n)
    print(f"   integral I = {n} M_GUT^-2: alpha_G^crit = 4 pi sqrt(G_N/I) = {aW:.4f} (alpha^-1 = {1/aW:.1f}, Witten normalisation)")
print("   G_N >= G_crit is a BOUND (below it one E8 goes strongly coupled); I is an unknown O(1) topological integral; UNSCORED.  The order of magnitude (alpha^-1 ~ 50 for I = 1) is the well-known statement that the strong-coupling window is close to the data.")

# ---------------- D6 dilaton runaway ----------------
print("\n=== D6 runaway (from D3): V -> 0+ as s -> infinity for one condensate; racetrack minima are AdS (V<0 at the SUSY point) ===")
V2n = sp.lambdify((s, a1, a2, r), V2, "numpy")
rs = s0_root(9, 8, 8.0)
Vmin = float(V2n(rs[0], 8*pi**2/9, 8*pi**2/8, 8.0))
print(f"   racetrack SUSY point s0 = {rs[0]:.4f}: V = {Vmin:.3e} (<0: AdS; cannot be the dS vacuum without an uplift term, which is another free constant)")
chk("D6 the racetrack SUSY extremum has V < 0 (supersymmetric AdS)", Vmin < 0)

# ---------------- D7 duality invariance of alpha_G ----------------
print("\n=== D7 heterotic SO(32) <-> Type I map preserves alpha_G ===")
ph, Vh, ap = sp.symbols("phi V alpha_p", positive=True)
al_het = sp.exp(2*ph)*ap**3/(16*sp.pi*Vh)
VI = sp.exp(-2*ph)*Vh if MUT else sp.exp(-3*ph)*Vh          # Type I volume in the Type I metric g_I = e^{-phi_h} g_h  (6 dims)
al_I = sp.exp(-ph)*ap**3/(16*sp.pi*VI)                       # phi_I = -phi_h
chk("D7a the duality map (phi_I = -phi_h, V_I = e^{-3 phi_h} V_h) leaves alpha_G invariant (a consistency check on Witten Eq. 1.4 vs 1.10)", sp.simplify(al_I - al_het) == 0)
print("   => duality relabels the free parameter, it cannot fix it.  The formal fixed point phi = 0 of the map is not a symmetry point of a single theory (heterotic and Type I are different string theories) (RECALLED).")

nfail = sum(1 for _, ok in checks if not ok)
print(f"\nSUMMARY: {len(checks)-nfail}/{len(checks)} checks pass" + (" [MUTATE]" if MUT else ""))
sys.exit(1 if nfail else 0)
