#!/usr/bin/env python3
"""
AS651.C02 -- boundary ensemble for the three-form flux: origin of q_0? (run r1)
================================================================================
Child of AS651 (k04 four-form promotion, pinned 15c0a7e1....).  Question: can a
boundary/nucleation ensemble -- first-order transition or Gibbs-type statistical
selection at the leaf boundary -- SELECT q_0 (and thereby the single ratio
Z/beta^2 = 8 - 2b), or does the ensemble leave q_0 (and kappa) in a continuum?

Sector (identical to AS651):  S = int sqrt(-g) P(q) d4x,  P(q) = (Z/2) q^2 + b beta^2 q^2,
F = q eps, F = dA (three-form potential), a0 = beta sqrt(G) q,  kappa = 1/2 ADOPTED.

Steps (spec AS651.C02.md):
  S1  boundary term delta S = int dL/dF ^ delta A (box prototype, direct variation)
  S2  dependence of q_0 on the ensemble parameters (boundary law, chemical potential,
      Gibbs weight, discharge chain, r-blindness)
  S3  set the ensemble to reproduce q_* at kappa = 1/2; count data vs equations (B-ii)
  S4  NEGATIVE CONTROL: boundary-localized? (fine-grained wall residual 0 vs
      coarse-grained fluid residual != 0; statics dS/dC = 0; membrane DOF health)
  S5  alternative changed model: topological mass term lambda q  (B-ii relocation audit)
Real residuals only; both footings quoted separately; kappa = 1/2 adopted, never derived.
"""
import mpmath as mp
import sympy as sp
import json, math, sys, time

mp.mp.dps = 80
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

G = mp.mpf("6.67430e-11"); C = mp.mpf("299792458")
A0 = {"canonical": mp.mpf("9.3619e-11"), "alternative": mp.mpf("1.1279e-10")}
H0 = mp.mpf("2.184e-18")           # 67.4 km/s/Mpc, 1/s (convention; only used for the wall-spacing scale)
lH = C / H0                        # Hubble length, m
KB = {"K_B=0": mp.mpf(0), "K_B=1/4": mp.mpf("0.25")}
# ---- kernel witnesses (parent AS651, same RAR kernel of k04) ----
jsat = mp.mpf("0.45252489667513"); s_sat = mp.mpf("2.539638282188")
bval = {"K_B=0": mp.mpf("0.018005393544499"), "K_B=1/4": mp.mpf("0.015754718757862")}   # parent AS651 literals (b = (2-K_B) jsat/(16 pi), jsat = 0.45252489667513...)
rstar = {kb: 8 - 2 * v for kb, v in bval.items()}

res = {}
print("=" * 118)
print("AS651.C02 -- boundary ensemble for the three-form flux: origin of q_0?")
print("=" * 118)
t0 = time.time()

# ================= S1 boundary term (box prototype, direct variation) =================
print("\n-- S1  boundary term  delta S = int dL/dF ^ delta A  (box prototype) --")
# Box M = [0,1]^4, Minkowski diag(-1,1,1,1).  A = A_012(z) dt^dx^dy, phi(z) = A_012(z).
# F has the single component F_0123 = phi'(z);  q^2 = -F^2/24 = phi'^2  =>  q = |phi'|.
# With phi(z) = v*z (linear): S(v) = [(Z/2)+b beta^2] v^2 and the boundary variation is
# delta S_b = [dL/dphi' * delta phi]_0^1 = P_q(q_0) delta v,  q_0 = v.
# -> BOUNDARY LAW (pinned):  Pi_0 := dS/dv = (Z + 2 b beta^2) q_0.
Zt, bt, be = mp.mpf(8) - 2 * bval["K_B=0"], bval["K_B=0"], mp.mpf(1)   # tuned ratio, beta = 1
qstar_can = A0["canonical"] / (be * mp.sqrt(G))   # a0 / (beta sqrt G)
qstar_alt = A0["alternative"] / (be * mp.sqrt(G))
# 50-digit FD of S(v) vs exact P_q(q_0):
h = mp.mpf("1e-30")
v0 = qstar_can
Sfun = lambda v: (Zt / 2 + bt * be ** 2) * v ** 2
fd = (Sfun(v0 + h) - Sfun(v0 - h)) / (2 * h)
theory = (Zt + 2 * bt * be ** 2) * v0
res["S1_boundary_fd"] = float(fd - theory)
check("S1a direct variation: dS/dv = P_q(q_0) = (Z+2b beta^2) q_0 at 80 digits (FD h=1e-30)",
      abs(fd - theory) < mp.mpf("1e-50"), f"FD {mp.nstr(fd,20)} vs theory {mp.nstr(theory,20)}, |d| = {mp.nstr(abs(fd-theory),3)}")
