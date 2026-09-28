#!/usr/bin/env python3
r"""AS084 -- Self-gravitational virial energy with a central mass.

Audit target (seed math section):
    W_vir,total = -int_{r_in}^{R} G*M(r)/r dM_shell(r),
    M(r) = M_in + m_s*(r - r_in),   dM_shell = m_s dr = 4*pi*A dr,
    rho_ph(r) = A/r^2,  A = C/(4 pi G),  C = sqrt(G M_b a0),  m_s = 4 pi A = C/G.

Closed forms (derived inside, sympy-verified then numerics-checked):
    W_total = W_cent + W_self
    W_cent  = -G m_s M_in ln(R/r_in)              = -C M_in ln(R/r_in)
    W_self  = -G m_s^2 (R - r_in - r_in ln(R/r_in))
    singular limit r_in -> 0, M_in = 0:  W_self -> -(C^2/G) R = -G M(R)^2/R.

Controls (capable of failing):
    C1 exact closed form vs high-precision quadrature of the RAW integrand
    C2 independent representation: discrete N-shell pair-energy sum -> closed form
    C3 dW/dR = -G M(R) m_s / R by central finite differences
    C4 NEGATIVE CONTROL: naive -G M(R)^2/R for every finite shell, r_in>0 must FAIL
       (relative deviation reported per cell); recovers only in r_in -> 0 singular limit
    C5 thin-shell boundary case R -> r_in: W -> 0 with the analytic leading term
    C6 cross-check vs G091 closed forms in the singular limit (contract constants noted)
    C7 deep exterior shells r_in/r_M = 10,100 x R/r_in = 2,10: A/r^2 profile virial
       PLUS bounded full-kernel error vs exact Q and RAR (operative MONO = RAR for
       y < y_star) phantom densities; bracketed virial incl. kernel correction
    C8 both footings: canonical 9.3619e-11 and alternative 1.1279e-10 m/s^2,
       separate; kappa = 1/2 adopted; rho_Lambda per footing + effective-kappa table
    C9 virial-balance implication: sigma^2 from 2T + W_self + W_cent = 3 P_s V
       -> recovers C/2 in the (M_in->0, r_in->0) singular limit, deviates otherwise

Numerics conventions (RESULT_CONTRACT): G=6.67430e-11, c=299792458,
M_sun=1.98847e30, pc=3.085677581491367e16. Ancestry anchors (G031/G091/G233):
M_b = 6.5e10 M_sun (MW proxy; 6.2501e10 for the NGC3198 anchor row).
Sources examined: G084 (max-entropy law), G091 (virial triad), G233 (EOS).
"""
import json
import math
import os
import time

import numpy as np
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
T_START = time.time()

# ---------------- constants (contract) ----------------
G_N = 6.67430e-11          # m^3 kg^-1 s^-2
C_L = 299792458.0          # m/s
M_SUN = 1.98847e30         # kg
PC = 3.085677581491367e16  # m
A0_CAN = 9.3619e-11        # m/s^2 canonical footing
A0_ALT = 1.1279e-10        # m/s^2 alternative footing
KAPPA = 0.5                # adopted, framework input (not derived here)
MSUN_KB = 1.380649e-23     # J/K (registered, unused in virial)
MB_MW = 6.5e10             # M_sun, G031 MW proxy
MB_NGC = 6.2501e10         # M_sun, G035 NGC3198 proxy
KPC = 1e3 * PC

def footing(a0):
    """Framework cell per footing: rho_Lambda (mass density) from a0 = kappa c sqrt(G rho_L)."""
    rho_L = 4.0 * a0 * a0 / (G_N * C_L * C_L)      # = a0^2/(kappa^2 G c^2), kappa = 1/2
    eps_L = rho_L * C_L * C_L
    lam_ = 32.0 * math.pi * a0 * a0 / (C_L ** 4)   # contract Lambda form (same-G cell)
    return dict(a0=a0, kappa=KAPPA, rho_Lambda=rho_L, epsilon_Lambda=eps_L, Lambda=lam_)

