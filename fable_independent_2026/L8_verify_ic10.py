#!/usr/bin/env python3
"""
L8 -- independent verification of the lead agent's IC8, IC9 and IC10
====================================================================
Lane L8 of `fable_independent_2026/CHARTER.md`, continuing L4 (`L4_VERIFICATION.md`).  The lead's construction lives in
`closure_2026/integrable_clock_construction_2026/`, which is READ-ONLY to this lane: nothing there is imported, executed
or copied.  Every number below is rebuilt from the ACTIONS AS WRITTEN in IC5_ACTION.md / OPTICAL_ALIGNMENT.md /
IC10_LOCAL_CLOCK.md, transcribed by hand into sympy here, and evaluated at 50 digits with mpmath.  Comparison with the
lead's committed outputs happens only at the end of each check.

THE FOUR QUESTIONS
  1. Does IC8/IC9/IC10 change the DEGREE-OF-FREEDOM count?  L4 found 3 for IC5/IC6/IC7 -- two tensor polarisations plus
     a healthy propagating khronon-type GRAVITATIONAL scalar the construction did not remove.  Is the extra scalar gone,
     or still there; and if still there, is it now identified and shown healthy?  Fried-chicken requirement 2 reads:
     "Exactly two propagating gravitational DOF, N_grav = 2 -- only the two tensor polarizations. ... A genuine matter or
     clock scalar is allowed ONLY if explicitly counted separately and shown healthy."  So the question has two parts:
     the COUNT, and the CHARACTER of the third mode (gravitational scalar = forbidden; clock scalar = permitted).
  2. Does IC10's "local Einstein-clock plateau" do what it says?  Extracted as an equation:
         S10|_{eta=1} = int sqrt(-gt) [ m* Rt/2 + P(Xt,w) ] + Sm[e^{2w} gt, psi],     m* = m e^{-1/6},
         gt = e^{-2w} g,  Xt = -gt^{mu nu} T_mu T_nu / 2,  S = -ln(2 Xt)/2,  xi = S+w,  u = (S+2w)/(S+w),
         P = -m e^{4w}[Lambda + a0^2 U(u^2)] + kappa e^{2w} Xt,   and the w equation is ALGEBRAIC: P_w = 0.
     i.e. on the expanding plateau the vacuum theory is claimed to be exactly Einstein gravity in a conformally related
     metric plus one shift-symmetric k-essence clock plus one auxiliary field with no derivatives.
  3. Do IC8's shear integrability and IC9's lightcone alignment close the two liabilities L4 raised -- (i) IC7's repair
     window was only |j-1| < 0.074 wide, and (ii) IC7 detuned the tensor cone off flat backgrounds as
     c_T^2 = 1 - 4 c_7 Rbar_0 / c?
  4. Spot-check the load-bearing numbers of `optical_run_001/` by rebuilding them here.

TRANSCRIBED CONSTANTS (IC4/IC5, identical to the set L4 already validated):
  ell = ln(9/5),  T = -27/16 + 54/(5 ell),  alpha = 81/(8T^2),  b = -T/9 - 3/8,  m = h0 = 1, kappa = 6,
  a0^2 = 9 kappa e^{-1/2}/(16 m ell^2),  U(c) = (1-c)[ln^2(1-c) - 2 ln(1-c) + 2] - 2,
  Lambda = kappa e^{-1/2}/m - a0^2 U(4/9),  C = Lambda + a0^2 U(u^2),  w = (u-1) xi,  S = (2-u) xi.

Every check is a statement about the lead's claim (or about requirement 2) that COULD come out false.  L8-C* are
controls that would catch MY OWN algebra being wrong; three of them recover known general-relativity results.
"""
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def close(a, b, tol):
    a, b = mp.mpf(a), mp.mpf(b)
    return abs(a - b) <= tol * max(mp.mpf(1), abs(b))


print("=" * 122)
print("L8 -- independent verification of the lead's IC8 shear integrability, IC9 optical alignment and IC10 local clock")
print("=" * 122)

# ==================================================================== independent transcription of the constants =====
ell = sp.log(sp.Rational(9, 5))
Tcal = -sp.Rational(27, 16) + 54 / (5 * ell)
alph = 81 / (8 * Tcal**2)
bpar = -Tcal / 9 - sp.Rational(3, 8)
mm, kap = sp.Integer(1), sp.Integer(6)
h0 = sp.sqrt(kap / (6 * mm))
a02 = 9 * kap * sp.exp(-sp.Rational(1, 2)) / (16 * mm * ell**2)
Ufun = lambda c: (1 - c) * (sp.log(1 - c)**2 - 2 * sp.log(1 - c) + 2) - 2
Lam = kap * sp.exp(-sp.Rational(1, 2)) / mm - a02 * Ufun(sp.Rational(4, 9))

xi, u, rho, tau = sp.symbols('xi u rho tau', real=True)
Ssy, wsy = sp.symbols('S w', real=True)
Esy = sp.exp((4 - 3 * u) * xi)
Cpot = Lam + a02 * Ufun(u**2)
# the unchanged IC5/IC8/IC9 nongradient trace density  L(rho,xi,u)  (OPTICAL_ALIGNMENT.md, "Common definitions")
Ltr = -Esy * rho**2 / (3 * mm) + mm * sp.exp((3 * u - 2) * xi) * Cpot - kap * sp.exp((3 * u - 4) * xi) / 2

NUM = lambda e: mp.mpf(str(sp.N(e, 45)))
Tn, aln, elln = NUM(Tcal), NUM(alph), NUM(ell)

# ============================================================================================ CONTROLS ===============
print("\n-- controls (these would catch my own algebra being wrong; three recover known GR results) ------------------")

Kg = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'K{min(i,j)}{max(i,j)}'))
hg = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'h{min(i,j)}{max(i,j)}'))
hgi = hg.inv()
Ktr = sum(hgi[i, j] * Kg[i, j] for i in range(3) for j in range(3))
KK = sum(hgi[i, k] * hgi[j, l] * Kg[i, j] * Kg[k, l] for i in range(3) for j in range(3) for k in range(3) for l in range(3))
Ktf2 = KK - Ktr**2 / 3
check("L8-C1 [control, GR] the bracket IC10 calls 'the ADM Einstein density' really is one: for a generic symmetric "
      "K_ij and metric h_ij, K_TF:K_TF - 2K^2/3 = K_ij K^ij - K^2 identically, so [Q_TF^2 - 2Q^2/3 + Rhat] is the ADM "
      "Lagrangian scalar (DeWitt lambda = 1)",
      sp.simplify(sp.expand(Ktf2 - 2 * Ktr**2 / 3 - (KK - Ktr**2))) == 0)