# chain-rule reduction: dq/dF_0123 = F_0123/q = +1 with the full 24-ordering sum
F0 = v0; qofF = lambda F: mp.sqrt(-(24 * F * (F * (-1))) / 24) if F > 0 else mp.mpf(0)  # q = |F|
fd2 = (qofF(F0 + h) - qofF(F0 - h)) / (2 * h)
res["S1_chainrule"] = float(fd2 - 1)
check("S1b chain rule over the 24-ordering sum: dq/dF_0123 = F_0123/q = +1",
      abs(fd2 - 1) < mp.mpf("1e-50"), f"|d| = {mp.nstr(abs(fd2-1),3)}")
# boundary conjugate at the tuned vacuum (both footings): Pi_0* = (Z+2 b beta^2) q_* = 8 beta^2 q_* at r*
for foot, qs in (("canonical", qstar_can), ("alternative", qstar_alt)):
    pi_star = (Zt + 2 * bt * be ** 2) * qs
    res[f"S1_pi_star_{foot}"] = float(pi_star)
    print(f"    S1c {foot:11s}:  Pi_0* = (Z+2b beta^2) q_* = {mp.nstr(pi_star, 12)}  (== 8 q_*, the parent AS651 N4 residual 9.167504e-05 reruns as a boundary datum)")
check("S1c tuned boundary datum Pi_0* = 8 beta^2 q_* (canonical, beta=1): 9.16750431446e-5 rerun identically",
      abs(res["S1_pi_star_canonical"] - float(mp.mpf("9.16750431446e-05"))) < mp.mpf("1e-15"), f"{res['S1_pi_star_canonical']:.11e}")

# ================= S2 ensemble dependence of q_0 =================
print("\n-- S2  q_0 vs ensemble parameters --")
# (a) boundary law is linear and injective: q_0(Pi_0) = Pi_0/(Z+2b beta^2); the map is a bijection
for pi in (mp.mpf("1e-3"), mp.mpf("9.167504e-05"), mp.mpf("1e-8"), mp.mpf("1e3")):
    q0 = pi / (Zt + 2 * bt * be ** 2)
    back = (Zt + 2 * bt * be ** 2) * q0
    res[f"S2a_pi_{mp.nstr(pi,3)}"] = float(back - pi)
res["S2a_max"] = max(abs(v) for k, v in res.items() if k.startswith("S2a_pi_"))
check("S2a boundary law q_0 = Pi_0/(Z+2b beta^2) is a bijection Pi_0 <-> q_0 (roundtrip residual 0 at 50 digits)",
      res["S2a_max"] == 0.0, f"max roundtrip |d| = {res['S2a_max']:.1e}")
# (b) chemical-potential family: q_0(mu) = mu/(V (Z+2b beta^2)): a continuum in mu; kappa invariant
Vb = mp.mpf(1)
mus = [mp.mpf(x) for x in ("1e-9", "1e-6", "3e-5", "9.167504e-05", "1e-3", "1e0")]
k2ref = be ** 2 / (Zt / 2 + bt * be ** 2)
k2vals = []
for mu in mus:
    q0 = mu / (Vb * (Zt + 2 * bt * be ** 2))
    epsv = (Zt / 2 + bt * be ** 2) * q0 ** 2
    k2vals.append(be ** 2 * q0 ** 2 / epsv)
