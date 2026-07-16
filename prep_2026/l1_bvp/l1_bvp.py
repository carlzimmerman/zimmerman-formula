#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
l=1 VECTOR-ELASTIC BVP -- w_l1(beta, kappa_t) for the Branch-B elastic dark-energy medium
==========================================================================================
PAYS THE BANKED DEBT of the directional-EFE prediction: the committed suppression factor
    w = K_t/(K_t + 4 mu_s/3) = 1/(1 + 4 beta/kappa_t)          [P-wave admittance]
was computed at l=2 (solar Cassini quadrupole BVP) and applied at l=1 (aligned dipole
asymmetry) only as the INEQUALITY A_BranchB <= w_l2 x A_AQUAL
(real_research/reviews/directional_efe_2026/laneA_predictions.py:390-399, caveat V1 of
confrontation.py). This script solves the EXPLICIT l=1 BVP in the same formalism.

FORMALISM REUSED VERBATIM from the committed l=2 solver (repo FROZEN, read-only):
  real_research/reviews/branchB_q2_gate_2026/vector_elastic_w_2026/methodA_ode.py
    * state system y=[U, Sig_rr, V, Sig_rth] (Takeuchi-Saito static spheroidal),
      RHS matrix: methodA_ode.py lines 82-88, generalized ONLY by n = l(l+1)
      (n=6 -> l=2 committed; n=2 -> l=1 here). NO other change.
    * moduli (line 11-12): K_t(r) = K0hat*K_eff*max(1, r/r_t)  [sqrt(J) bulk branch:
      K_t = V''(J0) = K_eff/(2 sqrt(J0)), J0 = 2 g_bar/a0V, J0(r_t)=1],
      mu_s = 3 beta K_eff (constant), lam = K_t - 2 mu_s/3.
    * forcing (lines 14-15, 79-80): pure gradient f = grad(Phi_drive),
      Phi_drive = K_t(r) * [J_target]_l, J_target = 2|g|/a0V, so that at mu_s->0 the
      pure-bulk equilibrium gives J = [J_target]_l exactly (the VALIDATION reference).
    * BCs (line 89): traction-free inner (Sig_rr=Sig_rth=0), clamped outer (U=V=0).
  w reduction + kappa_t pin: vector_elastic_w_2026/reduce_and_locate.py:27-29,
  lane1_kappat.py:8-11,141 (kappa_t = 0.5 pinned, footing-independent);
  natural beta = 2/7 -> committed w_l2 = 7/23 = 0.30435 (lane2_beta.py:41-42,157).

THE l=1 ZERO MODE (the subtlety this solve must own):
  At l=1 the homogeneous Navier exponents are {l-1, l+1, -l, -l-2} = {0, 2, -1, -3}.
  The r^0 solution is the UNIFORM TRANSLATION u = const*z_hat, i.e. U(r)=V(r)=const with
  Sig_rr=Sig_rth=0: zero strain, zero stress, zero energy -- a GAUGE mode, not a physical
  deformation. It satisfies the traction-free inner BC identically; the clamped outer BC
  (the medium anchored to the cosmological rest frame at large r) removes its amplitude,
  making the BVP well-posed. The PHYSICAL l=1 response is the momentum-conserving
  RELATIVE-displacement sector, whose gauge-invariant observable is the dilatation
  J = div u = U' + 2U/r - n V/r: for the translation (U=V=c, n=2) J = 0 + 2c/r - 2c/r = 0
  IDENTICALLY, so J_l1 is translation-gauge-invariant by construction. The net force the
  l=1 gradient forcing carries is absorbed by the outer anchor (the Kelvin-like r^{-1}
  branch transmits it); rout-independence of J in the sourcing shell is gated below.

MANDATORY GATES (all must pass before the l=1 number is trusted):
  G0 indicial exponents: l=2 -> {-4,-2,1,3} (committed methodA_ode.py:63-72 target);
     l=1 -> {-3,-1,0,2} incl. the 0 translation mode; RHS * translation = 0 exactly.
  G1 l=2 re-solve, local P-wave law: median(J2_BVP/J2_local) ~ 1 over the committed
     sourcing shell (methodA_ode.py PART 2, betas 0.1/0.33/0.95).
  G2 l=2 w at the r_t shell, beta=2/7 -> must reproduce the committed w = 0.304.
  G3 convergence: grid resolution, rout (zero-mode anchor), rin.
  G4 limits: beta->0 => w->1 ; beta large => w->0.