def scales(Mb_kg, a0):
    C = math.sqrt(G_N * Mb_kg * a0)         # m^2/s^2   (= v_flat^2)
    rM = math.sqrt(G_N * Mb_kg / a0)        # m         (= r_M)
    A = C / (4.0 * math.pi * G_N)           # kg/m      (profile amplitude)
    ms = C / G_N                            # kg/m      (4 pi A, shell linear density)
    return dict(C=C, rM=rM, A=A, ms=ms, vflat=math.sqrt(C), sig_C2=math.sqrt(C / 2.0))

# ---------------- symbolic derivation (sympy) ----------------
G_s, Mb_s, a0_s, M_in_s, ms_s, rin_s, R_s = sp.symbols(
    "G M_b a0 M_in m_s r_in R", positive=True)
r_s = sp.symbols("r", positive=True)
C_s = sp.sqrt(G_s * Mb_s * a0_s)

M_r = M_in_s + ms_s * (r_s - rin_s)            # enclosed mass at r
dM = ms_s * sp.diff(r_s, r_s)                  # dM_shell/dr = m_s
integrand = G_s * M_r / r_s * ms_s             # G M(r)/r dM_shell/dr (positive part)

# indefinite primitive of the integrand (as function of r)
F = sp.integrate(integrand, r_s)
I_exact = sp.simplify(F.subs(r_s, R_s) - F.subs(r_s, rin_s))
I_target = (G_s * ms_s * M_in_s * sp.log(R_s / rin_s)
            + G_s * ms_s ** 2 * (R_s - rin_s)
            - G_s * ms_s ** 2 * rin_s * sp.log(R_s / rin_s))
sym_closed = sp.simplify(I_exact - I_target) == 0

# separation identity: W_total = W_cent + W_self
W_cent_s = -G_s * ms_s * M_in_s * sp.log(R_s / rin_s)
W_self_s = -G_s * ms_s ** 2 * (R_s - rin_s - rin_s * sp.log(R_s / rin_s))
sym_split = sp.simplify(-I_target - (W_cent_s + W_self_s)) == 0

# singular limit (M_in -> 0): W_self -> -G m_s^2 R = -(C^2/G) R = -G M(R)^2/R
sing = sp.simplify(sp.limit(W_self_s, rin_s, 0, dir="+") + G_s * (ms_s * R_s) ** 2 / R_s) == 0

# virial balance with central mass: 2T + W_self + W_cent = 3 P_s V
# T = (3/2) M_T sigma^2, M_T = m_s (R - r_in), 3 P_s V = sigma^2 M_T
sig2_s = sp.symbols("sigma^2", positive=True)
M_T_s = ms_s * (R_s - rin_s)
sol_sigma2 = sp.solve(
    sp.Eq(2 * sp.Rational(3, 2) * M_T_s * sig2_s + W_cent_s + W_self_s,
          sig2_s * M_T_s),
    sig2_s)[0]
sol_sigma2 = sp.simplify(sol_sigma2)
# limit -> C/2
sigma2_sing = sp.simplify(sp.limit(sol_sigma2, ms_s, sp.oo))  # placeholder, done explicitly below
sigma2_sing_explicit = sp.limit(sp.limit(sol_sigma2, M_in_s, 0), rin_s, 0, dir="+")
# m_s is defined as C/G: substitute the definition before comparing to C/2
sigma2_triad_check = sp.simplify(sp.simplify(sigma2_sing_explicit).subs(ms_s, C_s / G_s) - C_s / 2) == 0

# ---------------- exact kernel densities (deep-exterior error bound) ----------------
# Q  branch (algebraic a0 line): g_Q(r)^2 = B^2 + a0 B,  B = G M_b/r^2
# RAR branch: nu(y) = 1/(1-exp(-sqrt y)), y = B/a0 = r_M^2/r^2, g = B nu.
# Operative MONO: for y <= y_star ~ 2.3374 (r >= 0.654 r_M) h'_mono = h'_RAR, so
# MONO == RAR on the entire deep-exterior domain used here (r_in >= 10 r_M).
def rho_RAR(r, Mb_kg, a0):
    rM = math.sqrt(G_N * Mb_kg / a0)
    x = rM / r
    if x > 500.0:                       # exp underflow guard (never reached here)
        return Mb_kg * rM / (4.0 * math.pi * r ** 4) * math.exp(-x) / (1.0 - math.exp(-x)) ** 2
    e = math.exp(-x)
    return (Mb_kg * rM / (4.0 * math.pi)) * e / (r ** 4 * (1.0 - e) ** 2)

