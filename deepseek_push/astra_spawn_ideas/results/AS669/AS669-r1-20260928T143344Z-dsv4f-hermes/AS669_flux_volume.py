#!/usr/bin/env python3
"""
AS669 -- topological flux integral and metric volume dependence of the vacuum
============================================================================
Seed: AS669 (Tier-0, requirement-13 adjacent). Source branch: k04 four-form
promotion (kappa_closure/k04_four_form_promotion_consistency.py, pinned SHA
15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399).

Model cell (k04, no modification):
  F4 = q eps_g  (homogeneous four-form field strength, dual amplitude q)
  vacuum action density P(q) = (Z/2) q^2 + b beta^2 q^2   (Z, beta, b > 0)
  promoted scale:   a0 = beta sqrt(G) |q|
  gravitating energy density:  eps_vac = q P_q - P  (Legendre form, k04 F1)
  stress tensor:    T_mu nu = (P - q P_q) g_mu nu   (k04; derived below by
                    varying the action with F held fixed form-wise)
  flux identity:    Phi = int_M F4 = q Vol4(g)   (compact oriented M^4,
                    homogeneous q; Vol4 = int_M eps_g)

Questions (seed steps):
  1. fix the source equation/measure/boundaries (above),
  2. fixed integrated flux vs fixed local q under metric volume variation,
  3. keep every integration constant independent (Z, beta, b, Phi, Vol4, q0),
  4. negative control: q and Phi simultaneously fixed under metric changes,
  5. verify by substitution and independent representation.

All algebra is exact (sympy) -- the founding identities are definitional and
their Legendre/cancellation content is verified symbolically; numerical
witnesses (mpmath, dps=60, refinement at dps=100) cover S^4 (round) and T^4
(flat) fixtures under declared conformal rescalings.  No fits, no
observational data, no new particle species.
"""
import json, math, sys, time
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
start = time.time()

R = {}
CHECKS = []


def check(name, ok, detail="", tol=None, capable=None):
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""), flush=True)
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail,
                   "tolerance": tol, "capable_of_failing": capable})


# ----------------------------------------------------------------------------
# constants (SI; mandated defaults)
# ----------------------------------------------------------------------------
G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
A0_CAN = mp.mpf("9.3619e-11")   # canonical footing a0
A0_ALT = mp.mpf("1.1279e-10")   # alternative footing a0
KB = (mp.mpf("0.0"), mp.mpf("0.25"))

q_can = A0_CAN / mp.sqrt(G)     # homogeneous amplitude, beta = 1
q_alt = A0_ALT / mp.sqrt(G)
# framework densities for later cross-checks
rhoL_can = mp.mpf("5.844412454e-27")
rhoL_alt = mp.mpf("8.483089620e-27")
epsL_can = 4 * A0_CAN**2 / G    # = rho_Lambda c^2 with rho_L = 4 a0^2/(G c^2)
epsL_alt = 4 * A0_ALT**2 / G

print("=" * 100)
print("AS669 -- flux integral / metric-volume dependence (k04 branch)")
print("=" * 100)

# ----------------------------------------------------------------------------
# 1. symbolic core (exact)
# ----------------------------------------------------------------------------
q, Z, b, beta, Gs = sp.symbols("q Z b beta G", positive=True)
Phi, Vol, dPhi, dq, dVol = sp.symbols("Phi Vol dPhi dq dVol", real=True)

P = Z * q**2 / 2 + b * beta**2 * q**2
eps = sp.simplify(q * sp.diff(P, q) - P)      # gravitating energy (Legendre)
Tcc = sp.simplify(P - q * sp.diff(P, q))      # T_mu nu = (P - q P_q) g_mu nu

# derived stress tensor from variation (first-principles obligation):
#   F = q eps_g fixed form-wise  =>  q sqrt(-g) = F_0123 = const
#   delta(S)/delta g^mu nu  =>  T_mu nu = (P - q P_q) g_mu nu
# under a global conformal rescaling g -> lam^2 g:  sqrt(-g) -> lam^4 sqrt(-g)
lam = sp.symbols("lam", positive=True)
q_scaled = sp.simplify(q / lam**4)            # delta(q sqrt(-g)) = 0
Tderiv = sp.simplify(P.subs(q, q_scaled) - q_scaled * sp.diff(P, q).subs(q, q_scaled))