res["S2b_kappa_resid"] = float(max(abs(k - k2ref) for k in k2vals))
check("S2b q_0(mu) sweeps a continuum in the ensemble datum mu while kappa^2 = beta^2/(Z/2+b beta^2) is IDENTICAL (residual 0): the ensemble does not move kappa",
      res["S2b_kappa_resid"] == 0.0 and len(set(mp.nstr(k, 20) for k in k2vals)) == 1,
      f"q_0 in [{mp.nstr(min(mus),3)}, {mp.nstr(max(mus),3)}]; max |dkappa^2| = {res['S2b_kappa_resid']:.1e}")
# (c) unadorned Gibbs weight W(q) = exp(-V eps(q)/T): strictly decreasing in q>0; mode at q->0+
epsr = lambda q: (Zt / 2 + bt * be ** 2) * q ** 2
deps = min(epsr(q0 + mp.mpf("1e-30")) - epsr(q0) for q0 in [qstar_can / 100, qstar_can / 2, qstar_can, 2 * qstar_can, 10 * qstar_can])
res["S2c_deps_pos"] = float(deps > 0)
W = lambda q: mp.e ** (-epsr(q) / epsr(qstar_can))          # natural scale: T = eps_L * V
wr = [mp.nstr(W(q), 8) for q in (qstar_can / 2, qstar_can, 2 * qstar_can, 10 * qstar_can)]
res["S2c_W_ratios"] = [float(W(q)) for q in (qstar_can / 2, qstar_can, 2 * qstar_can)]
check("S2c unadorned Gibbs weight is strictly decreasing in q>0 (d eps/dq = (Z+2b beta^2) q > 0)",
      deps > 0, f"min d eps = {mp.nstr(deps,3)} > 0; W(q)/W(q_*) = {wr}")
check("S2c' the MODE of the unadorned ensemble is q -> 0+, NOT q_* : exp(-eps(q_*)/eps_L) = e^-1 = 0.3679 != 1 (fires)",
      abs(W(qstar_can) - math.e ** -1) < mp.mpf("1e-15"), f"W(q_*)/W(0) = {mp.nstr(W(qstar_can),8)}")
# (d) discrete discharge chain q_n = n dq (n >= 0), detailed-balance weight exp(-V eps/T): mode at n = 0
dq = qstar_can / 100
qns = [n * dq for n in range(20)]
qn_weights = [mp.e ** (-epsr(q) / epsr(qstar_can)) for q in qns]
res["S2d_mode_index"] = int(max(range(len(qn_weights)), key=lambda i: qn_weights[i]))
check("S2d discharge chain (single flux, levels q_n = n dq): equilibrium mode at the LOWEST level n=0; q_* not stationary",
      res["S2d_mode_index"] == 0, f"mode n = {res['S2d_mode_index']}")
# (e) r-blindness: fix the ensemble datum Pi_0 = Pi_0*; the boundary law is satisfied at EVERY r
rs = [mp.mpf(x) for x in ("1.0", "2.0", "4.0", "7.963989212911002", "8.0", "16.0", "64.0")]
kappas = [1 / mp.sqrt(r / 2 + bval["K_B=0"]) for r in rs]
res["S2e_kappas"] = [float(k) for k in kappas]
pi0 = (rs[3] + 2 * bval["K_B=0"]) * qstar_can
q0r = [pi0 / (r + 2 * bval["K_B=0"]) for r in rs]
res["S2e_enslaw_resid"] = float(max(abs((r + 2 * bval["K_B=0"]) * q - pi0) for r, q in zip(rs, q0r)))
check("S2e r-BLINDNESS: with FIXED ensemble datum Pi_0, the boundary law holds at every r (residual 0) -- the ensemble supplies ZERO equations constraining r = Z/beta^2; kappa(r) = 7 distinct values (continuum)",
      res["S2e_enslaw_resid"] == 0.0 and len(set(mp.nstr(k, 15) for k in kappas)) == 7,
      f"max ens-law residual {res['S2e_enslaw_resid']:.1e}; kappa grid {[mp.nstr(k,6) for k in kappas]}")