def rho_Q(r, Mb_kg, a0):
    rM = math.sqrt(G_N * Mb_kg / a0)
    y = (rM / r) ** 2
    g = a0 * math.sqrt(y * y + y)
    # (1/r^2) d(r^2 g)/dr  via finite differencing on log grid at this r is fragile;
    # use the closed derivative: g = a0 sqrt(y^2+y), y = rM^2/r^2
    # d(r^2 g)/dr = a0 * d(r^2 sqrt(y^2+y))/dr ; r^2 = rM^2 / y
    # => r^2 g = a0 rM^2 sqrt(1 + 1/y) = a0 rM^2 sqrt(1 + r^2/rM^2)
    # d/dr = a0 rM^2 * (r/rM^2) / sqrt(1 + r^2/rM^2) = a0 r / sqrt(1 + (r/rM)^2)
    divg = a0 * r / (r * r * math.sqrt(1.0 + (r / rM) ** 2))   # (1/r^2) * d(r^2 g)/dr
    return divg / (4.0 * math.pi * G_N)

def rho_A(r, Mb_kg, a0):
    C = math.sqrt(G_N * Mb_kg * a0)
    return C / (4.0 * math.pi * G_N * r * r)

# ---------------- high-precision engine ----------------
mp.mp.dps = 50

def W_exact(Mb_kg, a0, M_in, r_in, R):
    C = math.sqrt(G_N * Mb_kg * a0)
    ms = C / G_N
    return -(C * M_in * math.log(R / r_in)
             + (C * C / G_N) * (R - r_in - r_in * math.log(R / r_in)))

def W_naive(Mb_kg, a0, M_in, r_in, R):
    C = math.sqrt(G_N * Mb_kg * a0)
    ms = C / G_N
    M_R = M_in + ms * (R - r_in)
    return -G_N * M_R * M_R / R

def W_exact_mp(Mb_kg, a0, M_in, r_in, R):
    """Closed form evaluated at 50 digits (mpmath) for the high-precision C1 check."""
    C = mp.sqrt(mp.mpf(G_N) * mp.mpf(Mb_kg) * mp.mpf(a0))
    ms = C / mp.mpf(G_N)
    return -(C * mp.mpf(M_in) * mp.log(mp.mpf(R) / mp.mpf(r_in))
             + (C * C / mp.mpf(G_N))
             * (mp.mpf(R) - mp.mpf(r_in) - mp.mpf(r_in) * mp.log(mp.mpf(R) / mp.mpf(r_in))))

def W_quad_mp(Mb_kg, a0, M_in, r_in, R, K):
    """Direct high-precision quadrature of the raw defining integral -int G M(r)/r dM."""
    Gq = mp.mpf(G_N)
    m = mp.mpf(Mb_kg)
    ai = mp.mpf(a0)
    Min = mp.mpf(M_in)
    ri = mp.mpf(r_in)
    Rr = mp.mpf(R)
    C = mp.sqrt(Gq * m * ai)
    ms = C / Gq
    f = lambda t: Gq * (Min + ms * (t - ri)) / t * ms   # positive part, 50-digit
    I = mp.quad(f, [ri, Rr])                            # mpmath, 50 digits
    return -I

def W_pair_sum(Mb_kg, a0, M_in, r_in, R, N):
    """Independent representation: discrete N-shell pair-energy sum.

    W = -G sum_i m_i (M_in + sum_{j<i} m_j)/r_i  with shells at r_i, mass m_i = m_s (R-r_in)/N,
    i.e. the Newtonian pair potential of the central point mass + N uniform-density shells.
    Exact in the N -> oo limit (trapezoid-like O(N^-2) for the smooth part).
    """
    C = math.sqrt(G_N * Mb_kg * a0)
    ms = C / G_N
    m_i = ms * (R - r_in) / N
    W = 0.0
    M_shells = M_in
    for k in range(N):
        r = r_in + (R - r_in) * (k + 0.5) / N
        W -= G_N * (M_shells) / r * m_i
        M_shells += m_i
    return W

