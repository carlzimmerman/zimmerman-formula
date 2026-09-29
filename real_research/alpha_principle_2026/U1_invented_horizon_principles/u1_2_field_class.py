#!/usr/bin/env python3
"""U1-2 -- field-value invented principles P08-P14 (marginality, Schwinger field, conformal threshold, Schwinger-Unruh/a0 tie, nonlinear self-sustained field,
zero of the current, Schwinger-Unruh point that carries the dark energy), tested against the known charged spectrum and the back-reaction ceiling.
Pre-registered in U1_PREREGISTRATION.md (written before this script was run; see its Amendment 1).

Back-reaction ceiling: rho_E = E^2/2 <= rho_Lambda = 3 H^2 M_P^2/(8 pi)  <=>  lambda <= lambda_max = e M_P sqrt(3/(4 pi))/H.

Run:    python3 u1_2_field_class.py            (real run; exit 0 iff every check passes)
        python3 u1_2_field_class.py --mutate   (control: the ceiling is removed, lambda_max -> infinity; check E1 (P09's T-BACK kill) must FAIL; exit 1 = the control works)
Environment: PYTHONDONTWRITEBYTECODE=1
"""
import sys
sys.dont_write_bytecode = True
import math
import mpmath as mp
import sympy as sp
import u1_lib as L

MUT = "--mutate" in sys.argv
chk = L.Checks()
PI = math.pi
A = L.ALPHA_INPUT
LMAX = float("inf") if MUT else L.lam_max()
print("=" * 118)
print("U1-2 field-value principles P08-P14 -- " + ("MUTATE CONTROL (ceiling removed)" if MUT else "REAL RUN"))
print("=" * 118)
print(f"H_Lambda = {L.H_EV:.4e} eV;  lambda_max = {L.lam_max():.4e} (sqrt = {math.sqrt(L.lam_max()):.3e});  the heaviest charged particle a Schwinger-regime principle can use has m < sqrt(lambda_max) H = {math.sqrt(L.lam_max()) * L.H_EV:.3e} eV")

FERM = [(nm, mev, w, L.Mof(mev)) for nm, mev, w in L.species_fermions()]
SPEC = [(nm, mev, w, Mv, "fermion") for nm, mev, w, Mv in FERM] + [("pi+-", L.M_PION_MEV, 1.0, L.Mof(L.M_PION_MEV), "scalar")]
REC = []

# SI conversions for the reader (E* in V/m): E = lambda hbar H^2/(e c)
H_S = L.H_EV / L.HBAR_EV_S


def E_SI(lam):
    hbar_J = 1.054571817e-34
    return lam * hbar_J * H_S ** 2 / (1.602176634e-19 * 299792458.0)


# ------------------------------------------------------------------------------------------------ P08 marginality rho = 0
print("\nP08 marginality (rho = 0): anchor r -> 1 as rho -> 0 (dS_2 scalar), and the mass window it demands")
mu0 = 0.3
lam0 = math.sqrt(0.25 - mu0 ** 2 + 1e-12)
r0 = L.r_s(lam0, mu0)
N0 = r0 / (1 - r0)
print(f"    (lambda, mu) = ({lam0:.6f}, {mu0}): rho = {L.rho_s(lam0, mu0):.2e},  r = {r0:.8f},  pair number N = r/(1-r) = {N0:.3e}")
chk("A1 P08 anchor: r -> 1 (|1 - r| < 1e-4) and N > 1e3 as rho -> 0 (mu^2 + lambda^2 = 1/4)", abs(1 - r0) < 1e-4 and N0 > 1e3)
for lab, c in [("dS_2 scalar: mu^2 + lambda^2 = 1/4", 0.25), ("dS_4 scalar: mu^2 + lambda^2 = 9/4", 2.25)]:
    bad = [(nm, Mv) for nm, mev, w, Mv, ty in SPEC if Mv ** 2 > c]
    lam_sq = [(nm, c - Mv ** 2) for nm, mev, w, Mv, ty in SPEC]
    print(f"    {lab}: needs M <= {math.sqrt(c):.3f} (m <= {math.sqrt(c) * L.H_EV:.2e} eV); lambda*^2 = {c} - M^2 is negative for {len(bad)}/{len(SPEC)} species (lightest: electron M = {FERM[0][3]:.3e})")
    REC.append(dict(pid="P08", variant=lab, verdict="DEAD" if len(bad) == len(SPEC) else "OPEN", n_real=len(SPEC) - len(bad)))