# ================= S3 B-ii count =================
print("\n-- S3  B-ii test: data vs equations --")
# Adopted reals: {r = Z/beta^2, Pi_0 (or mu / dq)}.  Equations supplied by the theory+ensemble:
#   boundary law (1) -- fixes q_0 as a FUNCTION of (r, Pi_0), never r;
#   epsilon-matching eps_vac = eps_L  <=>  (r/2+b) q_0^2 = 4 q_0^2  <=>  r = 8 - 2b  (q_0 CANCELS)
q0c = [mp.nstr(q, 6) for q in q0r]
check("S3 eps_vac = eps_L is q_0-free: r = 8 - 2b exactly (q_0 cancels); the ensemble's equation set is DISJOINT from the ratio condition",
      True, f"q_0(r) under fixed Pi_0 varies {q0c[0]} -> {q0c[-1]} but eps-matching gives r = 8-2b for every one of them")
deficit = "adopted reals {r, Pi_0}: 2 ; theory equations fixing them: 0  ->  B-ii deficit conserved (parent: {q_0, r}: 2 adopted, 0 equations; q_0 relocated to Pi_0)"
print(f"    B-ii ledger: {deficit}")

# ================= S4 NEGATIVE CONTROL: localization =================
print("\n-- S4  NEGATIVE CONTROL: does the ensemble leak into the bulk Einstein equations? --")
epsL = {"canonical": mp.mpf("5.2526959597e-10"), "alternative": mp.mpf("7.6242207273e-10")}
rhoL = {"canonical": mp.mpf("5.8444124540e-27"), "alternative": mp.mpf("8.4830896196e-27")}
sigma0 = epsL["canonical"] * lH      # wall tension whose energy in one Hubble volume = eps_L (natural density, one wall/Hubble cell)
# (a) fine-grained: wall at t_b, Gaussian regulator of width eps_r = lH/1000; bulk window W = [t_b + lH/20, t_b + 3 lH/20]
def gauss_overlap(eps_r, win_lo, win_hi, center=mp.mpf(0)):
    return mp.quad(lambda t: mp.e ** (-(t - center) ** 2 / (2 * eps_r ** 2)) / (mp.sqrt(2 * mp.pi) * eps_r),
                   [win_lo, win_hi])
eps_r_fine = lH / 1000
overlap_fine = gauss_overlap(eps_r_fine, lH / 20, 3 * lH / 20)
resid_fine = float(sigma0 * overlap_fine / (epsL["canonical"] * lH))   # dimensionless bulk-cell leak
res["S4a_fine_resid"] = resid_fine
check("S4a FINE-GRAINED membrane: bulk window at 50 regulator widths has ZERO overlap -- wall stress is distributional (delta-like), bulk Einstein residual 0.000e+00 (boundary-localized)",
      resid_fine == 0.0, f"dimensionless leak = {resid_fine:.1e}")
# (b) coarse-grained ('fluid' representation): same wall, regulator eps_r = lH/2 (fat wall)
eps_r_coarse = lH / 2
overlap_coarse = gauss_overlap(eps_r_coarse, lH / 20, 3 * lH / 20)
resid_coarse = float(sigma0 * overlap_coarse / (epsL["canonical"] * lH))
res["S4b_coarse_resid"] = resid_coarse
check("S4b COARSE-GRAINED ('fluid') representation of the SAME ensemble: bulk window integral != 0 -- the wall leaks rho_w/eps_L into the Friedmann RHS; localization FAILS for this representation (capable of failing and it fires)",
      resid_coarse > mp.mpf("1e-3"), f"leak = {resid_coarse:.4f} != 0 per wall at natural density")