dof = lambda npair, n2nd, n1st: sp.Rational(2 * npair - n2nd - 2 * n1st, 2)
check("L8-C2 [control, GR] the counting rule (2N - n_2nd - 2 n_1st)/2 returns 2 for ADM general relativity "
      "(10 pairs h_ij,N,N_i; 8 first-class = 4 primaries + H + H_i; 0 second-class)",
      dof(10, 0, 8) == 2, f"count = {dof(10,0,8)}")
check("L8-C3 [control, GR] the SAME rule returns 3 for general relativity plus one shift-symmetric k-essence scalar "
      "(11 pairs, 8 first-class) = 2 tensor polarisations + 1 scalar -- the textbook answer this lane will compare "
      "IC10's plateau against",
      dof(11, 0, 8) == 3, f"count = {dof(11,0,8)}")

nn = sp.Symbol('n', positive=True)
Xs = sp.exp(-2 * Ssy) / 2
Ptest = Xs**nn                                    # k-essence P = X^n: textbook c_s^2 = 1/(2n-1), rho = (2n-1)X^n
PS_t, PSS_t = sp.diff(Ptest, Ssy), sp.diff(Ptest, Ssy, 2)
PX_t = sp.simplify(-PS_t / (2 * Xs))
Q_t = sp.simplify((PSS_t + PS_t) / (2 * Xs))
cs2_t = sp.simplify(PX_t / Q_t)
rho_t = sp.simplify(-PS_t - Ptest)
check("L8-C4 [control] the S <-> X dictionary that every IC10 number is expressed in -- P_X = -P_S/(2X) and "
      "Q_clock = (P_SS + P_S)/(2X) = P_X + 2X P_XX, with X = e^{-2S}/2 -- reproduces the textbook k-essence results "
      "for P = X^n: P_X = n X^{n-1}, c_s^2 = 1/(2n-1) and rho = (2n-1) X^n, hence c_s^2 = 1 and rho = X for the "
      "canonical scalar n = 1",
      sp.simplify(PX_t - nn * Xs**(nn - 1)) == 0 and sp.simplify(cs2_t - 1 / (2 * nn - 1)) == 0
      and sp.simplify(rho_t - (2 * nn - 1) * Xs**nn) == 0 and cs2_t.subs(nn, 1) == 1)

# the IC4/IC5 witness, to revalidate the frozen constant set exactly as L4 did
Fcur = (3 * (sp.Rational(8, 3) + 4 * (3 - 81 / (4 * Tcal)) * sp.Rational(1, 3)) / (16 * ell**2)) * (xi - sp.Rational(1, 4)) \
    + (3 * (-1 - 3 * (sp.Rational(8, 3) + 4 * (3 - 81 / (4 * Tcal)) * sp.Rational(1, 3)) / 8) / (16 * ell**2)) * (u - sp.Rational(2, 3))
hIC5 = (2 * Esy / mm) * (tau / (1 + sp.exp(-6 * (u - 1) * xi) * rho**2 * Fcur / (mm**2 * a02)) - rho**2 / 6) \
    + mm * sp.exp((3 * u - 2) * xi) * Cpot - (kap / 2) * sp.exp((3 * u - 4) * xi)
f_hxi = sp.lambdify((xi, u, rho, tau), sp.diff(hIC5, xi), 'mpmath')
f_hu = sp.lambdify((xi, u, rho, tau), sp.diff(hIC5, u), 'mpmath')
f_F = sp.lambdify((xi, u), Fcur, 'mpmath')
WIT = [mp.mpf(1) / 4, mp.mpf(2) / 3, -3 * mp.e**mp.mpf('-0.5'), mp.mpf(0)]
r_wit = -WIT[2] * mp.e**mp.mpf('0.5') / 3
check("L8-C5 [control] my independently transcribed constant set reproduces the IC4/IC5 expanding witness "
      "(xi,u,rho,tau) = (1/4, 2/3, -3e^{-1/2}, 0) as an EXACT stationary point of h, with F = 0 and r = 1 -- this "
      "revalidates ell, T, sigma, A_R, B_R, a0^2, Lambda, U and b before anything below uses them",
      max(abs(f_hxi(*WIT)), abs(f_hu(*WIT))) < mp.mpf(10)**-40 and abs(f_F(WIT[0], WIT[1])) < mp.mpf(10)**-40
      and close(r_wit, 1, mp.mpf(10)**-40),
      f"|h_xi|,|h_u| = {mp.nstr(abs(f_hxi(*WIT)),3)}, {mp.nstr(abs(f_hu(*WIT)),3)}")

eps = sp.Symbol('epsilon')
Ktf2s, Ktrs, Rbs, Ms = sp.symbols('Ktf2 Ktrace Rbar mstar', real=True)
J9w = sp.exp(-2 * wsy - sp.Rational(1, 6))
lhs_conf = mm * sp.exp(4 * wsy) * J9w * sp.exp(-2 * wsy) * (Ktf2s - 2 * Ktrs**2 / 3 + Rbs) / 2
lhs_bad = mm * sp.exp(4 * wsy) * (J9w * sp.exp(eps * wsy)) * sp.exp(-2 * wsy) * (Ktf2s - 2 * Ktrs**2 / 3 + Rbs) / 2
rhs_conf = mm * sp.exp(-sp.Rational(1, 6)) * (Ktf2s - 2 * Ktrs**2 / 3 + Rbs) / 2
check("L8-C6 [negative control] the IC10 conformal cancellation is not vacuous: replacing J9 = e^{-2w-1/6} by "
      "e^{-2w-1/6+eps w} leaves a residual factor e^{eps w}, so the check below WOULD fail if the exponent were wrong",
      sp.simplify(lhs_conf - rhs_conf) == 0 and sp.simplify((lhs_bad - rhs_conf).subs(eps, sp.Rational(1, 10))) != 0)

# =================================================== (Q2) IC10's LOCAL EINSTEIN-CLOCK PLATEAU ========================
print("\n-- (Q2) IC10's 'local Einstein-clock plateau', extracted as an equation and verified ------------------------")

u_of = (Ssy + 2 * wsy) / (Ssy + wsy)
Xt = sp.exp(-2 * Ssy) / 2
Ppr = -mm * sp.exp(4 * wsy) * (Lam + a02 * Ufun(u_of**2)) + kap * sp.exp(2 * wsy) * Xt
# the pressure the lead's run actually printed (optical_run_001/ic10/stdout.txt, "action_clock_pressure"), retyped
usq = u_of**2
lead_P = (-3 * (-9 * (-1 + usq) * (sp.log(1 - usq)**2 - 2 * sp.log(1 - usq) + 2) - 10
               + sp.log(sp.Rational(9765625, 3486784401)) - 5 * sp.log(sp.Rational(5, 9))**2
               + 16 * sp.log(sp.Rational(9, 5))**2) * sp.exp(-sp.Rational(1, 2)) * sp.exp(4 * wsy)
          / (8 * sp.log(sp.Rational(9, 5))**2) + 3 * sp.exp(-2 * Ssy) * sp.exp(2 * wsy))