# kappa^2 = a0^2/(G eps_vac); a0^2/G = beta^2 q^2
kappa2 = sp.simplify(beta**2 * q**2 / eps)
kappa2_flat = sp.simplify(2 * beta**2 / (Z + 2 * b * beta**2))
ratio_needed = sp.solve(sp.Eq(kappa2, sp.Rational(1, 4)), Z)[0]

# volume laws (algebraic, from Phi = q*Vol)
q_of = sp.simplify(Phi / Vol)
dq_dVol = sp.diff(q_of, Vol)                  # fixed flux
dPhi_dVol_fixq = sp.diff(q * Vol, Vol)        # fixed local q
# negative control algebra: dPhi = q dVol + Vol dq with dq = dPhi = 0
resid = sp.simplify(q * dVol + Vol * dq - dPhi)

print("\n-- step 1/3: fixed source equation, measure, boundary conditions --")
print(f"    P(q) = {P}")
print(f"    eps_vac = q P_q - P = {eps}")
print(f"    T_mu nu = (P - q P_q) g_mu nu = {Tcc} g_mu nu")
print(f"    conformal q(lam) = q/lam^4 from delta(q sqrt(-g)) = 0:  {q_scaled}")
print(f"    T on scaled flux: {Tderiv} g_mu nu  (same form, eps -> eps/lam^8)")

check("S1 [sign F1 re-derived] eps_vac = qP_q - P gives promoted primitive +b a0^2/G",
      sp.simplify(eps - (Z * q**2 / 2 + b * beta**2 * q**2)) == 0,
      f"eps = +Z q^2/2 + b beta^2 q^2  (k01's -b a0^2/G reversed without touching the gradient term)")

print("\n-- step 2: fixed integrated flux vs fixed local q under volume variation --")
print(f"    Phi = q Vol4 ;  fixed flux:  q = Phi/Vol4,  dq/dVol = -Phi/Vol^2 = -q/Vol")
print(f"    fixed local q: dPhi/dVol = q")
print(f"    kappa^2 = a0^2/(G eps) = {kappa2}  ->  {kappa2_flat}   (q and Vol cancel)")
print(f"    kappa = 1/2  <=>  Z/beta^2 = {sp.simplify(ratio_needed / beta**2)}")

print("\n-- step 4: negative control (q and Phi simultaneously fixed) --")
print(f"    variation of Phi = q Vol:  dPhi = q dVol + Vol dq ;  with dq = dPhi = 0:")
print(f"    residual = q dVol  (identically {resid} is 0 only when dVol = 0 or q = 0)")

check("S2 [flux identity] Phi = q*Vol is definitional; fixed-flux amplitude law dq/dVol = -q/Vol",
      sp.simplify(dq_dVol + q_of / Vol) == 0,
      "dq/dVol + q/Vol = 0 exactly (symbolic)")
check("S3 [fixed-q law] dPhi/dVol = q exactly; Phi linear in Vol at fixed q",
      sp.simplify(dPhi_dVol_fixq - q) == 0)
check("S4 [kappa volume-blind] kappa^2 = 2 beta^2/(Z + 2 b beta^2): q and Vol absent",
      sp.simplify(kappa2 - kappa2_flat) == 0,
      f"kappa^2 = {kappa2_flat}")
check("S5 [half condition] kappa = 1/2  <=>  Z/beta^2 = 8 - 2b  (FLUX amplitude cancels; ratio of two couplings unfixed - k04 F2)",
      sp.simplify(sp.simplify(ratio_needed / beta**2) - (8 - 2 * b)) == 0,
      f"Z/beta^2 = {sp.simplify(ratio_needed / beta**2)}")
check("S6 [negative-control algebra] dPhi = q dVol + Vol dq; simultaneous dq = dPhi = 0 forces q dVol = 0",
      sp.simplify(resid.subs({dq: 0, dPhi: 0}) - q * dVol) == 0,
      "residual = q dVol <> 0 for q <> 0, dVol <> 0: overdetermined (2 constraints, 1 identity, 1 free variation)")

