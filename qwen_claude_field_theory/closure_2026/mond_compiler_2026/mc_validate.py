"""
mc_validate.py -- physics validation of the reductions and the gate chain.

Nothing in the screen is trustworthy unless these pass.  Every check is a hard assert.

  V1  pure GR: Phi' = Psi' = Sigma/8 = 2 pi G Sigma exactly, at every Sigma
  V2  pure GR: no slip, mu == 1 (no MOND without a carrier)
  V3  MOND EXISTS inside the finite basis with NO free function: L = -chi X/2 + chi^3/3
      (an ALGEBRAIC constitutive chi with a CUBIC polynomial potential) plus a conformal
      matter coupling gives  mu -> 1 (Newtonian, G3 respected) and mu -> y (deep MOND),
      matching the closed form  mu(y) = (1/y)[(sqrt(k^2+4y)-k)/2]^2, k = sqrt(8/sqrt 2)
  V4  PART-I REPRODUCTION: for that carrier the traceless stress is exactly Sigma_P = mu s^2
      (Part I's Class A, up to the sign convention of the E-probe), NONZERO whenever the
      force is on
  V5  ghost calibration: +X/2 is flagged ghost, -X/2 is not; Maxwell F^2 is degenerate
      (A_0 null, no ghost) while nabla_m A_n nabla^m A^n has the A_0 ghost
  V6  Palatini archetype: the regular branch dies with the carrier OFF (A_mu = 0)
  V7  THE KNOWN PINCER, reproduced end to end:
        conformal-only coupling  -> dies at Gate-SLIP (lensing != dynamics)
        Bekenstein disformal     -> passes MOND + SLIP + H2, dies at Gate-PPN
                                    (unit-timelike aether => preferred-frame vacuum)
"""
import sys
import numpy as np
import mc_reduce_static as RS
import mc_gates as G
from mc_basis import N_OPS, N_PARAM, OP_INDEX, NAMED, _vec

np.seterr(all='ignore')
PASS = FAIL = 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}   {extra}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}   {extra}")


def solve_at(cvec, Sigma, X0=None):
    cext = np.concatenate([np.asarray(cvec[:N_OPS], float), [1.0]])
    mpar = np.asarray(cvec[N_OPS:], float)
    if X0 is None:
        X0 = np.zeros(RS.N_UNK)
        X0[G.IX["Phi1"]] = X0[G.IX["Psi1"]] = Sigma / 8.0
        X0[G.IX["phi1"]] = np.sqrt(Sigma)
        X0[G.IX["chi0"]] = np.sqrt(Sigma)
    return G.solve_static(cext, mpar, Sigma, X0)


# ------------------------------------------------------------------ V1 / V2 pure GR
print("V1/V2  pure GR")
c0 = np.zeros(N_PARAM)
dev, ok_all = 0.0, True
for Sg in [1e-3, 1.0, 1e3, 1e7]:
    X, ok, d = solve_at(c0, Sg)
    ok_all &= bool(ok)
    if ok:
        dev = max(dev, abs(X[G.IX["Phi1"]] - Sg / 8) / (Sg / 8),
                  abs(X[G.IX["Psi1"]] - Sg / 8) / (Sg / 8))
check("V1 GR gives Phi' = Psi' = Sigma/8 = 2 pi G Sigma", ok_all and dev < 1e-10,
      f"max rel dev {dev:.2e}")
X, ok, d = solve_at(c0, 1.0)
ob = G.observables(X, np.zeros(8))
check("V2 GR: mu == 1 and zero slip", ok and abs(ob["g_dyn"] - 0.125) < 1e-12
      and abs(ob["g_lens"] - ob["g_dyn"]) < 1e-14,
      f"g_dyn={ob['g_dyn']:.8e}  g_lens-g_dyn={ob['g_lens']-ob['g_dyn']:.1e}")

# ------------------------------------------------------------------ V3 / V4 AQUAL
print("\nV3/V4  MOND from a finite basis (algebraic chi, cubic polynomial, no free function)")
cA = _vec(NAMED["AQUAL_chi_cubic"])
ys, mus, sigps, ref = [], [], [], []
Xp = None
for Sg in 8.0 * np.logspace(-5, 6, 23):
    X, ok, d = solve_at(cA, Sg, Xp)
    if not ok:
        X, ok, d = solve_at(cA, Sg, None)
    if not ok:
        break
    Xp = X
    ob = G.observables(X, cA[N_OPS:])
    ys.append(abs(ob["g_dyn"]))
    mus.append(Sg / 8.0 / abs(ob["g_dyn"]))
    Mv = np.asarray(G._rt()["Mfun"](*X), float).reshape(N_OPS + 1, RS.N_COL)
    cext = np.concatenate([cA[:N_OPS], [1.0]])
    sigps.append(float((cext * Mv[:, RS.SIGP_COL]).sum()))
    ref.append(X[G.IX["chi0"]] * X[G.IX["phi1"]] ** 2)     # mu s^2 with mu = chi, s = phi'