dP = sp.simplify(sp.expand_log(sp.expand(Ppr - lead_P), force=True))
check("L8-P1 the pressure the lead's run PRINTED is exactly the pressure I transcribe from IC10_LOCAL_CLOCK.md's "
      "P = -m e^{4w}[Lambda + a0^2 U(u^2)] + kappa e^{2w} Xt with my own Lambda, a0^2 and U: the action they computed "
      "with is the action they document",
      dP == 0, "symbolic difference simplifies to 0")

Smap, wmap = (2 - u) * xi, (u - 1) * xi
jac = sp.Matrix([[sp.diff(Smap, xi), sp.diff(Smap, u)], [sp.diff(wmap, xi), sp.diff(wmap, u)]]).det()
check("L8-P2 the chart: S = (2-u)xi and w = (u-1)xi invert to xi = S+w and u = (S+2w)/(S+w), and "
      "det[d(S,w)/d(xi,u)] = xi -- so the excluded locus S+w = 0 IS xi = 0, exactly as the review states",
      sp.simplify(Smap + wmap - xi) == 0 and sp.simplify(((Smap + 2 * wmap) / (Smap + wmap)) - u) == 0
      and sp.simplify(jac - xi) == 0)

pt, qt, pp, qq, Rh, Jv = sp.symbols('p_TF q_TF p q Rhat J', real=True)
phase = 2 * pt * qt + 2 * pp * qq / 3 - (2 * pt**2 - pp**2 / 3) / (mm * Jv)
sol = sp.solve([sp.diff(phase, pt), sp.diff(phase, pp)], [pt, pp], dict=True)[0]
L10 = sp.simplify(phase.subs(sol) + mm * Jv * Rh / 2)
check("L8-P3 my own variation of IC10's phase density 2P:Q - H10 on eta=1 gives the stationary momenta "
      "P_TF = m J9 Q_TF/2 and p = -m J9 Q, and eliminating them gives "
      "L10 = m J9 [Q_TF^2 - 2Q^2/3 + Rhat]/2 - m C + kappa X",
      sp.simplify(sol[pt] - mm * Jv * qt / 2) == 0 and sp.simplify(sol[pp] + mm * Jv * qq) == 0
      and sp.simplify(L10 - mm * Jv * (qt**2 - 2 * qq**2 / 3 + Rh) / 2) == 0)

check("L8-P4 THE PLATEAU CLAIM, metric sector: with gt = e^{-2w} g, so sqrt(-g) = e^{4w} sqrt(-gt), Q = e^{-w} Kt, "
      "Rhat = e^{-2w} Rbar and J9 = e^{-2w-1/6}, the metric part of L10 sqrt(-g) equals EXACTLY "
      "m* [Kt_ij Kt^ij - Kt^2 + Rt] sqrt(-gt)/2 with m* = m e^{-1/6}: every power of w cancels, and by L8-C1 the "
      "bracket is the ADM Einstein density. CONFIRMED.",
      sp.simplify(lhs_conf - rhs_conf) == 0 and sp.simplify(rhs_conf.subs(Ms, mm * sp.exp(-sp.Rational(1, 6)))
                                                            - mm * sp.exp(-sp.Rational(1, 6)) * (Ktf2s - 2 * Ktrs**2 / 3 + Rbs) / 2) == 0,
      f"m* = m e^-1/6 = {mp.nstr(mp.e**(-mp.mpf(1)/6),12)} > 0")

Xsy = sp.Symbol('X', positive=True)
map_pot = sp.simplify((-mm * (Lam + a02 * Ufun(u**2)) + kap * Xsy) * sp.exp(4 * wsy) - (-mm * sp.exp(4 * wsy) * (Lam + a02 * Ufun(u**2)) + kap * sp.exp(4 * wsy) * Xsy))
Sfrom = sp.simplify(-sp.log(2 * Xt) / 2 - Ssy)
check("L8-P5 THE PLATEAU CLAIM, clock sector: X = -g^{mu nu}T_mu T_nu/2 = e^{-2w} Xt, so (-m C + kappa X) sqrt(-g) "
      "= [-m e^{4w} C + kappa e^{2w} Xt] sqrt(-gt) = P(Xt,w) sqrt(-gt); and S = -ln(2 Xt)/2 is exactly the xi = ln N "
      "of the clock, since Xt = e^{-2S}/2. The plateau action is Einstein(gt) + k-essence(T) + auxiliary(w).",
      map_pot == 0 and Sfrom == 0 and sp.simplify(kap * sp.exp(4 * wsy) * sp.exp(-2 * wsy) * Xsy - kap * sp.exp(2 * wsy) * Xsy) == 0)

check("L8-P6 the w equation is genuinely ALGEBRAIC and LOCAL: P's free symbols are exactly {S,w}, no derivative of w "
      "and no inverse Laplacian occurs, so w is an auxiliary field eliminated pointwise -- IC10's central locality "
      "claim, verified on the expression itself",
      Ppr.free_symbols == {Ssy, wsy} and Ppr.atoms(sp.Derivative) == set(),
      f"free symbols = {sorted(str(s) for s in Ppr.free_symbols)}")

# ------------------------------------------------------- numerics on the plateau: my own root solve and derivatives
DER = [Ppr, sp.diff(Ppr, wsy), sp.diff(Ppr, Ssy), sp.diff(Ppr, wsy, 2), sp.diff(sp.diff(Ppr, Ssy), wsy), sp.diff(Ppr, Ssy, 2)]
ev = sp.lambdify((Ssy, wsy), DER, 'mpmath')
mstar = mp.e**(-mp.mpf(1) / 6)


def solve_w(Sv):
    """my own Newton solve of the auxiliary equation P_w = 0 inside the chart -S/2 < w < 0."""
    Sv = mp.mpf(Sv)
    wv = -Sv / 4
    for _ in range(200):
        v = ev(Sv, wv)
        d = -v[1] / v[3]
        wv = wv + d
        if abs(d) < mp.mpf(10)**(-mp.mp.dps + 8):
            break
    return wv