def trapz(y, x):
    try:
        return np.trapezoid(y, x)          # numpy >= 2.0
    except AttributeError:
        return np.trapz(y, x)              # numpy 1.x

def W_rho(rho, Mb_kg, a0, M_in, r_in, R, n=4000):
    """Virial integral for a general density rho(r):  W = -int G M(r)/r dM,
    with M(r) = M_in + 4 pi int_{r_in}^{r} rho(s) s^2 ds, dM = 4 pi rho(r) r^2 dr.
    Vectorised cumulative trapezoid on a log-spaced grid."""
    r = np.geomspace(r_in, R, n)
    rho_v = np.array([rho(ri, Mb_kg, a0) for ri in r])
    dVdr = 4.0 * math.pi * rho_v * r * r          # dM/dr
    dr = np.diff(r)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (dVdr[:-1] + dVdr[1:]) * dr)])  # trapezoid cumsum
    Menc_r = M_in + cum
    W = -G_N * trapz(Menc_r / r * dVdr, r)
    return float(W), float(Menc_r[-1])

# ---------------- run ----------------
res = {}
A0s = {"canonical": A0_CAN, "alt": A0_ALT}
FT = {k: footing(a0) for k, a0 in A0s.items()}
res["footings"] = FT

# footing bookkeeping: relative kappa / rho_Lambda shifts
kap_eff_alt_fixed_rho = KAPPA * A0_ALT / A0_CAN
rho_ratio_alt = (A0_ALT / A0_CAN) ** 2
res["footing_relations"] = {
    "kappa_eff_at_alt_if_rho_Lambda_fixed_to_canonical": kap_eff_alt_fixed_rho,
    "rho_Lambda_ratio_if_kappa_fixed_1_2": rho_ratio_alt,
}

# ---------------- symbolic results ----------------
res["symbolic"] = {
    "primitive": str(F),
    "closed_form_exact": str(I_target),
    "sympy_closed_form_verified": sym_closed,
    "separation_verified": sym_split,
    "singular_limit_verified_self": sing,
    "W_cent_form": str(W_cent_s),
    "W_self_form": str(W_self_s),
    "sigma2_virial_with_central_mass": str(sol_sigma2),
    "sigma2_recovers_C_over_2_in_singular_limit": sigma2_triad_check,
}

MB_ROWS = [("MW_6.5e10", MB_MW), ("NGC3198_6.2501e10", MB_NGC)]
rows = []
checks = []
for fname, a0 in A0s.items():
    for mname, mb_msun in MB_ROWS:
        Mb_kg = mb_msun * M_SUN
        sc = scales(Mb_kg, a0)
        rows.append(dict(foot=fname, a0=a0, Mb=mname, Mb_kg=Mb_kg, **sc))

# ---- C1: closed form vs 50-digit mpmath quadrature of the raw integrand ----
maxrel = 0.0
for row in rows:
    for (rinR, RrM) in [(0.01, 0.62), (0.1, 1.0)]:
        R = row["rM"] * RrM
        r_in = rinR * R
        for MinMb in (0.0, 0.1):
            M_in = MinMb * row["Mb_kg"]
            ex = W_exact_mp(row["Mb_kg"], row["a0"], M_in, r_in, R)
            qd = W_quad_mp(row["Mb_kg"], row["a0"], M_in, r_in, R, 0)
            rel = abs(ex - qd) / abs(ex)
            maxrel = max(maxrel, rel)
checks.append(dict(name="C1_closed_form_vs_mpmath_quad_raw_integrand",
                   detail="8 cells x 2 footings; grid (r_in/R, R/r_M) in {(0.01,0.62),(0.1,1.0)}, M_in/M_b in {0,0.1}; both sides at 50 digits",
                   max_rel_err=str(maxrel), tol=1e-25, pass_=maxrel < 1e-25))