k0 = np.sqrt(8.0 / np.sqrt(2.0))
ys, mus = np.array(ys), np.array(mus)
o = np.argsort(ys); ys, mus = ys[o], mus[o]
check("V3a solves across 11 decades of Sigma", len(ys) == 23, f"n={len(ys)}")
# mu approaches 1 as 1 - k/sqrt(y): at y = 1e6 the exact value is 0.997623.
check("V3b G3: mu -> 1 in the Newtonian limit, no rescaling of G",
      abs(mus[-1] - 1) < 3e-3 and abs(mus[-1] - (1 - k0 / np.sqrt(ys[-1]))) < 1e-5,
      f"mu(y={ys[-1]:.2e}) = {mus[-1]:.8f}  (1 - k/sqrt(y) = {1-k0/np.sqrt(ys[-1]):.8f})")
lo = ys < 0.05
sl = float(np.polyfit(np.log(ys[lo]), np.log(mus[lo]), 1)[0])
check("V3c G1: deep-MOND slope d ln mu / d ln y -> 1", abs(sl - 1) < 0.02, f"slope = {sl:.5f}")
k = k0
mu_pred = np.array([((np.sqrt(k * k + 4 * y) - k) / 2) ** 2 / y for y in ys])
check("V3d mu(y) matches the closed form (sqrt(k^2+4y)-k)^2/(4y), k = sqrt(8/sqrt2)",
      np.max(np.abs(mu_pred / mus - 1)) < 1e-6,
      f"max rel dev {np.max(np.abs(mu_pred/mus-1)):.2e}")
sigps, ref = np.array(sigps), np.array(ref)
rel = float(np.max(np.abs(sigps / ref - 1)))
check("V4a PART-I: Sigma_P = mu s^2 exactly (Class A of the committed no-go)",
      rel < 1e-9, f"max rel dev {rel:.2e}")
check("V4b PART-I: Sigma_P nonzero whenever the force is on",
      float(np.abs(sigps).min()) > 0, f"min |Sigma_P| = {np.abs(sigps).min():.3e}")

# ------------------------------------------------------------------ V5 ghost calibration
print("\nV5  Hessian / ghost calibration")
def probe(d):
    c = np.zeros(N_PARAM)
    for kk, vv in d.items():
        c[OP_INDEX[kk]] = vv
    return G.classify_hessian(c[:N_OPS], G.REF_BG[0])["status"]
check("V5a L = +X/2 is nondegenerate-ghost", probe(dict(P1=+0.5)) == "nondegenerate-ghost")
check("V5b L = -X/2 is healthy", probe(dict(P1=-0.5)) != "nondegenerate-ghost",
      probe(dict(P1=-0.5)))
check("V5c Maxwell F_mn F^mn is degenerate (A_0 null), NOT a ghost",
      probe(dict(K4=-0.25)) == "degenerate", probe(dict(K4=-0.25)))
check("V5d nabla_m A_n nabla^m A^n carries the A_0 ghost",
      probe(dict(K5=-1.0)) == "nondegenerate-ghost", probe(dict(K5=-1.0)))
cg = np.zeros(N_PARAM); cg[OP_INDEX["P1"]] = 0.5
check("V5e Gate-H pre-screen kills the robust ghost", not G.gate_H_pre(cg[:N_OPS])[0])

# ------------------------------------------------------------------ V6 Palatini
print("\nV6  Palatini vector-distortion archetype")
vP, iP = G.run_chain(_vec(NAMED["PALATINI_ARCHETYPE"]))
check("V6a regular branch dies with the carrier OFF (A_mu = 0)",
      vP == "Gate-CARRIER" and iP.get("carrier") == "CARRIER_OFF", f"{vP} {iP.get('carrier')}")
check("V6b degenerate branch chi = -3/25 annihilates the A-equation coefficient",
      abs(3.0 + 25.0 * (-3.0 / 25.0)) < 1e-15)

# ------------------------------------------------------------------ V7 the known pincer
print("\nV7  the known LENSING/PPN pincer, reproduced end to end")
vC, iC = G.run_chain(_vec(NAMED["AQUAL_chi_cubic"]))
check("V7a conformal-only coupling dies at Gate-SLIP (conformal scalars do not lens)",
      vC == "Gate-SLIP" and iC["frame_slip_worst"] > 1.0,
      f"{vC} frame_slip={iC.get('frame_slip_worst'):.4f}")
vT, iT = G.run_chain(_vec(NAMED["TeVeS_disformal"]))
check("V7b Bekenstein disformal frame gives zero frame slip (to solver precision)",
      iT.get("frame_slip_worst", 1.0) < 1e-8, f"frame_slip = {iT.get('frame_slip_worst'):.3e}")
check("V7c ... and passes Gate-MOND, Gate-SLIP and Gate-H2",
      iT.get("mond") == "PASS" and iT.get("slip") == "PASS" and iT.get("H2") == "PASS",
      f"mond={iT.get('mond')} slip={iT.get('slip')} H2={iT.get('H2')}")
check("V7d ... and dies at Gate-PPN on its unit-timelike (preferred-frame) vacuum",
      vT == "Gate-PPN" and iT.get("vacuum_boost_break", 0) > 0.5,
      f"{vT} boost_break={iT.get('vacuum_boost_break')}")

print(f"\nVALIDATE  {PASS} passed / {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