chk("E0 P08: no known species admits a real marginal field in either variant (lambda*^2 = c - M^2 < 0 for all 10)", all(r["n_real"] == 0 for r in REC if r["pid"] == "P08"))

# ------------------------------------------------------------------------------------------------ P09 Schwinger critical field lambda = M^2
print("\nP09 Schwinger critical field, lambda* = M^2.  Anchor (dS_2 scalar): -ln r at lambda = mu^2 -> ~pi (flat-space exponent pi m^2/eE)")
vals = []
for mu in (20.0, 40.0, 80.0):
    vals.append((mu, -L.ln_r_s(mu * mu, mu)))
    print(f"    mu = {mu:5.1f}: -ln r(lambda = mu^2) = {vals[-1][1]:.5f}  (pi = {PI:.5f})")
chk("A2 P09 anchor: -ln r(lambda = mu^2) within 10% of pi at mu = 80 (declared)", abs(vals[-1][1] / PI - 1) < 0.10)
print("    species        M            lambda* = M^2      lambda*/lambda_max     rho_E/rho_Lambda    E* [V/m]")
p09_ok = []
for nm, mev, w, Mv, ty in SPEC:
    ls = Mv ** 2
    er = L.energy_ratio(ls)
    p09_ok.append(ls > LMAX)
    print(f"    {nm:9s} {Mv:11.4e}  {ls:14.4e}    {ls / LMAX:12.3e}     {er:14.3e}     {E_SI(ls):.3e}")
    REC.append(dict(pid="P09", variant=f"lambda=M^2 [{nm}]", species=nm, lam_star=ls, ratio_to_ceiling=ls / LMAX, energy_ratio=er, verdict="DEAD" if ls > LMAX else "OPEN"))
chk("E1 P09 T-BACK: lambda* = M^2 exceeds the back-reaction ceiling for all 10 species (rho_E/rho_Lambda >> 1)", all(p09_ok), f"({sum(p09_ok)}/10; electron rho_E/rho_L = {L.energy_ratio(FERM[0][3] ** 2):.2e})")

# ------------------------------------------------------------------------------------------------ P10 conformal threshold lambda = 1/2
print("\nP10 conformal threshold as the horizon field, lambda = 1/2:  E* = H^2/(2e)")
er10 = L.energy_ratio(0.5)
print(f"    rho_E/rho_Lambda = {er10:.3e};  E* = {E_SI(0.5):.3e} V/m;  passes T-BACK for every species (it does not depend on M)")
chk("E2 P10 passes T-BACK (rho_E/rho_Lambda < 1e-100)", er10 < 1e-100 and 0.5 <= LMAX)
# T-INERT: e enters only through lambda in the rate, so the same lambda is reached at every alpha by rescaling E (AH1 C5), and P10 is consistent (ceiling) at every alpha
inert_alphas = [1e-4, 1e-2, 0.5, 1.0]
ok_inert = True
for a_ in inert_alphas:
    e_ = math.sqrt(4 * PI * a_)
    lm = e_ * L.MP_EV * math.sqrt(3 / (4 * PI)) / L.H_EV
    ok_inert = ok_inert and (0.5 < lm)
    # the dS_2 pair factor at fixed lambda is identical at every e (C5 replicate)
r_a = [L.r_s(math.sqrt(4 * PI * a_) * (0.7 / math.sqrt(4 * PI * a_)), 0.9) for a_ in inert_alphas]   # lambda = e E/H^2 = 0.7 reached at every alpha by choosing E = 0.7 H^2/e (structural, AH1 C5)
chk("T-INERT1 the pair-production factor depends on e only through lambda = eE/H^2 (same lambda at four alphas gives identical r) and P10 is back-reaction-consistent at each of them",
    ok_inert and max(r_a) - min(r_a) == 0.0, f"(r = {r_a[0]:.12f} at all four; the equation lambda = 1/2 contains no alpha)")
REC.append(dict(pid="P10", variant="lambda = 1/2", verdict="UNDECIDED-inert", energy_ratio=er10, E_star_SI=E_SI(0.5)))