def state(Sv):
    Sv = mp.mpf(Sv)
    wv = solve_w(Sv)
    P, Pw, PS, Pww, PSw, PSS = ev(Sv, wv)
    uv = (Sv + 2 * wv) / (Sv + wv)
    X = mp.e**(-2 * Sv) / 2
    PSSe = PSS - PSw * PSw / Pww
    PXv = -PS / (2 * X)
    Q = (PSSe + PS) / (2 * X)
    Qbare = (PSS + PS) / (2 * X)
    cs2 = PXv / Q
    energy = -PS - P
    Ht = mp.sqrt(energy / (3 * mstar)) if energy > 0 else mp.nan
    wS = -PSw / Pww
    J9 = mp.e**(-2 * wv - mp.mpf(1) / 6)
    return dict(S=Sv, w=wv, u=uv, X=X, P=P, Pw=Pw, PS=PS, Pww=Pww, PSw=PSw, PSS=PSS, PX=PXv, Q=Q, Qbare=Qbare,
                cs2=cs2, energy=energy, H=Ht, wS=wS, J9=J9, physH=mp.e**(-wv) * Ht * (1 + 3 * cs2 * wS),
                r=mp.e**Sv * J9 * Ht, A=Pww - PSw * PSw / (PSS + PS), charge=PXv * mp.sqrt(2 * X))


st = {k: state(k) for k in ('0.1', '0.15', '0.2')}
check("L8-P7 P_ww != 0 at each plateau sample, so w = w(Xt) exists locally and the elimination IC10 performs is "
      "legitimate there",
      all(abs(st[k]['Pww']) > mp.mpf('1e-3') for k in st),
      "P_ww = " + ", ".join(f"{k}:{mp.nstr(st[k]['Pww'],10)}" for k in st))

roots = []
for Sv in (mp.mpf('0.1'), mp.mpf('0.15'), mp.mpf('0.2')):
    grid = [-Sv / 2 + (Sv / 2) * mp.mpf(i) / 400 for i in range(1, 400)]
    vals = [ev(Sv, g)[1] for g in grid]
    roots.append(sum(1 for i in range(len(vals) - 1) if vals[i] * vals[i + 1] < 0))
check("L8-P8 the auxiliary root is UNIQUE in the stated chart -S/2 < w < 0 (0 < u < 1) at each sample -- a 399-point "
      "sign scan of P_w finds exactly one crossing, so the 'local clock pressure' P_eff is single-valued and the "
      "lead's choice of secant seeds is not selecting one branch out of several",
      roots == [1, 1, 1], f"sign changes found = {roots}")

J9s = sp.Symbol('J9', positive=True)
lam_of = lambda a_, c_: sp.simplify(sp.Rational(1, 3) - c_ / a_)
lam_IC10 = lam_of(mm * J9s / 2, -mm * J9s / 3)
lam_IC9 = lam_of(mm * J9s / 2, -mm / 3)
check("L8-P9 [the structural content of the IC9 -> IC10 step] IC10's trace kinetic term restores the GR DeWitt "
      "supermetric IDENTICALLY: from L10 = m J9[Q_TF^2 - 2Q^2/3 + Rhat]/2, lambda = 1 for every J9. IC9's compact "
      "Lagrangian m J9(Q_TF^2+Rhat)/2 - m Q^2/3 instead gives lambda = 1/3 + 2/(3 J9), which equals 1 only at J9 = 1 "
      "(w = -1/12, the witness). So IC9's metric sector is NOT Einstein off the witness; IC10's is.",
      sp.simplify(lam_IC10 - 1) == 0 and sp.simplify(lam_IC9 - (sp.Rational(1, 3) + 2 / (3 * J9s))) == 0
      and sp.simplify(lam_IC9.subs(J9s, 1) - 1) == 0 and sp.simplify(lam_IC9 - 1) != 0,
      f"IC9 lambda at its own sheared J9 = 0.99773128 is {mp.nstr(mp.mpf(1)/3 + 2/(3*mp.mpf('0.99773127963678760244')),12)}")

Jconst = sp.Symbol('Jc', positive=True)
resid_eta0 = sp.simplify(mm * sp.exp(4 * wsy) * Jconst * sp.exp(-2 * wsy) / (mm * sp.exp(-sp.Rational(1, 6))))
check("L8-P10 [scope] the cancellation is eta = 1 ONLY. It works because J9 carries exactly the factor e^{-2w}; the "
      "eta = 0 static plateau has no such factor (J -> const), and the same reduction then leaves a residual e^{2w}, "
      "so the 'Einstein + clock' form is a statement about the expanding plateau, not about the whole theory",
      sp.simplify(resid_eta0 - Jconst * sp.exp(2 * wsy) * sp.exp(sp.Rational(1, 6))) == 0)

# ================================================================ (Q1) THE DEGREE-OF-FREEDOM COUNT ==================
print("\n-- (Q1) the degree-of-freedom count ------------------------------------------------------------------------")

n_ic10 = dof(12, 2, 8)
check("L8-D1 IC10's own arithmetic, reproduced from my rule: 12 canonical pairs (h_ij, N, N_i, T, w) = 24 phase-space "
      "dimensions; 8 first-class constraints (4 primaries p_N, p_Ni + the Hamiltonian and 3 momentum constraints); "
      "2 second-class auxiliary constraints (p_w, C_w). (24 - 16 - 2)/2 = 3.",
      n_ic10 == 3, f"count = {n_ic10}")

check("L8-D2 [PROGRAMME REQUIREMENT, fried-chicken req 2: 'Exactly two propagating gravitational DOF, N_grav = 2'] "
      "the local count on IC10's plateau is 3, NOT 2. The extra mode L4 found in IC5/IC6/IC7 is NOT removed by IC8, "
      "IC9 or IC10; the count is identical to L4's (16-4-6)/2 = 3 under the unitary-gauge scheme. IC10 states this "
      "itself: 'locally (24-16-2)/2=3 physical modes: two tensors plus one genuine clock.'",
      n_ic10 == 2, f"count = {n_ic10} = 2 tensor + 1 clock scalar; L4's IC7 count was also {dof(8,4,3)}")

check("L8-D3 [what DID change] the CHARACTER of the third mode. In IC5/IC6/IC7 the extra scalar was GRAVITATIONAL: "
      "the lapse carried a second-class constraint, there was no local first-class Hamiltonian constraint, and the "
      "khronon propagated inside the metric sector (L4-D3). On IC10's plateau the metric sector is exactly Einstein "
      "with lambda = 1 and m* > 0 (L8-P4, L8-P9), the Hamiltonian constraint is first class again, and the third mode "
      "is a shift-symmetric k-essence CLOCK, matching L8-C3's textbook GR+k-essence count of 3. Requirement 2 permits "
      "that: 'A genuine matter or clock scalar is allowed ONLY if explicitly counted separately and shown healthy.'",
      dof(11, 0, 8) == 3 and n_ic10 == 3 and mstar > 0)

healthy = {k: (st[k]['PX'] > 0, st[k]['Q'] > 0, 0 < st[k]['cs2'] < 1, st[k]['energy'] > 0) for k in st}
check("L8-D4 [health of the third mode] at the three plateau samples S = 0.1, 0.15, 0.2 the clock is a healthy mode: "
      "m* = e^{-1/6} > 0 (no graviton ghost), P_X > 0, Q_clock = P_X + 2X P_XX > 0 (no ghost), 0 < c_s^2 < 1 (no "
      "gradient instability, subluminal on the shared conformal null cone), and rho_clock > 0. Requirement 2's "
      "'shown healthy' is MET on the sampled window.",
      all(all(v) for v in healthy.values()),
      "c_s^2 = " + ", ".join(f"{k}:{mp.nstr(st[k]['cs2'],9)}" for k in st))