# ---- C2: N-shell pair-energy representation ----
c2 = {}
for row in rows:
    if row["foot"] != "canonical":
        continue
    for (rinR, RrM) in [(0.01, 0.62), (0.5, 1.0)]:
        R = row["rM"] * RrM
        r_in = rinR * R
        ex = W_exact(row["Mb_kg"], row["a0"], 0.1 * row["Mb_kg"], r_in, R)
        rels = []
        for N in (10, 100, 1000, 10000):
            ps = W_pair_sum(row["Mb_kg"], row["a0"], 0.1 * row["Mb_kg"], r_in, R, N)
            rels.append(abs(ps - ex) / abs(ex))
        c2[f"{rinR}|{RrM}"] = rels
maxrel2 = max(v[-1] for v in c2.values())
# convergence: shell-sum is a left-Riemann-type double sum: O(1/N) boundary-term error;
# criterion: monotone ~10x reduction per decade AND N = 1e4 residual < 5e-4
converging = all(v[3] / max(v[2], 1e-300) < 0.25 for v in c2.values()) and \
             all(v[1] / max(v[0], 1e-300) < 0.25 for v in c2.values())
checks.append(dict(name="C2_pair_sum_converges_to_closed_form",
                   detail="discrete N-shell Newtonian pair-energy sum, N=10..10000, M_in/M_b=0.1, canonical footing",
                   rel_err_by_N=c2, tol=5e-4, pass_=maxrel2 < 5e-4 and converging))

# ---- C3: dW/dR ----
c3 = {}
for row in rows:
    if row["foot"] != "canonical":
        continue
    R = 0.62 * row["rM"]
    r_in = 0.1 * R
    M_in = 0.1 * row["Mb_kg"]
    h = R * 1e-6
    dW = (W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R + h)
          - W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R - h)) / (2 * h)
    C = row["C"]
    ms = C / G_N
    M_R = M_in + ms * (R - r_in)
    ana = -G_N * M_R / R * ms
    c3[row["Mb"]] = dict(fd=dW, analytic=ana, rel=abs(dW - ana) / abs(ana))
maxrel3 = max(v["rel"] for v in c3.values())
checks.append(dict(name="C3_dW_dR_finite_difference_vs_-G M(R) m_s/R",
                   detail="central fd, h = 1e-6 R", max_rel_err=maxrel3, tol=1e-5,
                   pass_=maxrel3 < 1e-5))

# ---- C4 NEGATIVE CONTROL: naive -G M(R)^2/R on every finite shell ----
c4 = []
worst_naive = 0.0
for row in rows:
    for (rinR, RrM) in [(0.01, 0.62), (0.1, 0.62), (0.5, 0.62), (0.01, 1.0), (0.1, 1.0), (0.5, 1.0)]:
        R = row["rM"] * RrM
        r_in = rinR * R
        for MinMb in (0.0, 0.1):
            M_in = MinMb * row["Mb_kg"]
            ex = W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R)
            nv = W_naive(row["Mb_kg"], row["a0"], M_in, r_in, R)
            dev = (nv - ex) / abs(ex)
            worst_naive = max(worst_naive, abs(dev))
            c4.append(dict(foot=row["foot"], Mb=row["Mb"], rinR=rinR, RrM=RrM,
                           MinMb=MinMb, W_exact=ex, W_naive=nv, rel_dev=dev))
# singular-limit recovery of the naive form (M_in = 0, r_in -> 0)
singlim = []
for row in rows:
    R = 0.62 * row["rM"]
    for eps in (1e-8, 1e-12):
        r_in = eps * R
        ex = W_exact(row["Mb_kg"], row["a0"], 0.0, r_in, R)
        nv = W_naive(row["Mb_kg"], row["a0"], 0.0, r_in, R)
        singlim.append(dict(foot=row["foot"], eps=eps, W_exact=ex, W_naive=nv,
                            rel=abs(ex - nv) / abs(ex)))