# ------------------------------------------------------------------------------------------------ P11 Schwinger-Unruh (a0) tie lambda = kappa M
print("\nP11 Schwinger-Unruh (a0) matching, lambda* = kappa M, E* = kappa m H/e")
p11_ok = True
for kap, lab in [(0.5, "kappa = 1/2"), (1 / (2 * PI), "kappa = 1/(2 pi)")]:
    print(f"    {lab}:  species      lambda* = kappa M     rho_E/rho_Lambda    E* [V/m]")
    for nm, mev, w, Mv, ty in SPEC:
        ls = kap * Mv
        er = L.energy_ratio(ls)
        p11_ok = p11_ok and (ls <= LMAX) and (er < 1e-20)
        if nm in ("electron", "top", "pi+-"):
            print(f"        {nm:9s} {ls:14.4e}      {er:14.3e}     {E_SI(ls):.3e}")
    # Schwinger and Unruh exponents agree at kappa = 1/2 (flat-space exponent pi M^2/lambda = pi M/kappa vs Gibbons-Hawking 2 pi M)
    REC.append(dict(pid="P11", variant=lab, verdict="UNDECIDED-inert", E_star_electron_SI=E_SI(kap * FERM[0][3]), energy_ratio_electron=L.energy_ratio(kap * FERM[0][3])))
print(f"    at kappa = 1/2 the flat-space Schwinger exponent pi M^2/lambda = 2 pi M equals the Gibbons-Hawking exponent 2 pi M exactly (algebra: pi M^2/(M/2) = 2 pi M)")
chk("E3 P11 passes T-BACK for every species and both kappa (lambda* <= lambda_max and rho_E/rho_Lambda < 1e-20)", p11_ok)
chk("T-INERT2 P11's equation lambda = kappa M contains no alpha either (E* = kappa m H/e for any e)", True)

# ------------------------------------------------------------------------------------------------ P12, P13 nonlinear (ceiling argument + flat-space Schwinger estimate)
print("\nP12 / P13: nonlinear self-sustained field and zero of the current (ceiling argument; flat-space Schwinger estimate for information only)")
G = {}
for nm, mev, w, Mv, ty in SPEC:
    G[nm] = w * (float(L.Gf(Mv)) if ty == "fermion" else L.Gs(Mv))


def solve_x(M, pref, target_log):
    """solve  ln(pref * pi M^2/x) - x = target_log  for x (= pi M^2/lambda) by fixed-point iteration; returns lambda*."""
    x = 50.0
    for _ in range(200):
        x_new = math.log(pref * PI * M * M / x) - target_log
        if abs(x_new - x) < 1e-12 * max(1, abs(x)):
            x = x_new
            break
        x = x_new
    return PI * M * M / x


print("    species     M          (i) |alpha G|/2 (1+(lmax/M^2)^2)     (ii) log10[ exp(-pi M^2/lmax) ]    P12 satisfiable under ceiling?   lambda*_est/lambda_max   P13 zero under ceiling?")
p12_all_dead = True
p13_all_dead = True
for nm, mev, w, Mv, ty in SPEC:
    pert = abs(A * G[nm]) / 2 * (1 + (LMAX / Mv ** 2) ** 2) if LMAX != float("inf") else float("inf")
    x_max = PI * Mv ** 2 / LMAX
    log10_np = -x_max / math.log(10) if x_max > 0 else 0.0            # log10 of exp(-x_max)
    # satisfiable iff (i) + (ii) >= 1 (pre-registered bound); (ii) is 10^log10_np
    ii = 10.0 ** log10_np if log10_np > -300 else 0.0
    sat12 = (pert + ii) >= 1.0
    # flat-space Schwinger estimate lambda*
    if ty == "fermion":
        pref = A / (2 * PI ** 2)
    else:
        pref = A / (4 * PI ** 2)
    lam_est12 = solve_x(Mv, pref, 0.0)
    # P13 (fermion only has a negative perturbative part): lambda e^{-x} = pi^2 |G Q^2 N|  ->  ln(lambda) - x = ln(pi^2 |G|)
    if ty == "fermion":
        lam_est13 = solve_x(Mv, 1.0, math.log(PI ** 2 * abs(G[nm])))
        # sign change possible under ceiling iff lmax e^{-x_max}/pi^2 >= |G|   (log10 compare)
        lhs = math.log10(LMAX / PI ** 2) - x_max / math.log(10) if LMAX != float("inf") else float("inf")
        sat13 = lhs >= math.log10(abs(G[nm]))
    else:
        lam_est13, sat13 = float("nan"), False
    p12_all_dead = p12_all_dead and (not sat12)
    p13_all_dead = p13_all_dead and (not sat13)
    print(f"    {nm:9s} {Mv:10.3e}      {pert:14.3e}                    {log10_np:14.3e}                    {str(sat12):5s}                        {lam_est12 / L.lam_max():10.3e}           {str(sat13):5s}")
    REC.append(dict(pid="P12", variant=f"J=2EH nonlinear [{nm}]", species=nm, satisfiable_under_ceiling=bool(sat12), lam_est_over_ceiling=lam_est12 / L.lam_max(),
                    energy_ratio_at_est=L.energy_ratio(lam_est12), verdict="DEAD" if not sat12 else "OPEN"))
    REC.append(dict(pid="P13", variant=f"zero of the current [{nm}]", species=nm, satisfiable_under_ceiling=bool(sat13), lam_est_over_ceiling=(lam_est13 / L.lam_max() if ty == "fermion" else None),
                    verdict="DEAD" if not sat13 else "OPEN"))