id_A = sp.symbols('PSS PSw Pww PS X', nonzero=True)
PSSv, PSwv, Pwwv, PSv, Xv = id_A
A_expr = Pwwv - PSwv**2 / (PSSv + PSv)
Qcl = (PSSv - PSwv**2 / Pwwv + PSv) / (2 * Xv)
Qba = (PSSv + PSv) / (2 * Xv)
check("L8-D5 the auxiliary pair (p_w, C_w) is SECOND class -- its bracket block [[0,A],[-A,0]] has A != 0, so the "
      "multiplier is fixed, no tertiary constraint appears and exactly 2 (not 4) second-class constraints are "
      "removed; and A = P_ww Q_clock/Q_bare is an identity. The independent reviewer's A = 58.2357645080571 at "
      "S = 0.15 is reproduced from my own P.",
      sp.simplify(A_expr - Pwwv * Qcl / Qba) == 0 and all(abs(st[k]['A']) > mp.mpf(1) for k in st)
      and close(st['0.15']['A'], '58.2357645080571', mp.mpf('1e-14')),
      f"A(0.15) = {mp.nstr(st['0.15']['A'],18)}")

out_hi = state('1')
check("L8-D6 the health is WINDOW-BOUND, and the lead says so: outside eta = 1 the same continued plateau pressure "
      "gives c_s^2 < 0 at S = 1 (a gradient instability), which I reproduce as -0.604346678994200880646694; IC10: "
      "'At S=1 the continued plateau pressure has cs2<0. That failure cannot be hidden.'",
      out_hi['cs2'] < 0 and close(out_hi['cs2'], '-0.604346678994200880646694', mp.mpf('1e-18')),
      f"c_s^2(S=1) = {mp.nstr(out_hi['cs2'],21)}")

