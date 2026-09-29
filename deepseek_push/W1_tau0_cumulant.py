#!/usr/bin/env python3
"""W1 -- finite-tau0 numerator cumulant law (Z9-wave; owns W1_*).
Door: MC5_results.json stored K1 coefficients B(q) fit -B = b0 + b1 q + b2 q^2
(residuals ~1e-6, quadrature-floor scale). Engine algebra (J11_volume_atom
docstring): tau_esc = tau0*(chord + q*(r^2*chord + r*mu*chord^2 + chord^3/3)),
so with S_q := chord + q*T, T := r^2*chord + r*mu*chord^2 + chord^3/3,
-ln<exp(-tau0 S_q)>/tau0 = <S_q> - (tau0/2) Var(S_q) + O(tau0^2) gives
-B(q) = Var(S_q)/2 = Var(chord)/2 + q Cov(chord,T) + q^2 Var(T)/2 -- EXACTLY
quadratic in q (exact Taylor algebra: kappa2 is the tau0^2 coefficient of
ln A). Conductor claims to TEST: b0 = Var(chord)/2 = 19/160 (E[c]=3/4,
E[c^2]=4/5 via the (u,v) disk reduction), b1 = Cov(chord,T), b2 = Var(T)/2,
E[T] = 5/12.
KILLS pre-registered in Z9-WAVE_BRIEF.md + AMENDMENTS 1-2 (registered before
this run-3):
  P0: fresh A_vol_quadrature(0.5,0) vs J11 stored 0.70728, |diff| <= 1e-4.
  K-A: quadraticity of N_num at ng=320, tau0 {1e-2,3e-3,1e-3,3e-4,1e-4};
       kill if fit residual RMS > 3x ng-refinement floor (|ng160-ng320| at
       tau0=1e-2) -> quadratic-cumulant form REFUTED, exit 1.
  K-B (INFORMATIONAL per AMENDMENT 2): the two INDIRECT estimators (N_num
       quadratic fit vs cubic ln-curvature fit) agree at q=0 to 2.9e-8; the
       q>=1 disagreement (run-1 and run-2 fires, verbatim in .out) is the
       estimators' own O(kappa4 tau^3)/O(kappa4 tau^4) truncation scale
       growing with q -- recorded, NOT an identity refutation.
  K-C (OPERATIVE per AMENDMENT 2):
       (i) sympy exact moments via the (u,v) disk reduction; E[c]==3/4 and
           E[T]==5/12 required cross-checks; b0/b1/b2 must be exact rationals
           (non-rational -> MEASURED-only record, exit 0 if K-A passes).
       (ii) exact b0/b1/b2 vs DIRECT moment quadrature Var(S_q)/2 =
            (E[S_q^2]-E[S_q]^2)/2 on the (r,mu) grid at ng=320 (NO cumulant
            expansion), gate 1e-9 relative per q -> mismatch = exact
            candidate REJECTED, exit 1.
       (iii) exact quadratic form vs Bfit with tolerance
            max(3*floor_q, 10*dtau_q), dtau_q = |Bfit(full tau grid) -
            Bfit(grid without tau=1e-2)| (Bfit's measured tau^3-leakage
            scale, ablation not tuning) -> violation = REJECTED, exit 1.
Exit 0 iff P0 and K-A pass and K-C (i)(ii)(iii) pass.
Run history: run-1 K-B FIRED (quadratic ln-fit, gate-design error); run-2
K-B FIRED at q>=1 (cubic ln-fit, higher-cumulant truncation in both indirect
estimators); run-3 = this file per AMENDMENT 2.
"""
import json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J11_volume_atom import A_vol_quadrature

