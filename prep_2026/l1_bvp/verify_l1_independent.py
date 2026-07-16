#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
ADVERSARIAL INDEPENDENT VERIFICATION of l1_bvp.py (the l=1 vector-elastic w solve)
===================================================================================
Independence from the solve under test:
  * DIFFERENT DISCRETIZATION: global box scheme (trapezoidal / midpoint-implicit,
    2nd order) assembled as ONE sparse linear system and solved by direct sparse LU.
    NO initial guess exists anywhere (the problem is linear) -- kills any residual
    guess-echo concern beyond l1_bvp's G5 by construction. l1_bvp.py used scipy
    solve_bvp (adaptive collocation + damped Newton, guess-seeded).
  * DIFFERENT w EXTRACTION: besides the shell median, w is extracted by a linear
    least-squares fit  J(rho) = w * Jt_l(rho) + a*rho^l + b*rho^-(l+1)  over the
    constant-moduli inner region. The two power laws are EXACTLY the homogeneous
    (harmonic) dilatation modes there [div Navier: (K+4mu/3) lap J = lap Phi, so
    J - w*Jt is harmonic where moduli are constant] -- this PROJECTS OUT the
    l=1 zero-mode-adjacent homogeneous content analytically instead of hoping
    the median is insensitive to it.
  * ZERO-MODE ATTACKS (the task's item 3):
      (Z1) add c*[1,0,1,0] (finite translation) to the solved state -> w must not
           move at machine precision (J gauge invariance, claimed algebraic).
      (Z2) replace the clamped outer BC (U=V=0) by two DIFFERENT translation-killing
           BC pairs -- (U=0, Sig_rth=0) and (Sig_rr=0, V=0) -- each removes the
           r^0 translation mode by a different mechanism; w in the sourcing shell
           must agree if the zero-mode handling is clean.
      (Z3) net-force balance: at l=1 the forcing carries net z-force; the outer
           anchor traction integral must absorb it (momentum bookkeeping), i.e.
           |F_traction(rout) - F_traction(rin) - F_forcing| / |F_forcing| << 1.
  * l=2 REPRODUCTION: the same box-scheme code at n=6 must give the committed
    w = 7/23 = 0.30435 at beta = 2/7 (frozen-repo anchor, lane2_beta.py re-run
    2026-07-16: "canonical kappa_t=0.5: w=0.304").
  * N-ARITHMETIC: recompute every rescaled N-target row of l1_bvp.py from the
    frozen confrontation.out N_null values by exact arithmetic.

Formalism itself (state system, moduli, forcing, background) is the COMMITTED one
(methodA_ode.py:82-88, 49, 79-80, 89 -- repo frozen, read-only); the ground rules
forbid re-derivation drift there. Independence is in the discretization, the
extraction, and the BC/zero-mode treatment.

Outputs only to /Users/carlzimmerman/new_physics/prep_2026/l1_bvp/. exit 0 iff all
verification gates pass.
"""
import sys
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

G = 6.674e-11; Msun = 1.989e30; AU = 1.496e11
Z = np.sqrt(32*np.pi/3.0)
YC = Z/2.0
A0C = 9.36e-11
BETA_NAT = 2.0/7.0
W_L2_COMMITTED = 7.0/23.0

CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")

# ------------------------------------------------------------------ background (committed setup)
def setup(a0=A0C, gext_a0=2.2, K0hat=0.5):
    a0V = Z*a0; r_t = np.sqrt(2*G*Msun/a0V); gext = gext_a0*a0
    def Jtl_of(rho, l):
        cc = np.linspace(-1, 1, 4001)
        Pl = cc if l == 1 else 0.5*(3*cc**2 - 1)
        rho = np.atleast_1d(np.asarray(rho, float)); out = np.empty_like(rho)
        for i, rr in enumerate(rho):
            gsun = a0V/(2*rr**2); gr = gsun + gext*cc; gth = -gext*np.sqrt(np.maximum(1-cc**2, 0))
            Jt = 2*np.sqrt(gr**2 + gth**2)/a0V
            out[i] = (2*l+1)/2.0*np.trapz(Jt*Pl, cc)
        return out
    kt = lambda rho: K0hat*np.maximum(1.0, np.asarray(rho, float))
    return dict(r_t=r_t, Jtl_of=Jtl_of, kt=kt, K0hat=K0hat)

# ------------------------------------------------------------------ committed A(x), F(x)
def A_of(x, kt, b, n):
    k = kt(x); lam = k - 2*b; mu = 3*b; M2 = k + 4*b
    return np.array([
        [-2*lam/(M2*x),                 1.0/M2,        n*lam/(M2*x),                    0.0   ],
        [4*mu*(3*lam+2*mu)/(M2*x**2), -4*mu/(M2*x), -2*mu*n*(3*lam+2*mu)/(M2*x**2),     n/x   ],
        [-1.0/x,                        0.0,           1.0/x,                           1.0/mu],
        [-2*mu*(3*lam+2*mu)/(M2*x**2), -lam/(M2*x),   2*mu*(2*n*(lam+mu)-M2)/(M2*x**2), -3.0/x]])

def F_of(x, Fr, Fth):
    return np.array([0.0, -Fr(x), 0.0, -Fth(x)])

# ------------------------------------------------------------------ box-scheme sparse solve
def solve_box(S, beta, l, gridN=3000, rin_AU=5.0, rout_AU=3.0e5, outer_bc="clamped"):
    """Trapezoidal box scheme, one global sparse linear solve. No initial guess."""
    r_t = S['r_t']; kt = S['kt']; n = float(l*(l+1)); b = beta
    rin = rin_AU*AU/r_t; rout = rout_AU*AU/r_t
    x = np.logspace(np.log10(rin), np.log10(rout), gridN)
    phi = kt(x)*S['Jtl_of'](x, l)
    sp_ = CubicSpline(np.log(x), phi)
    Fr = lambda t: sp_(np.log(t), 1)/t
    Fth = lambda t: sp_(np.log(t))/t

    N = gridN; M = lil_matrix((4*N, 4*N)); rhs = np.zeros(4*N)
    Ai = [A_of(xi, kt, b, n) for xi in x]
    Fi = [F_of(xi, Fr, Fth) for xi in x]
    I4 = np.eye(4)
    for i in range(N-1):
        h = x[i+1] - x[i]
        # (Y_{i+1}-Y_i)/h = (A_{i+1}Y_{i+1} + A_i Y_i)/2 + (F_{i+1}+F_i)/2
        Lb = -I4/h - 0.5*Ai[i]
        Rb = I4/h - 0.5*Ai[i+1]
        r0 = 4*i
        M[r0:r0+4, 4*i:4*i+4] = Lb
        M[r0:r0+4, 4*(i+1):4*(i+1)+4] = Rb
        rhs[r0:r0+4] = 0.5*(Fi[i] + Fi[i+1])
    # BC rows: inner traction-free (Srr=Srt=0); outer variant
    rb = 4*(N-1)
    M[rb+0, 1] = 1.0            # Srr(rin)=0
    M[rb+1, 3] = 1.0            # Srt(rin)=0
    j = 4*(N-1)
    if outer_bc == "clamped":       # committed: U=V=0
        M[rb+2, j+0] = 1.0; M[rb+3, j+2] = 1.0
    elif outer_bc == "U0_Srt0":     # kills translation via U
        M[rb+2, j+0] = 1.0; M[rb+3, j+3] = 1.0
    elif outer_bc == "Srr0_V0":     # kills translation via V
        M[rb+2, j+1] = 1.0; M[rb+3, j+2] = 1.0
    else:
        raise ValueError(outer_bc)
    Y = spsolve(csc_matrix(M), rhs).reshape(N, 4).T
    U, Srr, V, Srt = Y
    k = kt(x); lam = k - 2*b; mu = 3*b; M2 = k + 4*b
    dU = -(2*lam/(M2*x))*U + (1/M2)*Srr + (n*lam/(M2*x))*V
    J = dU + 2*U/x - n*V/x
    Jt = S['Jtl_of'](x, l)
    return x, Y, J, Jt

def w_median(x, J, Jt, lo=0.3, hi=1.0):
    m = (x >= lo) & (x <= hi)
    return float(np.median(J[m]/Jt[m]))

def w_fit_harmonic(x, J, Jt, l, lo=0.1, hi=1.0):
    """LSQ fit J = w*Jt + a*x^l + b*x^-(l+1) on the constant-moduli region.
    Returns (w, harm_frac) where harm_frac = harmonic contamination / |w*Jt| (median)."""
    m = (x >= lo) & (x <= hi)
    Xd = np.column_stack([Jt[m], x[m]**l, x[m]**(-(l+1))])
    coef, *_ = np.linalg.lstsq(Xd, J[m], rcond=None)
    w, a, b = coef
    harm = a*x[m]**l + b*x[m]**(-(l+1))
    resid = J[m] - (w*Jt[m] + harm)
    harm_frac = float(np.median(np.abs(harm))/np.median(np.abs(w*Jt[m])))
    resid_frac = float(np.max(np.abs(resid))/np.median(np.abs(w*Jt[m])))
    return float(w), harm_frac, resid_frac

def net_force_balance(S, beta, l, x, Y, gridN_used):
    """Z3: outer traction z-force vs volume z-force of the forcing (l=1 only).
    F_traction(r) = 2 pi r^2 (Srr*2/3 + Srt*4/3) ;
    F_forcing = int 2 pi r^2 (phi'*2/3 + (phi/r)*4/3) dr   [f = grad(phi P1)]"""
    U, Srr, V, Srt = Y
    kt = S['kt']; phi = kt(x)*S['Jtl_of'](x, l)
    sp_ = CubicSpline(np.log(x), phi)
    dphi = sp_(np.log(x), 1)/x
    fz = 2*np.pi*x**2*(dphi*(2.0/3.0) + (phi/x)*(4.0/3.0))
    F_forc = np.trapz(fz, x)
    Ftr = 2*np.pi*x**2*(Srr*(2.0/3.0) + Srt*(4.0/3.0))
    # inner end is traction-free (BC) -> F_traction(rin)=0; balance at outer:
    bal = (Ftr[-1] - Ftr[0]) + F_forc          # div sigma = -f convention
    bal2 = (Ftr[-1] - Ftr[0]) - F_forc         # div sigma = +f convention
    rel = min(abs(bal), abs(bal2))/abs(F_forc)
    return rel, F_forc, Ftr[-1]

# ==================================================================================
def main():
    S = setup()
    print("="*88)
    print("V1  BOX-SCHEME (independent discretization, direct sparse linear solve, NO guess)")
    print("="*88)

    # ---- sign convention: pure-bulk reference
    x, Y, J, Jt = solve_box(S, 0.001, l=2)
    raw = w_median(x, J, Jt)
    SGN = 1.0 if raw > 0 else -1.0
    print(f"  pure-bulk (beta=0.001, l=2): median(J/Jt) = {raw:+.4f}  -> SGN={SGN:+.0f} "
          f"(same one-global-sign structure as l1_bvp.py / committed magnitude-only P2 gate)")
    check("V1a pure-bulk |J/Jt|=1 (<3%)", abs(abs(raw)-1) < 0.03, f"|median|={abs(raw):.4f}")

    # ---- l=2 committed reproduction
    print("\n  l=2 reproduction (n=6), committed anchor w(2/7) = 7/23 = 0.30435:")
    wl2 = {}
    for b in [BETA_NAT, 0.33, 0.60, 0.95, 2.00]:
        x, Y, J, Jt = solve_box(S, b, l=2)
        wm = SGN*w_median(x, J, Jt)
        wf = 1.0/(1.0 + 8.0*b)
        wl2[b] = wm
        print(f"    beta={b:.4f}: w_box={wm:.5f}  formula={wf:.5f}  dev={(wm-wf)/wf*100:+.3f}%")
    check("V1b box-scheme l=2 reproduces committed 0.3043 (<1%)",
          abs(wl2[BETA_NAT] - W_L2_COMMITTED)/W_L2_COMMITTED < 0.01,
          f"{wl2[BETA_NAT]:.5f} vs 7/23={W_L2_COMMITTED:.5f}")

    # ---- l=1 by box scheme, both extractions
    print("\n  l=1 (n=2) by box scheme; w by shell median AND by harmonic-projected LSQ fit:")
    print(f"  {'beta':>8} {'w_median':>10} {'w_fit':>10} {'harm_frac':>10} {'resid':>9} {'formula':>9} {'l1_bvp.py':>10}")
    l1_claim = {0.05: 0.7143, 0.10: 0.5556, 0.20: 0.3846, BETA_NAT: 0.3043, 1/3: 0.2727,
                0.40: 0.2381, 0.60: 0.1724, 0.95: 0.1163, 1.00: 0.1111, 2.00: 0.0588}
    ok_med = ok_fit = True
    wl1 = {}
    for b, wc in l1_claim.items():
        x, Y, J, Jt = solve_box(S, b, l=1)
        wm = SGN*w_median(x, J, Jt)
        wf_, hf, rf = w_fit_harmonic(x, SGN*J, Jt, l=1)
        wform = 1.0/(1.0 + 8.0*b)
        wl1[b] = (wm, wf_, x, Y, J, Jt)
        ok_med &= abs(wm - wc)/wc < 0.005
        ok_fit &= abs(wf_ - wform)/wform < 0.005
        print(f"  {b:>8.4f} {wm:>10.5f} {wf_:>10.5f} {hf:>10.2e} {rf:>9.1e} {wform:>9.4f} {wc:>10.4f}")
    check("V1c l=1 box-scheme w matches l1_bvp.py claims (<0.5% each)", ok_med)
    check("V1d harmonic-projected LSQ w matches 1/(1+8b) (<0.5% each)", ok_fit)
    print("    (harm_frac = zero-mode-adjacent homogeneous contamination in the shell,")
    print("     projected out explicitly -- the median and the projected fit must agree.)")

    # ---- V2: zero-mode attacks
    print("\n" + "="*88)
    print("V2  ZERO-MODE ATTACKS (l=1 translation r^0 mode)")
    print("="*88)
    b = BETA_NAT
    wm0, wf0, x, Y, J, Jt = wl1[b]

    # Z1: add a finite translation to the state, recompute J
    n = 2.0; kt = S['kt']
    c_tr = 10.0*np.max(np.abs(Y[0]))   # translation 10x larger than the response
    U2 = Y[0] + c_tr; V2 = Y[2] + c_tr
    k = kt(x); lam = k - 2*b; mu = 3*b; M2 = k + 4*b
    dU2 = -(2*lam/(M2*x))*U2 + (1/M2)*Y[1] + (n*lam/(M2*x))*V2
    J2 = dU2 + 2*U2/x - n*V2/x
    dw = abs(SGN*w_median(x, J2, Jt) - wm0)/wm0
    check("V2-Z1 J invariant under added translation 10x response amplitude",
          dw < 1e-10, f"dw/w = {dw:.2e}")

    # Z2: different translation-killing outer BCs
    print("\n  alternative outer BCs (each kills the r^0 translation differently):")
    ws_bc = {}
    for bc in ["clamped", "U0_Srt0", "Srr0_V0"]:
        xb, Yb, Jb, Jtb = solve_box(S, b, l=1, outer_bc=bc)
        ws_bc[bc] = SGN*w_median(xb, Jb, Jtb)
        print(f"    outer_bc={bc:<9}: w_l1 = {ws_bc[bc]:.5f}")
    spread = (max(ws_bc.values()) - min(ws_bc.values()))/wm0
    check("V2-Z2 w_l1 agrees across 3 distinct translation-killing outer BCs (<1%)",
          spread < 0.01, f"spread {spread*100:.3f}%")

    # Z3: net-force bookkeeping
    rel, Ff, Ft = net_force_balance(S, b, 1, x, Y, len(x))
    check("V2-Z3 outer anchor absorbs the l=1 net force (balance <2%)",
          rel < 0.02, f"|imbalance|/|F_forcing| = {rel:.2e}")

    # ---- V3: w(x) at the RC sourcing radii
    print("\n" + "="*88)
    print("V3  w(rho) AT THE ALIGNED-STATISTIC RADII (box scheme, rout=1e6 AU)")
    print("="*88)
    claim_wx = {0.5: 0.513, 0.3: 0.576, 0.2: 0.625, 0.1: 0.702, 0.05: 0.769}
    x6, Y6, J6, Jt6 = solve_box(S, BETA_NAT, l=1, gridN=4000, rout_AU=1.0e6)
    prof = SGN*J6/Jt6
    ok_wx = True
    print(f"  {'x=gbar/a0':>10} {'rho':>8} {'w_box':>8} {'local law':>10} {'l1_bvp.py':>10}")
    w_at = {}
    for xx, wc in claim_wx.items():
        rho_x = float(np.sqrt(YC/xx)); ktx = 0.5*rho_x
        wloc = ktx/(ktx + 4*BETA_NAT)
        wb = float(np.interp(rho_x, x6, prof))
        w_at[xx] = wb
        ok_wx &= abs(wb - wc)/wc < 0.01 and abs(wb - wloc)/wloc < 0.01
        print(f"  {xx:>10.2f} {rho_x:>8.2f} {wb:>8.4f} {wloc:>10.4f} {wc:>10.4f}")
    check("V3 w(x) profile matches l1_bvp.py + local law (<1% each)", ok_wx)

    # ---- V4: N-target arithmetic (frozen confrontation.out anchors)
    print("\n" + "="*88)
    print("V4  N-TARGET ARITHMETIC (N = N_null/(1-w)^2; N_null from frozen confrontation.out)")
    print("="*88)
    N_NULL = {("canon", "maxclu"): 560, ("canon", "noclu"): 35390,
              ("alt", "maxclu"): 689, ("alt", "noclu"): 43595}
    N_BANKED_OUT = {("canon", "maxclu"): 1157, ("canon", "noclu"): 73129,
                    ("alt", "maxclu"): 1424, ("alt", "noclu"): 90084}
    ok_bank = True
    for kk, n0 in N_NULL.items():
        nb = n0/(1-W_L2_COMMITTED)**2
        ok_bank &= abs(nb - N_BANKED_OUT[kk]) < 2.0
        print(f"    {kk[0]:>5}/{kk[1]:<7}: {n0}/(1-7/23)^2 = {nb:8.0f}   confrontation.out: {N_BANKED_OUT[kk]}")
    check("V4a banked N reconstruction matches frozen confrontation.out (<2 abs)", ok_bank)

    x_rep = 0.107; rho_rep = float(np.sqrt(YC/x_rep))
    w_star = float(np.interp(rho_rep, x6, prof))
    claimed = {("canon", "maxclu"): 6007, ("canon", "noclu"): 379641,
               ("alt", "maxclu"): 7391, ("alt", "noclu"): 467659}
    ok_corr = True
    print(f"\n    w*(x=0.107) by box scheme = {w_star:.4f}  (l1_bvp.py: 0.695)")
    for kk, n0 in N_NULL.items():
        nc = n0/(1-w_star)**2
        dev = abs(nc - claimed[kk])/claimed[kk]
        ok_corr &= dev < 0.02
        print(f"    {kk[0]:>5}/{kk[1]:<7}: corrected N = {nc:9.0f}   l1_bvp.py: {claimed[kk]:>9,}   dev {dev*100:.2f}%")
    ok_corr &= abs(w_star - 0.695) < 0.01
    check("V4b corrected N-targets reproduced independently (<2% each)", ok_corr)
    fac = (1-W_L2_COMMITTED)**2/(1-w_star)**2
    check("V4c the x5.2 rescale factor", abs(fac - 5.2) < 0.15, f"factor = {fac:.2f}")

    # aligned band: w(0.5)*1% .. w(0.05)*4%
    lo_band = w_at[0.5]*1.0; hi_band = w_at[0.05]*4.0
    check("V4d corrected aligned band ~0.5-3.1%", abs(lo_band-0.51) < 0.03 and abs(hi_band-3.08) < 0.08,
          f"[{lo_band:.2f}%, {hi_band:.2f}%]")

    # ---- summary
    print("\n" + "="*88)
    print("VERIFICATION SUMMARY")
    print("="*88)
    allok = True
    for name, ok, detail in CHECKS:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}  {detail}")
        allok &= ok
    if not allok:
        print("\nVERIFICATION FAILED. exit 1"); sys.exit(1)
    print("\nALL INDEPENDENT CHECKS PASS. exit 0")

if __name__ == "__main__":
    main()
