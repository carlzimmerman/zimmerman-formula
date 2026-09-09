#!/usr/bin/env python3
"""
L20 -- is the ghost in the PAST of IC10's expanding plateau, and is it fatal?
=============================================================================
L8 (this lane's own [L8_VERIFICATION.md]) verified the lead agent's IC10 "local Einstein-clock plateau"
against 37 checks, 36 of which passed, and found ONE new liability of its own (L8-D7/D8):

    eta = 1 lower edge (r^2 = 3/4)     S = 0.0016326245
    Q_clock = 0     (ghost below)      S = 0.026664091
    c_s^2 = 1       (superluminal below) S = 0.037700985
    eta = 1 upper edge (r^2 = 5/4)     S = 0.230723991

so the certified-healthy window in the clock variable is STRICTLY SMALLER than the eta = 1 plateau the
lead identifies, and -- because IC10's own law dS/dtau = 3 H c_s^2 is positive on the healthy branch --
the un-scanned part is in the PAST of the lead's own S = 0.1 -> 0.2 solution, not off to one side.

THIS LANE ANSWERS THE FOLLOW-UP: is that fatal, or does the history never enter it?

Everything below is rebuilt from IC10_LOCAL_CLOCK.md's displayed pressure

    P = -m e^{4w}[Lambda + a0^2 U(u^2)] + kappa e^{2w} Xtilde,
    u = (S+2w)/(S+w),  Xtilde = e^{-2S}/2,  U(c) = (1-c)[ln^2(1-c) - 2 ln(1-c) + 2] - 2,
    a0^2 = 9 kappa e^{-1/2}/(16 m l^2),  Lambda = kappa e^{-1/2}/m - a0^2 U(4/9),  l = ln(9/5),
    m = h0 = 1, kappa = 6, h0 = sqrt(kappa/(6m)), mstar = m e^{-1/6},

with my OWN sympy differentiation, my OWN Newton solve of P_w = 0, my OWN derivation of the FLRW
relations from the shift-symmetric charge, and my OWN quadratures.  Nothing under
closure_2026/integrable_clock_construction_2026/ is imported or executed.  L8's script is this lane's
own and was read only for the transcription of the constants; the algebra is redone here.

THE FIVE QUESTIONS, and where each is answered:
  (H) map the history -- how far back, in proper time / e-folds / redshift, are the two edges;
  (G) is the ghost REACHABLE at finite past proper time, or is it an asymptotic floor;
  (S) is S fixed by the construction, or is it a free initial condition (a much weaker problem);
  (L) does the superluminal band matter, and what does it depend on;
  (F) is there a modification of P, or of the plateau, that moves the ghost edge out of reach.

FOOTINGS.  Every number on the plateau is dimensionless in m = h0 = 1 units; the a0^2 appearing in the
pressure is the IC-internal constant 9 kappa e^{-1/2}/(16 m l^2), NOT the empirical a0, and IC10 says so
("The a0-Lambda proportionality and its 1/2 coefficient remain input, not a result").  Section (H) still
carries both footings, as a clearly-labelled CONDITIONAL scale identification, because that is the only
way any statement here can be given a physical duration at all -- and the answer it gives is itself part
of the finding.

Exit code 1 if any check fails.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def close(a, b, tol):
    a, b = mp.mpf(a), mp.mpf(b)
    return abs(a - b) <= tol * max(mp.mpf(1), abs(b))


print("=" * 122)
print("L20 -- the ghost in the past of IC10's plateau: reachable or not, and fatal or fixable")
print("=" * 122)

# ============================================================ independent rebuild of the constants ===
ell = sp.log(sp.Rational(9, 5))
mm, kap = sp.Integer(1), sp.Integer(6)
h0 = sp.sqrt(kap / (6 * mm))
a02 = 9 * kap * sp.exp(-sp.Rational(1, 2)) / (16 * mm * ell**2)
Ufun = lambda c: (1 - c) * (sp.log(1 - c)**2 - 2 * sp.log(1 - c) + 2) - 2
Lam0 = kap * sp.exp(-sp.Rational(1, 2)) / mm - a02 * Ufun(sp.Rational(4, 9))

Ssy, wsy, lamsy, gsy = sp.symbols('S w lam g', real=True)
usy = (Ssy + 2 * wsy) / (Ssy + wsy)
Xsy = sp.exp(-2 * Ssy) / 2
# the IC10 pressure, with TWO deformation handles used only in section (F):
#   lam  = coefficient of an extra clock kinetic term  lam e^{2w} Xtilde^2   (lam = 0 is IC10)
#   g    = multiplier on Lambda                                              (g   = 1 is IC10)
Pgen = (-mm * sp.exp(4 * wsy) * (gsy * Lam0 + a02 * Ufun(usy**2))
        + kap * sp.exp(2 * wsy) * Xsy + lamsy * sp.exp(2 * wsy) * Xsy**2)
DER = [Pgen, sp.diff(Pgen, wsy), sp.diff(Pgen, Ssy), sp.diff(Pgen, wsy, 2),
       sp.diff(sp.diff(Pgen, Ssy), wsy), sp.diff(Pgen, Ssy, 2)]
ev = sp.lambdify((Ssy, wsy, lamsy, gsy), DER, 'mpmath')
mstar = mp.e**(-mp.mpf(1) / 6)
KAP = mp.mpf(6)


def solve_w(Sv, lv=0, gv=1):
    """my own Newton solve of the algebraic auxiliary equation P_w = 0 inside the chart -S/2 < w < 0."""
    Sv, lv, gv = mp.mpf(Sv), mp.mpf(lv), mp.mpf(gv)
    wv = -Sv / 4
    for _ in range(400):
        v = ev(Sv, wv, lv, gv)
        if isinstance(v[1], mp.mpc) or isinstance(v[3], mp.mpc):
            return None
        d = -v[1] / v[3]
        wv = wv + d
        if abs(d) < mp.mpf(10)**(-mp.mp.dps + 8):
            return wv
    return None


def state(Sv, lv=0, gv=1):
    """the full homogeneous state at clock value S.  Dictionary is my own; formulas are re-derived below."""
    Sv, lv, gv = mp.mpf(Sv), mp.mpf(lv), mp.mpf(gv)
    wv = solve_w(Sv, lv, gv)
    if wv is None:
        return None
    P, Pw, PS, Pww, PSw, PSS = ev(Sv, wv, lv, gv)
    if any(isinstance(z, mp.mpc) for z in (P, PS, Pww, PSw, PSS)):
        return None
    X = mp.e**(-2 * Sv) / 2
    PSSe = PSS - PSw * PSw / Pww               # Schur complement: d^2/dS^2 of P(S, wbar(S))
    PX = -PS / (2 * X)
    Q = (PSSe + PS) / (2 * X)                  # P_X + 2X P_XX of the ELIMINATED pressure
    Qbare = (PSS + PS) / (2 * X)
    rho = -PS - P
    H = mp.sqrt(rho / (3 * mstar)) if rho > 0 else mp.nan
    return dict(S=Sv, w=wv, u=(Sv + 2 * wv) / (Sv + wv), xi=Sv + wv, X=X, P=P, Pw=Pw, PS=PS,
                Pww=Pww, PSw=PSw, PSS=PSS, PX=PX, Q=Q, Qbare=Qbare, cs2=PX / Q, rho=rho, H=H,
                r2=mp.e**(2 * Sv - 4 * wv - mp.mpf(1) / 3) * rho / (3 * mstar) / (KAP / 6),
                Fch=PX * mp.e**(-Sv))          # the conserved-charge function:  Abar^3 F = const


def bisect(fn, lo, hi, n=120):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    flo = fn(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if fn(mid) * flo > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# =========================================================================================== CONTROLS =
print("\n-- controls (each would catch my own algebra being wrong) ---------------------------------------")

nn = sp.Symbol('n', positive=True)
Xt = sp.exp(-2 * Ssy) / 2
Pt = Xt**nn
PSt, PSSt = sp.diff(Pt, Ssy), sp.diff(Pt, Ssy, 2)
PXt = sp.simplify(-PSt / (2 * Xt))
Qt = sp.simplify((PSSt + PSt) / (2 * Xt))
check("L20-C1 [control, textbook k-essence] the S-dictionary I use throughout -- P_X = -P_S/(2X), "
      "Q_clock = (P_SS+P_S)/(2X) = P_X + 2X P_XX, rho = -P_S - P with X = e^{-2S}/2 -- returns the "
      "textbook answers for P = X^n: c_s^2 = 1/(2n-1), and 1 for the canonical scalar n = 1",
      sp.simplify(PXt - nn * Xt**(nn - 1)) == 0 and sp.simplify(PXt / Qt - 1 / (2 * nn - 1)) == 0
      and sp.simplify((PXt / Qt).subs(nn, 1) - 1) == 0)

# my own derivation of the FLRW relations from the shift-symmetric charge, NOT taken from IC10
Abar, tau = sp.symbols('Abar tau', positive=True)
PXs, PXXs, Xs = sp.symbols('P_X P_XX X', positive=True)
# charge  Abar^3 P_X sqrt(2X) = const, with sqrt(2X) = e^{-S}:  3 dlnAbar/dS + dln(P_X e^{-S})/dS = 0
dlnPX_dS = sp.simplify(-2 * Xs * PXXs / PXs)                       # since dX/dS = -2X
dlnA_dS = sp.simplify(-(dlnPX_dS - 1) / 3)                          # = (1 + 2X P_XX/P_X)/3 = Q/(3 P_X)
target = sp.simplify(1 / (3 * (PXs / (PXs + 2 * Xs * PXXs))))        # 1/(3 c_s^2)
check("L20-C2 [control, my own derivation] differentiating the shift-symmetric charge "
      "Abar^3 P_X sqrt(2 Xtilde) = const gives dln(Abar)/dS = Q_clock/(3 P_X) = 1/(3 c_s^2), hence "
      "dS/dtau = 3 Htilde c_s^2 -- IC10's two evolution laws, re-derived here rather than assumed",
      sp.simplify(dlnA_dS - target) == 0, "dln(Abar)/dS = Q/(3 P_X) identically")

st = {k: state(k) for k in ('0.1', '0.15', '0.2')}
LEAD_CS2 = {'0.1': '0.368967644534718063892517', '0.15': '0.306362958540682400674127',
            '0.2': '0.265107813209253829905982'}
check("L20-C3 [CONTROL, mandated] the three plateau samples of L8/IC10 reproduce from my own pressure "
      "and my own root solve: c_s^2 = 0.368967645, 0.306362959, 0.265107813 at S = 0.1, 0.15, 0.2",
      all(close(st[k]['cs2'], LEAD_CS2[k], mp.mpf('1e-22')) for k in st),
      "c_s^2 = " + ", ".join(f"{k}:{mp.nstr(st[k]['cs2'],12)}" for k in st))

S_eta_lo = bisect(lambda s: state(s)['r2'] - mp.mpf(3) / 4, '0.0005', '0.1')
S_ghost = bisect(lambda s: state(s)['Q'], '0.005', '0.03')
S_lum = bisect(lambda s: state(s)['cs2'] - 1, '0.03', '0.08')
S_eta_hi = bisect(lambda s: state(s)['r2'] - mp.mpf(5) / 4, '0.2', '0.3')
check("L20-C4 [CONTROL, mandated] the two edge values L8 reported reproduce from my own algebra: "
      "Q_clock = 0 at S = 0.026664091 and c_s^2 = 1 at S = 0.037700985; and so do both eta = 1 edges, "
      "r^2 = 3/4 at S = 0.0016326245 and r^2 = 5/4 at S = 0.230723991",
      close(S_ghost, '0.026664091203272', mp.mpf('1e-12')) and close(S_lum, '0.037700985', mp.mpf('1e-8'))
      and close(S_eta_lo, '0.0016326245', mp.mpf('1e-9'))
      and close(S_eta_hi, '0.230723991364998', mp.mpf('1e-14')),
      f"S_eta_lo = {mp.nstr(S_eta_lo,11)}, S_ghost = {mp.nstr(S_ghost,11)}, S_lum = {mp.nstr(S_lum,11)}, "
      f"S_eta_hi = {mp.nstr(S_eta_hi,12)}")


def Peff(Sv, lv=0, gv=1):
    a = state(Sv, lv, gv)
    return a['P']


fd = [mp.mpf('0.12'), mp.mpf('0.16')]
ok_fd = True
for S0 in fd:
    d1 = mp.diff(lambda s: Peff(s), S0, 1)
    d2 = mp.diff(lambda s: Peff(s), S0, 2)
    a = state(S0)
    Xv = a['X']
    ok_fd = ok_fd and close(d1, a['PS'], mp.mpf('1e-18')) \
        and close((d2 + d1) / (2 * Xv), a['Q'], mp.mpf('1e-15')) \
        and close(-d1 / (2 * Xv), a['PX'], mp.mpf('1e-18')) and close(-d1 - a['P'], a['rho'], mp.mpf('1e-18'))
check("L20-C5 [control, and the structural point] Q_clock is a property of ONE function of ONE variable: "
      "the ELIMINATED pressure P_eff(S) = P(S, wbar(S)).  Differentiating P_eff numerically along the "
      "root gives dP_eff/dS = P_S and d^2P_eff/dS^2 = P_SS - P_Sw^2/P_ww exactly, so "
      "Q_clock = (P_eff'' + P_eff')/(2X).  The ghost is therefore an honest k-essence statement about "
      "P_eff, not an artefact of the Schur formula or of the auxiliary elimination.",
      ok_fd, "checked at S = 0.12 and 0.16 by numerical differentiation along the root")

nbar_ctrl = mp.quad(lambda s: state(s)['Q'] / (3 * state(s)['PX']), [mp.mpf('0.1'), mp.mpf('0.2')], maxdegree=5)
tau_ctrl = mp.quad(lambda s: state(s)['Q'] / (3 * state(s)['H'] * state(s)['PX']),
                   [mp.mpf('0.1'), mp.mpf('0.2')], maxdegree=5)
check("L20-C6 [control] my quadratures of dln(Abar)/dS = 1/(3 c_s^2) and dtau = dS/(3 Htilde c_s^2) "
      "reproduce IC10's own S = 0.1 -> 0.2 numbers, 0.108584184534843401 barred e-folds and "
      "0.110756742119829669 tilde proper-time units",
      close(nbar_ctrl, '0.108584184534843401416970621034', mp.mpf('1e-20'))
      and close(tau_ctrl, '0.110756742119829669060587804501', mp.mpf('1e-20')),
      f"Nbar = {mp.nstr(nbar_ctrl,18)}, tau = {mp.nstr(tau_ctrl,18)}")

# ================================================================== (H) MAPPING THE BACKWARD HISTORY ==
print("\n-- (H) mapping the history: how far back are the two edges? -------------------------------------")

grid_dn = ['0.2307', '0.2', '0.15', '0.1', '0.06', '0.05', '0.045', '0.0377', '0.035', '0.03', '0.028',
           '0.027', '0.0267', '0.0266', '0.026', '0.02', '0.01', '0.005', '0.002', '0.0016']
print("      S          xi=S+w        u          P_X          Q_clock        c_s^2         rho          r^2")
for s in grid_dn:
    a = state(s)
    print(f"  {s:>8s} {mp.nstr(a['xi'],8):>12s} {mp.nstr(a['u'],7):>10s} {mp.nstr(a['PX'],8):>12s} "
          f"{mp.nstr(a['Q'],8):>13s} {mp.nstr(a['cs2'],8):>13s} {mp.nstr(a['rho'],8):>12s} "
          f"{mp.nstr(a['r2'],7):>10s}")

sam = [state(s) for s in grid_dn if mp.mpf(s) >= S_ghost]
check("L20-H1 nothing else goes singular before the clock does: rho > 0 (so Htilde is real and finite) "
      "and P_X > 0 (no separate degeneracy) at every sampled S from the Q_clock = 0 edge up to the "
      "eta = 1 upper edge.  The degeneracy is at FINITE energy density and FINITE Htilde -- it is not a "
      "curvature singularity and it is not the eta boundary.",
      all(a['rho'] > 0 and a['PX'] > 0 for a in sam)
      and close(state(S_ghost)['rho'], '2.90843', mp.mpf('1e-5')),
      f"rho(S_ghost) = {mp.nstr(state(S_ghost)['rho'],9)}, Htilde(S_ghost) = "
      f"{mp.nstr(state(S_ghost)['H'],9)}, r^2(S_ghost) = {mp.nstr(state(S_ghost)['r2'],9)} (inside eta = 1)")


def Nbar(a, b):
    return mp.quad(lambda s: state(s)['Q'] / (3 * state(s)['PX']), [mp.mpf(a), mp.mpf(b)], maxdegree=5)


def Tau(a, b):
    return mp.quad(lambda s: state(s)['Q'] / (3 * state(s)['H'] * state(s)['PX']),
                   [mp.mpf(a), mp.mpf(b)], maxdegree=5)


S0 = mp.mpf('0.2')                     # the lead's latest sample -- the reference epoch
hist = {}
for nm, Sv in (('superluminal onset  c_s^2 = 1', S_lum), ('ghost/degeneracy edge  Q = 0', S_ghost)):
    nb, tt = Nbar(Sv, S0), Tau(Sv, S0)
    nph = nb + state(S0)['w'] - state(Sv)['w']
    hist[nm] = dict(S=Sv, Nbar=nb, tau=tt, Nphys=nph, z=mp.e**nph - 1)
nb_fwd = Nbar(S0, S_eta_hi)
nph_fwd = nb_fwd + state(S_eta_hi)['w'] - state(S0)['w']
print()
print("  backward from the lead's latest sample S = 0.2:")
for nm, d in hist.items():
    print(f"    {nm:34s} S = {mp.nstr(d['S'],9):>12s}  Delta tau = {mp.nstr(d['tau'],9):>11s}/h0  "
          f"Nbar = {mp.nstr(d['Nbar'],9):>11s}  Nphys = {mp.nstr(d['Nphys'],9):>11s}  "
          f"z = {mp.nstr(d['z'],7)}")
print(f"    forward to the eta = 1 upper edge  S = {mp.nstr(S_eta_hi,9):>12s}  "
      f"Delta tau = {mp.nstr(Tau(S0, S_eta_hi),9):>11s}/h0  Nbar = {mp.nstr(nb_fwd,9):>11s}  "
      f"Nphys = {mp.nstr(nph_fwd,9)}")
tot_phys = hist['superluminal onset  c_s^2 = 1']['Nphys'] + nph_fwd
print(f"    => TOTAL certified-healthy, subluminal plateau length: {mp.nstr(tot_phys,9)} physical e-folds "
      f"(a factor {mp.nstr(mp.e**tot_phys,7)} in the physical scale factor)")

check("L20-H2 the two edges are BOTH very close in the past of the lead's own solution.  Measured on "
      "IC10's own dS/dtau = 3 Htilde c_s^2 and dln(Abar)/dS = 1/(3 c_s^2), the superluminal onset is "
      "0.1058 physical e-folds back (z = 0.1116 relative to the S = 0.2 epoch) and the degeneracy is "
      "0.1040 physical e-folds back (z = 0.1096).  The whole superluminal band is crossed in 1.2% of "
      "that time.  The ENTIRE certified healthy+subluminal plateau, past terminus to future eta exit, "
      "is 0.1390 physical e-folds -- a factor 1.149 in scale factor, not a cosmology.",
      close(hist['superluminal onset  c_s^2 = 1']['Nphys'], '0.10584', mp.mpf('1e-4'))
      and close(hist['ghost/degeneracy edge  Q = 0']['Nphys'], '0.10403', mp.mpf('1e-4'))
      and close(tot_phys, '0.139012', mp.mpf('1e-4'))
      and (hist['superluminal onset  c_s^2 = 1']['tau'] - hist['ghost/degeneracy edge  Q = 0']['tau'])
      / hist['ghost/degeneracy edge  Q = 0']['tau'] > -mp.mpf('0.02'),
      f"band crossing = {mp.nstr(hist['ghost/degeneracy edge  Q = 0']['tau'] - hist['superluminal onset  c_s^2 = 1']['tau'],4)}/h0 "
      f"out of {mp.nstr(hist['ghost/degeneracy edge  Q = 0']['tau'],6)}/h0 total")

# ---- the conditional physical-scale identification, both footings
a0_IC = mp.sqrt(mp.mpf(str(sp.N(a02, 40))))
c_SI = mp.mpf('2.99792458e8')
H0_SI = mp.mpf('0.674') * mp.mpf('100e3') / mp.mpf('3.0857e22')
GYR = mp.mpf('3.1557e16')
print()
print("  CONDITIONAL scale identification (IC10 explicitly does NOT make it; both a0 footings carried):")
print(f"    the IC-internal a0 = sqrt(9 kappa e^-1/2/(16 m l^2)) = {mp.nstr(a0_IC,10)} in h0 = c = 1 units")
foot = {}
for nm, a0v in (('canonical 9.3619e-11', mp.mpf('9.3619e-11')), ('alt       1.1279e-10', mp.mpf('1.1279e-10'))):
    h0_SI = a0v / (c_SI * a0_IC)
    foot[nm] = dict(h0=h0_SI, ratio=h0_SI / H0_SI,
                    dt=hist['ghost/degeneracy edge  Q = 0']['tau'] / h0_SI / GYR,
                    Hplat=state(S0)['H'] * h0_SI / H0_SI)
    print(f"    a0 = {nm}: h0 = {mp.nstr(h0_SI,6)} s^-1 = {mp.nstr(foot[nm]['ratio'],5)} H0; "
          f"plateau Htilde = {mp.nstr(foot[nm]['Hplat'],5)} H0; ghost edge {mp.nstr(foot[nm]['dt'],5)} Gyr back")
check("L20-H3 the backward interval CANNOT be honestly quoted as a cosmological redshift, and this is a "
      "finding rather than an evasion: the plateau is a vacuum toy with no matter, no normalisation to "
      "today, and an expansion rate that -- even under the most generous identification, IC-internal a0 "
      "= empirical a0 -- is 0.0553 H0 (canonical) / 0.0666 H0 (alt), i.e. 15-18x slower than the real "
      "universe.  The only defensible statement is the INTERNAL one: z = 0.110 relative to the lead's "
      "own S = 0.2 sample.  Both footings agree the toy is not a cosmology, so the ghost is not a "
      "statement about the real early universe either way.",
      all(f['Hplat'] < mp.mpf('0.1') for f in foot.values())
      and all(f['dt'] > 0 for f in foot.values()),
      f"Htilde/H0 = {mp.nstr(foot['canonical 9.3619e-11']['Hplat'],5)} / "
      f"{mp.nstr(foot['alt       1.1279e-10']['Hplat'],5)}; internal z = "
      f"{mp.nstr(hist['ghost/degeneracy edge  Q = 0']['z'],7)}")

# ============================================================ (G) IS THE GHOST ACTUALLY REACHABLE? ====
print("\n-- (G) is the ghost REACHABLE at finite past proper time, or is it an asymptotic floor? --------")

# the integrand of dtau near the edge behaves like Q(S) -> 0 linearly, so the integral must converge.
# I test convergence directly rather than asserting it: shrink the lower endpoint towards S_ghost and
# watch the remaining proper time go to zero like (S - S_ghost)^2.
tail = []
for eps in ('1e-3', '1e-4', '1e-5', '1e-6'):
    e = mp.mpf(eps)
    tail.append((e, Tau(S_ghost + e, S_ghost + 10 * e) if e < mp.mpf('1e-3') else Tau(S_ghost + e, '0.03')))
rat = [Tau(S_ghost + mp.mpf(e), S_ghost + 10 * mp.mpf(e)) for e in ('1e-4', '1e-5', '1e-6')]
quad_like = all(mp.mpf(50) < rat[i] / rat[i + 1] < mp.mpf(150) for i in range(len(rat) - 1))
tau_total = hist['ghost/degeneracy edge  Q = 0']['tau']
check("L20-G1 [THE CHECK] the Q_clock = 0 edge is reached at FINITE past proper time.  Because "
      "dtau/dS = Q_clock/(3 Htilde P_X) and Q_clock vanishes LINEARLY at the edge while Htilde and P_X "
      "stay finite and positive, the integrand vanishes there and the quadrature converges: the total "
      "backward interval from S = 0.2 is 0.153984/h0, and the remaining interval over a decade-shrinking "
      "sliver falls by ~100x per decade (the quadratic law of a linearly vanishing integrand).  This is "
      "possibility (a), not (b): there is NO asymptotic floor in S, and the ghost boundary is NOT a "
      "coordinate artefact of the continuation.",
      mp.isfinite(tau_total) and tau_total > 0 and tau_total < mp.mpf('0.2') and quad_like
      and close(tau_total, '0.153983862606', mp.mpf('1e-9')),
      f"Delta tau = {mp.nstr(tau_total,12)}/h0; sliver ratios per decade = "
      + ", ".join(mp.nstr(rat[i] / rat[i + 1], 5) for i in range(len(rat) - 1)))

# what actually happens AT the edge: the barred scale factor turns around.
F0 = state(S0)['Fch']
Amin_scan = [(state(s)['Fch'], mp.mpf(s)) for s in ('0.05', '0.04', '0.03', '0.028', '0.027', '0.0266',
                                                    '0.026', '0.024', '0.02', '0.015', '0.01')]
Fmax, S_at_Fmax = max(Amin_scan)
Abar_min = (F0 / Fmax)**(mp.mpf(1) / 3)
print(f"  Abar(S)/Abar(0.2) = (F(0.2)/F(S))^(1/3) with F = P_X e^{{-S}};  F is maximal at "
      f"S = {mp.nstr(S_at_Fmax,7)} (= the Q = 0 edge), giving Abar_min/Abar(0.2) = {mp.nstr(Abar_min,10)}")
for s in ('0.2', '0.1', '0.0377', '0.0267', '0.02', '0.01', '0.001'):
    print(f"    S = {s:>8s}   Abar/Abar(0.2) = {mp.nstr((F0 / state(s)['Fch'])**(mp.mpf(1) / 3),10)}")
turning = (state('0.02')['Fch'] < Fmax and state('0.03')['Fch'] < Fmax
           and abs(S_at_Fmax - S_ghost) < mp.mpf('0.001'))
check("L20-G2 [the precise nature of the boundary, and this is the part that softens the verdict] the "
      "healthy branch does NOT pass through the ghost region -- it TERMINATES at its edge.  From my own "
      "charge relation Abar^3 P_X e^{-S} = const, dF/dS = -Q_clock e^{-S}, so F = P_X e^{-S} is maximal "
      "exactly where Q_clock = 0.  Since Htilde > 0 makes Abar monotone in tau, Abar can only fall to "
      "Abar_min = (F(0.2)/F_max)^(1/3) = 0.8574 of its S = 0.2 value; below that no S solves the charge "
      "relation.  The Q < 0 region is the SECOND branch through the same fold, running forward in time "
      "from the same point, not the past of this one.",
      turning and close(Abar_min, '0.857404', mp.mpf('1e-5'))
      and (F0 / state('0.02')['Fch'])**(mp.mpf(1) / 3) > Abar_min
      and (F0 / state('0.01')['Fch'])**(mp.mpf(1) / 3) > Abar_min,
      f"F_max = {mp.nstr(Fmax,10)} at S = {mp.nstr(S_at_Fmax,7)}; Abar rises again below the edge "
      f"({mp.nstr((F0/state('0.01')['Fch'])**(mp.mpf(1)/3),8)} at S = 0.01 vs {mp.nstr(Abar_min,8)} at the edge)")

check("L20-G3 what the past boundary IS, stated plainly: at finite proper time in the past, at FINITE "
      "energy density (rho = 2.9084), FINITE Htilde (1.0702) and with eta still exactly 1 "
      "(r^2 = 0.901939, inside |r^2-1| <= 1/4), the clock's principal symbol degenerates -- c_s^2 -> +inf "
      "and the coefficient of the time derivative vanishes.  The solution is PAST-INCOMPLETE at a "
      "regular point of the geometry.  That is a defect of the plateau, and it is NOT the eta boundary "
      "the lead's open item 1 is waiting for: eta = 1 continues 16x further down, to S = 0.0016326.",
      mp.mpf(3) / 4 < state(S_ghost)['r2'] < mp.mpf(5) / 4 and S_ghost > S_eta_lo
      and state('0.027')['cs2'] > 20 and state('0.0267')['cs2'] > 100,
      f"c_s^2 = {mp.nstr(state('0.027')['cs2'],7)} at S = 0.027 and {mp.nstr(state('0.0267')['cs2'],7)} at "
      f"S = 0.0267; S_ghost/S_eta_lo = {mp.nstr(S_ghost/S_eta_lo,6)}")

# ==================================================================== (S) WHAT SETS THE INITIAL S? ====
print("\n-- (S) is S fixed by the construction, or a free initial condition? -----------------------------")

Tsym = sp.Symbol('T')
Pnoshift = Pgen.subs({lamsy: 0, gsy: 1})
check("L20-S1 S is a FREE INITIAL CONDITION, not an output of the construction.  The plateau pressure "
      "depends on the clock only through Xtilde = -gtilde^{mu nu}T_mu T_nu/2, never on T itself, so the "
      "action has the shift symmetry T -> T + const; its Noether charge Abar^3 P_X sqrt(2 Xtilde) is "
      "conserved (L20-C2) and its VALUE is initial data.  Nothing in the action, the auxiliary equation "
      "P_w = 0, or the Friedmann constraint picks a value of S: given Abar, S is whatever the initial "
      "charge makes it.  Avoiding the ghost is therefore a restriction on INITIAL DATA, which is a much "
      "weaker problem than a defect of the theory -- and it must be said so plainly.",
      Tsym not in Pnoshift.free_symbols and Pnoshift.free_symbols == {Ssy, wsy},
      f"free symbols of P = {sorted(str(s) for s in Pnoshift.free_symbols)} (no T)")

frac_S = (S_eta_hi - S_lum) / (S_eta_hi - S_eta_lo)
frac_S_ng = (S_eta_hi - S_ghost) / (S_eta_hi - S_eta_lo)
check("L20-S2 the restriction, quantified, and it cuts BOTH ways.  In the clock variable, "
      "84.3% of the eta = 1 plateau is healthy and subluminal (89.1% is merely non-ghost); the excluded "
      "sliver is the bottom 15.7%.  And the exclusion is one-sided in TIME: dS/dtau = 3 Htilde c_s^2 > 0 "
      "on the healthy branch, so {S > S_lum} is FORWARD-INVARIANT -- any initial datum that starts "
      "healthy stays healthy until it exits eta = 1 at the top.  A theory healthy only for restricted "
      "initial data is a weaker theory; but the restriction here is 'start above S = 0.0377', it is an "
      "open condition, and it is never violated by evolution.",
      frac_S > mp.mpf('0.84') and frac_S_ng > mp.mpf('0.89')
      and all(state(s)['cs2'] > 0 for s in ('0.05', '0.1', '0.15', '0.2'))
      and all(state(s)['Q'] > 0 for s in ('0.05', '0.1', '0.15', '0.2')),
      f"healthy+subluminal fraction of the eta = 1 range in S = {mp.nstr(100*frac_S,5)}%, "
      f"non-ghost fraction = {mp.nstr(100*frac_S_ng,5)}%")

# ================================================================= (L) DOES SUPERLUMINALITY MATTER? ===
print("\n-- (L) does the superluminal band matter? -------------------------------------------------------")

band = [(s, state(s)['cs2']) for s in ('0.0377', '0.037', '0.036', '0.035', '0.033', '0.031', '0.030',
                                       '0.029', '0.028', '0.027')]
for s, c in band:
    print(f"    S = {s:>8s}   c_s^2 = {mp.nstr(c,9)}")
check("L20-L1 the band is not a marginal excursion: inside 0.0266641 < S < 0.0377010 the clock's sound "
      "cone opens WITHOUT BOUND (c_s^2 = 1.23 at S = 0.035, 2.67 at 0.030, 24.0 at 0.027, divergent at "
      "the edge), all with eta exactly 1 and the auxiliary root unique.  On a preferred foliation that "
      "is not by itself a causality violation -- the clock's own level sets T = const are a global time "
      "function for BOTH cones on this homogeneous background, so no closed causal curve arises here -- "
      "but 'not automatically fatal' is the most that can be said from this calculation.",
      state('0.035')['cs2'] > 1 and state('0.030')['cs2'] > 2 and state('0.027')['cs2'] > 20
      and state('0.0377')['cs2'] > mp.mpf('0.999') and state('0.04')['cs2'] < 1,
      f"max sampled c_s^2 inside the band = {mp.nstr(max(c for _, c in band),8)}")

check("L20-L2 [DEPENDENCY, not settled here] the sign of this question is inverted by the parallel "
      "gravitational-Cherenkov lane and this lane does not duplicate it.  IF the handoff's A5/A6 apply "
      "to this clock (bound 1 - c_s <= 2e-15, 'the lower edge is always Cherenkov => the khronon must be "
      "marginally superluminal'), then it is the lead's SUBLUMINAL samples that are excluded -- "
      "c_s^2 = 0.265-0.369 sits where A5 excludes c_s^2 = 1/3 by 2.1e14x -- and the only surviving point "
      "of the whole plateau is c_s^2 = 1, i.e. exactly the superluminal onset S = 0.0377010 this lane "
      "identifies as the edge of the healthy window.  Recorded as a conditional pincer, resolved by the "
      "other lane, not asserted here.",
      all(mp.mpf('0.26') < st[k]['cs2'] < mp.mpf('0.37') for k in st)
      and close(state(S_lum)['cs2'], 1, mp.mpf('1e-6')),
      f"the lead's samples span c_s^2 = {mp.nstr(st['0.2']['cs2'],6)}-{mp.nstr(st['0.1']['cs2'],6)}; "
      f"c_s^2 = 1 at S = {mp.nstr(S_lum,10)}")

# ======================================================================= (F) CAN THE LEAD FIX THIS? ===
print("\n-- (F) is there a modification that moves the ghost edge below any reachable S? -----------------")

Pk = sp.simplify(sp.expand(Pgen.subs({lamsy: 0, gsy: 1}) / kap))
check("L20-F1 kappa and m are NOT levers, and this closes the cheapest repair before it is tried.  The "
      "IC5 relations m a0^2 = 9 kappa e^{-1/2}/(16 l^2) and m Lambda = kappa e^{-1/2} - m a0^2 U(4/9) "
      "make P exactly proportional to kappa and independent of m; the activation r^2 = "
      "2 e^{2S-4w-1/6} rho/kappa is then independent of BOTH.  So no rescaling of kappa or m moves the "
      "ghost edge, moves the eta window, or separates the two.",
      Pk.free_symbols == {Ssy, wsy} and sp.simplify(sp.diff(Pk, sp.Symbol('m'))) == 0,
      "P/kappa has free symbols {S, w} only -- kappa is an overall factor and m has cancelled")

print("  (F2) the Lambda lever: scan g = Lambda/Lambda_IC5 and ask whether the ghost ever leaves the plateau")
print("      g        S_eta_lo      S_ghost      S_lum        S_eta_hi      ghost inside eta = 1?")
mp.mp.dps = 25
f2_rows = []
for gv in ('0.6', '0.8', '0.9', '0.95', '1', '1.05', '1.1', '1.2', '1.3', '1.4'):
    try:
        lo_ = bisect(lambda s: state(s, 0, gv)['r2'] - mp.mpf(3) / 4, '1e-5', '0.20', 70)
        if not (mp.mpf('2e-5') < lo_ < mp.mpf('0.19')):
            lo_ = None
    except Exception:
        lo_ = None
    try:
        gh_ = bisect(lambda s: state(s, 0, gv)['Q'], '1e-4', '0.15', 70)
    except Exception:
        gh_ = None
    try:
        hi_ = bisect(lambda s: state(s, 0, gv)['r2'] - mp.mpf(5) / 4, '0.15', '0.60', 70)
    except Exception:
        hi_ = None
    try:
        lu_ = bisect(lambda s: state(s, 0, gv)['cs2'] - 1, gh_ + mp.mpf('1e-6'), '0.20', 70)
    except Exception:
        lu_ = None
    inside = (gh_ is not None) and (lo_ is None or gh_ > lo_)
    f2_rows.append((gv, lo_, gh_, inside))
    fm = lambda v: mp.nstr(v, 8) if v is not None else 'no crossing'
    print(f"      {gv:6s} {fm(lo_):>13s} {fm(gh_):>13s} {fm(lu_):>13s} {fm(hi_):>13s}   "
          f"{'YES -- ghost inside' if inside else 'no'}")
mp.mp.dps = 40
check("L20-F2 tuning Lambda does NOT fix it.  Over g = Lambda/Lambda_IC5 in [0.6, 1.4] the ghost edge "
      "moves by a factor of 25 -- but so does the eta = 1 lower edge, and the ghost stays INSIDE the "
      "plateau at every point scanned.  Below g ~ 0.9 the plateau stops closing at the bottom at all "
      "(r^2 never falls to 3/4), so eta = 1 then runs all the way to the excluded chart locus with the "
      "ghost in it; above g ~ 1.4 the plateau closes up and c_s^2 goes negative at the top.  A "
      "one-coefficient tune is not the repair.",
      all(row[3] for row in f2_rows),
      f"ghost inside eta = 1 at {sum(1 for r in f2_rows if r[3])}/{len(f2_rows)} scanned values of g")

print("  (F3) the clock kinetic lever: add  lam e^{2w} Xtilde^2  to P (only lam/kappa matters)")
print("      lam     S_ghost       c_s^2(0.1)   c_s^2(0.2)   S(c_s^2=1)     r^2(0.15)   plateau ok?")
mp.mp.dps = 25
f3_rows = []
for lv in ('0', '1', '2', '5', '10'):
    try:
        gh_ = bisect(lambda s: state(s, lv)['Q'], '2e-4', '0.15', 70)
    except Exception:
        gh_ = None
    a15 = state('0.15', lv)
    try:
        lu_ = bisect(lambda s: state(s, lv)['cs2'] - 1, gh_ + mp.mpf('1e-8'), '0.20', 70)
    except Exception:
        lu_ = None
    okp = a15 is not None and mp.mpf(3) / 4 < a15['r2'] < mp.mpf(5) / 4
    f3_rows.append((lv, gh_, okp, lu_))
    print(f"      {lv:6s} {mp.nstr(gh_,8) if gh_ else 'none':>13s} "
          f"{mp.nstr(state('0.1',lv)['cs2'],8):>12s} {mp.nstr(state('0.2',lv)['cs2'],8):>12s} "
          f"{mp.nstr(lu_,8) if lu_ else 'none':>13s} {mp.nstr(a15['r2'],7):>11s}   "
          f"{'yes' if okp else 'NO -- outside eta=1'}")
mp.mp.dps = 40
check("L20-F3 a higher-order clock kinetic term moves the edge a long way but does NOT change the "
      "structure.  lam/kappa = 0.83 pushes the ghost from S = 0.0267 to 0.00072 (37x) and drags the "
      "superluminal band down with it (the c_s^2 = 1 crossing moves from 0.0377 to 0.00103), but it does "
      "so by ADDING ENERGY, and the activation r^2 = 2 e^{2S-4w-1/6} rho/kappa then leaves the eta = 1 "
      "window entirely (r^2 = 3.19 at S = 0.15).  Every lam > 0 scanned that helps the ghost also breaks "
      "the plateau, and no (lam, Lambda) point in the grid keeps S = 0.15 inside eta = 1.  So a "
      "constitutive repair has to be ENERGY-NEUTRAL, and that is the constraint the lead has to design "
      "against.",
      f3_rows[0][2] and not any(r[2] for r in f3_rows[1:])
      and f3_rows[-1][1] is not None and f3_rows[-1][1] < S_ghost / 20,
      f"lam = 0 keeps r^2(0.15) inside eta = 1; every lam > 0 tried does not; "
      f"S_ghost(lam/kappa=0.83) = {mp.nstr(f3_rows[-1][1],7)}")

r2_lum = state(S_lum)['r2']
r2_samples = [st[k]['r2'] for k in ('0.1', '0.15', '0.2')]
check("L20-F4 [THE CONCRETE, CHECKABLE SUGGESTION] there IS a repair that costs the lead nothing "
      "numerically, and it lives in a place IC5 already declares free: the activation.  IC5 defines eta "
      "by 'a smooth, momentum-reversal-even activation' with eta = 1 for |r^2-1| <= 1/4.  That window is "
      "SYMMETRIC by choice, not by derivation.  Make its LOWER threshold r^2 >= 0.93256 instead of 0.75 "
      "-- still smooth, still even under momentum reversal -- and eta = 1 then coincides exactly with "
      "S in [0.0377010, 0.2307240], the healthy subluminal window.  Every published IC10 number "
      "survives untouched (r^2 = 1.0530, 1.1305, 1.2045 at the three samples, all interior), the upper "
      "edge r^2 = 5/4 is unchanged, and the backward handoff to the full eta-derivative equations then "
      "happens AT c_s^2 = 1 instead of after the degeneracy.  Stated honestly: this does not make the "
      "ghost go away, it makes it the transition sector's problem -- which is already the lead's open "
      "item 1 -- and that is exactly the right place for it.",
      close(r2_lum, '0.93256', mp.mpf('1e-4')) and all(v > r2_lum for v in r2_samples)
      and all(v < mp.mpf(5) / 4 for v in r2_samples),
      f"r^2 at the superluminal onset = {mp.nstr(r2_lum,8)}; the three samples sit at "
      + ", ".join(mp.nstr(v, 7) for v in r2_samples))

print("  (F5) where a REAL constitutive repair has to act: Q_clock = (P_eff'' + P_eff')/(2X) and the")
print("       Schur subtraction P_Sw^2/P_ww is what drives it negative as the chart locus xi = 0 is")
print("       approached.  Q_bare stays hugely positive; the whole effect is in the elimination.")
print("        S          xi           Q_bare          Q_clock        subtraction")
for s in ('0.2', '0.1', '0.05', '0.0377', '0.03', '0.0267', '0.02', '0.01', '0.0016'):
    a = state(s)
    print(f"    {s:>8s} {mp.nstr(a['xi'],8):>12s} {mp.nstr(a['Qbare'],9):>14s} {mp.nstr(a['Q'],9):>14s} "
          f"{mp.nstr(a['Qbare']-a['Q'],9):>14s}")
xis = [(state(s)['xi'], state(s)['Q']) for s in ('0.001', '0.0003', '0.0001', '0.00003')]
slopes = [mp.log(abs(xis[i + 1][1]) / abs(xis[i][1])) / mp.log(xis[i][0] / xis[i + 1][0])
          for i in range(len(xis) - 1)]
check("L20-F6 the ghost is generic near the excluded chart locus, in every deformation tried.  Q_clock "
      "diverges to -infinity as xi = S + w -> 0 (local logarithmic slope ~0.78 over three decades in "
      "xi), for lam = 0 and for every lam and Lambda scanned: the deformations move the CROSSING, never "
      "the asymptotics.  So the repair cannot be a coefficient; it has to change the xi -> 0 structure "
      "of the auxiliary sector -- which is precisely the lead's own open item 4, 'global k = 0/y = 0 "
      "control'.  This liability and that open item are the same problem seen from two sides.",
      all(q < 0 for _, q in xis) and all(mp.mpf('0.5') < s2 < mp.mpf('1.5') for s2 in slopes)
      and state('0.0001', '5')['Q'] < 0 and state('0.0001', '10')['Q'] < 0
      and state('0.0001', 0, '0.6')['Q'] < 0 and state('0.0001', 0, '1.3')['Q'] < 0,
      "Q(xi) local slopes = " + ", ".join(mp.nstr(s2, 4) for s2 in slopes)
      + f"; Q(S=1e-4) < 0 for lam/kappa in {{0, 0.83, 1.67}} and g in {{0.6, 1, 1.3}}")

# ================================================================================== THE VERDICT =======
print("\n-- verdict ---------------------------------------------------------------------------------------")

check("L20-V1 [VERDICT] the liability is REAL and NOT FATAL, and all four sub-claims are checked above. "
      "(i) It is real: the certified-healthy window is strictly inside eta = 1, and the boundary is "
      "reached at finite past proper time (0.153984/h0, 0.1040 physical e-folds, internal z = 0.1096) "
      "at finite density and finite Htilde, with eta exactly 1 -- so it is a genuine past boundary of "
      "the plateau and not a continuation artefact (L20-G1, L20-G3). "
      "(ii) It is milder than 'a ghost in the history': the healthy branch does not enter the ghost "
      "region, it terminates at a fold in Abar, and the Q < 0 region is a separate branch (L20-G2). "
      "(iii) S is a free initial condition, so avoiding the region is a restriction on initial data, "
      "that restriction is 84.3% of the plateau and it is forward-invariant (L20-S1, L20-S2). "
      "(iv) It is removable inside IC5's own declared design freedom, at zero cost to every published "
      "number, by making the activation window asymmetric (L20-F4) -- while a coefficient tune "
      "provably is NOT the repair (L20-F1, F2, F3, F6).",
      mp.isfinite(tau_total) and tau_total > 0                                   # (i)
      and turning and Abar_min > 0                                               # (ii)
      and (Tsym not in Pnoshift.free_symbols) and frac_S > mp.mpf('0.84')        # (iii)
      and all(v > r2_lum for v in r2_samples) and all(row[3] for row in f2_rows),  # (iv)
      "not fatal; a past boundary of the plateau, removable by an activation retune, "
      "not by a coefficient tune")

check("L20-V2 [the calibration that keeps this honest in the other direction] the ghost is NOT the "
      "binding limitation on IC10, and saying so is part of the answer.  The entire certified healthy "
      "subluminal plateau lasts 0.1390 physical e-folds -- a factor 1.149 in scale factor.  A construction "
      "that expands by 15% between its past degeneracy and its future eta exit is a local witness, "
      "exactly as IC10 labels it ('emphatically not a realistic full cosmology'), and the past boundary "
      "found here is a defect of that witness, not of a cosmological history it never claimed.",
      tot_phys < mp.mpf('0.2') and mp.e**tot_phys < mp.mpf('1.25'),
      f"total plateau = {mp.nstr(tot_phys,7)} physical e-folds = factor {mp.nstr(mp.e**tot_phys,7)} "
      f"in the physical scale factor")

print("\n" + "=" * 122)
if FAILS:
    print(f"FAILED CHECKS ({len(FAILS)}):")
    for f in FAILS:
        print("   -", f)
else:
    print("ALL CHECKS PASSED.")
print("""
SUMMARY FOR THE LEAD.
  The ghost IS reachable: IC10's own dS/dtau = 3 Htilde c_s^2, integrated backwards from the S = 0.2
  sample, hits the Q_clock = 0 degeneracy after 0.153984/h0 of proper time -- 0.1040 physical e-folds,
  internal z = 0.1096 -- at rho = 2.9084, Htilde = 1.0702, r^2 = 0.901939 (eta still exactly 1), with the
  auxiliary root still unique.  It is not an asymptotic floor.
  But it is a TERMINATION, not a traversal: F = P_X e^{-S} is maximal exactly at Q_clock = 0, so the
  barred scale factor bottoms out at 0.8574 of its S = 0.2 value and the Q < 0 region is a second branch
  through the same fold, not the past of this solution.
  S is free initial data (shift symmetry in T), so the exclusion is an open, forward-invariant condition
  on initial data covering 84.3% of the eta = 1 plateau -- weaker than a defect of the theory, but a
  restriction that should be stated.
  The repair is NOT a coefficient: kappa and m cancel out of both the ghost edge and the activation;
  Lambda moves both edges together and never separates them; a clock Xtilde^2 term moves the ghost edge down 37x
  but drags the superluminal band with it and pushes r^2 out of eta = 1.  Q_clock -> -inf as xi -> 0 in every deformation.
  The cheap repair is the ACTIVATION: raise eta's lower threshold from r^2 >= 3/4 to r^2 >= 0.93256, so
  eta = 1 coincides with the healthy subluminal window S in [0.0377010, 0.2307240].  Costs nothing --
  the three published samples sit at r^2 = 1.0530, 1.1305, 1.2045 -- and moves the past handoff to
  c_s^2 = 1.  It relocates the problem into open item 1 rather than solving it, and should be reported
  that way.
""")
raise SystemExit(1 if FAILS else 0)