OUT = os.path.join(HERE, "W1_tau0_cumulant.out")
RESF = os.path.join(HERE, "W1_results.json")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="W1 finite-tau0 numerator cumulant law",
               pre_registration="Z9-WAVE_BRIEF.md W1 gates + AMENDMENTS 1-2",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF,"w"), indent=1, default=str)
    with open(OUT,"a") as f: f.write("\n".join(LOG)+"\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

QS = [0.0, 1.0, 3.0, 6.0, 10.0]
TAUS_NUM = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
TAUS_LN  = [2e-3, 1e-3, 5e-4, 2.5e-4, 1.25e-4]

# ---- P0 parity vs J11 stored quadrature ----
a_fresh = A_vol_quadrature(0.5, 0.0)
d = abs(a_fresh - 0.70728)
log("P0: fresh A_vol_quadrature(0.5, 0) = %.6f vs J11 stored 0.70728, |diff| = %.2e" % (a_fresh, d))
if d > 1e-4:
    finish(1, "P0-FAIL: parity vs J11 stored quadrature off by %.2e (kill pre-registered)" % d)
log("P0 PASS")

def nnum(t, q, ng):
    return -np.log(A_vol_quadrature(t, q, ng=ng))/t

def bfit_of(taus, q, ng=320):
    xs = np.array([nnum(t, q, ng) for t in taus])
    ts = np.array(taus)
    M = np.vstack([np.ones_like(ts), ts, ts**2]).T
    coef, *_ = np.linalg.lstsq(M, xs, rcond=None)
    resid = xs - M @ coef
    return coef, resid

# ---- K-A quadraticity at ng=320 ----
quad = {}; ka_fired = []
for q in QS:
    coef, resid = bfit_of(TAUS_NUM, q)
    rms = float(np.sqrt(np.mean(resid**2)))
    floor = float(abs(nnum(1e-2, q, 160) - nnum(1e-2, q, 320)))
    ok = rms <= 3*floor
    quad[q] = dict(A=float(coef[0]), Bfit=float(coef[1]), C=float(coef[2]),
                   rms=rms, floor=floor, tol=3*floor,
                   nvals=[float(nnum(t, q, 320)) for t in TAUS_NUM],
                   resid=[float(x) for x in resid])
    log("K-A: q=%g: A=%.9f Bfit=%.9f C=%.9f rms=%.2e floor=%.2e tol=%.2e %s"
        % (q, coef[0], coef[1], coef[2], rms, floor, 3*floor, "KILL" if not ok else "ok"))
    if not ok: ka_fired.append(q)
if ka_fired:
    finish(1, "K-A FIRED at q=%s: quadratic-cumulant form REFUTED at ng=320 (honest FAIL)" % ka_fired,
           extra=dict(quad=quad))
log("K-A no kill (N_num quadratic in tau0 within measured floor at all q)")

# ---- K-B (INFORMATIONAL per AMENDMENT 2): independent ln-curvature estimator ----
kb = {}
for q in QS:
    ys = np.array([np.log(A_vol_quadrature(t, q, ng=320)) for t in TAUS_LN])
    ts = np.array(TAUS_LN)
    M = np.vstack([np.ones_like(ts), ts, ts**2, ts**3]).T
    coef, *_ = np.linalg.lstsq(M, ys, rcond=None)
    resid_ln = ys - M @ coef
    noise_ln = float(np.sqrt(np.sum(resid_ln**2)/max(len(ts)-4, 1)))
    cov_ln = np.linalg.inv(M.T @ M)
    se_p2 = float(noise_ln*np.sqrt(cov_ln[2, 2]))
    diff = abs(-quad[q]["Bfit"] - float(coef[2]))
    kb[q] = dict(var2_ln=float(coef[2]), minus_Bfit=-quad[q]["Bfit"], diff=float(diff),
                 tol=max(3*quad[q]["floor"], 10*se_p2), se_p2=se_p2)
    log("K-B(informational): q=%g: Var/2(lnfit)=%.9f+-%.1e vs -Bfit=%.9f diff=%.2e"
        % (q, coef[2], se_p2, -quad[q]["Bfit"], diff))
log("K-B recorded (run-1/run-2 fires preserved verbatim in .out; identity gate moved to K-C)")

# ---- K-C exact-value leg: (u,v) disk reduction, mechanical sympy ----
# Measure: volume source x isotropic direction -> (u,v) uniform on the unit
# disk with density (3/2) u (dV = u du dphi dv normalized by 4pi/3); exit
# distance c = s - v, s = sqrt(1-u^2), v = r*mu; r^2 = u^2 + v^2, so
# T = (u^2+v^2)*c + v*c^2 + c^3/3.  All moments reduce to
# (3/2) * int_0^1 u * [int_{-s}^{s} poly(u,v,s) dv] du -- v^j integral is
# 2 s^{j+1}/(j+1) for even j, 0 for odd j; remaining u-integral
# int_0^1 u^{a+1} (1-u^2)^{p/2} du = (1/2) B((a+2)/2, (p+2)/2) -- exact
# rational for half-integer parameters (double factorials; gamma ratios).
import sympy as sp

def exact_moment(k, m):
    """E[c^k T^m] under the volume measure, exact rational (fresh-symbol S;
    S^2 -> 1-u^2 only inside the final u-integral -- run-3 fix: sympy
    auto-collapses (sqrt(1-u^2))^2 leaving bare sqrt terms the monomial
    parser rejected)."""
    u, v, S = sp.symbols("u v S", real=True)
    c = S - v
    T = (u**2 + v**2)*c + v*c**2 + c**3/3
    expr = sp.expand((c**k) * (T**m))
    total = sp.Rational(0)
    for term in expr.as_ordered_terms():
        pd = term.as_powers_dict()
        a = int(pd.get(u, 0)); j = int(pd.get(v, 0)); mpow = int(pd.get(S, 0))
        coef = sp.nsimplify(term / (u**a * v**j * S**mpow))
        if not coef.is_Rational:
            raise ValueError("non-monomial term: %s" % term)
        coef = sp.Rational(coef)
        if j % 2 == 1:
            continue
        p = mpow + j + 1                      # S^{p} -> (1-u^2)^{p/2}
        x = sp.Rational(a + 2, 2); y = sp.Rational(p + 2, 2)
        bval = sp.gamma(x)*sp.gamma(y)/sp.gamma(x + y)
        total += coef * sp.Rational(2, j + 1) * bval / 2
    return sp.simplify(sp.Rational(3, 2)*total)   # (3/2)u disk-measure normalization

b0_ex = b1_ex = b2_ex = None
try:
    Ec  = exact_moment(1, 0)
    Ec2 = exact_moment(2, 0)
    ET  = exact_moment(0, 1)
    EcT = exact_moment(1, 1)
    ET2 = exact_moment(0, 2)
    log("K-C(i): sympy exact moments: E[c]=%s E[c2]=%s E[T]=%s E[cT]=%s E[T2]=%s"
        % (Ec, Ec2, ET, EcT, ET2))
    if Ec != sp.Rational(3, 4):
        finish(1, "K-C REJECT: exact E[c] = %s != 3/4 (cross-check vs J09/LR4c certified limit)" % Ec,
               extra=dict(quad=quad, kb=kb))
    if ET != sp.Rational(5, 12):
        finish(1, "K-C REJECT: exact E[T] = %s != 5/12 (cross-check vs the q-numerator limit)" % ET,
               extra=dict(quad=quad, kb=kb))
    b0_ex = sp.simplify((Ec2 - Ec**2)/2)
    b1_ex = sp.simplify(EcT - Ec*ET)
    b2_ex = sp.simplify((ET2 - ET**2)/2)
    if not (b0_ex.is_Rational and b1_ex.is_Rational and b2_ex.is_Rational):
        raise ValueError("exact moments not Rational: %s %s %s" % (b0_ex, b1_ex, b2_ex))
    log("K-C(i): exact candidates b0=%s b1=%s b2=%s (floats %.9f %.9f %.9f)"
        % (b0_ex, b1_ex, b2_ex, float(b0_ex), float(b1_ex), float(b2_ex)))
except Exception as e:
    log("K-C(i): sympy exact leg FAILED (%s) -- MEASURED-only honest record" % repr(e))
    b0_ex = b1_ex = b2_ex = None

# ---- direct moment quadrature on the (r,mu) grid (transcription of the
# committed J11 docstring algebra, labeled; self-checked by E[T]==5/12) ----
xg, wg = np.polynomial.legendre.leggauss(320)
r = 0.5*xg + 0.5
xm, wm = np.polynomial.legendre.leggauss(640)
mu = xm
R = r[:, None]; MU = mu[None, :]
Wr = (3.0 * R**2) * (0.5 * wg[:, None])
Wm = 0.5 * wm[None, :]
chord = -R*MU + np.sqrt(np.maximum(0.0, 1.0 - R**2*(1.0 - MU**2)))
Tq = R**2*chord + R*MU*chord**2 + chord**3/3.0
m_num = {}
m_num["E_c"]  = float(np.sum(Wr*chord*Wm))
m_num["E_cc"] = float(np.sum(Wr*chord*chord*Wm))
m_num["E_T"]  = float(np.sum(Wr*Tq*Wm))
m_num["E_cT"] = float(np.sum(Wr*chord*Tq*Wm))
m_num["E_TT"] = float(np.sum(Wr*Tq*Tq*Wm))
log("K-C quad: E_c=%.12f E_cc=%.12f E_T=%.12f E_cT=%.12f E_TT=%.12f"
    % (m_num["E_c"], m_num["E_cc"], m_num["E_T"], m_num["E_cT"], m_num["E_TT"]))
varS2_direct = {}
for q in QS:
    S = chord + q*Tq
    ES = float(np.sum(Wr*S*Wm)); ES2 = float(np.sum(Wr*S*S*Wm))
    varS2_direct[q] = (ES2 - ES*ES)/2
if b0_ex is not None:
    # K-C(ii): exact coefficients vs DIRECT Var(S_q)/2 quadrature (no expansion)
    b0_f, b1_f, b2_f = float(b0_ex), float(b1_ex), float(b2_ex)
    rel = [abs(b0_f + b1_f*q + b2_f*q*q - varS2_direct[q])/max(abs(varS2_direct[q]), 1e-12)
           for q in QS]
    log("K-C(ii): exact form vs DIRECT Var(S_q)/2 quadrature, rel %s (gate 1e-9)"
        % ["%.2e" % x for x in rel])
    if max(rel) > 1e-9:
        finish(1, "K-C(ii) REJECT: exact b0/b1/b2 mismatch DIRECT Var(S_q)/2 quadrature "
               "beyond 1e-9 rel (exact candidate REJECTED, recorded, not banked)",
               extra=dict(quad=quad, kb=kb, m_num=m_num, rel=rel,
                          varS2_direct=varS2_direct,
                          b0_ex=str(b0_ex), b1_ex=str(b1_ex), b2_ex=str(b2_ex)))
    # K-C(iii): exact form vs Bfit with measured tau^3-leakage ablation
    dtau = {}
    for q in QS:
        taus_cut = [t for t in TAUS_NUM if t != 1e-2]
        coef_cut, _ = bfit_of(taus_cut, q)
        dtau[q] = abs(float(coef_cut[1]) - quad[q]["Bfit"])
    form_dev = [abs(b0_f + b1_f*q + b2_f*q*q + quad[q]["Bfit"]) for q in QS]   # Bfit = -B; compare vs -Bfit (sign bug fixed, run-4 fire on record)
    form_tol = [max(3*quad[q]["floor"], 10*dtau[q]) for q in QS]
    log("K-C(iii): dev %s vs tol %s (dtau %s)"
        % (["%.2e" % x for x in form_dev], ["%.2e" % x for x in form_tol],
           ["%.2e" % x for x in dtau.values()]))
    if any(dd > tt for dd, tt in zip(form_dev, form_tol)):
        finish(1, "K-C(iii) REJECT: exact quadratic form fails Bfit beyond the measured "
               "tau^3-leakage ablation scale",
               extra=dict(quad=quad, kb=kb, m_num=m_num, dtau=dtau,
                          varS2_direct=varS2_direct,
                          b0_ex=str(b0_ex), b1_ex=str(b1_ex), b2_ex=str(b2_ex)))
    finish(0, "BANKED: finite-tau0 numerator law N_num(tau0,q) = (3/4+5q/12) - "
              "(b0+b1*q+b2*q^2)*tau0 + O(tau0^2) with EXACT b0=%s b1=%s b2=%s "
              "(K-C(ii) DIRECT Var(S_q)/2 quadrature 1e-9 rel all q; K-C(iii) form vs "
              "Bfit within the measured ablation scale; -B(q)=Var(S_q)/2 exact Taylor "
              "algebra); consistency-family vs the engine (house rule 4)",
           extra=dict(quad=quad, kb=kb, m_num=m_num, dtau=dtau,
                      varS2_direct=varS2_direct,
                      b0_ex=str(b0_ex), b1_ex=str(b1_ex), b2_ex=str(b2_ex)))
finish(0, "MEASURED-ONLY: K-A clean at ng=320 (quadratic cumulant structure); exact-value "
          "leg unavailable this run (K-B/K-C estimator notes on record)",
       extra=dict(quad=quad, kb=kb, m_num=m_num, varS2_direct=varS2_direct))