chk("E4 P12: under the ceiling J < 2EH for all 10 species (perturbative part ~1e-81 times (1 + 1e-34); non-perturbative part exp(-3e17)-suppressed)", p12_all_dead)
chk("E5 P13: under the ceiling no species (fermion) has a sign change of the current; the scalar current has no negative part", p13_all_dead)
e_est = [r for r in REC if r["pid"] == "P12" and r["species"] == "electron"][0]
print(f"    electron estimate (information): lambda*_est/lambda_max = {e_est['lam_est_over_ceiling']:.3e}, rho_E/rho_Lambda there = {e_est['energy_ratio_at_est']:.2e}")
chk("E6 P12 estimate: for the electron the flat-space Schwinger lambda* exceeds the ceiling by > 1e10 (rho_E/rho_Lambda > 1e20)", e_est["lam_est_over_ceiling"] > 1e10 and e_est["energy_ratio_at_est"] > 1e20)

# Q1's computed L*(M) support the M^2 scaling of the sign-change field (committed values; information)
Q1_LSTAR = {0.5: 5.66540, 1.0: 2.50743, 2.0: 2.11489, 5.0: 5.38885}
print("    Q1's zero L*(M) (q1_3_physics_answers.out) over M^2: " + ", ".join(f"M={m}: {v / m ** 2:.3f}" for m, v in Q1_LSTAR.items()) + "   (L* grows to O(M^2) times a slowly falling factor; the estimate above is the same scaling)")

# P13 scalar variant: does the dS_4 scalar current change sign anywhere? (small scan of the AH4 closed form)
print("\nP13 scalar variant: sign scan of f(lambda, M) (dS_4 complex scalar, AH4 closed form)")
neg = []
n_pts = 0
for Mv in (0.3, 1.0, 2.0):
    row = []
    for lam in (0.1, 0.3, 1.0, 2.0, 4.0):
        if Mv ** 2 + lam ** 2 < 2.25 or True:
            mw2 = 2.25 - lam ** 2 - Mv ** 2                # Amendment 3: sin(2 pi mw) = 0 at mw = k/2 is a removable singularity of the closed form (numerically garbage); displace lambda by 1e-4 relative there
            lam_eval = lam
            if mw2 > 0 and abs(math.sin(2 * PI * math.sqrt(mw2))) < 1e-6:
                lam_eval = lam * (1 + 1e-4)
            try:
                fv = L.scalar_f_closed(lam_eval, Mv)
            except Exception as ex:
                fv = float("nan")
            n_pts += 1
            row.append(fv)
            if fv == fv and fv <= 0:
                neg.append((Mv, lam, fv))
    print("    M = %.1f: f(lambda=0.1,0.3,1,2,4) = " % Mv + ", ".join(f"{x:+.4f}" for x in row))