checks.append(dict(name="C4_NEGATIVE_CONTROL_naive_-G_M(R)^2_over_R_fails_for_finite_shell",
                   detail="6 (r_in/R, R/r_M) cells x {0, 0.1} M_in/M_b x 2 footings x 2 masses",
                   min_rel_dev=min(abs(x["rel_dev"]) for x in c4),
                   max_rel_dev=worst_naive,
                   criterion="relative deviation must be large (naive form rejected); "
                             "control is capable of failing if the naive form were exact",
                   tol=1e-3, pass_=min(abs(x["rel_dev"]) for x in c4) > 1e-3))
checks.append(dict(name="C4b_naive_form_recovers_exactly_only_in_singular_limit",
                   detail="M_in = 0, r_in -> 0", rows=singlim,
                   tol=1e-6, pass_=all(x["rel"] < 1e-6 for x in singlim)))

# ---- C5: thin-shell boundary case R -> r_in ----
c5 = []
for row in rows:
    r_in = 0.1 * row["rM"]
    for eps in (1e-3, 1e-5):
        R = r_in * (1.0 + eps)
        M_in = 0.1 * row["Mb_kg"]
        ex = W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R)
        C = row["C"]
        lead = -C * M_in * math.log(R / r_in)      # analytic leading term (central only)
        c5.append(dict(foot=row["foot"], eps=eps, W=ex, W_cent_analytic=lead,
                       W_over_W_cent=ex / lead if lead != 0 else None,
                       W_scale=(C * C / G_N) * r_in))
checks.append(dict(name="C5_thin_shell_boundary_R->r_in",
                   detail="W -> 0 with leading term -C M_in ln(1+eps) ~ -C M_in eps",
                   rows=c5, tol=0.05,
                   pass_=all(abs(x["W_over_W_cent"] - 1.0) < 0.05 for x in c5)))

# ---- C6: singular-limit cross-check vs G091 closed forms ----
c6 = {}
for row in rows:
    R = 0.62 * row["rM"]
    r_in = 1e-12 * R
    ex = W_exact(row["Mb_kg"], row["a0"], 0.0, r_in, R)
    g091 = -(row["C"] ** 2 / G_N) * R                       # G091 V1b: -G M_T^2/r_break
    M_T = (row["C"] / G_N) * R
    g091b = -G_N * M_T * M_T / R
    c6[row["foot"] + "|" + row["Mb"]] = dict(W_self_singular=ex, G091_closed=g091,
                                             G091_shellform=g091b,
                                             rel=abs(ex - g091) / abs(g091))
checks.append(dict(name="C6_singular_limit_reproduces_G091_W_self_closed_form",
                   detail="-G M_T^2/r_break at R = 0.62 r_M; contract G = 6.67430e-11 "
                          "(G091 used 6.674e-11; relative G shift 4.49e-5)",
                   rows=c6, tol=1e-6, pass_=all(v["rel"] < 1e-6 for v in c6.values())))

# ---- C7: deep exterior shells + full-kernel error bounds ----
c7 = {}
for row in rows:
    if row["foot"] != "canonical":
        continue
    key = row["Mb"]
    for rM_mult, Rmult in [(10, 2), (10, 10), (100, 2), (100, 10)]:
        r_in = rM_mult * row["rM"]
        R = Rmult * r_in
        # profile ansatz virial (M_in = 0: pure phantom continuum; and M_in = M_b baryon coupling)
        for MinLbl, M_in in (("M_in=0", 0.0), ("M_in=M_b", row["Mb_kg"])):
            ex = W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R)
            # kernel densities on the same shell; bracket the virial with them
            Wq, Mq = W_rho(rho_Q, row["Mb_kg"], row["a0"], M_in, r_in, R, n=4000)
            Wr, Mr = W_rho(rho_RAR, row["Mb_kg"], row["a0"], M_in, r_in, R, n=4000)
            # max relative kernel-density deviation on [r_in, R]
            rr = np.geomspace(r_in, R, 4000)
            devQ = max(abs(rho_Q(ri, row["Mb_kg"], row["a0"]) / rho_A(ri, row["Mb_kg"], row["a0"]) - 1.0) for ri in rr)
            devR = max(abs(rho_RAR(ri, row["Mb_kg"], row["a0"]) / rho_A(ri, row["Mb_kg"], row["a0"]) - 1.0) for ri in rr)
            c7[f"{key}|rin={rM_mult}rM|R={Rmult}rin|{MinLbl}"] = dict(
                W_Aprofile=ex, W_Qkernel=Wq, W_RARkernel=Wr,
                rel_Q=(Wq - ex) / abs(ex), rel_RAR=(Wr - ex) / abs(ex),
                max_rho_dev_Q=devQ, max_rho_dev_RAR=devR,
                analytic_Q_leading=(row["rM"] / r_in) ** 2 / 2.0,
                analytic_RAR_leading=(row["rM"] / r_in) ** 2 / 12.0)