def bisect(fn, lo, hi, n=90):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    flo = fn(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if fn(mid) * flo > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


S_eta_lo = bisect(lambda S: state(S)['r']**2 - mp.mpf(3) / 4, '0.0005', '0.1')
S_ghost = bisect(lambda S: state(S)['Q'], '0.005', '0.03')
S_lum = bisect(lambda S: state(S)['cs2'] - 1, '0.03', '0.08')
ordering = (S_eta_lo < S_ghost < S_lum < mp.mpf('0.2307239914'))
check("L8-D7 [NEW LIABILITY, this lane] the healthy window is strictly SMALLER than the eta = 1 plateau, and the "
      "lead never scanned the difference. Continuing the same branch DOWN in S: the plateau's lower edge (r^2 = 3/4) "
      f"is at S = {mp.nstr(S_eta_lo,8)}, but the clock's kinetic coefficient Q_clock vanishes at "
      f"S = {mp.nstr(S_ghost,8)} and c_s^2 crosses 1 at S = {mp.nstr(S_lum,8)}. So inside eta = 1 there is a GHOST "
      f"region S < {mp.nstr(S_ghost,6)} (Q_clock < 0) and a SUPERLUMINAL band "
      f"{mp.nstr(S_ghost,6)} < S < {mp.nstr(S_lum,6)} (c_s^2 > 1 on the shared null cone). The lead's three samples "
      "and its reviewer's 101-point scan all sit in 0.1 <= S <= 0.2, entirely inside the healthy part.",
      ordering and state('0.01')['Q'] < 0 and state('0.03')['cs2'] > 1 and state('0.1')['cs2'] < 1,
      f"Q_clock(S=0.01) = {mp.nstr(state('0.01')['Q'],8)} < 0; c_s^2(S=0.03) = {mp.nstr(state('0.03')['cs2'],8)} > 1; "
      f"c_s^2(S=0.1) = {mp.nstr(state('0.1')['cs2'],8)} < 1")

roots_lo = []
for Sv in (mp.mpf('0.01'), mp.mpf('0.05')):
    grid = [-Sv / 2 + (Sv / 2) * mp.mpf(i) / 400 for i in range(1, 400)]
    vals = [ev(Sv, g)[1] for g in grid]
    roots_lo.append(sum(1 for i in range(len(vals) - 1) if vals[i] * vals[i + 1] < 0))
check("L8-D8 [consequence] that region is in the PAST of the lead's own solution, not off to one side. IC10's own "
      "evolution law dS/dtau = 3 H c_s^2 is positive on the healthy branch, so S increases with time; running the "
      "S = 0.1 -> 0.2 solution BACKWARDS therefore drives it through c_s^2 = 1 and then through Q_clock = 0, while "
      "eta is still exactly 1 and P_w = 0 still has its unique root in the chart. This is not a continuation "
      "artefact: the auxiliary root stays unique at S = 0.01 and 0.05, u stays in (0,1), and |P_w| < 1e-37 throughout.",
      roots_lo == [1, 1] and 0 < state('0.01')['u'] < 1 and 0 < state('0.05')['u'] < 1
      and abs(state('0.01')['Pw']) < mp.mpf('1e-30') and all(state(k)['cs2'] > 0 for k in ('0.1', '0.15', '0.2')),
      f"u(0.01) = {mp.nstr(state('0.01')['u'],8)}, |P_w| = {mp.nstr(abs(state('0.01')['Pw']),3)}, "
      f"unique roots = {roots_lo}")

# ============================================ (Q3) DO IC8 AND IC9 CLOSE L4's TWO LIABILITIES? =======================
print("\n-- (Q3) do IC8 and IC9 close L4's two liabilities (narrow repair window, tensor-cone detuning)? -------------")

optical = (2 - u) * xi
K9 = 2 * sp.exp(optical + sp.Rational(1, 6)) / mm
c9 = mm * sp.exp(optical - sp.Rational(1, 6))
Dt9 = lambda f_: sp.diff(f_, u) + xi / (2 - u) * sp.diff(f_, xi)          # null direction of IC9's |D S|^2
v9 = (sp.diff(c9, rho) / 2, Dt9(c9))
check("L8-A1 [liability 1 CLOSED, structurally] IC9's curvature-response vector vanishes IDENTICALLY. With "
      "D_t = d_u + xi/(2-u) d_xi (the null direction of IC9's replacement gradient term |D S|^2), both components of "
      "IC7's v = (c_rho/2, D_t c) are zero for ALL (rho,xi,u), because c9 and K9 depend only on the optical scalar "
      "S = (2-u)xi. Hence IC7's quartic S_4 = -4 v^T M^{-1} v is identically 0 with NO counterterm and NO theta "
      "cutoff -- so L4's finite repair window |j-1| < 0.074, which existed only because theta switched off, does not "
      "arise. This is a structural fix, not a numerical one.",
      sp.simplify(v9[0]) == 0 and sp.simplify(v9[1]) == 0 and sp.simplify(sp.diff(K9, rho)) == 0
      and sp.simplify(Dt9(K9)) == 0)

c7s, R0s = sp.symbols('c7 Rbar0', real=True)
B3 = sp.Symbol('B3', positive=True)
light2 = sp.exp(2 * optical) / B3**2
cone = lambda Kc, Gc: sp.simplify(4 * Kc * Gc / light2)
cT2_GR = sp.simplify(4 * (1 / mm) * (mm / (4 * B3**2)) * B3**2)
cT2_IC9 = cone(K9 / 2, c9 / (4 * B3**2))
cT2_IC9_detune = sp.simplify(cone(K9 / 2, c9 / (4 * B3**2) - c7s * R0s / B3**2).subs(c7s, 0))
check("L8-A2 [liability 2 CLOSED] IC9 carries NO Rbar^2 term at all ('There is no curvature-square term'), so "
      "c_7 = 0 and L4's exact detuning formula c_T^2 = 1 - 4 c_7 Rbar_0/c returns 1 for EVERY background curvature "
      "Rbar_0. The detuning L4 quantified at 0.008571 per unit Rbar_0 is removed by removing its source.",
      sp.simplify(cT2_IC9_detune - 1) == 0)

check("L8-A3 [independent confirmation] from my own tensor reduction -- the same one that returns c_T^2 = 1 for pure "
      "ADM general relativity -- IC9's cone identity K9 c9 = 2 e^{2S} holds IDENTICALLY in (xi,u), so c_T^2 = 1 on "
      "every background of the family, not just at the sampled states. IC9's table entry 'computed cT2 = 1' is "
      "confirmed as an exact identity.",
      sp.simplify(cT2_GR - 1) == 0 and sp.simplify(cT2_IC9 - 1) == 0
      and sp.powsimp(sp.simplify(K9 * c9 / (2 * sp.exp(2 * optical))), combine='exp') == 1)

sig8 = -sp.Rational(1, 4)
s8 = xi + bpar * u - sp.Rational(1, 4) - 2 * bpar / 3
K8 = 2 * sp.exp(sp.Rational(1, 2) + sig8 * s8) / mm
J8 = 2 * Esy / (mm * K8)
c8 = mm * sp.exp(u * xi) * J8
Dt8 = lambda f_: sp.diff(f_, u) - bpar * sp.diff(f_, xi)                  # null direction of IC8's |D(xi+bu)|^2
cT2_IC8 = cone(K8 / 2, c8 / (4 * B3**2))
check("L8-A4 [scope caveat on IC9's headline] the SAME cone identity holds for IC8: K8 c8 = 2 e^{2S} identically, so "
      "IC8's principal tensor cone is ALSO exactly 1 -- yet IC8's own report says 'on the re-solved sheared "
      "background the even tensor speed squared approaches approximately 1.00244, 1.01257 and 1.02487 on the three "
      "axes.' Those numbers come from the finite-k companion-matrix evolution, not from the principal symbol. IC9's "
      "table reports only the principal quantity, and the corresponding finite-k number is not in IC9's output. So "
      "IC9's 'cT2 = 1' does not by itself demonstrate that IC8's detuning is absent in IC9.",
      sp.simplify(cT2_IC8 - 1) == 0 and sp.simplify(sp.diff(K8, rho)) == 0 and sp.simplify(Dt8(K8)) == 0)

check("L8-A5 IC8 does NOT close liability 1: its curvature coefficient is not annihilated by its own passive "
      "direction (D_t c8 != 0), so IC8 still needs IC7's cutoff-defined counterterm d8, and inherits its finite "
      "theta window. Only IC9's choice -- making BOTH K and c functions of the optical scalar S alone, and making "
      "the gradient term |D S|^2 -- removes the counterterm.",
      sp.simplify(Dt8(c8)) != 0, f"D_t c8 at the witness = {mp.nstr(NUM(Dt8(c8).subs({xi: sp.Rational(1,4), u: sp.Rational(2,3)})),8)}")

xw, alw, Tsy = sp.symbols('x alpha T_', positive=True)
den_fw = 2 * ((64 * Tsy + 243) * alw * xw + 432 * Tsy - 2916)
a_fw = 9 * (16 * Tsy + alw * xw) / den_fw
a_printed = 9 * (16 * Tsy + alw * xw) / (2 * (64 * Tsy * alw * xw + 432 * Tsy + 243 * alw * xw - 2916))
den_root = (2916 - 432 * Tsy) / ((64 * Tsy + 243) * alw)
check("L8-A6 IC9's finite-wave coefficient a = 9(16T + alpha x)/[2((64T+243)alpha x + 432T - 2916)] is positive with "
      "no positive-x pole exactly when T > 27/4: its only denominator root is x = (2916 - 432T)/[(64T+243)alpha], "
      "which is negative iff T > 27/4 and sits exactly at x = 0 when T = 27/4. The lead's sentence 'This is positive "
      "and has no positive-x pole for Tcal>27/4, alpha>0' is CONFIRMED, and 27/4 is the exact threshold, not merely a "
      "sufficient condition.",
      sp.simplify(a_fw - a_printed) == 0 and sp.simplify(den_fw.subs(xw, den_root)) == 0
      and sp.simplify(den_root.subs(Tsy, sp.Rational(27, 4))) == 0
      and NUM(den_root.subs({Tsy: Tcal, alw: alph})) < 0 and Tn > mp.mpf(27) / 4,
      f"T = {mp.nstr(Tn,10)} > 6.75; denominator root at x = {mp.nstr(NUM(den_root.subs({Tsy: Tcal, alw: alph})),8)}")

Mrep = sp.Matrix([[24, -6], [-6, sp.Rational(27, 16)]])
vopt = sp.Matrix([sp.Rational(4, 3), -sp.Rational(1, 4)])
dval = (vopt.T * (-Mrep).inv() * vopt)[0]
Erep = xw * (2 * alw * xw - 2 * xw + 9) / (2 * alw * xw + 9)
pole = -9 / (2 * alw)
residue = sp.simplify(sp.numer(sp.together(Erep)).subs(xw, pole) / sp.diff(sp.denom(sp.together(Erep)), xw).subs(xw, pole))
check("L8-A7 IC9's OWN residual liability reproduces exactly: the potential-only repair gives "
      "d = v^T(-M)^{-1} v = -1/9 < 0 and leaves an uncancelled pole at x = -9/(2 alpha) with residue -81/(4 alpha^3) "
      "!= 0. IC9's statement 'this particular repair does not remove the spatial factor' is CONFIRMED.",
      sp.simplify(dval + sp.Rational(1, 9)) == 0 and sp.simplify(residue + 81 / (4 * alw**3)) == 0,
      f"d = {dval}, residue = {residue}")

# ================================================== (Q4) SPOT-CHECKS OF optical_run_001/ ============================
print("\n-- (Q4) spot-checks of optical_run_001/, rebuilt by hand ---------------------------------------------------")

LEAD = {'0.1': dict(w='-0.0336785175781002342051038', u='0.49219293133623656258361', PX='1.94070000788217149928783',
                    Q='5.25981081709608022629022', cs2='0.368967644534718063892517', energy='2.6703390023420635477895',
                    physH='0.719274745451737598282073', r='1.02615650412538494573224'),
        '0.15': dict(w='-0.0475000399259978283611151', u='0.536584795821343765583739', PX='1.75598034358457346247555',
                     Q='5.73169926269462558583761', cs2='0.306362958540682400674127', energy='2.45445965675571735128969',
                     physH='0.781458668516051543784086', r='1.06323263301950255497539'),
        '0.2': dict(w='-0.0600988487738407985995266', u='0.570419197789965663436675', PX='1.54851465315593232539346',
                    Q='5.84107512491027559696033', cs2='0.265107813209253829905982', energy='2.24994509974193576470111',
                    physH='0.807702987853333560710055', r='1.09747394765126597637313')}
worst, worst_key = mp.mpf(0), ''
for k, ref in LEAD.items():
    for q, val in ref.items():
        d = abs(st[k][q] - mp.mpf(val)) / max(mp.mpf(1), abs(mp.mpf(val)))
        if d > worst:
            worst, worst_key = d, f"S={k}:{q}"
check("L8-R1 all 24 numbers of IC10's three plateau rows (w, u, P_X, Q_clock, c_s^2, energy, physical H, activation "
      "r) reproduce from my own pressure, my own Newton solve and my own k-essence dictionary",
      worst < mp.mpf('1e-22'), f"worst relative difference {mp.nstr(worst,3)} at {worst_key}")

a_, b_ = state('0.1'), state('0.2')
efolds = mp.quad(lambda S: 1 / (3 * state(S)['cs2']), [mp.mpf('0.1'), mp.mpf('0.2')])
ptime = mp.quad(lambda S: 1 / (3 * state(S)['H'] * state(S)['cs2']), [mp.mpf('0.1'), mp.mpf('0.2')])
phys_e = efolds + b_['w'] - a_['w']
charge = mp.e**(3 * efolds) * b_['charge'] / a_['charge']
check("L8-R2 the finite FLRW quadrature: from the exact k-essence relations dS/dtau = 3 H c_s^2 and "
      "dln(barA)/dS = 1/(3 c_s^2), which I derive independently from a^3 P_X sqrt(2X) = const, the S = 0.1 -> 0.2 "
      "run gives 0.108584184534843401 barred e-folds, 0.0821638533391028370 physical e-folds and 0.110756742119829669 "
      "tilde proper-time units, and the conserved clock charge closes to 1",
      close(efolds, '0.108584184534843401416970621034', mp.mpf('1e-22'))
      and close(phys_e, '0.0821638533391028370225477978314', mp.mpf('1e-22'))
      and close(ptime, '0.110756742119829669060587804501', mp.mpf('1e-22'))
      and close(charge, 1, mp.mpf('1e-22')),
      f"charge ratio = {mp.nstr(charge,20)}")

lo, hi = mp.mpf('0.2'), mp.mpf('0.3')
for _ in range(100):
    mid = (lo + hi) / 2
    if state(mid)['r']**2 < mp.mpf(5) / 4:
        lo = mid
    else:
        hi = mid
Sb = (lo + hi) / 2
sb = state(Sb)
check("L8-R3 the next eta = 1 boundary: solving r^2 = 5/4 on the same continuation gives "
      "S = 0.230723991364997997, u = 0.587907209285499307, r = sqrt(5)/2 and c_s^2 = 0.242306706149330325 -- all four "
      "reproduced, and the reviewer's independently recovered crossing agrees",
      close(Sb, '0.230723991364997997176132', mp.mpf('1e-20')) and close(sb['u'], '0.587907209285499307236142', mp.mpf('1e-20'))
      and close(sb['cs2'], '0.242306706149330324562731', mp.mpf('1e-20')) and close(sb['r'], mp.sqrt(5) / 2, mp.mpf('1e-30')),
      f"S_boundary = {mp.nstr(Sb,21)}")

out_mid = state('0.5')
check("L8-R4 the two OUTSIDE-plateau continuation controls reproduce too: at S = 0.5, w = -0.119017564595326503, "
      "u = 0.687603538811683182, c_s^2 = 0.0193874674410151395 with r = 1.31016315739452534 > sqrt(5)/2 (outside "
      "eta = 1); at S = 1, u = 0.772488622079604143 and r = 1.83657650611313338. The lead labels both as continuation "
      "controls rather than solutions, which is the correct label.",
      close(out_mid['w'], '-0.119017564595326503202617', mp.mpf('1e-20'))
      and close(out_mid['cs2'], '0.0193874674410151395448578', mp.mpf('1e-20'))
      and close(out_mid['r'], '1.31016315739452534367411', mp.mpf('1e-20'))
      and close(out_hi['u'], '0.772488622079604142733495', mp.mpf('1e-20'))
      and close(out_hi['r'], '1.83657650611313338161932', mp.mpf('1e-20'))
      and out_mid['r']**2 > mp.mpf(5) / 4)

# ---- IC9's principal table, rebuilt from OPTICAL_ALIGNMENT.md's formulas with my own h
Ssub = {xi: Ssy / (2 - u)}
Ltr_S = Ltr.subs(Ssub)
Ks_S, cs_S = K9.subs(Ssub), c9.subs(Ssub)
Bcoef = mm * alph * sp.exp(u * Ssy / (2 - u))
a_zeta = Ks_S / 12 + sp.diff(Ltr_S, rho, 2) / 4 - sp.diff(sp.diff(Ltr_S, rho), u)**2 / (4 * sp.diff(Ltr_S, u, 2))
g_zeta = 2 * (sp.diff(cs_S, Ssy)**2 / Bcoef - cs_S)
prin = sp.lambdify((rho, Ssy, u), [a_zeta, g_zeta, sp.diff(Ltr_S, u, 2), a_zeta * g_zeta / sp.exp(2 * Ssy)], 'mpmath')

hIC9 = K9 * tau + Ltr
HES = sp.lambdify((xi, u, rho, tau), [sp.diff(hIC9, xi, 2), sp.diff(sp.diff(hIC9, xi), u), sp.diff(hIC9, u, 2)], 'mpmath')
GRD = sp.lambdify((xi, u, rho, tau), [sp.diff(hIC9, xi), sp.diff(hIC9, u)], 'mpmath')


def solve_aux9(rv, tv):
    q = mp.matrix([mp.mpf(1) / 4, mp.mpf(2) / 3])
    for _ in range(200):
        g = mp.matrix(GRD(q[0], q[1], rv, tv))
        hxx, hxu, huu = HES(q[0], q[1], rv, tv)
        d = mp.lu_solve(mp.matrix([[hxx, hxu], [hxu, huu]]), -g)
        q = q + d
        if mp.norm(d) < mp.mpf(10)**-45:
            break
    return q[0], q[1]


lamsh = [mp.mpf('-0.6424435072183933'), mp.mpf('-0.622272178918671'), mp.mpf('-0.5676134368548011')]
rsh, tsh = sum(lamsh), sum(x**2 for x in lamsh) - sum(lamsh)**2 / 3
IC9 = {}
for nm, (rv, tv) in (('isotropic', (-3 * mp.e**mp.mpf('-0.5'), mp.mpf(0))),
                     ('neighbor', (-3 * mp.e**mp.mpf('-0.5') * mp.mpf('1.007'), mp.mpf(0))),
                     ('sheared', (rsh, tsh))):
    xv, uv = solve_aux9(rv, tv)
    Sv = (2 - uv) * xv
    az, gz, Ltt, cs2v = prin(rv, Sv, uv)
    IC9[nm] = dict(xi=xv, u=uv, S=Sv, J=mp.e**(-2 * (uv - 1) * xv - mp.mpf(1) / 6), cs2=cs2v, mass=1 / az, Ltt=Ltt)

check("L8-R5 IC9's homogeneous principal table, rebuilt from my own h: the three backgrounds solve to "
      "xi = 0.25 / 0.24297808830014161622 / 0.24500221816306024072 with J9 = 1 / 0.99687683013160702409 / "
      "0.99773127963678760244, and its scalar speeds are 0.181932469587580540, 0.203829766908273217 and "
      "0.198458457703891493, with scalar mass 176.694087400156673 and passive Hessian -24.847606040647032 at the "
      "witness -- every entry reproduced",
      close(IC9['isotropic']['xi'], mp.mpf(1) / 4, mp.mpf('1e-30'))
      and close(IC9['neighbor']['xi'], '0.24297808830014161622', mp.mpf('1e-19'))
      and close(IC9['sheared']['xi'], '0.24500221816306024072', mp.mpf('1e-19'))
      and close(IC9['sheared']['J'], '0.99773127963678760244', mp.mpf('1e-19'))
      and close(IC9['isotropic']['cs2'], '0.181932469587580540283804', mp.mpf('1e-22'))
      and close(IC9['neighbor']['cs2'], '0.203829766908273217176351', mp.mpf('1e-22'))
      and close(IC9['sheared']['cs2'], '0.198458457703891492874301', mp.mpf('1e-22'))
      and close(IC9['isotropic']['mass'], '176.694087400156673278781', mp.mpf('1e-22'))
      and close(IC9['isotropic']['Ltt'], '-24.8476060406470321798286', mp.mpf('1e-22')),
      f"sheared c_s^2 = {mp.nstr(IC9['sheared']['cs2'],21)}")

Hxx, Hxu, Huu = HES(mp.mpf(1) / 4, mp.mpf(2) / 3, -3 * mp.e**mp.mpf('-0.5'), mp.mpf(0))
slope = (mp.mpf(1) / 4) / (2 - mp.mpf(2) / 3)
Ltt_from_L4 = Hxx * slope**2 + 2 * Hxu * slope + Huu
norm = mp.e**mp.mpf('-0.5')
check("L8-R6 [cross-check between lanes] IC9's 'passive Hessian' is exactly L4's already-verified auxiliary Hessian "
      "rotated into the fixed-S direction: with L4's normalised H = -e^{-1/2}[[24,-27],[-27,2T+135/8]] and "
      "dxi/du = xi/(2-u) = 3/16, the quadratic form gives e^{-1/2}[-24(3/16)^2 + 54(3/16) - (2T+135/8)] = "
      "-24.8476060406470322, IC9's number. The two lanes' transcriptions agree.",
      close(Ltt_from_L4, '-24.8476060406470321798286', mp.mpf('1e-22'))
      and close(Hxx / norm, -24, mp.mpf('1e-30')) and close(Hxu / norm, 27, mp.mpf('1e-30'))
      and close(Huu / norm, -(2 * Tn + mp.mpf(135) / 8), mp.mpf('1e-30')),
      f"L_tt = {mp.nstr(Ltt_from_L4,21)}")

print("\n-- what this lane did NOT independently verify ---------------------------------------------------------------")
for line in ("IC8's and IC9's finite-k companion-matrix speeds (the 1.00244 / 1.01257 / 1.02487 numbers and their "
             "complex parts): that needs the lead's full even-sector pencil with background time derivatives, which "
             "L4 also did not rebuild;",
             "IC10's full nonlinear, distribution-valued gravitational constraint algebra -- the lead does not claim "
             "it either ('This count is a plateau action argument, not a global IC10 Dirac certificate');",
             "everything off eta = 1: the transition, the matter-coupled characteristic matrix and strong-coupling "
             "scale, PPN, measured G, lensing, galactic matching, y = 0 control and any realistic cosmology. All "
             "remain as the lead states them: OPEN."):
    print(f"    - {line}")

print("\n" + "=" * 122)
hard = [n for n in FAILS if not n.startswith('L8-D2')]
print(f"L8 verification: {len(FAILS)} FAIL(S)" if FAILS else "L8 verification: ALL CHECKS PASS")
for n in FAILS:
    print(f"    FAIL: {n.split('.')[0]}")
print("    Every reproduction check of the lead's own IC8/IC9/IC10 numbers PASSES, to the precision it quotes. The")
print("    single FAIL is the programme's N_grav = 2 requirement read as a TOTAL mode count: IC10's plateau still")
print("    carries three modes, as L4 found for IC7. What changed is the third mode's CHARACTER (L8-D3): it is now a")
print("    separately counted k-essence clock outside a pure-Einstein metric sector, which requirement 2 permits when")
print("    it is shown healthy -- and on the lead's sampled window it is (L8-D4). Two liabilities L4 raised against")
print("    IC7 are CLOSED structurally by IC9 (L8-A1, L8-A2). One NEW liability is added by this lane (L8-D7/D8):")
print("    inside the same eta = 1 plateau, below S = 0.0377 the clock is superluminal and below S = 0.0267 it is a")
print("    ghost, and that region lies in the PAST of the lead's own expanding solution.")
print("    Exit 2 marks the designed requirement failure; exit 1 would mean one of the lead's numbers failed.")
print("=" * 122)
sys.exit(1 if hard else (2 if FAILS else 0))