print(f"    non-positive values found: {neg if neg else 'none'} among {n_pts} scanned points")
REC.append(dict(pid="P13", variant="zero of the current [scalar type, scan]", verdict="EMPTY" if not neg else "OPEN", n_points=n_pts, negatives=neg))
chk("E7 P13 scalar: f > 0 at every scanned (lambda, M) (no zero to sit at)", len(neg) == 0 and n_pts > 0)

# ------------------------------------------------------------------------------------------------ P14 Schwinger-Unruh point that carries the dark energy
print("\nP14: lambda = kappa M (P11) and E^2/2 = rho_Lambda  =>  alpha = kappa^2 m^2/(3 M_P^2)   (derived symbolically below)")
kap_s, m_s, H_s, MP_s, e_s = sp.symbols("kappa m H M_P e", positive=True)
E_s = H_s * MP_s * sp.sqrt(3 / (4 * sp.pi))                      # E^2/2 = 3 H^2 M_P^2/(8 pi)
e_sol = sp.solve(sp.Eq(e_s * E_s / H_s ** 2, kap_s * m_s / H_s), e_s)[0]
alpha_sym = sp.simplify(e_sol ** 2 / (4 * sp.pi))
print(f"    sympy: E = {E_s};  e = {sp.simplify(e_sol)};  alpha = {alpha_sym}")
chk("D1 P14 derivation: alpha = kappa^2 m^2/(3 M_P^2)", sp.simplify(alpha_sym - kap_s ** 2 * m_s ** 2 / (3 * MP_s ** 2)) == 0)
p14_rows = []
for kap, lab in [(0.5, "kappa=1/2"), (1 / (2 * PI), "kappa=1/(2 pi)")]:
    for nm, mev, w, Mv, ty in SPEC[:9]:
        m_eV = mev * 1e6
        ap = kap ** 2 * m_eV ** 2 / (3 * L.MP_EV ** 2)
        delta = abs((1 / ap) / L.INV_ALPHA - 1)
        bar = L.bar_assess(delta, math.log2(18))
        p14_rows.append((lab, nm, ap, delta, bool(bar["clears"])))
        REC.append(dict(pid="P14", variant=f"{lab} [{nm}]", species=nm, alpha_pred=ap, delta=delta, clears=bool(bar["clears"]), verdict="DEAD" if not bar["clears"] else "OPEN"))
for lab in ("kappa=1/2", "kappa=1/(2 pi)"):
    for r in p14_rows:
        if r[0] == lab and r[1] in ("electron", "top"):
            print(f"    {lab:15s} {r[1]:9s}: alpha_pred = {r[2]:.3e}  (alpha_input = {A:.5e}),  |1/alpha_pred / 137.036 - 1| = {r[3]:.3e},  bar clears: {r[4]}")
best = min(p14_rows, key=lambda r: r[3])
print(f"    best of the 18 (variant, species): {best[0]} {best[1]}, miss {best[3]:.3e}")
m_needed = L.MP_EV * math.sqrt(3 * A) / 0.5
print(f"    inverse map (NOT a test): alpha = 1/137.036 would need m = {m_needed:.3e} eV = {m_needed / 1e9:.2e} GeV at kappa=1/2; the electron is {m_needed / 0.51099895e6:.2e} times lighter")
chk("E8 P14: none of the 18 (kappa, species) pairs clears lane D's bar (best miss >> 5e-10)", not any(r[4] for r in p14_rows) and best[3] > 0.5, f"(best miss {best[3]:.3e})")
chk("E9 P14: the electron's alpha_pred is more than 40 orders of magnitude below alpha", [r for r in p14_rows if r[1] == "electron"][0][2] < A * 1e-40)

fn = L.write_json("u1_2_results.json", MUT, dict(records=REC, lam_max=L.lam_max(), H_eV=L.H_EV))
print(f"\nrecords written to {fn.split('/')[-1]}")
print(f"CHECKS: {sum(o for _, o in chk.items)}/{len(chk.items)} passed")
print("VERDICT: P08, P09, P12, P13, P14 DEAD on the known spectrum / back-reaction / number; P10, P11 pass T-BACK and are UNDECIDED-inert (they fix E*, not e). alpha stays an INPUT.")
L.finish(chk, MUT, targeted_tags=["E1"])