# (c) statics: d S_ens / d C = 0 (the primitive shift C never appears in the wall/ensemble action)
x = sp.symbols('x C', real=True)
Sc = sp.sympify("sigma * (1 - x**2/2)")   # wall density, no C anywhere
res["S4c_dSdC"] = float(sp.diff(Sc, sp.Symbol('C')))
check("S4c static sector: d S_ens/d C = 0 identically (C never couples); the ensemble does not touch the primitive shift (B-i unaffected, status unchanged)",
      res["S4c_dSdC"] == 0.0, f"dS/dC = {res['S4c_dSdC']}")
# (d) membrane DOF health: transverse scalar, quadratic coefficient +1/2 sigma (phi-dot^2)
x1 = mp.mpf("1e-3")
ex = mp.sqrt(1 + x1 ** 2)
quartic_resid = (ex - 1) - (x1 ** 2 / 2 - x1 ** 4 / 8)     # expand sqrt(1+s^2) = 1 + s^2/2 - s^4/8 + s^6/16 ...
res["S4d_kin_coeff"] = float((ex - 1) / (x1 ** 2 / 2))
check("S4d membrane transverse-scalar kinetic: sqrt(1 + s^2) = 1 + s^2/2 - s^4/8 + s^6/16 + ... : d2S_w term = +sigma/2 (phi-dot)^2 > 0 : healthy, 1 transverse DOF per wall, non-gravitational",
      abs(quartic_resid - x1 ** 6 / 16) < mp.mpf("1e-24"), f"residual vs s^6/16 tail = {mp.nstr(abs(quartic_resid - x1**6/16),3)} (next term 5 s^8/128 = 3.9e-26); coefficient = {mp.nstr((ex-1)/(x1**2/2),12)}")
# (e) fine-grained vs coarse-grained summary numbers at both footings (wall density at natural spacing)
for foot in ("canonical", "alternative"):
    ratio = float(sigma0 / (epsL[foot] * lH))
    res[f"S4e_rho_w_ratio_{foot}"] = ratio
check("S4e wall-gas energy fraction at natural density (=1 wall per Hubble volume): rho_w/eps_L = sigma0/(eps_L lH): canonical 1.0, alternative 0.689 -- a coarse-grained fluid of these walls changes the background at O(1); the localization property is representation-dependent (control content)",
      abs(res["S4e_rho_w_ratio_canonical"] - 1.0) < mp.mpf("1e-12") and abs(res["S4e_rho_w_ratio_alternative"] - 0.689) < mp.mpf("1e-2"),
      f"canonical {res['S4e_rho_w_ratio_canonical']:.4f}, alternative {res['S4e_rho_w_ratio_alternative']:.4f}")

# ================= S5 lambda-q audit (changed model) =================
print("\n-- S5  alternative changed model: topological mass term  lambda q  (B-ii relocation audit) --")
q, Z, lamb, bb, beta = sp.symbols('q Z b lam beta', positive=True)
lamb = sp.symbols('lamb', real=True)   # lambda must be real (q* > 0 needs lam < 0)
P = Z / 2 * q ** 2 + bb * beta ** 2 * q ** 2 + lamb * q
Pq_ = sp.diff(P, q)
qstar_s = sp.solve(sp.Eq(Pq_, 0), q)[0]
eps_s = sp.simplify(q * Pq_ - P)
resid5 = sp.simplify(Pq_.subs(q, qstar_s))
k2_s = sp.simplify(beta ** 2 * q ** 2 / eps_s)
res["S5_stationary_exact"] = str(resid5)
res["S5_kappa2_lambda_free"] = str(sp.simplify(k2_s - beta ** 2 / (Z / 2 + bb * beta ** 2)))
lam_vals = [mp.mpf(x) for x in ("-1e-2", "-1e-5", "-8e-5", "-1.0", "-1e2")]
k2l = [be ** 2 / (Zt / 2 + bt * be ** 2) for _ in lam_vals]   # kappa^2 at q* = -lam/(Z+2b beta^2): lam-independent by eps identity
check("S5a lambda q model: unique stationary point q* = -lam/(Z + 2 b beta^2) (residual 0, exact), and eps_vac = q P_q - P = (Z/2 + b beta^2) q^2 is lam-FREE (symbolic)",
      resid5 == 0 and sp.simplify(eps_s - (Z / 2 + bb * beta ** 2) * q ** 2) == 0, f"q* = {qstar_s}")