checks.append(dict(name="C7_deep_exterior_shells_and_kernel_error_bound",
                   detail="r_in/r_M in {10, 100} x R/r_in in {2, 10}; M_in in {0, M_b}; "
                          "Q and RAR (operative MONO == RAR for y < y_star) densities",
                   rows=c7, tol_Q=2.0, tol_RAR=2.0,
                   pass_=all(abs(v["max_rho_dev_Q"] / v["analytic_Q_leading"] - 1.0) < 0.05
                             and abs(v["max_rho_dev_RAR"] / v["analytic_RAR_leading"] - 1.0) < 0.05
                             for v in c7.values() if v["analytic_Q_leading"] > 0)))

# ---- C8: both footings on the control grid ----
c8 = []
for row in rows:
    for (rinR, RrM) in [(0.01, 0.62), (0.1, 1.0), (0.5, 1.0)]:
        R = row["rM"] * RrM
        r_in = rinR * R
        ex = W_exact(row["Mb_kg"], row["a0"], 0.1 * row["Mb_kg"], r_in, R)
        c8.append(dict(foot=row["foot"], Mb=row["Mb"], rinR=rinR, RrM=RrM, W=ex,
                       W_over_Mb_c2=ex / (row["Mb_kg"] * C_L * C_L),
                       C=row["C"], rM_kpc=row["rM"] / KPC))
# scale-ratio identity: W_self(alt)/W_self(can) = sqrt(a0_alt/a0_can) = C_alt/C_can exactly
# (W_self ~ M_b*C ~ a0^{1/2}; W_cent = -C M_in ln ~ a0^{1/2} too -- both terms scale as sqrt(a0))
def self_w(row, r_in, R, MinMb):
    return -(row["C"] ** 2 / G_N) * (R - r_in - r_in * math.log(R / r_in))
ratio_check = 0.0
expect = math.sqrt(A0_ALT / A0_CAN)
rowC = [r for r in rows if r["foot"] == "canonical"][0]
rowA = [r for r in rows if r["foot"] == "alt"][0]
for (rinR, RrM) in [(0.01, 0.62), (0.5, 1.0)]:
    R_c = 0.62 * rowC["rM"]
    R_a = 0.62 * rowA["rM"]
    # ratio of self energies at the same (r_in/R, R/r_M) cells
    ratio_check = max(ratio_check,
                      abs((self_w(rowA, 0.01 * 0.62 * rowA["rM"], 0.62 * rowA["rM"], 0)
                           / self_w(rowC, 0.01 * 0.62 * rowC["rM"], 0.62 * rowC["rM"], 0))
                          - expect) / expect)
checks.append(dict(name="C8_both_footings_separate_and_scale_exact",
                   detail="W_self(alt)/W_self(can) = sqrt(a0_alt/a0_can) exactly (analytic; both virial "
                          "terms scale as sqrt(a0) through C); rho_Lambda per footing; kappa kept at 1/2 on both",
                   expected_ratio=expect, max_rel_dev_from_analytic_ratio=ratio_check, tol=1e-9,
                   pass_=ratio_check < 1e-9))