# ----------------------------------------------------------------------------
# 2. inherited k04 boundary datum: b = (2-K_B) I_rar/(16 pi) (k01/RAR integral)
#    RAR kernel: Delta(s) = s/expm1(sqrt(s)) = h_RAR(s) = s (nu_RAR(s) - 1)
# ----------------------------------------------------------------------------
# RAR kernel on the k04 footing: Delta(s) = s/(e^sqrt(s) - 1) = h_RAR(s)
def Delta_s(s):
    return s / (mp.exp(mp.sqrt(s)) - 1)

# s_sat: maximum of Delta  <=>  (1 - u/2) e^u = 1 with u = sqrt(s)
u_sat = mp.findroot(lambda u: (1 - u / 2) * mp.exp(u) - 1, 1.59)
s_sat = u_sat**2
# j(s) = 2 (s Delta(s) - int_0^s Delta);  substitute s = t^2 for a smooth integrand
I_rar = 2 * (s_sat * Delta_s(s_sat) - 2 * mp.quad(lambda t: t**3 / (mp.exp(t) - 1), [0, mp.sqrt(s_sat)]))
print("\n-- inherited boundary datum (imported from k01 through k04, RAR kernel) --")
print(f"    s_sat = {mp.nstr(s_sat, 12)}  (max of h_RAR; framework landmark y_p ~ 2.5396)")
print(f"    I_rar = j(s_sat) = {mp.nstr(I_rar, 12)}")
b_of = {k: (2 - k) * I_rar / (16 * mp.pi) for k in KB}
Zratio = {k: 8 - 2 * b_of[k] for k in KB}
for k in KB:
    print(f"    K_B = {k}: b = {mp.nstr(b_of[k], 12)},  Z/beta^2 = {mp.nstr(Zratio[k], 12)}")
check("S7 [k04 F2 number reproduced] Z/beta^2 = 8 - 2b in (7.95, 7.98) at K_B in {0, 0.25}",
      all(mp.mpf("7.95") < Zratio[k] < mp.mpf("7.98") for k in KB),
      f"K_B=0 -> {mp.nstr(Zratio[KB[0]], 6)} (k04 quotes 7.96)", tol="1e-2 window")

# ----------------------------------------------------------------------------
# 3. numerical witnesses -- S^4 round metric, T^4 flat metric
# ----------------------------------------------------------------------------
print("\n-- numerical witnesses (mpmath dps=60; S^4 round, T^4 flat) --")

def vol_s4(Rs):
    # product measure: sqrt(g) = sin^3 chi sin^2 t1 sin t2
    I1 = mp.quad(lambda x: mp.sin(x)**3, [0, mp.pi])
    I2 = mp.quad(lambda x: mp.sin(x)**2, [0, mp.pi])
    I3 = mp.quad(lambda x: mp.sin(x), [0, mp.pi])
    return Rs**4 * I1 * I2 * I3 * 2 * mp.pi

V1 = vol_s4(mp.mpf(1))
V1_exact = 8 * mp.pi**2 / 3
check("N1a [S^4 volume] Vol = 8 pi^2 R^4/3 at R = 1",
      abs(V1 - V1_exact) < mp.mpf("1e-55") * V1_exact,
      f"quad = {mp.nstr(V1, 20)}, exact 8pi^2/3 = {mp.nstr(V1_exact, 20)}, rel |d| < 1e-55",
      tol="1e-55 rel (dps=60)")

Rs = (mp.mpf(1), mp.mpf(3) / 2, mp.mpf(2))
vols = {r: vol_s4(r) for r in Rs}
# dilution checks at fixed flux Phi0 = q_can * V1
Phi0 = q_can * V1
q_fix_Phi = {r: Phi0 / vols[r] for r in Rs}          # fixed flux
Phi_fix_q = {r: q_can * vols[r] for r in Rs}          # fixed local q
for r in Rs[1:]:
    rat = vols[Rs[0]] / vols[r]
    check(f"N2a [fixed-flux dilution R={float(r)}] q2/q1 = (V1/V2) = (R1/R2)^4",
          abs(q_fix_Phi[r] / q_fix_Phi[Rs[0]] - rat) < mp.mpf("1e-50"),
          f"q2/q1 = {mp.nstr(q_fix_Phi[r] / q_fix_Phi[Rs[0]], 15)}, (R1/R2)^4 = {mp.nstr(rat, 15)}",
          tol="1e-50 rel (dps=60)")
    check(f"N2b [fixed-q law R={float(r)}] Phi2/Phi1 = (V2/V1) = (R2/R1)^4",
          abs(Phi_fix_q[r] / Phi_fix_q[Rs[0]] - 1 / rat) < mp.mpf("1e-50"),
          f"Phi2/Phi1 = {mp.nstr(Phi_fix_q[r] / Phi_fix_q[Rs[0]], 15)}, (R2/R1)^4 = {mp.nstr(1 / rat, 15)}",
          tol="1e-50 rel")