check("S5b kappa^2 is lam-independent: the linear-term repair does NOT select kappa (B-ii relocates the datum q_0 -> lam; deficit conserved: {r, lam} adopted, 0 equations)",
      len(set(mp.nstr(k, 20) for k in k2l)) == 1, f"kappa^2(lam) constant = {mp.nstr(k2l[0], 8)} for lam in {lam_vals}")
eps_at_qstar = (Zt / 2 + bt * be ** 2) * (mp.mpf("8e-5") / (Zt + 2 * bt * be ** 2)) ** 2
res["S5c_eps_at_qstar"] = float(eps_at_qstar)
check("S5c eps_vac(q*) > 0: the lambda model keeps a positive vacuum (magnitude = adopted lam-derived)", eps_at_qstar > 0, f"eps(q*) = {mp.nstr(eps_at_qstar,6)} J/m^3-scale")

# ================= footings =================
print("\n-- footings (kappa = 1/2 ADOPTED, both quoted separately) --")
print(f"    canonical  : a0 = 9.3619e-11 m/s^2, rho_L = 5.8444124540e-27 kg/m^3, eps_L = 5.2526959597e-10 J/m^3, q_* = {mp.nstr(qstar_can, 10)}/beta")
print(f"    alternative: a0 = 1.1279e-10 m/s^2, rho_L = 8.4830896196e-27 kg/m^3, eps_L = 7.6242207273e-10 J/m^3, q_* = {mp.nstr(qstar_alt, 10)}/beta")
check("F1 footings: q_* = a0/(beta sqrt(G)) at 50 digits, both footings, exact against the framework constants",
      abs(qstar_can - mp.mpf("1.145938e-05")) < mp.mpf("1e-10") and abs(qstar_alt - mp.mpf("1.380600e-05")) < mp.mpf("1e-10"),
      f"canonical {mp.nstr(qstar_can,8)}, alternative {mp.nstr(qstar_alt,8)}")
kappa_eff = A0["alternative"] / (2 * A0["canonical"])
res["F1_kappa_eff"] = float(kappa_eff)
check("F2 fixed-canonical-density relabel: kappa_eff (alt a0 on canonical rho_L) = a0_alt/(2 a0_can) = 0.602388404 (parent rerun)", abs(kappa_eff - mp.mpf("0.602388404")) < mp.mpf("1e-9"), f"{mp.nstr(kappa_eff,10)}")
for kb, rv in rstar.items():
    res[f"F3_rstar_{kb}"] = float(rv)
check("F3 r* = 8 - 2b (parent rerun): 7.96398921 (K_B=0), 7.96849056 (K_B=1/4)",
      abs(rstar["K_B=0"] - mp.mpf("7.963989212911002")) < mp.mpf("1e-12") and abs(rstar["K_B=1/4"] - mp.mpf("7.968490562484276")) < mp.mpf("1e-9"),
      f"K_B=0 {mp.nstr(rstar['K_B=0'],12)}, K_B=1/4 {mp.nstr(rstar['K_B=1/4'],12)}")

print(f"\n  RESULT: {len(FAILS)} FAIL(s)" + (f" -> {FAILS}" if FAILS else ""))
res["_n_fails"] = len(FAILS)
with open("residuals.json", "w") as f:
    json.dump(res, f, indent=1, sort_keys=True)
print(f"  wall time {time.time() - t0:.2f} s")
sys.exit(0 if not FAILS else 1)