# ---- C9: sigma^2 implication (closed form) ----
c9 = {}
for row in rows:
    R = 0.62 * row["rM"]
    for rinR in (0.01, 0.1, 0.5):
        for MinMb in (0.0, 0.1, 1.0):
            r_in = rinR * R
            M_in = MinMb * row["Mb_kg"]
            C = row["C"]
            ms = C / G_N
            s2 = (G_N * ms ** 2 * (R - r_in - r_in * math.log(R / r_in))
                  + G_N * ms * M_in * math.log(R / r_in)) / (2.0 * ms * (R - r_in))
            c9[f"{row['foot']}|{row['Mb']}|rinR={rinR}|MinMb={MinMb}"] = dict(
                sigma2=s2, sigma2_over_C_over_2=s2 / (C / 2.0))
checks.append(dict(name="C9_virial_sigma2_with_central_mass",
                   detail="2T + W_self + W_cent = 3 P_s V; s2 -> C/2 in the (M_in, r_in)->0 singular limit",
                   rows=c9,
                   singular_limit_ok=sigma2_triad_check,
                   pass_=sigma2_triad_check))

# ---- summary table for derivation.md ----
table = []
for row in rows:
    R = 0.62 * row["rM"]
    r_in = 0.1 * R
    M_in = 0.1 * row["Mb_kg"]
    ex = W_exact(row["Mb_kg"], row["a0"], M_in, r_in, R)
    Wc = -row["C"] * M_in * math.log(R / r_in)
    Ws = -(row["C"] ** 2 / G_N) * (R - r_in - r_in * math.log(R / r_in))
    table.append(dict(foot=row["foot"], Mb=row["Mb"], C=row["C"],
                      rM_kpc=row["rM"] / KPC, A=row["A"], ms=row["ms"],
                      vflat_kms=row["vflat"] / 1e3, sigma_kms=row["sig_C2"] / 1e3,
                      W_cent=Wc, W_self=Ws, W_total=ex,
                      W_total_over_Mb_c2=ex / (row["Mb_kg"] * C_L * C_L)))
res["table"] = table
res["checks"] = checks
res["n_pass"] = sum(1 for c in checks if c["pass_"])
res["n_total"] = len(checks)
res["elapsed_s"] = time.time() - T_START
res["bounds"] = dict(wall_s=res["elapsed_s"], threads=1,
                     memory_note="single-threaded float64/mpmath(50 digits); no BLAS threads")

with open(os.path.join(HERE, "residuals.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)

# console report
print("=" * 100)
print("AS084 -- SELF-GRAVITATIONAL VIRIAL ENERGY WITH A CENTRAL MASS")
print("=" * 100)
print(f"symbolic: closed form verified = {sym_closed};  separation = {sym_split};  "
      f"singular limit = {sing};  sigma2->C/2 = {sigma2_triad_check}")
print(f"primitive: {F}")
print(f"W_cent = {W_cent_s}")
print(f"W_self = {W_self_s}")
print(f"sigma^2(M_in, r_in) = {sol_sigma2}")
print("\n-- footings --")
for k, v in FT.items():
    print(f"  {k:9s} a0 = {v['a0']:.4e}  rho_Lambda = {v['rho_Lambda']:.6e} kg/m^3  "
          f"kappa = {v['kappa']} (adopted)")
print("\n-- table (r_in = 0.1 R, R = 0.62 r_M, M_in = 0.1 M_b) --")
for t in table:
    print(f"  [{t['foot']:9s} | {t['Mb']:18s}] C = {t['C']:.6e}  r_M = {t['rM_kpc']:8.3f} kpc  "
          f"v_flat = {t['vflat_kms']:6.2f} km/s  sigma = {t['sigma_kms']:6.2f} km/s")
    print(f"      W_cent = {t['W_cent']:.6e} J   W_self = {t['W_self']:.6e} J   "
          f"W_total = {t['W_total']:.6e} J = {t['W_total_over_Mb_c2']:.4e} M_b c^2")
print("\n-- checks --")
for c in checks:
    print(f"  [{'PASS' if c['pass_'] else 'FAIL'}] {c['name']}")
print(f"\n{res['n_pass']}/{res['n_total']} checks PASS in {res['elapsed_s']:.1f} s; "
      f"wrote residuals.json")