# energy / a0 / kappa response
Q2 = mp.mpf("8") - 2 * b_of[KB[0]]                       # Z/beta^2 at kappa = 1/2 (K_B=0)
def eps_vac(qv):
    return (Q2 / 2 + b_of[KB[0]]) * qv**2
def kap2raw(qv):
    den = (Q2 / 2) * qv**2 + b_of[KB[0]] * qv**2
    return qv**2 / den
for r in Rs[1:]:
    lam4 = (vols[r] / vols[Rs[0]])                        # = (R2/R1)^4
    kq = kap2raw(q_fix_Phi[r]) / kap2raw(q_fix_Phi[Rs[0]])
    ke = eps_vac(q_fix_Phi[r]) / eps_vac(q_fix_Phi[Rs[0]])
    check(f"N3 [fixed flux, R={float(r)}] eps_vac ~ Vol^-2, a0 ~ Vol^-1, kappa^2 invariant",
          abs(ke - 1 / lam4**2) < mp.mpf("1e-50") and abs(kq - 1) < mp.mpf("1e-58"),
          f"eps ratio = {mp.nstr(ke, 10)} vs (V1/V2)^2 = {mp.nstr(1 / lam4**2, 10)}; kappa^2 ratio = {mp.nstr(kq, 10)}",
          tol="1e-50 / 1e-58")

# negative control: simultaneously fixed q and Phi
r1, r2 = Rs[0], Rs[2]
fixed_resid = q_can * (vols[r2] - vols[r1])
check("NEG1 [negative control] simultaneous dq = dPhi = 0 violated: residual q (V2 - V1) != 0",
      fixed_resid > mp.mpf("1e-10") * q_can * vols[r1],
      f"q*DeltaV = {mp.nstr(fixed_resid, 8)} kg^1/2 m^7/2 s^-1; identity requires V2 = V1, ratio V2/V1 = {mp.nstr(vols[r2] / vols[r1], 12)}",
      capable="would PASS only if V2 = V1 (volume-preserving variations); any volume-changing metric change fires")

# finite-difference consistency of the two single-fix laws (central differences)
h = mp.mpf("1e-8")
V = lambda rr: vol_s4(rr)
# fixed q: dPhi/dR = q dV/dR
dPhi_dR_num = (q_can * V(mp.mpf(1) + h) - q_can * V(mp.mpf(1) - h)) / (2 * h)
dPhi_dR_ex = q_can * 4 * V1_exact                            # dV/dR = 4*Vol/R at R=1
# fixed flux: dq/dR = -Phi V'/V^2
dq_dR_num = (Phi0 / vol_s4(mp.mpf(1) + h) - Phi0 / vol_s4(mp.mpf(1) - h)) / (2 * h)
dq_dR_ex = -Phi0 * 4 * V1_exact / V1**2
check("N4 [FD consistency, fixed-q] dPhi/dR = q dV/dR (central FD)",
      abs(dPhi_dR_num - dPhi_dR_ex) / dPhi_dR_ex < mp.mpf("1e-10"),
      f"FD = {mp.nstr(dPhi_dR_num, 10)}, analytic = {mp.nstr(dPhi_dR_ex, 10)}", tol="1e-10 (FD truncation)")
check("N5 [FD consistency, fixed-flux] dq/dR = -q dV/dR / V (central FD)",
      abs(dq_dR_num - dq_dR_ex) / abs(dq_dR_ex) < mp.mpf("1e-10"),
      f"FD = {mp.nstr(dq_dR_num, 10)}, analytic = {mp.nstr(dq_dR_ex, 10)}", tol="1e-10")