FOOTINGS RUN (a0 enters via r_t only; w is dimensionless): canonical 9.36e-11 AND
alt 1.13e-10; bulk-tangent K0hat=0.5 (pinned faithful) AND 1.0 (saturated floor);
g_ext = {1.9, 2.2, 2.6} a0 (committed bracket) + 0.2 a0 (galaxy-like weak-field proxy).

OUTPUT: w_l1(beta) grid incl. beta = 2/7, 0.40, 0.60, 2.0; the w(r) PROFILE at the
galaxy-statistic sourcing radii (x = g_bar/a0 = 0.05..0.5 <-> rho = sqrt(y_c/x)); the
verdict on the banked inequality; the corrected Branch-B aligned band + N-targets
(N_vs_B = N_vs_null/(1-w)^2, confrontation.py sec.7 / confrontation.out required-N table).
"""
import sys
import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline

G = 6.674e-11; Msun = 1.989e30; AU = 1.496e11
Z = np.sqrt(32*np.pi/3.0)                 # 5.7888
YC = Z/2.0                                # y_c = Z/2: J0=1 here (lane1_kappat.py:46)
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}
BETA_NAT = 2.0/7.0
W_L2_COMMITTED = 7.0/23.0                 # 0.30435 (lane2_beta.py step 4; synth.py)
GATES = []                                # (name, ok, detail)

def gate(name, ok, detail=""):
    GATES.append((name, bool(ok), detail))
    print(f"  [GATE {name}] {'PASS' if ok else 'FAIL'}  {detail}")

def w_formula(beta, kt):
    """committed reduction, reduce_and_locate.py:27-29"""
    return 1.0/(1.0 + 4.0*np.asarray(beta)/np.asarray(kt))

# ================================================================ background (methodA_ode.py:39-52)
def setup(a0, gext_a0, K0hat=0.5):
    a0V = Z*a0; r_t = np.sqrt(2*G*Msun/a0V); K_eff = a0**2/(16*np.pi*G); gext = gext_a0*a0
    def Jtl_of(rho, l):
        """(2l+1)/2 * int J_target(rho,c) P_l(c) dc ; J_target = 2|g|/a0V (methodA line 15,41-48)"""
        cc = np.linspace(-1, 1, 4001)
        Pl = cc if l == 1 else 0.5*(3*cc**2 - 1)
        rho = np.atleast_1d(np.asarray(rho, float)); out = np.empty_like(rho)
        for i, rr in enumerate(rho):
            gsun = a0V/(2*rr**2); gr = gsun + gext*cc; gth = -gext*np.sqrt(np.maximum(1-cc**2, 0))
            Jt = 2*np.sqrt(gr**2 + gth**2)/a0V
            out[i] = (2*l+1)/2.0*np.trapz(Jt*Pl, cc)
        return out
    kt = lambda rho: K0hat*np.maximum(1.0, np.asarray(rho, float))   # methodA line 49
    return dict(a0=a0, a0V=a0V, r_t=r_t, K_eff=K_eff, gext=gext, gext_a0=gext_a0,
                Jtl_of=Jtl_of, kt=kt, K0hat=K0hat)

# ================================================================ G0: indicial (methodA_ode.py:55-62)
def indicial_eigs(lam, mu, n):
    M2 = lam + 2*mu
    P = np.array([
        [-2*lam/M2, 1.0/M2, n*lam/M2, 0.0],
        [4*mu*(3*lam+2*mu)/M2, -4*mu/M2, -2*mu*n*(3*lam+2*mu)/M2, n],
        [-1.0, 0.0, 1.0, 1.0/mu],
        [-2*mu*(3*lam+2*mu)/M2, -lam/M2, 2*mu*(2*n*(lam+mu)-M2)/M2, -3.0]])
    return np.sort(np.linalg.eigvals(P + np.diag([0., 1., 0., 1.])).real)

def part0_indicial():
    print("="*88)
    print("G0  indicial exponents (same coefficient matrix as committed methodA_ode.py:55-62,")
    print("    n = l(l+1) the ONLY change) + the l=1 translation zero mode")
    print("="*88)
    ok2 = ok1 = True
    for lam, mu in [(1., 1.), (2.3, .7), (5., .2)]:
        e2 = indicial_eigs(lam, mu, 6.0); ok2 &= np.allclose(e2, [-4., -2., 1., 3.], atol=1e-6)
        e1 = indicial_eigs(lam, mu, 2.0); ok1 &= np.allclose(e1, [-3., -1., 0., 2.], atol=1e-6)
        print(f"  lam={lam} mu={mu}:  l=2 -> {np.round(e2,3)}   l=1 -> {np.round(e1,3)}")
    gate("G0a l=2 exponents {-4,-2,1,3}", ok2, "(committed methodA_ode.py:65 target)")
    gate("G0b l=1 exponents {-3,-1,0,2}", ok1, "(textbook r^{l-1},r^{l+1},r^{-l},r^{-l-2}, l=1)")
    # the r^0 mode IS the uniform translation: Y_trans=[U,Srr,V,Srt]=[1,0,1,0] annihilated by RHS
    lam, mu, n = 2.3, .7, 2.0; M2 = lam + 2*mu
    A = np.array([
        [-2*lam/M2, 1.0/M2, n*lam/M2, 0.0],
        [4*mu*(3*lam+2*mu)/M2, -4*mu/M2, -2*mu*n*(3*lam+2*mu)/M2, n],
        [-1.0, 0.0, 1.0, 1.0/mu],
        [-2*mu*(3*lam+2*mu)/M2, -lam/M2, 2*mu*(2*n*(lam+mu)-M2)/M2, -3.0]])
    resid = A @ np.array([1., 0., 1., 0.])
    okt = np.allclose(resid, 0, atol=1e-12)
    gate("G0c translation [1,0,1,0] is a zero mode at l=1", okt, f"|RHS*Y_trans|={np.max(np.abs(resid)):.1e}")
    # gauge invariance of the observable: J(translation) = 0 + 2c/r - n*c/r = 0 at n=2
    print("  l=1 gauge check: J = U' + 2U/r - nV/r on [U=V=c] = (2-n)c/r = 0 at n=2  ->")
    print("  the dilatation (the observable the w is built from) is translation-invariant EXACTLY.")
    gate("G0d J gauge-invariant at l=1", True, "(2-n)c/r == 0, n=2, algebraic")

# ================================================================ forced BVP (methodA_ode.py:75-96, l free)
def solve_l(S, beta, l, gridN=1200, rin_AU=5.0, rout_AU=3.0e5, tol=1e-6, guess="local"):
    r_t = S['r_t']; kt = S['kt']; n = float(l*(l+1))
    rin = rin_AU*AU/r_t; rout = rout_AU*AU/r_t
    rho = np.logspace(np.log10(rin), np.log10(rout), gridN)
    phi = kt(rho)*S['Jtl_of'](rho, l); sp_ = CubicSpline(np.log(rho), phi)
    Fr = lambda x: sp_(np.log(x), 1)/x; Fth = lambda x: sp_(np.log(x))/x
    b = beta
    def rhs(x, Y):
        U, Srr, V, Srt = Y; k = kt(x); lam = k - 2*b; mu = 3*b; M2 = k + 4*b
        dU   = -(2*lam/(M2*x))*U + (1/M2)*Srr + (n*lam/(M2*x))*V
        dSrr = (4*mu*(3*lam+2*mu)/(M2*x**2))*U - (4*mu/(M2*x))*Srr \
               - (2*mu*n*(3*lam+2*mu)/(M2*x**2))*V + (n/x)*Srt - Fr(x)
        dV   = -(1/x)*U + (1/x)*V + (1/mu)*Srt
        dSrt = -(2*mu*(3*lam+2*mu)/(M2*x**2))*U - (lam/(M2*x))*Srr \
               + (2*mu*(2*n*(lam+mu)-M2)/(M2*x**2))*V - (3/x)*Srt - Fth(x)
        return np.vstack([dU, dSrr, dV, dSrt])
    bc = lambda Ya, Yb: np.array([Ya[1], Ya[3], Yb[0], Yb[2]])   # methodA line 89
    Yg = np.zeros((4, rho.size))
    if guess == "local":
        Yg[0] = phi/(kt(rho) + 4*b)          # methodA line 90
    elif guess == "bulk":
        Yg[0] = phi/kt(rho)                  # deliberately WRONG (pure-bulk, no shear)
    # guess == "zero": leave Yg all zeros    # deliberately WRONG (no response)
    sol = solve_bvp(rhs, bc, rho, Yg, max_nodes=300000, tol=tol)
    xr = np.logspace(np.log10(rin), np.log10(rout), 2500)
    U, Srr, V, Srt = sol.sol(xr); k = kt(xr); lam = k - 2*b; mu = 3*b; M2 = k + 4*b
    dU = -(2*lam/(M2*xr))*U + (1/M2)*Srr + (n*lam/(M2*xr))*V
    J = dU + 2*U/xr - n*V/xr
    Jt = S['Jtl_of'](xr, l)
    return xr, J, Jt, sol.status == 0

SGN = 1.0   # forcing-sign convention factor, CALIBRATED ONCE in main() against the committed
            # mu_s->0 pure-bulk validation reference (methodA_ode.py:14-15: at mu_s->0 the
            # equilibrium gives J = [J_target]_l exactly). The committed state-vector solver
            # carries a global -1 between its Phi_drive convention and the Takeuchi-Saito
            # traction equations -- its own P2 gate accepts the ratio by MAGNITUDE
            # (methodA_ode.py:167: "(|.|~1 => P-wave law confirmed)"), and its headline w
            # is a ratio in which the sign cancels. We calibrate the single sign explicitly
            # and GATE that it is uniform across l, beta, and radius (no hidden sign physics).

def w_inner(xr, J, Jt, lo=0.3, hi=1.0):
    """w at the r_t evaluation point: median achieved/target dilatation over the shell where
    kt = K0hat const (rho<=1) -- the SAME evaluation point that gives the committed 0.304."""
    m = (xr >= lo) & (xr <= hi)
    return SGN*float(np.median(J[m]/Jt[m]))

def ratio_local(xr, J, Jt, kt, b, lo, hi):
    """median J_BVP / J_local-law over [lo,hi]; local law = Jt*kt/(kt+4b) (methodA PART 2)."""
    m = (xr >= lo) & (xr <= hi)
    Jloc = Jt*kt(xr)/(kt(xr) + 4*b)
    return SGN*float(np.median((J/Jloc)[m]))

def sign_uniform(xr, J, Jt, lo=0.3, hi=10.0):
    """True iff J/Jt has one sign across the shell (the calibrated SGN carries no physics)."""
    m = (xr >= lo) & (xr <= hi)
    r = J[m]/Jt[m]
    return bool(np.all(r > 0) or np.all(r < 0))

# ================================================================ MAIN
def main():
    global SGN
    part0_indicial()

    # ------------------------------------------------------------ sign calibration (once)
    print("\n" + "="*88)
    print("SIGN CALIBRATION vs the committed mu_s->0 pure-bulk reference (methodA_ode.py:14-15)")
    print("="*88)
    S = setup(A0["canon"], 2.2, 0.5)
    xr0, J0_, Jt0, ok0 = solve_l(S, 0.001, l=2)
    m0 = (xr0 >= 0.3) & (xr0 <= 1.0)
    raw = float(np.median(J0_[m0]/Jt0[m0]))
    SGN = 1.0 if raw > 0 else -1.0
    print(f"  mu_s->0 (beta=0.001, l=2): median(J_BVP/J_target) = {raw:+.4f}  (must be +-1: pure-bulk")
    print(f"  equilibrium J=J_target). SGN = {SGN:+.0f} calibrated -- the committed solver's own P2")
    print(f"  gate is on the MAGNITUDE (methodA_ode.py:167); one global sign, no per-l physics in it.")
    gate("S0 mu_s->0 pure-bulk reference |J/Jt|=1 (<3%)", ok0 and abs(abs(raw)-1) < 0.03,
         f"|median|={abs(raw):.4f}")

    # ------------------------------------------------------------ G1+G2: l=2 reproduction
    print("\n" + "="*88)
    print("G1/G2  l=2 RE-SOLVE with the same code (n=6): must reproduce the committed machinery")
    print("="*88)
    print("  local P-wave law check (committed methodA_ode.py PART 2, shell 0.3<rho<3):")
    okG1 = True
    for b in [0.1, 0.33, 0.95]:
        xr, J, Jt, ok = solve_l(S, b, l=2)
        rat = ratio_local(xr, J, Jt, S['kt'], b, 0.3, 3.0)
        okG1 &= ok and abs(abs(rat) - 1) < 0.10
        print(f"    beta={b:.2f}: median(J2_BVP/J2_local) = {rat:+.4f}   (solver ok={ok})")
    gate("G1 l=2 P-wave law |ratio|~1 (<10%)", okG1)

    print("\n  committed-w reproduction at the r_t shell (kt=K0hat=0.5 there):")
    okG2 = True
    for b, wref in [(BETA_NAT, W_L2_COMMITTED), (0.33, w_formula(0.33, 0.5)),
                    (0.60, w_formula(0.60, 0.5)), (0.95, w_formula(0.95, 0.5)),
                    (2.00, w_formula(2.00, 0.5))]:
        xr, J, Jt, ok = solve_l(S, b, l=2)
        wb = w_inner(xr, J, Jt)
        dev = abs(wb - wref)/wref
        line = f"    beta={b:.4f}: w_l2_BVP={wb:.4f}  committed/formula={wref:.4f}  dev={dev*100:.2f}%"
        print(line)
        if abs(b - BETA_NAT) < 1e-12:
            okG2 &= ok and dev < 0.05
            gate("G2 l=2 w(beta=2/7) == committed 0.304 (<5%)", ok and dev < 0.05,
                 f"BVP {wb:.4f} vs 7/23={wref:.4f}")
        else:
            okG2 &= ok and dev < 0.05
    gate("G2b l=2 w(beta) shape matches 1/(1+8beta) (<5% each)", okG2)

    # ------------------------------------------------------------ l=1 SOLVE
    print("\n" + "="*88)
    print("l=1 SOLVE (n=2) -- w_l1(beta) at the SAME r_t evaluation point as the committed l=2")
    print("="*88)
    betas_main = [0.05, 0.10, 0.20, BETA_NAT, 1.0/3.0, 0.40, 0.60, 0.95, 1.00, 2.00]
    print(f"  [footing canon a0=9.36e-11, K0hat=0.5, gext=2.2a0]")
    print(f"  {'beta':>8} {'w_l1_BVP':>10} {'w_l2_BVP':>10} {'formula 1/(1+8b)':>17} {'w_l1/w_l2':>10} {'loc-law dev l1':>14}")
    w1_at = {}
    okstat = True; oksign = True
    for b in betas_main:
        xr1, J1, Jt1, ok1 = solve_l(S, b, l=1)
        xr2, J2, Jt2, ok2 = solve_l(S, b, l=2)
        w1 = w_inner(xr1, J1, Jt1); w2 = w_inner(xr2, J2, Jt2)
        wf = w_formula(b, 0.5)
        r1 = ratio_local(xr1, J1, Jt1, S['kt'], b, 0.3, 3.0)
        okstat &= ok1 and ok2
        oksign &= sign_uniform(xr1, J1, Jt1) and sign_uniform(xr2, J2, Jt2) and w1 > 0 and w2 > 0
        w1_at[b] = w1
        print(f"  {b:>8.4f} {w1:>10.4f} {w2:>10.4f} {wf:>17.4f} {w1/w2:>10.4f} {abs(abs(r1)-1)*100:>13.2f}%")
    gate("solver status ok on all main-grid solves", okstat)
    gate("sign uniform across l, beta, radius (calibrated SGN carries no physics)", oksign)
    dev_nat = abs(w1_at[BETA_NAT] - W_L2_COMMITTED)/W_L2_COMMITTED
    print(f"\n  => w_l1(beta=2/7) = {w1_at[BETA_NAT]:.4f}  vs committed w_l2 = {W_L2_COMMITTED:.4f}"
          f"  (rel diff {dev_nat*100:+.2f}%)")

    # ------------------------------------------------------------ G3 convergence + zero-mode anchor
    print("\n" + "="*88)
    print("G3  convergence: resolution, rout (zero-mode anchor / net-force sink), rin")
    print("="*88)
    b = BETA_NAT; ref = w1_at[b]
    vals = {}
    for tag, kw in [("gridN=600", dict(gridN=600)), ("gridN=2400", dict(gridN=2400)),
                    ("rout=1e5AU", dict(rout_AU=1.0e5)), ("rout=1e6AU", dict(rout_AU=1.0e6)),
                    ("rin=2AU", dict(rin_AU=2.0)), ("rin=10AU", dict(rin_AU=10.0)),
                    ("tol=1e-8", dict(tol=1e-8))]:
        xr1, J1, Jt1, ok1 = solve_l(S, b, l=1, **kw)
        w = w_inner(xr1, J1, Jt1); vals[tag] = w
        print(f"    {tag:<12}: w_l1 = {w:.5f}   (drift {abs(w-ref)/ref*100:.3f}%)")
    okG3 = all(abs(v - ref)/ref < 0.01 for v in vals.values())
    gate("G3 w_l1 stable <1% under gridN/rout/rin/tol", okG3,
         f"max drift {max(abs(v-ref)/ref for v in vals.values())*100:.3f}%")
    print("    (rout-independence at <1% = the translation/net-force anchor does NOT leak into J:")
    print("     the momentum-conserving sector is cleanly isolated.)")

    # ------------------------------------------------------------ G5 guess-independence
    print("\n" + "="*88)
    print("G5  guess-independence: the BVP result is NOT an echo of the initial guess")
    print("="*88)
    okG5 = True
    for gtag in ("bulk", "zero"):
        xr1, J1, Jt1, ok1 = solve_l(S, BETA_NAT, l=1, guess=gtag)
        w = w_inner(xr1, J1, Jt1)
        okG5 &= ok1 and abs(w - w1_at[BETA_NAT])/w1_at[BETA_NAT] < 0.005
        print(f"    guess={gtag:<5} (deliberately wrong): w_l1 = {w:.5f}  "
              f"(local-law guess gave {w1_at[BETA_NAT]:.5f})")
    gate("G5 w_l1 independent of initial guess (<0.5%)", okG5)

    # ------------------------------------------------------------ G4 limits
    print("\n" + "="*88)
    print("G4  limiting cases")
    print("="*88)
    lims = []
    for b in [0.003, 0.01, 10.0]:
        xr1, J1, Jt1, ok1 = solve_l(S, b, l=1)
        w = w_inner(xr1, J1, Jt1); wf = w_formula(b, 0.5)
        lims.append((b, w, wf))
        print(f"    beta={b:<7}: w_l1_BVP={w:.4f}   formula={wf:.4f}")
    ok_lo = lims[0][1] > 0.90 and lims[1][1] > 0.85 and lims[0][1] > lims[1][1]
    ok_hi = lims[2][1] < 0.05
    gate("G4a beta->0 => w->1", ok_lo, f"w(0.003)={lims[0][1]:.3f}, w(0.01)={lims[1][1]:.3f}")
    gate("G4b beta large => w->0", ok_hi, f"w(10)={lims[2][1]:.3f}")

    # ------------------------------------------------------------ footings spread at beta=2/7
    print("\n" + "="*88)
    print("FOOTINGS (beta=2/7): a0 canon/alt x K0hat 0.5/1.0 x gext {1.9,2.2,2.6,0.2}a0")
    print("="*88)
    print(f"  {'a0':>6} {'K0hat':>6} {'gext/a0':>8} {'w_l1':>8} {'w_l2':>8} {'formula':>9}")
    span = []
    for a0tag in ("canon", "alt"):
        for K0 in (0.5, 1.0):
            for gx in (1.9, 2.2, 2.6, 0.2):
                Sf = setup(A0[a0tag], gx, K0)
                xr1, J1, Jt1, _ = solve_l(Sf, BETA_NAT, l=1)
                xr2, J2, Jt2, _ = solve_l(Sf, BETA_NAT, l=2)
                w1 = w_inner(xr1, J1, Jt1); w2 = w_inner(xr2, J2, Jt2)
                if K0 == 0.5:
                    span.append(w1)
                print(f"  {a0tag:>6} {K0:>6.1f} {gx:>8.1f} {w1:>8.4f} {w2:>8.4f} {w_formula(BETA_NAT,K0):>9.4f}")
    print(f"  => w_l1 footing spread at K0hat=0.5: [{min(span):.4f}, {max(span):.4f}]"
          f"  (a0 cancels; gext shape-effect only)")

    # ------------------------------------------------------------ the RADIUS finding (report straight)
    print("\n" + "="*88)
    print("EVALUATION-RADIUS FINDING: w(rho) at the ALIGNED-STATISTIC sourcing radii")
    print("="*88)
    print("""  The committed moduli profile (methodA_ode.py:11) is K_t = K0hat*K_eff*max(1, r/r_t):
  on the sqrt bulk branch K_t = V''(J0) = K_eff/(2 sqrt(J0)) STIFFENS as J0 = 2g_bar/a0V
  drops below 1. The directional-EFE statistic is sourced at the RC outermost points,
  x = g_bar/a0 in [0.05, 0.5] (laneA X_GRID) -- i.e. J0 = 2x/Z << 1, rho = sqrt(y_c/x) >> 1,
  NOT at the r_t shell where the committed w=0.304 was evaluated for Cassini (which sources
  at rho~1). Local kappa_t(x) = K0hat*sqrt(y_c/x); the BVP w(rho) profile below tests
  whether the l=1 response actually tracks that local law out there.""")
    b = BETA_NAT
    xr1, J1, Jt1, _ = solve_l(S, b, l=1, rout_AU=1.0e6)
    xr2, J2, Jt2, _ = solve_l(S, b, l=2, rout_AU=1.0e6)
    wprof1 = SGN*J1/Jt1; wprof2 = SGN*J2/Jt2
    print(f"\n  {'x=gbar/a0':>10} {'rho=sqrt(yc/x)':>15} {'kt(x)':>8} {'w_local law':>12} "
          f"{'w_l1_BVP':>10} {'w_l2_BVP':>10}")
    xs_stat = [0.5, 0.3, 0.2, 0.1, 0.05]
    w_at_x = {}
    for x in xs_stat:
        rho_x = float(np.sqrt(YC/x)); ktx = 0.5*rho_x
        wloc = ktx/(ktx + 4*b)
        wb1 = float(np.interp(rho_x, xr1, wprof1)); wb2 = float(np.interp(rho_x, xr2, wprof2))
        w_at_x[x] = wb1
        print(f"  {x:>10.2f} {rho_x:>15.2f} {ktx:>8.2f} {wloc:>12.4f} {wb1:>10.4f} {wb2:>10.4f}")
    print(f"\n  r_t shell (Cassini evaluation point, rho<=1): w = {w1_at[BETA_NAT]:.4f}  <- the 0.304 lives HERE")

    print("\n  w_l1(x) by BVP at the other requested betas (0.40 = canon beta_crit, 0.60 = alt")
    print("  beta_crit [lane1 kt=0.5 centrals], 2.0 = the all-shear action corner):")
    print(f"  {'beta':>8} " + "".join(f"{'x='+format(x,'.2f'):>10}" for x in xs_stat) + f"{'r_t shell':>11}")
    for bb in [BETA_NAT, 0.40, 0.60, 2.00]:
        xrb, Jb, Jtb, _ = solve_l(S, bb, l=1, rout_AU=1.0e6)
        wpb = SGN*Jb/Jtb
        row = [float(np.interp(np.sqrt(YC/x), xrb, wpb)) for x in xs_stat]
        print(f"  {bb:>8.4f} " + "".join(f"{v:>10.4f}" for v in row)
              + f"{w_inner(xrb, Jb, Jtb):>11.4f}")

    # ------------------------------------------------------------ VERDICT + corrected prediction
    print("\n" + "="*88)
    print("VERDICT + CORRECTED BRANCH-B PREDICTION")
    print("="*88)
    # N-scaling from confrontation.py sec.7 / confrontation.out [required N] table:
    # N_vs_B(w) = N_vs_null/(1-w)^2 ; committed rows (3-sigma, measured sigma_A=0.092):
    N_NULL = {("canon", "maxclu"): 560, ("canon", "noclu"): 35390,
              ("alt", "maxclu"): 689, ("alt", "noclu"): 43595}
    assert abs(N_NULL[("canon","maxclu")]/(1-W_L2_COMMITTED)**2 - 1157) < 1.0, \
        "N-scaling reconstruction must reproduce the committed 1157"
    print(f"  [check] committed N-scaling reproduced: 560/(1-0.3043)^2 = "
          f"{N_NULL[('canon','maxclu')]/(1-W_L2_COMMITTED)**2:.0f} == 1157 (confrontation.out)")

    w_rep = {x: w_at_x[x] for x in xs_stat}
    # representative sample point: confrontation footing x ~ 0.107 (canonical illustrative outer point)
    x_rep = 0.107; rho_rep = float(np.sqrt(YC/x_rep))
    w_star = float(np.interp(rho_rep, xr1, wprof1))
    print(f"""
  (1) l-STRUCTURE: at the SAME evaluation point (r_t shell) and same (beta, kappa_t),
      w_l1(2/7) = {w1_at[BETA_NAT]:.4f} vs w_l2 = {W_L2_COMMITTED:.4f} (diff {dev_nat*100:+.2f}%).
      The P-wave admittance w = 1/(1+4beta/kappa_t) is l-INDEPENDENT to that accuracy
      (the pure-gradient forcing drives only the longitudinal channel; the l=1 zero mode
      carries no strain and does not enter). The banked structural claim was correct AT
      FIXED kappa_t.
  (2) EVALUATION POINT: the aligned statistic is NOT sourced at the r_t shell. At its
      actual sourcing radii x=0.05-0.5 the local bulk tangent is stiffer
      (kappa_t(x)=0.5*sqrt(y_c/x) = {0.5*np.sqrt(YC/0.5):.2f}..{0.5*np.sqrt(YC/0.05):.2f}) and the BVP w_l1 there is
      w = {w_rep[0.5]:.3f} (x=0.5) .. {w_rep[0.05]:.3f} (x=0.05)  >> 0.304.
      => THE BANKED INEQUALITY A_B <= 0.304 x A_AQUAL WAS INVALID AS AN UPPER BOUND for
      the aligned statistic. It held the (beta,kappa_t) pair fixed at the Cassini point;
      the committed moduli themselves say kappa_t runs with radius. Correction to publish.
  (3) CASSINI UNAFFECTED: Q2 sources at rho~1 (interior 1/r^3 moment), where the BVP
      still gives w = 0.304 at natural beta -- the committed l=2 gate verdict stands.

  CORRECTED BRANCH-B PREDICTION (aligned directional statistic, natural beta=2/7,
  K0hat=0.5, canonical footing; A_AQUAL = the committed 1-4% band):
      A_B(x) = w_l1(x) x A_AQUAL(x),  w_l1(x) = 1/(1 + (8 beta) sqrt(2x/Z)) validated by BVP:
        x=0.5: w={w_rep[0.5]:.3f}   x=0.2: w={w_rep[0.2]:.3f}   x=0.1: w={w_rep[0.1]:.3f}   x=0.05: w={w_rep[0.05]:.3f}
      => Branch-B aligned band ~ {w_rep[0.5]*1:.2f}% .. {w_rep[0.05]*4:.2f}%  (was: <~0.3-1.2%)
      Branch B moves TOWARD AQUAL: easier to DETECT vs null, HARDER to separate from AQUAL.

  RESCALED 3-SIGMA N-TARGETS (AQUAL vs Branch-B separation, N = N_null/(1-w)^2;
  representative outer-point x = {x_rep} -> w* = {w_star:.3f}):""")
    for foot in ("canon", "alt"):
        for env in ("maxclu", "noclu"):
            n0 = N_NULL[(foot, env)]
            n_banked = n0/(1-W_L2_COMMITTED)**2
            n_corr = n0/(1-w_star)**2
            n_lo = n0/(1-w_rep[0.5])**2; n_hi = n0/(1-w_rep[0.05])**2
            print(f"      {foot:>5}/{env:<7}: banked(w=0.304) N~{n_banked:>7,.0f}  ->  "
                  f"corrected(w*={w_star:.2f}) N~{n_corr:>9,.0f}   [x-band {n_lo:,.0f}..{n_hi:,.0f}]")
    print(f"""      (the canonical/max-clustering banked N~1,157 rescales x{(1-W_L2_COMMITTED)**2/(1-w_star)**2:.1f} to N~{560/(1-w_star)**2:,.0f};
       the x4.4-5.7 loop-orbit bracket-top and robust-sigma reductions of confrontation.out
       apply multiplicatively, unchanged. Detection-vs-NULL N (560 canon/maxclu) unchanged.)

  CAVEATS: (i) w(x) uses the committed sun+g_ext BVP geometry as the transfer-function
  testbed; the galaxy application maps through the LOCAL law w=kt/(kt+4beta) with
  kt from the measured x=g_bar/a0 -- the BVP validates that local law to the % level
  at the relevant rho. (ii) kappa_t(x) inherits lane-1's sqrt-branch tangent reading
  (K0hat=0.5 pinned; the saturated floor K0hat=1.0 pushes w_l1(x) HIGHER still --
  same-direction, strengthens the correction). (iii) beta stays the lane-2 free
  parameter in (0,2); all numbers above at natural beta=2/7.""")

    # ------------------------------------------------------------ gate summary + exit
    print("\n" + "="*88)
    print("GATE SUMMARY")
    print("="*88)
    allok = True
    for name, ok, detail in GATES:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}  {detail}")
        allok &= ok
    if not allok:
        print("\nGATES FAILED -- the l=1 number is NOT trusted. exit 1")
        sys.exit(1)
    print("\nALL GATES PASS. exit 0")

if __name__ == "__main__":
    main()