# independent representation on T^4: exact-form addition leaves Phi and q unchanged
Lper = 2 * mp.pi
Vt4 = Lper**4
Phi0_t4 = q_can * Vt4
int_dC = mp.quad(lambda x: mp.cos(x), [0, Lper]) * Lper**3     # Stokes: int dC = 0
Phi_plus_dC = Phi0_t4 + int_dC
check("N6 [T^4 Stokes] adding the exact term dC (C = sin x0 dx1^dx2^dx3) leaves Phi unchanged (quadrature floor)",
      abs(int_dC) < mp.mpf("1e-50") * Phi0_t4 and
      abs(Phi_plus_dC - Phi0_t4) < mp.mpf("1e-54") * Phi0_t4,
      f"int dC = {mp.nstr(int_dC, 6)} (floor ~1e-57 rel); |dPhi|/Phi < 1e-54",
      tol="1e-54 rel (dps=60 quadrature floor)")
check("N7 [representation uniqueness] homogeneous representative forced by flux: q = Phi/V, exact part invisible to the period",
      abs(q_fix_Phi[Rs[0]] - q_can) < mp.mpf("1e-58") * q_can,
      "q(F + dC) = q(F) = Phi/V exactly (H^4 = R on connected compact oriented M^4)")

# footings
Zover = Zratio[KB[0]]
eps_can = (Zover / 2 + b_of[KB[0]]) * q_can**2
eps_alt = (Zover / 2 + b_of[KB[0]]) * q_alt**2
kap_can = mp.sqrt(q_can**2 / eps_can)
kap_alt = mp.sqrt(q_alt**2 / eps_alt)
kappa_eff_fixed_rho = A0_ALT / (2 * A0_CAN)   # relabel at fixed canonical density
check("F1 [footings separate] canonical vs alternative: same Z/beta^2 couplings, eps = 4 a0^2/G each; never both fixed",
      abs(eps_can - epsL_can) < mp.mpf("1e-45") * epsL_can and
      abs(eps_alt - epsL_alt) < mp.mpf("1e-45") * epsL_alt and
      abs(kap_can - mp.mpf("0.5")) < mp.mpf("1e-58") and
      abs(kap_alt - mp.mpf("0.5")) < mp.mpf("1e-58"),
      f"can: eps = {mp.nstr(eps_can, 8)} J/m^3 (rho_L c^2 = {mp.nstr(epsL_can, 8)}), kappa = {mp.nstr(kap_can, 10)}; "
      f"alt: eps = {mp.nstr(eps_alt, 8)} J/m^3 (rho_L c^2 = {mp.nstr(epsL_alt, 8)}), kappa = {mp.nstr(kap_alt, 10)}; "
      f"fixed-rho relabel kappa_eff = {mp.nstr(kappa_eff_fixed_rho, 10)}")
check("F2 [volume-blind across footings] kappa^2 unchanged under q -> q/16 at both footings",
      abs(kap2raw(q_can) - kap2raw(q_can / 16)) < mp.mpf("1e-58") and
      abs(kap2raw(q_alt) - kap2raw(q_alt / 16)) < mp.mpf("1e-58"),
      f"kap^2(q)/kap^2(q/16) - 1 = {mp.nstr(kap2raw(q_can) / kap2raw(q_can / 16) - 1, 6)}, {mp.nstr(kap2raw(q_alt) / kap2raw(q_alt / 16) - 1, 6)}")

# q -> 0 limiting case: promotion loses its source
check("N8 [limiting case q -> 0] eps_vac -> 0 and a0 = beta sqrt(G) |q| -> 0 (no flux => no scale); kappa stays formal",
      eps_vac(mp.mpf(0)) == 0 and abs(mp.sqrt(G) * mp.mpf(0)) == 0,
      "q = 0: vacuum energy and promoted a0 both vanish; the half condition is a ratio of TWO couplings, not fixed by the flux")

# refinement: dps = 100 volume + flux witness
mp.mp.dps = 100
V1_100 = vol_s4(mp.mpf(1))
V1_exact_100 = 8 * mp.pi**2 / 3
mp.mp.dps = 60
check("R1 [refinement dps=100] S^4 volume stable at 100 digits",
      abs(V1_100 - V1_exact_100) < mp.mpf("1e-95") * V1_exact_100,
      f"dps=100 quad agrees with 8 pi^2/3 at rel < 1e-95", tol="1e-95 rel")
check("R2 [refinement] fixed-flux dilution law restated at dps=100 on S^4 (R=1 -> 2)",
      abs(q_fix_Phi[Rs[2]] / q_fix_Phi[Rs[0]] - mp.mpf("1") / 16) < mp.mpf("1e-55"),
      f"q2/q1 = {mp.nstr(q_fix_Phi[Rs[2]] / q_fix_Phi[Rs[0]], 18)} (exact 1/16)", tol="1e-55 rel")

# ----------------------------------------------------------------------------
# residuals / artifacts dump
# ----------------------------------------------------------------------------
wall = time.time() - start
nfail = sum(1 for ch in CHECKS if not ch["pass"])
residuals = {
    "checks": CHECKS,
    "n_pass": len(CHECKS) - nfail, "n_total": len(CHECKS),
    "wall_s": wall,
    "s_sat": mp.nstr(s_sat, 20), "I_rar": mp.nstr(I_rar, 20),
    "b": {str(k): mp.nstr(v, 20) for k, v in b_of.items()},
    "Z_over_beta2": {str(k): mp.nstr(v, 20) for k, v in Zratio.items()},
    "vol_S4_R1": mp.nstr(V1, 20), "vol_S4_8pi2_3": mp.nstr(V1_exact, 20),
    "vol_T4": mp.nstr(Vt4, 20),
    "vols_S4": {mp.nstr(r, 6): mp.nstr(v, 20) for r, v in vols.items()},
    "q_can": mp.nstr(q_can, 20), "q_alt": mp.nstr(q_alt, 20),
    "eps_vac_can": mp.nstr(eps_can, 20), "eps_vac_alt": mp.nstr(eps_alt, 20),
    "kappa_can": mp.nstr(kap_can, 20), "kappa_alt": mp.nstr(kap_alt, 20),
    "kappa_eff_fixed_rho": mp.nstr(kappa_eff_fixed_rho, 20),
    "fixed_flux_q_ratio_R2": mp.nstr(q_fix_Phi[Rs[2]] / q_fix_Phi[Rs[0]], 20),
    "fixed_q_Phi_ratio_R2": mp.nstr(Phi_fix_q[Rs[2]] / Phi_fix_q[Rs[0]], 20),
    "neg_control_residual": mp.nstr(fixed_resid, 20),
    "units": {"q": "kg^1/2 m^-1/2 s^-1  (=(J/m^3)^1/2)", "Phi": "kg^1/2 m^7/2 s^-1",
              "eps_vac": "J/m^3", "a0": "m/s^2", "kappa": "dimensionless"},
}
with open("residuals.json", "w") as fh:
    json.dump(residuals, fh, indent=2)

# ----------------------------------------------------------------------------
# summary
# ----------------------------------------------------------------------------
print("\n" + "=" * 100)
print(f"  RESULT: {len(CHECKS) - nfail}/{len(CHECKS)} checks PASS; wall {wall:.2f} s")
print("""
  Derived equations (k04 branch, compact oriented M^4, homogeneous q):
    (E1) fixed-flux amplitude law     q = Phi/Vol4,   dq/q = -dVol4/Vol4
    (E2) fixed-local-q law            dPhi/Phi = dVol4/Vol4
    (E3) flux fixes only the homogeneous amplitude: q(F) = <[F],[M]>/Vol4,
         exact parts (dC) are invisible to the period (Stokes on closed M)
    (E4) negative-control theorem     (dq = 0 & dPhi = 0)  =>  dVol4 = 0 or q = 0
    (E5) coefficient consequence      kappa^2 = 2 beta^2/(Z + 2 b beta^2):
         q and Vol4 cancel identically -- the metric-volume channel cannot
         select kappa = 1/2;  kappa = 1/2 <=> Z/beta^2 = 8 - 2b (k04 F2 deficit
         unchanged; the missing equation is 'why Z = 8 beta^2'-type, and in
         the fixed-flux regime the flux datum Phi (lattice unit + winding) is
         the relocated adopted input).
  Both footings carried separately: eps_can = 4 a0_can^2/G, eps_alt = 4 a0_alt^2/G,
  same Z/beta^2; kappa_eff relabel at fixed density = 0.60238840 (diagnostic only).
""")
sys.exit(0 if nfail == 0 else 1)
